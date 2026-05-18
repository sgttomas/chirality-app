# QA Report — EST_DEL-006-03_2026-02-27_0700

## RUN_STATUS: OK

---

## 1. Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to a source document and section | PASS (20/20 rows have SourceDoc and SourceSection populated) |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS (16 LUMP_SUM, 4 UNIT_RATE) |
| No orphan ItemIDs | PASS |

### Detail.csv

| Check | Result |
|---|---|
| File parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (PARAMETRIC for all 20 rows) | PASS |
| Allowance/parametric convention respected | PASS — SCOPE items use Qty=1, Unit=LS, UnitRate=0, Amount=0; labour items use actual hours/rates |
| All ItemIDs in Detail.csv exist in Items.csv | PASS (20/20) |

---

## 2. Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-006-03) |
| Documents read | 5 of 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | 0 |
| Items extracted | 20 |
| Items from Procedure (work activities) | 16 (ITEM-001 through ITEM-016) |
| Items from Datasheet (role-based LOE) | 4 (ITEM-017 through ITEM-020) |

**Coverage assessment:** All four Procedure phases are represented (Phase 1: 3 items, Phase 2: 6 items, Phase 3: 5 items, Phase 4: 2 items). All four role allocations from Level_of_Effort.csv are captured. The Specification requirements (REQ-006-03-001 to 033) and Datasheet elements (drain elements, vent elements, system parameters) inform the scope items but are not separately priced as discrete line items because this is a professional design services estimate (Drawing Set artifact type) where the cost model is level-of-effort based.

---

## 3. Pricing Coverage

| Metric | Value |
|---|---|
| Total items | 20 |
| Items priced (Amount > 0) | 4 (L-001 through L-004) |
| Items with Amount = 0 (scope coverage) | 16 (L-005 through L-020) |
| Items with Amount = TBD | 0 |
| Pricing coverage (priced / total) | 100% (all items have a defined amount; zero-dollar scope items are intentionally $0 as their costs are carried by role-based labour lines) |

---

## 4. Provenance Completeness

| Metric | Value |
|---|---|
| Total Detail.csv rows | 20 |
| Rows with non-TBD SourceRef | 20 (100%) |
| Rows with `location TBD` SourceRef | 0 |
| Provenance completeness | 100% |

**Top missing-source offenders:** None. All rows have complete provenance references.

---

## 5. Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (20/20 rows) |
| Method consistency | PASS — 100% PARAMETRIC, consistent with declared basis |
| ALLOW_MIXED_METHODS | TRUE (but not exercised — all methods are PARAMETRIC) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (not exercised — primary basis covers all items) |

---

## 6. Scope Coverage

| Metric | Value |
|---|---|
| Deliverables included | 1: DEL-006-03 (Drain & Vent Plans) |
| Deliverables excluded | N/A (scope is single deliverable) |
| Package | PKG-006 — Plumbing Design |
| Scope exclusions noted | This estimate covers professional design services only. Plumbing material procurement, construction labour (PKG-014), permit fees (PKG-009), and subcontractor costs are outside this deliverable's scope. |

---

## 7. Write Quarantine Verification

| Check | Result |
|---|---|
| All outputs written under `_Estimates/` | PASS |
| No modifications to deliverable working files | PASS |
| No modifications to lifecycle files | PASS |
| No modifications to decomposition outputs | PASS |
| No modifications to dependency registers | PASS |

---

## 8. Operator Acceptance Checklist (S8)

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (OK) |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS — 20 items covering all Procedure phases and all LOE role allocations |
| Basis-consistency checks pass | PASS — 100% PARAMETRIC |
| Provenance completeness reported | PASS — 100% |
| Scope coverage explicit | PASS — single deliverable, inclusions and exclusions stated |
| No writes outside `_Estimates/` | PASS |

---

## 9. What to Fix for a Cleaner Rerun

1. **No critical issues.** The run completed with full coverage and no TBD amounts.
2. **Potential improvement:** If confirmed quotes or historical actuals become available for plumbing engineering design services, re-running with `BASIS_OF_ESTIMATE=QUOTE` or `HISTORICAL` would increase confidence from MEDIUM to HIGH.
3. **Potential improvement:** If the drawing sheet count becomes known (currently TBD in Datasheet), a per-sheet pricing model could provide an alternative cost check.
