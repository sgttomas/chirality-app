# Source Index — EST_DEL-002-05_2026-02-27_0600

## Indexed Pricing Sources

### Source 1 — Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv |
| **Type** | Rate Table (PARAMETRIC) |
| **Content** | 25 professional roles with hourly rates in CAD. Includes RoleID, Role, Category, HourlyRate_CAD, Basis (all PARAMETRIC), Confidence (all MEDIUM). |
| **Supports** | All UNIT_RATE items (ITEM-001 through ITEM-004) and effort-based parametric pricing for LUMP_SUM items. |
| **Parsing Notes** | Standard CSV; no issues. All rates stated as PARAMETRIC basis with MEDIUM confidence. |

**Key rates used for DEL-002-05:**

| RoleID | Role | HourlyRate_CAD |
|---|---|---|
| R-01 | Project Manager | 165 |
| R-08 | Cost Estimator | 135 |
| R-13 | BIM Technician | 95 |
| R-14 | Structural Engineer | 170 |

### Source 2 — Level_of_Effort.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv |
| **Type** | Parametric Model (PARAMETRIC) |
| **Content** | Estimated hours per role per deliverable across all project deliverables. Basis: PARAMETRIC. |
| **Supports** | Quantity (hours) for ITEM-001 through ITEM-004; basis for parametric effort estimates for lump-sum items. |
| **Parsing Notes** | Standard CSV; large file (all deliverables). Filtered to DEL-002-05 rows only. |

**DEL-002-05 rows:**

| RoleID | Role | EstimatedHours | Notes |
|---|---|---|---|
| R-01 | Project Manager | 6 | PKG-002 Structural Engineer -- Drawing Set |
| R-08 | Cost Estimator | 4 | PKG-002 Structural Engineer -- Drawing Set |
| R-13 | BIM Technician | 36 | PKG-002 Structural Engineer -- Drawing Set |
| R-14 | Structural Engineer | 84 | PKG-002 Structural Engineer -- Drawing Set |

### Source 3 — Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv |
| **Type** | Parametric Context (PARAMETRIC) |
| **Content** | 18 project parameters (identity, location, contract, schedule, facility, equipment, currency). |
| **Supports** | Contextual validation (currency = CAD, facility area ~13,000 sqft, 35' ceiling, 2x5-ton cranes, completion 2026-12-31). Does not directly supply unit rates. |
| **Parsing Notes** | Standard CSV; no issues. |

### Source 4 — Professional_Design_Fees.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv |
| **Type** | Parametric Model (PARAMETRIC) |
| **Content** | Design fee percentages by discipline as a percentage of construction value. Structural = 1.2%--2.5% (recommended 1.8%). |
| **Supports** | Cross-check / alternative parametric basis. Not used as primary pricing method for this deliverable (LOE-based approach preferred for single-deliverable scope). |
| **Parsing Notes** | Standard CSV; no issues. Construction value not determined, so fee-based method is not directly applicable at deliverable level. |
