## D50 - Native cloud job state and pre-dispatch checks

Date: 2026-10-11.
Status: Implementation clarification within D42 and the approved AWS blueprint.
Requirements: REQ-X02, REQ-X03, REQ-X05, REQ-X07, and REQ-X08.

The [cloud job contract](../delivery/spec-slice-05-cloud-jobs.md) adds conditional DynamoDB metadata, claims, and allowance counters.
The existing Mumbai S3 adapter keeps exact immutable snapshots and stage artifacts.
Large outputs remain outside DynamoDB items.
Competing claims and lost acknowledgements cannot reset the saved deadline or counters.
The job client permits one SDK write attempt.

Storage completion triggers a fresh execution check before inference.
An unused reservation remains consumed when that check prevents dispatch.
The trace records the known absence of dispatch separately.
The live-call report uses saved dispatch records instead of the reserved-call counter.
The [model contract](../delivery/spec-slice-05-model.md) assigns the corresponding deadline and storage checks.

Controlled checks do not establish live cloud behavior, model quality, or deployed permissions.
The cloud job component does not replace the remaining queue, API, review, and worker integration.
Cloud assessment routes remain disabled until the complete integration passes.
Provider selection, live quality gates, and AWS account verification remain pending.
VS5 remains a draft under D35.
