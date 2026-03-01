# Run_Context.md

## Run Identity

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-009-02_2026-02-27_0600 |
| **AsOf** | 2026-02-27T06:00:00-07:00 |
| **Scope** | DEL-009-02 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-009-02 Building Permit Application & Approval) in 1 package (PKG-009 Permitting & Regulatory Compliance) |

## Configuration

| Parameter | Value |
|-----------|-------|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-009-02 |

## Resolved Paths

| Path | Value |
|------|-------|
| **RUN_ROOT** | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude |
| **ESTIMATES_ROOT** | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md |
| **DELIVERABLE_PATH** | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-009_Permitting & Regulatory Compliance/1_Working/DEL-009-02_Building-Permit |

## PRICE_SOURCES (resolved)

1. `PriceSources/Professional_Staff_Rates.csv` — 25 roles with hourly rates in CAD (PARAMETRIC basis, MEDIUM confidence)
2. `PriceSources/Level_of_Effort.csv` — LOE allocations by deliverable and role (PARAMETRIC basis); DEL-009-02 has 2 entries (R-01: 6 hrs, R-08: 4 hrs)
3. `PriceSources/Assumed_Project_Parameters.csv` — 18 project parameters including facility size, equipment, and currency

## Documents Read

| Document | Status |
|----------|--------|
| _CONTEXT.md | Read successfully |
| Datasheet.md | Read successfully |
| Specification.md | Read successfully |
| Guidance.md | Read successfully |
| Procedure.md | Read successfully |

## Warnings

- LOE data for DEL-009-02 is minimal (only 2 role entries: PM and Cost Estimator). Per Procedure.md, DEL-009-02 involves 5 phases and 19 steps spanning pre-application engagement, application assembly, submission, permit conditions documentation, and inspection coordination. The Permitting Specialist (R-22) role is conspicuously absent from the LOE despite being the most directly relevant role. Additional hours have been estimated parametrically based on procedure scope.
