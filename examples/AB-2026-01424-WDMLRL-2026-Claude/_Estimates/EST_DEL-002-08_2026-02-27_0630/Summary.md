# Estimate Summary — DEL-002-08 Steel Plate Embedment Plan

**RunID:** EST_DEL-002-08_2026-02-27_0630
**AsOf:** 2026-02-27T06:30:00-07:00
**Basis of Estimate:** PARAMETRIC
**Currency:** CAD

---

## Basis of Estimate Used

- **Method:** PARAMETRIC — hours-based level-of-effort model
- **Rate Source:** Professional_Staff_Rates.csv (hourly rates by role, MEDIUM confidence)
- **Hours Source:** Level_of_Effort.csv (deliverable-specific hours allocation, MEDIUM confidence)
- **Fallback Policy:** ALLOW_PARAMETRIC (no fallback needed; primary parametric sources cover all priced items)
- **Mixed Methods:** Allowed (TRUE); all priced items use PARAMETRIC method

---

## Totals by Package / Deliverable / CBS

| WBS Package | WBS Deliverable | CBS | Amount (CAD) | Lines |
|---|---|---|---|---|
| PKG-002 | DEL-002-08 | Management | 1,530.00 | 2 |
| PKG-002 | DEL-002-08 | Design | 17,700.00 | 4 |
| **PKG-002** | **DEL-002-08** | **TOTAL** | **19,230.00** | **6** |

### Breakdown by Role

| Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|
| Project Manager (R-01) | 6 | 165.00 | 990.00 |
| Cost Estimator (R-08) | 4 | 135.00 | 540.00 |
| BIM Technician (R-13) | 36 | 95.00 | 3,420.00 |
| Structural Engineer (R-14) | 84 | 170.00 | 14,280.00 |
| **Total** | **130** | | **19,230.00** |

---

## Key Warnings and Coverage Gaps

1. **Peer review (LN-006 / ITM-006):** Independent peer review of IFC drawings is identified in Procedure (Enrichment D-003) as a best practice item, but no hours are allocated in Level_of_Effort.csv. Amount is TBD. If peer review is required, an additional 4-8 hours of Structural Engineer time (~$680-$1,360 CAD) would be a reasonable parametric estimate.

2. **Coordination review (LN-005 / ITM-005):** Inter-discipline coordination effort (Procedure Step 7) is captured within the Structural Engineer's 84-hour allocation. No incremental cost is added. If coordination requires dedicated time from other disciplines (Architect, Plumbing Engineer, Mechanical Engineer), those costs would be attributed to their respective deliverables.

3. **No material costs in scope:** DEL-002-08 is a design drawing set. Physical steel plate material, fabrication, and installation costs are scoped to DEL-011-02 (PKG-011 — Building Structure & Envelope construction).

4. **All rates at MEDIUM confidence:** Both hourly rates and hours allocations are marked MEDIUM confidence in source data. Actual hours may vary based on design complexity, number of coordination iterations, and geotech input timing.

---

## Scope Coverage

- **Deliverables included:** 1 (DEL-002-08 Steel Plate Embedment Plan)
- **Documents read:** 4 of 4 (Datasheet, Specification, Guidance, Procedure) — all present
- **Items extracted:** 6
- **Items priced:** 5 of 6 (83%)
- **Items TBD:** 1 (ITM-006 — peer review)
