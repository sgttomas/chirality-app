# Decision Log -- EST_DEL-08-01_2026-02-18_1400

## Defaults Applied

| ID | Decision | Rationale |
|---|---|---|
| DEC-EST-001 | Used `ESTIMATES_ROOT` as explicit tool root rather than deriving from `RUN_ROOT` | Both were provided; ESTIMATES_ROOT takes precedence per PROTOCOL when explicit. |
| DEC-EST-002 | CBS codes assigned as `PROF-{discipline}` based on role Category from Professional_Staff_Rates.csv | No CBSHint present in decomposition for DEL-08-01. Deterministic mapping: Construction category -> PROF-CM, Management category -> PROF-PM; R-17 Scheduler is Construction category but functionally scheduling, assigned PROF-SCHED for clarity. Documented in Run_Context.md. |
| DEC-EST-003 | Rounding applied at DOLLAR level: no rounding needed since all amounts are whole dollar values | All line computations (integer hours x integer rates) produce integer results. DOLLAR rounding has no effect on this run. |
| DEC-EST-004 | Confidence set to MED for all lines | Matches source confidence: Professional_Staff_Rates.csv rates are MEDIUM confidence; Level_of_Effort.csv hours are PARAMETRIC basis with MEDIUM implied accuracy (+/-20-30% per INDEX.md). |

## Scope Resolution Decisions

| ID | Decision | Rationale |
|---|---|---|
| DEC-EST-005 | Single deliverable DEL-08-01 resolved from SCOPE without expansion | SCOPE = "DEL-08-01" is a single deliverable ID; no package expansion needed. Confirmed in decomposition Section 8 and Level_of_Effort.csv. |

## Fallback Decisions

None. FALLBACK_POLICY = STRICT and no fallback was needed; all line items have direct basis evidence.
