# VS5 native admission and queue execution

Date: 2026-10-11.
Authorization: D42 permits VS5 development within the approved AWS architecture.
Parent contracts: [Cloud jobs](spec-slice-05-cloud-jobs.md) and [cloud records](spec-slice-05-cloud-records.md).

## Admission

Use the shared selection rules for historical regulations and fictional bank documents.
Read every passage from the selected bank version before admission.
Keep the public document endpoint paginated.
Verify the original bank bytes against the saved hash before processing.
Store regulatory originals in private, versioned S3 objects.
Keep the original references unchanged when admission repeats.
Reject changed selections with an existing admission key.
Save the snapshot, job, and run before queue delivery.
Verify that the run snapshot equals the job's pinned snapshot before processing or delivery.
Keep current-source verification unavailable until D20 passes.

## Delivery

Use a standard SQS queue in Mumbai in the configured development account.
Use one SDK attempt for each explicit send operation.
Send only the protocol version, owner identifier, case identifier, and job identifier.
Do not send bank text, model configuration, credentials, or executable instructions.
An uncertain send acknowledgement must preserve the saved admission.
A repeated request can send the same job again.
The conditional job claim prevents concurrent execution of duplicate deliveries.
Do not send a terminal job again.

Validate the event source, queue ARN, message identity, and body before constructing SDK clients.
Process one message per invocation.
Return failed message identifiers through the Lambda partial batch response.
Do not acknowledge a delivery whose execution or finalization remains uncertain.
Do not log message bodies or private exception text.

## Worker

Use the existing process supervisor with native persistence for cloud finalization.
Construct model and storage clients inside the child from trusted server configuration.
Stop the child before the invocation returns.
Do not use a multiprocessing queue or pool.
Keep the original job deadline and call counters during recovery.
Check the invocation time before obtaining an execution claim.
Leave a job available for another delivery when invocation time is insufficient.
Finalize an expired job without starting model processing.
Keep saved results and unchecked obligations when processing stops.
Reject finalization from a replaced execution claim.
An interrupted dispatch with incomplete audit evidence must show an unknown live-call count.

The worker needs 600 seconds for processing and additional time for cleanup.
D30 prohibits reserved concurrency for this account's first deployment.
Do not change the account quota.

## Acceptance checks

| Check | Required behavior |
|---|---|
| VS5-CE01 | Native admission saves historical originals, selected versions, and one immutable run without SQLite. |
| VS5-CE02 | Repeated admission keeps original S3 references. Changed selection conflicts. |
| VS5-CE03 | Bank reads include all pages. Corrupt original bytes prevent processing. |
| VS5-CE04 | Current mode and wrong ownership cannot admit or send work. |
| VS5-CE05 | Native SQS request shapes pass. Invalid region, endpoint, account, or retry configuration fails. |
| VS5-CE06 | Queue bodies contain only identifiers. Lost acknowledgements preserve one saved admission. |
| VS5-CE07 | Terminal jobs do not send. Active duplicates cannot obtain another claim. |
| VS5-CE08 | Invalid queue events fail before service construction. Responses identify failed messages. |
| VS5-CE09 | Worker delivery uses the saved native run and the shared processing rules. |
| VS5-CE10 | Insufficient invocation time starts no child and does not reset the saved job. |
| VS5-CE11 | Expired jobs finalize without inference. Partial results and counters remain unchanged. |
| VS5-CE12 | Unknown attempts become interrupted. Incomplete dispatch evidence remains unknown. |
| VS5-CE13 | Replaced claims reject cleanup writes and finalization. Uncertain storage errors require redelivery. |
| VS5-CE14 | A real supervised child stops at the deadline without a late write or private console output. |
| VS5-CE15 | A changed run snapshot cannot replace the job's original snapshot during delivery or processing. |

Write failing checks before implementation.
Use controlled native SDK responses without external traffic or live inference.
These checks do not establish deployed Lambda acceptance or live assessment quality.
Cloud assessment routes and deployment resources require separate integration checks before activation.

## AWS references

[SQS error handling](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html) describes partial batch responses.
[SQS configuration](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-configure.html) describes timeout and queue visibility conditions.
[Python processes](https://aws.amazon.com/blogs/compute/parallel-processing-in-python-with-aws-lambda/) describes process support and shared-memory limitations.

Vocabulary review is incomplete.
Manual review must preserve ownership, uncertainty, limits, and release conditions.
