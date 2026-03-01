# Run Context — EST_DEL-003-05_2026-02-27_0833

| Field | Value |
|---|---|
| **RunID** | EST_DEL-003-05_2026-02-27_0833 |
| **AsOf** | 2026-02-27T08:33Z |
| **Scope** | DEL-003-05 |
| **ScopeResolvedSummary** | 1 deliverable (Mechanical Equipment Schedule), 1 package (PKG-003 Mechanical Design) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Professional_Design_Fees.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **OUTPUT_LABEL** | DEL-003-05 |
| **Rounding** | NONE (default) |
| **RUN_TIMESTAMP** | 2026-02-27T08:33Z |

## Resolved Paths

| Input | Resolved Path |
|---|---|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates |
| DELIVERABLE_PATH | PKG-003_Mechanical Design/1_Working/DEL-003-05_Equipment-Schedule |
| Professional_Staff_Rates.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv |
| Level_of_Effort.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv |
| Assumed_Project_Parameters.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv |
| Professional_Design_Fees.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv |

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |

## Warnings

- W-001: All mechanical equipment performance values (capacities, airflows, etc.) are TBD in the deliverable documents pending DEL-003-06 Mechanical Calculation Package. Equipment quantities are known but unit procurement costs cannot be determined from available price sources (professional labour rates only).
- W-002: This estimate covers professional design services labour only. Construction material/equipment procurement costs are excluded from these price sources.
- W-003: The Professional_Design_Fees.csv provides percentage-based design fees (DF-03: Mechanical design fee 1.0-2.2%, recommended 1.6% of construction value) as an alternative pricing method, but construction value is not established; parametric LOE method used instead.
