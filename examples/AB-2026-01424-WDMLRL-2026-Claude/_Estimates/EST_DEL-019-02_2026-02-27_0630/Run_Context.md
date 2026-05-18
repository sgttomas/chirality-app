# Run Context — EST_DEL-019-02_2026-02-27_0630

| Field | Value |
|---|---|
| **RunID** | EST_DEL-019-02_2026-02-27_0630 |
| **AsOf** | 2026-02-27T06:30:00-07:00 |
| **Scope** | DEL-019-02 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-019-02_Weekly-Coordination) in PKG-019 (Construction Management & OH&S) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Fees_Permits_Insurance.csv |
| **DECOMPOSITION_PATH** | WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-019-02 |

## Resolved Paths

| Source | Path |
|---|---|
| Deliverable folder | `PKG-019_Construction Management & OH&S/1_Working/DEL-019-02_Weekly-Coordination/` |
| Decomposition | `_Decomposition/WDMLRL_Decomposition_Claude.md` |
| Staff rates | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` |
| Level of effort | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` |
| Project parameters | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` |
| Fees/permits/insurance | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Fees_Permits_Insurance.csv` |

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |

## Warnings

- LOE hours from Level_of_Effort.csv appear to represent total project hours for DEL-019-02 (a recurring weekly deliverable spanning ~9 months). The stated totals (38 hours combined) seem low for a weekly recurring activity. See QA_Report.md for details.
- Fees_Permits_Insurance.csv does not contain items directly attributable to DEL-019-02; no fees/permits/insurance line items generated for this deliverable.
