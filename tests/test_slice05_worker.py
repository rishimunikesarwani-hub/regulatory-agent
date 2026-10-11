"""Real local process-boundary checks with fictional inputs and no network access."""
import multiprocessing
from pathlib import Path
import time
import unittest
from unittest.mock import patch

import test_slice05_pipeline as fixtures
from regulatory_agent.assessment_pipeline import AssessmentPipeline
from regulatory_agent.assessments import Assessments
from regulatory_agent.cases import CaseService, SQLiteCases
from regulatory_agent.contracts import ContractError
from regulatory_agent.documents import Documents
from regulatory_agent.local import ControlledModel, Store


class BlockingModel(ControlledModel):
    def dispatch(self, *args, **kwargs):
        reply = super().dispatch(*args, **kwargs)
        if self.dispatches == 4:
            time.sleep(30)
        return reply


def pipeline_child(path, responses, blocked, owner, case, job, token):
    cases = CaseService(SQLiteCases(Store(path)))
    model = (BlockingModel if blocked else ControlledModel)(responses)
    AssessmentPipeline(Assessments(cases, Documents(cases)), model).run(owner, case, job, execution_token=token)


def hanging_child(path, marker, owner, case, job, token):
    store = Store(path)
    store.reserve(owner, case, job, token, 'model')
    time.sleep(30)
    store.save_stage(owner, case, job, token, 'late', {})
    Path(marker).write_text('late private output', encoding='utf-8')


def crashed_child(path, owner, case, job, token):
    print('PRIVATE EXCEPTION OUTPUT')
    raise RuntimeError('PRIVATE EXCEPTION OUTPUT')


def superseding_child(path, owner, case, job, token):
    store = Store(path)
    with store.transaction() as db:
        current = store._job(db, owner, case, job)
        current['token'] = 'replacement-token'
        store._save_job(db, current)


class WorkerTests(unittest.TestCase):
    def setUp(self):
        from regulatory_agent.assessment_worker import supervise
        self.supervise = supervise
        self.fixture = fixtures.PipelineTests('runTest')
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.f = self.fixture
        self.store = self.f.store
        self.scope = (self.f.owner, self.f.case, self.f.job_id)

    def remaining(self, seconds):
        with self.store.transaction() as db:
            job = self.store._job(db, *self.scope)
            job['started_at'] = time.time() - 600 + seconds
            job['deadline'] = job['started_at'] + 600
            self.store._save_job(db, job)
        return job['deadline']

    def run_pipeline(self, blocked=False):
        responses = [self.f.extraction(), self.f.controls(), self.f.proposed(), self.f.proposed('O-2')]
        return self.supervise(self.store, *self.scope, pipeline_child,
            args=(str(self.store.path), responses, blocked))

    def test_w01_pipeline_completes_with_supervisor_claim_in_spawned_process(self):
        result = self.run_pipeline()
        self.assertEqual(result['state'], 'completed')
        self.assertEqual(result['model_calls'], 4)
        self.assertEqual(len(self.f.findings()), 2)
        self.assertEqual(result['deadline'] - result['started_at'], 600)
        self.assertFalse(any(p.name.startswith('assessment-') for p in multiprocessing.active_children()))

    def test_w02_hung_child_is_stopped_without_late_write(self):
        deadline = self.remaining(2)
        marker = self.store.path.parent / 'late-worker-output.txt'
        started = time.monotonic()
        result = self.supervise(self.store, *self.scope, hanging_child, args=(str(self.store.path), str(marker)))
        self.assertLess(time.monotonic() - started, 5)
        self.assertEqual(result['state'], 'failed')
        self.assertEqual(result['stop_reason'], 'worker_timeout')
        self.assertEqual(result['deadline'], deadline)
        self.assertEqual(result['unchecked_obligations'], ['O-1', 'O-2'])
        self.assertNotIn('late', result['stages'])
        self.assertFalse(marker.exists())
        self.assertFalse(any(p.name.startswith('assessment-') for p in multiprocessing.active_children()))

    def test_w03_timeout_retains_findings_calls_and_unknown_usage(self):
        self.remaining(4)
        result = self.run_pipeline(blocked=True)
        self.assertEqual(result['state'], 'partial')
        self.assertEqual(result['model_calls'], 4)
        self.assertEqual(result['unchecked_obligations'], ['O-2'])
        self.assertEqual(len(self.f.findings()), 1)
        attempts = self.f.service.read(*self.scope)['trace']['attempts']
        interrupted = [a for a in attempts if a['operation'] == 'model' and a['state'] == 'interrupted']
        self.assertEqual(len(interrupted), 1)
        self.assertTrue(interrupted[0]['dispatched'])
        self.assertIsNone(interrupted[0]['usage']['input_tokens'])
        self.assertIn('timeout', interrupted[0]['errors'])
        self.assertFalse(any(a['state'] == 'unknown' for a in attempts))

    def test_w04_child_exception_is_not_completion_or_console_disclosure(self):
        result = self.supervise(self.store, *self.scope, crashed_child, args=(str(self.store.path),))
        self.assertEqual(result['state'], 'failed')
        self.assertEqual(result['stop_reason'], 'worker_crashed')
        self.assertNotIn('PRIVATE', str(result))

    def test_w05_wrong_owner_duplicate_and_terminal_delivery_start_no_child(self):
        invalid_target = lambda *args: None
        with self.assertRaises(ContractError):
            self.supervise(self.store, 'wrong-owner', *self.scope[1:], invalid_target)
        token = self.store.claim(*self.scope)
        active = self.supervise(self.store, *self.scope, invalid_target)
        self.assertEqual(active['token'], token)
        self.store.finalize(*self.scope, token, 'failed', ['O-1', 'O-2'])
        terminal = self.supervise(self.store, *self.scope, invalid_target)
        self.assertEqual(terminal['state'], 'failed')

    def test_w06_exhausted_deadline_does_not_start_child_or_reset_clock(self):
        deadline = self.remaining(-1)
        result = self.supervise(self.store, *self.scope, lambda *args: None)
        self.assertEqual(result['deadline'], deadline)
        self.assertEqual(result['state'], 'failed')
        self.assertEqual(result['model_calls'], 0)
        self.assertEqual(result['stop_reason'], 'worker_timeout')

    def test_w07_lease_renewal_preserves_budget_and_rejects_newer_claim(self):
        token = self.store.claim(*self.scope)
        before = self.store.read_job(*self.scope)
        self.store.renew(*self.scope, token, now=before['started_at'] + 10)
        after = self.store.read_job(*self.scope)
        self.assertEqual(after['lease_until'], before['started_at'] + 40)
        self.assertEqual(after['deadline'], before['deadline'])
        self.assertEqual(after['model_calls'], 0)
        with self.assertRaises(ContractError):
            self.store.renew(*self.scope, 'newer-token')
        with self.assertRaises(ContractError):
            self.store.renew(*self.scope, token, now=before['deadline'])

    def test_w08_stale_supervisor_does_not_finalize_replacement_claim(self):
        result = self.supervise(self.store, *self.scope, superseding_child, args=(str(self.store.path),))
        self.assertEqual(result['state'], 'running')
        self.assertEqual(result['token'], 'replacement-token')
        self.assertIsNone(result['stop_reason'])

    def test_w09_audit_failure_cannot_report_completion(self):
        token = self.store.claim(*self.scope)
        AssessmentPipeline(self.f.service, ControlledModel([]))._begin_attempt(
            self.f.owner, self.f.case, self.f.run, token, 'crash-test', 'source_verification', 'internal')
        with self.store.transaction() as db:
            job = self.store._job(db, *self.scope)
            job['lease_until'] = 0
            self.store._save_job(db, job)
            db.execute("CREATE TRIGGER fail_audit BEFORE UPDATE ON records WHEN OLD.kind='stage_attempt' "
                "BEGIN SELECT RAISE(ABORT,'audit storage unavailable'); END")
        with self.assertRaises(Exception):
            self.supervise(self.store, *self.scope, crashed_child, args=(str(self.store.path),))
        self.assertNotEqual(self.store.read_job(*self.scope)['state'], 'completed')

    def test_w10_start_failure_is_safe_and_does_not_leave_a_running_job(self):
        result = self.supervise(self.store, *self.scope, lambda *args: None)
        self.assertEqual(result['state'], 'failed')
        self.assertEqual(result['stop_reason'], 'worker_start_failed')
        self.assertEqual(result['model_calls'], 0)
        self.assertFalse(any(p.name.startswith('assessment-') for p in multiprocessing.active_children()))

    def test_w11_supervisor_renews_lease_without_extending_deadline(self):
        deadline = self.remaining(6)
        marker = self.store.path.parent / 'heartbeat-late.txt'
        with patch.object(self.store, 'renew', wraps=self.store.renew) as renew:
            result = self.supervise(self.store, *self.scope, hanging_child, args=(str(self.store.path), str(marker)))
        self.assertGreaterEqual(renew.call_count, 1)
        self.assertEqual(result['deadline'], deadline)
        self.assertEqual(result['model_calls'], 1)
        self.assertEqual(result['stop_reason'], 'worker_timeout')

    def test_w12_native_client_is_not_constructed_for_an_unapproved_data_mode(self):
        from regulatory_agent.assessment_worker import bedrock_child
        token = self.store.claim(*self.scope)
        with patch('regulatory_agent.bedrock_model.BedrockModel.configured') as configured:
            with self.assertRaises(ContractError):
                bedrock_child(str(self.store.path), 'et-hackathon-admin', *self.scope, token)
        configured.assert_not_called()

    def test_w13_invalid_inherited_claim_does_not_acquire_another_claim(self):
        token = self.store.claim(*self.scope)
        model = ControlledModel([])
        for invalid in ('', 'stale-token'):
            with self.assertRaises(ContractError):
                AssessmentPipeline(self.f.service, model).run(*self.scope, execution_token=invalid)
        self.assertEqual(self.store.read_job(*self.scope)['token'], token)
        self.assertEqual(model.dispatches, 0)


if __name__ == '__main__':
    unittest.main()
