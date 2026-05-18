# Source Index — EST_DEL-011-07_2026-02-27_0955

## Pricing Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | PriceSources/Professional_Staff_Rates.csv | RATE_TABLE | 25 roles; HourlyRate_CAD column; all PARAMETRIC basis, MEDIUM confidence | Professional services line items (DL-011 through DL-016). Provides hourly rates for PM, CPM, Superintendent, Estimator, QA/QC Lead, HSE Manager. |
| PS-02 | PriceSources/Level_of_Effort.csv | PARAMETRIC | Multi-deliverable LOE table; filtered to DEL-011-07 rows (6 rows). Columns: RoleID, EstimatedHours, Basis | Hour quantities for professional staff roles on DEL-011-07. 6 roles x hours: R-01(6), R-02(8), R-03(10), R-05(4), R-06(6), R-08(4). |
| PS-03 | PriceSources/Assumed_Project_Parameters.csv | PARAMETRIC | 19 parameters; project identity, facility dimensions, equipment, currency | Mezzanine context: building area ~13,000 sqft (PP-10), ceiling height 35 ft (PP-11), currency CAD (PP-17). Does not directly price items. |
| PS-04 | PriceSources/Structural_Concrete_Rates.csv | PARAMETRIC | 8 items; unit rates with Min/Max/Recommended; PARAMETRIC basis, MEDIUM confidence (SC-08 LOW) | SC-01 (slab-on-grade rate) used as basis for concrete topping rate derivation. SC-03 (concrete /m3) used for concrete supply. SC-04 (rebar /kg) used for reinforcing steel. SC-07 (concrete stairs) used as parametric for stair system. |
| PS-05 | PriceSources/Building_Envelope_Rates.csv | RATE_TABLE | 6 items; wall panels, roof, doors, glazing | Not directly applicable to DEL-011-07 (mezzanine is interior structural, not envelope). Not used. |
| PS-06 | PriceSources/Construction_Labour_Rates.csv | RATE_TABLE | 10 trades; FullyBurdenedRate_CAD with BurdenMultiplier; PARAMETRIC basis, MEDIUM confidence | T-02 (Concrete Finisher $77.50/hr) for DL-007. T-03 (Ironworker $92.80/hr) for DL-006. T-08 (Labourer $65.10/hr) for DL-008. |
| PS-07 | PriceSources/Equipment_Pricing.csv | ALLOWANCE | 3 items; cranes, wash bay, compressor; LOW confidence | Not directly applicable to DEL-011-07 (overhead cranes are separate scope; mezzanine does not include equipment). Not used. |

## Deliverable Documents Read

| Document | Status | Items Extracted |
|---|---|---|
| _CONTEXT.md | Read | Deliverable ID, name, package, discipline, type, anticipated artifacts |
| Datasheet.md | Read | Mezzanine attributes (location, function, area, structural system, deck type, stair config, guardrails, elevation) |
| Specification.md | Read | 10 requirements (R-01 through R-10); verification matrix; standards table |
| Guidance.md | Read | Principles, trade-offs, considerations, conflict table (CFT-011-07-01, CFT-011-07-02) |
| Procedure.md | Read | 8 construction steps; prerequisites; verification activities; records list |

## Decomposition Reference

| Document | Status | Usage |
|---|---|---|
| WDMLRL_Decomposition_Claude.md | Read | WBS traceability: DEL-011-07 in PKG-011; covers SOW-0032, SOW-0033, SOW-0034; maps to OBJ-001 |
