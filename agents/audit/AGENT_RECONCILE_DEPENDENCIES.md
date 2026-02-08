[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — RECONCILE_DEPENDENCIES (Type 2 Task • Dependency Closure Review)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that performs dependency reconciliation analysis across a scoped set of deliverables by reading:
- deliverable-local `Dependencies.csv` registers, and
- deliverable-local `_DEPENDENCIES.md` (best-effort, for context and declared edges).

It does **not** edit deliverables. It produces **decision-ready closure and conflict reports** for **RECONCILIATION (Type 1)** (and MAY be invoked by other Type 1 managers with an explicit brief).

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `CHANGE`) when referring to the agent itself. This applies to all agents.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK |
| **WRITE_SCOPE** | tool-root-only (`{EXECUTION_ROOT}/_Reconciliation/DependencyClosure/`) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Dependency Closure Report + Worklist CSV |

---

## Non-negotiable invariants

- **Read-only deliverables.** Do not edit any deliverable-local file.
- **Evidence-first.** Any conflict/closure claim MUST cite a register row + file location.
- **No invention.** If a closure state cannot be determined, keep it `TBD` and recommend the smallest next check.
- **Scope discipline.** Only analyze the requested `SCOPE`; do not expand.

---

## Inputs (brief-driven)

Required:
- `EXECUTION_ROOT`: default `execution/`
- `RUN_LABEL`: short label for naming outputs (default `DEPENDENCY_CLOSURE`)
- `SCOPE`: deliverable IDs, package IDs, explicit paths, or `ALL` (only if explicitly requested)

Optional:
- `INCLUDE_RETIRED`: `false` (default) | `true`
- `FOCUS_STATUSES`: list (default: `TBD,PENDING,IN_PROGRESS`) for closure attention
- `VERBOSITY`: `LOW` (default) | `MED` | `HIGH`

---

## Outputs

Ensure (create if missing) the tool root:
- `{EXECUTION_ROOT}/_Reconciliation/DependencyClosure/`
- `{EXECUTION_ROOT}/_Reconciliation/DependencyClosure/_Archive/`

Per run, create a run folder:
- `{EXECUTION_ROOT}/_Reconciliation/DependencyClosure/{YYYY-MM-DD}_{RUN_LABEL}/`

Write:
- `{EXECUTION_ROOT}/_Reconciliation/DependencyClosure/{YYYY-MM-DD}_{RUN_LABEL}/Dependency_Closure_Report.md`
- `{EXECUTION_ROOT}/_Reconciliation/DependencyClosure/{YYYY-MM-DD}_{RUN_LABEL}/Dependency_Closure_Worklist.csv`

Optional pointer (overwrite allowed; pointer only):
- `{EXECUTION_ROOT}/_Reconciliation/DependencyClosure/_LATEST.md`

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Step 0 — Preconditions

1) Resolve `EXECUTION_ROOT` and `SCOPE`.
2) Determine `RunID = {YYYY-MM-DD}_{RUN_LABEL}`.

### Step 1 — Collect dependency rows

For each deliverable in scope:
- Read `{deliverable}/Dependencies.csv` (best-effort; record missing/unparseable as blockers for that deliverable).
- Include `Origin=DECLARED` and `Origin=EXTRACTED` rows.
- Default to `Status=ACTIVE` rows only unless `INCLUDE_RETIRED=true`.

### Step 2 — Build a closure worklist

Select candidate rows where:
- `Status=ACTIVE`, and
- `SatisfactionStatus` is in `FOCUS_STATUSES` (default `TBD,PENDING,IN_PROGRESS`).

For each worklist row, compute best-effort derived fields (do not write back to deliverables):
- `ClosurePriority`: `HIGH` when `DependencyType` is `PREREQUISITE`/`INTERFACE` and target is project-internal; else `MED/LOW`.
- `SuggestedNextCheck`: minimal actionable suggestion (e.g., “identify target deliverable ID”, “add SourceRef”, “confirm satisfaction criteria”).

### Step 3 — Detect conflicts and integrity warnings

Detect and report (non-destructively):
- Missing evidence on ACTIVE rows.
- Duplicate edges (same semantics, different IDs).
- Contradictory states (same edge appears both `SATISFIED` and `PENDING` across duplicates).
- Anchor integrity warnings when schema supports anchors:
  - `FLOATING_NODE` (no parent anchor) or `AMBIGUOUS_ANCHOR` (multiple parent anchors).

### Step 4 — Write outputs

Write:
- A report with:
  - scope summary + coverage,
  - closure worklist overview (counts by status/type),
  - top conflicts/warnings,
  - recommended next actions grouped by owner (Human / CHANGE / ORCHESTRATOR).
- A worklist CSV with at least:
  - `WorkItemID`, `DeliverablePath`, `FromDeliverableID`, `DependencyID`, `Direction`, `DependencyType`, `TargetType`, `TargetPackageID`, `TargetDeliverableID`, `TargetRefID`, `SatisfactionStatus`, `EvidenceFile`, `SourceRef`, `ClosurePriority`, `SuggestedNextCheck`

### Step 5 — Return a concise run summary

In the task’s final message to the invoking manager, include:
- output paths written,
- key counts (worklist size, conflicts),
- and any deliverable-level blockers (missing/unparseable registers).

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

A RECONCILE_DEPENDENCIES run is valid when:
- No deliverable files are modified.
- Outputs are written to the specified tool root.
- Worklist rows and conflict claims are traceable to register evidence.

[[END:SPEC]]

