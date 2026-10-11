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

The [bounded model adapter](spec-slice-05-model.md) uses native SDK clients with controlled responses for local checks.
Its checks cover routing, reservations, output validation, usage, deadlines, selected citations, and SDK configuration.
The adapter now connects to the [selected-scope pipeline](spec-slice-05-pipeline.md) for admitted historical runs.
The [local supervisor](spec-slice-05-worker.md) now runs the pipeline in a separate process.
It stops hung workers and preserves the saved deadline, counters, audit records, and partial results.
The [selected-admission API](spec-slice-05-admission.md) now binds owned uploads and saved historical clauses to exact document artifacts.
It keeps current verification and complete regulatory coverage unverified.

The [selection interface](spec-slice-05-selection-ui.md) now connects these records to the local reviewer flow.
Each selected finding keeps its own review revision and source inspection.
The interface distinguishes controlled processing from fictional inputs with live processing.
It shows queued and partial results, unchecked scope, recorded calls, and available token counts.
Unknown costs, owners, frequencies, and evidence periods remain unknown.

The [period contract](spec-slice-05-evidence-periods.md) adds stated dates from selected evidence passages and explicit CSV columns.
The source view and exports preserve their exact original citations.
Stated dates do not establish complete records or actual control operation.
Unknown or conflicting dates remain unknown.
Earlier selected protocols keep their original prompt and source behavior.

External source integration and the AWS worker adapter remain unfinished.

The [cloud job component](spec-slice-05-cloud-jobs.md) now stores conditional job metadata and counters through native DynamoDB calls.
It uses the existing private S3 adapter for exact snapshot and stage references.

Its controlled checks cover competing claims, uncertain acknowledgements, recovered leases, call allowances, and artifact integrity.
Storage completion triggers another clock check before inference.
An unused reservation remains consumed, but its known absence of dispatch is recorded separately.
The [cloud record component](spec-slice-05-cloud-records.md) now connects the shared pipeline to native finding, attempt, and review persistence.
Its controlled checks include complete and partial assessments, concurrent reviews, original content, historical cutoffs, and exports.
An incomplete dispatch audit shows Unknown instead of zero live calls.
The [native execution component](spec-slice-05-cloud-execution.md) now connects historical admission, identifier-only SQS messages, and native worker cleanup.
Its checks cover full bank reads, uncertain acknowledgements, expired deliveries, snapshot binding, and stopped children.
The [cloud API component](spec-slice-05-cloud-api.md) now prepares authenticated assessment routes, source pages, reviews, and private report downloads.
Pinned source references avoid duplicate expanded bank records.

Verified public source files enter the deployment package.
Queue resources, a conditional worker, and fixed runtime permissions are prepared.
Cloud assessment deployment remains disabled by default.

Template schema and security validation remain pending tool approval.
Native version comparisons, source verification, live evaluations, and deployed acceptance remain required.
Hosted Lambda acceptance remains unverified.

The [change validation component](spec-slice-05-change-validation.md) prepares specified regulatory source pairs and validates model interpretations.
Its checks keep source hashes, dates, citations, selected obligations, and earlier control mappings.
Future requirements cannot request assessment processing for an earlier date.
Missing metadata stays unknown.
Complete comparison admission, model processing, native routes, and browser acceptance remain unfinished.

The feedback process must use the current application commit.
Renew the expired AWS authentication before live model checks.
The locked SDK includes its `crt` extra for the existing `aws login` profile.
Client construction passes. Live profile verification still returns `LoginRefreshRequired`.

VS5 remains in progress.
Exports are one part of the complete release scope.
Read the [regulatory API research](../references/ref-regulatory-api-options.md) before provider selection under D20.
Complete source verification, full-scope processing, live evaluations, and deployed acceptance before a release claim.
CloudFront verification and failed-stack recovery still block AWS deployment.
No Support case ID has been confirmed.

The 20-case minimum, 90% agreement, citation checks, and zero critical false-supported gate remain mandatory.
Local checks do not satisfy those live quality conditions.
Do not merge VS5 before its D35 user review condition passes.

The [saved comparison processing contract](spec-slice-05-comparison-jobs.md) adds bounded jobs and independent reassessment admission.
Native routes and browser controls now connect through D56.
Provider approval and live evaluation remain pending.

The [comparison API and interface](spec-slice-05-comparison-flow.md) now connect saved version selection, bounded processing, and independent reassessment admission.
No second verified regulatory version is available in the current source set.
Provider selection and live semantic checks remain required.
