# Source Index

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | What It Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 30 roles with RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence. All rates are MARKET basis, MEDIUM confidence. | Hourly unit rates for all professional roles. Used to price each role's hours. |
| 2 | `_PriceSources/Level_of_Effort.csv` | Rate Table (hours) | 73 rows mapping Execution/DeliverableID/RoleID to EstimatedHours. Basis=PARAMETRIC for all rows. | Hours allocation per role per deliverable. Used to determine quantities (hours) for each line item. |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | 29 parameters covering duration, area, quantities, financial estimates. Mixed confidence (CONFIRMED/ASSUMPTION/PARAMETRIC/DERIVED). | Background project parameters. Not directly used for DEL-01-01 pricing (no construction quantities involved). |

## Decomposition Source

| Source File | Version | Status | What It Supports |
|---|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | v2.3 FINAL | ACCEPTED | Package IDs, Deliverable IDs, scope item mappings, constraint IDs. Used for WBS assignment and scope validation. |

## Dependency Source

| Source File | Row Count | What It Supports |
|---|---|---|
| `DEL-01-01_ComplianceMatrixAndChecklist/Dependencies.csv` | 18 dependency rows | Blocker/readiness assessment. 0 rows identified as blocking estimate production. All dependencies are document prerequisites or constraint anchors. |
