# Technical blueprint: ASD-STE100 rewrite verification

Date: 2026-10-09.

This historical record describes the blueprint-only edit under D17.
Its counts and hashes describe that earlier check.
See the [project verification](2026-10-09-project-ste100-verification.md) for the later D18 edit.

## Scope and authorization

The user requested ASD-STE100 language and identified the technical architecture as the document.

- Revised document: [Technical Blueprint](../docs/architecture/02_TECHNICAL_BLUEPRINT.md).
- Language decision: [D17](../docs/decisions/gov-decision-log.md#d17--technical-blueprint-language).
- Original wording: [Preserved source copy](2026-10-09-technical-blueprint-before-ste100.txt).
- Project record: [LOG.md](../LOG.md).

This is a language edit. The approved architecture remains the source of the technical requirements.

## Language checks

The reference is [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf), dated 2025-01-15.

The accessible official rule excerpts support these checks:

- Use dictionary words and permitted technical terms (1.1–1.2).
- Use active voice, with the specified exception for an unknown actor in descriptive text (3.6).
- Keep procedural sentences within 20 words (5.1).
- Give one instruction per sentence (5.2).
- Use direct commands for instructions (5.3).
- Keep descriptive sentences within 25 words (6.3).
- Do not use semicolons (8.1).

The rewrite uses short sentences, direct commands, explicit actors, and consistent project terms. It removes the engine metaphor. It retains product names, configuration keys, record names, and field identifiers.

A local sentence and table-cell scan found no text unit above 20 words. The maximum was 17 words. The scan removes Markdown link destinations and formatting. It separates sentences, table cells, and colon-delimited items. This is a conservative structural check, not a complete STE parser. The document contains no semicolons.

Manual review compared all eight sections with the preserved source:

| Section | Technical content preserved |
|---|---|
| 1 | One application with local and AWS adapters. Same technology choices and unverified dependency state. |
| 2 | Ten flow steps, immutable input snapshot, separate background job, progress polling, and the original 30-second quota claim. |
| 3 | One bounded agent, permitted actions, pre-ranking filters, source inspection rule, prohibited actions, and persistent job allowances. |
| 4 | Exact configuration table, IAM roles, private-upload checks, India processing boundary, retention caveat, and reviewed model changes. |
| 5 | All eight record names and their identity/content cells, ownership, immutable versions, citations, original locations, and separate human decisions. |
| 6 | All nine API functions, authentication, request idempotency, exports, and T2 contract requirements. |
| 7 | All five job states, atomic call reservation, crash accounting, duplicate-delivery controls, retries, and persistent deadline. |
| 8 | Seven root folders, separated domain logic, test/evaluation references, and T8 integration/configuration work. |

## Preservation checks

- Eight numbered sections remain.
- All ten original link destinations remain.
- The configuration table header and all seven data rows match the source exactly.
- The identity/content cells for all eight records match the source exactly.
- No original numeric token, underscore-style field identifier, or configuration key is missing.
- The original copy matches the source SHA-256.
- Local Markdown file links and the new D17 anchor resolve.
- The project retains four root files and seven root folders.
- Existing files outside the blueprint, handbook writing note, decision log, and project log remain unchanged.

Source SHA-256:

`8ad15c85b35b833e62e6991e38c52237e7020b446e419e11256ed5edca0739d6`

Revised blueprint SHA-256:

`35bd4c21facb8c1be3dd2cc66a4ec6cb8bce87f3b2e47ff052e60161a476dabc`

## Verification limits

The full official PDF download was unavailable through the available fetch tools. Official indexed excerpts were available. A complete dictionary, part-of-speech, approved-meaning, and technical-term audit was not performed. Do not treat this record as proof of full ASD-STE100 compliance.

The original AWS links and claims remain in place. This language edit did not revalidate the AWS account, service behavior, profile destinations, model entitlement, or current cloud documentation.

No application code changed. No software tests, live model evaluations, cloud checks, or deployments ran. The project remains documentation only. T1 source and fixture acquisition remains the next application task.
