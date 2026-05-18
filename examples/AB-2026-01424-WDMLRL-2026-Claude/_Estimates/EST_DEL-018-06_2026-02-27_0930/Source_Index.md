# Source Index — EST_DEL-018-06_2026-02-27_0930

## Indexed Price Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|-----------|------------|---------------|----------|
| 1 | Professional_Staff_Rates.csv | RATE_TABLE | 25 roles with hourly rates in CAD; Basis = PARAMETRIC; Confidence = MEDIUM | Professional staff hourly rates for Items ITM-001 through ITM-006 |
| 2 | Level_of_Effort.csv | PARAMETRIC | Deliverable-by-role hour allocations; DEL-018-06 has 6 rows (R-01, R-02, R-03, R-05, R-06, R-08) | Hour quantities for professional staff items |
| 3 | Assumed_Project_Parameters.csv | REFERENCE | 18 project parameters (identity, location, schedule, facility, economics) | Context parameters — currency (CAD), project identity, site location |
| 4 | Earthwork_Civil_Rates.csv | RATE_TABLE | 4 items (EC-01 through EC-04); unit rates for excavation, fill, compaction, topsoil | Supports trench excavation and backfill pricing (ITM-010, ITM-014) |
| 5 | Paving_Surfacing_Rates.csv | RATE_TABLE | 4 items (PS-01 through PS-04); surfacing rates | Not directly applicable to DEL-018-06 utility tie-ins |
| 6 | Underground_Utility_Rates.csv | RATE_TABLE | 5 items (UU-01 through UU-05); underground utility installation rates including water line, sanitary line, electrical conduit, septic tank, cistern | Supports electrical conduit (UU-03) pricing; gas piping derived parametrically; communications conduit derived parametrically |
| 7 | Construction_Labour_Rates.csv | RATE_TABLE | 10 trades with hourly base + burden multiplier + fully burdened rates | Supports trade labour pricing for plumber (T-05), electrician (T-04), equipment operator (T-07), labourer (T-08) |

## Source Coverage Assessment

- **Well-supported items**: Professional staff hours (fully supported by Level_of_Effort.csv + Professional_Staff_Rates.csv); trade labour rates (fully supported by Construction_Labour_Rates.csv); underground electrical conduit (UU-03); earthwork rates for trenching.
- **Partially supported items**: Gas piping (no direct rate in Underground_Utility_Rates.csv — water line rate UU-01 used as parametric proxy); communication conduit (no direct rate — electrical conduit UU-03 used as proxy with adjustment).
- **Unsupported / TBD items**: Trench distance (assumed 75m — TBD); gas service connection fee; electrical service connection fee; transformer cost (if customer-owned); gas main extension cost (if required).
- **Not applicable**: Paving_Surfacing_Rates.csv has no direct bearing on utility tie-in scope.
