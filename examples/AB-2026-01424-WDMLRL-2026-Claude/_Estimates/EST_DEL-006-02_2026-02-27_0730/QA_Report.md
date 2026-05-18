# QA Report — EST_DEL-006-02_2026-02-27_0730

## RUN_STATUS: OK

Totals are meaningful. No critical input gaps. All items priced from parametric sources with full provenance.

---

## Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File exists and parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| All rows trace to a source document and section | PASS |
| Row count | 16 items |

### Detail.csv

| Check | Result |
|---|---|
| File exists and parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (PARAMETRIC for all lines) | PASS |
| Allowance/parametric convention respected (scope lines: Qty=1, Unit=LS, UnitRate=Amount=0) | PASS |
| Row count | 16 lines (4 costed + 12 scope coverage) |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-006-02 | 4 (Datasheet, Specification, Guidance, Procedure) | 0 | 16 |

### Item Traceability

| ItemID | SourceDoc | SourceSection | Priced? |
|---|---|---|---|
| ITEM-001 | Procedure | Step 1 | Scope coverage ($0; cost in role lines) |
| ITEM-002 | Procedure | Step 2 | Scope coverage ($0; cost in role lines) |
| ITEM-003 | Procedure | Step 3 | Scope coverage ($0; cost in role lines) |
| ITEM-004 | Procedure | Step 4 | Scope coverage ($0; cost in role lines) |
| ITEM-005 | Procedure | Step 5 | Scope coverage ($0; cost in role lines) |
| ITEM-006 | Procedure | Step 5A | Scope coverage ($0; cost in role lines) |
| ITEM-007 | Procedure | Step 6 | Scope coverage ($0; cost in role lines) |
| ITEM-008 | Procedure | Step 6A | Scope coverage ($0; cost in role lines) |
| ITEM-009 | Procedure | Step 7 | Scope coverage ($0; cost in role lines) |
| ITEM-010 | Procedure | Step 8 | Scope coverage ($0; cost in role lines) |
| ITEM-011 | Procedure | Step 8A | Scope coverage ($0; cost in role lines) |
| ITEM-012 | Procedure | Step 9 | Scope coverage ($0; cost in role lines) |
| ITEM-013 | Datasheet | Identification / Conditions | YES -- $990 |
| ITEM-014 | Datasheet | Identification / Conditions | YES -- $540 |
| ITEM-015 | Datasheet | Identification / Conditions | YES -- $1,995 |
| ITEM-016 | Datasheet | Identification / Conditions | YES -- $7,840 |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items | 16 |
| Items with non-zero Amount | 4 (25.0% of items) |
| Items with $0 Amount (scope coverage, not double-counted) | 12 (75.0% of items) |
| Items with TBD Amount | 0 (0%) |
| Total costed amount | $11,365 CAD |
| Pricing coverage (by cost) | 100% -- all cost-bearing items priced |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Detail.csv rows with non-TBD SourceRef | 16 / 16 (100%) |
| Detail.csv rows with TBD SourceRef | 0 |
| Top missing-source offenders | None |

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (all 16 lines) |
| Mixed methods detected | NO |
| ALLOW_MIXED_METHODS setting | TRUE (not triggered) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (not triggered -- all items priced from primary sources) |
| Consistency | PASS -- all methods match BASIS_OF_ESTIMATE |

---

## Scope Coverage

| Category | Count | Notes |
|---|---|---|
| Deliverables in scope | 1 (DEL-006-02) | |
| Deliverables excluded | 0 | DEL-006-01 and DEL-006-03 through DEL-006-08 are separate deliverables in PKG-006 |
| Documents read | 4 of 4 | Datasheet, Specification, Guidance, Procedure |
| Documents missing | 0 | |

---

## Write Quarantine Check

| Check | Result |
|---|---|
| All writes under _Estimates/ | PASS |
| No deliverable files modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition files modified | PASS |

---

## What to Fix for a Cleaner Rerun

No issues identified. This run produced a complete estimate with full provenance and no TBD amounts. The estimate could be improved by:

1. Obtaining task-level hour breakdowns within each role (to apportion cost across the 12 activity items rather than carrying them as $0 scope coverage items).
2. Confirming the LOE model parameters against actual plumbing distribution drawing effort benchmarks for comparable industrial shop facilities.
3. Confirming the hourly rates against current market rates for Alberta-based plumbing engineering consultants.
4. Verifying whether the drawing set complexity (cistern-fed distribution with freeze protection, emergency shower compliance, multiple fixture types) warrants additional hours beyond the parametric model allocation.

---

## Operator Acceptance Checklist

- [x] RUN_STATUS is OK
- [x] Quantity takeoff (Items.csv) complete -- 16 items with source traceability
- [x] Basis-consistency checks pass (all PARAMETRIC)
- [x] Provenance completeness reported (100%)
- [x] Scope coverage explicit (1 deliverable, 4 documents, 0 gaps)
- [x] No writes outside _Estimates/
