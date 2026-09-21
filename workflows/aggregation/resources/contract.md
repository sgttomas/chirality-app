# aggregation — contract

## Runtime variables and defaults

Before combining currencies, require an explicit reporting currency and accepted exchange-rate basis; otherwise report separate currency totals. Include accepted and excluded source manifests with exact row coverage.

This file is **project-generic**. Do not embed project-specific absolute paths in this workflow resource. Resolve instance paths from the brief.

Defaults (only when the brief does not override):
- `EXECUTION_ROOT = execution/` (relative to repo/project root)
- `AGGREGATION_ROOT = {EXECUTION_ROOT}/_Aggregation/`
- `INIT_TASK_PATH = {AGGREGATION_ROOT}/INIT-TASK.md`

When this document refers to `execution/`, it means `{EXECUTION_ROOT}`.

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

When directed (via `INIT-TASK` or an in-chat brief) to collate estimates, TASK must collect and collate, at minimum, for each deliverable in scope:

1) **Detailed estimate line items** (canonical table, typically `Detail.csv`)
2) **Basis of estimate (basis selection + evidence)**
   - Prefer `Run_Context.md` (or equivalent) that records `BASIS_OF_ESTIMATE` (a validated enum) and any supporting notes/refs.
   - If a legacy narrative `BOE.*` exists, collate it as evidence text (but do not require it).
3) **Assumptions** (table if parseable; otherwise raw collection with provenance)
4) **Risks** (table if parseable; otherwise raw collection with provenance)

Optional (if present, collate as supporting audit context):
- `QA_Report.*`, `Source_Index.*`, `Decision_Log.*`, `Change_Log.*`, `WBS_CBS_Matrix.*`, summaries.

---

## Validity

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

---

## Artifacts and schemas

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

---
