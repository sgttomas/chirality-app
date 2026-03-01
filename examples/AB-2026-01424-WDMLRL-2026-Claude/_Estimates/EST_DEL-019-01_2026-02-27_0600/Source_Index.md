# Source Index — EST_DEL-019-01_2026-02-27_0600

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `Professional_Staff_Rates.csv` | RATE_TABLE | 25 roles with RoleID, HourlyRate_CAD, Basis=PARAMETRIC, Confidence=MEDIUM | Hourly rates for all staff roles; used to price UNIT_RATE labour items |
| 2 | `Level_of_Effort.csv` | PARAMETRIC | ~500 rows mapping (Execution, DeliverableID, RoleID) to EstimatedHours; 6 rows match DEL-019-01 | Estimated hours per role per deliverable; primary quantity source for labour items |
| 3 | `Assumed_Project_Parameters.csv` | PARAMETRIC | 19 parameters covering identity, location, contract, schedule, facility, equipment, plumbing, mechanical, currency, economics | Project context parameters; confirms CAD currency (PP-17), project identity, site location |
| 4 | `Fees_Permits_Insurance.csv` | PARAMETRIC/ALLOWANCE | 5 items covering bonding, insurance, and permits with RateMin/RateMax/RecommendedRate | Insurance premiums (FP-03, FP-04) are PKG-021 scope, not DEL-019-01; noted for boundary clarity |

## Document Sources (Deliverable Content)

| Document | Path | Key Content Extracted |
|---|---|---|
| `_CONTEXT.md` | `PKG-019_.../DEL-019-01_Prime-Contractor/_CONTEXT.md` | Deliverable ID, package, title, category, responsible party, scope, linked SOW/OBJ |
| `Datasheet.md` | `PKG-019_.../DEL-019-01_Prime-Contractor/Datasheet.md` | Identification, attributes (designation details, regulatory framework, insurance requirements, safety evaluation criteria, hazard categories), conditions, construction components, references |
| `Specification.md` | `PKG-019_.../DEL-019-01_Prime-Contractor/Specification.md` | 11 requirements (REQ-019-01-001 through REQ-019-01-011), standards, verification methods, documentation artifacts |
| `Guidance.md` | `PKG-019_.../DEL-019-01_Prime-Contractor/Guidance.md` | 5 principles, considerations (COR, WCB timing, landfill context, safety officer qualifications, county oversight), trade-offs |
| `Procedure.md` | `PKG-019_.../DEL-019-01_Prime-Contractor/Procedure.md` | 3 phases (Proposal Prep, Post-Award Pre-Mobilization, Active Project), 14 steps, verification checklist, records table |

## Decomposition Source

| Document | Path | Key Content Extracted |
|---|---|---|
| `WDMLRL_Decomposition_Claude.md` | `_Decomposition/WDMLRL_Decomposition_Claude.md` | PKG-019 definition, DEL-019-01 entry (covers SOW-0083, supports OBJ-007), scope ledger row for SOW-0083 |
