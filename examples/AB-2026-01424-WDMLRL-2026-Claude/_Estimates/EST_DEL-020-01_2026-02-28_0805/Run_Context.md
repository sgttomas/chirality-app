# Run Context — EST_DEL-020-01_2026-02-28_0805

| Field | Value |
|---|---|
| **RunID** | EST_DEL-020-01_2026-02-28_0805 |
| **AsOf** | 2026-02-28T08:05:00-07:00 |
| **Scope** | DEL-020-01 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-020-01_Commissioning) in 1 package (PKG-020 Commissioning & Closeout) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv; Optional_Items_Pricing.csv; Fees_Permits_Insurance.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-020-01 |
| **PriorSnapshot** | EST_DEL-020-01_2026-02-27_0700 |
| **Warnings** | None |

## Resolved Price Source Paths

1. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`
2. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
3. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`
4. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Optional_Items_Pricing.csv`
5. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Fees_Permits_Insurance.csv`

## Documents Read

| Document | Status |
|---|---|
| DEL-020-01 _CONTEXT.md | Read |
| DEL-020-01 Datasheet.md | Read |
| DEL-020-01 Specification.md | Read |
| DEL-020-01 Guidance.md | Read |
| DEL-020-01 Procedure.md | Read |
| Decomposition (WDMLRL_Decomposition_Claude.md) | Read |

## Changes from Prior Snapshot (EST_DEL-020-01_2026-02-27_0700)

1. **DL-020-01-011 (Crane load testing):** Resolved from TBD to $6,000 using Fees_Permits_Insurance.csv FP-09 recommended rate.
2. **DL-020-01-018 (Safety Code inspection coordination):** Resolved from TBD to $3,500 using Fees_Permits_Insurance.csv FP-10 recommended rate.
3. **Price source added:** Fees_Permits_Insurance.csv added to PRICE_SOURCES list.
4. **Total updated:** $11,290 -> $20,790 (+$9,500 from resolved TBDs).
