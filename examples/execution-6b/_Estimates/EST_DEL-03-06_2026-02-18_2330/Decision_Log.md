# Decision Log -- DEL-03-06

**RunID:** EST_DEL-03-06_2026-02-18_2330

---

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS assigned as `DESIGN_BRIEF` for DEL-03-06 | No explicit CBSHint in decomposition. Deterministic rule applied: deliverable type "Design Brief / Narrative" maps to CBS = DESIGN_BRIEF. Consistent with all PKG-003 deliverables. |
| EST-DEC-002 | Hours sourced from Level_of_Effort.csv as quantity input for RATE_TABLE method | Level_of_Effort.csv provides hours with PARAMETRIC basis. These hours are used as `Qty` in the rate table calculation (Qty x UnitRate = Amount). The method remains RATE_TABLE because the rate is the pricing basis; hours are the quantity. |
| EST-DEC-003 | Single line item for DEL-03-06 (1 role: R-04 Architect Project) | Level_of_Effort.csv contains exactly one row for DEL-03-06. No additional roles are allocated. This is consistent with the decomposition description: "Responsible Party: Architect (coordinating structural and mechanical input)." |
| EST-DEC-004 | ROUNDING = DOLLAR applied; Amount $1,160 is already a whole dollar | 8 hr x $145/hr = $1,160.00. No rounding adjustment needed. |
| EST-DEC-005 | No fallback pricing applied | FALLBACK_POLICY = STRICT. All line items have complete basis evidence (hours from LOE, rates from rate table). No TBD amounts. |
