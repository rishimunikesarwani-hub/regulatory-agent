# VS5 local export development receipt

Date: 2026-10-11.
Status: VS5 is in progress. This receipt covers its local export work.

## Accepted integration

The user approved VS4 local acceptance, merge, and VS5 local development under D42.
The [VS4 GitHub receipt](vs4-github-checks.json) identifies the final checked commit and successful run `38107994304`.
That run passed 228 backend checks, 38 browser checks, and the frontend build.
The [merge receipt](vs4-merge.json) records PR12 and integration commit `4ffdd0713961a64da7d20ad91232c761f1dc07cd`.
Both integration and VS5 advanced through fast-forward updates.
The user's untracked design references remain unchanged.

## Specification and failing checks

The VS5 contract was committed as `2d4a0b5` before the new behavior tests.
The [backend red result](backend-red.txt) records eight checks with seven failures.
Ownership rejection already passed without a new export route.
The other checks reproduced missing exports and a separate review read outside the captured database events.
The [browser red result](browser-red.txt) records three missing-download failures before interface implementation.

The [first export checks](backend-first.txt) found excess Markdown escaping in version dates.
The first combined browser run passed 40 checks and failed one citation-location check.
The correction preserves readable dates and citation locations while quoting untrusted Markdown and HTML text.
The [refresh red result](export-refresh-red.txt) reproduced a missing download after the same assessment refreshed.
Its [passing result](export-refresh-green.txt) verifies the artifact-identity correction.
The [trace red result](trace-version-red.txt) reproduced the old application label before the `vs5-v1` change.
The [job metadata red result](job-metadata-red.txt) reproduced execution-lease metadata in an export before its removal.
Earlier stored traces remain unchanged.

## Passing local checks

The complete backend checks passed 236 checks after the VS5 trace correction.
The focused export checks passed all eight cases after the cohort and safe-job metadata additions.
The complete browser checks passed 42 checks after the download-refresh correction.
The frontend TypeScript check and Vite build passed.
Read the [backend result](backend-green.txt), [focused result](backend-slice-green.txt), and [browser result](browser-green.txt).
The first backend environment run lacked the already-locked `pypdf` dependency.
Dependency synchronization installed that package without a manifest change.
The earlier environment failure remains in `backend-environment-first.txt`.

The checks cover authorized sources, immutable versions, review history, cutoff consistency, incomplete jobs, download failures, and mobile access.
The export checks also cover invalid citations, ownership denial, unknown costs, and absence of writes or extra model calls.
The JSON and Markdown examples contain fictional test data.
The application never uses held-out answers as runtime assessment logic.

## Language and meaning review

The contract, guide, and provider research passed the selected mechanical STE checks.
The manual review examined authorization, prohibitions, version identifiers, cutoff semantics, and missing evidence.
New prose uses the project glossary for technical terms.
Source titles, URLs, identifiers, commands, and numbers remain protected.
The complete dictionary and approved-meaning review remain incomplete.
These checks do not establish full ASD-STE100 compliance.

## Remaining release conditions

Exports do not complete VS5 or the full approved project scope.
The [provider research](../../docs/references/ref-regulatory-api-options.md) includes one successful public-only historical-source transport probe.
Provider integration needs explicit selection under D20.
Current-source completeness, amendments, versions, and freshness remain unverified.
Full-scope live assessments, separate retrieval reports, held-out model evaluations, and quality gates remain pending.
AWS account verification, failed-stack recovery, deployment, and live service acceptance remain pending.
No Support case ID has been confirmed.
No deployment or external submission occurred.

Next: continue the VS5 contract after the final GitHub checks.
Keep VS5 outside `main` until its D35 user review condition passes.
