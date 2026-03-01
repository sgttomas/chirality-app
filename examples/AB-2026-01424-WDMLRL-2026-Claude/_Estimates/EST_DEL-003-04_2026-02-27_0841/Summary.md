# Estimate Summary — DEL-003-04 Exhaust System Plans

**RunID:** EST_DEL-003-04_2026-02-27_0841
**Date:** 2026-02-27
**Basis of Estimate:** PARAMETRIC
**Currency:** CAD
**Scope:** DEL-003-04 (Exhaust System Plans) within PKG-003 (Mechanical Design)

---

## Basis of Estimate Used

| Field | Value |
|---|---|
| Primary method | PARAMETRIC — Level of Effort (hours) x Professional Staff Rates ($/hr) |
| Pricing sources | Level_of_Effort.csv (hours per role), Professional_Staff_Rates.csv (hourly rates) |
| Fallback applied | None required; all items priced from primary sources |
| Mixed methods | Not used; all lines are PARAMETRIC |

---

## Totals by Deliverable

| Deliverable | Description | Amount (CAD) |
|---|---|---|
| DEL-003-04 | Exhaust System Plans | **$18,810.00** |

---

## Totals by CBS (Cost Breakdown Structure)

| CBS | Description | Amount (CAD) | % of Total |
|---|---|---|---|
| Design-Management | Project Manager + Cost Estimator | $1,530.00 | 8.1% |
| Design-Production | BIM Technician (modeling and sheet production) | $3,420.00 | 18.2% |
| Design-Engineering | Mechanical Engineer (all design tasks) | $13,860.00 | 73.7% |
| **TOTAL** | | **$18,810.00** | **100.0%** |

---

## Totals by Role

| RoleID | Role | Hours | Rate ($/hr) | Amount (CAD) | % of Total |
|---|---|---|---|---|---|
| R-01 | Project Manager | 6 | $165.00 | $990.00 | 5.3% |
| R-08 | Cost Estimator | 4 | $135.00 | $540.00 | 2.9% |
| R-13 | BIM Technician | 36 | $95.00 | $3,420.00 | 18.2% |
| R-15 | Mechanical Engineer | 84 | $165.00 | $13,860.00 | 73.7% |
| | **TOTAL** | **130** | | **$18,810.00** | **100.0%** |

---

## Key Warnings and Coverage Gaps

1. **P.Eng. stamp cost included in Mechanical Engineer hours (ASM-003):** The P.Eng. review and stamp is assumed to be performed by the same Mechanical Engineer (R-15) whose 84 hours are already estimated. If an external P.Eng. reviewer is required, an additional cost line would be needed.

2. **Sub-task hour breakdown is TBD:** The 84 Mechanical Engineer hours are allocated as a lump total from the LOE model. The breakdown across individual design tasks (REQ-001 through REQ-010, code review, coordination, IFC production, preliminary design) is not specified in the source data. Items ITEM-004 through ITEM-015 capture the sub-tasks but individual hour allocations are TBD.

3. **No material or equipment costs included:** This estimate covers professional design services only. Physical exhaust system components (fans, ductwork, hose reels, dampers) are construction costs not within the scope of this design deliverable estimate.

4. **Rates are MEDIUM confidence:** All hourly rates are parametric estimates, not contracted rates.

5. **Wash bay scope boundary unresolved (CFT-001):** The estimate assumes wash bay exhaust design is in scope of DEL-003-04 (per Guidance CFT-001 proposal). If this scope is reassigned to DEL-003-02, the hour allocation may change.

6. **Fee-percentage cross-check not performed:** The Professional_Design_Fees.csv suggests 1.6% of construction value for mechanical design fees. Without a construction value estimate, this cross-check cannot be completed at this time.
