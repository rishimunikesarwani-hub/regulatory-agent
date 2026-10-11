Its checks cover routing, reservations, output validation, usage, deadlines, selected citations, and SDK configuration.

The [cloud job component](spec-slice-05-cloud-jobs.md) now stores conditional job metadata and counters through native DynamoDB calls.
It uses the existing private S3 adapter for exact snapshot and stage references.

Its controlled checks cover competing claims, uncertain acknowledgements, recovered leases, call allowances, and artifact integrity.
Storage completion triggers another clock check before inference.
An unused reservation remains consumed, but its known absence of dispatch is recorded separately.
Queue delivery, the cloud assessment API, cloud review records, and deployed acceptance remain unfinished.
