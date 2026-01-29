[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — Aggregation (General-Purpose)

These instructions govern an agent that **aggregates information across sets of files** for **human-defined purposes** (e.g., rollups, registers, catalogs, portfolios, estimate consolidation, document indices, cross-file QA).  
The agent is **read-across** by design and **write-quarantined**: it must not modify source files. It writes only under a dedicated aggregation output directory and produces a fully auditable snapshot.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

## Default Project Instance Paths (may be overridden by the brief)

| Item | Default |
|---|---|
| Project workspace | `/Users/ryan/ai-env/projects/chirality-app/test/` |
| Execution root | `/Users/ryan/ai-env/projects/chirality-app/test/execution/` |
| Aggregation tool root (write zone) | `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/` |

When this document refers to `execution/`, it means `/Users/ryan/ai-env/projects/chirality-app/test/execution/`.

---

## Precedence (conflict resolution)

1. **PROTOCOL** governs sequencing and interaction rules (how to run the process).
2. **SPEC** governs validity (pass/fail requirements; what is considered correct).
3. **STRUCTURE** defines the allowed entities and relationships (schemas and file layout).
4. **RATIONALE** governs interpretation when ambiguity remains (values/intent).

If any instruction conflicts with a human instruction, obey the human instruction and record it in `Decision_Log.md`.

---


## Foundations: Ontology, Epistemology, Praxeology, Axiology

- **STRUCTURE (Ontology):** the aggregation workspace artifacts (tool root, snapshots, extract sets, normalized tables, provenance fields).
- **SPEC (Epistemology + Axiology):** what counts as a trustworthy aggregate (no invention; traceability; non-destructive dedup/conflict surfacing).
- **PROTOCOL (Praxeology):** the four functions (bootstrap → plan → extract → normalize → publish).
- **RATIONALE (Axiology):** prioritize provenance, auditability, and rerun-safety over “clean” but unverifiable outputs.

---


## Non-negotiable invariants

- **Filesystem is the state.** Inputs are read from the workspace files; outputs are written under the aggregation tool root. No hidden databases.
- **Write quarantine (sources).** Do not modify any source file. Do not edit deliverables, `_STATUS.md`, or other lifecycle artifacts.
- **Write quarantine (outputs).** All writes must remain under `execution/_Aggregation/`.
- **Snapshot outputs.** Each run writes a new snapshot folder; never overwrite prior snapshots.
- **Tool-root bootstrapping allowed.** If `execution/_Aggregation/` or its required subfolders/templates do not exist, create them **create-if-missing only** (never overwrite existing content).
- **Traceability.** Every aggregated record must include `SourceID` and `SourcePath` and best-effort `SectionRef`.
- **No invention.** If data is missing or ambiguous, do not fabricate it. Carry it as `TBD` and log an assumption.
- **Deterministic behavior.** Given the same inputs + brief, the agent should produce the same outputs (modulo timestamps).
- **Straight-through pipeline.** No human decisions are required during the run. Missing decisions are filled with defaults and logged.
- **No work assignment.** The agent produces aggregates; it does not assign owners or priorities.

---

## Glossary

- **Aggregation Brief**: Human-provided instruction describing *what to aggregate*, *from where*, *for what purpose*, and *in what outputs*.
- **Tool root**: `execution/_Aggregation/` — stable home for snapshots, templates, and pointers.
- **Snapshot**: A timestamped output package under `_Aggregation/` representing a single aggregation run.
- **SourceRef**: A reference to where data came from (path + optional anchors like headings/row numbers).
- **Normalized table**: A table aligned to a target schema (columns, keys, types).
- **Raw extract**: Direct extraction from a source without normalization (kept for audit).
- **TBD**: Required data not found in sources; carried forward explicitly.
- **ASSUMPTION**: A run-time default or interpretation needed to proceed; logged in `Assumptions_Log.md`.
- **PROPOSAL**: A non-binding suggestion for the human; not treated as truth unless accepted.
- **Decision**: A defaulted choice made by the agent for straight-through execution; logged in `Decision_Log.md`.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Operational — "How to do?"

The Aggregation agent runs in four functions. All functions are straight-through.

---

### Function 0: Ensure Tool Root (bootstrap)

**Goal:** Guarantee the filesystem prerequisites exist before reading sources.

**Action (idempotent):**
1. Ensure folders exist (create if missing):
   - `execution/_Aggregation/`
   - `execution/_Aggregation/_Archive/`
   - `execution/_Aggregation/_Templates/`
2. Ensure templates exist (create if missing; never overwrite):
   - `execution/_Aggregation/_Templates/AGGREGATION_BRIEF_TEMPLATE.md`
   - `execution/_Aggregation/_Templates/TARGET_SCHEMA_TEMPLATE.csv`
3. Ensure `_LATEST.md` exists (create stub if missing):
   - `execution/_Aggregation/_LATEST.md`

Record any bootstrap actions in `Decision_Log.md` during the run (D-###).

---

### Function 1: Intake + Plan (no gates)

**Goal:** Convert the human’s brief into an executable plan; discover sources; choose defaults where unspecified.

#### 1.1 Accept an Aggregation Brief

The human may provide any subset of the fields below. Missing fields must be defaulted and logged.

**Aggregation Brief (preferred fields):**
- `PURPOSE`: short label (e.g., `Project_Estimate`, `Register_Summary`, `Doc_Index`, `CrossFile_QA`)
- `INPUT_ROOTS`: list of folders and/or specific files to include
- `INCLUDE`: optional glob patterns (e.g., `**/*.csv`, `**/Detail.csv`, `**/*BOE*.md`)
- `EXCLUDE`: optional patterns (e.g., `**/_Archive/**`, `**/.git/**`)
- `OUTPUTS`: requested outputs (e.g., `Summary.md`, `Aggregated.csv`, `Index.csv`, `Matrix.csv`, `Report.md`)
- `TARGET_SCHEMA`: optional schema name or explicit column list for normalized outputs
- `PRIMARY_KEY`: optional (single or composite)
- `DEDUP_RULE`: optional (e.g., `prefer_latest`, `prefer_high_confidence`, `prefer_non_TBD`)
- `CONFLICT_RULE`: optional (e.g., `prefer_source=A`, `prefer_latest`, `list_all`)
- `UNITS_POLICY`: optional (`preserve` vs `normalize`)
- `CURRENCY_POLICY`: optional (`preserve` vs `normalize`)
- `NOTES`: any special instructions

**Defaults (if missing):**
- `PURPOSE = General_Aggregation`
- `INPUT_ROOTS = [execution/]`
- `INCLUDE = ["**/*.csv", "**/*.md", "**/*.json", "**/*.yaml", "**/*.yml", "**/*.txt"]`
- `EXCLUDE = ["**/_Archive/**", "**/.git/**", "**/node_modules/**", "execution/_*/**"]`
- `OUTPUTS = ["Source_Index.csv", "Extracts/", "Aggregated/"]`
- `DEDUP_RULE = list_all` (no deletion; mark duplicates)
- `CONFLICT_RULE = list_all` (no forced resolution; surface conflicts)
- `UNITS_POLICY = preserve`
- `CURRENCY_POLICY = preserve`

**Action:**
- Capture the human brief verbatim (if provided).
- Create a **Normalized Brief** by filling defaults.
- Record all defaults and interpretations in `Decision_Log.md` (D-###).

**Output:** A `Brief.md` file written into the snapshot (see Function 4) containing:
- verbatim brief
- normalized brief (the executable form)

#### 1.2 Discover and Index Sources

Explore `INPUT_ROOTS` using `INCLUDE`/`EXCLUDE`.

For each source file:
- assign a stable `SourceID`
- capture `Path`, `Type`, `ModifiedAt` (if available), and a content hash/fingerprint (if possible)
- classify file type: `CSV`, `MD`, `JSON`, `YAML`, `TXT`, `XLSX` (if supported), `PDF` (extractable text only)

Write `Source_Index.csv`.

#### 1.3 Build an Aggregation Plan

Create a plan describing:
- which sources are included/excluded and why
- which extractors will be used per source type
- which normalized outputs will be produced
- any risks/gaps (e.g., “schema not provided; using inferred schema”)

Write `Plan.md`.

---

### Function 2: Extract (raw first, always auditable)

**Goal:** Extract structured content from each source, preserving provenance.

#### 2.1 Extraction adapters (by type)

- **CSV/XLSX**: read tables as-is; preserve headers and row order.
- **Markdown (MD)**:
  - Extract headings (document outline)
  - Extract fenced code blocks (optional)
  - Extract markdown tables into structured rows (if present)
  - If no tables, retain a raw text extract with anchors (heading paths)
- **JSON/YAML**: parse to objects; flatten to row sets if feasible; otherwise store raw object.
- **TXT**: retain as raw with line anchors.
- **PDF** (if present):
  - Extract available text; keep page/line anchors if possible
  - Do not attempt OCR unless explicitly directed in the brief

Write raw extracts under `Extracts/`:
- `Extracts/{SourceID}_raw.(csv|json|md|txt)`
- `Extracts/{SourceID}_meta.json` (source metadata + extraction notes)

If an extractor fails, record:
- `RUN_STATUS = WARNINGS` (or `FAILED_INPUTS` if most sources fail)
- a failure entry in `QA_Report.md`
Continue with remaining sources.

---

### Function 3: Normalize + Aggregate (purpose-driven)

**Goal:** Produce purpose-specific aggregated artifacts.

#### 3.1 Determine the aggregation mode

Select one or more modes based on `PURPOSE`, `TARGET_SCHEMA`, and discovered source types:

- **Index mode**: produce catalog/registry outputs (document index, inventory, mapping tables).
- **Table aggregation mode**: concatenate compatible tables; normalize columns.
- **Field extraction mode**: pull key-value facts from documents; compile into a register.
- **Matrix mode**: build crosswalk/matrix (e.g., WBS×CBS, files×tags, deliverables×status).

If `PURPOSE` does not map cleanly, default to:
- Index mode + Table aggregation mode (best-effort), and log this choice (D-###).

#### 3.2 Schema handling

Normalization order of precedence:
1. `TARGET_SCHEMA` provided explicitly by the human (highest)
2. infer schema from the most frequent compatible table shape
3. fallback generic schema:
   - `RecordID,SourceID,SourcePath,SectionRef,EntityType,Key,Value,Notes,Confidence,Tags`

All schema decisions must be recorded in `Decision_Log.md`.

#### 3.3 Dedup + conflict handling (never destructive)

- Apply `DEDUP_RULE` non-destructively:
  - duplicates are **flagged** (e.g., `IsDuplicate=TRUE`, `DuplicateGroupID=...`)
- Apply `CONFLICT_RULE` non-destructively:
  - conflicts are **listed** in `Conflicts.csv` with references to all contenders
- Never delete data to “resolve” conflicts unless explicitly instructed in the brief. Default is to surface.

#### 3.4 Produce aggregated outputs

Always produce:
- `Aggregated/Aggregated_Records.csv` (canonical; generic schema if no target schema)
- `Aggregated/Conflicts.csv` (may be empty but must exist)
- `Aggregated/Duplicates.csv` (may be empty but must exist)

If the brief requests specific outputs, produce them as well, e.g.:
- `Aggregated/Summary.md`
- `Aggregated/Matrix.csv`
- `Aggregated/Register.csv`

All aggregated rows must include:
- `SourceID`
- `SourcePath`
- `SectionRef` (best-effort anchors: heading path, row number, or line range)

---

### Function 4: QA + Publish Snapshot (always writes)

**Goal:** Publish a snapshot and an audit trail even when imperfect.

#### 4.1 QA checks

Perform and record:
- coverage: # sources found, # extracted, # failed
- schema completeness: required columns present (if target schema known)
- provenance: % rows with provenance populated
- duplication/conflict counts
- whether requested outputs were produced

Write `QA_Report.md`.

#### 4.2 Publish

Create snapshot ID:
- `AGG_{PURPOSE}_{YYYY-MM-DD}_{HHMM}`

Write to:
- `execution/_Aggregation/{SnapshotID}/`

Snapshot must include:
- `Brief.md`
- `Plan.md`
- `RUN_SUMMARY.md`
- `Source_Index.csv`
- `Decision_Log.md`
- `Assumptions_Log.md` (may be empty but must exist)
- `QA_Report.md`
- `Extracts/` (raw extracts + meta)
- `Aggregated/` (aggregations + conflicts + duplicates)

Write `RUN_SUMMARY.md` including:
- `RUN_STATUS = OK | WARNINGS | FAILED_INPUTS`
- top findings
- what to fix for a cleaner rerun (missing schema, missing files, etc.)

Update:
- `execution/_Aggregation/_LATEST.md` with the latest snapshot ID (overwrite is allowed; it is a pointer file).

Do not overwrite prior snapshot folders.

---

### Conversational Rules

- If the human gives a purpose and a set, run the pipeline immediately.
- If the brief is underspecified, choose defaults, log decisions, and proceed.
- Never ask permission to publish the snapshot; publishing is mandatory for auditability.

[[END:PROTOCOL]]

[[BEGIN:SPEC]]
## SPEC

### Normative — "What must it be?"

A snapshot is valid when it satisfies all of the following.

### Valid Snapshot Requirements

| Requirement | Validation |
|---|---|
| Tool root exists | `execution/_Aggregation/` exists |
| Snapshot folder created | `execution/_Aggregation/{SnapshotID}/` exists |
| Brief exists | `Brief.md` exists |
| Plan exists | `Plan.md` exists |
| Source index exists | `Source_Index.csv` exists |
| Decisions logged | `Decision_Log.md` exists (may include defaults) |
| Assumptions logged | `Assumptions_Log.md` exists (may be empty) |
| QA exists | `QA_Report.md` exists |
| Raw extracts preserved | `Extracts/` exists with per-source raw + meta |
| Aggregations produced | `Aggregated/` exists with `Aggregated_Records.csv`, `Conflicts.csv`, `Duplicates.csv` |
| Traceability preserved | aggregated records include provenance + `SectionRef` best-effort |
| No source edits | agent does not modify any input file |

### Decision and Assumption Logging

- **Decision_Log.md**: records defaults, rule choices, schema inference, unit/currency handling, bootstrap actions.
  - IDs: `D-001`, `D-002`, ...
- **Assumptions_Log.md**: records any assumption required to proceed without data.
  - IDs: `A-001`, `A-002`, ...

### Data Integrity

- Never alter numeric values unless the brief explicitly requests transformation.
- If transformations occur (e.g., unit conversion), record:
  - method, factor, and before/after examples in `Decision_Log.md`.

### Invalid States

| Invalid State | Why |
|---|---|
| No snapshot written | no audit trail |
| Missing Source_Index.csv | cannot reproduce or audit |
| Aggregated records lack provenance | cannot trust aggregation |
| Overwriting prior snapshots | destroys history |
| Silent conflict resolution | hides reality; breaks trust |

[[END:SPEC]]

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Descriptive — "What is it?"

### Tool Root Hierarchy

The agent writes only to:

```
execution/_Aggregation/
  _Archive/
  _Templates/
    AGGREGATION_BRIEF_TEMPLATE.md
    TARGET_SCHEMA_TEMPLATE.csv
  _LATEST.md
  AGG_{PURPOSE}_{DATE}_{TIME}/
    Brief.md
    Plan.md
    RUN_SUMMARY.md
    Source_Index.csv
    Decision_Log.md
    Assumptions_Log.md
    QA_Report.md
    Extracts/
      {SourceID}_raw.*
      {SourceID}_meta.json
    Aggregated/
      Aggregated_Records.csv
      Conflicts.csv
      Duplicates.csv
      Summary.md           # optional
      Matrix.csv           # optional
      Register.csv         # optional
```

### Source_Index.csv schema (minimum)

- `SourceID`
- `Path`
- `Type`
- `ModifiedAt` (if available)
- `Fingerprint` (hash or best-effort signature)
- `Included` (TRUE/FALSE)
- `Reason` (why included/excluded)

### Aggregated_Records.csv schema (minimum fallback)

If no target schema is provided and inference is not stable, use:

- `RecordID`
- `SourceID`
- `SourcePath`
- `SectionRef`
- `EntityType` (e.g., `TableRow`, `KeyValue`, `DocSection`)
- `Key`
- `Value`
- `Notes`
- `Confidence` (`LOW|MED|HIGH`)
- `Tags` (comma-separated)

If a target schema is provided, prepend provenance fields:
- `SourceID`, `SourcePath`, `SectionRef`

### Conflicts.csv schema (minimum)

- `ConflictID`
- `Key` (or primary key)
- `Description`
- `ContenderCount`
- `SourceRefs` (list)
- `SuggestedRule` (non-binding)

### Duplicates.csv schema (minimum)

- `DuplicateGroupID`
- `RecordID`
- `SourceRef`
- `Reason`

[[END:STRUCTURE]]

[[BEGIN:RATIONALE]]
## RATIONALE

### Directional — "How to think?"

- Aggregation is a **truth-preserving activity**: prioritize provenance and auditability over neatness.
- The agent must be safe to rerun: snapshot outputs + non-destructive dedup/conflict handling support iterative refinement.
- Straight-through execution enables fast cycles: the human inspects outputs and reruns with a tighter brief or additional sources.
- When in doubt, **surface** ambiguity (conflicts, duplicates, missing schema) rather than masking it.

[[END:RATIONALE]]