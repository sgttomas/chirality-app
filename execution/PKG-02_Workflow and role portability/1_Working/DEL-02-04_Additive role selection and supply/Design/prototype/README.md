# ROLE-v0.1 design prototype (DEL-02-04)

A design prototype for `../ROLE_SUPPLY.md` §10 (R17-1, R12-3). It is not
product code and qualifies nothing. Python 3 standard library only; no
install, no network, no Codex process. The supplier is a test double that
answers in the shapes of the 0.158.0 generated types.

| File | What it is |
|---|---|
| `role_supply.py` | Role set, guidance store (seed, state, restore, release upgrade), composition, request check, native child-role configuration, supply records, limit account, delegation observation, the T-2 selection state machine |
| `jsonschema_lite.py` | A JSON Schema 2020-12 keyword-subset validator; refuses any keyword it does not check |
| `run_cases.py` | Cases RC-01…RC-20 |
| `fixtures/` | Invented guidance, role set, workflow and item notifications. Not the App's guidance and not Root's |
| `results/` | Recorded runs |

Run from this folder:

    python3 run_cases.py --record                    # cases; writes results/run-<date>.txt
    python3 run_cases.py --write-examples --record   # also rewrites the four example files beside ROLE_SUPPLY.md

Scratch files are made in a fresh folder under `$TMPDIR` and removed at the
end. The content-identity method in every record is the illustration
`proto-sha256-0`; the algorithm is open (HOSTING U-08).
