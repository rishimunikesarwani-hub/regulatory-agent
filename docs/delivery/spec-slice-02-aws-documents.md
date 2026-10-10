# VS2 AWS document integration

Date: 2026-10-11.
Status: Development within the accepted VS2 flow. Cloud deployment and acceptance stay pending.

## Scope and isolation

Complete the approved document flow through Cognito, the cloud API, private S3 objects, and DynamoDB records.
Keep PDF, DOCX, TXT, CSV, source versions, original downloads, ownership checks, and existing limits.
Keep all application data and logs in Mumbai.
Keep private uploads disabled until the approved India checks pass.
Use fictional documents for development and initial deployment checks.

Use branch `work/t3-aws-documents` and worktree `.worktrees/regulatory-agent-t3-aws-documents`.
Reserve web port `5192`, feedback API port `8190`, and test API port `8191`.
Use `runs/private/slice-02-aws/browser-tests.sqlite` for browser tests.
Use `runs/private/slice-02-aws/feedback.sqlite` for feedback.
Keep the VS3 review worktree and its services unchanged.

## Transfer contract

The API authorizes the operator's case before any document operation.
It receives upload metadata, not the file bytes.
Use a signed S3 POST policy with an exact object key and file length.
A signed policy is a temporary permission for one specified browser upload.
Its validity is 300 seconds.
Its content-length condition must match the declared file size exactly.
Reject sizes above the approved 10,000,000-byte limit.
Use the existing filename, format, role, and fictional-data validation.

Do not put the filename in the S3 object key.
Use server-created upload identifiers within an owner and case prefix.
Require HTTPS and server-side encryption with SSE-S3.
SSE-S3 is S3-managed encryption of stored objects.
Require the configured AWS account, Mumbai bucket location, and enabled S3 versioning.
Configure the SDK with explicit endpoint `https://s3.ap-south-1.amazonaws.com` and signature version `s3v4`.
Set the SDK's S3 addressing style to `virtual`.
Reject a generated transfer link outside the bucket's exact Mumbai hostname.

After upload, get its actual S3 version identifier.
Read that exact version within the declared byte limit.
Close the response stream after every read or failure.
Calculate SHA-256 from the actual bytes.
Keep the key, version identifier, size, and hash in the authorized upload record.
Reject missing or `null` S3 version identifiers.
Later reads and downloads must use the saved version identifier.
They must not silently use the latest object version.

An original download needs case authorization and verified stored bytes.
Give it a version-specific signed GET link with 300-second validity.
Do not send a 10 MB file through the synchronous Lambda response.
Treat upload and download links as credentials.
Do not put them in operational logs or tracked evidence.

## Complete cloud flow

Save an idempotent upload reservation before giving temporary upload permission.
An idempotency key gives repeated requests one logical effect.
Complete finalization only after content validation and bounded extraction.
Reuse the accepted parser and exact source-location rules.
Keep original bytes and extracted evidence in private S3 storage.
Keep source metadata and aggregate counters in DynamoDB.
Commit the source record and counters atomically.
An atomic operation applies all its changes or none of them.

Keep at most 10 saved versions, 100 extraction units, and 400,000 extracted UTF-8 bytes per case.
Keep replacements and earlier versions unchanged.
Keep unfinished uploads out of assessment selection.
Repeated or uncertain finalization must not add another version or change counters twice.
Use safe failures and explicit recovery states.
Do not add automatic object deletion or retention expiry.

Add the necessary cloud routes and private storage configuration.
Give roles only the necessary Mumbai bucket and table permissions.
Enable the document interface in AWS mode after the adapters are connected.
Keep the local upload protocol unchanged.
Test complete upload, inspection, replacement, and download behavior before deployment.

## Storage acceptance cases

| ID | Behavior |
|---|---|
| VS2-S3-01 | Authorize the case before any S3 operation. Deny cross-owner and cross-case access. |
| VS2-S3-02 | Give temporary POST permission for the exact key, length, content type, and encryption settings. |
| VS2-S3-03 | Reject real-data flags, unsafe filenames, unsupported formats, and excessive size before S3 operations. |
| VS2-S3-04 | Reject a different client Region, bucket Region, account owner, or disabled versioning. |
| VS2-S3-05 | Keep the exact original version and hash after a later overwrite. |
| VS2-S3-06 | Reject missing versions, changed sizes, truncated streams, and stored hash mismatches. |
| VS2-S3-07 | Close response streams after successful reads and read failures. |
| VS2-S3-08 | Bind downloads to the authorized case and saved version. Keep filenames out of object keys. |
| VS2-S3-09 | Deny a forged stored key before a content read or signed download. |

Passing storage checks alone does not complete the AWS document flow.

## Cloud API contract

Use the existing Cognito access-token checks for every document route.
Use `POST /api/cases/{case}/uploads` for upload metadata and temporary permission.
Require `Idempotency-Key` for reservation requests.
Reuse that key after an uncertain response.
Reject the same key with different metadata.
Use `GET /api/cases/{case}/uploads/{upload}` for upload status.
Use `POST /api/cases/{case}/uploads/{upload}/finalize` after the S3 upload succeeds.
Use `POST /api/cases/{case}/uploads/{upload}/cancel` to release an unfinished reservation.
Cancellation changes metadata only. It does not delete stored objects.

Keep unfinished reservations separate from saved source metadata.
Count unfinished reservations toward the ten-version limit.
Keep each upload record separate from the case counters.
Use one conditional DynamoDB transaction for both records.
A revision condition prevents concurrent requests from overwriting another accepted change.
Keep finalization retries bound to the same upload identifier and original version.
Keep failed uploads out of the saved-version list.

Use `GET /api/cases/{case}/documents` to list saved versions.
Use `GET /api/cases/{case}/documents/{version}?offset={offset}` for source inspection.
Return at most 500 passages per inspection response.
Return the passage count, current offset, and next offset.
Keep passage identifiers and exact source locations stable across pages.
Do not remove passages or reduce the approved extraction limits.
Use `GET /api/cases/{case}/documents/{version}/original` for an authorized download link.
Keep upload permissions and internal storage references out of source lists.
Restrict case-list queries to records with the `CASE#` sort-key prefix.

## Cloud acceptance cases

| ID | Behavior |
|---|---|
| VS2-AWS-01 | Reject missing, expired, or cross-owner authorization before document storage access. |
| VS2-AWS-02 | Reserve once for repeated metadata. Reject changed metadata with the same key. |
| VS2-AWS-03 | Finalize once across retries and new service instances. Preserve original bytes, locations, and counters. |
| VS2-AWS-04 | Save replacement versions without changing earlier versions. Reject foreign replacement identifiers. |
| VS2-AWS-05 | Enforce concurrent reservation and aggregate extraction limits through conditional transactions. |
| VS2-AWS-06 | Exclude failed and unfinished uploads. Release cancelled reservations without object deletion. |
| VS2-AWS-07 | Handle an uncertain transaction acknowledgement without duplicate versions or counter changes. |
| VS2-AWS-08 | Page a large source without losing text or exceeding Lambda response limits. |
| VS2-AWS-09 | Bind artifacts and downloads to saved S3 versions. Reject changed hashes and storage failures safely. |
| VS2-AWS-10 | Keep case lists functional when upload and document records share the table. |
| VS2-AWS-BT01 | Upload directly to S3, finalize, inspect, reload, replace, and download in AWS mode. |
| VS2-AWS-BT02 | Resume an uncertain upload with its existing identifier. Preserve file selection until confirmation. |
| VS2-AWS-BT03 | Inspect all source pages through explicit navigation. |
| VS2-AWS-BT04 | Clear private source state when the authenticated session expires. |

Controlled cloud tests use isolated records and simulated service responses.
They do not prove a live AWS deployment or live Cognito sign-in.

## Integration focus regression

CI run `38084172144` found a keyboard-focus change while the case list completed its request.
The interface could move focus from a form control to the case heading.
This integration correction stays within the accepted case workflow.
Use branch `work/t3-aws-documents-focus` in the existing AWS preparation worktree.
Keep its test ports and test database unchanged.

VS1-BT04 delays the case-list response during form entry.
The user enters a name and moves to its confirmation checkbox.
Complete the response after the checkbox receives focus.
The checkbox must keep focus.
The user must then complete the save through keyboard controls.
Move focus to a loaded heading only when no application control has focus.
Keep the existing user-review checkpoints and AWS deployment conditions unchanged.

## Deployment and cost limits

CloudFront account verification and failed-stack recovery remain necessary before deployment.
Do not delete cloud resources manually without approval.
Keep the USD 25 monthly budget alerts.
Stored object versions, S3 requests, and data transfer can incur charges.
Each stored version has its own storage charge.
Preparation and controlled tests create no cloud resources.

Use access logging, CloudTrail data events, and CloudWatch metrics for deployed storage observability.
Keep private object contents and signed links out of those logs.
Encrypt log destinations and review their Mumbai location, permissions, and cost before activation.
Existing CloudTrail event history is not a durable trail or an S3 data-event audit.

## Verified AWS references

- [Lambda payload limits](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html) restrict synchronous requests and responses to 6 MB each.
- [S3 versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html) assigns identifiers to stored versions and charges for each version.
- [DynamoDB transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html) support atomic conditional writes.
- [S3 pricing](https://aws.amazon.com/s3/pricing/) gives storage, request, and transfer charges.
- [Approved source contract](spec-slice-02-documents.md) defines the document formats, extraction, limits, and version behavior.
