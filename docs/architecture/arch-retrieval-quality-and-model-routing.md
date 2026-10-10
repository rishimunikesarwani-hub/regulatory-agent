# Retrieval quality, assessment audit, and model routing

Date: 2026-10-10.
Status: Earlier discussion, kept for review history.
Update: [D24](../decisions/gov-decision-log.md#d24---reviewer-outcomes-and-measured-agent-baseline) now adopts the baseline, different evaluations, and stage traces.
The [measurement contract](../testing/spec-measurement-contract.md) controls implementation. Routing and a second reviewer are still later experiments.

The user requested an argument, not automatic acceptance of their proposed direction.
The approved one-agent design and fixed model stay unchanged.

## Position

One agent can use several models through a router controlled by code.
Agent count, model count, and measurement quality are different choices.
An additional agent does not establish retrieval completeness or independent assessment quality.

The earlier comparison gave too much importance to fewer calls and handoffs.
Observability must also help identify incorrect retrieval, missing evidence, and incorrect findings.
Observability means records and measurements that explain system behavior.
These records alone do not give the correct reference answer.

The [blueprint](02_TECHNICAL_BLUEPRINT.md) already specifies different measurements for retrieval and assessment.
The [evaluation plan](../testing/eval-model-quality.md) has approved gates, but its labeled fixtures do not yet exist.
There is no measured quality, latency, or cost result.

## How to judge retrieval

S3 stores the bank documents.
Application code extracts and searches their passages.
The external API supplies public regulatory sources.
It receives no private bank evidence.

| Check | Regulatory source | Bank evidence |
|---|---|---|
| Source scope | Correct authority, jurisdiction, assessment date, version, and applicable amendments. | Correct case, selected snapshot, document version, evidence type, and assessment period. |
| Passage selection | Required clause, definitions, conditions, exceptions, and applicable amendments. | Relevant control, operational records, dates, exceptions, and conflicting records. |
| Reference integrity | Exact source text, version, location, and verified source status. | Exact extracted text, version, page or row, and authorized access. |

A recent API response does not prove that its provider found every amendment.
An exact quotation does not prove that the quotation supports the conclusion.
A high retrieval score does not prove completeness.
It is not a calibrated probability.

Use development cases based on source evidence.
Add labels to the required passages before model execution.
Add labels to original page or row spans.
This method lets a comparison use different chunk boundaries.
Include exceptions that can change the result.
Include conflicting records, irrelevant documents, and cases with missing evidence.

Record whether a qualified domain expert reviewed the reference answers.
Do not use the assessed model as the only source of reference answers.

Measure regulatory retrieval and bank-evidence retrieval independently.
Measure the external provider's source coverage independently of passage selection inside returned documents.

| Measurement | Meaning |
|---|---|
| Required-span recall | Retrieved required source spans divided by all labeled required source spans. |
| Context relevance | Whether the passages sent to the model address the assessment question. |
| Decisive omissions | Missing exceptions or conflicting records that could change the outcome. |

These measurements apply to the labeled benchmark.
They cannot establish complete recall for every live request.

AWS also uses different metrics for context relevance and context coverage.
Context coverage needs ground truth.
Ground truth means the reference information used to judge the result.
See [AWS retrieval evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-eval-llm-results.html).
This reference does not add Bedrock Knowledge Bases to the approved stack.

During a live run, code does checks of scope, freshness, references, and required evidence fields.
The agent can request another permitted retrieval pass when evidence is insufficient.
Unresolved missing or conflicting evidence produces needs_review.
A failed current-source check stops the current assessment under the existing contract.
These checks reduce risk. They do not prove that retrieval found all relevant evidence.

## How to audit the assessment

Keep this relationship for each conclusion:

```text
Finding -> requirement element -> cited source spans -> evidence period
                                     |
                        exceptions and conflicts considered
```

Code does checks of identity, versions, quote matches, schemas, permissions, and limits.
Code cannot establish every semantic relationship between evidence and a regulatory requirement.
A human reviewer examines whether the cited evidence supports the claim.
An optional model judge can identify suspect claims, but its score can be incorrect.
A fixed model check does not need another autonomous agent.
Agreement between models does not prove correctness.

Keep the approved primary agreement gate and critical false-supported checks.
Do not hide errors or unexpected abstentions by removing them from the evaluation total.

## Observability and improvement

Use one run ID to connect stage records.
Record source and snapshot IDs, selected passage IDs, retrieval settings, and model choice.
Also record attempts, durations, token usage, validation failures, and outcomes.
Keep query records and private source text in authorized evidence storage.
Keep raw private text, full prompts, responses, and credentials out of operational logs.

Keep short assessment reasons.
Do not keep hidden model reasoning traces.

AWS supplies operational metrics for latency, tokens, errors, and throttles.
Application records must add retrieval quality, evidence links, review outcomes, and failure causes.
See [AWS runtime metrics](https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-runtime-metrics.html).

Classify a failure before you change the system:

```text
Wrong source      -> correct source selection or provider coverage
Missing passage   -> correct extraction, retrieval, or context selection
Wrong conclusion  -> correct assessment instructions or model choice
Invalid reference -> correct output checks and reference handling
```

An incorrect conclusion with correct evidence suggests an assessment problem.
It does not automatically justify a more expensive model.
Prompt, schema, and task-definition errors can cause the same symptom.

Change one factor on development cases.
Then compare the revision on a different held-out set.
Do not use held-out answers to adjust routing and still call those cases unused.
Keep earlier results.
Record prompt, retriever, router, model, and source versions.

## Argument for and against model routing

| Argument for routing | Counterargument |
|---|---|
| A less expensive model may do a specified small task correctly. | It can make an undetected error. Its own confidence is insufficient. |
| A more capable model may need fewer attempts on difficult cases. | More reasoning cannot replace a missing source that can change the result. |
| Different tasks can use different model capabilities. | Model changes can change tool formats, context handling, and output behavior. |
| Routing may reduce average inference cost. | Routing, retries, escalation, and repeated context can remove the saving. |

One agent can keep one job state while code selects a model for each permitted call.
Permissions and the evidence snapshot stay outside model control.
Code should do fixed-rule validation without a model call.
Development results must support the selection of routes for each task.

All live routed calls, retries, and fallbacks share the existing 24-call allowance and 600-second deadline.
Keep offline evaluation costs in their own category.
Show these costs in the comparison.

AWS Intelligent Prompt Routing has model, language, and Region limits.
Its documentation says it cannot adjust from application-specific performance data.
Therefore, it does not supply our feedback loop automatically.
See [AWS routing limits](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html).

Make sure each proposed model uses India-only destinations before private processing.
Make sure it works with the tools.
This discussion does not replace the current fixed model.

Cost depends on model rates, token use, tools, retries, and infrastructure.
Review effort is an additional operational cost.
Better reasoning can reduce total cost if it prevents enough repeated work.
It can also increase cost without improving the outcome.
See [Bedrock pricing](https://aws.amazon.com/bedrock/pricing/).

For a two-model escalation experiment, compare these quantities:

```text
Expected inference cost = routing cost + first-model cost
                        + escalation rate * second-model cost

Cost per correct assessment = total measured run cost
                            / correctly assessed cases
```

Measure actual inputs, outputs, cache use, and repeated attempts.
Keep all evaluated cases in quality reports.
Apply critical quality gates before you decrease cost per correct assessment.

## Recommended next step

Keep one agent and the approved model for the baseline.
Make the labeled retrieval fixtures.
Add measurements to each stage.
Measure the quality loss and cost for each failure cause and stage.
Then do tests of a fixed routing policy against that baseline on the same held-out cases.

Use routing only if it meets the quality gates and produces a useful measured benefit.
Add another agent only when a specified task or review boundary needs its own context and handoff.

ELI10: Record the pages the analyst read.
Record how those pages support the finding.
Do tests of a different model only after these records show what needs improvement.
