# DEL-01-02 prototype — recovery model and supplier stub

**This is a design prototype, not product code.** It belongs to
DEL-01-02/RECOVERY-v0.2 (`../EXECUTION_AND_RECOVERY.md` §11.2) and was
written by node D1 of run `APP-V4-DESIGN-PASS-3-20261001` under R17-1 and
R12-3 (round 1, 2026-10-01; round 2, 2026-10-02). It is not an App candidate and not the OI-008 O-1 proposal realized.
Python 3 standard library only; no package is installed; no network is used;
the Codex binary is never started; no model is run.

| File | Role |
|---|---|
| `supplier_stub.py` | An in-memory stand-in for the parts of Codex App Server 0.158.0 the design relies on (thread and turn status, `turn/interrupt`, `thread/resume`, `thread/read`, `thread/turns/list`, `serverRequest/resolved`, `thread/closed`, child threads). Every behaviour is **constructed**; since round 2 its default behaviour copies what OBS-2 observed at 0.158.0 (interrupt order, a held request resolved by Codex, items never completed, `cancel` interrupting the turn, history after a stop, no re-raise; children announced by the parent's item, through an adapter). The other **variants** are kept as defences, and the cases run under each |
| `recovery_model.py` | An executable model of the design's five transition tables (AS, CV, OA, SR, RQ) and its sequences, over a simplified stand-in for DEL-01-01's seam S-1 (generations, register, client requests), with one Codex child per App-owned home (DECISION-L L-1). Open numbers are TEST VALUES |
| `run_cases.py` | Cases C-01…C-11 and C-13…C-17: observer loss, interrupt under every variant (with G-4), request settlement, unknown request and lost acknowledgment, supplier exit and recovery, quit and relaunch (K-4, with G-5), App killed, the handoff's refusal of stronger claims, the schemas and their examples, equality of the Design file's tables with the model, no content in the ledger, two App-owned homes, the cancel-answer cause, runs in sequence and a fork, Stop and Restart Codex, and coverage of every table row. Exit status 0 when every result is as expected |
| `results/RUN_2026-10-01.txt` | The recorded run of round 1 (v0.1), kept |
| `results/RUN_2026-10-02.txt` | The recorded run of round 2 (v0.2) |

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

- Round 1: 2026-10-01; macOS (Darwin 25.6.0, arm64); Python 3.13.7; `python3 run_cases.py`: 12 results, 12 as expected (exit status 0).
- Round 2: 2026-10-02; same host and Python; `python3 run_cases.py`: 16 results, 16 as expected (exit status 0).

"PASS" means the design's rules ran as written against the stub under every
variant the case lists. It is evidence about the design only: no VER
criterion is passed (no candidate exists), and it shows nothing about which
variant the supplier really exhibits.

CC-REC-GEN: `python3 -B check_generation_ref.py` checks full-tuple tagged UTF-8-hex references; `run_cases.py` uses this encoding after each scripted actual spawn. Earlier results remain evidence of their historical fixture representation. No schema shape or supplier wire field changes.

CC-REC-RT-LINK: the later-error check receives reviewed HOSTING RT-14/RT-15, with full-generation/request and open-generation guards; receipt RT-02/03 and failed-write uncertainty remain separate.

CC-REC-ATTACHMENT-PROJECT-CONTEXT: `python3 -B check_project_context.py` checks existing0.2 shape, no-row unknown, historical/current distinction and opaque NIR owner codec. Values are scripted source classifications, not production trusted Root context or native proof; no index/schema kind bump.
