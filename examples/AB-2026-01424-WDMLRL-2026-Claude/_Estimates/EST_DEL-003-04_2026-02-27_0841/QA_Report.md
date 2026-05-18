# QA Report — EST_DEL-003-04_2026-02-27_0841

**RUN_STATUS: OK**

---

## Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to a source document and section | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Total rows | 17 (4 priced roles + 12 sub-task breakdowns + 1 aggregate) |

### Detail.csv

| Check | Result |
|---|---|
| File parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (all PARAMETRIC) | PASS |
| Allowance/parametric convention respected (L-005: Qty=1, Unit=LS, UnitRate=Amount) | PASS (L-005 is $0.00; convention met trivially) |
| Total rows | 5 |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Missing Documents |
|---|---|---|---|
| DEL-003-04 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 17 items | None |

**Assessment:** Full document coverage. All four production documents were read. Priceable items were extracted from Specification (requirements REQ-001 through REQ-010), Procedure (work steps), and Datasheet (components and parameters).

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 17 |
| Items with TBD Qty (sub-task breakdowns) | 12 (ITEM-004 through ITEM-015) |
| Items with determined Qty (priced) | 5 (ITEM-001, ITEM-002, ITEM-003, ITEM-016, ITEM-017) |
| Total lines in Detail.csv | 5 |
| Lines with Amount > 0 | 4 of 5 (L-005 is $0.00 — included in L-004) |
| Lines with Amount = TBD | 0 |
| **Pricing coverage** | **100% of Detail.csv lines are priced** |

**Assessment:** All Detail.csv lines are priced. The sub-task items (ITEM-004 through ITEM-015) are intentionally TBD at the individual level because the LOE source provides only the aggregate 84-hour total for R-15. The aggregate is fully priced in L-004.

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Total lines in Detail.csv | 5 |
| Lines with non-TBD SourceRef | 5 (100%) |
| Lines with TBD SourceRef | 0 |
| **Provenance completeness** | **100%** |

**Assessment:** All lines trace to specific pricing source files and rows.

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (5 of 5 lines) |
| Method mix consistent with basis | PASS (100% PARAMETRIC) |
| FALLBACK_POLICY invoked | No |
| ALLOW_MIXED_METHODS relevant | No (single method used) |

---

## Scope Coverage

| Check | Result |
|---|---|
| Deliverables in scope | 1 (DEL-003-04) |
| Deliverables estimated | 1 (DEL-003-04) |
| Deliverables excluded | 0 |
| Documents missing | 0 of 4 |

---

## Warnings Summary

| ID | Severity | Description |
|---|---|---|
| W-001 | LOW | Sub-task hour breakdown (ITEM-004 through ITEM-015) is TBD; only aggregate R-15 total (84 hrs) is priced. Individual task allocations not available from LOE source. |
| W-002 | LOW | P.Eng. stamp cost assumed included in R-15 hours (ASM-003). If external reviewer required, additional cost line needed. |
| W-003 | INFO | Wash bay exhaust scope boundary (CFT-001) unresolved; estimate assumes in-scope per Guidance proposal. |
| W-004 | INFO | Professional_Design_Fees.csv (fee-percentage model) available but not applied; could serve as cross-check when construction value is known. |
| W-005 | INFO | All rates at MEDIUM confidence per source data. |

---

## What to Fix for a Cleaner Rerun

1. **Resolve sub-task hour allocations:** If the LOE model is updated to provide per-task hour breakdowns for the Mechanical Engineer (ITEM-004 through ITEM-015), a rerun would produce a more granular Detail.csv.
2. **Resolve CFT-001 scope boundary:** Confirm whether wash bay exhaust is in DEL-003-04 or DEL-003-02 scope.
3. **Obtain contracted rates:** Replace MEDIUM-confidence parametric rates with actual contracted professional staff rates for HIGH-confidence pricing.
4. **Compute fee-percentage cross-check:** When a construction value estimate is available, apply the 1.6% mechanical design fee from Professional_Design_Fees.csv as a reasonableness check.

---

## Write Quarantine Verification

All outputs written exclusively under:
`_Estimates/EST_DEL-003-04_2026-02-27_0841/`

No files outside `_Estimates/` were modified.
