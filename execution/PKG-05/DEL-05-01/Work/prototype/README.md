# DEL-05-01 prototype: streamed tool-call assembly (not product code)

A local prototype under R12-3 of run `APP-V4-DESIGN-PASS-2-20260930`
(node B9). Python 3 standard library only. Nothing was installed. It is
**not product code**: it builds no loop, selects no provider or server, and
shows nothing about any host.

## What it shows

That the assembly and malformed-call rules of LOOP-v0.8 §7 and §7.1
(R-F1…R-F5, MC-1…MC-13, with R12-7 for MC-8) are consistent and executable
on input shaped like **FB-CC-1**, the published Chat Completions reference
named in LOOP-v0.8 §4.1 as a **fixture basis, not a product selection**.
Each assembled call is checked against `../LOOP_TOOL_CALL.schema.json`.

It does not show that model servers in general emit these shapes. OBS-1
observed the four points on one local server (LOOP-v0.8 §4.1, OBS-1 column;
DEL-01-01 `OBS_1_0.158.0.md` §10); fixtures OBS1-C1…OBS1-C3 reproduce the
observed shapes (reasoning and whitespace content deltas included; observed
tool names replaced by FX-PIPE-01 entries) and assemble as observed.

## Files

| File | Role |
|---|---|
| `assemble_tool_calls.py` | Joins streamed fragments by position, applies the termination-reason and per-call rules, emits one record per call, compares with the expected result, validates each record against the schema |
| `schema_subset.py` | JSON Schema 2020-12 validator for the subset the DEL-05-01 and DEL-05-02 schemas use (type, properties, required, additionalProperties false, enum, const, items, minItems, minLength, minimum, oneOf, anyOf, local `$ref`); any other keyword raises an error |
| `fixtures/stream_fixtures.json` | 22 streams (19 written from FB-CC-1 at node B9; OBS1-C1…OBS1-C3 added at RP-4 in the shapes OBS-1 observed) in FB-CC-1's chunk shape with invented content on FX-PIPE-01 identifiers, each with its expected result. Chunks carry only the members the assembly reads. Written with a throw-away generator in the executor's scratch folder; this JSON is the fixture of record |

## How to run

```sh
cd prototype
python3 assemble_tool_calls.py
python3 schema_subset.py ../LOOP_TOOL_CALL.schema.json ../LOOP_TOOL_CALL.example.valid.json ../LOOP_TOOL_CALL.example.invalid.json
```

`schema_subset.py` exits with status 1 whenever any instance it is given is
invalid, so the commands above that pass the invalid example exit 1 by
design; the expected output is VALID for the valid example and INVALID for
the invalid one (RQ; V19-B n-7).

## Recorded run (2026-09-30, Python 3.13.7, macOS)

The 2026-09-30 Python 3.13.7 prototype run assembled the 19 FB-CC-1
fixture streams as expected; the later OBS1-C1…OBS1-C3 replay also matched
the observed shapes. The schema accepted the valid example and refused the
invalid example. These are fixture results, not host qualification.

"FX-M5 complete/MC-5" means the call parsed completely and was refused at
V-2 (*not offered*).

## Destination flow (node B5; LOOP-v0.8 §5.3)

`destination_flow.py` (Python 3 standard library; not product code) runs
the one destination flow of LOOP-v0.8 §5.3 on a **scripted** native layer
and host control: the allow rule DF-3 (A-1…A-7), the check V-D (DF-4 (b))
and at contact (DF-4 (c)), the in-work request with a carried call (DF-5),
the request states and results (DF-6) and the stateless MCP evidence
(DF-7, from scripted discovery answers). Every RS entry it writes is
checked against DEL-04-03's `RS_RECORD.schema.json` with DEL-04-03's
`minischema.py`; every request record against
`../LOOP_DESTINATION_REQUEST.schema.json` with `schema_subset.py`. It
observes no host, native layer or MCP server; all subjects are invented.

```sh
cd prototype
python3 -B destination_flow.py
python3 -B destination_flow.py --emit "$TMPDIR/b5/e14.jsonl"   # the E-14 log
python3 schema_subset.py ../LOOP_DESTINATION_REQUEST.schema.json ../LOOP_DESTINATION_REQUEST.example.valid.json ../LOOP_DESTINATION_REQUEST.example.invalid.json
```

Recorded run (2026-09-30, Python 3.13.7, macOS): 16 cases (MS-06,
MS-14…MS-24, MS-25a, MS-25b, MS-26, MS-27) PASS; 68 RS entries and 11
request records valid; the valid example accepted and the invalid one
refused (two reasons: scope once with no carried call; a decline worded as
"destination not allowed"); "RESULT: all expectations held", exit 0. With
`--emit` it wrote the 12-entry E-14 log that DEL-04-03 keeps as
`RS_RECORD.valid.host-destinations.example.jsonl`. Negative control: with
MS-24's expectation altered in memory, the run reported "RESULT: failures"
and exit 1.
