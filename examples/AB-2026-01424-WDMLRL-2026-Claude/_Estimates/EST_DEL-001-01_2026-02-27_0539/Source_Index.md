# Source Index — EST_DEL-001-01_2026-02-27_0539

## Price Sources

| # | Source File | Absolute Path | Source Type | Parsing Notes | What It Supports | What It Cannot Support |
|---|---|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | Rate Table | CSV; 25 roles; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Hourly rates (CAD) for all professional staff roles used in the estimate (R-01, R-08, R-11, R-12, R-13) | Does not provide hours/quantity; does not cover material or equipment costs |
| 2 | Level_of_Effort.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | Parametric Model | CSV; rows by Execution+DeliverableID+RoleID; columns: EstimatedHours, Basis, Notes | Hours per role per deliverable; DEL-001-01 has 5 rows (R-01: 6h, R-08: 4h, R-11: 27h, R-12: 21h, R-13: 12h) | Does not provide rates; parametric basis only (not activity-level build-up) |
| 3 | Assumed_Project_Parameters.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | Reference Parameters | CSV; 19 parameters covering identity, location, contract, schedule, facility attributes | Project context: 13,000 sqft, 35 ft ceiling, 2x5T cranes, CAD currency | Not a pricing source; provides context and cross-check parameters only |
| 4 | Professional_Design_Fees.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` | Parametric Model | CSV; 5 discipline fee percentage ranges as % of construction value | Cross-check of total architectural design fee (DF-01: 3.0%-6.0%, recommended 4.5%) | Not used for primary pricing; used for reasonableness cross-check only |
| 5 | Parametric_Building_Rates.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Parametric_Building_Rates.csv` | Parametric Model | CSV; 2 items: base industrial building rate and wash bay premium | Cross-check of estimated construction value (PB-01: $220-360/sf, recommended $285/sf) | Not used for primary pricing; used for reasonableness cross-check only |

## Document Sources (Deliverable Content)

| Document | Path | Role in Estimate |
|---|---|---|
| _CONTEXT.md | `PKG-001_Architectural Design/1_Working/DEL-001-01_Preliminary-Design/_CONTEXT.md` | Deliverable identification: ID, name, package, discipline, type |
| Datasheet.md | `PKG-001_Architectural Design/1_Working/DEL-001-01_Preliminary-Design/Datasheet.md` | Building program attributes and quantities; conditions; construction details |
| Specification.md | `PKG-001_Architectural Design/1_Working/DEL-001-01_Preliminary-Design/Specification.md` | Requirements and verification criteria; scope definition |
| Guidance.md | `PKG-001_Architectural Design/1_Working/DEL-001-01_Preliminary-Design/Guidance.md` | Design principles, trade-offs, considerations, assumptions |
| Procedure.md | `PKG-001_Architectural Design/1_Working/DEL-001-01_Preliminary-Design/Procedure.md` | Work steps (8 steps), prerequisites, verification activities |

## Decomposition Source

| Document | Path | Role in Estimate |
|---|---|---|
| WDMLRL_Decomposition_Claude.md | `_Decomposition/WDMLRL_Decomposition_Claude.md` | WBS traceability: PKG-001, DEL-001-01, SOW-0010a; OBJ-001 and OBJ-003 |
