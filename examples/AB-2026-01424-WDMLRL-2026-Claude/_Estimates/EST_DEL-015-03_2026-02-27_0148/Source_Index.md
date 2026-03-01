# Source Index — EST_DEL-015-03_2026-02-27_0148

## Pricing Sources Indexed

| Source File | Source Type | Parsing Notes | Supports | Gaps |
|---|---|---|---|---|
| Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 roles with hourly rates in CAD; basis = PARAMETRIC, confidence = MEDIUM | Professional staff hourly costing (PM, CPM, Superintendent, Cost Estimator, QA/QC Lead, HSE Manager, Electrical Engineer) | Does not include trade labour rates |
| Level_of_Effort.csv | PARAMETRIC (hours model) | Per-deliverable hours by role across full project; DEL-015-03 has 6 rows (R-01, R-02, R-03, R-05, R-06, R-08) | Staff hours allocation for DEL-015-03 management and oversight | Does not include electrician trade hours; trade labour must be estimated parametrically |
| Assumed_Project_Parameters.csv | PARAMETRIC (context) | 18 parameters covering project identity, facility, equipment, schedule, currency | Context for parametric modelling — building area (~13,000 sqft), facility type (maintenance shop) | No direct pricing data; used for contextual validation |
| Electrical_System_Rates.csv | PARAMETRIC / ALLOWANCE (rate table) | 6 items: lighting fixtures, panelboards, 3-phase service, welding receptacles, security camera rough-in, motor connections | ES-04: Welding receptacle (50A class) installed at $950/EA; ES-02: Panelboard at $4,800/EA | Limited to 6 item types; does not cover all receptacle types (15A, 20A, 30A); conduit/wire rates not itemized |
| Underground_Utility_Rates.csv | PARAMETRIC / ALLOWANCE (rate table) | 5 items: water, sanitary, underground conduit, septic tank, cistern | UU-03: Underground conduit (power) at $95/m — relevant if any receptacle circuits require underground routing | Not directly applicable to most receptacle installation work |
| Construction_Labour_Rates.csv | PARAMETRIC (rate table) | 10 trades with base hourly rate, burden multiplier, and fully burdened rate in CAD | T-04: Electrician at $96.00/hr fully burdened; T-08: Labourer at $65.10/hr | Covers electrician trade rate; does not include material rates |

## Source Coverage Assessment

- **Professional staff hours and rates**: COVERED — Level_of_Effort.csv provides hours; Professional_Staff_Rates.csv provides rates.
- **Electrician trade labour rate**: COVERED — Construction_Labour_Rates.csv T-04 at $96.00/hr fully burdened.
- **Welding receptacle (50A) material + install**: PARTIALLY COVERED — Electrical_System_Rates.csv ES-04 provides $950/EA installed rate (includes device + install labour).
- **15A/120V, 20A/120V, 20A/240V, 30A/240V receptacle material**: NOT DIRECTLY COVERED — no explicit rates in price sources; must use parametric estimation.
- **Conduit, wire, boxes (rough-in materials)**: NOT DIRECTLY COVERED — no itemized material rates; must use parametric installed-cost estimation or labour-only approach.
- **GFCI devices/breakers**: NOT DIRECTLY COVERED — must use parametric estimation.
- **Permit fees**: NOT DIRECTLY COVERED — must use parametric estimation / allowance.
