# Source Index — EST_DEL-004-04_2026-02-28_0809

## Pricing Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `PriceSources/Professional_Staff_Rates.csv` | Rate Table (parametric) | 25 roles with hourly rates in CAD; Basis=PARAMETRIC; Confidence=MEDIUM for all. Parseable CSV with header row. | Unit rates for all professional staff line items (DL-001 through DL-004) |
| 2 | `PriceSources/Level_of_Effort.csv` | Parametric Model (LOE allocation) | Multi-deliverable LOE matrix. Columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. Filtered to DEL-004-04 rows: 4 roles, 130 total hours. Parseable CSV. | Hour quantities for ITEM-001 through ITEM-004 |
| 3 | `PriceSources/Assumed_Project_Parameters.csv` | Parametric Parameters | 19 parameters (PP-01 through PP-18) covering identity, location, contract, schedule, facility, equipment, plumbing, mechanical, currency, economics. Parseable CSV. | Context parameters (building area 13,000 sqft, ceiling height 35 ft, currency CAD). Not directly used for unit pricing but confirms scope context. |
| 4 | `PriceSources/Professional_Design_Fees.csv` | Parametric Model (fee percentages) | 5 discipline fee ranges (DF-01 through DF-05) as percentage of construction value. Electrical (DF-04): 1.0%--2.2%, recommended 1.6%. Parseable CSV. | Alternative fee-based pricing method for electrical design (not used for this run -- LOE-based pricing preferred for single-deliverable scope). |

## Sources NOT Available

| Gap | Impact |
|---|---|
| Emergency/exit lighting scope determination | Cannot price ITEM-015/DL-015 until Alberta Building Code applicability is confirmed (CONF-LT-003). Conditional allowance ~$5,800 noted in project notes. |

## Sources Resolved Since Prior Snapshot

| Gap (Prior) | Resolution |
|---|---|
| Fixture hardware unit pricing (ITEM-005 through ITEM-010) | Resolved: hardware cost is in PKG-015 scope, not PKG-004 design-fee scope. DL-005 through DL-010 set to $0 per Decision_Log DEC-R01. No fixture pricing source needed for this estimate. |
| Service pit fixture specifications (CONF-LT-002) | Partially resolved for design-fee purposes: DL-010 set to $0 (hardware cost in PKG-015). Fixture specs remain TBD but do not affect design-fee total. |
