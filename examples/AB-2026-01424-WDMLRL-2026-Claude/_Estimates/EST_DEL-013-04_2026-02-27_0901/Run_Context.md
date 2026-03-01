# Run Context — EST_DEL-013-04_2026-02-27_0901

| Field | Value |
|---|---|
| **RunID** | EST_DEL-013-04_2026-02-27_0901 |
| **AsOf** | 2026-02-27T09:01:00Z |
| **Scope** | DEL-013-04 |
| **ScopeResolvedSummary** | 1 deliverable: DEL-013-04 (Heavy Equipment Exhaust System) in PKG-013 (Mechanical & HVAC Installation) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Mechanical_System_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| **DECOMPOSITION_PATH** | {RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-013-04 |
| **DELIVERABLE_PATH** | {RUN_ROOT}/PKG-013_Mechanical & HVAC Installation/1_Working/DEL-013-04_Equipment-Exhaust |

## Warnings

- Multiple TBD items exist in engineering documents (exhaust volumes, fan sizing, filtration requirements, ductwork material spec, controls spec). These reduce estimate confidence.
- Mechanical_System_Rates.csv provides ALLOWANCE-basis rates; used under ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_PARAMETRIC.
- Exact quantity of exhaust hose drops per bay is TBD in Datasheet; assumed 4 drops (2 per bay) for parametric estimate per Appendix B (Shop) two drive-through repair bays.
- Filtration scope is subject to open question CQ-002; included as conditional line item.
