# DEL-01-04 prototype — request cards, outcomes, attachments, drafts, act control

**This is a design prototype, not product code.** It belongs to
DEL-01-04/NIR-v0.1 (`../NATIVE_INTERACTION_RECEIVING.md`, §13.2) and
DEL-01-04/AAC-v0.1 (`../APP_ACT_CONTROL.md`, §8), written by node D3 of run
`APP-V4-DESIGN-PASS-3-20261001` under R17-1 (R12-3 limits). It is not an App
candidate and not the OI-008 placement; nothing in it is qualified or
selected. Python 3 standard library only; no package is installed; no network
is used; the Codex binary is never started; all content is invented.

## Files

| File | Role |
|---|---|
| `nir_model.py` | The card model per 0.158.0 server-request kind (NIR §4.1–§4.3); a register double applying HOSTING-BOUNDARY-v0.8 §6.2.1 RT-01…RT-13 and the U-26 refusal order, used only to drive card states (NIR §4.4); card states; turn/outcome labels and the start display (NIR §5); attachment supply records (NIR §6); the draft view (NIR §7) |
| `act_control.py` | The App act control (AAC §1–§5): offers, native-only operation, stale binding, capture evidence, RS entries written through DEL-04-03's writer, A15 with a stub workspace registrar, late write and relaunch recovery |
| `run_cases.py` | Runs every check; exit status 0 when all are as expected |
| `results/RUN_2026-10-01.txt` | The recorded output of the run below |

**Read-only imports of first-increment prototypes** (located by path from this
folder; nothing in them is changed): DEL-04-03's `minischema.py` (validator)
and `record_store.py` (the PROPOSED writer and reader), so the act control's
entries are validated by RS's own schema before they are written; DEL-01-01's
`jsonschema_subset.py`, so every register entry the walk produces is checked
against HOSTING's PROPOSED entry schema. If the already-installed `jsonschema`
package is importable, the five DEL-01-04 schemas are cross-checked with it
(S-4); otherwise that check is skipped.

## How to run

```sh
cd "<this folder>"
python3 run_cases.py      # one line per check; exit status 0 = all as expected
```

Logs written by the act control go to a temporary folder under `$TMPDIR`
(`d3-del-01-04-*`).

## Run recorded

- Date: 2026-10-01; host: macOS (Darwin 25.6.0, arm64); Python 3.13.7.
- Command: `python3 run_cases.py` in this folder.
- Output: `results/RUN_2026-10-01.txt` — 103 checks, 0 failed, exit status 0.

A "pass" means the rules ran as written on this model. It is evidence about
the design, never a VER pass: no App candidate exists.
