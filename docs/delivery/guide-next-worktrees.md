# Active worktree and next user flow

Date: 2026-10-10.
Decision: [D27](../decisions/gov-decision-log.md#d27---delivery-by-complete-user-flow).

The user selected delivery by complete user flows.
The earlier eight-folder schedule is replaced by the slice order below.
The folder count does not establish feature progress.
One active worktree contains the selected slice.
Frontend and backend contributors can work concurrently after agreement on its shared API contract.

## Observed workspace state

Parent folder: `C:\Users\Be Flith Rich\My Project Folder\ET-Hackathon`.
Four worktrees were registered during the 2026-10-10 reconciliation.
The original Session A and Session B worktrees had no uncommitted changes.
The integration folder contained pre-existing changes that must stay unchanged.

| Folder relative to the parent | Observed branch | Current role |
|---|---|---|
| `MVP` | `work/integration-handoff` | Existing integration and documentation changes. |
| `.worktrees/regulatory-agent-session-a` | `work/session-a` | Integrated fixture source and historical evidence. |
| `.worktrees/regulatory-agent-session-b` | `work/session-b` | Integrated contracts, adapters, and historical evidence. |
| `.worktrees/regulatory-agent-autonomous-build` | `work/autonomous-build` | Active D24 reconciliation and VS1 work. |

The earlier eight task folders were a plan, not verified existing worktrees.
No additional worktree is necessary for frontend and backend cooperation within the active slice.
The [parallel guide](guide-parallel-development.md#file-ownership) controls file ownership.

## Reconciled foundation

Session A supplied historical RBI content, synthetic bank fixtures, and 20 held-out cases.
Session B supplied local contracts, adapters, and a credential-free test command.
Their integrated baseline passed 60 offline checks.
The current D24 additions passed 123 offline checks.
The [recorded output](../../runs/2026-10-10-autonomous-build/combined-green.txt) gives the latter result.

These results do not establish completion of all T1 or T2 acceptance conditions.
They do not establish a deployed flow, live provider coverage, or model quality.
The [reconciliation record](../../runs/2026-10-10-autonomous-build/reconciliation.json) records the source comparison.

## Current flow and subsequent slices

| Slice | Complete user flow | Required next evidence |
|---|---|---|
| VS0 | Reconcile the foundations and agree on the shared VS1 API contract. | Source differences, contract version, and offline results. |
| VS1 | Sign in, make a case, save it, reload, and reopen the saved case. | Deployed browser acceptance and persistence evidence. |
| VS2 | Reopen the case, upload evidence, and inspect its source version and location. | Deployed source inspection, upload-limit checks, and denied-access checks. |
| VS3 | Inspect evidence, assess one obligation, inspect citations, and save a review. | Deployed full flow with original findings, saved review history, and processing labels. |
| VS4 | Compare regulatory versions and inspect changed obligations and a new assessment. | Version, change, snapshot, and independent review-history evidence. |
| VS5 | Use all eight features and inspect the complete release results. | Full acceptance inventory, live held-out evaluation, exports, and recorded limits. |

Start with the [VS1 contract](spec-slice-01-cases.md).
The [feature tickets](05_FEATURE_TICKETS.md#delivery-slices) define slice acceptance and retained T1-T9 criteria.
A session must finish its selected flow across browser, server, and AWS development.
Do not give a slice completed status from isolated frontend or backend work.
If access prevents deployment, record the blocked step and keep the slice incomplete.

## AWS development access

The first flow needs no regulatory retrieval provider or model invocation.
AWS development still needs a usable account profile, deployment role, and target region.
The initial inspection found no AWS or SAM command-line tools and no configured GitHub deployment variables or workflow.

The user confirmed that an AWS account is not available yet and will set it up.
Development deployment is blocked by account setup, identity roles, budget configuration, and a test operator.
Local implementation, tests, and a reviewed GitHub push can continue.
These are setup conditions, not application test failures.

Complete the reviewed AWS development setup before the first deployment.
Keep credentials outside chat and version control.
Use the single serialized development pipeline for all later slices.
Do integration tests before deployment.
Do browser acceptance after deployment.
Keep production deployment and external submission outside development authorization.

## Start and finish a session

Open PowerShell in the active worktree.

```powershell
cd 'C:\Users\Be Flith Rich\My Project Folder\ET-Hackathon\.worktrees\regulatory-agent-autonomous-build'
git status --short
```

Read `AGENTS.md`, the current slice contract, and D27 before changes.
Keep existing changes unless their owner assigned them to this session.
Use the documented project environment for default checks.
The [Session B guide](guide-session-b-testing.md) records the existing setup procedure.

Give the user progress against the eight MVP features at each handoff.
Identify foundation work separately from a completed feature.
Give a development release its URL, commit SHA, tests, and known limits.
Record failures and blocked checks explicitly.
