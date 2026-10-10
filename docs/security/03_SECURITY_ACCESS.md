# Security & Access

> Status: Approved in the planning conversation. First saved on 2026-10-08.
> Required document: [Technical Blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md).
> Decisions: [D05, D09, D10, and D24](../decisions/gov-decision-log.md).

> Verification: These are requirements. No deployed security control has a test result.
> Language revision: 2026-10-10.

Document access is necessary for application assessments.
A document or model response cannot give more access or tool permissions.

## 1. Authentication

Use Cognito authorization-code sign-in with PKCE.
PKCE protects the sign-in code exchange.
Keep access tokens in browser memory.
Disable public sign-up for the demo.

The API must validate authentication.
It must get user identity from the validated token.
It must not trust an owner_id from a request body.

For local operation, use a specified development identity.
Restrict that identity to local mode and loopback access.
Reject a cloud configuration that enables this bypass.


## 2. Roles and permissions

| Role | Permitted actions | Prohibited actions |
|---|---|---|
| Authenticated operator | Make own cases. Upload authorized files. Do assessments. Examine sources. Record reviews. Export own reports. | Get access to a different operator's case. Change historical document versions. Add agent tools without approval. |
| Unauthenticated visitor | Load public application assets and the sign-in page. | Read cases, job states, evidence, or reports. |
| Deployment administrator | Configure AWS infrastructure with reviewed permissions. | Bypass normal user ownership rules. Expose private content through public assets. |

The first release lets the same operator do the review of their own assessment.
Record the human review accurately.
Do not claim independent four-eyes approval.

## 3. Data access and processing regions

| Data | Access rule |
|---|---|
| Cases and bank profiles | Authenticated owner only |
| Original documents and extracted passages | Owner authorization is mandatory. Use private storage and a selected version. |
| Jobs, snapshots, and findings | Use owner-scoped APIs. Restrict the worker to necessary resources. |
| Review decisions | Authorized case owner only. Add review events. Keep original findings and recommendations. |
| Review edits and reasons | Store in authorized private case evidence. Do not include in operational logs. |
| Stage traces and metric reports | Validate case ownership. Send controlled metadata and authorized artifact references. |
| Exports | Use an authorized snapshot. Keep source and version references. |
| Public frontend assets | CloudFront can serve these assets. Do not include private documents or reports. |

Store private documents, records, and application logs in Mumbai.
The approved model profile can use Mumbai and Hyderabad only.
Before private uploads, do checks of the profile's destination regions and permissions.

Encrypt data during transfer and storage.
Block public access to the document bucket.
Give service roles only the necessary permissions.
Authorize each download through an ownership check.
Use download links with a short validity period.
Do not cache private assessments at a public edge.

Operational logs can contain controlled identifiers, stages, durations, safe error classes, call counts, and numeric model-token counts.
Do not include private text, raw prompts, raw responses, authentication tokens, credentials, or hidden model reasoning.
Keep source text, query text, review edits, and review reasons in authorized case evidence storage in Mumbai.

Treat record identifiers as controlled metadata, not as unrestricted public information.
Keep unknown usage and cost fields unknown.
Do not enable raw model invocation logs by default.
Examine service retention terms during T8.

Do not use files from banks as development fixtures or tracked source files.
Explain retention and deletion during deployment.
No automatic deletion schedule has approval.

### External regulatory API

Send only public regulatory identifiers, public topics, and public source URLs.
Do not send bank profiles, private documents, evidence, findings, owner IDs, or private prompts.
Keep the India-only boundary for private content.

Only configured HTTPS API endpoints and approved authority domains are permitted.
Reject arbitrary hosts, private network addresses, and unapproved redirects.
Do not let document text or the model select new destinations.
Keep provider credentials in server-side secret storage.
Do not expose them in browser assets or logs.

Treat retrieved text as untrusted evidence.
Do checks of its authority, version metadata, and current-source check.
Reject snippets, responses with missing content, or unknown freshness for a current assessment.
Apply bounded requests, retries, timeouts, pagination, and response sizes.

## 4. Upload and extraction limits

| Item | Approved requirement |
|---|---|
| Formats | English text PDF, DOCX, TXT, and CSV |
| Number | At most 10 documents per case |
| File size | At most 10 MB per file |
| Extracted scope | At most 100 extracted document pages per case |
| Assessment scope | At most 20 obligations that the user selects |
| Unsupported inputs | Scanned, unreadable, encrypted, oversized, or unsupported files |

Validate file contents as well as extensions.
Upload success is not proof of extraction success.
Do not include unvalidated input in retrieval.

Do not truncate documents without a warning.
Do not imply full coverage when only part of a document is readable.
Explain the rejection or request a smaller supported source.

**T2 implementation detail:** DOCX, TXT, and CSV do not have reliable fixed page counts.
Before you claim enforcement of the total page limit, set an extracted-size equivalent.
Keep the approved size limits.
Use paragraph, line, and row references for these formats.
Do not invent PDF page numbers.

## 5. Agent authority and allowances

- Limit reads to the current case and selected snapshot.
- Limit writes to assessment and progress records.
- Do not treat document text as instructions or permissions.
- Do not execute commands.
- Do not retrieve URLs outside the permitted set.
- Do not send messages.
- Do not publish content.
- Do not change controls in bank systems.
- Limit each job to 24 model requests.
- Limit processing to ten minutes from worker start.
- Keep the allowance and deadline through retries and queue redelivery.
- Count malformed responses, rejected actions, and uncertain dispatched calls.
- Show the stop reason and unchecked obligations.
- If a partial job has no remaining allowance, do not show it as completed.

Provider safety functions do not replace application authorization or citation validation.
They do not replace prompt-injection tests.

Start with one bounded agent and the approved pinned model.
Do not enable automatic model routing or an autonomous second reviewer in the baseline.
Use observed failures to set subsequent experiments as specified in the [measurement contract](../testing/spec-measurement-contract.md#5-development-and-controlled-improvement).
Before private use, do checks of candidate destinations, permissions, and tool compatibility.
Experiments keep the total job limits and do not authorize automatic adoption.

## 6. Assessment and review rules

A policy statement is evidence of the stated policy.
It is not proof of operational execution.

If necessary evidence is missing, use needs_review.
Identify the necessary evidence.
Conflicting evidence related to the requirement prevents a supported finding.

A control gap must identify a shortfall with evidence.
An evidence gap must identify missing information.
If applicability is uncertain, a supported result is not permitted.

REQ-X07/AC-X07 uses approved, edited, and rejected as final reviewer outcomes.
The [measurement contract](../testing/spec-measurement-contract.md#1-product-metric-and-review-unit) gives their meaning and reporting rules.
Keep one immutable finding and primary recommendation per selected obligation and run.
Only the authenticated case owner can save a human review outcome.
An agent cannot submit that outcome as human approval.

Approved always means acceptance of the original AI item.
Acceptance of an existing edited revision stays edited.
After an edit, the reviewer must select the original item to save approved.
Before you save approved, validate accepted content against the original item.

An edited outcome must contain saved changed content and a nonblank reason.
Before you compare content for changes, normalize outer whitespace and line endings.
A rejected outcome must contain a nonblank reason.
The request_more_evidence action stays pending unless the reviewer saves a final outcome.
A comment or unsaved draft cannot count as an edited outcome.

Record reviewer identity, UTC time, event identity, and idempotency key.
Use server commit time and a strictly increasing per-item revision for authoritative event order.
Reject stale writes against an unexpected current revision. Do not trust a client timestamp to order reviews.

Add new review events. Do not change previous events or original AI content.
Reject repeated requests that change the payload with the same idempotency key.
Identical retries must have one saved effect.

Use the last saved final event at the report cutoff for each eligible item.
Keep previous events to make reproduction of previous reports possible.
Do not count revisions or retries as more review items.
A new run must have its own review.
During an unsaved revision, the previous final outcome stays active.
A subsequent evidence request does not erase an existing final outcome.

Record metric_definition_version as d24-v1 with each outcome report.
Reviewer acceptance is product feedback, not proof of regulatory correctness or operational execution.
Approval of an evidence request is not proof that the bank meets the requirement.
Keep the same-operator limitation in outcome reports.
A review decision does not authorize changes to bank systems.

REQ-X08/AC-X08 makes per-stage traces with controlled metadata mandatory as specified in the [trace contract](../testing/spec-measurement-contract.md#4-runtime-traces-and-cost).
Keep stage and attempt identity through retries.
Record unknown or interrupted outcomes. Do not invent success.
Before you show completion, save the mandatory audit references and finalization data.

REQ-X09/AC-X09 makes different retrieval and assessment evaluations mandatory.
Use labeled public or fictional sources in development fixtures.
Do not use the evaluated model as the only authority for expected labels.
Validated references and fresh timestamps are not proof of full retrieval.
Human approval does not replace the existing reference-based quality gates.

## 7. Failures

| Failure | User information | Saved information |
|---|---|---|
| Invalid or unsupported file | File-specific reason and a supported next action | Error class, source ID, and validation stage |
| Missing or conflicting evidence | Needs review. Identify the affected evidence. | Finding status, evidence condition, and validated source references |
| Malformed AI output or false citation | A limited retry. Then a visible failure or partial result. | Validation failure and remaining allowance. No raw private output. |
| Regulatory retrieval unavailable or outdated | Block a current assessment. Show the last check that passed. | Source identity, verification state, and safe failure reason |
| Model or service unavailable | Keep inputs. If sufficient allowance is available, give a retry option. | Failed stage, attempt ID, and consumed allowance |
| Storage unavailable | No success claim. Keep safe form input where possible. | Safe error class and correlation ID |
| Audit-critical save unavailable | Do not show a completed auditable assessment. Keep recoverable progress. | Safe failure, stage references, and finalization state |
| Review save unavailable | The new outcome is not saved. Keep the previous final outcome. | Safe failure and review request identity |
| External metric export unavailable | Retry the export. Do not repeat the assessment. | Stable metric-event identity and safe export failure |
| Rate limit | Wait or retry information. No false progress. | Retry data and remaining deadline |
| Duplicate message | Existing progress or result. No second assessment. | Execution claim and finalization result |
| Unauthorized request | Access denied. No case-content disclosure. | Minimal access-denial event |
| No remaining allowance | Partial or failed status. Show unchecked work. | Saved counter, deadline, and completed stage outputs |

Do not show raw stack traces.
Keep safe user input where possible.
Give the next action.

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
- Allowances with no remaining calls or time.
- Malformed files.
- Forged review identity or access to another case's trace.
- An edited outcome without changed content or a reason.
- A rejected outcome without a reason.
- Repeated review requests or conflicting idempotency payloads.
- Private text or authentication tokens in operational telemetry.
- Audit-save failures that could incorrectly produce completed status.

The [local test plan](../testing/spec-local-test-plan.md) assigns tests for review outcomes, trace privacy, and audit failures.
The [measurement contract](../testing/spec-measurement-contract.md) controls their required behavior.

Live tests must include checks of IAM permissions, storage privacy, Cognito, inference destinations, and service connections.
Do different checks of the regulatory provider's authority coverage and request privacy.
Do checks of trace and review-data privacy in the deployed cloud configuration.
Local substitutes are not proof that these cloud controls work.

[Next: Frontend specification](../frontend/04_FRONTEND_SPEC.md)
