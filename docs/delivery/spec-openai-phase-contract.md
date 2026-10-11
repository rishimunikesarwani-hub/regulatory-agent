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

Version `assessment-vs5-openai-period-v2` introduced phase instructions but did not complete the live assessment.
Version `assessment-vs5-openai-period-v3` also restricts the response schema.
Its completed live result incorrectly treated a weekly bank review schedule as an RBI mismatch.
Version `assessment-vs5-openai-period-v4` corrects this interpretation and states the missing-record classification.
Earlier version identifiers retain their earlier instruction and schema behavior.

The prompt identifier identifies the saved instruction version.
An assessment phase is one step that extracts obligations, extracts controls, or assesses an obligation.

## Verification

`tests/test_openai_phase_contract.py` checks admission, version separation, and the dispatched instruction contract without external calls.
A separate live check must show a completed fictional-policy assessment with accessible findings and source references.
The live check must also confirm remote Langfuse observations.
This check does not establish held-out model quality, current regulatory coverage, or AWS acceptance.
