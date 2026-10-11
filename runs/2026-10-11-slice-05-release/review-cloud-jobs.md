# Native cloud job review

Date: 2026-10-11.
Scope: VS5-CJ01 through VS5-CJ11, VS5-MT11, VS5-MT12, and VS5-PT18.

## Behavior evidence

The first eleven cloud job checks passed after the recorded missing-adapter failures.
Separate failing checks reproduced stale clock values after storage reads and model reservation writes.
A further failing check detected a consumed reservation incorrectly reported as live inference.
The corrections check time again and keep known absence of dispatch in the saved trace.
The consumed reservation remains saved.

The combined local backend suite passed 312 checks in 172.341 seconds.
The final focused cloud job suite passed eleven checks with the one-attempt SDK client restriction.
The default checker removed credentials and disabled external networking.
Native SDK parameter validation examined DynamoDB read and conditional write requests.
Native Bedrock requests used controlled SDK responses.
No live cloud or model request was made by these software checks.

The checks cover competing claims, concurrent allowance reservations, lost acknowledgements, and recovered execution leases.
Recovered jobs preserve the original start, deadline, counters, and stage references.
Large outputs remain in private, versioned S3 artifacts through the existing adapter.
The job record stores their references and accounting metadata.
Changed stages, wrong owners, forged job identities, and corrupted artifacts fail safely.
The completed state requires accounted selected obligations and a valid execution claim.

## Implementation references

[DynamoDB item limits](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Constraints.html) include attribute names and values in the item-size limit.
The metadata guard leaves room for those names and keys.
[Conditional writes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html) require the saved revision to match before replacement.
[SDK retry configuration](https://docs.aws.amazon.com/boto3/latest/guide/retries.html) counts the initial request in `total_max_attempts`.
The job metadata client requires `total_max_attempts=1`.

## Language and meaning review

Reference: ASD-STE100 Issue 9 and the project glossary.
Scope includes the cloud job contract, model changes, D50, the guide, ticket status, and new LOG entry.
Protected text includes SDK fields, requirement IDs, test IDs, Regions, model IDs, and saved allowance limits.
Manual review preserved ownership, immutable artifacts, deadline recovery, no hidden write retries, and the cloud integration boundary.
The complete dictionary meaning review remains incomplete.
This receipt does not claim full compliance or ASD approval.

## Integration limits

The component does not yet connect cloud API admission to SQS delivery and the complete assessment worker.
The cloud selection and source reader must validate exact owned document references before admission.
Cloud review, audit, result, and export integration remain unfinished.
Use a dedicated DynamoDB client with one SDK attempt for job metadata.
Do not reuse the existing case client with two SDK attempts for these writes.
Keep cloud assessment routes disabled until the complete integration passes its checks.

Provider selection, current-source verification, live quality gates, and AWS acceptance remain pending.
AWS authentication still needs renewal.
No CloudFront verification resolution has been confirmed.
VS5 remains a draft under D35.
