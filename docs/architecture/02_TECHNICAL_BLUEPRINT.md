# Technical Blueprint: local operation and AWS operation

> Approval: The user approved the design in the planning conversation. The project first saved this document on 2026-10-08.
> Language revision: 2026-10-09.
> Required document: [PRD](../product/01_PRD.md).
> Decision references: [D07–D10, D16, D17, and D20](../decisions/gov-decision-log.md).
> Evidence status: The design has approval. This project has no deployed services or verified model invocation.
> Writing reference: [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf).

## 1. Architecture

### Architecture views

Open the [AWS system view](arch-system.html) to inspect components and service boundaries.
Open the [assessment view](arch-assessment.html) to inspect source checks, evidence processing, and human review.
Both views use ArchView and show the approved design.
The application remains unimplemented.

Use Zoom to inspect a view.
Use Image to export a PNG.
Use Report to open the browser print dialog.
Select Save as PDF to save the report.
Use the navigation links to change views.

The editable sources are [system JSON](arch-system.json) and [assessment JSON](arch-assessment.json).
The external regulatory API remains part of the design.
Provider selection remains undecided.
The user excluded a crawler view.

**ELI10:** The system view shows the parts and their connections.
The assessment view shows the checks before the operator reviews a finding.

![AWS system architecture](arch-system.png)

![Assessment controls](arch-assessment.png)

### Components

Use the same application logic for local operation and AWS operation. Keep the domain rules separate from the connections to external services.

An interface specifies how application logic communicates with a service. An adapter connects that interface to a local resource or an AWS service. The interfaces cover storage, records, jobs, identity, model calls, and public regulatory retrieval.

The local adapters let developers understand the assessment logic and do tests before AWS account configuration. At deployment, AWS adapters use the same interfaces. The adapters do not create two separate products.

| Component | Approved technology | Function |
|---|---|---|
| Frontend | React and TypeScript with Vite | Gives the user a browser workspace for evidence inspection and review. |
| Backend | Python and FastAPI | Uses request and response types to check data at the assessment interface. |
| Cloud API | API Gateway and Lambda | Processes short requests from authenticated users. Assessments run separately. |
| Private document storage | S3 in Mumbai | Stores bank files, assessment evidence copies, extracted passages, and reports. It does not determine the current regulatory version. |
| Regulatory source retrieval | External retrieval API. Provider TBD. | Retrieves current public regulations and amendments with source metadata. |
| Cloud records | DynamoDB in Mumbai | Stores case metadata, job states, counters, and references. |
| Background work | SQS and Lambda worker | Runs assessments separately from API requests. Saves progress. |
| Identity | Cognito | Authenticates operators. Does not permit demo sign-up. |
| AI | Bedrock profile in.openai.gpt-5.6-luna | Uses the selected India profile. Destination, access, and quality checks remain necessary. |
| Public frontend hosting | S3 and CloudFront | Serves public static assets only. Does not cache private reports or documents. |
| Infrastructure | AWS SAM configuration in ops/ | Describes the deployment for review. |
| Local adapters | Filesystem, SQLite, local worker, controlled AI and retrieval responses | Permits default development and tests without AWS credentials. |

Framework and package versions remain uninstalled and unverified. Packaging configuration also remains unverified. T2 must select compatible versions. The package configuration must require these exact versions. T2 must record these versions. The current root manifest contains documentation metadata only.

## 2. Request and assessment flow

The steps below describe the required application behavior.

1. The authenticated user creates a case and saves a bank profile.
2. The API authorizes the upload. It completes the upload process only after validation and extraction.
3. The application refreshes public regulations through the external retrieval API. The user selects returned versions and obligations.
4. The application starts the assessment with an input snapshot that cannot change. It returns a job ID.
5. The job runner calls the same worker service locally or through SQS.
6. The worker verifies that selected regulatory versions remain current. If selected versions changed, it requests selection review before assessment.
   After verification, it retrieves obligations and controls. Then it runs the bounded agent.
7. The agent selects permitted actions. Application code checks each action before execution.
8. The worker checks results and citations before it saves findings.
9. The UI polls job progress. It shows findings, source passages, and reviewer actions.
10. A later version comparison creates new results with links to the old snapshot. It does not change previous results.

Do not keep the browser request open until the assessment finishes.

API Gateway HTTP integrations have a documented integration limit of 30 seconds. The application uses jobs and does not depend on this time window. See [AWS HTTP API quotas](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-quotas.html).

### Current regulatory sources

The external retrieval API supplies current regulatory content.
S3 stores evidence of past assessments.
Do not use an S3 copy to establish that a regulation is current.

Refresh the scoped source catalogue before obligation selection.
Revalidate selected regulations at worker start before assessment.
Use the existing job service for these network operations.
Keep the ten-minute processing deadline.

The provider must return authoritative source text and source URLs.
It must identify applicable amendments, replacements, and withdrawals.
A search snippet or provider retrieval timestamp alone cannot prove current coverage.
Record the authority verification time and provider coverage limitations.

Use publication dates and effective dates separately.
Assess applicability for the selected assessment date.
An amendment with a future effective date does not automatically replace the currently applicable requirement.

Save the exact response text and citation locations as assessment evidence.
Keep its authority, source URL, version, content hash, and amendment references.
Record retrieval time, authority verification time, and freshness status.
A freshness status states whether current-source verification succeeded for this run.
It does not promise that no later update exists.

When available, use provider version identifiers or HTTP validators.
An ETag identifies a particular HTTP representation.
Validate it against the authority or a provider with verified authority synchronization.
See [HTTP response validation](https://www.rfc-editor.org/rfc/rfc9111.html#section-4.3).

When source content or applicable regulatory metadata changes, create a new version.
Include withdrawals and effective-date changes in that comparison.
Keep the earlier assessment and its source copy.
If selected versions changed, require selection review.
Do not change the selected obligation scope automatically.

If verification fails, block a new current assessment.
Show the last successful check and the failure.
Keep historical reports accessible with their original assessment date and freshness status.
Do not silently use old content or mark it current.

T1 must select and verify the provider.
Its API endpoint, authority coverage, update delay, historical versions, terms, and pricing remain TBD.
The project has not verified a direct RBI API or a zero-delay update guarantee.

T2 must define retrieval request and response schemas.
Set request limits, timeouts, pagination limits, and response-size limits before implementation.
Count retries against the saved retrieval allowance.
Keep retrieval counters separate from the 24 model calls.
All requests must fit within the existing job deadline and document limits.
Incomplete pagination or exhausted allowances cannot establish current coverage.

The first release refreshes on request and before each current assessment.

Controlled local tests and held-out model evaluations use fixed source versions.
Label these runs as simulations or historical benchmarks.
They cannot establish current regulatory coverage.

An independent scheduled monitor remains future work.

The regulator remains the authority.
The provider transports and retrieves its content.
See [RBI Master Directions](https://www.rbi.org.in/Scripts/BS_ViewMasterDirections.aspx?did=338).

## 3. Agent and retrieval rules

Use one bounded agent. A bounded agent can use only the tools, data, and allowances that the application permits.

Keep tool execution under application control. Do not require a multi-agent framework for this release. Do not require native tool execution on the model provider's server.

The model returns a structured action request. Before tool execution, application code checks these items:

- Action name.
- Case and snapshot scope.
- Arguments.
- Remaining allowance.
- Response schema.

The agent can request only these actions:

- Retrieve obligations from the selected regulatory version.
- Find possible controls in the selected case documents.
- Inspect specified evidence passages.
- If the evidence is insufficient, request another retrieval pass within the permitted limits.
- Propose structured findings, remediation requests, and evidence requests.

Use keyword/BM25 retrieval to search selected bank documents and verified regulatory response passages. Before the relevance ranking, filter passages by owner, case, document kind, and selected version.

If retrieval did not return a passage, do not count that passage as inspected evidence. This rule also applies to relevant passages.

Measure retrieval errors separately from assessment errors.

Do not treat a tool request in an uploaded document as authorization. The agent cannot do these actions:

- Run shell commands.
- Send messages.
- Access unrelated cases.
- Browse arbitrary URLs.
- Change bank systems.

Count every dispatched model request against the **24-call** allowance for the job. This includes schema failures, retries, and requests with an uncertain outcome.

Save a **ten-minute** job deadline that starts when the worker starts. Do not reset the deadline after a delivery retry. Record queue waiting time separately.

If the allowance is exhausted, keep the partial results that have source references. Keep the record of unchecked obligations.

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

AWS documentation describes Bedrock runtime support, structured outputs, and the India inference profile for the selected model. The project selected this model as an implementation dependency. This selection does not prove model quality.

Before the application accepts private uploads, complete these checks:

1. Check the installed SDK and API structure.
2. Check response processing.
3. Check the inference profile destinations.
4. Check an actual model invocation.

A regional endpoint alone does not prove that processing stays in India.

Sources:

- [AWS model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-56-luna.html)
- [Inference profile destinations](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
- [Bedrock data retention](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html)

Do not claim that all model processing has zero retention. During integration, check the applicable model terms and service settings.

If the selected model cannot meet the approved boundaries or quality gate, record the problem. Propose a model change for review. Do not substitute another endpoint without an approved change.

## 5. Records and evidence

The records below specify the approved data requirements. The field names are implementation guidance. They do not mean that a database exists.

| Record | Identity and contents | Required condition |
|---|---|---|
| Case | case_id, owner_id, bank profile, created_at | Check the owner before access to each child record. |
| DocumentVersion | document_version_id, case_id, source identity, kind, version label, SHA-256, storage reference, source URL, publication/effective dates | Do not change the content or extraction for this version. |
| Passage | passage_id, document_version_id, location, extracted text | Each passage identifies one original version and a source location that the user can inspect. |
| AssessmentSnapshot | snapshot_id, case_id, bank-profile copy, selected versions and obligations, prompt/model versions | Save the contents before execution. Do not change these contents. Do not automatically include later uploads. |
| Job | job_id, snapshot_id, state, stage, call count, deadline, execution claim, timestamps, retrieval count, authority verification time, freshness status | Permit only one active execution and one finalization. Keep counters through retries. |
| Obligation/Control | stable ID, structured requirement or control, applicability, source passage references | Keep unknown fields unknown. |
| Finding | finding_id, snapshot_id, obligation/control references, status, evidence condition, citations, proposed remedy | Use only evidence that passes validation to support a finding. |
| ReviewDecision | finding_id, reviewer_id, disposition, note, timestamp | Keep the original AI finding. Do not overwrite it with the review decision. |

Keep large extracted content and reports in private blob storage. Use the record store for metadata and references. Do not use it for report bodies of unlimited size.

Keep these original source locations:

- PDF: the original page number and a stable passage ID.
- DOCX: the paragraph or table-cell location from extraction.
- TXT: the line range.
- CSV: the row and the applicable column identifiers.

Include these items in every citation:

- Selected document version.
- Passage ID.
- Source location.
- Quoted excerpt.

Check that the stored extraction contains the quote. Check that the quote, in its context, supports the related claim.

A replacement document creates a new version. Existing snapshots continue to use the old version. Each new run must explicitly select its versions. Do not let retrieval automatically mix current and superseded files.

## 6. API functions

The first API requires authentication for the functions below.

| Function | Required input and output behavior |
|---|---|
| Create/list/read case | Restrict the bank profile and case metadata to the owner. |
| Authorize/finalize upload | Connect the upload to the case. Return validation and extraction results before the document becomes eligible for analysis. |
| List/read document sources | Return version metadata. Permit passage inspection only after authorization. |
| Refresh regulations | Retrieve the configured public source scope through the external API. Return version metadata and freshness results through a job. |
| Start assessment | Accept selected versions, obligations, and an idempotency key. Return the job ID promptly. Revalidate current sources before assessment. |
| Start regulatory comparison | Require explicit older and newer regulatory versions and the affected assessment context. |
| Read job | Return the stage, terminal state, progress, allowance, and stop information. |
| Read findings | Return evidence, limitations, and proposed remedies for the specified snapshot. |
| Save review decision | Save the reviewer disposition and note separately from the finding. |
| Export assessment | Export Markdown or JSON. Include input versions, citations, findings, review decisions, run status, and regulatory verification time. |

An idempotency key identifies repeated requests for the same operation.

In T2, set the executable request and response schemas before development of the handlers. Also set the related contract tests before development of the handlers.

D20 adds regulatory refresh and current-source verification to the approved API functions. Exact URL spellings are not additional product requirements.

## 7. Retries and failures

Use these job states:

| State | Meaning |
|---|---|
| queued | The job waits for execution. |
| running | The worker processes the job. |
| completed | The job accounts for every selected obligation. An individual finding can still require review. |
| partial | The job has useful results that pass validation. Some required work remains unchecked. |
| failed | The assessment cannot produce a usable result. |

An atomic reservation completes as one indivisible operation.

Reserve the model-call allowance atomically before dispatch. If a process stops after dispatch, the reserved call still counts.

Use conditional execution claims to prevent competing assessments and duplicate finalization after duplicate queue deliveries.

Save the stage outputs. Save the identity of work that is already complete. Retry only within the remaining job allowance.

If regulatory verification fails or selected versions changed, stop before assessment. Record the reason in the failed job.

Reject invalid outputs. Reject unauthorized actions. Do not use these outputs or actions as evidence.

Set infrastructure timeouts and queue retry settings to support the saved application deadline. Do not let these settings reset that deadline.

Standard SQS queues can deliver the same message more than once. See [AWS delivery semantics](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html).

## 8. Project organization and verification

Keep these folders in the project root:

- docs/
- src/
- tests/
- evals/
- ops/
- data/
- runs/

Inside src/, keep domain logic separate from HTTP handlers and provider adapters. Do not create a layers/ folder.

The [local test plan](../testing/spec-local-test-plan.md) covers domain and adapter contracts. The [AI evaluation plan](../testing/eval-model-quality.md) covers actual retrieval and model behavior.

T8 must check the real AWS integration. T8 must also provide the configuration lesson with steps in sequence.

[Next: Security and access](../security/03_SECURITY_ACCESS.md)
