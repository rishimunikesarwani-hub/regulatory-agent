# Measurement specification verification

Date: 2026-10-10.
Scope: Specification consistency, reference checks, formula examples, and language review.
Application tests and live evaluations did not run.

## Saved change

[D24](../docs/decisions/gov-decision-log.md#d24---reviewer-outcomes-and-measured-agent-baseline) records the user's approved direction.
The [measurement contract](../docs/testing/spec-measurement-contract.md) defines implementation behavior.
The five specifications, local test plan, and AI evaluation plan now reference that behavior.

The north star is approval without edits among finally reviewed items.
Edited and rejected shares use the same denominator.
Adoption including edits is separate.
Review coverage, pending items, result coverage, and failed or partial jobs remain visible.
Reviewer acceptance does not replace the existing correctness gates.

The baseline remains one agent with the approved model.
Retrieval and assessment evaluations remain separate.
Stage traces include identity, source references, attempts, duration, usage, costs, failures, and review outcomes.
Later routing or reviewer experiments must address observed failures.
No application, cloud resource, or model configuration changed.

## Verification evidence

- [Original documents](2026-10-10-before-measurement-spec.zip).
- [Original hashes](2026-10-10-before-measurement-spec.json).
- [Consistency and arithmetic checks](2026-10-10-measurement-spec-check.json).
- [STE mechanical check](2026-10-10-measurement-spec-ste-v5.json).

The consistency check confirmed three new requirements and their acceptance IDs.
It confirmed 11 new software and cloud test groups and six retrieval evaluation groups.
All 20 existing EVAL case rows retain their exact wording.
New local links and anchors resolve.
Six earlier ArchView targets remain missing, as recorded before this task.
This change adds no missing link target.

Independent review checked cohort definitions, concurrent review revisions, and cost accounting.
The final definitions include admitted failed runs, server event ordering, and one effective amount per charge.
The test plan includes the related negative cases.

The formula examples were checked with exact fractions.
Six approved, three edited, one rejected, and two pending items give 60%, 30%, and 10% final-outcome shares.
Review coverage is 10/12. Adoption including edits is 90%.

A successful 20-obligation run and a failed 20-obligation run give result coverage of 20/40.
The checks confirm the example arithmetic. They do not test an application implementation.

The final descriptive STE check found no mechanical findings in the reviewed specification files.
Manual review checked instructions, domain terms, source boundaries, limits, negation, and approval history.
The full official dictionary remains unavailable. Full dictionary and approved-meaning compliance remain unverified.
The Git whitespace check passed after preserving the existing LF line endings.

## Development handoff

Create and freeze source-grounded retrieval and assessment fixtures under T1.
Define executable contracts and one local test command under T2.
Write the named failing tests before their application behavior.
Save actual failing and passing results during implementation.
Run cloud checks and live evaluations separately.
Do not mark these planned tests as passed from this document review.

No numerical reviewer-acceptance target, latency target, or monetary cost ceiling was invented.
Measure the baseline before selecting improvement targets.
