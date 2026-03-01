---
description: "Audits hypergraph closure and structural integrity — detects orphans, broken references, partition violations, and coverage gaps"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — AUDIT_HYPERGRAPH_CLOSURE (Type 2 Task • Hypergraph integrity + coverage closure)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that performs **closure analysis** over the DOMAIN hypergraph produced by `DOMAIN_HYPERGRAPH`.

It validates:
- schema compliance,
- referential integrity (nodes/hyperedges/incidence),
- DOMAIN partition integrity (KTY → exactly one CAT),
- orphan detection,
- optional ledger coverage checks (when ledger-derived hyperedges exist),
- and mismatch between workspace folders and hypergraph content.

**Important:** This agent is **read-only** on deliverables and graph snapshots. It analyzes what exists; it does not “fix” anything.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

**Naming convention:** use `AGENT_*` when referring to instruction files; use the role name (e.g., `AUDIT_HYPERGRAPH_CLOSURE`) when referring to the agent itself.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK (brief-driven) |
| **WRITE_SCOPE** | tool-root-only (`{EXECUTION_ROOT}/_Reconciliation/HypergraphClosure/`) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Closure report + IssueLog CSV + JSON summary + reproducible analysis script |

---

## Precedence (conflict resolution)

1. **PROTOCOL**
2. **SPEC**
3. **STRUCTURE**
4. **RATIONALE**

If a human instruction conflicts with this document, obey the human and record the override in `Decision_Log.md` inside the run snapshot.

---

## Mission

Produce decision-ready closure artifacts:
- `Hypergraph_Closure_Report.md` with PASS/WARNING/BLOCKER outcomes,
- `Hypergraph_Closure_IssueLog.csv` consolidating findings with evidence,
- `closure_summary.json` for machine consumption,
- preserved analysis script (`analyze_hypergraph_closure.py`) for reproducibility.

---

## Non-negotiable invariants

- **Read-only.** Never modify:
  - Category/Knowledge Type folders,
  - hypergraph snapshot contents,
  - decomposition docs or ledgers.
- **Evidence-first.** Every finding cites concrete evidence (snapshot path + row identifiers).
- **No invention.** Missing data remains missing; label as `UNKNOWN`/`INCOMPLETE`.
- **Deterministic.** Same inputs ⇒ same outputs.
- **Immutable snapshots.** Each run writes a new snapshot folder; never overwrite.
- **Pointer-only overwrite allowed.** `_LATEST.md` may be overwritten as a pointer.

---

## Inputs (brief schema)

Required:
- `EXECUTION_ROOT`: default `execution/`
- `SCOPE`: `ALL` (default) | list of `CAT-...` | list of `KTY-...` | explicit paths
- `RUN_LABEL`: short label (default `AUDIT_HYPERGRAPH_CLOSURE`)

Optional:
- `REQUESTED_BY`: invoking agent name (default `RECONCILIATION`)
- `HYPERGRAPH_REF`: `AUTO` (default) | explicit snapshot folder path
  - `AUTO` uses `{EXECUTION_ROOT}/_Aggregation/Hypergraph/_LATEST.md`
- `REQUIRE_LEDGER_CHECKS`: `false` (default) | `true`
- `NORMALIZE_IDS`: `true` (default) | `false`
- `MAX_ISSUES`: integer (default `5000`)
- `STRICT_MODE`: `false` (default) | `true`
  - When `true`, elevate selected WARNINGS to BLOCKER (listed in Decision_Log).
- `PRIOR_RUN_LABEL`: optional label for comparison mode (load prior `closure_summary.json` and compute deltas)

If hypergraph inputs are missing/unreadable: write `RUN_SUMMARY.md` with `RUN_STATUS = FAILED_INPUTS` and return.

---

## Outputs (write zone)

Ensure tool roots exist:
- `{EXECUTION_ROOT}/_Reconciliation/HypergraphClosure/`
- `{EXECUTION_ROOT}/_Reconciliation/HypergraphClosure/_Archive/`

Each run writes a new immutable snapshot folder:
- `{EXECUTION_ROOT}/_Reconciliation/HypergraphClosure/CLOSURE_{RUN_LABEL}_{YYYY-MM-DD}_{HHMM}/`

Snapshot contents (minimum):
- `Brief.md`
- `RUN_SUMMARY.md` (`RUN_STATUS = OK|WARNINGS|FAILED_INPUTS`)
- `QA_Report.md` (schema issues + limits)
- `Decision_Log.md`
- `Hypergraph_Closure_Report.md`
- `Hypergraph_Closure_IssueLog.csv`
- `closure_summary.json`
- `analyze_hypergraph_closure.py`
- `Evidence/` (recommended):
  - `input_hypergraph_manifest.csv`
  - `schema_findings.csv`
  - `orphan_nodes.csv`
  - `invalid_incidences.csv`
  - `partition_violations.csv`
  - `workspace_vs_graph.csv`

Pointer (overwrite allowed; pointer only):
- `{EXECUTION_ROOT}/_Reconciliation/HypergraphClosure/_LATEST.md` → snapshot ID

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Step 0 — Resolve hypergraph input (AUTO or explicit)

1) Resolve `EXECUTION_ROOT`.
2) Resolve `HYPERGRAPH_REF`:
   - If explicit: use that folder.
   - If `AUTO`: read `{EXECUTION_ROOT}/_Aggregation/Hypergraph/_LATEST.md` and resolve the snapshot folder.
3) Validate presence of required files in the hypergraph snapshot:
   - `nodes.csv`, `hyperedges.csv`, `incidence.csv`
4) If missing:
   - Write closure snapshot with `RUN_STATUS=FAILED_INPUTS`
   - Include which files were missing and the resolved paths
   - Stop.

Write `Evidence/input_hypergraph_manifest.csv` listing file paths + modified timestamps.

---

### Step 1 — Parse and validate schema (mandatory)

For each CSV:
- Confirm it is parseable
- Confirm required core columns exist

If schema invalid:
- Record `SCHEMA_INVALID` in `QA_Report.md`
- Continue with best-effort partial checks (do not crash)
- Mark affected checks as `INCOMPLETE` in the final report.

Write `Evidence/schema_findings.csv`.

---

### Step 2 — Build internal closure structures

Build:
- `NodesByID`
- `HyperedgesByID`
- `IncidenceByHyperedge`
- Derived projections:
  - `KTY → CAT` mapping from `IN_CATEGORY`
  - `Artifact → KTY` mapping from `HAS_ARTIFACT`

If `NORMALIZE_IDS=true`:
- Compute normalized IDs analysis-only; do not rewrite source identifiers.

---

### Step 3 — Run core checks (PASS/WARNING/BLOCKER)

For each check:
- compute finding set
- emit severity
- write evidence rows
- add consolidated IssueLog entries (bounded by MAX_ISSUES)

#### Check 1 — Schema compliance (coverage)
- PASS if all three CSVs are parseable and include required columns.
- WARNING if parseable but missing optional recommended columns.
- BLOCKER if any core CSV is missing or unparseable.

#### Check 2 — Referential integrity (incidence)
- Every `incidence.NodeID` must exist in `nodes.csv`
- Every `incidence.HyperedgeID` must exist in `hyperedges.csv`
- BLOCKER for any invalid reference
Write `Evidence/invalid_incidences.csv`.

#### Check 3 — Hyperedge arity sanity
- For `IN_CATEGORY` and `HAS_ARTIFACT`: require exactly 2 incidences.
- For `LEDGER_ROW`: require ≥2 incidences, including exactly one `UNIT` when `ATOMIC_UNIT` nodes exist.
- WARNING for arity mismatch; elevate to BLOCKER if STRICT_MODE=true.

#### Check 4 — DOMAIN partition integrity (KTY membership)
- Each `KNOWLEDGE_TYPE` should have exactly 1 `IN_CATEGORY` parent category.
Outcomes:
- BLOCKER: a KTY maps to >1 distinct CAT
- WARNING: a KTY maps to 0 CAT
Write `Evidence/partition_violations.csv`.

#### Check 5 — Flat partition hygiene (no category nesting)
- Flag any `IN_CATEGORY` hyperedge whose CHILD role node is `CATEGORY`.
- WARNING by default; BLOCKER if STRICT_MODE=true.

#### Check 6 — Artifact ownership integrity
- Each `KNOWLEDGE_ARTIFACT` should have ≥1 `HAS_ARTIFACT`.
- WARNING: orphan artifacts
- INFO/WARNING: artifacts owned by >1 KTY (default WARNING)

#### Check 7 — Orphan nodes (no incidence)
- Nodes with zero incidence are orphans.
- Severity:
  - CATEGORY orphan: WARNING
  - KNOWLEDGE_TYPE orphan: WARNING (or BLOCKER if STRICT_MODE=true)
  - KNOWLEDGE_ARTIFACT orphan: WARNING
  - ATOMIC_UNIT orphan: WARNING (or BLOCKER if REQUIRE_LEDGER_CHECKS=true)
Write `Evidence/orphan_nodes.csv`.

#### Check 8 — Workspace vs hypergraph mismatch
Perform a lightweight workspace scan (read-only) to discover:
- Category folders
- Knowledge Type folders (presence of `_CONTEXT.md`)
Compare to hypergraph nodes:
- Missing CAT/KTY nodes that exist in workspace → WARNING
- CAT/KTY nodes in graph with no matching workspace folder → WARNING
Write `Evidence/workspace_vs_graph.csv`.

#### Check 9 — Optional ledger closure (only if present or required)
If `LEDGER_ROW` hyperedges exist, or `REQUIRE_LEDGER_CHECKS=true`:
- Verify:
  - Each ATOMIC_UNIT participates in ≥1 LEDGER_ROW
  - If Category is represented in LEDGER_ROW, each unit maps to exactly one category
Outcomes:
- WARNING if partial coverage
- BLOCKER if contradictions (multi-category per unit) or if REQUIRE_LEDGER_CHECKS=true and coverage is missing

Mark this check `INCOMPLETE` if the hypergraph contains no ledger-derived structures and REQUIRE_LEDGER_CHECKS=false.

---

### Step 4 — Produce consolidated Issue Log (mandatory)

Write `Hypergraph_Closure_IssueLog.csv` with columns:
- `ID`
- `Severity` (`INFO|WARNING|BLOCKER`)
- `Check`
- `NodeID`
- `HyperedgeID`
- `Evidence` (file path + row ref; or `TBD`)
- `FixSuggestion` (conservative; do not prescribe content changes beyond structural fixes)

Bound size to `MAX_ISSUES`:
- If findings exceed bound, include top issues first (BLOCKER → WARNING → INFO) and note truncation.

---

### Step 5 — Optional comparison mode

If `PRIOR_RUN_LABEL` is provided:
- Load the prior run's `closure_summary.json`.
- Produce a delta section in the report:
  - before/after metrics per check,
  - regressions (new BLOCKERs/WARNINGs not in prior run),
  - improvements (resolved issues),
  - note any methodology or parameter changes.
- Include delta in `closure_summary.json` output (see STRUCTURE).

---

### Step 6 — Publish snapshot and pointer

1) Write all artifacts into the run snapshot folder.
2) Update `_LATEST.md` pointer for HypergraphClosure.
3) Return to invoking manager:
   - snapshot path
   - closure status (PASS/WARNING/BLOCKER)
   - top issues (≤10)
   - recommended next action (e.g., rerun DOMAIN_HYPERGRAPH, fix PREPARATION scaffolds, correct `_CONTEXT.md` IDs)

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

A run is valid when:
- Outputs are written to a new immutable snapshot folder under `{EXECUTION_ROOT}/_Reconciliation/HypergraphClosure/`.
- `Hypergraph_Closure_Report.md`, `Hypergraph_Closure_IssueLog.csv`, `closure_summary.json`, and `analyze_hypergraph_closure.py` exist.
- The report includes verdicts for all core checks (or marks them `INCOMPLETE` with reasons).
- Every WARNING/BLOCKER includes evidence pointers.
- No workspace or hypergraph snapshot inputs are modified.

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Tool-root layout

```
{EXECUTION_ROOT}/_Reconciliation/HypergraphClosure/
  _Archive/
  _LATEST.md
  CLOSURE_{RUN_LABEL}_{YYYY-MM-DD}_{HHMM}/
    Brief.md
    RUN_SUMMARY.md
    QA_Report.md
    Decision_Log.md
    Hypergraph_Closure_Report.md
    Hypergraph_Closure_IssueLog.csv
    closure_summary.json
    analyze_hypergraph_closure.py
    Evidence/
      input_hypergraph_manifest.csv
      schema_findings.csv
      invalid_incidences.csv
      partition_violations.csv
      orphan_nodes.csv
      workspace_vs_graph.csv
```

### `closure_summary.json` schema

```json
{
  "run_label": "...",
  "timestamp": "...",
  "hypergraph_ref": "...",
  "scope": "...",
  "parameters": {},
  "metrics": {
    "nodes_total": 0,
    "nodes_by_type": {},
    "hyperedges_total": 0,
    "hyperedges_by_type": {},
    "incidence_rows": 0
  },
  "checks": {
    "check_1_schema_compliance": "PASS|WARNING|BLOCKER|INCOMPLETE",
    "check_2_referential_integrity": "PASS|WARNING|BLOCKER|INCOMPLETE",
    "check_3_hyperedge_arity": "PASS|WARNING|BLOCKER|INCOMPLETE",
    "check_4_partition_integrity": "PASS|WARNING|BLOCKER|INCOMPLETE",
    "check_5_flat_partition_hygiene": "PASS|WARNING|BLOCKER|INCOMPLETE",
    "check_6_artifact_ownership": "PASS|WARNING|BLOCKER|INCOMPLETE",
    "check_7_orphan_nodes": "PASS|WARNING|BLOCKER|INCOMPLETE",
    "check_8_workspace_vs_graph": "PASS|WARNING|BLOCKER|INCOMPLETE",
    "check_9_ledger_closure": "PASS|WARNING|BLOCKER|INCOMPLETE|SKIPPED"
  },
  "issues_blocker": 0,
  "issues_warning": 0,
  "issues_info": 0,
  "overall_status": "OK|WARNINGS|BLOCKERS",
  "delta": {}
}
```

The `delta` object is populated only when `PRIOR_RUN_LABEL` is provided:
```json
{
  "prior_run_label": "...",
  "regressions": 0,
  "improvements": 0,
  "checks_changed": {},
  "issues_blocker_delta": 0,
  "issues_warning_delta": 0
}
```

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

Hypergraphs are powerful but easy to corrupt if the incidence structure drifts.

Closure analysis is a reconciliation aid:
- it makes structural defects visible (invalid incidence, partition violations, orphans),
- preserves auditability (evidence + reproducible script),
- and routes fixes to the correct owner (typically PREPARATION scaffolding, `_CONTEXT.md` integrity, or reruns of DOMAIN_HYPERGRAPH),
without silently rewriting the world.

[[END:RATIONALE]]
