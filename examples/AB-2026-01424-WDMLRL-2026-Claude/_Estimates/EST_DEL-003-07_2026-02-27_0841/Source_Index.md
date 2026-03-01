# Source Index — EST_DEL-003-07_2026-02-27_0841

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | RATE_TABLE | 25 roles; CSV with RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Hourly rates for all professional staff roles; used to price ITEM-001 through ITEM-004 |
| PS-02 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | PARAMETRIC | ~200+ rows; CSV with Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes | Hours per role per deliverable; DEL-003-07 has 4 rows (R-01: 6h, R-08: 4h, R-13: 18h, R-15: 42h) |
| PS-03 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC | 19 rows; project identity, location, schedule, facility, equipment, and economic parameters | Context parameters (building area, currency, base year); not directly used for line-item pricing |
| PS-04 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` | PARAMETRIC | 5 rows; fee % ranges by discipline as % of construction value | Cross-check benchmark for mechanical design fees (DF-03: 1.0%–2.2%, recommended 1.6%); not used as primary pricing method for this run |

## Document Sources (quantity takeoff inputs)

| # | Document | Path | Notes |
|---|---|---|---|
| DS-01 | _CONTEXT.md | `PKG-003_Mechanical Design/1_Working/DEL-003-07_Specification/_CONTEXT.md` | Deliverable identification and metadata |
| DS-02 | Datasheet.md | `PKG-003_Mechanical Design/1_Working/DEL-003-07_Specification/Datasheet.md` | Building context, mechanical systems inventory, parameters, conditions |
| DS-03 | Specification.md | `PKG-003_Mechanical Design/1_Working/DEL-003-07_Specification/Specification.md` | 15 requirements (REQ-M-001 through REQ-M-015), standards, verification |
| DS-04 | Guidance.md | `PKG-003_Mechanical Design/1_Working/DEL-003-07_Specification/Guidance.md` | Design principles, considerations, trade-offs, conflicts |
| DS-05 | Procedure.md | `PKG-003_Mechanical Design/1_Working/DEL-003-07_Specification/Procedure.md` | 9-step production procedure, prerequisites, verification, records |

## Decomposition Source

| # | Document | Path | Notes |
|---|---|---|---|
| DC-01 | WDMLRL_Decomposition_Claude.md | `_Decomposition/WDMLRL_Decomposition_Claude.md` | PKG-003 definition, DEL-003-07 entry, SOW-0013, OBJ-003/OBJ-004 traceability |
