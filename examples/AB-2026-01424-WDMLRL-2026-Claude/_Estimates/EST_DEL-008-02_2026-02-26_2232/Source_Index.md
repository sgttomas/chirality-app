# Source Index — EST_DEL-008-02_2026-02-26_2232

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports | Cannot Support |
|---|---|---|---|---|---|
| 1 | `Professional_Staff_Rates.csv` | Rate Table | 25 roles; hourly rates in CAD; all PARAMETRIC basis, MEDIUM confidence | Hourly rates for all professional roles (R-01 through R-25) | Does not provide hours or lump-sum amounts; does not cover materials, equipment, or subconsultant costs |
| 2 | `Level_of_Effort.csv` | Parametric | Multi-deliverable LOE table; role-by-deliverable hour estimates | Hours for R-01 (PM, 6 hr) and R-08 (Cost Estimator, 4 hr) for DEL-008-02 | Surveyor (R-21) hours for DEL-008-02 are TBD (notes say "PKG-008 TBD -- TBD"); no surveyor field or office hours provided |
| 3 | `Assumed_Project_Parameters.csv` | Parametric | 19 parameters; project identity, location, facility attributes, schedule, currency | Project context (site location, building size ~13,000 sqft, 35 ft ceiling, project deadline Dec 31 2026, CAD currency) | Does not provide pricing data directly; used for parametric scaling context |

## Deliverable Documents (Quantity Takeoff Sources)

| # | Document | Path | Role in Estimate |
|---|---|---|---|
| 1 | Datasheet.md | `PKG-008_.../DEL-008-02_.../Datasheet.md` | Attributes, quantities, conditions, survey scope elements |
| 2 | Specification.md | `PKG-008_.../DEL-008-02_.../Specification.md` | Requirements R-001 through R-013; verification criteria; acceptance criteria |
| 3 | Guidance.md | `PKG-008_.../DEL-008-02_.../Guidance.md` | Principles, trade-offs, priority ranking, budget/cost considerations |
| 4 | Procedure.md | `PKG-008_.../DEL-008-02_.../Procedure.md` | 7 procedural steps defining work activities; prerequisites; records |

## Decomposition (WBS Traceability)

| # | Document | Path | Role in Estimate |
|---|---|---|---|
| 1 | WDMLRL_Decomposition_Claude.md | `_Decomposition/WDMLRL_Decomposition_Claude.md` | PKG-008 package definition; DEL-008-02 deliverable entry; SOW-0002; OBJ-003 |
