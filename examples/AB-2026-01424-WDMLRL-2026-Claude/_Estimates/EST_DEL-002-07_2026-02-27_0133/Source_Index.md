# Source Index — EST_DEL-002-07_2026-02-27_0133

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports | Limitations |
|---|---|---|---|---|---|
| PS-1 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | PARAMETRIC (rate table) | CSV; 25 roles with RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Hourly rates for all professional staff roles (R-01 through R-25) | Rates are PARAMETRIC basis with MEDIUM confidence; not vendor quotes |
| PS-2 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | PARAMETRIC (LOE model) | CSV; rows per Execution/DeliverableID/RoleID with EstimatedHours | Hour estimates for each role on each deliverable | Hours are parametric estimates with PARAMETRIC basis; not actuals or quotes |
| PS-3 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC (project parameters) | CSV; 19 rows of project-level parameters (identity, location, contract, schedule, facility, equipment, currency) | Context parameters for parametric models (building area, crane count/capacity, ceiling height, currency) | Parameters are a mix of CONFIRMED, DERIVED, DESIGN_BASIS, and ASSUMPTION confidence levels |
| PS-4 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` | PARAMETRIC (fee model) | CSV; 5 discipline-level design fee percentages (Architecture, Structural, Mechanical, Electrical, Civil) | Alternative fee-based pricing if LOE is unavailable; structural fee = 1.8% of construction value (recommended) | Fee-based pricing not used in this run (LOE-based pricing preferred); construction value not established |

## Document Sources (Deliverable Content)

| # | Source File | Role |
|---|---|---|
| DS-1 | `PKG-002_Structural Design/1_Working/DEL-002-07_Crane-Support-Details/_CONTEXT.md` | Deliverable identity, package, discipline, type |
| DS-2 | `PKG-002_Structural Design/1_Working/DEL-002-07_Crane-Support-Details/Datasheet.md` | Attributes, quantities, materials, conditions |
| DS-3 | `PKG-002_Structural Design/1_Working/DEL-002-07_Crane-Support-Details/Specification.md` | Requirements, standards, verification criteria |
| DS-4 | `PKG-002_Structural Design/1_Working/DEL-002-07_Crane-Support-Details/Guidance.md` | Principles, trade-offs, design rationale |
| DS-5 | `PKG-002_Structural Design/1_Working/DEL-002-07_Crane-Support-Details/Procedure.md` | Prerequisites, work steps, verification, records |

## Decomposition Source

| # | Source File | Role |
|---|---|---|
| DEC-1 | `_Decomposition/WDMLRL_Decomposition_Claude.md` | WBS traceability — PKG-002, DEL-002-07, SOW-0012 mapping |
