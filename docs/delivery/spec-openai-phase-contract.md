# Local OpenAI action contract

Date: 2026-10-11. Source: The user's fictional-policy demonstration request and the failed live checks.

The live provider returned valid JSON but supplied actions that failed assessment validation.
This correction gives the model the same action requirements that the application checks.
It does not remove validation or change the meaning of evidence.

## Requirements

- OP01: Give new OpenAI assessments the prompt identifier `assessment-vs5-openai-period-v4`.
- OP02: Keep earlier prompt identifiers and their instructions unchanged.
- OP03: State the required action and field relationships for each assessment phase.
- OP04: Extract exactly the selected obligation identifiers. Do not extract additional applicability clauses as separate obligations.
- OP05: Copy citation identifiers and locations from supplied passages. Include claim citations in the finding citations.
- OP06: Keep unknown dates, owners, and frequencies unknown. Missing operational evidence must not establish a control failure.
- OP07: Process a fictional policy through the local interface without AWS credentials or service activation.
- OP08: Preserve mandatory local audit records and optional metadata-only Langfuse Cloud observations.
- OP09: Restrict the response schema to the requested phase, selected identifiers, and exact supplied citations.
- OP10: Keep a bank's specific review schedule separate from a regulation's unspecified periodic review requirement.
- OP11: Use `assessment-vs5-openai-period-v5` for new local assessments and reassessments. Keep v4 behavior for earlier snapshots.
- OP12: Require a stated source interval for supported operational claims. Do not infer a missing year from the assessment period.
- OP13: For v5, add valid claim references to the finding reference list. Keep all original references and claim content.
- OP14: Reject invalid or unexamined references before this addition. Preserve all subsequent evidence checks and execution limits.
- OP15: Use `assessment-vs5-openai-period-v6` for new jobs after the v5 live check. Keep previous instruction and schema versions unchanged.
- OP16: For v6 operational assessments, exclude Supported when selected evidence has no stated interval. Reject a provider response that violates this condition.

Version `assessment-vs5-openai-period-v2` introduced phase instructions but did not complete the live assessment.
Version `assessment-vs5-openai-period-v3` also restricts the response schema.
Its completed live result incorrectly treated a weekly bank review schedule as an RBI mismatch.
Version `assessment-vs5-openai-period-v4` corrects this interpretation and states the missing-record classification.
Earlier version identifiers retain their earlier instruction and schema behavior.

Version `assessment-vs5-openai-period-v5` follows diagnostic results from the separate local evaluation.
Some fictional records omit the year, although the benchmark expects supported operational findings.
The existing source interval check rejects those unsupported dates.
Version v5 explicitly requests Needs review when source dates cannot establish operational support.

The evaluation also exposed a missing duplicated reference in the finding reference list.
For v5 and v6, the adapter adds exact, examined claim references to that list.
This addition changes reference metadata only, without changing the claim, status, remedy, or source text.
The application still rejects invalid references and unsupported operational periods.

These cases now form development evidence because their failures are known.
The original benchmark and its failed result remain unchanged.
New independent evaluation and the required Bedrock result remain pending.

Version v5 instructions did not prevent all unsupported operational responses in the live check.
Version v6 applies the same date condition to the generation schema and the response boundary.
These selected assessment flows require operational evidence for Supported.
The condition does not authorize a supported finding merely because an interval exists.
All claim, context, scope, ownership, and period checks remain mandatory.

The prompt identifier identifies the saved instruction version.
An assessment phase is one step that extracts obligations, extracts controls, or assesses an obligation.

## Verification

`tests/test_openai_phase_contract.py` checks admission, version separation, and the dispatched instruction contract without external calls.
A separate live check must show a completed fictional-policy assessment with accessible findings and source references.
The live check must also confirm remote Langfuse observations.
This check does not establish held-out model quality, current regulatory coverage, or AWS acceptance.
