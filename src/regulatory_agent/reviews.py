"""D24 review service. All records use the existing case-owned SQLite transaction."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
import time
import uuid

from .contracts import (ContractError, ReviewCohort, ReviewDecision, ReviewItem, ReviewOutcomeReport,
                        ReviewRequest, RunCohort, RunMeasure, ResultCoverageReport)
from .local import encoded, identifier


def instant(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def counts(items, events):
    totals = Counter(event.disposition for event in events if event is not None)
    reviewed = sum(totals.values())
    eligible = len(items)
    return dict(eligible=eligible, reviewed=reviewed, pending=eligible - reviewed,
                approved=totals["approved"], edited=totals["edited"], rejected=totals["rejected"],
                approval_rate=totals["approved"] / reviewed if reviewed else None,
                edit_rate=totals["edited"] / reviewed if reviewed else None,
                rejection_rate=totals["rejected"] / reviewed if reviewed else None,
                adoption_rate=(totals["approved"] + totals["edited"]) / reviewed if reviewed else None,
                review_coverage=reviewed / eligible if eligible else None)


def result_coverage(runs, cohort):
    cohort = RunCohort.model_validate(cohort.model_dump())
    unique = {}
    for value in runs:
        run = RunMeasure.model_validate(value.model_dump())
        if run.run_id in unique and unique[run.run_id] != run:
            raise ContractError("conflicting_run_measure")
        unique[run.run_id] = run
    selected = [run for run in unique.values()
                if instant(cohort.start) <= instant(run.job_admitted_at) < instant(cohort.end)
                and instant(run.job_admitted_at) <= instant(cohort.cutoff)
                and (run.model_id, run.prompt_version, run.data_mode) ==
                    (cohort.model_id, cohort.prompt_version, cohort.data_mode)]
    denominator = sum(len(run.selected_obligations) for run in selected)
    numerator = sum(sum(instant(stamp) <= instant(cohort.cutoff) for stamp in run.presented_obligations.values())
                    for run in selected)
    # A newer state cannot establish the state at a historical cutoff.
    states = Counter(run.state if instant(run.state_recorded_at) <= instant(cohort.cutoff)
                     else "unknown" for run in selected)
    return ResultCoverageReport(cohort=cohort, admitted=len(selected), selected=denominator, presented=numerator,
                                unchecked=denominator - numerator,
                                result_coverage=numerator / denominator if denominator else None,
                                completed_share=states["completed"] / len(selected) if selected else None,
                                completed=states["completed"], failed=states["failed"], partial=states["partial"],
                                queued=states["queued"], running=states["running"], state_unknown_at_cutoff=states["unknown"])


class Reviews:
    def __init__(self, store, clock=None):
        self.store = store
        self.clock = clock or (lambda: datetime.now(timezone.utc))

    def admit(self, owner, case, run_id, snapshot_id, data_mode):
        """Bind a server-created run to its saved snapshot before presenting findings."""
        identifier(run_id)
        snapshot = self.store.get(owner, case, "snapshot", snapshot_id)
        if data_mode not in {"controlled_simulation", "offline_benchmark", "synthetic_live", "live"}:
            raise ContractError("invalid_data_mode")
        if snapshot["synthetic"] != (data_mode != "live"):
            raise ContractError("data_mode_snapshot_mismatch")
        now = self.clock()
        if now.utcoffset() is None:
            raise ContractError("server_clock_timezone_missing")
        job = self.store.enqueue(owner, case, snapshot_id, run_id, now=now.timestamp())
        body = dict(run_id=run_id, job_id=job["job_id"], snapshot_id=snapshot_id, data_mode=data_mode,
                    job_admitted_at=datetime.fromtimestamp(job["created_at"], timezone.utc).isoformat().replace("+00:00", "Z"),
                    model_id=snapshot["model_version"], prompt_version=snapshot["prompt_version"],
                    selected_obligations=snapshot["selected_obligations"])
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            old = db.execute("SELECT body FROM records WHERE case_id=? AND kind='run' AND id=?", (case, run_id)).fetchone()
            if old:
                if json.loads(old[0]) != body:
                    raise ContractError("immutable_run")
            else:
                self._insert(db, case, "run", run_id, body)
        return body

    @staticmethod
    def _records(db, case, kind):
        return [json.loads(row[0]) for row in db.execute(
            "SELECT body FROM records WHERE case_id=? AND kind=?", (case, kind))]

    @staticmethod
    def _item(db, case, finding_id):
        row = db.execute("SELECT body FROM records WHERE case_id=? AND kind='finding' AND id=?",
                         (case, finding_id)).fetchone()
        if row is None:
            raise ContractError("record_not_found")
        return ReviewItem.model_validate(json.loads(row[0]))

    def _history(self, db, case, finding_id):
        return sorted((ReviewDecision.model_validate(record) for record in self._records(db, case, "review")
                       if record["finding_id"] == finding_id), key=lambda event: event.revision)

    @staticmethod
    def _insert(db, case, kind, identity, body):
        text = encoded(body)
        if len(text.encode("utf-8")) > 400_000:
            raise ContractError("record_too_large")
        db.execute("INSERT INTO records VALUES (?,?,?,?)", (case, kind, identity, text))

    def present(self, owner, case, item, *, execution_token=None):
        item = ReviewItem.model_validate(item.model_dump())
        snapshot = self.store.get(owner, case, "snapshot", item.snapshot_id)
        selected_versions = {f"{name}:{version}" for name, version in snapshot["selected_versions"].items()}
        if item.obligation_id not in snapshot["selected_obligations"] or set(item.source_version_ids) != selected_versions:
            raise ContractError("item_snapshot_scope_denied")
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            row = db.execute("SELECT body FROM records WHERE case_id=? AND kind='run' AND id=?", (case, item.run_id)).fetchone()
            if row is None:
                raise ContractError("run_not_found")
            run = json.loads(row[0])
            if execution_token is not None:
                self.store._claimed(self.store._job(db, owner, case, run['job_id']), execution_token, time.time())
            if any(getattr(item, field) != run[field] for field in ("snapshot_id", "model_id", "prompt_version", "data_mode")):
                raise ContractError("item_run_mismatch")
            existing = self._records(db, case, "finding")
            for record in existing:
                if record["finding_id"] == item.finding_id:
                    if record != item.model_copy(update={"available_at": record["available_at"]}).model_dump():
                        raise ContractError("immutable_record")
                    return ReviewItem.model_validate(record)
                if (record.get("run_id"), record["obligation_id"]) == (item.run_id, item.obligation_id):
                    raise ContractError("duplicate_review_item")
            now = self.clock()
            if now.utcoffset() is None or now < instant(run["job_admitted_at"]):
                raise ContractError("invalid_presentation_time")
            item = ReviewItem.model_validate(item.model_dump() | {"available_at": now.isoformat()})
            self._insert(db, case, "finding", item.finding_id, item.model_dump())
        return item

    def save(self, owner, case, finding_id, request):
        request = ReviewRequest.model_validate(request.model_dump())
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            item = self._item(db, case, finding_id)
            history = self._history(db, case, finding_id)
            # A delayed duplicate must return its original event before revision validation.
            for event in history:
                if event.idempotency_key == request.idempotency_key:
                    original = {key: getattr(event, key) for key in ReviewRequest.model_fields}
                    if ReviewRequest(**original) != request:
                        raise ContractError("idempotency_conflict")
                    return event
            revision = history[-1].revision if history else 0
            if request.expected_revision != revision:
                raise ContractError("revision_conflict")
            if request.disposition in {"approved", "edited"}:
                unchanged = request.accepted_content.normalized() == item.original_content().normalized()
                if request.disposition == "approved" and not unchanged:
                    raise ContractError("approval_requires_original")
                if request.disposition == "edited" and unchanged:
                    raise ContractError("edited_content_unchanged")
            now = self.clock()
            if now.utcoffset() is None:
                raise ContractError("server_clock_timezone_missing")
            now = now.astimezone(timezone.utc)
            if now < instant(item.available_at):
                raise ContractError("review_precedes_availability")
            if history:
                now = max(now, instant(history[-1].committed_at))
            event = ReviewDecision(**request.model_dump(), event_id=uuid.uuid4().hex,
                                   finding_id=finding_id, reviewer_id=owner, committed_at=now.isoformat(),
                                   revision=revision + 1)
            self._insert(db, case, "review", event.event_id, event.model_dump())
            return event

    def history(self, owner, case, finding_id):
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            self._item(db, case, finding_id)
            return self._history(db, case, finding_id)

    def report(self, owner, case, cohort):
        cohort = ReviewCohort.model_validate(cohort.model_dump())
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            items = [ReviewItem.model_validate(record) for record in self._records(db, case, "finding")]
            items = [item for item in items if instant(cohort.start) <= instant(item.available_at) < instant(cohort.end)
                     and instant(item.available_at) <= instant(cohort.cutoff)
                     and (item.model_id, item.prompt_version, item.data_mode) ==
                         (cohort.model_id, cohort.prompt_version, cohort.data_mode)
                     and (cohort.finding_status is None or item.status == cohort.finding_status)
                     and set(cohort.source_version_ids) <= set(item.source_version_ids)]
            latest, delays, groups = [], [], defaultdict(lambda: ([], []))
            for item in items:
                finals = [event for event in self._history(db, case, item.finding_id)
                          if event.event_kind == "final_review" and instant(event.committed_at) <= instant(cohort.cutoff)]
                final = finals[-1] if finals else None
                latest.append(final)
                if finals:
                    delays.append((instant(finals[0].committed_at) - instant(item.available_at)).total_seconds())
                group_items, group_events = groups[(item.status, final.reviewer_id if final else None)]
                group_items.append(item)
                group_events.append(final)
            return ReviewOutcomeReport(cohort=cohort, **counts(items, latest), review_delays_seconds=delays,
                                       status_reviewer_groups=[dict(finding_status=status, reviewer_id=reviewer,
                                                                    **counts(group_items, group_events))
                                                               for (status, reviewer), (group_items, group_events) in groups.items()])
