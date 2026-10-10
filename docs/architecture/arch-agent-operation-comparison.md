# One-agent and multi-agent operation

Date: 2026-10-10.
Status: Revised review recommendation. No measured performance comparison exists.

## Recommendation

Use one bounded ReAct agent with orchestration in code.
Keep two specialists as an evaluation candidate.
Do not add an AI master for fixed routing, authentication, registry lookup, or budget checks.

The user specified one operator.
The user prefers code for tasks that have fixed rules.
One operator does not need tenant management or several AI roles.
The full [AWS review](arch-agent-aws-review.md) explains this revision.
The approved one-agent blueprint stays unchanged.

## Five decision points

| Point | One agent with code | Two specialists with code | Selection rule |
| --- | --- | --- | --- |
| Hosting | One assessment worker and the existing AWS services. | Both specialists can share the same worker and services. | Do not make a service for each prompt. |
| Security | IAM and application code control access. | The same execution role does not give different AWS permissions to each agent. | Add infrastructure isolation only for a demonstrated requirement. |
| Performance | Fewer handoffs. Unnecessary context can still increase work. | Narrower contexts can help. Extra calls and handoffs can remove that benefit. | Compare complete time and total token usage. |
| Evidence | Less information transfer. Earlier assumptions can stay unchanged. | Different judgments. Exceptions can be lost during transfer. | Compare source-grounded assessment errors. |
| Delivery | Fewer contracts and failure paths. | More role contracts and recovery paths. | Keep one agent unless two solve a named problem. |

## Work that remains in code

Use code for authentication, case checks, retrieval filters, hashes, and schemas.
Also use code for limits, retries, saved state, and progress events.
Use the model for regulatory interpretation, unclear applicability, evidence assessment, and correction proposals based on sources.
Do exact reference validation and assessment of claim support independently.

A ReAct loop selects further permitted actions from observed evidence.
It does not need a model call for every fixed processing step.

## Candidate and evidence gate

The candidate has two roles: regulatory interpretation and evidence assessment.
Fixed code coordinates both.
The [earlier seven-role proposal](arch-multi-agent-proposal.md) stays review history, not an implementation target.

Apply the same model, sources, cases, output checks, and aggregate limits to both designs.
Keep 24 dispatched model calls and 600 seconds of processing per job.
Set a shared token limit before a live comparison.
The existing 20-case evaluation and critical evidence gates stay unchanged.

No measurements show a slowdown, privacy incident, or quality advantage.
If quality is equal, prefer lower cost and simpler recovery.

**ELI10:** More AI workers need more coordination.
Use another worker only when its result justifies that extra work.
