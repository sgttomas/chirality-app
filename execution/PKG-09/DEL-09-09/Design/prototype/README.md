# DEL-09-09 prototype — XT suite rehearsal, result records and the work account

**Not product code.** A local prototype under R12-3 (run
APP-V4-DESIGN-PASS-2-20260930, node B7): Python 3 standard library only, no
package installed, no network. It runs the XC and TR rehearsals that SH-1 can
carry, in the suite order of XT-v0.6 §3.5 (segments, saved branch points,
set-up and reset per case), and shows that the PROPOSED formats of XT-v0.6
§3.4 (`../xt-result-record.schema.json`) and §5.1–§5.2
(`../xt-work-account.schema.json`) can be produced and validated.

| File | What it shows |
|---|---|
| `run_xt_suite.py` | Drives **SH-1**, the one simulated host (DEL-03-01 C-v0.8 §10.8), over both native paths through its driver `run_fixture.py`; forks saved states for the branch segments (B-T9, B-T10, B-T11) and resets by discarding them; maps the imitated native items with ADAPTER-v0.6's mapper (`observe_map.py`) for the App-side records; writes one XT result record per case and the V-ED1 work account for OP-C9 tied to C §8's rows; validates them and the committed example instances with DEL-03-01's subset validator |

The round-1 prototypes are imported read-only from their own folders and are
not changed; `sys.dont_write_bytecode` keeps their folders free of caches.

## Run

```sh
cd "<this folder>/.."
python3 -B prototype/run_xt_suite.py --out "$TMPDIR/b7-xt"
# --write-examples regenerates the four xt-*.example.*.json files
```

Exit status 0 only if every check holds. The observed output of the run of
2026-09-30 is recorded in XT-v0.6 §3.6 and in
`_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/WAVE_B/B7.md`.

**RP-4 (2026-09-30).** Evidence limits are written in RS R11's own spelling
(the mapper's tokens are mapped once) and checked against the labels of
DEL-04-03's `RS_RECORD.schema.json`. Rerun output in `WAVE_B/RP-4.md`. The
result-record examples record the sha256 of the other prototypes' files, so
they are regenerated (`--write-examples`) whenever those change.

## Limits

- Everything is *test-double* evidence. XF rehearsals never complete an XC
  case (XT §0); no record counts toward V4-EXM-25 or V4-EXM-24.
- SH-1 has no H or E surface, no per-surface exposure element, no host views
  or selection, no A4 facility, no origin mark on the applied association,
  no restart of its own records, no OP-C10 or OP-C11 and no checkpoint
  declarations (C §10.8). Parts that need these are recorded *not run* with
  the reason. Every TR comparison is therefore *not comparable* (X only).
- The work account rows for X describe the double's own route (it renders
  its catalog from the edition), not any host's.
