# Blockers Report — EST_DEL-04-02_2026-02-18_1100

## Summary

**Estimate-blocking dependencies:** 0
**Design-phase coordination items (non-blocking for estimating):** 9

No dependencies in the DEL-04-02 Dependencies.csv prevent meaningful pricing at the proposal stage. All dependencies are design-phase coordination items that will need resolution during detailed design but do not block rate-table-based estimating.

---

## Dependency Analysis

### DEP-0402-A01 — Implements SOW-0302 (Anchor)
- **Type:** ANCHOR / IMPLEMENTS_NODE
- **Blocks estimate?** No. This is a scope traceability anchor, not a pricing dependency.

### DEP-0402-A02 — Traces to OBJ-004 (Anchor)
- **Type:** ANCHOR / TRACES_TO_REQUIREMENT
- **Blocks estimate?** No. Objective traceability anchor.

### DEP-0402-E01 — Requires DEL-04-01 Design Basis
- **Type:** EXECUTION / PREREQUISITE
- **Target:** DEL-04-01 (Cold Storage Design Basis & Configuration)
- **Impact on estimate:** Does not block pricing. Building orientation and side identification affect which sides get openings, but the number, size, and specification of doors/openings is fixed by SOW-0302 regardless of orientation. Quantities and rates are unaffected.
- **Impact on design:** Must be resolved before detailed design submission.

### DEP-0402-E02 — Main Building Overhead Door Spec Cross-Reference
- **Type:** EXECUTION / INTERFACE
- **Target:** DEL-02-04 (Structure, Envelope, Roof & Overhead Doors -- Main Building)
- **Impact on estimate:** Does not block pricing. The window profile alignment requirement (REQ-4202-03) affects specification details but not the cost basis. EQ-02 pricing already assumes insulated doors with windows at standard grade.
- **Impact on design:** Must be resolved to confirm window material (poly vs. metal) and profile configuration.

### DEP-0402-E03 — Site Layout for Access Axis
- **Type:** EXECUTION / INTERFACE
- **Target:** DEL-03-01 (Site Plan, Circulation, Parking)
- **Impact on estimate:** Does not block pricing. Access axis affects door placement but not quantity, size, or cost.

### DEP-0402-E04 — Site Grading for Apron Drainage
- **Type:** EXECUTION / INTERFACE
- **Target:** DEL-03-02 (Grading, Earthworks, Drainage)
- **Impact on estimate:** Does not block pricing. Drainage direction may affect apron slope but not material quantity or unit rate at this level of estimating.

### DEP-0402-E05 — Floor/Foundation Coordination
- **Type:** EXECUTION / INTERFACE (downstream)
- **Target:** DEL-04-03 (Cold Storage Floor & Foundation)
- **Impact on estimate:** Does not block pricing. Apron-to-floor transition details affect design, not the cost basis for aprons.

### DEP-0402-E06 — Electrical Coordination for Door Openers
- **Type:** EXECUTION / INTERFACE (downstream)
- **Target:** DEL-04-04 (Cold Storage Electrical & Ventilation)
- **Impact on estimate:** Does not block pricing. Electrical feed costs are explicitly excluded from DEL-04-02 per cost ownership rules. Only coordination is required.

### DEP-0402-E07 — Alberta Building Code Compliance
- **Type:** EXECUTION / CONSTRAINT (external)
- **Target:** Alberta Building Code
- **Impact on estimate:** Does not block pricing. Code compliance is assumed in door sizing and hardware selection. Actual code edition confirmation is a design-phase item.

### DEP-0402-E08 — Pickled-Sand Building Key Commonality
- **Type:** EXECUTION / INTERFACE (external)
- **Target:** Pickled-Sand Storage Building (out of scope -- SOW-0400)
- **Impact on estimate:** Does not block pricing. Key commonality is a hardware specification detail that does not change the cost of the hardware set (BE-13 rate applies regardless of keying scheme).

### DEP-0402-E09 — RFP Document Review
- **Type:** EXECUTION / PREREQUISITE (document)
- **Target:** RFP Appendix A (OSR)
- **Impact on estimate:** Does not block pricing. OSR has been reviewed and requirements extracted into the Datasheet and Specification.
