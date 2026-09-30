# DEL-09-06 prototype — W14 rehearsals and the W14 result record

**Not product code.** A local prototype under R12-3 (run
APP-V4-DESIGN-PASS-2-20260930, node B7): Python 3 standard library only, no
package installed, no network. It shows that the PROPOSED W14 result record
of CA-v0.6 §8.4 (`../w14-result-record.schema.json`) can be produced from
rehearsal runs and validated, and it runs the W14 parts that the round-1
doubles can carry (CA-v0.6 §8.5).

| File | What it shows |
|---|---|
| `run_w14_rehearsals.py` | Drives **SH-1**, the one simulated host (DEL-03-01 C-v0.8 §10.8), over both native paths through its driver `run_fixture.py`; maps the imitated native items with ADAPTER-v0.6's mapper (`observe_map.py`); runs EXEC-v0.6's current-phase recorder and required-tool check (`run_all.py`, `checkpoint_recorder.py`); writes one W14 result record per case and phase reading; validates them and the committed example instances with DEL-03-01's subset validator (`schema_subset.py`) |

The round-1 prototypes are imported read-only from their own folders and are
not changed; `sys.dont_write_bytecode` keeps their folders free of caches.

## Run

```sh
cd "<this folder>/.."
python3 -B prototype/run_w14_rehearsals.py --out "$TMPDIR/b7-w14"
# --write-examples regenerates w14-result-record.example.{valid,invalid}.json
```

Exit status 0 only if every check holds. The observed output of the run of
2026-09-30 is recorded in CA-v0.6 §8.5 and in
`_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/WAVE_B/B7.md`.

## Limits

- Everything is *test-double* evidence (C-v0.8 evidence-label mapping). No
  record counts toward OUT-003 (CA §8.1, §8.3); nothing here observes Codex,
  SWBPIPE or any host, and no person performed any act.
- SH-1 has no workflow library, no A4 facility, no whole-model staleness or
  identity profile, no restart of its own records, no H or E surface and no
  checkpoint declarations (C §10.8). The recorder double has no A5 item
  decisions (CE-7), no interruption and no rebuild. The parts that need these
  are recorded *not run* with the reason.
- The App's Codex is imitated, not run; the model destination is never
  observed (OBS-1 pending).
