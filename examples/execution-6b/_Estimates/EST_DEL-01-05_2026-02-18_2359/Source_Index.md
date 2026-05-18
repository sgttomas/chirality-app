# Source Index -- EST_DEL-01-05_2026-02-18_2359

## Price Sources Used

| # | Source File | Source Type | Usage in This Estimate | Parsing Notes |
|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate Table | Production cost line items (R-02, R-18, R-19 hourly rates) | 30 roles; CSV; used 3 roles for DEL-01-05 production |
| 2 | Level_of_Effort.csv | Rate Table | Production hours for DEL-01-05 (R-18: 24 hrs, R-19: 16 hrs, R-02: 4 hrs) | 73 rows; filtered to DEL-01-05 = 3 rows |
| 3 | Assumed_Project_Parameters.csv | Reference | Building areas (PP-05 through PP-08), quantities (PP-11 through PP-20), financial parameters (PP-21 through PP-25) | 29 parameters; provides scope basis for quantity takeoffs |
| 4 | Structural_Concrete_Rates.csv | Rate Table | Foundations, slab, structural steel, joists, deck (B-BLD-100 through B-BLD-130) | 15 items; used SC-03/04/08/10/11/13/14/15 |
| 5 | Building_Envelope_Rates.csv | Rate Table | Wall panels, roof panels, glazing, doors, sealant, air barrier (B-BLD-200 through B-BLD-250) | 15 items; used BE-01/04/08/09/10/11/12/13/14/15 |
| 6 | Interior_Architectural_Rates.csv | Rate Table | Partitions, ceilings, flooring, paint, accessibility, millwork (B-BLD-300 through B-BLD-350) | 25 items; used IA-01 through IA-25 selectively |
| 7 | Mechanical_System_Rates.csv | Rate Table | HVAC, plumbing, fire protection, exhaust, ventilation, BAS (B-BLD-400 through B-BLD-460) | 14 items; used MS-01 through MS-14 selectively |
| 8 | Electrical_System_Rates.csv | Rate Table | Power, lighting, IT/telecom, fire alarm, emergency, solar-ready (B-BLD-600 through B-BLD-670) | 14 items; used ES-01 through ES-14 selectively |
| 9 | Earthwork_Civil_Rates.csv | Rate Table | Site clearing, stripping, excavation, fill, pad prep, ESC, drainage, seeding, survey (B-SIT-100 through B-SIT-180) | 11 items; used EC-01 through EC-11 selectively |
| 10 | Paving_Surfacing_Rates.csv | Rate Table | Asphalt, aggregate, concrete aprons/curb/sidewalk, markings, bollards (B-SIT-200 through B-SIT-270) | 9 items; used PS-01 through PS-09 selectively |
| 11 | Underground_Utility_Rates.csv | Rate Table | Water, sewer, storm, gas, power duct, telecom, municipal tie-in (B-SIT-300 through B-SIT-360) | 12 items; used UU-01 through UU-12 selectively |
| 12 | Equipment_Pricing.csv | Rate Table | OH doors, generator, lockers, breathing air, fill stations, sumps, displays, PA, workshop, temp facilities (B-BLD-500 through B-BLD-720) | 17 items; used EQ-01 through EQ-15 selectively |
| 13 | Optional_Items_Pricing.csv | Rate Table | Wash bay, yard lighting, access control, security, signage, FF&E (C-100 through C-600) | 18 items; used OPT-01 through OPT-18 selectively |
| 14 | Parametric_Building_Rates.csv | Parametric | Cold storage PEMB turnkey (B-BLD-700 using PB-02) | 9 items; used PB-02 for cold storage |
| 15 | Construction_Labour_Rates.csv | Reference | Not directly used for line pricing; labour rates embedded in composite rates from other sources | 15 trade rates; context reference for labour component validation |
| 16 | Professional_Design_Fees.csv | Rate Table | Design fees in General Requirements (B-GR-100 using DF-01 through DF-08) | 8 items; all used for GR design fee computation |
| 17 | Fees_Permits_Insurance.csv | Rate Table | Bonds, insurance, permits, utility fees, environmental (B-GR-110 through B-GR-195) | 19 items; used FP-01 through FP-19 selectively |

## Upstream Estimate Referenced

| Source | Type | Usage |
|---|---|---|
| EST_DEL-01-04_2026-02-18_2359 | Prior estimate snapshot | Reconciliation target: construction content totals ($7,710,000) used to validate Schedule B totals; individual line amounts cross-checked |

## Sources NOT Used

| Source | Reason |
|---|---|
| Construction_Labour_Rates.csv | Labour rates are embedded in composite unit rates from other CSV files; not used as a standalone pricing input for any line item |
