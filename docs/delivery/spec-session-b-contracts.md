# Session B local contracts

Date: 2026-10-10.
Scope: T2.
Related requirements: REQ-X06 and the shared contracts for REQ-F01 through REQ-F08.

## Dependency evidence

Session A supplied three development cases and 20 separate held-out cases.
Session B verified the frozen file hashes before copying the handoff.
The import receipt is [t1-import.json](../../runs/2026-10-10-session-b/t1-import.json).
The copied source contains one real historical RBI version and four explicit simulations.
The fixture does not establish current regulatory coverage.

T1 provider selection remains open.
The minimum labelled fixture permits T2 work under the development guide.
T2 does not select a regulatory provider.

## Executable contracts

[contracts.py](../../src/regulatory_agent/contracts.py) defines validated input and output models.
It rejects unknown fields and invalid types.
Public request models exclude caller-supplied owner identities.
The future HTTP handler must obtain the owner from authenticated identity.

The `API_CONTRACTS` table covers all 14 approved API operations.
Schemas define case, source, upload, assessment, comparison, job, finding, review, export, and safe-error data.
The package also defines snapshots, obligations, controls, model actions, and regulatory responses.
These schemas do not implement HTTP handlers.

[ports.py](../../src/regulatory_agent/ports.py) defines shared adapter interfaces.
Local records and jobs use SQLite transactions.
Local blobs use immutable files with content hashes and case authorization.
AWS adapters must satisfy these interfaces during T8.
No AWS adapter has been implemented or tested.

The job adapter saves deadlines, allowances, execution claims, and completed stages.
A claim gives one worker permission to process the job.
A later claim invalidates the earlier worker token.
The claim lasts 30 seconds between short stages or dispatch reservations.
Handlers must save progress within that period.
Handlers must tolerate repeated execution after a process stops before it saves a stage.

The runner resumes interrupted jobs after claim expiry.
Terminal jobs remain terminal.
User-requested retry behavior and HTTP retry handlers remain part of T6.
Retries must retain the saved deadline and allowances.

Large regulatory response pages use blob storage.
The job record stores their references.
Stage records are bounded to 400,000 UTF-8 bytes.
Stages must contain validated outputs or references, not operational logs of prompts or responses.

## Extraction limits

These T2 defaults make the approved extraction limit executable.
They do not implement file parsing or upload handlers.

| Quantity | Contract |
| --- | --- |
| File size | At most 10,000,000 bytes. |
| Selected case documents | At most 10. |
| Extracted page equivalent | 4,000 UTF-8 bytes of extracted text. Round upwards. |
| PDF units | The larger of actual PDF pages and the extracted page equivalent. |
| DOCX, TXT, CSV units | The extracted page equivalent. Keep original paragraph, line, or row locations. |
| Aggregate case scope | At most 100 units, including selected regulatory content. |
| Empty or unsupported extraction | Reject. Do not truncate. |

T3 must include every selected document when it calls the aggregate limit check.
The equivalent count is a processing limit.
It is not an invented source page number.
The integration owner must incorporate these defaults into the controlling specifications before T3.

## Regulatory retrieval limits

| Quantity | Contract |
| --- | --- |
| Source query | Explicit public source IDs from an application-configured catalogue. |
| Private query fields | Reject. |
| Requests per job | At most 20, including retries. |
| Retries per page attempt | At most two retries after the first dispatch. |
| Pages per retrieval | At most 10. |
| Per-request timeout | At most 10 seconds within the saved job deadline. |
| Response size | At most 1,000,000 serialized UTF-8 bytes per page. |
| Total response size | At most 10,000,000 serialized UTF-8 bytes per retrieval. |
| Combined regulatory text | At most 400,000 UTF-8 bytes, subject to the remaining case allowance in T3. |
| Model calls | Separate saved allowance of 24. |
| Worker deadline | 600 seconds from the first worker start. |

The controlled adapter simulates timeout and provider failures.
It does not implement an HTTP transport or enforce a real network timeout.
The live adapter must enforce these limits before reading an unlimited response.
It must reject private destination addresses and unapproved redirects before dispatch.
The public source URL validator permits only HTTPS RBI authority URLs.
Other authorities require an explicit contract revision.

Verification must occur between the job start and the current check time.
Missing authority timestamps, incomplete amendments, incomplete pagination, and unverified synchronization block acceptance.
Conditional responses require a matching cached validator and a new authority verification time.
Withdrawals, future-effective selections, and changed selected fingerprints block acceptance.
Fingerprints include content, dates, amendments, source identity, and withdrawal state.

A future amendment can remain in amendment metadata.
It cannot silently replace the selected rule for an earlier assessment date.
The live provider must supply the applicable version.

Every controlled response retains the `Simulated` label.
Its `live_current_coverage` value remains `false`.
Saved source copies cannot establish current coverage independently.

## Test boundaries

The default command installs a Python network guard in each test process.
Child Python workers inherit the guard through `sitecustomize.py`.
The tests verify blocked external DNS, external connections, and allowed loopback connections.
The guard is a Python test control, not an operating-system firewall.
It does not sandbox arbitrary native executables.

The tests exercise actual SQLite and filesystem adapters.
Controlled responses exercise schema, allowance, and failure behavior.
They do not measure model accuracy or regulatory completeness.

The dependency lock pins all installed packages.
FastAPI recommends selecting and testing compatible versions before upgrades.
See [FastAPI version guidance](https://fastapi.tiangolo.com/deployment/versions/).
The models use [Pydantic strict validation](https://pydantic.dev/docs/validation/latest/concepts/strict_mode/).

## Integration handoff

Review the new contracts before dependent implementation.
Keep Session A fixture files byte-identical during integration.
Merge T1 fixture changes before T2 adapter changes.
Update shared specifications, the root manifest, and `LOG.md` from the integration session.
Preserve the recorded approval history.

T3 owns file parsing, document eligibility, exact citations, and the live retrieval connection.
T4 owns the complete assessment sequence.
T6 owns HTTP handlers, authenticated requests, and operational retry behavior.

T7 owns the reviewer interface.
T8 and T9 own live AWS verification and model-quality evidence.

No merge, push, production deployment, or submission forms part of this handoff.

## Language review

The new prose follows the project STE writing rules.
Technical terms use the [project glossary](../guide-ste100-writing.md#project-terms).
A fingerprint identifies selected content and regulatory metadata through a computed hash.
An execution claim identifies the worker that can change a running job.
These are project technical terms, not verified dictionary approvals.

The complete official Issue 9 PDF remained unavailable during this review.
Full dictionary and approved-meaning compliance remain unverified.
