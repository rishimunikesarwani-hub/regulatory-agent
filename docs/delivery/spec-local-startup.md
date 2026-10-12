# Portable local startup

Date: 2026-10-11. Decision: D67.
Requirements: REQ-X06, LD09, and LS01 through LS07.

The user deferred AWS and authorized continued local development.
This correction lets a developer start the accepted local application after downloading its source.
It does not replace AWS acceptance or model-quality requirements.

## Workspace

Use branch `work/vs5-local-startup` in worktree `regulatory-agent-vs5-local-startup`.
Reserve web port `5187` and API port `8160`.
Use `runs/private/local-startup/feedback.sqlite` for manual checks.
Use temporary databases for startup tests.
Keep the existing demonstration on ports `5185` and `8150` unchanged.

## Acceptance

| ID | Required behavior |
|---|---|
| LS01 | A missing OpenAI key stops configuration checks and startup before child processes start. Error messages exclude configuration values. |
| LS02 | A developer can select separate web and API ports and an ignored database path. All launched processes receive these settings. |
| LS03 | An occupied required port stops startup before child processes start. The launcher does not stop another server. |
| LS04 | Invalid ports, equal ports, and database paths outside `runs/private/` stop startup. |
| LS05 | Missing frontend dependencies give setup instructions before child processes start. API-only operation does not require frontend dependencies. |
| LS06 | The repository supplies an empty key template and setup instructions without machine-specific paths. Langfuse remains optional. |
| LS07 | A source archive starts without Git metadata or a Git executable. Its runtime version is `source-archive`, not a commit claim. |

Configuration checks do not dispatch a model request or establish API credit.
The default ports and database remain compatible with the accepted demonstration.
Fictional content capture stays disabled by default.
Only the existing D64 setting permits eligible fictional content in Langfuse.

Write failing startup checks before the implementation.
Verify the real local launcher with separate ports and storage after the checks pass.
Keep software checks separate from live model-quality evaluations.

## Terms

**Launcher:** The program that starts the local API and browser server.
**Child process:** A program that the launcher starts.
**Port:** A numbered network endpoint used by a local server.
**Configuration template:** A file with setting names and no credentials.
**Source archive:** A downloaded copy of repository files without Git metadata.
