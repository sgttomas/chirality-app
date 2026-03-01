# QA Report — EST_DEL-011-03_2026-02-27_0854

## RUN_STATUS: WARNINGS

---

## Schema Validity

### Items.csv
- **Columns present:** ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes -- ALL REQUIRED COLUMNS PRESENT
- **Row count:** 22 items
- **PricingMode values:** UNIT_RATE (20 rows), LUMP_SUM (2 rows) -- ALL VALID
- **All rows trace to a source document and section:** YES
- **TBD quantities:** 0 (all quantities are numeric)
- **Result:** PASS

### Detail.csv
- **Columns present:** LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes -- ALL REQUIRED COLUMNS PRESENT
- **Row count:** 22 lines
- **Method values:** PARAMETRIC (21 rows), ALLOWANCE (1 row) -- ALL VALID
- **Allowance/parametric convention check:** L-001 (ALLOWANCE) uses Qty=4, Unit=EA -- note: this follows UNIT_RATE convention (4 EA at $19,000), not the LS convention prescribed for allowance items. However, BE-03 provides a per-unit rate for overhead doors, so unit-rate pricing is appropriate here. This is a minor convention deviation flagged for awareness.
- **Amount computation check:** All Amount = Qty * UnitRate verified correct
- **Result:** PASS (minor convention note on L-001)

### WBS_CBS_Matrix.csv
- **Columns present:** WBS_PackageID, WBS_DeliverableID, CBS, Currency, Amount_Total, LineCount, ProvenanceCompletenessPct, Notes -- ALL REQUIRED COLUMNS PRESENT
- **CBS totals match Detail.csv:** YES (verified: 01-GENERAL=$16,214.80, 03-CONCRETE=$45,324.00, 05-METALS=$11,924.00, 08-OPENINGS=$105,224.00, 16-ELECTRICAL=$1,000.00; sum=$179,686.80)
- **Result:** PASS

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Missing Documents |
|---|---|---|---|
| DEL-011-03 | 5/5 (CONTEXT, Datasheet, Specification, Guidance, Procedure) | 22 | None |

- **Coverage assessment:** All four production documents plus _CONTEXT.md were read. Items were extracted from all four documents (Datasheet for physical attributes, Specification for requirements, Guidance for considerations, Procedure for work steps).
- **Key scope items covered:**
  - Overhead doors (4 units): YES
  - Door operators: YES
  - Safety devices: YES
  - Weather seals: YES
  - Door frame structural elements: YES
  - Floor drainage provisions: YES
  - Exhaust structural provisions: YES
  - Conduit provisions: YES
  - Commissioning/testing: YES
  - Inspection coordination: YES
  - Documentation: YES
  - Professional staff effort: YES (6 roles per Level_of_Effort.csv)
  - Construction labour: YES (4 trade categories)

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items priced | 22 / 22 (100%) |
| Items with TBD Amount | 0 |
| Items priced via direct rate table match | 8 (professional staff rates + construction labour rates) |
| Items priced via derived parametric model | 13 |
| Items priced via ALLOWANCE | 1 (overhead doors) |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Total Detail.csv rows | 22 |
| Rows with non-TBD SourceRef | 22 (100%) |
| Rows with direct price source citation | 14 (professional staff + labour + overhead doors + floor provisions) |
| Rows with derived parametric SourceRef | 8 |
| Top missing-source offenders | None -- all rows have SourceRef |

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC | VALID |
| ALLOW_MIXED_METHODS = TRUE | Methods used: PARAMETRIC (21 lines), ALLOWANCE (1 line) -- CONSISTENT with policy |
| FALLBACK_POLICY = ALLOW_PARAMETRIC | ALLOWANCE method used for L-001 (overhead doors) where BE-03 provides an ALLOWANCE-basis rate; CONSISTENT with fallback policy allowing parametric/allowance methods |
| Method distribution: 57.7% PARAMETRIC, 42.3% ALLOWANCE (by dollar) | ALLOWANCE share is high by dollar value due to single large line item (overhead doors). This is a structural feature of the estimate, not a quality issue -- overhead doors are the dominant material cost. |

---

## Warnings Summary

| ID | Warning | Severity | Impact |
|---|---|---|---|
| W-01 | Overhead door dimensions (width, height) TBD per IFC drawings | MATERIAL | Door cost ($76K, 42.3% of total) could vary +/-25% |
| W-02 | Door height (14-16 ft assumed) TBD pending County fleet data | MATERIAL | Affects door sizing and cost |
| W-03 | Door type (sectional vs. rolling) TBD in IFC | MINOR | Minor cost differential |
| W-04 | Bay width 24' nominal vs. clear definition TBD | MINOR | Minor impact on door frame sizing |
| W-05 | Door operator specifications TBD | MINOR | Operator cost may vary |
| W-06 | Oil/water separator requirement TBD per Alberta regulations | POTENTIAL | Could add scope and cost if required |
| W-07 | Fire separation requirements TBD | POTENTIAL | Could add scope if required |

---

## What to Fix for a Cleaner Rerun

1. **Confirm overhead door specifications** from IFC door schedule (DEL-001-07): exact width, height, type, insulation R-value, and operator specs. This would convert L-001 from ALLOWANCE to PARAMETRIC with higher confidence.
2. **Confirm door height** from County fleet data and Structural Engineer clearance envelope analysis.
3. **Obtain overhead door manufacturer quotation** to replace parametric/allowance rates with QUOTE basis for the dominant cost item.
4. **Confirm oil/water separator requirement** (Alberta Environment) to determine if additional structural slab provisions are needed.
5. **Confirm fire separation requirements** per design team Alberta Building Code/Fire Code assessment.
6. **Resolve bay width dimension** (nominal vs. clear) from IFC drawings to firm up door frame structural scope.
7. **Obtain door installer labour rate** rather than using ironworker rate as proxy.

---

## Operator Acceptance Checklist

| Check | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS | WARNINGS -- material TBDs remain on overhead door specifications |
| Quantity takeoff (Items.csv) reviewed for completeness | 22 items covering all scope elements from 4 documents |
| Basis-consistency checks pass | PASS (PARAMETRIC + ALLOWANCE consistent with policy) |
| Provenance completeness reported | 100% of rows have SourceRef |
| Scope coverage explicit | 1 deliverable (DEL-011-03); all in-scope items priced; excluded items per Specification documented |
| No writes outside _Estimates/ | CONFIRMED |
