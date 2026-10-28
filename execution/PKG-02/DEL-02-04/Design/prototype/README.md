# ROLE-v0.2 design prototype (DEL-02-04)

A design prototype for `../ROLE_SUPPLY.md` §10 (R17-1, R12-3). It is not
product code and qualifies nothing. Python 3 standard library only; no
install, no network, no Codex process. The supplier is a test double that
answers in the shapes of the 0.158.0 generated types and with the behaviour
OBS-2 and OBS-3 observed at 0.158.0 (resume and fork ignore new instructions).

| File | What it is |
|---|---|
| `role_supply.py` | Role set, guidance store (seed, state, restore, release upgrade), role-only composition, request check, native child-role configuration, start and fork records, guidance-changed check, limit account, child discovery and delegation observation, the T-2 state machine with "Continue as" |
| `jsonschema_lite.py` | A JSON Schema 2020-12 keyword-subset validator; refuses any keyword it does not check |
| `run_cases.py` | Cases RC-01…RC-20 |
| `fixtures/` | Invented guidance, role set and item notifications. Not the App's guidance and not Root's |
| `results/` | Recorded runs (`run-2026-10-01.txt` is ROLE-v0.1's; `run-2026-10-02.txt` is v0.2's) |

Run from this folder:

    python3 run_cases.py --record                    # cases; writes results/run-<date>.txt
    python3 run_cases.py --write-examples --record   # also rewrites the four example files beside ROLE_SUPPLY.md

Scratch files are made in a fresh folder under `$TMPDIR` and removed at the
end. New App-produced content identities use CC-CONTENT-IDENTITY
`chirality.app.exact-bytes.sha256/v1`, SHA-256 over exact bytes. Historical
fixtures retain their old method designation; HOSTING's wider U-08 and
host-native methods remain open. The suite includes a known vector and
line-ending/Unicode sensitivity checks.

## Current receiving pin and historical double

CC-ROLE-PIN-0160 maintains0.160.0 for the App's generic primary role carrier;
`../ROLE_PIN_0.160.0.md` identifies the independently reviewed HELP_HUMAN
capture-only sample and its limits. This prototype remains a **historical
0.158.0-shaped invented supplier double**: its pin defaults, adapter/child
assumptions and resume/fork outcomes are not silently relabelled0.160.0 native
evidence. Run the existing suite without --record/--write-examples to verify
unchanged source/role/request/record meaning. It proves no new native carrier,
other/no-role case, lifetime, child availability, model adoption or qualification.
