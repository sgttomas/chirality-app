# Estimate Summary — DEL-003-01 Preliminary Mechanical Design

**RunID:** EST_DEL-003-01_2026-03-26_1400
**Date:** 2026-03-26
**Currency:** CAD
**Basis of Estimate:** RATE_TABLE
**Prior Snapshot:** EST_DEL-003-01_2026-02-26_2232 ($10,170 CAD)
**Refresh Trigger:** SCA-001 (Addenda 2, 3, 4)

---

## Basis of Estimate Used

| Field | Value |
|---|---|
| Primary Method | RATE_TABLE (Level-of-Effort hours x Staff Hourly Rate Table) |
| LOE Source | Level_of_Effort.csv (PS-LOE) — 4 role assignments for DEL-003-01 |
| Rate Source | Professional_Staff_Rates.csv (PS-STAFF) — hourly rates in CAD |
| Fallback Applied | None required — all items priced from primary rate table sources |
| Mixed Methods | Not triggered — all lines use RATE_TABLE |
| Alternative Cross-Check | Professional_Design_Fees.csv (DF-03: Mechanical design fee at 1.6% of construction value) — not applied because construction value is not yet established |

---

## SCA-001 Impact on This Estimate

| Change | Effect |
|---|---|
| Gas supply parameters defined (2" PVC, 50 PSI; Add. 3, Q8) | Resolves prior information gap C-001. No change to design effort or cost. |
| Gas pipeline relocation is County responsibility | Not in DEL-003-01 scope. No cost impact. |
| **Net change vs prior estimate** | **$0 (unchanged at $10,170 CAD)** |

---

## Totals by Package

| WBS_PackageID | Currency | Amount_Total | Hours |
|---|---|---|---|
| PKG-003 | CAD | $10,170 | 70 |

## Totals by Deliverable

| WBS_DeliverableID | Name | Currency | Amount_Total | Hours |
|---|---|---|---|---|
| DEL-003-01 | Preliminary Mechanical Design | CAD | $10,170 | 70 |

## Totals by CBS (Cost Breakdown Structure)

| CBS | Description | Currency | Amount_Total | Hours | Lines |
|---|---|---|---|---|---|
| CBS-01 | Professional Services > Design & Engineering | CAD | $8,640 | 60 | 8 |
| CBS-02 | Professional Services > Project Management | CAD | $1,530 | 10 | 4 |
| **TOTAL** | | **CAD** | **$10,170** | **70** | **12** |

## Labour Breakdown

| Role | RoleID | Hours | Rate ($/hr) | Amount (CAD) | % of Total |
|---|---|---|---|---|---|
| Project Manager | R-01 | 6 | 165 | 990 | 9.7% |
| Cost Estimator | R-08 | 4 | 135 | 540 | 5.3% |
| BIM Technician | R-13 | 18 | 95 | 1,710 | 16.8% |
| Mechanical Engineer | R-15 | 42 | 165 | 6,930 | 68.1% |
| **Total** | | **70** | | **$10,170** | **100.0%** |

---

## Key Warnings and Coverage Gaps

1. **No material or equipment costs included.** DEL-003-01 is a design services deliverable (Design Presentation). No physical materials, equipment procurement, or subcontractor costs are within scope.
2. **Fee-based cross-check not completed.** The Professional_Design_Fees.csv provides a parametric fee percentage (DF-03: 1.6% of construction value for mechanical design), but no construction value has been established for this project. This cross-check is deferred.
3. **Confidence level is MEDIUM for all lines.** All source rates and LOE hours carry MEDIUM confidence per the pricing source files. This is consistent with a rate-table estimate at the preliminary design stage.
4. **P.Eng. review assumed within Mechanical Engineer hours.** The LOE model does not separately allocate P.Eng. review time. Assumption A-003 treats the Mechanical Engineer (R-15) as the P.Eng. of Record performing the preliminary design direction review.
5. **Scope exclusions:** Downstream deliverables (DEL-003-02 through DEL-003-07) are not included in this estimate. Only the preliminary design presentation (DEL-003-01) is scoped.
6. **Gas supply parameters now resolved.** The prior estimate flagged natural gas availability (C-001) as TBD. Addendum 3, Q8 now confirms 2-inch PVC pipe at 50 PSI constant pressure. This does not change design effort hours but removes an information blocker for downstream heating system sizing.
