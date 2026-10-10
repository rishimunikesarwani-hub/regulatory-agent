"""T2 validated request/response contracts. HTTP handlers belong to T6."""
from datetime import date, datetime
import hashlib
import ipaddress
import json
import math
from typing import Annotated, Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ContractError(ValueError):
    """A safe error code; never attach private content or provider messages."""


Identifier = Annotated[str, Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")]
Text = Annotated[str, Field(min_length=1, max_length=400_000)]
Status = Literal["supported", "partial", "gap", "needs_review", "not_applicable"]
State = Literal["queued", "running", "completed", "partial", "failed"]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


def iso_date(value):
    if date.fromisoformat(value).isoformat() != value:
        raise ValueError("Use an ISO calendar date")
    return value


def iso_time(value):
    if value is not None and datetime.fromisoformat(value.replace("Z", "+00:00")).utcoffset() is None:
        raise ValueError("Timezone required")
    return value


def public_url(value):
    parts = urlsplit(value)
    if (parts.scheme != "https" or parts.hostname not in {"rbi.org.in", "www.rbi.org.in"}
            or parts.username or parts.password or parts.port not in (None, 443) or parts.fragment):
        raise ValueError("Unapproved public source URL")
    return value


class LocalIdentity:
    @staticmethod
    def resolve(environment: str, peer: str, user: str) -> str:
        try:
            address = ipaddress.ip_address(peer)
            allowed = address.is_loopback or bool(getattr(address, "ipv4_mapped", None) and address.ipv4_mapped.is_loopback)
        except ValueError:
            allowed = False
        if environment != "local" or not allowed or not user:
            raise ContractError("development_identity_denied")
        return user


class Empty(Contract):
    pass


class CaseCreate(Contract):
    bank_profile: dict[str, str | bool | None]
    synthetic: bool = True


class CaseRecord(CaseCreate):
    case_id: Identifier
    owner_id: Identifier
    created_at: str


class CaseList(Contract):
    cases: list[CaseRecord]


class Selection(Contract):
    selected_versions: dict[Identifier, Identifier] = Field(min_length=1, max_length=10)
    selected_obligations: list[Identifier] = Field(min_length=1, max_length=20)
    assessment_date: str
    mode: Literal["historical", "current"]
    _date = field_validator("assessment_date")(iso_date)

    @field_validator("selected_obligations")
    @classmethod
    def unique(cls, values):
        if len(set(values)) != len(values):
            raise ValueError("Duplicate obligation IDs")
        return values


class StartAssessment(Selection):
    idempotency_key: Identifier


class Snapshot(Selection):
    snapshot_id: Identifier
    case_id: Identifier
    bank_profile: dict[str, str | bool | None]
    prompt_version: Identifier
    model_version: Identifier
    synthetic: bool


class Citation(Contract):
    document_version_id: Identifier
    passage_id: Identifier
    location: Text
    quote: Text


class Passage(Contract):
    passage_id: Identifier
    document_version_id: Identifier
    location: Text
    text: Text


class DocumentVersion(Contract):
    document_version_id: Identifier
    case_id: Identifier
    source_id: Identifier
    kind: Literal["regulation", "profile", "policy", "control", "evidence"]
    version: Identifier
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    storage_reference: Identifier
    synthetic: bool
    source_url: str | None = None
    publication_date: str | None = None
    effective_date: str | None = None


class SourceRead(Contract):
    document: DocumentVersion
    passages: list[Passage]


class SourceList(Contract):
    sources: list[DocumentVersion]


class UploadRequest(Contract):
    filename: str = Field(min_length=1, max_length=255)
    kind: Literal["profile", "policy", "control", "evidence"]
    size_bytes: int = Field(gt=0, le=10_000_000)
    synthetic: bool


class UploadAuthorization(Contract):
    upload_id: Identifier
    destination: str
    expires_at: str
    eligible_for_assessment: Literal[False] = False


class FinalizeUpload(Contract):
    upload_id: Identifier


class ExtractionResult(Contract):
    document_version_id: Identifier | None
    eligible_for_assessment: bool
    units: int = Field(ge=0, le=100)
    errors: list[str]


class Obligation(Contract):
    obligation_id: Identifier
    requirement: Text
    conditions: list[str]
    exceptions: list[str]
    applicability: str | None
    citations: list[Citation] = Field(min_length=1)


class Control(Contract):
    control_id: Identifier
    statement: Text
    purpose: str | None
    owner: str | None
    frequency: str | None
    citations: list[Citation] = Field(min_length=1)


class Finding(Contract):
    finding_id: Identifier
    snapshot_id: Identifier
    obligation_id: Identifier
    control_ids: list[Identifier]
    status: Status
    evidence_condition: Literal["sufficient", "partial", "missing", "conflicting"]
    citations: list[Citation]
    rationale: Text
    remedy: str | None
    gap_kind: Literal["control", "evidence"] | None
    applicability_reason: str | None = None

    @model_validator(mode="after")
    def evidence(self):
        if self.status == "supported" and (self.evidence_condition != "sufficient" or not self.citations or self.gap_kind):
            raise ValueError("Supported requires sufficient cited evidence")
        if self.status == "not_applicable" and (not self.applicability_reason or not self.citations):
            raise ValueError("Not applicable requires cited applicability")
        return self


class Findings(Contract):
    findings: list[Finding]


class ReviewRequest(Contract):
    disposition: Literal["agree", "disagree", "request_more_evidence"]
    note: str = Field(max_length=4000)
    idempotency_key: Identifier = "review"


class ReviewDecision(ReviewRequest):
    finding_id: Identifier
    reviewer_id: Identifier
    timestamp: str


class JobAccepted(Contract):
    job_id: Identifier
    state: State


class JobView(JobAccepted):
    snapshot_id: Identifier
    stage: str | None
    model_calls: int = Field(ge=0, le=24)
    retrieval_calls: int = Field(ge=0, le=20)
    deadline: float | None
    unchecked_obligations: list[Identifier]
    stop_reason: str | None
    freshness: Literal["unverified", "verified", "changed", "historical"]
    authority_verified_at: str | None
    label: str


class ComparisonRequest(Contract):
    older_version_id: Identifier
    newer_version_id: Identifier
    snapshot_id: Identifier
    idempotency_key: Identifier

    @model_validator(mode="after")
    def distinct(self):
        if self.older_version_id == self.newer_version_id:
            raise ValueError("Select different versions")
        return self


class ExportRequest(Contract):
    format: Literal["json", "markdown"]


class ExportResponse(Contract):
    snapshot: Snapshot
    state: Literal["completed", "partial", "failed"]
    findings: list[Finding]
    reviews: list[ReviewDecision]
    source_urls: list[str]
    authority_verified_at: str | None
    freshness: Literal["unverified", "verified", "changed", "historical"]
    unchecked_obligations: list[Identifier]
    limitations: list[str]
    label: str

    @model_validator(mode="after")
    def complete(self):
        if self.state == "completed" and self.unchecked_obligations:
            raise ValueError("Completed export has unchecked obligations")
        return self


class SafeError(Contract):
    code: Identifier
    message: str = Field(max_length=200)
    next_action: str = Field(max_length=200)
    correlation_id: Identifier


class ModelAction(Contract):
    action: Literal["retrieve_obligations", "find_controls", "inspect_evidence", "refine_retrieval", "propose_findings"]
    snapshot_id: Identifier
    document_version_ids: list[Identifier]
    passage_ids: list[Identifier] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)


class ModelReply(Contract):
    label: Literal["Simulated"] = "Simulated"
    action: ModelAction


class RegulatoryRequest(Contract):
    source_ids: list[Identifier] = Field(min_length=1, max_length=10)
    assessment_date: str
    _date = field_validator("assessment_date")(iso_date)

    @field_validator("source_ids")
    @classmethod
    def unique(cls, values):
        if len(values) != len(set(values)):
            raise ValueError("Duplicate sources")
        return values


class RegulatorySource(Contract):
    source_id: Identifier
    version: Identifier
    authority: Literal["Reserve Bank of India"]
    source_url: str
    publication_date: str
    effective_date: str
    text: Text
    content_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    retrieved_at: str
    authority_verified_at: str | None
    freshness: Literal["verified", "unverified"]
    synchronization_verified: bool
    amendments_complete: bool
    amendments: list[Identifier]
    withdrawn: bool
    etag: str | None = None
    _url = field_validator("source_url")(public_url)
    _dates = field_validator("publication_date", "effective_date")(iso_date)
    _times = field_validator("retrieved_at", "authority_verified_at")(iso_time)

    @model_validator(mode="after")
    def correct_hash(self):
        if hashlib.sha256(self.text.encode()).hexdigest() != self.content_hash:
            raise ValueError("Source hash mismatch")
        return self

    def fingerprint(self):
        fields = ("source_id", "version", "authority", "source_url", "publication_date", "effective_date",
                  "content_hash", "amendments", "withdrawn")
        return hashlib.sha256(json.dumps({k: getattr(self, k) for k in fields}, sort_keys=True).encode()).hexdigest()


class RegulatoryPage(Contract):
    sources: list[RegulatorySource]
    complete: bool
    next_cursor: str | None = Field(default=None, max_length=256)
    not_modified: dict[Identifier, str] = Field(default_factory=dict)
    authority_verified_at: str | None = None
    synchronization_verified: bool = False
    _time = field_validator("authority_verified_at")(iso_time)


class RetrievalResult(Contract):
    sources: list[RegulatorySource]
    label: Literal["Simulated"] = "Simulated"
    live_current_coverage: Literal[False] = False


def extraction_units(kind: str, text: str, pages: int | None = None) -> int:
    size = len(text.encode("utf-8"))
    if kind not in {"pdf", "docx", "txt", "csv"} or not text.strip() or size > 400_000:
        raise ContractError("invalid_extracted_scope")
    if kind == "pdf":
        if type(pages) is not int or not 1 <= pages <= 100:
            raise ContractError("invalid_pdf_pages")
        return max(pages, math.ceil(size / 4000))
    return math.ceil(size / 4000)


def check_document_limits(documents: list[dict]) -> None:
    if len(documents) > 10 or any(type(d["bytes"]) is not int or not 0 < d["bytes"] <= 10_000_000
                                or type(d["units"]) is not int or d["units"] < 1 for d in documents):
        raise ContractError("document_limit")
    if sum(d["units"] for d in documents) > 100:
        raise ContractError("extraction_limit")


API_CONTRACTS = {
    "create_case": (CaseCreate, CaseRecord), "list_cases": (Empty, CaseList), "read_case": (Empty, CaseRecord),
    "authorize_upload": (UploadRequest, UploadAuthorization), "finalize_upload": (FinalizeUpload, ExtractionResult),
    "list_sources": (Empty, SourceList), "read_source": (Empty, SourceRead),
    "refresh_regulations": (RegulatoryRequest, JobAccepted), "start_assessment": (StartAssessment, JobAccepted),
    "compare_versions": (ComparisonRequest, JobAccepted), "read_job": (Empty, JobView),
    "read_findings": (Empty, Findings), "save_review": (ReviewRequest, ReviewDecision),
    "export_assessment": (ExportRequest, ExportResponse),
}


def schema_bundle():
    return {"version": 1, "operations": {name: {"request": req.model_json_schema(), "response": resp.model_json_schema()}
                                         for name, (req, resp) in API_CONTRACTS.items()},
            "error": SafeError.model_json_schema(), "model_action": ModelAction.model_json_schema(),
            "regulatory_page": RegulatoryPage.model_json_schema()}
