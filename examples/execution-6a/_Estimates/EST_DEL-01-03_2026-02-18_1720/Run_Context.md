# Run Context

## Run Identity

| Field | Value |
|---|---|
| RunID | EST_DEL-01-03_2026-02-18_1720 |
| AsOf | 2026-02-18T17:20:03Z |
| Agent | ESTIMATING (Type 2) |

## Brief Inputs (Resolved)

| Parameter | Value |
|---|---|
| SCOPE | DEL-01-03 |
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/ |
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| DECOMPOSITION_PATH | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| DEPENDENCY_SOURCES | AUTO (resolved: Dependencies.csv found for DEL-01-03) |
| PRICE_SOURCES | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| OUTPUT_LABEL | DEL-01-03 |
| UPDATE_LATEST_POINTER | FALSE |
| ALLOW_MIXED_METHODS | FALSE |
| FALLBACK_POLICY | STRICT |
| ROUNDING | DOLLAR |

## Scope Resolved Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (priced) | 1 |
| Deliverables blocked | 0 |
| Deliverables with partial pricing | 1 (labour priced; training costs and PPE/signage supplies have no pricing source) |

## Scope Resolution

| DeliverableID | PackageID | Name | Path | InScope |
|---|---|---|---|---|
| DEL-01-03 | PKG-001 | Health & Safety (Prime Contractor) Plan | PKG-001_.../DEL-01-03_Health & Safety (Prime Contractor) Plan | TRUE |

## CBS Mapping Rule

No explicit CBSHint was provided in the decomposition for DEL-01-03. The CBS codes used in this estimate are derived deterministically as follows:

- **CBS-LABOUR-SAFETY**: Labour hours for Safety Officer role (R-20), directly supporting H&S plan development and site safety management.
- **CBS-LABOUR-ADMIN**: Labour hours for Administrative / Document Control role (R-24), supporting safety documentation filing.
- **CBS-TRAINING**: Training costs (orientation, site-specific training). No pricing source available under STRICT policy; marked TBD.
- **CBS-SUPPLIES**: PPE and signage supplies. No pricing source available under STRICT policy; marked TBD.

These CBS codes are project-specific labels applied by the estimating agent. They are not sourced from a formal CBS standard.

## Price Source Resolution

| Source File | Type | Status | Supports |
|---|---|---|---|
| Professional_Staff_Rates.csv | Rate table | LOADED | Hourly rates by role (31 roles); R-20 Safety Officer = $110/hr CAD; R-24 Admin/Doc Control = $80/hr CAD |
| Level_of_Effort.csv | Level of effort / hours table | LOADED | Estimated hours by deliverable and role; DEL-01-03 rows: R-20 = 60h, R-24 = 8h |
| Assumed_Project_Parameters.csv | Project parameters | LOADED | Duration, area, quantity assumptions; PP-01 construction duration = 18 months |

## Warnings

- [WARNING] PARTIAL_PRICING: Brief cost drivers include "training costs" and "PPE/signage supplies" but no pricing source provides unit rates or quantities for these items. Under STRICT fallback policy, amounts are TBD.
- [WARNING] LOE_BASIS_MISMATCH: Level_of_Effort.csv records Basis=PARAMETRIC for its hour estimates, but this run uses BASIS_OF_ESTIMATE=RATE_TABLE. The hours are treated as quantity inputs (Qty) and the rates from Professional_Staff_Rates.csv are the pricing basis. This is consistent with RATE_TABLE method: Qty x UnitRate = Amount. See Decision_Log.md DEC-EST-001.
