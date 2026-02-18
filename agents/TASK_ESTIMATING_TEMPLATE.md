# TASK_ESTIMATING_TEMPLATE — Reusable Estimating Run Brief (INIT-TASK)

This file is a **template** for authoring a one-run estimating brief that invokes the **ESTIMATING** Type 2 task agent.

- Use placeholders like `{RUN_ID}` and `{RUN_ROOT}`.
- Treat anything marked **EXAMPLE** as non-normative.
- Keep the brief **brief**: it should be machine-readable enough for automation, but not so elaborate that humans stop using it.

Recommended practice:
- Store the filled brief somewhere operator-visible (repo, ticket, or run folder).
- Copy (or embed) the brief into the snapshot (optional) for audit traceability.

---

## Variable Glossary (placeholders)

- `{RUN_ROOT}`: root folder for the current run workspace (contains packages/deliverables and tool roots like `_Estimates/`)
- `{ESTIMATES_ROOT}`: estimating tool root (default: `{RUN_ROOT}/_Estimates/`)
- `{RUN_ID}`: stable identifier for this run (string; recommended for parallel runs)
- `{OUTPUT_LABEL}`: short label for snapshot naming (e.g., `REV0`, `BUDGET`, `IFC_DRAFT`)
- `{DECOMPOSITION_PATH}`: explicit path to the accepted project decomposition document
- `{DEPENDENCY_SOURCES}`: `AUTO` or explicit dependency register paths
- `{PRICE_SOURCES}`: list of files/folders that contain basis evidence (quotes, rate tables, historical data, models, allowance tables)
- `{SCOPE}`: deliverables/packages/paths included in this run

---

## 1) Assignment

PURPOSE:
- Produce an auditable estimate snapshot under `{ESTIMATES_ROOT}` for `{SCOPE}` using the selected `BASIS_OF_ESTIMATE`.

SCOPE:
- `{SCOPE}`

OUTPUT_LABEL:
- `{OUTPUT_LABEL}`

RUN_ID:
- `{RUN_ID}`

---

## 2) Agent Routing

- Operator-facing manager (Type 1 / persona): `{MANAGER_AGENT_ROLE}` (e.g., `WORKING_ITEMS`, `ORCHESTRATOR`)
- Task-execution agent (Type 2): `ESTIMATING` (instruction basis: your repo’s `AGENT_ESTIMATING.md` or `AGENT_ESTIMATING_GENERIC.md`)
- Design standard basis: `HELPS_HUMANS` (`AGENT_HELPS_HUMANS.md`)

Execution posture:
- Persona-managed orchestration (human decisions stay human)
- Straight-through task execution (ESTIMATING)
- Filesystem-grounded outputs with write quarantine

---

## 3) Startup Read Order (recommended)

1. `README.md`
2. `AGENTS.md`
3. `{RUN_ROOT}/INIT-PERSONA.md` (if your project uses it)
4. `{MANAGER_AGENT_INSTRUCTIONS_PATH}` (if applicable)
5. `AGENT_ESTIMATING.md` (repo canonical) OR `AGENT_ESTIMATING_GENERIC.md`
6. `AGENT_PROJECT_DECOMP.md` and the chosen decomposition instance (if available)
7. `AGENT_DEPENDENCIES.md` (to understand dependency evidence expectations)

---

## 4) INIT-TASK Inputs

### 4.1 Required (fail if missing/invalid)

RUN_ROOT: `{RUN_ROOT}`
# If RUN_ROOT is unavailable in your harness, provide ESTIMATES_ROOT explicitly instead.

ESTIMATES_ROOT: `{ESTIMATES_ROOT}`

SCOPE: `{SCOPE}`

BASIS_OF_ESTIMATE: `{BASIS_OF_ESTIMATE}`
# Allowed values (exact match; case-sensitive):
# - QUOTE
# - RATE_TABLE
# - HISTORICAL
# - PARAMETRIC
# - ALLOWANCE

CURRENCY: `{CURRENCY}`

### 4.2 Strongly recommended

DECOMPOSITION_PATH: `{DECOMPOSITION_PATH}`

DEPENDENCY_SOURCES: `{DEPENDENCY_SOURCES}`
# Default recommendation: AUTO

PRICE_SOURCES:
  - {PRICE_SOURCES}

### 4.3 Optional controls (defaults shown)

OUTPUT_LABEL: `{OUTPUT_LABEL}`

UPDATE_LATEST_POINTER: FALSE
# Set TRUE only if the manager authorizes pointer updates.

ALLOW_MIXED_METHODS: FALSE

FALLBACK_POLICY: STRICT
# STRICT | ALLOW_ALLOWANCE | ALLOW_PARAMETRIC

ROUNDING: NONE
# NONE | CENT | DOLLAR | project-defined

RUN_TIMESTAMP: `{RUN_TIMESTAMP}`

EXCLUSIONS:
  - "{RUN_ROOT}/_Estimates/**"
  - "{RUN_ROOT}/_Aggregation/**"
  - "{RUN_ROOT}/_Reconciliation/**"
  - "{RUN_ROOT}/_Archive/**"

---

## 5) Scope and Permissions

READ_SCOPE:
- Cross-deliverable reads are allowed as required for estimating.

WRITE_SCOPE (hard rule):
- Write ONLY under `{ESTIMATES_ROOT}`.
- Do not edit deliverable working files.
- Do not modify any deliverable `_STATUS.md`.

---

## 6) Output Contract (per run)

Each run MUST publish a new immutable snapshot folder under `{ESTIMATES_ROOT}`:

- `EST_{OUTPUT_LABEL}_{YYYY-MM-DD}_{HHMM}/`

Snapshot MUST include at minimum:
- `Run_Context.md`
- `Summary.md`
- `QA_Report.md`
- `Source_Index.md`
- `Decision_Log.md`
- `Assumptions_Log.md`
- `WBS_CBS_Matrix.csv`

When feasible, include:
- `Detail.csv`

When applicable, include:
- `blocker_report.csv` or `Blockers.md`
- `Risk_Register.md`
- `Change_Log.md`
- `Scope_Resolved.csv`

**Note:** A standalone BOE document is NOT required. The brief’s `BASIS_OF_ESTIMATE` is the basis input; the run records `BasisOfEstimate_Used` in `Summary.md` / `QA_Report.md`.

---

## 7) Acceptance Criteria (quick operator checklist)

A run is acceptable to publish when:

- Snapshot exists and is immutable (new folder; no overwrites).
- No writes occurred outside `{ESTIMATES_ROOT}`.
- `BASIS_OF_ESTIMATE` is valid and recorded.
- `Detail.csv` (if produced) matches schema and method constraints.
- Provenance coverage meets the chosen basis requirements (or gaps are explicitly listed).
- Scope coverage summary is present (what was included/excluded and why).
- Open blockers/unknowns are captured as TBD in logs (not guessed).

Run classification:
- `OK` / `WARNINGS` / `FAILED_INPUTS` (as emitted by ESTIMATING)

---

## 8) OPTIONAL: Project-specific add-ons (template)

Use this section only if your repo has explicit conventions for these topics.

### 8.1 OPTIONAL: Authoritative DAG / dependency control snapshot

DAG_SNAPSHOT_PATH: `{DAG_SNAPSHOT_PATH}`
# EXAMPLE (non-normative): `{RUN_ROOT}/_Estimates/EST_DAG_HARDENED_YYYY-MM-DD_HHMM/`

### 8.2 OPTIONAL: Parallel-run governance

- Integration branch: `{INTEGRATION_BRANCH}`
- Run branch prefix: `{RUN_BRANCH_PREFIX}`
- Worktree path: `{WORKTREE_ROOT}/{PROJECT_SLUG}__wt__{RUN_ID}`

### 8.3 OPTIONAL: Progress tracking

- Per-run tracker (EXAMPLE): `{ESTIMATES_ROOT}/_RUN_PROGRESS_{RUN_ID}.md` and `.csv`
- Shared tracker (EXAMPLE): `{ESTIMATES_ROOT}/_RUN_PROGRESS.md` and `.csv`

(End OPTIONAL section.)
