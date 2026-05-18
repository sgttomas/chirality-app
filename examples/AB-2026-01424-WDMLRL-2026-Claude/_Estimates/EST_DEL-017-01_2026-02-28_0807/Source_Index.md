# Source Index — EST_DEL-017-01_2026-02-28_0807

## Indexed Price Sources

| Source # | File | Source Type | Parsing Notes | Supports |
|----------|------|-------------|---------------|----------|
| PS-01 | Professional_Staff_Rates.csv | Rate Table (PARAMETRIC) | 25 roles; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. All rates in CAD/hr. | Professional staff hourly rates for management, design, specialty, and admin roles. |
| PS-02 | Level_of_Effort.csv | Parametric Model | ~500+ rows; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. Filtered to DEL-017-01: 6 rows (R-01, R-02, R-03, R-05, R-06, R-08). | Professional staff hours allocated to DEL-017-01 by role. |
| PS-03 | Assumed_Project_Parameters.csv | Parametric Parameters | 19 rows; columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes. Includes project identity, location, schedule, facility dimensions, currency. | Project-level parameters; currency (CAD); kitchenette area not explicitly listed but referenced via RFP section 3.4 (250 sqft). |
| PS-04 | Interior_Architectural_Rates.csv | Rate Table (PARAMETRIC) | 5 items; columns: ItemID, Category, Description, Unit, RateMin, RateMax, RecommendedRate, Basis, Confidence, Notes. Rates in CAD. | Interior partitions (IA-01), paint (IA-02), ceilings (IA-03), flooring (IA-04), millwork/casework (IA-05). |
| PS-05 | Construction_Labour_Rates.csv | Rate Table (PARAMETRIC) | 10 trades; columns: TradeID, Trade, HourlyRate_CAD, BurdenMultiplier, FullyBurdenedRate_CAD, Basis, Confidence, Notes. Rates in CAD/hr. | Construction trade labour rates (carpenter, electrician, plumber, painter, drywaller, labourer, etc.). |
| PS-06 | Mechanical_System_Rates.csv | Rate Table (PARAMETRIC) | 8 items; columns: ItemID, Category, Description, Unit, RateMin, RateMax, RecommendedRate, Basis, Confidence, Notes. Rates in CAD. | Mechanical systems including gas fitting (MS-07) and kitchen ventilation (MS-08). |

## Coverage Assessment

| Item Category | Covered By | Coverage Quality |
|---------------|-----------|-----------------|
| Professional staff costs (ITM-001 to ITM-006) | PS-01 + PS-02 | GOOD -- hours from LOE, rates from staff rates |
| Existing conditions / utility verification (ITM-007, ITM-008) | PS-01, PS-05 | PARTIAL -- rates available; hours estimated parametrically |
| Design coordination (ITM-009) | PS-01 | PARTIAL -- rates available; hours estimated parametrically |
| Interior finishes (ITM-022, ITM-023, ITM-024, ITM-025) | PS-04 (IA-01 to IA-04) | GOOD -- unit rates available; area from RFP (250 sqft = 23.2 m2) |
| Cabinetry and fixtures (ITM-026, ITM-027) | PS-04 (IA-05) | PARTIAL -- lump-sum allowance available; actual fixtures TBD |
| Construction labour -- demolition, rough-in, protection (ITM-013 to ITM-018, ITM-021) | PS-05 | PARTIAL -- trade rates available; hours/scope estimated parametrically |
| Gas fitting rough-in (ITM-019) | PS-06 (MS-07) | GOOD -- recommended rate from Mechanical_System_Rates.csv; conditional on appliance schedule |
| Mechanical/HVAC rough-in (ITM-020) | PS-06 (MS-08) | GOOD -- recommended rate from Mechanical_System_Rates.csv; conditional on appliance schedule |
| Permits, inspections, coordination, closeout (ITM-010, ITM-011, ITM-028 to ITM-032) | PS-01, PS-05 | PARTIAL -- staff/trade rates available; effort is parametric estimate |

## Gaps

- No kitchenette-specific fixture/appliance rate table in any price source. Appliance and cabinetry scope is TBD pending design. Cabinetry priced from IA-05 allowance.
- No material-only rates for plumbing fixtures, electrical fixtures, or appliances. Labour rates from Construction_Labour_Rates.csv cover trade hours only; material costs embedded parametrically.
- No hazardous materials abatement rate table. ITM-012 priced as parametric allowance.
- No waste disposal rate. ITM-016 priced as parametric allowance.
