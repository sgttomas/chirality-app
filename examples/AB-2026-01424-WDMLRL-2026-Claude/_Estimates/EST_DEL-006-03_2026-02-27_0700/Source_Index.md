# Source Index — EST_DEL-006-03_2026-02-27_0700

## Price Sources

| # | Source File | Source Type | Parsing Notes | Supports | Limitations |
|---|---|---|---|---|---|
| 1 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | PARAMETRIC (rate table) | 25 roles with hourly rates in CAD; all rates marked PARAMETRIC basis, MEDIUM confidence | Hourly rates for all professional staff roles (R-01 through R-25) | Rates are parametric estimates, not confirmed quotes; MEDIUM confidence |
| 2 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | PARAMETRIC (level of effort) | Estimated hours by deliverable and role; DEL-006-03 has 4 role allocations (R-01, R-08, R-13, R-18) | Hour allocations per deliverable per role for all project deliverables | Hours are parametric estimates, not confirmed actuals; PARAMETRIC basis |
| 3 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC (parameters) | 18 project parameters covering identity, location, contract, schedule, facility, equipment, plumbing, currency | Context parameters: building area (~13,000 sqft), cistern 50,000L, septic 2,000 US gal, currency CAD | Parameters are mix of CONFIRMED and DERIVED; some MEDIUM confidence |
| 4 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` | PARAMETRIC (fee percentages) | 5 discipline fee ranges as percentage of construction value | Alternative fee-based pricing for design services | Not used for DEL-006-03 (LOE-based pricing preferred for individual deliverables; fee-based approach applies to package-level aggregation) |

## Deliverable Documents Read

| Document | Path | Used For |
|---|---|---|
| _CONTEXT.md | `PKG-006_Plumbing Design/1_Working/DEL-006-03_Drain-Vent-Plans/_CONTEXT.md` | Deliverable identity, scope, anticipated artifacts |
| Datasheet.md | `PKG-006_Plumbing Design/1_Working/DEL-006-03_Drain-Vent-Plans/Datasheet.md` | Drain/vent system elements, quantities, system parameters, conditions |
| Specification.md | `PKG-006_Plumbing Design/1_Working/DEL-006-03_Drain-Vent-Plans/Specification.md` | Requirements (REQ-006-03-001 to 033), code compliance, verification criteria |
| Guidance.md | `PKG-006_Plumbing Design/1_Working/DEL-006-03_Drain-Vent-Plans/Guidance.md` | Design principles, trade-offs, conflict table, considerations |
| Procedure.md | `PKG-006_Plumbing Design/1_Working/DEL-006-03_Drain-Vent-Plans/Procedure.md` | Work steps (Phase 1–4), prerequisites, verification, records |

## Decomposition Reference

| Document | Path | Used For |
|---|---|---|
| WDMLRL_Decomposition_Claude.md | `_Decomposition/WDMLRL_Decomposition_Claude.md` | WBS traceability — PKG-006 scope, DEL-006-03 entry, SOW-0016 reference |
