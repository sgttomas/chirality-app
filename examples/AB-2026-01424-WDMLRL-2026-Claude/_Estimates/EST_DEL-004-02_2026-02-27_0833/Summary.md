# Estimate Summary — DEL-004-02 Single-Line Diagram

**RunID:** EST_DEL-004-02_2026-02-27_0833
**Scope:** DEL-004-02 (Single-Line Diagram) — PKG-004 Electrical Design
**Basis of Estimate:** PARAMETRIC
**Currency:** CAD
**As Of:** 2026-02-27

---

## Basis of Estimate Used

| Parameter | Value |
|---|---|
| Method | PARAMETRIC — level-of-effort hours x professional staff hourly rates |
| Primary Sources | Level_of_Effort.csv (hours) + Professional_Staff_Rates.csv (rates) |
| Fallback Policy | ALLOW_PARAMETRIC |
| Mixed Methods | Allowed (TRUE) — all lines use PARAMETRIC; no mixed methods required |
| Confidence | MEDIUM (all source rates and hours are parametric, not firm quotes) |

---

## Total Estimate

| Category | Amount (CAD) |
|---|---|
| **Grand Total** | **$18,810.00** |

---

## Totals by CBS (Cost Breakdown Structure)

| CBS | Amount (CAD) | Line Count | Description |
|---|---|---|---|
| Management | $1,530.00 | 4 | Project Manager ($990) + Cost Estimator ($540) |
| Design | $17,280.00 | 12 | BIM Technician ($3,420) + Electrical Engineer ($13,860) |
| **Total** | **$18,810.00** | **16** | |

---

## Totals by Role

| RoleID | Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| R-01 | Project Manager | 6 | $165.00 | $990.00 |
| R-08 | Cost Estimator | 4 | $135.00 | $540.00 |
| R-13 | BIM Technician | 36 | $95.00 | $3,420.00 |
| R-16 | Electrical Engineer | 84 | $165.00 | $13,860.00 |
| | **Total** | **130** | | **$18,810.00** |

---

## Totals by Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Amount (CAD) |
|---|---|---|
| PKG-004 | DEL-004-02 | $18,810.00 |

---

## Key Warnings and Coverage Gaps

1. **All rates are PARAMETRIC (MEDIUM confidence).** No firm quotes or historical actuals were available for this deliverable. Rates are based on parametric models for Alberta design-build professional staff.

2. **Scope is professional design labor only.** DEL-004-02 is a Drawing Set deliverable; no materials, equipment, or construction labor are included. Construction-phase electrical costs are covered under PKG-015 (Electrical Installation).

3. **Multiple TBD items in source documents** (crane circuit ratings, overhead door motor ratings, system voltage, mechanical equipment ratings, exhaust fan ratings, ceiling fan ratings) may require additional design iterations beyond the estimated 84 Electrical Engineer hours if resolution is protracted. The LOE estimate assumes timely resolution of these items.

4. **Cross-check against fee-based model:** At a hypothetical $2.5M construction value, 1.6% electrical design fee = ~$40,000 for all PKG-004 deliverables. DEL-004-02 at $18,810 represents ~47% of that allocation for the SLD alone (one of 9 deliverables in PKG-004). This is reasonable given that the SLD is the foundational distribution hierarchy document and carries significant engineering content (84 Electrical Engineer hours), but the cross-check suggests the LOE hours may be on the high side. This is a note for human review, not a basis for adjustment.

---

## RUN_STATUS: WARNINGS

**Reason:** All items are priced (0% TBD amounts), but all pricing is based on PARAMETRIC sources at MEDIUM confidence. Multiple TBD design inputs exist in the source engineering documents that could affect actual effort.
