# Local test plan

> Status: Approved workflow and acceptance requirements. Implementation checklist saved 2026-10-08.
> Software tests executed so far: **none**. No application or test runner exists yet.
> Related: [tickets](../delivery/05_FEATURE_TICKETS.md), [architecture](../architecture/02_TECHNICAL_BLUEPRINT.md), [AI quality plan](eval-model-quality.md).

Tests must detect errors that affect review decisions. A returned value alone does not prove correct behavior. For example, a finding can cite the wrong document version.

## 1. Development loop

For each small behaviour:
1. Name the requirement and acceptance case.
2. Write a test that fails for the intended missing behaviour.
3. Record the failure before implementing the behaviour.
4. Implement the smallest change that satisfies the contract.
5. Run the relevant test and then the affected regression checks.
6. Refactor the code. Keep the required tests passing.
7. Record results and remaining limitations in runs/ and LOG.md.

T2 must define one runnable local check command and record exact versions. No command is advertised as available before it exists.

## 2. Local boundaries

- Run domain tests with controlled inputs and explicit expected outcomes.
- Test real local filesystem/SQLite adapters through the same contracts as AWS adapters.
- Stub AWS requests/responses for adapter contract checks. Do not interpret a stub as proof of real IAM or service behaviour.
- Use controlled model responses to cover malformed output, tool selection, retries, and evidence validation.
- Use controlled regulatory API responses. Default tests must not contact the provider.
- Browser tests may contact loopback services. Default tests block external network calls and need no AWS credentials.
- Verify the network guard inside actual test workers, not merely in a parent process.
- Use fictional documents only. Private uploads are never fixtures or CI artifacts.

**Plain explanation:** Tests give the application known problems. The results show whether the application follows the rules. Live AI quality needs a separate evaluation.

## 3. Domain tests

| Test ID | Requirement / acceptance | Scenario and required result |
|---|---|---|
| UT-01 | REQ-F01 / AC-F01 | Each supported format extracts text with stable source/version IDs and usable source locations. Synthetic labels survive. |
| UT-02 | REQ-F01, REQ-X01 / AC-X01 | Unsupported, empty, corrupt, encrypted, scanned/unreadable, or oversized files are rejected. Document/page/scope limits never silently truncate. |
| UT-03 | REQ-F03 / AC-F03 | Obligation extraction retains conditions, exceptions, applicability, and citations. Absent fields are unknown. |
| UT-04 | REQ-F04, REQ-F05 / AC-F04, AC-F05 | Documented controls retain their stated scope. A merely similar control is not sufficient coverage. |
| UT-05 | REQ-F06, REQ-F07 / AC-F06, AC-F07 | Policy-only, missing, conflicting, and mixed operational evidence produce the correct distinct statuses. No unsupported pass. |
| UT-06 | REQ-F08 / AC-F08 | A proposed remedy/evidence request refers to the actual finding and obligation. No action on bank systems occurs. |
| UT-07 | REQ-X01 / AC-X01 | Untrusted document instructions and unknown tool actions cannot expand scope or execute capabilities. |
| UT-08 | REQ-X03 / AC-X03 | An invented quote, a valid passage from a different version, or a quote from another case fails validation. |
| UT-09 | REQ-X01 / AC-X01 | Invalid JSON, rejected actions, timeouts, and uncertain dispatched calls consume the persisted allowance. Call 25 cannot be dispatched. |
| UT-10 | REQ-F01, REQ-F02, REQ-X03 / AC-F01, AC-F02, AC-X03 | A substantive change selects affected obligations/controls. Cosmetic wording changes do not automatically change the obligation. Snapshots remain immutable. Amendments and withdrawals create new version metadata. |
| UT-11 | REQ-X04 / AC-X04 | Deadline exhaustion preserves completed findings and lists unchecked work. Partial/failed jobs never masquerade as completed. |
| UT-12 | REQ-X05 / AC-X05 | Human disposition is stored separately. Disagreeing never erases the original finding or source history. |

## 4. Contract and integration checks

| Test ID | Requirement | Required result |
|---|---|---|
| CT-01 | REQ-F01, REQ-X06 | Local adapters satisfy shared contracts. Controlled model and regulatory API responses have explicit labels. |
| CT-02 | REQ-X02 | Read/write operations reject another owner's case IDs, source IDs, jobs, findings, and exports, including forged owner fields. |
| CT-03 | REQ-X04 | Duplicate requests/messages and concurrent claims produce one active execution and one finalization. Retry does not reset deadline/counters. |
| CT-04 | REQ-X03, REQ-X04 | A replacement uploaded during processing cannot alter the frozen snapshot. Process restart preserves stage outputs and version references. |
| CT-05 | REQ-F01, REQ-X05, REQ-X06 | API schemas, safe error responses, and exports match the contract. Partial exports stay partial. No external calls occur in default checks. Retrieval exports include verification metadata. |

The regulatory adapter contract must cover these cases:

- Current source responses and valid conditional responses.
- Cached provider content without an authority verification time.
- Missing amendments, withdrawals, or incomplete pagination.
- Changed selected versions before assessment.
- Future-effective amendments and historical assessment dates.
- Timeouts, denied credentials, rate limits, and exhausted retrieval allowances.
- Private query content, arbitrary hosts, private addresses, and unapproved redirects.
- A provider update during an active assessment.
- Restart without repeated source selection or reset retrieval counters.

Reject current-source claims without verification.
Keep active snapshots unchanged.
Never replace private upload limits with unlimited API responses.

A controlled AWS response tests the adapter. It does not prove that AWS accepts the role, request, or region. T8 verifies those conditions.

## 5. Browser checks

| Test ID | Scenario |
|---|---|
| BT-01 | Create/load a case. Refresh regulations. Upload bank files. Inspect extraction. Select obligations. Run an assessment. |
| BT-02 | Open a finding and exact citation. Save each review disposition. Export Markdown and JSON with the original snapshot. |
| BT-03 | Compare explicit regulatory versions, inspect affected controls, and retain the earlier assessment and review history. |
| BT-04 | Exercise empty, uploading, running, denied, partial, failed, invalid-citation, freshness-unverified, changed-selection, and retry states. Preserve entered review notes on failure. |
| BT-05 | Check keyboard focus and navigation, below-768-px layout, text status labels, Synthetic demo badges, and independent Simulated model labels. |

## 6. Live cloud checks — outside the default local suite

| Check ID | What must be observed in AWS |
|---|---|
| CLOUD-01 | Pinned model access, valid SDK/API request, actual inference-profile destinations limited to approved India regions, and a successful synthetic-input invocation |
| CLOUD-02 | Private S3 storage, authorized downloads, real case ownership enforcement, and no private content in frontend assets or operational logs |
| CLOUD-03 | Cognito sign-in and API token validation. Cloud startup/configuration rejects development identity |
| CLOUD-04 | Real SQS/worker/record-store behaviour, including duplicate delivery, persisted allowance, and observable partial/failure outcomes |
| CLOUD-05 | Deployed browser flow, SAM/resource review, spending controls, configuration/retention record, and guided deployment/rollback instructions. Verify real regulatory retrieval, authority synchronization, request privacy, and failure handling. |

Use separate invocation flags or commands for these checks. The default local command must never run them implicitly.

## 7. Acceptance and reporting

Record the run time, source revision or file hashes, environment, command, test IDs, passed/failed/skipped counts, and known limitations.

All required P0 cases must pass. Include skipped and unimplemented cases in the total case count. Do not count them as passes. Identify failures from the application, test harness, or unavailable cloud integration.

Save dated records of failing and passing tests. Exclude private prompt content. Keep logs outside the product UI. Run affected checks after changes. Add other checks when the change or an unresolved concern requires them.

Before delivery, verify the project from a clean source package or checkout. Use the documented dependencies. The recipient must not need ignored local files or an existing developer cache.

[Next: AI evaluation plan](eval-model-quality.md)
