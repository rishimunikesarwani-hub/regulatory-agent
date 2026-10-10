# Architecture diagram verification

Date: 2026-10-10

## Request and scope

The user requested a separate copy with the architecture-diagrams skill.
The user selected Public as the diagram classification.
The [technical blueprint](../docs/architecture/02_TECHNICAL_BLUEPRINT.md) supplies the design.
No file named `earchitecture.md` exists in this project.

## Saved files

| File | Purpose |
| --- | --- |
| [Draw.io source](../docs/architecture/arch-regulatory-agent-component-v1.drawio) | Edit the shapes and connections. |
| [SVG](../docs/architecture/arch-regulatory-agent-component-v1.svg) | View the diagram. The file also contains editable diagram data. |
| [JSON specification](../docs/architecture/arch-regulatory-agent-component-v1.json) | Keep the component and flow definitions. |
| [Render script](../ops/render_drawio_architecture.py) | Generate the diagram with the installed skill. |
| [Checked image](2026-10-10-drawio-components-checked.png) | Inspect the desktop render. |
| [Audit data](2026-10-10-drawio-audit.json) | Check counts, file hashes, and source preservation. |

## Verification results

| Check | Result |
| --- | --- |
| Diagram scope | 12 components and 13 flows match the specification. |
| Original files | All seven recorded file hashes remain unchanged. |
| SVG source data | All 57 labelled elements match the Draw.io source. |
| SVG connections | All 15 connections match. Two connections belong to the legend. |
| SVG appearance | Draw.io desktop produced the complete image. All component symbols are visible. |
| Grayscale view | Labels, symbols, boundaries, and flow styles remain readable. |
| Web import | The SVG opens as separate shapes in diagrams.net. |
| Web edit | A browser label accepted a temporary edit. The edit was then undone. |
| Desktop source edit | An extracted copy accepted a label edit and rendered with the desktop command. |
| Architecture review | A separate review found no design conflicts. |

The [original hash record](2026-10-10-before-drawio-hashes.json) covers the blueprint and all six ArchView files.
The [browser image](2026-10-10-drawio-web-edit.png) shows the temporary label edit.
The [desktop test copy](2026-10-10-drawio-roundtrip-edit.drawio) contains the same test edit.
The delivered diagram contains no test edit.
Desktop editing through the graphical interface was not tested.

## Design retained

- Use the external regulatory retrieval API. Provider selection remains undecided.
- Refresh regulatory sources before selection. Verify selected versions when the worker starts.
- Stop the assessment if verification fails or selected versions change.
- Use S3 regulatory copies as historical evidence.
- Keep one bounded agent, 24 model calls, and a 600-second deadline.
- Verify model access and destinations before private uploads.
- Keep the application and private data in Mumbai.
- Do not add a crawler or an independent reviewer role.

The diagram shows planned components. It does not identify deployed AWS resources.
HTTPS port 443 is the intended transport. Live connections remain unverified.
The zones show responsibility and trust. They do not specify VPCs or subnets.
The title block marks the design as not implemented and the human review as pending.

## Render correction

Three icon mappings required correction against the installed Draw.io library.
The script applies local mappings for S3, SQS, and the operator device.
It uses official AWS symbols for AWS components.
The undecided provider uses a neutral server symbol.
The shared skill files remain unchanged.

## Language review

Applied short sentences, direct instructions, and consistent technical terms.
The local ASD-STE100 check covers sentence length and selected writing rules.
The [check result](2026-10-10-drawio-ste-check-v2.json) has zero findings for this record and the new log entry.
It does not prove complete dictionary compliance.
Full dictionary compliance remains unverified.

## Implementation status

This work adds a diagram copy and verification records.
Application implementation, model evaluation, and AWS deployment remain pending.
