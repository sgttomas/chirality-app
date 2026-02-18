# Source Index — EST_DEL-01-06_2026-02-18_2100

## Revision Note

This source index extends the prior run (EST_DEL-01-06_2026-02-18_1030) with no additional price source files. TBD resolutions for L-0106-003 and L-0106-004 use parametric allowances.

## Price Sources

### Source 1: Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| Path | {RUN_ROOT}/_PriceSources/Professional_Staff_Rates.csv |
| Used for DEL-01-06 | R-16 Site Superintendent ($135/hr); R-15 Construction Manager ($155/hr) |

### Source 2: Level_of_Effort.csv

| Field | Value |
|---|---|
| Path | {RUN_ROOT}/_PriceSources/Level_of_Effort.csv |
| Used for DEL-01-06 | R-16 (1,440 hrs); R-15 (60 hrs) |

### Source 3: Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| Path | {RUN_ROOT}/_PriceSources/Assumed_Project_Parameters.csv |
| Used for DEL-01-06 | PP-01 (18-month duration); PP-05 (18,000 sf main building); PP-07 (6,000 sf cold storage) |

## Parametric Allowance Sources (no file reference)

| Line | Item | Allowance Basis |
|---|---|---|
| L-0106-003 | Temp facilities/fencing | Parametric estimate based on typical rural Alberta construction site: trailer rental, temp power, fencing, portable washrooms over 18-month duration. Compressed from component sum (~$60k) to $35k reflecting rural site efficiencies. |
| L-0106-004 | Site cleaning | Parametric estimate: ongoing cleanup at $800/mo x 18mo ($14,400) + final pre-occupancy clean for 24,000 sf ($10,000). Total $25,000 (rounded). |
