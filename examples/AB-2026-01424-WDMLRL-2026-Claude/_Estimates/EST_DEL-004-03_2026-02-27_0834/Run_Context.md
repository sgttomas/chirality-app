# Run Context — EST_DEL-004-03_2026-02-27_0834

| Field | Value |
|---|---|
| **RunID** | EST_DEL-004-03_2026-02-27_0834 |
| **AsOf** | 2026-02-27T08:34:00Z |
| **Scope** | DEL-004-03 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-004-03 Power Distribution Plans) in PKG-004 Electrical Design |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Professional_Design_Fees.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-004-03 |
| **Warnings** | None at input validation stage |

## Resolved Paths

- **RUN_ROOT:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude
- **ESTIMATES_ROOT:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates
- **DELIVERABLE_PATH:** PKG-004_Electrical Design/1_Working/DEL-004-03_Power-Plans
- **DECOMPOSITION_PATH:** _Decomposition/WDMLRL_Decomposition_Claude.md

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |

## Price Sources Indexed

| Source | Type | Status |
|---|---|---|
| Professional_Staff_Rates.csv | Rate Table (hourly rates by role) | Indexed — 25 roles |
| Level_of_Effort.csv | Parametric (hours by deliverable × role) | Indexed — 4 rows for DEL-004-03 |
| Assumed_Project_Parameters.csv | Parametric (project parameters) | Indexed — 19 parameters |
| Professional_Design_Fees.csv | Parametric (fee percentages) | Indexed — 5 disciplines; not used as primary method for this deliverable |
