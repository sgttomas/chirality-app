# Source Index

**RunID:** EST_DEL-012-01_2026-02-27_0901

## Pricing Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| S-01 | Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 roles with hourly rates in CAD; basis=PARAMETRIC; confidence=MEDIUM | Professional/management staff hourly rates (R-01 through R-25) |
| S-02 | Level_of_Effort.csv | PARAMETRIC (hours allocation) | Per-deliverable role-hour allocations; 6 rows for DEL-012-01 (R-01, R-02, R-03, R-05, R-06, R-08) | Hours quantities for professional staff on DEL-012-01 |
| S-03 | Assumed_Project_Parameters.csv | PARAMETRIC (parameters) | 18 project parameters including facility area (~13,000 sqft), ceiling height (35 ft), currency (CAD) | Context parameters; no direct pricing; used for area/dimension validation |
| S-04 | Interior_Architectural_Rates.csv | PARAMETRIC (unit rates) | 5 items: partitions (IA-01), paint (IA-02), ceilings (IA-03), flooring (IA-04), millwork (IA-05) | Partition rate (IA-01: $90/m2), paint rate (IA-02: $12/m2) |
| S-05 | Construction_Labour_Rates.csv | PARAMETRIC (labour rates) | 10 trades with base rate, burden multiplier, and fully-burdened rate in CAD | Trade labour: carpenter (T-01: $80.60/hr), drywaller (T-10: $71.30/hr), painter (T-09: $69.75/hr), labourer (T-08: $65.10/hr) |

## Additional Sources Referenced (not in PRICE_SOURCES but used for context/scaling)

| # | Source File | Source Type | Usage |
|---|---|---|---|
| S-06 | Building_Envelope_Rates.csv | PARAMETRIC/ALLOWANCE | BE-03 (24-ft overhead door @ $19,000) used as scaling basis for 6-ft roll-up door parametric derivation |

## Sources Not Used

| Source | Reason |
|---|---|
| Equipment_Pricing.csv | No equipment items in DEL-012-01 scope |
| Electrical_System_Rates.csv | Electrical scope excluded (PKG-015) |
| Mechanical_System_Rates.csv | Mechanical scope excluded (PKG-013) |
| Structural_Concrete_Rates.csv | Foundation/structure excluded (PKG-010/011) |
| All other PriceSources CSVs | Not within DEL-012-01 scope boundary |
