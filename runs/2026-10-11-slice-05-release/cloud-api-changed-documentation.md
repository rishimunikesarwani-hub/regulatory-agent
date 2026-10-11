
## D53 - Native assessment API and deployment preparation

Date: 2026-10-11.
Status: Implementation clarification within D42 and the approved AWS blueprint.
Requirements: REQ-X02, REQ-X03, REQ-X05, REQ-X07, and REQ-X08.

The [cloud API contract](../delivery/spec-slice-05-cloud-api.md) connects authenticated native admission, reports, review records, source pages, and private downloads.
Case ownership is checked before assessment client construction.

Native bank source records keep pinned original and extraction references.
Internal processing reads all verified passages.
Public source inspection uses stable passage identifiers and pages.
Reports use private, versioned S3 objects with checksum verification before download signing.

The deployment package contains application code and verified public source files.
The package excludes private fixtures and unrelated source files.
Previous packages remain in a private archive.

The SAM template prepares encrypted queues, a dead-letter queue, and a bounded Lambda worker.
The bootstrap template defines fixed runtime roles and scoped resource permissions.
Assessment deployment remains disabled by default.
The frontend supports selected cloud assessments behind that release flag.
D30 still prohibits reserved concurrency for the first deployment.

W14 records deadline or lease exhaustion during renewal as timeout.
The correction preserves saved deadlines, counters, and replacement-claim protection.

Controlled SDK and browser checks do not establish deployed AWS permissions or live model quality.
CloudFormation schema and security validation remain pending tool approval.
Native version comparisons, provider selection, source verification, live evaluations, and deployed acceptance remain required.
AWS authentication and CloudFront acceptance remain pending.
VS5 remains a draft under D35.



The [cloud API component](spec-slice-05-cloud-api.md) now prepares authenticated assessment routes, source pages, reviews, and private report downloads.
Pinned source references avoid duplicate expanded bank records.

Verified public source files enter the deployment package.
Queue resources, a conditional worker, and fixed runtime permissions are prepared.
Cloud assessment deployment remains disabled by default.

Template schema and security validation remain pending tool approval.
Native version comparisons, source verification, live evaluations, and deployed acceptance remain required.


D53 prepares an additional worker role and narrower queue permissions.
These template changes are not installed.
Current schema and security validation remain pending.


| `regulatory-agent-dev-case-runtime` role | Reads and writes owned development records and document objects. Sends assessment queue messages. Writes application logs in Mumbai. |
| `regulatory-agent-dev-assessment-worker` role, prepared | Processes saved jobs with scoped storage, queue, log, and model permissions. Uses the specified India inference profile. |

The revised template permits CloudFormation to pass only the fixed case and assessment worker roles to Lambda.

The case role has no model or IAM modification permissions.
The prepared worker role permits only the specified inference profile and its Mumbai and Hyderabad model resources.

Earlier case and document templates passed `cfn-lint 1.57.2` without findings.

The case role test excludes model and IAM modification actions.

Ten selected AWS Guard rules ran against earlier templates with `cfn-guard 3.2.1`.

CloudFormation reported no pre-deployment validation errors for the earlier installed setup.


The [cloud API component](spec-slice-05-cloud-api.md) prepares authenticated routes, private reports, source pages, verified public packaging, and conditional worker resources.
The deployment flag defaults to disabled.
Template validation, native version comparisons, provider verification, live evaluations, and deployed acceptance remain unfinished.



## 2026-10-11 - Native assessment API and deployment preparation

The cloud API connects native selection, job reports, human reviews, source pages, and private report downloads.
Large bank documents use pinned source references instead of duplicate expanded records.

The deployment package includes verified public sources and preserves previous packages in a private archive.
Conditional queues, a Lambda worker, and fixed runtime permissions are prepared.
Cloud assessment deployment remains disabled by default.
The frontend supports selected cloud assessments, source pagination, and private artifact downloads behind that flag.

The 18 focused backend checks and three controlled cloud browser checks pass.
W14 reproduces deadline exhaustion during lease renewal.
The correction preserves timeout classification, the original deadline, counters, and replacement-claim protection.
D53 records the component boundary and remaining validation, comparison, provider, quality, and deployed acceptance conditions.
