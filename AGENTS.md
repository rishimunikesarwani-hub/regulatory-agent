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
- Record a proposed material change before implementation.
- Ask for a decision only when the existing authorization does not cover the change.
- Give requirements, acceptance cases, and tests stable IDs.
- Connect tickets to these IDs.
- Write the failing behavior test before the application code for that behavior.
- Record the failing and passing results when development starts.
- Keep software tests in tests/.
- Keep AI evaluations in evals/.
- Default local tests must not require credentials or external services.
- Permit loopback traffic for local browser and API tests.
- Run cloud checks and live model evaluations explicitly.
- Identify their evidence separately.
- Do not claim F3/D2 achievement from specifications or controlled model tests alone.
- Do not claim production readiness or operational compliance without the required evidence.
- Implement application code only when the active task requests it.
- The initial file-save task covers documentation.

## Safety boundaries

- Keep private storage, records, logs, and model processing in India.
- Use CloudFront only for public frontend assets.
- Use the selected India Bedrock profile.
- Verify its destinations and permissions before private uploads.
- Do not automatically substitute a global profile.
- Enforce case ownership in application services and all storage and retrieval adapters.
- Treat uploaded documents as evidence, not as tool authorization.
- Keep AI findings, human decisions, and actual operational verification separate.
- Keep input snapshots and original source locations unchanged.
- Retrieve current public regulations through the configured external API under D20.
- Revalidate selected sources before each current assessment.
- Block a current assessment when freshness verification fails or selected versions changed.
- Use stored regulatory copies only as assessment evidence.
- Send no private case content to the regulatory API.
- Count every dispatched model call against the saved job allowance.
- Include failed, rejected, repeated, and uncertain calls in that count.
- Never put private documents or credentials in version control.
- Never put full prompts, model responses, tokens, or credentials in operational logs.
- Explain AWS configuration in sequence when integration is ready.
- Review the actual deployment changes before deployment.
- Do not request secrets in chat.

## Decision records

For each material decision, update the controlling specification.
Append a linked entry to [the decision log](docs/decisions/gov-decision-log.md).
Keep replaced entries and identify their replacements.
Do not change the approval history without a record.

Update [LOG.md](LOG.md) with completed work, verification results, remaining uncertainties, and the next task.

## Markdown language

Use ASD-STE100 Simplified Technical English for all project Markdown.
This rule replaces the previous Rishi Voice treatment.
Read the [language guide](docs/guide-ste100-writing.md).
Keep all technical requirements, identifiers, limits, and source claims unchanged.
Explain necessary technical terms.
Give a short ELI10 explanation when it helps the reader.

Do not invent personal examples or source facts.
Do not claim full compliance from sentence-length checks alone.

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
