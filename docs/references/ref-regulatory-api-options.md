# Regulatory API options for D20

Research date: 2026-10-11.
Authorization: The user selected research of RBI-source API options during VS5 development.
Status: Provider selection remains pending.

## Findings

The official [RBI RSS documentation](https://www.rbi.org.in/Scripts/rss.aspx) describes update headlines and summaries linked to full documents.
RSS is useful for discovery.
It does not provide full-text completeness or amendment verification by itself.

The RBIH [Unified Lending Interface](https://rbihub.in/projects/unified-lending-interface) page describes land records, credit data, and verification services.
The [ULI service catalog](https://docs.rbihub.in/unified-lending-interface/services) also describes lending services.
Neither source establishes an API for regulatory texts.
The earlier `rbih.tech/docs/intro` reference has unverified affiliation.
Do not use that earlier URL as authority evidence.

The [Jina Reader documentation](https://jina.ai/reader/) describes URL-to-text retrieval and JSON output.
It provides options to bypass cached content and respect source-site robot rules.
This is a retrieval service, not a regulatory authority or a complete amendment register.
Public RBI URLs can be examined without sending private case content.
The anonymous endpoint permits a public-only prototype without purchasing access.
Provider pricing, terms, limits, and operational coverage need verification before release.

The [India regulatory MCP project](https://github.com/Akhilgovind02/india-regulatory-mcp) describes a local scraped RBI and SEBI collection.
Its repository is evidence of its implementation proposal.
It does not establish a hosted external API, complete current coverage, or validated amendment history.
This research did not install or run that project.

## Candidate comparison

| Candidate | Available evidence | D20 condition still missing |
|---|---|---|
| Official RBI RSS | Official discovery feed with links to documents. | Full-text API, complete source scope, versions, and amendment verification. |
| RBIH APIs | Documented services for financial and verification functions. | A demonstrated regulatory-text endpoint. |
| Jina Reader with official RBI sources | A public historical page returned JSON and relevant passages in one probe. | Complete scope checks, authoritative version checks, amendment history, terms, and operational reliability. |
| Local regulatory MCP collection | Public source-code proposal for scraped regulatory retrieval. | Hosted external service, complete coverage, and current-source verification. |

## Public transport probe

The [probe receipt](../../runs/2026-10-11-slice-05-release/provider-probe.json) records one anonymous Jina Reader request.
The target was the saved public RBI IT direction URL.
The response returned HTTP `200`, JSON, and `66,305` text characters.
Checks found the expected title, privileged-access passage, and backup passage.

The request contained no private case content.
The request bypassed cached content and requested source-site robot-rule checks.
The research saved response metadata, not private source content.

This probe does not establish complete text, current applicability, amendment coverage, version history, or a source freshness result.
Its duration is one observation, not a latency percentile or reliability measurement.
The application still blocks current assessments.

## Recommendation and next verification

Use Jina Reader only as a candidate for a public-source prototype.
Keep RBI documents as the authority.
Do not interpret a provider fetch time as proof of regulatory currency.

Review the complete selected regulation and its authoritative amendment references.
Compare returned content with the complete official source.
Reject missing text, stale copies, redirects outside the permitted domains, and changed selected versions.
Record the permitted source scope, coverage limits, publication dates, effective dates, checks, and preserved source versions.

Make provider selection explicit before application integration.
Keep private case data outside the regulatory API.
Keep current assessments blocked until the complete verification contract passes.
