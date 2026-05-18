# QA Report — EST_DEL-007-04_2026-02-27_0700

## RUN_STATUS: OK

---

## 1. Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows have non-empty ItemID | PASS |
| All rows trace to a source document (SourceDoc) | PASS |
| All rows trace to a source section (SourceSection) | PASS |
| PricingMode values are valid (UNIT_RATE or LUMP_SUM) | PASS |
| Row count | 12 items |

### Detail.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All rows have non-empty LineID | PASS |
| All ItemID values reference Items.csv | PASS (LN-001 -> ITEM-001, LN-002 -> ITEM-002, LN-003 -> ITEM-003) |
| Method values are valid enum (PARAMETRIC) | PASS |
| Currency is consistent (CAD) | PASS |
| Allowance/parametric convention not applicable (all lines are UNIT_RATE with real quantities) | N/A — lines are priced with actual Qty x UnitRate, not lump-sum parametric convention |
| Row count | 3 priced lines |

### WBS_CBS_Matrix.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present | PASS |
| Totals reconcile with Detail.csv | PASS ($990 + $540 = $1,530 Management; $9,450 Design; Grand Total $10,980) |

---

## 2. Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-007-04) |
| Documents read | 4 of 4 (Datasheet, Specification, Guidance, Procedure) |
| Missing documents | 0 |
| Items extracted | 12 |
| Priced items (with Detail.csv rows) | 3 (ITEM-001, ITEM-002, ITEM-003) |
| Scope-tracking items (embedded in priced items) | 9 (ITEM-004 through ITEM-012) |

**Note:** Items ITEM-004 through ITEM-012 are intentionally not priced separately in Detail.csv. They represent specification sub-sections whose effort is embedded in the Landscape Architect's 70-hour allocation (ITEM-003). See Decision_Log.md DEC-003.

---

## 3. Pricing Coverage

| Metric | Value |
|---|---|
| Total items requiring pricing | 3 (labour line items) |
| Items priced | 3 (100%) |
| Items with Amount = TBD | 0 (0%) |
| Items with partial pricing | 0 |

---

## 4. Provenance Completeness

| Metric | Value |
|---|---|
| Detail.csv rows with SourceRef | 3 of 3 (100%) |
| Detail.csv rows with SourceRef = "location TBD" | 0 |
| Provenance completeness | 100% |

**Top missing-source offenders:** None.

---

## 5. Basis Consistency

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (3 of 3 lines) |
| Method mix consistent with basis | PASS — 100% PARAMETRIC |
| FALLBACK_POLICY exercised | No — all items priced using primary method |
| ALLOW_MIXED_METHODS exercised | No — single method used |

---

## 6. Scope Coverage

| Metric | Value |
|---|---|
| Deliverables included | 1 (DEL-007-04) |
| Deliverables excluded | 0 |
| Packages included | 1 (PKG-007) |
| Packages excluded | 0 |
| Scope boundary notes | Estimate covers professional services (specification authoring) only. Physical construction costs for landscape work are outside the scope of this specification deliverable estimate. |

---

## 7. Write Quarantine Verification

| Check | Result |
|---|---|
| All files written under _Estimates/ | PASS |
| Files written outside _Estimates/ | NONE |
| Project truth files modified | NONE |
| Lifecycle files modified | NONE |

---

## 8. Operator Acceptance Checklist (S8)

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Items.csv reviewed for completeness | 12 items extracted from 4 documents; all specification requirement groups represented |
| Basis-consistency checks pass | PASS — 100% PARAMETRIC |
| Provenance completeness reported | 100% (3/3 lines) |
| Scope coverage explicit | 1 deliverable, 1 package; inclusions/exclusions stated |
| No writes outside _Estimates/ | PASS |

---

## 9. What to Fix for a Cleaner Rerun

1. **Add a Landscape Architectural fee row to Professional_Design_Fees.csv** to enable a fee-percentage cross-check of the LOE-based estimate.
2. **Re-estimate when upstream deliverables (DEL-007-02, DEL-007-03) are approved** to confirm or adjust the 70-hour Landscape Architect allocation based on resolved TBDs.
3. **Obtain geotechnical report (DEL-008-01)** to assess whether unusual site conditions affect specification scope and effort.
