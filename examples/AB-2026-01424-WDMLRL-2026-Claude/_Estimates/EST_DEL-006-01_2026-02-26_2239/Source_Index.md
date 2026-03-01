# Source Index — EST_DEL-006-01_2026-02-26_2239

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports | Does Not Support |
|---|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate Table | 25 roles with hourly CAD rates; all PARAMETRIC basis, MEDIUM confidence | Hourly rates for all design and management roles (R-01 through R-25) | No material or equipment unit prices; no subcontractor quotes |
| 2 | Level_of_Effort.csv | Parametric LOE Model | Hours by deliverable and role; DEL-006-01 has 4 role entries totalling 80 hours | Direct hour allocations for DEL-006-01: R-01 (6h), R-08 (4h), R-13 (21h), R-18 (49h) | Does not provide task-level breakdown within each role; hours are aggregate per deliverable |
| 3 | Assumed_Project_Parameters.csv | Project Parameters | 19 parameters covering identity, location, facility, equipment, plumbing, economics | Plumbing-specific parameters: PP-14 (cistern 50000L), PP-15 (septic 2000 US gal), PP-17 (CAD currency) | No pricing data; reference parameters only |
| 4 | Professional_Design_Fees.csv | Fee Schedule | 5 discipline-level fee percentages (% of construction value) | Alternative fee-based pricing method (not used for this estimate — LOE approach preferred for single-deliverable scope) | No plumbing-specific fee line; would require construction value input which is not available |

## Deliverable Documents Read

| Document | File | Key Pricing Content Extracted |
|---|---|---|
| Datasheet.md | DEL-006-01 Datasheet | Facility attributes, plumbing system parameters, fixture list, conditions, construction items |
| Specification.md | DEL-006-01 Specification | 20 requirements (REQ-001 through REQ-020) defining scope of design work |
| Guidance.md | DEL-006-01 Guidance | Design principles, trade-offs, considerations (hot water TBD, freeze protection, cistern sizing) |
| Procedure.md | DEL-006-01 Procedure | 8-step production procedure from document review through County submission |

## Decomposition Reference

| Document | Key Content |
|---|---|
| WDMLRL_Decomposition_Claude.md | PKG-006 Plumbing Design package definition; DEL-006-01 entry (Design Presentation type, covers SOW-0010f, supports OBJ-003 and OBJ-004) |
