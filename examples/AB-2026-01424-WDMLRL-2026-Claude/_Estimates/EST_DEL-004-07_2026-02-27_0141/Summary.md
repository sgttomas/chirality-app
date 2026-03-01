# Estimate Summary — DEL-004-07 Low-Voltage System Plans

**RunID:** EST_DEL-004-07_2026-02-27_0141
**Date:** 2026-02-27
**Basis of Estimate:** PARAMETRIC
**Currency:** CAD

---

## Basis of Estimate Used

| Parameter | Value |
|---|---|
| **Primary Method** | PARAMETRIC — Level of Effort (hours) x Staff Hourly Rates |
| **Hour Source** | Level_of_Effort.csv (DEL-004-07 rows) |
| **Rate Source** | Professional_Staff_Rates.csv (roles R-01, R-08, R-13, R-16) |
| **Fallback Policy** | ALLOW_PARAMETRIC |
| **Mixed Methods** | TRUE (allowed but not exercised; all priced lines use PARAMETRIC) |

---

## Total by Deliverable

| WBS_DeliverableID | Name | Currency | Priced Amount | TBD Lines | Total Lines |
|---|---|---|---|---|---|
| DEL-004-07 | Low-Voltage System Plans | CAD | **$18,810.00** | 3 | 7 |

---

## Total by CBS (Cost Breakdown Structure)

| CBS | Currency | Amount | Line Count | Notes |
|---|---|---|---|---|
| Management | CAD | $1,530.00 | 2 | Project Manager + Cost Estimator |
| Design | CAD | $17,280.00 | 5 | BIM Technician + Electrical Engineer + 3 TBD lines |
| **TOTAL** | **CAD** | **$18,810.00** | **7** | |

---

## Total by Role

| RoleID | Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| R-01 | Project Manager | 6 | $165.00 | $990.00 |
| R-08 | Cost Estimator | 4 | $135.00 | $540.00 |
| R-13 | BIM Technician | 36 | $95.00 | $3,420.00 |
| R-16 | Electrical Engineer | 84 | $165.00 | $13,860.00 |
| | **Total** | **130** | | **$18,810.00** |

---

## Key Warnings and Coverage Gaps

### W-001 — TBD Quantities for Physical Low-Voltage Systems
Three line items (LN-005, LN-006, LN-007) have TBD quantities because the Datasheet records camera counts, antenna points, and additional low-voltage system scope as TBD pending County confirmation at preliminary design. The design effort for the confirmed scope (security cameras + radio antenna) is included in the Electrical Engineer's 84 hours (LN-004), but if additional systems are confirmed (fire alarm, data/network, access control, intercom per Specification REQ-007-08/09), hours may increase.

### W-002 — Old North Shop Scope Boundary TBD
The Specification references "applicable renovation areas of the Old North Shop" but the Datasheet and Guidance record this scope as TBD (see Conflict Table CON-007-02). If Old North Shop low-voltage scope is confirmed, hours may increase beyond the current 130-hour allocation.

### W-003 — LOE Hours Are Parametric Estimates
All hour quantities are from a parametric LOE model, not confirmed resource plans. The 84 hours for Electrical Engineer and 36 hours for BIM Technician are standard drawing-set allocations that may not fully reflect the complexity of low-voltage design with multiple TBD scope items.

### W-004 — No Construction Material Costs
This estimate covers professional design services only. Physical materials, equipment procurement, and installation labour for low-voltage systems are in PKG-015 (DEL-015-05), not this deliverable.

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total line items (Detail.csv) | 7 |
| Priced line items | 4 (57%) |
| TBD line items | 3 (43%) |
| Priced amount | $18,810.00 CAD |
| TBD amount exposure | Unknown — depends on scope confirmation at preliminary design |
| Provenance completeness (priced lines) | 100% — all 4 priced lines have full SourceRef |
