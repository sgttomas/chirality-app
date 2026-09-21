# preparation — contract

## Runtime parameters (provided by WORKING_ITEMS (workflow: project-setup); do not hard-code)

| Parameter | Meaning | Default / Notes |
|---|---|---|
| `EXECUTION_ROOT` | Execution workspace root | `execution/` (repo-relative) |
| `DECOMPOSITION_REF` | Path to decomposition doc(s) or folder | Provided by WORKING_ITEMS (workflow: project-setup) |
| `AGENTS_ROOT` | Where agent instruction files live (optional) | Provided by WORKING_ITEMS (workflow: project-setup) if needed |
| `SOURCES_ROOT` | Where shared source/reference files live (optional) | Provided by WORKING_ITEMS (workflow: project-setup) if available |
| `TASK_TYPE` | One of `A|B|C|D|E|F|G` (defined below) | Required |

> Notes:
> - Use repo-relative paths where possible.
> - If WORKING_ITEMS (workflow: project-setup) provides absolute paths, treat them as inputs (do not embed them into templates unless explicitly requested).

---

## Non-negotiable invariants

- **One task per invocation.** Each TASK instance receives one specific task and completes it.
- **No engineering content.** Do not write Datasheet/Specification/Guidance/Procedure content (PROJECT/SOFTWARE) or Knowledge Subject content (DOMAIN).
- **Production routing.** TASK scaffolds control files only. New
  PROJECT/SOFTWARE production initialization routes to `TASK + scope-of-work`
  with `MODE=INIT`; it never creates a legacy kit. DOMAIN/KTY schemas remain
  independently routed and unchanged.
- **Idempotent.** If a target file/folder already exists, do not modify it; skip and report.
- **Source-faithful.** `_CONTEXT.md` and any human-declared dependency stubs in `_DEPENDENCIES.md` must be extracted from:
  - the decomposition document, and/or
  - WORKING_ITEMS (workflow: project-setup)’s human-confirmed coordination declarations (if supplied).
  Do not invent, infer, or embellish.
- **Minimum viable fileset always.** Every deliverable or knowledge-type folder must contain:
  `_CONTEXT.md`, `_DEPENDENCIES.md`, `_STATUS.md`, `_REFERENCES.md`, `_SEMANTIC.md` (even if empty/placeholder).
- **Tool-folder setup is structural only.** When initializing project-level tool folders (e.g., `_Aggregation/`), create only folders and neutral templates; do not populate with project-specific data.

---

## Validity

### Validity

A TASK run is valid when:
- It completes exactly one assigned task type (A/B/C/D/E/F/G).
- It creates only missing files/folders (no overwrites).
- It uses deterministic scaffolding/status tools for filesystem and lifecycle operations.
- It does not create engineering content.
- `_CONTEXT.md` is exact to the decomposition for the deliverable (Task C) or knowledge type (Task F).
- Minimum viable fileset exists for any created deliverable or knowledge-type folder and passes `tools/validation/check_min_viable_fileset.sh`.

### Invalid states (examples)

| Invalid State | Why |
|---|---|
| Any required metadata file missing after Task C or F | Downstream agents cannot operate |
| `_CONTEXT.md` differs from decomposition | Breaks traceability |
| Dependencies invented | Misleads humans and tools |
| Existing files overwritten | Violates idempotency |

---

## Artifacts and schemas

This section defines the file schemas TASK writes.

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

> TASK creates `_DEPENDENCIES.md` as a **durable container**.
> - Humans/WORKING_ITEMS (workflow: project-setup) may add declared upstream/downstream items.
> - The **`dependency-extract` workflow** (dispatched via TASK) may later populate extracted-register summaries and run history.
> TASK itself must not infer edges.

```markdown
# Dependencies: [DEL-ID] [Deliverable Name]

## Coordination (human-owned)
- **Mode:** [NOT_TRACKED | DECLARED | FULL_GRAPH]
- **Notes:** [pointer to coordination record or external system, or "TBD"]

## Upstream (I need these before I can proceed) — human-owned declarations
- (If Mode = NOT_TRACKED: write “Dependencies coordinated externally by humans.”)
- [DEL-ID] [Name] — Reason: [from WORKING_ITEMS (workflow: project-setup) declarations]
  - Required maturity: [OPEN | INITIALIZED | SEMANTIC_READY | IN_PROGRESS | CHECKING | ISSUED]
  - Location: [path if known, else TBD]

## Downstream (These need me) — human-owned declarations
- (If Mode = NOT_TRACKED: write “Dependencies coordinated externally by humans.”)
- [DEL-ID] [Name] — Reason: [from WORKING_ITEMS (workflow: project-setup) declarations]
  - Required maturity: [state they need from me]
  - Location: [path if known, else TBD]

## Extracted Dependency Register (populated by TASK+dependency-extract)
- **Status:** NOT_RUN_YET
- **Dependencies.csv:** TBD
- **Summary:** TBD

## Run Notes & History (populated by TASK+dependency-extract)
- (placeholder)

## Lifecycle Summary (populated by TASK+dependency-extract)
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
- [YYYY-MM-DD] — State set to OPEN (TASK)
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
### `_MEMORY.md` Template Schema

`_MEMORY.md` is the deliverable’s working memory. When CREATE_MEMORY=true is selected and its path authorized, TASK creates a missing file as a structured empty template for later use by WORKING_ITEMS and deliverable-local task sub-agents. It is intentionally **non-normative** and may grow over time.

Default CREATE_MEMORY=false; memory is optional and outside the five-file minimum. Preserve any existing memory. Create with this minimum schema (adapted from `docs/templates/MEMORY_TEMPLATE.md`):

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

TASK creates `_SEMANTIC.md` as a **structural placeholder** only. It is intended to be overwritten later by the semantic-matrix pipeline.

```markdown
# Semantic Lens: [DEL-ID] [Deliverable Name]

**Status:** PLACEHOLDER
**Generated:** TBD

## Notes
- This file is intentionally minimal at TASK time.
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

---
