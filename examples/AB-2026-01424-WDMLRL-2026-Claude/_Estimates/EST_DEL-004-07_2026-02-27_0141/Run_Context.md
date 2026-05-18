# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-004-07_2026-02-27_0141 |
| **AsOf** | 2026-02-27 08:41 UTC |
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
| **Warnings** | Multiple TBD quantities in Datasheet (camera counts, cable types, antenna points); scope boundary for Old North Shop low-voltage is TBD |

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
