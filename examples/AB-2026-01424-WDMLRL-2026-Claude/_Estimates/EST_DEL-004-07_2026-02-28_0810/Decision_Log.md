# Decision Log

**RunID:** EST_DEL-004-07_2026-02-28_0810

---

## DEC-001 — Primary Pricing Method: LOE x Rate Table

**Decision:** Price DEL-004-07 using Level_of_Effort.csv hours multiplied by Professional_Staff_Rates.csv hourly rates.

**Rationale:** The deliverable is a professional design services drawing set. The LOE model provides deliverable-specific hour allocations by role, and the rate table provides per-role hourly rates. This is the most direct parametric method available for a design deliverable.

**Alternative considered:** Professional_Design_Fees.csv (DF-04: 1.6% of construction value) — rejected as primary method because (a) construction value is not yet established, and (b) DF-04 covers the entire PKG-004 electrical design, not DEL-004-07 individually. Retained as a future cross-check when construction value is available.

---

## DEC-002 — TBD Item LN-007 Not Force-Priced

**Decision:** LN-007 (additional low-voltage systems) is carried as TBD in Detail.csv rather than force-priced with an allowance.

**Rationale:** FALLBACK_POLICY = ALLOW_PARAMETRIC permits parametric fallback, but LN-007 lacks sufficient scope definition (fire alarm, data, access control, intercom — none confirmed) to build even a parametric estimate. Force-pricing undefined scope would violate the no-invention invariant. This item is pending County confirmation at preliminary design.

**Prior context:** In the prior snapshot (EST_DEL-004-07_2026-02-27_0141), three items (LN-005, LN-006, LN-007) were TBD. LN-005 and LN-006 have been resolved in this snapshot per DEC-R01 and DEC-R02. LN-007 remains the sole TBD.

---

## DEC-003 — Items ITM-008, ITM-009, ITM-010 Not Separately Priced in Detail.csv

**Decision:** Coordination review (ITM-008), P.Eng. IFC stamp (ITM-009), and construction support (ITM-010) are identified as priceable items in Items.csv but not given separate lines in Detail.csv.

**Rationale:** These activities are included within the LOE hours for Project Manager (R-01, 6 hours) and Electrical Engineer (R-16, 84 hours). Creating separate Detail.csv lines would double-count effort. Items.csv records them for completeness of the quantity takeoff; their costs are embedded in LN-001 and LN-004.

---

## DEC-004 — CBS Classification

**Decision:** CBS categories assigned as Management (PM, Cost Estimator) and Design (BIM Technician, Electrical Engineer, hardware reference items).

**Rationale:** Follows the Category column from Professional_Staff_Rates.csv: R-01 = Management, R-08 = Management, R-13 = Design, R-16 = Design. Hardware reference items LN-005 and LN-006 are classified as Design because their design effort is embedded in Design-category engineer hours.

---

## DEC-005 — Scope Resolved to Single Deliverable

**Decision:** SCOPE = DEL-004-07 resolved to exactly one deliverable within PKG-004, per the decomposition deliverables table.

**Rationale:** The INIT-TASK brief specified DEL-004-07 as the scope. The deliverable folder exists with all four production documents. No ambiguity in scope resolution.

---

## DEC-R01 — Security Camera Wiring Layout (LN-005) Set to $0 Hardware Reference

**Decision:** Resolve LN-005 (security camera wiring layout) to Qty=1, Unit=LS, UnitRate=$0, Amount=$0.

**Rationale:** The design effort for security camera wiring layout is already included in LN-004 (Electrical Engineering, 84 hours). The physical camera hardware cost is allocated to PKG-015 (equipment procurement and installation). Setting LN-005 to $0 avoids double-counting design effort while maintaining the line item for scope traceability. The line item is retained to document that camera wiring design is within the DEL-004-07 scope, even though its cost is captured elsewhere.

**Confidence:** MED — design effort coverage in LN-004 is well-documented; PKG-015 hardware allocation is per decomposition.

---

## DEC-R02 — 2-Way Radio Antenna Routing (LN-006) Set to $0 Hardware Reference

**Decision:** Resolve LN-006 (2-way radio antenna wire routing) to Qty=1, Unit=LS, UnitRate=$0, Amount=$0.

**Rationale:** The design effort for radio antenna wire routing is already included in LN-004 (Electrical Engineering, 84 hours). The physical antenna hardware cost is allocated to PKG-015 (equipment procurement and installation). Setting LN-006 to $0 avoids double-counting design effort while maintaining the line item for scope traceability. The line item is retained to document that antenna routing design is within the DEL-004-07 scope, even though its cost is captured elsewhere.

**Confidence:** MED — design effort coverage in LN-004 is well-documented; PKG-015 hardware allocation is per decomposition.
