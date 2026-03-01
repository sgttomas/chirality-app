# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-004-07_2026-02-28_0810 |
| **AsOf** | 2026-02-28 08:10 UTC |
| **Scope** | DEL-004-07 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-004-07 Low-Voltage System Plans), 1 package (PKG-004 Electrical Design) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Professional_Design_Fees.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-004-07 |
| **PriorSnapshot** | EST_DEL-004-07_2026-02-27_0141 |
| **Warnings** | 1 residual TBD (LN-007 additional low-voltage systems); scope boundary for Old North Shop low-voltage is TBD |

## Price Sources Resolved

| Source File | Source Type | Notes |
|---|---|---|
| Professional_Staff_Rates.csv | Rate Table (Parametric) | 25 roles with hourly rates in CAD |
| Level_of_Effort.csv | Parametric Model (LOE) | Hours per role per deliverable; DEL-004-07 has 4 role assignments totaling 130 hours |
| Assumed_Project_Parameters.csv | Parametric Parameters | 19 project-level parameters including facility area, currency, schedule |
| Professional_Design_Fees.csv | Parametric Model (Fee %) | Discipline-level design fees as % of construction value; DF-04 Electrical = 1.6% recommended |

## Scope Resolution

- Deliverable: DEL-004-07 (Low-Voltage System Plans)
- Package: PKG-004 (Electrical Design)
- Discipline: Electrical Engineering
- Type: Drawing Set
- SOW Coverage: SOW-0014 (Complete final electrical design), SOW-0064, SOW-0065
- Objectives: OBJ-001, OBJ-003, OBJ-005
- All four production documents present: Datasheet.md, Specification.md, Guidance.md, Procedure.md

## Changes From Prior Snapshot

| Change | Detail |
|---|---|
| LN-005 resolved | Security camera wiring layout set to $0 — design effort in LN-004; camera hardware cost in PKG-015 (DEC-R01) |
| LN-006 resolved | 2-way radio antenna routing set to $0 — design effort in LN-004; antenna hardware cost in PKG-015 (DEC-R02) |
| LN-007 remains TBD | Additional low-voltage systems cannot be resolved; pending County confirmation of fire alarm/data/access control/intercom requirements |
| TBD count | Reduced from 3 to 1 |
| Priced total | Unchanged at $18,810.00 CAD |
