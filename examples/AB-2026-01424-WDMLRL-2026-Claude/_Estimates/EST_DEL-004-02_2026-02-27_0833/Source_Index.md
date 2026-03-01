# Source Index — EST_DEL-004-02_2026-02-27_0833

## Pricing Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 roles with hourly rates in CAD; Basis=PARAMETRIC; Confidence=MEDIUM for all entries | Hourly rate lookup for all staff roles (R-01 through R-25) |
| PS-02 | Level_of_Effort.csv | PARAMETRIC (hours model) | Estimated hours by DeliverableID and RoleID; DEL-004-02 has 4 role entries (R-01, R-08, R-13, R-16) totalling 130 hours | Hour quantities for DEL-004-02 priceable labor items |
| PS-03 | Assumed_Project_Parameters.csv | PARAMETRIC (context) | 19 project parameters (identity, location, contract, facility, equipment, currency); provides context for parametric model validation | Context/validation — building area (~13,000 sqft), two 5-tonne cranes, 35' ceiling, CAD currency |
| PS-04 | Professional_Design_Fees.csv | PARAMETRIC (fee model) | 5 discipline fee percentages as % of construction value; Electrical=1.0-2.2% (recommended 1.6%) | Alternative fee-based pricing model — not used as primary method; LOE method preferred for this deliverable |

## Source Coverage Assessment

- **Primary pricing method:** PARAMETRIC via Level_of_Effort.csv (hours) x Professional_Staff_Rates.csv (rates)
- **All 4 LOE line items for DEL-004-02 are matched** to rate entries in Professional_Staff_Rates.csv
- **Professional_Design_Fees.csv not used** as primary method for this deliverable; LOE-based pricing is more granular and preferred when available
- **No gaps in pricing source coverage** for this deliverable's labor scope

## Source Limitations

- All rates carry Confidence=MEDIUM (parametric basis, not firm quotes)
- Level of effort estimates are parametric — not validated against historical actuals for this specific project
- Professional_Design_Fees.csv provides a cross-check opportunity: at a $2.5M construction value (ASSUMPTION), 1.6% electrical design fee = $40,000 for all electrical design deliverables in PKG-004; DEL-004-02 at $18,810 appears proportionally reasonable for one of 9 deliverables in PKG-004
