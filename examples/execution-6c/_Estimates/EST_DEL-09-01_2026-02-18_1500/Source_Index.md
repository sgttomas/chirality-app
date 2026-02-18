# Source Index

## Run: EST_DEL-09-01_2026-02-18_1500

---

## Indexed Price Sources

### PS-01: Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv |
| **Source Type** | Rate Table |
| **Format** | CSV (7 columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes) |
| **Items** | 30 roles (R-01 through R-30) |
| **Basis** | MARKET (Alberta 2024 market rates for DB professional services) |
| **Confidence** | MEDIUM for all active roles |
| **Parsing Notes** | Clean CSV; no parsing issues. R-30 (Surety Broker) has $0 rate (commission-based). |
| **Supports** | Unit rates ($/hr) for all professional labour line items |
| **Does Not Support** | Material costs, equipment costs, construction trade labour |
| **Roles Used for DEL-09-01** | R-02 (PM, $175/hr), R-15 (CM, $155/hr), R-23 (Quality Lead, $130/hr) |

### PS-02: Level_of_Effort.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv |
| **Source Type** | Rate Table (hours allocation) |
| **Format** | CSV (8 columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes) |
| **Items** | 65 rows total; 3 rows for DEL-09-01 |
| **Basis** | PARAMETRIC (planning estimates based on comparable $15-20M municipal DB proposal efforts) |
| **Confidence** | MEDIUM (inherent in LOE estimates) |
| **Parsing Notes** | Clean CSV; filtered to Execution=6c and DeliverableID=DEL-09-01. |
| **Supports** | Quantities (hours) per role per deliverable |
| **Does Not Support** | Unit rates (those come from PS-01) |
| **Rows Used for DEL-09-01** | R-02: 10hr, R-23: 8hr, R-15: 4hr (total 22hr) |

### PS-03: Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv |
| **Source Type** | Reference parameters (context) |
| **Format** | CSV (8 columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes) |
| **Items** | 29 parameters (PP-01 through PP-29) |
| **Parsing Notes** | Clean CSV; no direct pricing data for DEL-09-01 production. |
| **Supports** | Project context for scope calibration (e.g., PP-04 proposal preparation duration = 6 weeks) |
| **Does Not Support** | Direct pricing of DEL-09-01 line items |

---

## Source Coverage Assessment

| Metric | Value |
|---|---|
| Line items in Detail.csv | 3 |
| Line items with complete SourceRef | 3 (100%) |
| Line items with TBD SourceRef | 0 (0%) |
| Rate table coverage | All 3 roles have confirmed hourly rates in PS-01 |
| LOE coverage | All 3 roles have confirmed hour allocations in PS-02 |
