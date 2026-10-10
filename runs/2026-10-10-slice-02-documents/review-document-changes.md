# Changed documentation text



### VS2 local document slice



The user approved VS1 locally and authorized VS2 while AWS verification is pending.

D35 controls the isolated branch, worktree, ports, and databases.

D36 and the VS2 source contract were recorded before implementation.

The new HTTP tests failed for missing document routes.

The browser tests failed for the missing document interface.

The port guard found the old API address before any writes.



Local upload now supports text PDF, DOCX, TXT, and CSV.

Each source version keeps its original bytes and exact text locations.

Replacements keep earlier versions accessible.

Case access checks apply to upload, inspection, replacement, and original download.

File and case limits reject excess input without a partial save.

One different extraction process stops after 10 seconds.

The timeout test failed before its safe rejection correction.

The uncertain-save test failed before its retry guard.



All 178 backend checks and 20 combined browser checks passed.

The frontend build passed.

The source screen was inspected in Chrome with the fictional policy fixture.

The feedback interface uses port `5182` and API port `8120`.

Its database is `runs/private/slice-02/feedback.sqlite`.

Browser tests use API port `8121` and their own database.

The VS1 feedback services and unrelated worktree changes stay unchanged.



Read the [local evidence](runs/2026-10-10-slice-02-documents/review-local.md) and [development guide](docs/delivery/guide-slice-02-development.md).

VS2 user acceptance and the integration merge stay pending.

AWS source adapters, service permissions, and deployed browser acceptance stay pending.

The Support verification request has not been sent by this session.

No cloud resources were deleted manually.



Next: obtain VS2 feedback and complete its checked integration merge.

Start VS3 locally only after that feedback permits it.

Keep the CloudFront verification handoff open.

## D36 - VS2 local source contract



Date: 2026-10-10.

Status: Implementation details within the user's approved VS2 local development.



Use the [VS2 contract](../delivery/spec-slice-02-documents.md) for upload and exact source-version inspection.

Combine local authorization, extraction, and finalization in one request.

Use SQLite transactions to keep original bytes and source versions unchanged.

Count saved replacement versions against the existing case allowance.

Keep the original page, paragraph, line, or row locations.

Use one bounded extraction process and the pinned `pypdf 6.20.0` parser.

Use the Python standard library for DOCX, TXT, and CSV.

Do not add assessment or regulatory retrieval behavior to this slice.

Keep private AWS upload and storage acceptance pending until the required cloud checks pass.



VS2 local implementation passed 178 combined Python checks and 20 combined browser checks.

VS2 user acceptance, integration merge, and AWS acceptance stay pending.

The [VS2 source contract](spec-slice-02-documents.md) defines the local document behavior.

- [x] Extracted-size and page-equivalent rules passed contract tests. VS2 local parsers and upload limits passed their API checks.

**Status:** In progress. Local bank-file upload and inspection passed VS2 checks. Regulatory retrieval and AWS source storage stay pending.

- [x] Local PDF, DOCX, TXT, and CSV keep the applicable source locations. AWS extraction checks stay pending.

- [x] Local input rejection gives safe reasons for tested invalid, encrypted, scanned, unreadable, unsupported, and oversized files.

- [x] Local file and aggregate limits apply without silent truncation. Concurrent upload checks passed.

The VS2 local case view now adds Documents and Source evidence panels.

The upload form shows format limits, document roles, replacement selection, and fictional-data confirmation.

The source panel shows the exact version, source locations, content hash, and original download.

Each replacement keeps the earlier version unchanged.

The selected version opens again after refresh and local sign-in.

An uncertain upload needs a document-list refresh before another upload.



The combined local browser suite passed 20 checks, including six document checks.

User acceptance and AWS document storage stay pending.

Regulatory retrieval, assessment execution, and comparison tabs stay pending.

Read the [VS2 contract](../delivery/spec-slice-02-documents.md) and [current browser result](../../runs/2026-10-10-slice-02-documents/browser-green-v2.txt).



The AWS development access setup is installed.

CloudFront distribution creation needs AWS account verification under D34.

The [verification guide](delivery/guide-aws-cloudfront-verification.md) gives the user's remaining Support steps.

The USD 25 monthly alert is configured and healthy.

The alert is not a spending cap.



The user approved VS1 locally and authorized VS2 local development.

The VS2 document flow passed 178 combined Python checks and 20 combined browser checks.

VS2 user acceptance and its integration merge stay pending.

AWS application acceptance stays pending.

Read the [VS2 development guide](delivery/guide-slice-02-development.md) for local review.

The [workspace guide](delivery/guide-slice-workspaces.md) controls the current branches, ports, and databases.

| Extraction | Software | Conversion of original file content to text with source locations. |

| Extraction unit | Software | A page equivalent under the approved document limits. PDF units also count actual pages. |

| Transaction | Database | An operation that applies related database changes together or keeps all changes out. |

| Upload | Software | Transfer of file bytes from the browser to authorized application storage. |
