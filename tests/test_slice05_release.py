"""VS5 authorized exports: exact sources, historical decisions, and incomplete jobs."""
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from urllib.parse import quote

import test_slice03_assessment as assessment_flow
from regulatory_agent.local import Store, encoded
from regulatory_agent.reviews import Reviews


class ReleaseSliceTests(unittest.TestCase):
    def setUp(self):
        self.flow = assessment_flow.AssessmentSliceTests('runTest')
        self.flow.setUp()
        self.call = self.flow.call

    def tearDown(self):
        self.flow.tearDown()

    def export(self, started, format='json', cutoff=None, **kwargs):
        path = f"{self.flow.url}/{started['job_id']}/export"
        if cutoff is not None:
            path += '?cutoff=' + quote(cutoff)
        return self.call('POST', path, json={'format': format}, **kwargs)

    def report(self, started, **kwargs):
        response = self.export(started, **kwargs)
        self.assertEqual(response.status_code, 200, response.text)
        self.assertIn('attachment;', response.headers['content-disposition'])
        self.assertEqual(response.headers['cache-control'], 'no-store')
        return response.json()

    def test_ct01_json_retains_sources_snapshot_trace_and_unknown_cost(self):
        started = self.flow.start()
        result = self.flow.result(started)
        report = self.report(started, cutoff=result['summary']['cutoff'])
        self.assertEqual(report['snapshot'], result['snapshot'])
        self.assertEqual(report['state'], 'completed')
        self.assertEqual(report['job']['state'], 'completed')
        self.assertEqual(report['findings'], result['findings'])
        self.assertEqual(report['summary'], result['summary'])
        self.assertEqual(report['data_mode'], 'controlled_simulation')
        self.assertIn('Simulated', report['label'])
        self.assertIsNone(report['cost_usd'])
        self.assertEqual(report['cost_status'], 'unknown')
        self.assertIsNone(report['authority_verified_at'])
        for citation in result['findings'][0]['citations']:
            source = next(s for s in report['sources'] if s['document']['document_version_id'] == citation['document_version_id'])
            passage = next(p for p in source['passages'] if p['passage_id'] == citation['passage_id'])
            self.assertIn(citation['quote'], passage['text'])
            self.assertEqual(citation['location'], passage['location'])
        self.assertIn('https://www.rbi.org.in', '\n'.join(report['source_urls']))
        self.assertTrue(report['trace']['attempts'])
        self.assertTrue(all(t['versions']['application'] == 'vs5-v1' for t in report['trace']['attempts']))
        self.assertTrue(all(t['versions']['prompt'] == result['snapshot']['prompt_version'] for t in report['trace']['attempts']))
        self.assertNotIn('token', report['job'])
        self.assertNotIn('stages', report['job'])
        self.assertNotIn('lease_until', report['job'])
        self.assertEqual(report['cohort']['kind'], 'single_assessment')
        self.assertEqual(report['cohort']['run_id'], report['summary']['run_id'])
        self.assertEqual(report['cohort']['prompt_version'], report['snapshot']['prompt_version'])

    def test_ct02_markdown_parity_and_safe_untrusted_text(self):
        started = self.flow.start()
        finding = self.flow.result(started)['findings'][0]
        event = self.flow.review(started, finding, reason='<script>alert(1)</script>\n# false report [link](https://evil.example)').json()
        report = self.report(started, cutoff=event['committed_at'])
        markdown = self.export(started, 'markdown', event['committed_at'])
        self.assertEqual(markdown.status_code, 200, markdown.text)
        self.assertTrue(markdown.headers['content-type'].startswith('text/markdown'))
        for text in ('Simulated', 'unverified', report['snapshot']['snapshot_id'], finding['finding_id'], 'approved: 1', 'reviewed: 1', 'cost: Unknown'):
            self.assertIn(text, markdown.text)
        self.assertNotIn('<script>', markdown.text)
        self.assertNotIn('\n# false report', markdown.text)
        self.assertNotIn('[link](https://evil.example)', markdown.text)
        for version in report['snapshot']['selected_versions'].values():
            self.assertIn(version, markdown.text)

    def test_ct03_historical_cutoff_preserves_outcome_and_deterministic_bytes(self):
        started = self.flow.start()
        finding = self.flow.result(started)['findings'][0]
        approval = self.flow.review(started, finding).json()
        before = self.export(started, cutoff=approval['committed_at'])
        self.flow.review(started, finding, 'rejected', 1, 'later-reject', reason='Later decision.')
        after = self.export(started, cutoff=approval['committed_at'])
        self.assertEqual(before.status_code, 200, before.text)
        self.assertEqual(before.content, after.content)
        historical = after.json()
        self.assertEqual(historical['summary']['approved'], 1)
        self.assertEqual(historical['summary']['rejected'], 0)
        self.assertEqual([e['revision'] for e in historical['reviews']], [1])
        self.assertEqual(self.report(started)['summary']['rejected'], 1)

    def test_ct04_queued_partial_and_failed_exports_keep_unchecked_scope(self):
        with patch('fastapi.BackgroundTasks.add_task'):
            queued = self.flow.start()
        report = self.report(queued)
        self.assertEqual(report['state'], 'partial')
        self.assertEqual(report['job']['state'], 'queued')
        self.assertIn('Partial export', report['label'])
        self.assertEqual(report['unchecked_obligations'], ['RBI-IT-19b'])
        self.assertEqual(report['findings'], [])
        self.assertIsNone(report['summary']['approval_rate'])
        self.call('POST', f"{self.flow.url}/{queued['job_id']}/resume")
        store = Store(self.flow.path)
        for state in ('partial', 'failed'):
            with store.transaction() as db:
                job = store._job(db, 'operator-a', self.flow.case, queued['job_id'])
                job.update(state=state, stop_reason='test_safe_stop')
                store._save_job(db, job)
            report = self.report(queued)
            self.assertEqual(report['state'], state)
            self.assertEqual(report['job']['stop_reason'], 'test_safe_stop')
            self.assertEqual(len(report['findings']), 1)
            self.assertEqual(report['unchecked_obligations'], [])

    def test_ct05_ownership_and_aws_mode_block_exports(self):
        started = self.flow.start()
        self.assertEqual(self.export(started, app=self.flow.application('operator-b')).status_code, 404)
        other = self.call('POST', '/api/cases', json={'bank_profile': {'name': 'Other fictional bank'}}).json()['case_id']
        response = self.call('POST', f"/api/cases/{other}/assessments/{started['job_id']}/export", json={'format':'json'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.export({'job_id': 'unknown'}).status_code, 404)
        from regulatory_agent.api import create_app
        aws = create_app(store=self.flow.path, environment='aws')
        self.assertEqual(self.export(started, app=aws).status_code, 401)
        with patch('regulatory_agent.api.LocalIdentity.resolve', return_value=object()), \
                patch('regulatory_agent.api.authenticated_owner', return_value='operator-a'):
            self.assertEqual(self.export(started, app=aws).status_code, 404)

    def test_ct06_invalid_requests_and_repeated_exports_have_no_side_effects(self):
        started = self.flow.start()
        before = self.flow.result(started)
        for cutoff in ('invalid', '2026-10-11T12:00:00', (datetime.now(timezone.utc)+timedelta(days=1)).isoformat()):
            self.assertEqual(self.export(started, cutoff=cutoff).status_code, 422)
        self.assertEqual(self.export(started, format='pdf').status_code, 422)
        for _ in range(2):
            self.report(started, cutoff=before['summary']['cutoff'])
        after = self.flow.result(started)
        self.assertEqual(after['job'], before['job'])
        self.assertEqual(after['reviews'], before['reviews'])
        self.assertEqual(after['trace'], before['trace'])
        self.assertEqual(len(self.call('GET', self.flow.url).json()['runs']), 1)

    def test_ct07_replacements_preserve_sources_and_invalid_citations_fail(self):
        started = self.flow.start()
        result = self.flow.result(started)
        source_id = self.flow.policy['document']['source_id']
        self.flow.upload(assessment_flow.POLICY + b'\nChanged future policy.', source_id)
        self.assertEqual(self.report(started)['snapshot'], result['snapshot'])
        self.assertIn('Version', self.export(started, 'markdown').text)
        store = Store(self.flow.path)
        with store.transaction() as db:
            finding = result['findings'][0] | {'citations': [result['findings'][0]['citations'][0] | {'quote':'invented citation'}]}
            db.execute("UPDATE records SET body=? WHERE case_id=? AND kind='finding' AND id=?", (encoded(finding), self.flow.case, finding['finding_id']))
        response = self.export(started)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['code'], 'export_citation_invalid')

    def test_ct08_read_uses_captured_events_and_excludes_later_reviews(self):
        started = self.flow.start()
        finding = self.flow.result(started)['findings'][0]
        approval = self.flow.review(started, finding).json()
        self.flow.review(started, finding, 'rejected', 1, 'later', reason='Later decision.')
        with patch.object(Reviews, 'history', side_effect=AssertionError('Must use captured database events')):
            response = self.call('GET', f"{self.flow.url}/{started['job_id']}?cutoff={quote(approval['committed_at'])}")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual([e['revision'] for e in response.json()['reviews']], [1])
        self.assertEqual(response.json()['summary']['approved'], 1)


if __name__ == '__main__':
    unittest.main()
