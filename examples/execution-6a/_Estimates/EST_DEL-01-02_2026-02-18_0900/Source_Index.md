# Source Index — EST_DEL-01-02_2026-02-18_0900

## Indexed Price Sources

### 1. Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| Path | {RUN_ROOT}/_PriceSources/Professional_Staff_Rates.csv |
| Source Type | Rate Table |
| Format | CSV; 31 rows (header + 30 roles + 1 N/A row) |
| Currency | CAD |
| Confidence | MEDIUM (all rates marked MARKET basis) |
| Used For | Hourly unit rates for R-02 (Project Manager, $175/hr) and R-17 (Scheduler, $130/hr) |
| Cannot Support | Software/tools costs; non-labour items; construction material rates |
| Parsing Notes | Clean CSV; no parsing issues. RoleID is the primary key. |

### 2. Level_of_Effort.csv

| Field | Value |
|---|---|
| Path | {RUN_ROOT}/_PriceSources/Level_of_Effort.csv |
| Source Type | Rate Table (quantity input — hours by role by deliverable) |
| Format | CSV; 18 rows (header + 17 role-deliverable assignments) |
| Basis | PARAMETRIC (all rows declare Basis=PARAMETRIC) |
| Used For | Hour quantities for DEL-01-02: R-17 (80 hrs), R-02 (20 hrs) |
| Cannot Support | Non-labour costs; rates (rates come from Professional_Staff_Rates.csv) |
| Parsing Notes | Clean CSV. Filtered to Execution=6a and DeliverableID=DEL-01-02. Two matching rows found. Notes column provides hour derivation narratives. |

### 3. Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| Path | {RUN_ROOT}/_PriceSources/Assumed_Project_Parameters.csv |
| Source Type | Rate Table (project parameters supporting quantity derivation) |
| Format | CSV; 29 rows (header + 28 parameters) |
| Used For | Corroboration of LOE assumptions — PP-01 (18-month construction duration) supports the monthly-update hour calculation in LOE (2h/mo x 18mo = 36h) |
| Cannot Support | Direct pricing; no unit rates or costs (except rough parametric values at LOW confidence not used here) |
| Parsing Notes | Clean CSV. ParameterID is the primary key. Financial parameters (PP-21 through PP-25) are LOW confidence parametric values not used for this estimate. |

## Sources Not Indexed (Excluded per Brief)

The following paths were excluded per the EXCLUSIONS list in the brief:
- `{RUN_ROOT}/_Estimates/**`
- `{RUN_ROOT}/_Aggregation/**`
- `{RUN_ROOT}/_Reconciliation/**`
- `{RUN_ROOT}/_Archive/**`

## Dependency Evidence (Not a Pricing Source)

| Path | Used For |
|---|---|
| DEL-01-02/Dependencies.csv | Blocker/readiness analysis only; not used for pricing |
