# DEL-04-03 record-format prototype (R12-3)

**This is a prototype, not product code.** It shows that the PROPOSED record
format of RS-v0.8 §13 can be written and read back, and it exercises the
writer and reader failure behaviour of RS-v0.8 §14. It selects no placement
(OI-013, OI-014), no path, no identity algorithm and no canonicalization
(DEL-03-01 TBD-003). It sends nothing anywhere and installs nothing.

| File | What it is |
|---|---|
| `minischema.py` | A JSON Schema draft 2020-12 validator for a declared keyword subset: `type`, `enum`, `const`, `required`, `properties`, `additionalProperties`, `items`, `minItems`, `minLength`, `pattern`, `minimum`, `oneOf`, `anyOf`, `allOf`, `not`, `$ref` (local pointers and `$id` URNs through a registry), `$defs`; annotations `$schema`, `$id`, `$comment`, `title`, `description`, `examples`. Any other keyword fails the schema load, so no schema relies on a keyword this validator ignores. |
| `record_store.py` | The prototype writer (W-0 open, W-1 append, W-2 late write after a failure, W-3 correction) and reader (R-1…R-8) of RS §14 |
| `run_prototype.py` | Loads the three schemas (ACT, AS, RS), validates every valid and invalid example beside them, round-trips each valid RS example log through the writer and reader, and runs the failure cases FC-1…FC-7 |

The ACT and AS prototype folders hold a small script each that uses
`minischema.py` from here to validate their own examples.

## Run

```text
cd "<this folder>"
python3 -B run_prototype.py "$TMPDIR/b4-proto"
```

Python 3 standard library only (observed with Python 3.13.7 on macOS,
2026-09-30). The scratch folder receives the round-trip and failure-case
files; nothing is written beside the Design files.

## What it showed (2026-09-30)

- The three schemas load under the subset check.
- ACT: the P-01…P-06 configuration (with P-01a) validates; three invalid
  records fail for their stated reasons.
- AS: two settings-in versions validate; three invalid ones fail for their
  stated reasons.
- RS: the three example logs (20, 20 and 3 entries) validate; nine invalid
  entries fail for their stated reasons.
- Each valid log written through the writer and read back gives identical
  entries and identical bytes.
- FC-1…FC-7 each hold: a failed write is reported and later written in
  order with "record write failed"; a torn last line is kept, terminated and
  recorded as "partial entry not recovered"; two records of one capture count
  as one act with the direct capture governing, and a disagreement gives
  "recorders disagree"; a newer minor version is read limited, another major
  version or another format is refused; a correction keeps both entries and
  cannot change the kind; a sequence gap is reported; the writer refuses an
  act without capture evidence; the reader flags a recorder named as the
  decision actor and an unsandboxed process without "process network not
  observed".

The exact console output is recorded in the Wave B return file
`_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/WAVE_B/B4.md`.
