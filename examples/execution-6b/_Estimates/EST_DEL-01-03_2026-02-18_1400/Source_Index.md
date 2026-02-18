# Source Index

## Pricing Sources Used

| Source File | Source Type | What It Supports | Parsing Notes |
|---|---|---|---|
| `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | Hourly rates for 30 roles (R-01 through R-30) in CAD | Clean CSV; 31 rows; used R-02, R-24, R-25 for DEL-01-03 |
| `_PriceSources/Level_of_Effort.csv` | Rate Table (hours) | Estimated hours by role per deliverable for execution-6b | Clean CSV; 73 rows; filtered to DEL-01-03: 3 rows (R-02=4h, R-25=4h, R-24=2h) |
| `_PriceSources/Assumed_Project_Parameters.csv` | Parametric Parameters | Project-level parameters including estimated contract value (PP-25=$12M) | Clean CSV; 29 rows; used PP-25 as basis for percentage-based bond/insurance calculations |
| `_PriceSources/Fees_Permits_Insurance.csv` | Allowance Table | Bond premiums, insurance rates, surety broker fee, permits, utility fees | Clean CSV; 19 rows; used FP-01, FP-02, FP-03, FP-19 for DEL-01-03 |

## Dependency Sources Used

| Source File | Source Type | What It Supports | Parsing Notes |
|---|---|---|---|
| `DEL-01-03_BondingAndInsuranceEvidence/Dependencies.csv` | Dependency Register | 13 dependency rows; upstream prereqs (DEL-01-04, DEL-01-05), downstream handovers (DEL-01-01, -02, -04, -05, -06), constraints (RFP 5.3.1, Appendix J SC 50-52) | Clean CSV v3.1 schema; no blocker dependencies identified that prevent estimating |

## Decomposition Source

| Source File | Version | What It Supports |
|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | v2.3 FINAL | Package/deliverable IDs, scope item mapping (SOW-0004), objectives (OBJ-001, OBJ-007), constraints (C-08) |
