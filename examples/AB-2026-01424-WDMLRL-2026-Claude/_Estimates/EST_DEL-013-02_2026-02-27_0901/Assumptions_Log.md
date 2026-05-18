# Assumptions Log — EST_DEL-013-02_2026-02-27_0901

| AssumptionID | Assumption | Source / Basis | Impact on Estimate | Sensitivity |
|---|---|---|---|---|
| A-001 | Facility floor area is approximately 13,000 sqft (130 ft x 100 ft) with 35 ft ceiling | Assumed_Project_Parameters.csv PP-10 (DERIVED, MEDIUM) and PP-11 (CONFIRMED, HIGH); R-04 Appendix B | Drives ductwork quantity (L-005 = $25,368) via MS-06 rate per m2 | HIGH — ductwork is 33% of total estimate |
| A-002 | Air exchanger distribution ductwork represents 35% of total building ductwork scope | Parametric allocation — air exchanger serves general supply/return; remaining 65% allocated to heating, makeup air, and exhaust systems | L-005 = $25,368 (35% x 1,208 m2 x $60/m2) | HIGH — a 25% to 45% range would yield $18,120 to $32,616 |
| A-003 | Single HRV/ERV unit (1 EA) for the facility | Datasheet and Specification describe a single system; Guidance Trade-offs notes "single unit vs. distributed units" as TBD | L-001 = $13,500 for 1 unit; if multiple units needed, equipment cost increases proportionally | MEDIUM |
| A-004 | Equipment price uses MS-03 recommended midpoint ($13,500) from range $9,000–$18,000 | Mechanical_System_Rates.csv MS-03; ALLOWANCE basis, LOW confidence | L-001 = $13,500; range = $9,000 to $18,000 | MEDIUM — $4,500 variance |
| A-005 | HVAC sheet metal labour for ductwork: 80 hours (2 trades x 5 days x 8 hrs) | Parametric estimate for single-deliverable duct installation in industrial building | L-023 = $7,296 | MEDIUM |
| A-006 | General labourer: 24 hours (1 labourer x 3 days x 8 hrs) | Parametric estimate for installation support | L-024 = $1,562.40 | LOW |
| A-007 | Controls and sensors package: $4,500 lump sum | Parametric assumption for HVAC controls (controller, thermostats, CO/CO2 sensors, damper actuators) | L-009 = $4,500 | MEDIUM — actual depends on DEL-003-07 specification |
| A-008 | Heating system integration: $3,500 lump sum | Parametric assumption for mechanical interconnection labour + materials | L-010 = $3,500 | MEDIUM — depends on system design |
| A-009 | Vibration isolation: $2,000 lump sum | Parametric assumption for spring mounts or rubber pads for industrial HRV/ERV | L-008 = $2,000 | LOW |
| A-010 | Safety codes permit and inspections: $1,500 lump sum | Parametric assumption for Alberta mechanical permit fee + inspection scheduling | L-014 = $1,500 | LOW |
| A-011 | Wall penetration rate: $750/EA for industrial wall core, sleeve, and flashing | Parametric assumption | L-006 = $1,500 (2 EA) | LOW |
| A-012 | Fire stopping rate: $350/EA | Parametric assumption per standard practice | L-007 = $700 (2 EA) | LOW |
| A-013 | Electrical power connection: 12 hrs electrician labour at $96/hr + small material allowance | Parametric; scope boundary TBD per Guidance Conflict C-002 | L-012 = $1,200 | LOW |
| A-014 | Condensate drain: $800 lump sum | Parametric assumption for drain line, trap, and freeze protection | L-011 = $800 | LOW |
| A-015 | Closeout documentation (O&M + as-builts + commissioning report compilation): $1,500 lump sum | Parametric assumption for documentation assembly | L-016 = $1,500 | LOW |
| A-016 | Fresh air intake ductwork material: $1,500 + 16 hrs T-06 labour | Parametric; duct material assumed for single run from exterior wall to Utility Room | L-003 = $2,959.20 | MEDIUM |
| A-017 | Exhaust outlet ductwork material: $1,500 + 16 hrs T-06 labour | Parametric; duct material assumed for single run from Utility Room to exterior wall | L-004 = $2,959.20 | MEDIUM |
| A-018 | Equipment installation: 16 hrs HVAC trade labour (2 trades x 8 hrs) for rigging and setting unit | Parametric estimate for single-unit placement | L-002 = $1,459.20 | LOW |
| A-019 | Training cost (Procedure Step 5.4) is included within closeout allowance (A-015) | TBD whether formally required under contract | No separate line | LOW |
| A-020 | Currency is CAD | Assumed_Project_Parameters.csv PP-17 (ASSUMPTION, MEDIUM); Alberta context | All amounts in CAD | N/A |
