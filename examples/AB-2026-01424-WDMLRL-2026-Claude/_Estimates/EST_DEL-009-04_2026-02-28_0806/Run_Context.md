# Run_Context.md

| Field | Value |
|---|---|
| **RunID** | EST_DEL-009-04_2026-02-28_0806 |
| **AsOf** | 2026-02-28T08:06:00-07:00 |
| **PriorSnapshot** | EST_DEL-009-04_2026-02-27_0730 |
| **Scope** | DEL-009-04 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-009-04 — Code Compliance Register & Inspection Log), 1 package (PKG-009 — Permitting & Regulatory Compliance) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | 1. Professional_Staff_Rates.csv, 2. Level_of_Effort.csv, 3. Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-009-04 |
| **Warnings** | 3 ALLOWANCE items (DL-015, DL-016, DL-017) carry LOW confidence as fixed allowances for operationally contingent activities. |

## What Changed from Prior Snapshot

| Change | Detail |
|---|---|
| LOE source expanded | Level_of_Effort.csv now includes 3 new role rows for DEL-009-04: R-06 QA/QC Lead 16h, R-09 Document Controller 12h, R-22 Permitting Specialist 20h (rows 580-582) |
| 10 TBDs resolved | DL-009 through DL-018 all previously had Amount=TBD; now 7 are PARAMETRIC-priced and 3 are ALLOWANCE-priced |
| Total priced amount | Increased from $3,090.00 (DL-001 through DL-008 + DL-019 + DL-020) to $10,670.00 |
| TBD count | Reduced from 10 to 0 |
| New roles priced | R-06 QA/QC Lead ($135/h), R-09 Document Controller ($75/h), R-22 Permitting Specialist ($125/h) |

## Resolved Paths

| Item | Path |
|---|---|
| ESTIMATES_ROOT | {RUN_ROOT}/_Estimates/ |
| Snapshot | _Estimates/EST_DEL-009-04_2026-02-28_0806/ |
| Prior Snapshot | _Estimates/EST_DEL-009-04_2026-02-27_0730/ |
| Deliverable | PKG-009_Permitting & Regulatory Compliance/1_Working/DEL-009-04_Code-Compliance-Register/ |
| Decomposition | _Decomposition/WDMLRL_Decomposition_Claude.md |
| Professional_Staff_Rates.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv |
| Level_of_Effort.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv |
| Assumed_Project_Parameters.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv |

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |
