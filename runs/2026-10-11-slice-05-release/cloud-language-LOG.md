
## 2026-10-11 - Native cloud job state

The cloud job component stores conditional metadata, claims, and counters through native DynamoDB calls.
The existing private S3 adapter keeps versioned snapshots and stage outputs.
Failing tests reproduced stale clock checks and false dispatch accounting after reservation storage.
The correction preserves the consumed allowance and records known absence of dispatch separately.
D50 records this clarification within the approved VS5 and AWS scope.
Queue, cloud API, review, worker, source, live quality, and AWS acceptance remain unfinished.
