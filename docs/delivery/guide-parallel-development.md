# Parallel development

Date: 2026-10-10

The user selected a new private GitHub repository named `regulatory-agent`.
Use separate worktrees for the two development sessions.
Keep the approved application scope and ticket dependencies.

## Terms

| Term | Meaning |
| --- | --- |
| Repository | The project files and their recorded history. |
| Commit | A recorded version of selected files. |
| Branch | A separate sequence of commits. |
| Worktree | A separate project folder connected to the same Git repository. |
| Merge | An operation that combines branch changes. |
| Integration tests | Tests that check how connected components work together. |

## Locations

Repository: `https://github.com/rishimunikesarwani-hub/regulatory-agent`

The folders below are relative to the parent `ET-Hackathon` folder.

| Role | Folder | Branch |
| --- | --- | --- |
| Integration | `MVP` | `main` |
| Session A | `.worktrees/regulatory-agent-session-a` | `work/session-a` |
| Session B | `.worktrees/regulatory-agent-session-b` | `work/session-b` |

These branches start from the same checkpoint.
The setup does not start development sessions or application processes.

## Initial work allocation

The PRD defines eight product features.
The delivery plan defines nine tickets, T1 through T9.
The feature count does not remove ticket dependencies.

| Session | Initial work | Dependency |
| --- | --- | --- |
| A | T1 source and fictional fixture preparation | Follow approved source rules. Keep provider selection undecided until the user selects it. |
| B | T2 local tests and shared contracts | Wait for T1 specifications and the minimum labelled fixture before dependent implementation. |

Session B can inspect the specifications while Session A prepares the minimum fixture.
Inspection does not satisfy the T2 implementation gate.
T3 follows T2. T4 follows T3.
T5 and T6 are the first independent implementation tickets after T4.
Assign T5 to Session A and T6 to Session B at that point.
Keep T7, T8, and T9 behind their recorded dependencies.

The [feature tickets](05_FEATURE_TICKETS.md) control task acceptance and sequence.
The [local test plan](../testing/spec-local-test-plan.md) controls software checks.

## File ownership

The integration session owns shared specifications, interfaces, dependency locks, and the project log.
Session B defines the initial shared contracts under T2.
Merge those contracts before dependent feature implementation.
Record any later contract change in the integration session first.

Each development session owns its assigned implementation and tests.
Keep its test results in a distinct dated folder under `runs/`.
Do not edit the other session's worktree.
Do not commit private bank data or credentials.
Keep evaluation cases separate from software tests.

## Development procedure

1. Start the session in its assigned worktree.
2. Read `AGENTS.md` and the assigned ticket.
3. Confirm that the ticket dependencies are complete.
4. Identify the applicable requirement and acceptance IDs.
5. Write the failing behavior test.
6. Record the failing result.
7. Implement the required behavior.
8. Run the relevant tests.
9. Record the passing result and any remaining failures.
10. Review the changed files before a commit.

Default tests must not require credentials or external services.
Use separate local ports and runtime folders for each session.
Do not share a writable local database between worktrees.

## Integration procedure

1. Confirm that both sessions have saved their current work.
2. Review the branch changes against the assigned ticket.
3. Confirm the required test evidence.
4. Merge one branch into `main`.
5. Resolve any conflicts against the approved specification.
6. Run the combined software checks and integration tests.
7. Record the result in `LOG.md`.
8. Push the verified commit to GitHub.
9. Update each session branch from `main` before its next ticket.

Do not mark a ticket complete from branch isolation alone.
Passing local tests does not prove live model quality or AWS deployment.
The user must authorize production deployment separately.

## Current limits

The application is not implemented. No application test command exists yet.
T2 must supply that command before implementation can claim test completion.
The retrieval provider remains undecided.
Six existing ArchView file links in the technical blueprint have missing targets.
The separate Draw.io and SVG architecture files are present.
The Git setup preserves this current documentation state.

Use the [language guide](../guide-ste100-writing.md) for Markdown edits.
Full ASD-STE100 dictionary review remains incomplete.
