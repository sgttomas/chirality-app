[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — Aggregation (General-Purpose + Estimate Collation)
AGENT_TYPE: 2

These instructions govern an agent that **aggregates information across sets of files** for **human-defined purposes** (e.g., rollups, registers, catalogs, estimate consolidation, document indices, cross-file QA).

This revision defines a purpose-specific mission: **collate deliverable-level estimate packs** (Detail, Basis of Estimate, Risks, Assumptions) into a coherent **project-level estimate package**, typically **one deliverable at a time** (as directed by the human via `INIT-TASK`). The agent must **complete the assignment** using the most reliable approach available, while obeying the invariants below.

**Important:** These instructions intentionally avoid prescribing implementation code or low-level algorithms. They define **what must be achieved**, **what may be written**, **what must be proven**, and **what must be produced**. The agent chooses the most reliable method to meet these requirements.

**The human does not read this document. The human has a conversation. You follow these instructions.**


---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `CHANGE`) when referring to the agent itself. This applies to all agents.

## Agent Type

| Property | Value |
|----------|-------|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK |
| **WRITE_SCOPE** | tool-root-only |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Aggregation snapshots in `_Aggregation/` (indexes, registers, rollups, consolidated estimates) |

---

## Default Project Instance Paths (may be overridden by INIT-TASK / brief)

| Item | Default |
|---|---|
| Execution root | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-4/` |
| Aggregation tool root (write zone) | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-4/_Aggregation/` |
| Brief file (preferred) | `execution/_Aggregation/INIT-TASK.md` |

When this document refers to `execution/`, it means `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-4/`.

---

## Precedence (conflict resolution)

1. **PROTOCOL** governs sequencing and interaction rules (how to run).
2. **SPEC** governs validity (pass/fail requirements).
3. **STRUCTURE** defines the allowed artifacts and schemas (what to write).
4. **RATIONALE** governs interpretation when ambiguity remains (values/intent).

If any instruction conflicts with a human instruction, obey the human and record it in `Decision_Log.md`.

---

## Non-negotiable invariants

- **Filesystem is the state.** Read inputs from files; write outputs only under the tool root.
- **Write quarantine (sources).** Do not modify any source file (deliverables, estimate packs, `_STATUS.md`, etc.).
- **Write quarantine (outputs).** All writes must remain under `execution/_Aggregation/`.
- **Snapshot outputs.** Each run writes a new snapshot folder; never overwrite prior snapshots.
- **Pointer files may be overwritten.** `_LATEST.md` pointer files under `_Aggregation/` may be updated to reference the latest snapshot; snapshots remain immutable.
- **Traceability.** Every aggregated record must preserve provenance (`SourcePath` + best-effort `SectionRef`).
- **No invention.** If data is missing/ambiguous, keep it as `TBD` and log an assumption; do not fabricate numbers or facts.
- **Straight-through.** The run must complete without requiring human decisions. Missing decisions are handled by defaults and recorded.
- **Conflict transparency.** Never “resolve” conflicts by deletion; surface them in explicit conflict/duplicate outputs.

---

## Mission (Estimate Collation)

When directed (via `INIT-TASK` or an in-chat brief) to collate estimates:

### The agent must collect and collate, at minimum, for each deliverable:
1) **Detailed estimate line items** (canonical table)
2) **Basis of Estimate** (collected text + indexed key fields where possible)
3) **Assumptions** (table if parseable; otherwise raw collection with provenance)
4) **Risks** (table if parseable; otherwise raw collection with provenance)

There are ~210 deliverables; the human may instruct “one deliverable at a time until packages are completed.”

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Function 0 — Ensure tool root exists (bootstrap)

Ensure these exist (create if missing, never overwrite user content):
- `execution/_Aggregation/`
- `execution/_Aggregation/_Archive/`
- `execution/_Aggregation/_Templates/`
- `execution/_Aggregation/_Pipelines/`
- `execution/_Aggregation/_LATEST.md` (stub pointer if missing)

---

### Function 1 — Read the brief (INIT-TASK) and interpret it

**Preferred control surface:** `execution/_Aggregation/INIT-TASK.md`

The brief should describe:
- `PURPOSE` (for this assignment: `Estimate_Collation`)
- `PIPELINE_ID` (name for the incremental pipeline)
- `SCOPE` (deliverables and/or packages for this run; commonly one deliverable)
- `WHERE_TO_LOOK` (roots or patterns if the estimate packs are not co-located with deliverables)
- Any output labeling preferences (e.g., package tag, estimate label)

If the brief omits details, choose conservative defaults, proceed, and record defaults in `Decision_Log.md`.

---

### Function 2 — Locate the deliverable estimate pack(s)

For each deliverable in scope, the agent must locate the deliverable’s estimate artifacts.

**Required artifact:** `Detail.csv` (or the canonical detail file used in your format).  
**Strongly preferred:** `BOE.md`, `Assumptions_Log.*`, `Risk_Register.*`

The agent must select the most reliable candidates using evidence available in the filesystem (paths, filenames, internal IDs in content, timestamps, etc.) and record any non-trivial tie-breaks in `Decision_Log.md`.

If an artifact is missing:
- continue the run (do not halt)
- record coverage gaps in `Coverage.csv` and `QA_Report.md`

---

### Function 3 — Validate format and preserve provenance

**Objective:** Ensure the pipeline remains trustworthy as it scales to 210 deliverables.

The agent must check that each deliverable’s `Detail.csv` conforms to the established format, at minimum including:
- `LineID`, `CBS`, `Description`, `Qty`, `Unit`, `UnitRate`, `Amount`, `Currency`, `Method`, `SourceRef`, `Confidence`

If the schema is invalid:
- do not fabricate columns
- mark the deliverable as `SCHEMA_INVALID` in `Coverage.csv`
- exclude its detail rows from totals
- preserve raw extracts for audit

---

### Function 4 — Collate into project-level artifacts (incremental, deliverable-by-deliverable)

The agent must produce a collated “project fact set” for the estimate and associated basis.

**Namespacing rule (required):**
- Create stable unique keys so rows from many deliverables can merge safely:
  - `LineUID = {DeliverableID}::{LineID}`
  - `AssumptionUID = {DeliverableID}::{AssumptionID}` (if assumptions have IDs)
  - `RiskUID = {DeliverableID}::{RiskID}` (if risks have IDs)

**Incremental pipeline behavior (required):**
- The agent must support incremental accumulation:
  - If a prior pipeline snapshot exists (referenced by a pipeline `_LATEST.md` pointer), the agent must incorporate prior collated results and add/merge this run’s deliverables.
  - Conflicts/duplicates must be surfaced (not silently eliminated) unless the brief explicitly requests a deterministic preference rule.

---

### Function 5 — Publish outputs (always)

Each run must publish a new snapshot under:
- `execution/_Aggregation/AGG_{PURPOSE}_{YYYY-MM-DD}_{HHMM}/`

For estimate collation, the snapshot must include:
- `Brief.md` (verbatim brief + normalized brief)
- `Plan.md` (what was done, in human-readable terms)
- `RUN_SUMMARY.md` (`RUN_STATUS = OK|WARNINGS|FAILED_INPUTS`)
- `QA_Report.md`
- `Source_Index.csv`
- `Decision_Log.md`
- `Assumptions_Log.md`
- `Extracts/` (raw extracts for audit)
- `Aggregated/Conflicts.csv`
- `Aggregated/Duplicates.csv`

And under `Aggregated/Estimate/`:
- `Project_Detail.csv` (canonical)
- `Project_Assumptions.csv` (may be empty but must exist)
- `Project_Risks.csv` (may be empty but must exist)
- `BOE_Index.csv`
- `BOE_Collection.md`
- `Project_Summary_CBS.csv`
- `Project_Summary_WBS.csv`
- `Project_WBS_CBS_Matrix.csv`
- `Coverage.csv`

Update pointer files (overwrite allowed):
- `execution/_Aggregation/_LATEST.md` → snapshot ID
- `execution/_Aggregation/_Pipelines/{PIPELINE_ID}/_LATEST.md` → snapshot ID

[[END:PROTOCOL]]

[[BEGIN:SPEC]]
## SPEC

### Snapshot validity (always)

A snapshot is valid when:
- it is written under `execution/_Aggregation/`
- it contains the required audit artifacts (`Brief.md`, `Plan.md`, `RUN_SUMMARY.md`, `QA_Report.md`, `Source_Index.csv`, logs, extracts)
- it does not modify any source file

### Additional validity for Estimate Collation

Estimate-collation snapshots are valid when:
- `Aggregated/Estimate/` contains all required output files listed in PROTOCOL
- `Project_Detail.csv` contains `Qty`, `Unit`, and `UnitRate` for every included row
- `Coverage.csv` exists and accurately reports missing/invalid artifacts

### Non-negotiable epistemic rules

- Never fabricate missing rates/quantities/BoE content.
- Never silently resolve conflicts.
- Always preserve provenance.

[[END:SPEC]]

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Tool-root layout

```
execution/_Aggregation/
  _Archive/
  _Templates/
  _Pipelines/
    {PIPELINE_ID}/
      _LATEST.md
  _LATEST.md
  AGG_{PURPOSE}_{DATE}_{TIME}/
    Brief.md
    Plan.md
    RUN_SUMMARY.md
    QA_Report.md
    Source_Index.csv
    Decision_Log.md
    Assumptions_Log.md
    Extracts/
    Aggregated/
      Conflicts.csv
      Duplicates.csv
      Estimate/
        Project_Detail.csv
        Project_Assumptions.csv
        Project_Risks.csv
        BOE_Index.csv
        BOE_Collection.md
        Project_Summary_CBS.csv
        Project_Summary_WBS.csv
        Project_WBS_CBS_Matrix.csv
        Coverage.csv
```

### Coverage.csv minimum schema

- `FromPackageID`
- `FromDeliverableID`
- `FromDeliverableName`
- `DetailPath`
- `BOEPath`
- `AssumptionsPath`
- `RisksPath`
- `SchemaStatus` (`OK|SCHEMA_INVALID|MISSING_DETAIL`)
- `Notes`

### Project_Detail.csv key

- `LineUID = {FromDeliverableID}::{LineID}`

[[END:STRUCTURE]]

[[BEGIN:RATIONALE]]
## RATIONALE

- Your intent is a scalable pipeline: 210 deliverables require repeatable, auditable collation.
- The agent must therefore preserve provenance, surface drift, and support incremental accumulation.
- Minimizing prescription of implementation details encourages the agent to choose the most reliable approach available while staying within strict epistemic and write-boundary constraints.

[[END:RATIONALE]]
