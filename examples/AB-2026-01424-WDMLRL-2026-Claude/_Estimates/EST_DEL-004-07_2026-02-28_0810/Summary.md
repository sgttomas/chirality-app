# Estimate Summary — DEL-004-07 Low-Voltage System Plans

**RunID:** EST_DEL-004-07_2026-02-28_0810
**Date:** 2026-02-28
**Basis of Estimate:** PARAMETRIC
**Currency:** CAD
**Prior Snapshot:** EST_DEL-004-07_2026-02-27_0141

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
| DEL-004-07 | Low-Voltage System Plans | CAD | **$18,810.00** | 1 | 7 |

---

## Total by CBS (Cost Breakdown Structure)

| CBS | Currency | Amount | Line Count | Notes |
|---|---|---|---|---|
| Management | CAD | $1,530.00 | 2 | Project Manager + Cost Estimator |
| Design | CAD | $17,280.00 | 5 | BIM Technician + Electrical Engineer + 2 resolved $0 refs + 1 TBD line |
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

### W-001 — TBD: Additional Low-Voltage Systems Scope (LN-007)
One line item (LN-007) remains TBD because the scope for additional low-voltage systems (fire alarm, data/network, access control, intercom) is pending County confirmation at preliminary design per Specification REQ-007-08 and REQ-007-09. If additional systems are confirmed, engineering hours (LN-004) and BIM hours (LN-003) may need to increase.

### W-002 — Old North Shop Scope Boundary TBD
The Specification references "applicable renovation areas of the Old North Shop" but the Datasheet and Guidance record this scope as TBD (see Conflict Table CON-007-02). If Old North Shop low-voltage scope is confirmed, hours may increase beyond the current 130-hour allocation.

### W-003 — LOE Hours Are Parametric Estimates
All hour quantities are from a parametric LOE model, not confirmed resource plans. The 84 hours for Electrical Engineer and 36 hours for BIM Technician are standard drawing-set allocations that may not fully reflect the complexity of low-voltage design.

### W-004 — No Construction Material Costs
This estimate covers professional design services only. Physical materials, equipment procurement, and installation labour for low-voltage systems are in PKG-015 (DEL-015-05), not this deliverable.

---

## Changes From Prior Snapshot (EST_DEL-004-07_2026-02-27_0141)

| Item | Prior | Current | Change |
|---|---|---|---|
| LN-005 (Security camera wiring) | TBD | $0 (1 LS) | Resolved — design effort in LN-004; hardware in PKG-015 |
| LN-006 (Radio antenna routing) | TBD | $0 (1 LS) | Resolved — design effort in LN-004; hardware in PKG-015 |
| LN-007 (Additional LV systems) | TBD | TBD | Unchanged — pending County confirmation |
| TBD line count | 3 | 1 | Reduced by 2 |
| Priced total | $18,810.00 | $18,810.00 | No change |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total line items (Detail.csv) | 7 |
| Priced line items | 6 (86%) |
| TBD line items | 1 (14%) |
| Priced amount | $18,810.00 CAD |
| TBD amount exposure | Unknown — depends on scope confirmation at preliminary design |
| Provenance completeness (priced lines) | 100% — all 6 priced lines have full SourceRef |
