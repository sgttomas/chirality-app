# Summary — EST_DEL-001-11_2026-02-28_0803

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method | Level-of-Effort (hours) x Staff Hourly Rates + Fees/Permits allowances |
| Currency | CAD |
| Fallback Policy | ALLOW_PARAMETRIC |
| Mixed Methods | TRUE (allowed) |
| Rounding | NONE |

The estimate for DEL-001-11 (Architectural Specification) is computed using a parametric effort-based model. Professional staff hours are sourced from `Level_of_Effort.csv` (6 role-specific entries for DEL-001-11) and priced using hourly rates from `Professional_Staff_Rates.csv`. Regulatory fees and permit costs are sourced from `Fees_Permits_Insurance.csv` (FP-11 and FP-12). All LOE-based rate confidences are MEDIUM; fee/permit items are LOW confidence.

## Totals by Deliverable

| Deliverable | Description | Priced Amount (CAD) | TBD Lines | Total Lines |
|---|---|---|---|---|
| DEL-001-11 | Architectural Specification | 25,105 | 0 | 11 |

## Totals by CBS

| CBS Category | Amount (CAD) | Lines | Status |
|---|---|---|---|
| Professional Services -- Management | 1,530 | 3 | Priced |
| Professional Services -- Design | 8,835 | 4 | Priced |
| Professional Services -- Specialty | 2,240 | 1 | Priced |
| Professional Services -- Regulatory | 2,500 | 1 | Priced |
| Fees and Permits | 10,000 | 1 | Priced |
| **TOTAL** | **25,105** | **11** | **All priced** |

## Effort Summary

| RoleID | Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| R-01 | Project Manager | 6 | 165 | 990 |
| R-08 | Cost Estimator | 4 | 135 | 540 |
| R-11 | Senior Architect | 27 | 180 | 4,860 |
| R-12 | Architect | 21 | 135 | 2,835 |
| R-13 | BIM Technician | 12 | 95 | 1,140 |
| R-21 | Surveyor | 16 | 140 | 2,240 |
| | **Total effort** | **86** | | **12,605** |

## Non-Effort Items

| LineID | Description | Amount (CAD) | Source |
|---|---|---|---|
| DL-010 | P.Eng. stamp and AAAL review | 2,500 | FP-11 |
| DL-011 | Building permit -- Camrose County | 10,000 | FP-12 |
| | **Total non-effort** | | **12,500** |

## Grand Total Reconciliation

| Component | Amount (CAD) |
|---|---|
| Effort-based (86 hours) | 12,605 |
| Non-effort (fees/permits) | 12,500 |
| **Grand Total** | **25,105** |

## Key Notes

1. **All TBDs resolved** -- This snapshot resolves the 3 TBD items from the prior snapshot (EST_DEL-001-11_2026-02-26_2245): existing conditions survey (DL-006), P.Eng./AAAL stamp fees (DL-010), and building permit (DL-011).

2. **Existing conditions survey (DL-006)** -- Now priced at $2,240 using R-21 Surveyor at 16 hours (8 field + 8 data processing) from Level_of_Effort.csv line 583 and $140/hr from Professional_Staff_Rates.csv R-21. Confidence upgraded from LOW to MED.

3. **P.Eng. stamp / AAAL review (DL-010)** -- Priced at $2,500 using the recommended rate from Fees_Permits_Insurance.csv FP-11 (range $1,500-$4,000). Confidence remains LOW (fee amount may vary by issuance cycle complexity).

4. **Building permit (DL-011)** -- Priced at $10,000 using the recommended rate from Fees_Permits_Insurance.csv FP-12 (range $5,000-$15,000). Confidence remains LOW. Payment responsibility still subject to OI-003 resolution.

5. **Scope note** -- This estimate covers the *design professional services effort* to produce the Architectural Specification document (DEL-001-11). It does not cover the *construction cost* of the items specified (those are estimated under construction packages PKG-010 through PKG-018).

6. **Confidence** -- Effort-based lines (DL-001 through DL-006) are MEDIUM confidence (+/-20-30%). Fee/permit lines (DL-010, DL-011) are LOW confidence. Replace with actual contracted rates and confirmed fees when available.

## Cross-Check: Fee-Based Method

For reference, `Professional_Design_Fees.csv` (DF-01) suggests architectural design fees of 3.0%-6.0% of construction value (recommended 4.5%). Applying this cross-check requires a construction value estimate, which is outside this deliverable's scope. The effort-based total of $12,605 for professional services on the specification document alone (one of 11 deliverables in PKG-001) is directionally consistent with a fee-based approach when viewed as a fraction of total architectural design effort. The additional $12,500 for regulatory fees and permits represents pass-through costs not typically included in fee-based calculations.
