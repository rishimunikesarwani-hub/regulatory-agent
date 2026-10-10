"""D24 arithmetic over supplied reference labels, not a model or citation judge.

Span coverage and contextual support must come from saved annotation rules.
Reference validity includes case, snapshot, version, period, and quote checks.
These functions do not retrieve sources or certify the supplied judgments.
"""
from dataclasses import dataclass
import math


SOURCE_CLASSES = ("regulatory", "bank_evidence")
STATUSES = ("supported", "partial", "gap", "needs_review", "not_applicable")
OUTCOMES = STATUSES + ("error", "malformed", "missing", "abstained")
ERROR_CATEGORIES = ("retrieval_misses", "incorrect_mappings", "unsupported_claims",
                    "invalid_citations", "decisive_omissions", "incorrect_status", "poor_remedies")


@dataclass(frozen=True)
class SelectedPassage:
    passage_id: str
    covered_span_ids: tuple[str, ...]
    relevance: str
    reference_valid: bool
    text_size_chars: int


@dataclass(frozen=True)
class RetrievalQuery:
    query_id: str
    source_class: str
    candidate_passage_ids: tuple[str, ...]
    selected_passages: tuple[SelectedPassage, ...]
    required_span_ids: tuple[str, ...] | None = None
    decisive_span_ids: tuple[str, ...] = ()
    expected_abstention: bool | None = None
    abstained: bool | None = None
    duration_seconds: float | None = None
    attempts: int | None = None


@dataclass(frozen=True)
class ProviderQuery:
    query_id: str
    retrieved_source_versions: tuple[str, ...]
    required_source_versions: tuple[str, ...] | None = None


@dataclass(frozen=True)
class AssessmentCase:
    case_id: str
    expected_status: str
    critical: bool = False
    citations_required: bool = True


@dataclass(frozen=True)
class CitationCheck:
    resolves: bool | None
    supports: bool | None


@dataclass(frozen=True)
class AssessmentResult:
    case_id: str
    status: str
    citations: tuple[CitationCheck, ...] = ()
    error_categories: tuple[str, ...] = ()


def _require(condition, error):
    if not condition:
        raise ValueError(error)


def _ids(values, *, unique=False):
    _require(isinstance(values, (tuple, list)), "invalid_id_sequence")
    _require(all(isinstance(v, str) and v and v == v.strip() for v in values), "invalid_identifier")
    _require(not unique or len(values) == len(set(values)), "duplicate_reference_id")
    return set(values)


def _boolean(value, optional=False):
    _require(type(value) is bool or optional and value is None, "invalid_boolean")


def _records(values, record_type, identity):
    _require(isinstance(values, (tuple, list)), "invalid_record_sequence")
    _require(all(type(v) is record_type for v in values), "invalid_record_type")
    _ids([getattr(v, identity) for v in values], unique=True)
    return {getattr(v, identity): v for v in values}


def _ratio(numerator, denominator, empty="not_measured", status="measured"):
    return {"numerator": numerator, "denominator": denominator,
            "value": numerator / denominator if denominator else None,
            "status": status if denominator else empty}


def _retrieval_score(query):
    _require(query.source_class in SOURCE_CLASSES, "invalid_source_class")
    candidates = _ids(query.candidate_passage_ids)
    required = None if query.required_span_ids is None else _ids(query.required_span_ids, unique=True)
    decisive = _ids(query.decisive_span_ids, unique=True)
    _require(not decisive or required is not None and decisive <= required, "invalid_decisive_spans")
    _boolean(query.expected_abstention, optional=True)
    _boolean(query.abstained, optional=True)
    _require(query.expected_abstention is None or required == set(), "abstention_requires_empty_reference")
    if query.attempts is not None:
        _require(type(query.attempts) is int and query.attempts >= 0, "invalid_attempt_count")
    if query.duration_seconds is not None:
        _require(type(query.duration_seconds) in (int, float) and math.isfinite(query.duration_seconds)
                 and query.duration_seconds >= 0, "invalid_duration")
    _require(isinstance(query.selected_passages, (tuple, list)), "invalid_passage_sequence")
    passages = {}
    covered = set()
    relevant = unknown = invalid = text_size = 0
    for passage in query.selected_passages:
        _require(type(passage) is SelectedPassage, "invalid_passage_type")
        _ids([passage.passage_id])
        spans = _ids(passage.covered_span_ids)
        _require(passage.passage_id in candidates, "selection_outside_candidates")
        _require(passage.relevance in ("relevant", "irrelevant", "unknown"), "invalid_relevance_label")
        _boolean(passage.reference_valid)
        _require(type(passage.text_size_chars) is int and passage.text_size_chars >= 0, "invalid_text_size")
        if passage.passage_id in passages:
            _require(passage == passages[passage.passage_id], "conflicting_duplicate_passage")
            continue
        passages[passage.passage_id] = passage
        text_size += passage.text_size_chars
        invalid += not passage.reference_valid
        unknown += passage.relevance == "unknown"
        relevant += passage.reference_valid and passage.relevance == "relevant"
        if passage.reference_valid:
            covered.update(spans)
    missing_decisive = sorted(decisive - covered) if required is not None else None
    return {
        "query_id": query.query_id, "source_class": query.source_class,
        "candidate_passage_ids": list(query.candidate_passage_ids),
        "selected_passage_ids": list(passages),
        "returned_passage_count": len(query.candidate_passage_ids),
        "selected_passage_count": len(passages), "selected_text_size_chars": text_size,
        "unknown_relevance_count": unknown, "invalid_reference_count": invalid,
        "required_span_recall": (_ratio(len(required & covered), len(required), "not_applicable")
                                 if required is not None else _ratio(None, None)),
        "context_relevance": _ratio(relevant, len(passages), "undefined",
                                    "lower_bound" if unknown else "measured"),
        "missing_decisive_span_ids": missing_decisive,
        "decisive_omission": bool(missing_decisive) if required is not None else None,
        "correct_abstention": (query.abstained == query.expected_abstention
                               if query.expected_abstention is not None and query.abstained is not None else None),
        "duration_seconds": query.duration_seconds, "attempts": query.attempts,
    }


def _aggregate_ratio(reports, key, empty):
    measured = [r[key] for r in reports if r[key]["denominator"] is not None]
    if not measured:
        return _ratio(None, None)
    status = "partial" if len(measured) != len(reports) else "measured"
    return _ratio(sum(r["numerator"] for r in measured), sum(r["denominator"] for r in measured), empty, status)


def evaluate_retrieval(queries, provider_queries=()):
    """Return query counts and separate source-class totals under D24."""
    _records(queries, RetrievalQuery, "query_id")
    _records(provider_queries, ProviderQuery, "query_id")
    _ids([q.query_id for q in (*queries, *provider_queries)], unique=True)
    reports = [_retrieval_score(query) for query in queries]
    grouped = {}
    for source_class in SOURCE_CLASSES:
        rows = [r for r in reports if r["source_class"] == source_class]
        selected = sum(r["selected_passage_count"] for r in rows)
        unknown = sum(r["unknown_relevance_count"] for r in rows)
        grouped[source_class] = {
            "query_count": len(rows),
            "labeled_query_count": sum(r["decisive_omission"] is not None for r in rows),
            "unlabeled_query_count": sum(r["decisive_omission"] is None for r in rows),
            "required_span_recall": _aggregate_ratio(rows, "required_span_recall", "not_applicable"),
            "context_relevance": _ratio(sum(r["context_relevance"]["numerator"] for r in rows),
                                        selected, "undefined", "lower_bound" if unknown else "measured"),
            "unknown_relevance_count": unknown,
            "invalid_reference_count": sum(r["invalid_reference_count"] for r in rows),
            "decisive_omission_cases": sum(r["decisive_omission"] is True for r in rows),
            "correct_abstention": _ratio(sum(r["correct_abstention"] is True for r in rows),
                                         sum(r["correct_abstention"] is not None for r in rows)),
        }
    provider_rows = []
    for query in provider_queries:
        retrieved = _ids(query.retrieved_source_versions)
        required = None if query.required_source_versions is None else _ids(query.required_source_versions, unique=True)
        provider_rows.append({
            "query_id": query.query_id, "retrieved_source_versions": sorted(retrieved),
            "missing_source_versions": sorted(required - retrieved) if required is not None else None,
            "source_coverage": (_ratio(len(required & retrieved), len(required), "not_applicable")
                                if required is not None else _ratio(None, None)),
        })
    return {"metric_definition_version": "d24-v1", "queries": reports, "by_source_class": grouped,
            "provider": {"queries": provider_rows, "query_count": len(provider_rows),
                         "unlabeled_query_count": sum(q.required_source_versions is None for q in provider_queries),
                         "source_coverage": _aggregate_ratio(provider_rows, "source_coverage", "not_applicable")}}


def evaluate_assessments(cases, results, *, split="development", execution_mode="controlled",
                         same_operator_review=True):
    """Score all required cases using supplied citation and support judgments.

    Execution mode records caller provenance. It does not verify a live run.
    Quality gates alone do not establish operational or release readiness.
    """
    references = _records(cases, AssessmentCase, "case_id")
    outcomes = _records(results, AssessmentResult, "case_id")
    _require(set(outcomes) <= set(references), "unexpected_case_result")
    _require(split in ("development", "held_out"), "invalid_evaluation_split")
    _require(execution_mode in ("controlled", "offline_benchmark", "live"), "invalid_execution_mode")
    _boolean(same_operator_review)
    for case in cases:
        _require(case.expected_status in STATUSES, "invalid_reference_status")
        _boolean(case.critical)
        _boolean(case.citations_required)
    for result in results:
        _require(result.status in OUTCOMES, "invalid_assessment_status")
        _require(isinstance(result.citations, (tuple, list)), "invalid_citation_sequence")
        _require(isinstance(result.error_categories, (tuple, list)) and
                 all(e in ERROR_CATEGORIES for e in result.error_categories), "invalid_error_category")
        for citation in result.citations:
            _require(type(citation) is CitationCheck, "invalid_citation_check")
            _boolean(citation.resolves, optional=True)
            _boolean(citation.supports, optional=True)
    matrix = {expected: dict.fromkeys(OUTCOMES, 0) for expected in STATUSES}
    per_status = {status: {"required": 0, "correct": 0} for status in STATUSES}
    categories = dict.fromkeys(ERROR_CATEGORIES, 0)
    critical_failures, citation_failures, rows = [], [], []
    correct = unexpected_abstentions = resolved = supported = citation_count = unknown = 0
    for case in cases:
        result = outcomes.get(case.case_id, AssessmentResult(case.case_id, "missing"))
        status = result.status
        matches = status == case.expected_status
        correct += matches
        matrix[case.expected_status][status] += 1
        per_status[case.expected_status]["required"] += 1
        per_status[case.expected_status]["correct"] += matches
        unexpected_abstentions += status == "abstained" or status == "needs_review" and not matches
        errors = set(result.error_categories)
        if not matches:
            errors.add("incorrect_status")
        missing_citations = case.citations_required and not result.citations
        citations_ok = not missing_citations
        if missing_citations:
            errors.add("invalid_citations")
        for citation in result.citations:
            citation_count += 1
            resolved += citation.resolves is True
            supported += citation.resolves is True and citation.supports is True
            unknown += citation.resolves is None or citation.supports is None
            if citation.resolves is not True:
                errors.add("invalid_citations")
            if citation.supports is False:
                errors.add("unsupported_claims")
            citations_ok &= citation.resolves is True and citation.supports is True
        citations_ok = citations_ok and not errors.intersection(("invalid_citations", "unsupported_claims"))
        if not citations_ok:
            citation_failures.append(case.case_id)
        false_supported = case.critical and status == "supported" and (
            not matches or not citations_ok or bool(errors.intersection(
                ("incorrect_mappings", "decisive_omissions", "unsupported_claims"))))
        if false_supported:
            critical_failures.append(case.case_id)
        for error in errors:
            categories[error] += 1
        rows.append({"case_id": case.case_id, "expected_status": case.expected_status,
                     "actual_status": status, "correct": matches, "citation_support_pass": bool(citations_ok),
                     "critical_false_supported": bool(false_supported), "error_categories": sorted(errors)})
    gates = {"held_out_sample": split == "held_out" and len(cases) >= 20,
             "primary_agreement": bool(cases) and correct * 10 >= len(cases) * 9,
             "citation_support": bool(cases) and not citation_failures,
             "critical_false_supported": not critical_failures}
    passed = all(gates.values())
    return {
        "metric_definition_version": "d24-v1", "split": split, "execution_mode": execution_mode,
        "same_operator_review": same_operator_review, "cases": rows,
        "primary_agreement": _ratio(correct, len(cases)), "confusion_matrix": matrix,
        "per_status": per_status, "outcome_counts": {s: sum(r["actual_status"] == s for r in rows) for s in OUTCOMES},
        "unexpected_abstention_count": unexpected_abstentions, "error_categories": categories,
        "citation_resolution": _ratio(resolved, citation_count),
        "citation_support": _ratio(supported, citation_count), "unknown_citation_check_count": unknown,
        "citation_failure_case_ids": citation_failures,
        "critical_case_count": sum(case.critical for case in cases),
        "critical_false_supported_case_ids": critical_failures,
        "gates": gates, "quality_gates_pass": passed,
    }
