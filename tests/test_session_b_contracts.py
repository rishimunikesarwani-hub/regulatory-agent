"""T2: executable contracts, local adapters, and failure boundaries."""
import concurrent.futures
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest

from pydantic import ValidationError
from regulatory_agent.contracts import (
    API_CONTRACTS, CaseCreate, Snapshot, StartAssessment, ReviewRequest,
    Finding, Citation, RegulatoryRequest, RegulatorySource, RegulatoryPage,
    LocalIdentity, extraction_units, check_document_limits, schema_bundle,
)
from regulatory_agent.local import Store, BlobStore, ControlledModel, LocalRunner, ContractError
from regulatory_agent.retrieval import ControlledRetrieval, RetrievalLimits
from regulatory_agent.ports import Records, Storage, Jobs, Model, RegulatoryRetrieval

ROOT = Path(__file__).resolve().parents[1]
VERIFY_START = datetime.fromisoformat("2026-10-10T00:00:00+00:00").timestamp()


def snapshot(identity="snap-1", case="case-a"):
    return Snapshot(snapshot_id=identity, case_id=case, bank_profile={"name": "Synthetic demo"},
                    selected_versions={"policy": "v1", "rbi": "2023"},
                    selected_obligations=["O-1"], prompt_version="test-v1", model_version="controlled-v1",
                    assessment_date="2024-04-07", mode="historical", synthetic=True)


def source(**changes):
    text = "Public regulatory test passage."
    data = dict(source_id="RBI-IT-2023", version="2023", authority="Reserve Bank of India",
                source_url="https://www.rbi.org.in/Scripts/test", publication_date="2023-11-07",
                effective_date="2024-04-01", text=text, content_hash=hashlib.sha256(text.encode()).hexdigest(),
                retrieved_at="2026-10-10T00:00:01Z", authority_verified_at="2026-10-10T00:00:01Z",
                freshness="verified", synchronization_verified=True, amendments_complete=True,
                amendments=[], withdrawn=False, etag="tag-1")
    data.update(changes)
    return RegulatorySource(**data)


class SchemaTests(unittest.TestCase):
    def test_b01_request_rejects_forged_owner_and_unknown_fields(self):
        for data in ({"bank_profile": {}, "owner_id": "other"}, {"bank_profile": {}, "extra": True}):
            with self.assertRaises(ValidationError):
                CaseCreate(**data)

    def test_b02_scope_limits_and_duplicate_ids(self):
        for obligations in ([], ["x"] * 2, [f"x{i}" for i in range(21)]):
            with self.assertRaises(ValidationError):
                StartAssessment(selected_versions={"d": "v"}, selected_obligations=obligations,
                                idempotency_key="same", assessment_date="2024-04-07", mode="historical")
        with self.assertRaises(ValidationError):
            ReviewRequest(disposition="erase", note="no")

    def test_b03_export_and_all_api_contracts_are_executable(self):
        required = {"create_case", "list_cases", "read_case", "authorize_upload", "finalize_upload",
                    "list_sources", "read_source", "refresh_regulations", "start_assessment",
                    "compare_versions", "read_job", "read_findings", "save_review", "export_assessment",
                    "read_reviewer_outcomes", "read_stage_trace"}
        self.assertEqual(set(API_CONTRACTS), required)
        self.assertEqual(set(schema_bundle()["operations"]), required)
        for request, response in API_CONTRACTS.values():
            self.assertIn("properties", request.model_json_schema())
            self.assertIn("properties", response.model_json_schema())

    def test_b04_finding_refuses_supported_missing_evidence(self):
        data = dict(finding_id="f1", snapshot_id="snap-1", obligation_id="O-1", control_ids=[],
                    status="supported", evidence_condition="missing", citations=[],
                    rationale="No evidence", remedy="Request evidence", gap_kind="evidence")
        with self.assertRaises(ValidationError):
            Finding(**data)

    def test_b05_nonpaginated_and_aggregate_limits(self):
        self.assertEqual(extraction_units("txt", "a" * 4000), 1)
        self.assertEqual(extraction_units("csv", "a" * 4001), 2)
        self.assertEqual(extraction_units("docx", "₹" * 1334), 2)
        self.assertEqual(extraction_units("pdf", "text", pages=5), 5)
        for args in (("txt", ""), ("html", "text"), ("pdf", "text")):
            with self.assertRaises(ContractError):
                extraction_units(*args)
        check_document_limits([{"bytes": 10_000_000, "units": 100}])
        for docs in ([{"bytes": 1, "units": 1}] * 11,
                     [{"bytes": 10_000_001, "units": 1}], [{"bytes": 1, "units": 101}]):
            with self.assertRaises(ContractError):
                check_document_limits(docs)
        with self.assertRaises(ContractError):
            extraction_units("pdf", "a" * 400001, pages=1)

    def test_b06_development_identity_requires_local_loopback(self):
        self.assertEqual(LocalIdentity.resolve("local", "127.0.0.1", "demo"), "demo")
        for env, peer in (("aws", "127.0.0.1"), ("local", "8.8.8.8"), ("local", "localhost.attacker")):
            with self.assertRaises(ContractError):
                LocalIdentity.resolve(env, peer, "demo")


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)
        self.store = Store(self.path / "records.db")
        self.store.create_case("alice", "case-a", {"name": "Synthetic demo"})
        self.store.create_case("bob", "case-b", {})
        self.store.save_snapshot("alice", snapshot())

    def job(self, key="key-1"):
        return self.store.enqueue("alice", "case-a", "snap-1", key)

    def test_b07_records_enforce_owner_case_and_immutable_versions(self):
        self.store.put("alice", "case-a", "document", "d-v1", {"text": "old"})
        for owner, case in (("bob", "case-a"), ("bob", "case-b")):
            with self.assertRaises(ContractError):
                self.store.get(owner, case, "document", "d-v1")
        with self.assertRaises(ContractError):
            self.store.put("alice", "case-a", "document", "d-v1", {"text": "new"})
        with self.assertRaises(ContractError):
            self.store.put("alice", "case-a", "document", "d2", {"owner_id": "bob"})
        self.store.put("alice", "case-a", "document", "d-v2", {"text": "new"})
        self.assertEqual(self.store.get("alice", "case-a", "snapshot", "snap-1")["selected_versions"]["policy"], "v1")

    def test_b08_blob_adapter_rejects_traversal_and_replacement(self):
        blobs = BlobStore(self.path / "blobs", self.store)
        blobs.put("alice", "case-a", "d-v1", b"original")
        self.assertEqual(blobs.read("alice", "case-a", "d-v1"), b"original")
        for owner, case, key in (("bob", "case-a", "d-v1"), ("alice", "case-a", "../escape")):
            with self.assertRaises(ContractError):
                blobs.read(owner, case, key)
        with self.assertRaises(ContractError):
            blobs.put("alice", "case-a", "d-v1", b"replacement")

    def test_b09_duplicate_requests_and_claims_have_one_winner(self):
        jobs = [self.job() for _ in range(2)]
        self.assertEqual(jobs[0]["job_id"], jobs[1]["job_id"])
        identity = jobs[0]["job_id"]
        def claim(_):
            return Store(self.path / "records.db").claim("alice", "case-a", identity, now=100)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            claims = list(executor.map(claim, range(4)))
        self.assertEqual(sum(c is not None for c in claims), 1)
        self.store.save_snapshot("alice", snapshot("snap-2"))
        with self.assertRaises(ContractError):
            self.store.enqueue("alice", "case-a", "snap-2", "key-1")

    def test_b10_restart_keeps_deadline_budget_stages_and_fences_old_claim(self):
        identity = self.job()["job_id"]
        token = self.store.claim("alice", "case-a", identity, now=100)
        self.store.reserve("alice", "case-a", identity, token, "model", now=101)
        self.store.save_stage("alice", "case-a", identity, token, "one", {"done": True}, now=102)
        again = Store(self.path / "records.db")
        new_token = again.claim("alice", "case-a", identity, now=140)
        job = again.read_job("alice", "case-a", identity)
        self.assertEqual((job["deadline"], job["model_calls"]), (700, 1))
        self.assertEqual(job["stages"]["one"], {"done": True})
        with self.assertRaises(ContractError):
            self.store.reserve("alice", "case-a", identity, token, "model", now=141)
        again.reserve("alice", "case-a", identity, new_token, "model", now=141)

    def test_b11_failed_model_dispatches_are_counted_and_call25_is_blocked(self):
        identity = self.job()["job_id"]
        token = self.store.claim("alice", "case-a", identity, now=100)
        model = ControlledModel(["not json"] * 24)
        for _ in range(24):
            with self.assertRaises(ContractError):
                model.dispatch(self.store, "alice", "case-a", identity, token, {}, now=101)
        with self.assertRaises(ContractError):
            model.dispatch(self.store, "alice", "case-a", identity, token, {}, now=102)
        self.assertEqual(model.dispatches, 24)
        self.assertEqual(self.store.read_job("alice", "case-a", identity)["model_calls"], 24)

    def test_b12_deadline_and_completion_are_truthful(self):
        identity = self.job()["job_id"]
        token = self.store.claim("alice", "case-a", identity, now=100)
        with self.assertRaises(ContractError):
            self.store.reserve("alice", "case-a", identity, token, "model", now=701)
        with self.assertRaises(ContractError):
            self.store.finalize("alice", "case-a", identity, token, "completed", ["O-1"], now=701)
        self.store.finalize("alice", "case-a", identity, token, "failed", ["O-1"], reason="deadline", now=701)
        with self.assertRaises(ContractError):
            self.store.finalize("alice", "case-a", identity, token, "completed", [], now=702)

    def test_b13_runner_persists_controlled_output_and_does_not_repeat(self):
        identity = self.job()["job_id"]
        calls = []
        runner = LocalRunner(self.store)
        def stage(job):
            calls.append(job["job_id"])
            return {"label": "Simulated", "accounted_obligations": ["O-1"]}
        runner.run("alice", "case-a", identity, {"fixture-contract": stage})
        runner.run("alice", "case-a", identity, {"fixture-contract": stage})
        self.assertEqual(len(calls), 1)
        self.assertEqual(self.store.read_job("alice", "case-a", identity)["state"], "completed")

    def test_b14_review_record_does_not_replace_finding(self):
        self.store.put("alice", "case-a", "finding", "f1", {"status": "needs_review"})
        self.store.put("alice", "case-a", "review", "r1", {"finding_id": "f1", "disposition": "disagree"})
        self.assertEqual(self.store.get("alice", "case-a", "finding", "f1")["status"], "needs_review")

    def test_b29_ports_and_model_tool_scope_are_enforced(self):
        self.assertIsInstance(self.store, Records)
        self.assertIsInstance(self.store, Jobs)
        self.assertIsInstance(BlobStore(self.path / "blobs", self.store), Storage)
        self.assertIsInstance(ControlledRetrieval([], {"RBI-IT-2023"}), RegulatoryRetrieval)
        identity = self.job()["job_id"]
        token = self.store.claim("alice", "case-a", identity, now=100)
        action = {"action": "inspect_evidence", "snapshot_id": "snap-1", "document_version_ids": ["policy:v1"]}
        model = ControlledModel([json.dumps(action), json.dumps({**action, "action": "run_shell"}),
                                 json.dumps({**action, "snapshot_id": "other"}),
                                 json.dumps({**action, "document_version_ids": ["policy:v2"]})])
        self.assertIsInstance(model, Model)
        self.assertEqual(model.dispatch(self.store, "alice", "case-a", identity, token, {}, now=101).label, "Simulated")
        for _ in range(3):
            with self.assertRaises(ContractError):
                model.dispatch(self.store, "alice", "case-a", identity, token, {}, now=102)
        self.assertEqual(self.store.read_job("alice", "case-a", identity)["model_calls"], 4)

    def test_b30_new_process_observes_saved_allowance_and_snapshot(self):
        identity = self.job()["job_id"]
        token = self.store.claim("alice", "case-a", identity, now=100)
        self.store.reserve("alice", "case-a", identity, token, "model", now=101)
        code = "from regulatory_agent.local import Store; import json,sys; s=Store(sys.argv[1]); print(json.dumps(s.read_job('alice','case-a',sys.argv[2])))"
        run = subprocess.run([sys.executable, "-c", code, str(self.path / "records.db"), identity], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        loaded = json.loads(run.stdout)
        self.assertEqual((loaded["deadline"], loaded["model_calls"], loaded["snapshot_id"]), (700, 1, "snap-1"))


class RetrievalTests(unittest.TestCase):
    setUp = AdapterTests.setUp
    job = AdapterTests.job
    def fetch(self, pages, **kwargs):
        job = self.job()
        token = self.store.claim("alice", "case-a", job["job_id"], now=VERIFY_START)
        adapter = ControlledRetrieval(pages, {"RBI-IT-2023"}, **kwargs)
        request = RegulatoryRequest(source_ids=["RBI-IT-2023"], assessment_date="2024-04-07")
        return adapter.fetch(request, self.store, "alice", "case-a", job["job_id"], token,
                             now=VERIFY_START + 3), adapter

    def test_b15_complete_verified_response_stays_labelled_simulated(self):
        result, adapter = self.fetch([RegulatoryPage(sources=[source()], complete=True)])
        self.assertEqual(result.label, "Simulated")
        self.assertFalse(result.live_current_coverage)
        self.assertEqual(adapter.dispatches, 1)

    def test_b16_unknown_freshness_incomplete_amendments_and_pagination_fail(self):
        for item in (source(authority_verified_at=None), source(amendments_complete=False),
                     source(freshness="unverified"), source(synchronization_verified=False)):
            with self.subTest(item=item):
                self.setUp()
                with self.assertRaises(ContractError):
                    self.fetch([RegulatoryPage(sources=[item], complete=True)])
        self.setUp()
        with self.assertRaises(ContractError):
            self.fetch([RegulatoryPage(sources=[source()], complete=False)])

    def test_b17_retries_consume_saved_retrieval_allowance(self):
        result, adapter = self.fetch(["timeout", "rate_limited", RegulatoryPage(sources=[source()], complete=True)])
        job = self.store.read_job("alice", "case-a", self.job()["job_id"])
        self.assertEqual((adapter.dispatches, job["retrieval_calls"], job["model_calls"]), (3, 3, 0))

    def test_b18_private_queries_unknown_hosts_redirects_and_oversize_fail(self):
        with self.assertRaises(ValidationError):
            RegulatoryRequest(source_ids=["RBI-IT-2023"], assessment_date="2024-04-07", bank_profile="private")
        for url in ("http://www.rbi.org.in/test", "https://127.0.0.1/test", "https://attacker.test/test",
                    "https://www.rbi.org.in@attacker.test/test"):
            with self.subTest(url=url), self.assertRaises((ValidationError, ContractError)):
                source(source_url=url)
        with self.assertRaises(ContractError):
            self.fetch([RegulatoryPage(sources=[source()], complete=True)], limits=RetrievalLimits(max_response_bytes=10))

    def test_b19_changed_withdrawn_future_and_hash_mismatch_fail(self):
        for item in (source(withdrawn=True), source(effective_date="2027-01-01"), source(version="new")):
            self.setUp()
            with self.assertRaises(ContractError):
                self.fetch([RegulatoryPage(sources=[item], complete=True)], selected={"RBI-IT-2023": source().fingerprint()})
        with self.assertRaises(ValidationError):
            source(content_hash="0" * 64)

    def test_b20_conditional_response_requires_verified_matching_cache(self):
        conditional = RegulatoryPage(sources=[], complete=True, not_modified={"RBI-IT-2023": "tag-1"},
                                     authority_verified_at="2026-10-10T00:00:02Z", synchronization_verified=True)
        result, _ = self.fetch([conditional], cache={"RBI-IT-2023": source()})
        self.assertEqual(len(result.sources), 1)
        self.setUp()
        with self.assertRaises(ContractError):
            self.fetch([conditional])

    def test_b24_future_verification_time_and_cached_old_check_fail(self):
        for timestamp in ("2027-01-01T00:00:00Z", "2026-10-09T23:59:59Z"):
            self.setUp()
            with self.assertRaises(ContractError):
                self.fetch([RegulatoryPage(sources=[source(authority_verified_at=timestamp)], complete=True)])

    def test_b25_restart_reuses_pages_without_dispatch_or_selection_reset(self):
        pages = [RegulatoryPage(sources=[], complete=False, next_cursor="page-2"), "denied"]
        with self.assertRaises(ContractError):
            self.fetch(pages)
        job = self.job()
        token = self.store.claim("alice", "case-a", job["job_id"], now=VERIFY_START + 40)
        adapter = ControlledRetrieval([RegulatoryPage(sources=[source(authority_verified_at="2026-10-10T00:00:41Z")], complete=True)], {"RBI-IT-2023"})
        request = RegulatoryRequest(source_ids=["RBI-IT-2023"], assessment_date="2024-04-07")
        result = adapter.fetch(request, self.store, "alice", "case-a", job["job_id"], token, now=VERIFY_START + 42)
        self.assertEqual(len(result.sources), 1)
        self.assertEqual(adapter.dispatches, 1)
        self.assertEqual(self.store.read_job("alice", "case-a", job["job_id"])["retrieval_calls"], 3)

    def test_b26_unknown_query_denied_and_retries_are_bounded(self):
        for response in ("denied", "redirect", "timeout", "rate_limited"):
            self.setUp()
            with self.assertRaises(ContractError):
                self.fetch([response] * 3)
            consumed = self.store.read_job("alice", "case-a", self.job()["job_id"])["retrieval_calls"]
            self.assertEqual(consumed, 3 if response in {"timeout", "rate_limited"} else 1)
        self.setUp()
        with self.assertRaises(ContractError):
            self.fetch([RegulatoryPage(sources=[], complete=False, next_cursor="again")] * 2)

    def test_b27_provider_update_does_not_mutate_prior_snapshot(self):
        before = self.store.get("alice", "case-a", "snapshot", "snap-1")
        self.fetch([RegulatoryPage(sources=[source(version="new")], complete=True)])
        self.assertEqual(self.store.get("alice", "case-a", "snapshot", "snap-1"), before)

    def test_b28_limits_cannot_be_relaxed(self):
        for limits in (RetrievalLimits(max_requests=21), RetrievalLimits(retries=3), RetrievalLimits(timeout_seconds=11)):
            with self.assertRaises(ContractError):
                ControlledRetrieval([], {"RBI-IT-2023"}, limits=limits)


class WorkerBoundaryTests(unittest.TestCase):
    def test_b21_network_blocked_in_actual_subprocess_loopback_allowed(self):
        code = """
import socket
from regulatory_agent.offline import installed
assert installed
for host in ('example.com', '8.8.8.8', '169.254.169.254', '::ffff:8.8.8.8'):
    try: socket.create_connection((host, 443), timeout=.1)
    except PermissionError: pass
    else: raise AssertionError(host)
with socket.socket() as listener:
    listener.bind(('127.0.0.1', 0)); listener.listen(1)
    with socket.create_connection(listener.getsockname()): pass
print('external blocked; loopback allowed')
"""
        run = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("loopback allowed", run.stdout)

    def test_b22_default_worker_has_no_aws_credentials(self):
        self.assertFalse(any(k.startswith(("AWS_", "OPENAI_", "ANTHROPIC_")) for k in os.environ))

    def test_b23_t1_development_fixture_is_present_and_labelled(self):
        cases = json.loads((ROOT / "data/fixtures/development-inputs.json").read_text())["cases"]
        self.assertEqual(len(cases), 3)
        self.assertTrue(all(c["synthetic"] and c["label"] == "Synthetic demo" for c in cases))


if __name__ == "__main__":
    unittest.main()
