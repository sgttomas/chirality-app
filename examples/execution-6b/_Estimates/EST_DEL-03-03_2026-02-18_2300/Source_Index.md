# Source Index

## Price Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 30 roles with hourly rates in CAD; used R-09 (Structural Engineer Senior, $155/hr) | Unit rate for DEL-03-03 line item |
| 2 | `_PriceSources/Level_of_Effort.csv` | Rate Table (hours) | 73 rows mapping deliverables to roles with estimated hours; Execution=6b; used DEL-03-03/R-09 row (10 hr) | Quantity (hours) for DEL-03-03 line item |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Parametric Parameters | 29 parameters covering duration, area, quantities, financial estimates; no direct pricing role for this deliverable | Not used for pricing; available for context only |

## Decomposition Source

| Source File | Version | Used For |
|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | v2.3 FINAL | Package ID (PKG-003), Deliverable ID (DEL-03-03), deliverable description, scope item mappings (SOW-0011, SOW-0014), objective mappings (OBJ-004) |

## Dependency Source

| Source File | Row Count | Used For |
|---|---|---|
| `PKG-003_Design_Brief/1_Working/DEL-03-03_StructuralDesignBrief/Dependencies.csv` | 15 rows | Blocker identification; upstream prerequisite sequencing; downstream handover awareness |

## Source Usage Summary

- **Rows priced:** 1
- **Rows with complete SourceRef:** 1 (100%)
- **Rows with TBD SourceRef:** 0 (0%)
