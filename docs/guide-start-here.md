# Project handbook

The application connects regulatory requirements to bank controls and supplied evidence.
A reviewer can examine each finding and its sources.

## Reading order

| Document | Purpose |
|---|---|
| [1. Product requirements](product/01_PRD.md) | Gives the user, eight features, scope, and success criteria. |
| [2. Technical blueprint](architecture/02_TECHNICAL_BLUEPRINT.md) | Gives local operation and AWS connections. |
| [3. Security and access](security/03_SECURITY_ACCESS.md) | Gives permissions, private data rules, and agent limits. |
| [4. Frontend specification](frontend/04_FRONTEND_SPEC.md) | Gives the reviewer interface and source inspection. |
| [5. Feature tickets](delivery/05_FEATURE_TICKETS.md) | Gives task order, dependencies, and acceptance checks. |
| [Decision history](decisions/gov-decision-log.md) | Records approvals, reasons, replacements, and uncertainties. |
| [Local test plan](testing/spec-local-test-plan.md) | Gives tests of application behavior. |
| [AI evaluation plan](testing/eval-model-quality.md) | Gives measurements of model quality. |
| [Measurement contract](testing/spec-measurement-contract.md) | Gives reviewer acceptance, retrieval quality, assessment checks, stage traces, and runtime measurements. |
| [STE language guide](guide-ste100-writing.md) | Gives the document language and project terms. |

## Status definitions

- **Approved:** The user selected a design.
- **Implemented:** The necessary code exists.
- **Verified:** A specified check gave evidence.
- **Achieved:** All necessary acceptance conditions passed.

The product and architecture have approval.
The integrated foundation passed its initial 60 offline tests.
The first slice now includes the browser interface and persistent case storage.
Read the [current verification records](../runs/2026-10-10-autonomous-build/) for local results.

D24 measurement functions have unit tests.
Complete runtime measurement integration and live evaluations are pending.
AWS templates are prepared, but AWS deployment is unverified.
The AWS development access setup is installed.
CloudFront distribution creation needs AWS account verification under D34.
The [verification guide](delivery/guide-aws-cloudfront-verification.md) gives the user's remaining Support steps.
The USD 25 monthly alert is configured and healthy.
The alert is not a spending cap.

The user approved VS1 locally and authorized VS2 local development.
The VS2 document flow passed 178 combined Python checks and 20 combined browser checks.
The user approved VS2 locally and authorized VS3 local development.
VS2 local work merged through PR8 after its checks passed.
The controlled AWS document extension merged through PR10 after its checks passed.
The focus correction then merged through PR11 after its checks passed.
The combined checks passed 204 Python tests and 27 browser tests.
Read the [cloud preparation guide](delivery/guide-slice-02-aws-documents.md) for the remaining deployment conditions.
VS3 is ready in its separate review worktree at `http://127.0.0.1:5183/`.
The user review and subsequent integration remain pending.
The [integration candidate](delivery/spec-slice-03-integration.md) contains VS3 and current `main` changes for different checks.
This candidate does not change the running review build or establish user acceptance.
AWS application acceptance stays pending.
Read the [VS2 development guide](delivery/guide-slice-02-development.md) for local review.
The [workspace guide](delivery/guide-slice-workspaces.md) controls the current branches, ports, and databases.

F3: At least eight features from the hackathon list are mandatory.
D2: Reliability evidence for mostly structured and textual input is mandatory.
Our numerical evaluation limits are additional release requirements.
The organizer did not supply those numerical limits.

## Local operation and AWS operation

**Technical:** Application services use interfaces for storage, records, jobs, identity, and model calls.
Local adapters and AWS adapters obey the same interface contracts.

Each slice includes its AWS configuration and verification steps.
The [first-slice guide](delivery/guide-slice-01-development.md) gives the local commands and missing AWS setup.
An AWS account is not necessary for default local tests.

## Document updates

Record each important decision in its specification and the decision log.
Include its date, status, reason, and related requirement and test IDs.
Keep the previous decision when a new decision replaces it.

Read [the project log](../LOG.md) to continue the work.
Read [the project instructions](../AGENTS.md) before changes.
Use each document's Next link to continue in order.

## Current language rule

Use ASD-STE100 for all project Markdown under [D18](decisions/gov-decision-log.md#d18--project-markdown-language).
This rule replaces D12's Rishi Voice treatment.
It extends [D17](decisions/gov-decision-log.md#d17--technical-blueprint-language) from the blueprint to all project Markdown.

The language review includes selected dictionary entries and their approved meanings.
It is not a full compliance assessment.
Structural checks and checks for unchanged meaning are different from this language review.

[Next: Product requirements](product/01_PRD.md)
