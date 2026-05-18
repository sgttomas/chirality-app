# Assumptions Log

**RunID:** EST_DEL-004-07_2026-02-28_0810

---

## ASM-001 — LOE Hours Represent Full Design-Through-IFC Lifecycle

**Assumption:** The 130 hours allocated in Level_of_Effort.csv for DEL-004-07 (6 PM + 4 Cost Estimator + 36 BIM Technician + 84 Electrical Engineer) cover the complete lifecycle from scope confirmation through IFC issue and construction support, including all 8 procedure steps.

**Basis:** Level_of_Effort.csv Notes column states "PKG-004 Electrical Engineer -- Drawing Set" for all four role entries, indicating a standard drawing-set LOE model.

**Risk if wrong:** If hours represent only a subset of the lifecycle (e.g., design only, excluding construction support), total effort and cost may be underestimated. Conversely, if the narrow confirmed scope (2 low-voltage systems) requires less than 130 hours, the estimate may be conservative.

---

## ASM-002 — Confirmed Low-Voltage Scope Fits Within 84 Electrical Engineer Hours

**Assumption:** The design effort for the two confirmed low-voltage systems (security camera wiring, SOW-0064; radio antenna wire, SOW-0065) is encompassed within the Electrical Engineer's 84-hour allocation, including scope confirmation, code research, layout design, coordination, IFC review, and P.Eng. stamp.

**Basis:** The LOE model assigns 84 hours to R-16 for a Drawing Set deliverable in PKG-004. The confirmed low-voltage scope is relatively narrow (2 systems with limited complexity documented in sources). This assumption supports the DEC-R01 and DEC-R02 decisions to set LN-005 and LN-006 to $0.

**Risk if wrong:** If additional low-voltage systems are confirmed at preliminary design (fire alarm, data/network, access control, intercom per REQ-007-08/09), or if Old North Shop scope is added, 84 hours may be insufficient. A rerun would be required.

---

## ASM-003 — Staff Rates Are Blended/Loaded Rates

**Assumption:** The hourly rates in Professional_Staff_Rates.csv are blended rates that include overhead, benefits, and profit margin (i.e., billing rates, not bare labour costs).

**Basis:** The rate table provides a single HourlyRate_CAD per role with no separate overhead or markup columns. The rates are reasonable for Alberta professional services billing rates (e.g., $165/hr for P.Eng. electrical engineer, $95/hr for BIM technician).

**Risk if wrong:** If rates are bare labour costs, total estimate would need an overhead/profit multiplier (typically 1.5x to 2.5x for professional services), which would significantly increase the total.

---

## ASM-004 — No Physical Material or Equipment Costs in This Deliverable

**Assumption:** DEL-004-07 covers design documentation only. Physical low-voltage materials (cables, conduit, cameras, NVR, antenna equipment) and installation labour are covered by PKG-015 / DEL-015-05.

**Basis:** _CONTEXT.md Type = "Drawing Set"; Specification scope excludes physical procurement and installation; Decomposition assigns installation to PKG-015. This assumption is consistent with DEC-R01 and DEC-R02, which set hardware reference items to $0 because hardware cost resides in PKG-015.

**Risk if wrong:** None expected — scope boundary is clearly documented.

---

## ASM-005 — Currency Is CAD

**Assumption:** All pricing is in Canadian Dollars (CAD) with no foreign exchange exposure.

**Basis:** INIT-TASK brief specifies CURRENCY = CAD; Assumed_Project_Parameters.csv PP-17 records Currency = CAD; project is located in Alberta, Canada.

**Risk if wrong:** Negligible — project is entirely domestic.

---

## ASM-006 — Single Execution (No Rework Iterations)

**Assumption:** The LOE hours assume a single design-review-issue cycle without major rework iterations. Minor revisions during coordination (Procedure Step 6) are included, but a full redesign (e.g., due to scope change after preliminary design) is not.

**Basis:** Standard parametric LOE model for a drawing set deliverable. The Notes column in Level_of_Effort.csv does not indicate rework contingency.

**Risk if wrong:** If County preliminary design review results in significant scope changes (e.g., adding fire alarm system, changing camera technology), additional hours beyond the 130-hour allocation may be needed.
