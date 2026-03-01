# Source Index — EST_DEL-014-03_2026-02-27_0901

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports | Limitations |
|---|---|---|---|---|---|
| PS-1 | Professional_Staff_Rates.csv | PARAMETRIC | 25 roles with hourly CAD rates; MEDIUM confidence | Staff labour pricing for management, design, construction supervision, QA/QC, admin roles | Does not cover trade labour or materials |
| PS-2 | Level_of_Effort.csv | PARAMETRIC | Hours per role per deliverable; 6 rows found for DEL-014-03 | Professional staff hours allocation for DEL-014-03 (PM, CPM, Superintendent, Estimator, QA/QC, HSE) | Trade labour hours not included; management hours only |
| PS-3 | Assumed_Project_Parameters.csv | PARAMETRIC | 19 parameters; project identity, location, facility, schedule, currency | Context parameters (cistern 50,000L, currency CAD, completion Dec 2026, building 13,000 sqft) | Not a pricing source per se; contextual |
| PS-4 | Underground_Utility_Rates.csv | PARAMETRIC / ALLOWANCE | 5 items; water line, sanitary, electrical conduit, septic tank, cistern | Water line rate (UU-01: $130/m recommended); cistern supply+set allowance (UU-05: $65,000) | Cistern allowance is for DEL-014-01, not DEL-014-03; water line rate useful for fill line piping |
| PS-5 | Construction_Labour_Rates.csv | PARAMETRIC | 10 trades; hourly + burden multiplier + fully burdened rate | Plumber (T-05: $92.80/hr burdened), Labourer (T-08: $65.10/hr burdened) | Does not include material costs; labour only |
| PS-6 | Equipment_Pricing.csv | ALLOWANCE | 3 items; cranes, wash bay, air compressor | No direct match for bulk water fill pump | No pump pricing; pump must be estimated parametrically |

## Additional Sources Referenced (from Deliverable Documents)

| # | Source | Type | Notes |
|---|---|---|---|
| DS-1 | Datasheet.md (DEL-014-03) | Engineering document | Attributes, conditions, construction details for quantity takeoff |
| DS-2 | Specification.md (DEL-014-03) | Engineering document | Requirements, verification criteria, standards |
| DS-3 | Guidance.md (DEL-014-03) | Engineering document | Principles, trade-offs, conflict table |
| DS-4 | Procedure.md (DEL-014-03) | Engineering document | Work steps, prerequisites, hold points, verification, records |
| DS-5 | _CONTEXT.md (DEL-014-03) | Context file | Deliverable ID, package, SOW, objectives |
| DS-6 | WDMLRL_Decomposition_Claude.md | Decomposition | WBS traceability — PKG-014, DEL-014-03, SOW-0044 |
