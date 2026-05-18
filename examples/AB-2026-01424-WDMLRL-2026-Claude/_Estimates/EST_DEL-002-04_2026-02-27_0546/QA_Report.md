# QA Report — EST_DEL-002-04_2026-02-27_0546

## RUN_STATUS: OK

---

## Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| All rows trace to a source document and section | PASS |
| Row count | 8 items |

### Detail.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values valid (PARAMETRIC) | PASS |
| Allowance/parametric convention respected (Qty=1, Unit=LS, UnitRate=Amount for LS items) | PASS (zero-cost LS items: Qty=1, Unit=LS, UnitRate=0, Amount=0) |
| All ItemIDs in Detail.csv exist in Items.csv | PASS |
| Row count | 8 lines |

### WBS_CBS_Matrix.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present | PASS |
| Totals reconcile with Detail.csv | PASS (Design-Structural: 17,700; Management: 1,530; Total: 19,230) |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Missing Documents |
|---|---|---|---|
| DEL-002-04 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 8 | None |

### Item Extraction Notes

- Items extracted primarily from Procedure.md (work steps mapped to professional roles)
- Datasheet.md provided structural element inventory for scope validation
- Specification.md provided requirements coverage for scope completeness
- Guidance.md provided design principles and trade-off context
- All priceable items are design labour activities consistent with a Drawing Set deliverable type

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total line items in Detail.csv | 8 |
| Lines with non-zero Amount | 4 (L-001 through L-004) |
| Lines with Amount = 0 (embedded activities) | 4 (L-005 through L-008) |
| Lines with Amount = TBD | 0 |
| **Pricing coverage** | **100%** (all items priced or explicitly zero-cost with effort captured in parent items) |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Total lines in Detail.csv | 8 |
| Lines with non-TBD SourceRef | 8 (100%) |
| Lines with TBD SourceRef | 0 |
| **Provenance completeness** | **100%** |

---

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (all 8 lines) |
| Mixed methods? | No — all lines use PARAMETRIC |
| Consistent with BASIS_OF_ESTIMATE? | PASS |
| FALLBACK_POLICY used? | No — all items priced from primary sources |

---

## Scope Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-002-04) |
| Deliverables estimated | 1 (DEL-002-04) |
| Deliverables excluded | 0 |
| Coverage | 100% |

---

## Arithmetic Verification

| LineID | Qty | UnitRate | Expected Amount | Actual Amount | Check |
|---|---|---|---|---|---|
| L-001 | 84 | 170 | 14,280 | 14,280 | PASS |
| L-002 | 36 | 95 | 3,420 | 3,420 | PASS |
| L-003 | 6 | 165 | 990 | 990 | PASS |
| L-004 | 4 | 135 | 540 | 540 | PASS |
| L-005 | 1 | 0 | 0 | 0 | PASS |
| L-006 | 1 | 0 | 0 | 0 | PASS |
| L-007 | 1 | 0 | 0 | 0 | PASS |
| L-008 | 1 | 0 | 0 | 0 | PASS |
| **Sum** | | | **19,230** | **19,230** | **PASS** |

---

## Warnings

| ID | Severity | Description |
|---|---|---|
| W-001 | LOW | Estimate covers design labour only; no material, printing, or reproduction costs included |
| W-002 | LOW | All price source rates and hours are MEDIUM confidence (parametric basis) |
| W-003 | MEDIUM | Multiple TBD design inputs in Datasheet (service pit depth, mezzanine load, steel plate dimensions, crane supplier data, construction method) may drive additional design iterations not captured in the LOE |
| W-004 | LOW | No contingency or escalation factor applied to the parametric estimate |

---

## What to Fix for a Cleaner Rerun

1. **Resolve TBD design inputs** (service pit depth, mezzanine load, steel plate specs, crane supplier, construction method) to confirm the LOE hours are adequate for the actual design complexity.
2. **Add material/printing cost sources** if hard-copy reproduction or third-party review costs should be included.
3. **Consider contingency** — a 10-15% contingency on design hours may be appropriate given the number of unresolved design questions (W-003).
4. **Validate LOE hours** against comparable structural drawing set deliverables for a ~13,000 sqft industrial building with 35 ft ceiling height and specialized elements (crane, pit, mezzanine, embedments).

---

## Write Quarantine Verification

| Check | Result |
|---|---|
| All files written under _Estimates/ | PASS |
| No files modified outside _Estimates/ | PASS |
| No deliverable content modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition outputs modified | PASS |
