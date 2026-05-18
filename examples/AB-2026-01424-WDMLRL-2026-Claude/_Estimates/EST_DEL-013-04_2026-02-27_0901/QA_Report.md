# QA Report — EST_DEL-013-04_2026-02-27_0901

## RUN_STATUS: WARNINGS

---

## Schema Validity

### Items.csv
- **Columns present:** ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes -- ALL REQUIRED COLUMNS PRESENT.
- **Row count:** 21 items.
- **PricingMode values:** UNIT_RATE (17), LUMP_SUM (4) -- all valid enum values.
- **TBD quantities:** 0 (all quantities populated; however quantities are parametric assumptions for several items).
- **Source traceability:** All 21 rows have SourceDoc and SourceSection populated.
- **PASS.**

### Detail.csv
- **Columns present:** LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes -- ALL REQUIRED COLUMNS PRESENT.
- **Row count:** 21 lines.
- **Method values:** PARAMETRIC (16), ALLOWANCE (5) -- all valid enum values.
- **Allowance/parametric convention check:** Lines L-003, L-007, L-008, L-010, L-011, L-012 use Qty=1, Unit=LS, UnitRate=Amount as required.
- **PASS.**

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-013-04 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 0 | 21 |

- All four production documents were available and read.
- Items span all major construction elements identified in the Datasheet (hose drops, fans, ductwork, hoods, filtration, outlet/stack, controls, supports, fire-rated penetrations) plus commissioning, training, documentation, and professional staff effort.
- **PASS.**

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total line items | 21 |
| Items priced (non-TBD Amount) | 21 (100%) |
| Items with Amount = TBD | 0 |
| **Pricing coverage** | **100%** |

All items have numeric amounts. However, 5 lines use ALLOWANCE method with LOW confidence ratings, and 1 line (L-005 filtration) is conditional on CQ-002 resolution.

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Lines with SourceRef populated | 21 (100%) |
| Lines with SourceRef = "location TBD" | 0 |
| **Provenance completeness** | **100%** |

All SourceRef fields trace to specific price source files and line IDs, or to documented parametric rationale.

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC (valid enum) |
| Methods used | PARAMETRIC (16 lines, 76%), ALLOWANCE (5 lines, 24%) |
| ALLOW_MIXED_METHODS | TRUE -- mixed methods permitted |
| FALLBACK_POLICY | ALLOW_PARAMETRIC -- ALLOWANCE fallback is within policy |
| **Basis-consistency** | **PASS (mixed methods within policy)** |

---

## Warnings

| # | Severity | Warning | Impact | Recommendation |
|---|---|---|---|---|
| W-001 | MATERIAL | 5 Datasheet TBD items unresolved (TBD-DS-01 through TBD-DS-05) | Equipment sizing, quantities, and material specs are assumed; actual costs may differ significantly | Resolve TBDs before next estimate iteration |
| W-002 | MATERIAL | Filtration scope conditional on CQ-002 | $8,500 line item may be $0 if direct discharge confirmed | Resolve CQ-002 with environmental compliance review |
| W-003 | MODERATE | Hose drop quantity assumed at 4 (2 per bay) | Each additional drop adds ~$9,850 to equipment costs | Confirm hose drop count with mechanical engineer (DEL-003-04) |
| W-004 | MODERATE | ALLOWANCE-basis equipment rates have wide ranges (MS-04: $6,000-$14,000/EA) | Total equipment cost could range from ~$42,000 to ~$82,000 for hose+fan assemblies alone | Obtain manufacturer quotes for retractable hose reel assemblies |
| W-005 | LOW | Labour hours are parametric; no detailed task schedule | Actual labour hours may vary +/-30% | Refine with mechanical contractor input |
| W-006 | LOW | No contingency or escalation applied | Total represents base-case estimate only | Apply project-level contingency per estimating policy |
| W-007 | LOW | Controls cost ($5,500) based on parametric assumption; functional spec is TBD | Controls cost depends on complexity of interlock logic and monitoring requirements | Confirm controls scope with mechanical engineer (REQ-012) |

---

## What to Fix for a Cleaner Rerun

1. **Resolve Datasheet TBDs** (TBD-DS-01 through TBD-DS-05): equipment list, exhaust volumes, hose drop count, ductwork material, controls spec.
2. **Resolve CQ-002** (filtration vs. direct discharge): removes conditional line item uncertainty.
3. **Obtain manufacturer quotes** for exhaust hose drop/reel assemblies and fans to replace ALLOWANCE rates with QUOTE-based pricing.
4. **Confirm hose drop quantity** with mechanical engineer after design completion (DEL-003-04).
5. **Add detailed labour breakdown** from mechanical contractor's installation schedule.
6. **Apply contingency** at project level per estimating policy.
