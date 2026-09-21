# audit-hypergraph-closure — contract

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
- `RUN_LABEL`: short label (default `TASK`)

Optional:
- `REQUESTED_BY`: invoking agent name (default `WORKING_ITEMS`)
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

Bootstrap tool root: `tools/scaffolding/scaffold_tool_root.sh {EXECUTION_ROOT}/_Evaluation HypergraphClosure`

Create snapshot folder: `tools/scaffolding/create_snapshot_folder.sh {EXECUTION_ROOT}/_Evaluation/HypergraphClosure CLOSURE {RUN_LABEL}`

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

Update pointer: `tools/scaffolding/update_latest_pointer.sh {EXECUTION_ROOT}/_Evaluation/HypergraphClosure {snapshot_folder_name}`

---

## Validity

Audit completion is distinct from graph validity. A successfully executed audit may report BLOCKER findings. Optional absent ledger checks are SKIPPED; missing required evidence is INCOMPLETE.

A run is valid when:
- Outputs are written to a new immutable snapshot folder under `{EXECUTION_ROOT}/_Evaluation/HypergraphClosure/`.
- `Hypergraph_Closure_Report.md`, `Hypergraph_Closure_IssueLog.csv`, `closure_summary.json`, and `analyze_hypergraph_closure.py` exist.
- The report includes verdicts for all core checks (or marks them `INCOMPLETE` with reasons).
- Every WARNING/BLOCKER includes evidence pointers.
- No workspace or hypergraph snapshot inputs are modified.

---

## Artifacts and schemas

### Tool-root layout

```
{EXECUTION_ROOT}/_Evaluation/HypergraphClosure/
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

---
