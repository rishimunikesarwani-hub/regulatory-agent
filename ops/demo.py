"""Run a controlled T2 demonstration using development inputs only."""
import argparse
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from regulatory_agent.offline import install
install()
from regulatory_agent.contracts import Snapshot, schema_bundle
from regulatory_agent.local import BlobStore, ControlledModel, LocalRunner, Store, ContractError


def demonstration(case_id):
    cases = json.loads((ROOT / "data/fixtures/development-inputs.json").read_text(encoding="utf-8"))["cases"]
    case = next((c for c in cases if c["case_id"] == case_id), None)
    if case is None:
        raise ContractError("Choose DEV-01, DEV-02, or DEV-03. Held-out cases are unavailable.")
    with tempfile.TemporaryDirectory(prefix="regulatory-agent-b-") as directory:
        path = Path(directory)
        store = Store(path / "records.db")
        owner = case["owner_id"]
        store.create_case(owner, case_id, case["profile"])
        snap = Snapshot(snapshot_id=f"{case_id}-snapshot", case_id=case_id, bank_profile=case["profile"],
                        selected_versions=case["selected_versions"], selected_obligations=["RBI-IT-2023-19b"],
                        assessment_date=case["assessment_as_of"], mode="historical", prompt_version="contract-demo-v1",
                        model_version="controlled-v1", synthetic=True)
        store.save_snapshot(owner, snap)
        blobs = BlobStore(path / "blobs", store)
        for document in case["documents"]:
            blobs.put(owner, case_id, f"{document['document_id']}:{document['version_id']}", json.dumps(document).encode())
        job = store.enqueue(owner, case_id, snap.snapshot_id, "demo-request")
        repeated = store.enqueue(owner, case_id, snap.snapshot_id, "demo-request")
        action = {"action": "inspect_evidence", "snapshot_id": snap.snapshot_id,
                  "document_version_ids": [f"{d['document_id']}:{d['version_id']}" for d in case["documents"]],
                  "passage_ids": [], "findings": []}
        model = ControlledModel([json.dumps(action)])

        def inspect(job):
            reply = model.dispatch(store, owner, case_id, job["job_id"], job["token"], {"snapshot_id": snap.snapshot_id})
            return {"label": reply.label, "validated_action": reply.action.action, "accounted_obligations": []}

        # This exercises contracts. It intentionally produces no assessment finding.
        result = LocalRunner(store).run(owner, case_id, job["job_id"], {"controlled-action": inspect})
        try:
            store.read_job("another-user", case_id, job["job_id"])
            denied = False
        except ContractError:
            denied = True
        restarted = Store(path / "records.db").read_job(owner, case_id, job["job_id"])
        return {"label": "Synthetic demo / Simulated model", "case": case_id,
                "demonstration": "T2 contracts only; no compliance assessment",
                "fixture_documents_stored": len(case["documents"]), "snapshot_saved": True,
                "duplicate_request_same_job": job["job_id"] == repeated["job_id"],
                "cross_owner_access_denied": denied, "model_calls_saved_after_restart": restarted["model_calls"],
                "validated_model_action": result["stages"]["controlled-action"]["validated_action"],
                "assessment_state": result["state"], "unchecked_obligations": result["unchecked_obligations"],
                "live_model_calls": 0, "current_regulatory_coverage": "unverified",
                "expected": "Assessment stays failed because the contract demonstration produces no findings."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_id", nargs="?", default="DEV-02")
    parser.add_argument("--schemas", action="store_true")
    args = parser.parse_args()
    try:
        result = schema_bundle() if args.schemas else demonstration(args.case_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except ContractError as exc:
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
