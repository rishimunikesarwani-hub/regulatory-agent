# VS5 selection interface

Date: 2026-10-11.
Authorization: D42 permits local VS5 development.
Parent contract: [Selected historical admission](spec-slice-05-admission.md).
Requirements: REQ-F03–REQ-F08 and REQ-X03–REQ-X06.

## Selection and processing

Show the owned selection catalog in local mode.
Keep the earlier controlled example accessible.
Use different actions for controlled processing and live model processing.
Do not substitute controlled processing after a live request fails.

Show saved historical coverage and unverified current status.
Show the source authority, original URL, publication date, and effective date.
Keep current assessment selection unavailable.
Do not treat historical excerpts as complete coverage.

Let the reviewer select bank document versions, regulatory clauses, and an assessment date.
Accept arbitrary valid fictional uploads through the existing admission API.
Permit one version per bank source.
Keep the ten-document and twenty-obligation limits visible.
Do not select a smaller scope without the reviewer’s instruction.

Keep an uncertain admission request key for an identical retry.
Preserve the selected scope after a failed request.
Send no model configuration, processing label, or profile in an admission request.

## Results and reviews

Open saved controlled and fictional-input live runs.
Show the saved processing mode and recorded call count.
Keep unknown cost and usage values unknown.
Show queued, failed, and partial results without requiring a finding.
Show the exact unchecked obligation IDs.

Let the reviewer select each saved finding.
Show its requirement, mapped controls, evidence condition, claims, and recommendation.
Keep unknown owners, frequencies, and evidence periods visible.
Inspect source citations through the saved assessment snapshot.
Do not assume that a document ID contains its source type.

Save the review against the selected finding.
Use that finding’s latest review revision.
Keep review histories separate and retain the original findings.
Keep the aggregate review measures for the complete assessment.

## Browser checks

| Check | Required behavior |
|---|---|
| VS5-SB01 | Select an arbitrary fictional upload and two historical clauses. Send the exact selected versions and date. |
| VS5-SB02 | Open a queued live run with no finding. Show its mode, calls, and unchecked scope. |
| VS5-SB03 | Select either of two findings. Save against the selected finding and its own revision. |
| VS5-SB04 | An uncertain admission preserves scope and reuses its request key after refresh. |
| VS5-SB05 | Mobile keyboard selection has no page overflow. Current verification limits stay visible. |
| VS5-SB06 | A failed live run keeps partial findings and the exact unchecked scope. |

Use controlled browser responses for native processing in default checks.
Do not dispatch an external model from browser checks.
Keep browser conformance, backend execution, and live quality evidence separate.

## Language review

Use ASD-STE100 Issue 9 and the project glossary.
Preserve scope limits, unknown values, processing labels, and review ownership.
Save a separate review receipt.
