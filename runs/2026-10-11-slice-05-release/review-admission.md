# Selected historical admission review

Date: 2026-10-11.
Contract: [Selected admission](../../docs/delivery/spec-slice-05-admission.md).
Scope: Historical selection, immutable artifacts, processing dispatch, source inspection, and original downloads.

The selection catalog uses owned bank versions and the existing real-source manifest.
It excludes simulated amendment fixtures.
It compares saved quotations with text from the original HTML file.
It verifies original hashes and copies the public original into authorized storage.
The catalog identifies its saved excerpt scope and unverified current status.

Snapshots bind every selected source to an exact document artifact.
The shared resolver keeps source publication versions separate from saved artifact IDs.
New model actions use those artifact IDs.
Legacy snapshots keep their original lookup paths and records.
Identical retries keep the original versions after upload replacement.

The API uses the existing separate worker and server-controlled model configuration.
Requests cannot choose a model, profile, worker, or processing label.
Public archive checks apply to processing, source inspection, and exports.
Unknown bank evidence periods remain unknown.

## Behavior evidence

| Record | Result |
|---|---|
| `admission-red.txt` | Ten checks failed because the implementation was absent. |
| `admission-first.txt` | The catalog incorrectly treated document summaries as complete extracted sources. |
| `admission-second.txt` | Seven checks passed. Three fixtures assumed source ordering after JSON storage. |
| `admission-artifact-red.txt` | The old action guard rejected explicit saved artifact IDs. |
| `admission-artifact-green.txt` | All ten initial checks passed. |
| `admission-integrity-red.txt` | Source inspection missed archive corruption. A provider stub used the wrong label field. |
| `admission-integrity-green.txt` | All twelve checks passed after shared archive validation and the fixture correction. |
| `backend-admission-first.txt` | All 288 combined checks passed before separate protocol-version labels. |
| `admission-version-red.txt` | New snapshots and traces used the earlier protocol versions. |
| `admission-version-green.txt` | All twelve checks passed with distinct prompt and schema versions. |
| `backend-admission-final.txt` | All 288 combined checks passed before the missing-reference guard. |
| `admission-missing-reference-red.txt` | An empty reference map allowed the new protocol to use legacy lookup behavior. |
| `admission-reference-green.txt` | All twelve checks passed after requiring explicit references for the new protocol. |
| `backend-admission-reference-final.txt` | All 288 combined backend checks passed with the final reference guard. |

The pipeline integration check uses controlled provider responses with a declared live label.
This label tests metadata compatibility. It does not establish actual live access.
The check does not establish contextual model quality.
The controlled results request evidence rather than assert operational support.

## Remaining conditions

The feedback interface still uses the earlier fixed example.
The selection interface remains unfinished.
The historical catalog exposes the existing saved excerpts, not complete current regulations.
Provider selection and current verification remain pending under D20.
Bank evidence-period extraction still needs integration before full live acceptance.

Live model quality, held-out gates, and AWS acceptance remain pending.
AWS authentication needs renewal.
No external source request, live inference, or deployment occurred during this work.
VS5 remains a draft under D35.

## Language and meaning review

Reference: ASD-STE100 Issue 9 and the project glossary.
Protected content includes artifact IDs, source versions, quantities, permissions, and evidence limits.
The manual review checked snapshot immutability, ownership, failed checks, and processing labels.
The review preserves the distinction between stored source evidence and current authority verification.

The complete dictionary meaning review remains incomplete.
Mechanical checker results are separate records.
This receipt does not claim full ASD-STE100 compliance.
