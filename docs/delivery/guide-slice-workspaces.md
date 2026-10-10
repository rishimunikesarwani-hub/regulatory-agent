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
| VS3 | `regulatory-agent-t4-assessment` | `work/t4-assessment` | `5183` | `8130` | `runs/private/slice-03/` |
| VS4 | `regulatory-agent-t5-agent` | `work/t5-agent` | `5184` | `8140` | `runs/private/slice-04/` |
| VS5 | `regulatory-agent-t9-quality` | `work/t9-quality` | `5185` | `8150` | `runs/private/slice-05/` |

VS2 is selected for local development after the user's VS1 acceptance.
The VS3 through VS5 assignments are reserved until their slice is selected.
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
