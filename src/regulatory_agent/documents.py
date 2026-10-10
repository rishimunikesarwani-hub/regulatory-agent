"""Authorized local document versions with original bytes and immutable source locations."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote
import uuid

from pydantic import ValidationError

from .cases import CaseError, not_found, unavailable
from .contracts import DocumentVersion, Passage, UploadRequest


def rejected(code="invalid_document", *, oversized=False):
    messages = {
        "encrypted_document": "Encrypted documents are not supported.",
        "unreadable_document": "The document has empty or unreadable text. Scanned pages are not supported.",
        "extraction_limit": "The document exceeds the case document or extraction limit.",
        "unsupported_format": "Use a supported text PDF, DOCX, TXT, or CSV file.",
        "extraction_timeout": "The document could not be extracted within the time limit.",
    }
    return CaseError(413 if oversized else 422, code,
                     "The file exceeds the 10 MB limit." if oversized else messages.get(code, "The document is invalid or unsupported."),
                     "Use a smaller, readable English text file with fictional data only.")


def upload_request(headers, size):
    try:
        filename = unquote(headers.get("x-filename", ""), errors="strict")
        if any(ord(c) < 32 or c in "/\\" for c in filename) or filename in {".", ".."}:
            raise ValueError("unsafe_filename")
        request = UploadRequest(filename=filename, kind=headers.get("x-document-kind", ""),
                                size_bytes=size, synthetic=headers.get("x-synthetic") == "true")
        if not request.synthetic:
            raise ValueError("synthetic_required")
        kind = Path(filename).suffix.lower().lstrip(".")
        if kind not in {"pdf", "docx", "txt", "csv"}:
            raise rejected("unsupported_format")
        return request, kind
    except (ValidationError, ValueError, TypeError):
        raise rejected() from None


def extract_document(kind, data):
    try:
        process = subprocess.run([sys.executable, "-X", "utf8", str(Path(__file__).with_name("document_extractor.py")), kind],
                                 input=data, capture_output=True, timeout=10)
    except subprocess.TimeoutExpired:
        raise rejected("extraction_timeout") from None
    try:
        extracted = json.loads(process.stdout)
        if process.returncode or "error" in extracted:
            raise rejected(extracted.get("error", "invalid_document"))
    except (ValueError, UnicodeError):
        raise rejected() from None
    return extracted


class Documents:
    def __init__(self, cases):
        self.cases = cases
        self.store = cases.repository.store
        with self.store.transaction() as db:
            db.execute("CREATE TABLE IF NOT EXISTS documents (id TEXT PRIMARY KEY, case_id TEXT NOT NULL, "
                       "source_id TEXT NOT NULL, original BLOB NOT NULL, body TEXT NOT NULL, units INTEGER NOT NULL, text_bytes INTEGER NOT NULL)")

    def list(self, owner, case):
        self.cases.read(owner, case)
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            rows = db.execute("SELECT body FROM documents WHERE case_id=? ORDER BY rowid DESC", (case,)).fetchall()
        return {"sources": [{k: v for k, v in json.loads(row[0]).items() if k != "passages"} for row in rows]}

    def read(self, owner, case, identity, *, original=False):
        self.cases.read(owner, case)
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            row = db.execute("SELECT body,original FROM documents WHERE case_id=? AND id=?", (case, identity)).fetchone()
        if row is None:
            raise not_found()
        result = json.loads(row[0])
        if hashlib.sha256(row[1]).hexdigest() != result["document"]["sha256"]:
            raise unavailable()
        return (row[1], result["filename"]) if original else result

    def upload(self, owner, case, headers, data):
        self.cases.read(owner, case)
        request, kind = upload_request(headers, len(data))
        extracted = extract_document(kind, data)
        identity = uuid.uuid4().hex
        source = headers.get("x-source-id") or uuid.uuid4().hex
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            if headers.get("x-source-id"):
                if not db.execute("SELECT 1 FROM documents WHERE case_id=? AND source_id=?", (case, source)).fetchone():
                    raise not_found()
            count, units, text_bytes = db.execute("SELECT COUNT(*), COALESCE(SUM(units),0), COALESCE(SUM(text_bytes),0) "
                                                "FROM documents WHERE case_id=?", (case,)).fetchone()
            if count >= 10 or units + extracted["units"] > 100 or text_bytes + extracted["text_bytes"] > 400_000:
                raise rejected("extraction_limit")
            version = db.execute("SELECT COUNT(*) FROM documents WHERE case_id=? AND source_id=?", (case, source)).fetchone()[0] + 1
            document = DocumentVersion(document_version_id=identity, case_id=case, source_id=source,
                kind=request.kind, version=str(version), sha256=hashlib.sha256(data).hexdigest(),
                storage_reference=identity, synthetic=True)
            passages = [Passage(passage_id=f"{identity}-{index}", document_version_id=identity, **passage).model_dump()
                        for index, passage in enumerate(extracted["passages"], 1)]
            result = {"document": document.model_dump(), "filename": request.filename, "format": kind,
                      "units": extracted["units"], "uploaded_at": datetime.now(timezone.utc).isoformat(), "passages": passages}
            db.execute("INSERT INTO documents VALUES (?,?,?,?,?,?,?)",
                       (identity, case, source, data, json.dumps(result), extracted["units"], extracted["text_bytes"]))
        return result
