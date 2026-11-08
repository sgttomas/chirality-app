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

`schema_subset.py` exits with status 1 whenever any instance it is given is
invalid, so the commands above that pass the invalid example exit 1 by
design; the expected output is VALID for the valid example and INVALID for
the invalid one (RQ; V19-B n-7).

## Recorded run (2026-09-30, Python 3.13.7, macOS)

The 2026-09-30 Python 3.13.7 prototype run produced the expected displays
for PC-38…PC-41: interrupted model stream, unresolved reference, missing
event ordinals, and an unanswered destination request at run end. The schema
accepted the valid example and refused the invalid example. These are scripted
display results, not observations of a host panel.
