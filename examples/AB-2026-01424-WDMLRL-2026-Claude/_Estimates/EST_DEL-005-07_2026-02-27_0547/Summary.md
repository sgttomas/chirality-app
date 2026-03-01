# Estimate Summary — DEL-005-07 Civil Specification

**RunID:** EST_DEL-005-07_2026-02-27_0547
**Date:** 2026-02-27
**Currency:** CAD
**Basis of Estimate:** PARAMETRIC

---

## Basis of Estimate Used

| Field | Value |
|---|---|
| Primary Method | PARAMETRIC (Level-of-Effort hours x Staff Hourly Rates) |
| LOE Source | Level_of_Effort.csv — 4 role assignments for DEL-005-07 |
| Rate Source | Professional_Staff_Rates.csv — hourly rates in CAD |
| Fallback Applied | None required — all items priced from primary sources |
| Mixed Methods | Not triggered — all lines use PARAMETRIC |
| Alternative Cross-Check | Professional_Design_Fees.csv (DF-05: Civil design fee at 1.0% of construction value) — not applied because construction value is not yet established |

---

## Totals by Package

| WBS_PackageID | Currency | Amount_Total | Hours |
|---|---|---|---|
| PKG-005 | CAD | $9,960 | 70 |

## Totals by Deliverable

| WBS_DeliverableID | Name | Currency | Amount_Total | Hours |
|---|---|---|---|---|
| DEL-005-07 | Civil Specification | CAD | $9,960 | 70 |

## Totals by CBS (Cost Breakdown Structure)

| CBS | Currency | Amount_Total | Hours | Lines |
|---|---|---|---|---|
| Management | CAD | $1,530 | 10 | 4 |
| Design | CAD | $8,430 | 60 | 16 |
| **TOTAL** | **CAD** | **$9,960** | **70** | **20** |

## Labour Breakdown

| Role | RoleID | Hours | Rate ($/hr) | Amount (CAD) | % of Total |
|---|---|---|---|---|---|
| Project Manager | R-01 | 6 | 165 | 990 | 9.9% |
| Cost Estimator | R-08 | 4 | 135 | 540 | 5.4% |
| BIM Technician | R-13 | 18 | 95 | 1,710 | 17.2% |
| Civil Engineer | R-17 | 42 | 160 | 6,720 | 67.5% |
| **Total** | | **70** | | **$9,960** | **100.0%** |

---

## Key Warnings and Coverage Gaps

1. **No material or equipment costs included.** DEL-005-07 is a design services deliverable (Civil Specification authoring). No physical materials, equipment procurement, or subcontractor costs are within scope. Construction costs for civil works are estimated separately under PKG-018 (Construction).
2. **Fee-based cross-check not completed.** The Professional_Design_Fees.csv provides a parametric fee percentage (DF-05: 1.0% of construction value for civil design), but no construction value has been established for this project. This cross-check is deferred.
3. **Confidence level is MEDIUM for all lines.** All source rates and LOE hours carry MEDIUM confidence per the pricing source files. This is consistent with a parametric estimate at the specification stage.
4. **P.Eng. review assumed within Civil Engineer hours.** The LOE model does not separately allocate P.Eng. review time. Assumption A-003 treats the Civil Engineer (R-17) as the P.Eng. of Record performing the internal quality review and IFC stamp.
5. **Scope exclusions.** Downstream civil drawing deliverables (DEL-005-01 through DEL-005-06) and civil construction packages (PKG-018) are not included in this estimate. Only the civil specification document (DEL-005-07) is scoped.
6. **Geotechnical dependency.** The specification includes placeholder values dependent on the geotechnical report (DEL-008-01). If geotechnical data requires specification revision after initial issue, additional engineering hours may be required beyond this estimate.
7. **Specification scope is comprehensive.** DEL-005-07 covers 17 requirements (REQ-CIVIL-001 through REQ-CIVIL-017), including drainage, driving surface, pads, ESC, environmental compliance, submittals, and warranty criteria. The 42-hour Civil Engineer allocation covers all these specification sections.
