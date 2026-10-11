# VS5 cloud job state

Date: 2026-10-11.
Authorization: D42 permits VS5 development. The approved blueprint requires DynamoDB, S3, SQS, and a Lambda worker.
Requirements: REQ-X02, REQ-X03, REQ-X05, REQ-X07, and REQ-X08.
Parent contracts: [Worker](spec-slice-05-worker.md) and [release](spec-slice-05-release.md).

## Storage and admission

Store job metadata, execution claims, and counters in DynamoDB in Mumbai.
Use the existing private, versioned S3 adapter for immutable snapshots and stage outputs.
Keep large outputs outside DynamoDB items.
Keep their exact S3 versions, byte lengths, and hashes in the job record.
Authorize the owner and case before every operation.
Reject client configurations outside Mumbai.
Reject records whose saved owner, case, or job identity differs from the requested identity.

Use one deterministic job identity for each owner, case, and admission key.
An identical admission returns the existing job.
A changed snapshot or processing mode with the same key is a conflict.
Do not replace the original snapshot on retry.
Store only supported selected protocols and fictional inputs for this development release.
Keep current-source verification unverified.

## Execution and recovery

Use conditional DynamoDB writes to claim and change a job.
An active duplicate delivery cannot obtain another execution claim.
An expired lease permits recovery with a new claim.
Recovery preserves the original start time, deadline, counters, and saved stages.
Keep the existing 600-second deadline, 24 model calls, and 20 retrieval calls.
Reserve each call before dispatch.
Check the current time again after storage reads and before model dispatch.
Include failed and uncertain dispatches in the saved counters.
Do not retry an uncertain database acknowledgement as a new reservation.
Disable SDK write retries for the job metadata client.
Renew the lease without renewing the deadline or allowances.
Reject writes from an old execution claim.

Save a stage artifact before conditionally attaching its reference to the current job.
A lost claim cannot attach its artifact.
Keep an already saved stage unchanged.
Reject an output that accounts for an unselected obligation.
Finalize only with valid accounted and unchecked obligations.
Keep failed and partial finalization available after deadline exhaustion.
Reject completed finalization after the deadline.

## Acceptance checks

| Check | Required behavior |
|---|---|
| VS5-CJ01 | Identical admission keeps one job and one immutable snapshot. Changed admission conflicts. |
| VS5-CJ02 | Wrong ownership and altered saved identities cannot read or write job state. |
| VS5-CJ03 | Native SDK request shapes and Mumbai client restrictions pass controlled checks. |
| VS5-CJ04 | Competing claims produce one active execution. Lease recovery keeps the original allowance and deadline. |
| VS5-CJ05 | Concurrent reservations cannot exceed either call allowance. Uncertain acknowledgements preserve consumed counters. |
| VS5-CJ06 | Renewal preserves the deadline and rejects stale or exhausted claims. |
| VS5-CJ07 | Large stage outputs use exact private S3 references and remain immutable. |
| VS5-CJ08 | Lost claims cannot attach stage artifacts. Storage failures cannot produce saved-stage success. |
| VS5-CJ09 | Finalization preserves accounted results and rejects invalid or exhausted completion. |
| VS5-CJ10 | Terminal retries and incomplete reads cannot create a second execution or reveal unverified artifacts. |
| VS5-CJ11 | Slow storage reads cannot renew or reserve after the original deadline. Failure finalization remains available. |

Write failing checks before implementation.
Use controlled SDK responses without credentials or external traffic.

## Integration boundary

This component is part of the full cloud worker integration.
It does not replace the required SQS delivery, cloud assessment API, reviewer records, or deployed acceptance.
Keep cloud assessment routes disabled until that complete integration passes its checks.
Do not treat these local checks as AWS deployment or live model evidence.
Keep VS5 under the D35 review condition.

## Language review

Use ASD-STE100 Issue 9 and the project glossary.
Keep a separate language and meaning review receipt.
