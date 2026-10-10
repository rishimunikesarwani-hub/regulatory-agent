"""Bounded controlled regulatory retrieval. No HTTP transport or live provider."""
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
import time

from .contracts import ContractError, RegulatoryPage, RegulatorySource, RetrievalResult
from .local import BlobStore


@dataclass(frozen=True)
class RetrievalLimits:
    max_response_bytes: int = 1_000_000
    max_total_bytes: int = 10_000_000
    max_pages: int = 10
    max_requests: int = 20
    retries: int = 2
    timeout_seconds: int = 10


class ControlledRetrieval:
    def __init__(self, responses, public_source_ids, *, limits=None, selected=None, cache=None):
        self.responses = iter(responses)
        self.public_source_ids = frozenset(public_source_ids)
        self.limits = limits or RetrievalLimits()
        self.selected = selected or {}
        self.cache = cache or {}
        self.dispatches = 0
        if (not 1 <= self.limits.max_requests <= 20 or not 1 <= self.limits.max_pages <= 10
                or not 0 <= self.limits.retries <= 2 or not 0 < self.limits.timeout_seconds <= 10
                or not 0 < self.limits.max_response_bytes <= 1_000_000
                or not 0 < self.limits.max_total_bytes <= 10_000_000):
            raise ContractError("invalid_retrieval_limits")

    def fetch(self, request, store, owner, case, identity, token, now=None):
        if not set(request.source_ids) <= self.public_source_ids:
            raise ContractError("nonpublic_query")
        request_key = hashlib.sha256(json.dumps({"request": request.model_dump(), "selected": self.selected}, sort_keys=True).encode()).hexdigest()[:24]
        accumulated, cursors, total_bytes = {}, set(), 0
        blobs = BlobStore(store.path.parent / "retrieval-blobs", store)
        for number in range(self.limits.max_pages):
            stage = f"retrieval-{request_key}-{number}"
            job = store.read_job(owner, case, identity)
            if stage in job["stages"]:
                page = RegulatoryPage.model_validate_json(blobs.read(owner, case, job["stages"][stage]["blob_id"]))
            else:
                page = self._dispatch(store, owner, case, identity, token, now)
            total_bytes += len(page.model_dump_json().encode())
            if total_bytes > self.limits.max_total_bytes:
                raise ContractError("retrieval_size_limit")
            items = list(page.sources)
            for source_id, validator in page.not_modified.items():
                cached = self.cache.get(source_id)
                if (cached is None or cached.etag != validator or not page.authority_verified_at
                        or not page.synchronization_verified):
                    raise ContractError("unverified_conditional_response")
                items.append(RegulatorySource.model_validate({**cached.model_dump(),
                             "authority_verified_at": page.authority_verified_at, "freshness": "verified"}))
            for source in items:
                if source.source_id not in request.source_ids or source.source_id in accumulated:
                    raise ContractError("unexpected_or_duplicate_source")
                verified = datetime.fromisoformat(source.authority_verified_at.replace("Z", "+00:00")).timestamp() if source.authority_verified_at else None
                current = time.time() if now is None else now
                if (verified is None or not job["started_at"] <= verified <= current or source.freshness != "verified"
                        or not source.synchronization_verified or not source.amendments_complete):
                    raise ContractError("freshness_unverified")
                if source.withdrawn or source.effective_date > request.assessment_date:
                    raise ContractError("source_not_applicable")
                if self.selected and self.selected.get(source.source_id) != source.fingerprint():
                    raise ContractError("selected_version_changed")
                accumulated[source.source_id] = source
            if sum(len(s.text.encode()) for s in accumulated.values()) > 400_000:
                raise ContractError("regulatory_extraction_limit")
            blob_id = f"{identity}-{stage}"
            blobs.put(owner, case, blob_id, page.model_dump_json().encode())
            store.save_stage(owner, case, identity, token, stage, {"blob_id": blob_id}, now)
            if page.complete:
                if page.next_cursor or set(accumulated) != set(request.source_ids):
                    raise ContractError("incomplete_regulatory_coverage")
                return RetrievalResult(sources=list(accumulated.values()))
            if not page.next_cursor or page.next_cursor in cursors:
                raise ContractError("incomplete_pagination")
            cursors.add(page.next_cursor)
        raise ContractError("pagination_limit")

    def _dispatch(self, store, owner, case, identity, token, now):
        for attempt in range(self.limits.retries + 1):
            current = time.time() if now is None else now
            job = store.read_job(owner, case, identity)
            if job["retrieval_calls"] >= self.limits.max_requests:
                raise ContractError("retrieval_allowance_exhausted")
            if current + self.limits.timeout_seconds > job["deadline"]:
                raise ContractError("retrieval_deadline")
            store.reserve(owner, case, identity, token, "retrieval", current)
            self.dispatches += 1
            try:
                raw = next(self.responses)
            except StopIteration:
                raise ContractError("incomplete_provider_response") from None
            if isinstance(raw, str):
                if raw in {"timeout", "rate_limited"} and attempt < self.limits.retries:
                    continue
                raise ContractError("provider_unavailable")
            if not isinstance(raw, RegulatoryPage):
                raise ContractError("invalid_provider_response")
            if len(raw.model_dump_json().encode()) > self.limits.max_response_bytes:
                raise ContractError("retrieval_response_too_large")
            return raw
        raise ContractError("retrieval_retries_exhausted")
