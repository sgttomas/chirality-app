# audit-hypergraph-closure — method

## Method

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

Write `Evidence/input_hypergraph_manifest.csv` listing file paths, SHA-256 hashes, accepted upstream snapshot references, and observation timestamps.

> Direct file reads (no dedicated tool; read-only): `{HYPERGRAPH_REF}/_LATEST.md` (pointer), `{snapshot}/nodes.csv`, `{snapshot}/hyperedges.csv`, `{snapshot}/incidence.csv`, and `{snapshot}/hypergraph.json` when present.

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

> Direct file reads (no dedicated hypergraph-parse tool): `{snapshot}/nodes.csv`, `{snapshot}/hyperedges.csv`, `{snapshot}/incidence.csv`. Enum-valued columns (e.g., node types, hyperedge types) can be spot-checked with `tools/validation/validate_enum.py` when enum names align with the Chirality type system.

---

### Step 2 — Build internal closure structures

Build:
- `NodesByID`
- `HyperedgesByID`
- `IncidenceByHyperedge`
- Derived projections:
  - `KTY → CAT` mapping from `IN_CATEGORY`
  - `Artifact → KTY` mapping from `HAS_ARTIFACT`
  - `Subject → KTY` mapping from `HAS_SUBJECT`
  - `Subject ↔ Artifact` mapping from `SUBJECT_MATERIALIZED_AS`

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
- For `IN_CATEGORY`, `HAS_ARTIFACT`, `HAS_SUBJECT`, `SUBJECT_MATERIALIZED_AS`, and `KTY_SUPPORTS_OBJ`: require exactly 2 incidences with the builder-defined roles and node types.
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

For each KNOWLEDGE_SUBJECT require at least one HAS_SUBJECT edge to an owner KTY. Validate SUBJECT_MATERIALIZED_AS endpoints as KNOWLEDGE_SUBJECT and KNOWLEDGE_ARTIFACT. More than one bridge per subject is a split-subject BLOCKER; more than one bridge per artifact is a merged-artifact BLOCKER. Record absent bridge evidence separately from absent artifacts; anticipated artifacts are not proof of materialization.

#### Check 7 — Orphan nodes (no incidence)
- Nodes with zero incidence are orphans.
- Severity:
  - CATEGORY orphan: WARNING
  - KNOWLEDGE_TYPE orphan: WARNING (or BLOCKER if STRICT_MODE=true)
  - KNOWLEDGE_SUBJECT orphan: WARNING
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

> Tool invocation (optional, for package/deliverable context): `tools/query/count_workspace_state.sh {EXECUTION_ROOT}` — summarizes workspace package/deliverable counts. Category/Knowledge Type folder enumeration remains a direct read-only scan of `{EXECUTION_ROOT}`.

#### Check 9 — Optional ledger closure (only if present or required)
If `LEDGER_ROW` hyperedges exist, or `REQUIRE_LEDGER_CHECKS=true`:
- Verify:
  - Each ATOMIC_UNIT participates in ≥1 LEDGER_ROW
  - If Category is represented in LEDGER_ROW, each unit maps to exactly one category
Outcomes:
- WARNING if partial coverage
- BLOCKER if contradictions (multi-category per unit) or if REQUIRE_LEDGER_CHECKS=true and coverage is missing

Mark this check `SKIPPED` if the hypergraph contains no ledger-derived structures and REQUIRE_LEDGER_CHECKS=false. Required but unavailable ledger data is INCOMPLETE and blocks a passing closure verdict.

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
- If findings exceed bound, include top issues first (BLOCKER → WARNING → INFO) and note truncation. Compute full findings and severity totals before truncation; expose total_findings, displayed_findings, and truncated in the summary.

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
   - recommended next action (e.g., rerun TASK (workflow: domain-hypergraph), fix TASK (workflow: preparation) scaffolds, correct `_CONTEXT.md` IDs)

> Tool invocations (from Outputs section; used during snapshot publication):
> - `tools/scaffolding/scaffold_tool_root.sh {EXECUTION_ROOT}/_Evaluation HypergraphClosure` (bootstrap once per tool root)
> - `tools/scaffolding/create_snapshot_folder.sh {EXECUTION_ROOT}/_Evaluation/HypergraphClosure CLOSURE {RUN_LABEL}` (per-run snapshot)
> - `tools/scaffolding/update_latest_pointer.sh {EXECUTION_ROOT}/_Evaluation/HypergraphClosure {snapshot_folder_name}` (pointer-only overwrite)

---
