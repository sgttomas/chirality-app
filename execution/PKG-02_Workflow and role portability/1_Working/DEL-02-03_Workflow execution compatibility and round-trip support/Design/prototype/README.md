# EXEC-v0.6 design prototype (DEL-02-03) — not product code

This folder is a **design prototype** under R12-3 of run
`APP-V4-DESIGN-PASS-2-20260930`. It is not product code, selects no
implementation, placement (OI-013, OI-014), wire format, transport, hash or
persistence, and establishes nothing about a host, the supplier or a human
act. All subject matter is the invented FX-PIPE-01 fixture (C-v0.7 §10;
WD-EX-v0.7). Python 3 standard library only; nothing is installed and
nothing uses the network.

## What it shows

| File | Shows |
|---|---|
| `jsonschema_subset.py` | A small JSON Schema 2020-12 validator for the keyword subset the two schemas use: `$ref` (local `#/$defs/…`), `type`, `properties`, `required`, `additionalProperties`, `enum`, `const`, `items`, `minItems`, `minLength`, `pattern`, `minimum`, `oneOf`, `anyOf` (annotations ignored). Any other keyword raises an error, so no schema relies on an unchecked keyword |
| `fx_double.py` | A test-double catalog built from C §10.2 (editions e1/e2; variants V-X1, OP-C4 absent, OP-C5 absent, OP-C1 v2; the T8 unavailable case) and the fixture declared parts EXEC §7.1 uses (WD-EX E1, E1c, E1d, E5, E6 and the L-EXEC local variants, including L-EXEC-33, E1 with `CP-accept` declared `governed`) |
| `required_tool_check.py` | EXEC §3.4 EV-1…EV-11 (EV-3's harness-capability presence rule read through the EV-3a table, `harness_presence`, from node G), §3.5 (three-valued result; current phase and governance phase), §3.6 HS rows by held actions, PS-2/PS-4 wording; renders each report as a `compatibility-report.schema.json` instance |
| `checkpoint_recorder.py` | The current-phase recorder of EXEC §2.4 over scripted observations (already mapped to CE events; the native-item mapping of §2.5 is not exercised: its MCP-path cells stay OBS-1 pending, R13-6). It applies the §2.4.3 transition table with SP-6 (earlier act counts on current content), JA-1 (joint answer) and the lapse labels, and emits **recorder outputs** {RS entry kind, observed time, CE body} valid against `checkpoint-record-entries.schema.json`. Since the R14-1 repair it writes no container: RS format 0.1 is the one container, and DEL-04-03's `prototype/exec_to_rs.py` appends these outputs as RS entries and validates each. It has no operation that requests, pauses, refuses or prompts |
| `run_all.py` | Runs MT-1…MT-18 (current phase and governance phase) and the eighteen EV-3a presence readings (node G), CH-7/CH-8, CH-10, CH-20, CH-31 (i) and (ii), validates every report and every recorder output, and checks that the committed valid examples validate and that each invalid recorder output (INV-EXEC-1…7) and the invalid report are rejected |

## How to run

```sh
cd "…/DEL-02-03_…/Design/prototype"
PYTHONDONTWRITEBYTECODE=1 python3 run_all.py            # check only
PYTHONDONTWRITEBYTECODE=1 python3 run_all.py --write-examples   # regenerate the four example files
```

Exit status 0 means every expected result held. The recorded run (command,
date and output) is in the node's return file `WAVE_B/B2.md`.

## Limits

- The catalog and the host are test doubles; exposure is FXA-1; SWBPIPE's
  SQ-02 answer (route (iv)) is applied to surface X as EXEC does.
- The recorder's input is semantic. Whether stock Codex 0.158.0 delivers the
  native items in the order EXEC §2.5 assumes is not observed (OBS-1).
- App-side positive capture needs DEL-01-04's act control; here an App act
  record is a scripted test double.
