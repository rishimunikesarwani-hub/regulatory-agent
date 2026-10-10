# VS2 AWS preparation evidence

Date: 2026-10-11.
Branch: `work/t3-aws-documents`.
Status: Controlled checks passed. Live AWS acceptance remains pending.

## Specifications and failing checks

The source specification preceded storage and cloud API code.
Specification commits: `96c5928` and `6ad7494`.
`storage-red.txt` records the missing storage module before implementation.
`cloud-red.txt` records the missing cloud service module before implementation.
These import failures are module failures, not separate failures for every acceptance case.

`artifact-red.txt` records the absent extraction-artifact method.
`infrastructure-red.txt` records missing storage resources and permissions.
`browser-red.txt` records four missing AWS document-interface flows.

## Passing checks

| Evidence | Result and boundary |
|---|---|
| `python-green-v3.txt` | 204 backend checks passed. The worker has external networking disabled. |
| `browser-green-v4.txt` | 26 browser checks passed: 14 case checks, six local document checks, and six cloud protocol checks. |
| `frontend-build-v3.txt` | TypeScript checking and the Vite production build passed. |
| `template-lint-v2.json` | Both CloudFormation templates passed cfn-lint 1.57.2. |
| `runtime-policy-validation.txt` | AWS IAM Access Analyzer returned no findings for the prepared runtime identity policy. |

IAM policy validation checks the policy document. It does not apply permissions or prove live application access.
S3 transport checks use native botocore request models and controlled responses.
They inspect signed policy conditions without storing generated signed links.
Cloud service tests validate transaction parameters against the native DynamoDB model.
Their storage state is isolated from feedback databases.

## Verified failure handling

Cross-owner checks precede document storage access.
Reservations and finalization remain idempotent after service restart and a lost transaction acknowledgement.
An interleaved reservation cannot take the same final case slot.
Failed extraction cannot create a saved source or consume its extraction counters.
Saved originals and extraction artifacts use their exact S3 versions and hashes.
Every S3 response stream closes after a successful read or failure.

The default SDK signer generated a global S3 hostname despite its Mumbai Region setting.
The transfer boundary rejected that hostname.
An explicit Mumbai endpoint and virtual addressing produced the required bucket hostname.
The passing storage tests verify both settings.

A 200,000-line source produced an extraction artifact above Lambda's synchronous response limit.
The artifact stayed in S3.
The first and final API pages preserved exact locations and stayed below the response limit.
A separate test inspected every passage across a smaller source's pages.

Cloud browser checks cover direct transfer, replacement, original download, source reload, mobile page navigation, and expired access.
They also cover uncertain finalization after reload, failed-transfer resumption, and reservation cancellation.
An interrupted upload keeps its selected file until confirmation.
The earlier combined run rejected an old, fixed test-port guard.
The corrected guard checks the isolated API configured for the active slice.

## Manual review and limits

The review preserved the accepted formats, 10 MB file limit, ten-version limit, 100 extraction units, and 400,000 text bytes.
The local upload protocol stays unchanged.
The shared extraction helper now has two concrete callers.
No new dependency, generic storage interface, model call, or automatic deletion was added.
The templates limit document access to the specified Mumbai bucket and owner prefixes.
They keep CloudFront access separate from private document storage.

Live deployment is still blocked by CloudFront account verification and failed-stack recovery.
The deployed browser check now includes fictional upload, replacement, original download, and source reload.
That live check has not run because no application deployment is available.

The new storage and permission templates have not been applied to AWS.
No cloud resource was created or deleted during this preparation.
VS3 review and feedback services remain unchanged.
The complete project and live model integration remain incomplete.

The documentation received sentence-length, punctuation, and meaning-preservation review.
The dictionary and approved-meaning review remains incomplete.
Do not treat the mechanical checker as proof of full ASD-STE100 compliance.
