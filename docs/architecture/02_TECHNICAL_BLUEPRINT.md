# Technical Blueprint: local operation and AWS operation

> Approval: The user gave approval to the design in the planning conversation. The project first saved this document on 2026-10-08.
> Language revision: 2026-10-10.
> Required document: [PRD](../product/01_PRD.md).
> Decision references: [D07–D10, D16, D17, D20, and D24](../decisions/gov-decision-log.md).

> Evidence status: The design has approval. This project has no deployed services or completed model-invocation check.
> Writing reference: [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf).

## 1. Architecture

### Architecture views

Open the [AWS system view](arch-system.html) to examine components and service boundaries.
Open the [assessment view](arch-assessment.html) to examine source checks, evidence processing, and human review.
Both views use ArchView and show the approved design.

Local contracts, adapters, and the first case interface are implemented.
The complete assessment and review interface are pending.
Each delivery slice includes frontend, backend, AWS configuration, and tests under D27.
Read the [first-slice contract](../delivery/spec-slice-01-cases.md) for the current implementation boundary.

Use Zoom to examine a view.
Use Image to export a PNG.
Use Report to open the browser print dialog.
Select Save as PDF to save the report.
Use the navigation links to change views.

The editable sources are [system JSON](arch-system.json) and [assessment JSON](arch-assessment.json).
The external regulatory API is part of the design.
The project did not select a provider.
A crawler view is outside the user's selected scope.

**ELI10:** The system view shows the parts and their connections.
The assessment view shows the checks before the operator examines a finding.

![AWS system architecture](arch-system.png)

![Assessment controls](arch-assessment.png)

### Components

Use the same application logic for local operation and AWS operation. Keep domain rules outside the code for connections to external services.

An interface gives the rules for communication between application logic and a service. An adapter connects that interface to a local resource or an AWS service. The interfaces are for storage, records, jobs, identity, model calls, and public regulatory retrieval.

The local adapters let developers examine the assessment logic and do tests before AWS account configuration. At deployment, AWS adapters use the same interfaces. The adapters do not make two different products.

| Component | Approved technology | Function |
|---|---|---|
| Frontend | React and TypeScript with Vite | Gives the user a browser workspace for evidence inspection and review. |
| Backend | Python and FastAPI | Uses request and response types to validate data at the assessment interface. |
| Cloud API | API Gateway and Lambda | Processes short requests from authenticated users. The worker does assessments independently. |
| Private document storage | S3 in Mumbai | Stores bank files, assessment evidence copies, extracted passages, and reports. It is not the authority for the current regulatory version. |
| Regulatory source retrieval | External retrieval API. Provider TBD. | Retrieves current public regulations and amendments with source metadata. |
| Cloud records | DynamoDB in Mumbai | Stores case metadata, job states, counters, and references. |
| Background work | SQS and Lambda worker | Does assessments independently from API requests. Saves progress. |
| Identity | Cognito | Authenticates operators. Demo sign-up is not permitted. |
| AI | Bedrock profile in.openai.gpt-5.6-luna | Uses the selected India profile. Destination, access, and quality checks are necessary. |
| Public frontend hosting | S3 and CloudFront | Serves public static assets only. Does not cache private reports or documents. |
| Infrastructure | AWS SAM configuration in ops/ | Describes the deployment for review. |
| Local adapters | Filesystem, SQLite, local worker, controlled AI and retrieval responses | Lets developers do default development and tests without AWS credentials. |

The local foundation uses Python 3.12.13 and the versions in `ops/requirements.lock`.
The recorded clean-copy check passed with these versions.
The root manifest identifies the setup and test commands.
D24 contract additions and application handlers are pending.

### Integrated T2 limits

[D26](../decisions/gov-decision-log.md#d26---foundation-integration-and-remaining-worktrees) records the implemented T2 defaults.
The [contract handoff](../delivery/spec-session-b-contracts.md) gives their original evidence and limits.
These defaults do not establish live provider behavior or file-upload enforcement.

| Quantity | Local contract default |
|---|---|
| File size | At most 10,000,000 bytes. |
| Selected documents | At most 10. |
| Extracted page equivalent | 4,000 UTF-8 bytes of extracted text, rounded upwards. |
| PDF units | The larger of actual pages and extracted page equivalents. |
| DOCX, TXT, CSV units | Extracted page equivalents, with original paragraph, line, or row locations. |
| Case extraction allowance | At most 100 units and 400,000 extracted UTF-8 bytes. |
| Regulatory requests | At most 20 dispatches per job, including retries. |
| Regulatory pagination | At most 10 pages. |
| Provider retries | At most two retries after the first attempt. |
| Provider timeout | 10 seconds for each attempt. Only simulated behavior has tests. |
| Response size | At most 1,000,000 bytes per page and 10,000,000 bytes per retrieval operation. |
| Regulatory extracted text | At most 400,000 UTF-8 bytes across the sources in one retrieval operation. |

The live adapter must enforce network timeouts, response limits, destination checks, and redirect rules.
T3 must enforce the remaining case allowance across retrieval operations.
The controlled adapter saves the request count per job, but not a shared response-byte total across different retrieval operations.
The source URL validator permits HTTPS RBI authority URLs only.
Any additional authority needs an integration contract revision.

## 2. Request and assessment flow

The steps that follow give the mandatory application behavior.

1. The authenticated user makes a case. The user saves a bank profile.
2. The API authorizes the upload. It completes the upload process only after validation and extraction.
3. The application refreshes public regulations through the external retrieval API. The user selects returned versions and obligations.
4. The application starts the assessment with an input snapshot that cannot change. It sends a job ID to the client.
5. The job runner calls the same worker service locally or through SQS.
6. The worker makes sure that the selected regulatory versions are current. If selected versions changed, it requests selection review before assessment.
   After this check, it retrieves obligations and controls. Then it starts the bounded agent.
7. The agent selects permitted actions. Application code validates each action before execution.
8. The worker validates results and citations before it saves immutable findings, recommendations, and audit references.
9. The UI polls saved job progress. It shows findings, source passages, and reviewer actions. Each saved final review adds an event.
10. A subsequent version comparison makes new results with links to the old snapshot. It does not change previous results.

Do not keep the browser request open until the assessment finishes.

API Gateway HTTP integrations have a documented integration limit of 30 seconds. The application uses jobs and does not depend on this time window. Refer to [AWS HTTP API quotas](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-quotas.html).

### Current regulatory sources

The external retrieval API supplies current regulatory content.
S3 stores evidence of past assessments.
Do not use an S3 copy as proof that a regulation is current.

Refresh the source catalog for the selected scope before obligation selection.
Revalidate selected regulations at worker start before assessment.
Use the existing job service for these network operations.
Keep the ten-minute processing deadline.

The provider must send authoritative source text and source URLs in its response.
It must identify applicable amendments, replacements, and withdrawals.
A search snippet or provider retrieval timestamp alone is not proof of current coverage.
Record the authority verification time and provider coverage limitations.

Use publication dates and effective dates independently.
Find which requirements are applicable on the selected assessment date.
An amendment with a future effective date does not automatically replace the requirement applicable on that date.

Save the exact response text and citation locations as assessment evidence.
Keep its authority, source URL, version, content hash, and amendment references.
Record retrieval time, authority verification time, and freshness status.
A freshness status shows whether current-source verification passed for this run.
It is not a guarantee that no subsequent update exists.

When available, use provider version identifiers or HTTP validators.
An ETag identifies a particular HTTP representation.
Validate it against the authority or a provider with verified authority synchronization.
Refer to [HTTP response validation](https://www.rfc-editor.org/rfc/rfc9111.html#section-4.3).

When source content or applicable regulatory metadata changes, make a new version.
Include withdrawals and effective-date changes in that comparison.
Keep the previous assessment and its source copy.
If selected versions changed, make selection review mandatory.
Do not change the selected obligation scope automatically.

If verification does not pass, block a new current assessment.
Show the last check that passed and the failure.
Keep access to historical reports with their initial assessment date and freshness status.
Do not use old content without a warning or mark it current.

T1 must select the provider. T1 must complete the provider checks.
Its API endpoint, authority coverage, update delay, historical versions, terms, and pricing are TBD.
The project has no verification evidence for a direct RBI API or a zero-delay update guarantee.

T2 must set the retrieval request and response schemas.
Set request limits, timeouts, pagination limits, and response-size limits before implementation.
Count retries against the saved retrieval allowance.
Use different counters for retrieval calls and the 24 model calls.
All requests must fit within the existing job deadline and document limits.
If pagination is not completed or no retrieval allowance is available, current coverage is unverified.

The first release refreshes on request and before each current assessment.

Controlled local tests and held-out model evaluations use fixed source versions.
Label these runs as simulations or historical benchmarks.
They are not proof of current regulatory coverage.

An independent scheduled monitor is future work.

The regulator is the authority.
The provider transports and retrieves its content.
Refer to [RBI Master Directions](https://www.rbi.org.in/Scripts/BS_ViewMasterDirections.aspx?did=338).

## 3. Agent and retrieval rules

Use one bounded agent. A bounded agent can use only the tools, data, and allowances permitted by the application.

Use application code to control tool execution. Do not make a multi-agent framework mandatory for this release. Do not make native tool execution on the model provider's server mandatory.

The model sends a structured action request. Before tool execution, application code validates these items:

- Action name.
- Case and snapshot scope.
- Arguments.
- Remaining allowance.
- Response schema.

The agent can request only these actions:

- Retrieve obligations from the selected regulatory version.
- Find possible controls in the selected case documents.
- Examine specified evidence passages.
- If the evidence is not sufficient, request one more retrieval pass within the permitted limits.
- Propose structured findings, remediation requests, and evidence requests.

Use keyword/BM25 retrieval to search selected bank documents and validated regulatory response passages. Before relevance ranking, filter passages by owner, case, document kind, and selected version.

If retrieval did not give a passage, do not count that passage as examined evidence. This rule also applies to passages related to the obligation.

Measure retrieval errors independently from assessment errors.

Use the [measurement contract](../testing/spec-measurement-contract.md) for different retrieval and assessment evaluations for REQ-X09 and AC-X09.
Measure provider source coverage, regulatory passage retrieval, and bank-evidence retrieval independently.
Use human-labeled source spans for retrieval tests.
Runtime source checks and validated citations are not proof of full retrieval.
Do not give live recall values without a full set of reference labels.

Keep orchestration, permissions, counters, stage order, and persistence in application code.
Use the agent for evidence interpretation and subsequent permitted retrieval.
Do not add an autonomous second reviewer or automatic model routing to the baseline.

Do not treat a tool request in an uploaded document as authorization. The agent cannot do these actions:

- Execute shell commands.
- Send messages.
- Get access to cases outside the authorized scope.
- Open URLs outside the permitted set.
- Change bank systems.

Count every dispatched model request against the **24-call** allowance for the job. This includes schema failures, retries, and requests with an uncertain outcome.

Save a **ten-minute** job deadline that starts when the worker starts. Do not reset the deadline after a delivery retry. Record queue waiting time independently.

If no allowance is available, keep the partial results that have source references. Keep the record of unchecked obligations.

## 4. Model and region configuration

| Configuration | Intended value | Secret? |
|---|---|---|
| APP_ENV | local or aws | No |
| AWS_REGION | ap-south-1, Mumbai | No |
| BEDROCK_MODEL_ID | in.openai.gpt-5.6-luna | No |
| ALLOWED_INFERENCE_REGIONS | ap-south-1 and ap-south-2 | No |
| MAX_MODEL_CALLS_PER_JOB | 24 | No |
| JOB_BUDGET_SECONDS | 600 | No |
| Document bucket, record table, queue, user pool | Outputs of the actual SAM deployment | Identifiers, not credentials |

Use IAM execution roles in AWS. Do not put credentials in configuration, browser code, or the repository.

AWS documentation gives information about Bedrock runtime support, structured outputs, and the India inference profile for the selected model. The project selected this model as an implementation dependency. This selection is not proof of model quality.

Before the application accepts private uploads, complete these checks:

1. Do a check of the installed SDK and API structure.
2. Do a check of response processing.
3. Do a check of the inference profile destinations.
4. Do a check of a live model invocation.

A regional endpoint alone is not proof that processing stays in India.

Sources:

- [AWS model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-56-luna.html)
- [Inference profile destinations](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
- [Bedrock data retention](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html)

Do not claim that all model processing has zero retention. During integration, examine the applicable model terms and service settings.

If the selected model cannot meet the approved boundaries or quality gate, record the problem. Propose a model change for review. Do not substitute another endpoint without an approved change.

Start measurements with the approved pinned model.
Record its configuration version and every model attempt.
Test subsequent routing or a second reviewer only against a named observed failure.
Before private use, do checks of candidate regions, permissions, and tool compatibility.
Keep the aggregate call allowance and deadline unchanged during those experiments.
An experiment does not authorize adoption or replace the approved baseline.

## 5. Records and evidence

The records that follow give the approved data requirements. The field names are implementation guidance. They do not mean that a database exists.

| Record | Identity and contents | Required condition |
|---|---|---|
| Case | case_id, owner_id, bank profile, created_at | Validate the owner before access to each child record. |
| DocumentVersion | document_version_id, case_id, source identity, kind, version label, SHA-256, storage reference, source URL, publication/effective dates | Do not change the content or extraction for this version. |
| Passage | passage_id, document_version_id, location, extracted text | Each passage identifies one source version and a source location that the user can examine. |
| AssessmentSnapshot | snapshot_id, case_id, bank-profile copy, selected versions and obligations, prompt/model versions | Save the contents before execution. Do not change these contents. Do not automatically include subsequent uploads. |
| Job | job_id, run_id, snapshot_id, state, stage, call count, deadline, execution claim, job_admitted_at, timestamps. Retrieval count, authority verification time, freshness status, audit references. | Only one active execution and one finalization are permitted. Keep counters through retries. |
| Obligation/Control | stable ID, structured requirement or control, applicability, source passage references | Keep unknown fields unknown. |
| Finding | finding_id, run_id, snapshot_id, obligation/control references, status, evidence condition, citations, primary recommendation, available_at | At most one immutable review item per selected obligation and run is permitted. Keep the original content. Use only validated evidence. |
| ClaimEvidence | claim_id, finding_id, obligation element, claim reference, passage references, evidence period, reason reference, considered exceptions and conflicts | Keep claim-to-source links. An accurate quotation alone is not proof of contextual support. |
| ReviewDecision | event_id, finding_id, reviewer_id, event_kind, disposition, content references, committed_at, revision, idempotency key | Add each saved event. Keep notes, edited content, and reasons in authorized storage. Do not overwrite previous events or original content. |
| StageAttempt | run_id, job_id, snapshot_id, stage_id, attempt_id, state, timestamps, version references, measurements, artifact references | Keep attempt identity and outcome. Record missing usage fields as unknown. |

Keep large extracted content and reports in private blob storage. Use the record store for metadata and references. Do not use it for report bodies of unlimited size.

Keep these source locations unchanged:

- PDF: the source page number and a stable passage ID.
- DOCX: the paragraph or table-cell location from extraction.
- TXT: the line range.
- CSV: the row and the applicable column identifiers.

Include these items in every citation:

- Selected document version.
- Passage ID.
- Source location.
- Quoted excerpt.

Make sure that the stored extraction contains the quotation. Make sure that the quotation, in its context, is evidence for the related claim.

Make a new version for a replacement document. Existing snapshots continue to use the old version. For each new run, the user must select the versions. Do not let retrieval automatically mix current and superseded files.

### Reviewer outcomes

REQ-X07 and AC-X07 make the reviewer outcomes in the [measurement contract](../testing/spec-measurement-contract.md#1-product-metric-and-review-unit) mandatory.
Each finding and its primary recommendation form one review item.
Supporting observations do not add more counted items.
Do not make findings for unchecked obligations only to fill a report.

Use approved, edited, or rejected for saved final outcomes.
Use final_review and evidence_request event kinds. Only final_review carries a final disposition.
Approved always means acceptance of the original AI item.
Acceptance of an existing edited revision stays edited.
After an edit, the reviewer must select the original item to save approved.

An edited outcome must contain changed content and a nonblank reason.
Before you compare edited content with the original item, normalize outer whitespace and line endings.
A rejected outcome must contain a nonblank reason.

A comment, unsaved draft, or request for more evidence does not set a final outcome.
While a revision is an unsaved draft, keep the previous final outcome active.
A subsequent evidence request does not erase an existing final outcome.

Calculate reports from the last saved final event for each eligible finding_id at the report cutoff.
Use server commit time for the cutoff and a strictly increasing per-item revision to order committed events.
Save against the expected current revision. Reject stale writes. Keep the client draft.

Before you add an event, remove duplicate requests.
Review revisions cannot add more counted items.
Do not carry reviews into a new run automatically.

Record cohort filters, time zone, start time, exclusive end time, and report cutoff.
Record metric_definition_version as d24-v1.
Store timestamps in UTC.

Include validated review items from partial jobs.
Use recommendation available_at for review cohorts and job_admitted_at for run cohorts.
Include admitted failed jobs without review items in result coverage and runtime measures.
Show counts, denominators, review coverage, failed jobs, partial jobs, and unchecked obligations.
Use the contract's formulas and zero-denominator rules.

Reviewer acceptance is not proof of regulatory correctness.
Keep the same-operator review limitation visible.

### Stage traces

The [runtime trace contract](../testing/spec-measurement-contract.md#4-runtime-traces-and-cost) is mandatory for REQ-X08 and AC-X08.
Record traces for source verification, extraction, retrieval, context selection, model calls, validation, persistence, and review events.
Use run_id, job_id, snapshot_id, stage_id, and attempt_id to connect records.
Record started attempts and their final, unknown, or interrupted states.
When a stage uses a saved artifact again, record skipped or not_applicable and the reference to that artifact's processing.

Record candidate and selected passage IDs, algorithm versions, model configuration, prompt version, schema version, and application version.
Record numeric usage, durations, attempts, safe error categories, and cost evidence when available.

Keep missing usage or cost fields unknown.
Remove duplicate logical charges. Add only charges with compatible currency and cost scopes.
For the same charge, an authoritative bill replaces its estimate at the report cutoff.
Record queue wait, worker time, stage time, and reviewer delay independently.
Do not add overlapping durations as wall-clock time.

Keep source text, query text, review edits, and review reasons in authorized case evidence storage.
Operational logs contain controlled identifiers, numeric measurements, and safe error categories only.
Numeric model-token counts are permitted.
Authentication tokens, private text, and hidden model reasoning are prohibited in operational logs.
Keep all private records and logs in Mumbai as specified in the security specification.

## 6. API functions

Authentication is mandatory for the first API functions that follow.

| Function | Required input and output behavior |
|---|---|
| Create/list/read case | Restrict the bank profile and case metadata to the owner. |
| Authorize/finalize upload | Connect the upload to the case. Send validation and extraction results before the document becomes eligible for analysis. |
| List/read document sources | Send version metadata. Passage inspection is permitted only after authorization. |
| Refresh regulations | Retrieve the configured public source scope through the external API. Send version metadata and freshness results through a job. |
| Start assessment | Accept selected versions, obligations, and an idempotency key. Send the job ID immediately. Revalidate current sources before assessment. |
| Start regulatory comparison | Make selection of older and newer regulatory versions and the affected assessment context mandatory. |
| Read job | Send the stage, terminal state, progress, allowance, and stop information. |
| Read findings | Send evidence, limitations, and proposed remedies for the specified snapshot. |
| Save review decision | Validate the outcome, accepted content, reason, and idempotency key. Approved must accept the original item. Add the event without changing the AI item. |
| Read reviewer outcomes | Send cohort filters, cutoff, counts, denominators, and coverage as specified in the measurement contract. Enforce case ownership. |
| Read stage trace | Send authorized controlled metadata and permitted artifact references. Keep private text outside operational telemetry. |
| Export assessment | Export Markdown or JSON. Include versions, citations, findings, review events, run status, regulatory verification time, and report cutoff. |

An idempotency key identifies repeated requests for the same operation.

In T2, set the executable request and response schemas before development of the handlers. Also set the related contract tests before development of the handlers.

D20 adds regulatory refresh and current-source verification to the approved API functions. Exact URL spellings are not more product requirements.
D24 adds reviewer outcomes and stage traces for REQ-X07/AC-X07 and REQ-X08/AC-X08.
REQ-X09/AC-X09 gives different evaluation procedures, not a public evaluation API.

## 7. Retries and failures

Use these job states:

| State | Meaning |
|---|---|
| queued | The job waits for execution. |
| running | The worker processes the job. |
| completed | The job records a result for every selected obligation. The worker saves mandatory audit references and finalization data. Human review can stay pending. |
| partial | The job has useful results that pass validation. Some mandatory work is unchecked. |
| failed | The assessment cannot produce a usable result. |

An atomic reservation completes as one indivisible operation.

Reserve the model-call allowance atomically before dispatch. If a process stops after dispatch, the reserved call still counts.

Use conditional execution claims to prevent competing assessments and duplicate finalization after duplicate queue deliveries.

Save the stage outputs. Save the identity of completed work. Retry only within the remaining job allowance.

Before you show success, save audit-critical stage references and finalization data.
If that save does not complete, do not mark the assessment completed.
Keep recoverable progress. Show the failure.
Retry the failed save. Do not repeat a completed model assessment.

A failed external metric export does not make one more assessment necessary.
Record that failure safely. Retry the export.
Remove duplicate metric events by stable event identity.
A failed review save cannot change the reported final outcome or its counts.

If regulatory verification does not pass or selected versions changed, stop before assessment. Record the reason in the failed job.

Reject invalid outputs. Reject unauthorized actions. Do not use these outputs or actions as evidence.

Set infrastructure timeouts and queue retry settings to obey the saved application deadline. Do not let these settings reset that deadline.

Standard SQS queues can deliver the same message more than once. Refer to [AWS delivery semantics](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html).

## 8. Project organization and verification

Keep these folders in the project root:

- docs/
- src/
- tests/
- evals/
- ops/
- data/
- runs/

Inside src/, keep domain logic outside HTTP handlers and provider adapters. Do not make a layers/ folder.

The [local test plan](../testing/spec-local-test-plan.md) gives tests for domain and adapter contracts. The [AI evaluation plan](../testing/eval-model-quality.md) gives evaluations of retrieval and model behavior.

The [measurement contract](../testing/spec-measurement-contract.md) controls reviewer metrics, retrieval scoring, stage traces, and measured improvement.
Keep different evidence records for local calculation tests, live source integration, and held-out model evaluation.
Reviewer approval does not replace the existing assessment quality gates.

T8 must test the AWS integration. T8 must also give the configuration lesson with steps in sequence.

[Next: Security and access](../security/03_SECURITY_ACCESS.md)
