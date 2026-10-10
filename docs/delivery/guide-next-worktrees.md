# Next development worktrees

Date: 2026-10-10.
Scope: Worktree preparation and later development instructions.

The user requested all worktrees before further feature development.
This preparation starts no application feature work, servers, cloud operations, or live evaluations.
Before development, each new worktree must contain integrated `main` and the documentation pull request.
The original Session A and Session B folders stay unchanged.

A worktree is a project folder with its own Git branch.
A branch is a named sequence of commits, which are recorded file versions.
A pull request is a request to review and combine branch changes.
The integration owner controls shared changes and their inclusion in `main`.

## Worktree map

Parent folder: `C:\Users\Be Flith Rich\My Project Folder\ET-Hackathon\.worktrees`.
The port numbers below are allocations for later loopback services.
A port identifies a network connection point.
Loopback traffic stays on this computer.
Preparation starts no service on these ports.

| Work | Folder | Branch | Start condition | Future port |
|---|---|---|---|---|
| D24 foundation | `regulatory-agent-foundation` | `work/foundation-measurements` | Integrated Session A, Session B, and approved documents | 8110 |
| T3 documents | `regulatory-agent-t3-documents` | `work/t3-documents` | D24 foundation completed and merged | 8113 |
| T4 assessment | `regulatory-agent-t4-assessment` | `work/t4-assessment` | T3 completed and merged | 8114 |
| T5 agent | `regulatory-agent-t5-agent` | `work/t5-agent` | T4 completed and merged | 8115 |
| T6 persistence | `regulatory-agent-t6-persistence` | `work/t6-persistence` | T4 completed and merged | 8116 |
| T7 review interface | `regulatory-agent-t7-review-ui` | `work/t7-review-ui` | T5 and T6 completed and merged | 8117 |
| T8 AWS | `regulatory-agent-t8-aws` | `work/t8-aws` | T6 and T7 completed and merged | 8118 |
| T9 quality | `regulatory-agent-t9-quality` | `work/t9-quality` | T8 completed and merged, with all T1 requirements completed | 8119 |

The development sequence is foundation, T3, T4, then T5 and T6, then T7, T8, and T9.
T5 and T6 can continue independently after T4.
The start condition still applies when its folder exists.

The [feature tickets](05_FEATURE_TICKETS.md) control scope, dependencies, and acceptance.
The [measurement contract](../testing/spec-measurement-contract.md) controls D24 behavior.
The [local test plan](../testing/spec-local-test-plan.md) and [quality plan](../testing/eval-model-quality.md) control verification.

## Work in each worktree

### Foundation: D24 additions to T1 and T2

[D26](../decisions/gov-decision-log.md) gives this worktree responsibility for D24 fixture and contract changes during this phase.
The foundation extends the integrated Session A fixtures and Session B contracts.
The existing checks do not prove completion of D24.

Prepare source-span labels, annotation rules, review histories, controlled clocks, usage records, and failure fixtures.
Keep held-out answers outside development and prompt adjustment.
Record the domain-review status of reference labels.

Extend the contracts for original review items, review events, revisions, cohorts, cutoffs, and reports.
Add stage and attempt contracts with stable identities, versions, timing, usage, and safe errors.
Give retrieval evaluation and assessment evaluation different contracts.
Use the D24 final outcomes and pending-action rules.

Write failing behavior tests before the corresponding code.
Use UT-13 through UT-18 and CT-06 through CT-08 for the applicable foundation behavior.
Keep later persistence, browser, cloud, and live quality checks pending until the corresponding code exists.
Give the integration owner the changed contracts, fixture references, test evidence, and remaining gaps before T3.

### T3: Documents and traceability

Use the merged foundation contracts.
Add the approved file validation, extraction, source locations, immutable versions, and selected-snapshot retrieval.
Add regulatory refresh and source-version verification through the specified adapter.
Keep controlled provider responses visibly simulated until live integration passes its checks.
Give T4 the source spans, citation records, freshness behavior, and saved audit references.

### T4: First complete assessment

Use the merged T3 document and source records.
Complete one obligation-to-control-to-evidence assessment with a finding and proposed correction.
Apply source, case, snapshot, and evidence-period filters before retrieval.
Record candidate and selected passages with the D24 retrieval measurements.
Give T5 and T6 the assessment contracts, reference fixtures, and verified local sequence.

### T5: Bounded agent and changes

Extend the merged T4 sequence with validated model actions and regulatory version comparisons.
Keep one agent and `in.openai.gpt-5.6-luna` as the baseline.
Keep the shared 24-call allowance and 600-second worker deadline across retries and restarts.
Record stages, attempts, partial outcomes, and new review items for new assessments.
Give T7 the integrated agent behavior and change-comparison evidence after T6 integration.

### T6: API and persistence

Extend the merged T4 sequence with authorized API operations, jobs, recovery, and persistent records.
Write code for D24 review history, outcome reports, timing summaries, and cost calculations.
Keep original AI findings unchanged.
Prevent duplicate effects from repeated requests and events.
Give T7 the integrated API behavior, report contracts, and persistence evidence after T5 integration.

### T7: Review interface

Use the integrated T5 and T6 behavior.
Write code for the [frontend specification](../frontend/04_FRONTEND_SPEC.md), including source inspection, review history, measurements, and exports.
Do browser checks for normal, denied, empty, partial, and failed states.
Give T8 the verified local user sequence and known interface limits.

### T8: AWS integration

Use the integrated local application.
Prepare AWS adapters, SAM configuration, and the numbered deployment guide.
Follow the [security specification](../security/03_SECURITY_ACCESS.md) for access and India processing.
Review actual deployment changes with the user before deployment.
Keep private uploads disabled until the required region and access checks pass.
Give T9 the authorized cloud verification records and remaining provider or model limits.

### T9: Quality and submission evidence

Make sure that all T1 requirements are completed before live evaluation.
These include provider verification, source records, labels, and at least 20 held-out assessment cases.
Use the approved baseline and the [quality plan](../testing/eval-model-quality.md).
Keep retrieval results, assessment accuracy, reviewer outcomes, latency, and costs in their specified result groups.
Prepare the demonstration, architecture evidence, and submission package.
Do not submit externally without explicit authorization.

The user must select the live regulatory provider.
No worktree owner can make that selection on the user's behalf.
Local controlled responses do not establish current regulatory coverage.

## Start a selected task

1. Make sure that the user has requested feature development.
2. Make sure that `main` contains completed work for the stated start condition.
3. Open PowerShell in the selected folder from the map.
4. Read [AGENTS.md](../../AGENTS.md) and the [project handbook](../guide-start-here.md).
5. Read the selected ticket and the latest decision records.
6. Examine the worktree status.

```powershell
git status --short
```

If the command shows any changes, stop before the update commands.
Ask the integration owner how to continue.
Do not discard or temporarily hide another session's changes.

Use the following commands only before new work, when the worktree has no changed or untracked files.
Get the current remote references.

```powershell
git fetch origin
```

If that command succeeds, update the branch through a fast-forward merge.
A fast-forward merge sets the branch to a later commit without combining different development histories.

```powershell
git merge --ff-only origin/main
```

If either command fails, stop.
Ask the integration owner how to continue.
Do not reset, rebase, or force a merge after this failure.

Use the supplied `.venv` in the selected worktree.
A virtual environment is a local Python installation with the project's dependency versions.
Do the local checks before changes.

```powershell
.\.venv\Scripts\python.exe -X utf8 ops/check.py
```

If the environment or command is unavailable, ask the integration owner to complete preparation.
If a check fails, record the failure before code changes.
Do not treat an existing failure as a completed start condition.

## Shared changes and runtime files

The integration owner controls specifications, dependency locks, shared interfaces, and the project log.
D26 gives the foundation owner responsibility only for the stated D24 fixture and contract extension work.
Get the integration owner's agreement for other shared contract or specification changes before edits.
Keep each task's code and tests in its selected worktree.
Do not edit another session's worktree.

Use the specified future port when an authorized task needs a local service.
Keep runtime files in that worktree's ignored `runs/private/` folder.
Do not share a writable database between worktrees.
Do not add private data, credentials, or runtime files to Git.

Save safe failing and passing test evidence in a new dated folder under `runs/`.
Include the requirement IDs, commands, results, and remaining limits.
Use the [language guide](../guide-ste100-writing.md) for documentation changes.
Give the integration owner the changes and evidence for review before dependent work starts.
Passing local checks do not prove live model quality or cloud readiness.
