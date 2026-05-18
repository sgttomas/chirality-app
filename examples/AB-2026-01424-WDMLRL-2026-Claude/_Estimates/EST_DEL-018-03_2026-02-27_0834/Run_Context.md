# Run_Context — EST_DEL-018-03_2026-02-27_0834

## Run Identity

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-018-03_2026-02-27_0834 |
| **AsOf** | 2026-02-27T08:34:00Z |
| **Scope** | DEL-018-03 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-018-03 — Gravel Driving Surface), 1 package (PKG-018 — Sitework & Civil Construction) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-018-03 |

## PRICE_SOURCES (resolved)

| # | Path | Type |
|---|------|------|
| 1 | PriceSources/Professional_Staff_Rates.csv | Rate table — professional staff hourly rates |
| 2 | PriceSources/Level_of_Effort.csv | Parametric — estimated hours by role per deliverable |
| 3 | PriceSources/Assumed_Project_Parameters.csv | Reference — project parameters and assumptions |
| 4 | PriceSources/Earthwork_Civil_Rates.csv | Rate table — earthwork unit rates |
| 5 | PriceSources/Paving_Surfacing_Rates.csv | Rate table — paving and surfacing unit rates |
| 6 | PriceSources/Underground_Utility_Rates.csv | Rate table — underground utility unit rates |
| 7 | PriceSources/Construction_Labour_Rates.csv | Rate table — construction trade labour rates |

All paths relative to: `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/`

## DECOMPOSITION_PATH

`_Decomposition/WDMLRL_Decomposition_Claude.md`

## DELIVERABLE_PATH

`PKG-018_Sitework & Civil Construction/1_Working/DEL-018-03_Driving-Surface/`

## Documents Read

| Document | Status |
|----------|--------|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |

## Warnings

- W-01: Gravel aggregate is Owner-supplied (SOW-0203); material procurement cost excluded from this estimate per RFP §3.3.1.
- W-02: Full driving surface area extent is TBD pending civil design (DEL-005-04). Only one gravel pad area (~60' x 130') is readable from the conceptual drawings. Quantity assumptions are based on an estimated total driving surface area (see Assumptions_Log.md ASM-002).
- W-03: Gravel depth/thickness is TBD pending civil specification (DEL-005-07). A parametric assumption of 400 mm compacted depth is used (see ASM-003).
- W-04: Compaction standard is TBD pending civil specification (DEL-005-07).
- W-05: Several items rely on parametric assumptions rather than firm design values. Confidence is LOW to MEDIUM across most construction line items.
