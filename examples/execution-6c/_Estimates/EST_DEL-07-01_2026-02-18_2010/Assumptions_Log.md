# Assumptions Log — EST_DEL-07-01_2026-02-18_2010

## Assumptions

### ASM-01: Hourly Rates Reflect Alberta 2024 Market

| Field | Value |
|---|---|
| **Assumption** | Hourly rates in Professional_Staff_Rates.csv are representative of Alberta 2024 market rates for a Design-Build firm |
| **Source** | Professional_Staff_Rates.csv header note: "Basis = MARKET"; INDEX.md Data Quality Statement |
| **Impact if Wrong** | +/- 20-30% on total estimate (both rates marked MEDIUM confidence) |
| **Confidence** | MED |

### ASM-02: Level of Effort Calibrated for Consolidated Decomposition

| Field | Value |
|---|---|
| **Assumption** | The 20 total hours (16 writer + 4 PM) in Level_of_Effort.csv are appropriately calibrated for the consolidated 6c decomposition scope of DEL-07-01 |
| **Source** | Level_of_Effort.csv rows 52-53; LOE Notes state "Same scope as 6b DEL-01-07" |
| **Impact if Wrong** | Hours could vary +/- 25% depending on actual firm portfolio complexity and number of comparable projects to summarize |
| **Confidence** | MED |

### ASM-03: Firm Experience Scope Limited to DEL-07-01

| Field | Value |
|---|---|
| **Assumption** | Firm experience narrative writing is entirely within DEL-07-01 and does not overlap with DEL-07-02 (Key Team Members) costs |
| **Source** | BOE Context states "Cost Ownership: Firm experience narrative writing belongs to DEL-07-01 (NOT in DEL-07-02)" |
| **Impact if Wrong** | Double-counting risk if firm experience writing is also costed in DEL-07-02 |
| **Confidence** | HIGH |

### ASM-04: No External Costs for Reference Compilation

| Field | Value |
|---|---|
| **Assumption** | Reference compilation (contacting past clients, gathering project data) is performed by internal staff at the costed hourly rates; no external fees |
| **Source** | Level_of_Effort.csv does not include any external cost rows for DEL-07-01 |
| **Impact if Wrong** | Minor -- external reference verification fees would be small if incurred |
| **Confidence** | HIGH |
