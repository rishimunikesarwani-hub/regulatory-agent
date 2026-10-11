# VS5 local worker supervision

Date: 2026-10-11.
Authorization: D42 permits local VS5 development.
Parent contracts: [Pipeline](spec-slice-05-pipeline.md) and [Technical Blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md#7-retries-and-failures).

A supervisor is a separate process that controls the assessment worker.
Use Python process controls without another dependency.
Keep this local adapter separate from the future AWS queue and Lambda adapter.

## Execution controls

Authorize the owner and case before starting a worker.
Reserve the existing conditional execution claim in the supervisor.
Pass that claim to the pipeline without a second claim operation.
Construct native SDK clients inside the worker.
Never accept a worker function or AWS profile from uploaded content.

Keep the original 600-second deadline and saved allowance counters.
Include process startup time in the remaining deadline.
Use a monotonic clock for the remaining wait.
Renew the execution lease while the supervisor waits.
Do not renew the deadline or model allowance.

When the deadline expires, stop the child process before finalizing the job.
Keep saved findings, validated stages, and dispatched-call reservations.
Keep unreturned usage unknown.
Mark unfinished audit attempts interrupted with a safe reason.
Save partial results when accounted obligations exist.
Otherwise, save a failed job with every selected obligation unchecked.

Reject late writes and stale supervisor claims.
Keep duplicate deliveries from starting a competing worker.
Do not run another assessment after a worker crash in the same delivery.
Discard child console output, including exception text.
Do not report success from a process exit code alone.

## Acceptance checks

| Check | Required behavior |
|---|---|
| VS5-W01 | A controlled pipeline completes in a spawned child with the parent's execution claim. |
| VS5-W02 | A hung child stops at the remaining deadline without a late stage write. |
| VS5-W03 | Timeout preserves accounted results, dispatched calls, unknown usage, and unchecked scope. |
| VS5-W04 | A crashed child cannot become a completed job or expose exception text. |
| VS5-W05 | Wrong ownership, active duplicate delivery, and terminal delivery start no child. |
| VS5-W06 | An already exhausted deadline starts no child and preserves the original start time. |
| VS5-W07 | Lease renewal cannot change the deadline, counters, or a newer claim. |
| VS5-W08 | A stale supervisor cannot change a replacement worker's job. |
| VS5-W09 | Audit persistence failure cannot produce a completed job. |

Write failing checks before implementation.
Use shortened remaining time on the existing saved 600-second budget for local timeout checks.
Do not use a new application timeout setting for those checks.

## Evidence limits

These checks verify local process controls with controlled model responses.
They do not establish live model quality or deployed AWS timeout behavior.
Catastrophic supervisor termination and operating-system failure remain outside these local checks.
The AWS adapter still needs infrastructure timeout and queue retry verification.
General admission, source selection, and current verification remain separate unfinished work.

## Language review

Use ASD-STE100 Issue 9 and the project glossary.
Keep claims, deadlines, permissions, and evidence limits unchanged.
Save the separate language review receipt.
