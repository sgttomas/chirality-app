# Source Index

**RunID:** EST_DEL-06-01_2026-02-18_1600

---

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 31 rows; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. All rates marked MARKET basis, MEDIUM confidence. | Provides hourly rates (UnitRate) for all roles. Used for R-02 ($175/hr) and R-03 ($165/hr) in this estimate. |
| 2 | `_PriceSources/Level_of_Effort.csv` | Rate Table (quantity complement) | 73 rows covering all deliverables in execution 6b; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. All hours marked PARAMETRIC basis. | Provides hours (Qty) by deliverable and role. Used for DEL-06-01: R-03 = 10 hrs, R-02 = 4 hrs. |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | 29 rows; covers duration, area, quantity, and financial parameters. Not directly used for DEL-06-01 pricing but provides project context. | Not directly used for line-item pricing in this run. Available for parametric cross-checks if needed. |

## Decomposition Source

| Source File | Source Type | Notes |
|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | Decomposition (v2.3 FINAL) | Provides Package IDs, Deliverable IDs, descriptions, scope item mappings, and responsible parties. Used for WBS mapping and scope validation. |

## Dependency Sources

| Source File | Source Type | Notes |
|---|---|---|
| `PKG-006_Delivery_Plan/1_Working/DEL-06-01_DesignMethodologyNarrative/Dependencies.csv` | Dependency Register (v3.1) | 17 dependency rows for DEL-06-01. Used for blocker assessment only; not used for pricing evidence. |
