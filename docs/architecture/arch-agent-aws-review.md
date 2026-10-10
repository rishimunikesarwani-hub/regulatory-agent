# AWS review of agent operation

Date: 2026-10-10.
Scope: One operator, one assessment workflow, and the proposed AWS deployment.
Status: Design audit. Runtime performance and security behavior are unverified.

## Recommendation

Use one bounded ReAct agent with orchestration in application code.
Keep two specialists as an evaluation candidate.
Remove the AI master from the recommended design.
The current workflow has fixed dependencies and specified limits.
Code can select the next stage without one more model call.

This recommendation replaces the previous multi-agent recommendation in this review series.
It is not a claim of better quality from one agent.
The approved one-agent blueprint stays unchanged.

**ELI10:** Use software for rules and record handling.
Use AI where evidence interpretation is necessary.
Add one more AI role only after it corrects a measured problem.

## Five material differences

| Area | One bounded agent | Two specialists | Review judgment |
| --- | --- | --- | --- |
| AWS deployment | One assessment worker can host the agent loop. | The same worker can host both loops. | Agent count does not make more AWS services necessary. |
| IAM and identity | Code and IAM restrict operations. | Agents using the same function credentials share its AWS permissions. | Different agent names do not make an IAM boundary. |
| Time and cost | Fewer role transfers are necessary. A large context can still have a high cost. | Smaller contexts are possible. Repeated instructions and sequential handoffs can add work. | Both designs have unmeasured latency and cost here. |
| Evidence and context | One agent can keep context across judgments. It can also keep an incorrect assumption. | Different instructions can help the model examine one subject. Transfers can omit an exception or copy an error. | Keep source passages. Test their meaning, not only JSON validity. |
| Private information | Code must restrict case data and model input. | One specialist can remove private evidence that is not necessary. | A smaller data set can help either design. Model separation alone is not sufficient. |

The two-specialist candidate has one regulatory interpretation role and one evidence assessment role.
The first finds applicable requirements.
The second compares controls and evidence with those requirements.
Code controls the sequence of both roles.
Different prompts do not make different functions, models, or providers necessary.

## IAM does not require a multi-user product

An AWS execution role gives the Lambda function access to AWS resources.
Agent roles are application concepts.
Two agents using that function's default credentials share the same execution role.
This is a consequence of the [Lambda execution-role model](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html).

Different functions with restricted roles can have different AWS permission boundaries.
Do not add that infrastructure without a specified isolation requirement.
That infrastructure can also protect fixed code services without more AI agents.

IAM can authorize API access with signed requests and applicable AWS credentials.
A client identity mechanism is still necessary.
Refer to [IAM API authorization](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-access-control-iam.html).

The approved browser design already uses Cognito.
One invited operator is sufficient for this product scope.
An IAM-signed client is an alternative access design, not a reason for more agents.
Do not embed permanent AWS access keys in browser code.
Tenant management, an organization hierarchy, and one more reviewer account are not necessary for this review.

Keep case and snapshot checks even with one operator.
The same operator can do assessments of different banks, documents, and dates.
A previous case must not supply evidence to the next case.

## What is a risk, and what is observed?

| Concern | Current evidence | Required response |
| --- | --- | --- |
| Performance degradation | No runtime or baseline exists. The project has no measured slowdown. | Measure model, retrieval, queue, tool, and total time independently. |
| Personal-data leakage or mixing | The project has no observed incident or runtime isolation tests. | Filter by case and snapshot. Remove identifiers that are not necessary. Test synthetic cross-case records. |
| Context manipulation | Authorized documents can contain hostile instructions. The project did not do an attack test. | Treat source text as evidence. Validate every tool action in code. |
| Lost context | Both designs have unmeasured omission rates. | Test exceptions, amendments, contradictions, and source-version boundaries. |
| Agent collusion | The project has no observed collusion. | Test shared errors and unauthorized transfers. Do not use collusion as the architecture justification. |

IAM authorizes resource operations.
It does not show whether text inside an authorized document is a permitted instruction or a correct regulatory interpretation.
Source hashes show changes compared with saved content.
They are not proof of truth, freshness, or protection from prompt injection.

Do not keep case documents or conversation history in reusable Lambda global state.
Use safe service clients again, independently from per-job evidence.
AWS gives a warning against storage of sensitive user data across execution-environment reuse.
Refer to [Lambda best practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html).

## Use code wherever the rules are fixed

| Work | Use code for | Use the model for |
| --- | --- | --- |
| Access and governance | Identity validation, case scope, tool permissions, limits, and audit events. | No access decision. |
| Source handling | API requests, response validation, version hashes, stored snapshots, and exact text differences. | Interpret substantive changes and regulatory exceptions. |
| Retrieval and context | Parse supported text. Filter sources. Rank passages. Remove duplicates. Enforce size limits. | If related evidence is missing, select subsequent permitted searches. |
| Assessment checks | Validate schemas, IDs, source versions, exact quotations, and arithmetic. | Judge applicability, control relevance, and evidential support. |
| Workflow and output | Stage order, registry lookup, retries, deadlines, persistence, progress, and report formatting. | Propose findings and corrections grounded in evidence. |

An accurate quotation alone is not proof of claim support.
An exact text difference is not proof that a regulatory requirement changed.
Keep those meaning checks in the assessment and evaluation process.

Use a static tool allowlist and versioned role configuration.
An AI registry manager or dynamic agent marketplace is not necessary.
Keep the bounded ReAct loop only where evidence controls the next useful action.
Do not force every fixed processing step through a model.

## Reduce context without losing evidence

One agent can work without every document in every request.
Two agents can work without copies of each other's full conversation.
Keep canonical documents outside model context.

1. Select the case, snapshot, document versions, and obligation before retrieval.
2. Retrieve the necessary passages and their source references.
3. Include applicable conditions, definitions, exceptions, and contradictory evidence.
4. Remove duplicate passages and unrelated tool fields.
5. Remove personal identifiers that are not necessary for the assessment.
6. Keep a short structured record of completed work and unresolved questions.
7. If the selected passages are not sufficient, retrieve more evidence.
8. If limits prevent sufficient coverage, stop the current run with partial or failed status.

Keep unchecked obligations in the result.
A new user-selected snapshot is mandatory for a smaller scope.

Do not remove an exception without a warning to meet a token limit.
Do not replace all source evidence with a model-written summary.
Known-field removal cannot guarantee removal of personal information from free text.
Test that boundary with synthetic identifiers. Examine the remaining disclosure.

## AWS latency and cost

Prompt processing depends partly on input length.
Output generation also consumes time.
More sequential model calls add waiting and processing work.
Their smaller inputs might offset some overhead.
AWS distinguishes prompt processing from output generation in its [latency guidance](https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-runtime-otps.html).

Different agent loops in one worker do not cause a Lambda cold start for each role.
Different Lambda invocations add invocation boundaries and possible initialization work.
Do not add that deployment split to get different prompts.

Measure total duration, not only time to the first streamed event.
Progress streaming does not decrease the assessment duration.
For sequential work, total time includes queue wait, initialization, model calls, tools, and orchestration.
If independent work occurs at the same time, do not add overlapping spans twice.

Both designs can use the existing API, SQS worker, S3, DynamoDB, and Bedrock connections.
SQS and saved job state support recovery.
They do not reduce model work.
Code must handle duplicate queue delivery without restarting the allowance.
Refer to [Lambda with SQS](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html).

The 600-second worker budget is less than standard Lambda's documented 900-second maximum.
This is not proof that the assessment will finish in time.
Reserve finalization time. Set dependency timeouts from the remaining budget.
Refer to [Lambda timeout configuration](https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html).

There is no evidence for a fixed cost estimate yet.
Count all model attempts, tokens, retrieval charges, Lambda duration, storage, requests, and telemetry in the declared cost scope.
Use rates for the model, API, and regions in the validated configuration.
Before measurement, do not assume that Lambda or Bedrock is the primary cost.

Prompt caching is optional.
Before you count savings, do checks of the model, API, region, cache limits, and observed hits.
Caching is not proof of regulatory freshness or case authorization.
Refer to [Bedrock prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html).

## Smallest useful comparison

Build the one-agent path first with the same output contracts necessary for the two-specialist candidate.
Use fixed-code orchestration for both paths.
Keep the source adapter, retrieval rules, model, regions, and validation checks equal.

Use the existing 20 held-out cases after development tuning.
Keep the 24-call job ceiling, 600-second processing deadline, and selected obligation limit equal.
Before the comparison, set the same total token ceiling.
The existing call ceiling is not a token or monetary budget.

Compare correct assessments, critical false supported findings, citation support, completion, total time, and total cost.
Include failures, retries, incorrect abstentions, and partial results.
Keep the existing 90% agreement gate and all critical evidence gates.
Do not treat 20 cases as a reliable production tail-latency estimate.

Measure each model attempt in application records.
The Bedrock Invocations metric does not include throttled requests or requests rejected before processing.
It cannot replace the application's stricter 24-dispatch counter.
Use applicable [Bedrock runtime metrics](https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-runtime-metrics.html) as supporting telemetry.

The 600-second deadline starts at worker execution.
Record queue wait independently. Also include it in user-visible completion time.
No end-to-end percentile target has approval.

Use two specialists only if they correct a named quality or data-exposure problem within the same limits.
If quality is equal, prefer lower cost and simpler recovery.
If the candidate does not pass a critical gate, keep the one-agent path.

## Review evidence

The source, test, and evaluation folders contain only placeholder files.
No application runtime, traces, or measured comparison was available.
Thus, the formal audit shows UNVERIFIED performance.
Refer to [the audit output](../../runs/2026-10-10-aws-agent-review-audit/audit.md).
Language and preservation checks are in [the verification record](../../runs/2026-10-10-aws-agent-review-verification.md).
