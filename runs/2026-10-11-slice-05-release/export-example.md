# The Regulator assessment report

## Export status

> Assessment export · Simulated processing · Fictional bank data

## Snapshot and selected versions

> \{
>   "assessment\_date": "2024-04-08",
>   "bank\_profile": \{
>     "name": "Fictional export bank 1791713887717"
>   \},
>   "case\_id": "ac50ba2784d44c72a49142a9cf4393ae",
>   "mode": "historical",
>   "model\_version": "in.openai.gpt-5.6-luna",
>   "prompt\_version": "controlled-vs3-v1",
>   "selected\_document\_ids": \{\},
>   "selected\_obligations": \[
>     "RBI-IT-19b"
>   \],
>   "selected\_versions": \{
>     "RBI-IT-2023": "2023-11-07",
>     "d1de51780464480ab0432299c48742f4": "1"
>   \},
>   "snapshot\_id": "3940db0e3d905334b511b22687d5b82c",
>   "synthetic": true
> \}

## Cohort filters and time bases

> \{
>   "kind": "single\_assessment",
>   "case\_id": "ac50ba2784d44c72a49142a9cf4393ae",
>   "run\_id": "3940db0e3d905334b511b22687d5b82c",
>   "snapshot\_id": "3940db0e3d905334b511b22687d5b82c",
>   "model\_id": "in.openai.gpt-5.6-luna",
>   "prompt\_version": "controlled-vs3-v1",
>   "data\_mode": "controlled\_simulation",
>   "recommendation\_availability": \{
>     "through": "2026-10-11T10:18:10.147729\+00:00",
>     "end\_inclusive": true
>   \},
>   "runtime\_selection": \{
>     "job\_id": "71215479eaba40ff99621bc1c618b40b",
>     "job\_admitted\_at": "2026-10-11T10:18:09.217303\+00:00",
>     "job\_state\_time\_basis": "observed\_current\_state"
>   \}
> \}

## Observed job state

> \{
>   "authority\_verified\_at": null,
>   "case\_id": "ac50ba2784d44c72a49142a9cf4393ae",
>   "created\_at": 1791713889.217303,
>   "deadline": 1791714489.4248216,
>   "finished\_at": 1791713889.679573,
>   "freshness": "unverified",
>   "job\_id": "71215479eaba40ff99621bc1c618b40b",
>   "label": "Simulated",
>   "model\_calls": 1,
>   "retrieval\_calls": 0,
>   "snapshot\_id": "3940db0e3d905334b511b22687d5b82c",
>   "stage": "persistence",
>   "started\_at": 1791713889.4248216,
>   "state": "completed",
>   "stop\_reason": null,
>   "unchecked\_obligations": \[\]
> \}

## Report cutoff

> 2026-10-11T10:18:10.147729\+00:00

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
>       "document\_version\_id": "a43ac560695649bf9d23a5aeda163a98",
>       "passage\_id": "a43ac560695649bf9d23a5aeda163a98-2",
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
>         "document\_version\_id": "a43ac560695649bf9d23a5aeda163a98",
>         "passage\_id": "a43ac560695649bf9d23a5aeda163a98-2",
>         "location": "Line 2",
>         "quote": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>       \}
>     \]
>   \}
> \]

## Original findings and recommendation IDs

> \[
>   \{
>     "finding\_id": "6e6b879e4f485b2ea1f987855de17134",
>     "snapshot\_id": "3940db0e3d905334b511b22687d5b82c",
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
>         "document\_version\_id": "a43ac560695649bf9d23a5aeda163a98",
>         "passage\_id": "a43ac560695649bf9d23a5aeda163a98-2",
>         "location": "Line 2",
>         "quote": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>       \}
>     \],
>     "rationale": "Controlled example. The policy states a control, but this example has no verified operational evidence. Applicability and activity records need human review.",
>     "remedy": "Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.",
>     "gap\_kind": "evidence",
>     "applicability\_reason": null,
>     "claims": \[\],
>     "run\_id": "3940db0e3d905334b511b22687d5b82c",
>     "primary\_recommendation": "Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.",
>     "available\_at": "2026-10-11T10:18:09.642613Z",
>     "model\_id": "in.openai.gpt-5.6-luna",
>     "prompt\_version": "controlled-vs3-v1",
>     "data\_mode": "controlled\_simulation",
>     "source\_version\_ids": \[
>       "RBI-IT-2023:2023-11-07",
>       "d1de51780464480ab0432299c48742f4:1"
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
>     "idempotency\_key": "e767d801-66ca-4140-995a-64834ea1a879",
>     "event\_id": "1298125b77d24d2bb61be60c7cab06f5",
>     "finding\_id": "6e6b879e4f485b2ea1f987855de17134",
>     "reviewer\_id": "slice-05-tests",
>     "committed\_at": "2026-10-11T10:18:10.106041Z",
>     "revision": 1
>   \}
> \]

## Review summary

metric_definition_version: d24-v1

cutoff: 2026-10-11T10:18:10.147729+00:00

data_mode: controlled_simulation

run_id: 3940db0e3d905334b511b22687d5b82c

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
>   "run\_id": "3940db0e3d905334b511b22687d5b82c",
>   "attempts": \[
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[\],
>       "attempt\_id": "1ee549245c744fcf92aaa2e400f10797",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.015000000013969839,
>       "errors": \[\],
>       "event\_id": "32c560ad19a14577a3783f6366ee2968",
>       "finished\_at": "2026-10-11T10:18:09.651632Z",
>       "first\_token\_seconds": null,
>       "job\_id": "71215479eaba40ff99621bc1c618b40b",
>       "model\_id": null,
>       "operation": "storage",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "3940db0e3d905334b511b22687d5b82c",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "3940db0e3d905334b511b22687d5b82c",
>       "stage": "persistence",
>       "stage\_id": "persistence",
>       "started\_at": "2026-10-11T10:18:09.640603Z",
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
>       "attempt\_id": "98e42f475a9c48359a74335d0e8dc743",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "48df3228fc9f42dab790b09cf7251000",
>       "finished\_at": "2026-10-11T10:18:09.532531Z",
>       "first\_token\_seconds": null,
>       "job\_id": "71215479eaba40ff99621bc1c618b40b",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "3940db0e3d905334b511b22687d5b82c",
>       "selected\_passage\_ids": \[
>         "RBI-IT-2023:2023-11-07:19b",
>         "RBI-IT-2023:2023-11-07:2ai",
>         "RBI-IT-2023:2023-11-07:2b",
>         "a43ac560695649bf9d23a5aeda163a98-2"
>       \],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "3940db0e3d905334b511b22687d5b82c",
>       "stage": "context\_selection",
>       "stage\_id": "context\_selection",
>       "started\_at": "2026-10-11T10:18:09.532531Z",
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
>         "1298125b77d24d2bb61be60c7cab06f5"
>       \],
>       "attempt\_id": "b199cda61a8141ef849e702271f2e23f",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.01600000000325963,
>       "errors": \[\],
>       "event\_id": "7126b2e487174bc3ae849ae2d9842d72",
>       "finished\_at": "2026-10-11T10:18:10.115872Z",
>       "first\_token\_seconds": null,
>       "job\_id": "71215479eaba40ff99621bc1c618b40b",
>       "model\_id": null,
>       "operation": "storage",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "3940db0e3d905334b511b22687d5b82c",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "3940db0e3d905334b511b22687d5b82c",
>       "stage": "review\_event",
>       "stage\_id": "review\_event",
>       "started\_at": "2026-10-11T10:18:10.103029Z",
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
>       "attempt\_id": "b5bf6ff5fd92475bb176feb966e89112",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.01600000000325963,
>       "errors": \[\],
>       "event\_id": "9a0a02822b5a4b32914a3dd01e418762",
>       "finished\_at": "2026-10-11T10:18:09.443632Z",
>       "first\_token\_seconds": null,
>       "job\_id": "71215479eaba40ff99621bc1c618b40b",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "3940db0e3d905334b511b22687d5b82c",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "3940db0e3d905334b511b22687d5b82c",
>       "stage": "source\_verification",
>       "stage\_id": "source\_verification",
>       "started\_at": "2026-10-11T10:18:09.437860Z",
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
>       "attempt\_id": "046266e935cb4316bcfdd7cc2a7bc956",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.03200000000651926,
>       "errors": \[\],
>       "event\_id": "be97bf13dc3c453799bccc1689a72fd6",
>       "finished\_at": "2026-10-11T10:18:09.589532Z",
>       "first\_token\_seconds": null,
>       "job\_id": "71215479eaba40ff99621bc1c618b40b",
>       "model\_id": "in.openai.gpt-5.6-luna",
>       "operation": "model",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "3940db0e3d905334b511b22687d5b82c",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "3940db0e3d905334b511b22687d5b82c",
>       "stage": "model\_call",
>       "stage\_id": "model\_call",
>       "started\_at": "2026-10-11T10:18:09.558286Z",
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
>       "attempt\_id": "264eb9491dd2480a9b8d8d87acc9288d",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "dcc345dbb88c4ad5b342eaabe2d103ab",
>       "finished\_at": "2026-10-11T10:18:09.612249Z",
>       "first\_token\_seconds": null,
>       "job\_id": "71215479eaba40ff99621bc1c618b40b",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "3940db0e3d905334b511b22687d5b82c",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "3940db0e3d905334b511b22687d5b82c",
>       "stage": "validation",
>       "stage\_id": "validation",
>       "started\_at": "2026-10-11T10:18:09.612249Z",
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
>       "attempt\_id": "a16186536a7b48ab87b9b37ba280abd3",
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
>         "a43ac560695649bf9d23a5aeda163a98-1",
>         "a43ac560695649bf9d23a5aeda163a98-2",
>         "a43ac560695649bf9d23a5aeda163a98-3"
>       \],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "f24a0bfc63b947eba64c5ec0e3997558",
>       "finished\_at": "2026-10-11T10:18:09.509316Z",
>       "first\_token\_seconds": null,
>       "job\_id": "71215479eaba40ff99621bc1c618b40b",
>       "model\_id": null,
>       "operation": "retrieval",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "3940db0e3d905334b511b22687d5b82c",
>       "selected\_passage\_ids": \[
>         "RBI-IT-2023:2023-11-07:19b",
>         "RBI-IT-2023:2023-11-07:2ai",
>         "RBI-IT-2023:2023-11-07:2b",
>         "a43ac560695649bf9d23a5aeda163a98-2"
>       \],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "3940db0e3d905334b511b22687d5b82c",
>       "stage": "retrieval",
>       "stage\_id": "retrieval",
>       "started\_at": "2026-10-11T10:18:09.509316Z",
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
>         "a43ac560695649bf9d23a5aeda163a98"
>       \],
>       "attempt\_id": "3786cce9779a4f0abb14d2c0c937cce7",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": false,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "ff3199172c0240a2aed24c70d19483d9",
>       "finished\_at": "2026-10-11T10:18:09.471212Z",
>       "first\_token\_seconds": null,
>       "job\_id": "71215479eaba40ff99621bc1c618b40b",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": "a43ac560695649bf9d23a5aeda163a98",
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "3940db0e3d905334b511b22687d5b82c",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "3940db0e3d905334b511b22687d5b82c",
>       "stage": "extraction",
>       "stage\_id": "extraction",
>       "started\_at": "2026-10-11T10:18:09.471212Z",
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
>     "case\_id": "ac50ba2784d44c72a49142a9cf4393ae",
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
>     "case\_id": "ac50ba2784d44c72a49142a9cf4393ae",
>     "document\_version\_id": "a43ac560695649bf9d23a5aeda163a98",
>     "effective\_date": null,
>     "kind": "policy",
>     "publication\_date": null,
>     "sha256": "e5b255e307bc926270d6a12c7499dce86350ab981325fd74264c344af32f9e6f",
>     "source\_id": "d1de51780464480ab0432299c48742f4",
>     "source\_url": null,
>     "storage\_reference": "a43ac560695649bf9d23a5aeda163a98",
>     "synthetic": true,
>     "version": "1"
>   \},
>   "filename": "policy.txt",
>   "format": "txt",
>   "passages": \[
>     \{
>       "document\_version\_id": "a43ac560695649bf9d23a5aeda163a98",
>       "location": "Line 1",
>       "passage\_id": "a43ac560695649bf9d23a5aeda163a98-1",
>       "text": "Synthetic demo. Fictional bank policy."
>     \},
>     \{
>       "document\_version\_id": "a43ac560695649bf9d23a5aeda163a98",
>       "location": "Line 2",
>       "passage\_id": "a43ac560695649bf9d23a5aeda163a98-2",
>       "text": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>     \},
>     \{
>       "document\_version\_id": "a43ac560695649bf9d23a5aeda163a98",
>       "location": "Line 3",
>       "passage\_id": "a43ac560695649bf9d23a5aeda163a98-3",
>       "text": "Weekly timing is bank policy, not an RBI-specified interval."
>     \}
>   \],
>   "units": 1,
>   "uploaded\_at": "2026-10-11T10:18:08.605038\+00:00"
> \}

## Limitations

> Controlled example only. No live model call occurred.
> Current regulatory status is unverified. This report does not certify bank compliance.
> A policy alone does not prove operational execution.
> Human approval measures review decisions, not assessment accuracy.
> Available token usage appears in recorded attempts. Inference and total system costs remain unknown.
> The observed job state is current. The report cutoff controls saved findings, reviews, and trace events.
