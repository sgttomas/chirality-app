# Run Context — EST_DEL-016-01_2026-02-27_0133

## Run Identity

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-016-01_2026-02-27_0133 |
| **AsOf** | 2026-02-27T01:33:00-07:00 |
| **Scope** | DEL-016-01 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-016-01: Overhead Cranes — Two 5-Tonne Units), 1 package (PKG-016: Crane & Lifting Equipment) |

## Configuration

| Parameter | Value |
|-----------|-------|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **OUTPUT_LABEL** | DEL-016-01 |
| **Rounding** | NONE (default) |

## Resolved Paths

| Path | Value |
|------|-------|
| **RUN_ROOT** | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude |
| **ESTIMATES_ROOT** | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md |
| **DELIVERABLE_PATH** | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-016_Crane & Lifting Equipment/1_Working/DEL-016-01_Overhead-Cranes |

## Price Sources (resolved)

| # | Path | Type | Notes |
|---|------|------|-------|
| 1 | .../PriceSources/Professional_Staff_Rates.csv | Rate table | 25 professional staff roles with hourly rates (CAD) |
| 2 | .../PriceSources/Level_of_Effort.csv | Parametric model | Estimated hours by deliverable and role |
| 3 | .../PriceSources/Assumed_Project_Parameters.csv | Parametric model | Project parameters including crane quantity (2), capacity (5 ton) |
| 4 | .../PriceSources/Equipment_Pricing.csv | Allowance table | Crane equipment pricing (EQ-01): $120k–$280k range, recommended $190k/each |
| 5 | .../PriceSources/Construction_Labour_Rates.csv | Rate table | 10 construction trade rates with burden multipliers |

## Documents Read

| Document | Status |
|----------|--------|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |
| Decomposition (PKG-016 section) | Read |

## Warnings

- W-001: Equipment pricing (EQ-01) is classified as ALLOWANCE with LOW confidence. The recommended price of $190,000/each has a wide range ($120k–$280k), contributing significant uncertainty.
- W-002: Multiple TBD attributes in Datasheet (crane span, hook height, runway length, voltage/amperage, duty class, applicable standards) mean the equipment specification is not yet finalized for procurement. Pricing is based on parametric allowance for a generic 5-tonne overhead crane.
- W-003: Construction labour for crane installation is estimated parametrically; actual hours depend on crane model selected and site conditions.
