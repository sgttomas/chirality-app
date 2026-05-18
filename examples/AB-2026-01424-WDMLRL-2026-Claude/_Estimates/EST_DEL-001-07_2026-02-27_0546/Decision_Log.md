# Decision Log — EST_DEL-001-07_2026-02-27_0546

## Defaults Applied

| ID | Decision | Rationale |
|---|---|---|
| DEC-001 | Snapshot folder named `EST_DEL-001-07_2026-02-27_0546` per naming convention | OUTPUT_LABEL = DEL-001-07; timestamp at run start |
| DEC-002 | UPDATE_LATEST_POINTER = FALSE; no pointer file modified | Per brief instruction |
| DEC-003 | ROUNDING = NONE; all amounts carried at full precision | Per brief instruction |
| DEC-004 | FALLBACK_POLICY = ALLOW_PARAMETRIC; not exercised (all items priced via primary method) | Per brief instruction; no fallback was needed |
| DEC-005 | ALLOW_MIXED_METHODS = TRUE; not exercised (all methods are PARAMETRIC) | Per brief instruction; no method mixing occurred |

## Scope Resolution Decisions

| ID | Decision | Rationale |
|---|---|---|
| DEC-006 | Scope resolved to DEL-001-07 only (1 deliverable within PKG-001) | SCOPE parameter specified a single deliverable ID |
| DEC-007 | Items represent professional services effort (staff hours) to produce the schedule, not physical door/window material or installation costs | DEL-001-07 is a design-phase schedule deliverable; physical door/window procurement and installation are construction activities under PKG-011/PKG-012/PKG-017; pricing approach consistent with Level_of_Effort.csv which provides staff hours per deliverable |
| DEC-008 | CBS categories assigned as Management (PM, Cost Estimator) and Design (Senior Architect, Architect, BIM Technician) | Consistent with role categories in Professional_Staff_Rates.csv and CBS assignments used in other DEL-001-xx estimates (e.g., EST_DEL-001-01) |

## Pricing Decisions

| ID | Decision | Rationale |
|---|---|---|
| DEC-009 | All 5 items priced at PARAMETRIC method using LOE hours x staff rates | Level_of_Effort.csv provides 5 role entries for DEL-001-07 totalling 50 hrs; Professional_Staff_Rates.csv provides corresponding hourly rates; both sources are PARAMETRIC basis with MEDIUM confidence |
| DEC-010 | No additional items created beyond the 5 LOE role entries | LOE model covers all professional service activities for the deliverable; the Procedure steps (code analysis, Owner confirmation, tag list, schedule population, coordination, QA review, IFC issue) are captured within the role allocations rather than priced as separate activities |
