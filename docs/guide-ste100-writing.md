# ASD-STE100 document language

Date: 2026-10-09.
Scope: All Markdown files in this project.

The user selected ASD-STE100 Simplified Technical English as the document language.
The global AGENTS.md also applies this rule to new projects.
Other existing projects need separate authorization for conversion.

## Reference and verification limit

Use [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf), dated 2025-01-15, as the current reference.
Consult the [official standard website](https://www.asd-ste100.org/) for later issues.

The official public description and indexed excerpts were available.
The complete official PDF request returned HTTP 403.
A complete dictionary and approved-meaning review was not possible.

The project uses STE writing rules.
The report does not certify full compliance with the standard.
Sentence-length checks do not establish dictionary or part-of-speech compliance.

## Writing procedure

1. Identify the instructions and descriptions.
2. Keep instructions separate from descriptions.
3. Use direct commands for instructions.
4. Give one instruction in each sentence.
5. Keep instruction sentences within 20 words.
6. Keep descriptive sentences within 25 words.
7. Use active voice where the actor is known.
8. Keep one topic in each paragraph.
9. Use the same term for the same item.
10. Explain a necessary technical term before further use.
11. Use dictionary-approved words or permitted technical nouns and technical verbs.
12. Do not use metaphors or rhetorical questions.
13. Do not use semicolons in new prose.
14. Preserve the source meaning.

Do not invent an actor to remove passive voice.
Do not change a recommendation into an obligation.
Keep all conditions, exceptions, prohibitions, and uncertainty.

## Text that must remain exact

Keep these items unchanged when exact text is necessary:

- Requirement, decision, test, and ticket IDs.
- Code, commands, configuration keys, and field names.
- Product names, model IDs, filenames, paths, and links.
- Numbers, units, dates, limits, and hashes.
- Source quotations and third-party text.
- Historic result values and approval records.

Identify exact source text as a quotation.
Do not use exceptions to avoid a language review of ordinary prose.

## Project terms

These definitions control project usage.
They do not assert that the official dictionary approves each term.

| Technical term | Project meaning |
|---|---|
| Adapter | Code that connects an application interface to a local resource or external service. |
| Agent | A component that selects permitted tool actions to complete a task. |
| API | Application programming interface. A defined connection through which software exchanges requests and responses. |
| Applicability | The conditions that determine whether a requirement applies to a bank or assessment. |
| Assessment | A comparison of selected requirements, controls, and supplied evidence. |
| Bounded agent | An agent with explicit limits on tools, data, calls, and time. |
| Case | A bank profile and the documents, assessments, and review records related to it. |
| Citation | A reference to the exact source passage that supports a statement. |
| Control | A bank policy or process that addresses a requirement. |
| Evidence | Supplied information used to support or challenge an assessment. |
| Evidence gap | Missing or insufficient information needed for an assessment. |
| Fixture | Fixed test data with a known purpose and expected result. |
| Frontend | The browser interface that the user operates. |
| Hash | A computed value used to identify file content and detect a content change. |
| Held-out case | An evaluation case not used to develop or tune the model instructions. |
| IAM | AWS Identity and Access Management. The AWS service for identities and access permissions. |
| Idempotency key | An identifier for repeated requests that must have one logical effect. |
| Inference | Processing by an AI model to produce an output. |
| Integration | The connection and operation of separate application components or services. |
| Job | A recorded unit of background work with progress and a final state. |
| Loopback | A network connection from a computer to that same computer. |
| Model profile | A service configuration that selects the permitted model and processing destinations. |
| Obligation | A specific regulatory requirement and its conditions. |
| Operational evidence | Records that show whether an actual activity occurred within the required scope and period. |
| PKCE | Proof Key for Code Exchange. A method that protects the sign-in code exchange. |
| Prompt | Instructions and context supplied to an AI model. |
| Remediation | A proposed correction for an identified gap. |
| Repository | The project's stored source files and related records. |
| Retrieval | Selection of relevant passages from permitted documents. |
| Schema | The specified structure and constraints of data. |
| Snapshot | A fixed copy of the selected assessment inputs and versions. |
| Token | A unit of model input or output, or an identity credential where the context explicitly states authentication. |

Product names such as S3, Cognito, DynamoDB, SQS, Lambda, FastAPI, and React retain their official spelling.
Use “model token” or “access token” when “token” alone is ambiguous.

## Verification procedure

1. Compare the revised text with the preserved source.
2. Make sure all technical requirements and conditions remain.
3. Make sure all exact identifiers and numeric limits remain.
4. Make sure local links and section anchors resolve.
5. Do the sentence-length and punctuation checks.
6. Review the technical terms and their use.
7. Record the checks and their limitations.

Read [the current verification record](../runs/2026-10-09-project-ste100-verification.md).
