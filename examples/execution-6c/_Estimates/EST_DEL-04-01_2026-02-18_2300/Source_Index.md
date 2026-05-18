# Source Index

## Price Sources Used

### PS-01: Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| **Path** | `_PriceSources/Professional_Staff_Rates.csv` |
| **Source Type** | Rate table |
| **Format** | CSV, 30 rows (roles R-01 through R-30) |
| **Parsing Notes** | Clean CSV; all rates in CAD/hr; Confidence column present |
| **Supports** | Hourly rates for all professional staff roles. DEL-04-01 uses R-15 (Construction Manager, $155/hr) and R-02 (Project Manager, $175/hr). |
| **Cannot Support** | Construction material/equipment pricing; subcontractor quotes |

### PS-02: Level_of_Effort.csv

| Field | Value |
|---|---|
| **Path** | `_PriceSources/Level_of_Effort.csv` |
| **Source Type** | Rate table (hours per role per deliverable) |
| **Format** | CSV, 65 rows total; 2 rows for DEL-04-01 |
| **Parsing Notes** | Filtered on `DeliverableID=DEL-04-01` and `Execution=6c`. Basis column = PARAMETRIC for all rows. |
| **Supports** | Hours allocation: R-15 = 14 hours, R-02 = 4 hours for DEL-04-01. Notes confirm consolidated SOW-019 + SOW-020 scope. |
| **Cannot Support** | Rates (rates come from Professional_Staff_Rates.csv) |

### PS-03: Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | `_PriceSources/Assumed_Project_Parameters.csv` |
| **Source Type** | Parameters (contextual) |
| **Format** | CSV, 29 rows |
| **Parsing Notes** | No direct pricing data for DEL-04-01. Provides project context (durations, areas, quantities). |
| **Supports** | Context for scope calibration: PP-01 (18-month construction), PP-04 (6-week proposal prep), PP-05 through PP-08 (building areas). Used as background for LOE reasonableness check only. |
| **Cannot Support** | Direct pricing of any line item |

## Dependency Sources Used

### DEP-01: Dependencies.csv (DEL-04-01)

| Field | Value |
|---|---|
| **Path** | `PKG-06_Construction Methodology + Administration/1_Working/DEL-04-01_ConstructionMethodologyNarrative/Dependencies.csv` |
| **Source Type** | Dependency register |
| **Used For** | Blocker/readiness assessment only (not pricing evidence) |
| **Key Finding** | 3 upstream prerequisites (DEL-02-01, DEL-08-01, DEL-09-02) all PENDING; no impact on estimating since cost is driven by staff effort, not upstream content |
