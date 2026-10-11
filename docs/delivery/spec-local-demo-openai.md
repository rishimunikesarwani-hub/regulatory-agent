# Local demo with OpenAI and Langfuse

Date: 2026-10-11. Source: D57 and the user's submission-day request.

The user authorized OpenAI API processing and Langfuse for the local demo because AWS activation is incomplete.
This authorization changes the model provider for new local demo jobs only.
The AWS release and original model evaluation gates stay pending.

## Requirements

- LD01: Select the OpenAI provider before admission. Save `openai:gpt-4.1-mini-2025-04-14` in each new snapshot.
- LD02: Keep earlier snapshots and their model providers unchanged. Do not change providers during a saved job.
- LD03: Use public regulatory text and fictional bank data only. Reject private or current assessments.
- LD04: Count each provider request before dispatch. Keep the 24-call allowance, execution claim, deadline, and citation checks.
- LD05: Use strict structured output. Keep provider failures safe and unknown token counts unknown.
- LD06: Send only safe stage identifiers, model identifiers, durations, outcomes, and numeric token counts to Langfuse.
- LD07: Do not send prompts, responses, source text, review text, owner identifiers, credentials, or hidden reasoning to Langfuse.
- LD08: Keep local audit records mandatory. A failed optional Langfuse export must not repeat or fail an assessment.
- LD09: Keep all credentials in ignored local configuration. Show provider readiness without credential values.

OpenAI processing does not establish India residency.
Langfuse Cloud processing uses the configured project region.
This limited demo exception does not authorize private bank documents outside the approved India boundary.
The source collection contains historical RBI excerpts without verified current coverage or a second verified amendment.
Controlled comparisons must remain labeled Simulated.

## Acceptance

`tests/test_local_demo_openai.py` covers LD01 through LD09 with fake providers and no external traffic.
The existing browser checks protect upload, source inspection, reviews, exports, and saved comparisons.
A live demo needs working OpenAI and Langfuse project credentials.
Controlled tests cannot establish live provider access, trace delivery, or semantic quality.

## Terms

**Model provider:** The service that processes a model request.
**Langfuse:** The external service that displays model execution measurements.
**Structured output:** A model response whose fields obey a specified JSON schema.
