# Isolated vertical slice development

Date: 2026-10-10.
Status: The user selected this development workflow under D35.

A vertical slice connects one complete user flow across the interface, server, and storage.
A worktree gives a Git branch its own working directory.
Ponytail selects the smallest implementation that meets the approved behavior.

## Workspaces

Keep `MVP` on `main` as the integration worktree.
Use a different branch, worktree, port pair, and database path for each selected slice.
Keep browser-test records separate from user-feedback records.
Do not run tests against the feedback database.
Keep database files under ignored `runs/private/` directories.

| Slice | Worktree under `.worktrees/` | Branch | Web port | API port | Database directory |
|---|---|---|---|---|---|
| VS1 | `regulatory-agent-autonomous-build` | `work/autonomous-build` | `5173` | `8110` | `runs/private/` with existing `slice-01-*` filenames |
| VS2 | `regulatory-agent-t3-documents` | `work/t3-documents` | `5182` | `8120` | `runs/private/slice-02/` |
| VS2 AWS | `regulatory-agent-t3-aws-documents` | `work/t3-aws-documents` | `5192` | `8190` | `runs/private/slice-02-aws/` |
| VS3 | `regulatory-agent-t4-assessment` | `work/t4-assessment` | `5183` | `8130` | `runs/private/slice-03/` |
| VS3 candidate | `regulatory-agent-t4-integration` | `work/t4-integration-candidate` | `5193` | `8192` | `runs/private/slice-03-integration/` |
| VS4 | `regulatory-agent-t5-agent` | `work/t5-agent` | `5184` | `8140` | `runs/private/slice-04/` |
| VS5 | `regulatory-agent-t9-quality` | `work/t9-quality` | `5185` | `8150` | `runs/private/slice-05/` |
| VS5 local startup | `regulatory-agent-vs5-local-startup` | `work/vs5-local-startup` | `5187` | `8160` | `runs/private/local-startup/` |

VS2 local work and its controlled AWS extension are integrated.
The user approved VS3 locally. Its checked integration merged through PR9.
The user approved VS4 locally and authorized its merge.
VS5 is selected for local development after that merge.
VS4 merged through PR12. VS5 uses that checked integration base.
VS5 browser checks use API port `8151` and their own browser-test database.
Local-startup unit checks use temporary databases and do not launch child processes.
Its real startup verification uses its separate feedback ports and database.
VS4 browser checks use API port `8141` and their own browser-test database.
The VS2 AWS browser checks use API port `8191` and their own browser-test database.
Its feedback ports are reserved. Feedback services are not running from that worktree.
The VS3 candidate contains current `main` changes and VS3 for different integration checks.
Its browser tests use API port `8193` and their own database.
Its feedback ports are reserved. Feedback services are not running from that worktree.
The candidate does not change the review build or establish user acceptance.
Read [the integration contract](spec-slice-03-integration.md) for its acceptance conditions.
Use `browser-tests.sqlite` for browser tests and `feedback.sqlite` for manual feedback in each later database directory.
Stop only the processes owned by the selected slice.
Keep unrelated worktrees and feedback services unchanged.

## Development sequence

1. Read the five approved specifications and the selected slice contract.
2. Record requirements and acceptance IDs before implementation.
3. Write behavior tests that fail for the missing behavior.
4. Save the failing results.
5. Implement the minimum behavior with Ponytail.
6. Run the affected checks and save their passing results.
7. Inspect the interface and request slice feedback.
8. Merge accepted work into `main` after integration checks pass.
9. Test the combined application locally.
10. Deploy the reviewed combined commit through the serialized AWS development workflow.
11. Verify AWS authentication, permissions, service connections, and the deployed user flow.

Local acceptance and AWS release acceptance have different evidence records.
Do not describe local acceptance as a verified AWS release.
Keep the earlier feedback checkpoint before the next slice.
CloudFront verification remains necessary for deployment under D34.
The user can approve continued local development while AWS verification is pending.

The historical worktree guide still records the earlier workspace state.
This guide controls the current port and database assignments.
The [feature tickets](05_FEATURE_TICKETS.md#delivery-slices) control slice scope.
