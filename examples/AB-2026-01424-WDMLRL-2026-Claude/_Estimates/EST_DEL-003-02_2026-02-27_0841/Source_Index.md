# Source Index — EST_DEL-003-02_2026-02-27_0841

## Pricing Sources

| # | Source File | Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv | PARAMETRIC rate table | 25 rows; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. All rates in CAD. | Hourly rates for all 4 roles used in this estimate (R-01, R-08, R-13, R-15) |
| 2 | Level_of_Effort.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv | PARAMETRIC LOE model | Multi-deliverable file; rows filtered to DEL-003-02 only. Columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. | Hour estimates for DEL-003-02: R-01=6h, R-08=4h, R-13=36h, R-15=84h |
| 3 | Assumed_Project_Parameters.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv | Project parameters | 19 rows of confirmed/assumed project parameters. Used for context validation (building area, ceiling height, crane count, currency). | Context validation — confirms building is ~13,000 sqft, 35 ft ceiling, 2 cranes, CAD currency |
| 4 | Professional_Design_Fees.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv | PARAMETRIC fee model | 5 rows by discipline. Mechanical fee = 1.0%–2.2% of construction value (recommended 1.6%). | Not used for primary pricing (construction value not established). Available as cross-check if construction value becomes known. |

## Document Sources (Read-Only — Deliverable Content)

| Document | Path | Used For |
|---|---|---|
| _CONTEXT.md | PKG-003_Mechanical Design/1_Working/DEL-003-02_HVAC-Plans/_CONTEXT.md | Deliverable identification, package, discipline |
| Datasheet.md | PKG-003_Mechanical Design/1_Working/DEL-003-02_HVAC-Plans/Datasheet.md | HVAC system attributes, building context, equipment list, conditions |
| Specification.md | PKG-003_Mechanical Design/1_Working/DEL-003-02_HVAC-Plans/Specification.md | Requirements (REQ-001 through REQ-016), verification methods, standards |
| Guidance.md | PKG-003_Mechanical Design/1_Working/DEL-003-02_HVAC-Plans/Guidance.md | Design principles, considerations, trade-offs |
| Procedure.md | PKG-003_Mechanical Design/1_Working/DEL-003-02_HVAC-Plans/Procedure.md | Work steps (Steps 1-9), prerequisites, verification, records |
| Decomposition | _Decomposition/WDMLRL_Decomposition_Claude.md | WBS traceability — PKG-003, DEL-003-02, SOW-0013 |

## Source Gaps

| Gap | Impact | Mitigation |
|---|---|---|
| Construction value not established | Cannot cross-check LOE estimate against percentage-of-construction-value method (Professional_Design_Fees.csv DF-03) | LOE-based estimate used as sole method; fee-based cross-check deferred |
| No quote or historical data available | Cannot validate PARAMETRIC rates against market quotes or prior project actuals | Rates accepted at MEDIUM confidence per source data |
