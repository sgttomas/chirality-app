# Source Index — EST_DEL-006-08_2026-02-27_0730

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports | Limitations |
|---|------------|-------------|---------------|----------|-------------|
| PS-1 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | Rate table | CSV; 25 roles; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Hourly rates for all professional staff roles (R-01 through R-25) | Rates are PARAMETRIC basis with MEDIUM confidence; no overtime/premium rates included |
| PS-2 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | Parametric LOE | CSV; rows by Execution/DeliverableID/Role; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes | Estimated hours by role for each deliverable; DEL-006-08 has 4 rows (R-01: 6h, R-08: 4h, R-13: 21h, R-18: 49h) | Hours are PARAMETRIC basis; no breakdown by activity/phase within each deliverable |
| PS-3 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | Parametric parameters | CSV; 19 parameters; columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes | Project-level parameters: building area (13,000 sqft), ceiling height (35 ft), cistern (50,000 L), septic (2,000 US gal), cranes (2x 5-ton), currency (CAD) | Parameters are contextual; not directly priced but inform quantity validation |
| PS-4 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` | Parametric fee model | CSV; 5 discipline fee percentage ranges; columns: ItemID, Discipline, Description, FeePercentMin/Max/Recommended, FeeBase, Basis, Confidence, Notes | Alternative pricing method: percentage of construction value by discipline | Not used for DEL-level pricing in this run; LOE method from PS-2 preferred for deliverable-specific estimates |

## Document Sources (read for quantity takeoff)

| # | Source File | Type | Notes |
|---|------------|------|-------|
| DS-1 | `PKG-006_Plumbing Design/1_Working/DEL-006-08_Specification/_CONTEXT.md` | Deliverable context | Deliverable ID, name, package, discipline, artifact type, anticipated artifacts |
| DS-2 | `PKG-006_Plumbing Design/1_Working/DEL-006-08_Specification/Datasheet.md` | Engineering content | Systems covered, key dimensional/quantity data, conditions, construction details |
| DS-3 | `PKG-006_Plumbing Design/1_Working/DEL-006-08_Specification/Specification.md` | Engineering content | Requirements (SPEC-PLB-001 to SPEC-PLB-091), standards, verification, documentation |
| DS-4 | `PKG-006_Plumbing Design/1_Working/DEL-006-08_Specification/Guidance.md` | Engineering content | Principles, considerations, trade-offs, conflict table |
| DS-5 | `PKG-006_Plumbing Design/1_Working/DEL-006-08_Specification/Procedure.md` | Engineering content | 5-phase procedure, prerequisites, steps, verification, records |
| DS-6 | `_Decomposition/WDMLRL_Decomposition_Claude.md` | Decomposition | PKG-006 section; DEL-006-08 entry; WBS traceability |
