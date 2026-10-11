# Native admission and execution review

Date: 2026-10-11.
Contract: [VS5 native execution](../../docs/delivery/spec-slice-05-cloud-execution.md).

## Verified behavior

The first 14 checks failed before implementation.
The missing native component and supervisor arguments caused those failures.
CE09 then reproduced an acknowledgement without saved terminal state.
The correction reads the durable job state before acknowledging a message.
CE15 reproduced a changed run snapshot that differed from the job's original snapshot.
The correction compares both immutable snapshots before delivery and processing.
All 15 focused checks passed after those corrections.
The final local suite passed 343 backend checks in 184.613 seconds.
The browser suite passed 51 checks.
The frontend build passed in 254 milliseconds.

Native admission uses the existing selection rules with private S3 originals and DynamoDB records.
Identical admission preserves the original object versions and one run.
Changed selection conflicts with the existing admission key.
The internal bank read includes all 510 test passages and verifies the pinned original.
The public document endpoint retains its 500-passage page.
Corrupt original bytes prevent admission.

The SQS adapter validates native request shapes, Mumbai configuration, account identity, and one SDK attempt.
Messages contain identifiers only.
An uncertain send acknowledgement keeps the saved admission available for the same-key retry.
Invalid events fail before constructing the service.
Terminal deliveries do not start processing.
Uncertain processing requires redelivery.

Native cleanup preserves saved findings, counters, the original deadline, and unchecked obligations.
An expired delivery starts no child.
A replaced claim cannot finalize the old execution.
Interrupted model attempts retain unknown usage and unknown dispatch counts when audit evidence is incomplete.
The shared supervisor stops a real local child without a late write.

## Evidence limits

The native service checks use controlled DynamoDB, S3, and SQS responses.
The process check uses local persistence to observe child termination across a real process boundary.
It does not establish hosted Lambda process acceptance.
Existing controlled pipeline checks cover native complete and partial assessments.
These checks do not establish live model quality.

Cloud assessment API routes, source packaging, queue resources, event-source mapping, and worker IAM still require integration.
Cloud routes remain disabled.
No AWS resources changed during this work.
No live inference occurred.
Provider selection, current-source verification, live quality, and deployed acceptance remain pending.
VS5 remains an open draft under D35.

## Language and meaning review

Instruction and descriptive sentence lengths received a mechanical check.
Manual review preserves ownership, snapshot binding, retries, uncertainty, and release conditions.
Technical terms use the existing project glossary.
The regulatory API research now uses the verified RBIH domain and identifies the earlier affiliation uncertainty.
The dictionary and approved-meaning review is incomplete.
This review does not claim full ASD-STE100 compliance.
