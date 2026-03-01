# Run Context — EST_DEL-006-06_2026-02-27_0630

| Field | Value |
|---|---|
| **RunID** | EST_DEL-006-06_2026-02-27_0630 |
| **AsOf** | 2026-02-27T06:30:00-07:00 |
| **Scope** | DEL-006-06 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-006-06 — Plumbing Fixture Schedule), within PKG-006 Plumbing Design |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Professional_Design_Fees.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **OUTPUT_LABEL** | DEL-006-06 |
| **Rounding** | NONE (default) |
| **Warnings** | None |

## Scope Resolution

DEL-006-06 (Plumbing Fixture Schedule) is a Schedule-type deliverable under PKG-006 — Plumbing Design. Responsible party: Plumbing Engineer. The deliverable is a design artifact (tabular fixture schedule) produced by professional staff. The estimating approach is PARAMETRIC using professional staff rates and level-of-effort hours from the provided price sources.

## Price Sources Resolved

1. `Professional_Staff_Rates.csv` — hourly rates for 25 professional roles (CAD); basis: PARAMETRIC; confidence: MEDIUM
2. `Level_of_Effort.csv` — estimated hours per deliverable per role; basis: PARAMETRIC; 4 rows matched for DEL-006-06
3. `Assumed_Project_Parameters.csv` — project parameters (19 rows); used for context and cross-referencing
4. `Professional_Design_Fees.csv` — percentage-based design fees (5 rows); not directly used for this deliverable (LOE-based pricing preferred over fee-percentage for individual schedule deliverables)
