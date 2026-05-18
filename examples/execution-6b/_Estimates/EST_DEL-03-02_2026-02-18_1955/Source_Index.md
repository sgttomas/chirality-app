# Source Index

**RunID:** EST_DEL-03-02_2026-02-18_1955

---

## Price Sources

| # | Source File | Source Type | Used For | Parsing Notes | Coverage |
|---|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | Hourly rates (CAD) by role | CSV; 30 roles; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Used R-07 ($155/hr) for DEL-03-02 |
| 2 | `_PriceSources/Level_of_Effort.csv` | Level of Effort (hours) | Estimated hours per role per deliverable | CSV; 73 rows across all deliverables; filtered to Execution=6b, DeliverableID=DEL-03-02 | 1 row: R-07 at 10 hrs |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | Contextual parameters (not directly used for line-item pricing) | CSV; 29 parameters; confirmed site area (PP-09, PP-10) | Not used for DEL-03-02 pricing; context only |

## Decomposition Source

| Source File | Version | Status | Used For |
|---|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | v2.3 FINAL | ACCEPTED | Package/deliverable IDs, scope mapping, CBS rule derivation |

## Dependency Source

| Source File | Row Count | Used For |
|---|---|---|
| `PKG-003_Design_Brief/1_Working/DEL-03-02_CivilDesignBrief/Dependencies.csv` | 18 rows | Blocker/readiness assessment; upstream prerequisite identification |
