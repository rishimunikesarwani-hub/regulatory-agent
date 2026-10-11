# Langfuse execution tracing

Date: 2026-10-11. Source: The user's Langfuse skill and application tracing request.

This contract extends LD06 through LD08 under D57.
Metadata-only tracing remains the default.
The [D64 exception](spec-demo-details.md) permits fictional model content in explicitly enabled local runs.

## Requirements

- LF01: Create one `agent` parent for each claimed live execution. Group executions by the saved job's deterministic trace ID.
- LF02: Nest stage observations under their active processing stage or execution parent.
- LF03: Use stable operation names. Keep permitted event and stage identifiers in metadata.
- LF04: Mark model calls as `generation` and retrieval as `retriever`. Keep actual model identity and numeric token counts.
- LF05: End observations after success, failure, or interruption. End an observation even if its metadata update fails.
- LF06: Keep local audit storage mandatory. Optional tracing failures must not change assessment results or repeat model calls.
- LF07: Exclude content by default. DD01 through DD06 permit fictional model messages and responses under D64.
  Reviewer text, owner identifiers, credentials, and hidden reasoning remain excluded.
- LF08: Use an isolated OpenTelemetry provider. Export only explicit Langfuse observations.
- LF09: Flush the worker's trace queue before normal process exit. Forced process termination can prevent remote delivery.

OpenTelemetry is the library that records timed operations.
An observation is one recorded operation.
A parent observation contains its child operations.
The trace ID identifies the saved job without sending its original identifier.

## Verification

`tests/test_langfuse_tracing.py` checks hierarchy, privacy, lifecycle, disabled configuration, and failure isolation.
Tests use the installed Langfuse SDK and an in-memory exporter without external traffic.
A separate authorized smoke check sends only fictional execution metadata to the configured project.
The check retrieves the saved trace through the Langfuse CLI.
Controlled provider responses do not establish live inference quality.

## References

- [Best practices](https://langfuse.com/docs/observability/best-practices).
- [Manual observations](https://langfuse.com/docs/observability/sdk/instrumentation#manual-observations).
- [Isolated provider](https://langfuse.com/docs/observability/sdk/advanced-features#isolated-tracer-provider).

These general references recommend richer content capture.
LF07 takes precedence for this application.
