# Source Index — EST_DEL-015-05_2026-02-27_0848

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | Professional_Staff_Rates.csv | RATE_TABLE | 25 rows; RoleID R-01 through R-25; HourlyRate_CAD column; Basis=PARAMETRIC for all | Professional staff hourly rates for management, design, and specialty roles |
| PS-02 | Level_of_Effort.csv | PARAMETRIC | Multi-deliverable LoE table; filtered to DEL-015-05 rows (6 rows: R-01, R-02, R-03, R-05, R-06, R-08) | Estimated hours per role for DEL-015-05 |
| PS-03 | Assumed_Project_Parameters.csv | REFERENCE | 19 rows; project identity, location, facility dimensions, equipment, and currency parameters | Building area (~13,000 sqft), ceiling height (35 ft), currency (CAD) |
| PS-04 | Electrical_System_Rates.csv | RATE_TABLE | 6 rows (ES-01 through ES-06); RecommendedRate column; mix of PARAMETRIC and ALLOWANCE basis | ES-05 directly applicable (security camera rough-in $280/ea); ES-06 (motor connection) not applicable to this deliverable |
| PS-05 | Underground_Utility_Rates.csv | RATE_TABLE | 5 rows (UU-01 through UU-05); RecommendedRate column | Not directly applicable to DEL-015-05 (underground utility rates); reviewed but no items matched |
| PS-06 | Construction_Labour_Rates.csv | RATE_TABLE | 10 rows (T-01 through T-10); FullyBurdenedRate_CAD column | T-04 Electrician ($96.00/hr) directly applicable for installation labour |

## Source Coverage Assessment

- **Directly supported items:** Security camera rough-in rate (ES-05), electrician labour rate (T-04), professional staff rates (PS-01 + PS-02)
- **Parametrically derived items:** Conduit supply/install rates, cable material costs, junction box/fitting costs, inspection allowance, closeout documentation -- derived from labour rates and parametric material estimates
- **Not supported (TBD in sources):** Exact quantities for camera locations, antenna locations, conduit runs, cable lengths -- all pending DEL-004-07 IFC drawings
- **Underground_Utility_Rates.csv:** Reviewed; no items in DEL-015-05 scope match underground utility categories (water, sanitary, underground conduit). DEL-015-05 is interior low-voltage wiring.
