# VS3 - Controlled assessment and saved review

Date: 2026-10-10.
Status: The user approved VS2 locally and authorized VS3 local development under D36.

## User result

Open a fictional case and select the approved fictional policy version.
Start one controlled assessment of historical RBI clause 19(b).
Inspect its exact citations.
Save Approved, Edited, Rejected, or Request more evidence as a different human record.
Reopen the result and its review history after refresh.

Use the existing historical RBI source and synthetic policy fixture.
This controlled example does not assess arbitrary bank files or invoke a live model.
It demonstrates source binding, saved jobs, finding presentation, and human review.
The fixed finding is `needs_review` and does not establish operational compliance.
Keep applicability unverified for a case that contains only a bank name.
Keep the historical source's conditions and exceptions accessible.

Current assessments stay blocked until the regulatory provider and freshness checks are configured.
AWS document adapters, model access, and deployed assessment acceptance stay pending.
The approved baseline model stays `in.openai.gpt-5.6-luna`.
Controlled dispatch records must not claim an actual response from that model.

## HTTP contract

Use the existing `StartAssessment`, `Snapshot`, `Finding`, `ReviewItem`, and `ReviewRequest` contracts.
Use the existing local job store, controlled model adapter, and review service.
Keep every API operation within the authenticated case.
Return `404` for unknown or unauthorized cases, jobs, findings, and source versions.

| Operation | Route | Result |
|---|---|---|
| Start | `POST /api/cases/{case_id}/assessments` | `202` with the saved run and job identifiers. |
| List | `GET /api/cases/{case_id}/assessments` | Saved runs for that case. |
| Read | `GET /api/cases/{case_id}/assessments/{job_id}` | Job, fixed snapshot, finding, review history, summary, and safe stage trace. |
| Resume | `POST /api/cases/{case_id}/assessments/{job_id}/resume` | The same job. No second active worker or finding. |
| Inspect | `GET /api/cases/{case_id}/assessments/{job_id}/sources/{version_id}` | The exact source selected by that snapshot. |
| Review | `POST /api/cases/{case_id}/assessments/{job_id}/findings/{finding_id}/reviews` | Saved review event and revision. |

For this example, select one policy source and `RBI-IT-2023:2023-11-07`.
Select only obligation `RBI-IT-19b` and date `2024-04-08` in historical mode.
The policy must match the approved fictional policy fixture.
Reject another source with a clear fixture instruction.
Use the selected version's original bytes and locations.
Do not substitute a newer version after admission.

The start request needs an idempotency key.
The same key and payload return the same saved job.
A different payload with that key returns `409`.
Save the snapshot and job before worker execution.
Permit restart through the saved job's resume operation.
Keep its original 600-second deadline and 24-call allowance.

## Findings, citations, and review

The controlled finding describes an unverified evidence state.
Its proposed control mapping refers to `ACCESS-01` in the supplied fictional policy.
Its recommendation requests applicable operational evidence and reviewer examination.
Do not turn a policy commitment into proof that an activity occurred.
Show the controlled label beside the finding and summary.

Validate each citation against the selected source version, passage, location, and exact quotation.
Reject an invalid citation before finding presentation.
Keep the initial finding, recommendation, and citations unchanged after human review.
Use server timestamps and the existing review revision rules.

Approved accepts the original item unchanged.
Edited needs changed accepted content and a reason.
Rejected needs a reason and no accepted content.
Request more evidence is not a final outcome.
A later evidence request does not remove an existing final outcome.
Repeated review requests do not add duplicate decisions or metric items.

A stale revision returns `409` and keeps the user's draft.

Use the D24 formulas for reviewed, pending, approval, edit, rejection, adoption, and review coverage.
Keep zero denominators undefined.
Show the report cutoff, controlled data class, and `d24-v1` metric version.
Keep human acceptance different from regulatory correctness and actual operational compliance.

## Trace and interface

Record source verification, reused extraction, retrieval, context selection, controlled dispatch, validation, persistence, and review events.
Use the existing stage trace schema and monotonic timer.
Keep candidate and selected passage identifiers.
Link reused extraction to the initial saved document processing record.
Keep raw source text, prompts, responses, and review reasons out of operational logs and trace fields.

Keep unknown model usage, actual model identity, and cost fields unknown.
Do not calculate retrieval quality without the necessary labels.

Add the controlled assessment panel to the local case view.
Show its selected policy version, historical date, fixed obligation, and source limits before start.
Show saved job state, safe failures, citations, review actions, and review history afterward.
Inspect citations through the authorized snapshot source route.
Keep keyboard access and a narrow-screen layout.

## Acceptance cases

| ID | Behavior |
|---|---|
| VS3-CT01 | Save the fixed snapshot, execute the controlled job, and present a labeled finding with exact citations. |
| VS3-CT02 | Deny cross-owner and cross-case start, read, resume, source inspection, and review. |
| VS3-CT03 | Repeat start safely. Reject conflicting payloads. Keep the source snapshot unchanged after replacement. |
| VS3-CT04 | Reject current mode, unsupported scope, wrong fixtures, and forged selections without a job. |
| VS3-CT05 | Keep the original finding unchanged across Approved, Edited, Rejected, and stale review requests. |
| VS3-CT06 | Keep evidence requests pending. Apply saved outcomes and cutoff rules without duplicate items. |
| VS3-CT07 | Reopen exact sources and reviews after an application restart. |
| VS3-CT08 | Save safe stage records with controlled dispatch counts and unknown live model measurements. |
| VS3-CT09 | Fail invalid controlled citations safely without presenting a finding. |
| VS3-CT09B | Reject a controlled supported claim that has only policy text and no operational evidence. |
| VS3-CT10 | Resume an admitted job after worker interruption without a duplicate job or finding. |
| VS3-BT01 | Complete the controlled assessment, inspect a citation, save approval, refresh, and reopen. |
| VS3-BT02 | Save changed content and rejection reasons. Keep evidence requests different from final outcomes. |
| VS3-BT03 | Keep a draft after a stale revision or uncertain review save. Support keyboard and mobile operation. |
| VS3-BT04 | Keep uncertain review retries disabled when the saved assessment cannot be refreshed. |
| VS3-BT05 | Clear private findings and review drafts after assessment access expires. |
| VS3-BT06 | Keep a new case's assessment state independent of the previous case. |
| VS3-REL01 | Pass combined VS1, VS2, and VS3 checks before merge. Keep AWS acceptance different. |

## References

- [Feature tickets](05_FEATURE_TICKETS.md#delivery-slices).
- [Measurement contract](../testing/spec-measurement-contract.md).
- [Historical source manifest](../../data/sources/source-manifest.json).
- [Approved fictional policy](../../data/fixtures/slice-02-policy.txt).
- [Technical terms](../guide-ste100-writing.md#project-technical-terms).
