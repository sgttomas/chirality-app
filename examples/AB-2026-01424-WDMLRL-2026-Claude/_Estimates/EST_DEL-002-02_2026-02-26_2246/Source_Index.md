# Source Index — EST_DEL-002-02_2026-02-26_2246

## Price Sources Used

| Source File | Source Type | Path | What It Supports | Parsing Notes |
|---|---|---|---|---|
| Professional_Staff_Rates.csv | Rate table | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv | Hourly rates by role (R-01 through R-25); CAD; PARAMETRIC basis; MEDIUM confidence | CSV with columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. All rates are PARAMETRIC basis. |
| Level_of_Effort.csv | Parametric model | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv | Estimated hours per role per deliverable; DEL-002-02 has 4 role assignments (R-01, R-08, R-13, R-14) totalling 130 hr | CSV with columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. Filtered to DEL-002-02 rows. |
| Assumed_Project_Parameters.csv | Parametric context | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv | Project parameters for validation (building area, ceiling height, equipment counts, currency); 19 parameters | CSV with columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes. Used for context validation only — no direct pricing. |
| Professional_Design_Fees.csv | Parametric model (cross-check) | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv | Fee percentage model for structural design (DF-02: 1.2%-2.5%, recommended 1.8% of construction value); used as cross-check only | CSV with columns: ItemID, Discipline, Description, FeePercentMin, FeePercentMax, RecommendedPercent, FeeBase, Basis, Confidence, Notes. Not directly used for line-item pricing. |

## Document Sources Read

| Document | Path | Role in Estimate |
|---|---|---|
| _CONTEXT.md | PKG-002_Structural Design/1_Working/DEL-002-02_Foundation-Plan/_CONTEXT.md | Deliverable identification, package, discipline, type |
| Datasheet.md | PKG-002_Structural Design/1_Working/DEL-002-02_Foundation-Plan/Datasheet.md | Building configuration, foundation attributes, structural loads, bay layout, conditions |
| Specification.md | PKG-002_Structural Design/1_Working/DEL-002-02_Foundation-Plan/Specification.md | 13 requirements (R-001 through R-013), standards, verification matrix |
| Guidance.md | PKG-002_Structural Design/1_Working/DEL-002-02_Foundation-Plan/Guidance.md | Design principles, considerations, trade-offs |
| Procedure.md | PKG-002_Structural Design/1_Working/DEL-002-02_Foundation-Plan/Procedure.md | 8 procedural steps, prerequisites, verification checks, records |
| WDMLRL_Decomposition_Claude.md | _Decomposition/WDMLRL_Decomposition_Claude.md | WBS traceability (PKG-002, DEL-002-02, SOW-0012, SOW-0019) |

## Sources Not Used (available but not applicable to this deliverable scope)

| Source File | Reason Not Used |
|---|---|
| Structural_Concrete_Rates.csv | Construction material/labour rates — DEL-002-02 is a design deliverable (drawing set), not a construction deliverable |
| Building_Envelope_Rates.csv | Not applicable to foundation plan design |
| Construction_Labour_Rates.csv | Not applicable to design deliverable |
| Earthwork_Civil_Rates.csv | Not applicable to design deliverable |
| Electrical_System_Rates.csv | Not applicable to structural design |
| Equipment_Pricing.csv | Not applicable to design deliverable |
| Fees_Permits_Insurance.csv | Not applicable to this deliverable |
| Interior_Architectural_Rates.csv | Not applicable to structural design |
| Mechanical_System_Rates.csv | Not applicable to structural design |
| Optional_Items_Pricing.csv | Not applicable to this deliverable |
| Parametric_Building_Rates.csv | Not applicable to design deliverable |
| Paving_Surfacing_Rates.csv | Not applicable to structural design |
| Underground_Utility_Rates.csv | Not applicable to design deliverable |
