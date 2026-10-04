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
| `evidence/` | The frozen build (named `build/` until EUD1-R9; the root `.gitignore` line `**/build/` kept that folder out of every commit): `records/` (route accounts, receiving records, `exp/` EXP records), `RUN_LOG.json`, `reader_input/` (the isolated reader's whole input set, with `MANIFEST.sha256`) |

## Run

```text
cd "<this folder>"
python3 -B run_d.py "$TMPDIR/eud1"          # includes B-2: the on-disk evidence/ equals a fresh build
python3 -B run_d.py "$TMPDIR/eud1" --freeze  # rewrites evidence/ (owner only)
```

Needs Python 3 with `jsonschema` (Draft 2020-12, `referencing`). It reads
DEL-09-01's EXP schema and `check_exp.py` without changing them.

## Comparison method and its limit (RV2 EUD1-R14; R23-52 item 2)

`compare_eud1.py` scores a reader's account against the frozen key, item by
item: met, not met or referred. Structured fields (standing, relied claims,
answers, bases, booleans, the forbidden kinds named in `cannot_conclude`)
are judged mechanically. Free text is judged only by a fixed paraphrase
lexicon, which cannot reach "in any wording" and is not grown further.
Therefore **a "met" on a case whose free text is non-empty is flagged
`examiner_reading_required`** and counted separately in the tally. It
needs an examiner's reading before it is relied on, as a "referred" item
does. For RR-EUD1, the eight flagged K6 items were read by RV2 (RV2-EUD1,
repair confirmation). `compare_sensitivity.py` shows that the flag is raised
for paraphrases the lexicon misses (RV2's N-2, N-6).

