# Source Index — EST_DEL-001-06_2026-02-27_0630

## Price Sources

| # | Source Path | Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-1 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv | RATE_TABLE | 25 rows; RoleID R-01 through R-25; HourlyRate_CAD column; all PARAMETRIC basis; MEDIUM confidence | Hourly rates for all professional staff roles (PM, architects, engineers, technicians, admin) |
| PS-2 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv | PARAMETRIC | Multi-deliverable LOE matrix; rows filtered for DEL-001-06 yield 5 role assignments (R-01, R-08, R-11, R-12, R-13) totaling 130 hours | Hour allocations per role per deliverable; PARAMETRIC basis |
| PS-3 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv | PARAMETRIC | 18 rows; project identity, facility attributes, schedule, equipment; PP-10 floor area ~13,000 sqft; PP-11 ceiling 35 ft | Project parameters for parametric calculations; not directly pricing but informs quantities |
| PS-4 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv | PARAMETRIC | 5 rows; discipline-level fee percentages against construction value; DF-01 Architecture 4.5% recommended | Alternative pricing method for design deliverables as % of construction value; used as cross-check only |
| PS-5 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Parametric_Building_Rates.csv | PARAMETRIC | 2 rows; PB-01 maintenance shop at $285/sf recommended; PB-02 wash bay premium at $70/sf | Building construction parametric rates; used for cross-check of design fee method only |

## Source Coverage Assessment

- **Primary pricing method:** PARAMETRIC (staff hours x hourly rates)
- **Hours source:** Level_of_Effort.csv provides DEL-001-06 allocations for 5 roles
- **Rate source:** Professional_Staff_Rates.csv provides CAD hourly rates for all 5 roles
- **Coverage:** 100% of labour line items (ITM-001 through ITM-005) have both hours and rates from price sources
- **Non-labour items (ITM-006 through ITM-023):** These are scope-description items from the Datasheet and Procedure. Their production effort is captured within the labour hours. They are not independently priced; they represent the scope of work performed during the billed hours. Coordination items (ITM-006, ITM-007, ITM-008) and QA items (ITM-021, ITM-022) are embedded in the Senior Architect and Architect hour allocations. Drawing sheet items (ITM-009, ITM-010, ITM-011) and element placement items (ITM-012 through ITM-019) represent the output of the production hours. Field verification (ITM-020) is included in the architect time allocation. P.Eng. stamp (ITM-023) is included in the Senior Architect allocation.
