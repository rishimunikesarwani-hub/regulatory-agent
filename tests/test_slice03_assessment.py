"""VS3 local HTTP flow: fixed historical simulation, source integrity, and human decisions."""
import asyncio
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import quote

import httpx

from regulatory_agent.api import create_app
from regulatory_agent.contracts import ModelReply, StageTrace
from regulatory_agent.local import ControlledModel

ROOT = Path(__file__).resolve().parents[1]
POLICY = (ROOT / 'data/fixtures/slice-02-policy.txt').read_bytes()


class AssessmentSliceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'assessments.sqlite'
        self.app = self.application('operator-a')
        self.case = self.call('POST', '/api/cases', json={'bank_profile': {'name': 'Fictional assessment bank'}}).json()['case_id']
        self.sources = f'/api/cases/{self.case}/documents'
        self.url = f'/api/cases/{self.case}/assessments'
        self.policy = self.upload().json()
        self.selection = {'selected_versions': {self.policy['document']['source_id']: '1', 'RBI-IT-2023': '2023-11-07'},
            'selected_obligations': ['RBI-IT-19b'], 'assessment_date': '2024-04-08', 'mode': 'historical', 'idempotency_key': 'request-1'}

    def tearDown(self):
        self.temp.cleanup()

    def application(self, owner):
        return create_app(store=self.path, environment='local', development_user=owner)

    def call(self, method, path, *, app=None, **kwargs):
        async def send():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app or self.app, client=('127.0.0.1', 10000)),
                    base_url='http://127.0.0.1') as client:
                return await client.request(method, path, **kwargs)
        return asyncio.run(send())

    def upload(self, data=POLICY, source=None):
        return self.call('POST', self.sources, content=data, headers={'X-Filename': 'policy.txt', 'X-Document-Kind': 'policy',
            'X-Synthetic': 'true', **({'X-Source-Id': source} if source else {})})

    def start(self, **changes):
        response = self.call('POST', self.url, json=self.selection | changes)
        self.assertEqual(response.status_code, 202, response.text)
        return response.json()

    def result(self, started):
        response = self.call('GET', f"{self.url}/{started['job_id']}")
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def review(self, started, finding, disposition='approved', revision=0, key='review-1', **changes):
        content = {'status': finding['status'], 'rationale': finding['rationale'], 'recommendation': finding['primary_recommendation']}
        request = {'event_kind': 'final_review', 'disposition': disposition, 'expected_revision': revision, 'idempotency_key': key,
                   'accepted_content': content if disposition in {'approved', 'edited'} else None} | changes
        return self.call('POST', f"{self.url}/{started['job_id']}/findings/{finding['finding_id']}/reviews", json=request)

    def test_ct01_controlled_job_binds_snapshot_and_exact_citations(self):
        started = self.start()
        result = self.result(started)
        self.assertEqual(result['job']['state'], 'completed')
        self.assertEqual(result['data_mode'], 'controlled_simulation')
        self.assertEqual(result['freshness'], 'unverified')
        self.assertEqual(result['snapshot']['selected_versions'], self.selection['selected_versions'])
        finding, = result['findings']
        self.assertEqual(finding['status'], 'needs_review')
        self.assertEqual(finding['control_ids'], ['ACCESS-01'])
        self.assertEqual(finding['data_mode'], 'controlled_simulation')
        self.assertTrue(result['obligation']['conditions'])
        self.assertTrue(result['obligation']['exceptions'])
        self.assertIn('unverified', result['obligation']['applicability'].lower())
        for citation in finding['citations']:
            source = self.call('GET', f"{self.url}/{started['job_id']}/sources/{citation['document_version_id']}")
            self.assertEqual(source.status_code, 200)
            self.assertTrue(any(p['passage_id'] == citation['passage_id'] and p['location'] == citation['location']
                and citation['quote'] in p['text'] for p in source.json()['passages']))

    def test_ct02_owner_and_case_checks_cover_every_assessment_operation(self):
        started = self.start()
        finding = self.result(started)['findings'][0]
        other = self.application('operator-b')
        paths = [(self.url, 'GET'), (self.url, 'POST'), (f"{self.url}/{started['job_id']}", 'GET'),
            (f"{self.url}/{started['job_id']}/resume", 'POST'),
            (f"{self.url}/{started['job_id']}/sources/{finding['citations'][0]['document_version_id']}", 'GET'),
            (f"{self.url}/{started['job_id']}/findings/{finding['finding_id']}/reviews", 'POST')]
        for path, method in paths:
            with self.subTest(path=path):
                self.assertEqual(self.call(method, path, app=other, **({'json': self.selection} if path == self.url and method == 'POST' else {})).status_code, 404)
        another = self.call('POST', '/api/cases', json={'bank_profile': {'name': 'Another fictional bank'}}).json()['case_id']
        self.assertEqual(self.call('GET', f"/api/cases/{another}/assessments/{started['job_id']}").status_code, 404)

    def test_ct03_start_is_idempotent_and_replacement_cannot_change_snapshot(self):
        started = self.start()
        original = self.result(started)
        self.assertEqual(self.start()['job_id'], started['job_id'])
        conflict = self.call('POST', self.url, json=self.selection | {'assessment_date': '2024-04-09'})
        self.assertEqual(conflict.status_code, 409)
        self.assertEqual(self.upload(b'Revised fictional policy.', self.policy['document']['source_id']).status_code, 201)
        self.assertEqual(self.result(started)['snapshot'], original['snapshot'])
        self.assertEqual(self.result(started)['findings'], original['findings'])
        self.assertEqual(len(self.call('GET', self.url).json()['runs']), 1)

    def test_ct04_current_mode_and_forged_or_unsupported_scope_are_blocked(self):
        for changed in ({'mode': 'current'}, {'selected_obligations': ['other-obligation']},
                {'selected_versions': {'forged-source': '1', 'RBI-IT-2023': '2023-11-07'}}):
            with self.subTest(changed=changed):
                response = self.call('POST', self.url, json=self.selection | changed)
                self.assertIn(response.status_code, (404, 422, 503))
        invalid = self.upload(b'An unrelated fictional policy.').json()
        selected = {invalid['document']['source_id']: '1', 'RBI-IT-2023': '2023-11-07'}
        response = self.call('POST', self.url, json=self.selection | {'selected_versions': selected})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.call('GET', self.url).json()['runs'], [])

    def test_ct05_reviews_keep_original_item_and_reject_stale_or_unchanged_edits(self):
        started = self.start()
        finding = self.result(started)['findings'][0]
        approved = self.review(started, finding)
        self.assertEqual(approved.status_code, 201, approved.text)
        self.assertEqual(approved.json()['revision'], 1)
        self.assertEqual(self.review(started, finding).json()['event_id'], approved.json()['event_id'])
        unchanged = self.review(started, finding, 'edited', 1, 'edit-bad', reason='Only a note.')
        self.assertEqual(unchanged.status_code, 422)
        changed = {'status': 'needs_review', 'rationale': 'Human review needs dated evidence.', 'recommendation': 'Request the fictional activity log.'}
        edited = self.review(started, finding, 'edited', 1, 'edit-1', accepted_content=changed, reason='The period was missing.')
        self.assertEqual(edited.status_code, 201, edited.text)
        self.assertEqual(self.review(started, finding, 'rejected', 1, 'stale', reason='Stale tab.').status_code, 409)
        rejected = self.review(started, finding, 'rejected', 2, 'reject-1', reason='Evidence has not been examined.')
        self.assertEqual(rejected.status_code, 201)
        result = self.result(started)
        self.assertEqual(result['findings'][0], finding)
        self.assertEqual(len(result['reviews']), 3)
        self.assertEqual(result['summary']['rejected'], 1)
        self.assertEqual(result['summary']['eligible'], 1)

    def test_ct06_evidence_requests_and_cutoffs_preserve_final_outcomes(self):
        started = self.start()
        finding = self.result(started)['findings'][0]
        summary = self.result(started)['summary']
        self.assertEqual(summary['pending'], 1)
        self.assertIsNone(summary['approval_rate'])
        route = f"{self.url}/{started['job_id']}/findings/{finding['finding_id']}/reviews"
        request = {'event_kind': 'evidence_request', 'expected_revision': 0, 'idempotency_key': 'evidence-1', 'reason': 'Supply dated fictional logs.'}
        self.assertEqual(self.call('POST', route, json=request).status_code, 201)
        self.assertEqual(self.result(started)['summary']['pending'], 1)
        approval = self.review(started, finding, revision=1, key='approval-after-request').json()
        self.assertEqual(self.call('POST', route, json=request | {'expected_revision': 2, 'idempotency_key': 'evidence-2'}).status_code, 201)
        self.assertEqual(self.result(started)['summary']['approved'], 1)
        self.review(started, finding, 'rejected', 3, 'later-rejection', reason='Later review.')
        cutoff = quote(approval['committed_at'])
        historical = self.call('GET', f"{self.url}/{started['job_id']}?cutoff={cutoff}").json()['summary']
        self.assertEqual(historical['approved'], 1)
        self.assertEqual(historical['rejected'], 0)
        self.assertEqual(historical['metric_definition_version'], 'd24-v1')

    def test_ct07_restart_keeps_findings_source_versions_and_reviews(self):
        started = self.start()
        result = self.result(started)
        self.assertEqual(self.review(started, result['findings'][0]).status_code, 201)
        reopened = self.call('GET', f"{self.url}/{started['job_id']}", app=self.application('operator-a')).json()
        self.assertEqual(reopened['findings'], result['findings'])
        self.assertEqual(reopened['summary']['approved'], 1)
        source_id = result['findings'][0]['citations'][0]['document_version_id']
        self.assertEqual(self.call('GET', f"{self.url}/{started['job_id']}/sources/{source_id}").status_code, 200)
        self.assertEqual(self.call('GET', f"{self.url}/{started['job_id']}/sources/not-selected").status_code, 404)

    def test_ct08_trace_is_safe_and_live_measurements_are_not_invented(self):
        result = self.result(self.start())
        trace = StageTrace.model_validate_json(json.dumps(result['trace']))
        self.assertTrue({'source_verification', 'extraction', 'retrieval', 'context_selection', 'model_call', 'validation', 'persistence'} <= {a.stage for a in trace.attempts})
        self.assertEqual(result['job']['model_calls'], 1)
        self.assertEqual(result['live_model_calls'], 0)
        self.assertIsNone(result['cost_usd'])
        for attempt in trace.attempts:
            self.assertIsNone(attempt.actual_response_model_id)
            self.assertIsNone(attempt.usage.input_tokens)
        self.assertNotIn('Control ACCESS-01 requires supervision', json.dumps(result['trace']))

    def test_ct09_invalid_controlled_citation_cannot_present_a_finding(self):
        dispatch = ControlledModel.dispatch
        def forged(_adapter, *_args, **_kwargs):
            reply = dispatch(_adapter, *_args, **_kwargs).model_dump()
            reply['action']['findings'][0]['citations'][0]['quote'] = 'Fabricated private quotation.'
            return ModelReply(**reply)
        with patch('regulatory_agent.local.ControlledModel.dispatch', new=forged):
            failed = self.start(idempotency_key='invalid-citation')
        result = self.result(failed)
        self.assertEqual(result['job']['state'], 'failed')
        self.assertEqual(result['findings'], [])
        self.assertNotIn('Fabricated private quotation.', json.dumps(result['trace']))

    def test_ct10_admitted_job_resumes_after_worker_interruption(self):
        with patch('fastapi.BackgroundTasks.add_task'):
            started = self.start()
        self.assertEqual(self.result(started)['job']['state'], 'queued')
        app = self.application('operator-a')
        resumed = self.call('POST', f"{self.url}/{started['job_id']}/resume", app=app)
        self.assertEqual(resumed.status_code, 202)
        result = self.call('GET', f"{self.url}/{started['job_id']}", app=app).json()
        self.assertEqual(result['job']['state'], 'completed')
        self.assertEqual(len(result['findings']), 1)
        self.assertEqual(self.call('POST', f"{self.url}/{started['job_id']}/resume", app=app).status_code, 202)
        self.assertEqual(len(self.call('GET', self.url, app=app).json()['runs']), 1)

    def test_ct09_policy_citations_cannot_become_proof_of_completed_operation(self):
        dispatch = ControlledModel.dispatch
        def unsupported(_adapter, *_args, **_kwargs):
            reply = dispatch(_adapter, *_args, **_kwargs).model_dump()
            finding = reply['action']['findings'][0]
            finding.update(status='supported', evidence_condition='sufficient', gap_kind=None)
            return ModelReply(**reply)
        with patch('regulatory_agent.local.ControlledModel.dispatch', new=unsupported):
            started = self.start()
        result = self.result(started)
        self.assertEqual(result['job']['state'], 'failed')
        self.assertEqual(result['findings'], [])


if __name__ == '__main__':
    unittest.main()
