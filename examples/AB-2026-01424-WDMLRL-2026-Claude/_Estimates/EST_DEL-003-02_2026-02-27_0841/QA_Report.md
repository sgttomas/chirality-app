# QA Report — EST_DEL-003-02_2026-02-27_0841

## RUN_STATUS: OK

---

## Schema Validity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows have valid PricingMode (UNIT_RATE or LUMP_SUM) | PASS |
| All rows trace to a SourceDoc and SourceSection | PASS |
| Row count | 16 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values valid (PARAMETRIC) | PASS |
| All ItemIDs trace back to Items.csv | PASS |
| Allowance/parametric convention respected (N/A — all items are UNIT_RATE with Qty > 1) | N/A |
| Row count | 4 priced lines |

### WBS_CBS_Matrix.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present | PASS |
| Totals consistent with Detail.csv | PASS — Management ($1,530.00) + Design ($17,280.00) = $18,810.00 |

---

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Documents present | 4 of 4 (100%) |
| Missing documents | 0 |
| Items extracted from Datasheet | 8 (ITEM-005 through ITEM-012: HVAC system scope items) |
| Items extracted from Specification | 1 (ITEM-012 also references REQ-012) |
| Items extracted from Procedure | 8 (ITEM-001 through ITEM-004 labor lines + ITEM-013 through ITEM-016 workflow scope items) |
| Items extracted from Guidance | 0 (principles/trade-offs inform design but do not add discrete priceable items) |
| Total items | 16 |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Items with assigned cost | 4 of 16 (25% of all items; 100% of costed items) |
| Items with $0 / scope-traceability only | 12 (included for scope completeness; work is subsumed by the 4 labor lines) |
| Items at TBD amount | 0 |
| Total estimated amount | $18,810.00 CAD |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Detail.csv rows with non-TBD SourceRef | 4 of 4 (100%) |
| Detail.csv rows with TBD SourceRef | 0 |
| Top missing-source offenders | None |

---

## Basis Consistency

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (4 of 4 lines) |
| Mixed methods | NO — all lines are PARAMETRIC |
| ALLOW_MIXED_METHODS setting | TRUE (not exercised — no mixed methods needed) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (not exercised — all items priced under primary basis) |
| Basis consistency | PASS |

---

## Arithmetic Verification

| LineID | Qty | UnitRate | Expected Amount | Actual Amount | Check |
|---|---|---|---|---|---|
| L-001 | 6 | 165.00 | 990.00 | 990.00 | PASS |
| L-002 | 4 | 135.00 | 540.00 | 540.00 | PASS |
| L-003 | 36 | 95.00 | 3,420.00 | 3,420.00 | PASS |
| L-004 | 84 | 165.00 | 13,860.00 | 13,860.00 | PASS |
| **TOTAL** | | | **18,810.00** | **18,810.00** | **PASS** |

---

## Warnings

| # | Severity | Description |
|---|---|---|
| W-001 | LOW | LOE model covers 4 roles only for this deliverable. Additional roles (QA/QC, Document Control, Controls Specialist) may contribute effort not captured in the estimate. |
| W-002 | LOW | No cross-check method available — construction value not established for percentage-of-construction-value validation via Professional_Design_Fees.csv (DF-03). |
| W-003 | INFO | All rates are PARAMETRIC with MEDIUM confidence per source data. No market quote or historical validation available. |
| W-004 | INFO | Scope items ITEM-005 through ITEM-016 are listed for traceability but carry no separate cost; their effort is subsumed under the 4 labor line items (ITEM-001 through ITEM-004). |

---

## What to Fix for a Cleaner Rerun

1. **Obtain construction value estimate** to enable cross-check via Professional_Design_Fees.csv (DF-03 Mechanical design fee = 1.0%–2.2% of construction value, recommended 1.6%).
2. **Validate rates against quotes** — obtain market quotes for mechanical engineering services in Alberta to validate PARAMETRIC rates and improve confidence from MEDIUM to HIGH.
3. **Confirm LOE completeness** — verify with PKG-003 lead whether additional roles (R-06, R-09, R-24) contribute hours to DEL-003-02 that should be added to the LOE model.

---

## Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Quantity takeoff reviewed for completeness | 16 items extracted; all 4 documents read; scope traceability items included |
| Basis-consistency checks pass | PASS — all PARAMETRIC |
| Provenance completeness reported | 100% (4/4 Detail.csv rows) |
| Scope coverage explicit | 1 deliverable, 4 documents, 16 items, 4 priced lines |
| No writes outside _Estimates/ | CONFIRMED |
