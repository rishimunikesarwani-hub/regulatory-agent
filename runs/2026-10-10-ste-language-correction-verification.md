# STE language correction record

Date: 2026-10-10.
Scope: The 19 maintained Markdown documents in the source backup.
Decision: [D25](../docs/decisions/gov-decision-log.md#d25---permanent-documentation-language-rule).

## Request and result

The user requested ASD-STE100 documentation and a permanent rule in the local AGENTS.md.
The [local instructions](../AGENTS.md#documentation-language-always-use-asd-ste100) now make STE mandatory for new documentation and each document change.
The rule includes a skill review, dictionary review, meaning review, and mechanical checks.

Corrected the 19 maintained documents with the ASD-STE100 skill.
The [language guide](../docs/guide-ste100-writing.md) gives the writing procedure, dictionary decisions, and project terms.
Earlier records in runs/ keep their dated evidence and results.

## Reference and review

Reference: [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf), dated 2025-01-15.
The complete official PDF has 434 pages.
The standard and dictionary were available for this correction.
An earlier HTTP 403 response did not prevent access through a later public download.

The reference copy and extracted text are in the ignored runs/private/ folder.
They are not project deliverables.

The manual review included instructions, descriptions, active voice, paragraph structure, grammar, word meaning, and part of speech.
It included technical nouns and verbs in their subject context.
The dictionary decisions included check, test, verify, preserve, retain, main, create, run, remain, and separate.
The language guide records source pages and replacement wording.

Fixed identifiers, code, model IDs, source quotations, and link targets have exact-text protection.
Some historical headings keep their original wording to protect existing anchors.
A technical term is not permission to use an ordinary word with an unapproved meaning.

## Meaning checks

The source [archive](2026-10-10-before-ste-language-correction.zip) contains the 19 documents before this correction.
The [source manifest](2026-10-10-before-ste-language-correction.json) contains their paths and hashes.
The comparison used this archive, including changes from earlier tasks.

The review kept these decisions unchanged:

- One agent with the approved in.openai.gpt-5.6-luna model.
- The 24-call allowance and 600-second worker deadline.
- India-only private processing and the external regulatory API.
- Original AI items, saved review events, and reviewer outcome formulas.
- Different evaluations for provider coverage, passage retrieval, and assessment quality.
- Trace records, privacy rules, usage measurements, cost calculations, and retry limits.
- Existing quality gates, test outcomes, ticket dependencies, and approval history.

An independent review found two possible meaning changes in the measurement contract.
The corrected text keeps evidence that the assessment examined, including evidence not accepted.
The corrected text applies the quality gate to selection of a new baseline.
The earlier candidate experiment is still permitted.

A history review also kept two original conditions precise.
A silent fallback is different from an automatic fallback.
A record of no evaluation execution is different from a record of no result.
The corrected decision history keeps the original conditions.

## Verification results

The [mechanical results](2026-10-10-ste-correction-full-v2.json) record both checker modes.
The earlier [comparison results](2026-10-10-ste-correction-protected-v2.json) record protected text, document hashes, and links.

- The saved whole-project check applies to an earlier revision.
- Later wording corrections do not have a completed whole-project check.
- Original requirement, test, ticket, and decision ID occurrences are present.
- Application model IDs, numeric limits, formulas, and code blocks are unchanged.
- All 115 ticket checkbox states and their sequence are unchanged.
- New numbers describe language rules, review dates, dictionary pages, or split procedure steps.
- Local links have no new missing target.
- Six earlier ArchView targets are still missing.
- Changed Markdown uses LF line endings.
- The Git whitespace check passed.

The language guide has new section titles and current reference information.
The local instructions have a new language heading and review procedure.
D25 and the project log record the user's permanent language rule.
These documentation changes do not change the application design.

## Limits

The mechanical checker finds selected structural errors.
A clean result is not ASD approval or formal STE certification.
The manual review used the official rules, dictionary entries, and the project technical context.
This record does not claim external certification.

Application code, software tests, live model evaluations, and AWS deployment were outside this language correction.
No application test result or measured quality improvement is claimed.

The extra review stopped after the user raised the task cost.
The permanent language rule is saved.
No further review work is active.
