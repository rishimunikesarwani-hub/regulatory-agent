# ASD-STE100 documentation language

Date: 2026-10-10.
Scope: All project documentation, including new documents and changes.

The user selected ASD-STE100 Simplified Technical English for project documentation.
The [local instructions](../AGENTS.md#documentation-language-always-use-asd-ste100) make this a permanent project rule.
This rule replaces the earlier Rishi Voice rule.
Use this guide with the installed `asd-ste100` skill.

## Reference

Use [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf), dated 2025-01-15, for this review.
The complete official PDF became available to this project on 2026-10-10.
It includes the writing rules and dictionary.
For standard information, see the [official website](https://www.asd-ste100.org/).
An earlier request returned HTTP 403. That earlier limit no longer applies to this review.

The reference copy is in the ignored `runs/private/` folder.
Do not add the standard or its extracted text to the project repository.
The standard has its own copyright conditions.

The text checker finds selected mechanical errors.
It does not establish dictionary compliance or ASD approval.
A manual review must also examine meanings, parts of speech, technical terms, and all applicable writing rules.

## Writing procedure

1. Read the complete source before you change it.
2. Identify instructions, descriptions, tables, and exact text.
3. Put instructions and descriptions in different paragraphs.
4. Use direct commands for instructions.
5. Give one instruction in each sentence, unless the actions occur at the same time.
6. Keep instruction sentences at 20 words or fewer.
7. Keep descriptive sentences at 25 words or fewer.
8. Use the active voice when the actor is known.
9. Keep one topic and no more than six sentences in each paragraph.
10. Use the same term for the same item.
11. Explain each necessary technical term at its first use or link to this guide.
12. Use dictionary words only with their approved meanings and parts of speech.
13. Use technical nouns and technical verbs only as permitted by the standard.
14. Use American English spelling in ordinary prose.
15. Keep articles when the grammar needs them.
16. Do not use metaphors, rhetorical questions, contractions, or semicolons in new prose.
17. Keep the source meaning unchanged.

Do not invent an actor to remove the passive voice.
Do not change a recommendation into an obligation.
Keep all conditions, exceptions, prohibitions, and uncertainty.
Do not use a technical-term exception for an ordinary word with an unapproved meaning.

## Exact text

Keep these items unchanged when exact text is necessary:

- Requirement, decision, test, and ticket IDs.
- Code, commands, configuration keys, and field names.
- Product names, model IDs, filenames, paths, and links.
- Numbers, units, dates, limits, and hashes.
- Source quotations and third-party text.
- Historical results and approval records.

Identify exact source text as a quotation.
Do a language review of all ordinary prose around exact text.
Do not change a historical result to match a later result.

## Dictionary decisions

The page numbers below are PDF page numbers, starting at one.
They refer to the official Issue 9 PDF with 434 pages.
These decisions apply to ordinary prose. Fixed identifiers and valid technical terms need their own review.

| Source wording | Project wording | Reason and PDF page |
|---|---|---|
| main product measure | primary product measure | MAIN is not approved as an adjective. PRIMARY is an alternative. Page 145. |
| check, as a verb | do a check or make sure | CHECK is approved as a noun. Pages 188-189. |
| test, as a verb | do a test or do the tests | TEST is approved as a noun. Pages 400-401. |
| verify | make sure | VERIFY is not an approved verb. Page 422. |
| retain | keep | RETAIN is not an approved verb. Page 362. |
| preserve, meaning keep unchanged | keep unchanged | The dictionary entry concerns PRESERVATION of materials. Page 338. |
| ensure | make sure | ENSURE is not approved. Page 233. |
| require, as a verb | must, necessary, or a direct command | Select wording that keeps the original obligation. Page 360. |
| distinct item count | count each item once | Keep the calculation clear. DISTINCT is not approved. Page 221. |
| freeze the evaluation data | keep the evaluation data unchanged | FREEZE has a temperature meaning. Page 257. |
| report, as a verb | record, show, or give a report | REPORT is approved as a noun. Page 359. |
| create | make | CREATE is not approved. Page 205. |
| run, as an ordinary verb | do, start, or operate | Select the verb that keeps the action correct. Page 365. |
| remain | stay | REMAIN is not approved. REMAINING is an approved adjective. Page 357. |
| separate or separately | different, independently, or different records | Select the wording from the sentence context. Page 373. |

Do not replace words without a review of the sentence meaning.
For example, a fixed UI label or metric name can need its original spelling.

## Project technical terms

STE permits technical nouns for a specified subject.
The terms below name software, AI, statistics, or bank assurance concepts used by the approved specifications.
They are not a list of ordinary words that the project can use without dictionary review.
Use them only with these meanings.

| Technical term | Subject | Project meaning |
|---|---|---|
| Branch | Git | A named sequence of recorded file versions. |
| Commit | Git | A recorded version of selected files. |
| Fast-forward merge | Git | A branch update to a later commit without combining different development histories. |
| Integration owner | Project delivery | The person or session responsible for shared changes and their inclusion in main. |
| Persistence | Software | Storage that keeps application records after a process restart. |
| Port | Networking | A numbered network connection point. |
| Pull request | GitHub | A request to review and combine branch changes. |
| Virtual environment | Python | A local Python installation with the project's dependency versions. |
| Worktree | Git | A project folder with its own Git branch. |
| Abstention | Evaluation | A model decision not to give an assessment. |
| Adapter | Software | Code that connects an application interface to another service or resource. |
| AI agent | AI | A software component that selects permitted tool actions to complete a task. |
| API | Software | Application programming interface. A connection through which software exchanges requests and responses. |
| Applicability | Bank assurance | The conditions that determine whether a requirement applies to the assessment. |
| Assessment | Bank assurance | A comparison of selected requirements, controls, and evidence. |
| Attempt | Software | One recorded start of a tool operation or model call. A retry is another attempt. |
| Audit record | Bank assurance | A saved record that lets an authorized person examine an action and its result. |
| Benchmark | Evaluation | A specified set of cases and measures for a comparison. |
| Bounded agent | AI | An AI agent with specified limits on tools, data, calls, and time. |
| Cache | Software | Saved data that a later operation can use again. |
| Case | Bank assurance | A bank profile and its related documents, assessments, and review records. |
| Chunk | Retrieval | A part of a document used for search or model context. |
| Citation | Bank assurance | A reference to the source passage that supports a statement. |
| Cohort | Statistics | A group selected for a report by specified filters and dates. |
| Confusion matrix | Evaluation | A table of reference labels and model labels that shows correct and incorrect classifications. |
| Context | AI | Information supplied to a model for the current task. |
| Context relevance | Evaluation | The share of selected passages that have a relevant label under the saved annotation rules. |
| Claim support | Bank assurance | The relationship between a claim and the cited evidence that supports it. |
| Control | Bank assurance | A bank policy or process that addresses a requirement. |
| Evidence | Bank assurance | Information used to support or challenge an assessment. |
| Evidence gap | Bank assurance | Missing or insufficient information necessary for an assessment. |
| Final outcome | Product measurement | The saved approved, edited, or rejected reviewer decision for an item. |
| Fixture | Software tests | Fixed test data with a specified purpose and result. |
| Frontend | Software | The browser interface that the user operates. |
| Hash | Software | A calculated value used to identify file content and find a content change. |
| Extraction | Software | Conversion of original file content to text with source locations. |
| Extraction unit | Software | A page equivalent under the approved document limits. PDF units also count actual pages. |
| Transaction | Database | An operation that applies related database changes together or keeps all changes out. |
| Upload | Software | Transfer of file bytes from the browser to authorized application storage. |
| Held-out case | Evaluation | An evaluation case not used to develop or adjust the model instructions. |
| IAM | AWS | AWS Identity and Access Management. The service for identities and access permissions. |
| Idempotency key | Software | An identifier for repeated requests that must have one logical effect. |
| Idempotency | Software | The property that repeated requests with the same key and payload have one logical effect. |
| Inference | AI | Processing by an AI model to produce an output. |
| Integration | Software | The connection and operation of different application components or services. |
| Integration candidate | Git | A branch for checks of combined application changes before acceptance. |
| Simulated amendment | Software tests | A constructed regulatory change for a fixed test. It is not an actual authority event. |
| Version comparison | Bank assurance | An examination of two specified source versions and their effects on selected obligations and controls. |
| Model interpretation | AI and bank assurance | A model proposal about a requirement and its meaning. Citation resolution does not prove correct semantic support. |
| Whitespace normalization | Software | A comparison operation that replaces whitespace sequences with one space and removes outer whitespace. |
| Job | Software | A recorded unit of background work with progress and a final state. |
| Live evaluation | Evaluation | An evaluation that calls the actual model or service instead of a controlled test response. |
| Loopback | Networks | A network connection from a computer to that same computer. |
| Model judge | Evaluation | A model used to assess another model's output. Its judgment can be incorrect. |
| Model profile | AWS | A service configuration that selects the permitted model and processing destinations. |
| Monotonic clock | Software | A clock for elapsed time that does not move backward after a system clock adjustment. |
| Obligation | Bank assurance | A specified regulatory requirement and its conditions. |
| Operational evidence | Bank assurance | Records that show whether an actual activity occurred in the necessary scope and period. |
| Original AI item | Product measurement | The unchanged finding and primary recommendation that the AI produced. |
| Percentile | Statistics | A position in a sorted set of measurements. The measurement contract specifies the calculation. |
| PKCE | Security | Proof Key for Code Exchange. A method that protects the sign-in code exchange. |
| Prompt | AI | Instructions and context supplied to an AI model. |
| ReAct | AI | A pattern that repeats assessment, tool selection, tool execution, and observation until a stop condition applies. |
| Recall | Evaluation | The share of required source spans covered by the selected passages. |
| Regulatory evidence | Bank assurance | Source text and metadata that support the regulatory part of an assessment. |
| Remediation | Bank assurance | A proposed correction for an identified gap. |
| Repository | Software | The project's stored source files and related records. |
| Retrieval | AI | Selection of passages from permitted documents for the task. |
| Review item | Product measurement | One original finding and its primary recommendation for one selected obligation in one assessment run. |
| Run | Software | One recorded execution of an assessment or evaluation. Use this term as a noun. |
| Supervisor | Software | A separate process that controls the assessment worker. |
| Execution lease | Software | A time-limited permission that lets the current worker process a saved job. |
| Monotonic clock | Software | A clock that measures elapsed time without changes to the system date or time. |
| Schema | Software | The specified structure and constraints of data. |
| Snapshot | Software | A fixed copy of selected assessment inputs and versions. |
| Artifact reference | Software | The ID of an exact saved document used by an assessment snapshot. |
| Source span | Retrieval | A labeled part of an original page, paragraph, or row. Its identity does not depend on chunk boundaries. |
| Stage trace | Software | Records that connect the attempts and results in one stage. |
| Telemetry | Software | Recorded runtime measurements and event data. |
| Token | AI or security | A unit of model text, or an identity credential when the text specifies authentication. |
| Trace | Software | Connected records of the stages and attempts in one run. |
| Unexpected abstention | Evaluation | A model decision not to give an assessment when the labeled case needs one. |

Product names such as S3, Cognito, DynamoDB, SQS, Lambda, FastAPI, and React keep their official spelling.
Use "model token" or "access token" when "token" alone is not clear.
The user's term "north star" means the primary product measure: approval without edits.
Use the metric names and formulas from the [measurement contract](testing/spec-measurement-contract.md).

## Review procedure

### VS5 period terms

| Term | Permitted project meaning |
|---|---|
| Stated period | A date interval declared by an original evidence record. |
| Period grounding | Exact source citations that establish a stated interval. |

A stated period does not establish complete records or actual control operation.

### VS2 cloud terms

| Term | Permitted project meaning |
|---|---|
| Signed POST policy | Temporary S3 permission with specified upload conditions. |
| Idempotency key | An identifier that gives repeated requests one logical effect. |
| Conditional transaction | An atomic record change that requires specified stored conditions. |
| S3 version identifier | The identifier of one stored object version. |
| Virtual addressing | An S3 address with the bucket name in the hostname. |
| Source page | A bounded set of extracted passages for source inspection. |

These are technical terms for the accepted VS2 cloud implementation.

### VS5 cloud record terms

| Term | Permitted project meaning |
|---|---|
| Record revision | An integer that increases after an accepted change to stored metadata. |
| Strongly consistent read | A DynamoDB read that includes all successful writes before that read. |

A sequence of strongly consistent reads does not give one atomic view of all records.

### Apply the review procedure

1. Compare the changed text with the saved source.
2. Make sure all technical requirements and conditions stay unchanged.
3. Make sure all exact identifiers and numeric limits stay unchanged.
4. Make sure local links and section anchors have the correct targets.
5. Do the sentence-length and punctuation checks.
6. Do a dictionary review of uncertain words, meanings, and parts of speech.
7. Do a review of technical terms in their subject context.
8. Make sure the text follows all applicable writing rules.
9. Record the checks, corrected errors, exact-text exceptions, and review limits.

Keep the review record in a different file from the user document.
Do not claim full compliance from a clean script result.
Earlier verification records describe their own dates and review limits.
