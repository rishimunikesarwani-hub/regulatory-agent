"""UT-15 and D24 scoring checks with constructed calculation fixtures."""
from dataclasses import replace
import unittest

from regulatory_agent.evaluation import (
    AssessmentCase, AssessmentResult, CitationCheck, ProviderQuery,
    RetrievalQuery, SelectedPassage, evaluate_assessments, evaluate_retrieval,
)


def passage(identity, spans=(), relevance="relevant", **changes):
    values = dict(passage_id=identity, covered_span_ids=tuple(spans),
                  relevance=relevance, reference_valid=True, text_size_chars=10)
    values.update(changes)
    return SelectedPassage(**values)


def query(identity="q1", required=("s1",), passages=None, **changes):
    passages = (passage("p1", ("s1",)),) if passages is None else tuple(passages)
    values = dict(query_id=identity, source_class="regulatory", required_span_ids=required,
                  candidate_passage_ids=tuple(p.passage_id for p in passages),
                  selected_passages=passages)
    values.update(changes)
    return RetrievalQuery(**values)


def score(item):
    return evaluate_retrieval([item])["queries"][0]


def assessment_batch(count=20):
    cases = [AssessmentCase(f"case-{i}", "supported") for i in range(count)]
    results = [AssessmentResult(c.case_id, "supported", (CitationCheck(True, True),))
               for c in cases]
    return cases, results


class RetrievalEvaluationTests(unittest.TestCase):
    def test_ut15_deduplicates_passages_and_overlapping_original_spans(self):
        p1 = passage("p1", ("s1", "s2", "s2"))
        p2 = passage("p2", ("s2", "s3"))
        report = score(query(required=("s1", "s2", "s3", "s4"), passages=(p1, p1, p2)))
        self.assertEqual(report["required_span_recall"]["value"], 3 / 4)
        self.assertEqual(report["selected_passage_count"], 2)
        self.assertEqual(report["selected_text_size_chars"], 20)
        self.assertEqual(report["selected_passage_ids"], ["p1", "p2"])
        self.assertEqual(report["candidate_passage_ids"], ["p1", "p1", "p2"])

    def test_ut15_scores_selected_context_and_unknown_labels_are_lower_bound(self):
        selected = (passage("p1"), passage("p2"), passage("p3", relevance="irrelevant"),
                    passage("p4", relevance="unknown"))
        report = score(query(required=(), passages=selected,
                             candidate_passage_ids=tuple(f"p{i}" for i in range(1, 7))))
        self.assertEqual(report["context_relevance"],
                         dict(numerator=2, denominator=4, value=0.5, status="lower_bound"))
        self.assertEqual(report["unknown_relevance_count"], 1)
        self.assertEqual(report["returned_passage_count"], 6)

    def test_ut15_empty_retrieval_counts_misses_and_undefined_relevance(self):
        report = score(query(required=("s1", "s2"), passages=()))
        self.assertEqual(report["required_span_recall"]["value"], 0)
        self.assertIsNone(report["context_relevance"]["value"])
        self.assertEqual(report["context_relevance"]["status"], "undefined")

    def test_ut15_no_required_evidence_needs_separate_abstention_check(self):
        report = score(query(required=(), passages=(), expected_abstention=True, abstained=True))
        self.assertEqual(report["required_span_recall"]["status"], "not_applicable")
        self.assertIs(report["correct_abstention"], True)
        self.assertIs(score(query(required=(), passages=(), expected_abstention=True,
                                 abstained=False))["correct_abstention"], False)
        self.assertIsNone(score(query(required=(), passages=()))["correct_abstention"])

    def test_ut15_unlabeled_live_queries_do_not_get_measured_recall(self):
        report = score(query(required=None))
        self.assertEqual(report["required_span_recall"],
                         dict(numerator=None, denominator=None, value=None, status="not_measured"))
        self.assertIsNone(report["decisive_omission"])

    def test_ut15_invalid_references_do_not_count_as_coverage_or_relevance(self):
        report = score(query(passages=(passage("p1", ("s1",), reference_valid=False),)))
        self.assertEqual(report["required_span_recall"]["value"], 0)
        self.assertEqual(report["context_relevance"]["value"], 0)
        self.assertEqual(report["invalid_reference_count"], 1)

    def test_ut15_decisive_omissions_count_cases_not_missing_spans(self):
        item = query(required=("s1", "exception", "conflict"),
                     decisive_span_ids=("exception", "conflict"))
        report = evaluate_retrieval([item])
        self.assertEqual(report["queries"][0]["missing_decisive_span_ids"], ["conflict", "exception"])
        self.assertEqual(report["by_source_class"]["regulatory"]["decisive_omission_cases"], 1)

    def test_ut15_separate_source_classes_and_sum_counts_instead_of_percentages(self):
        reports = evaluate_retrieval([
            query("q1"), query("q2", required=("s1", "s2", "s3")),
            query("q3", source_class="bank_evidence", required=("s1", "s2")),
        ])["by_source_class"]
        self.assertEqual(reports["regulatory"]["required_span_recall"]["value"], 2 / 4)
        self.assertEqual(reports["bank_evidence"]["required_span_recall"]["value"], 1 / 2)
        self.assertEqual(reports["regulatory"]["required_span_recall"]["denominator"], 4)

    def test_ut15_partial_reference_coverage_is_visible_in_aggregate(self):
        report = evaluate_retrieval([query("q1"), query("q2", required=None)])
        aggregate = report["by_source_class"]["regulatory"]
        self.assertEqual(aggregate["unlabeled_query_count"], 1)
        self.assertEqual(aggregate["required_span_recall"]["status"], "partial")
        self.assertEqual(aggregate["required_span_recall"]["denominator"], 1)

    def test_ut15_provider_coverage_has_its_own_version_denominator(self):
        report = evaluate_retrieval([query()], [ProviderQuery(
            "provider-1", ("base:v1", "amendment:v2", "amendment:v2", "unrelated:v3"),
            ("base:v1", "amendment:v2", "withdrawal:v3"))])
        coverage = report["provider"]["source_coverage"]
        self.assertEqual(coverage["value"], 2 / 3)
        self.assertEqual(coverage["denominator"], 3)
        self.assertEqual(report["by_source_class"]["regulatory"]["required_span_recall"]["value"], 1)

    def test_ut15_empty_report_is_not_a_perfect_score(self):
        report = evaluate_retrieval([])
        self.assertIsNone(report["provider"]["source_coverage"]["value"])
        self.assertIsNone(report["by_source_class"]["bank_evidence"]["required_span_recall"]["value"])

    def test_ut15_preserves_duration_attempts_and_unknown_telemetry(self):
        measured = score(query(duration_seconds=1.25, attempts=2))
        self.assertEqual((measured["duration_seconds"], measured["attempts"]), (1.25, 2))
        self.assertIsNone(score(query())["duration_seconds"])

    def test_ut15_rejects_invalid_data_and_conflicting_duplicate_passages(self):
        invalid = [query(source_class="combined"), query(query_id=" "),
                   query(required=("s1", "s1")), query(decisive_span_ids=("missing",)),
                   query(candidate_passage_ids=()), query(attempts=True),
                   query(duration_seconds=float("nan")), query(duration_seconds=-1),
                   query(passages=(passage("p1", relevance="probably"),)),
                   query(passages=(passage("p1", reference_valid="true"),)),
                   query(passages=(passage("p1", text_size_chars=-1),)),
                   query(passages=(passage("p1"), passage("p1", relevance="irrelevant"))),
                   query(required=None, decisive_span_ids=("s1",)),
                   query(expected_abstention="yes"), query(required_span_ids="s1")]
        for item in invalid:
            with self.subTest(item=item), self.assertRaises(ValueError):
                evaluate_retrieval([item])
        with self.assertRaises(ValueError):
            evaluate_retrieval([query(), query()])
        with self.assertRaises(ValueError):
            evaluate_retrieval([], [ProviderQuery("p", (), ("v1", "v1"))])


class AssessmentEvaluationTests(unittest.TestCase):
    def test_all_cases_stay_in_denominator_and_matrix_keeps_failure_outcomes(self):
        cases, results = assessment_batch(6)
        results[1] = replace(results[1], status="needs_review")
        results[2] = replace(results[2], status="error", citations=())
        results[3] = replace(results[3], status="malformed", citations=())
        results[4] = replace(results[4], status="abstained", citations=())
        report = evaluate_assessments(cases, results[:-1])
        self.assertEqual(report["primary_agreement"]["value"], 1 / 6)
        for status in ("supported", "needs_review", "error", "malformed", "abstained", "missing"):
            self.assertEqual(report["confusion_matrix"]["supported"][status], 1)
        self.assertEqual(report["unexpected_abstention_count"], 2)
        self.assertEqual(report["per_status"]["supported"], dict(required=6, correct=1))

    def test_expected_needs_review_is_correct_but_explicit_abstention_is_not(self):
        cases = [AssessmentCase("c1", "needs_review", citations_required=False),
                 AssessmentCase("c2", "needs_review", citations_required=False)]
        results = [AssessmentResult("c1", "needs_review"), AssessmentResult("c2", "abstained")]
        report = evaluate_assessments(cases, results)
        self.assertEqual(report["primary_agreement"]["value"], 0.5)
        self.assertEqual(report["unexpected_abstention_count"], 1)

    def test_held_out_sample_gate_needs_twenty_and_ninety_percent(self):
        cases, results = assessment_batch()
        for index in (18, 19):
            results[index] = replace(results[index], status="partial")
        report = evaluate_assessments(cases, results, split="held_out")
        self.assertTrue(report["gates"]["primary_agreement"])
        self.assertTrue(report["quality_gates_pass"])
        self.assertEqual(report["execution_mode"], "controlled")
        self.assertFalse(evaluate_assessments(cases[:19], results[:19], split="held_out")["quality_gates_pass"])
        self.assertFalse(evaluate_assessments(cases, results)["gates"]["held_out_sample"])
        results[17] = replace(results[17], status="partial")
        self.assertFalse(evaluate_assessments(cases, results, split="held_out")["gates"]["primary_agreement"])

    def test_false_supported_critical_case_blocks_gate_at_ninety_five_percent(self):
        cases, results = assessment_batch()
        cases[0] = replace(cases[0], expected_status="needs_review", critical=True)
        report = evaluate_assessments(cases, results, split="held_out")
        self.assertEqual(report["primary_agreement"]["value"], 0.95)
        self.assertEqual(report["critical_false_supported_case_ids"], ["case-0"])
        self.assertFalse(report["gates"]["critical_false_supported"])
        self.assertFalse(report["quality_gates_pass"])

    def test_missing_unresolved_or_unsupported_citations_block_gate(self):
        cases, results = assessment_batch()
        for citations in ((), (CitationCheck(False, True),), (CitationCheck(True, False),),
                          (CitationCheck(None, True),), (CitationCheck(True, None),)):
            with self.subTest(citations=citations):
                modified = [replace(results[0], citations=citations), *results[1:]]
                report = evaluate_assessments(cases, modified, split="held_out")
                self.assertEqual(report["primary_agreement"]["value"], 1)
                self.assertFalse(report["gates"]["citation_support"])
                self.assertFalse(report["quality_gates_pass"])

    def test_optional_citations_are_still_checked_when_reported(self):
        case = AssessmentCase("c1", "not_applicable", citations_required=False)
        report = evaluate_assessments([case], [AssessmentResult(
            "c1", "not_applicable", (CitationCheck(False, False),))])
        self.assertFalse(report["gates"]["citation_support"])
        self.assertEqual(report["error_categories"]["invalid_citations"], 1)

    def test_critical_supported_with_failed_context_support_is_not_safe(self):
        case = AssessmentCase("c1", "supported", critical=True)
        report = evaluate_assessments([case], [AssessmentResult(
            "c1", "supported", (CitationCheck(True, False),))])
        self.assertEqual(report["critical_false_supported_case_ids"], ["c1"])

    def test_error_categories_remain_separate_and_count_cases_once(self):
        case = AssessmentCase("c1", "gap")
        result = AssessmentResult("c1", "supported", (CitationCheck(False, False),),
                                  ("incorrect_mappings", "decisive_omissions", "poor_remedies",
                                   "unsupported_claims", "unsupported_claims"))
        report = evaluate_assessments([case], [result])
        for category in ("invalid_citations", "unsupported_claims", "incorrect_mappings",
                         "decisive_omissions", "incorrect_status", "poor_remedies"):
            self.assertEqual(report["error_categories"][category], 1)

    def test_empty_assessment_is_not_measured_and_cannot_pass(self):
        report = evaluate_assessments([], [], split="held_out")
        self.assertIsNone(report["primary_agreement"]["value"])
        self.assertFalse(report["quality_gates_pass"])
        self.assertFalse(report["gates"]["citation_support"])

    def test_evidence_mode_and_same_operator_are_explicit(self):
        cases, results = assessment_batch()
        report = evaluate_assessments(cases, results, split="held_out", execution_mode="live",
                                      same_operator_review=True)
        self.assertEqual(report["execution_mode"], "live")
        self.assertTrue(report["same_operator_review"])
        self.assertEqual(report["metric_definition_version"], "d24-v1")

    def test_supplied_mode_is_not_independent_proof_of_live_release_evidence(self):
        cases, results = assessment_batch()
        report = evaluate_assessments(cases, results, split="held_out", execution_mode="live")
        self.assertNotIn("live_release_evidence", report)

    def test_rejects_duplicate_unexpected_or_invalid_assessment_records(self):
        cases, results = assessment_batch(1)
        invalid = [(cases * 2, results), (cases, results * 2),
                   (cases, [replace(results[0], case_id="unexpected")]),
                   ([replace(cases[0], expected_status="error")], results),
                   (cases, [replace(results[0], status="unknown")]),
                   ([replace(cases[0], critical="yes")], results),
                   (cases, [replace(results[0], citations=(CitationCheck(1, True),))]),
                   (cases, [replace(results[0], error_categories=("unspecified",))])]
        for references, outcomes in invalid:
            with self.subTest(references=references, outcomes=outcomes), self.assertRaises(ValueError):
                evaluate_assessments(references, outcomes)
        with self.assertRaises(ValueError):
            evaluate_assessments(cases, results, split="mixed")


if __name__ == "__main__":
    unittest.main()
