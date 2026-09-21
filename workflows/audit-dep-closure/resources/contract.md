# audit-dep-closure — contract

## Mission

Build and analyze the cross‑deliverable dependency graph from deliverable-local `Dependencies.csv` files and produce:

- a closure report with PASS/WARNING/BLOCKER outcomes for core checks,
- machine-readable metrics (JSON),
- the registered tool fingerprint, effective arguments, input manifest, and output evidence (reproducibility).

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
- `RUN_LABEL`: short label for this run (default `TASK`)

Optional:
- `REQUESTED_BY`: invoking agent name (default `WORKING_ITEMS`)
- `FILTER_ACTIVE_ONLY`: `true` (default) | `false`
- `NORMALIZE_IDS`: `true` (default) | `false`
  - When `true`, normalize long-form IDs by stripping descriptive suffixes for analysis only. Examples: `DEL-XXX-YY_Label` → `DEL-XXX-YY` (WORKING_ITEMS (workflow: project-decomp)), `DEL-XX-YY` (WORKING_ITEMS (workflow: software-decomp), already short-form). If DOMAIN folders are encountered in a mixed workspace, their `KTY-CC-TT_Label` IDs are normalized to `KTY-CC-TT`.
- `EDGE_FILTER` (default):
  - `DependencyClass = EXECUTION`
  - `TargetType = DELIVERABLE`
- `HUB_THRESHOLD`: integer (default `20`)
- `MAX_CYCLES`: integer (default `10000`)
- `PRIOR_RUN_LABEL`: optional label for comparison mode (load prior JSON and compute deltas)

If `EXECUTION_ROOT` is missing/invalid or no deliverables can be discovered in scope: write `RUN_SUMMARY.md` with `RUN_STATUS = FAILED_INPUTS` and return.

---

## Outputs (write zone)

Bootstrap tool root: `tools/scaffolding/scaffold_tool_root.sh {EXECUTION_ROOT}/_Evaluation DepClosure`

Create snapshot folder: `tools/scaffolding/create_snapshot_folder.sh {EXECUTION_ROOT}/_Evaluation/DepClosure CLOSURE {RUN_LABEL}`

Run graph analysis: `python3 tools/coordination/analyze_dep_closure.py {EXECUTION_ROOT} --output-dir {snapshot_folder} --scope {SCOPE} --filter-active-only {FILTER_ACTIVE_ONLY} --normalize-ids {NORMALIZE_IDS} --dependency-class EXECUTION --target-type DELIVERABLE --hub-threshold {HUB_THRESHOLD} --max-cycles {MAX_CYCLES}`
This produces: `closure_summary.json`, `coverage.csv`, `orphans.csv` (missing workspace targets), `outside_scope.csv` (existing targets outside selected scope), `isolated.csv` (zero-edge nodes), `cycles_sample.csv`, `scc_summary.csv`, `hubs.csv`, `bidirectional_pairs.csv`, `id_normalization.csv`.

`Tool_Run.json` records the tool path and SHA-256, exact arguments, accepted input basis, exit code, run_status, and subject_status. Process success is distinct from subject PASS. Optional comparison uses --prior-summary with the explicit accepted prior summary.

Additional snapshot contents (minimum, produced by LLM):
- `Brief.md` (verbatim + normalized)
- `RUN_SUMMARY.md` (`RUN_STATUS = OK|WARNINGS|FAILED_INPUTS`)
- `QA_Report.md` (coverage + schema issues + limits)
- `Decision_Log.md` (defaults, overrides, tie-breaks)
- `Dependency_Closure_Report.md`
- `Dependency_Closure_IssueLog.csv`

Update pointer: `tools/scaffolding/update_latest_pointer.sh {EXECUTION_ROOT}/_Evaluation/DepClosure {snapshot_folder_name}`

---

## Validity

A run is valid when:
- Outputs are written to a new immutable snapshot folder under `{EXECUTION_ROOT}/_Evaluation/DepClosure/`.
- `Dependency_Closure_Report.md`, `Dependency_Closure_IssueLog.csv`, `closure_summary.json`, and `Tool_Run.json` exist.
- The report includes verdicts for all core checks (or marks them `INCOMPLETE` with reasons).
- Every WARNING/BLOCKER finding includes evidence pointers (file + row identifiers).
- No deliverable file is modified.

---

## Artifacts and schemas

### Tool-root layout

```
{EXECUTION_ROOT}/_Evaluation/DepClosure/
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
    Tool_Run.json
    Evidence/
      coverage.csv
      orphans.csv
      cycles_sample.csv
      scc_summary.csv
      hubs.csv
      bidirectional_pairs.csv
```

---
