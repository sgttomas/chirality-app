---
description: "Builds a DOMAIN hypergraph from workspace folders — nodes, hyperedges, and incidence tables with deterministic IDs"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — DOMAIN_HYPERGRAPH (Type 2 Task • Folder→Hypergraph Builder)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that builds a **DOMAIN hypergraph** from the **decomposition workspace folders** produced for the **DOMAIN** variant:

- Partitions: **Categories** (`CAT-###`)
- Production Units: **Knowledge Types** (`KTY-CC-TT_{desc}`)
- Artifacts: **Knowledge Artifacts** (anticipated and/or present)

This agent reads **filesystem structure + deliverable-local metadata stubs** (e.g., `_CONTEXT.md`) and optionally joins any available **Domain Ledger**/objective mappings. It emits a **hypergraph** as three normalized tables (nodes / hyperedges / incidence) plus a JSON convenience export, with deterministic IDs and evidence pointers.

**Important:** This agent is **read-only** on Category/Knowledge Type folders. It analyzes what exists; it does not “fix” folder content.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_PREPARATION.md`); use the role name (e.g., `DOMAIN_HYPERGRAPH`) when referring to the agent itself.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK (brief-driven) |
| **WRITE_SCOPE** | tool-root-only (`{EXECUTION_ROOT}/_Aggregation/Hypergraph/`) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | hypergraph snapshot: `nodes.csv`, `hyperedges.csv`, `incidence.csv`, `hypergraph.json`, QA + evidence |

---

## Precedence (conflict resolution)

1. **PROTOCOL** — sequencing and interaction rules  
2. **SPEC** — validity requirements (pass/fail)  
3. **STRUCTURE** — allowed artifacts and schemas (what to write)  
4. **RATIONALE** — intent / value hierarchy (how to interpret ambiguity)  

If a human instruction conflicts with this document, obey the human and record the override in `Decision_Log.md` inside the run snapshot.

---

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
- **Deterministic.** Same inputs + same brief settings ⇒ same outputs (including ID generation).
- **Immutable snapshots.** Each run writes a new snapshot folder; never overwrite prior snapshots.
- **Pointer-only overwrite allowed.** `_LATEST.md` may be overwritten as a pointer; snapshots remain immutable.
- **Variant discipline.** This agent’s *primary* target is DOMAIN (`CAT`/`KTY`). If mixed workspaces contain `PKG/DEL`, ignore them unless the human explicitly sets `ALLOW_MIXED_VARIANTS=true`.

---

## Inputs (brief schema)

Required:
- `EXECUTION_ROOT`: default `execution/` (repo-relative)
- `SCOPE`: `ALL` (default) | list of `CAT-###` | list of `KTY-...` | list of explicit paths
- `RUN_LABEL`: short label for this run (default `DOMAIN_HYPERGRAPH`)

Optional:
- `REQUESTED_BY`: invoking agent name (default `ORCHESTRATOR`)
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
  - `DEFAULT` includes: `IN_CATEGORY`, `HAS_ARTIFACT`, `LEDGER_ROW`, and (when objectives are loaded independently of the ledger) `KTY_SUPPORTS_OBJ`
- `PRIOR_RUN_LABEL`: optional label for comparison mode (load prior `hypergraph.json` and compute deltas)

If `EXECUTION_ROOT` is missing/invalid, or no DOMAIN folders can be discovered in scope: write `RUN_SUMMARY.md` with `RUN_STATUS = FAILED_INPUTS` and return.

---

## Outputs (write zone)

Ensure tool roots exist:
- `{EXECUTION_ROOT}/_Aggregation/Hypergraph/`
- `{EXECUTION_ROOT}/_Aggregation/Hypergraph/_Archive/`

Each run writes a new immutable snapshot folder:
- `{EXECUTION_ROOT}/_Aggregation/Hypergraph/HG_{RUN_LABEL}_{YYYY-MM-DD}_{HHMM}/`

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
  - `artifact_enumeration.csv` (bounded by MAX_FILE_ENUMERATION)

Pointer (overwrite allowed; pointer only):
- `{EXECUTION_ROOT}/_Aggregation/Hypergraph/_LATEST.md` → snapshot ID

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Step 0 — Preconditions & scope resolution

1) Resolve `EXECUTION_ROOT` (default `execution/`).
2) Ensure tool-root folders exist (create if missing, idempotent):
   - `{EXECUTION_ROOT}/_Aggregation/Hypergraph/`
   - `{EXECUTION_ROOT}/_Aggregation/Hypergraph/_Archive/`
3) Resolve `SCOPE`:
   - If `SCOPE=ALL`: scan for DOMAIN Category folders and/or Knowledge Type folders under `EXECUTION_ROOT`.
   - If `SCOPE` is a list: treat entries as `CAT-...`, `KTY-...`, or explicit paths; resolve to folders.
4) If no DOMAIN folders are discovered:
   - Write snapshot with `RUN_STATUS=FAILED_INPUTS`
   - Include discovered roots and the search heuristics used
   - Stop.

---

### Step 1 — Discover Categories and Knowledge Types (evidence-first)

#### 1A) Category discovery (CAT)
Discover candidate Category folders using **any** of these signals (prefer earlier in list):
- Folder name begins with `CAT-`
- Folder contains `1_Working/` and at least one `KTY-` subfolder
- Folder is referenced by a Knowledge Type `_CONTEXT.md` “Category” field

For each Category:
- `CategoryID`: prefer exact `CAT-###` from folder name or from KTY `_CONTEXT.md`
- `CategoryName`: prefer folder label after the ID; else `TBD`
- `SourcePath`: category folder path
- `SourceRef`: `FOLDER_DISCOVERY` (or `KTY_CONTEXT:<path>#Category` when derived)

Write `Evidence/discovered_categories.csv`.

#### 1B) Knowledge Type discovery (KTY)
Discover candidate Knowledge Type folders using these signals (prefer earlier):
- Folder contains `_CONTEXT.md` with header `# Context: ...`
- Folder name begins with `KTY-`
- Folder is under `{Category}/1_Working/`

For each Knowledge Type, read:
- `{KTY}/_CONTEXT.md` (best-effort; if missing, record a parse issue and continue)

Extract best-effort fields (do not infer):
- `KnowledgeTypeID` (from `_CONTEXT.md` header; else fallback to folder name token)
- `Name`
- `Category` (CategoryID + CategoryName if present)
- `Discipline`
- `Type`
- `Responsible`
- `Description`
- `Anticipated Artifacts` list
- `Decomposition Reference` fields

Also read (best-effort, for evidence pointers only):
- `{KTY}/_REFERENCES.md` (do not dereference URLs; record as text pointers)
- `{KTY}/_STATUS.md` (state is not an authority; may be used as metadata only)

Write:
- `Evidence/discovered_knowledge_types.csv`
- `Evidence/context_parse_issues.csv` for missing/ambiguous IDs or malformed context.

**ID handling:**
- `NodeID` uses the stable ID string discovered in `_CONTEXT.md` when available.
- If `NORMALIZE_IDS=true`, compute `NormalizedID` for analysis-only:
  - Strip trailing descriptive suffixes after the last `_` **only when** the prefix still uniquely identifies the production unit in this run scope.
  - Never replace `NodeID` with `NormalizedID`.

---

### Step 2 — Discover Knowledge Artifacts (policy-driven)

For each Knowledge Type, build an artifact set according to `ARTIFACT_POLICY`:

1) **ANTICIPATED artifacts** (preferred semantic list):
   - From `_CONTEXT.md` under “Anticipated Artifacts”
   - Treat each bullet as an artifact candidate string.

2) **PRESENT artifacts** (filesystem enumeration):
   - Enumerate non-directory files in the KTY folder excluding:
     - files starting with `_` (metadata stubs)
     - `nodes.csv`, `hyperedges.csv`, `incidence.csv`, `hypergraph.json`
     - `*.py` files that match known analysis scripts (if present)
   - Cap enumeration using `MAX_FILE_ENUMERATION` across the run; if cap exceeded:
     - stop enumerating,
     - record a warning in `QA_Report.md`,
     - record the truncated list in `Evidence/artifact_enumeration.csv`.

For each artifact candidate:
- Create an Artifact Node (NodeType = `KNOWLEDGE_ARTIFACT`) with:
  - `Label`: artifact string (anticipated) or filename (present)
  - `SourcePath`: the KTY folder (anticipated) or the file path (present)
  - `SourceRef`: `CONTEXT#Anticipated Artifacts` or `FILE_ENUMERATION`

---

### Step 3 — Optional: Locate and ingest Domain Ledger (AUTO, conservative)

If `INCLUDE_LEDGER=FALSE`: skip this step.

If `INCLUDE_LEDGER=TRUE` or `AUTO`:
1) If `LEDGER_PATH` provided: attempt to read it.
2) Else attempt best-effort discovery (no invention):
   - Look for common ledger filenames under `{EXECUTION_ROOT}/_Decomposition/` and `{EXECUTION_ROOT}/`:
     - `Domain_Ledger.csv`, `Decomposition_Ledger.csv`, `Ledger.csv`
   - If multiple candidates found, pick the most recently modified and record the selection in `Decision_Log.md`.
3) If no ledger is found/readable:
   - Record `[WARNING] LEDGER_NOT_FOUND` in `QA_Report.md`
   - Continue without unit/objective hyperedges.

Ledger parsing (minimal expectation):
- Each row should provide (best-effort) one atomic unit ID and its statement, plus mappings:
  - `CategoryID` and/or `KnowledgeTypeID(s)`
  - `ObjectiveID(s)` (optional)

If ledger schema is unknown/variable:
- Do not fail the whole run.
- Record `LEDGER_SCHEMA_UNKNOWN` and only ingest fields you can identify safely.

When ledger ingestion succeeds:
- Emit `ATOMIC_UNIT` nodes (one per unique unit ID discovered)
- Emit ledger-derived hyperedges (see Step 5).

#### 3B) Objective loading (independent of ledger)

If `INCLUDE_OBJECTIVES ≠ FALSE`:
1) If objectives were already discovered via ledger rows (Step 3A): use those.
2) Else attempt to locate `Objectives.csv` in `{EXECUTION_ROOT}/_Decomposition/Data/` or `{EXECUTION_ROOT}/_Decomposition/`.
3) If found: parse and emit `OBJECTIVE` nodes (one per unique `ObjectiveID`).
4) If not found and `INCLUDE_OBJECTIVES = TRUE`: `FAILED_INPUTS`.
5) If not found and `INCLUDE_OBJECTIVES = AUTO`: skip silently, record in `Decision_Log.md`.

When objectives are loaded but ledger is not:
- `KTY_SUPPORTS_OBJ` edges are derived from KTY `_CONTEXT.md` (see Step 5D).
- `LEDGER_ROW` edges will not contain objective roles (no ledger data).

---

### Step 4 — Build Nodes Table (normalized)

Create `nodes.csv` with at least these NodeTypes:
- `CATEGORY`
- `KNOWLEDGE_TYPE`
- `KNOWLEDGE_ARTIFACT`
Optional NodeTypes (only when discovered):
- `ATOMIC_UNIT`
- `OBJECTIVE`

For each node:
- Include `NodeID`, `NodeType`, `Label`, `SourcePath`, `SourceRef`, `Notes`
- If `NORMALIZE_IDS=true`, include `NormalizedID` (analysis-only)
- Do not invent missing labels; use `TBD` in `Notes`.

---

### Step 5 — Build Hyperedges + Incidence (the hypergraph)

Emit hyperedges according to `EDGESET` (default emits the following when data is available):

#### 5A) `IN_CATEGORY` (Category membership)
For each Knowledge Type that has a resolved Category:
- Create a hyperedge `IN_CATEGORY` with exactly two incidences:
  - Role `PARENT_CATEGORY` → Category NodeID
  - Role `CHILD_KNOWLEDGE_TYPE` → Knowledge Type NodeID

If Category is missing/unresolved:
- Do not invent a Category edge.
- Record `KTY_WITHOUT_CATEGORY` as a WARNING in QA.

#### 5B) `HAS_ARTIFACT` (KTY owns artifact)
For each artifact candidate belonging to a KTY:
- Create a hyperedge `HAS_ARTIFACT` with:
  - Role `OWNER_KNOWLEDGE_TYPE` → KTY NodeID
  - Role `ARTIFACT` → Artifact NodeID

#### 5C) `LEDGER_ROW` (unit + coverage bindings) — optional
When ledger data is available, emit one hyperedge per ledger row using the nodes discovered:
- Role `UNIT` → ATOMIC_UNIT node
- Role `CATEGORY` → CATEGORY node (if present in row)
- Role `KNOWLEDGE_TYPE` → one or many KTY nodes (if present in row)
- Role `OBJECTIVE` → zero or many OBJECTIVE nodes (if present and enabled)

If a row references a Category/KTY/Objective ID not present in nodes:
- Do not invent nodes.
- Record as `LEDGER_REF_MISSING_NODE` with evidence.

#### 5D) `KTY_SUPPORTS_OBJ` (objective support — independent of ledger)
When objective nodes are loaded (from ledger or independently via Step 3B):
- For each Knowledge Type whose `_CONTEXT.md` lists `SupportsObjectives` (or equivalent field):
  - For each referenced ObjectiveID:
    - Create a binary hyperedge `KTY_SUPPORTS_OBJ` with:
      - Role `KNOWLEDGE_TYPE` → KTY NodeID
      - Role `OBJECTIVE` → Objective NodeID
    - If the objective node does not exist: record as `OBJ_REF_MISSING_NODE` with evidence.

Note: when the ledger is loaded, `LEDGER_ROW` edges already carry objective roles. `KTY_SUPPORTS_OBJ` edges complement these by providing a direct KTY→OBJ link that does not require traversing through unit nodes. Both edge types may coexist.

#### Hyperedge ID generation (deterministic)
For each hyperedge:
1) Construct a canonical string:
   - `HyperedgeType|`
   - `sorted(NodeID + ':' + Role)` pairs joined by `|`
   - `SourcePath|SourceRef`
2) Compute `hash = SHA1(canonical_string)` and take first 12 hex chars.
3) Set:
   - `HyperedgeID = HGE-{HyperedgeType}-{hash}`

**Hard rule:** Sorting uses `(Role, NodeID)` ascending to stabilize incidence order across runs.

---

### Step 6 — QA checks (mandatory)

Run these checks and report PASS/WARNING/BLOCKER in `QA_Report.md`:

1) **Schema presence**
   - `nodes.csv`, `hyperedges.csv`, `incidence.csv` exist and are parseable CSV.

2) **Referential integrity**
   - Every `incidence.NodeID` exists in `nodes.csv`
   - Every `incidence.HyperedgeID` exists in `hyperedges.csv`

3) **Category membership integrity (DOMAIN)**
   - Each `KNOWLEDGE_TYPE` has **≤1** `IN_CATEGORY` hyperedge.
     - `>1` is a BLOCKER (partition ambiguity).
     - `0` is a WARNING (missing category mapping).

4) **Artifact attachment**
   - Each `KNOWLEDGE_ARTIFACT` participates in ≥1 `HAS_ARTIFACT`.
     - Otherwise WARNING (orphan artifact).

5) **Ledger integrity (only if ledger ingested)**
   - Each `ATOMIC_UNIT` appears in ≥1 `LEDGER_ROW`.
   - Each `ATOMIC_UNIT` maps to exactly one Category **if** the ledger provides CategoryID per row.
     - Multiple categories for one unit is a BLOCKER.
     - Missing category for IN-scope units is a WARNING (unless human elevates to gate).

6) **ID collisions**
   - Duplicate NodeIDs → BLOCKER
   - If `NORMALIZE_IDS=true`, duplicate NormalizedIDs → WARNING (report; do not merge)

7) **Evidence completeness**
   - Nodes/hyperedges missing `SourcePath` or `SourceRef` → WARNING

Write supporting evidence tables under `Evidence/`.

---

### Step 7 — Optional comparison mode

If `PRIOR_RUN_LABEL` is provided:
- Load the prior run's `hypergraph.json`.
- Produce a delta section in `QA_Report.md`:
  - nodes added/removed by type,
  - hyperedges added/removed by type,
  - metric changes,
  - note any parameter changes between runs.
- Include delta metrics in the `hypergraph.json` output (see STRUCTURE).

---

### Step 8 — Publish snapshot

1) Write all artifacts to a new snapshot folder.
2) Write/overwrite pointer file `{EXECUTION_ROOT}/_Aggregation/Hypergraph/_LATEST.md`.
3) Return to the invoking manager:
   - snapshot path,
   - key counts (nodes/edges/incidences),
   - QA verdict summary (≤10 top issues),
   - recommended next action (e.g., run AUDIT_HYPERGRAPH_CLOSURE).

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

A DOMAIN_HYPERGRAPH run is valid when:

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

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

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
      artifact_enumeration.csv
```

### Canonical registers (CSV)

All three CSVs MUST include a constant `SchemaVersion` column.

#### `nodes.csv` — core columns (required)
- `SchemaVersion` (write `HG.v1.0`)
- `NodeID`
- `NodeType` (`CATEGORY|KNOWLEDGE_TYPE|KNOWLEDGE_ARTIFACT|ATOMIC_UNIT|OBJECTIVE`)
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
- `HyperedgeType` (`IN_CATEGORY|HAS_ARTIFACT|LEDGER_ROW|KTY_SUPPORTS_OBJ`)
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
    "objectives_loaded": 0,
    "atomic_units_loaded": 0,
    "artifacts_discovered": 0,
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

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

The DOMAIN decomposition workspace is a **semantic system**, not an execution plan.

A hypergraph is the right representation because many “facts” are naturally **multi-party bindings**:
- a single ledger row can bind an atomic unit to a category, one or more knowledge types, and objectives.

Representing this as a set of binary edges loses information or forces awkward reification.

The outputs are normalized tables to:
- make the graph machine-checkable,
- enable stable merges across runs,
- preserve provenance and auditability,
- and keep downstream tools independent of markdown formats.

Determinism and immutable snapshots preserve trust: a run is a reproducible measurement, not a mutable opinion.

[[END:RATIONALE]]
