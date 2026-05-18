# Source Index — EST_DEL-014-04_2026-02-27_1130

## Pricing Sources Indexed

| Source File | Source Type | Coverage | Parsing Notes |
|---|---|---|---|
| `Professional_Staff_Rates.csv` | Rate Table | Professional staff hourly rates (R-01 through R-25); used for PM, Construction PM, Site Superintendent, Cost Estimator, QA/QC Lead, HSE Manager allocations | CSV; 25 rows; all rates in CAD/hr |
| `Level_of_Effort.csv` | Rate Table | Hours allocation per deliverable per role; DEL-014-04 has 6 rows (R-01: 6hr, R-02: 8hr, R-03: 10hr, R-08: 4hr, R-06: 6hr, R-05: 4hr) | CSV; filtered to DEL-014-04 rows |
| `Assumed_Project_Parameters.csv` | Parametric Parameters | Project parameters including facility type, floor area (~13,000 sqft), ceiling height (35 ft), currency (CAD) | CSV; 19 parameters; used for context and validation |
| `Underground_Utility_Rates.csv` | Rate Table | Underground utility installation rates; UU-02 Sanitary line at $160/m recommended rate used for drain piping | CSV; 5 items; sanitary line rate directly applicable |
| `Construction_Labour_Rates.csv` | Rate Table | Trade labour rates; T-05 Plumber at $92.80/hr fully burdened, T-08 Labourer at $65.10/hr fully burdened | CSV; 10 trades; plumber and labourer rates directly applicable |
| `Equipment_Pricing.csv` | Rate Table | Equipment allowances (cranes, pressure washer, compressor) | CSV; 3 items; no items directly applicable to floor drain scope |

## Coverage Gaps

| Gap | Impact | Mitigation |
|---|---|---|
| No drain body/grate unit pricing in any PRICE_SOURCE | Material costs for drain bodies, grates, traps, and trap primers must be parametrically estimated | Used PARAMETRIC method with Alberta industrial construction benchmarks; confidence LOW |
| No above-ground vent piping rate | Above-grade vent piping rate not in Underground_Utility_Rates.csv | Used PARAMETRIC estimate at $95/m; confidence LOW |
| No plumbing permit fee schedule | Permit and inspection fees not in PRICE_SOURCES | Used PARAMETRIC lump sum of $1,800; confidence LOW |
| No coordination/submittal cost rate | Submittal preparation and multi-contractor coordination cost not in PRICE_SOURCES | Used PARAMETRIC lump sum of $1,500; confidence LOW |
