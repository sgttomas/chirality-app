# Source_Index — EST_DEL-013-01_2026-02-27_1045

## Pricing Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | Professional_Staff_Rates.csv | RATE_TABLE | 25 roles; HourlyRate_CAD column; Basis=PARAMETRIC; Confidence=MEDIUM | Professional staff hourly rates (R-01 through R-25) for management, design, specialty, and admin roles |
| PS-02 | Level_of_Effort.csv | PARAMETRIC | Multi-deliverable LOE allocation; columns: DeliverableID, RoleID, EstimatedHours | DEL-013-01 has 6 role allocations: R-01 (6 hr), R-02 (8 hr), R-03 (10 hr), R-05 (4 hr), R-06 (6 hr), R-08 (4 hr) |
| PS-03 | Assumed_Project_Parameters.csv | PARAMETRIC | 19 project parameters; includes building area (13,000 sqft), ceiling height (35 ft), currency (CAD), crane quantities | Building area for ductwork normalization; general project parameters |
| PS-04 | Mechanical_System_Rates.csv | ALLOWANCE / PARAMETRIC | 6 mechanical system items; RateMin/RateMax/RecommendedRate | MS-01 (unit heater $6,500/ea), MS-06 (ductwork $60/m2) directly applicable to DEL-013-01 |
| PS-05 | Construction_Labour_Rates.csv | RATE_TABLE | 10 trades; HourlyRate + BurdenMultiplier = FullyBurdenedRate_CAD | T-04 Electrician ($96/hr), T-05 Plumber ($92.80/hr), T-06 HVAC Sheet Metal ($91.20/hr), T-08 Labourer ($65.10/hr) |
| PS-06 | Equipment_Pricing.csv | ALLOWANCE | 3 major equipment items; not directly applicable to heating system | EQ-01 (cranes), EQ-02 (wash bay), EQ-03 (compressor) — none apply to DEL-013-01 |

## Coverage Assessment

- **Directly applicable:** PS-01, PS-02, PS-04, PS-05 provide direct pricing evidence for the majority of line items.
- **Indirectly applicable:** PS-03 provides the building area parameter (13,000 sqft = ~1,208 m2) used for ductwork quantity normalization.
- **Not applicable:** PS-06 (Equipment_Pricing.csv) contains no heating system equipment; heating unit priced via PS-04 (Mechanical_System_Rates.csv MS-01).
- **Gaps:** No source provides a specific quote or rate for BMS/controls integration, heat recovery connections, or gas fitter scope. These are priced parametrically with assumptions documented in Assumptions_Log.md.
