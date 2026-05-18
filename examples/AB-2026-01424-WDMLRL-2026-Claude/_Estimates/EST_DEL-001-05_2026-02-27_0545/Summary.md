# Estimate Summary — DEL-001-05 Interior Elevations

**Snapshot:** EST_DEL-001-05_2026-02-27_0545
**As Of:** 2026-02-27
**Currency:** CAD
**Basis of Estimate:** PARAMETRIC

---

## Basis of Estimate Used

| Parameter | Value |
|---|---|
| Primary Method | PARAMETRIC (effort-based: hours x hourly rates) |
| Hours Source | Level_of_Effort.csv — DEL-001-05 rows (5 roles, 130 total hours) |
| Rate Source | Professional_Staff_Rates.csv — role hourly rates (CAD) |
| Fallback Policy | ALLOW_PARAMETRIC |
| Mixed Methods | TRUE (allowed but not exercised; all priced lines use PARAMETRIC) |
| Rounding | NONE |

---

## Totals by Deliverable

| Deliverable | Description | Amount (CAD) | Hours | Priced Lines | TBD Lines |
|---|---|---|---|---|---|
| DEL-001-05 | Interior Elevations | 19,200 | 130 | 5 | 1 |

---

## Totals by CBS Category

| CBS | Amount (CAD) | Line Count |
|---|---|---|
| Design-Labour | 17,670 | 3 |
| Management-Labour | 1,530 | 2 |
| Design-Coordination | 0 | 1 |
| Management-Admin | 0 | 1 |
| Design-QA | 0 | 2 |
| Design-Contingency | 0 | 1 |
| **TOTAL** | **19,200** | **10** |

---

## Totals by Role

| Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|
| R-11 Senior Architect | 54 | 180 | 9,720 |
| R-12 Architect | 42 | 135 | 5,670 |
| R-13 BIM Technician | 24 | 95 | 2,280 |
| R-01 Project Manager | 6 | 165 | 990 |
| R-08 Cost Estimator | 4 | 135 | 540 |
| **TOTAL** | **130** | — | **19,200** |

---

## Cross-Check: Fee-Based Method

For reference, an alternative pricing approach using Professional_Design_Fees.csv (DF-01: Architectural design fee at 4.5% of construction value) is available but requires a known construction value. Using the parametric building rate (PB-01: $285/sf for 13,000 sqft = $3,705,000 estimated construction value), the architectural design fee would be approximately $166,725 for the entire PKG-001 scope (11 deliverables). DEL-001-05 as one of 11 architectural deliverables would represent approximately $15,157 under a uniform allocation, which is within the same order of magnitude as the $19,200 effort-based estimate. This provides directional validation that the effort-based estimate is reasonable.

---

## Key Warnings and Coverage Gaps

1. **Post-IFC revision allowance (ITEM-010 / L-010):** Not priced ($0); scope is TBD pending construction phase. This is a known gap.
2. **Coordination and QA items (ITEM-006 through ITEM-009):** Priced at $0 because effort is embedded in the role-based labour line items. These are tracked as scope elements for completeness, not as separate cost items.
3. **Confidence level:** All priced lines are MEDIUM confidence per the parametric rate basis (+/- 20-30% accuracy per INDEX.md data quality statement).
4. **Scope note:** This estimate covers the design effort (professional services) to produce the Interior Elevations drawing set. It does not include construction costs for the items shown on the drawings (those are covered by construction packages PKG-010 through PKG-021).
