# Test Session B

Session B implements T2 local contracts and adapters.
A contract defines the permitted input and output data.
An adapter connects that contract to a service or local resource.

This package does not include the reviewer website.
The controlled demonstration does not assess bank compliance.
The model and regulatory responses use fixed test data.

## Run the checks

Open PowerShell.
Select the worktree.

```powershell
cd 'C:\Users\Be Flith Rich\My Project Folder\ET-Hackathon\.worktrees\regulatory-agent-session-b'
```

Run the local checks.

```powershell
.\.venv\Scripts\python.exe -X utf8 ops/check.py
```

The last line must show `OK`.
A nonzero exit code means that a check failed.
The command runs fixture checks and T2 checks.
It requires no AWS credentials or external service calls.

## Try the demonstration

Run the controlled demonstration.

```powershell
.\.venv\Scripts\python.exe -X utf8 ops/demo.py DEV-02
```

Check these results:

| Result | Expected value |
| --- | --- |
| Label | `Synthetic demo / Simulated model` |
| Saved snapshot | `true` |
| Repeated request uses the same job | `true` |
| Another user cannot read the job | `true` |
| Saved model-call count | `1` |
| Validated model action | `inspect_evidence` |
| Assessment state | `failed` |
| Actual model calls | `0` |
| Current regulatory coverage | `unverified` |

The `failed` assessment state is expected in this demonstration.
The demonstration validates an action but produces no assessment findings.
It must not report a completed assessment.
The command itself exits successfully when the demonstration runs.

Use `DEV-01` or `DEV-03` to inspect another development case.
The command rejects held-out evaluation cases.
It creates a temporary database and removes that temporary database after the demonstration.

ELI10: These checks test the foundation that saves data and controls jobs.
The bank-review screens are a later ticket.

## Set up a clean environment

The required runtime is CPython `3.12.13`.
The setup command requires the `uv` package manager.
Setup can download packages.
The default checks run without external network access.

Run setup in a new source copy.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ops/setup.ps1
```

The exact package versions are in [the dependency lock](../../ops/requirements.lock).
The setup script creates a worktree-local `.venv`.
It does not change the other worktree.

Run the clean-copy verification when dependencies change.

```powershell
.\.venv\Scripts\python.exe -X utf8 ops/clean_check.py
```

This command uses a new temporary source copy, Python environment, and package cache.
It requires package-download access during setup.
It removes its temporary copy after verification.

## Inspect the contracts

Print the generated JSON schemas.

```powershell
.\.venv\Scripts\python.exe -X utf8 ops/demo.py --schemas
```

Read [the T2 contract specification](spec-session-b-contracts.md) for the limits and integration requirements.
Read [the verification record](../../runs/2026-10-10-session-b/verification.md) for the results and remaining work.
