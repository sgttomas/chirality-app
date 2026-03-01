# Source Index — EST_DEL-006-02_2026-02-27_0730

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports | Does Not Support |
|---|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate Table | 25 roles with hourly CAD rates; all PARAMETRIC basis, MEDIUM confidence | Hourly rates for all design and management roles (R-01 through R-25) | No material or equipment unit prices; no subcontractor quotes |
| 2 | Level_of_Effort.csv | Parametric LOE Model | Hours by deliverable and role; DEL-006-02 has 4 role entries totalling 80 hours | Direct hour allocations for DEL-006-02: R-01 (6h), R-08 (4h), R-13 (21h), R-18 (49h) | Does not provide task-level breakdown within each role; hours are aggregate per deliverable |
| 3 | Assumed_Project_Parameters.csv | Project Parameters | 19 parameters covering identity, location, facility, equipment, plumbing, economics | Plumbing-specific parameters: PP-14 (cistern 50000L), PP-15 (septic 2000 US gal), PP-17 (CAD currency), PP-18 (base year 2026) | No pricing data; reference parameters only |
| 4 | Professional_Design_Fees.csv | Fee Schedule | 5 discipline-level fee percentages (% of construction value) | Alternative fee-based pricing method (not used for this estimate -- LOE approach preferred for single-deliverable scope) | No plumbing-specific fee line; would require construction value input which is not available |

## Deliverable Documents Read

| Document | File | Key Pricing Content Extracted |
|---|---|---|
| Datasheet.md | DEL-006-02 Datasheet | Water distribution system scope, key system parameters (50000L cistern, 100 LPM pump, 2.5-inch filling connection), fixture/tap locations (emergency shower, water taps, pressure washer reel, wash station, washroom), freeze protection parameters, drawing sheet anticipated content, pipe material TBD, conditions |
| Specification.md | DEL-006-02 Specification | 13 requirements (REQ-001 through REQ-013) covering cistern-fed distribution, emergency shower, water taps, wash station, washroom fixtures, bulk water fill, drawing completeness, code compliance, P.Eng. stamp, coordination, preliminary design basis, freeze protection, revision control; SOW-to-drawing traceability matrix |
| Guidance.md | DEL-006-02 Guidance | Design principles (cistern-first mindset, conceptual layout as anchor, deliverable separation, coordination as core attribute), considerations (Alberta climate freeze protection, emergency shower compliance, bulk fill interface, pressure washer supply, washroom/laundry expansion), trade-offs (pipe material, hot water system, freeze protection approach, bulk fill interface), conflict table (CF-001 hot water, CF-002 bulk fill scope boundary) |
| Procedure.md | DEL-006-02 Procedure | 11-step production procedure (Steps 1 through 9 plus 5A, 6A, 8A) from scope boundary confirmation through P.Eng. stamp and IFC issue; prerequisite verification gate; internal quality review; DEL-006-01 approval hold point |

## Decomposition Reference

| Document | Key Content |
|---|---|
| WDMLRL_Decomposition_Claude.md | PKG-006 Plumbing Design package definition; DEL-006-02 entry (Drawing Set type, covers SOW-0016, supports OBJ-001, OBJ-003, and OBJ-004); responsible party: Plumbing Engineer |
