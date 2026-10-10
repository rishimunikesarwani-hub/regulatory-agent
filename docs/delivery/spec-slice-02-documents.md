# VS2 - Fictional documents and source inspection

Date: 2026-10-10.
Status: Authorized local development after VS1 local acceptance under D35.

## User result

Reopen a fictional case.
Upload an English text document.
Inspect its unchanged source version.
Keep original file bytes and extracted text in private case storage.
Make a replacement a new version of the same source.
Keep all earlier versions accessible.

This slice adds no regulatory retrieval or assessment execution.
AWS upload and storage acceptance stay pending under D34.
Accept fictional data only in the local development interface.

## HTTP contract

Authorization uses the existing case ownership checks.
Use the existing `UploadRequest`, `DocumentVersion`, and `Passage` value contracts.
Use one operation for local authorization, validation, extraction, and storage.
This implementation combines the authorization and finalization functions without a temporary upload destination.
The exact route spelling does not change the approved product requirements.

| Operation | Route | Result |
|---|---|---|
| Upload | `POST /api/cases/{case_id}/documents` | `201` with document metadata and extracted passages. |
| List | `GET /api/cases/{case_id}/documents` | Source metadata for the authorized case. |
| Inspect | `GET /api/cases/{case_id}/documents/{version_id}` | Metadata and passages for that exact unchanged version. |
| Original | `GET /api/cases/{case_id}/documents/{version_id}/original` | Exact original bytes as an attachment. |

Send file bytes as `application/octet-stream`.
Send the URI-encoded filename in `X-Filename`.
Send the approved role in `X-Document-Kind`.
Send `true` in `X-Synthetic` for fictional input.
Optionally send an existing source ID in `X-Source-Id` to replace that source.
Do not include filenames or source content in operational logs.

The role must be `profile`, `policy`, `control`, or `evidence`.
Response metadata adds the filename, format, extraction units, and upload time around the existing document value.
Return the existing safe error structure for rejected input and unavailable storage.
Return `404` for unknown or unauthorized cases and document versions.
Do not reveal whether another owner's document exists.

## Content and limits

Support English text PDF, DOCX, TXT, and CSV.
Validate the contents and extension.
Reject invalid, encrypted, scanned, empty, unreadable, unsupported, and oversized files.
Reject unsafe filenames and forged case or source identifiers.
Treat document text as evidence only.
Never execute commands or follow instructions from document content.

Apply the existing 10,000,000-byte file limit before extraction.
Apply the existing 4,000-byte extracted page equivalent.
Use the larger of actual PDF pages and extracted page equivalents for PDF units.

Keep at most 10 saved document versions and 100 extraction units per case.
Keep at most 400,000 extracted UTF-8 bytes per case.
Count replacement versions against the same case allowance.
Reject excess scope without truncation or a partial save.

Use actual PDF page references, DOCX paragraph references, TXT line references, and CSV row references.
Keep CSV physical line ranges when a row contains line breaks.
Do not invent PDF page numbers for other formats.
Show text extraction limits beside the source preview.
Do not claim that extracted text covers images, visual tables, or OCR accuracy.

Bound extraction time and decoded document content.
Use one different extraction process to contain parser failures.
Stop extraction after 10 seconds.
The process must not emit private input or raw parser errors to operational logs.

## Persistence and interface

Use SQLite transactions for local source records and original file bytes.
A transaction applies its database changes together or keeps all changes out.
Keep the selected slice's database separate from VS1 feedback and browser-test databases.
Apply case access checks to each transaction and every source read.
Use one SQLite transaction for the count check and insertion.
This prevents concurrent uploads from exceeding case limits.

Make rejected uploads leave the accepted source list unchanged.
Compare the original content hash during original-file reads.

Add Documents and Source evidence panels to the selected case.
Show formats, limits, role selection, and fictional-data confirmation before upload.
Show extraction failures with the corrective action.
Show each version, content hash, source location, and original-file download.

Render extracted text as text, not executable HTML.
Keep the selected source version after refresh through the saved case.
Keep keyboard access and narrow-screen layouts.

## Acceptance cases

| ID | Behavior |
|---|---|
| VS2-CT01 | Save supported files and preserve their exact original bytes and source locations. |
| VS2-CT02 | Reopen saved documents after a new application instance starts. |
| VS2-CT03 | Deny cross-owner and cross-case reads, uploads, replacements, and original downloads. |
| VS2-CT04 | Reject false fictional-data declarations, unsupported input, mismatched contents, and unsafe filenames. |
| VS2-CT05 | Reject encrypted, scanned, empty, and unreadable documents with safe errors. |
| VS2-CT06 | Enforce file, version, extracted-byte, and extraction-unit limits without partial persistence. |
| VS2-CT07 | Preserve the previous version when replacement succeeds or fails. |
| VS2-CT08 | Prevent concurrent uploads from bypassing aggregate limits. |
| VS2-CT09 | Reject altered original bytes and stop extraction timeouts without logging private input. |
| VS2-BT01 | Upload fictional evidence, inspect its location, refresh, and reopen the saved version. |
| VS2-BT02 | Inspect a replacement. Reopen the unchanged earlier version. |
| VS2-BT03 | Show a rejection and keep earlier accepted documents visible. |
| VS2-BT04 | Support keyboard use and mobile layout without horizontal overflow. |
| VS2-BT05 | Refresh saved versions before another upload when a save acknowledgment is uncertain. |
| VS2-BT06 | Download the exact original bytes through the authenticated source screen. |
| VS2-REL01 | Pass combined VS1 and VS2 checks before merge. Record AWS acceptance separately. |

## References

- [Approved security requirements](../security/03_SECURITY_ACCESS.md#4-upload-and-extraction-limits).
- [Local size equivalents](../architecture/02_TECHNICAL_BLUEPRINT.md).
- [Isolated slice workflow](guide-slice-workspaces.md).
- [Project technical terms](../guide-ste100-writing.md#project-technical-terms).
- [pypdf text extraction and limits](https://pypdf.readthedocs.io/en/stable/user/extract-text.html).
