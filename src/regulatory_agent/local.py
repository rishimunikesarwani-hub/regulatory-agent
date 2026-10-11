"""Local filesystem, SQLite, controlled-model, and durable job adapters."""
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import time
import uuid

from pydantic import ValidationError
from .contracts import ContractError, ModelAction, ModelReply, Snapshot


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}", value):
        raise ContractError("invalid_identifier")
    return value


class Store:
    """Each operation uses its own connection and an atomic SQLite transaction."""
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.transaction() as db:
            db.execute("CREATE TABLE IF NOT EXISTS cases (id TEXT PRIMARY KEY, owner TEXT NOT NULL, profile TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS records (case_id TEXT, kind TEXT, id TEXT, body TEXT NOT NULL, PRIMARY KEY(case_id,kind,id))")
            db.execute("CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, case_id TEXT, idem TEXT, snapshot TEXT, body TEXT NOT NULL, UNIQUE(case_id,idem))")

    @contextmanager
    def transaction(self):
        db = sqlite3.connect(self.path, timeout=10)
        try:
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def authorize(self, owner, case, db=None):
        if db is None:
            with self.transaction() as connection:
                return self.authorize(owner, case, connection)
        row = db.execute("SELECT owner FROM cases WHERE id=?", (case,)).fetchone()
        if not owner or row is None or row[0] != owner:
            raise ContractError("access_denied")

    def create_case(self, owner, case, profile):
        identifier(owner)
        identifier(case)
        with self.transaction() as db:
            try:
                db.execute("INSERT INTO cases VALUES (?,?,?)", (case, owner, encoded(profile)))
            except sqlite3.IntegrityError:
                raise ContractError("case_exists") from None

    def put(self, owner, case, kind, identity, body):
        identifier(identity)
        if kind not in {"document", "snapshot", "finding", "review", "export", "blob"}:
            raise ContractError("invalid_record_kind")
        if body.get("owner_id", owner) != owner or body.get("case_id", case) != case:
            raise ContractError("forged_scope")
        serialized = encoded(body)
        if len(serialized.encode()) > 400_000:
            raise ContractError("record_too_large")
        with self.transaction() as db:
            self.authorize(owner, case, db)
            row = db.execute("SELECT body FROM records WHERE case_id=? AND kind=? AND id=?", (case, kind, identity)).fetchone()
            if row and row[0] != serialized:
                raise ContractError("immutable_record")
            db.execute("INSERT OR IGNORE INTO records VALUES (?,?,?,?)", (case, kind, identity, serialized))

    def get(self, owner, case, kind, identity):
        with self.transaction() as db:
            self.authorize(owner, case, db)
            row = db.execute("SELECT body FROM records WHERE case_id=? AND kind=? AND id=?", (case, kind, identity)).fetchone()
            if row is None:
                raise ContractError("record_not_found")
            return json.loads(row[0])

    def save_snapshot(self, owner, snapshot):
        validated = Snapshot.model_validate(snapshot.model_dump())
        self.put(owner, validated.case_id, "snapshot", validated.snapshot_id, validated.model_dump())

    def enqueue(self, owner, case, snapshot_id, key, now=None):
        identifier(key)
        self.get(owner, case, "snapshot", snapshot_id)
        with self.transaction() as db:
            self.authorize(owner, case, db)
            previous = db.execute("SELECT snapshot,body FROM jobs WHERE case_id=? AND idem=?", (case, key)).fetchone()
            if previous:
                if previous[0] != snapshot_id:
                    raise ContractError("idempotency_conflict")
                return json.loads(previous[1])
            job = dict(job_id=uuid.uuid4().hex, case_id=case, snapshot_id=snapshot_id, state="queued", stage=None,
                       created_at=time.time() if now is None else now, started_at=None, deadline=None, token=None, lease_until=None,
                       model_calls=0, retrieval_calls=0, stages={}, unchecked_obligations=[], stop_reason=None,
                       freshness="unverified", authority_verified_at=None, label="Simulated")
            db.execute("INSERT INTO jobs VALUES (?,?,?,?,?)", (job["job_id"], case, key, snapshot_id, encoded(job)))
            return job

    def _job(self, db, owner, case, identity):
        self.authorize(owner, case, db)
        row = db.execute("SELECT body FROM jobs WHERE id=? AND case_id=?", (identity, case)).fetchone()
        if row is None:
            raise ContractError("job_not_found")
        return json.loads(row[0])

    @staticmethod
    def _save_job(db, job):
        db.execute("UPDATE jobs SET body=? WHERE id=?", (encoded(job), job["job_id"]))

    def read_job(self, owner, case, identity):
        with self.transaction() as db:
            return self._job(db, owner, case, identity)

    def claim(self, owner, case, identity, now=None):
        now = time.time() if now is None else now
        with self.transaction() as db:
            job = self._job(db, owner, case, identity)
            if job["state"] in {"completed", "partial", "failed"}:
                return None
            if job["state"] == "running" and job["lease_until"] > now:
                return None
            job["started_at"] = now if job["started_at"] is None else job["started_at"]
            job["deadline"] = job["started_at"] + 600
            job.update(state="running", token=uuid.uuid4().hex, lease_until=now + 30)
            self._save_job(db, job)
            return job["token"]

    @staticmethod
    def _claimed(job, token, now, permit_expired=False):
        if job["state"] != "running" or job["token"] != token:
            raise ContractError("stale_execution_claim")
        if not permit_expired and (now >= job["deadline"] or now >= job["lease_until"]):
            raise ContractError("deadline_or_lease_exhausted")

    def reserve(self, owner, case, identity, token, kind, now=None):
        now = time.time() if now is None else now
        if kind not in {"model", "retrieval"}:
            raise ContractError("invalid_allowance")
        field, maximum = ("model_calls", 24) if kind == "model" else ("retrieval_calls", 20)
        with self.transaction() as db:
            job = self._job(db, owner, case, identity)
            self._claimed(job, token, now)
            if job[field] >= maximum:
                raise ContractError("allowance_exhausted")
            job[field] += 1
            job["lease_until"] = min(now + 30, job["deadline"])
            self._save_job(db, job)
            return job[field]

    def renew(self, owner, case, identity, token, now=None):
        now = time.time() if now is None else now
        with self.transaction() as db:
            job = self._job(db, owner, case, identity)
            self._claimed(job, token, now)
            job['lease_until'] = min(now + 30, job['deadline'])
            self._save_job(db, job)

    def save_stage(self, owner, case, identity, token, stage, output, now=None):
        now = time.time() if now is None else now
        serialized = encoded(output)
        if len(serialized.encode()) > 400_000:
            raise ContractError("stage_too_large")
        with self.transaction() as db:
            job = self._job(db, owner, case, identity)
            self._claimed(job, token, now)
            if stage in job["stages"] and job["stages"][stage] != output:
                raise ContractError("immutable_stage")
            job["stages"][stage] = output
            job["stage"] = stage
            job["lease_until"] = min(now + 30, job["deadline"])
            self._save_job(db, job)

    def finalize(self, owner, case, identity, token, state, unchecked, reason=None, now=None):
        now = time.time() if now is None else now
        snapshot = self.get(owner, case, "snapshot", self.read_job(owner, case, identity)["snapshot_id"])
        if state not in {"completed", "partial", "failed"} or not set(unchecked) <= set(snapshot["selected_obligations"]):
            raise ContractError("invalid_finalization")
        with self.transaction() as db:
            job = self._job(db, owner, case, identity)
            self._claimed(job, token, now, permit_expired=state != "completed")
            accounted = {item for stage in job["stages"].values() for item in stage.get("accounted_obligations", [])}
            required = set(snapshot["selected_obligations"])
            if state == "completed" and (unchecked or not required <= accounted):
                raise ContractError("unchecked_obligations")
            if state == "partial" and (not accounted or set(unchecked) != required - accounted):
                raise ContractError("invalid_partial_result")
            job.update(state=state, unchecked_obligations=unchecked, stop_reason=reason, finished_at=now)
            self._save_job(db, job)


class BlobStore:
    def __init__(self, root, records):
        self.root = Path(root).resolve()
        self.records = records

    def path(self, owner, case, key):
        self.records.authorize(owner, case)
        for value in (owner, case, key):
            identifier(value)
        # Opaque filenames avoid Windows reserved names and caller-controlled paths.
        relative = [hashlib.sha256(value.encode()).hexdigest() for value in (owner, case, key)]
        path = self.root.joinpath(*relative).resolve()
        if not path.is_relative_to(self.root):
            raise ContractError("invalid_blob_path")
        return path

    def put(self, owner, case, key, data):
        if not isinstance(data, bytes) or not 0 < len(data) <= 10_000_000:
            raise ContractError("invalid_blob_size")
        path = self.path(owner, case, key)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with path.open("xb") as stream:
                stream.write(data)
        except FileExistsError:
            if path.read_bytes() != data:
                raise ContractError("immutable_blob") from None
        self.records.put(owner, case, "blob", key, {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data)})

    def read(self, owner, case, key):
        path = self.path(owner, case, key)
        metadata = self.records.get(owner, case, "blob", key)
        try:
            content = path.read_bytes()
        except FileNotFoundError:
            raise ContractError("blob_not_found") from None
        if hashlib.sha256(content).hexdigest() != metadata["sha256"]:
            raise ContractError("blob_integrity_failure")
        return content


class ControlledModel:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.dispatches = 0

    def dispatch(self, store, owner, case, identity, token, request, now=None):
        store.reserve(owner, case, identity, token, "model", now)
        self.dispatches += 1
        try:
            raw = next(self.responses)
            if not isinstance(raw, str) or len(raw.encode()) > 400_000:
                raise ContractError("invalid_model_response")
            return ModelReply(action=validated_action(raw, store, owner, case, identity))
        except (ValidationError, StopIteration):
            raise ContractError("invalid_model_response") from None


def validated_action(raw, store, owner, case, identity):
    """Share the saved-snapshot boundary between controlled and live dispatch adapters."""
    try:
        action = ModelAction.model_validate_json(raw)
    except ValidationError:
        raise ContractError('invalid_model_response') from None
    job = store.read_job(owner, case, identity)
    snapshot = store.get(owner, case, 'snapshot', job['snapshot_id'])
    allowed = {f'{doc}:{version}' for doc, version in snapshot['selected_versions'].items()}
    if action.snapshot_id != snapshot['snapshot_id'] or not set(action.document_version_ids) <= allowed:
        raise ContractError('model_scope_denied')
    if any(f.snapshot_id != snapshot['snapshot_id'] or f.obligation_id not in snapshot['selected_obligations'] for f in action.findings):
        raise ContractError('model_finding_scope_denied')
    if any(o.obligation_id not in snapshot['selected_obligations'] for o in action.obligations):
        raise ContractError('model_obligation_scope_denied')
    citations = [c for record in (*action.findings, *action.obligations, *action.controls) for c in record.citations]
    citations += [c for finding in action.findings for claim in finding.claims
                  for c in (*claim.citations, *claim.examined_exceptions, *claim.conflicting_evidence)]
    if citations:
        saved_versions = {store.get(owner, case, 'document', key)['document']['document_version_id'] for key in allowed}
        if any(c.document_version_id not in saved_versions for c in citations):
            raise ContractError('model_citation_scope_denied')
    return action


class LocalRunner:
    """Runs trusted short stages. Stage handlers must be idempotent."""
    def __init__(self, store):
        self.store = store

    def run(self, owner, case, identity, stages):
        token = self.store.claim(owner, case, identity)
        if token is None:
            return self.store.read_job(owner, case, identity)
        try:
            for name, handler in stages.items():
                job = self.store.read_job(owner, case, identity)
                if name not in job["stages"]:
                    self.store._claimed(job, token, time.time())
                    output = handler(job)
                    self.store.save_stage(owner, case, identity, token, name, output)
            job = self.store.read_job(owner, case, identity)
            snapshot = self.store.get(owner, case, "snapshot", job["snapshot_id"])
            accounted = {item for value in job["stages"].values() for item in value.get("accounted_obligations", [])}
            unchecked = [item for item in snapshot["selected_obligations"] if item not in accounted]
            state = "partial" if unchecked and accounted else "failed" if unchecked else "completed"
            self.store.finalize(owner, case, identity, token, state, unchecked)
        except Exception:
            job = self.store.read_job(owner, case, identity)
            if job["token"] != token or job["state"] != "running":
                raise ContractError("stale_execution_claim") from None
            snapshot = self.store.get(owner, case, "snapshot", job["snapshot_id"])
            accounted = {item for value in job["stages"].values() for item in value.get("accounted_obligations", [])}
            unchecked = [item for item in snapshot["selected_obligations"] if item not in accounted]
            self.store.finalize(owner, case, identity, token, "partial" if accounted else "failed", unchecked, reason="stage_failed")
        return self.store.read_job(owner, case, identity)
