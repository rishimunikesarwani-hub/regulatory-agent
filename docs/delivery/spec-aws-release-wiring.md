# VS5 AWS release settings

Date: 2026-10-11.
Authorization: The combined AWS release goal and D35 permit this VS5 deployment correction.
Base: Approved PR15 merge `8816e000ad57d164f9dc26c928a482de8dce81eb`.
The [release contract](spec-slice-05-release.md) retains all existing quality and AWS conditions.

## Isolation

Use branch `work/vs5-release-wiring` in worktree `regulatory-agent-vs5-release-wiring`.
Reserve web port `5186`, feedback API port `8152`, and browser API port `8153`.
Keep databases under `runs/private/vs5-release-wiring/` in this worktree.
Keep feedback and browser databases separate.
The existing user demonstration remains on ports `5185` and `8150`.

## Required behavior

Keep assessments disabled by default.
Accept only `true` or `false` for `AWS_DEV_ASSESSMENTS_ENABLED`.
When enabled, require `AWS_DEV_ASSESSMENT_RELEASE_APPROVED_SHA` to equal the exact release commit.
The approved SHA records the operator's release approval. It does not measure quality or verify AWS services.

Set this approval only after the controlling release conditions pass.
Missing approval prevents any deployment command.

Pass the explicit assessment setting to SAM.
SAM is the existing AWS template deployment tool.
Add a stack output for that setting.
Reject a missing or different output before uploading frontend assets.
Use the verified output for the frontend `assessments_enabled` boolean.
Record the setting and the checked feature scope in release evidence.

An ordinary deployed browser check verifies identity, cases, and documents only.
An enabled assessment release needs additional deployed assessment, review, and export checks.
Successful ordinary browser checks cannot verify that additional scope.
Keep an enabled release unverified when its assessment browser result is missing.

## Acceptance cases

| ID | Required result |
|---|---|
| RW01 | Missing assessment setting deploys with the flag false in SAM and frontend configuration. |
| RW02 | True requires approval for the exact commit before any command. Invalid settings fail before commands. |
| RW03 | Missing, malformed, or different stack outputs prevent frontend synchronization and invalidation. |
| RW04 | An approved true setting agrees across SAM, stack output, configuration, and deployment record. |
| RW05 | Workflow inputs and environment settings preserve the false default and exact-commit approval. |
| RW06 | Release evidence states document scope. An enabled release without assessment acceptance stays unverified. |
| RW07 | Deployed assessment checks verify admission, completion, citations, saved review, and JSON and Markdown exports. |

Write failing behavior checks before implementation.
Run these checks without AWS access or model calls.
RW07 needs the actual deployed service flow before AWS acceptance.
Controlled checks cannot establish AWS acceptance.
The local content exception under D64 remains local and fictional.

## Language review

The review preserves approval, default settings, exact commits, and incomplete acceptance conditions.
The complete dictionary review remains incomplete.
Do not claim full ASD-STE100 compliance.
