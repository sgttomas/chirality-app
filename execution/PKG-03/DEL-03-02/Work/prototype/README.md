# DEL-03-02 prototype — per-item transitions and the derived proposal state

**Not product code.** A local prototype under R12-3 (run
APP-V4-DESIGN-PASS-2-20260930, node B3): Python 3 standard library only.

`proposal_states.py` writes P-v0.8 §4.6 as executable rules:

- `TABLE`: the per-item transition table PT-1…PT-17 (from, event → to), with
  outcome unknown as an overlay that changes no state (PT-18, PT-19);
- `derive`: the derived proposal state DS-1…DS-4;
- a self-test of ten legal sequences (main timeline, V-S1, withdrawal, direct
  branch failure, partial application error, undo, lost observation, queue
  cleared by the person) and five illegal ones that the table must refuse;
- `--check RUN`: reads an SH-1 run (DEL-03-01 `Design/prototype`, C-v0.8
  §10.8) and checks that every observed item-state change is reachable in the
  table and that every derived state the double reported equals DS-1…DS-4;
- since the RP-2 repair (R14-8 N-18), `item_left_ok`: an item that left the
  queue carries its explicit item-left event (P §4.3) with the matching cause
  and a time, and no other item carries one; checked in the self-test and on
  every item of an SH-1 run.

The proposal and proposal-state schemas beside the Design file are validated
by DEL-03-01's `validate_all.py`. Nothing here is host behaviour: the table is
PROPOSED, and a host decides what it does (P §4.6).

```sh
python3 proposal_states.py --check "$TMPDIR/b3-sh1-run"
```

The observed output of the run of 2026-09-30 is recorded in `WAVE_B/B3.md`,
and that of the RP-2 rerun in `WAVE_B/RP-2.md`.
