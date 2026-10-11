"""T2 validated request/response contracts. HTTP handlers belong to T6."""
from datetime import date, datetime, timezone
import hashlib
import ipaddress
import json
import math
from typing import Annotated, Literal
from urllib.parse import urlsplit

from pydantic import Field, field_validator, model_validator
from .contract_types import Contract, Identifier
from .telemetry import StageAttempt, TokenUsage


class ContractError(ValueError):
    """A safe error code; never attach private content or provider messages."""


Text = Annotated[str, Field(min_length=1, max_length=400_000)]
Status = Literal["supported", "partial", "gap", "needs_review", "not_applicable"]
State = Literal["queued", "running", "completed", "partial", "failed"]
SELECTED_PROMPT = 'assessment-vs5-selected-v1'
PERIOD_PROMPT = 'assessment-vs5-selected-period-v1'
SELECTED_PROMPTS = frozenset((SELECTED_PROMPT, PERIOD_PROMPT))


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

    @field_validator("bank_profile")
    @classmethod
    def valid_case_name(cls, value):
        name = value.get("name")
        if not isinstance(name, str) or not 1 <= len(name.strip()) <= 200:
            raise ValueError("A case name of 1 to 200 characters is necessary")
        return value | {"name": name.strip()}


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
    selected_document_ids: dict[Identifier, Identifier] = Field(default_factory=dict, max_length=10)

    @model_validator(mode='after')
    def artifact_scope(self):
        if self.prompt_version in SELECTED_PROMPTS and not self.selected_document_ids:
            raise ValueError('artifact_scope_missing')
        if self.selected_document_ids and (self.selected_document_ids.keys() != self.selected_versions.keys()
                or len(set(self.selected_document_ids.values())) != len(self.selected_document_ids)):
            raise ValueError('artifact_scope_invalid')
        return self


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


class EvidencePeriod(Contract):
    start: str
    end: str
    _dates = field_validator('start', 'end')(iso_date)

    @model_validator(mode='after')
    def ordered(self):
        if self.start > self.end:
            raise ValueError('Invalid evidence period')
        return self


class AssessmentClaim(Contract):
    obligation_element: Text
    citations: list[Citation] = Field(min_length=1)
    reason: Text
    operational: bool
    evidence_period: EvidencePeriod | None
    examined_exceptions: list[Citation]
    conflicting_evidence: list[Citation]


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
    claims: list[AssessmentClaim] = Field(default_factory=list)

    @model_validator(mode="after")
    def evidence(self):
        if self.status == "supported" and (self.evidence_condition != "sufficient" or not self.citations or self.gap_kind):
            raise ValueError("Supported requires sufficient cited evidence")
        if self.status == "not_applicable" and (not self.applicability_reason or not self.citations):
            raise ValueError("Not applicable requires cited applicability")
        return self


class Findings(Contract):
    findings: list[Finding]


def utc_time(value):
    iso_time(value)
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


DataMode = Literal["controlled_simulation", "offline_benchmark", "synthetic_live", "live"]


class ReviewContent(Contract):
    status: Status
    rationale: Text
    recommendation: Text

    @field_validator("rationale", "recommendation")
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError("Review content must not be blank")
        return value

    def normalized(self):
        return {key: value.replace("\r\n", "\n").replace("\r", "\n").strip()
                for key, value in self.model_dump().items()}


class ReviewItem(Finding):
    run_id: Identifier
    primary_recommendation: Text
    available_at: str
    model_id: Identifier
    prompt_version: Identifier
    data_mode: DataMode
    source_version_ids: list[Identifier] = Field(min_length=1, max_length=10)
    _available = field_validator("available_at")(utc_time)

    def original_content(self):
        return ReviewContent(status=self.status, rationale=self.rationale, recommendation=self.primary_recommendation)


class ReviewRequest(Contract):
    event_kind: Literal["final_review", "evidence_request"]
    disposition: Literal["approved", "edited", "rejected"] | None = None
    accepted_content: ReviewContent | None = None
    reason: str | None = Field(default=None, max_length=4000)
    expected_revision: int = Field(ge=0)
    idempotency_key: Identifier

    @model_validator(mode="after")
    def valid_event(self):
        if self.event_kind == "evidence_request":
            if self.disposition is not None or self.accepted_content is not None:
                raise ValueError("Evidence requests have no final outcome or accepted content")
        elif self.disposition is None:
            raise ValueError("Final reviews need an outcome")
        if self.disposition in {"approved", "edited"} and self.accepted_content is None:
            raise ValueError("Accepted content is necessary")
        if self.disposition == "rejected" and self.accepted_content is not None:
            raise ValueError("Rejected content cannot be accepted")
        if self.disposition in {"edited", "rejected"} and (self.reason is None or not self.reason.strip()):
            raise ValueError("A nonblank reason is necessary")
        return self


class ReviewDecision(ReviewRequest):
    event_id: Identifier
    finding_id: Identifier
    reviewer_id: Identifier
    committed_at: str
    revision: int = Field(ge=1)
    _committed = field_validator("committed_at")(utc_time)


class ReviewCohort(Contract):
    start: str
    end: str
    cutoff: str
    display_timezone: Literal["UTC", "Asia/Kolkata", "Asia/Calcutta"] = "UTC"
    model_id: Identifier
    prompt_version: Identifier
    data_mode: DataMode
    finding_status: Status | None = None
    source_version_ids: list[Identifier] = Field(default_factory=list, max_length=10)
    _times = field_validator("start", "end", "cutoff")(utc_time)

    @model_validator(mode="after")
    def ordered_window(self):
        if datetime.fromisoformat(self.start) >= datetime.fromisoformat(self.end):
            raise ValueError("The start must precede the end")
        return self


class ReviewOutcomeReport(Contract):
    metric_definition_version: Literal["d24-v1"] = "d24-v1"
    cohort: ReviewCohort
    eligible: int = Field(ge=0)
    reviewed: int = Field(ge=0)
    approved: int = Field(ge=0)
    edited: int = Field(ge=0)
    rejected: int = Field(ge=0)
    pending: int = Field(ge=0)
    approval_rate: float | None
    edit_rate: float | None
    rejection_rate: float | None
    adoption_rate: float | None
    review_coverage: float | None
    review_delays_seconds: list[float]
    status_reviewer_groups: list[dict]
    same_operator_review: Literal[True] = True
    acceptance_is_accuracy: Literal[False] = False


class RunCohort(Contract):
    start: str
    end: str
    cutoff: str
    model_id: Identifier
    prompt_version: Identifier
    data_mode: DataMode
    _times = field_validator("start", "end", "cutoff")(utc_time)

    @model_validator(mode="after")
    def ordered_window(self):
        if datetime.fromisoformat(self.start) >= datetime.fromisoformat(self.end):
            raise ValueError("The start must precede the end")
        return self


class RunMeasure(Contract):
    run_id: Identifier
    job_id: Identifier
    snapshot_id: Identifier
    job_admitted_at: str
    state: State
    state_recorded_at: str
    selected_obligations: list[Identifier] = Field(min_length=1, max_length=20)
    presented_obligations: dict[Identifier, str]
    model_id: Identifier
    prompt_version: Identifier
    data_mode: DataMode
    _times = field_validator("job_admitted_at", "state_recorded_at")(utc_time)

    @field_validator("presented_obligations")
    @classmethod
    def output_times(cls, value):
        return {key: utc_time(timestamp) for key, timestamp in value.items()}

    @model_validator(mode="after")
    def valid_scope(self):
        selected = set(self.selected_obligations)
        if len(selected) != len(self.selected_obligations) or not set(self.presented_obligations) <= selected:
            raise ValueError("Invalid obligation scope")
        admitted = datetime.fromisoformat(self.job_admitted_at)
        if datetime.fromisoformat(self.state_recorded_at) < admitted:
            raise ValueError("State precedes admission")
        if any(datetime.fromisoformat(stamp) < admitted for stamp in self.presented_obligations.values()):
            raise ValueError("Output precedes admission")
        return self


class ResultCoverageReport(Contract):
    metric_definition_version: Literal["d24-v1"] = "d24-v1"
    time_basis: Literal["job_admitted_at"] = "job_admitted_at"
    cohort: RunCohort
    admitted: int
    selected: int
    presented: int
    unchecked: int
    result_coverage: float | None
    completed_share: float | None
    completed: int
    failed: int
    partial: int
    queued: int
    running: int
    state_unknown_at_cutoff: int


class TraceQuery(Contract):
    run_id: Identifier


class StageTrace(Contract):
    run_id: Identifier
    attempts: list[StageAttempt]

    @model_validator(mode="after")
    def scoped(self):
        if any(attempt.run_id != self.run_id for attempt in self.attempts):
            raise ValueError("Trace belongs to another run")
        return self


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
    obligations: list[Obligation] = Field(default_factory=list, max_length=20)
    controls: list[Control] = Field(default_factory=list)
    retrieval_query: str | None = Field(default=None, min_length=1, max_length=1000)


class ModelReply(Contract):
    label: Literal["Simulated", "Live"] = "Simulated"
    action: ModelAction
    model_id: Identifier | None = None
    actual_response_model_id: Identifier | None = None
    provider_request_id: Identifier | None = None
    usage: TokenUsage = Field(default_factory=TokenUsage)


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
    "read_reviewer_outcomes": (ReviewCohort, ReviewOutcomeReport),
    "read_stage_trace": (TraceQuery, StageTrace),
}


def schema_bundle():
    return {"version": 2, "operations": {name: {"request": req.model_json_schema(), "response": resp.model_json_schema()}
                                         for name, (req, resp) in API_CONTRACTS.items()},
            "error": SafeError.model_json_schema(), "model_action": ModelAction.model_json_schema(),
            "regulatory_page": RegulatoryPage.model_json_schema()}
