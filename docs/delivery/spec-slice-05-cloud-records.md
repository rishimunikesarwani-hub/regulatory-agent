# VS5 cloud assessment records

Date: 2026-10-11.
Authorization: D42 and the approved AWS blueprint permit native cloud integration for VS5.
Requirements: REQ-X02, REQ-X03, REQ-X04, REQ-X05, REQ-X07, and REQ-X08.
Parent: [Cloud job contract](spec-slice-05-cloud-jobs.md).
Terms: [Project glossary](../guide-ste100-writing.md#project-technical-terms).

## Native persistence

Use the existing DynamoDB job component and versioned S3 adapter in Mumbai.
Keep record bodies in private S3 storage.
Keep identities, revisions, and exact artifact references in DynamoDB.
Authorize the case owner before each read or write.
Reject altered record identities, artifact hashes, and source versions.
Use strongly consistent reads and complete query pagination.

Save immutable snapshots, selected documents, runs, and findings.
Keep one finding for each run and selected obligation.
Use a DynamoDB transaction for the finding and its unique obligation record.
Include the saved job revision in each worker transaction.
Reject a worker whose execution claim changed before the transaction.
Do not use SQLite files or a SQL parser for cloud records.

## Attempts and reviews

Save an attempt before dispatch.
Permit one transition from unknown to a terminal attempt state.
Keep terminal attempts unchanged.
If dispatch audit data is incomplete, show the live call count as Unknown.
Use the current execution claim for worker attempt changes.
Keep recovery, allowances, and deadlines under the cloud job contract.

Save review events independently of the original finding.
Use the finding revision and event identity in one DynamoDB transaction.
An identical retry returns its original event, including after later reviews.
A changed request with the same key is a conflict.
Concurrent saves at one expected revision cannot both succeed.
Keep Edited, Rejected, Approved, and pending evidence requests under the existing review rules.
Use the same calculation functions and assessment pipeline for local and cloud operation.
Keep historical cutoffs, source inspection, and exports available.

## Acceptance checks

| Check | Required behavior |
|---|---|
| VS5-CR01 | Immutable records use exact S3 references and deny conflicting replacements. |
| VS5-CR02 | Wrong owners, altered identities, and corrupted artifacts cannot read records. |
| VS5-CR03 | Strongly consistent query pagination returns the complete authorized record set. |
| VS5-CR04 | Native transaction shapes pass SDK validation. An expired execution claim cannot save a finding or attempt. |
| VS5-CR05 | One run and obligation cannot receive duplicate findings, including concurrent attempts. |
| VS5-CR06 | Attempt transitions retain audit identity and cannot replace terminal content. |
| VS5-CR07 | Review retries, conflicts, revisions, and original content meet the existing review contract. |
| VS5-CR08 | Concurrent review saves produce one event. An uncertain acknowledgement cannot add another event. |
| VS5-CR09 | Review cutoffs and aggregate calculations keep earlier outcomes and pending items. |
| VS5-CR10 | The shared pipeline completes selected obligations using native cloud records without SQLite. |
| VS5-CR11 | Partial execution keeps findings, original sources, and unchecked obligations in exports. |
| VS5-CR12 | Record bodies match their saved identities. Attempt completion cannot change the original attempt identity. |
| VS5-CR13 | Missing dispatch audit data produces an unknown count instead of zero live calls. |
| VS5-CR14 | Local attempt completion also rejects changed audit identities. |
| VS5-CR15 | Edited revisions, evidence requests, and later approval keep the original review rules. |
| VS5-CR16 | The assessment service saves native human reviews and exports the correct processing configuration. |
| VS5-CRB01 | The browser shows Unknown when the saved dispatch count is unknown. |

Write failing behavior checks before implementation.
Use controlled SDK responses without credentials, live inference, or external traffic.
Record focused results and combined regression results independently.

## Remaining integration

The cloud assessment API and SQS worker still need complete integration and acceptance checks.
Provider selection, current-source verification, live quality, and AWS acceptance remain pending.
Keep cloud assessment routes disabled until the complete integration passes.
Keep VS5 as a draft until D35 review passes.
