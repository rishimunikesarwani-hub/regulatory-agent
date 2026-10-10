# VS2 AWS document preparation

Date: 2026-10-11.
Status: Controlled integration complete. Live deployment and AWS acceptance remain pending.

## Prepared behavior

The cloud API authorizes each case through the existing Cognito access-token checks.
The browser sends file bytes directly to private S3 storage in Mumbai.
The API receives upload metadata and gives temporary transfer permission.
Each permission fixes the object key, file length, content type, and encryption setting.
The approved 10 MB file limit stays unchanged.

The upload record keeps the original S3 version identifier and content hash.
Extraction uses the same bounded parser as local uploads.
One conditional DynamoDB transaction saves source metadata and case counters together.
Repeated finalization keeps one saved document version.
Cancellation releases an unfinished reservation without deleting stored objects.

The source interface shows at most 500 passages per page in AWS mode.
Its page controls give access to every extracted passage.
Exact locations, passage identifiers, source versions, and earlier originals stay unchanged.
Original downloads use authorized links for the saved S3 version.
Signed links stay out of tracked evidence and operational logs.

## Isolation and checks

Branch: `work/t3-aws-documents`.
Worktree: `.worktrees/regulatory-agent-t3-aws-documents`.
Web test port: `5192`. API test port: `8191`.
Browser database: `runs/private/slice-02-aws/browser-tests.sqlite`.
Ports `5192` and `8190` remain reserved for future feedback services.
No feedback services are running from this worktree.
The VS3 review services remain available at `http://127.0.0.1:5183/`.

Run these checks from this worktree:

```powershell
.venv/Scripts/python.exe ops/check.py
npm --prefix src/web run build
npm --prefix src/web test -- --config playwright.aws-documents.config.ts
uvx --python 3.12.13 cfn-lint ops/sam-dev.yaml ops/aws-development-bootstrap.yaml
```

The browser configuration starts and stops its isolated test servers.
It rejects a different configured test API before local document writes.
The cloud browser checks use controlled responses for Cognito, the API, and S3.
These checks do not establish live sign-in or live cloud storage behavior.
Read the [evidence receipt](../../runs/2026-10-11-slice-02-aws-documents/review-cloud-preparation.md).

## Deployment prerequisites

The development stack remains `ROLLBACK_COMPLETE` after the CloudFront account-verification failure.
Follow the [verification guide](guide-aws-cloudfront-verification.md) for the manual AWS Support request.
The user chose to keep CloudFront while AWS verification is pending.
This session has not sent that request.
Failed-stack recovery needs a separate review before any deletion.

The prepared access template adds document storage permissions to the fixed runtime role.
Its permissions cover the specified Mumbai bucket and owner prefixes.
It grants no object deletion or model invocation.
The deployment role can upload public frontend assets and deployment packages.
It has no application document-object grant.
These permission changes have not been applied to AWS.

The application template defines a retained, encrypted, private, versioned document bucket.
It permits browser transfers only from the configured CloudFront origin.
Its bucket policy denies HTTP traffic and uploads without the required encryption setting.
The function has 512 MB memory and a 29-second timeout for bounded extraction.
Storage observability activation and live permission checks remain pending.

Keep the USD 25 monthly budget alerts.
The alerts do not stop spending.
Stored versions and repeated storage requests can incur charges.
Private bank uploads remain disabled until the approved India checks pass.

## Current acceptance boundary

VS2 local acceptance and its integration merge are complete.
VS3 remains in its separate review branch.
Do not merge VS3 or start VS4 before the pending user review.
The AWS document branch merged through PR10 after its GitHub checks passed.
The integrated commit is `a53eb94d92aecddda640ffece5c128877ecf75ff`.
It has not been deployed.
Live AWS upload, source inspection, replacement, and download acceptance remain pending.

## References

- [Cloud source specification](spec-slice-02-aws-documents.md) defines routes and acceptance cases.
- [DynamoDB transaction permissions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis-iam.html) use the permissions for each underlying item operation.
- [S3 security guidance](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html) covers private access, encryption, versioning, and role permissions.
