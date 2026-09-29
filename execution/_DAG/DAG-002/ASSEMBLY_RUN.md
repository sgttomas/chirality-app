# Assembly run — DAG-002 candidate

- **Run and node:** `APP-V4-BASIS-ALIGN-20260928`, node D1, 2026-09-29.
- **Actor:** Type 2 TASK executor, a Claude Code `Agent` subagent. Parent: HELP_HUMAN, integrating under a recorded WORKING_ITEMS consultation (`DISPATCH.md`). No delegation; Git read-only; no network.
- **Method:** `chirality-root:bundled:workflow:project-dag`, TRIGGER=SUCCESSOR, `CURRENCY_REPORT` = `_Evaluation/DAGCurrency/CURRENCY_APP_V4_BASISALIGN_2026-09-29_0856/CURRENCY_REPORT.md`. Resources loaded: `contract.md`, `method.md`, `graph-version.md`, `currency.md`. Also `audit-dep-closure` and, for the case update, `scc-resolution-case`. Hashes of every loaded body are in `Evidence/Tool_Run.json`.
- **Brief write boundary:** `_Evaluation/` (closure and currency snapshots and their `_LATEST.md`), this candidate folder, the SCC case files for evidence updates, and `DAG_PREP/CHECKPOINT_C.md` in the run folder. The host allows wider writes; nothing enforces this boundary at OS level.

## Stages performed

| Stage | Output |
|---|---|
| Stage 0: precondition and trigger | FULL_GRAPH; accepted decomposition GROUP3; accepted DAG-001 (prose pointer; see the pointer finding); no open candidate; latest currency audit then `CURRENCY_APP_V4_ACCEPTANCE_2026-09-28` (CURRENT). Trigger SUCCESSOR from the accepted SCA-V4-001 change |
| Freeze | `SOURCE_MANIFEST.sha256` over DAG-001's 130 paths at `b585e5ebe` (clean tree), verified against the committed bytes |
| Stage 2: closure | `_Evaluation/DepClosure/CLOSURE_APP_V4_BASISALIGN_2026-09-29_0855`; observation pointer moved |
| Currency audit | `_Evaluation/DAGCurrency/CURRENCY_APP_V4_BASISALIGN_2026-09-29_0856`: DEPARTURE, 15 pending; observation pointer moved |
| Stage 1: candidate opened | `_DAG/_Candidates/DAG-002/` (next unused number), predecessor DAG-001 |
| Stage 3: coupled work | SCC-CASE-002 evidence update only (validator PASS); other cases untouched |
| Stage 4: assembly | `Evidence/assemble_graph.py`, adapted from DAG-001's script (both hashes in `Evidence/Tool_Run.json`). Strict audit exit 0 |

## Not done here

- **Independent review.** It needs a separate TASK instance that did not assemble this candidate (graph-version rules; SUCCESSOR_PLAN §7).
- **`REVIEW_PACKET.md`.** It records the hashes presented at checkpoint C and is written by the integrator after the review. The current hashes of every file are in the D1 return and in `DAG_PREP/CHECKPOINT_C.md`.
- **Publication.** `ACCEPTANCE_RECORD.md`, `HANDOFF_STATE.md`, `MANIFEST.sha256`, the `_DAG/DAG-002/` copy and the pointer move all wait for the owner's decision. `PROPOSED_LATEST.md` is the prepared pointer text, with `{ACCEPT_DATE}` to be filled in.

## Protected inputs

`assemble_graph.py` hashes 308 protected files before and after assembly and asserts they are unchanged. They are DAG-001 and its historical candidate folder, `_DAG/_LATEST.md`, every `Dependencies.csv`, `_DEPENDENCIES.md`, `ScopeOfWork.md` and `_STATUS.md`, and the closure snapshot.
