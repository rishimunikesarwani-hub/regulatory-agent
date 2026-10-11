# VS5 selected-scope assessment pipeline

Date: 2026-10-11.
Authorization: D42 permits local VS5 development.
Requirements: REQ-F03–REQ-F08 and REQ-X01–REQ-X09.
Parent contracts: [Release](spec-slice-05-release.md) and [model dispatch](spec-slice-05-model.md).

This pipeline processes admitted historical runs before API admission and source-selection integration.
Those integrations remain necessary for the complete application.
Use the existing immutable snapshots, case documents, jobs, reviews, and model interface.
Keep current assessments blocked until source verification under D20 is available.
Keep private input blocked until the required processing checks pass.

A synthetic snapshot identifies fictional bank input.
Real public regulations do not need a synthetic-data flag.
Validate their allowed RBI authority URL before model access.
An allowed URL does not establish freshness or content authenticity.

## Source selection and retrieval

Resolve every selected source/version key to its exact saved document.
Check its case, source ID, version, kind, and extracted passages.
Check original bank document integrity through the existing document service.

Require a saved regulatory scope map for each selected obligation.
A scope map connects an obligation ID to its original regulatory passage IDs.
Reject missing, empty, or outside-source scope entries before model access.
Keep conditions and applicability passages in the selected scope.

Use keyword ranking without another dependency.
Filter selected versions, document kinds, and known evidence periods before ranking.
Keep unknown document periods explicit.
Do not invent periods from filenames or upload times.

Keep at most 20 passages and 64,000 UTF-8 text bytes in each context.
Do not split a saved passage or change its location.
Keep the candidate IDs, selected IDs, and selected byte count.
Report incomplete regulatory scope instead of silently dropping mandatory passages.

## Model and result processing

Extract selected obligations with their conditions, exceptions, applicability, and exact citations.
Extract relevant controls with source references and nullable owners and frequencies.
Then process each selected obligation through the same bounded agent.
Permit only the existing five model actions.
Validate the action against the current processing phase before tool execution.

Permit one retrieval refinement for each obligation within the shared allowance.
Use a bounded optional retrieval query only for that action.
Accept inspection requests only for passages in the current candidate set.
Count every model dispatch against the saved 24-call limit.
Do not add an autonomous second reviewer.

A claim connects an obligation element to cited passages and a short reason.
Keep the examined exceptions and conflicts in the claim record.
Keep the evidence period explicit or unknown.

Check quote matches and selected passage membership before persistence.
Require operational supported claims to cite operational evidence with a known relevant period.
A policy promise cannot replace that evidence.
These runtime checks do not establish contextual meaning or model quality.
Human held-out evaluation remains mandatory under the measurement contract.

Require one finding and a nonblank primary recommendation for each completed obligation.
Give findings stable server-created IDs within the saved run.
Save validated outputs before presentation so a resumed delivery can reuse them.
Save original findings and human decisions in different records.

Mark an obligation accounted only after finding and audit persistence succeed.
Keep unchecked obligations after failure or exhausted allowances.
Keep usable findings from incomplete runs.

## Audit and failure handling

Save a started model attempt before dispatch.
Keep it unknown if the worker stops before its outcome is available.
Save terminal state, numeric usage, request ID, and safe errors after the attempt.
Preserve available usage when output validation fails.
Keep missing usage unknown.

Do not save raw responses, reasoning blocks, or provider error text in traces.
Save application, schema, extraction, chunking, retrieval, prompt, and model configuration versions.
Do not report completion after an audit-save failure.
Keep the original deadline and counters during resumed processing.
Reject late persistence and stale worker tokens.

The independent process supervisor remains a separate required worker integration.
Do not claim that this synchronous pipeline alone enforces a hard wall-clock deadline.

## Acceptance checks

| Check | Required behavior |
|---|---|
| VS5-PT01 | Two selected obligations produce different review items with conditions, nullable control fields, claims, and exact source references. |
| VS5-PT02 | Source versions, kinds, and known periods are filtered before keyword ranking. Unknown periods stay explicit. |
| VS5-PT03 | Unselected sources, invalid scopes, altered original documents, and wrong owners prevent inference. |
| VS5-PT04 | Policy-only operational support, missing periods, invalid quotes, and unexamined passages cannot become valid findings. |
| VS5-PT05 | A bounded refinement and inspection preserve selected passages. Repeated or prohibited actions fail safely. |
| VS5-PT06 | Failure on later scope retains prior usable findings and reports every unchecked obligation. |
| VS5-PT07 | Resumed validated output does not repeat inference or create duplicate findings. |
| VS5-PT08 | Failed dispatched calls keep available numeric usage and safe request IDs in terminal audit records. |
| VS5-PT09 | Audit failure, late output, and stale execution claims cannot produce a completed job. |
| VS5-PT10 | Regulatory scope and bank candidates share one context allowance. |
| VS5-PT11 | All five statuses and repeated assessments preserve independent finding identities. |
| VS5-PT12 | Presentation validates the execution claim within its database transaction. |
| VS5-PT13 | Declared live processing keeps correct export labels and required stage metadata. Controlled provider stubs do not prove live access. |
| VS5-PT14 | Exports validate claim, exception, and conflict citations as well as finding citations. |
| VS5-PT15 | Real public regulations with an allowed authority URL remain distinct from unverified private bank documents. |
| VS5-PT16 | All 20 selected obligations can complete within one shared model allowance. |
| VS5-PT17 | Repeated refinements stop at the shared allowance and preserve every unchecked obligation. |

Write failing behavior checks before implementation.
Run the combined backend suite after shared contract changes.
Keep controlled checks separate from live model and held-out quality evidence.

## Language review

Use the project glossary and ASD-STE100 Issue 9.
Keep identifiers, limits, permissions, and prohibitions unchanged during review.
Save a separate review receipt.
Mechanical checks alone do not establish full dictionary compliance.
