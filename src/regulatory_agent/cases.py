"""Shared case validation and owner scope for the first complete user flow."""
from datetime import datetime, timezone
import json
import uuid

from pydantic import ValidationError

from .contracts import CaseCreate, CaseList, CaseRecord, SafeError
from .local import Store, identifier


class CaseError(Exception):
    def __init__(self, status_code, code, message, next_action):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.next_action = next_action
        super().__init__(code)


def authentication_error():
    return CaseError(401, "authentication_required", "Sign-in is required.", "Sign in again, then reopen your case list.")


def invalid_request():
    return CaseError(422, "invalid_request", "The case request is invalid.", "Use a fictional bank name of 1 to 200 characters.")


def unavailable():
    return CaseError(503, "storage_unavailable", "The case service is unavailable.", "Keep your inputs. Check the case list before another save.")


def not_found():
    return CaseError(404, "case_not_found", "The case is unavailable.", "Return to your case list.")


def error_body(error):
    return SafeError(code=error.code, message=error.message, next_action=error.next_action,
                     correlation_id=uuid.uuid4().hex).model_dump()


def authenticated_owner(owner):
    try:
        return identifier(owner)
    except (ValueError, TypeError):
        raise authentication_error() from None


class SQLiteCases:
    """Use the existing tables without changing legacy case profile values."""
    def __init__(self, store):
        self.store = store if isinstance(store, Store) else Store(store)

    def save(self, record):
        with self.store.transaction() as db:
            db.execute("INSERT INTO cases (id,owner,profile) VALUES (?,?,?)",
                       (record.case_id, record.owner_id, json.dumps(record.bank_profile)))
            db.execute("INSERT INTO records (case_id,kind,id,body) VALUES (?,?,?,?)",
                       (record.case_id, "case_metadata", record.case_id, record.model_dump_json()))

    def list(self, owner):
        with self.store.transaction() as db:
            rows = db.execute("SELECT r.body FROM cases c JOIN records r ON c.id=r.case_id "
                              "WHERE c.owner=? AND r.kind='case_metadata' AND r.id=c.id ORDER BY c.id", (owner,)).fetchall()
        return [CaseRecord.model_validate_json(row[0]) for row in rows]

    def read(self, owner, case_id):
        with self.store.transaction() as db:
            row = db.execute("SELECT r.body FROM cases c JOIN records r ON c.id=r.case_id "
                             "WHERE c.owner=? AND c.id=? AND r.kind='case_metadata' AND r.id=c.id",
                             (owner, case_id)).fetchone()
        return CaseRecord.model_validate_json(row[0]) if row else None


class CaseService:
    def __init__(self, repository):
        self.repository = repository

    def create(self, owner, payload):
        owner = authenticated_owner(owner)
        try:
            request = CaseCreate.model_validate(payload)
        except (ValidationError, TypeError, ValueError):
            raise invalid_request() from None
        if not request.synthetic:
            raise CaseError(422, "synthetic_required", "This release accepts fictional cases only.", "Use a fictional bank profile.")
        record = CaseRecord(**request.model_dump(), case_id=uuid.uuid4().hex, owner_id=owner,
                            created_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
        try:
            self.repository.save(record)
        except Exception:
            raise unavailable() from None
        return record

    def list(self, owner):
        owner = authenticated_owner(owner)
        try:
            records = [CaseRecord.model_validate(record) for record in self.repository.list(owner)]
            if any(record.owner_id != owner for record in records):
                raise ValueError("invalid_owner_scope")
            if len({record.case_id for record in records}) != len(records):
                raise ValueError("duplicate_case")
            return CaseList(cases=sorted(records, key=lambda record: (record.created_at, record.case_id), reverse=True))
        except Exception:
            raise unavailable() from None

    def read(self, owner, case_id):
        owner = authenticated_owner(owner)
        try:
            identifier(case_id)
        except (ValueError, TypeError):
            raise not_found() from None
        try:
            record = self.repository.read(owner, case_id)
            record = CaseRecord.model_validate(record) if record is not None else None
        except Exception:
            raise unavailable() from None
        if record is None or record.owner_id != owner or record.case_id != case_id:
            raise not_found()
        return record
