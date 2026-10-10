# Agent comparison verification

Date: 2026-10-10.
Scope: Design comparison and proposed operating contract.

## Files

- [Comparison](../docs/architecture/arch-agent-operation-comparison.md).
- [Operating proposal](../docs/architecture/arch-multi-agent-proposal.md).
- [Decision record](../docs/decisions/gov-decision-log.md#d22---agent-operation-comparison).

## Evidence boundary

The comparison uses the current specifications and primary technical sources.
Two separate reviews examined the cases for one agent and several agents.
The recommendation is a design judgment.
No application tests, model evaluations, or performance measurements ran.

The user requested the architecture direction.
The document marks the detailed role and allowance allocations as proposed.
The current one-agent specifications remain authoritative.
No new agent framework, provider, model, deployment, or crawler was selected.

## Protected requirements

The preservation record covers the five approved specifications and existing diagram sources and outputs found before this task.
See [the file hashes](2026-10-10-before-agent-comparison-hashes.json).
The check covers files present in this working copy.
It does not claim that missing ArchView files were restored.

The proposal retains these requirements:

- One case and one fixed input snapshot per assessment.
- At most 20 selected obligations.
- At most 24 dispatched model calls across the complete job.
- A 600-second deadline from worker start, preserved through retries.
- Current-source verification through the external regulatory API.
- A stop when verification fails or selected versions change.
- Private case isolation and the existing India boundary.
- Separate AI findings and human review decisions.

## Language review

Reference: ASD-STE100 Issue 9 and the installed skill's review rules.
The official dictionary request failed during this task.
Full dictionary and approved-meaning review remains incomplete.

Reviewed sentence length, active wording, consistent terms, conditions, negation, and status labels.
Defined ReAct, runtime, registry, governance, coordinator, and handoff as technical terms.
These definitions do not establish dictionary approval.
Kept identifiers, limits, product names, source links, and status values exact where required.

The local checker uses the stricter procedural mode for all new prose.
The checker result does not certify full STE compliance.
See [the final language check](2026-10-10-agent-comparison-ste-check-v2.json).

## Mechanical checks

The role base allowances total 22 model calls.
The shared reserve contains two additional calls.
The complete allowance is 24 calls.
Local elapsed-time caps total 495 seconds before shared overhead.
The global 600-second deadline always takes precedence.

The local-link and preservation checks cover the changed documents.
No live API or cloud behavior is established by these checks.
