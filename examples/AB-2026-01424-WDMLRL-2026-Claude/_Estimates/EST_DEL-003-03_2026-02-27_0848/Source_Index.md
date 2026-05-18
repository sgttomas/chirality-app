# Source Index — EST_DEL-003-03_2026-02-27_0848

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-1 | `Professional_Staff_Rates.csv` | Rate Table | 25 roles with hourly rates in CAD; PARAMETRIC basis; MEDIUM confidence | Unit rates for all professional staff roles (R-01 through R-25) |
| PS-2 | `Level_of_Effort.csv` | Parametric | LOE by deliverable/role; PARAMETRIC basis; hours estimated per deliverable | Hour quantities for DEL-003-03: R-01 (6 hr), R-08 (4 hr), R-13 (36 hr), R-15 (84 hr) |
| PS-3 | `Assumed_Project_Parameters.csv` | Parametric | 19 project parameters (identity, location, facility, equipment, schedule) | Building context validation: 13,000 sqft, 35 ft ceiling, 2 cranes, CAD currency |
| PS-4 | `Professional_Design_Fees.csv` | Parametric | Fee percentages by discipline as % of construction value | Mechanical design fee: 1.0%–2.2% (recommended 1.6%) of construction value. Not used for this run — LOE-based pricing preferred for individual deliverables |

## Source Usability Assessment

- **PS-1 + PS-2**: Primary pricing pair. Together they provide both unit rates ($/hr) and quantities (hours) for all four roles assigned to DEL-003-03. Fully usable for PARAMETRIC pricing.
- **PS-3**: Context validation only. Confirms building parameters referenced in the deliverable documents. Not a direct pricing source.
- **PS-4**: Alternative parametric approach (fee-based). Not used for this run because LOE-based pricing (PS-1 + PS-2) provides more granular, role-level traceability for a single-deliverable scope. Could be used as a cross-check at package level.

## Document Sources (Quantity Takeoff)

| Document | Path | Used For |
|---|---|---|
| _CONTEXT.md | `PKG-003_Mechanical Design/1_Working/DEL-003-03_Ductwork-Plans/_CONTEXT.md` | Deliverable identity, package, discipline, type |
| Datasheet.md | `PKG-003_Mechanical Design/1_Working/DEL-003-03_Ductwork-Plans/Datasheet.md` | Systems coverage, key spaces, duct parameters, conditions |
| Specification.md | `PKG-003_Mechanical Design/1_Working/DEL-003-03_Ductwork-Plans/Specification.md` | Requirements (15 REQs), verification methods, documentation artifacts |
| Guidance.md | `PKG-003_Mechanical Design/1_Working/DEL-003-03_Ductwork-Plans/Guidance.md` | Design principles, space-by-space considerations, trade-offs, conflicts |
| Procedure.md | `PKG-003_Mechanical Design/1_Working/DEL-003-03_Ductwork-Plans/Procedure.md` | 10-step production procedure, prerequisites, verification checks, records |
| Decomposition | `_Decomposition/WDMLRL_Decomposition_Claude.md` | WBS traceability: PKG-003, DEL-003-03, SOW-0013, OBJ-001/003/004 |
