"""UT-16/17/18: controlled runtime calculations and telemetry boundaries."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import unittest

from pydantic import ValidationError
from regulatory_agent.telemetry import (
    AttemptTimer, Charge, StageAttempt, TokenUsage, VersionMetadata,
    attempt_summary, cost_summary, job_outcome_summary, latency_summary,
    review_delay_seconds,
)


T0 = datetime(2026, 10, 10, tzinfo=timezone.utc)


def attempt(**changes):
    values = dict(event_id="event-1", run_id="run-1", job_id="job-1", snapshot_id="snapshot-1",
                  stage_id="stage-1", attempt_id="attempt-1", stage="model_call", operation="model",
                  state="succeeded", dispatched=True, started_at=T0, finished_at=T0 + timedelta(seconds=10),
                  duration_seconds=10.0, versions=VersionMetadata(application="app-v1", schema="schema-v1",
                  extraction="extract-v1", chunking="chunk-v1", retrieval="retrieve-v1", prompt="prompt-v1",
                  model_configuration="model-config-v1"), model_id="in.openai.gpt-5.6-luna")
    values.update(changes)
    return StageAttempt(**values)


def charge(**changes):
    values = dict(event_id="cost-event-1", charge_id="charge-1", scope_id="eval-1", recorded_at=T0,
                  currency="USD", amount=Decimal("4"), status="estimated", component="inference",
                  rate_source="controlled-rates", rate_date="2026-10-10", model_id="in.openai.gpt-5.6-luna",
                  region="ap-south-1", pricing_dimensions={"input_tokens": Decimal("0.01")})
    values.update(changes)
    return Charge(**values)


class RuntimeTests(unittest.TestCase):
    def test_ut16_identity_versions_and_all_stage_names(self):
        for stage in ("source_verification", "extraction", "retrieval", "context_selection", "model_call",
                      "validation", "persistence", "review_event"):
            self.assertEqual(attempt(stage=stage).stage, stage)
        for key in ("event_id", "run_id", "job_id", "snapshot_id", "stage_id", "attempt_id"):
            with self.assertRaises(ValidationError):
                attempt(**{key: ""})
        with self.assertRaises(ValidationError):
            attempt(model_id=None)
        with self.assertRaises(ValidationError):
            attempt(versions=VersionMetadata(application="v1", schema="v1", extraction="v1", chunking="v1",
                                             retrieval="v1", prompt="v1"))

    def test_ut16_saved_stages_require_original_processing_reference(self):
        for state in ("skipped", "not_applicable"):
            with self.assertRaises(ValidationError):
                attempt(state=state, dispatched=False)
            saved = attempt(state=state, dispatched=False, artifact_ids=("artifact-1",),
                            original_processing_event_id="extract-event-1")
            self.assertEqual(saved.original_processing_event_id, "extract-event-1")

    def test_ut16_monotonic_duration_survives_backward_wall_clock(self):
        mono = iter((10.0, 12.0, 18.0))
        wall = iter((T0, T0 - timedelta(hours=1)))
        timer = AttemptTimer(monotonic=lambda: next(mono), utcnow=lambda: next(wall), streaming=True)
        timer.first_token()
        times = timer.finish()
        self.assertEqual(times["duration_seconds"], 8.0)
        self.assertEqual(times["first_token_seconds"], 2.0)
        self.assertLess(times["finished_at"], times["started_at"])
        self.assertEqual(attempt(streaming=True, **times).duration_seconds, 8.0)

    def test_ut16_nonstreaming_never_records_first_token(self):
        with self.assertRaises(ValueError):
            AttemptTimer().first_token()
        with self.assertRaises(ValidationError):
            attempt(first_token_seconds=1.0)
        with self.assertRaises(ValidationError):
            attempt(streaming=True, operation="retrieval", first_token_seconds=1.0)
        with self.assertRaises(ValidationError):
            attempt(streaming=True, first_token_seconds=11.0)

    def test_ut16_timing_values_and_utc(self):
        for value in (-1.0, float("nan"), float("inf"), True):
            with self.assertRaises(ValidationError):
                attempt(duration_seconds=value)
        with self.assertRaises(ValidationError):
            attempt(started_at=T0.replace(tzinfo=None))
        local = T0.astimezone(timezone(timedelta(hours=5, minutes=30)))
        self.assertEqual(attempt(started_at=local).started_at.utcoffset(), timedelta(0))

    def test_ut16_interrupted_and_unknown_are_final_observations(self):
        for state in ("unknown", "interrupted"):
            self.assertEqual(attempt(state=state, finished_at=None, duration_seconds=None).state, state)
        with self.assertRaises(ValidationError):
            attempt(state="running")
        with self.assertRaises(ValidationError):
            attempt(finished_at=None)

    def test_ut16_first_final_review_controls_delay(self):
        self.assertEqual(review_delay_seconds(T0, [T0 + timedelta(seconds=40), T0 + timedelta(seconds=20)]), 20)
        self.assertIsNone(review_delay_seconds(T0, []))
        with self.assertRaises(ValueError):
            review_delay_seconds(T0, [T0 - timedelta(seconds=1)])

    def test_ut17_usage_unknown_is_not_zero_and_values_are_numeric(self):
        usage = TokenUsage(input_tokens=0, cache_read_tokens=12)
        self.assertEqual(usage.input_tokens, 0)
        self.assertIsNone(usage.output_tokens)
        self.assertIsNone(usage.cache_write_tokens)
        self.assertIsNone(attempt().provider_request_id)
        for value in ("12", -1, 1.5, True):
            with self.assertRaises(ValidationError):
                TokenUsage(input_tokens=value)

    def test_ut17_percentiles_and_empty_sample(self):
        summary = latency_summary([10, 20, 30, 40], cohort_id="model-v1")
        self.assertEqual((summary["count"], summary["p50"], summary["p95"]), (4, 20, 40))
        self.assertEqual(summary["interpretation"], "descriptive")
        self.assertEqual(summary["cohort_id"], "model-v1")
        self.assertIsNone(latency_summary([], cohort_id="empty")["p95"])
        for value in (-1, float("nan"), float("inf"), True):
            with self.assertRaises(ValueError):
                latency_summary([value], cohort_id="invalid")

    def test_ut17_attempt_error_denominator_unknown_and_duplicate_export(self):
        records = [attempt(event_id=f"event-{i}", attempt_id=f"attempt-{i}", state=state, errors=errors)
                   for i, (state, errors) in enumerate((("failed", ("timeout", "throttled")),
                   ("failed", ("schema_failure",)), ("succeeded", ()), ("unknown", ())))]
        records += [records[0], attempt(event_id="tool-1", attempt_id="tool-1", operation="retrieval"),
                    attempt(event_id="nondispatched", attempt_id="nondispatched", dispatched=False, state="failed")]
        result = attempt_summary(records)["model"]
        self.assertEqual((result["known_failed"], result["dispatched"], result["error_rate"]), (2, 4, .5))
        self.assertEqual((result["unknown"], result["known_successful"]), (1, 1))
        self.assertEqual(attempt_summary(records)["retrieval"]["dispatched"], 1)
        with self.assertRaises(ValueError):
            attempt_summary([records[0], attempt(event_id="event-0", attempt_id="attempt-0")])

    def test_ut17_completion_includes_pending_and_failed_jobs(self):
        result = job_outcome_summary(["completed", "completed", "completed", "failed", "running"])
        self.assertEqual((result["admitted"], result["completed_share"], result["running"]), (5, .6, 1))
        self.assertIsNone(job_outcome_summary([])["completed_share"])
        with self.assertRaises(ValueError):
            job_outcome_summary(["invented"])

    def test_ut18_private_fields_are_not_telemetry_or_safe_errors(self):
        for key in ("source_text", "query", "review_edit", "review_reason", "authentication_token",
                    "prompt", "response", "hidden_reasoning", "error_message"):
            with self.assertRaises(ValidationError):
                attempt(**{key: "PRIVATE MARKER"})
        with self.assertRaises(ValidationError):
            attempt(errors=("PRIVATE MARKER",))
        with self.assertRaises(ValidationError):
            TokenUsage(authentication_token="PRIVATE MARKER")
        self.assertNotIn("PRIVATE MARKER", attempt().model_dump_json())

    def test_ut18_safe_trace_json_can_be_replayed(self):
        original = attempt(usage=TokenUsage(input_tokens=14, cache_read_tokens=3))
        self.assertEqual(StageAttempt.model_validate_json(original.model_dump_json()), original)

    def test_ut16_final_state_does_not_conflict_with_safe_error_categories(self):
        with self.assertRaises(ValidationError):
            attempt(errors=("timeout",))

    def test_ut17_attempts_of_different_models_have_their_own_denominators(self):
        records = [attempt(), attempt(event_id="other", attempt_id="other", model_id="controlled-other",
                                     state="failed", errors=("throttled",))]
        models = attempt_summary(records)["model"]["by_model"]
        self.assertEqual(models["in.openai.gpt-5.6-luna"]["error_rate"], 0)
        self.assertEqual(models["controlled-other"]["error_rate"], 1)


class CostTests(unittest.TestCase):
    def test_ut17_bill_replaces_estimate_at_cutoff_and_exports_are_deduplicated(self):
        estimate = charge()
        bill = charge(event_id="bill-1", recorded_at=T0 + timedelta(seconds=10), status="billed", amount=Decimal("5"))
        late_estimate = charge(event_id="estimate-2", recorded_at=T0 + timedelta(seconds=20), amount=Decimal("6"))
        records = [estimate, bill, bill, late_estimate]
        early = cost_summary(records, cutoff=T0, scope_id="eval-1", expected_components=("inference",))
        late = cost_summary(records, cutoff=T0 + timedelta(seconds=30), scope_id="eval-1", expected_components=("inference",))
        self.assertEqual(early["measured_total_by_currency"], {"USD": Decimal("4")})
        self.assertEqual(late["measured_total_by_currency"], {"USD": Decimal("5")})
        self.assertEqual(late["effective_charge_count"], 1)
        self.assertEqual(len(records), 4)

    def test_ut17_currency_scope_and_inference_are_separate(self):
        records = [charge(), charge(event_id="cost-2", charge_id="tool-charge", component="tool", currency="INR", amount=Decimal("30")),
                   charge(event_id="other", charge_id="other", scope_id="other", amount=Decimal("100"))]
        result = cost_summary(records, cutoff=T0, scope_id="eval-1", expected_components=("inference", "tool"))
        self.assertEqual(result["measured_total_by_currency"], {"USD": Decimal("4"), "INR": Decimal("30")})
        self.assertEqual(result["inference_by_currency"], {"USD": Decimal("4")})
        self.assertEqual(result["coverage"], "complete")

    def test_ut17_unknown_costs_and_missing_components_are_partial(self):
        result = cost_summary([charge(amount=None)], cutoff=T0, scope_id="eval-1", expected_components=("inference", "tool"))
        self.assertEqual(result["coverage"], "partial")
        self.assertEqual(result["unknown_charge_ids"], ["charge-1"])
        self.assertEqual(result["missing_components"], ["tool"])
        self.assertEqual(result["measured_total_by_currency"], {})
        self.assertIsNone(result["cost_per_correct_by_currency"])

    def test_ut17_total_and_components_cannot_double_count(self):
        total = charge(event_id="total", charge_id="total", component="system_total", included_charge_ids=("charge-1",), amount=Decimal("9"))
        with self.assertRaises(ValueError):
            cost_summary([charge(), total], cutoff=T0, scope_id="eval-1", expected_components=("system_total",))

    def test_ut17_cost_per_correct_includes_incorrect_and_failed_case_costs(self):
        records = [charge(event_id=f"cost-{i}", charge_id=f"case-{i}", amount=Decimal(amount))
                   for i, amount in enumerate(("4", "3", "2"))]
        result = cost_summary(records, cutoff=T0, scope_id="eval-1", expected_components=("inference",), correct_primary_cases=1)
        self.assertEqual(result["measured_total_by_currency"]["USD"], 9)
        self.assertEqual(result["cost_per_correct_by_currency"]["USD"], 9)
        self.assertIsNone(cost_summary(records, cutoff=T0, scope_id="eval-1", expected_components=("inference",), correct_primary_cases=0)["cost_per_correct_by_currency"])

    def test_ut17_invalid_money_identity_and_currency_changes_rejected(self):
        for value in (Decimal("-1"), Decimal("NaN"), Decimal("Infinity")):
            with self.assertRaises(ValidationError):
                charge(amount=value)
        with self.assertRaises(ValidationError):
            charge(currency="private text")
        for conflict in (charge(amount=Decimal("10")), charge(event_id="changed-currency", currency="INR")):
            with self.assertRaises(ValueError):
                cost_summary([charge(), conflict], cutoff=T0, scope_id="eval-1", expected_components=("inference",))

    def test_ut17_retry_and_cache_charge_dimensions_are_retained(self):
        records = [charge(pricing_dimensions={"input_tokens": Decimal("0.01"), "cache_read_tokens": Decimal("0.001"),
                                             "cache_write_tokens": Decimal("0.02")}),
                   charge(event_id="retry", charge_id="retry-charge", amount=Decimal("3"))]
        result = cost_summary(records, cutoff=T0, scope_id="eval-1", expected_components=("inference",))
        self.assertEqual(result["measured_total_by_currency"]["USD"], 7)
        self.assertEqual(records[0].pricing_dimensions["cache_read_tokens"], Decimal("0.001"))


if __name__ == "__main__":
    unittest.main()
