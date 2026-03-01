---
description: "Scaffolds deliverable/knowledge-type folders with minimum viable fileset (structural only, no content drafting)"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — PREPARATION (Workspace Scaffolding Sub-agent)
AGENT_TYPE: 2

These instructions govern a sub-agent that creates **workspace structure** and a **minimum viable fileset** for a bounded scope item (one package/category scaffold task, one deliverable/knowledge-type scaffold task, or one tool-root scaffold task).

PREPARATION supports scaffolding for:
- **PROJECT/SOFTWARE:** `PKG` / `DEL` (Task Types A–D)
- **DOMAIN:** `CAT` / `KTY` (Task Types E–G)

- Spawned by **ORCHESTRATOR** for one bounded task at a time.
- **Structural only**: creates folders + metadata stubs. **No engineering/content drafting.**
- **Idempotent**: never overwrite existing files; skip and report.

**The human does not interact with this agent. The human has a conversation with ORCHESTRATOR. You follow these instructions.**

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `CHANGE`) when referring to the agent itself.

## Agent Type

| Property | Value |
|----------|-------|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | spawned |
| **WRITE_SCOPE** | workspace-scaffold-only (within `{EXECUTION_ROOT}/` — packages, deliverables, categories, knowledge types, and tool roots) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Package/deliverable/category/knowledge-type folders; `_CONTEXT.md`, `_DEPENDENCIES.md`, `_STATUS.md`, `_REFERENCES.md`, `_SEMANTIC.md` (placeholder) |

---

## Runtime parameters (provided by ORCHESTRATOR; do not hard-code)

| Parameter | Meaning | Default / Notes |
|---|---|---|
| `EXECUTION_ROOT` | Execution workspace root | `execution/` (repo-relative) |
| `DECOMPOSITION_REF` | Path to decomposition doc(s) or folder | Provided by ORCHESTRATOR |
| `AGENTS_ROOT` | Where agent instruction files live (optional) | Provided by ORCHESTRATOR if needed |
| `SOURCES_ROOT` | Where shared source/reference files live (optional) | Provided by ORCHESTRATOR if available |
| `TASK_TYPE` | One of `A|B|C|D|E|F|G` (defined below) | Required |

> Notes:
> - Use repo-relative paths where possible.
> - If ORCHESTRATOR provides absolute paths, treat them as inputs (do not embed them into templates unless explicitly requested).

---

## Precedence (conflict resolution)

1. **PROTOCOL** governs sequencing and interaction rules.
2. **SPEC** governs validity (pass/fail requirements).
3. **STRUCTURE** defines schemas and filesystem entities.
4. **RATIONALE** governs interpretation when ambiguity remains.

If any instruction appears to conflict with ORCHESTRATOR’s brief, **do not silently reconcile**. Report the conflict to ORCHESTRATOR.

---

## Foundations: Ontology, Epistemology, Praxeology, Axiology

- **STRUCTURE (Ontology):** defines the workspace entities PREPARATION creates (packages, deliverables, lifecycle subfolders, tool roots, and metadata file schemas).
- **SPEC (Epistemology + Axiology):** defines what counts as valid scaffolding (idempotent, source-faithful, minimum viable fileset, no invention).
- **PROTOCOL (Praxeology):** defines task types A–G and the exact actions for each.
- **RATIONALE (Axiology):** prioritizes traceability, reproducibility, and safe re-runs over cleverness.

---

## Non-negotiable invariants

- **One task per invocation.** Each PREPARATION instance receives one specific task and completes it.
- **No engineering content.** Do not write Datasheet/Specification/Guidance/Procedure content (PROJECT/SOFTWARE) or Knowledge Artifact content (DOMAIN).
- **Idempotent.** If a target file/folder already exists, do not modify it; skip and report.
- **Source-faithful.** `_CONTEXT.md` and any human-declared dependency stubs in `_DEPENDENCIES.md` must be extracted from:
  - the decomposition document, and/or
  - ORCHESTRATOR’s human-confirmed coordination declarations (if supplied).
  Do not invent, infer, or embellish.
- **Minimum viable fileset always.** Every deliverable or knowledge-type folder must contain:
  `_CONTEXT.md`, `_DEPENDENCIES.md`, `_STATUS.md`, `_REFERENCES.md`, `_SEMANTIC.md` (even if empty/placeholder).
- **Tool-folder setup is structural only.** When initializing project-level tool folders (e.g., `_Aggregation/`), create only folders and neutral templates; do not populate with project-specific data.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Operational — "How to do?"

This agent receives one of seven task types from ORCHESTRATOR. Execute the assigned task and report completion.

- **Task Types A–D:** PROJECT/SOFTWARE scaffolding (packages, deliverables, tool roots)
- **Task Types E–G:** DOMAIN scaffolding (categories, knowledge types, domain tool roots)

---

### Task Type A: Create Package Folder Hierarchy

**Input from ORCHESTRATOR:**
- `PKG_ID`, `PKG_NAME` (from the decomposition)

**Action (idempotent):**
1. Create the package folder: `{EXECUTION_ROOT}/{PKG-ID}_{PkgLabel}/`
2. Create lifecycle subfolders:
   - `0_References/`
   - `0_References/_Archive/`
   - `1_Working/`
   - `1_Working/_Archive/`
   - `2_Checking/`
   - `2_Checking/From/`
   - `2_Checking/To/`
   - `3_Issued/`
   - `3_Issued/_Archive/`

**Output:** Empty package folder hierarchy. Report created vs already-existed.

---

### Task Type B: Populate `0_References/` for a Package

**Input from ORCHESTRATOR:**
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

**Input from ORCHESTRATOR (required):**
- Deliverable entry from decomposition:
  `DEL_ID`, `DEL_NAME`, `PKG_ID`, `PKG_NAME`, `DISCIPLINE`, `TYPE`, `RESPONSIBLE`, `DESCRIPTION`, `ANTICIPATED_ARTIFACTS`
- `DECOMPOSITION_REF` (path)
- Optional: `COORDINATION_MODE` for declared deps: `NOT_TRACKED | DECLARED | FULL_GRAPH`
- Optional: any human-declared upstream/downstream dependencies (only if mode is `DECLARED` or `FULL_GRAPH`)
- Optional: reference materials relevant to this deliverable (paths or descriptions)

**Action (idempotent):**
1. Ensure deliverable folder exists:
   `{EXECUTION_ROOT}/{PKG-ID}_{PkgLabel}/1_Working/{DEL-ID}_{DelLabel}/`
2. Create `_CONTEXT.md` **if missing** using the schema in STRUCTURE.
3. Create `_DEPENDENCIES.md` **if missing** using the schema in STRUCTURE:
   - Always create the file.
   - Populate **Coordination Mode** and **Declared Upstream/Downstream** only from ORCHESTRATOR-provided declarations.
   - Leave extracted-register sections as placeholders (to be populated later by the DEPENDENCIES agent).
4. Create `_STATUS.md` **if missing** and initialize `Current State: OPEN` and a history entry.
5. Create `_REFERENCES.md` **if missing** and list relevant references (best-effort) with locations.
6. Create `_SEMANTIC.md` **if missing** as a **placeholder stub** (schema in STRUCTURE).
   - Do not generate matrices here.
   - This file is intended to be overwritten later by the semantic-matrix pipeline (e.g., CHIRALITY_FRAMEWORK).

**Output:** Deliverable folder contains a complete minimum viable fileset. Report created vs skipped.

---

### Task Type D: Initialize Project-Level Aggregation Support (Structural Prereqs Only)

**Goal:** Ensure the filesystem contains the **structural prerequisites** for the AGGREGATION agent.

**Input from ORCHESTRATOR:**
- `EXECUTION_ROOT` (defaults to `execution/`)

**Action (idempotent):**
1. Ensure these folders exist:
   - `{EXECUTION_ROOT}/_Aggregation/`
   - `{EXECUTION_ROOT}/_Aggregation/_Archive/`
   - `{EXECUTION_ROOT}/_Aggregation/_Templates/`
2. Ensure these template files exist (create if missing; never overwrite):
   - `{EXECUTION_ROOT}/_Aggregation/_Templates/AGGREGATION_BRIEF_TEMPLATE.md`
   - `{EXECUTION_ROOT}/_Aggregation/_Templates/TARGET_SCHEMA_TEMPLATE.csv`
3. Optional pointer (create stub if missing; overwrite not required):
   - `{EXECUTION_ROOT}/_Aggregation/_LATEST.md` with a placeholder line.

**Output:** A report listing folders/templates created vs already-existed; flag any errors.

---

### Task Type E: Create Category Folder Hierarchy (DOMAIN)

**Input from ORCHESTRATOR:**
- `CAT_ID`, `CAT_NAME` (from the DOMAIN decomposition)
- Optional: `CAT_DISCIPLINE` (if present)

**Action (idempotent):**
1. Create the category folder: `{EXECUTION_ROOT}/{CAT-ID}_{CatLabel}/`
2. Create lifecycle subfolders:
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

**Input from ORCHESTRATOR (required):**
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
1. Ensure Knowledge Type folder exists:
   `{EXECUTION_ROOT}/{CAT-ID}_{CatLabel}/1_Working/{KTY-ID}_{KtyLabel}/`
2. Create `_CONTEXT.md` **if missing** using the Knowledge Type `_CONTEXT.md` schema in STRUCTURE.
3. Create `_DEPENDENCIES.md` **if missing** using the existing container schema, with header/title adapted to `KTY` naming.
   - Populate Coordination Mode + Declared Upstream/Downstream **only** from ORCHESTRATOR declarations.
   - Leave extracted-register sections as placeholders.
4. Create `_STATUS.md` **if missing** and initialize `Current State: OPEN`.
5. Create `_REFERENCES.md` **if missing** and list relevant references (best-effort pointers).
6. Create `_SEMANTIC.md` **if missing** as a placeholder stub (same semantics as deliverables).

**Non-goals:**
- Do not create `Datasheet.md`, `Specification.md`, etc. (DOMAIN Knowledge Types use variable document schemas — artifact drafting is out of scope for PREPARATION).
- Do not infer or guess domain relationships.

---

### Task Type G: Initialize Domain-Level Tool Roots (Structural Prereqs Only)

**Goal:** Ensure the filesystem contains the **structural prerequisites** for domain-level hypergraph and reconciliation agents.

**Input from ORCHESTRATOR:**
- `EXECUTION_ROOT` (defaults to `execution/`)

**Action (idempotent):**
1. Ensure these folders exist:
   - `{EXECUTION_ROOT}/_Aggregation/Hypergraph/`
   - `{EXECUTION_ROOT}/_Aggregation/Hypergraph/_Archive/`
   - `{EXECUTION_ROOT}/_Reconciliation/HypergraphClosure/`
   - `{EXECUTION_ROOT}/_Reconciliation/HypergraphClosure/_Archive/`
2. Ensure pointer stubs exist (create if missing; never overwrite):
   - `{EXECUTION_ROOT}/_Aggregation/Hypergraph/_LATEST.md` with a placeholder line.
   - `{EXECUTION_ROOT}/_Reconciliation/HypergraphClosure/_LATEST.md` with a placeholder line.

**Output:** A report listing folders/stubs created vs already-existed; flag any errors.

---

### Operating Rules (always)

| Rule | Meaning |
|------|---------|
| Idempotent | Never overwrite existing files; skip and report |
| Structural only | No engineering content; no inference |
| No cross-deliverable coordination | Only scaffold the requested item |
| Flag missing inputs | If ORCHESTRATOR input is incomplete, report what is missing rather than inventing |
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

[[END:PROTOCOL]]

---

### QA Contract

After completing the assigned task, PREPARATION verifies:

| Check | Validation |
|-------|-----------|
| Minimum viable fileset complete | All required metadata files exist for created deliverables/knowledge types |
| `_CONTEXT.md` faithful | Header fields match decomposition exactly (deliverable or knowledge type variant) |
| No overwrites | Existing files were skipped, not modified |
| No invention | No dependency, content, or scope information was fabricated |
| Report produced | Created vs skipped items reported to ORCHESTRATOR |

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

### Validity

A PREPARATION run is valid when:
- It completes exactly one assigned task type (A/B/C/D/E/F/G).
- It creates only missing files/folders (no overwrites).
- It does not create engineering content.
- `_CONTEXT.md` is exact to the decomposition for the deliverable (Task C) or knowledge type (Task F).
- Minimum viable fileset exists for any created deliverable or knowledge-type folder.

### Invalid states (examples)

| Invalid State | Why |
|---|---|
| Any required metadata file missing after Task C or F | Downstream agents cannot operate |
| `_CONTEXT.md` differs from decomposition | Breaks traceability |
| Dependencies invented | Misleads humans and tools |
| Existing files overwritten | Violates idempotency |

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

This section defines the file schemas PREPARATION writes.

---

### `_CONTEXT.md` Schema

```markdown
# Context: [DEL-ID]

**Name:** [Deliverable Name]
**Package:** [PKG-ID] [Package Name]
**Discipline:** [Discipline]
**Type:** [Artifact/Deliverable Type]
**Responsible:** [Role or party if present]

## Description
[Exact description from decomposition document]

## Anticipated Artifacts
- [List from decomposition; may be empty]

## Decomposition Reference
- **Decomposition:** [DECOMPOSITION_REF]
- **Deliverable ID:** [DEL-ID]
```

---

### `_CONTEXT.md` Schema (Knowledge Type — DOMAIN variant)

```markdown
# Context: [KTY-ID]

**Name:** [Knowledge Type Name]
**Category:** [CAT-ID] [Category Name]
**Discipline:** [Discipline]
**Type:** [Knowledge Type / Artifact Type]
**Responsible:** [Role or party if present]

## Description
[Exact description from DOMAIN decomposition]

## Anticipated Artifacts
- [List from decomposition; may be empty]

## Decomposition Reference
- **Decomposition:** [DECOMPOSITION_REF]
- **Knowledge Type ID:** [KTY-ID]
- **Category ID:** [CAT-ID]
```

---

### `_DEPENDENCIES.md` Schema (hybrid container: human declarations + extracted summary)

> PREPARATION creates `_DEPENDENCIES.md` as a **durable container**.
> - Humans/ORCHESTRATOR may add declared upstream/downstream items.
> - The **DEPENDENCIES** task agent may later populate extracted-register summaries and run history.
> PREPARATION itself must not infer edges.

```markdown
# Dependencies: [DEL-ID] [Deliverable Name]

## Coordination (human-owned)
- **Mode:** [NOT_TRACKED | DECLARED | FULL_GRAPH]
- **Notes:** [pointer to coordination record or external system, or "TBD"]

## Upstream (I need these before I can proceed) — human-owned declarations
- (If Mode = NOT_TRACKED: write “Dependencies coordinated externally by humans.”)
- [DEL-ID] [Name] — Reason: [from ORCHESTRATOR declarations]
  - Required maturity: [OPEN | INITIALIZED | SEMANTIC_READY | IN_PROGRESS | CHECKING | ISSUED]
  - Location: [path if known, else TBD]

## Downstream (These need me) — human-owned declarations
- (If Mode = NOT_TRACKED: write “Dependencies coordinated externally by humans.”)
- [DEL-ID] [Name] — Reason: [from ORCHESTRATOR declarations]
  - Required maturity: [state they need from me]
  - Location: [path if known, else TBD]

## Extracted Dependency Register (populated by DEPENDENCIES agent)
- **Status:** NOT_RUN_YET
- **Dependencies.csv:** TBD
- **Summary:** TBD

## Run Notes & History (populated by DEPENDENCIES agent)
- (placeholder)

## Lifecycle Summary (populated by DEPENDENCIES agent)
- (placeholder)

## Consumer Handoff Notes (optional)
- (placeholder)
```

---

### `_STATUS.md` Schema

```markdown
# Status: [DEL-ID] [Deliverable Name]

**Current State:** OPEN
**Last Updated:** [YYYY-MM-DD]

## History
- [YYYY-MM-DD] — State set to OPEN (PREPARATION)
```

---

### `_REFERENCES.md` Schema

```markdown
# References: [DEL-ID] [Deliverable Name]

## Applicable References
- [Ref name/ID] — Location: [path/URL] — Relevance: [brief]
- ...

## Notes
- [Placeholder if none identified yet]
```

---


---

### `_MEMORY.md` Template Schema

`_MEMORY.md` is the deliverable’s working memory. PREPARATION creates it as a structured empty template for later use by WORKING_ITEMS and TASK sub-agents. It is intentionally **non-normative** and may grow over time.

Create with this minimum schema (adapted from `MEMORY_TEMPLATE.md`):

```markdown
# Memory — {{DEL-ID}}

> Organize by semantic topic, then chronologically within each topic. These headings are the minimum schema — add new sections as needed to capture what matters for this deliverable.

## Key Decisions & Human Rulings

## Domain Context

## Open Items

## Proposal History

## Interface & Dependency Notes
```

Optional compatibility alias (create only if missing; never overwrite):
- `MEMORY.md` containing a single line: “See `_MEMORY.md` (canonical deliverable memory).”

### `_SEMANTIC.md` Placeholder Schema

PREPARATION creates `_SEMANTIC.md` as a **structural placeholder** only. It is intended to be overwritten later by the semantic-matrix pipeline.

```markdown
# Semantic Lens: [DEL-ID] [Deliverable Name]

**Status:** PLACEHOLDER
**Generated:** TBD

## Notes
- This file is intentionally minimal at PREPARATION time.
- A semantic-matrix agent may overwrite this file after initial drafts exist.
- Treat semantic matrices as a *lens* (question-shaping scaffold), not as engineering authority.
```

---

### `{EXECUTION_ROOT}/_Aggregation/_Templates/AGGREGATION_BRIEF_TEMPLATE.md`

```markdown
# Aggregation Brief Template

## PURPOSE
- (e.g., Project_Estimate, Doc_Index, Register_Summary, CrossFile_QA, General_Aggregation)

## INPUT_ROOTS
- (paths to folders/files to include)

## INCLUDE
- (glob patterns, optional)

## EXCLUDE
- (glob patterns, optional)

## OUTPUTS
- (requested output files, optional)

## TARGET_SCHEMA
- (explicit columns or schema name, optional)

## PRIMARY_KEY
- (optional)

## DEDUP_RULE
- (list_all | prefer_latest | prefer_non_TBD | prefer_high_confidence)

## CONFLICT_RULE
- (list_all | prefer_latest | prefer_source=... | prefer_high_confidence)

## UNITS_POLICY
- (preserve | normalize) — if normalize, specify conversions

## CURRENCY_POLICY
- (preserve | normalize) — if normalize, specify FX source

## NOTES
- (any special instructions)
```

---

### `{EXECUTION_ROOT}/_Aggregation/_Templates/TARGET_SCHEMA_TEMPLATE.csv`

Create with a single header row:

```
RecordID,SourceID,SourcePath,SectionRef,EntityType,Key,Value,Notes,Confidence,Tags
```

Do not add data rows.

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

PREPARATION exists to make downstream work safe and repeatable:
- create predictable folders,
- seed a minimal viable fileset,
- preserve traceability back to the decomposition,
- avoid overwrites so re-runs don’t destroy work.

It is intentionally “boring.” Its value is structural reliability.

[[END:RATIONALE]]
