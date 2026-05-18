# Source Index

**RunID:** EST_DEL-01-04_2026-02-18_2359

---

## Price Sources Used

| # | File Path | Source Type | Rows/Items | Used For | Parsing Notes |
|---|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 30 roles | Production cost line rates (R-02, R-18, R-19) | CSV; clean parse; all rates in CAD/hr |
| 2 | `_PriceSources/Level_of_Effort.csv` | Rate Table | 73 rows (all deliverables) | DEL-01-04 production hours: 3 rows (R-18 40hr, R-19 24hr, R-02 8hr) | CSV; filtered to DEL-01-04; Execution=6b |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Parameters | 29 parameters | PP-05 (18000 sf), PP-07 (6000 sf), PP-08 (24000 sf), PP-10 (4.5 ac), PP-11 thru PP-20 (quantities), PP-25 ($12M) | CSV; clean parse |
| 4 | `_PriceSources/Structural_Concrete_Rates.csv` | Rate Table | 15 items (SC-01 to SC-15) | Lines B-100 to B-140 (foundations, slabs, steel, deck) | CSV; RecommendedRate used; units in m2/m3/kg/each/lm |
| 5 | `_PriceSources/Building_Envelope_Rates.csv` | Rate Table | 15 items (BE-01 to BE-15) | Lines B-200 to B-250 (wall panels, roof, glazing, doors, sealant, air barrier) | CSV; RecommendedRate used |
| 6 | `_PriceSources/Interior_Architectural_Rates.csv` | Rate Table | 25 items (IA-01 to IA-25) | Lines B-300 to B-350 (partitions, ceilings, flooring, paint, accessibility, millwork) | CSV; RecommendedRate used |
| 7 | `_PriceSources/Mechanical_System_Rates.csv` | Rate Table | 14 items (MS-01 to MS-14) | Lines B-400 to B-460 (HVAC, plumbing, fire protection, exhaust, ventilation, BAS) | CSV; RecommendedRate used; units in sf/each/system |
| 8 | `_PriceSources/Electrical_System_Rates.csv` | Rate Table | 14 items (ES-01 to ES-14) | Lines B-600 to B-670 (power, lighting, IT, fire alarm, emergency, solar-ready, cold storage) | CSV; RecommendedRate used |
| 9 | `_PriceSources/Earthwork_Civil_Rates.csv` | Rate Table | 11 items (EC-01 to EC-11) | Lines B-700 to B-780 (clearing, stripping, excavation, fill, pads, ESC, drainage, landscaping, survey) | CSV; RecommendedRate used |
| 10 | `_PriceSources/Paving_Surfacing_Rates.csv` | Rate Table | 9 items (PS-01 to PS-09) | Lines B-800 to B-870 (heavy/light asphalt, aggregate, aprons, curb, sidewalk, marking, bollards) | CSV; RecommendedRate used |
| 11 | `_PriceSources/Underground_Utility_Rates.csv` | Rate Table | 12 items (UU-01 to UU-12) | Lines B-900 to B-960 (water, sewer, storm, gas, power duct, telecom, tie-in allowance) | CSV; RecommendedRate used; UU-12 is ALLOWANCE basis |
| 12 | `_PriceSources/Equipment_Pricing.csv` | Rate Table | 15 items (EQ-01 to EQ-15) | Lines B-500 to B-1020 (OH doors, generator, lockers, SCBA, fill stations, sumps, displays, PA, workshop, temp facilities) | CSV; RecommendedPrice used; EQ-13 is ALLOWANCE |
| 13 | `_PriceSources/Optional_Items_Pricing.csv` | Rate Table | 18 items (OPT-01 to OPT-18) | Lines C-100 to C-600 (6 additional options) | CSV; RecommendedPrice used; OPT-18 is ALLOWANCE |
| 14 | `_PriceSources/Parametric_Building_Rates.csv` | Parametric | 9 items (PB-01 to PB-09) | Line B-1000 (cold storage PEMB turnkey) + cross-check benchmarks | CSV; PB-02 used for cold storage pricing; PB-03/PB-04/PB-07 used for cross-check only |
| 15 | `_PriceSources/Construction_Labour_Rates.csv` | Rate Table (reference) | 15 trades (T-01 to T-15) | Not directly used -- labour rates are embedded in the composite unit rates above | CSV; reference only |
| 16 | `_PriceSources/Professional_Design_Fees.csv` | Rate Table | 8 items (DF-01 to DF-08) | Line B-1100 (design fees in General Requirements) | CSV; fee percentages and lump sums used |
| 17 | `_PriceSources/Fees_Permits_Insurance.csv` | Rate Table | 19 items (FP-01 to FP-19) | Lines B-1110 to B-1195 (bonds, insurance, permits, utility fees, environmental, broker) | CSV; percentages applied to PP-25 ($12M) or PP-24 ($8.7M) as appropriate |

## Decomposition Source

| File | Version | Used For |
|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | v2.3 FINAL | Package/deliverable ID validation; scope item mapping (SOW-0005); constraint references (C-05 to C-12); project vocabulary |

## Dependency Source

| File | Rows | Used For |
|---|---|---|
| `DEL-01-04/Dependencies.csv` | 13 ACTIVE | Blocker identification; upstream prerequisite awareness (DEL-01-05, DEL-01-06, DEL-01-03); constraint traceability |

## Files NOT Used (in Price Sources but not applicable to DEL-01-04)

None -- all 17 price source files were consulted. Construction_Labour_Rates.csv was referenced but not directly used (rates are embedded in composite unit rates in the other files).
