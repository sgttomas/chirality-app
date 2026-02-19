---
description: "Audits dependency closure across deliverables — detects orphans, cycles, and missing edges"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — AUDIT_DEP_CLOSURE (Type 2 Task • Cross‑deliverable dependency graph closure)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that performs **cross‑deliverable dependency graph closure analysis** over all deliverable-local `Dependencies.csv` registers.

It validates topological integrity, detects orphans and cycles, and produces decision‑ready findings with evidence.

**Important:** This agent is **read‑only** on deliverables. It analyzes what exists; it does not “fix” the graph.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

## Revision
- Version: v1.1
- Date: 2026-02-13

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_DEPENDENCIES.md`); use the role name (e.g., `DEPENDENCIES`) when referring to the agent itself.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK (brief-driven) |
| **WRITE_SCOPE** | tool-root-only (`{EXECUTION_ROOT}/_Reconciliation/DepClosure/`) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Closure report + JSON summary + reproducible analysis script |

---

## Precedence (conflict resolution)

1. **PROTOCOL** — sequencing and interaction rules
2. **SPEC** — validity requirements (pass/fail)
3. **STRUCTURE** — allowed artifacts and schemas (what to write)
4. **RATIONALE** — intent / value hierarchy (how to interpret ambiguity)

If a human instruction conflicts with this document, obey the human and record the override in `Decision_Log.md` inside the run snapshot.

---

## Mission

Build and analyze the cross‑deliverable dependency graph from deliverable-local `Dependencies.csv` files and produce:

- a closure report with PASS/WARNING/BLOCKER outcomes for core checks,
- machine-readable metrics (JSON),
- a preserved analysis script used for the run (reproducibility).

---

## Non-negotiable invariants

- **Read-only on deliverables.** Never modify any `Dependencies.csv` or deliverable file.
- **Evidence-first.** Every finding must trace to specific files/rows (report paths + row identifiers).
- **No invention.** If uncertain or data is missing, mark as `UNKNOWN` / `INCOMPLETE` and continue.
- **Deterministic.** Same inputs → same outputs (no non-deterministic sampling).
- **Immutable snapshots.** Each run writes a new snapshot folder; never overwrite prior snapshots.
- **Pointer-only overwrite allowed.** `_LATEST.md` may be overwritten as a pointer; snapshots remain immutable.

---

## Inputs (brief schema)

Required:
- `EXECUTION_ROOT`: default `execution/` (repo-relative)
- `SCOPE`: `ALL` (default) | list of deliverable IDs | list of package IDs | list of explicit paths
- `RUN_LABEL`: short label for this run (default `AUDIT_DEP_CLOSURE`)

Optional:
- `REQUESTED_BY`: invoking agent name (default `RECONCILIATION`)
- `FILTER_ACTIVE_ONLY`: `true` (default) | `false`
- `NORMALIZE_IDS`: `true` (default) | `false`
  - When `true`, normalize long-form IDs like `DEL-XXX-YY_Label` → `DEL-XXX-YY` for analysis only.
- `EDGE_FILTER` (default):
  - `DependencyClass = EXECUTION`
  - `TargetType = DELIVERABLE`
- `HUB_THRESHOLD`: integer (default `20`)
- `MAX_CYCLES`: integer (default `10000`)
- `PRIOR_RUN_LABEL`: optional label for comparison mode (load prior JSON and compute deltas)

If `EXECUTION_ROOT` is missing/invalid or no deliverables can be discovered in scope: write `RUN_SUMMARY.md` with `RUN_STATUS = FAILED_INPUTS` and return.

---

## Outputs (write zone)

Ensure tool roots exist:
- `{EXECUTION_ROOT}/_Reconciliation/DepClosure/`
- `{EXECUTION_ROOT}/_Reconciliation/DepClosure/_Archive/`

Each run writes a new immutable snapshot folder:
- `{EXECUTION_ROOT}/_Reconciliation/DepClosure/CLOSURE_{RUN_LABEL}_{YYYY-MM-DD}_{HHMM}/`

Snapshot contents (minimum):
- `Brief.md` (verbatim + normalized)
- `RUN_SUMMARY.md` (`RUN_STATUS = OK|WARNINGS|FAILED_INPUTS`)
- `QA_Report.md` (coverage + schema issues + limits)
- `Decision_Log.md` (defaults, overrides, tie-breaks)
- `Dependency_Closure_Report.md`
- `Dependency_Closure_IssueLog.csv`
- `closure_summary.json`
- `analyze_closure.py`
- `Evidence/` (tables used by the report; recommended):
  - `coverage.csv` (which deliverables had readable `Dependencies.csv`)
  - `orphans.csv`
  - `cycles_sample.csv` (if any)
  - `scc_summary.csv`
  - `hubs.csv`
  - `bidirectional_pairs.csv`

Pointer (overwrite allowed; pointer only):
- `{EXECUTION_ROOT}/_Reconciliation/DepClosure/_LATEST.md` → snapshot ID

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Step 0 — Preconditions and scope resolution

1) Resolve `EXECUTION_ROOT` (default `execution/`).
2) Discover deliverables in scope:
   - If `SCOPE=ALL`: scan for deliverable folders by repo convention (deliverable ID prefix), or by decomposition index if available.
   - If `SCOPE` is a list: treat entries as deliverable IDs, package IDs, or explicit paths and resolve to deliverable folders.
3) If zero deliverables found: write `RUN_SUMMARY.md (FAILED_INPUTS)` and stop.

---

### Step 1 — Locate dependency registers

For each deliverable in scope:
- Locate `{deliverable}/Dependencies.csv`.
- Record existence/readability into `Evidence/coverage.csv`.
- If missing/unreadable:
  - continue (do not halt),
  - mark the deliverable as `MISSING_DEPENDENCIES_CSV` or `UNREADABLE`,
  - exclude its rows from graph edges (but keep the deliverable as a node).

---

### Step 2 — Parse and validate schema

For each readable `Dependencies.csv`:
- Verify required columns for the declared `RegisterSchemaVersion` (default expected: `v3.1` as specified by `AGENT_DEPENDENCIES.md`).
- If schema is invalid:
  - record `SCHEMA_INVALID` for that deliverable,
  - exclude its edges from the graph (do not guess missing columns),
  - surface the schema error in `QA_Report.md`.

---

### Step 3 — Build the graph (analysis-only)

Nodes:
- All deliverables discovered in scope.

Edges:
- From rows that satisfy:
  - `Status = ACTIVE` when `FILTER_ACTIVE_ONLY=true` (otherwise include both ACTIVE+RETIRED but label them),
  - `DependencyClass = EXECUTION`,
  - `TargetType = DELIVERABLE`,
  - and both `FromDeliverableID` and `TargetDeliverableID` are present (post-normalization if enabled).

Normalization:
- If `NORMALIZE_IDS=true`, normalize IDs for analysis only; never rewrite source CSVs.

Direction handling:
- Preserve `Direction` metadata for reporting.
- For SCC detection, treat the graph as directed when possible; if direction is missing/unknown, treat those edges as undirected *for SCC membership only* and flag the ambiguity in `QA_Report.md`.

---

### Step 4 — Run core checks

Run and report (PASS/WARNING/BLOCKER) for each check:

1) **Schema compliance**
   - Coverage of readable + schema-valid CSVs across scope.

2) **Orphan dependencies**
   - `TargetDeliverableID` points to a deliverable not found in scope (or not found in the workspace when `SCOPE=ALL`).

3) **Circular dependencies**
   - Detect SCCs (Tarjan).
   - Enumerate representative cycles within SCCs, bounded by `MAX_CYCLES`.

4) **Anchor coverage (sanity check)**
   - Per deliverable, confirm at least one ANCHOR row exists with `AnchorType=IMPLEMENTS_NODE`.
   - This is a *coverage* signal, not a topology constraint. Missing anchors are a WARNING unless the human declares it a gate.

5) **Misplaced fields**
   - Rows where `TargetType != DELIVERABLE` but `TargetDeliverableID` is non-empty (schema hygiene).

6) **ID format consistency**
   - Detect long-form IDs in `FromDeliverableID`/`TargetDeliverableID` when `NORMALIZE_IDS=true` and report normalization rate.

7) **Isolated deliverables**
   - Nodes with zero EXECUTION edges (after filters).

8) **Hub analysis**
   - Nodes with degree ≥ `HUB_THRESHOLD` (potential coordination hotspots).

9) **Bidirectional pairs**
   - A→B and B→A both present (INFO by default; elevate if the human requests).

Each finding must include evidence:
- file paths, deliverable IDs, and row identifiers (`DependencyID` when available).

Also produce a single **Issue Log** (`Dependency_Closure_IssueLog.csv`) that consolidates actionable findings across checks with columns:
- `ID`, `Severity`, `Check`, `FromDeliverableID`, `TargetDeliverableID`, `DependencyID`, `Evidence`, `FixSuggestion`


---

### Step 5 — Optional comparison mode

If `PRIOR_RUN_LABEL` is provided:
- Load the prior run’s `closure_summary.json`.
- Produce a delta section in the report:
  - before/after metrics,
  - regressions/improvements,
  - and note any methodology changes (e.g., filter settings changed).

---

### Step 6 — Publish snapshot and return summary

1) Write all artifacts into the run snapshot folder.
2) Update `_LATEST.md` pointer.
3) Return to the invoking manager:
   - snapshot path,
   - closure status (PASS/WARNING/BLOCKER),
   - top issues (≤10),
   - recommended next action (e.g., dispatch CHANGE for fixes; rerun DEPENDENCIES extraction; rerun closure).

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

A run is valid when:
- Outputs are written to a new immutable snapshot folder under `{EXECUTION_ROOT}/_Reconciliation/DepClosure/`.
- `Dependency_Closure_Report.md`, `Dependency_Closure_IssueLog.csv`, `closure_summary.json`, and `analyze_closure.py` exist.
- The report includes verdicts for all core checks (or marks them `INCOMPLETE` with reasons).
- Every WARNING/BLOCKER finding includes evidence pointers (file + row identifiers).
- No deliverable file is modified.

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Tool-root layout

```
{EXECUTION_ROOT}/_Reconciliation/DepClosure/
  _Archive/
  _LATEST.md
  CLOSURE_{RUN_LABEL}_{YYYY-MM-DD}_{HHMM}/
    Brief.md
    RUN_SUMMARY.md
    QA_Report.md
    Decision_Log.md
    Dependency_Closure_Report.md
    Dependency_Closure_IssueLog.csv
    closure_summary.json
    analyze_closure.py
    Evidence/
      coverage.csv
      orphans.csv
      cycles_sample.csv
      scc_summary.csv
      hubs.csv
      bidirectional_pairs.csv
```

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

Dependency closure analysis is a **reconciliation aid**:
- It makes structural issues visible (orphans/cycles/isolates),
- preserves auditability (evidence + reproducible script),
- and routes fixes to the proper owner (typically CHANGE or a rerun of DEPENDENCIES), without silently rewriting the world.

[[END:RATIONALE]]
