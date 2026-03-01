# Source Index — EST_DEL-018-05_2026-02-27_0855

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|-----------|-------------|---------------|----------|
| 1 | Professional_Staff_Rates.csv | RATE_TABLE | 25 roles; HourlyRate_CAD; all PARAMETRIC basis, MEDIUM confidence | Professional staff hourly rates for PM, CPM, Superintendent, QA/QC, HSE, Estimator |
| 2 | Level_of_Effort.csv | PARAMETRIC | Rows for DEL-018-05: R-01 (PM, 6h), R-02 (CPM, 8h), R-03 (Superintendent, 10h), R-08 (Estimator, 4h), R-06 (QA/QC, 6h), R-05 (HSE, 4h) | Staff hours allocation for DEL-018-05; total 38 professional hours |
| 3 | Assumed_Project_Parameters.csv | PARAMETRIC | 18 parameters; project identity, location, facility, equipment, currency | Confirms CAD currency (PP-17), site location (PP-03/PP-04), wash bay context |
| 4 | Earthwork_Civil_Rates.csv | RATE_TABLE | 4 items: excavation (EC-01), granular fill (EC-02), compaction (EC-03), topsoil strip (EC-04) | Sump excavation, bedding, trench excavation, backfill, compaction |
| 5 | Paving_Surfacing_Rates.csv | RATE_TABLE | 4 items: gravel surface (PS-01), asphalt (PS-02), concrete apron (PS-03), curb/gutter (PS-04) | Local grading not directly matched; used for reference only |
| 6 | Underground_Utility_Rates.csv | RATE_TABLE | 5 items: water line (UU-01), sanitary line (UU-02), conduit (UU-03), septic tank (UU-04), cistern (UU-05) | Drainage pipe (UU-02 sanitary line rate used as parametric proxy for drainage pipe) |
| 7 | Construction_Labour_Rates.csv | RATE_TABLE | 10 trades; HourlyRate + BurdenMultiplier + FullyBurdenedRate_CAD | Equipment Operator (T-07), Concrete Finisher (T-02), Plumber (T-05), Labourer (T-08) |

## Source Gaps

- No rate table entry for precast concrete sump structure (supply + set). PARAMETRIC estimate used based on UU-04 (septic tank) as a proxy, adjusted upward for larger sump.
- No rate table entry for floor drain (supply + install). PARAMETRIC estimate used.
- No rate table entry for cold-weather construction measures. ALLOWANCE used.
- No rate table entry for environmental regulatory scoping. ALLOWANCE used.
- No rate table entry for as-built survey. PARAMETRIC estimate based on staff rates.
