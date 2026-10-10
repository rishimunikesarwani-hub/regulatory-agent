# Architecture language review

Date: 2026-10-09.
Scope: [Technical Blueprint](../docs/architecture/02_TECHNICAL_BLUEPRINT.md).
Reviewer: Codex.
Result: STE-oriented revision. Vocabulary review remains incomplete.

## Review method

The review used the installed ASD-STE100 skill, its review contract, and its rule checklist.
It also used the [project language guide](../docs/guide-ste100-writing.md).
The complete blueprint and decision log were read before editing.
No OPEN observation applied specifically to this skill.

The [preserved source](2026-10-09-before-archview-blueprint.txt) is the comparison input.
The review covered instructions, descriptions, tables, fixed labels, and approval metadata.
It preserved the existing headings and section links.
This receipt covers the language revision before the architecture views were added.

## Edition and evidence limit

The selected reference is [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf).
The official PDF request returned HTTP 403 during this review.
The [official downloads page](https://www.asd-ste100.org/STE_downloads.html) also returned HTTP 403.
The complete rule text and dictionary were unavailable.

The review applied the available rule checklist.
It did not verify every word against the official dictionary.
Approved meanings, grammatical roles, and permitted word forms remain unverified where dictionary evidence was unavailable.
The result does not establish full compliance or ASD approval.

## Changes and meaning review

| Location | Original phrase | Revised phrase or action | Check | Meaning | Result |
|---|---|---|---|---|---|
| Request flow, step 6 | If versions changed | If selected versions changed | Makes the existing selection scope explicit. | PASS | RESOLVED |
| Request flow, request duration | Instruction and explanation in one paragraph | Separate the instruction from its explanation. | Separates text types. | PASS | RESOLVED |
| Current regulatory sources | A future-effective amendment | An amendment with a future effective date | Removes an unusual compound adjective. | PASS | RESOLVED |
| Current regulatory sources | Use identifiers when available | Put the availability condition first. | Procedure condition order. | PASS | RESOLVED |
| Current regulatory sources | Create a version when content changes | Put the existing change condition first. | Procedure condition order. | PASS | RESOLVED |
| Current regulatory sources | No direct RBI API ... has been verified | The project has not verified a direct RBI API ... | Uses the project as the known actor. | PASS | RESOLVED |
| Current regulatory sources | Eight sentences in one paragraph | Separate release behavior, test evidence, future monitoring, and authority. | One topic per paragraph. | PASS | RESOLVED |
| Agent actions | Request another pass when evidence is insufficient | Put the insufficient-evidence condition first. | Procedure condition order. | PASS | RESOLVED |
| Inspected evidence | Do not count a passage if retrieval did not return it | Put the retrieval condition first. | Preserves the evidence prohibition. | PASS | RESOLVED |
| Inspected evidence | Error measurement in the same paragraph | Separate the measurement instruction. | One topic per paragraph. | PASS | RESOLVED |
| Retries and failures | Definition after the reservation instruction | Put the definition before the instruction. | Explains the term before use. | PASS | RESOLVED |

Each changed instruction retains its original actor, object, condition, limit, and consequence.
Negation, obligation, permissions, operation order, and failure behavior remain unchanged.
No change approves a provider, crawler, OCR process, implementation, or deployment.

## Protected content

| Item | Review result |
|---|---|
| Configuration table and model identifiers | Exact text retained. |
| Record names, fields, and required conditions | Exact table retained. |
| All table rows | Exact text retained. |
| Headings and existing link targets | Exact text retained. |
| Numbers, units, dates, limits, code, and external URLs | No differences in the skill comparison. |
| Selected India profile and permitted regions | Requirements retained. |
| Model calls, retrieval counters, and job deadline | Requirements retained. |
| Approval history and implementation status | Statements retained. |
| Current-source checks, version review, and failure blocks | Conditions retained. |
| Ownership, source locations, immutable snapshots, and human review | Requirements retained. |

## Technical terms

The approved specification controls these domain meanings.
The [project glossary](../docs/guide-ste100-writing.md#project-terms) remains the shared term reference.
These entries record domain use. They do not establish dictionary approval.

| Term | Role and form | Meaning in this document | Owner and evidence |
|---|---|---|---|
| Adapter | Technical noun. Singular or plural. | Code that connects an application interface to a resource or service. | Project specification. Architecture section and glossary. |
| API | Technical noun and abbreviation. | A defined software connection for requests and responses. | Project specification. Glossary and component table. |
| Bounded agent | Technical noun. | An agent subject to explicit tool, data, call, and time limits. | Project specification. Agent rules and glossary. |
| BM25 | Technical name. | The selected method for ranking retrieved passages. | Project specification. D09 and agent rules. |
| ETag | Technical noun. | An identifier for a particular HTTP representation. | Project specification. Current-source section and retained RFC link. |
| Freshness status | Technical noun. | A record of whether current-source verification succeeded for the run. | Project specification. D20 and current-source section. |
| Snapshot | Technical noun. | A fixed copy of selected inputs and versions. | Project specification. Record table and glossary. |
| Atomic reservation | Technical noun. | A reservation that completes as one indivisible operation. | Project specification. Retry section. |
| Idempotency key | Technical noun. | An identifier for repeated requests for the same operation. | Project specification. API section and glossary. |
| IAM, S3, SQS, Cognito, DynamoDB, Lambda, Bedrock, SAM | Technical names. Exact forms retained. | The named AWS components in the approved design. | Project specification. D08 and configuration table. |

## Completed checks

The skill checker self-test passed.
The [procedural check](2026-10-09-architecture-ste-procedural-check.json) examined 355 sentence units with zero findings.
The [descriptive check](2026-10-09-architecture-ste-descriptive-check.json) examined 355 sentence units with one finding.
Both checks used the preserved source for comparison.

The descriptive finding concerns the opening metadata block.
The checker combines six labelled metadata lines into one eight-sentence paragraph.
Manual review treated these lines as separate metadata entries.
The approval and reference text remains unchanged.

The procedural check uses the stricter 20-word limit for all examined sentences.
The descriptive check also checks paragraph length.
Tables, labels, and protected content require manual interpretation.
No arbitrary phrase exemptions were supplied.

Manual review covered conditions, compound terms, voice, verb forms, contractions, paragraph topics, instruction order, punctuation, and consistent domain use.
The source comparison also covered technical requirements, permissions, prohibitions, and uncertainty.
The checker cannot establish meaning preservation by itself.

Exact comparisons passed for all headings, table rows, link targets, and approval metadata.
Counts of must, may, cannot, can, and only remained unchanged.
The active-voice revision replaced one No with one not.
Manual review confirmed that this change preserves the lack of verification.

## Remaining limits

A complete official dictionary and approved-meaning review remains open.
Product names, field lists, and technical terms retain their required forms.
The review did not revalidate AWS capability claims or test the application.
The project remains an approved design without implementation evidence.
