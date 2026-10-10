# Security & Access

> Status: Approved in the planning conversation. First saved on 2026-10-08.
> Required document: [Technical Blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md).
> Decisions: [D05, D09, and D10](../decisions/gov-decision-log.md).
> Verification: These are requirements. No deployed security control has a test result.
> Language revision: 2026-10-09.

The application needs document access for assessments.
A document or model response cannot grant additional access or tool permissions.

## 1. Authentication

Use Cognito authorization-code sign-in with PKCE.
PKCE protects the sign-in code exchange.
Keep access tokens in browser memory.
Disable public sign-up for the demo.

The API must validate authentication.
It must get user identity from the verified token.
It must not trust an owner_id from a request body.

Use an explicit development identity for local operation.
Restrict that identity to local mode and loopback access.
Reject a cloud configuration that enables this bypass.


## 2. Roles and permissions

| Role | Permitted actions | Prohibited actions |
|---|---|---|
| Authenticated operator | Create own cases. Upload authorized files. Run assessments. Inspect sources. Record reviews. Export own reports. | Access another operator's case. Change historical document versions. Add agent tools without approval. |
| Unauthenticated visitor | Load public application assets and the sign-in page. | Read cases, job states, evidence, or reports. |
| Deployment administrator | Configure AWS infrastructure with reviewed permissions. | Bypass normal user ownership rules. Expose private content through public assets. |

The first release permits the same operator to review their own assessment.
Record the human review accurately.
Do not claim independent four-eyes approval.

## 3. Data access and processing regions

| Data | Access rule |
|---|---|
| Cases and bank profiles | Authenticated owner only |
| Original documents and extracted passages | Owner authorization required. Use private storage and an explicit version. |
| Jobs, snapshots, and findings | Use owner-scoped APIs. Restrict the worker to required resources. |
| Review decisions | Authorized case owner only. Keep the original AI finding. |
| Exports | Use an authorized snapshot. Keep source and version references. |
| Public frontend assets | CloudFront can serve these assets. Do not include private documents or reports. |

Store private documents, records, and application logs in Mumbai.
The approved model profile can use Mumbai and Hyderabad only.
Verify its actual destinations and permissions before private uploads.

Encrypt data during transfer and storage.
Block public access to the document bucket.
Grant service roles only the required permissions.
Authorize each download through an ownership check.
Use download links with a short validity period.
Do not cache private assessments at a public edge.

Operational logs can contain identifiers, stages, durations, error classes, and call counts.
Do not include full documents, prompts, responses, tokens, or credentials.
Do not enable raw model invocation logs by default.
Review service retention terms during T8.

Do not use real bank files as development fixtures or tracked source files.
Explain retention and deletion during deployment.
No automatic deletion schedule has approval.

### External regulatory API

Send only public regulatory identifiers, public topics, and public source URLs.
Do not send bank profiles, private documents, evidence, findings, owner IDs, or private prompts.
Keep the India-only boundary for private content.

Permit only configured HTTPS API endpoints and approved authority domains.
Reject arbitrary hosts, private network addresses, and unapproved redirects.
Do not let document text or the model select new destinations.
Keep provider credentials in server-side secret storage.
Do not expose them in browser assets or logs.

Treat retrieved text as untrusted evidence.
Verify its authority, version metadata, and current-source check.
Reject snippets, incomplete responses, or unknown freshness for a current assessment.
Apply bounded requests, retries, timeouts, pagination, and response sizes.

## 4. Upload and extraction limits

| Item | Approved requirement |
|---|---|
| Formats | English text PDF, DOCX, TXT, and CSV |
| Number | At most 10 documents per case |
| File size | At most 10 MB per file |
| Extracted scope | At most 100 extracted document pages per case |
| Assessment scope | At most 20 explicitly selected obligations |
| Unsupported inputs | Scanned, unreadable, encrypted, oversized, or unsupported files |

Validate file contents as well as extensions.
An upload success does not prove extraction success.
Exclude unvalidated input from retrieval.

Do not silently truncate documents.
Do not imply full coverage when only part of a document is readable.
Explain the rejection or request a smaller supported source.

**T2 implementation detail:** DOCX, TXT, and CSV do not have reliable fixed page counts.
Define an extracted-size equivalent before claiming enforcement of the aggregate page limit.
Keep the approved size limits.
Use paragraph, line, and row references for these formats.
Do not invent PDF page numbers.

## 5. Agent authority and allowances

- Limit reads to the current case and selected snapshot.
- Limit writes to assessment and progress records.
- Do not treat document text as instructions or permissions.
- Do not execute commands or retrieve arbitrary URLs.
- Do not send messages, publish content, or change real bank controls.
- Limit each job to 24 model requests.
- Limit processing to ten minutes from worker start.
- Keep the allowance and deadline through retries and queue redelivery.
- Count malformed responses, rejected actions, and uncertain dispatched calls.
- Show the stop reason and unchecked obligations.
- Do not report an exhausted partial job as completed.

Provider safety functions do not replace application authorization or citation validation.
They do not replace prompt-injection tests.

## 6. Assessment and review rules

A policy statement is evidence of the stated policy.
It does not establish operational execution.

If required evidence is missing, use needs_review.
Identify the required evidence.
Conflicting relevant evidence prevents a supported finding.

A control gap must identify an evidenced shortfall.
An evidence gap must identify missing information.
Uncertain applicability cannot justify a supported result.

Use agree, disagree, or request_more_evidence for reviewer dispositions.
Record a note, reviewer identity, and time.
Keep the original AI result.
A review decision does not authorize changes to bank systems.

## 7. Failures

| Failure | User information | Saved information |
|---|---|---|
| Invalid or unsupported file | File-specific reason and a supported next action | Error class, source ID, and validation stage |
| Missing or conflicting evidence | Needs review. Identify the affected evidence. | Finding status, evidence condition, and valid source references |
| Malformed AI output or false citation | A limited retry. Then a visible failure or partial result. | Validation failure and remaining allowance. No raw private output. |
| Regulatory retrieval unavailable or outdated | Block a current assessment. Show the last successful check. | Source identity, verification state, and safe failure reason |
| Model or service unavailable | Keep inputs. Offer a retry when the allowance permits it. | Failed stage, attempt ID, and consumed allowance |
| Storage unavailable | No success claim. Keep safe form input where possible. | Safe error class and correlation ID |
| Rate limit | Wait or retry information. No false progress. | Retry data and remaining deadline |
| Duplicate message | Existing progress or result. No second assessment. | Execution claim and finalization result |
| Unauthorized request | Access denied. No case-content disclosure. | Minimal access-denial event |
| Exhausted allowance | Partial or failed status. Show unchecked work. | Saved counter, deadline, and completed stage outputs |

Do not display raw stack traces.
Keep safe user input where possible.
State the next action.

## 8. Required negative tests

The local test plan covers these cases:

- Requests for another case's objects.
- Altered owner fields.
- Invalid tokens.
- A cloud configuration with development identity.
- Source instructions that request prohibited actions.
- Invented citations.
- Missing or stale evidence.
- Repeated delivery.
- Exhausted allowances.
- Malformed files.

Live checks must verify IAM permissions, storage privacy, Cognito, inference destinations, and service connections.
Verify the regulatory provider's authority coverage and request privacy separately.
Local substitutes cannot prove that these cloud controls work.

[Next: Frontend specification](../frontend/04_FRONTEND_SPEC.md)
