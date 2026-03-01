# QA Report — EST_DEL-004-06_2026-02-27_0833

## RUN_STATUS: OK

---

## Schema Validity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Every row has SourceDoc and SourceSection | PASS |
| Row count | 20 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (all PARAMETRIC) | PASS |
| Allowance/parametric convention check | N/A — all lines are UNIT_RATE with real quantities (hours), not lump-sum parametric |
| Row count | 4 priced lines |

### WBS_CBS_Matrix.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present | PASS |
| Totals consistent with Detail.csv | PASS — $7,290.00 matches sum of Detail.csv amounts |

---

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-004-06) |
| Documents read | 5 of 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | 0 |
| Items extracted | 20 |
| Items with Qty = TBD | 6 (ITEM-011, ITEM-013, ITEM-017, ITEM-018, ITEM-019, ITEM-020) |

**Note on TBD quantities:** The 6 TBD-quantity items are load-enumeration entries from the Datasheet where exact circuit/equipment counts are design-stage unknowns. These are correctly flagged as TBD per the deliverable documents. They do not affect the parametric LOE cost estimate (which prices design hours, not individual circuit items).

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 20 |
| Items with corresponding priced lines in Detail.csv | 4 (ITEM-001 through ITEM-004) |
| Items without priced lines (load enumeration / activity scope items) | 16 (ITEM-005 through ITEM-020) |
| Percentage of cost-bearing items priced | 100% (4 of 4 LOE items priced) |
| Total priced amount | $7,290.00 CAD |
| TBD amounts | $0 — no TBD amounts in Detail.csv |

**Explanation:** Items ITEM-005 through ITEM-020 are quantity-takeoff entries documenting the engineering scope (specific loads, circuits, and work activities described in the four documents). Their cost is fully captured by the LOE-based professional hours in ITEM-001 through ITEM-004. They are included in Items.csv for scope traceability and completeness, not for independent pricing.

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Detail.csv rows with non-TBD SourceRef | 4 of 4 (100%) |
| Detail.csv rows with TBD SourceRef | 0 |
| Top missing-source offenders | None |

---

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE declared | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (4 of 4 lines) |
| Mixed methods? | No — 100% PARAMETRIC |
| Fallback used? | No |
| Consistency | PASS — all methods match declared basis |

---

## Scope Coverage

| Metric | Value |
|---|---|
| Scope requested | DEL-004-06 |
| Deliverables included | 1 (DEL-004-06 Panel Schedules) |
| Deliverables excluded | 0 |
| Package context | PKG-004 Electrical Design |
| Scope boundary | Design professional services only (panel schedule production). Excludes physical materials, panel hardware, and construction installation (PKG-015 scope). |

---

## Write Quarantine Check

| Check | Result |
|---|---|
| All output files under _Estimates/ | PASS |
| No files modified outside _Estimates/ | PASS |

---

## Acceptance Checklist (S8)

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Items.csv reviewed for completeness | PASS — 20 items covering all loads from Datasheet plus work activities from Procedure |
| Basis-consistency checks pass | PASS |
| Provenance completeness reported | PASS — 100% |
| Scope coverage explicit | PASS |
| No writes outside _Estimates/ | PASS |
