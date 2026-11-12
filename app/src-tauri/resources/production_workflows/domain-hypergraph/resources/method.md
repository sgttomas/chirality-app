# domain-hypergraph — method

## Method

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
- `{KTY}/Scoping.md` (if present; preferred bridge source for `SubjectID -> ArtifactID -> Filename`)

Write:
- `Evidence/discovered_knowledge_types.csv`
- `Evidence/context_parse_issues.csv` for missing/ambiguous IDs or malformed context.

**ID handling:**
- `NodeID` uses the stable ID string discovered in `_CONTEXT.md` when available.
- If `NORMALIZE_IDS=true`, compute `NormalizedID` for analysis-only:
  - Strip trailing descriptive suffixes after the last `_` **only when** the prefix still uniquely identifies the production unit in this run scope.
  - Never replace `NodeID` with `NormalizedID`.

---

### Step 2 — Discover Knowledge Subjects and Knowledge Artifacts (policy-driven)

For each Knowledge Type, build the decomposition layer and document layer separately, then bridge them where evidence allows:

1) **Preferred bridge source: `Scoping.md` Artifact Plan**
   - If `{KTY}/Scoping.md` exists, parse the Artifact Plan table.
   - Treat each row as the authoritative bridge between:
     - `SubjectID` / `SubjectName` (decomposition layer), and
     - `ArtifactID` / `Filename` (document layer).
   - For each valid row:
     - create a Knowledge Subject candidate,
     - create a Knowledge Artifact candidate,
     - record a mapping row in `Evidence/subject_artifact_mapping.csv`.
   - `Scoping.md` itself is evidence for the bridge, but is not a Knowledge Subject node and is not a `KNOWLEDGE_ARTIFACT` node.

2) **ANTICIPATED artifact hints** (fallback only when no `Scoping.md` Artifact Plan is available):
   - From `_CONTEXT.md` under “Anticipated Artifacts”
   - Treat each bullet as an artifact- or section-level hint only.
   - Do not synthesize Knowledge Subject nodes from this field.
   - If used to create artifact candidates, set `SourceRef = CONTEXT#Anticipated Artifacts` and record in `Decision_Log.md` that the subject layer was unavailable.

3) **PRESENT artifacts** (filesystem enumeration):
   - Enumerate non-directory files in the KTY folder excluding:
     - files starting with `_` (metadata stubs)
     - `Scoping.md` (KTY entrypoint; not a subject-backed artifact)
     - `nodes.csv`, `hyperedges.csv`, `incidence.csv`, `hypergraph.json`
     - `*.py` files that match known analysis scripts (if present)
   - Cap enumeration using `MAX_FILE_ENUMERATION` across the run; if cap exceeded:
     - stop enumerating,
     - record a warning in `QA_Report.md`,
     - record the truncated list in `Evidence/artifact_enumeration.csv`.

4) **Create nodes (evidence-first):**
   - For each Knowledge Subject candidate:
     - Create a Subject Node (NodeType = `KNOWLEDGE_SUBJECT`) with:
       - `NodeID`: `SubjectID` when available; otherwise do not invent a subject node
       - `Label`: `SubjectName`
       - `SourcePath`: `Scoping.md` or other authoritative source path
       - `SourceRef`: `SCOPING#Artifact Plan` or equivalent evidence pointer
   - For each Knowledge Artifact candidate:
     - Create an Artifact Node (NodeType = `KNOWLEDGE_ARTIFACT`) with:
       - `NodeID`: `ArtifactID` when available; otherwise a deterministic fallback derived from `{KTY_ID}:{filename_or_hint}`
       - `Label`: filename or artifact label
       - `SourcePath`: the file path (present) or the source file carrying the artifact plan/hint
       - `SourceRef`: `SCOPING#Artifact Plan`, `FILE_ENUMERATION`, or `CONTEXT#Anticipated Artifacts`

---

### Step 3 — Optional: Locate and ingest Domain Ledger (AUTO, conservative)

If `INCLUDE_LEDGER=FALSE`: skip this step.

If `INCLUDE_LEDGER=TRUE` or `AUTO`:
1) If `LEDGER_PATH` provided: attempt to read it.
2) Else resolve the ledger named by the accepted upstream snapshot or handoff:
   - To locate the accepted reference, look for common ledger filenames under `{EXECUTION_ROOT}/_Decomposition/` and `{EXECUTION_ROOT}/`:
     - `Domain_Ledger.csv`, `Decomposition_Ledger.csv`, `Ledger.csv`
   - Candidate enumeration is discovery only. Bind a ledger only when the accepted snapshot or human ruling identifies it; otherwise record LEDGER_BASIS_AMBIGUOUS and the candidates in Decision_Log.md. Continue without the optional ledger layer for AUTO, or return incomplete required input for TRUE.
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
- `KTY_SUPPORTS_OBJ` edges are derived from KTY `_CONTEXT.md` (see Step 5).
- `LEDGER_ROW` edges will not contain objective roles (no ledger data).

---

### Evidence CSV Contracts (tool input)

After Steps 0-3 complete discovery, the agent emits the following CSV files to `{snapshot}/Evidence/`. These files are the contract consumed by `tools/aggregation/build_hypergraph.py` in Steps 4-7. Column ordering is flexible; column names MUST match exactly.

| File | Status | Columns |
|---|---|---|
| `discovered_categories.csv` | **required** | `CategoryID`, `CategoryName`, `SourcePath`, `SourceRef`, `Notes` |
| `discovered_knowledge_types.csv` | **required** | `KnowledgeTypeID`, `Name`, `CategoryID`, `Discipline`, `Type`, `Responsible`, `Description`, `AnticipatedArtifacts`, `DecompositionRef`, `SourcePath`, `SourceRef`, `Notes` |
| `discovered_knowledge_subjects.csv` | conditional | `SubjectID`, `SubjectName`, `KnowledgeTypeID`, `SourcePath`, `SourceRef`, `Notes` |
| `artifact_enumeration.csv` | conditional | `ArtifactID`, `ArtifactLabel`, `KnowledgeTypeID`, `Filename`, `ArtifactSource`, `SourcePath`, `SourceRef`, `Notes` |
| `subject_artifact_mapping.csv` | conditional | `SubjectID`, `ArtifactID`, `KnowledgeTypeID`, `SourcePath`, `SourceRef`, `Notes` |
| `discovered_ledger_rows.csv` | optional | `AtomicUnitID`, `UnitStatement`, `CategoryID`, `KnowledgeTypeIDs`, `ObjectiveIDs`, `SourcePath`, `SourceRef`, `Notes` |
| `discovered_objectives.csv` | optional | `ObjectiveID`, `Label`, `SourcePath`, `SourceRef`, `Notes` |
| `kty_supports_obj.csv` | optional | `KnowledgeTypeID`, `ObjectiveID`, `SourcePath`, `SourceRef`, `Notes` |

**Semi-colon list fields** (`KnowledgeTypeIDs`, `ObjectiveIDs` in `discovered_ledger_rows.csv`): the tool trims, dedupes, and sorts each list ascending before edge construction. Source ordering does not affect output.

**`ArtifactSource` values** (in `artifact_enumeration.csv`): `SCOPING_PLAN` | `ANTICIPATED` | `PRESENT`. The tool records this in node `Notes` but does not alter construction logic by source. The `AnticipatedArtifacts` field in `discovered_knowledge_types.csv` is **informational metadata only**; the tool does NOT use it for artifact node construction.

**Conditional/optional file absence behavior:**
- If `discovered_knowledge_subjects.csv` absent → no KNOWLEDGE_SUBJECT nodes, no HAS_SUBJECT edges.
- If `artifact_enumeration.csv` absent → no KNOWLEDGE_ARTIFACT nodes, no HAS_ARTIFACT edges.
- If `subject_artifact_mapping.csv` absent → no SUBJECT_MATERIALIZED_AS edges.
- If `discovered_ledger_rows.csv` absent → no ATOMIC_UNIT nodes, no LEDGER_ROW edges.
- If `discovered_objectives.csv` absent → OBJECTIVE nodes derived from ledger rows only (if ledger present).
- If `kty_supports_obj.csv` absent → no KTY_SUPPORTS_OBJ edges (ledger-derived objective roles still emitted via LEDGER_ROW).

The required files (`discovered_categories.csv`, `discovered_knowledge_types.csv`) establish the workspace's skeletal structure; absence of either → tool returns FAILED_INPUTS.

---

### Step 4 — Invoke build_hypergraph.py (deterministic graph construction)

Steps 4-7 are executed by the deterministic tool `tools/aggregation/build_hypergraph.py`. Invoke:

```sh
python3 tools/aggregation/build_hypergraph.py \
  --staging-dir {snapshot}/Evidence/ \
  --output-dir {snapshot}/ \
  --run-label {RUN_LABEL} \
  --execution-root {EXECUTION_ROOT} \
  --scope {SCOPE} \
  --normalize-ids {NORMALIZE_IDS} \
  --edgeset {EDGESET} \
  --variant DOMAIN \
  [--prior-snapshot {prior_snapshot_path}]
```

The tool reads the Evidence CSV contracts above, constructs `nodes.csv`, `hyperedges.csv`, `incidence.csv`, `hypergraph.json`, and `QA_Report.md` in `{snapshot}/`, runs the 9 QA checks (see Step 6), and optionally computes deltas vs a prior snapshot.

**Node construction (Step 4 deterministic detail):** The tool emits nodes of type `CATEGORY`, `KNOWLEDGE_TYPE`, `KNOWLEDGE_SUBJECT`, `KNOWLEDGE_ARTIFACT`; plus `ATOMIC_UNIT` and `OBJECTIVE` when optional staging files are present. Rows with blank primary IDs are skipped (no invention). Each node row carries `NodeID`, `NodeType`, `Label`, `SourcePath`, `SourceRef`, `Notes`, and `Variant=DOMAIN`. When `NORMALIZE_IDS=true`, a `NormalizedID` column is populated (strip trailing `_suffix` after last underscore, analysis-only; never replaces `NodeID`).

---

### Step 5 — Hyperedge + incidence construction (tool-emitted; hashing algorithm locked)

The tool emits hyperedges per `EDGESET` (default emits all 6 types when data is available):

- `IN_CATEGORY`: `PARENT_CATEGORY` → Category, `CHILD_KNOWLEDGE_TYPE` → KTY (from `discovered_knowledge_types.csv.CategoryID`)
- `HAS_SUBJECT`: `OWNER_KNOWLEDGE_TYPE` → KTY, `SUBJECT` → Subject (from `discovered_knowledge_subjects.csv.KnowledgeTypeID`)
- `HAS_ARTIFACT`: `OWNER_KNOWLEDGE_TYPE` → KTY, `ARTIFACT` → Artifact (from `artifact_enumeration.csv.KnowledgeTypeID`)
- `SUBJECT_MATERIALIZED_AS`: `SUBJECT` → Subject, `ARTIFACT` → Artifact (from `subject_artifact_mapping.csv`)
- `LEDGER_ROW`: `UNIT` → AtomicUnit, `CATEGORY` → Category, `KNOWLEDGE_TYPE` → KTY (0..N), `OBJECTIVE` → Objective (0..N) (from `discovered_ledger_rows.csv`)
- `KTY_SUPPORTS_OBJ`: `KNOWLEDGE_TYPE` → KTY, `OBJECTIVE` → Objective (from `kty_supports_obj.csv`)

**Missing-node references** (e.g., KTY references `CategoryID=CAT-999` with no CATEGORY node) are NOT silently dropped — the tool records a `*_REF_MISSING_NODE` WARNING and skips only that edge.

The registered builder owns ID generation, sort order, and canonical serialization. Record its source fingerprint and effective options rather than reproducing that implementation in the workflow.

---

### Step 6 — QA checks (tool-emitted, 9 checks)

The tool writes findings to `QA_Report.md` with PASS / WARNING / BLOCKER per check:

1. **Schema presence** — CSVs exist and have `SchemaVersion` headers.
2. **Referential integrity** — every incidence NodeID exists in `nodes.csv`; every incidence HyperedgeID exists in `hyperedges.csv`. BLOCKER on failure.
3. **Category membership integrity** — each `KNOWLEDGE_TYPE` has ≤1 `IN_CATEGORY` edge. `>1` = BLOCKER (partition ambiguity); `0` = WARNING.
4. **Subject attachment** — each `KNOWLEDGE_SUBJECT` participates in ≥1 `HAS_SUBJECT` edge. Otherwise WARNING (orphan subject).
5. **Artifact attachment** — each `KNOWLEDGE_ARTIFACT` participates in ≥1 `HAS_ARTIFACT` edge. Otherwise WARNING (orphan artifact).
6. **Bridge integrity** — each SUBJECT and each ARTIFACT participates in ≤1 `SUBJECT_MATERIALIZED_AS` edge. `>1` on SUBJECT = BLOCKER (split-subject); `>1` on ARTIFACT = BLOCKER (merged-artifact).
7. **Ledger integrity** (when `discovered_ledger_rows.csv` present) — each `ATOMIC_UNIT` appears in ≥1 `LEDGER_ROW` (WARNING otherwise); each unit maps to ≤1 category via ledger rows (`>1` = BLOCKER).
8. **ID collisions** — duplicate NodeIDs = BLOCKER. Duplicate NormalizedIDs (when enabled) = WARNING.
9. **Evidence completeness** — nodes/hyperedges missing `SourcePath` or `SourceRef` = WARNING.

The tool also records reference-miss warnings during edge construction (`CATEGORY_REF_MISSING_NODE`, `LEDGER_REF_MISSING_NODE`, etc.) to preserve provenance for unresolved references.

---

### Step 7 — Optional comparison mode

If `PRIOR_RUN_LABEL` is set in the brief:
1. Resolve `{prior_snapshot_path}` from the prior label (e.g., `{EXECUTION_ROOT}/_Aggregation/Hypergraph/HG_{PRIOR_RUN_LABEL}_*/`).
2. Pass `--prior-snapshot {prior_snapshot_path}` to the tool invocation in Step 4.

The tool loads the prior run's `hypergraph.json`, computes node/edge adds/removes by type, and writes:
- `delta` block in the new `hypergraph.json`
- "Delta vs prior run" section in `QA_Report.md`

---

### Step 8 — Publish snapshot + record provenance

After the tool invocation (Step 4) completes:

1. **Copy tool file for reproducibility** (required by STRUCTURE):
   ```sh
   cp tools/aggregation/build_hypergraph.py {snapshot}/build_hypergraph.py
   ```
2. **Record tool provenance** in `{snapshot}/Decision_Log.md`:
   - Absolute path of tool invoked: `tools/aggregation/build_hypergraph.py`
   - Git commit SHA at invocation time: `git rev-parse HEAD`
   - Full command line used (including all flags)
3. **Write `RUN_SUMMARY.md`** with `RUN_STATUS = OK|WARNINGS|FAILED_INPUTS` based on `QA_Report.md` blocker/warning counts.
4. **Update pointer:**
   ```sh
   tools/scaffolding/update_latest_pointer.sh {EXECUTION_ROOT}/_Aggregation/Hypergraph {snapshot_folder_name}
   ```
5. **Return to the invoking manager:**
   - snapshot path,
   - key counts (nodes/edges/incidences),
   - QA verdict summary (≤10 top issues),
   - recommended next action (e.g., run TASK (workflow: audit-hypergraph-closure)).

---
