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
The integrated local foundation passed 60 offline tests.
The [combined report](../runs/2026-10-10-integration/combined-tests.txt) records these results.
D24 measurement contracts, application features, live evaluations, and AWS integration are pending.
Read the [remaining worktree guide](delivery/guide-next-worktrees.md) before the next development session.

F3: At least eight features from the hackathon list are mandatory.
D2: Reliability evidence for mostly structured and textual input is mandatory.
Our numerical evaluation limits are additional release requirements.
The organizer did not supply those numerical limits.

## Local operation and AWS operation

**Technical:** Application services use interfaces for storage, records, jobs, identity, and model calls.
Local adapters and AWS adapters obey the same interface contracts.

AWS configuration is a later development step.
The configuration guide must explain each service, action, and verification result.
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
