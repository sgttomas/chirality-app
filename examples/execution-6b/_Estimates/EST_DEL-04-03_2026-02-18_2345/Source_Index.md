# Source Index

## Price Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 30 roles with RoleID, Role name, HourlyRate_CAD, Basis, Confidence. All rates basis=MARKET, confidence=MEDIUM. | Provides hourly rates by RoleID for all professional staff. Used to price DEL-04-03 line items via R-13 ($155/hr). |
| 2 | `_PriceSources/Level_of_Effort.csv` | Rate Table (hours) | 73 rows for Execution=6b across all 38 deliverables. Columns: DeliverableID, RoleID, EstimatedHours, Basis, Notes. All hours basis=PARAMETRIC. | Provides estimated hours per role per deliverable. DEL-04-03 has 1 row: R-13 at 8 hours. |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Parametric Parameters | 29 parameters covering duration, area, quantities, financial estimates. Mixed confidence (LOW to HIGH). | Contextual project parameters. Not directly used for DEL-04-03 pricing but provides project context (building areas, quantities, estimated values). |

## Decomposition Source

| Source | Version | Status |
|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | v2.3 FINAL | Used for package/deliverable ID validation, scope mapping, and deliverable descriptions. |

## Dependency Source

| Source | Rows | Status |
|---|---|---|
| `DEL-04-03_ElectricalEnergyEfficiency/Dependencies.csv` | 12 rows (v3.1 schema) | Read via AUTO mode. Used for blocker identification and readiness assessment. |
