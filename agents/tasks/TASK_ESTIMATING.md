# TASK_ESTIMATING — DAG-Directed Estimating Run Brief

## 1) Assignment
Run the estimating process for `execution-7` through the hardened DAG direction, using `WORKING_ITEMS` as the operator-facing manager and `AGENT_ESTIMATING.md` as execution basis.

This brief is the single task contract for the run.

## 2) Agent Routing
- Primary persona interface: `WORKING_ITEMS` (`agents/AGENT_WORKING_ITEMS.md`)
- Task-execution basis: `AGENT_ESTIMATING` (`agents/AGENT_ESTIMATING.md`) when present; otherwise this task file Section 11A is authoritative for estimate schema and fallback behavior
- Design standard basis: `AGENT_HELPS_HUMANS` (`agents/AGENT_HELPS_HUMANS.md`)

Execution posture:
- Persona-managed orchestration (`WORKING_ITEMS`)
- Straight-through task behavior (`AGENT_ESTIMATING`)
- Filesystem-grounded outputs with write quarantine

## 3) Startup Read Order (Mandatory)
1. `README.md`
2. `AGENTS.md`
3. `test/execution-7/INIT-PERSONA.md`
4. `agents/AGENT_WORKING_ITEMS.md`
5. `agents/AGENT_ESTIMATING.md` (if present). If archived/missing, use Section 11A in this file as the execution contract for `Detail.csv` and fallback rules.

## 4) Authoritative DAG Control Snapshot (Mandatory)
Use this hardened snapshot as dependency authority:
- `test/execution-7/_Estimates/EST_DAG_HARDENED_2026-02-06_1623/`

Mandatory control files:
- `nodes.csv`
- `edges.csv`
- `topo_order.csv`
- `blocker_report.csv`
- `execution_plan.md`
- `WBS_CBS_Matrix.csv`
- `Summary.md`
- `QA_Report.md`
- `Decision_Log.md`
- `Source_Index.md`

## 5) Objective and DAG Sequence
Execute estimating in this run order:
- `DEL-02-01/02/03 -> DEL-02-04 -> DEL-02-07/08 -> DEL-02-09/10`

Checkpoint classification:
- BLOCKING: `DEL-04-01`, `DEL-04-02`, `DEL-04-03`, `DEL-08-01`, and hard gate `DEL-02-01 -> DEL-02-02`
- ADVISORY: `DEL-05-01`, `DEL-05-02`, `DEL-06-01`, `DEL-06-02`, `DEL-09-01`, `DEL-09-02`

## 6) Scope and Permissions
Read scope:
- Cross-deliverable reads are allowed and required.

Write scope:
- Write only under: `test/execution-7/_Estimates/`
- Do not edit files under: `test/execution-7/PKG-*/1_Working/`
- Do not modify any `_STATUS.md`

Explicit prohibition:
- `agents/AGENT_TASK_SETUP.md` was intentionally deleted by user. Do not investigate, restore, or reference recovery actions.

## 7) Git Worktree Governance (Mandatory for Parallel Runs)
This policy applies whenever two or more estimating runs are active concurrently.

### 7.1 Naming
- `RunID` format: `YYYYMMDD-HHMM-{owner}`
- Integration branch: `est/ex7/integration`
- Run branch: `est/ex7/run-{RunID}`
- Optional stage branch: `est/ex7/run-{RunID}-stage-{a|b|c|d}`
- Worktree path: `../chirality-app-test__wt__ex7__{RunID}`

### 7.2 Ownership
- Integration Owner: single authority for merge selection, merge execution, and authoritative pointer updates.
- Run Owner: one owner per run branch/worktree; responsible for all commits, diagnostics, and per-run tracking on that branch.
- A worktree MUST have exactly one active Run Owner at a time.
- Run Owners MUST NOT commit directly to `est/ex7/integration`.

### 7.3 Merge Order (DAG-Gated)
- Stage acceptance order is mandatory: `A -> B -> C -> D`.
- Stage B artifacts MUST NOT merge unless Stage A is accepted on integration.
- Stage C artifacts MUST NOT merge unless Stage B is accepted on integration.
- Stage D artifacts MUST NOT merge unless Stage C is accepted on integration.
- If parallel runs compete at the same stage, the Integration Owner selects one winner for merge using:
  - DAG integrity pass
  - blocker reduction quality
  - evidence traceability quality
  - scope compliance (no writes outside `_Estimates`)
- Non-winning branches remain audit artifacts or are closed; they are not merged by default.

### 7.4 `_LATEST.md` Update Authority
- Only the Integration Owner may update `test/execution-7/_Estimates/_LATEST.md` on `est/ex7/integration`.
- Run branches may maintain branch-local `_LATEST.md` for local execution context, but it is non-authoritative.
- On merge conflicts involving `_LATEST.md`, keep integration authority unless the Integration Owner explicitly approves replacement.

### 7.5 Tracker Authority
- Per-run trackers (run branch):
  - `test/execution-7/_Estimates/_RUN_PROGRESS_{RunID}.md`
  - `test/execution-7/_Estimates/_RUN_PROGRESS_{RunID}.csv`
- Shared consolidated trackers (integration branch):
  - `test/execution-7/_Estimates/_RUN_PROGRESS.md`
  - `test/execution-7/_Estimates/_RUN_PROGRESS.csv`
- Run Owner updates per-run trackers.
- Integration Owner updates shared consolidated trackers after each accepted merge.

## 8) Human Decision Rights vs Agent Rights
Human-owned decisions:
- Lifecycle transitions and `_STATUS.md` changes
- Scope boundary changes
- Acceptance of any blockers that cannot be resolved from existing project state

Agent-execution rights:
- Re-check readiness and blockers from current filesystem state
- Execute DAG-directed estimating stages
- Publish estimate snapshot diagnostics and outputs in `_Estimates`
- Update branch-local `_LATEST.md` only on run branch; do not update authoritative integration `_LATEST.md` unless you are Integration Owner

## 9) Required Run Behavior
1. Re-read all relevant `_STATUS.md` files and compare to `blocker_report.csv`.
2. Execute Stage A through Stage D from `execution_plan.md` in order.
3. Use `edges.csv` as dependency authority for sequencing decisions.
4. If blockers prevent full completion, publish a non-blocking partial snapshot with explicit diagnostics and unblock plan.
5. If full run is feasible, produce a standard `AGENT_ESTIMATING` snapshot artifact set, including `Detail.csv`.
6. On run branches, update only branch-local pointers/trackers; leave integration `_LATEST.md` to Integration Owner per Section 7.

## 10) Progress Tracker Updates (Mandatory)
For non-parallel single-run mode, update shared trackers under `_Estimates`:
- `test/execution-7/_Estimates/_RUN_PROGRESS.md`
- `test/execution-7/_Estimates/_RUN_PROGRESS.csv`

For parallel worktree mode, update per-run trackers:
- `test/execution-7/_Estimates/_RUN_PROGRESS_{RunID}.md`
- `test/execution-7/_Estimates/_RUN_PROGRESS_{RunID}.csv`

Required update cadence:
1. On assignment start (set `run_status`, baseline snapshot, initial blockers, next action).
2. After completion of each stage/task segment (A, B, C, D), update stage status and counts.
3. After any blocker state change (new blocker, resolved blocker, or severity change), update blockers and next action.
4. On assignment completion, set final `run_status` and final stage states.

Minimum fields to refresh each update:
- `as_of`
- `run_id`
- `branch`
- `worktree_path`
- `run_owner`
- `run_baseline`
- `run_status`
- `stage_a`, `stage_b`, `stage_c`, `stage_d`
- `active_blockers`
- `top_blocker_1` ... `top_blocker_5`
- `next_action`

Status values:
- Run: `NOT_STARTED | IN_PROGRESS | BLOCKED | OK | WARNINGS | FAILED_INPUTS`
- Stage: `NOT_STARTED | IN_PROGRESS | BLOCKED | DONE`

Integration update rule:
- After accepted stage/run merge, Integration Owner copies run outcomes into shared trackers (`_RUN_PROGRESS.md/.csv`) and records the accepted `RunID`.

## 11) Output Contract
Each run must publish a new immutable snapshot folder under:
- `test/execution-7/_Estimates/EST_{Label}_{YYYY-MM-DD}_{HHMM}/`

At minimum include:
- `BOE.md`
- `Summary.md`
- `Source_Index.md`
- `Decision_Log.md`
- `Assumptions_Log.md`
- `Risk_Register.md`
- `QA_Report.md`
- `Change_Log.md`
- `WBS_CBS_Matrix.csv`

For full estimating runs also include:
- `Detail.csv`

### 11A) Canonical `Detail.csv` Schema (Required)

When `Detail.csv` is produced, the following columns are mandatory and must be populated on every row:

- `LineID`
- `CBS`
- `WBS_PackageID`
- `WBS_DeliverableID`
- `Description`
- `Qty`
- `Unit`
- `UnitRate`
- `Amount`
- `Currency`
- `Method` (`QUOTE|RATE_TABLE|HISTORICAL|ALLOWANCE|PARAMETRIC`)
- `SourceRef` (file path + section or assumption/decision reference)
- `Confidence` (`LOW|MED|HIGH`)
- `Notes`

Allowance/parametric convention (mandatory):
- Set `Qty = 1`
- Set `Unit = LS`
- Set `UnitRate = Amount`

If quote/rate-table sources are unavailable, fallback pricing is allowed using `ALLOWANCE`/`PARAMETRIC`, but assumptions and decision rationale must be recorded in:
- `Assumptions_Log.md`
- `Decision_Log.md`

`RUN_STATUS` guidance:
- `OK`: no critical failures and outputs are meaningful
- `WARNINGS`: material assumptions/ambiguities remain
- `FAILED_INPUTS`: inputs insufficient for meaningful totals

For DAG-directed run control include:
- `nodes.csv` (if updated)
- `edges.csv` (if updated)
- `topo_order.csv`
- `blocker_report.csv`
- `execution_plan.md`

For parallel worktree mode also include:
- `_RUN_PROGRESS_{RunID}.md`
- `_RUN_PROGRESS_{RunID}.csv`

## 12) Acceptance Criteria
- DAG remains acyclic.
- No writes occur under `PKG-*/1_Working`.
- `_STATUS.md` files remain unchanged.
- Every dependency claim used in summary is evidence-linked.
- Snapshot is created even when blocked (`RUN_STATUS = WARNINGS` or `FAILED_INPUTS` as applicable).
- Progress trackers are updated at assignment start, after each stage/task completion, and at assignment completion.
- Worktree naming/ownership rules in Section 7 are followed.
- Merge order follows Stage A -> B -> C -> D.
- Authoritative `_LATEST.md` is updated only by Integration Owner.

## 13) Final Response Format (Mandatory)
- Snapshot path
- Run status (`OK` / `WARNINGS` / `FAILED_INPUTS`)
- Counts: nodes, edges used, blockers active at run time
- Stage progress: A/B/C/D completion state
- Top blockers still open
- Immediate next actions to unblock or continue
