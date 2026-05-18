# Source Index

## Price Sources Used

| # | File | Type | Items Used | Coverage | Notes |
|---|------|------|-----------|----------|-------|
| 1 | `_PriceSources/Mechanical_System_Rates.csv` | Rate Table | MS-01, MS-02, MS-03, MS-04, MS-05, MS-06, MS-07, MS-09, MS-10, MS-11, MS-12 | 11 of 14 items used | Primary pricing source for all mechanical/plumbing/exhaust systems. MS-08 (breathing air) excluded per cost ownership (DEL-02-02). MS-13 (cold storage vent) excluded (DEL-04-04). MS-14 (radiant in-floor) not selected for this estimate basis. |
| 2 | `_PriceSources/Equipment_Pricing.csv` | Rate Table | EQ-10 (reference only) | 1 of 15 items referenced | EQ-10 (bay sump) used as cross-reference to confirm MS-10 rate; MS-10 rate used for pricing. EQ-09 cross-confirms MS-09. |
| 3 | `_PriceSources/Construction_Labour_Rates.csv` | Labour Rate Table | T-05, T-06 | 2 of 15 trades used | Plumber/pipefitter ($82/hr) and sheet metal worker ($78/hr) rates used for commissioning labour and rough-in lump sums. |
| 4 | `_PriceSources/Professional_Design_Fees.csv` | Fee Schedule | DF-04 | 1 of 8 items used | Mechanical engineering design fees at 2.5% of mechanical construction cost. |
| 5 | `_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | PP-05, PP-11, PP-12, PP-17, PP-18 | 5 of 29 parameters used | Building area, bay counts, fill station count, sump count. |

## Decomposition Source

- **File:** `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md`
- **Used for:** Package/deliverable ID validation; scope item traceability (SOW-0204, SOW-0213, SOW-0214, SOW-0223, SOW-0230)
- **Status:** Loaded successfully

## Dependency Source

- **File:** `PKG-002.../DEL-02-05.../Dependencies.csv` (18 rows; schema v3.1)
- **Used for:** Blocker/readiness analysis; interface identification
- **Not used for:** Pricing evidence
