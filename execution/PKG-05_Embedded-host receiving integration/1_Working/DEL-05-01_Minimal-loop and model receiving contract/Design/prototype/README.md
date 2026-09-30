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

It does not show that any model server emits these shapes. That is OBS-1's
to observe (LOOP-v0.8 §4.1, OBS-1 column).

## Files

| File | Role |
|---|---|
| `assemble_tool_calls.py` | Joins streamed fragments by position, applies the termination-reason and per-call rules, emits one record per call, compares with the expected result, validates each record against the schema |
| `schema_subset.py` | JSON Schema 2020-12 validator for the subset the DEL-05-01 and DEL-05-02 schemas use (type, properties, required, additionalProperties false, enum, const, items, minItems, minLength, minimum, oneOf, anyOf, local `$ref`); any other keyword raises an error |
| `fixtures/stream_fixtures.json` | 19 streams in FB-CC-1's chunk shape with invented content on FX-PIPE-01 identifiers, each with its expected result. Chunks carry only the members the assembly reads. Written with a throw-away generator in the executor's scratch folder; this JSON is the fixture of record |

## How to run

```sh
cd prototype
python3 assemble_tool_calls.py
python3 schema_subset.py ../LOOP_TOOL_CALL.schema.json ../LOOP_TOOL_CALL.example.valid.json ../LOOP_TOOL_CALL.example.invalid.json
```

## Recorded run (2026-09-30, Python 3.13.7, macOS)

`python3 assemble_tool_calls.py`:

```text
PASS FX-V1s   FX-V1 (stream) termination=tool-calls             #0 complete
PASS FX-V1i   FX-V1 (two)    termination=tool-calls             #0 complete; #1 complete
PASS FX-M1    MC-1           termination=length-truncated       #0 truncated/MC-1
PASS FX-M1b   MC-1           termination=length-truncated       #0 truncated/MC-1; #1 truncated/MC-1
PASS FX-M2    MC-2           termination=ended-without-reason   #0 interrupted/MC-2
PASS FX-M3    MC-3           termination=tool-calls             #0 malformed/MC-3
PASS FX-M4    MC-4           termination=tool-calls             #0 malformed/MC-4
PASS FX-M4b   MC-4           termination=tool-calls             #0 malformed/MC-4
PASS FX-M4c   MC-4           termination=tool-calls             #0 malformed/MC-4
PASS FX-M5    MC-5           termination=tool-calls             #0 complete/MC-5
PASS FX-M6a   MC-6           termination=tool-calls             #0 malformed/MC-6
PASS FX-M6b   MC-6           termination=tool-calls             #0 complete
PASS FX-M6c   MC-6           termination=tool-calls             #0 malformed/MC-6
PASS FX-M7    MC-7           termination=tool-calls             #0 malformed/MC-7; #1 malformed/MC-7
PASS FX-M8    MC-8 (R12-7)   termination=tool-calls             #0 complete; #1 malformed/MC-3; #2 complete
PASS FX-M10   MC-10          termination=tool-calls             #0 malformed/MC-10
PASS FX-M11   MC-11          termination=content-filtered       #0 filtered/MC-11
PASS FX-M12   MC-12          termination=tool-calls             #0 malformed/MC-12
PASS FX-M13   MC-13          termination=tool-calls             #0 malformed/MC-13; #1 malformed/MC-13
19/19 cases as expected; every record checked against LOOP_TOOL_CALL.schema.json
```

Schema examples:

```text
VALID   ../LOOP_TOOL_CALL.example.valid.json
INVALID ../LOOP_TOOL_CALL.example.invalid.json
    $: oneOf matched 0 branches [], exactly 1 required
```

"FX-M5 complete/MC-5" means the call parsed completely and was refused at
V-2 (*not offered*).
