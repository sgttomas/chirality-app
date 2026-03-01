# Summary — EST_DEL-001-11_2026-02-26_2245

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method | Level-of-Effort (hours) x Staff Hourly Rates |
| Currency | CAD |
| Fallback Policy | ALLOW_PARAMETRIC |
| Mixed Methods | TRUE (allowed) |
| Rounding | NONE |

The estimate for DEL-001-11 (Architectural Specification) is computed using a parametric effort-based model. Professional staff hours are sourced from `Level_of_Effort.csv` (5 role-specific entries for DEL-001-11) and priced using hourly rates from `Professional_Staff_Rates.csv`. All rate confidences are MEDIUM (+/-20-30% accuracy).

## Totals by Deliverable

| Deliverable | Description | Priced Amount (CAD) | TBD Lines | Total Lines |
|---|---|---|---|---|
| DEL-001-11 | Architectural Specification | 10,365 | 3 | 11 |

## Totals by CBS

| CBS Category | Amount (CAD) | Lines | Status |
|---|---|---|---|
| Professional Services — Management | 1,530 | 3 | Priced |
| Professional Services — Design | 8,835 | 4 | Priced |
| Professional Services — Specialty | TBD | 1 | TBD (existing conditions survey) |
| Professional Services — Regulatory | TBD | 1 | TBD (P.Eng./AAAL stamp fees) |
| Fees and Permits | TBD | 1 | TBD (building permit) |
| **TOTAL (priced lines)** | **10,365** | **8** | |
| **TOTAL (all lines)** | **10,365 + TBD** | **11** | |

## Effort Summary

| RoleID | Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| R-01 | Project Manager | 6 | 165 | 990 |
| R-08 | Cost Estimator | 4 | 135 | 540 |
| R-11 | Senior Architect | 27 | 180 | 4,860 |
| R-12 | Architect | 21 | 135 | 2,835 |
| R-13 | BIM Technician | 12 | 95 | 1,140 |
| | **Total** | **70** | | **10,365** |

## Key Warnings and Coverage Gaps

1. **TBD: Existing Conditions Survey (ITEM-006 / DL-006)** — The Old North Shop existing conditions survey is identified in Procedure Step 2 as a prerequisite for renovation specification sections ARCH-040 through ARCH-044. No pricing source is available for survey logistics. This cost should be obtained via quote from a surveyor or included in a site investigation allowance.

2. **TBD: P.Eng. Stamp / AAAL Registration Fees (ITEM-010 / DL-010)** — Professional stamp fees for IFC issuance and potential AAAL registration confirmation (Guidance C-002) are not covered by the LOE-based price sources. These are typically nominal but should be confirmed.

3. **TBD: Building Permit Fees (ITEM-011 / DL-011)** — Permit application fees for Camrose County are not in the price sources. Payment responsibility (Owner vs. Proponent) is an open issue (OI-003 from INDEX.md).

4. **Scope note** — This estimate covers the *design professional services effort* to produce the Architectural Specification document (DEL-001-11). It does not cover the *construction cost* of the items specified (those are estimated under construction packages PKG-010 through PKG-018).

5. **Confidence** — All priced lines are MEDIUM confidence (+/-20-30%). Rates are parametric baselines; replace with actual contracted rates when available.

## Cross-Check: Fee-Based Method

For reference, `Professional_Design_Fees.csv` (DF-01) suggests architectural design fees of 3.0%-6.0% of construction value (recommended 4.5%). Applying this cross-check requires a construction value estimate, which is outside this deliverable's scope. The LOE-based total of $10,365 for the specification document alone (one of 11 deliverables in PKG-001) is directionally consistent with a fee-based approach when viewed as a fraction of total architectural design effort.
