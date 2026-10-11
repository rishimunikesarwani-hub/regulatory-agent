# Regulatory change validation review

Date: 2026-10-11.
Contract: [Specified version pairs](../../docs/delivery/spec-slice-05-change-validation.md).
Decision: D54.

## Scope

The component prepares specified regulatory source pairs and validates model interpretation records.
Original hashes, passage locations, dates, selected scope, and baseline control mappings control acceptance.
The code does not infer requirement changes from text differences.
Missing metadata stays unknown.
Future effective changes do not request assessment processing for an earlier date.

The interpretation keeps requirements, conditions, exceptions, applicability, and citations from both versions.
Added and withdrawn classifications have different before and after structures.
Undetermined results keep uncertainty without claiming affected controls.
The component does not write sources, snapshots, findings, or human reviews.

## Failing and passing checks

The initial import check failed because the component did not exist.
The subsequent behavior checks used empty function bodies.
The 12-check run failed through missing results or missing rejection of invalid input.
It recorded 40 failures and four errors.
The first implementation passed those 12 checks.

Additional checks exposed whitespace-only quotes in the shared assessment citation validator.
Another check exposed an unchanged classification with a different requirement statement.
Both failures were recorded before their corrections.
The corrected focused suite passed all 15 checks.

Comparison validation now uses the shared assessment citation validator.
Both paths reject whitespace-only quotes.
Unchanged requirement statements must match after whitespace normalization.
Wording-only and appearance-only results must keep conditions, exceptions, and applicability unchanged.

The first full suite passed 377 checks and failed W14.
The child did not reserve its call before the supervisor's first renewal.
The comparison checks passed.
W14 now starts with one saved reservation and an expired lease.
Its child cannot add another reservation.
The test keeps the original deadline, timeout classification, saved budget, and stopped-child assertions.

The corrected worker suite passed all 14 checks in 30.039 seconds.
No production worker behavior changed for this fixture correction.

The next complete backend suite passed all 378 checks in 152.826 seconds.
Inspection of the other citation paths then found the same whitespace problem in saved exports.
VC16 reproduced a successful export with a whitespace-only saved quote.
The correction uses one citation-resolution rule for pipeline, controlled assessment, comparison, and export validation.
The final focused suite passed all 16 checks.

The final complete backend suite passed all 379 checks in 161.922 seconds.

## Evidence and remaining work

The saved receipts contain the failed and passed checks.
These checks use controlled public source text and model response records.
They do not use AWS credentials, live inference, or provider calls.

Structural validation cannot establish semantic support for a model interpretation.
Durable admission, bounded model processing, native comparison routes, and browser acceptance remain unfinished.
Applicable changed requirements must still cause a new assessment snapshot in the complete flow.
Provider verification, live quality, AWS authentication, and deployed acceptance remain pending.
VS5 remains a draft under D35.
