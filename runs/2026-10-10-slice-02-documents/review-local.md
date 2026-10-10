# VS2 local evidence

Date: 2026-10-10.
Scope: Local fictional upload, unchanged versions, source inspection, and original download.

## Development sequence

The user approved VS1 local acceptance and authorized VS2 local development.
D35 records the isolated workspace workflow.
D36 and the source contract record implementation details before application code.

| Record | Result |
|---|---|
| `api-red-v2.txt` | Missing document routes failed the HTTP behavior tests. |
| `workspace-isolation-red-v2.txt` | The configuration incorrectly selected API port `8110` instead of `8121`. The guard stopped before writes. |
| `browser-red.txt` | The authorized case opened, but the Documents heading was missing. |
| `api-green-v1.txt` | Document behavior passed. A Windows test cleanup failed because its direct SQLite connection stayed open. |
| `api-timeout-red.txt` | Extraction timeout returned `503` instead of the specified safe `422` rejection. |
| `browser-uncertain-red.txt` | Upload stayed enabled after an uncertain save acknowledgment. |
| `browser-green-v1.txt` | Four historical sign-in fixtures used the old web port. Sixteen checks passed. |
| `python-green-v1.txt` | All 178 Python checks passed after the timeout correction and connection cleanup. |
| `browser-green-v2.txt` | All 20 combined browser checks passed after the fixture port correction. |

The timeout test preceded the timeout correction.
The uncertain-save browser test preceded the retry guard.
The sign-in fixture correction keeps the application's redirect checks unchanged.
The frontend build passed after these changes.

## Verified behavior

- PDF, DOCX, TXT, and CSV fixtures keep their exact source locations.
- Original downloads contain the unchanged uploaded bytes.
- Replacements keep earlier source versions unchanged.
- Application restart and page refresh keep saved versions accessible.
- Other owners and cases cannot inspect, replace, or download the sources.
- File, version, extraction-unit, and extracted-byte limits reject excess input without a partial save.
- Concurrent uploads cannot bypass the version count.
- Altered original bytes fail the content hash comparison.
- Extraction timeout returns a safe rejection without saved records.
- Extracted source text cannot execute HTML in the preview.
- Keyboard operation and a 375-pixel viewport passed browser checks.

## Workspace and limits

The branch is `work/t3-documents` in its own worktree.
Feedback uses web port `5182`, API port `8120`, and `runs/private/slice-02/feedback.sqlite`.
Browser tests use API port `8121` and `runs/private/slice-02/browser-tests.sqlite`.
The test configuration guards the API address before any document writes.
The VS1 feedback database and unrelated worktree changes stay unchanged.

Desktop and mobile screenshots show the checked document interface.
The user approved VS2 local acceptance and authorized VS3 local development.
The integration merge stays pending.
The current interface and its feedback API are active.

AWS deployment waits for CloudFront account verification.
AWS document adapters, live source retrieval, assessments, and model evaluations stay pending.
Text extraction does not establish coverage of images, visual tables, or OCR.
These checks do not establish production readiness or regulatory compliance.
