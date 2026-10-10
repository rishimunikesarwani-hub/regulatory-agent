# Project handbook

The application connects regulatory requirements to bank controls and supplied evidence.
A reviewer can inspect each finding and its sources.


## Reading order

| Document | Purpose |
|---|---|
| [1. Product requirements](product/01_PRD.md) | Defines the user, eight features, scope, and success criteria. |
| [2. Technical blueprint](architecture/02_TECHNICAL_BLUEPRINT.md) | Specifies local operation and AWS connections. |
| [3. Security and access](security/03_SECURITY_ACCESS.md) | Specifies permissions, private data rules, and agent limits. |
| [4. Frontend specification](frontend/04_FRONTEND_SPEC.md) | Specifies the reviewer interface and source inspection. |
| [5. Feature tickets](delivery/05_FEATURE_TICKETS.md) | Specifies task order, dependencies, and acceptance checks. |
| [Decision history](decisions/gov-decision-log.md) | Records approvals, reasons, replacements, and uncertainties. |
| [Local test plan](testing/spec-local-test-plan.md) | Specifies tests of application behavior. |
| [AI evaluation plan](testing/eval-model-quality.md) | Specifies measurements of actual model quality. |
| [STE language guide](guide-ste100-writing.md) | Specifies the document language and project terms. |

## Status definitions

- **Approved:** The user selected a design.
- **Implemented:** The required code exists.
- **Verified:** A specified check produced evidence.
- **Achieved:** All required acceptance conditions passed.

The product and architecture have approval.
The project has no verified application results.

F3 requires at least eight features from the hackathon list.
D2 requires demonstrable reliability on mostly structured and textual input.
Our numerical evaluation limits are additional release requirements.
The organizer did not supply those numerical limits.

## Local operation and AWS operation

**Technical:** Application services use interfaces for storage, records, jobs, identity, and model calls.
Local adapters and AWS adapters implement the same interfaces.

AWS configuration is a later implementation step.
The configuration guide must explain each service, action, and verification result.
Default local tests do not require an AWS account.

## Document updates

Record each material decision in its specification and the decision log.
Include its date, status, reason, and related requirement and test IDs.
Keep the old decision when a new decision replaces it.

Read [the project log](../LOG.md) to continue the work.
Read [the project instructions](../AGENTS.md) before changes.
Use each document's Next link to continue in order.

## Current language rule

Use ASD-STE100 for all project Markdown under [D18](decisions/gov-decision-log.md#d18--project-markdown-language).
This rule replaces D12's Rishi Voice treatment.
It extends [D17](decisions/gov-decision-log.md#d17--technical-blueprint-language) from the blueprint to all project Markdown.

The full dictionary and approved-meaning review remains unverified.
Keep that limit separate from the completed structural and meaning-preservation checks.

[Next: Product requirements](product/01_PRD.md)
