# Agent Performance Audit

Result: **UNVERIFIED**

| Scope | Value |
|---|---|
| system | The Regulatory Agent |
| workflow | Selected regulatory assessment. one agent versus two specialists |
| environment | Design only. no AWS runtime |
| window | 2026-10-10 document and placeholder inspection. no runtime samples |
| currency | USD |
| Measured run | candidate |

| ID | Area | Result | Evidence | Finding | Acceptance check | Next action |
|---|---|---|---|---|---|---|
| A01 | Workflow performance | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | No runtime paths exist. | Measure ordinary and adverse assessment paths. | Implement one-agent baseline and record each step. |
| A02 | Observability | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | No runtime traces exist. | Join request and stage records without private content. | Record model, tool, queue, and retry spans. |
| A03 | Budgets and service objectives | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | Call and time limits exist only in specifications. | Enforce global limits outside the model. | Test dispatch reservation and deadline persistence. |
| A04 | Cost drivers | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | No token usage, actual rates, or charges exist. | Reconcile every in-scope attempt and allocated cost. | Record usage and verify rates for the actual configuration. |
| A05 | Latency sources | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | No latency samples exist. | Separate complete duration from first-token time. | Measure queue, initialization, model, and tool time. |
| A06 | Model call reduction | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | Fixed routing and validation do not require model judgment. | Removal preserves quality and access controls. | Compare code orchestration without an AI master. |
| A07 | Model routing | NOT_APPLICABLE | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | Both designs retain the same pinned model. | No model-router comparison is in scope. | Reopen this check if model selection changes. |
| A08 | Prompt and context | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | Context assembly is not implemented. | Preserve exceptions and contradictions under context reduction. | Test scoped passages and structured state. |
| A09 | Token budgets | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | No aggregate token ceiling or usage samples exist. | Set input, output, and aggregate token limits. | Measure development cases before freezing a common ceiling. |
| A10 | Caching | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | Prompt-cache support and benefit remain unverified. | Verify support, version separation, and observed hits. | Leave caching optional until measured evidence supports it. |
| A11 | Parallel work and streaming | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | Tools and progress events are not implemented. | Only independent work overlaps. Events reveal no private content. | Test safe progress and client disconnect behavior. |
| A12 | Background jobs | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | Saved jobs and duplicate-delivery checks are specified only. | A duplicate cannot reset limits or repeat finalization. | Test restart, redelivery, and expired jobs. |
| A13 | Rate limits and backpressure | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | No provider quotas or burst tests exist. | Bound dispatch and recovery under throttling. | Check actual quotas and repeated user requests. |
| A14 | Failure controls | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | No failure-control tests exist. | Count uncertain attempts and contain late responses. | Test timeouts, capped retries, and dependency failures. |
| A15 | Scaling and state | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | No cold-start or saved-state recovery measurements exist. | Keep case state separate from reused service clients. | Test warm reuse with different synthetic cases. |
| A16 | Measurement | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | Both request arrays are empty. | Use matched cases, scope, load, and recorded versions. | Collect paired runs without inventing missing values. |
| A17 | Cost and quality | UNVERIFIED | ../docs/architecture/arch-agent-aws-review.md (Review evidence and five material differences): Design inspection and cited primary AWS sources. No runtime measurement. | No candidate has demonstrated an improvement. | Pass all quality gates within common limits. | Retain one agent when quality is equal and operation is simpler. |

| Metric | Observed | Target | Result |
|---|---|---|---|
| sample_size | 0 | 20 | UNVERIFIED |
| p95_latency_ms | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| p99_latency_ms | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| cost_per_success | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| success_rate | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| mean_quality_score | UNVERIFIED | 0.9 | UNVERIFIED |
| error_rate | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| comparison_context | Insufficient comparison sample | matched cases and context | UNVERIFIED |
| scope | complete | complete | PASS |

Comparison: UNVERIFIED

| Context | Baseline | Candidate |
|---|---|---|
| dataset_id | NOT_CREATED. planned held-out 20 cases | NOT_CREATED. planned held-out 20 cases |
| rubric_id | eval-model-quality.md primary outcome agreement | eval-model-quality.md primary outcome agreement |
| workload_id | one case and at most 20 selected obligations | one case and at most 20 selected obligations |
| load_profile | one operator. no load measurements | one operator. no load measurements |
| cost_basis | All model attempts, external retrieval, and allocated AWS infrastructure. rates unverified | All model attempts, external retrieval, and allocated AWS infrastructure. rates unverified |

| Metric | Baseline | Candidate | Candidate minus baseline |
|---|---|---|---|
| p95_latency_ms | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| p99_latency_ms | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| cost_per_success | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| success_rate | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| mean_quality_score | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| error_rate | UNVERIFIED | UNVERIFIED | UNVERIFIED |

- Insufficient comparison sample
- Check verdicts are reviewer judgments. File existence does not prove evidence content.
- Metric gates apply only to supplied samples and declared costs.
- No statistical significance, runtime enforcement, or production certification is established.
