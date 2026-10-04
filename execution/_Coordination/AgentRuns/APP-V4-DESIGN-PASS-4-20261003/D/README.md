# EU-D1 — one question, five conditions, two connectors

**Bounded prototype, not product code** (LOOP_INIT: "bounded implementation
and connected tests"). Owner O-D, run `APP-V4-DESIGN-PASS-4-20261003`;
ruling R23-34. Every PEC and Domains input is constructed; the two work-graph
files are this run's real `WORK_GRAPH.md` at commits `e4a0c2c4c3` (S) and
`e086dfff32` (R), read with `git show`. No network; nothing is installed.

| File | What it is |
|---|---|
| `make_fixture.py` | Writes fixture FX-EUD1 deterministically (`fixtures/FX-EUD1/`, `MANIFEST.sha256`) |
| `eud1.py` | The route (DEL-07-02 CFB-v0.1), PEC receiving (DEL-07-01 PRC-v0.1), Domains receiving (DEL-08-01 DRC-v0.1) and DEL-09-10's rehearsal records (CW-v0.1) |
| `run_d.py` | The check (F, S, E, I, T, X, B, R groups; see its docstring) |
| `compare_eud1.py`, `compare_sensitivity.py` | The reader comparison checker, written against the first real account (RR-EUD1), and its sensitivity test on altered copies of that account |
| `probe/` | H-1 probes P-H1 (`probe_mcp_call.py`) and P-H1b (`probe_model_input.py`), with redacted results |
| `key/EUD1_KEY.json` | The question key, fixed before any reader runs. **Not** in the reader's input set |
| `reader/READER_TASK.md` | The reader's task and answer form |
| `build/` | The frozen build: `records/` (route accounts, receiving records, `exp/` EXP records), `RUN_LOG.json`, `reader_input/` (the isolated reader's whole input set, with `MANIFEST.sha256`) |

## Run

```text
cd "<this folder>"
python3 -B run_d.py "$TMPDIR/eud1"          # includes B-2: build/ equals a fresh build
python3 -B run_d.py "$TMPDIR/eud1" --freeze  # rewrites build/ (owner only)
```

Needs Python 3 with `jsonschema` (Draft 2020-12, `referencing`). It reads
DEL-09-01's EXP schema and `check_exp.py` without changing them.
