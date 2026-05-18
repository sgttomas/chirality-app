# Source Index — EST_DEL-019-04_2026-02-27_0630

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `Professional_Staff_Rates.csv` | RATE_TABLE | 25 roles with RoleID, HourlyRate_CAD, Basis=PARAMETRIC, Confidence=MEDIUM | Hourly rates for all staff roles; used to price UNIT_RATE labour items |
| 2 | `Level_of_Effort.csv` | PARAMETRIC | ~500 rows mapping (Execution, DeliverableID, RoleID) to EstimatedHours; 6 rows match DEL-019-04 | Estimated hours per role per deliverable; primary quantity source for labour items |
| 3 | `Assumed_Project_Parameters.csv` | PARAMETRIC | 19 parameters covering identity, location, contract, schedule, facility, equipment, plumbing, mechanical, currency, economics | Project context parameters; confirms CAD currency (PP-17), project identity, completion deadline (PP-07) |
| 4 | `Fees_Permits_Insurance.csv` | PARAMETRIC/ALLOWANCE | 5 items covering bonding, insurance, and permits with RateMin/RateMax/RecommendedRate | Not directly applicable to DEL-019-04; no fees, permits, or insurance costs within QC Management scope |

## Document Sources (Deliverable Content)

| Document | Path | Key Content Extracted |
|---|---|---|
| `_CONTEXT.md` | `PKG-019_.../DEL-019-04_QC-Management/_CONTEXT.md` | Deliverable ID, package, title, category (Management), responsible party (PM / QC Manager), scope (QC program implementation and oversight), linked SOW-0089, linked OBJ-001/OBJ-007, success criteria |
| `Datasheet.md` | `PKG-019_.../DEL-019-04_QC-Management/Datasheet.md` | Identification (regulatory basis, upstream dependencies, downstream handoff to PKG-020), attributes (program scope, QC Plan status, inspection coverage, deficiency standard, testing, County verification right, evaluation weighting 5%), conditions (Prime Contractor designation, Alberta OH&S, deficiency holdback, guarantee period, lien holdback, IFC conformance), construction elements (QC Plan, inspection schedule, testing protocols, deficiency tracking, subcontractor oversight, record retention) |
| `Specification.md` | `PKG-019_.../DEL-019-04_QC-Management/Specification.md` | 18 requirements (REQ-QC-01 through REQ-QC-18) covering QC Plan, inspection schedule, County attendance, inspection requests, testing protocols, deficiency tracking, subcontractor oversight, QC reporting, IFC conformance, Safety Codes compliance, QC Manager qualifications, guarantee period, approval authority, test method standards, KPIs, conformance determination, third-party lab qualifications, inspection personnel competency; standards table; verification matrix; documentation list (12 artifact types) |
| `Guidance.md` | `PKG-019_.../DEL-019-04_QC-Management/Guidance.md` | 6 principles (prevention over detection, County visibility, subcontractor scope, deficiency loop closure, weekly meeting cadence, IFC baseline), considerations (upstream sequencing, phase alignment, Safety Codes interface, guarantee period linkage, design-build accountability, dispute resolution, onboarding/training, standardized report format), trade-offs (inspection frequency, notification lead time, tracking tool, QC Plan scope, severity approach, third-party testing), conflict table (2 conflicts: CONF-001 inspection coordination chain, CONF-002 QC Plan approval authority) |
| `Procedure.md` | `PKG-019_.../DEL-019-04_QC-Management/Procedure.md` | 3 phases (A: Program Establishment — 9 steps, B: Ongoing Operations — 10 steps, C: Construction Completion — 5 steps), prerequisites (DEL-019-01, DEL-019-02, QC Manager assignment, IFC drawings), verification checklist (24 items), records table (16 record types with custodian and retention period) |

## Decomposition Source

| Document | Path | Key Content Extracted |
|---|---|---|
| `WDMLRL_Decomposition_Claude.md` | `_Decomposition/WDMLRL_Decomposition_Claude.md` | PKG-019 definition (Construction Management & OH&S), DEL-019-04 entry (QC-Management, covers SOW-0089, supports OBJ-001/OBJ-007), scope ledger row for SOW-0089, objective coverage matrix (OBJ-001 and OBJ-007 both map to PKG-019) |
