# Local OpenAI evaluation execution

Date: 2026-10-11. Authorization: D57 and the active complete-application goal.

This evaluation uses the frozen fictional assessment cases with the local OpenAI provider.
It gives a separate result group from the required India Bedrock evaluation.
It cannot establish current source coverage, live amendments, AWS acceptance, or regulatory certification.

## Requirements

- OE01: Verify every frozen file hash before preparation or model dispatch.
- OE02: Read model inputs from the input files only. Keep expected answers outside every model request.
- OE03: Save explicit clause selections before execution. Do not derive selections from expected answers.
- OE04: Keep each case, selected version, passage text, and source location unchanged in its saved snapshot sources.
- OE05: Use the existing owner checks, immutable sources, pipeline, citation validation, and execution limits.
- OE06: Use a new evaluation database under ignored `runs/private/`. Do not use the feedback or browser-test database.
- OE07: Keep all 20 primary cases in the result denominator, including failures and cases without findings.
- OE08: Keep actual provider identity, prompt version, model calls, token counts, and elapsed time in safe results.
- OE09: Calculate status agreement after model execution. Leave claim support unknown until a person reviews the cited context.
- OE10: Preserve previous results. Require an explicit run option before any live model call.
- OE11: Keep diagnostic failures in the private evaluation directory. Save only fixed error codes and stage identifiers.
- OE12: Identify selected-case diagnostic runs as development results. Keep missing cases in the denominator and release gates pending.

The benchmark source format contains frozen passages rather than uploaded PDF or DOCX files.
Untrusted fixture passages use the application evidence role, with the original fixture kind saved.
The evidence role does not authorize instructions in source text.

This evaluation does not verify document extraction or API admission.
Untrusted proposed-reference fields remain separate citation-boundary test vectors, outside the model evidence passages.

The fixture author has no qualified regulatory domain review.
The existing cases have appeared in fixture-validation tests.
Do not describe them as independently reviewed or guaranteed unseen.

An evaluation database is a separate database that holds benchmark jobs and sources.
Clause selection identifies the primary regulatory passage and its saved applicability passages.

## Verification

Offline checks must verify hash rejection, answer separation, source preservation, database isolation, and failure accounting.
The live record must distinguish agreement from citation support and the full release gates.
The OpenAI result must not replace the required Bedrock result.

The diagnostic child uses the same supervised worker and application processing path.
It records approved error codes after the application saves its mandatory audit record.
An optional diagnostic write failure must not change assessment processing.
Mandatory audit failures must still stop processing.
Unknown exception messages remain excluded.
The diagnostic record contains no prompts, responses, source text, credentials, or hidden reasoning.

The initial result exposed benchmark failures to the developer.
Subsequent runs use the development designation, including runs with all 20 cases.
Such results cannot establish the independent held-out release gate.
