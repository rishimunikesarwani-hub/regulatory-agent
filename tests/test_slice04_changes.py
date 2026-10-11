"""VS4 HTTP acceptance: fixed simulations, version changes, ownership, and durable reviews."""
from unittest.mock import patch

from regulatory_agent.contracts import ContractError
import test_slice03_assessment as assessment_flow

import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier


class ChangeSliceTests(unittest.TestCase):
    def setUp(self):
        self.flow = assessment_flow.AssessmentSliceTests('runTest')
        self.flow.setUp()
        self.call = self.flow.call
        self.url = f'/api/cases/{self.flow.case}/comparisons'
        self.selection = self.flow.selection | {'selected_versions': {
            self.flow.policy['document']['source_id']: '1', 'SIM-ACCESS': 'v1'},
            'selected_obligations': ['SIM-ACCESS-1'], 'assessment_date': '2024-05-08'}

    def tearDown(self):
        self.flow.tearDown()

    def baseline(self):
        response = self.call('POST', self.flow.url, json=self.selection)
        self.assertEqual(response.status_code, 202, response.text)
        started = response.json()
        return started, self.flow.result(started)

    def compare(self, baseline, newer='v2-added', key='change-1', **changes):
        body = {'older_version_id': 'SIM-ACCESS:v1', 'newer_version_id': f'SIM-ACCESS:{newer}',
                'snapshot_id': baseline['snapshot']['snapshot_id'], 'idempotency_key': key} | changes
        return self.call('POST', self.url, json=body)

    def changed(self):
        started, baseline = self.baseline()
        response = self.compare(baseline)
        self.assertEqual(response.status_code, 202, response.text)
        comparison = response.json()
        return started, baseline, comparison, self.flow.result({'job_id': comparison['new_job_id']})

    def test_ct01_simulated_baseline_has_exact_source_and_saved_review(self):
        started, baseline = self.baseline()
        self.assertEqual(baseline['job']['state'], 'completed')
        self.assertEqual(baseline['obligation']['requirement'], 'Privileged sessions must be logged and reviewed each week.')
        self.assertEqual(baseline['obligation']['exceptions'], [])
        finding = baseline['findings'][0]
        source = self.call('GET', f"{self.flow.url}/{started['job_id']}/sources/SIM-ACCESS:v1").json()
        self.assertTrue(source['document']['synthetic'])
        self.assertIn('simulation', source['label'].lower())
        self.assertEqual(self.flow.review(started, finding).status_code, 201)
        self.assertEqual(self.flow.result(started)['summary']['approved'], 1)

    def test_ct02_added_requirement_has_new_snapshot_and_both_version_passages(self):
        started, baseline, comparison, result = self.changed()
        self.assertEqual(comparison['change_kind'], 'added_requirement')
        self.assertEqual(comparison['affected_control_ids'], ['ACCESS-01'])
        self.assertTrue(comparison['obligation_changed'])
        self.assertNotEqual(result['snapshot']['snapshot_id'], baseline['snapshot']['snapshot_id'])
        self.assertEqual(result['snapshot']['selected_versions']['SIM-ACCESS'], 'v2-added')
        self.assertIn('separate reviewer', comparison['newer_source']['passages'][0]['text'])
        self.assertEqual(comparison['older_source']['passages'][0]['text'], baseline['obligation']['requirement'])
        self.assertIn('separate', result['findings'][0]['primary_recommendation'].lower())
        self.assertEqual(result['findings'][0]['status'], 'needs_review')
        self.assertEqual(result['findings'][0]['gap_kind'], 'evidence')

    def test_ct03_new_review_cannot_copy_or_change_earlier_review(self):
        started, baseline = self.baseline()
        self.assertEqual(self.flow.review(started, baseline['findings'][0]).status_code, 201)
        before = self.flow.result(started)
        comparison = self.compare(before).json()
        new = {'job_id': comparison['new_job_id']}
        result = self.flow.result(new)
        self.assertEqual(result['reviews'], [])
        self.assertEqual(result['summary']['pending'], 1)
        self.assertNotEqual(result['findings'][0]['finding_id'], baseline['findings'][0]['finding_id'])
        self.assertEqual(self.flow.review(new, result['findings'][0], 'rejected', reason='Approval evidence is missing.').status_code, 201)
        after = self.flow.result(started)
        for field in ('snapshot', 'findings', 'reviews'):
            self.assertEqual(after[field], before[field])
        self.assertEqual(after['summary']['approved'], 1)
        self.assertEqual(self.flow.result(new)['summary']['rejected'], 1)

    def test_ct04_wording_and_appearance_do_not_create_jobs(self):
        _, baseline = self.baseline()
        for version, kind in [('v2-cosmetic', 'appearance_only'), ('v2-replaced', 'wording_only')]:
            with self.subTest(version=version):
                response = self.compare(baseline, version, version)
                self.assertEqual(response.status_code, 202, response.text)
                result = response.json()
                self.assertEqual(result['change_kind'], kind)
                self.assertFalse(result['obligation_changed'])
                self.assertEqual(result['affected_control_ids'], [])
                self.assertIsNone(result['new_job_id'])
                self.assertTrue(result['metadata_changes'])
        self.assertEqual(len(self.call('GET', self.flow.url).json()['runs']), 1)

    def test_ct05_retries_and_restart_keep_identity_and_reject_key_conflicts(self):
        _, baseline, saved, result = self.changed()
        self.assertEqual(self.compare(baseline).json(), saved)
        app = self.flow.application('operator-a')
        persisted = self.call('GET', f"{self.url}/{saved['comparison_id']}", app=app)
        self.assertEqual(persisted.json(), saved)
        self.assertEqual(self.compare(baseline, 'v2-cosmetic').status_code, 409)
        self.assertEqual(len(self.call('GET', self.url, app=app).json()['comparisons']), 1)
        self.assertEqual(len(self.call('GET', self.flow.url).json()['runs']), 2)

    def test_ct06_owner_and_snapshot_scope_are_mandatory(self):
        _, baseline, comparison, result = self.changed()
        app = self.flow.application('operator-b')
        for method, url, kwargs in [('GET', self.url, {}), ('GET', f"{self.url}/{comparison['comparison_id']}", {}),
                ('POST', self.url, {'json': {'older_version_id': 'SIM-ACCESS:v1', 'newer_version_id': 'SIM-ACCESS:v2-added',
                    'snapshot_id': baseline['snapshot']['snapshot_id'], 'idempotency_key': 'other'}}),
                ('GET', f"{self.flow.url}/{comparison['new_job_id']}", {})]:
            self.assertEqual(self.call(method, url, app=app, **kwargs).status_code, 404)
        self.assertEqual(self.flow.review({'job_id': comparison['new_job_id']}, baseline['findings'][0]).status_code, 404)

    def test_ct07_invalid_pairs_and_snapshots_are_rejected(self):
        _, baseline = self.baseline()
        for older, newer, snapshot in [('SIM-ACCESS:v1', 'SIM-ACCESS:v1', baseline['snapshot']['snapshot_id']),
                ('SIM-ACCESS:v2-added', 'SIM-ACCESS:v1', baseline['snapshot']['snapshot_id']),
                ('SIM-ACCESS:v1', 'RBI-IT-2023:2023-11-07', baseline['snapshot']['snapshot_id']),
                ('SIM-ACCESS:v1', 'SIM-ACCESS:unknown', baseline['snapshot']['snapshot_id']),
                ('SIM-ACCESS:v1', 'SIM-ACCESS:v2-added', 'unknown-snapshot')]:
            response = self.compare(baseline, key='invalid', older_version_id=older, newer_version_id=newer, snapshot_id=snapshot)
            self.assertIn(response.status_code, (404, 422), response.text)
        original = self.flow.start(idempotency_key='rbi-example')
        self.assertEqual(self.compare(self.flow.result(original), key='rbi-context').status_code, 422)
        with patch('fastapi.BackgroundTasks.add_task'):
            queued = self.call('POST', self.flow.url, json=self.selection | {'idempotency_key': 'queued'}).json()
        unfinished = self.flow.result(queued)
        self.assertEqual(self.compare(unfinished, key='queued-comparison').status_code, 409)

    def test_ct08_current_and_aws_modes_cannot_run_simulations(self):
        response = self.call('POST', self.flow.url, json=self.selection | {'mode': 'current'})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()['code'], 'freshness_unverified')
        from regulatory_agent.api import create_app
        app = create_app(store=self.flow.path, environment='aws')
        with patch('regulatory_agent.api.LocalIdentity.resolve', return_value=object()), \
                patch('regulatory_agent.api.authenticated_owner', return_value='operator-a'):
            self.assertEqual(self.call('GET', self.url, app=app).status_code, 404)

    def test_ct09_policy_replacement_cannot_change_either_snapshot(self):
        started, baseline, comparison, result = self.changed()
        self.flow.upload(data=b'Synthetic policy\nControl ACCESS-01 has different wording.\n', source=self.flow.policy['document']['source_id'])
        self.assertEqual(self.flow.result(started)['snapshot'], baseline['snapshot'])
        self.assertEqual(self.flow.result({'job_id': comparison['new_job_id']})['findings'], result['findings'])
        source = self.call('GET', f"{self.flow.url}/{comparison['new_job_id']}/sources/{self.flow.policy['document']['document_version_id']}").json()
        self.assertEqual(source['document']['version'], '1')

    def test_ct10_new_job_keeps_budget_and_citations_and_resume_is_idempotent(self):
        _, _, comparison, result = self.changed()
        self.assertEqual(result['job']['model_calls'], 1)
        self.assertEqual(result['job']['deadline'] - result['job']['started_at'], 600)
        stages = {attempt['stage'] for attempt in result['trace']['attempts']}
        self.assertTrue({'retrieval', 'model_call', 'validation', 'persistence'} <= stages)
        for attempt in result['trace']['attempts']:
            self.assertEqual(attempt['versions']['prompt'], result['snapshot']['prompt_version'])
            self.assertEqual(attempt['versions']['application'], 'vs4-v1')
        for citation in result['findings'][0]['citations']:
            source = self.call('GET', f"{self.flow.url}/{comparison['new_job_id']}/sources/{citation['document_version_id']}").json()
            self.assertTrue(any(p['location'] == citation['location'] and citation['quote'] in p['text'] for p in source['passages']))
        self.call('POST', f"{self.flow.url}/{comparison['new_job_id']}/resume")
        again = self.flow.result({'job_id': comparison['new_job_id']})
        self.assertEqual(again['job']['model_calls'], 1)
        self.assertEqual(again['findings'], result['findings'])

    def test_ct11_interrupted_comparison_save_recovers_without_duplicate_assessment(self):
        _, baseline = self.baseline()
        from regulatory_agent.reviews import Reviews
        original = Reviews._insert
        def interrupted(db, case, kind, identity, body):
            if kind == 'comparison':
                raise ContractError('interrupted_comparison')
            return original(db, case, kind, identity, body)
        with patch.object(Reviews, '_insert', side_effect=interrupted):
            response = self.compare(baseline)
        self.assertEqual(response.status_code, 503)
        saved = self.compare(baseline)
        self.assertEqual(saved.status_code, 202, saved.text)
        self.assertEqual(len(self.call('GET', self.flow.url).json()['runs']), 2)
        self.assertEqual(self.flow.result({'job_id': saved.json()['new_job_id']})['job']['model_calls'], 1)

    def test_ct12_simultaneous_retries_keep_one_admission_and_one_model_call(self):
        _, baseline = self.baseline()
        from regulatory_agent.reviews import Reviews
        original = Reviews.admit
        barrier = Barrier(2)
        def synchronized(service, *args, **kwargs):
            barrier.wait(timeout=5)
            return original(service, *args, **kwargs)
        with patch.object(Reviews, 'admit', new=synchronized), ThreadPoolExecutor(max_workers=2) as workers:
            responses = list(workers.map(lambda _: self.compare(baseline), range(2)))
        self.assertEqual([r.status_code for r in responses], [202, 202], [r.text for r in responses])
        self.assertEqual(responses[0].json(), responses[1].json())
        self.assertEqual(len(self.call('GET', self.flow.url).json()['runs']), 2)
        result = self.flow.result({'job_id': responses[0].json()['new_job_id']})
        self.assertEqual(result['job']['model_calls'], 1)

    def test_ct13_completed_response_cannot_omit_its_committed_finding(self):
        from regulatory_agent.local import Store
        with patch('fastapi.BackgroundTasks.add_task'):
            queued = self.call('POST', self.flow.url, json=self.selection).json()
        original = Store.read_job
        finished = False
        def finish_during_read(store, owner, case, job):
            nonlocal finished
            if not finished:
                finished = True
                response = self.call('POST', f"{self.flow.url}/{queued['job_id']}/resume")
                self.assertEqual(response.status_code, 202, response.text)
            return original(store, owner, case, job)
        with patch.object(Store, 'read_job', new=finish_during_read):
            result = self.flow.result(queued)
        if result['job']['state'] == 'completed':
            self.assertEqual(len(result['findings']), 1, 'Completed state must use the same committed read as its findings.')
        else:
            self.assertIn(result['job']['state'], ('queued', 'running'))
            self.call('POST', f"{self.flow.url}/{queued['job_id']}/resume")
        final = self.flow.result(queued)
        self.assertEqual(final['job']['state'], 'completed')
        self.assertEqual(len(final['findings']), 1)
        self.assertEqual(final['summary']['pending'], 1)
