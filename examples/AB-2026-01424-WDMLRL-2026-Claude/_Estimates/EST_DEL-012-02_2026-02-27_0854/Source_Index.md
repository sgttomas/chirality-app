# Source Index — EST_DEL-012-02_2026-02-27_0854

## Price Sources Indexed

| # | Source File | Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | Professional_Staff_Rates.csv | PARAMETRIC rate table | 25 roles with hourly rates (CAD); MEDIUM confidence | Professional staff hourly rates for PM, CPM, Superintendent, QA/QC, HSE, Cost Estimator |
| PS-02 | Level_of_Effort.csv | PARAMETRIC hours model | Per-deliverable hours allocation by role; rows for DEL-012-02 found (6 roles, 38 total hours) | Staff hours allocation for DEL-012-02 |
| PS-03 | Assumed_Project_Parameters.csv | PARAMETRIC reference | 19 parameters including facility dimensions, equipment counts, currency | Building area (~13,000 sqft), ceiling height (35'), cistern volume (50,000 L), currency (CAD) |
| PS-04 | Interior_Architectural_Rates.csv | PARAMETRIC rate table | 5 interior items (partitions, paint, ceilings, flooring, millwork) with min/max/recommended rates | Partition walls (IA-01: $90/m2), paint (IA-02: $12/m2), suspended ceiling (IA-03: $80/m2) |
| PS-05 | Construction_Labour_Rates.csv | PARAMETRIC rate table | 10 trades with hourly + fully burdened rates (CAD); burden multiplier 1.55-1.60 | Labour rates for Carpenter (T-01: $80.60/hr), Concrete Finisher (T-02: $77.50/hr), Drywaller (T-10: $71.30/hr), Painter (T-09: $69.75/hr), Ironworker (T-03: $92.80/hr), Plumber (T-05: $92.80/hr), Electrician (T-04: $96.00/hr), Labourer (T-08: $65.10/hr) |

## Source Gaps

- No explicit quote or rate table for industrial access doors (ITEM-005). Priced parametrically.
- No explicit rate for fire-rated wall assembly upgrade (ITEM-007). Priced as parametric allowance.
- No explicit rate for equipment platforms/mounting (ITEM-008). Priced as parametric allowance based on materials + labour.
- No explicit rate for cistern structural pad (ITEM-009). Priced as parametric allowance.
- No explicit rate for penetration fire-stopping per unit (ITEM-013). Priced parametrically from labour rates.
- No explicit rate for mezzanine stair interface (ITEM-010). Priced as parametric allowance.
