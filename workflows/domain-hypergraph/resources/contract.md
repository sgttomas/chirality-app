# domain-hypergraph — contract

## Mission

Build a **DOMAIN hypergraph** from the decomposition workspace and produce:

- a normalized hypergraph (tables + JSON) suitable for downstream merging/search,
- evidence-first QA (coverage and integrity checks),
- a reproducible analysis script used for the run.

The hypergraph is intended to represent **semantic structure** and **coverage bindings**, not execution scheduling.

---

## Non-negotiable invariants

- **Read-only on Category/Knowledge Type folders.** Never modify `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`, drafts, or any decomposition files.
- **Evidence-first.** Every node and hyperedge must include `SourcePath` and `SourceRef` (or explicit `TBD`).
- **No invention.** If metadata is missing/ambiguous, emit `TBD` in `Notes` and continue; do not guess.
- **Deterministic.** Identical staging tables, settings, and tool version yield identical constructed graph data; source discovery judgments retain evidence and limitations.
- **Immutable snapshots.** Each run writes a new snapshot folder; never overwrite prior snapshots.
- **Pointer-only overwrite allowed.** `_LATEST.md` may be overwritten as a pointer; snapshots remain immutable.
- **Variant discipline.** This agent’s *primary* target is DOMAIN (`CAT`/`KTY`). If mixed workspaces contain `PKG/DEL`, ignore them unless the human explicitly sets `ALLOW_MIXED_VARIANTS=true`.

---

## Inputs (brief schema)

The brief names accepted upstream snapshot(s), their ledger/objective paths and fingerprints, and derivative status. File recency is not an acceptance rule.

Required:
- `EXECUTION_ROOT`: default `execution/` (repo-relative)
- `SCOPE`: `ALL` (default) | list of `CAT-###` | list of `KTY-...` | list of explicit paths
- `RUN_LABEL`: short label for this run (default `TASK`)

Optional:
- `REQUESTED_BY`: invoking agent name (default `WORKING_ITEMS (workflow: project-setup)`)
- `ALLOW_MIXED_VARIANTS`: `false` (default) | `true`
- `INCLUDE_LEDGER`: `AUTO` (default) | `TRUE` | `FALSE`
- `LEDGER_PATH`: explicit path to a Domain Ledger CSV/TSV (optional)
- `INCLUDE_OBJECTIVES`: `AUTO` (default) | `TRUE` | `FALSE`
  - `AUTO`: include if `Objectives.csv` is found alongside the ledger (in `{EXECUTION_ROOT}/_Decomposition/Data/` or `{EXECUTION_ROOT}/_Decomposition/`)
  - `TRUE`: require objectives; fail if not found
  - `FALSE`: skip objectives entirely (no objective nodes or KTY→OBJ edges)
  - Note: objectives can be loaded independently of the ledger. When `INCLUDE_LEDGER=FALSE` but `INCLUDE_OBJECTIVES=TRUE`, objective nodes and `KTY_SUPPORTS_OBJ` edges (derived from KTY `_CONTEXT.md` `SupportsObjectives` fields) are still emitted.
- `NORMALIZE_IDS`: `true` (default) | `false`
  - When `true`, add `NormalizedID` fields (analysis-only). Do not rewrite source IDs.
- `MAX_FILE_ENUMERATION`: integer (default `5000`) — safety cap for enumerating present files as artifacts
- `ARTIFACT_POLICY`: `ANTICIPATED_PLUS_PRESENT` (default) | `ANTICIPATED_ONLY` | `PRESENT_ONLY`
- `EDGESET`: `DEFAULT` (default) | explicit list of hyperedge types to emit
  - `DEFAULT` includes: `IN_CATEGORY`, `HAS_SUBJECT`, `HAS_ARTIFACT`, `SUBJECT_MATERIALIZED_AS`, `LEDGER_ROW`, and (when objectives are loaded independently of the ledger) `KTY_SUPPORTS_OBJ`
- `PRIOR_RUN_LABEL`: optional label for comparison mode (load prior `hypergraph.json` and compute deltas)

If `EXECUTION_ROOT` is missing/invalid, or no DOMAIN folders can be discovered in scope: write `RUN_SUMMARY.md` with `RUN_STATUS = FAILED_INPUTS` and return.

---

## Outputs (write zone)

Bootstrap tool root: `tools/scaffolding/scaffold_tool_root.sh {EXECUTION_ROOT}/_Aggregation Hypergraph`

Create snapshot folder: `tools/scaffolding/create_snapshot_folder.sh {EXECUTION_ROOT}/_Aggregation/Hypergraph HG {RUN_LABEL}`

Snapshot contents (minimum):
- `Brief.md` (verbatim + normalized)
- `RUN_SUMMARY.md` (`RUN_STATUS = OK|WARNINGS|FAILED_INPUTS`)
- `QA_Report.md`
- `Decision_Log.md` (defaults, heuristics, overrides)
- `nodes.csv`
- `hyperedges.csv`
- `incidence.csv`
- `hypergraph.json` (convenience export)
- `build_hypergraph.py` (reproducibility; preserved script)
- `Evidence/` (recommended tables used by QA/report):
  - `discovered_categories.csv`
  - `discovered_knowledge_types.csv`
  - `context_parse_issues.csv`
  - `subject_artifact_mapping.csv`
  - `artifact_enumeration.csv` (bounded by MAX_FILE_ENUMERATION)

Update pointer: `tools/scaffolding/update_latest_pointer.sh {EXECUTION_ROOT}/_Aggregation/Hypergraph {snapshot_folder_name}`

---

## Validity

A TASK run is valid when:

- Outputs are written to a new immutable snapshot folder under `{EXECUTION_ROOT}/_Aggregation/Hypergraph/`.
- `nodes.csv`, `hyperedges.csv`, `incidence.csv`, and `QA_Report.md` exist and are parseable.
- All incidences reference existing nodes and hyperedges (referential integrity).
- Hyperedge IDs are deterministic per the algorithm (same inputs → same IDs).
- Every WARNING/BLOCKER includes evidence pointers (`SourcePath` + `SourceRef`, plus file/row pointers when applicable).
- No Category/Knowledge Type folder content is modified.

Invalid when:
- snapshots are overwritten,
- deliverable-local files are modified,
- CSV schemas are missing required core columns,
- or referential integrity fails without being reported as a BLOCKER.

---

## Artifacts and schemas

### Tool-root layout

```
{EXECUTION_ROOT}/_Aggregation/Hypergraph/
  _Archive/
  _LATEST.md
  HG_{RUN_LABEL}_{YYYY-MM-DD}_{HHMM}/
    Brief.md
    RUN_SUMMARY.md
    QA_Report.md
    Decision_Log.md
    nodes.csv
    hyperedges.csv
    incidence.csv
    hypergraph.json
    build_hypergraph.py
    Evidence/
      discovered_categories.csv
      discovered_knowledge_types.csv
      context_parse_issues.csv
      subject_artifact_mapping.csv
      artifact_enumeration.csv
```

### Canonical registers (CSV)

All three CSVs MUST include a constant `SchemaVersion` column.

#### `nodes.csv` — core columns (required)
- `SchemaVersion` (write `HG.v1.0`)
- `NodeID`
- `NodeType` (`CATEGORY|KNOWLEDGE_TYPE|KNOWLEDGE_SUBJECT|KNOWLEDGE_ARTIFACT|ATOMIC_UNIT|OBJECTIVE`)
- `Label`
- `SourcePath`
- `SourceRef`
- `Notes`

Optional (non-breaking) columns:
- `NormalizedID` (when NORMALIZE_IDS=true)
- `Tags` (semicolon-separated)
- `Variant` (write `DOMAIN`)

#### `hyperedges.csv` — core columns (required)
- `SchemaVersion` (write `HG.v1.0`)
- `HyperedgeID`
- `HyperedgeType` (`IN_CATEGORY|HAS_SUBJECT|HAS_ARTIFACT|SUBJECT_MATERIALIZED_AS|LEDGER_ROW|KTY_SUPPORTS_OBJ`)
- `SourcePath`
- `SourceRef`
- `Notes`

Optional columns:
- `Tags`
- `Label`

#### `incidence.csv` — core columns (required)
- `SchemaVersion` (write `HG.v1.0`)
- `HyperedgeID`
- `NodeID`
- `Role`
- `Ordinal` (integer; deterministic ordering)
- `Notes`

### `hypergraph.json` (convenience export)

Must include:
- `schema_version`
- `generated_at`
- `run_label`
- `execution_root`
- `scope`
- `brief` (normalized parameters)
- `nodes` (array)
- `hyperedges` (array with incidence lists)
- `metrics`:
  ```json
  {
    "node_count": 0,
    "node_counts_by_type": {},
    "hyperedge_count": 0,
    "hyperedge_counts_by_type": {},
    "incidence_count": 0,
    "categories_discovered": 0,
    "knowledge_types_discovered": 0,
    "knowledge_subjects_discovered": 0,
    "knowledge_artifacts_discovered": 0,
    "objectives_loaded": 0,
    "atomic_units_loaded": 0,
    "unresolved_references": 0,
    "qa_blockers": 0,
    "qa_warnings": 0
  }
  ```
- `delta` (optional; present only when `PRIOR_RUN_LABEL` was provided):
  ```json
  {
    "prior_run_label": "...",
    "nodes_added": 0,
    "nodes_removed": 0,
    "hyperedges_added": 0,
    "hyperedges_removed": 0,
    "changes_by_type": {}
  }
  ```

This JSON is convenience-only; CSV tables are authoritative.

---
