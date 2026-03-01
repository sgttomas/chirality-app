# Source_Index — EST_DEL-018-03_2026-02-27_0834

## Pricing Sources Indexed

| # | Source File | Source Type | What It Supports | What It Cannot Support | Parsing Notes |
|---|------------|-------------|------------------|----------------------|---------------|
| 1 | Professional_Staff_Rates.csv | Rate table | Professional/management hourly rates (R-01 through R-25) for PM, superintendent, QA/QC, HSE, estimator, surveyor, document control | Does not provide hours; hours come from Level_of_Effort.csv | 25 roles; all rates in CAD; basis PARAMETRIC; confidence MEDIUM |
| 2 | Level_of_Effort.csv | Parametric model | Estimated hours by role for each deliverable; DEL-018-03 has 6 role entries (R-01, R-02, R-03, R-05, R-06, R-08) | Does not provide rates; paired with Professional_Staff_Rates.csv | Rows 467-472 for DEL-018-03; 38 total hours |
| 3 | Assumed_Project_Parameters.csv | Reference parameters | Project identity, location, facility dimensions, equipment counts, currency | Not a pricing source; provides context for parametric assumptions | 18 parameters; used for area estimation and context |
| 4 | Earthwork_Civil_Rates.csv | Rate table | Common excavation, imported fill, compaction/proof-roll, topsoil stripping | Limited to 4 line items; no drainage or underground rates | EC-01 through EC-04; all in CAD; basis PARAMETRIC |
| 5 | Paving_Surfacing_Rates.csv | Rate table | Gravel driving surface, asphalt paving, concrete apron, curb and gutter | Only 4 line items; no specialty surfacing | PS-01 through PS-04; all in CAD; basis PARAMETRIC |
| 6 | Underground_Utility_Rates.csv | Rate table | Water line, sanitary line, underground conduit, septic tank, cistern | Not directly applicable to DEL-018-03 (driving surface); no utility tie-in work in this deliverable | UU-01 through UU-05; included for completeness |
| 7 | Construction_Labour_Rates.csv | Rate table | Trade labour rates — carpenter, concrete finisher, ironworker, electrician, plumber, HVAC, equipment operator, labourer, painter, drywaller | Fully burdened rates available; 10 trades | T-01 through T-10; burden multiplier 1.55-1.60; all in CAD |

## Source Applicability to DEL-018-03

**Directly applicable:**
- Professional_Staff_Rates.csv + Level_of_Effort.csv: professional/management staff costs (6 roles, 38 total hours)
- Paving_Surfacing_Rates.csv: PS-01 (gravel driving surface) is the primary construction rate
- Earthwork_Civil_Rates.csv: EC-03 (compaction/proof-roll) applicable to subgrade and gravel compaction
- Construction_Labour_Rates.csv: T-07 (Equipment Operator) and T-08 (Labourer) for construction labour

**Not directly applicable:**
- Underground_Utility_Rates.csv: no underground utility work in DEL-018-03
- Assumed_Project_Parameters.csv: context only (used for area estimation)

## Key Gap

The driving surface area (2,400 m2) is a parametric assumption. The actual area will be determined by the civil design (DEL-005-04). This is the single largest quantity uncertainty in this estimate.
