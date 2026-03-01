# Source_Index — EST_DEL-014-06_2026-02-27_0201

## Pricing Sources Indexed

| PS-ID | File Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-STAFF | PriceSources/Professional_Staff_Rates.csv | Rate Table | 25 roles; HourlyRate_CAD column; all PARAMETRIC basis, MEDIUM confidence | Management/professional LOE line items (DL-013 through DL-018) |
| PS-LOE | PriceSources/Level_of_Effort.csv | Parametric | 577 rows total; 6 rows for DEL-014-06 (R-01, R-02, R-03, R-05, R-06, R-08) | Hours allocation for management/oversight roles |
| PS-PARAMS | PriceSources/Assumed_Project_Parameters.csv | Parametric | 18 parameters; key: PP-17 Currency=CAD, PP-14 Cistern=50,000L | Project context validation |
| PS-UU | PriceSources/Underground_Utility_Rates.csv | Allowance | 5 items; does not directly support fixture pricing | Not directly used for DEL-014-06 fixture items |
| PS-LAB | PriceSources/Construction_Labour_Rates.csv | Rate Table | 10 trades; T-05 Plumber = $92.80/hr fully burdened | Plumber labour line items (DL-010 through DL-012) |
| PS-EQ | PriceSources/Equipment_Pricing.csv | Allowance | 3 items; EQ-02 Pressure washer system allowance = $11,000 (full system, not fixture-only) | Reference only; EQ-02 covers full pressure washer system which exceeds DEL-014-06 reel-only scope |

## Sources NOT Available (Gaps)

| Gap | Impact | Mitigation |
|---|---|---|
| No fixture material pricing table in PRICE_SOURCES | Cannot price water taps, wash station, reel from rate table evidence | PARAMETRIC estimates used per FALLBACK_POLICY=ALLOW_PARAMETRIC |
| No plumbing fixture supply catalogue or quotes | Fixture unit costs are parametric estimates, not quote-backed | Flag for quote replacement; LOW/MED confidence |
| No AHJ fee schedule | Safety Code inspection fee is parametric allowance | LOW confidence allowance |
| No hot water heater pricing | Conditional item priced as parametric allowance | LOW confidence; conditional on CONF-014-06-01 resolution |

## Deliverable Documents Read

| Document | Path | Key Extractions |
|---|---|---|
| _CONTEXT.md | DEL-014-06_Fixtures/_CONTEXT.md | Deliverable ID, package, SOW refs, objectives |
| Datasheet.md | DEL-014-06_Fixtures/Datasheet.md | Fixture inventory (3 fixture groups), attributes, conditions, construction prerequisites |
| Specification.md | DEL-014-06_Fixtures/Specification.md | 20+ requirements, verification methods, interface requirements, submittal requirements |
| Guidance.md | DEL-014-06_Fixtures/Guidance.md | 6 principles, trade-offs, CONF-014-06-01/02/03 conflict items, hot water supply question |
| Procedure.md | DEL-014-06_Fixtures/Procedure.md | 8+ steps from design review through commissioning, coordination checklist, pressure testing |
