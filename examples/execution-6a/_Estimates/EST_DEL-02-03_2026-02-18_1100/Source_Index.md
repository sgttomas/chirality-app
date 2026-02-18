# Source Index

## Run: EST_DEL-02-03_2026-02-18_1100

### Price Sources Indexed

| # | File | Source Type | Items Used | Items Available | Coverage for DEL-02-03 | Notes |
|---|---|---|---|---|---|---|
| 1 | Structural_Concrete_Rates.csv | Rate Table | 0 | 15 (SC-01 to SC-15) | Not directly used | Structural slab is excluded per cost ownership (DEL-02-04 scope). Floor finish is from IA-08. |
| 2 | Building_Envelope_Rates.csv | Rate Table | 0 | 15 (BE-01 to BE-15) | Not directly used | Envelope scope is DEL-02-04. |
| 3 | Interior_Architectural_Rates.csv | Rate Table | 15 distinct items | 25 (IA-01 to IA-25) | Primary source | Used: IA-04, IA-05, IA-06, IA-07, IA-08, IA-10, IA-12, IA-13, IA-17, IA-22, IA-24, IA-25. Interior fit-up rates for partitions, ceilings, flooring, paint, accessories. |
| 4 | Mechanical_System_Rates.csv | Rate Table | 0 | 14 (MS-01 to MS-14) | Not directly used | Mechanical scope (HVAC, plumbing, sumps) excluded per cost ownership (DEL-02-05). |
| 5 | Electrical_System_Rates.csv | Rate Table | 0 | 14 (ES-01 to ES-14) | Not directly used | Electrical scope excluded per cost ownership (DEL-02-06). |
| 6 | Equipment_Pricing.csv | Rate Table / Allowance | 2 items | 15 (EQ-01 to EQ-15) | Used for equipment | EQ-07 (PW lockers, 40 units); EQ-13 (workshop equipment allowance). |
| 7 | Professional_Design_Fees.csv | Rate Table | 0 | 8 (DF-01 to DF-08) | Not used | Design fees not included at deliverable level; typically rolled up at package or project level. |
| 8 | Construction_Labour_Rates.csv | Rate Table | 0 | 15 (T-01 to T-15) | Not directly used | Labour rates are embedded in the unit rates from other source files (rates are supply-and-install). |
| 9 | Assumed_Project_Parameters.csv | Parameters | 3 items | 29 (PP-01 to PP-29) | Used for quantities | PP-12 (4 PW bays), PP-16 (40 PW lockers), PP-05 (building footprint for area ratios). |

### Source Type Summary

| Type | Count | Notes |
|---|---|---|
| Rate Table | 8 files | Primary basis; supply-and-install unit rates |
| Parameters | 1 file | Area and quantity assumptions |
| Allowance | Contained within Equipment_Pricing.csv | EQ-13 explicitly marked as ALLOWANCE basis |

### Parsing Notes

- All CSV files parsed successfully with consistent column schemas.
- Equipment_Pricing.csv uses `PriceMin/PriceMax/RecommendedPrice` column naming vs `RateMin/RateMax/RecommendedRate` in rate tables; functionally equivalent.
- Construction_Labour_Rates.csv provides hourly rates; these are not directly applied since rate table items include labour in their unit rates (supply-and-install basis).
- Professional_Design_Fees.csv is percentage-based; not applicable at individual deliverable level.
