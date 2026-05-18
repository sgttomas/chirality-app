# Source Index

## Pricing Sources Used

| Source File | Source Type | Role in Estimate | Parsing Notes |
|---|---|---|---|
| `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | Provides hourly rates by RoleID; R-11 (Mechanical Engineer Senior) = $160/hr CAD | 31 rows; CSV format; clean parse; all rates in CAD |
| `_PriceSources/Level_of_Effort.csv` | Hours Table (Level of Effort) | Provides estimated hours by DeliverableID and RoleID; DEL-03-04 row: R-11 = 10 hrs | 73 rows; CSV format; clean parse; hours basis noted as PARAMETRIC in source |
| `_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | Referenced for context (building areas, quantities); not directly used for pricing DEL-03-04 | 29 rows; CSV format; clean parse; provides project-level context |

## Non-Pricing Sources Used

| Source File | Source Type | Role in Estimate |
|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | Decomposition (v2.3 FINAL) | Provides stable IDs, deliverable definition, package assignment, scope-item mapping |
| `PKG-003_Design_Brief/1_Working/DEL-03-04_MechanicalDesignBrief/Dependencies.csv` | Dependency Register | Provides upstream prerequisites and downstream interfaces for blocker assessment |

## Source Limitations

- **Level_of_Effort.csv hours basis:** The hours in Level_of_Effort.csv are noted as `PARAMETRIC` basis, meaning they are estimated rather than drawn from actual time records. This is acceptable for proposal-stage estimating but carries inherent uncertainty.
- **Rate confidence:** Professional_Staff_Rates.csv rates are noted as `MARKET` basis with `MEDIUM` confidence. Rates may vary by firm and region.
