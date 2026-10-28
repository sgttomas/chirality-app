# Assembly run — DAG-004 candidate

- **Run and node:** `APP-V4-SCA003-20261002`, node D1, 2026-10-03 (from 19:36 MDT).
- **Actor:** Type 2 TASK executor, a Claude Code `Agent` subagent. Parent: HELP_HUMAN, integrating under a recorded WORKING_ITEMS consultation (`RUN/BRIEFS.md`, `RUN/DISPATCH.md`). No delegation; Git read-only; no network.
- **Method:** `chirality-root:bundled:workflow:project-dag`, TRIGGER=SUCCESSOR, `CURRENCY_REPORT` = `DAG_PREP/CURRENCY_APP_V4_SCA003_2026-10-03_1937/CURRENCY_REPORT.md`. Resources loaded: `WORKFLOW.md`, `contract.md` (layout section), `method.md`, `graph-version.md`, `currency.md`. Hashes of the loaded bodies and the run records read are in `Evidence/Tool_Run.json` (`selected_context`).
- **Precedent:** the DAG-003 preparation (`APP-V4-SCA002-20260929/DAG_PREP/`, its DISPATCH rows D1, V15 and D2, and the published `_DAG/DAG-003/`), followed stage for stage. The assembly script is DAG-003's, retargeted and made location-independent (both hashes in `Evidence/Tool_Run.json`).
- **Brief write boundary:** the run folder's `DAG_PREP/` and scratch under `$TMPDIR`. The host allows wider writes; nothing enforces this boundary at OS level. Checked at the end with `git status --short` (only `DAG_PREP/` is new).

## Departures from the precedent, because of the fence

| Precedent (SCA-V4-002 D1) | Here | Consequence |
|---|---|---|
| Closure snapshot in `_Evaluation/DepClosure/`, pointer moved | `DAG_PREP/CLOSURE_APP_V4_SCA003_2026-10-03_1936/`; no pointer moved | Copy to `_Evaluation/DepClosure/` at publication (optional for the graph; the candidate cites it by path) |
| Currency audit in `_Evaluation/DAGCurrency/`, pointer moved | `DAG_PREP/CURRENCY_APP_V4_SCA003_2026-10-03_1937/`; **`_Evaluation/DAGCurrency/_LATEST.md` still names the CURRENT observation of 2026-09-29** | Copy and move the pointer as soon as authorized, so that consumers reading the pointer see the 11 `DAG pending` deliverables |
| Candidate in `_DAG/_Candidates/DAG-003/` | `DAG_PREP/DAG-004/` | Copy byte for byte to `_DAG/_Candidates/DAG-004/` (and on acceptance to `_DAG/DAG-004/`), verified against `DAG_PREP/REVIEW_PACKET.md` |
| CASE-002 evidence update written in the case files | Drafted only: `DAG_PREP/CASE-002_EVIDENCE_UPDATE.proposed.md` | Apply through `scc-resolution-case` before or at publication |

## Stages performed

| Stage | Output |
|---|---|
| Stage 0: precondition and trigger | FULL_GRAPH; accepted decomposition GROUP3 through `_LATEST_ACCEPTED.md` (byte-unchanged); accepted DAG-003 (§11.2 pointer, MANIFEST 37/37 OK); no open candidate (`_Candidates/` holds DAG-001…003); no `REJECTION_RECORD.md`; latest currency observation `CURRENCY_APP_V4_DAG003_ACCEPTED_2026-09-29_2218` (CURRENT). Trigger SUCCESSOR from the accepted scope change SCA-V4-003 applied to 19 SoWs and 20 registers |
| Freeze | `SOURCE_MANIFEST.sha256` over DAG-003's 130 paths, same order, at `75764184b9` (clean tree); each member checked against the working bytes and `git show` of the commit; 59 members changed since DAG-003 |
| Stage 2: closure | `DAG_PREP/CLOSURE_APP_V4_SCA003_2026-10-03_1936/`: coverage PASS; six SCCs, `scc_summary.csv` byte-identical to SCA-V4-002's; 212 arcs |
| Currency audit | `DAG_PREP/CURRENCY_APP_V4_SCA003_2026-10-03_1937/`: DEPARTURE, +10 arcs (5 admitted, 5 held), 0 removed, 11 pending |
| Stage 1: candidate opened | DAG-004 (next unused number), predecessor DAG-003 |
| Stage 3: coupled work | No SCC formed, changed or dissolved. CASE-002 update drafted, not applied (fence) |
| Stage 4: assembly | `Evidence/assemble_graph.py`. Strict audit exit 0. `Evidence/successor_currency_precheck.json`: the analyzer reports `NO_DEPARTURE_FOUND` against this candidate installed as DAG-004 in scratch |

## Not done here

- **Independent review.** It needs a separate TASK instance that did not assemble this candidate (graph-version rules; method Stage 4 step 3). Its `INDEPENDENT_REVIEW.md` is added when returned.
- **Publication.** `ACCEPTANCE_RECORD.md`, `HANDOFF_STATE.md`, `MANIFEST.sha256`, the `_DAG/` copies and the pointer move all wait for the owner's decision. `PROPOSED_LATEST.md` is the prepared pointer text, with `{ACCEPT_DATE}` to be filled in. It cites the currency audit at its `_Evaluation/DAGCurrency/` home, so that copy must precede or accompany publication.

## Written before the checkpoint

`DAG_PREP/REVIEW_PACKET.md` lists the SHA-256 of every file in this candidate as presented (method Stage 4 step 4).

## Protected inputs

`assemble_graph.py` hashes the protected files (729 at the final run) before and after assembly and asserts they are unchanged. The script was run twice; the second run (after the closure and currency records were completed) reproduced every candidate file byte for byte except `Evidence/Tool_Run.json` (`finished_at`) and `Evidence/AssemblyChecks.json` (`protected_input_count` 725 → 729, the four snapshot records written in between). The protected set is DAG-001…003, `_DAG/_Candidates/`, `_DAG/cases/`, `_DAG/_LATEST.md`, every `Dependencies.csv`, `_DEPENDENCIES.md`, `ScopeOfWork.md` and `_STATUS.md`, all of `_Evaluation/`, and this run's closure and currency snapshots.
