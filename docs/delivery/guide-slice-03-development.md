# VS3 local assessment review

Date: 2026-10-11.
Status: Local checks passed. User acceptance, integration merge, and AWS acceptance stay pending.

The [assessment contract](spec-slice-03-assessment.md) controls this slice.
The branch is `work/t4-assessment`.
The worktree is `ET-Hackathon/.worktrees/regulatory-agent-t4-assessment`.
VS2 merged into `main` through [pull request 8](https://github.com/rishimunikesarwani-hub/regulatory-agent/pull/8).

## Review the interface

1. Open `http://127.0.0.1:5183/`.
2. Select **Continue with local identity**.
3. Open a fictional case or create a fictional case.
4. In **Assessment**, select **Download the fictional policy**.
5. Upload that file as a policy document.
6. Confirm that the document contains fictional data only.
7. Select **Run controlled assessment**.
8. Read the requirement, conditions, exceptions, and original finding.
9. Select **Inspect Clause 19(b)**.
10. Close the source dialog.
11. Select a human review outcome.
12. For Edited, change accepted content and give a reason.
13. For Rejected or Request more evidence, give a reason.
14. Select **Save review**.
15. Inspect the saved revision and summary.
16. Refresh the page.
17. Sign in again to open the same saved assessment.

This example uses historical date `2024-04-08` and saved RBI version `2023-11-07`.
It accepts only the supplied fictional policy and clause 19(b).
The finding is a fixed controlled response, not a live model result.
Current regulatory status and bank applicability stay unverified.
A policy commitment does not prove completed operational activity.

Approved accepts the original finding unchanged.
Edited saves changed human content separately.
Rejected saves no accepted content.
An evidence request is not a final decision.
A later evidence request does not remove an earlier final decision.
The shown rates measure human acceptance, not correctness.

## Start the feedback services

Use two PowerShell windows from the VS3 worktree.
Keep both services on loopback.
Loopback traffic stays on this computer.

Start the feedback API:

```powershell
$env:APP_ENV = 'local'
$env:DEVELOPMENT_USER = 'slice-03-rishi-feedback'
$env:LOCAL_WEB_PORT = '5183'
$env:CASES_DB_PATH = 'runs/private/slice-03/feedback.sqlite'
.venv/Scripts/python.exe -m uvicorn regulatory_agent.api:app --app-dir src --host 127.0.0.1 --port 8130 --no-proxy-headers
```

Start the interface in the second window:

```powershell
$env:LOCAL_API_PORT = '8130'
Set-Location src/web
node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5183 --strictPort
```

Do not start another process on an occupied port.
Keep the VS1 and VS2 feedback services unchanged.

## Local checks

The Python suite passed 189 checks.
The browser suite passed 26 checks: 14 case checks, six document checks, and six assessment checks.
The TypeScript and Vite build passed.
The browser configuration uses API port `8131` and database `runs/private/slice-03/browser-tests.sqlite`.
It never uses the feedback database.
Stop only the VS3 feedback interface before browser tests because both use web port `5183`.

```powershell
.venv/Scripts/python.exe -X utf8 ops/check.py
npm --prefix src/web run build
Set-Location src/web
npx playwright test --config playwright.assessment.config.ts
```

The saved job permits explicit resume after worker interruption.
Its original 600-second deadline and 24-call allowance stay unchanged.
This short controlled example uses local background execution.
Live model work needs the approved AWS worker integration.

## Remaining acceptance

VS3 needs user feedback before integration merge and VS4 development.
AWS document and assessment adapters remain pending.
Current regulatory verification and live model quality remain unverified.
Keep private uploads disabled until the approved India checks pass.
Use [the CloudFront verification guide](guide-aws-cloudfront-verification.md) for the external account check.

Read [the local evidence](../../runs/2026-10-10-slice-03-assessment/review-local.md) for failing and passing results.
