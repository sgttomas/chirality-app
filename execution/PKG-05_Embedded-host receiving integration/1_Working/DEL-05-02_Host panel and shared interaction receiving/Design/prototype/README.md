# DEL-05-02 prototype: scripted loop double and failure displays (not product code)

A local prototype under R12-3 of run `APP-V4-DESIGN-PASS-2-20260930`
(node B9). Python 3 standard library only. Nothing was installed. It is
**not product code** and not a panel: it chooses no wording, layout or
component, and shows nothing about any host.

## What it shows

- That the failure-display rules FD-1…FD-4 of PANEL-v0.8 §3.10 can be
  applied mechanically to a stream of loop events carrying LOOP-v0.8's
  event ordinal (E-6), including dropped events and a destination request
  left pending at run end.
- That `../PANEL_RETURN_INPUT.schema.json` accepts its valid example and
  refuses its invalid one.

It implements the replay and fault-injection part of the scripted loop
double described in PANEL-v0.8 §7.1. The return-input receiver and the
capture stand-in are described there, not built. The host-view double is
emulated by a list of unresolved references in the script.

## Files

| File | Role |
|---|---|
| `panel_double.py` | Replays each script, drops the listed ordinals, applies FD-1…FD-4, compares the display items with the expected ones |
| `fixtures/event_script.json` | Four scripts, PC-38…PC-41, invented example material on FX-PIPE-01 identifiers |
| `schema_subset.py` | Copy of DEL-05-01's `prototype/schema_subset.py` (same bytes), a validator for the JSON Schema 2020-12 subset the schemas use |

## How to run

```sh
cd prototype
python3 panel_double.py
python3 schema_subset.py ../PANEL_RETURN_INPUT.schema.json ../PANEL_RETURN_INPUT.example.valid.json ../PANEL_RETURN_INPUT.example.invalid.json
```

## Recorded run (2026-09-30, Python 3.13.7, macOS)

`python3 panel_double.py`:

```text
PASS PC-38: Model interface failure during a turn (FD-1)
     turn started
     model stream progress
     FD-1 model interface failure: ended-without-reason (reported by loop)
     FD-1 turn turn-3 failed: model interface failure; partial message shown as interrupted
PASS PC-39: A reference that no longer resolves (FD-2)
     reference ref:S-2@r12 ('S-2 (r12)')
     FD-2 reference ref:PR-1 no longer resolves; last known label 'PR-1' kept, marked unresolved
PASS PC-40: Missed events: ordinals 3 and 4 dropped in delivery (FD-3)
     turn started
     tool call received
     FD-3 events 3-4 not received; nothing inferred for them
     turn completed
PASS PC-41: A destination request still pending when the run ends (FD-4; request states are node B5's)
     destination request dr-1 for A-1 shown (ND-2)
     FD-4 destination request dr-1 for A-1: not answered, run ended; no grant shown; requesting call not sent
     run ended (person stopped)
4/4 scripts as expected
```

Schema examples:

```text
VALID   ../PANEL_RETURN_INPUT.example.valid.json
INVALID ../PANEL_RETURN_INPUT.example.invalid.json
    $: oneOf matched 0 branches [], exactly 1 required
```
