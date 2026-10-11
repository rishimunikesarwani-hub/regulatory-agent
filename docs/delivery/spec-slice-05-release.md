# VS5 — Complete scope and release evidence

Date: 2026-10-11.
Authorization: D42 approves VS5 local development after the checked VS4 merge.
Integration base: `4ffdd0713961a64da7d20ad91232c761f1dc07cd`.

## Delivery conditions

VS5 includes all remaining acceptance conditions in the five approved specifications and T1–T9.
Local software checks do not establish live model quality or AWS acceptance.
Keep the eight feature claims connected to their actual evidence and remaining conditions.
Use the existing job, snapshot, source, review, and measurement services.
Do not add dependencies for exports.

Use branch `work/t9-quality` in `regulatory-agent-t9-quality`.
Use web port `5185`, feedback API port `8150`, and browser API port `8151`.
Keep feedback and browser-test databases in different files under `runs/private/slice-05/`.

## Local export contract

An export is a downloaded assessment report.
REQ-X03, REQ-X05, REQ-X07, and REQ-X08 control its contents and access.
Use `POST /api/cases/{case_id}/assessments/{job_id}/export` with the existing `ExportRequest` format.
Accept an optional timezone-aware `cutoff` query value for historical review outcomes.
Reject invalid and future cutoffs.
The cutoff controls findings, review events, review counts, and trace events.
The export records the observed job state separately from the review cutoff.
Do not invent a historical job state from its current state.

Export JSON or Markdown without a write to assessment or review records.
Include the immutable snapshot, selected versions, assessment date, findings, citations, and referenced source passages.
Include original recommendation IDs, saved reviewer content, applicable review events, counts, denominators, and the metric definition.
Include authority URLs, verification time, freshness, job state, stop reason, unchecked obligations, and limitations.
Include safe trace versions, recorded attempts, durations, usage, and missing cost labels.
Use `vs5-v1` for new processing traces. Preserve older saved application and prompt versions.
Keep controlled processing and synthetic data labels visible.
Keep private evidence only in the authorized downloaded report.
Do not include worker tokens, execution claims, raw prompts, hidden reasoning, or credentials.

An incomplete report must say Partial export.
A failed job must say Failed assessment export.
Keep usable findings from incomplete jobs.
Keep every selected obligation without an exported finding in the unchecked list.
Do not classify a queued job as completed.
Keep full source versions from the snapshot after replacement uploads.
Resolve each exported citation against its saved version, passage, location, and quoted text.
Reject an export with an invalid citation instead of inventing a passage.
Encode uploaded and reviewer text safely in Markdown.
Return download headers and `Cache-Control: no-store`.
Repeated exports at one cutoff must produce identical bytes.

## Local acceptance checks

| Check | Required behavior |
|---|---|
| VS5-CT01 | JSON keeps snapshot, source passages, citations, simulated labels, trace versions, and unknown costs. |
| VS5-CT02 | Markdown keeps the same review counts, versions, evidence relationship, and limitations as JSON. |
| VS5-CT03 | A previous cutoff keeps its original final review after later edits and evidence requests. |
| VS5-CT04 | Queued, partial, and failed jobs retain actual state, valid findings, and unchecked scope. |
| VS5-CT05 | Cross-owner, cross-case, unknown, and AWS controlled-route requests cannot export. |
| VS5-CT06 | Invalid cutoffs and formats fail safely. Repeated exports do not add calls, events, or jobs. |
| VS5-CT07 | Replacement uploads cannot change report sources. Invalid citations prevent export. |
| VS5-CT08 | A review committed during a read cannot enter the captured report after its cutoff. |
| VS5-BT01 | Download both formats after review. Match saved review counts and exact versions. |
| VS5-BT02 | Export failure keeps the selected assessment and saved review. A retry can succeed. |
| VS5-BT03 | Mobile and keyboard operation have no horizontal overflow. Downloads keep synthetic labels. |
| VS5-BT04 | A refresh of the same assessment cannot discard an export or prevent later downloads. |

Record failing behavior checks before implementation.
Then run all backend checks, the frontend build, and all slice browser checks.
Keep the earlier slice evidence unchanged.

## Remaining release conditions

REQ-F01 needs the configured external API, authority coverage, complete source text, versions, and current-source verification under D20.
REQ-F02 needs live obligation comparisons in addition to the checked fixed simulations.
REQ-F03–REQ-F08 need full selected-scope processing with the approved live model.
Keep conditions, exceptions, applicability, missing owners, operational evidence, conflicting records, and source-supported mappings.
Support all five finding statuses without using evaluation answers as application logic.
Keep each dispatch within the saved 24-call allowance and 600-second worker deadline.
Use the existing bounded retrieval contracts for selected source versions and evidence periods.
Source-provider selection and live configuration remain unresolved.

REQ-X09 needs separate provider coverage, regulatory retrieval, bank-evidence retrieval, and held-out assessment reports.
Use at least 20 held-out cases with the fixed live model.
Include errors and abstentions in the denominator.
Require at least 90% agreement, correct citations, and zero critical false-supported findings.
Record comparable runtime groups, safe traces, usage availability, and separate inference and system costs.
Keep unknown measures unknown.
Controlled software checks cannot satisfy these live gates.

AWS acceptance needs account verification, failed-stack recovery, reviewed deployment changes, and live service checks.
Check Cognito, ownership, private storage, jobs, worker permissions, source access, and India model destinations.
Keep private uploads disabled until the required region and access checks pass.
No Support case ID has been confirmed.
Prepare the demonstration and architecture evidence after the complete flow passes.
External submission needs separate user authorization.

## Language review

Use the project glossary for technical terms.
Keep a separate language and meaning review receipt.
Sentence checks alone do not establish full ASD-STE100 compliance.
