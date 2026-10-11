# VS5 local development

Date: 2026-10-11.
Authorization: [D42](../decisions/gov-decision-log.md#d42--vs4-local-acceptance-and-vs5-authorization).
Contract: [VS5 release requirements](spec-slice-05-release.md).

The checked VS4 commit merged through PR12 into `main` at `4ffdd0713961a64da7d20ad91232c761f1dc07cd`.
GitHub run `38107994304` passed 228 backend checks, 38 browser checks, and the frontend build before that merge.
The integration folder and this slice advanced through fast-forward updates.
The user's design references remain unchanged.

## Local setup

Use the `regulatory-agent-t9-quality` worktree on `work/t9-quality`.
Use Python `3.12.13` and the locked dependencies.
Use feedback web port `5185` and API port `8150`.
Use `runs/private/slice-05/feedback.sqlite` for manual feedback.
The browser checks use API port `8151` and `runs/private/slice-05/browser-tests.sqlite`.
Stop this slice's feedback interface before browser checks.
Keep the earlier slice services and databases unchanged.

```powershell
uv pip sync --python .venv/Scripts/python.exe ops/requirements.lock
.venv/Scripts/python.exe -X utf8 ops/check.py --report runs/2026-10-11-slice-05-release/backend-green.txt
npm --prefix src/web run build
npm --prefix src/web test -- --config playwright.release.config.ts
```

## Export review

1. Open a fictional case.
2. Upload the supplied fictional policy.
3. Run a historical or simulated assessment.
4. Examine the finding and its source passages.
5. Save a human review outcome.
6. Download JSON or Markdown.
7. Examine the selected versions, citations, review counts, and report cutoff.

The report preserves the initial finding and saved reviewer decisions in different fields.
The report identifies incomplete jobs and unchecked obligations.
The report keeps unknown usage and costs unknown.
Download failures do not start another assessment or remove saved reviews.

## Remaining work

VS5 remains in progress.
Exports are one part of the complete release scope.
Read the [regulatory API research](../references/ref-regulatory-api-options.md) before provider selection under D20.
Complete source verification, full-scope processing, live evaluations, and deployed acceptance before a release claim.
CloudFront verification and failed-stack recovery still block AWS deployment.
No Support case ID has been confirmed.

The 20-case minimum, 90% agreement, citation checks, and zero critical false-supported gate remain mandatory.
Local checks do not satisfy those live quality conditions.
Do not merge VS5 before its D35 user review condition passes.
