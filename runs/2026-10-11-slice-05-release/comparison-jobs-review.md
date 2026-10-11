# Saved comparison review

Date: 2026-10-11.
Contract: [Comparison jobs](../../docs/delivery/spec-slice-05-comparison-jobs.md).
Decision: D55.

## Implementation

The shared comparison service uses existing local records or native DynamoDB and private S3 records.
It saves the specified version pair, baseline snapshot, original AI mappings, and cited control statements.
Case ownership checks apply before admission and reads.
Saved request keys prevent a second admission after an uncertain acknowledgment.

The saved snapshot selects the comparison model protocol.
Ordinary assessments keep their original model protocol.
The existing India model adapter checks its profile, destinations, call allowance, execution claim, and deadline.
The native worker selects the processing service from its saved snapshot.

Each selected obligation has a separate call and validated result.
The service verifies source originals before processing.
It rejects unsupported control IDs and citations outside the examined context.
Saved results survive interrupted execution without another model call.
Failed processing keeps consumed calls and unchecked obligations.

Applicable changes can admit one new assessment with pinned bank versions and independent review records.
The service rejects unfinished or unresolved comparisons.
Future and unchanged requirements cannot request reassessment.
Comparison jobs stay outside ordinary assessment lists.
The implementation adds no dependency or AWS resource.

## Verification

The first red check failed because the comparison module did not exist.
An initial fixture failed because its baseline had no saved completion stage.
The corrected fixture then ran 11 checks against the implementation stub.
All 11 checks failed before implementation.

The implemented feature passed 11 focused checks.
The complete local backend suite passed 390 checks in 152.716 seconds.
Two additional native SDK and worker checks then joined the focused suite.
All 13 focused checks passed in 5.195 seconds.
These additional checks used controlled SDK responses without external traffic.

The complete local suite preceded the two additional checks.
GitHub must verify the complete final test set at the committed revision.
Browser acceptance and live semantic evaluation remain pending.
Controlled results cannot establish correct real regulatory interpretation or complete REQ-F02 acceptance.

## Language and meaning review

Reference: ASD-STE100 Issue 9, 2025-01-15.
Reviewed files: The new contract, this receipt, D55, and the added ticket and development-guide references.
Protected items: Requirement IDs, test IDs, saved evidence paths, numeric limits, source references, and earlier approval history.
Technical terms: Snapshot, execution claim, model protocol, control mapping, citation, DynamoDB, and S3.
The project glossary gives the existing technical meanings.

The new instructions keep one action and no more than 20 words.
The descriptions use active voice and no more than 25 words.
The review preserves historical processing, fictional data limits, source uncertainty, and the D35 review gate.
Sentence checks do not establish full compliance.
The complete dictionary and approved-meaning review remain incomplete.
