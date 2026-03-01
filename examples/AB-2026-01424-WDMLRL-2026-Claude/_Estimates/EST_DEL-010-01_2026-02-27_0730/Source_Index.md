# Source Index — EST_DEL-010-01_2026-02-27_0730

## Indexed Price Sources

| # | Source File | Source Type | Items Supported | Parsing Notes |
|---|---|---|---|---|
| PS-01 | Professional_Staff_Rates.csv | RATE_TABLE | ITM-021 through ITM-026 (professional staff hourly rates) | 25 roles with CAD hourly rates; directly applicable to LOE-based professional staff line items |
| PS-02 | Level_of_Effort.csv | PARAMETRIC | ITM-021 through ITM-026 (professional staff hours) | Provides estimated hours per deliverable per role; DEL-010-01 has 6 role entries (R-01, R-02, R-03, R-05, R-06, R-08) |
| PS-03 | Assumed_Project_Parameters.csv | PARAMETRIC | All items (provides building dimensions and attributes for quantity derivation) | 19 parameters; key parameters: PP-10 (floor area ~13000 sqft), PP-11 (ceiling height 35 ft), PP-12/PP-13 (cranes), PP-17 (CAD currency) |
| PS-04 | Structural_Concrete_Rates.csv | RATE_TABLE | ITM-005 through ITM-010, ITM-020 (concrete, rebar, formwork, embedments) | 8 items with CAD unit rates (min/max/recommended); PARAMETRIC basis with MEDIUM confidence |
| PS-05 | Earthwork_Civil_Rates.csv | RATE_TABLE | ITM-001 through ITM-004, ITM-011 (earthwork activities) | 4 items with CAD unit rates; PARAMETRIC basis with MEDIUM confidence |
| PS-06 | Construction_Labour_Rates.csv | RATE_TABLE | ITM-027 through ITM-031 (construction trade labour) | 10 trades with hourly and fully-burdened rates in CAD; burden multiplier 1.55-1.60 |

## Source Coverage Summary

- **Professional staff (6 items):** Fully supported by PS-01 + PS-02 (rates and hours from price sources)
- **Earthwork/civil (5 items):** Rates supported by PS-05; quantities derived parametrically from PS-03 parameters
- **Structural concrete (6 items):** Rates supported by PS-04; quantities derived parametrically from PS-03 parameters
- **Construction labour (5 items):** Rates supported by PS-06; hours estimated parametrically from scope
- **Lump-sum allowances (8 items):** Testing, documentation, inspections, and embedded items priced as PARAMETRIC allowances; no direct quote or rate table support

## Limitations

- No direct quotes available for any items (this is a PARAMETRIC estimate, not a QUOTE-based estimate)
- All earthwork and concrete quantities are derived from assumed building footprint dimensions; foundation type is TBD pending geotech
- Lump-sum items for testing, inspection, and documentation are parametric allowances based on professional judgment
- Aggregate supply is by County (out of Proponent scope) but placement cost is included
