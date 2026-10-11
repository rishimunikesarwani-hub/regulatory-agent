# VS4 verification record

Date: 2026-10-11.
Status: Local checks passed. User acceptance and AWS acceptance are pending.

## Source and isolation

The accepted base is `5f50e7f6fdf3218aee657390c00d2641da2df60a` from merged PR9.
The branch is `work/t5-agent` in `.worktrees/regulatory-agent-t5-agent`.
The [contract](../../docs/delivery/spec-slice-04-changes.md) preceded new tests and application code.
Its initial specification commit is `3488c55`.

The browser configuration uses web port `5184`, API port `8141`, and a different test database.
The feedback API uses port `8140` and `runs/private/slice-04/feedback.sqlite`.
Earlier feedback services and records stayed unchanged.

## Failing results

The [backend red record](backend-red.txt) contains 11 checks, with 10 expected failures for missing simulated assessments.
The current-mode restriction already passed.
The [browser red record](browser-red.txt) contains four failures for the missing regulatory source selection.
The [AWS-mode red record](aws-mode-red.txt) shows the missing explicit controlled-route restriction.
The initial application browser checks passed two checks and failed two checks.
Their [error artifacts](browser-first-implementation-artifacts/) record an early review save and mobile text overflow.

The first [combined browser run](browser-combined-first.txt) passed 36 checks and failed one check.
That check examined the URL before the previous assessment finished loading.
Both assessments had the same visible approval text.
The corrected check waits for the assessment identifier to change.
The earlier failure and its [artifacts](browser-combined-first-artifacts/) stay recorded.

The [concurrent retry check](concurrent-retry-first.txt) passed before another implementation change was necessary.
The existing saved job admission already kept one new assessment and one model call.
This passing result is not a failing-test record.

## Passing results

| Check | Result | Evidence |
|---|---|---|
| All backend checks | 228 passed | [Backend results](backend-green.txt) |
| All browser suites | 38 passed | [Browser results](browser-green.txt) |
| TypeScript and frontend build | Return code `0` | [Build results](frontend-build.txt) |
| Desktop interface | Inspected | [Desktop screenshot](changes-desktop.png) |
| Mobile interface | Inspected, with no horizontal overflow | [Mobile screenshot](changes-mobile.png) |

The backend checks cover changed snapshots, exact passages, independent reviews, ownership, invalid pairs, and unfinished baselines.
They also cover retries, process restart, interrupted persistence, simultaneous requests, unchanged sources, and existing job limits.
The browser checks cover comparison, citation inspection, review persistence, reload, keyboard use, and delayed assessment loading.
Review saves stay disabled while the selected assessment loads.
Source passages use the existing wrapped-text style.

The added simulated requirement affects `ACCESS-01` and gives a new pending review item.
The earlier approved finding stays unchanged.
Cosmetic and wording changes do not start another assessment in these fixed examples.
Source date changes stay visible independently of the requirement classification.

## GitHub failure and consistent database reads

The first GitHub run `38106934698` failed one browser check and passed 37 browser checks.
It used commit `0bdf761a132015d97aa59d64adb3d1cbb3860df4`.
The [failed log](github-first-failure.txt) and [page artifacts](github-first-artifacts/) stay recorded.
The API could read findings before persistence and then read a later completed job state.
That response showed a completed assessment without its committed finding.

VS4-CT13 reproduced this race before the correction.
The [failing result](consistent-read-red.txt) shows the missing finding.
The shared assessment read now gets its job, findings, review events, and traces in one transaction.
The default review cutoff starts inside that transaction.
This correction also applies to the earlier historical assessment flow.
The earlier [227-check result](backend-first-green.txt) and [38-check result](browser-first-green.txt) stay unchanged.

Updated GitHub checks must pass before this branch can merge after user acceptance.

## Language and meaning review

The official ASD-STE100 Issue 9 reference was available from the ignored project reference directory.
The new contract and guide passed the selected mechanical checks.
The manual review examined conditions, prohibitions, source labels, identifiers, permissions, and unchanged approval history.
Selected dictionary decisions follow the project language guide.

The glossary defines simulated amendment and version comparison.
The dictionary and approved-meaning review is incomplete.
These receipts do not establish full ASD-STE100 compliance.

## Limits and next action

No live model call or external regulatory retrieval occurred.
The application did not read evaluation labels.
The fixed classifications do not establish general regulatory interpretation or held-out model quality.
Current assessments and controlled AWS assessment routes stay blocked.
CloudFront verification and failed-stack recovery still block deployment.
No Support case ID has been confirmed.

Next: complete the GitHub checks and obtain local VS4 user acceptance.
Keep VS4 outside `main` until that acceptance.
Keep VS5 and the complete project marked incomplete.
