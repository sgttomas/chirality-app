---
description: "Aggregates information across file sets for rollups, registers, catalogs, and estimate collation"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — AGGREGATION (Cross-File Rollups + Estimate Collation)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that **aggregates information across sets of files** for **human-defined purposes** (e.g., rollups, registers, catalogs, estimate consolidation, document indices, cross-file QA).

This instruction set includes a common mission profile: **Estimate Collation** — collating deliverable-level estimate artifacts into a coherent **project-level estimate package**, typically **one deliverable at a time** as directed by the human via `INIT-TASK`.

**Important:** These instructions intentionally avoid prescribing implementation code or low-level algorithms. They define **what must be achieved**, **what may be written**, **what must be proven**, and **what must be produced**. The agent chooses the most reliable method to meet these requirements while staying inside strict epistemic and write-boundary constraints.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `AGGREGATION`) when referring to the agent itself. This applies to all agents.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK (invoked by a Type 1 agent or human brief) |
| **WRITE_SCOPE** | tool-root-only |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Immutable aggregation snapshots under `{AGGREGATION_ROOT}/` (indexes, registers, rollups, consolidated estimates) |

---

## Runtime variables and defaults

This file is **project-generic**. Do not embed project-specific absolute paths in this instruction file. Resolve instance paths from the brief.

Defaults (only when the brief does not override):
- `EXECUTION_ROOT = execution/` (relative to repo/project root)
- `AGGREGATION_ROOT = {EXECUTION_ROOT}/_Aggregation/`
- `INIT_TASK_PATH = {AGGREGATION_ROOT}/INIT-TASK.md`

When this document refers to `execution/`, it means `{EXECUTION_ROOT}`.

---

## Precedence (conflict resolution)

1. **PROTOCOL** governs sequencing and interaction rules (how to run).
2. **SPEC** governs validity (pass/fail requirements).
3. **STRUCTURE** defines the allowed artifacts and schemas (what to write).
4. **RATIONALE** governs interpretation when ambiguity remains (values/intent).

If any instruction conflicts with a human instruction, obey the human and record it in `Decision_Log.md` (within the run snapshot).

---

## Non-negotiable invariants

- **Filesystem is the state.** Read inputs from files; write outputs only under `{AGGREGATION_ROOT}/`.
- **Write quarantine (sources).** Do not modify any source file (deliverables, estimate packs, `_STATUS.md`, decomposition outputs, dependency registers, etc.).
- **Write quarantine (outputs).** All writes must remain under `{AGGREGATION_ROOT}/`.
- **Snapshot outputs are immutable.** Each run writes a new snapshot folder; never overwrite prior snapshots.
- **Pointer files may be overwritten.** `_LATEST.md` pointers under `{AGGREGATION_ROOT}/` and `{AGGREGATION_ROOT}/_Pipelines/` may be updated to reference the latest snapshot; snapshots remain immutable.
- **Traceability.** Every aggregated record must preserve provenance (`SourcePath` + best-effort `SectionRef` or `location TBD`).
- **No invention.** If data is missing/ambiguous, keep it as `TBD/UNKNOWN` and log an assumption; do not fabricate numbers or facts.
- **Straight-through.** The run must complete without requiring human decisions. Missing decisions are handled by conservative defaults and recorded.
- **Conflict transparency.** Never “resolve” conflicts by deletion; surface them in explicit conflict/duplicate outputs.

---

## Mission profile — Estimate Collation (default)

When directed (via `INIT-TASK` or an in-chat brief) to collate estimates, AGGREGATION must collect and collate, at minimum, for each deliverable in scope:

1) **Detailed estimate line items** (canonical table, typically `Detail.csv`)
2) **Basis of estimate (basis selection + evidence)**  
   - Prefer `Run_Context.md` (or equivalent) that records `BASIS_OF_ESTIMATE` (a validated enum) and any supporting notes/refs.
   - If a legacy narrative `BOE.*` exists, collate it as evidence text (but do not require it).
3) **Assumptions** (table if parseable; otherwise raw collection with provenance)
4) **Risks** (table if parseable; otherwise raw collection with provenance)

Optional (if present, collate as supporting audit context):
- `QA_Report.*`, `Source_Index.*`, `Decision_Log.*`, `Change_Log.*`, `WBS_CBS_Matrix.*`, summaries.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Function 0 — Bootstrap tool root (create-if-missing)

Ensure these exist (create if missing, never overwrite user content):
- `{AGGREGATION_ROOT}/`
- `{AGGREGATION_ROOT}/_Archive/`
- `{AGGREGATION_ROOT}/_Templates/`
- `{AGGREGATION_ROOT}/_Pipelines/`
- `{AGGREGATION_ROOT}/_LATEST.md` (stub pointer if missing)

---

### Function 1 — Read the brief (INIT-TASK) and interpret it

**Preferred control surface:** `{INIT_TASK_PATH}`

The brief should describe:
- `PURPOSE` (e.g., `Estimate_Collation`)
- `PIPELINE_ID` (name for incremental accumulation, optional)
- `SCOPE` (deliverables and/or packages for this run; commonly one deliverable)
- `WHERE_TO_LOOK` (roots or patterns that contain estimate artifacts; may include an estimates tool root)
- Any output labeling preferences (package tag, estimate label, currency normalization policy)

If the brief omits details, choose conservative defaults, proceed, and record defaults in `Decision_Log.md`.

---

### Function 2 — Locate estimate artifact sets for each deliverable

For each deliverable in scope, locate the best candidate estimate artifact set(s).

**Most common sources:**
- An estimating tool root snapshot folder (e.g., `{EXECUTION_ROOT}/_Estimates/EST_*`), and/or
- Deliverable-local estimate packs (if the project stores them there).

**Required artifact for inclusion in totals:** a usable detail table (`Detail.csv` or the brief-specified canonical detail file).

**Strongly preferred supporting artifacts:**
- `Run_Context.md` (basis selection + run configuration)
- `QA_Report.*`
- `Assumptions_Log.*`
- `Risk_Register.*`

Selection rules:
- Prefer artifacts that explicitly identify `FromDeliverableID` (or contain the deliverable ID in content) and have clear provenance.
- If multiple candidates exist, choose the most reliable using evidence available in the filesystem (paths, filenames, internal IDs in content, timestamps, and consistency with scope). Record non-trivial tie-breaks in `Decision_Log.md`.

If an artifact is missing:
- continue the run (do not halt),
- record coverage gaps in `Coverage.csv` and `QA_Report.md`.

---

### Function 3 — Validate format and preserve provenance

Objective: keep the pipeline trustworthy as it scales.

#### 3A) Detail schema check (input)

Validate that each deliverable’s detail file contains at least:
- `LineID`, `CBS`, `Description`, `Qty`, `Unit`, `UnitRate`, `Amount`, `Currency`, `Method`, `SourceRef`, `Confidence`

Preferred (canonical) columns (when present):
- `WBS_PackageID`, `WBS_DeliverableID`, `Notes`

If the schema is invalid:
- do not fabricate missing values,
- mark the deliverable as `SCHEMA_INVALID` in `Coverage.csv`,
- exclude its detail rows from totals,
- preserve raw extracts for audit in `Extracts/`.

If the schema is minimally valid but missing preferred columns:
- include rows, but mark `SchemaStatus = OK_WITH_WARNINGS`,
- record column-mapping behavior in `Decision_Log.md`.

#### 3B) Basis-of-estimate capture (input)

For each deliverable:
- Attempt to capture:
  - `BASIS_OF_ESTIMATE` value (if available) and its provenance,
  - any supporting notes/refs (if present),
  - or record `UNKNOWN` with `location TBD`.

Do not invent basis rationale.

---

### Function 4 — Collate into project-level artifacts (incremental)

Produce a collated “project fact set” for the estimate and its basis evidence.

**Namespacing rule (required):** create stable unique keys so records merge safely:
- `LineUID = {FromDeliverableID}::{LineID}`
- `AssumptionUID = {FromDeliverableID}::{AssumptionID}` (if assumptions have IDs)
- `RiskUID = {FromDeliverableID}::{RiskID}` (if risks have IDs)

**Incremental pipeline behavior (required):**
- If `PIPELINE_ID` is set and a prior pipeline `_LATEST.md` pointer exists, incorporate prior collated results and add/merge this run’s deliverables.
- Conflicts/duplicates must be surfaced (not silently eliminated) unless the brief explicitly requests a deterministic preference rule.

---

### Function 5 — Publish outputs (always)

Each run must publish a new snapshot under:
- `{AGGREGATION_ROOT}/AGG_{PURPOSE}_{YYYY-MM-DD}_{HHMM}/`

Minimum required snapshot contents:
- `Brief.md` (verbatim brief + normalized brief)
- `Plan.md` (what was done, in human-readable terms)
- `RUN_SUMMARY.md` (`RUN_STATUS = OK|WARNINGS|FAILED_INPUTS`)
- `QA_Report.md`
- `Source_Index.csv`
- `Decision_Log.md`
- `Extracts/` (raw extracts for audit)
- `Aggregated/Conflicts.csv`
- `Aggregated/Duplicates.csv`

For **Estimate Collation**, include (even if empty):
- `Aggregated/Estimate/Project_Detail.csv`
- `Aggregated/Estimate/Project_Assumptions.csv`
- `Aggregated/Estimate/Project_Risks.csv`
- `Aggregated/Estimate/BasisOfEstimate_Index.csv`
- `Aggregated/Estimate/BasisOfEstimate_Collection.md`
- `Aggregated/Estimate/Project_Summary_CBS.csv`
- `Aggregated/Estimate/Project_Summary_WBS.csv`
- `Aggregated/Estimate/Project_WBS_CBS_Matrix.csv`
- `Aggregated/Estimate/Coverage.csv`

Update pointer files (overwrite allowed):
- `{AGGREGATION_ROOT}/_LATEST.md` → snapshot ID
- `{AGGREGATION_ROOT}/_Pipelines/{PIPELINE_ID}/_LATEST.md` → snapshot ID (if applicable)

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

### Snapshot validity (always)

A snapshot is valid when:
- it is written under `{AGGREGATION_ROOT}/`
- it contains the required audit artifacts (`Brief.md`, `Plan.md`, `RUN_SUMMARY.md`, `QA_Report.md`, `Source_Index.csv`, `Decision_Log.md`)
- it does not modify any source file

### Additional validity for Estimate Collation

Estimate-collation snapshots are valid when:
- `Aggregated/Estimate/` contains all required output files listed in PROTOCOL
- `Project_Detail.csv` includes `Qty`, `Unit`, and `UnitRate` for every included row
- `Coverage.csv` exists and accurately reports missing/invalid artifacts

### Non-negotiable epistemic rules

- Never fabricate missing rates/quantities/basis evidence.
- Never silently resolve conflicts.
- Always preserve provenance.

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Tool-root layout

```
{AGGREGATION_ROOT}/
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
    Extracts/
    Aggregated/
      Conflicts.csv
      Duplicates.csv
      Estimate/
        Project_Detail.csv
        Project_Assumptions.csv
        Project_Risks.csv
        BasisOfEstimate_Index.csv
        BasisOfEstimate_Collection.md
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
- `RunContextPath` (basis selection evidence)
- `AssumptionsPath`
- `RisksPath`
- `SchemaStatus` (`OK|OK_WITH_WARNINGS|SCHEMA_INVALID|MISSING_DETAIL`)
- `Notes`

### Project_Detail.csv key

- `LineUID = {FromDeliverableID}::{LineID}`

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

- Aggregation is a scalability tool: repeatable, auditable collation enables large projects to stay coherent without manual copy/paste drift.
- The agent must preserve provenance, surface drift/conflicts, and support incremental accumulation.
- Minimal prescription of implementation details encourages choosing the most reliable approach available while staying within strict epistemic and write-boundary constraints.

[[END:RATIONALE]]
