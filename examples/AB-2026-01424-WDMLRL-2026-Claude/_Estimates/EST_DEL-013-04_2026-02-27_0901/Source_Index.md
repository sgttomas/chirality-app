# Source Index — EST_DEL-013-04_2026-02-27_0901

## Pricing Sources Indexed

| Source File | Source Type | Parsing Notes | Supports | Limitations |
|---|---|---|---|---|
| Professional_Staff_Rates.csv | RATE_TABLE | 25 roles; CAD hourly rates; PARAMETRIC basis | Professional staff labour costing (PM, superintendent, QA/QC, HSE, commissioning agent) | Does not cover construction trade labour |
| Level_of_Effort.csv | PARAMETRIC | ~600+ rows; hours by deliverable x role | DEL-013-04 has 6 role allocations (R-01, R-02, R-03, R-05, R-06, R-08) | Hours are parametric estimates; no construction trade hours included |
| Assumed_Project_Parameters.csv | REFERENCE | 19 parameters; project identity, facility dimensions, equipment | Building area (13,000 sqft), ceiling height (35 ft), crane qty/capacity, currency (CAD) | Does not contain pricing data directly |
| Mechanical_System_Rates.csv | ALLOWANCE / PARAMETRIC | 6 items; mechanical equipment and ductwork rates | MS-04 (vehicle exhaust hose + fan system @ 9,500/EA); MS-06 (ductwork @ 60 CAD/m2) | LOW confidence; rates are allowances; sizing TBD |
| Construction_Labour_Rates.csv | PARAMETRIC | 10 trades; hourly + burdened rates | T-06 (HVAC Sheet Metal @ 91.2/hr burdened); T-08 (Labourer @ 65.1/hr burdened) | Labour hours are parametric (not from detailed task scheduling) |
| Equipment_Pricing.csv | ALLOWANCE | 3 items; major equipment | No items directly applicable to DEL-013-04 exhaust system | Cranes and shop equipment only; exhaust equipment covered by Mechanical_System_Rates.csv |

## Engineering Documents Read

| Document | Deliverable | Status | Notes |
|---|---|---|---|
| _CONTEXT.md | DEL-013-04 | Read | Deliverable identity, scope, key requirements |
| Datasheet.md | DEL-013-04 | Read | Attributes, TBD register (5 TBDs), construction elements, conditions |
| Specification.md | DEL-013-04 | Read | 18 requirements (REQ-001 through REQ-018); standards; verification; documentation |
| Guidance.md | DEL-013-04 | Read | 6 principles; 10 considerations; 4 trade-offs; 5 conflict items |
| Procedure.md | DEL-013-04 | Read | 17 steps across 3 phases + regulatory hold points; 12 records |

## Decomposition Reference

| Document | Status | Notes |
|---|---|---|
| WDMLRL_Decomposition_Claude.md | Read | DEL-013-04 in PKG-013; SOW-0038; Mechanical Contractor; Installation type |
