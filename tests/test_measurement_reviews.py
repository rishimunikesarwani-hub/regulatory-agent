"""D24 / UT-13, UT-14: saved human outcomes, ownership, and reproducible reports."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest

from pydantic import ValidationError
from regulatory_agent.contracts import ContractError, ReviewContent, ReviewItem, ReviewRequest, ReviewCohort
from regulatory_agent.local import Store
from regulatory_agent.reviews import Reviews
from test_session_b_contracts import snapshot


def item(n=0, **changes):
    value = dict(finding_id=f"f{n}", run_id=f"run{n}", snapshot_id="snap-1", obligation_id="O-1",
                 control_ids=[], status="needs_review", evidence_condition="missing", citations=[],
                 rationale="Operational evidence is missing.", remedy="Supply the evidence.", gap_kind="evidence",
                 primary_recommendation="Supply the evidence.", available_at="2026-10-10T10:00:00Z",
                 model_id="in.openai.gpt-5.6-luna", prompt_version="v1", data_mode="controlled_simulation",
                 source_version_ids=["policy:v1", "rbi:2023"])
    return ReviewItem(**(value | changes))


def cohort(**changes):
    return ReviewCohort(**(dict(start="2026-10-10T10:00:00Z", end="2026-10-11T00:00:00Z",
                              cutoff="2026-10-11T00:00:00Z", display_timezone="Asia/Kolkata",
                              model_id="in.openai.gpt-5.6-luna", prompt_version="v1",
                              data_mode="controlled_simulation") | changes))


def request(outcome="approved", revision=0, key="k1", content=None, reason=None):
    return ReviewRequest(event_kind="final_review", disposition=outcome, expected_revision=revision,
                         idempotency_key=key, accepted_content=content, reason=reason)


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "records.sqlite"
        self.store = Store(self.path)
        self.store.create_case("alice", "case-a", {})
        self.store.create_case("bob", "case-b", {})
        self.store.save_snapshot("alice", snapshot().model_copy(update={
            "model_version": "in.openai.gpt-5.6-luna", "prompt_version": "v1"}))
        self.now = "2026-10-10T11:00:00Z"
        self.reviews = Reviews(self.store, clock=lambda: datetime.fromisoformat(self.now.replace("Z", "+00:00")))

    def save(self, value=None):
        value = value or item()
        previous = self.now
        self.now = "2026-10-10T09:00:00Z"
        self.reviews.admit("alice", "case-a", value.run_id, "snap-1", "controlled_simulation")
        self.now = value.available_at
        saved = self.reviews.present("alice", "case-a", value)
        self.now = previous
        return saved

    def final(self, value, outcome="approved", revision=0, key="k1"):
        content = value.original_content()
        if outcome == "edited":
            content = content.model_copy(update={"recommendation": "Supply dated evidence."})
        return self.reviews.save("alice", "case-a", value.finding_id,
                                 request(outcome, revision, key, content if outcome != "rejected" else None,
                                         "Reviewer reason" if outcome != "approved" else None))

    def test_immutable_item_and_one_item_per_run_obligation(self):
        value = self.save()
        self.save(value)
        with self.assertRaisesRegex(ContractError, "immutable"):
            self.save(item(rationale="Changed"))
        with self.assertRaisesRegex(ContractError, "duplicate_review_item"):
            self.save(item(1, run_id=value.run_id))
        self.save(item(2))
        self.assertEqual(self.reviews.report("alice", "case-a", cohort()).pending, 2)

    def test_reject_forged_identity_and_legacy_outcome(self):
        for fields in ({"reviewer_id": "bob"}, {"disposition": "agree"}, {"committed_at": self.now}):
            data = request(content=item().original_content()).model_dump() | fields
            with self.assertRaises(ValidationError):
                ReviewRequest(**data)
        value = self.save()
        for action in (lambda: self.reviews.history("bob", "case-a", value.finding_id),
                       lambda: self.reviews.report("bob", "case-a", cohort()),
                       lambda: self.reviews.save("bob", "case-a", value.finding_id,
                                                  request(content=value.original_content()))):
            with self.assertRaisesRegex(ContractError, "access_denied"):
                action()

    def test_edited_requires_changed_content_and_reason(self):
        value = self.save()
        unchanged = value.original_content().model_copy(update={"rationale": "  Operational evidence is missing.\r\n"})
        with self.assertRaisesRegex(ContractError, "unchanged"):
            self.reviews.save("alice", "case-a", value.finding_id,
                              request("edited", content=unchanged, reason="Change"))
        for reason in (None, "", " \n"):
            with self.assertRaises(ValidationError):
                request("edited", content=value.original_content(), reason=reason)
            with self.assertRaises(ValidationError):
                request("rejected", reason=reason)
        changed = value.original_content().model_copy(update={"recommendation": "Other"})
        with self.assertRaisesRegex(ContractError, "original"):
            self.reviews.save("alice", "case-a", value.finding_id, request(content=changed))

    def test_revisions_cutoffs_pending_request_and_original_after_edit(self):
        value = self.save()
        approved = self.final(value)
        self.now = "2026-10-10T12:00:00Z"
        edited = self.final(value, "edited", 1, "k2")
        pending = ReviewRequest(event_kind="evidence_request", expected_revision=2,
                                idempotency_key="k3", reason="Need more records")
        self.reviews.save("alice", "case-a", value.finding_id, pending)
        self.assertEqual(self.reviews.report("alice", "case-a", cohort()).edited, 1)
        self.now = "2026-10-10T13:00:00Z"
        self.final(value, "rejected", 3, "k4")
        for cutoff, expected in ((approved.committed_at, "approved"), (edited.committed_at, "edited"),
                                 (self.now, "rejected")):
            report = self.reviews.report("alice", "case-a", cohort(cutoff=cutoff))
            self.assertEqual(getattr(report, expected), 1)
            self.assertEqual(report.review_delays_seconds, [3600.0])
        self.final(value, "approved", 4, "k5")
        self.assertEqual(self.reviews.report("alice", "case-a", cohort()).approved, 1)
        self.assertEqual(value.status, "needs_review")
        self.assertEqual(len(self.reviews.history("alice", "case-a", value.finding_id)), 5)

    def test_duplicate_retries_concurrency_and_restart(self):
        value = self.save()
        req = request(content=value.original_content())
        with ThreadPoolExecutor(max_workers=4) as pool:
            events = list(pool.map(lambda _: self.reviews.save("alice", "case-a", value.finding_id, req), range(4)))
        self.assertEqual(len({e.event_id for e in events}), 1)
        self.final(value, "rejected", 1, "k2")
        restarted = Reviews(Store(self.path))
        self.assertEqual(restarted.save("alice", "case-a", value.finding_id, req), events[0])
        with self.assertRaisesRegex(ContractError, "idempotency_conflict"):
            restarted.save("alice", "case-a", value.finding_id, req.model_copy(update={"reason": "Changed"}))
        with self.assertRaisesRegex(ContractError, "revision_conflict"):
            self.final(value, "edited", 0, "stale")

    def test_competing_writes_same_revision_only_one_wins(self):
        value = self.save()
        def write(n):
            try:
                return self.final(value, "approved", 0, f"key{n}").revision
            except ContractError as error:
                return str(error)
        with ThreadPoolExecutor(max_workers=2) as pool:
            result = list(pool.map(write, range(2)))
        self.assertCountEqual(result, [1, "revision_conflict"])

    def test_north_star_counts_and_empty_cohort(self):
        for n in range(12):
            value = self.save(item(n))
            if n < 10:
                self.final(value, "approved" if n < 6 else "edited" if n < 9 else "rejected")
        report = self.reviews.report("alice", "case-a", cohort())
        self.assertEqual((report.eligible, report.reviewed, report.pending), (12, 10, 2))
        self.assertEqual((report.approval_rate, report.edit_rate, report.rejection_rate), (.6, .3, .1))
        self.assertEqual((report.adoption_rate, report.review_coverage), (.9, 10 / 12))
        self.assertEqual(report.metric_definition_version, "d24-v1")
        empty = self.reviews.report("alice", "case-a", cohort(prompt_version="other"))
        self.assertIsNone(empty.approval_rate)
        self.assertIsNone(empty.review_coverage)

    def test_windows_filters_and_same_timestamp_order(self):
        value = self.save()
        self.save(item(1, available_at=cohort().end))
        self.save(item(2, available_at="2026-10-10T09:59:59Z"))
        self.reviews.admit("alice", "case-a", "run3", "snap-1", "synthetic_live")
        self.reviews.present("alice", "case-a", item(3, data_mode="synthetic_live"))
        self.final(value)
        self.final(value, "rejected", 1, "k2")
        report = self.reviews.report("alice", "case-a", cohort())
        self.assertEqual((report.eligible, report.rejected), (1, 1))
        self.assertEqual(report.cohort.display_timezone, "Asia/Kolkata")
        self.assertEqual(self.reviews.report("alice", "case-a", cohort(source_version_ids=["absent"])).eligible, 0)
        before = self.reviews.report("alice", "case-a", cohort(cutoff="2026-10-10T10:30:00Z"))
        self.assertEqual((before.pending, before.review_coverage, before.approval_rate), (1, 0, None))

    def test_save_failure_keeps_previous_outcome(self):
        from unittest.mock import patch
        value = self.save()
        self.final(value)
        with patch.object(self.store, "transaction", side_effect=OSError("unavailable")):
            with self.assertRaises(OSError):
                self.final(value, "rejected", 1, "k2")
        self.assertEqual(self.reviews.report("alice", "case-a", cohort()).approved, 1)

    def test_cohort_timezone_and_unknown_fields(self):
        for changes in ({"start": "2026-10-10T10:00:00"}, {"display_timezone": "invalid/zone"},
                        {"start": cohort().end}, {"end": cohort().start}):
            with self.assertRaises(ValidationError):
                cohort(**changes)

    def test_late_presentation_cannot_rewrite_previous_cutoff(self):
        past = cohort(cutoff="2026-10-10T10:30:00Z")
        self.assertEqual(self.reviews.report("alice", "case-a", past).eligible, 0)
        self.reviews.admit("alice", "case-a", "run0", "snap-1", "controlled_simulation")
        saved = self.reviews.present("alice", "case-a", item())
        self.assertEqual(saved.available_at, self.now)
        self.assertEqual(self.reviews.report("alice", "case-a", past).eligible, 0)

    def test_run_provenance_and_nonblank_content(self):
        self.reviews.admit("alice", "case-a", "run0", "snap-1", "controlled_simulation")
        for changes in ({"run_id": "absent"}, {"model_id": "wrong"}, {"prompt_version": "wrong"},
                        {"data_mode": "live"}):
            with self.assertRaises(ContractError):
                self.reviews.present("alice", "case-a", item(**changes))
        for changes in ({"rationale": " \r\n"}, {"recommendation": "\t"}):
            with self.assertRaises(ValidationError):
                ReviewContent(**(item().original_content().model_dump() | changes))
