# Source Index — EST_DEL-01-02_2026-02-18_2100

## Revision Note

This source index extends the prior run (EST_DEL-01-02_2026-02-18_0900) with no additional price source files. The TBD resolution for L-003 uses a parametric allowance (not sourced from a rate table file).

## Indexed Price Sources

### 1. Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| Path | {RUN_ROOT}/_PriceSources/Professional_Staff_Rates.csv |
| Source Type | Rate Table |
| Used For | Hourly unit rates for R-02 (PM, $175/hr) and R-17 (Scheduler, $130/hr) |

### 2. Level_of_Effort.csv

| Field | Value |
|---|---|
| Path | {RUN_ROOT}/_PriceSources/Level_of_Effort.csv |
| Source Type | Rate Table (quantity input) |
| Used For | Hour quantities for DEL-01-02: R-17 (80 hrs), R-02 (20 hrs) |

### 3. Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| Path | {RUN_ROOT}/_PriceSources/Assumed_Project_Parameters.csv |
| Source Type | Project parameters |
| Used For | PP-01 (18-month duration) corroborates LOE hour derivation |

## Parametric Allowance Sources (no file reference)

| Line | Item | Allowance Basis |
|---|---|---|
| L-003 | Scheduling software/tools | Parametric estimate based on typical project scheduling software licensing costs (P6/MS Project) for an 18-month Alberta construction project. No vendor quote or rate table. |
