"""UT-13: failed and partial runs remain in result coverage."""
import unittest
from pydantic import ValidationError
from regulatory_agent.contracts import RunMeasure, RunCohort
from regulatory_agent.reviews import result_coverage


def run(n=0, **changes):
    return RunMeasure(**(dict(run_id=f"r{n}", job_id=f"j{n}", snapshot_id=f"s{n}",
                            job_admitted_at="2026-10-10T10:00:00Z", state="completed",
                            state_recorded_at="2026-10-10T11:00:00Z",
                            selected_obligations=[f"o{x}" for x in range(20)],
                            presented_obligations={f"o{x}": "2026-10-10T10:30:00Z" for x in range(20)},
                            model_id="in.openai.gpt-5.6-luna", prompt_version="v1", data_mode="controlled_simulation") | changes))


def cohort(**changes):
    return RunCohort(**(dict(start="2026-10-10T10:00:00Z", end="2026-10-11T00:00:00Z",
                           cutoff="2026-10-11T00:00:00Z", model_id="in.openai.gpt-5.6-luna",
                           prompt_version="v1", data_mode="controlled_simulation") | changes))


class RunMeasurementTests(unittest.TestCase):
    def test_failed_runs_and_duplicates_in_denominator(self):
        complete = run()
        failed = run(1, state="failed", presented_obligations={})
        report = result_coverage([complete, failed, complete], cohort())
        self.assertEqual((report.selected, report.presented, report.result_coverage), (40, 20, .5))
        self.assertEqual((report.failed, report.unchecked, report.completed_share), (1, 20, .5))
        self.assertEqual(report.time_basis, "job_admitted_at")

    def test_empty_partial_pending_and_window_filters(self):
        partial = run(state="partial", selected_obligations=["a", "b", "c"],
                      presented_obligations={"a": "2026-10-10T10:30:00Z"})
        queued = run(1, state="queued", state_recorded_at="2026-10-10T10:00:00Z", presented_obligations={})
        later = run(2, job_admitted_at=cohort().end, state_recorded_at=cohort().end,
                    state="queued", presented_obligations={})
        report = result_coverage([partial, queued, later], cohort())
        self.assertEqual((report.partial, report.queued, report.running, report.unchecked), (1, 1, 0, 22))
        self.assertEqual(report.result_coverage, 1 / 23)
        self.assertIsNone(result_coverage([], cohort()).result_coverage)

    def test_future_outputs_and_unknown_state_at_cutoff(self):
        report = result_coverage([run()], cohort(cutoff="2026-10-10T10:20:00Z"))
        self.assertEqual((report.presented, report.selected, report.state_unknown_at_cutoff), (0, 20, 1))
        self.assertEqual(report.completed_share, 0)

    def test_scope_and_contradictory_duplicate_rejection(self):
        for changes in ({"selected_obligations": ["a", "a"]},
                        {"presented_obligations": {"unselected": "2026-10-10T10:30:00Z"}},
                        {"presented_obligations": {"o0": "2026-10-10T09:00:00Z"}}):
            with self.assertRaises(ValidationError):
                run(**changes)
        with self.assertRaises(ValueError):
            result_coverage([run(), run(state="failed", presented_obligations={})], cohort())
        self.assertEqual(result_coverage([run(data_mode="live")], cohort()).admitted, 0)
