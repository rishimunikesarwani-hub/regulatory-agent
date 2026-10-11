# The Regulator assessment report

## Export status

> Assessment export · Simulated processing · Fictional bank data

## Snapshot and selected versions

> \{
>   "assessment\_date": "2024-04-08",
>   "bank\_profile": \{
>     "name": "Fictional export bank 1791726558122"
>   \},
>   "case\_id": "fc1644fda3c945cea77d280594cec543",
>   "mode": "historical",
>   "model\_version": "in.openai.gpt-5.6-luna",
>   "prompt\_version": "controlled-vs3-v1",
>   "selected\_document\_ids": \{\},
>   "selected\_obligations": \[
>     "RBI-IT-19b"
>   \],
>   "selected\_versions": \{
>     "RBI-IT-2023": "2023-11-07",
>     "ad73bdc9377f424885678a03384012d0": "1"
>   \},
>   "snapshot\_id": "69abe4ae7cb65fb49f20d00749b17477",
>   "synthetic": true
> \}

## Cohort filters and time bases

> \{
>   "kind": "single\_assessment",
>   "case\_id": "fc1644fda3c945cea77d280594cec543",
>   "run\_id": "69abe4ae7cb65fb49f20d00749b17477",
>   "snapshot\_id": "69abe4ae7cb65fb49f20d00749b17477",
>   "model\_id": "in.openai.gpt-5.6-luna",
>   "prompt\_version": "controlled-vs3-v1",
>   "data\_mode": "controlled\_simulation",
>   "recommendation\_availability": \{
>     "through": "2026-10-11T13:49:20.091758\+00:00",
>     "end\_inclusive": true
>   \},
>   "runtime\_selection": \{
>     "job\_id": "404662b58d1e42f28b70637b8218bda5",
>     "job\_admitted\_at": "2026-10-11T13:49:19.164551\+00:00",
>     "job\_state\_time\_basis": "observed\_current\_state"
>   \}
> \}

## Observed job state

> \{
>   "authority\_verified\_at": null,
>   "case\_id": "fc1644fda3c945cea77d280594cec543",
>   "created\_at": 1791726559.164551,
>   "deadline": 1791727159.1965497,
>   "finished\_at": 1791726559.5094047,
>   "freshness": "unverified",
>   "job\_id": "404662b58d1e42f28b70637b8218bda5",
>   "label": "Simulated",
>   "model\_calls": 1,
>   "retrieval\_calls": 0,
>   "snapshot\_id": "69abe4ae7cb65fb49f20d00749b17477",
>   "stage": "persistence",
>   "started\_at": 1791726559.1965497,
>   "state": "completed",
>   "stop\_reason": null,
>   "unchecked\_obligations": \[\]
> \}

## Report cutoff

> 2026-10-11T13:49:20.091758\+00:00

## Freshness and authority verification

> \{
>   "freshness": "unverified",
>   "authority\_verified\_at": null
> \}

## Obligation

> \{
>   "obligation\_id": "RBI-IT-19b",
>   "requirement": "Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed.",
>   "conditions": \[
>     "Personnel with elevated system access entitlements.",
>     "Applicability to the listed regulated entities must be established."
>   \],
>   "exceptions": \[
>     "Local Area Banks",
>     "NBFC-Core Investment Companies"
>   \],
>   "applicability": "Unverified for this fictional bank profile.",
>   "citations": \[
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "passage\_id": "RBI-IT-2023:2023-11-07:19b",
>       "location": "Clause 19(b)",
>       "quote": "Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "passage\_id": "RBI-IT-2023:2023-11-07:2ai",
>       "location": "Clause 2(a)(i)",
>       "quote": "all Banking Companies 1 , Corresponding New Banks and State Bank of India as defined under subsections (c), (da) and (nc) of section 5 of the Banking Regulation Act, 1949 (collectively referred to as ‘commercial banks’ hereinafter)."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "passage\_id": "RBI-IT-2023:2023-11-07:2b",
>       "location": "Clause 2(b)",
>       "quote": "These Directions shall not be applicable to: Local Area Banks NBFC-Core Investment Companies"
>     \}
>   \]
> \}

## Mapped control

> \{
>   "control\_id": "ACCESS-01",
>   "statement": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.",
>   "purpose": "Privileged session oversight",
>   "owner": null,
>   "frequency": "Weekly under the fictional bank policy.",
>   "citations": \[
>     \{
>       "document\_version\_id": "1500b0a7be9b48bdb1daa375e520de7f",
>       "passage\_id": "1500b0a7be9b48bdb1daa375e520de7f-2",
>       "location": "Line 2",
>       "quote": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>     \}
>   \]
> \}

## Selected obligations

> \[
>   \{
>     "obligation\_id": "RBI-IT-19b",
>     "requirement": "Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed.",
>     "conditions": \[
>       "Personnel with elevated system access entitlements.",
>       "Applicability to the listed regulated entities must be established."
>     \],
>     "exceptions": \[
>       "Local Area Banks",
>       "NBFC-Core Investment Companies"
>     \],
>     "applicability": "Unverified for this fictional bank profile.",
>     "citations": \[
>       \{
>         "document\_version\_id": "RBI-IT-2023:2023-11-07",
>         "passage\_id": "RBI-IT-2023:2023-11-07:19b",
>         "location": "Clause 19(b)",
>         "quote": "Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed."
>       \},
>       \{
>         "document\_version\_id": "RBI-IT-2023:2023-11-07",
>         "passage\_id": "RBI-IT-2023:2023-11-07:2ai",
>         "location": "Clause 2(a)(i)",
>         "quote": "all Banking Companies 1 , Corresponding New Banks and State Bank of India as defined under subsections (c), (da) and (nc) of section 5 of the Banking Regulation Act, 1949 (collectively referred to as ‘commercial banks’ hereinafter)."
>       \},
>       \{
>         "document\_version\_id": "RBI-IT-2023:2023-11-07",
>         "passage\_id": "RBI-IT-2023:2023-11-07:2b",
>         "location": "Clause 2(b)",
>         "quote": "These Directions shall not be applicable to: Local Area Banks NBFC-Core Investment Companies"
>       \}
>     \]
>   \}
> \]

## Extracted controls

> \[
>   \{
>     "control\_id": "ACCESS-01",
>     "statement": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.",
>     "purpose": "Privileged session oversight",
>     "owner": null,
>     "frequency": "Weekly under the fictional bank policy.",
>     "citations": \[
>       \{
>         "document\_version\_id": "1500b0a7be9b48bdb1daa375e520de7f",
>         "passage\_id": "1500b0a7be9b48bdb1daa375e520de7f-2",
>         "location": "Line 2",
>         "quote": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>       \}
>     \]
>   \}
> \]

## Original findings and recommendation IDs

> \[
>   \{
>     "finding\_id": "dbc62fcd0fad5e648e326d99aee54e9b",
>     "snapshot\_id": "69abe4ae7cb65fb49f20d00749b17477",
>     "obligation\_id": "RBI-IT-19b",
>     "control\_ids": \[
>       "ACCESS-01"
>     \],
>     "status": "needs\_review",
>     "evidence\_condition": "missing",
>     "citations": \[
>       \{
>         "document\_version\_id": "RBI-IT-2023:2023-11-07",
>         "passage\_id": "RBI-IT-2023:2023-11-07:19b",
>         "location": "Clause 19(b)",
>         "quote": "Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed."
>       \},
>       \{
>         "document\_version\_id": "1500b0a7be9b48bdb1daa375e520de7f",
>         "passage\_id": "1500b0a7be9b48bdb1daa375e520de7f-2",
>         "location": "Line 2",
>         "quote": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>       \}
>     \],
>     "rationale": "Controlled example. The policy states a control, but this example has no verified operational evidence. Applicability and activity records need human review.",
>     "remedy": "Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.",
>     "gap\_kind": "evidence",
>     "applicability\_reason": null,
>     "claims": \[\],
>     "run\_id": "69abe4ae7cb65fb49f20d00749b17477",
>     "primary\_recommendation": "Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.",
>     "available\_at": "2026-10-11T13:49:19.482288Z",
>     "model\_id": "in.openai.gpt-5.6-luna",
>     "prompt\_version": "controlled-vs3-v1",
>     "data\_mode": "controlled\_simulation",
>     "source\_version\_ids": \[
>       "RBI-IT-2023:2023-11-07",
>       "ad73bdc9377f424885678a03384012d0:1"
>     \]
>   \}
> \]

## Saved review events

> \[
>   \{
>     "event\_kind": "final\_review",
>     "disposition": "approved",
>     "accepted\_content": \{
>       "status": "needs\_review",
>       "rationale": "Controlled example. The policy states a control, but this example has no verified operational evidence. Applicability and activity records need human review.",
>       "recommendation": "Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews."
>     \},
>     "reason": null,
>     "expected\_revision": 0,
>     "idempotency\_key": "0fdf59f2-b5d6-487a-9e14-38b54913d7bc",
>     "event\_id": "e185a55d0384438dbe4ef4ce510c5d2b",
>     "finding\_id": "dbc62fcd0fad5e648e326d99aee54e9b",
>     "reviewer\_id": "slice-05-tests",
>     "committed\_at": "2026-10-11T13:49:20.054623Z",
>     "revision": 1
>   \}
> \]

## Review summary

metric_definition_version: d24-v1

cutoff: 2026-10-11T13:49:20.091758+00:00

data_mode: controlled_simulation

run_id: 69abe4ae7cb65fb49f20d00749b17477

eligible: 1

reviewed: 1

pending: 0

approved: 1

edited: 0

rejected: 0

approval_rate: 1.0

edit_rate: 0.0

rejection_rate: 0.0

adoption_rate: 1.0

review_coverage: 1.0

## Recorded runtime

cost: Unknown

> \{
>   "run\_id": "69abe4ae7cb65fb49f20d00749b17477",
>   "attempts": \[
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[\],
>       "attempt\_id": "b7ed145e3f02464ab92508e057f95d5a",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "3befd4c290c5436cbc91b72177db06d6",
>       "finished\_at": "2026-10-11T13:49:19.461305Z",
>       "first\_token\_seconds": null,
>       "job\_id": "404662b58d1e42f28b70637b8218bda5",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "stage": "validation",
>       "stage\_id": "validation",
>       "started\_at": "2026-10-11T13:49:19.461305Z",
>       "state": "succeeded",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \},
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[\],
>       "attempt\_id": "caafadeb14fe46f183832ccb60e7eb31",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "43f64eacb5c442e8abfc767c370256ac",
>       "finished\_at": "2026-10-11T13:49:19.368423Z",
>       "first\_token\_seconds": null,
>       "job\_id": "404662b58d1e42f28b70637b8218bda5",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "selected\_passage\_ids": \[
>         "RBI-IT-2023:2023-11-07:19b",
>         "RBI-IT-2023:2023-11-07:2ai",
>         "RBI-IT-2023:2023-11-07:2b",
>         "1500b0a7be9b48bdb1daa375e520de7f-2"
>       \],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "stage": "context\_selection",
>       "stage\_id": "context\_selection",
>       "started\_at": "2026-10-11T13:49:19.368423Z",
>       "state": "succeeded",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \},
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[\],
>       "attempt\_id": "dfd0987c7d954a959faebec3909cd7eb",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.01600000000325963,
>       "errors": \[\],
>       "event\_id": "70c50d24bf9841329ea49972723cb322",
>       "finished\_at": "2026-10-11T13:49:19.488294Z",
>       "first\_token\_seconds": null,
>       "job\_id": "404662b58d1e42f28b70637b8218bda5",
>       "model\_id": null,
>       "operation": "storage",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "stage": "persistence",
>       "stage\_id": "persistence",
>       "started\_at": "2026-10-11T13:49:19.480288Z",
>       "state": "succeeded",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \},
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[\],
>       "attempt\_id": "ae8fb736c80c4dac9c1706fdecdd1d28",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.062000000005355105,
>       "errors": \[\],
>       "event\_id": "72ee1c08c3234d4c874bd1b82333a50b",
>       "finished\_at": "2026-10-11T13:49:19.443108Z",
>       "first\_token\_seconds": null,
>       "job\_id": "404662b58d1e42f28b70637b8218bda5",
>       "model\_id": "in.openai.gpt-5.6-luna",
>       "operation": "model",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "stage": "model\_call",
>       "stage\_id": "model\_call",
>       "started\_at": "2026-10-11T13:49:19.384494Z",
>       "state": "succeeded",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \},
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[\],
>       "attempt\_id": "4f162d9f109840fe81a052d5cfc1a42c",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.030999999988125637,
>       "errors": \[\],
>       "event\_id": "8296317cd45c4b82a79b5fba728e27f2",
>       "finished\_at": "2026-10-11T13:49:19.237550Z",
>       "first\_token\_seconds": null,
>       "job\_id": "404662b58d1e42f28b70637b8218bda5",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "stage": "source\_verification",
>       "stage\_id": "source\_verification",
>       "started\_at": "2026-10-11T13:49:19.204558Z",
>       "state": "succeeded",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \},
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[
>         "e185a55d0384438dbe4ef4ce510c5d2b"
>       \],
>       "attempt\_id": "10bfe20728c342c38d2e62cac865850c",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "a5d48a9cbc224a96bb8b041abc6d042f",
>       "finished\_at": "2026-10-11T13:49:20.061621Z",
>       "first\_token\_seconds": null,
>       "job\_id": "404662b58d1e42f28b70637b8218bda5",
>       "model\_id": null,
>       "operation": "storage",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "stage": "review\_event",
>       "stage\_id": "review\_event",
>       "started\_at": "2026-10-11T13:49:20.052626Z",
>       "state": "succeeded",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \},
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[\],
>       "attempt\_id": "59374b453aed40898841323d18370ee1",
>       "candidate\_passage\_ids": \[
>         "RBI-IT-2023:2023-11-07:2a",
>         "RBI-IT-2023:2023-11-07:2ai",
>         "RBI-IT-2023:2023-11-07:2b",
>         "RBI-IT-2023:2023-11-07:19a",
>         "RBI-IT-2023:2023-11-07:19b",
>         "RBI-IT-2023:2023-11-07:19c",
>         "RBI-IT-2023:2023-11-07:29a",
>         "RBI-IT-2023:2023-11-07:29b",
>         "RBI-IT-2023:2023-11-07:29e",
>         "1500b0a7be9b48bdb1daa375e520de7f-1",
>         "1500b0a7be9b48bdb1daa375e520de7f-2",
>         "1500b0a7be9b48bdb1daa375e520de7f-3"
>       \],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "b6602fdaacf6428ca76a7ba3b701c442",
>       "finished\_at": "2026-10-11T13:49:19.330966Z",
>       "first\_token\_seconds": null,
>       "job\_id": "404662b58d1e42f28b70637b8218bda5",
>       "model\_id": null,
>       "operation": "retrieval",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "selected\_passage\_ids": \[
>         "RBI-IT-2023:2023-11-07:19b",
>         "RBI-IT-2023:2023-11-07:2ai",
>         "RBI-IT-2023:2023-11-07:2b",
>         "1500b0a7be9b48bdb1daa375e520de7f-2"
>       \],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "stage": "retrieval",
>       "stage\_id": "retrieval",
>       "started\_at": "2026-10-11T13:49:19.330966Z",
>       "state": "succeeded",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \},
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[
>         "1500b0a7be9b48bdb1daa375e520de7f"
>       \],
>       "attempt\_id": "378ee7c836c040809d527319842ff22c",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": false,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "c78ba2302e9b4af29cf5dd4bd7760831",
>       "finished\_at": "2026-10-11T13:49:19.314963Z",
>       "first\_token\_seconds": null,
>       "job\_id": "404662b58d1e42f28b70637b8218bda5",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": "1500b0a7be9b48bdb1daa375e520de7f",
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "69abe4ae7cb65fb49f20d00749b17477",
>       "stage": "extraction",
>       "stage\_id": "extraction",
>       "started\_at": "2026-10-11T13:49:19.314963Z",
>       "state": "skipped",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \}
>   \]
> \}

## Unchecked obligations

> \[\]

## Source Version

> \{
>   "document": \{
>     "case\_id": "fc1644fda3c945cea77d280594cec543",
>     "document\_version\_id": "RBI-IT-2023:2023-11-07",
>     "kind": "regulation",
>     "sha256": "d742aece8d2b5d74240e83e4d2ec6150a57f2076c02a9c878528ad6c42151786",
>     "source\_id": "RBI-IT-2023",
>     "synthetic": false,
>     "version": "2023-11-07"
>   \},
>   "effective\_date": "2024-04-01",
>   "filename": "Master Direction on Information Technology Governance, Risk, Controls and Assurance Practices",
>   "format": "html",
>   "freshness": "unverified",
>   "passages": \[
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 2(a)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:2a",
>       "text": "These Directions shall be applicable to the following entities (collectively referred to as ‘regulated entities’ or ’REs’ in these directions):"
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 2(a)(i)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:2ai",
>       "text": "all Banking Companies 1 , Corresponding New Banks and State Bank of India as defined under subsections (c), (da) and (nc) of section 5 of the Banking Regulation Act, 1949 (collectively referred to as ‘commercial banks’ hereinafter)."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 2(b)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:2b",
>       "text": "These Directions shall not be applicable to: Local Area Banks NBFC-Core Investment Companies"
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 19(a)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:19a",
>       "text": "Access to information assets shall be allowed only where a valid business need exists. REs shall have documented standards and procedures, which are approved by the ITSC and kept up to date for administering need-based access to an information system."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 19(b)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:19b",
>       "text": "Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 19(c)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:19c",
>       "text": "REs shall adopt multi-factor authentication for privileged users of i) critical information systems and ii) for critical activities, basis the RE’s risk assessment."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 29(a)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:29a",
>       "text": "Periodicity of DR drills for critical information systems shall be at least on a half-yearly basis and for other information systems, as per RE’s risk assessment."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 29(b)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:29b",
>       "text": "Any major issues observed during the DR drill shall be resolved and tested again to ensure successful conduct of drill before the next cycle."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 29(e)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:29e",
>       "text": "REs shall backup data and periodically restore such backed-up data to check its usability. The integrity of such backup data shall be preserved along with securing it from unauthorised access."
>     \}
>   \],
>   "publication\_date": "2023-11-07",
>   "source\_url": "https://www.rbi.org.in/Scripts/BS\_ViewMasDirections.aspx?id=12562"
> \}

## Source Version

> \{
>   "document": \{
>     "case\_id": "fc1644fda3c945cea77d280594cec543",
>     "document\_version\_id": "1500b0a7be9b48bdb1daa375e520de7f",
>     "effective\_date": null,
>     "kind": "policy",
>     "publication\_date": null,
>     "sha256": "e5b255e307bc926270d6a12c7499dce86350ab981325fd74264c344af32f9e6f",
>     "source\_id": "ad73bdc9377f424885678a03384012d0",
>     "source\_url": null,
>     "storage\_reference": "1500b0a7be9b48bdb1daa375e520de7f",
>     "synthetic": true,
>     "version": "1"
>   \},
>   "filename": "policy.txt",
>   "format": "txt",
>   "passages": \[
>     \{
>       "document\_version\_id": "1500b0a7be9b48bdb1daa375e520de7f",
>       "location": "Line 1",
>       "passage\_id": "1500b0a7be9b48bdb1daa375e520de7f-1",
>       "text": "Synthetic demo. Fictional bank policy."
>     \},
>     \{
>       "document\_version\_id": "1500b0a7be9b48bdb1daa375e520de7f",
>       "location": "Line 2",
>       "passage\_id": "1500b0a7be9b48bdb1daa375e520de7f-2",
>       "text": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>     \},
>     \{
>       "document\_version\_id": "1500b0a7be9b48bdb1daa375e520de7f",
>       "location": "Line 3",
>       "passage\_id": "1500b0a7be9b48bdb1daa375e520de7f-3",
>       "text": "Weekly timing is bank policy, not an RBI-specified interval."
>     \}
>   \],
>   "units": 1,
>   "uploaded\_at": "2026-10-11T13:49:18.938621\+00:00"
> \}

## Limitations

> Controlled example only. No live model call occurred.
> Current regulatory status is unverified. This report does not certify bank compliance.
> A policy alone does not prove operational execution.
> Human approval measures review decisions, not assessment accuracy.
> Available token usage appears in recorded attempts. Inference and total system costs remain unknown.
> The observed job state is current. The report cutoff controls saved findings, reviews, and trace events.
