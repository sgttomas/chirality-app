# Source Index — EST_DEL-015-04_2026-02-27_0834

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | `Professional_Staff_Rates.csv` | RATE_TABLE | 25 roles with hourly rates in CAD; all marked PARAMETRIC basis, MEDIUM confidence | Professional staff labour costs (PM, CPM, Superintendent, QA/QC, HSE, Estimator) |
| PS-02 | `Level_of_Effort.csv` | PARAMETRIC | Hours by role per deliverable; DEL-015-04 has 6 entries (R-01, R-02, R-03, R-08, R-06, R-05) totalling 38 hours | Professional staff hour allocations for DEL-015-04 |
| PS-03 | `Assumed_Project_Parameters.csv` | REFERENCE | 19 project parameters; confirms building area ~13,000 sqft, 35 ft ceiling, 2 cranes, CAD currency | Building parameters for parametric sizing of conduit runs and labour hours |
| PS-04 | `Electrical_System_Rates.csv` | RATE_TABLE | 6 electrical items (ES-01 through ES-06); includes motor connection allowance (ES-06: $1,150/EA), panelboard (ES-02: $4,800/EA) | Motor connection pricing for equipment circuits; panelboard reference |
| PS-05 | `Underground_Utility_Rates.csv` | RATE_TABLE | 5 items (UU-01 through UU-05); includes underground conduit rate (UU-03: $95/m) | Underground conduit rate reference for conduit pricing |
| PS-06 | `Construction_Labour_Rates.csv` | RATE_TABLE | 10 trades; Electrician (T-04) at $96.00/hr fully burdened; Labourer (T-08) at $65.10/hr fully burdened | Construction labour costs for installation activities |

## Source Coverage Assessment

- **Well-covered:** Professional staff hours and rates (PS-01 + PS-02); electrician and labourer labour rates (PS-06); motor connection allowance (PS-04).
- **Partially covered:** Conduit/raceway pricing uses underground utility rate (PS-05 UU-03) as a proxy for above-ground industrial conduit; actual above-ground rates are not separately provided.
- **Not covered:** Crane runway power supply system (conductor bar, festoon cable) material costs; circuit breaker unit costs; motor disconnect unit costs; conductor wire material costs; grounding/bonding material costs. These are priced via PARAMETRIC method using industry benchmarks.

## Engineering Documents Read

| Document | Status | Items Extracted |
|---|---|---|
| `Datasheet.md` | Present | 7 equipment circuits (C-01 through C-07); conditions; materials (TBD) |
| `Specification.md` | Present | 13 requirements (REQ-015-04-001 through -013); scope inclusions/exclusions |
| `Guidance.md` | Present | Design principles; trade-offs; sequencing guidance |
| `Procedure.md` | Present | 7 phases; prerequisites; verification checks; records |
