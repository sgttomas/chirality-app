# Source Index — EST_DEL-013-03_2026-02-27_0901

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports | Gaps / Limitations |
|---|---|---|---|---|---|
| PS-01 | Professional_Staff_Rates.csv | Rate Table | 25 roles; RoleID/HourlyRate_CAD; all PARAMETRIC basis | Professional staff hourly rates for management line items (ITM-022) | No trade labour rates; no overtime/premium rates |
| PS-02 | Level_of_Effort.csv | Parametric Model | Multi-deliverable LOE; filtered to DEL-013-03 rows; 6 role allocations found | Hour allocations for PM, CPM, Superintendent, Estimator, QA/QC, HSE | No field trade hours (sheet metal, gas fitter, electrician); management only |
| PS-03 | Assumed_Project_Parameters.csv | Parameter Table | 18 parameters; PP-10 floor area (13,000 sqft), PP-16 MUA required=Yes | Building parameters for parametric scaling (floor area -> ductwork qty) | No MUA-specific parameters (airflow, heating capacity) |
| PS-04 | Mechanical_System_Rates.csv | Rate Table | 6 items; MS-02 MUA installed, MS-06 ductwork per m2 | MUA unit installed cost (MS-02: 28,000-65,000 CAD); ductwork rate (MS-06: 40-85/m2) | ALLOWANCE/LOW confidence on MS-02; sizing TBD; no breakout of dampers, controls, insulation, fire dampers |
| PS-05 | Construction_Labour_Rates.csv | Rate Table | 10 trades; T-06 HVAC Sheet Metal at $91.20/hr burdened | Trade labour rates for field installation hours | No LOE hours for trades on this deliverable in Level_of_Effort.csv |
| PS-06 | Equipment_Pricing.csv | Rate Table | 3 items (cranes, wash bay, air compressor) | Not directly applicable to DEL-013-03 | No MUA equipment line; MUA covered by MS-02 in Mechanical_System_Rates.csv |

## Deliverable Documents Read

| Document | Path | Items Extracted |
|---|---|---|
| _CONTEXT.md | PKG-013.../DEL-013-03_Makeup-Air/_CONTEXT.md | Deliverable identity, scope boundaries, related deliverables |
| Datasheet.md | PKG-013.../DEL-013-03_Makeup-Air/Datasheet.md | Equipment attributes, ductwork scope, conditions, construction elements |
| Specification.md | PKG-013.../DEL-013-03_Makeup-Air/Specification.md | 19 requirements (REQ-013-03-01 through -19), verification methods, documentation artifacts |
| Guidance.md | PKG-013.../DEL-013-03_Makeup-Air/Guidance.md | 5 principles, 8 considerations, 3 trade-offs, 1 conflict |
| Procedure.md | PKG-013.../DEL-013-03_Makeup-Air/Procedure.md | 6 phases, 12 prerequisites, ~25 work steps, verification table, records table |

## Decomposition Reference

| Document | Path | Data Used |
|---|---|---|
| WDMLRL_Decomposition_Claude.md | {RUN_ROOT}/_Decomposition/ | PKG-013 identity, DEL-013-03 confirmed (SOW-0037), OBJ-001/OBJ-004 linkage |
