# DEL-04-03 record-format prototype (R12-3)

**This is a prototype, not product code.** It shows that the PROPOSED record
format of RS-v0.9 §13 can be written and read back, and it exercises the
writer and reader failure behaviour of RS-v0.9 §14. It selects no placement
(OI-013, OI-014), no path, no identity algorithm and no canonicalization
(DEL-03-01 TBD-003). It sends nothing anywhere and installs nothing.

| File | What it is |
|---|---|
| `minischema.py` | A JSON Schema draft 2020-12 validator for a declared keyword subset: `type`, `enum`, `const`, `required`, `properties`, `additionalProperties`, `items`, `minItems`, `minLength`, `pattern`, `minimum`, `oneOf`, `anyOf`, `allOf`, `not`, `$ref` (local pointers, `$id` URNs through a registry, and relative file paths resolved against the referring schema's directory — how RS references EXEC's CE bodies, R14-1; a standard validator needs the same retrieval rule, RS §13), `$defs`; annotations `$schema`, `$id`, `$comment`, `title`, `description`, `examples`. Any other keyword fails the schema load, so no schema relies on a keyword this validator ignores. |
| `record_store.py` | The prototype writer (W-0 open, W-1 append, W-2 late write after a failure, W-3 correction) and reader (R-1…R-8) of RS §14 |
| `run_prototype.py` | Loads the three schemas (ACT, AS, RS), validates every valid and invalid example beside them, round-trips each valid RS example log through the writer and reader, and runs the failure cases FC-1…FC-7 ; then runs `exec_to_rs.py`'s checks |
| `exec_to_rs.py` | R14-1: RS format 0.1 is the one container. Checks that each of EXEC's 19 CE bodies has an RS kind that references it, writes EXEC's valid recorder outputs (DEL-02-03 `checkpoint-record-entries.example.valid.json`) through the writer as RS entries and reads them back, then does the same for EXEC's other CH scripts and one sample of each remaining kind. Every entry must be valid and none without a kind |

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
- RS: the three example logs of node B4 (20, 20 and 3 entries) validate;
  nine invalid entries fail for their stated reasons. Since then two logs
  were added (host destinations, 12 entries, node B5; run not started, 1
  entry, node B8) and six invalid entries (INV-RS-10…15): at the RQ rerun
  all five logs (3, 20, 12, 20 and 1 entries) validate and round-trip, and
  INV-RS-1…15 fail for their stated reasons.
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

- RS-v0.9 (node F-C of run `APP-V4-DESIGN-PASS-3-20261001`, 2026-10-02):
  six logs (4, 8, 20, 12, 20 and 1 entries; the act log gained a two-entry
  A15 and the chained-run log is new) validate and round-trip; INV-RS-1…24
  fail for their stated reasons; the reader's new A15 rule (bound content
  equals reviewed content, WR ID-2; registered entries in order) flags the
  two FC-7c entries; 63 PASS, 0 FAIL. Output in `F/F-C.md` of that run.

The exact console output is recorded in the Wave B return file
`_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/WAVE_B/B4.md`; the
R14 repair's rerun (four logs, INV-RS-1…15, and the EXEC → RS conversion:
12 of 12 and 40 of 40 entries valid) in `WAVE_B/RP-1.md`.

```text
python3 -B exec_to_rs.py "$TMPDIR/exec-to-rs"
```
