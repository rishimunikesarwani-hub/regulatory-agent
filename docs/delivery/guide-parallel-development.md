# Delivery ownership and parallel work

Date: 2026-10-10.
Decision: [D27](../decisions/gov-decision-log.md#d27---delivery-by-complete-user-flow).

The delivery unit is one complete user flow, called a vertical slice.
The [slice inventory](05_FEATURE_TICKETS.md#delivery-slices) gives VS0 through VS5.
The approved eight features, T1-T9 acceptance conditions, and quality limits stay unchanged.

## Terms

| Term | Meaning |
|---|---|
| Frontend | The browser interface that the user operates. |
| Backend | The server code that validates requests and stores records. |
| API contract | The shared request, response, identity, error, and limit definitions for an operation. |
| Development pipeline | The automated sequence that checks and installs a commit in the AWS development environment. |
| Release record | The development URL, commit SHA, checks, and known limits for a delivered flow. |

See the [language guide](../guide-ste100-writing.md) for Git and application terms.

## Shared contract before concurrent work

1. Select one slice and one active worktree.
2. Compare its source state with Session A, Session B, and the current approved specifications.
3. Record its API contract and controlled responses.
4. Give each file one owner.
5. Start frontend and backend work against that same contract.
6. Record failing behavior tests before the corresponding code.
7. Combine the browser and server changes for the complete flow.
8. Do integration tests before AWS development deployment.
9. Do browser acceptance checks after deployment.
10. Record the release evidence and remaining limits.

Frontend and backend contributors can work concurrently after step 3.
They must not change shared fields independently.
A backend-only or frontend-only handoff does not complete an application slice.
VS0 is the contract preparation step, not a deployed application slice.

## File ownership

The integration owner assigns these roles for each slice.
One person or session can perform more than one role.
Assignments do not authorize simultaneous edits to the same file.

| Owner | Files or area | Responsibility |
|---|---|---|
| Integration | `AGENTS.md`, `README.md`, `LOG.md`, `pyproject.toml`, `docs/`, and shared dependency locks | Approved scope, slice status, API contract, and combined evidence. |
| Integration | `src/regulatory_agent/contracts.py`, `src/regulatory_agent/contract_types.py`, `src/regulatory_agent/ports.py`, and `data/contracts/slice-01-api.json` | Shared schemas and adapter interfaces before dependent work. |
| Backend owner | `src/regulatory_agent/cases.py`, `src/regulatory_agent/api.py`, and `src/regulatory_agent/aws_cases.py` | VS1 authorized case operations and persistent records. |
| Backend owner | `tests/test_slice01_cases.py`, `tests/test_slice01_aws.py`, and `tests/test_slice01_contract.py` | VS1 behavior, adapters, and contract checks. |
| Frontend owner | `src/web/`, including its package lock and browser tests | React, TypeScript, and Vite application for the selected flow. |
| Integration | `ops/sam-dev.yaml`, `.github/workflows/dev-release.yml`, `ops/record_release.py`, `ops/wait_for_api.py`, and `ops/deploy_dev.py` | Development configuration, pipeline, and deployment evidence. |
| Integration | `ops/requirements.in`, `ops/requirements.lock`, and `docs/delivery/spec-slice-01-cases.md` | Python dependencies and the shared VS1 API specification. |
| Fixture owner | Assigned files under `data/fixtures/`, `data/sources/`, and `evals/fixtures/` | Sources, labels, controlled inputs, and held-out-data separation. |
| Integration | A dated slice folder under `runs/` | Combined test evidence and the release record. |

Record exact new paths in the slice contract before concurrent edits.
The [VS1 contract](spec-slice-01-cases.md) gives the first application boundary.
Keep source inputs and held-out answers unchanged unless an assigned fixture task explicitly needs a new version.

## One AWS development pipeline

All application slices use the same AWS development deployment pipeline.
The pipeline permits only one deployment at a time.
It must not cancel an active deployment when another commit arrives.

Before deployment, do offline checks, contract checks, integration tests, and infrastructure validation.
Review the actual resources, permissions, costs, and recovery procedure.
A failing check blocks deployment.

After deployment, do browser acceptance against the deployed URL.
Use the same commit as the deployment record.
Include the success flow, denied access, and relevant failure states.
If a browser check fails, keep the slice incomplete.

Give every slice release its URL, commit SHA, test results, and known limits.
Keep failed attempts in the evidence record.
Do not claim deployment when AWS access or a deployment result is unavailable.
Production deployment and external submission need additional explicit authorization.

## Workspace and integration rules

The [worktree guide](guide-next-worktrees.md) records observed folders and the active assignment.
Use one selected worktree for the active slice.
Keep Session A and Session B unchanged during the new flow.
Keep pre-existing changes in `MVP` unchanged during reconciliation.

The integration owner controls shared changes and inclusion in `main`.
Examine the source differences and test results before integration.
Push only reviewed commits with recorded checks.
Update the selected branch from integrated work before the next slice.
Do not reset, remove, or hide another session's changes.

Default local tests need no credentials or external services.
Local browser and API tests can use loopback traffic.
Keep runtime files in ignored worktree-local folders.
Do not share a writable database between worktrees.
Do not commit private documents, credentials, or runtime files.

Use the [local test plan](../testing/spec-local-test-plan.md) and [measurement contract](../testing/spec-measurement-contract.md).
Use the [language guide](../guide-ste100-writing.md) for documentation changes.
Keep the language review receipt outside the user document.
