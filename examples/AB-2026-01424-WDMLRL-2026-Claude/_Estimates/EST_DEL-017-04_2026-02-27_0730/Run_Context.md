# Run Context — EST_DEL-017-04_2026-02-27_0730

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-017-04_2026-02-27_0730 |
| **AsOf** | 2026-02-27T07:30:00-07:00 |
| **Scope** | DEL-017-04 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-017-04 — New Locker/Change Room), 1 package (PKG-017 — Existing Building Renovation, Old North Shop) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Interior_Architectural_Rates.csv, Construction_Labour_Rates.csv |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |

## Warnings

- Multiple Datasheet attributes are TBD (locker room footprint, workforce headcount, locker count, shower facilities, fixture counts, finish specifications, door fire rating). Quantities derived parametrically using assumptions documented in Assumptions_Log.md.
- Level_of_Effort.csv provides professional staff hours for DEL-017-04 but the Notes column reads "PKG-017 TBD -- TBD" indicating these are placeholder estimates.
- No explicit construction material quantities are provided in source documents; all material quantities are parametrically estimated from assumed room dimensions and industry norms.

## Resolved Paths

| Input | Resolved Path |
|-------|---------------|
| DELIVERABLE_PATH | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-017_Existing Building Renovation (Old North Shop)/1_Working/DEL-017-04_Locker-Room |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates |
| PRICE_SOURCE_1 | .../_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv |
| PRICE_SOURCE_2 | .../_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv |
| PRICE_SOURCE_3 | .../_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv |
| PRICE_SOURCE_4 | .../_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Interior_Architectural_Rates.csv |
| PRICE_SOURCE_5 | .../_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv |

## Documents Read

| Document | Status |
|----------|--------|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |
| WDMLRL_Decomposition_Claude.md | Read |
