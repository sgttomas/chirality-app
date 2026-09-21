# aggregation — method

## Method

### Function 0 — Bootstrap tool root (create-if-missing)

Bootstrap using: `tools/scaffolding/scaffold_tool_root.sh {EXECUTION_ROOT} _Aggregation`

Then ensure these additional subdirectories exist (create if missing, never overwrite user content):
- `{AGGREGATION_ROOT}/_Templates/`
- `{AGGREGATION_ROOT}/_Pipelines/`

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

For **Estimate Collation**, merge detail CSVs using: `python3 {INSTRUCTION_ROOT}/tools/reporting/merge_detail_csvs.py {snapshot}/Aggregated/Estimate/Project_Detail.csv <selected-detail-path-1> <selected-detail-path-2> ...` (auto-injects `SourcePath` provenance column). Supply exactly the accepted input-manifest paths. First verify identical ordered headers and valid row widths; normalize approved candidates or exclude incompatible files with explicit findings before invoking this concatenation helper. Then produce (even if empty):
- `Aggregated/Estimate/Project_Detail.csv` (produced by merge tool above)
- `Aggregated/Estimate/Project_Assumptions.csv`
- `Aggregated/Estimate/Project_Risks.csv`
- `Aggregated/Estimate/BasisOfEstimate_Index.csv`
- `Aggregated/Estimate/BasisOfEstimate_Collection.md`
- `Aggregated/Estimate/Project_Summary_CBS.csv`
- `Aggregated/Estimate/Project_Summary_WBS.csv`
- `Aggregated/Estimate/Project_WBS_CBS_Matrix.csv`
- `Aggregated/Estimate/Coverage.csv`

Update pointer files (overwrite allowed):
- `tools/scaffolding/update_latest_pointer.sh {AGGREGATION_ROOT} {snapshot_folder_name}`
- If `PIPELINE_ID` set: `tools/scaffolding/update_latest_pointer.sh {AGGREGATION_ROOT}/_Pipelines/{PIPELINE_ID} {snapshot_folder_name}`

---
