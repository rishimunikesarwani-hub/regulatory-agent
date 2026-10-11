# Native assessment API and deployment preparation review

Date: 2026-10-11.
Contract: [Native cloud API](../../docs/delivery/spec-slice-05-cloud-api.md).

## Verified behavior

The first checks reproduced missing cloud routes and oversized duplicate bank source records.
Additional checks reproduced missing deployment packaging and missing native report operations.
Destination checks reproduced URLs with credentials and nonstandard ports.
An earlier full-source record reproduced a missing original download reference.
The corrections preserve source versions, complete internal reads, and private downloads.

Case ownership is checked before assessment client construction.
Uncertain queue acknowledgements preserve one admission and its retry identity.
Source inspection uses stable passage identifiers and pages.
The complete report includes all source passages at the selected cutoff.
Report signing verifies the exact S3 version, size, encryption, and checksum.

The package excludes private fixtures and unrelated source files.
It verifies each public source hash before replacing the package.
Previous packages remain in a private archive.
A relocated package loads the actual historical source catalog.

The SAM and bootstrap templates prepare encrypted queues, bounded execution, and fixed runtime permissions.
The deployment flag defaults to disabled.
Structural checks do not replace CloudFormation schema or security validation.

All 54 browser checks pass.
The three new cloud browser checks use controlled protocol responses.
They verify the disabled default, selected assessment flow, source pages, and private downloads without bearer tokens.
The frontend build passes.
Desktop and source-dialog screenshots were inspected.

## Verification limits

The first complete backend run used the integration environment instead of the slice environment.
That environment lacked the PDF test dependency.
An older role assertion also excluded the newly specified SQS permission.
The corrected role assertion retains exact resource restrictions.
All 13 worker checks pass in the slice environment.

The next complete run passed 360 checks and found a missing download method in the earlier-format test double.
The corrected test verifies the exact original reference passed to the download adapter.
All 18 focused API checks pass.

The next complete run reproduced a deadline race during lease renewal.
W14 reproduces that classification failure with a controlled renewal error.
The correction classifies deadline or lease exhaustion as timeout.
Replacement claims still prevent stale finalization.
The final complete backend run passed all 362 checks in 180.400 seconds.

Exact-commit GitHub verification passed the backend and build checks but failed one browser check.
A concurrent completion occurred after the default cutoff was sampled.
The resulting report hid a finding that its record read already returned.
CA16 reproduces this ordering failure.
The default cutoff now follows the record read.
Explicit historical cutoffs remain unchanged.
The corrected complete local run passed 363 backend checks in 227.216 seconds.
All 54 browser checks and 19 focused API checks also passed.

CloudFormation schema and security validation remain pending tool availability or installation approval.
No AWS deployment, account mutation, provider integration, or live inference occurred during this work.
These checks do not establish live permissions, hosted worker behavior, complete regulatory coverage, or model quality.
Native version comparisons, provider selection, source verification, live evaluations, and deployed acceptance remain required.
VS5 remains a draft under D35.
