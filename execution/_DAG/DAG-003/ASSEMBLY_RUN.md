# Assembly run — DAG-003 candidate

- **Run and node:** `APP-V4-SCA002-20260929`, node D1, 2026-09-29.
- **Actor:** Type 2 TASK executor, a Claude Code `Agent` subagent. Parent: HELP_HUMAN, integrating under a recorded WORKING_ITEMS consultation (`DISPATCH.md`). No delegation; Git read-only; no network.
- **Method:** `chirality-root:bundled:workflow:project-dag`, TRIGGER=SUCCESSOR, `CURRENCY_REPORT` = `_Evaluation/DAGCurrency/CURRENCY_APP_V4_SCA002_2026-09-29_2057/CURRENCY_REPORT.md`. Resources loaded: `contract.md`, `method.md`, `graph-version.md`, `currency.md`. Also `audit-dep-closure` (WORKFLOW, contract, method) and, for the case update, `scc-resolution-case`. Hashes of every loaded body are in `Evidence/Tool_Run.json`.
- **Precedent:** the DAG-002 preparation (`APP-V4-BASIS-ALIGN-20260928/DAG_PREP/`, `_DAG/_Candidates/DAG-002/`, `_DAG/DAG-002/`), followed stage for stage. The assembly script is DAG-002's, retargeted (both hashes in `Evidence/Tool_Run.json`).
- **Brief write boundary:** `_Evaluation/` (closure and currency snapshots and their `_LATEST.md`), this candidate folder, the SCC case files for evidence updates, and the run folder's `DAG_PREP/`. The host allows wider writes; nothing enforces this boundary at OS level.

## Stages performed

| Stage | Output |
|---|---|
| Stage 0: precondition and trigger | FULL_GRAPH (`_COORDINATION.md`); accepted decomposition GROUP3 through `_LATEST_ACCEPTED.md` (pointer text amended by B-06a, same snapshot named); accepted DAG-002 (§11.2 pointer); no open candidate; latest currency audit then `CURRENCY_APP_V4_DAG002_ACCEPTED_2026-09-29_1050` (CURRENT). Trigger SUCCESSOR from the accepted scope change SCA-V4-002 (DECISION-2, DECISION-3) applied to 9 SoWs and 11 registers |
| Freeze | `SOURCE_MANIFEST.sha256` over DAG-002's 130 paths at `8cd783d8d` (clean tree), verified against the committed bytes; 32 members changed since DAG-002 |
| Stage 2: closure | `_Evaluation/DepClosure/CLOSURE_APP_V4_SCA002_2026-09-29_2056`; observation pointer moved. Coverage PASS; six SCCs, identical members; 202 arcs |
| Currency audit | `_Evaluation/DAGCurrency/CURRENCY_APP_V4_SCA002_2026-09-29_2057`: DEPARTURE, +4 held arcs, 0 removed, 5 pending; observation pointer moved |
| Stage 1: candidate opened | `_DAG/_Candidates/DAG-003/` (next unused number), predecessor DAG-002 |
| Stage 3: coupled work | SCC-CASE-002 evidence update only (validator run recorded in its run record); other cases untouched |
| Stage 4: assembly | `Evidence/assemble_graph.py`, adapted from DAG-002's script. Strict audit exit 0. `Evidence/successor_currency_precheck.json`: the analyzer reports `NO_DEPARTURE_FOUND` against this candidate installed as DAG-003 in scratch |

## Not done here

- **Independent review.** It needs a separate TASK instance that did not assemble this candidate (graph-version rules; method Stage 4 step 3). Its `INDEPENDENT_REVIEW.md` is added to the candidate when returned.
- **Publication.** `ACCEPTANCE_RECORD.md`, `HANDOFF_STATE.md`, `MANIFEST.sha256`, the `_DAG/DAG-003/` copy and the pointer move all wait for the owner's decision. `PROPOSED_LATEST.md` is the prepared pointer text, with `{ACCEPT_DATE}` to be filled in.

## Written before checkpoint 2

`DAG_PREP/REVIEW_PACKET.md` in the run folder lists the SHA-256 of every file in this candidate as presented, as method Stage 4 step 4 requires (the predecessor's V12 F2 lesson). It states that checkpoints 1 and 2 are decided together.

## Protected inputs

`assemble_graph.py` hashes 399 protected files before and after assembly and asserts they are unchanged. They are DAG-001, DAG-002 and their candidate folders, `_DAG/_LATEST.md`, every `Dependencies.csv`, `_DEPENDENCIES.md`, `ScopeOfWork.md` and `_STATUS.md`, and the closure and currency snapshots.
