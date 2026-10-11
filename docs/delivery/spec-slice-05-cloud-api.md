# VS5 native assessment API

Date: 2026-10-11.
Authorization: D42 permits VS5 development within the approved AWS architecture.
Parent contracts: [Native execution](spec-slice-05-cloud-execution.md) and [release](spec-slice-05-release.md).

## Authentication and admission

Use the existing API Gateway Cognito authorizer and verified access-token claims.
Resolve the owner from the token subject.
Reject owner fields supplied in request bodies.
Authorize the case before constructing assessment or queue clients.
Keep assessment routes disabled unless trusted server configuration enables them.
Do not let a request header or body enable a route.
Keep current assessments unavailable until D20 passes.
Keep controlled local assessment routes unavailable in AWS.

Use the existing selected-assessment, report, source, review, resume, and export paths.
Validate JSON requests with the existing strict contracts.
Limit decoded request bodies to 32,000 bytes.
Save admission before sending the job to SQS.
An uncertain queue send must preserve the original admission key and job.
Return only public job fields.
Do not return execution tokens or private source references in catalog entries.

## Complete sources

Store exact original and extraction references for each selected bank document.
Do not store another expanded copy of all bank passages during admission.
Verify original bytes against the saved document hash.
Reconstruct complete model inputs from the pinned extraction.
Retain the original references when an upload is replaced.
Preserve the previously stored source format for existing assessment records.
Use 500-passage pages for source inspection.
Keep passage identifiers, locations, counts, and offsets consistent across pages.
Reject sources outside the saved snapshot.
Keep catalog entries as source metadata and obligation metadata.
Do not treat catalog entries as complete document reads.

## Reports and downloads

Keep the shared finding, review, cutoff, and export calculations.
Return a controlled error instead of truncating an oversized JSON response.
Use a private, versioned S3 artifact for cloud exports.
Keep the full export content required by the release contract.
Use a maximum export artifact size of 128,000,000 bytes.
Sign downloads for the exact object version in the configured Mumbai bucket.
Keep original document downloads scoped to the saved snapshot.
Verify the report checksum and object metadata before returning its download link.
Use a five-minute download authorization.
Do not send an access token to the storage URL.
Repeated exports cannot create model calls, jobs, or review events.
Do not log download authorizations or private response content.

## Deployment preparation

Include the historical source manifest and its referenced public files in the Lambda package.
Validate source hashes and permitted paths before packaging.
Do not package private fixtures or held-out labels.
The deployment check must include committed public source files.
Prepare SQS, its dead-letter queue, the worker, and the event-source mapping in Mumbai.
Use batch size 1 and partial batch responses.
Use a 660-second worker timeout and 3,960-second queue visibility timeout.
Use a maximum receive count of 5 before dead-letter delivery.
Keep queue contents encrypted.
D30 still prohibits reserved concurrency for the first deployment.
Prepare fixed runtime permissions through the separate bootstrap template.
Application deployment cannot change IAM policies.
Do not enable cloud assessment routes before the remaining release conditions pass.

## Acceptance checks

| Check | Required behavior |
|---|---|
| VS5-CA01 | Disabled routes and invalid Cognito claims cannot construct assessment or queue clients. |
| VS5-CA02 | Case ownership is checked before client construction. Body-supplied ownership fails strict validation. |
| VS5-CA03 | Selected admission returns a run and sends its saved job. An uncertain send keeps one admission. |
| VS5-CA04 | Current mode and controlled local routes cannot start model processing in AWS. |
| VS5-CA05 | Large bank documents use pinned references. Complete inputs remain available without duplicate expanded source storage. |
| VS5-CA06 | Replacement uploads and altered originals cannot change a saved assessment's sources. |
| VS5-CA07 | Source pages retain exact selected passage identities, locations, counts, and offsets. Unselected sources fail. |
| VS5-CA08 | Reports and review saves retain the shared revision, cutoff, ownership, and original-content rules. |
| VS5-CA09 | Resume preserves the original job, counters, and deadline. Public responses exclude execution tokens. |
| VS5-CA10 | Cloud exports contain complete report content and use exact private S3 versions. Repeats do not start processing. |
| VS5-CA11 | Download checks reject wrong scope, metadata, checksum, endpoint, or missing object versions. |
| VS5-CA12 | Invalid bodies, offsets, cutoffs, and oversized responses fail without private exception content. |
| VS5-CA13 | Packaging retains only the permitted source files and rejects changed hashes or paths. |
| VS5-CA14 | Prepared queue, worker, event mapping, and runtime policies match the approved region and permissions. |
| VS5-CA15 | Cloud download and source-page browser flows preserve authentication and complete source inspection. |

Write failing checks before implementation.
Use controlled native SDK responses without credentials, external traffic, or live inference.
These checks do not establish deployed permissions, live quality, or current regulatory completeness.
Native version comparisons, provider selection, live evaluations, and deployed acceptance remain required for the complete project.

## References and review limits

[SQS configuration](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-configure.html) defines the timeout and queue visibility conditions.
[SQS error handling](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html) defines partial batch responses.
Vocabulary review is incomplete.
Manual review must preserve ownership, uncertainty, limits, and release conditions.
