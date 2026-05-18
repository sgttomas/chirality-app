# Source Index: EST_DEL-05-02_2026-02-18_1500

## Price Sources Used

| # | File | Source Type | Items Used | Supports |
|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate table | R-02 ($175/hr), R-18 ($145/hr), R-19 ($115/hr) | Production cost lines L-001 through L-003 |
| 2 | Level_of_Effort.csv | Parametric hours | DEL-05-02: R-18 (24 hrs), R-19 (16 hrs), R-02 (4 hrs) | Production cost hours |
| 3 | Assumed_Project_Parameters.csv | Project parameters | PP-01 (18 months), PP-05 (18000 sf), PP-07 (6000 sf), PP-10 (4.5 ac), PP-11 (4 fire bays), PP-12 (4 PW bays), PP-13 (8 OH doors), PP-15 (40 bunker lockers), PP-16 (40 PW lockers), PP-17 (2 fill stations), PP-18 (8 sumps), PP-19 (40 parking), PP-20 (12 light poles), PP-24 ($8.7M base), PP-27 (45 IT drops), PP-28 (10 access zones), PP-29 (16 cameras) | Quantity derivations throughout |
| 4 | Structural_Concrete_Rates.csv | Construction rates | SC-02 through SC-15 | L-020 through L-022 (structural breakdown) |
| 5 | Building_Envelope_Rates.csv | Construction rates | BE-01 through BE-15 | L-025 through L-028 (envelope breakdown) |
| 6 | Interior_Architectural_Rates.csv | Construction rates | IA-01 through IA-25 | L-030 through L-036 (interior breakdown) |
| 7 | Mechanical_System_Rates.csv | Construction rates | MS-01 through MS-14 | L-040 through L-047 (mechanical breakdown) |
| 8 | Electrical_System_Rates.csv | Construction rates | ES-01 through ES-14 | L-050 through L-059 (electrical breakdown) |
| 9 | Earthwork_Civil_Rates.csv | Construction rates | EC-01 through EC-11 | L-060 through L-068 (site/civil breakdown) |
| 10 | Paving_Surfacing_Rates.csv | Construction rates | PS-01 through PS-09 | L-062 through L-066 (paving breakdown) |
| 11 | Underground_Utility_Rates.csv | Construction rates | UU-01 through UU-12 | L-070 through L-078 (utility breakdown) |
| 12 | Equipment_Pricing.csv | Construction pricing | EQ-01 through EQ-15 | L-090 through L-096 (equipment breakdown) |
| 13 | Optional_Items_Pricing.csv | Construction pricing | OPT-01 through OPT-18 | L-120 through L-170 (options breakdown) |
| 14 | Parametric_Building_Rates.csv | Parametric cross-check | PB-01, PB-02 | L-080 (cold storage building) |
| 15 | Construction_Labour_Rates.csv | Labour rates | Reference only | Used for GR sub-line derivations (supervision rates) |
| 16 | Professional_Design_Fees.csv | Design fee percentages | DF-01 through DF-08 | L-100 through L-108 (design fee breakdown) |
| 17 | Fees_Permits_Insurance.csv | Fees and permits | FP-01 through FP-19 | L-110 through L-116 (bonds/insurance/permits) + L-077 (utility connection fees) + L-078 (environmental) |

## Non-Price Sources Referenced

| Source | Type | Used For |
|---|---|---|
| EST_DEL-05-01_2026-02-18_1400/Detail.csv | Prior estimate snapshot | Reconciliation targets -- Schedule A totals that Schedule B must match |
| EST_DEL-05-01_2026-02-18_1400/Summary.md | Prior estimate snapshot | Reconciliation verification |
| Dependencies.csv (DEL-05-02 folder) | Dependency register | Blocker identification; dependency context |
| Decomposition (v1.md) | Project decomposition | Package/deliverable IDs; scope item mapping |
| BASIS_OF_ESTIMATE.md | BOE strategy document | Dual cost nature; cost ownership rules; estimation approach |

## Sources NOT Used (available but not applicable)

| File | Reason |
|---|---|
| None | All 17 price source files were used for DEL-05-02 construction pricing detail |

## Parsing Notes

- All CSV files parsed successfully with standard comma delimiters
- No encoding issues encountered
- Rate files use RecommendedRate column as primary pricing input
- Equipment/Optional files use RecommendedPrice column
- Level_of_Effort.csv filtered to Execution=6c and DeliverableID=DEL-05-02 rows
