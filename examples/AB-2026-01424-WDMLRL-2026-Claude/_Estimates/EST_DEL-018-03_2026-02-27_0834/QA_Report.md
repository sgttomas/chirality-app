# QA_Report — EST_DEL-018-03_2026-02-27_0834

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and internally consistent. However, material quantity assumptions (driving surface area and gravel depth) are parametric estimates pending civil design confirmation. Multiple TBD values from upstream deliverables (DEL-005-04, DEL-005-07) affect confidence. The estimate should be treated as a Class 4/5 parametric estimate suitable for budgeting but not for firm pricing.

---

## S1 — Write Quarantine Respected

**PASS.** All output files written exclusively under `_Estimates/EST_DEL-018-03_2026-02-27_0834/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-018-03_2026-02-27_0834` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts produced:
- [x] Run_Context.md
- [x] Items.csv (19 items)
- [x] Detail.csv (19 lines)
- [x] Summary.md
- [x] QA_Report.md (this file)
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv

## S5 — CSV Schema Integrity

### Items.csv
**PASS.**
- Columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- All 19 rows have valid PricingMode values (UNIT_RATE or LUMP_SUM)
- All rows trace to a SourceDoc (Datasheet, Specification, or Procedure) and SourceSection
- 1 row has Qty = TBD (ITM-009 — Owner-supplied aggregate, excluded)
- Lump-sum items (ITM-013 through ITM-017) correctly use Qty=1, Unit=LS

### Detail.csv
**PASS.**
- Columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- All 19 rows have valid Method values (all PARAMETRIC — consistent with BASIS_OF_ESTIMATE)
- Allowance/parametric convention respected: LS items have Qty=1, Unit=LS, UnitRate=Amount
- 2 excluded items (L-007, L-009) correctly show Amount=0.00

## S6 — Provenance Discipline

**PASS with notes.**

| Metric | Value |
|--------|-------|
| Total priced rows (Amount > 0) | 15 of 19 |
| Rows with file-level SourceRef | 14 of 15 (93%) |
| Rows with `location TBD` SourceRef | 0 |
| Rows with assumption-only SourceRef | 4 (L-012, L-013, L-014, L-016) |

**Top missing-source items:**
1. L-012 (Final grading, $12,000) — rate ($5/m2) is a parametric assumption (ASM-005), not from a published rate table. Confidence LOW.
2. L-013 (Compaction testing, $5,000) — lump-sum allowance (ASM-006). No quote or rate table basis. Confidence LOW.
3. L-014 (Proof-rolling, $3,000) — lump-sum allowance (ASM-007). Conditional item. Confidence LOW.

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Declared per SPEC S7. Totals exist and are meaningful ($154,666 CAD), but material TBDs and assumptions remain:
- Driving surface area is a parametric assumption (not from IFC drawings)
- Gravel depth/thickness is TBD pending civil specification
- 3 line items at LOW confidence represent $20,000 (13% of total)

## S8 — Operator Acceptance Checklist

| Check | Status |
|-------|--------|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS — WARNINGS with clearly identified gaps |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS — 19 items covering all identified priceable scope |
| Basis-consistency checks (method mix) | PASS — all lines use PARAMETRIC method, consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS — 93% file-level provenance; top gaps listed |
| Scope coverage explicit | PASS — 2 items explicitly excluded (topsoil stripping, aggregate supply) with reasons |
| No writes outside _Estimates/ | PASS |

---

## What to Fix for a Cleaner Rerun

1. **Obtain civil design (DEL-005-04)** to confirm actual driving surface area. This eliminates the largest quantity uncertainty.
2. **Obtain civil specification (DEL-005-07)** to confirm gravel depth, compaction standard, and aggregate gradation. This enables refinement of PS-01 rate applicability.
3. **Obtain compaction testing quote** from a third-party testing firm to replace the $5,000 parametric allowance with a firm price.
4. **Confirm proof-rolling requirement** with civil engineer (REQ-018-03-11) — if not required, remove L-014 ($3,000).
5. **Refine final grading rate** (L-012) with contractor pricing or historical data for motor grader finish work on gravel surfaces.
6. **Obtain surveyor quote** for layout staking and as-built work to replace parametric hour estimate.
