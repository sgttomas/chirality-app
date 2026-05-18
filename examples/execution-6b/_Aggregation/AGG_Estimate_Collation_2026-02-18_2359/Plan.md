# Plan — AGG_Estimate_Collation_2026-02-18_2359

## What Was Done

### 1. Bootstrap (Function 0)
- Created AGGREGATION_ROOT directory structure: `_Archive/`, `_Templates/`, `_Pipelines/Proposal_Production_Estimate/`, `_LATEST.md`

### 2. Locate Estimate Artifacts (Function 2)
- Located all 40 estimate snapshot directories under `_Estimates/`
- Confirmed each contains: Detail.csv, Run_Context.md, Assumptions_Log.md, QA_Report.md, Source_Index.md, Summary.md, WBS_CBS_Matrix.csv, Decision_Log.md, Scope_Resolved.csv, Blockers.md
- No Risk_Register files found in any snapshot (recorded in Coverage.csv)

### 3. Validate Format and Provenance (Function 3)
- Validated all 40 Detail.csv files against required schema (LineID, CBS, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence)
- All files also contain preferred columns: WBS_PackageID, WBS_DeliverableID, Notes
- Schema status: OK for all 40 files

### 4. Separate Dual-Nature Lines (Critical per BOE)
- **DEL-01-03**: Separated production lines (L-001 through L-003, Method=RATE_TABLE) from financial allowance lines (L-004 through L-007, Method=ALLOWANCE) -- bond/insurance premiums
- **DEL-01-04**: Separated production lines (A-010 through A-030, Method=RATE_TABLE with CBS=PRD.COMP) from construction pricing content lines (B-* and C-*, Method=RATE_TABLE/PARAMETRIC/ALLOWANCE with CBS=CON.*)
- **DEL-01-05**: Separated production lines (A-010 through A-030, Method=RATE_TABLE with CBS=PRD.COMP) from construction pricing content lines (B-* and C-*, Method=various with CBS=CON.*)

### 5. Collate into Project-Level Artifacts (Function 4)
- Created LineUID namespace: `{FromDeliverableID}::{LineID}`
- Created AssumptionUID namespace: `{FromDeliverableID}::{AssumptionID}`
- Produced consolidated Project_Detail.csv with all 215 line items
- Produced package-level and project-level rollups per BOE Section 7
- Produced effort matrix (hours by role x package)
- Produced evaluation-weight-adjusted view

### 6. Publish Outputs (Function 5)
- All outputs written to `AGG_Estimate_Collation_2026-02-18_2359/`
- Pipeline pointer updated: `_Pipelines/Proposal_Production_Estimate/_LATEST.md`
- Root pointer updated: `_LATEST.md`

## Key Decisions
- See Decision_Log.md for all decisions and tie-breaks
- DEL-01-04/05 construction lines with Method=RATE_TABLE are classified as construction pricing (not production) because their CBS codes begin with CON.* and their descriptions are construction scope items; the fact that RATE_TABLE was used as the estimation method does not change their cost nature
- DEL-01-03 bond/insurance premium lines (L-004 through L-007) classified as financial allowances, separate from production costs
