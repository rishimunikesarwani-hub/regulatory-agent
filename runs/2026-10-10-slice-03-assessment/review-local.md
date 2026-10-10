# VS3 local verification

Date: 2026-10-11.
Status: Local checks passed. User acceptance, integration merge, and AWS acceptance stay pending.

## Scope

The [slice contract](../../docs/delivery/spec-slice-03-assessment.md) controls one historical controlled assessment and saved human review.
This work reuses the existing local job, snapshot, source, trace, and review services.
No dependency was added for this slice.
The model baseline stays unchanged.
No live model or regulatory provider call was made.

## Evidence

| Record | Result |
|---|---|
| `api-red.txt` | Ten assessment checks failed for missing HTTP routes before implementation. |
| `api-green-v1.txt` | Nine passed. One trace parser used strict dictionary parsing instead of JSON parsing. |
| `unsupported-red.txt` | Ten passed. The unsupported operational-claim test failed before the validation correction. |
| `python-green-v1.txt` | All 189 backend checks passed. |
| `browser-red.txt` | The assessment screen was absent before interface implementation. |
| `browser-green-v1.txt` | Twenty passed. Three assessment checks failed because the interface used the wrong trace time field. |
| `browser-green-v2.txt` | All 23 combined checks passed after the time-field correction. |
| `browser-green-v3.txt` | All 25 combined checks passed, including failed-refresh and expired-access checks. |
| `browser-case-state-red.txt` | The new-case status test failed before the stale status correction. |
| `browser-green-v4.txt` | All 26 combined checks passed after the new-case status correction. |
| `build-green.txt` | TypeScript and Vite checks passed for the final interface code. |
| `assessment-desktop.png` | The saved approval screen was inspected. |
| `assessment-mobile.png` | The mobile edited-review screen was inspected. No horizontal overflow was detected. |
| `assessment-review.png` | The saved assessment result and review summary were captured together. |

The TypeScript and Vite build passed.
The browser suite tested real loopback services and an isolated SQLite database.
It did not use the manual feedback database.
The earlier slice screenshots stay unchanged.
The regression screenshots in this directory belong to the combined VS3 check.

The API checks cover source binding, ownership, idempotency, unchanged snapshots, review revisions, cutoff rules, restart, and safe traces.
They also reject unsupported scope, invalid citations, and policy-only proof of operational activity.
The browser checks cover citations, saved review outcomes, reload, mobile operation, uncertain saves, failed refresh, and expired access.

## Limits

This is one controlled example with one original finding.
It does not establish live model accuracy, current regulatory coverage, or operational compliance.
Retrieval quality has no measured score in this slice.
Actual model identity, token usage, and inference cost remain unknown because no provider call occurred.
The selected model identifier is configuration metadata only.

The feedback interface uses port `5183` and API port `8130`.
Its private database is `runs/private/slice-03/feedback.sqlite`.
The test API uses port `8131` and its own private database.
User acceptance and GitHub checks are necessary before integration merge.
CloudFront verification and live AWS acceptance stay pending.
