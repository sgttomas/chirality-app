# Source Index

## Price Sources Used

### PS-01: Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| **Path** | `_PriceSources/Professional_Staff_Rates.csv` |
| **Source Type** | Rate table |
| **Format** | CSV, 30 rows (roles R-01 through R-30) |
| **Parsing Notes** | Clean CSV; all rates in CAD/hr; Confidence column present |
| **Supports** | Hourly rates for all professional staff roles. DEL-04-02 uses R-02 (Project Manager, $175/hr) and R-15 (Construction Manager, $155/hr). |
| **Cannot Support** | Construction material/equipment pricing; subcontractor quotes |

### PS-02: Level_of_Effort.csv

| Field | Value |
|---|---|
| **Path** | `_PriceSources/Level_of_Effort.csv` |
| **Source Type** | Rate table (hours per role per deliverable) |
| **Format** | CSV, 65 rows total; 2 rows for DEL-04-02 |
| **Parsing Notes** | Filtered on `DeliverableID=DEL-04-02` and `Execution=6c`. Basis column = PARAMETRIC for all rows. |
| **Supports** | Hours allocation: R-02 = 8 hours (cost reporting, change management, contingency approach), R-15 = 4 hours (budget control input) for DEL-04-02. |
| **Cannot Support** | Rates (rates come from Professional_Staff_Rates.csv) |

### PS-03: Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | `_PriceSources/Assumed_Project_Parameters.csv` |
| **Source Type** | Parameters (contextual) |
| **Format** | CSV, 29 rows |
| **Parsing Notes** | No direct pricing data for DEL-04-02. Provides project context (durations, areas, quantities). |
| **Supports** | Context for scope calibration: PP-01 (18-month construction duration), PP-04 (6-week proposal prep), PP-25 ($12M estimated total project value). Used as background for LOE reasonableness check only. |
| **Cannot Support** | Direct pricing of any line item |

## Dependency Sources Used

### DEP-01: Dependencies.csv (DEL-04-02)

| Field | Value |
|---|---|
| **Path** | `PKG-06_Construction Methodology + Administration/1_Working/DEL-04-02_BudgetControlAndChangeManagementPlan/Dependencies.csv` |
| **Source Type** | Dependency register |
| **Used For** | Blocker/readiness assessment only (not pricing evidence) |
| **Key Finding** | 3 upstream PREREQUISITE dependencies (DEL-05-01, DEL-05-02, DEL-05-03) all PENDING; 4 upstream INTERFACE dependencies (DEL-04-03, DEL-08-01, DEL-09-01, DEL-04-01) all PENDING; no impact on estimating since cost is driven by staff effort, not upstream content |
