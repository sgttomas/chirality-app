# QA Report — EST_DEL-001-05_2026-02-27_0545

**RUN_STATUS: OK**

---

## 1. Schema Validity

### Items.csv
| Check | Result |
|---|---|
| File exists and parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — 5 UNIT_RATE, 5 LUMP_SUM |
| All rows trace to source document and section | PASS — all 10 rows have SourceDoc and SourceSection populated |
| Qty values present or explicitly TBD | PASS — all quantities specified |

### Detail.csv
| Check | Result |
|---|---|
| File exists and parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (PARAMETRIC) | PASS — all 10 rows use PARAMETRIC |
| Allowance/parametric convention respected (LS items: Qty=1, Unit=LS, UnitRate=Amount) | PASS — LS items at $0 have UnitRate=0=Amount |
| ItemID references valid against Items.csv | PASS — all 10 ItemIDs match |

---

## 2. Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-001-05) |
| Documents read | 4 of 4 (Datasheet, Specification, Guidance, Procedure) |
| Missing documents | 0 |
| Items extracted | 10 |
| Items with numeric quantities | 10 (all have explicit Qty) |
| Items with TBD quantities | 0 |

### Coverage by Source Document

| Source Document | Items Extracted |
|---|---|
| Procedure | 7 (ITEM-001 through ITEM-005, ITEM-009, ITEM-010) |
| Specification | 3 (ITEM-006, ITEM-007, ITEM-008) |

**Note:** Datasheet and Guidance were read and informed the understanding of scope and trade-offs, but the priceable items for this deliverable (a drawing set) are primarily professional service effort activities described in the Procedure and requirements in the Specification.

---

## 3. Pricing Coverage

| Metric | Value |
|---|---|
| Total line items in Detail.csv | 10 |
| Lines with non-zero Amount | 5 (L-001 through L-005) |
| Lines with $0 Amount (embedded effort) | 4 (L-006 through L-009) |
| Lines with TBD / unpriced scope | 1 (L-010: post-IFC revisions) |
| Pricing coverage (non-zero lines / total) | 50% (5/10) |
| Pricing coverage (priced value / total priced + identifiable scope) | 100% of identifiable effort is priced; $0 items are intentionally $0 (double-count avoidance) |
| Effective pricing coverage | 90% (9 of 10 items have resolved pricing; 1 item is TBD scope) |
| Total priced amount | $19,200 CAD |

---

## 4. Provenance Completeness

| Metric | Value |
|---|---|
| Lines with non-TBD SourceRef | 9 of 10 (90%) |
| Lines with TBD SourceRef | 1 (L-010: SourceRef = Assumptions_Log.md ASM-004) |

### Top Missing-Source Offenders

| LineID | Description | Issue |
|---|---|---|
| L-010 | Post-IFC revision allowance | No pricing basis available; scope is TBD pending construction phase; SourceRef points to Assumptions_Log.md ASM-004 |

---

## 5. Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (all 10 lines) |
| Method mix consistent with basis | PASS — 100% PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE (allowed but not exercised) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (not exercised; all items priced from primary sources) |

---

## 6. Scope Coverage

| Metric | Value |
|---|---|
| Deliverables included | 1 (DEL-001-05 Interior Elevations) |
| Deliverables excluded | 0 (single-deliverable scope) |
| Package | PKG-001 Architectural Design |

---

## 7. Write Quarantine Check

| Check | Result |
|---|---|
| All outputs written under _Estimates/ | PASS |
| No modifications to deliverable working files | PASS |
| No modifications to lifecycle files | PASS |
| No modifications to decomposition outputs | PASS |

---

## 8. What to Fix for a Cleaner Rerun

1. **Post-IFC revision scope (L-010):** Define the expected post-IFC revision effort (hours by role) once construction phase scope is better understood. This would convert L-010 from $0/TBD to a priced item.
2. **Coordination and QA scope items (L-006 through L-009):** These are tracked at $0 because effort is embedded in role labour lines. If finer CBS granularity is desired (separating coordination effort from production effort), the Level_of_Effort.csv would need to break down hours by activity type within each role.
3. **Confidence upgrade:** Replace PARAMETRIC rates with actual quotes from the project Architect's firm to move from MEDIUM to HIGH confidence.
