# Source Index — EST_DEL-001-04_2026-02-27_0840

## Pricing Sources

| # | Source Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | Rate Table | 25 roles with hourly rates in CAD; all marked PARAMETRIC basis, MEDIUM confidence | Hourly rates for all 5 roles used in this estimate (R-01, R-08, R-11, R-12, R-13) |
| 2 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | Parametric (LOE model) | Multi-deliverable LOE table; rows filtered for DEL-001-04; 5 rows matched | Estimated hours for all 5 roles assigned to DEL-001-04 |
| 3 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | Parametric (parameters) | 18 project-level parameters; provides context (building area, ceiling height, currency, etc.) | Context only — no direct pricing used from this source |
| 4 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` | Parametric (fee percentages) | 5 discipline-level design fee percentage ranges | Not used for this deliverable — LOE-based pricing is more specific than fee-percentage method |

## Deliverable Documents (quantity takeoff sources)

| Document | Path | Used For |
|---|---|---|
| _CONTEXT.md | `PKG-001_Architectural Design/1_Working/DEL-001-04_Building-Sections/_CONTEXT.md` | Deliverable identification, package, discipline, type |
| Datasheet.md | `PKG-001_Architectural Design/1_Working/DEL-001-04_Building-Sections/Datasheet.md` | Building attributes, space types, crane infrastructure, conditions, construction elements |
| Specification.md | `PKG-001_Architectural Design/1_Working/DEL-001-04_Building-Sections/Specification.md` | Requirements (REQ-001 through REQ-012), verification criteria, documentation scope |
| Guidance.md | `PKG-001_Architectural Design/1_Working/DEL-001-04_Building-Sections/Guidance.md` | Design principles, trade-offs, considerations for section drawing production |
| Procedure.md | `PKG-001_Architectural Design/1_Working/DEL-001-04_Building-Sections/Procedure.md` | Work steps (Phase A preliminary, Phase B IFC), prerequisites, verification, records |

## Decomposition

| Document | Path | Used For |
|---|---|---|
| WDMLRL_Decomposition_Claude.md | `_Decomposition/WDMLRL_Decomposition_Claude.md` | WBS traceability — DEL-001-04 maps to PKG-001, SOW-0011, OBJ-001/OBJ-003 |
