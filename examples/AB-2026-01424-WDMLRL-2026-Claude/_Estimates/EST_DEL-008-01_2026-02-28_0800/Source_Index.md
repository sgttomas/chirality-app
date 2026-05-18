# Source Index — EST_DEL-008-01_2026-02-28_0800

## Indexed Price Sources

### Source 1: Professional_Staff_Rates.csv

- **Path:** `_PriceSources/Professional_Staff_Rates.csv`
- **Source Type:** Rate Table (parametric)
- **Content:** 31 professional staff roles with hourly rates in CAD
- **Confidence:** MEDIUM (all rows)
- **Basis:** MARKET
- **Relevant Roles for DEL-008-01:**
  - R-01 Project Manager: $165/hr (used in L-001)
  - R-08 Cost Estimator: $135/hr (used in L-002)
  - R-20 Geotechnical Engineer: $175/hr (used in L-004, L-013, L-019, L-022)
- **Lines Sourced:** L-001 (rate only), L-002 (rate only), L-004 (rate), L-013 (rate), L-019 (rate), L-022 (rate)

### Source 2: Level_of_Effort.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
- **Source Type:** Parametric model (hours by role by deliverable)
- **Content:** Level-of-effort hours for all deliverables across the project
- **Relevant Rows for DEL-008-01:**
  - R-01 Project Manager: 6 hours (PARAMETRIC)
  - R-08 Cost Estimator: 4 hours (PARAMETRIC)
  - R-20 Geotechnical Engineer: 60 hours (PARAMETRIC) — program development (16) + field supervision (24) + analysis/review (20)
- **Lines Sourced:** L-001 (qty), L-002 (qty); R-20 hours inform L-004, L-013, L-019, L-022 allocation
- **Change from Prior Snapshot:** R-20 row added since prior snapshot (was missing in EST_DEL-008-01_2026-02-26_2232)

### Source 3: Assumed_Project_Parameters.csv

- **Path:** `_PriceSources/Assumed_Project_Parameters.csv`
- **Source Type:** Parametric parameters
- **Content:** 29 project-level parameters (duration, area, quantity, financial)
- **Confidence:** Varies (CONFIRMED, ASSUMPTION, DERIVED, PARAMETRIC)
- **Relevant Parameters for DEL-008-01:**
  - PP-05: Main PSB building footprint — 18,000 sf (DESIGN_BASIS, MEDIUM)
  - PP-07: Cold storage building footprint — 6,000 sf (CONFIRMED, HIGH)
  - PP-09: Site area — 12 acres (CONFIRMED, HIGH)
- **Lines Sourced:** Indirectly informs investigation scope (borehole count, depth, test pit count) but does not directly price any line item

### Source 4: Geotechnical_Investigation_Rates.csv (NEW)

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Geotechnical_Investigation_Rates.csv`
- **Source Type:** Rate Table (parametric)
- **Content:** 15 rows (GI-01 through GI-15) — Alberta 2026 geotechnical investigation rates for drilling, lab testing, professional services, mobilization, restoration, documentation
- **Confidence:** LOW to MEDIUM (varies by item)
- **Basis:** PARAMETRIC
- **Relevant Rates for DEL-008-01:**
  - GI-01: Drill rig mob/demob — $6,000 LS (used in L-005)
  - GI-02: Borehole drilling — $40/m (used in L-006)
  - GI-03: Test pit excavation — $800/EA (used in L-007)
  - GI-04: Monitoring well — $2,500/EA (used in L-008)
  - GI-05: Soil sample collection — $50/EA (used in L-009)
  - GI-06: Lab classification/index — $250/EA (used in L-012)
  - GI-07: Lab consolidation/oedometer — $550/EA (used in L-024)
  - GI-08: Lab direct shear/triaxial — $500/EA (used in L-025)
  - GI-09: Lab chemical analysis — $350/EA (used in L-026)
  - GI-10: Geotech engineer field supervision — $1,750/day (used in L-010)
  - GI-11: Investigation program development — $3,000 LS (used in L-003)
  - GI-12: Analysis and report preparation — $9,000 LS (used in L-018; also covers L-014, L-015, L-016, L-017)
  - GI-13: P.Eng. certification/seal — $1,000 LS (used in L-020)
  - GI-14: Site restoration — $1,000 LS (used in L-023)
  - GI-15: Photo documentation — $250 LS (used in L-011)
- **Lines Sourced:** L-003, L-005, L-006, L-007, L-008, L-009, L-010, L-011, L-012, L-014, L-015, L-016, L-017, L-018, L-020, L-023, L-024, L-025, L-026
- **Change from Prior Snapshot:** Entire source is new; resolves critical gap W-002 from prior snapshot

## Coverage Assessment

| Items.csv Category | Price Source Available | Coverage |
|---|---|---|
| Professional staff hours (PM, Cost Estimator) | Staff Rates + LoE | FULL — rates and hours provided |
| Geotechnical Engineer hours (project team items) | Staff Rates R-20 + LoE R-20 | FULL — rate $175/hr and 60 hr total from LoE; hours allocated across L-004, L-013, L-019, L-022 |
| Geotechnical subcontractor (program dev, field supervision, report) | GI Rates (GI-10, GI-11, GI-12) | FULL — lump-sum and daily rates applied |
| Field investigation (drilling, sampling, test pits, monitoring) | GI Rates (GI-01 through GI-05) | FULL — all items priced |
| Laboratory testing (classification, consolidation, shear, chemical) | GI Rates (GI-06 through GI-09) | FULL — all test types priced |
| Documentation and certification | GI Rates (GI-13, GI-15) | FULL — P.Eng. seal and photo documentation priced |
| Site restoration | GI Rates (GI-14) | FULL — lump sum applied |
| Report delivery | Bundled in PM hours (L-001) | FULL — administrative; $0 standalone |

**Overall pricing coverage: 26 of 26 items (100%) are fully priced. Total priced: $46,130 CAD.**
