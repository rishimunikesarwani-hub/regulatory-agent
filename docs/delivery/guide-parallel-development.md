# Parallel development

Date: 2026-10-10

The user selected a new private GitHub repository named `regulatory-agent`.
Use different worktrees for development sessions.
Keep the approved application scope and ticket dependencies.

## Terms

| Term | Meaning |
| --- | --- |
| Repository | The project files and their recorded history. |
| Commit | A recorded version of selected files. |
| Branch | A different sequence of commits. |
| Worktree | A different project folder connected to the same Git repository. |
| Merge | An operation that combines branch changes. |
| Integration tests | Tests of how connected components operate together. |

## Locations

Repository: `https://github.com/rishimunikesarwani-hub/regulatory-agent`

The folders below are relative to the parent `ET-Hackathon` folder.

| Role | Folder | Branch |
| --- | --- | --- |
| Integration | `MVP` | `main` |
| Session A | `.worktrees/regulatory-agent-session-a` | `work/session-a` |
| Session B | `.worktrees/regulatory-agent-session-b` | `work/session-b` |

The original Session A and Session B branches started from the same checkpoint.
Their foundations are now integrated through PR #1 and PR #2.
The [remaining worktree guide](guide-next-worktrees.md) gives the next assignments under D26.
The setup does not start development sessions or application processes.

## Initial work allocation

The PRD gives eight product features.
The delivery plan gives nine tickets, T1 through T9.
The feature count does not remove ticket dependencies.

| Session | Initial work | Dependency |
| --- | --- | --- |
| A | T1 source and fictional fixture preparation | Obey approved source rules. Keep provider selection undecided until the user selects it. |
| B | T2 local tests and shared contracts | Wait for T1 specifications and the minimum labeled fixture before you write dependent code. |

Session B can examine the specifications while Session A prepares the minimum fixture.
Inspection does not satisfy the T2 implementation gate.

T3 starts after T2. T4 starts after T3.
After T4, T5 and T6 are the first development tickets that can proceed independently.
The new T5 and T6 worktrees replace the original folder assignments under D26.
Keep the recorded dependencies for T7, T8, and T9.

The [feature tickets](05_FEATURE_TICKETS.md) control task acceptance and sequence.
The [local test plan](../testing/spec-local-test-plan.md) controls software checks.

## File ownership

The integration session owns shared specifications, interfaces, dependency locks, and the project log.
Session B writes the initial shared contracts under T2.
Merge those contracts before you write dependent feature code.
Record any later contract change in the integration session first.
Under D26, the foundation worktree can prepare the approved D24 fixture and contract additions.
The integration session must review and merge these additions before T3 implementation.

Each development session owns its assigned code and tests.
Keep its test results in a different dated folder under `runs/`.
Do not edit the other session's worktree.
Do not commit private bank data or credentials.
Keep evaluation cases in a different data set from software tests.

## Development procedure

1. Start the session in its assigned worktree.
2. Read `AGENTS.md` and the assigned ticket.
3. Make sure that the ticket dependencies are completed.
4. Identify the applicable requirement and acceptance IDs.
5. Write the failing behavior test.
6. Record the failing result.
7. Write the code for the necessary behavior.
8. Do the relevant tests.
9. Record the passing result and any remaining failures.
10. Examine the changed files before a commit.

Default tests must operate without credentials or external services.
Use different local ports and runtime folders for each session.
Do not share a writable local database between worktrees.

## Integration procedure

1. Make sure that both sessions have saved their current work.
2. Examine the branch changes against the assigned ticket.
3. Make sure that the necessary test evidence is available.
4. Merge one branch into `main`.
5. Resolve any conflicts against the approved specification.
6. Do the combined software checks and integration tests.
7. Record the result in `LOG.md`.
8. Push the commit with completed verification to GitHub.
9. Update each session branch from `main` before its next ticket.

Do not give a ticket completed status because it has an isolated branch.
Passing local tests are not sufficient evidence of live model quality or AWS deployment.
Additional user authorization is mandatory for production deployment.

## Current limits

The integrated foundation passed 60 offline tests through `ops/check.py`.
The [testing guide](guide-session-b-testing.md) gives setup and demonstration commands.
T1 and T2 are incomplete against the newer D24 requirements.
T3 through T9 implementation is pending.

The retrieval provider is undecided.
Six existing ArchView file links in the technical blueprint have missing targets.
The additional Draw.io and SVG architecture files are present.
The Git setup keeps this current documentation state.

Use the [language guide](../guide-ste100-writing.md) for Markdown edits.
Save a language review record for the edited text.
