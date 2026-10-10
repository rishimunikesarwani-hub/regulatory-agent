# Session A foundation guide

Date: 2026-10-10
Branch: `work/session-a`
Scope: T1 source records and test fixtures.

## What is ready

The package contains one official historical source and nine exact source passages.
It also contains four explicitly simulated rule versions.
There are three development cases and 20 separate evaluation cases.
The 30 software tests pass in the worktree and a clean temporary copy.

This work prepares Feature 1, regulatory knowledge ingestion.
It supplies known inputs for later assessment features.
It does not implement ingestion, retrieval, an assessment agent, or a user interface.

T1 remains in progress.
The external provider remains undecided.
Current regulatory coverage remains unverified.
The [foundation specification](spec-session-a-foundation.md) defines the completed scope.

## Run the checks

Use PowerShell from the Session A folder.

```powershell
cd "C:\Users\Be Flith Rich\My Project Folder\ET-Hackathon\.worktrees\regulatory-agent-session-a"
py -X utf8 -B -m unittest discover -s tests -p test_session_a_fixtures.py -v
py -X utf8 -B ops/session_a_fixtures.py validate
py -X utf8 -B ops/session_a_fixtures.py inspect DEV-02
```

The verified runtime is Python 3.14.6.
The commands use only the Python standard library.
No dependency installation, credentials, or AWS account is required.
The tests block network access inside the test process.
The inspection command reads local files only.

Add `--json` to show the complete development record and its expected answer.
The inspector rejects evaluation IDs such as `EVAL-01`.
This restriction prevents accidental inspection through this command.
It is not a security boundary for repository readers.

## Inspect the examples

The output shows the benchmark author's expected answer.
No model generates these answers.

| Case | Supplied records | Expected answer |
| --- | --- | --- |
| DEV-01 | Policy, session inventory, logs, supervision, and completed review | `supported` |
| DEV-02 | Policy promise without operational records | `needs_review` |
| DEV-03 | Incident record confirms disabled activity logging | `gap` |

For `DEV-02`, the next required input is operational evidence.
A policy states what the bank intends to do.
It does not prove that the bank performed the control.

Read the [recorded command output](../../runs/2026-10-10-session-a/inspection.txt).
Read the [verification record](../../runs/2026-10-10-session-a/guide-verification.md).

## How this enters the application

1. Integrate the reviewed Session A changes.
2. Use the development inputs and answers to build the T2 contracts.
3. Use the source passages to test T3 citation and version handling.
4. Build the first complete assessment under T4.
5. Reserve the 20 evaluation cases for the later live quality checks.

Session B owns the application contracts and test environment.
The fixture format does not define an application API.
Bank documents are fictional text records inside JSON files.
Later parser tests still need PDF, DOCX, TXT, and CSV input files.

The integration session owns shared specifications and `LOG.md`.
It must reconcile their status when these changes are merged.
Session A keeps its verification record separate to preserve that ownership.

## RAG and retrieval

RAG means retrieval-augmented generation.
The system retrieves evidence before the model generates an assessment.
Retrieval is one part of RAG.

The approved design has three stages:

1. An external API supplies regulatory text and current-version information.
2. Internal keyword/BM25 search selects passages from authorized case records and selected regulatory versions.
3. The model uses those passages to produce a cited assessment.

BM25 ranks passages through query-term matches and frequency.
This design does not require a vector database.
No retrieval engine or model call is implemented in this package.

In everyday words, this package supplies checked practice records and answer keys.
The later agent must find the right records and explain its answer from them.

## Files and terms

| Item | Location or meaning |
| --- | --- |
| Fixture | Fixed test data with a specified purpose. |
| Snapshot | The selected document versions for one assessment. |
| Hash | A file fingerprint that changes when its bytes change. |
| Held-out case | A case reserved for evaluation rather than prompt development. |
| Source provenance | The authority, URL, dates, original bytes, and file hash. |
| Source files | [Source manifest](../../data/sources/source-manifest.json). |
| Development inputs | [Input file](../../data/fixtures/development-inputs.json). |
| Development answers | [Answer file](../../data/fixtures/development-labels.json). |
| Evaluation inputs | `evals/fixtures/held-out-inputs.json`. |
| Evaluation answers | `evals/fixtures/held-out-labels.json`. |
| Frozen hashes | [Freeze manifest](../../data/fixtures/freeze-manifest.json). |
| Validator and inspector | [Python command](../../ops/session_a_fixtures.py). |
| Software tests | [Test module](../../tests/test_session_a_fixtures.py). |

Each input records its owner, case, profile, period, selected versions, and document passages.
The assessment date can follow the evidence period to include its completed review.
Each answer records the status, element outcomes, mapping, permitted citations, rationale, and missing information.
Each citation records its case, owner, document, version, passage, location, and exact quote.
Untrusted proposed references remain separate from permitted citations.

Use only input files in model requests.
Keep answer files outside prompts.
Do not tune prompts against evaluation answers.
Record any later contamination or changes before another evaluation.

## Source and review limits

The RBI source is a historical version dated 2023-11-07.
Its stated commencement date is 2024-04-01.
The source copy records evidence for fixed historical cases.
It does not replace the external retrieval API.

HTML passages use clause locations.
Whitespace and HTML entities are normalized for matching.
Original HTML bytes and footnote markers are preserved.
The quoted RBI text is fixed source content.

Constructed changes are synthetic regulatory simulations.
They are not actual RBI amendments or verified API responses.
Expected answers have no qualified regulatory expert review.
No live model evaluation has run.
Passing fixture tests does not establish regulatory accuracy or application security.

The Markdown uses the ASD-STE100 skill and mechanical checks.
Full official dictionary and approved-meaning review remains incomplete.
