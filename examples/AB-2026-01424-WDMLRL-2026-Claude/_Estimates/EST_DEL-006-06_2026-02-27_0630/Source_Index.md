# Source Index — EST_DEL-006-06_2026-02-27_0630

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-1 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | PARAMETRIC (rate table) | 25 rows; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. All rates in CAD. Confidence: MEDIUM. | Hourly rates for all professional roles. Used for DL-001 through DL-004. |
| PS-2 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | PARAMETRIC (level of effort) | Multi-row CSV; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. 4 rows matched for DEL-006-06 (R-01: 6 hr, R-08: 4 hr, R-13: 21 hr, R-18: 49 hr). | Estimated hours per role per deliverable. Used for DL-001 through DL-004. |
| PS-3 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC (parameters) | 19 rows; project-level attributes (building area, cistern volume, equipment, schedule, currency). | Context and validation only; not directly used for line pricing. Key parameter used: PP-17 Currency = CAD. |
| PS-4 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` | PARAMETRIC (fee percentage) | 5 rows; percentage-based design fees by discipline. No plumbing-specific row. | Not directly used for this deliverable. LOE-based pricing is preferred over fee-percentage for individual schedule deliverables. No plumbing-specific design fee row exists (closest would be Mechanical DF-03 at 1.6% but this is not applicable to a fixture schedule). |

## Deliverable Documents Read

| Document | Path | Status |
|---|---|---|
| _CONTEXT.md | `PKG-006_Plumbing Design/1_Working/DEL-006-06_Fixture-Schedule/_CONTEXT.md` | Read successfully |
| Datasheet.md | `PKG-006_Plumbing Design/1_Working/DEL-006-06_Fixture-Schedule/Datasheet.md` | Read successfully |
| Specification.md | `PKG-006_Plumbing Design/1_Working/DEL-006-06_Fixture-Schedule/Specification.md` | Read successfully |
| Guidance.md | `PKG-006_Plumbing Design/1_Working/DEL-006-06_Fixture-Schedule/Guidance.md` | Read successfully |
| Procedure.md | `PKG-006_Plumbing Design/1_Working/DEL-006-06_Fixture-Schedule/Procedure.md` | Read successfully |

## Decomposition Reference

| Document | Path | Status |
|---|---|---|
| WDMLRL_Decomposition_Claude.md | `_Decomposition/WDMLRL_Decomposition_Claude.md` | Read successfully; DEL-006-06 found in PKG-006 table at line 440 |
