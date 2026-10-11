# VS5 stated evidence periods

Date: 2026-10-11.
Authorization: D42 permits local VS5 development.
Requirements: REQ-F06, REQ-X03, REQ-X05, and REQ-X08.
Parent contracts: [Pipeline](spec-slice-05-pipeline.md) and [admission](spec-slice-05-admission.md).

A stated period is a date interval that the supplied evidence declares.
It does not establish complete coverage or actual operation of a control.
Keep those conclusions subject to claim inspection and the required quality evaluations.

## Extraction and provenance

Use the standard library to extract explicit intervals from evidence-role passages.
Recognize ISO calendar dates and English month-name dates with a stated year.
Recognize the connectors `to`, `through`, `until`, and a dash between complete dates.
Keep other date forms unknown.
Do not infer dates from filenames, upload times, or isolated dates.

For CSV records, recognize explicit `period_start` and `period_end` columns.
Also recognize their `evidence_period_start` and `evidence_period_end` forms.
Keep the header and record as separate original source citations.
Reject ambiguous column identities and malformed rows as period metadata.
Do not reject the entire document because its period is unknown.

Keep the original source passages and bytes unchanged.
Keep exact citations for every extracted interval.
Keep invalid, reversed, or conflicting intervals unknown.
Do not combine different intervals into continuous coverage.
Do not convert dates in a policy into operational evidence periods.

Derive metadata only after checking the selected source against its original document.
Use the shared source reader for processing, inspection, and exports.
Save no replacement source record or extra model inference for this extraction.

## Retrieval and claims

Filter each known evidence passage period before keyword ranking.
Exclude periods after the assessment date and periods outside a requested interval.
Keep undated passages available with an explicit unknown-period indication.
Include a CSV header when selecting a record whose period depends on that header.
Count these passages against the existing context allowance.

Send period metadata only for passages in the model's selected context.
Keep the existing twenty-passage, 64,000-byte, and 24-call limits.
Do not treat metadata from unexamined passages as claim support.

Require each known claim period to be within a stated interval in a cited evidence record.
Require all period-grounding citations to be in the selected context.
A period from another passage in the same document is not sufficient.
Keep operational supported findings blocked when their cited period is unknown.
Keep the existing original findings and separate human decisions.

## Protocol and interface

Use `assessment-vs5-selected-period-v1` for new selected runs.
Use `vs5-selection-period-v1` and `vs2-period-v1` for their schema and extraction records.
Use `keyword-period-vs5-v1` for their retrieval records.
Keep earlier protocols, snapshots, processing paths, and stored source records unchanged.
Require immutable artifact references for both selected protocols.

Show stated intervals, grounding quotes, and original locations in the evidence source view.
Show unknown metadata when no unambiguous interval exists.
Keep the statement-versus-operation limit visible.
Keep extracted periods in exports for the same selected artifact.

## Acceptance checks

| Check | Required behavior |
|---|---|
| VS5-EP01 | Explicit ISO and English month-name intervals retain exact original citations. |
| VS5-EP02 | Invalid, reversed, conflicting, isolated, and filename-only dates remain unknown. |
| VS5-EP03 | CSV period columns retain the header and row without inferred continuous coverage. |
| VS5-EP04 | Retrieval filters periods per passage and includes required CSV header context within the allowance. |
| VS5-EP05 | Actual selected admission and uploaded evidence support grounded periods through controlled pipeline responses. |
| VS5-EP06 | Missing periods and periods in unrelated passages cannot support an operational claim. |
| VS5-EP07 | Earlier selected protocols and their source records remain unchanged. Both protocols retain the worker path. |
| VS5-EP08 | Altered stored source text cannot supply period metadata when it differs from the original document. |
| VS5-EP09 | Source inspection and export retain the selected period after an upload replacement. |
| VS5-EP10 | Prompts contain period metadata only for the selected context and add no model dispatch. |
| VS5-EP11 | The source dialog shows grounding quotes and the limit on what stated periods establish. |

Write failing behavior checks before implementation.
Keep controlled checks separate from live model evaluations.

## Release limits

This extraction does not verify record completeness or operation of a bank control.
It does not complete current-source retrieval, held-out quality gates, or AWS acceptance.
VS5 remains a draft under D35.

## Language review

Use ASD-STE100 Issue 9 and the project glossary.
Preserve source identities, unknown values, context limits, and earlier protocol behavior.
Save a separate review receipt.
