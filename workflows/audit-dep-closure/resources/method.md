# audit-dep-closure — method

## Method

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
- Record existence/readability into `coverage.csv`.
- If missing/unreadable:
  - continue (do not halt),
  - mark the deliverable as `MISSING_DEPENDENCIES_CSV` or `UNREADABLE`,
  - exclude its rows from graph edges (but keep the deliverable as a node).

---

### Step 2 — Parse and validate schema

For each readable `Dependencies.csv`:
- Verify required columns for the declared `RegisterSchemaVersion` (default expected: `v3.1` as specified by `docs/SPEC.md` §6 and `workflows/dependency-extract/`).
- If schema is invalid:
  - record `SCHEMA_INVALID` for that deliverable,
  - exclude its edges from the graph (do not guess missing columns),
  - surface the schema error in `QA_Report.md`.

---

### Step 3 — Build the graph (analysis-only)

> Tool invocation: steps 1–4 are performed by a single deterministic call to `tools/coordination/analyze_dep_closure.py`, which handles register discovery, schema validation, graph construction, and core-check outputs.
> `python3 tools/coordination/analyze_dep_closure.py {EXECUTION_ROOT} --output-dir {snapshot_folder} --scope {SCOPE} --filter-active-only {FILTER_ACTIVE_ONLY} --normalize-ids {NORMALIZE_IDS} --dependency-class EXECUTION --target-type DELIVERABLE --hub-threshold {HUB_THRESHOLD} --max-cycles {MAX_CYCLES}`

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
- Use canonical UPSTREAM/DOWNSTREAM direction. Missing, unknown, or otherwise invalid direction rows are excluded from topology and reported as invalid input evidence; mark the affected topology coverage incomplete. Never invent reverse edges from invalid direction values.

---

### Step 4 — Run core checks

Run and report (PASS/WARNING/BLOCKER) for each check:

1) **Schema compliance**
   - Coverage of readable + schema-valid CSVs across scope.

2) **Orphan dependencies**
   - `TargetDeliverableID` points to a deliverable absent from the independent workspace inventory. Existing targets outside the selected scope are outside-scope findings, recorded separately.

3) **Circular dependencies**
   - Use the registered analyzer’s strongly connected components result and record its tool fingerprint; do not duplicate its graph algorithm.
   - Enumerate representative cycles within SCCs, bounded by `MAX_CYCLES`.

4) **Anchor coverage (sanity check)**
   - Per deliverable, confirm at least one ANCHOR row exists with `AnchorType=IMPLEMENTS_NODE`.
   - This is a *coverage* signal, not a topology constraint. Missing anchors are a WARNING unless the human declares it a gate.

5) **Misplaced fields**
   - Rows where `TargetType != DELIVERABLE` but `TargetDeliverableID` is non-empty (schema hygiene).

6) **ID format consistency**
   - Detect long-form IDs in `FromDeliverableID`/`TargetDeliverableID` when `NORMALIZE_IDS=true` and report normalization rate.
   - Normalization strips the `_{description}` suffix. Expected ID prefixes: `DEL-` (PROJECT/SOFTWARE), `KTY-` (DOMAIN, if encountered in mixed workspaces).

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

> Tool invocation: snapshot bootstrap and pointer updates use `tools/scaffolding/scaffold_tool_root.sh`, `tools/scaffolding/create_snapshot_folder.sh`, and `tools/scaffolding/update_latest_pointer.sh` (see Outputs section for concrete command lines).

1) Write all artifacts into the run snapshot folder.
2) Update `_LATEST.md` pointer.
3) Return to the invoking manager:
   - snapshot path,
   - closure status (PASS/WARNING/BLOCKER),
   - top issues (≤10),
   - recommended next action (e.g., dispatch WORKING_ITEMS (workflow: change) for fixes; rerun TASK+dependency-extract; rerun closure).

---
