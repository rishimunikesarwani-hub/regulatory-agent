# VS5 bounded Bedrock model adapter

Date: 2026-10-11.
Authorization: D42 permits local VS5 development.
Requirements: REQ-F03–REQ-F08, REQ-X01, REQ-X02, REQ-X08, and T4–T8.
Parent contract: [VS5 release](spec-slice-05-release.md).

A model adapter connects the existing worker interface to the selected model API.
This adapter does not complete the assessment worker or establish model quality.
Keep the five permitted model actions.
Add extracted obligations and controls to their structured outputs.
Keep owners and frequencies nullable.
Keep the existing controlled response label as its default.
Label an actual provider response Live.
Save numeric token usage and the provider request identifier when available.
Do not invent the actual response model identifier when the API does not return it.

## Dispatch requirements

Use `bedrock-runtime` Converse in Mumbai with `in.openai.gpt-5.6-luna`.
Reject other runtime endpoints, Regions, model profiles, and inactive profiles.
Check the profile's destination model ARNs before inference.
An ARN is an AWS resource identifier.
Permit only the selected foundation model in `ap-south-1` and `ap-south-2`.
Keep private processing disabled until the separate privacy checks pass.
The initial adapter permits synthetic snapshots only.

Authorize the case and saved job before provider access.
Use the saved snapshot as the source and obligation allowlist.
Reject caller-supplied model routing or arbitrary provider request fields.
Set an explicit output-token limit.
Use the native SDK request schema for structured JSON output.
Keep a strict local output validator after the provider response.
Treat source text as evidence, not instructions or tool permissions.
Return no model reasoning blocks or raw provider response in the application result.

Disable SDK inference retries with `total_max_attempts=1`.
Reserve the saved model-call allowance before each inference dispatch.
Count failed, malformed, rejected, timed-out, and uncertain dispatched calls.
Keep available numeric usage and request identifiers on failed responses.
Keep the allowance unchanged when authentication, profile verification, or local request validation prevents inference.
Application retries must reserve another call.
Reject a late response after the saved job deadline.
The complete worker must enforce its wall-clock deadline independently.
Do not claim that socket timeouts alone enforce that deadline.

Accept only a complete text response with `end_turn`.
Reject truncated responses, blocked responses, tool instructions, invalid JSON, and actions outside the selected snapshot.
Reject citations to source versions outside the snapshot.
Resolve citation version IDs through the saved records for the selected source versions.
Keep source/version lookup keys separate from saved document version IDs.
Leave exact passage and contextual-support validation to the assessment pipeline before persistence.
Never put prompts, returned content, or provider error messages in operational logs.
Return safe error identifiers.

## Acceptance checks

| Check | Required behavior |
|---|---|
| VS5-MT01 | The native Converse request uses the pinned profile, explicit token limit, strict output schema, and one reserved call. |
| VS5-MT02 | A successful response keeps extracted objects, nullable fields, numeric usage, request ID, and Live status. |
| VS5-MT03 | Missing usage remains unknown. Reasoning content is not returned. |
| VS5-MT04 | Malformed output and outside-snapshot source, obligation, or citation IDs consume the dispatched call and fail safely. |
| VS5-MT05 | Provider rejection, timeout, truncation, and unknown outcomes do not trigger hidden retries. |
| VS5-MT06 | Wrong owner, inactive profile, non-India destinations, and unverified private input prevent inference. |
| VS5-MT07 | Expired deadlines and exhausted allowances prevent dispatch. A late response cannot become a valid result. |
| VS5-MT08 | Forbidden request fields and oversized input fail before provider access. Controlled responses remain compatible. |
| VS5-MT09 | Citations use selected saved document IDs. Unselected IDs and substituted lookup keys fail. |
| VS5-MT10 | Client configuration cannot change Regions, endpoints, retry counts, or bounded socket timeouts. |

Save failing checks before adapter implementation.
Use native SDK clients with fake credentials and SDK response stubs for default checks.
Keep real account credentials outside tests.
Run the existing backend suite after the shared contract changes.

## Live prerequisites and limits

The current AWS login session has expired.
Renew authentication before live profile, permissions, logging, and synthetic-inference checks.
Install the SDK's `crt` extra for profiles created through `aws login`.
Keep the existing locked package versions when adding this required dependency.
The CLI version is `2.37.12`.
The installed boto3 version is `1.43.111`.
SDK inspection confirmed the native Converse `outputConfig.textFormat.structure.jsonSchema` request shape.

The [AWS model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-56-luna.html) documents Converse and the India inference profile.
The [Converse reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) controls request and response fields.
Do not interpret documentation or stubbed responses as live account access or model-quality evidence.
CloudFront verification still blocks the application deployment.
Current-source verification and provider selection remain separate unfinished conditions under D20.
