# Source Index — EST_DEL-01-03_2026-02-18_2100

## Revision Note

This source index extends the prior run (EST_DEL-01-03_2026-02-18_1720) with no additional price source files. TBD resolutions for L-0103-003 and L-0103-004 use parametric allowances.

## Indexed Price Sources

### 1. Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| Path | {RUN_ROOT}/_PriceSources/Professional_Staff_Rates.csv |
| Source Type | Rate table |
| Relevant Roles | R-20 (Safety Officer, $110/hr); R-24 (Admin/Doc Control, $80/hr) |

### 2. Level_of_Effort.csv

| Field | Value |
|---|---|
| Path | {RUN_ROOT}/_PriceSources/Level_of_Effort.csv |
| Source Type | Level of effort / hours table |
| Relevant Rows | DEL-01-03: R-20 = 60h; R-24 = 8h |

### 3. Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| Path | {RUN_ROOT}/_PriceSources/Assumed_Project_Parameters.csv |
| Source Type | Project parameters |
| Relevant Parameters | PP-01 (18-month construction duration) |

## Parametric Allowance Sources (no file reference)

| Line | Item | Allowance Basis |
|---|---|---|
| L-0103-003 | Training costs | Parametric estimate: site orientation + safety training sessions (WHMIS, first aid, confined space) for 30-40 construction workers over 18-month project. Based on typical Alberta construction site training budgets. |
| L-0103-004 | PPE/signage supplies | Parametric estimate: standard PPE inventory (hard hats, hi-vis vests, safety glasses, gloves) + first aid kits + site safety signage for 18-month project. Based on typical Alberta construction site safety supply budgets. |
