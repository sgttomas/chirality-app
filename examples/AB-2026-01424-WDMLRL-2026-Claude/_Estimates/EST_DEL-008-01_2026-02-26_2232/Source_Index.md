# Source Index — EST_DEL-008-01_2026-02-26_2232

## Indexed Price Sources

### Source 1: Professional_Staff_Rates.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`
- **Source Type:** Rate Table (parametric)
- **Content:** 25 professional staff roles with hourly rates in CAD
- **Confidence:** MEDIUM (all rows)
- **Basis:** PARAMETRIC
- **Relevant Roles for DEL-008-01:**
  - R-01 Project Manager: $165/hr
  - R-08 Cost Estimator: $135/hr
  - R-20 Geotechnical Engineer: $175/hr
  - R-21 Surveyor: $140/hr (not directly needed for geotech investigation but in PKG-008)
- **Cannot Support:** Drill rig rates, drilling crew rates, laboratory testing costs, mobilization costs, equipment rental, subcontractor rates

### Source 2: Level_of_Effort.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
- **Source Type:** Parametric model (hours by role by deliverable)
- **Content:** Level-of-effort hours for all deliverables across the project
- **Relevant Rows for DEL-008-01:**
  - R-01 Project Manager: 6 hours (PARAMETRIC)
  - R-08 Cost Estimator: 4 hours (PARAMETRIC)
- **Cannot Support:** Geotechnical Engineer hours (not provided), field crew hours, laboratory testing hours, any non-professional-staff effort
- **Parsing Notes:** Only 2 rows exist for DEL-008-01 out of what would typically be 5-10+ role allocations for a geotechnical investigation deliverable. This is a significant gap.

### Source 3: Assumed_Project_Parameters.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`
- **Source Type:** Parametric parameters
- **Content:** 18 project-level parameters (identity, location, contract, schedule, facility, equipment, plumbing, mechanical, currency, economics)
- **Relevant Parameters for DEL-008-01:**
  - PP-03: Site location — WDMLRL near Ferintosh, Alberta
  - PP-04: Legal location — SW 14-44-21-W4
  - PP-10: Addition floor area — approx 13,000 sqft (DERIVED, MEDIUM confidence)
  - PP-11: Ceiling height — 35 ft (CONFIRMED, HIGH)
  - PP-12: Overhead cranes — 2 EA (CONFIRMED, HIGH)
  - PP-13: Crane capacity — 5 ton (CONFIRMED, HIGH)
  - PP-17: Currency — CAD (ASSUMPTION, MEDIUM)
- **Cannot Support:** Direct pricing of any geotech investigation line items; these are design parameters that inform scope, not costs

## Coverage Assessment

| Items.csv Category | Price Source Available | Coverage |
|---|---|---|
| Professional staff hours (PM, Cost Estimator) | Staff Rates + LoE | FULL — rates and hours provided |
| Geotechnical Engineer hours (all phases) | Staff Rates only (rate $175/hr) | PARTIAL — rate available but no hours in LoE; hours TBD |
| Field investigation (drilling, sampling, test pits) | NONE | NONE — no drill rig, drilling crew, or equipment rates in any source |
| Groundwater monitoring equipment | NONE | NONE |
| Laboratory testing | NONE | NONE — no lab test unit costs in any source |
| Mob/demob | NONE | NONE — no mobilization rates |
| Report production (non-engineer) | NONE | NONE — no admin/drafting rates specific to report production |
| Site restoration | NONE | NONE |

**Overall pricing coverage: 2 of 23 items (8.7%) can be fully priced from provided sources. An additional ~10 items could be partially priced (rate available for engineer hours, but quantities TBD).**
