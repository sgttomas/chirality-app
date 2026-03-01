# Decision Log

**RunID:** EST_DEL-004-07_2026-02-27_0141

---

## DEC-001 — Primary Pricing Method: LOE x Rate Table

**Decision:** Price DEL-004-07 using Level_of_Effort.csv hours multiplied by Professional_Staff_Rates.csv hourly rates.

**Rationale:** The deliverable is a professional design services drawing set. The LOE model provides deliverable-specific hour allocations by role, and the rate table provides per-role hourly rates. This is the most direct parametric method available for a design deliverable.

**Alternative considered:** Professional_Design_Fees.csv (DF-04: 1.6% of construction value) — rejected as primary method because (a) construction value is not yet established, and (b) DF-04 covers the entire PKG-004 electrical design, not DEL-004-07 individually. Retained as a future cross-check when construction value is available.

---

## DEC-002 — TBD Items Not Force-Priced

**Decision:** Items with TBD quantities (ITM-005, ITM-006, ITM-007) are carried as TBD in Detail.csv rather than force-priced with allowances.

**Rationale:** FALLBACK_POLICY = ALLOW_PARAMETRIC permits parametric fallback, but these items lack sufficient scope definition (camera count, antenna count, additional system confirmation) to build even a parametric estimate. The design effort for the two confirmed systems (security cameras + radio antenna) is already included in the Electrical Engineer's 84-hour allocation (LN-004). Force-pricing undefined scope would violate the no-invention invariant.

---

## DEC-003 — Items ITM-008, ITM-009, ITM-010 Not Separately Priced in Detail.csv

**Decision:** Coordination review (ITM-008), P.Eng. IFC stamp (ITM-009), and construction support (ITM-010) are identified as priceable items in Items.csv but not given separate lines in Detail.csv.

**Rationale:** These activities are included within the LOE hours for Project Manager (R-01, 6 hours) and Electrical Engineer (R-16, 84 hours). Creating separate Detail.csv lines would double-count effort. Items.csv records them for completeness of the quantity takeoff; their costs are embedded in LN-001 and LN-004.

---

## DEC-004 — CBS Classification

**Decision:** CBS categories assigned as Management (PM, Cost Estimator) and Design (BIM Technician, Electrical Engineer).

**Rationale:** Follows the Category column from Professional_Staff_Rates.csv: R-01 = Management, R-08 = Management, R-13 = Design, R-16 = Design.

---

## DEC-005 — Scope Resolved to Single Deliverable

**Decision:** SCOPE = DEL-004-07 resolved to exactly one deliverable within PKG-004, per the decomposition deliverables table.

**Rationale:** The INIT-TASK brief specified DEL-004-07 as the scope. The deliverable folder exists with all four production documents. No ambiguity in scope resolution.
