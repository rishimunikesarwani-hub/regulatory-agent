# ET-Hackathon MVP instructions

These instructions apply to this folder and its subfolders.
Keep the source PDF in the parent project's hackthon_data folder.

## Required documents

Read the [handbook](docs/guide-start-here.md).
Then read the [decision log](docs/decisions/gov-decision-log.md).

The five approved specifications are:

1. [PRD](docs/product/01_PRD.md).
2. [Technical Blueprint](docs/architecture/02_TECHNICAL_BLUEPRINT.md).
3. [Security & Access](docs/security/03_SECURITY_ACCESS.md).
4. [Frontend Specification](docs/frontend/04_FRONTEND_SPEC.md).
5. [Feature Tickets](docs/delivery/05_FEATURE_TICKETS.md).

The user approved each specification before the project saved it.
The nested paths are intentional.
The absence of docs/01_PRD.md does not mean that the specification is missing.

## Specifications and tests

- Obey the approved scope.
- Record a proposed material change before you write its code.
- Ask for a decision only when the change is outside the existing authorization.
- Give requirements, acceptance cases, and tests stable IDs.
- Connect tickets to these IDs.
- Write the failing behavior test before the application code for that behavior.
- Record the failing and passing results when development starts.
- Keep software tests in tests/.
- Keep AI evaluations in evals/.
- Make default local tests independent of credentials and external services.
- Let local browser and API tests use loopback traffic.
- Start cloud checks and live model evaluations only for an authorized task.
- Give each check its own evidence record.
- Do not claim F3/D2 achievement from specifications or controlled model tests alone.
- Do not claim production readiness or operational compliance without the required evidence.
- Write application code only when the active task requests it.
- The initial file-save task includes documentation.

## Safety boundaries

- Keep private storage, records, logs, and model processing in India.
- Use CloudFront only for public frontend assets.
- Use the selected India Bedrock profile.
- Make sure its destinations and permissions are correct before private uploads.
- Do not automatically substitute a global profile.
- Apply case ownership rules in application services and all storage and retrieval adapters.
- Treat uploaded documents as evidence, not as tool authorization.
- Keep different records for AI findings, human decisions, and actual operational verification.
- Keep input snapshots and original source locations unchanged.
- Retrieve current public regulations through the configured external API under D20.
- Do source verification again before each current assessment.
- Block a current assessment when freshness verification fails or selected versions changed.
- Use stored regulatory copies only as assessment evidence.
- Send no private case content to the regulatory API.
- Count every dispatched model call against the saved job allowance.
- Include failed, rejected, repeated, and uncertain calls in that count.
- Never put private documents or credentials in version control.
- Never put full prompts, model responses, authentication tokens, or credentials in operational logs.
- Use numeric token counts and safe stage metadata as specified in the measurement contract.
- Explain AWS configuration in sequence when integration is ready.
- Review the actual deployment changes before deployment.
- Do not request secrets in chat.

## Decision records

For each material decision, update the controlling specification.
Append a linked entry to [the decision log](docs/decisions/gov-decision-log.md).
Keep replaced entries and identify their replacements.
Do not change the approval history without a record.

Update [LOG.md](LOG.md) with completed work, verification results, remaining uncertainties, and the next task.

## Documentation language: always use ASD-STE100

Use ASD-STE100 Simplified Technical English for all project documentation.
Apply this rule to each new document and each document change.
The rule includes Markdown, specifications, plans, instructions, architecture descriptions, tables, diagrams, and review records.
This rule replaces the previous Rishi Voice rule for project documentation.
Do not wait for the user to request STE again.

Before you write or change documentation, read the installed `asd-ste100` skill.
Then read the [language guide](docs/guide-ste100-writing.md).
Use the official standard and dictionary for the selected issue.
Do not use sentence length as the only acceptance test.

1. Identify instructions, descriptions, and exact text that must not change.
2. Keep each instruction sentence at 20 words or fewer.
3. Keep each descriptive sentence at 25 words or fewer.
4. Give one instruction in each sentence, unless the actions occur at the same time.
5. Use direct commands for instructions.
6. Use the active voice when the actor is known.
7. Keep one topic and no more than six sentences in each paragraph.
8. Use American English spelling in ordinary prose.
9. Use each dictionary word only with its approved meaning and part of speech.
10. Explain each necessary technical term at its first use or link to its definition.
11. Record the subject and meaning of technical terms in the language guide.
12. Do a manual review of the rules, dictionary choices, and technical meaning.
13. Use the skill's text checker for sentence length and punctuation.
14. Correct language errors before you give the document to the user.

Do not classify ordinary jargon as a technical term to keep an unapproved word.
Do not use metaphors, rhetorical questions, contractions, or semicolons in new prose.
Keep exact identifiers, code, commands, paths, links, numbers, units, and source quotations unchanged.
Keep all conditions, permissions, prohibitions, uncertainty, and approval history unchanged.
Do not change a recommendation into a requirement during a language correction.

Give a short plain-language explanation when it helps the reader.
Do not invent personal examples or source facts.

Save the language review record in a different file from the document.
Record the issue, reviewed files, protected text, dictionary decisions, checks, and remaining limits.
If the complete dictionary is unavailable, identify the incomplete review.
Do not call an incomplete review complete.
Do not claim ASD approval or full compliance from a clean checker result.

## Folder and file rules

Keep these four files in the project root:

- README.md
- AGENTS.md
- LOG.md
- pyproject.toml

Keep these seven folders in the project root:

- docs/
- src/
- tests/
- evals/
- ops/
- data/
- runs/

Add machine-required hidden files only when implementation requires them.
Do not add infrastructure for an unapproved future need.
Use kebab-case for new document filenames.
Keep the five approved specification filenames.
Keep the folder structure shallow.
