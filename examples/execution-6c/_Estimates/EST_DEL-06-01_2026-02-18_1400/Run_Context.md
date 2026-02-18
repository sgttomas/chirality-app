# Run Context — EST_DEL-06-01_2026-02-18_1400

## Run Identification

| Field | Value |
|-------|-------|
| RunID | EST_DEL-06-01_2026-02-18_1400 |
| AsOf | 2026-02-18T14:00:00 |
| Agent | ESTIMATING (Type 2 Task Agent) |

## Brief Inputs (as provided)

| Parameter | Value |
|-----------|-------|
| SCOPE | DEL-06-01 |
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates |
| BASIS_OF_ESTIMATE | RATE_TABLE (per BOE Section 4, PKG-07 table) |
| CURRENCY | CAD |
| DECOMPOSITION_PATH | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md |
| DEPENDENCY_SOURCES | AUTO |
| PRICE_SOURCES | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| OUTPUT_LABEL | EST_DEL-06-01 |
| UPDATE_LATEST_POINTER | FALSE |
| FALLBACK_POLICY | STRICT |
| ALLOW_MIXED_METHODS | FALSE |
| ROUNDING | DOLLAR |

## Scope Resolution Summary

| Metric | Value |
|--------|-------|
| Deliverables in scope | 1 |
| Deliverables estimated | 1 |
| Deliverables blocked | 0 |
| Deliverables excluded | 0 |

## Resolved Paths

| Resource | Resolved Path |
|----------|---------------|
| Decomposition | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md |
| Dependencies (AUTO) | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-07_Commissioning, Closeout & Warranty/1_Working/DEL-06-01_CommissioningTrainingCloseoutWarrantyNarrative/Dependencies.csv |
| Staff Rates | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv |
| Level of Effort | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv |
| Project Parameters | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv |

## CBS Mapping Rule

CBS codes are assigned using a deterministic mapping: `CBS = PROPOSAL_PRODUCTION.{RoleCategory}` where RoleCategory is derived from the `Category` column of Professional_Staff_Rates.csv. This groups all proposal production costs by role category (Management, Construction, Administrative) rather than by construction trade.

## Warnings

- None.

---

**END OF RUN CONTEXT**
