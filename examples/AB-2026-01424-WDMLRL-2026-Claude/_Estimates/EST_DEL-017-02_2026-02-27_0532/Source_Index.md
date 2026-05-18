# Source Index — EST_DEL-017-02_2026-02-27_0532

## Indexed Price Sources

| Source # | File | Source Type | Parsing Notes | Supports |
|----------|------|-------------|---------------|----------|
| PS-01 | Professional_Staff_Rates.csv | Rate Table (PARAMETRIC) | 25 roles; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. All rates in CAD/hr. | Professional staff hourly rates for management, design, specialty, and admin roles. |
| PS-02 | Level_of_Effort.csv | Parametric Model | ~500+ rows; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. Filtered to DEL-017-02: 6 rows (R-01, R-02, R-03, R-05, R-06, R-08). | Professional staff hours allocated to DEL-017-02 by role. |
| PS-03 | Assumed_Project_Parameters.csv | Parametric Parameters | 19 rows; columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes. Includes project identity, location, schedule, facility dimensions, currency. | Project-level parameters; currency (CAD); facility context. No DEL-017-02-specific area parameter. |
| PS-04 | Interior_Architectural_Rates.csv | Rate Table (PARAMETRIC) | 5 items; columns: ItemID, Category, Description, Unit, RateMin, RateMax, RecommendedRate, Basis, Confidence, Notes. Rates in CAD. | Interior partitions (IA-01), paint (IA-02), ceilings (IA-03), flooring (IA-04), millwork/casework (IA-05). |
| PS-05 | Construction_Labour_Rates.csv | Rate Table (PARAMETRIC) | 10 trades; columns: TradeID, Trade, HourlyRate_CAD, BurdenMultiplier, FullyBurdenedRate_CAD, Basis, Confidence, Notes. Rates in CAD/hr. | Construction trade labour rates (carpenter, electrician, plumber, painter, drywaller, labourer, etc.). |

## Coverage Assessment

| Item Category | Covered By | Coverage Quality |
|---------------|-----------|-----------------|
| Professional staff costs (ITM-001 to ITM-006) | PS-01 + PS-02 | GOOD — hours from LOE, rates from staff rates |
| Structural engineering assessment (ITM-007) | PS-01 (R-14 Structural Engineer rate) | PARTIAL — rate available; hours estimated parametrically |
| Design services (ITM-009) | PS-01 (R-11, R-12, R-14, R-16 rates) | PARTIAL — rates available; hours estimated parametrically |
| Interior finishes (ITM-017, ITM-019, ITM-020, ITM-021) | PS-04 (IA-01 to IA-04) | GOOD — unit rates available; area is assumed |
| Millwork/casework (ITM-022, ITM-023) | PS-04 (IA-05) | PARTIAL — lump-sum allowance available |
| Construction labour (ITM-013, ITM-014, ITM-015, ITM-016, ITM-018) | PS-05 | PARTIAL — trade rates available; hours/scope estimated parametrically |
| Permits, inspections, coordination, closeout (ITM-010, ITM-011, ITM-024-ITM-030) | PS-01, PS-05 | PARTIAL — staff/trade rates available; effort is parametric estimate |

## Gaps

- No mezzanine-specific area measurement in any price source. Area assumed at 30 m2 (see ASM-001).
- No material-only rates for stair/railing, electrical fixtures, or structural repair materials. Labour rates cover trade hours only.
- No hazardous materials abatement rate table. ITM-012 priced as parametric allowance.
- No waste disposal rate. ITM-029 priced as parametric allowance.
