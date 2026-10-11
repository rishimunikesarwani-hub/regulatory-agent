# VS4 local review

Date: 2026-10-11.
Status: Controlled local development. User review and AWS acceptance are pending.

VS3 merged through PR9 at `5f50e7f6fdf3218aee657390c00d2641da2df60a`.
GitHub run `38105951972` passed 215 backend checks, 33 browser checks, and the frontend build before merge.
The subsequent `main` run `38106158635` also passed.
The deployment job was skipped.

The [VS4 contract](spec-slice-04-changes.md) defines this comparison and its limits.
The comparison uses fixed simulated source versions and one fictional policy.
It does not establish current regulatory coverage or live model quality.

## Review procedure

1. Open `http://127.0.0.1:5184/`.
2. Select **Continue with local identity**.
3. Make a fictional case.
4. Download the fictional policy from the Assessment section.
5. Upload that file with the Policy role and fictional-data confirmation.
6. Select **Simulated access rule · v1** under **Regulatory source**.
7. Select **Run controlled assessment**.
8. Examine its source passage and original finding.
9. Save an Approved review for the earlier assessment.
10. Select **v2-added · Separate reviewer approval** under **Newer version**.
11. Select **Compare versions**.
12. Examine both passages and the affected control.
13. Select **Open new assessment**.
14. Make sure that the new assessment has no saved review.
15. Save its own review with the necessary reason.
16. Select **Open previous assessment**.
17. Make sure that its original finding and Approved review are unchanged.
18. Reload the page.
19. Sign in again.
20. Examine the saved comparison and both assessment histories.

For cosmetic and wording checks, open the earlier `v1` assessment.
Select `v2-cosmetic` or `v2-replaced` as the newer version.
Compare the versions.
These fixed examples must not start another assessment.
The source metadata changes stay visible.

## Local commands

Use this directory:

```powershell
cd 'C:\Users\Be Flith Rich\My Project Folder\ET-Hackathon\.worktrees\regulatory-agent-t5-agent'
```

Start the feedback API in one terminal:

```powershell
$env:APP_ENV = 'local'
$env:DEVELOPMENT_USER = 'slice-04-rishi-feedback'
$env:LOCAL_WEB_PORT = '5184'
$env:CASES_DB_PATH = 'runs/private/slice-04/feedback.sqlite'
$env:COMMIT_SHA = git rev-parse HEAD
.venv/Scripts/python.exe -m uvicorn regulatory_agent.api:app --app-dir src --host 127.0.0.1 --port 8140 --no-proxy-headers
```

Start the interface in a different terminal:

```powershell
cd 'C:\Users\Be Flith Rich\My Project Folder\ET-Hackathon\.worktrees\regulatory-agent-t5-agent\src\web'
$env:LOCAL_API_PORT = '8140'
node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5184 --strictPort
```

Stop this worktree's feedback interface before browser checks.
The tests need its web port `5184` and their own API port `8141`.
Do not use the feedback database for tests.

```powershell
.venv/Scripts/python.exe -X utf8 ops/check.py --report runs/2026-10-11-slice-04-changes/backend-green.txt
npm --prefix src/web run build
npm --prefix src/web test -- --config playwright.changes.config.ts
```

## Remaining conditions

The user approved VS4 locally and authorized its merge and VS5 development on 2026-10-11.
Merge the final checked commit before VS5 development.
CloudFront account verification and failed-stack recovery still block AWS deployment.
No Support case ID has been confirmed.
The prepared AWS document storage and permission changes have not been applied.
Live providers, the complete scope, model evaluations, and deployed service checks are incomplete.
