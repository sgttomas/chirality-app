# preparation — method

## Method

Before each scaffold call inventory the target paths. Capture each CREATED_PATH: record emitted by scaffold_deliverable.sh or scaffold_package.sh and compare with the pre-run inventory and fill only paths created in this invocation. Existing empty files also count as existing work; leave them unchanged unless a separate repair brief authorizes them. Initialize OPEN status only when _STATUS.md was newly created. Return exact created_paths and skipped_paths, not only totals.

### Operational — "How to do?"

TASK receives one of seven operation modes from WORKING_ITEMS (workflow: project-setup). Execute the assigned task and report completion.

- **Task Types A–D:** PROJECT/SOFTWARE scaffolding (packages, deliverables, tool roots)
- **Task Types E–G:** DOMAIN scaffolding (categories, knowledge types, domain tool roots)

---

### Task Type A: Create Package Folder Hierarchy

**Input from WORKING_ITEMS (workflow: project-setup):**
- `PKG_ID`, `PKG_NAME` (from the decomposition)

**Action (idempotent):**
Run: `tools/scaffolding/scaffold_package.sh {EXECUTION_ROOT} {PKG_ID} {PkgLabel}`

This creates the package folder with all 9 lifecycle subfolders (`0_References/`, `0_References/_Archive/`, `1_Working/`, `1_Working/_Archive/`, `2_Checking/`, `2_Checking/From/`, `2_Checking/To/`, `3_Issued/`, `3_Issued/_Archive/`). Idempotent — reports created vs already-existed.

**Output:** Empty package folder hierarchy.

---

### Task Type B: Populate `0_References/` for a Package

**Input from WORKING_ITEMS (workflow: project-setup):**
- `PKG_ID`, `PKG_NAME`
- Optional: `PKG_DISCIPLINE`
- Optional: list of available reference materials (paths or descriptions)

**Action (idempotent):**
1. Navigate to `{EXECUTION_ROOT}/{PKG-ID}_{PkgLabel}/0_References/`
2. If reference materials are files that can be copied or linked, place them in `0_References/` **only if not already present**.
3. If reference materials are external or cannot be copied, create `_REFERENCE_INDEX.md` listing:
   - Reference ID or name
   - Location (path, URL, or description)
   - Relevance to this package
4. If no references are available, create `_REFERENCE_INDEX.md` noting that references are not identified yet.

**Output:** Populated `0_References/` folder (files and/or index). Report what was placed/indexed and any missing materials.

---

### Task Type C: Populate One Deliverable Folder (Minimum Viable Fileset)

**Input from WORKING_ITEMS (workflow: project-setup) (required):**
- Deliverable entry from decomposition:
  `DEL_ID`, `DEL_NAME`, `PKG_ID`, `PKG_NAME`, `DISCIPLINE`, `TYPE`, `RESPONSIBLE`, `DESCRIPTION`, `ANTICIPATED_ARTIFACTS`
- `DECOMPOSITION_REF` (path)
- Optional: `COORDINATION_MODE` for declared deps: `NOT_TRACKED | DECLARED | FULL_GRAPH`
- Optional: any human-declared upstream/downstream dependencies (only if mode is `DECLARED` or `FULL_GRAPH`)
- Optional: reference materials relevant to this deliverable (paths or descriptions)

**Action (idempotent):**
1. Optionally validate the deliverable ID before creating paths:
   - `tools/validation/validate_id_format.sh DEL {DEL_ID}`
   - If invalid, do not scaffold; report the invalid ID to WORKING_ITEMS (workflow: project-setup).
2. Create deliverable folder with stubs using the deterministic scaffolding tool:
   - `tools/scaffolding/scaffold_deliverable.sh {pkg_folder}/1_Working {DEL_ID} {DelLabel}`
   This creates the folder and touches the 5 stub files (`_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_SEMANTIC.md`).
3. Populate newly created `_CONTEXT.md` content using the schema in contract.md (LLM work — fills the stub created above).
4. Populate newly created `_DEPENDENCIES.md` content using the schema in contract.md:
   - Populate **Coordination Mode** and **Declared Upstream/Downstream** only from WORKING_ITEMS (workflow: project-setup)-provided declarations.
   - Leave extracted-register sections as placeholders (to be populated later by the `dependency-extract` workflow via TASK).
5. If `_STATUS.md` was newly created, initialize it using the deterministic status tool:
   - `tools/scaffolding/write_status.sh {deliverable_folder} OPEN TASK`
6. Populate newly created `_REFERENCES.md` and list relevant references (best-effort) with locations.
7. `_SEMANTIC.md` is left as a **placeholder stub** (created by the scaffold tool above).
   - Do not generate matrices here.
   - This file is intended to be overwritten later by the semantic-matrix pipeline (the `semantic-matrix-build` workflow, dispatched via TASK).
8. Verify the result with the deterministic validator:
   - `tools/validation/check_min_viable_fileset.sh {deliverable_folder}`
   - If the check fails, report the missing files and mark the task invalid.

When the brief selects `CREATE_MEMORY=true` and grants its exact path, create missing `_MEMORY.md` from `docs/templates/MEMORY_TEMPLATE.md`; default false. Pass --memory to scaffold_deliverable.sh for this selection; it creates only missing memory and emits CREATED_PATH. Include it in created/skipped paths.

**Output:** Deliverable folder contains a complete minimum viable fileset validated by the deterministic checker. Report created vs skipped.

---

### Task Type D: Initialize Project-Level Aggregation Support (Structural Prereqs Only)

**Goal:** Ensure the filesystem contains the **structural prerequisites** for the TASK (workflow: aggregation) agent.

**Input from WORKING_ITEMS (workflow: project-setup):**
- `EXECUTION_ROOT` (defaults to `execution/`)

**Action (idempotent):**
1. Bootstrap tool root: `tools/scaffolding/scaffold_tool_root.sh {EXECUTION_ROOT} _Aggregation`
   This creates `_Aggregation/`, `_Aggregation/_Archive/`, and `_LATEST.md` stub.
2. Create additional subfolders if missing: `_Aggregation/_Templates/`
3. Ensure these template files exist (create if missing; never overwrite):
   - `{EXECUTION_ROOT}/_Aggregation/_Templates/AGGREGATION_BRIEF_TEMPLATE.md`
   - `{EXECUTION_ROOT}/_Aggregation/_Templates/TARGET_SCHEMA_TEMPLATE.csv`

**Output:** A report listing folders/templates created vs already-existed; flag any errors.

---

### Task Type E: Create Category Folder Hierarchy (DOMAIN)

**Input from WORKING_ITEMS (workflow: project-setup):**
- `CAT_ID`, `CAT_NAME` (from the DOMAIN decomposition)
- Optional: `CAT_DISCIPLINE` (if present)

**Action (idempotent):**
Run: `tools/scaffolding/scaffold_package.sh {EXECUTION_ROOT} {CAT_ID} {CatLabel}`
(Same folder schema as packages — `CAT_ID`/`CatLabel` map directly to the tool's `PKG_ID`/`PkgLabel` inputs.)

This creates the category folder with all 9 lifecycle subfolders:
   - `0_References/`
   - `0_References/_Archive/`
   - `1_Working/`
   - `1_Working/_Archive/`
   - `2_Checking/`
   - `2_Checking/From/`
   - `2_Checking/To/`
   - `3_Issued/`
   - `3_Issued/_Archive/`

**Output:** Empty category folder hierarchy. Report created vs already-existed.

---

### Task Type F: Populate One Knowledge Type Folder (Minimum Viable Fileset) (DOMAIN)

**Input from WORKING_ITEMS (workflow: project-setup) (required):**
- Knowledge Type entry from DOMAIN decomposition:
  - `KTY_ID`, `KTY_NAME`
  - `CAT_ID`, `CAT_NAME`
  - `DISCIPLINE`, `TYPE`, `RESPONSIBLE`, `DESCRIPTION`
  - `ANTICIPATED_ARTIFACTS`
- `DECOMPOSITION_REF` (path)
- Optional: `COORDINATION_MODE` (same enum; default `NOT_TRACKED`)
- Optional: any human-declared upstream/downstream relationships (only if mode is `DECLARED` or `FULL_GRAPH`)
- Optional: reference materials relevant to this Knowledge Type (paths or descriptions)

**Action (idempotent):**
1. Optionally validate the Knowledge Type ID before creating paths:
   - `tools/validation/validate_id_format.sh KTY {KTY_ID}`
   - If invalid, do not scaffold; report the invalid ID to WORKING_ITEMS (workflow: project-setup).
2. Create KTY folder with stubs using the deterministic scaffolding tool:
   - `tools/scaffolding/scaffold_deliverable.sh {cat_folder}/1_Working {KTY_ID} {KtyLabel}`
   (Same tool as deliverables — `KTY_ID`/`KtyLabel` map to `DEL_ID`/`DelLabel` inputs.)
3. Populate newly created `_CONTEXT.md` content using the Knowledge Type schema in contract.md (LLM work).
4. Populate newly created `_DEPENDENCIES.md` content using the existing container schema, with header/title adapted to `KTY` naming.
   - Populate Coordination Mode + Declared Upstream/Downstream **only** from WORKING_ITEMS (workflow: project-setup) declarations.
   - Leave extracted-register sections as placeholders.
5. If `_STATUS.md` was newly created, initialize it using the deterministic status tool:
   - `tools/scaffolding/write_status.sh {kty_folder} OPEN TASK`
6. Populate newly created `_REFERENCES.md` and list relevant references (best-effort pointers).
7. `_SEMANTIC.md` is left as a placeholder stub (created by scaffold tool above).
8. Verify the result with the deterministic validator:
   - `tools/validation/check_min_viable_fileset.sh {kty_folder}`
   - If the check fails, report the missing files and mark the task invalid.

**Non-goals:**
- Do not create `Datasheet.md`, `Specification.md`, etc. (DOMAIN Knowledge Types use variable document schemas — artifact drafting is out of scope for TASK).
- Do not infer or guess domain relationships.

---

### Task Type G: Initialize Domain-Level Tool Roots (Structural Prereqs Only)

**Goal:** Ensure the filesystem contains the **structural prerequisites** for domain-level hypergraph and reconciliation agents.

**Input from WORKING_ITEMS (workflow: project-setup):**
- `EXECUTION_ROOT` (defaults to `execution/`)

**Action (idempotent):**
1. Bootstrap hypergraph tool root: `tools/scaffolding/scaffold_tool_root.sh {EXECUTION_ROOT}/_Aggregation Hypergraph`
2. Bootstrap closure tool root: `tools/scaffolding/scaffold_tool_root.sh {EXECUTION_ROOT}/_Evaluation HypergraphClosure`

Both calls create the folder, `_Archive/` subfolder, and `_LATEST.md` stub.

**Output:** A report listing folders/stubs created vs already-existed; flag any errors.

---

### Operating Rules (always)

| Rule | Meaning |
|------|---------|
| Idempotent | Never overwrite existing files; skip and report |
| Structural only | Use deterministic tools for filesystem/state operations; use the language model only to populate metadata text from provided sources; no engineering content; no inference |
| No cross-deliverable coordination | Only scaffold the requested item |
| Flag missing inputs | If WORKING_ITEMS (workflow: project-setup) input is incomplete, report what is missing rather than inventing |
| Exact extraction | `_CONTEXT.md` fields must match decomposition exactly |

---

### Filesystem-safe folder labels

Use filesystem-safe labels derived from canonical names:

**Sanitize(name)**:
- Replace any of these characters with `-`: `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`
- Collapse consecutive whitespace to a single space
- Trim leading/trailing whitespace

Folder names:
- `{PKG-ID}_{PkgLabel}` where `PkgLabel = Sanitize(Package Name)`
- `{DEL-ID}_{DelLabel}` where `DelLabel = Sanitize(Deliverable Name)`
- `{CAT-ID}_{CatLabel}` where `CatLabel = Sanitize(Category Name)`
- `{KTY-ID}_{KtyLabel}` where `KtyLabel = Sanitize(Knowledge Type Name)`

Always record canonical (unsanitized) names inside `_CONTEXT.md` for traceability.

---

### QA Contract

After completing the assigned task, TASK verifies:

| Check | Validation |
|-------|-----------|
| Minimum viable fileset complete | Run `tools/validation/check_min_viable_fileset.sh` for each created deliverable/knowledge-type folder and require PASS |
| `_CONTEXT.md` faithful | Header fields match decomposition exactly (deliverable or knowledge type variant) |
| No overwrites | Existing files were skipped, not modified |
| No invention | No dependency, content, or scope information was fabricated |
| Report produced | Created vs skipped items reported to WORKING_ITEMS (workflow: project-setup) |

---
