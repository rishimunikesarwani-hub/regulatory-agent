# Fictional demo content and batch uploads

Date: 2026-10-11. Source: The user's trace screenshot and multiple-document request.

D64 permits model input and output in Langfuse for explicitly enabled fictional local runs.
This exception replaces LD06, LD07, and LF07 only within the conditions below.
All other runs keep metadata-only tracing.

## Requirements

- DD01: Enable content capture only with `APP_ENV=local` and `LANGFUSE_CAPTURE_CONTENT=fictional-local`.
- DD02: Capture only historical, synthetic snapshots whose saved model provider is OpenAI.
- DD03: Record the actual model messages, selected context, prompt version, response schema, and assistant response on the existing generation.
- DD04: Exclude credentials, HTTP headers, owner identifiers, reviewer text, provider error bodies, and hidden reasoning.
- DD05: Keep audit records metadata-only. Optional capture failures must not change results or repeat model requests.
- DD06: Keep existing saved traces unchanged. Show the active capture setting in the local application.
- DD07: Allow multiple selected files for new sources. Apply the selected document role to each file.
- DD08: Keep the 10 MB file limit and 10-version case limit. Allow only one replacement file at a time.
- DD09: Save files in sequence through the existing local or AWS upload flow. Give each cloud upload its own idempotency key.
- DD10: Stop the batch after the first failure. Keep confirmed files and report the remaining selected files.
- DD11: Block another upload after an uncertain result until the user confirms the saved versions or upload status.
- DD12: Make every confirmed source available for assessment selection. Keep earlier versions and original bytes unchanged.

An idempotency key identifies one cloud upload request across retries.
A batch is the selected group of files.
Content capture sends fictional model messages to the configured Langfuse project region.
The setting does not authorize private bank data or AWS content capture.

## Acceptance

`tests/test_langfuse_tracing.py` checks content capture, disabled conditions, failure isolation, and audit privacy.
`src/web/tests/documents.spec.ts` checks batch upload, case limits, replacements, and partial failures.
A separate live fictional run must show input and output through remote Langfuse readback.
Software success does not establish model quality or AWS acceptance.
