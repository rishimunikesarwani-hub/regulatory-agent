# VS5 comparison API and interface

Date: 2026-10-11.
Authorization: D42 permits REQ-F02 implementation.
Tickets: T3, T5, T6, T7, and T8.
Processing contract: [Saved comparison jobs](spec-slice-05-comparison-jobs.md).

The comparison interface connects saved version selection, bounded comparison jobs, and independent reassessment admission.
The accepted VS4 simulation keeps its separate local flow.
These routes use `/api/cases/{case_id}/regulatory-comparisons`.
They cannot establish current regulatory coverage or correct live interpretation from controlled checks.

## API

| Method and suffix | Request | Response |
|---|---|---|
| GET `/selection` | `snapshot_id` query | Baseline selection and eligible saved regulatory version metadata. |
| GET | None | Saved comparison summaries without internal artifact references. |
| POST | Existing `ComparisonRequest` | Saved comparison ID, job state, specified sources, progress, and safe results. |
| GET `/{comparison_id}` | None | Authorized comparison results, unchecked obligations, and numeric stage traces. |
| POST `/{comparison_id}/resume` | Empty JSON object | Saved comparison state after identifier-only queue delivery. |
| POST `/{comparison_id}/reassess` | `selection_reviewed: true` | Independent assessment admission. |

Require Cognito authentication and case ownership before native service construction.
Keep the existing disabled assessment flag for all native comparison routes.
Use the existing queue, worker, deadline, and permissions.
Add no AWS resource or dependency.
Keep local routes available only to the local development identity.

Build selection options from the baseline snapshot and owned saved regulatory records.
Require a completed, eligible historical assessment.
Show only permitted RBI authority sources with valid public metadata.
Do not use the latest catalog to replace a pinned baseline version.
Do not create a new source version from test text.

Save comparison admission before queue delivery.
Keep the same job after an uncertain acknowledgment and repeated request.
Return no execution token, original storage reference, or private control text in admission or list responses.
Reject forged owners, unknown fields, invalid identifiers, and unsupported version selections.

Require explicit selection review before reassessment admission.
The new snapshot keeps baseline bank sources, the assessment date, and the complete obligation scope.
The specified newer regulatory version replaces only its older selected version.
Future, unchanged, unresolved, and unfinished comparisons cannot authorize reassessment.
Keep the previous assessment and human decisions accessible.

## Interface

Use a separate component in the existing assessment workspace.
Load comparison options when the user opens the comparison flow.
Require explicit selection of the newer saved version.
Show the baseline assessment, versions, publication dates, effective dates, and unverified freshness.
Show an empty state when no other saved version exists.

Keep a failed admission draft and its request key after an uncertain response.
Disable new actions until the user refreshes the saved state.
Keep saved comparisons accessible after reload.
Show queued, running, failed, partial, and completed states independently of the requirement interpretation.
Show unchecked and unresolved obligations without claiming completion.

Show before and after requirements, conditions, exceptions, applicability, cited quotes, and original affected control IDs.
Keep metadata changes separate from requirement changes.
Require a selection-review acknowledgment before the user starts the new assessment.
Open the new assessment with independent findings and human reviews.
Keep a link to the previous assessment.

Use labeled controls, visible keyboard focus, and a layout that fits a mobile viewport.
Preserve expiry handling and bearer-token boundaries.
Keep implementation details outside ordinary product actions.

## Acceptance checks

| Check | Required behavior |
|---|---|
| VS5-CF01 | Authentication, ownership, and the disabled flag precede native comparison services. |
| VS5-CF02 | Selection returns owned pinned versions and safe metadata with unverified freshness. |
| VS5-CF03 | Admission and uncertain queue retry keep one saved job and return no internal execution data. |
| VS5-CF04 | Reads and lists preserve cited results, progress, unchecked obligations, and case scope. |
| VS5-CF05 | Explicit reviewed selection admits and queues an independent assessment without copying earlier reviews. |
| VS5-CF06 | Resume uses only saved identifiers. Missing records and forged bodies fail safely. |
| VS5-CF07 | Future, unresolved, partial, and unfinished results cannot start reassessment. |
| VS5-CF08 | Local HTTP routes use the same comparison rules with supervised background execution. |
| VS5-CF09 | SAM routes use the existing Cognito authorizer and disabled assessment resources. |
| VS5-CF10 | Browser selection, progress, citations, reload, and independent assessment links work. |
| VS5-CF11 | Uncertain requests retain their key. Mobile and keyboard controls remain usable. |
| VS5-CF12 | Empty versions and unresolved results keep reassessment unavailable. |

Live source coverage, semantic evaluation, template validation, AWS authentication, CloudFront verification, and deployed acceptance remain pending.
Use a different language receipt. Complete vocabulary review remains pending.
