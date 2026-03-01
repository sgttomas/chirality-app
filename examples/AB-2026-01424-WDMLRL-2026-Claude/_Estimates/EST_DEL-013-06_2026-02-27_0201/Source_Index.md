# Source Index — EST_DEL-013-06_2026-02-27_0201

## Pricing Sources Indexed

| Source File | Source Type | Coverage | Parsing Notes |
|---|---|---|---|
| Professional_Staff_Rates.csv | Rate Table | Hourly rates for all professional/management roles (R-01 through R-25) | CSV; 25 roles; all CAD; PARAMETRIC basis; MEDIUM confidence |
| Level_of_Effort.csv | Parametric Model | Estimated hours by role for each deliverable | CSV; DEL-013-06 has 6 rows (PM, CPM, Site Super, Estimator, QA/QC, HSE); total 38 hrs |
| Assumed_Project_Parameters.csv | Reference Data | Project identity, location, facility parameters (ceiling height, floor area, cranes) | CSV; 19 parameters; confirms 35 ft ceiling, 13,000 sqft, 2x 5-ton cranes, CAD currency |
| Mechanical_System_Rates.csv | Rate Table (Allowance) | Mechanical system installed rates (heating, ventilation, exhaust, ductwork) | CSV; 6 items; NO ceiling fan line item present — gap |
| Construction_Labour_Rates.csv | Rate Table | Fully burdened hourly rates for construction trades | CSV; 10 trades; used T-04 Electrician ($96.00/hr) and T-06 HVAC Sheet Metal ($91.20/hr) |
| Equipment_Pricing.csv | Allowance Table | Major equipment pricing (cranes, wash bay, air compressor) | CSV; 3 items; NO ceiling fan line item present — gap |

## Coverage Gaps

| Gap | Impact | Mitigation |
|---|---|---|
| No ceiling fan unit price in any PRICE_SOURCE | ITEM-01 (fan supply) priced parametrically without quote/rate table evidence | PARAMETRIC estimate at $5,500/unit based on HVLS industry pricing; Confidence LOW |
| No mounting hardware pricing | ITEM-02 priced parametrically | PARAMETRIC estimate at $1,100/unit; Confidence LOW |
| No speed controller pricing | ITEM-05 priced parametrically | PARAMETRIC estimate at $475/unit; Confidence LOW |
| No permit fee schedule | ITEM-10 priced parametrically | PARAMETRIC estimate at $1,000 total; Confidence LOW |
| No scaffolding/lift rental rates | ITEM-12 priced parametrically | PARAMETRIC estimate at $2,500; Confidence LOW |

## Deliverable Documents Read

| Document | Path | Status |
|---|---|---|
| _CONTEXT.md | PKG-013_.../DEL-013-06_Ceiling-Fans/_CONTEXT.md | Read successfully |
| Datasheet.md | PKG-013_.../DEL-013-06_Ceiling-Fans/Datasheet.md | Read successfully |
| Specification.md | PKG-013_.../DEL-013-06_Ceiling-Fans/Specification.md | Read successfully |
| Guidance.md | PKG-013_.../DEL-013-06_Ceiling-Fans/Guidance.md | Read successfully |
| Procedure.md | PKG-013_.../DEL-013-06_Ceiling-Fans/Procedure.md | Read successfully |
| Decomposition | _Decomposition/WDMLRL_Decomposition_Claude.md | Read successfully; DEL-013-06 confirmed in PKG-013, SOW-0040 |
