# QA Report — EST_DEL-012-02_2026-02-27_0854

## RUN_STATUS: WARNINGS

---

## Schema Validity

### Items.csv
- **Columns:** All 9 required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes).
- **Row count:** 21 items.
- **PricingMode values:** All valid (UNIT_RATE or LUMP_SUM).
- **SourceDoc values:** All valid (Datasheet, Specification, Procedure).
- **Result:** PASS

### Detail.csv
- **Columns:** All 15 required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes).
- **Row count:** 21 lines.
- **Method values:** All PARAMETRIC (consistent with BASIS_OF_ESTIMATE).
- **Lump-sum convention:** All LUMP_SUM items have Qty=1, Unit=LS, UnitRate=Amount. PASS.
- **Result:** PASS

### WBS_CBS_Matrix.csv
- **Columns:** All required columns present.
- **Row count:** 18 CBS categories.
- **Amount_Total sum:** $47,492.00 (matches Detail.csv total). PASS.
- **Result:** PASS

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Missing Documents |
|---|---|---|---|
| DEL-012-02 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 21 | None |

**Coverage assessment:** All four production documents were read and contributed to item extraction. Datasheet provided physical attributes and quantities. Specification provided requirements and compliance activities. Procedure provided work steps and coordination activities. Guidance informed trade-off decisions and risk factors.

**Result:** PASS — full document coverage.

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 21 |
| Items priced in Detail.csv | 21 |
| Items with TBD Amount | 0 |
| **Pricing coverage** | **100%** |

**Note:** All items are priced using PARAMETRIC method. Two items (L-006 fire-rated door, L-007 fire-rated wall) are conditional allowances that may be removed if AHJ determines fire rating is not required.

**Result:** PASS

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Total lines in Detail.csv | 21 |
| Lines with SourceRef populated | 21 |
| Lines with SourceRef = "location TBD" | 0 |
| **Provenance completeness** | **100%** |

All lines reference specific price source files and rate IDs, or provide parametric derivation details in the SourceRef field.

**Result:** PASS

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (21 of 21 lines) |
| Method mix consistent with basis? | YES |
| ALLOW_MIXED_METHODS | TRUE (not exercised; all lines are PARAMETRIC) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (not exercised; basis is already PARAMETRIC) |

**Result:** PASS — all methods match declared basis.

---

## Scope Coverage

| Check | Result |
|---|---|
| Deliverables in scope | 1 (DEL-012-02) |
| Deliverables estimated | 1 (DEL-012-02) |
| Excluded deliverables | None |
| Missing deliverables | None |

**Result:** PASS

---

## Warnings Summary

| Warning ID | Severity | Description | Impact |
|---|---|---|---|
| W-01 | MEDIUM | Room dimensions TBD; area estimated parametrically from bay width assumption | Quantities for wall area (46 m2) and floor area (30 m2) are assumptions. Actual dimensions may change these by +/-30%. |
| W-02 | MEDIUM | Clear height below mezzanine TBD | Wall height assumed at 12'; actual height affects wall area quantity. |
| W-03 | MEDIUM | Fire rating requirements TBD per AHJ | $4,000 in conditional allowances (L-006 + L-007) may or may not apply. |
| W-04 | LOW | Door count, size, type TBD | Estimated 1 standard door; additional doors would increase cost. |
| W-05 | LOW | Gas code applicability TBD | If gas-fired equipment, additional provisions not yet priced. |
| W-06 | MEDIUM | Cistern pad scope boundary TBD (CON-012-02-02) | $4,800 included for cistern pad; may be PKG-014 scope. |
| W-07 | MEDIUM | Equipment platform design TBD per PKG-013 submittals | $6,500 parametric estimate; actual cost depends on equipment specifics. |

---

## Confidence Assessment

| Confidence Level | Line Count | Amount (CAD) | % of Total |
|---|---|---|---|
| HIGH | 0 | $0.00 | 0% |
| MED | 19 | $43,492.00 | 91.6% |
| LOW | 2 | $4,000.00 | 8.4% |

---

## What to Fix for a Cleaner Rerun

1. **Confirm utility room dimensions** from IFC drawings to replace the 16' x 20' assumption. This will correct wall area (ITEM-001, ITEM-002) and floor area (ITEM-003, ITEM-004) quantities.
2. **Confirm clear height below mezzanine** to validate the 12' wall height assumption used for perimeter wall area.
3. **Obtain AHJ determination on fire rating** to either confirm or remove the $4,000 in fire-rated assembly allowances (L-006, L-007).
4. **Resolve cistern pad scope boundary** (CON-012-02-02) to confirm whether $4,800 belongs in DEL-012-02 or PKG-014.
5. **Obtain PKG-013 equipment submittals** to refine equipment platform estimate ($6,500) from parametric to rate-based.
6. **Confirm door specifications** (count, size, type, fire rating) from IFC drawings.
7. **Confirm fuel type** for PKG-013 heating system to determine gas code provisions.
