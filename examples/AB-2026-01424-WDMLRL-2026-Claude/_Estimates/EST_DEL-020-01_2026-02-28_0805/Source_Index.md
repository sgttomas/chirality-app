# Source Index — EST_DEL-020-01_2026-02-28_0805

## Indexed Price Sources

| Source # | File Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | PriceSources/Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 roles with hourly rates in CAD; all marked PARAMETRIC basis with MEDIUM confidence | Provides unit rates ($/hr) for all professional staff roles referenced in Level_of_Effort.csv |
| PS-02 | PriceSources/Level_of_Effort.csv | PARAMETRIC (level of effort) | Multi-deliverable CSV; 8 rows found for DEL-020-01 (Building Systems Commissioning) covering roles R-01, R-02, R-03, R-05, R-06, R-08, R-09, R-23 | Provides estimated hours per role for DEL-020-01; basis for quantity (hours) in parametric costing |
| PS-03 | PriceSources/Assumed_Project_Parameters.csv | PARAMETRIC (parameters) | 19 parameters covering identity, location, contract, schedule, facility, equipment, plumbing, mechanical, currency, economics | Provides project context parameters (building area, crane count, cistern volume, etc.); supports validation of scope but does not directly price line items |
| PS-04 | PriceSources/Optional_Items_Pricing.csv | ALLOWANCE | 2 optional items (winter conditions, contaminated soils); neither directly applicable to DEL-020-01 commissioning scope | Does not support DEL-020-01 pricing directly; noted for completeness |
| PS-05 | PriceSources/Fees_Permits_Insurance.csv | PARAMETRIC (fee schedule) | 12 items covering bonding, insurance, permits, inspection, and regulatory fees; FP-09 and FP-10 used for DEL-020-01 | Provides parametric rates for crane load testing (FP-09, $6,000) and Safety Code inspection coordination (FP-10, $3,500) |

## Coverage Assessment

- **Professional staff labour (ITM-020-01-001 through ITM-020-01-008):** Fully supported by PS-01 (rates) + PS-02 (hours). All 8 roles have matching rate and hour entries.
- **Activity-based lump sums (ITM-020-01-009 through ITM-020-01-017):** Labour component covered by the professional staff hours above. No separate material, equipment, or third-party fee pricing required for these items. Priced PARAMETRIC based on the labour model.
- **Third-party inspection fees (ITM-020-01-011, ITM-020-01-018):** Now supported by PS-05 (Fees_Permits_Insurance.csv). FP-09 provides crane load testing rate; FP-10 provides Safety Code inspection coordination rate. Both LOW confidence.
- **TBD items remaining:** 0 (resolved from 2 in prior snapshot).
