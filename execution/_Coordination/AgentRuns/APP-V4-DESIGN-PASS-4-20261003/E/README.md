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
| `proposed_rows.json` | PR-1…PR-13: rows proposed for DEL-02-03's `checkpoint-record-entries.schema.json` (CE-4 `actRequest`; CE-10's `actRef`, PR-13) and DEL-01-04's `aac.offer` and `aac.capture-evidence` schemas. **Not applied to those files**; outside O-A's write boundary |
| `run_e.py` | The check: A (schemas as they are), B (with PR-1…PR-13 in memory, plus invalid cases INV-E-1…7), C (RS's own A16 cases), D (the decision view; reader cases RV-1…RV-7; inputs unchanged) |

It reuses DEL-04-03's subset validator `prototype/minischema.py`, read-only.

## Run

```text
cd "<this folder>"
python3 -B run_e.py "$TMPDIR/early-path"
```

## What it showed (2026-10-03, Python 3, macOS; 39/39 expectations held)

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
