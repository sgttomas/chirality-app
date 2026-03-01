# Run_Context.md

## Run Identity

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-009-03_2026-02-27_0700 |
| **AsOf** | 2026-02-27T07:00:00-07:00 |
| **Scope** | DEL-009-03 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-009-03 Safety Code Permits) in 1 package (PKG-009 Permitting & Regulatory Compliance) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-009-03 |

## Resolved Paths

| Input | Resolved Path |
|-------|---------------|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates |
| Snapshot | _Estimates/EST_DEL-009-03_2026-02-27_0700/ |
| DELIVERABLE_PATH | PKG-009_Permitting & Regulatory Compliance/1_Working/DEL-009-03_Safety-Code-Permits |
| Price Source 1 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv |
| Price Source 2 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv |
| Price Source 3 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv |

## Documents Read

| Document | Status |
|----------|--------|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |

## Warnings

- LOE data for DEL-009-03 lists only R-01 (Project Manager, 6 hr) and R-08 (Cost Estimator, 4 hr). This appears to undercount the effort required for the 5-phase safety code permitting process described in the four documents. Additional roles (R-05 HSE Manager, R-22 Permitting Specialist) are not present in the LOE for this deliverable. Items have been priced using the LOE hours where available and PARAMETRIC estimates where the LOE is silent but the documents clearly describe discrete work activities.
- Permit fee costs are explicitly excluded from Proponent scope per RFP Section 3.3.1 (County pays fees). No permit fee line items are included.
- Several TBDs exist in the Datasheet (permit types, number of permits, accredited agency identity) which affect quantity certainty for permit application and inspection items.
