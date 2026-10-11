# Local worker review

Date: 2026-10-11.
Contract: [Worker supervision](../../docs/delivery/spec-slice-05-worker.md).
Scope: Local process controls for admitted VS5 historical jobs.

The supervisor uses Python process controls and the existing SQLite store.
It passes its execution claim to the pipeline.
It renews the lease while preserving the deadline and counters.
It stops the child before saving a failed or partial state.
It saves interrupted audit records and job finalization in one transaction.

Saved findings and validated outputs remain available after timeout.
Dispatched calls stay counted.
Unreturned usage remains unknown.
The child discards console output and exception text.
Native client construction requires the approved fictional live data mode.

## Behavior evidence

| Record | Result |
|---|---|
| `worker-red.txt` | Nine checks failed because the implementation was absent. |
| `worker-first.txt` | Eight checks passed. The partial-result check used the wrong model stub method. |
| `worker-start-red.txt` | Eleven checks passed. A process-start failure left the job running. |
| `worker-green.txt` | All twelve checks passed after argument validation before startup. |
| `worker-claim-red.txt` | An empty inherited claim did not produce the required rejection. |
| `worker-claim-green.txt` | All thirteen worker checks passed after rejecting empty inherited claims. |
| `backend-worker-final.txt` | All 275 combined checks passed before the inherited-claim correction. |
| `backend-worker-claim-final.txt` | All 276 combined backend checks passed with the inherited-claim correction. |

Windows can launch a process before serializing its arguments.
The supervisor now validates arguments before startup.
The test uses an invalid trusted-code target to reproduce that startup condition.
The inherited-claim correction distinguishes an absent claim from an empty claim.

## Remaining conditions

These tests use fictional bank data and controlled model responses.
They do not establish contextual model quality.
General admission, source-selection integration, and current verification remain unfinished.
The local adapter does not establish deployed AWS timeout behavior.
Catastrophic supervisor termination and operating-system failure remain outside this evidence.
The AWS adapter needs infrastructure timeout and queue retry checks.

AWS authentication needs renewal.
No inference or deployment occurred during this work.
VS5 remains a draft under D35.

## Language and meaning review

Reference: ASD-STE100 Issue 9 and the project glossary.
Protected content includes identifiers, counts, durations, permissions, and evidence limits.
The manual review checked claims, deadlines, allowances, ownership, and failure states.
The review preserved the distinction between controlled software checks and live acceptance.

The complete dictionary meaning review remains incomplete.
Mechanical checker results are separate records.
This receipt does not claim full ASD-STE100 compliance.
