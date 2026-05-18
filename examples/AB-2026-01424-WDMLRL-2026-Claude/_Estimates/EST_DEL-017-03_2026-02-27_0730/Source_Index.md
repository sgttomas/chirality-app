# Source Index

## Indexed Price Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | `PriceSources/Professional_Staff_Rates.csv` | PARAMETRIC (rate table) | 25 roles with hourly rates in CAD; Category, HourlyRate_CAD, Basis, Confidence columns. All rates marked PARAMETRIC / MEDIUM confidence. | Professional staff cost items: PM (R-01 $165/hr), Construction PM (R-02 $155/hr), Site Superintendent (R-03 $145/hr), Cost Estimator (R-08 $135/hr), QA/QC Lead (R-06 $135/hr), HSE Manager (R-05 $140/hr), Senior Architect (R-11 $180/hr), Architect (R-12 $135/hr), Plumbing Engineer (R-18 $160/hr) |
| PS-02 | `PriceSources/Level_of_Effort.csv` | PARAMETRIC (effort model) | Execution-level hours by DeliverableID and RoleID. DEL-017-03 has 6 role entries totalling 38 hours. | Direct hours allocation for DEL-017-03: R-01 (6h), R-02 (8h), R-03 (10h), R-08 (4h), R-06 (6h), R-05 (4h) |
| PS-03 | `PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC (parameters) | 18 parameters covering project identity, facility dimensions, equipment, plumbing, currency. | Context parameters: building area ~13,000 sqft (PP-10), 35ft ceiling (PP-11), 50,000L cistern (PP-14), CAD currency (PP-17) |
| PS-04 | `PriceSources/Interior_Architectural_Rates.csv` | PARAMETRIC (rate table) | 5 items with rate ranges and recommended rates. Categories: Partitions, Finishes, Ceilings, Flooring, Millwork. | IA-01 partitions $90/m2, IA-02 paint $12/m2, IA-03 ceilings $80/m2, IA-04 flooring $70/m2, IA-05 millwork $11,000 LS |
| PS-05 | `PriceSources/Construction_Labour_Rates.csv` | PARAMETRIC (rate table) | 10 trades with base hourly rates, burden multipliers, and fully burdened rates in CAD. | T-01 Carpenter $80.60/hr, T-02 Concrete Finisher $77.50/hr, T-05 Plumber $92.80/hr, T-06 HVAC $91.20/hr, T-04 Electrician $96.00/hr, T-08 Labourer $65.10/hr, T-09 Painter $69.75/hr, T-10 Drywaller $71.30/hr |

## Source Coverage Assessment

| Coverage Area | Status | Notes |
|---|---|---|
| Professional staff rates | COVERED | PS-01 provides hourly rates for all relevant roles |
| Level of effort (hours) | COVERED | PS-02 provides hours for DEL-017-03 professional staff |
| Construction labour rates | COVERED | PS-05 provides fully burdened rates for all relevant trades |
| Interior architectural rates | COVERED | PS-04 provides unit rates for partitions, paint, ceilings, flooring |
| Fixture unit prices (toilet, sink, urinal) | NOT COVERED | No fixture pricing source provided; parametric estimates used |
| Exhaust fan / mechanical equipment | NOT COVERED | No mechanical equipment pricing source; parametric estimate used |
| Lighting fixtures | NOT COVERED | No lighting fixture pricing source; parametric estimate used |
| Washroom accessories | NOT COVERED | No accessories pricing source; parametric estimate used |
| Demolition rates | NOT COVERED | No demolition pricing source; parametric estimate derived from labour rates |
| Hazardous materials assessment | NOT COVERED | No hazmat pricing source; parametric estimate used |
| Permit fees | N/A | County responsibility per RFP §3.3.1 — excluded from estimate |
