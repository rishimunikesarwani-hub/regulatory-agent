# VS2 local document review

Date: 2026-10-10.
Status: Local implementation passed checks. User acceptance, integration merge, and AWS acceptance stay pending.

The [source contract](spec-slice-02-documents.md) controls this slice.
The worktree uses branch `work/t3-documents`.
Its folder is `ET-Hackathon/.worktrees/regulatory-agent-t3-documents`.
The integration worktree stays on `main` in `MVP`.

## Review the interface

1. Open `http://127.0.0.1:5182/`.
2. Select **Continue with local identity**.
3. Open a saved fictional case or make a new fictional case.
4. Select a fictional PDF, DOCX, TXT, or CSV file.
5. Select its document role.
6. Confirm that the file contains fictional data only.
7. Select **Upload fictional document**.
8. Inspect its exact version and source locations in **Source evidence**.
9. Select **Download original** to compare the initial file.
10. Select an existing source under **Replace source**.
11. Upload a revised fictional file.
12. Open the earlier version from **Saved versions**.
13. Refresh the page.
14. Sign in again to open the same source version.

Use [the fictional policy fixture](../../data/fixtures/slice-02-policy.txt) for a small manual upload.
Its policy statements come from the existing synthetic development inputs.
It is not regulatory or operational evidence.

The case permits 10 saved document versions and 100 extraction units.
Each file must have at most 10,000,000 bytes.
The case permits at most 400,000 extracted UTF-8 bytes.
Replacements count against these same limits.
The source preview can omit images and visual table structure.
No assessment has started.

## Start the feedback services

Use two PowerShell windows from the VS2 worktree.
Keep all addresses on loopback.
Loopback traffic stays on this computer.

Start the feedback API:

```powershell
$env:APP_ENV = 'local'
$env:DEVELOPMENT_USER = 'slice-02-rishi-feedback'
$env:LOCAL_WEB_PORT = '5182'
$env:CASES_DB_PATH = 'runs/private/slice-02/feedback.sqlite'
.venv/Scripts/python.exe -m uvicorn regulatory_agent.api:app --app-dir src --host 127.0.0.1 --port 8120 --no-proxy-headers
```

Start the interface in the second window:

```powershell
$env:LOCAL_API_PORT = '8120'
Set-Location src/web
node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5182 --strictPort
```

These services are already active for the current review.
Do not start another process on an occupied port.
Keep the VS1 feedback services unchanged.

## Local checks

The backend suite passed 178 checks.
The combined browser suite passed 20 checks: 14 case checks and six document checks.
The frontend build passed TypeScript and Vite checks.
These results do not establish live AWS behavior or model quality.

The browser configuration starts its own API on port `8121`.
It uses `runs/private/slice-02/browser-tests.sqlite`.
It never uses the feedback database.
Stop the VS2 feedback interface before browser tests because both use web port `5182`.

```powershell
.venv/Scripts/python.exe -X utf8 ops/check.py
Set-Location src/web
npx playwright test --config playwright.documents.config.ts
```

Read [the evidence record](../../runs/2026-10-10-slice-02-documents/review-local.md) for failing and passing results.

## Remaining acceptance

Obtain user feedback before the integration merge and next slice.
Do the GitHub integration checks before merge.
Keep local acceptance different from AWS acceptance.
The AWS interface still exposes only the first case slice.

AWS source upload and storage are not implemented in this local slice.
Complete those adapters and permissions before a deployed document acceptance check.
Keep private uploads disabled until the approved India checks pass.
Use [the CloudFront guide](guide-aws-cloudfront-verification.md) for the pending account verification.
