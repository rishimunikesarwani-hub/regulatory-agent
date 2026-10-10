"""D24 safe terminal trace records and controlled runtime calculations."""
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from decimal import Decimal
import math
import time
from typing import Annotated, Literal

from pydantic import AliasChoices, Field, field_validator, model_validator

from .contract_types import Contract, Identifier


Seconds = Annotated[float, Field(ge=0, allow_inf_nan=False)]
Count = Annotated[int, Field(ge=0)]
Amount = Annotated[Decimal, Field(ge=0, allow_inf_nan=False)]
Stage = Literal["source_verification", "extraction", "retrieval", "context_selection", "model_call",
                "validation", "persistence", "review_event"]
ErrorCategory = Literal["throttled", "provider_rejected", "schema_failure", "rejected_action", "timeout",
                        "tool_failure", "storage_failure", "audit_save_failure", "metric_export_failure",
                        "interrupted", "unknown_outcome", "limit_reached", "validation_failure"]
Component = Literal["inference", "tool", "infrastructure", "system_total"]


def _utc(value):
    if value is None:
        return None
    if not isinstance(value, datetime) or value.utcoffset() is None:
        raise ValueError("timezone_required")
    return value.astimezone(timezone.utc)


class VersionMetadata(Contract):
    application: Identifier
    schema_version: Identifier = Field(validation_alias=AliasChoices("schema", "schema_version"))
    extraction: Identifier
    chunking: Identifier
    retrieval: Identifier
    prompt: Identifier
    model_configuration: Identifier | None = None


class TokenUsage(Contract):
    input_tokens: Count | None = None
    output_tokens: Count | None = None
    cache_read_tokens: Count | None = None
    cache_write_tokens: Count | None = None


class StageAttempt(Contract):
    event_id: Identifier
    run_id: Identifier
    job_id: Identifier
    snapshot_id: Identifier
    stage_id: Identifier
    attempt_id: Identifier
    stage: Stage
    operation: Literal["model", "regulatory_api", "storage", "retrieval", "internal"]
    state: Literal["succeeded", "failed", "unknown", "interrupted", "skipped", "not_applicable"]
    dispatched: bool
    started_at: datetime
    finished_at: datetime | None
    duration_seconds: Seconds | None
    versions: VersionMetadata
    model_id: Identifier | None = None
    actual_response_model_id: Identifier | None = None
    provider_request_id: Identifier | None = None
    usage: TokenUsage = Field(default_factory=TokenUsage)
    streaming: bool = False
    first_token_seconds: Seconds | None = None
    retry_index: Count = 0
    returned_bytes: Count | None = None
    unused_allowance: Count | None = None
    errors: tuple[ErrorCategory, ...] = ()
    artifact_ids: tuple[Identifier, ...] = ()
    original_processing_event_id: Identifier | None = None
    candidate_passage_ids: tuple[Identifier, ...] = ()
    selected_passage_ids: tuple[Identifier, ...] = ()

    _times = field_validator("started_at", "finished_at")(_utc)

    @model_validator(mode="after")
    def consistent(self):
        if self.state in {"succeeded", "skipped", "not_applicable"} and self.errors:
            raise ValueError("success_has_failure_categories")
        if self.operation == "model" and (self.model_id is None or self.versions.model_configuration is None):
            raise ValueError("model_configuration_required")
        if self.state in {"skipped", "not_applicable"}:
            if self.dispatched or not self.artifact_ids or not self.original_processing_event_id:
                raise ValueError("saved_processing_reference_required")
        if self.state not in {"unknown", "interrupted"} and (self.finished_at is None or self.duration_seconds is None):
            raise ValueError("terminal_timing_required")
        if self.first_token_seconds is not None:
            if not self.streaming or self.operation != "model":
                raise ValueError("streaming_model_required")
            if self.duration_seconds is not None and self.first_token_seconds > self.duration_seconds:
                raise ValueError("first_token_after_finish")
        return self


class AttemptTimer:
    """Measure one active interval. Never sum overlapping intervals."""

    def __init__(self, *, monotonic=time.monotonic, utcnow=lambda: datetime.now(timezone.utc), streaming=False):
        self._monotonic = monotonic
        self._utcnow = utcnow
        self._start = monotonic()
        self.started_at = _utc(utcnow())
        self.streaming = streaming
        self.first_token_seconds = None
        self._finished = False

    def _elapsed(self):
        elapsed = self._monotonic() - self._start
        if not math.isfinite(elapsed) or elapsed < 0:
            raise ValueError("invalid_monotonic_clock")
        return elapsed

    def first_token(self):
        if not self.streaming or self._finished:
            raise ValueError("invalid_first_token_event")
        if self.first_token_seconds is None:
            self.first_token_seconds = self._elapsed()

    def finish(self):
        if self._finished:
            raise ValueError("timer_already_finished")
        elapsed = self._elapsed()
        self._finished = True
        return {"started_at": self.started_at, "finished_at": _utc(self._utcnow()),
                "duration_seconds": elapsed, "first_token_seconds": self.first_token_seconds}


def latency_summary(durations, *, cohort_id):
    values = list(durations)
    if any(type(value) not in {int, float} or not math.isfinite(value) or value < 0 for value in values):
        raise ValueError("invalid_duration")
    values.sort()
    count = len(values)
    return {"cohort_id": cohort_id, "count": count,
            "p50": values[math.ceil(.50 * count) - 1] if count else None,
            "p95": values[math.ceil(.95 * count) - 1] if count else None,
            "method": "nearest_rank", "interpretation": "descriptive"}


def _unique(records, identity):
    found = {}
    for record in records:
        key = identity(record)
        if key in found and found[key] != record:
            raise ValueError("conflicting_event_identity")
        found[key] = record
    return list(found.values())


def _outcomes(records):
    counts = Counter(record.state for record in records)
    return {"dispatched": len(records), "known_failed": counts["failed"], "known_successful": counts["succeeded"],
            "unknown": counts["unknown"], "interrupted": counts["interrupted"],
            "error_rate": counts["failed"] / len(records) if records else None}


def attempt_summary(records):
    records = _unique(records, lambda record: record.event_id)
    records = _unique(records, lambda record: (record.run_id, record.stage_id, record.attempt_id))
    groups = defaultdict(list)
    for record in records:
        if record.dispatched:
            groups[record.operation].append(record)
    result = {operation: _outcomes(group) for operation, group in groups.items()}
    if "model" in result:
        model_groups = defaultdict(list)
        for record in groups["model"]:
            model_groups[record.model_id].append(record)
        result["model"]["by_model"] = {model: _outcomes(group) for model, group in model_groups.items()}
    return result


def job_outcome_summary(states):
    counts = Counter(states)
    allowed = ("queued", "running", "completed", "partial", "failed")
    if counts.keys() - set(allowed):
        raise ValueError("invalid_job_state")
    total = counts.total()
    return {**{state: counts[state] for state in allowed}, "admitted": total,
            "completed_share": counts["completed"] / total if total else None}


def review_delay_seconds(recommendation_available_at, final_review_times):
    available = _utc(recommendation_available_at)
    times = [_utc(value) for value in final_review_times]
    if not times:
        return None
    delay = (min(times) - available).total_seconds()
    if delay < 0:
        raise ValueError("review_precedes_recommendation")
    return delay


class Charge(Contract):
    event_id: Identifier
    charge_id: Identifier
    scope_id: Identifier
    recorded_at: datetime
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    amount: Amount | None
    status: Literal["estimated", "billed"]
    component: Component
    rate_source: Identifier | None = None
    rate_date: str | None = None
    model_id: Identifier | None = None
    region: Identifier | None = None
    pricing_dimensions: dict[Identifier, Amount | None] = Field(default_factory=dict)
    included_charge_ids: tuple[Identifier, ...] = ()

    _time = field_validator("recorded_at")(_utc)

    @field_validator("rate_date")
    @classmethod
    def valid_date(cls, value):
        if value is not None and date.fromisoformat(value).isoformat() != value:
            raise ValueError("invalid_rate_date")
        return value

    @model_validator(mode="after")
    def valid_inclusions(self):
        if self.included_charge_ids and self.component != "system_total":
            raise ValueError("system_total_required")
        if self.charge_id in self.included_charge_ids or len(set(self.included_charge_ids)) != len(self.included_charge_ids):
            raise ValueError("invalid_charge_inclusion")
        return self


def cost_summary(records, *, cutoff, scope_id, expected_components, correct_primary_cases=None):
    """Aggregate caller-selected evaluation scope. Correctness labels come from its evaluator."""
    cutoff = _utc(cutoff)
    if correct_primary_cases is not None and (type(correct_primary_cases) is not int or correct_primary_cases < 0):
        raise ValueError("invalid_correct_case_count")
    if not expected_components or set(expected_components) - {"inference", "tool", "infrastructure", "system_total"}:
        raise ValueError("expected_cost_components_required")
    records = _unique((r for r in records if r.scope_id == scope_id and r.recorded_at <= cutoff), lambda r: r.event_id)
    groups = defaultdict(list)
    for record in records:
        groups[record.charge_id].append(record)
    effective = {}
    for charge_id, history in groups.items():
        if len({(r.currency, r.component, r.included_charge_ids) for r in history}) != 1:
            raise ValueError("incompatible_logical_charge")
        bills = [r for r in history if r.status == "billed"]
        candidates = bills or history
        latest_time = max(r.recorded_at for r in candidates)
        latest = [r for r in candidates if r.recorded_at == latest_time]
        if len({r.amount for r in latest}) != 1:
            raise ValueError("ambiguous_charge_revision")
        effective[charge_id] = latest[0]
    included = set()
    for record in effective.values():
        if set(record.included_charge_ids) & (effective.keys() | included):
            raise ValueError("overlapping_cost_scope")
        included.update(record.included_charge_ids)
    # A total without a component list cannot establish nonoverlap with other charges.
    if len(effective) > 1 and any(r.component == "system_total" and not r.included_charge_ids for r in effective.values()):
        raise ValueError("unspecified_total_cost_scope")
    total, inference = defaultdict(Decimal), defaultdict(Decimal)
    unknown = []
    for charge_id, record in effective.items():
        if record.amount is None:
            unknown.append(charge_id)
            continue
        total[record.currency] += record.amount
        if record.component == "inference":
            inference[record.currency] += record.amount
    missing = sorted(set(expected_components) - {r.component for r in effective.values()})
    return {"scope_id": scope_id, "cutoff": cutoff, "effective_charge_count": len(effective),
            "measured_total_by_currency": dict(total), "inference_by_currency": dict(inference),
            "coverage": "partial" if unknown or missing else "complete", "missing_components": missing,
            "unknown_charge_ids": sorted(unknown), "human_review_effort": None,
            "cost_per_correct_by_currency": {currency: amount / correct_primary_cases for currency, amount in total.items()}
            if correct_primary_cases and total else None}
