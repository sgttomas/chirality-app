# Source Index — EST_DEL-015-01_2026-02-26_2232

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | RATE_TABLE | 25 roles with hourly rates in CAD; PARAMETRIC basis; MEDIUM confidence | Professional/management/design staff labour pricing |
| 2 | Level_of_Effort.csv | PARAMETRIC | Project-wide LoE by deliverable and role; 6 rows for DEL-015-01 (PM, CPM, Site Super, Cost Estimator, QA/QC Lead, HSE Manager) | Staff hours allocation for management/oversight of DEL-015-01 |
| 3 | Assumed_Project_Parameters.csv | REFERENCE | 19 project parameters (location, schedule, facility size, equipment counts, currency); HIGH confidence on confirmed items | Context and validation — not direct pricing |
| 4 | Electrical_System_Rates.csv | PARAMETRIC/ALLOWANCE | 6 electrical items; ES-03 (3-phase service allowance) directly applicable; ES-02 (panelboard), ES-04 (welding receptacle), ES-06 (motor connection) relevant for subcomponents | Direct material + install rates for electrical items |
| 5 | Underground_Utility_Rates.csv | PARAMETRIC | 5 items; UU-03 (underground conduit) directly applicable for service trench | Underground conduit rate for service trench |
| 6 | Construction_Labour_Rates.csv | RATE_TABLE | 10 trades with hourly, burden multiplier, and fully burdened rates in CAD; T-04 Electrician ($96.00/hr burdened), T-07 Equipment Operator ($88.00/hr burdened), T-08 Labourer ($65.10/hr burdened) relevant | Trade labour pricing for installation activities |

## Source Gaps

- No quote-based pricing available (BASIS_OF_ESTIMATE is PARAMETRIC — acceptable).
- No historical cost data available for comparable projects.
- Electrical_System_Rates.csv ES-03 (3-phase service allowance) is classified as ALLOWANCE with LOW confidence — service ampacity TBD.
- Underground conduit length for service trench is not specified in documents — estimated parametrically.
- Grounding system material costs not individually itemized in any source — included in ES-03 allowance or estimated parametrically.
