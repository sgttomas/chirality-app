# Run Context

**RunID:** EST_DEL-01-04_2026-02-18_2359
**AsOf:** 2026-02-18T23:59:00-07:00
**Agent:** ESTIMATING (Type 2)

---

## Inputs

| Field | Value |
|---|---|
| **Scope** | DEL-01-04 (Appendix H -- Schedule A -- Pricing Summary) |
| **ScopeResolvedSummary** | 1 deliverable in PKG-001; dual cost nature (production + construction pricing content) |
| **RUN_ROOT** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b` |
| **ESTIMATES_ROOT** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Estimates` |
| **BASIS_OF_ESTIMATE** | `RATE_TABLE` (validated) |
| **CURRENCY** | CAD |
| **ROUNDING** | DOLLAR |
| **DECOMPOSITION_PATH** | `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO -- read `DEL-01-04/Dependencies.csv` (13 ACTIVE rows) |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **OUTPUT_LABEL** | DEL-01-04 |

## Resolved Price Sources

| # | File | Type | Used For |
|---|---|---|---|
| 1 | `Professional_Staff_Rates.csv` | Rate Table | Production cost lines (staff hourly rates) |
| 2 | `Level_of_Effort.csv` | Rate Table | Production cost lines (hours by role for DEL-01-04) |
| 3 | `Assumed_Project_Parameters.csv` | Parameters | Project quantities, areas, financial parameters |
| 4 | `Structural_Concrete_Rates.csv` | Rate Table | Construction pricing -- structural/concrete scope |
| 5 | `Building_Envelope_Rates.csv` | Rate Table | Construction pricing -- envelope/cladding scope |
| 6 | `Interior_Architectural_Rates.csv` | Rate Table | Construction pricing -- interior finishes scope |
| 7 | `Mechanical_System_Rates.csv` | Rate Table | Construction pricing -- HVAC/plumbing/fire protection |
| 8 | `Electrical_System_Rates.csv` | Rate Table | Construction pricing -- power/lighting/telecom/FA |
| 9 | `Earthwork_Civil_Rates.csv` | Rate Table | Construction pricing -- earthwork/grading |
| 10 | `Paving_Surfacing_Rates.csv` | Rate Table | Construction pricing -- paving/surfacing |
| 11 | `Underground_Utility_Rates.csv` | Rate Table | Construction pricing -- underground utilities |
| 12 | `Equipment_Pricing.csv` | Rate Table | Construction pricing -- equipment/doors/lockers |
| 13 | `Optional_Items_Pricing.csv` | Rate Table | Construction pricing -- 6 additional options |
| 14 | `Parametric_Building_Rates.csv` | Parametric | Cross-check benchmark (not primary pricing) |
| 15 | `Construction_Labour_Rates.csv` | Rate Table | Reference (rates embedded in unit rates above) |
| 16 | `Professional_Design_Fees.csv` | Rate Table | Design fees for General Requirements |
| 17 | `Fees_Permits_Insurance.csv` | Rate Table | Bond/insurance/permits/fees for General Requirements |

## Scope Resolution

DEL-01-04 has **dual cost nature** per brief:

1. **Production cost lines** (Group A): Estimator/PM hours to compile Schedule A form and perform QA review. Method = RATE_TABLE. Source = Level_of_Effort.csv + Professional_Staff_Rates.csv.

2. **Construction pricing content lines** (Group B): The actual proposal prices that populate the Schedule A form -- base price (Line 1-1) + 6 additional options (Lines 1-2 through 1-7). Method = RATE_TABLE / PARAMETRIC / ALLOWANCE (mixed methods enabled). Source = all construction rate files.

## Boundary Rules Applied

- Bond/insurance premium calculation: included in Line 1-1 base (flows from DEL-01-03 via Schedule B General Requirements). Priced here at summary level using Fees_Permits_Insurance.csv percentages.
- Pricing narrative content: belongs to DEL-01-06, NOT priced here.
- Schedule B detail: belongs to DEL-01-05, NOT priced here. DEL-01-04 carries summary-level construction prices only.
- FF&E: priced as $20,000 cash allowance on Line 1-7 per DEC-012.
- Site servicing tie-ins: cash allowance per C-12 / Addendum 03.

## CBS Mapping Rule

CBS codes assigned deterministically:
- `PRD.COMP` = Production compilation costs (Group A)
- `CON.STR` = Structural/concrete
- `CON.ENV` = Building envelope
- `CON.INT` = Interior architectural
- `CON.MEC` = Mechanical systems
- `CON.ELC` = Electrical systems
- `CON.CIV` = Earthwork/civil
- `CON.PAV` = Paving/surfacing
- `CON.UTL` = Underground utilities
- `CON.EQP` = Equipment/specialty items
- `CON.GR` = General requirements (design fees, bonds, insurance, permits, contingency)
- `OPT.WSH` = Option 1 -- Wash Bay
- `OPT.YLT` = Option 2 -- Yard Lighting
- `OPT.ACC` = Option 3 -- Access Control
- `OPT.SEC` = Option 4 -- Security/Cameras
- `OPT.SGN` = Option 5 -- Signage
- `OPT.FFE` = Option 6 -- FF&E

## Warnings

- ALLOW_MIXED_METHODS=TRUE active: Detail.csv contains RATE_TABLE, PARAMETRIC, and ALLOWANCE methods.
- Construction pricing is summary-level (Schedule A); detailed breakdown belongs to DEL-01-05 (Schedule B).
- Parametric cross-check used PB-04 ($370/sf fire station) and PB-07 ($415/sf combined) as benchmarks.
- Some quantities are assumed (PP-series parameters) with MEDIUM or LOW confidence.
