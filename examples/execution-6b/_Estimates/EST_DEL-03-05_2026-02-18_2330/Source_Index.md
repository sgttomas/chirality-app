# Source Index

## Pricing Sources Used

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 30 roles; CAD hourly rates; Basis=MARKET; Confidence=MEDIUM | Unit rates for all labour line items |
| 2 | `_PriceSources/Level_of_Effort.csv` | Level of Effort (hours) | 73 rows; maps deliverable/role to estimated hours; Basis=PARAMETRIC | Quantity (hours) for all labour line items |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | 29 parameters; used for context only | No direct pricing for DEL-03-05; context for scope understanding |

## Pricing Sources -- DEL-03-05 Specific Usage

### Professional_Staff_Rates.csv

| RoleID | Role | HourlyRate_CAD | Used In |
|---|---|---:|---|
| R-13 | Electrical Engineer (Senior) | $155 | L-0305-01 |

### Level_of_Effort.csv

| DeliverableID | RoleID | Role | EstimatedHours | Used In |
|---|---|---|---:|---|
| DEL-03-05 | R-13 | Electrical Engineer (Senior) | 10 | L-0305-01 |

## Non-Pricing Sources Referenced

| Source | Usage |
|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL) | Package/deliverable IDs, scope mapping, deliverable description |
| `DEL-03-05/Dependencies.csv` | Dependency evidence for blocker analysis (10 rows) |
