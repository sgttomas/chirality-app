# DEL-01-01 prototype — supplier double, boundary model, schema checks

**This is a design prototype, not product code.** It belongs to
DEL-01-01/HOSTING-BOUNDARY-v0.8 (§9.6) and was written by node B6 of run
`APP-V4-DESIGN-PASS-2-20260930` under R12-3. It is not an App candidate, not
the O-1 proposal of HOSTING §12, and nothing in it is qualified or selected.
Python 3 standard library only; no package is installed; no network is used;
the Codex binary is never started.

## What it shows

| File | Role |
|---|---|
| `supplier_double.py` | A stand-in for the stock Codex App Server 0.158.0 on stdio. It replays the supplier frames recorded in the eight committed, redacted spike transcripts (`../generated/0.158.0/_spike/transcripts/`) and labels every frame it writes `recorded`, `mutated` (identity or method name substituted) or `constructed` (HOSTING §9.2). |
| `double_scenarios.py` | The constructed scenarios (server requests, items, malformed lines, exits) for the cases. All content is invented example material. |
| `boundary_model.py` | An executable model of the HOSTING rules (H1–H11, §4 lifecycle with the §4.7 table, §5 client requests, §6 register with R1–R9 and the §6.2.1 table, §8.3 destination facts). Numbers the design leaves open are marked TEST VALUE. |
| `run_cases.py` | Runs the cases HOSTING marks runnable with a double, the double's fidelity checks, the transition-table and capability-account checks against `../HOSTING_BOUNDARY.md`, the schema checks, and a local check of the OBS-1 test tools. Exit status 0 when every result is as expected. |
| `jsonschema_subset.py` | A small validator for the JSON Schema keywords used here: type, enum, const, properties, required, additionalProperties, items, minItems, minimum, minLength, pattern, oneOf, anyOf, allOf, if/then/else, not, local `$ref`. Anything else raises an error. |
| `fixtures/` | A valid and an invalid instance for each PROPOSED schema beside HOSTING (`../hosting.*.schema.json`). |
| `obs1_mcp_double.py`, `obs1_cli_tool.py` | Test tools for the OBS-1 observation (MCP path and command-line path). Invented data only. |
| `results/RUN_2026-09-30.txt` | The recorded output of the run below. |

A "pass (model)" means the rules ran as written against the double, with
this model standing in for the App side. It is evidence about the design,
never a VER pass: no App candidate exists.

The model validates answers and the double's constructed frames against the
committed JSON Schema bundle for convenience. That is not a choice of the
reference output (HOSTING U-15, F-29).

## How to run

```sh
cd "<this folder>"
python3 run_cases.py              # prints one line per case; exit 0 = all as expected
python3 run_cases.py --keep-logs  # also prints the temporary log folders
```

Logs (the double's frame logs) go to temporary folders under `$TMPDIR`.
A run takes about 20 seconds.

## Run recorded

- Date: 2026-09-30; host: macOS (Darwin 25.6.0, arm64); Python 3.13.7.
- Command: `python3 run_cases.py` in this folder.
- Output: `results/RUN_2026-09-30.txt` (35 results, all as expected).
- Rerun after the RP-3 repair (HOSTING §8.4 annotations and §10.1; no prototype file changed): `results/RUN_2026-09-30_RP-3.txt` (35 results, all as expected). The name-to-group check of WD §4.2.5 against §8.4 (HOSTING VC-31) runs in DEL-02-01's prototype (`wdproto.py selftest`, S-11).

CC-H (2026-10-04) candidate: internal counters and correlation maps are scoped to
one Boundary instance/session/home; records() and delivered envelopes export the
full H5 identity. The counter is never a standalone persisted identity. LT-24
keeps unverifiable and labels the ready announcement unverified-development.
Original verification/qualification obligations remain unchanged.

CC-H independent-review repair: answer() accepts a full current generation
object and refuses a foreign session/home/counter or bare integer; its internal
cache remains instance-scoped. Server-request schema successor is v0.10.

SUP1: this prototype remains a historical 0.158.0 record/type model. Its
constants and expected rows are not the maintained product development pin;
HOSTING §7.0/generated/0.160.0 supplies that pin. Historical observations are
not silently relabelled at the adopted version. New product qualification
and connected consumer replay remain manager/receiving-owner work.
