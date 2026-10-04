# Early path E — one decision package decided by the person

**This is a bounded prototype, not product code** (LOOP_INIT: "bounded
implementation and connected tests"). Owner O-A, run
`APP-V4-DESIGN-PASS-4-20261003`; rulings R23-2, R23-3, R23-8. Every fixture is
invented, and no person performed any act. It installs nothing, uses no
network and writes only into the scratch folder you give it.

| File | What it is |
|---|---|
| `make_fixture.py` | Writes fixture FX-DP1 deterministically (rerunning it gives the same bytes) |
| `fixtures/FX-DP1/` | The input set: two package files an agent wrote, an RS 0.1 log (two `act_request` packages and one A16 `human_act`), the act control's offer and capture evidence, and an agent message that is **not** a record. `MANIFEST.sha256` lists all of them |
| `decision_view.py` | DEL-06-02's decision view (DECISION_VIEW.md DV-1…DV-9), derived from the input set only |
| `proposed_rows.json` | PR-1…PR-13 as proposed at E-1; **applied** under R23-18 to DEL-02-03's `checkpoint-record-entries.schema.json` (schema 0.7; PR-5 written in the keyword subset EXEC's checker reads) and DEL-01-04's `aac.offer` and `aac.capture-evidence` schemas (AAC-v0.3) |
| `run_e.py` | The check, on the files as they are: A (each PR row present; every record and object valid; capture, offer and record agree; INV-E-1…7), C (RS's own A16 cases), D (the decision view; reader cases RV-1…RV-7; inputs unchanged) |

It reuses DEL-04-03's subset validator `prototype/minischema.py`, read-only.

## Run

```text
cd "<this folder>"
python3 -B run_e.py "$TMPDIR/early-path"
```

## What it showed

**E-1 refrozen after RV-E1 (2026-10-03): 56/56 expectations held, on the
files as they are.**

- **R23-24.** FX-DP1's package files have their own shape, DEL-02-03
  `$defs/decisionPackageFile`, and validate against it. Each `act_request`
  equals DEL-02-03's stated mapping of its file (`request_from_file`), and its
  evidence is the file's own sha-256. A file carrying a recorder element is
  refused.
- **E1-R4.** An implementation written from AAC-v0.3 §5.1's text, not from
  Python's `json`, gives the same offer digest over ü, ≈ and U+2028. It also
  agrees on integers.
- **R23-25.** RV-8: a second A16 on the same package supersedes the first,
  and the first stays listed. RV-9: a correction is shown as a correction.
- Everything from the previous refreeze still holds. The fixture was rebuilt,
  with manifest `9501ef81…`.

### Previous refreeze (before RV-E1)

**E-1 refrozen (2026-10-03), on the files as they are after R23-18: 47/47
expectations held.** The offer digest now follows AAC-v0.3 §5.1
(`aac-offer-digest/0.1`) and recomputes from the offer file alone (RR-E's
finding). The fixture's offer and capture changed for this; nothing else in
the fixture did. Every PR row is present in its file. Both package
`act_request` entries, the A16 `human_act`, the A16 `act_lapsed`, the offer
and the capture evidence are valid. The capture, offer and record agree.
INV-E-1…7 fail under the new rules. RS's INV-RS-25…28 fail as intended. The
decision view gives the same rows and reader-case results as below, and the
input set is unchanged.

The earlier E-1 run (37/37, then 39/39) is below as history. It was made
before the rows were applied and checked them in memory.

### Earlier run (before R23-18)

Run of 2026-10-03 (Python 3, macOS): 39/39 expectations held.

- **A.** The A16 `human_act` is valid against `RS_RECORD.schema.json` as it
  now is. Both package `act_request` entries are **not** valid, because their
  body is DEL-02-03's CE-4: `form` has no "decision package file", `actKind`
  has no A16, and `alternatives`/`consequences` are refused. The `act_lapsed` the writer
  would record if the package changed after the decision is not valid either
  (CE-10's `actRef` has no A16), nor are the AAC offer and capture evidence
  (no A16).
- **B.** With PR-1…PR-13 in memory, every record and object is valid,
  including that `act_lapsed`. The
  capture, offer and A16 record agree on record id, capture reference,
  request, chosen alternative and bound content. Seven invalid cases fail
  under the new rules.
- **C.** RS's INV-RS-25…28 fail as intended, and the act-log example's A16
  entry is valid.
- **D.** PKG-1 is *decided* (ALT-2, not lapsed, actor "identity not verified"
  apart from the recorder). PKG-2 stays *pending*, even though the agent's
  message claims a decision. Reader cases:
  - RV-1: an alternative the package does not name is not counted;
  - RV-2: a package edited after the decision shows *lapsed*;
  - RV-3: an absent package file gives *unknown (unavailable)*;
  - RV-5: an act of another kind citing the package does not decide it;
  - RV-6: positive control;
  - RV-7: an act citing an unknown request is a view limit.

  The input-set hashes are unchanged after every derivation.

The DEL-04-03 prototype (`run_prototype.py`) also still holds after the RS
rows: 67 checks, up from 63, the four new being INV-RS-25…28.
