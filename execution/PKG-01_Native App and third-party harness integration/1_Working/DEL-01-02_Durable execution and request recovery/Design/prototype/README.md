# DEL-01-02 prototype — recovery model and supplier stub

**This is a design prototype, not product code.** It belongs to
DEL-01-02/RECOVERY-v0.1 (`../EXECUTION_AND_RECOVERY.md` §11.2) and was
written by node D1 of run `APP-V4-DESIGN-PASS-3-20261001` under R17-1 and
R12-3. It is not an App candidate and not the OI-008 O-1 proposal realized.
Python 3 standard library only; no package is installed; no network is used;
the Codex binary is never started; no model is run.

| File | Role |
|---|---|
| `supplier_stub.py` | An in-memory stand-in for the parts of Codex App Server 0.158.0 the design relies on (thread and turn status, `turn/interrupt`, `thread/resume`, `thread/read`, `thread/turns/list`, `serverRequest/resolved`, `thread/closed`, child threads). Every behaviour is **constructed** from the generated types and the design's assumptions. Where the live behaviour is not observed (OBS-2 items O-1, O-2, O-4), it offers **variants**, and the cases run under each |
| `recovery_model.py` | An executable model of the design's five transition tables (AS, CV, OA, SR, RQ) and its sequences, over a simplified stand-in for DEL-01-01's seam S-1 (generations, register, client requests). Open numbers are TEST VALUES |
| `run_cases.py` | Cases C-01…C-12: observer loss, interrupt under every variant, request settlement, unknown request and lost acknowledgment, supplier exit and recovery, quit and relaunch (K-4), App killed, the handoff's refusal of stronger claims, the schemas and their examples, equality of the Design file's tables with the model, no content in the ledger, and coverage of every table row. Exit status 0 when every result is as expected |
| `results/RUN_2026-10-01.txt` | The recorded run |

The JSON Schema validator is DEL-01-01's
`../../../DEL-01-01_Stock Codex hosting and supplier contract/Design/prototype/jsonschema_subset.py`
(sha256 486e9286e5aa56888b5473f1c08493a115591255685a8a7bb88b93ff2cacffc0 at
this run), imported read-only; DEL-01-02 consumes DEL-01-01 (DEP-01-02-018).
The ledger the model writes goes to a temporary folder under `$TMPDIR`.

## How to run

```sh
cd "<this folder>"
python3 run_cases.py
```

## Run recorded

- Date 2026-10-01; macOS (Darwin 25.6.0, arm64); Python 3.13.7.
- `python3 run_cases.py`: 12 results, 12 as expected (exit status 0).

"PASS" means the design's rules ran as written against the stub under every
variant the case lists. It is evidence about the design only: no VER
criterion is passed (no candidate exists), and it shows nothing about which
variant the supplier really exhibits.
