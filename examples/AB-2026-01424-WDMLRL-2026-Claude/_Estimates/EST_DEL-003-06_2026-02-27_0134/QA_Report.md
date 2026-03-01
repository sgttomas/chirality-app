# QA Report — EST_DEL-003-06_2026-02-27_0134

**RUN_STATUS: OK**

---

## 1. Schema Validity

### Items.csv
- **Columns present:** ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes — ALL REQUIRED COLUMNS PRESENT
- **Row count:** 14
- **PricingMode values:** All UNIT_RATE — VALID
- **Qty values:** All numeric (no TBD) — VALID
- **Unit values:** All "hr" — VALID for professional services deliverable

### Detail.csv
- **Columns present:** LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes — ALL REQUIRED COLUMNS PRESENT
- **Row count:** 14
- **Method values:** All PARAMETRIC — VALID
- **Amount computation check:** All rows Qty x UnitRate = Amount — VALID
- **Currency values:** All CAD — VALID

---

## 2. Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Notes |
|---|---|---|---|
| DEL-003-06 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 14 | All 4 documents read successfully; no missing documents |

**Assessment:** Full document coverage. Items extracted span all 13 specification requirements (REQ-M-001 through REQ-M-013) plus management and support activities.

---

## 3. Pricing Coverage

| Metric | Value |
|---|---|
| Total items | 14 |
| Items priced (Amount != TBD) | 14 |
| Items unpriced (Amount = TBD) | 0 |
| **Pricing coverage** | **100%** |

---

## 4. Provenance Completeness

| Metric | Value |
|---|---|
| Rows with non-TBD SourceRef | 14 |
| Rows with TBD SourceRef | 0 |
| **Provenance completeness** | **100%** |

All SourceRef entries point to specific rows in Professional_Staff_Rates.csv and Level_of_Effort.csv.

---

## 5. Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (14 of 14 lines) |
| Mixed methods? | NO — 100% PARAMETRIC |
| Fallback used? | NO |
| ALLOW_MIXED_METHODS setting | TRUE (not exercised) |
| FALLBACK_POLICY setting | ALLOW_PARAMETRIC (not exercised — all items had primary basis) |

**Assessment:** Fully consistent. All lines match the declared BASIS_OF_ESTIMATE.

---

## 6. Scope Coverage

| Scope Element | Status |
|---|---|
| DEL-003-06 included | YES |
| Package PKG-003 identified | YES |
| SOW-0013 coverage | YES — all 13 requirements (REQ-M-001 through REQ-M-013) mapped to items |
| Items excluded | None |
| Deliverables excluded | Not applicable (single-deliverable scope) |

---

## 7. Aggregate Totals Check

| Roll-up | Amount (CAD) |
|---|---|
| Sum of Detail.csv Amount column | $13,050.00 |
| Sum of WBS_CBS_Matrix.csv Amount_Total (excl. TOTAL row) | $13,050.00 |
| Summary.md total | $13,050.00 |
| **Cross-check** | **PASS — all three match** |

### Hour verification
| Source | Hours |
|---|---|
| Level_of_Effort.csv total for DEL-003-06 | 90 (6+4+24+56) |
| Items.csv Qty sum | 90 |
| Detail.csv Qty sum | 90 |
| **Cross-check** | **PASS — all three match** |

---

## 8. Warnings

| # | Severity | Warning | Recommendation |
|---|---|---|---|
| W-01 | LOW | Mechanical Engineer 56-hour block sub-allocated across 11 tasks by estimated complexity. Sub-allocation is an assumption; aggregate is firmly sourced. | Accept for parametric estimate; refine sub-allocation if task-level tracking is needed. |
| W-02 | LOW | P.Eng. stamp cost assumed included in ME hours. External review not priced. | Confirm with project team whether external P.Eng. review is required. |
| W-03 | LOW | No material/software/reproduction costs included. | If applicable, add as separate line items in a future run. |
| W-04 | LOW | No contingency applied to estimate. Source confidence is MEDIUM. | Consider applying contingency at portfolio level if warranted. |
| W-05 | INFO | Welding exhaust calculation (ITEM-008) is PRELIMINARY pending County specs (SOW-0204). Rework hours not budgeted. | Monitor RFI status; budget rework hours if specs differ materially from assumptions. |

---

## 9. What to Fix for a Cleaner Rerun

1. No critical issues. Estimate is complete with 100% pricing and provenance coverage.
2. If task-level hour tracking is desired, obtain sub-task hour allocations from the Mechanical Engineer rather than using the aggregate 56-hour block allocation.
3. If material, software, or reproduction costs are in scope, add those price sources and re-run.
4. If contingency is to be applied, provide a contingency policy/percentage in the run brief.

---

## 10. Operator Acceptance Checklist

| Check | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Items.csv reviewed for completeness | 14 items covering all 13 requirements + management/support |
| Basis-consistency checks pass | PASS — 100% PARAMETRIC |
| Provenance completeness reported | 100% |
| Scope coverage explicit | 1 deliverable, 14 items, 0 excluded |
| No writes outside _Estimates/ | CONFIRMED |
