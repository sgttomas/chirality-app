# Source Index -- EST_DEL-02-03_2026-02-18_1500

## Price Sources Indexed

### PS-01: Professional_Staff_Rates.csv

| Field | Value |
|-------|-------|
| **Path** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv` |
| **Source Type** | Rate Table |
| **Items** | 30 roles with RoleID, Role name, Category, HourlyRate_CAD, Basis, Confidence |
| **Parsing Notes** | Standard CSV; header row present; all rates in CAD. Basis = MARKET for all active roles. |
| **Supports** | Hourly unit rates for all professional staff roles used in DEL-02-03 line items |
| **Roles Used (DEL-02-03)** | R-04 ($145/hr), R-11 ($160/hr), R-13 ($155/hr), R-27 ($165/hr) |

### PS-02: Level_of_Effort.csv

| Field | Value |
|-------|-------|
| **Path** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv` |
| **Source Type** | Rate Table (hours allocation) |
| **Items** | 65 rows across 21 deliverables; 4 rows applicable to DEL-02-03 |
| **Parsing Notes** | Standard CSV; Execution=6c filter applied; Basis column = PARAMETRIC for all rows |
| **Supports** | Quantity (hours) for each role assigned to DEL-02-03 |
| **Rows Used (DEL-02-03)** | Row 28: R-27/12hr; Row 29: R-11/8hr; Row 30: R-13/6hr; Row 31: R-04/4hr |
| **Cannot Support** | Direct unit rates (rates come from PS-01) |

### PS-03: Assumed_Project_Parameters.csv

| Field | Value |
|-------|-------|
| **Path** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv` |
| **Source Type** | Parameter Table |
| **Items** | 29 project parameters (durations, areas, quantities, financial estimates) |
| **Parsing Notes** | Standard CSV; mixed Confidence levels (HIGH/MEDIUM/LOW) |
| **Supports** | Contextual scope calibration (building area, site parameters) used to validate reasonableness of LOE hours |
| **Cannot Support** | Direct pricing for DEL-02-03 (no unit rates or amounts applicable to proposal production) |

---

## Source Coverage Assessment

| Line Item | UnitRate Source | Qty Source | Coverage |
|-----------|---------------|-----------|----------|
| L-001 (R-27 Building Science) | PS-01 R-27 | PS-02 row 28 | COMPLETE |
| L-002 (R-11 Mech Eng Sr) | PS-01 R-11 | PS-02 row 29 | COMPLETE |
| L-003 (R-13 Elec Eng Sr) | PS-01 R-13 | PS-02 row 30 | COMPLETE |
| L-004 (R-04 Architect) | PS-01 R-04 | PS-02 row 31 | COMPLETE |

**Provenance completeness: 4/4 lines = 100%**
