# QA Report — EST_DEL-003-03_2026-02-27_0848

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

**PASS.** All output files written exclusively under `_Estimates/EST_DEL-003-03_2026-02-27_0848/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-003-03_2026-02-27_0848` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value. All Detail.csv lines use `Method = PARAMETRIC`, consistent with the declared basis.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts produced:

| Artifact | Status |
|---|---|
| Run_Context.md | Present |
| Items.csv | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Detail.csv | Present |
| WBS_CBS_Matrix.csv | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**
- Columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- 17 rows; all rows have valid PricingMode (UNIT_RATE or LUMP_SUM)
- All rows trace to a source document and section
- Items ITEM-005 through ITEM-017 are artifact/scope traceability items (LUMP_SUM, Qty=1) whose cost is embedded in the four priced labor lines; they carry $0 direct cost but provide scope-to-item traceability

### Detail.csv

**PASS.**
- Columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- 4 rows; all Method values = PARAMETRIC (valid enum)
- No allowance/parametric convention violations (all lines are UNIT_RATE with explicit Qty and UnitRate)
- Arithmetic verified: Qty x UnitRate = Amount for all rows

## S6 — Provenance Discipline

**PASS.**
- 4/4 Detail.csv rows (100%) have non-TBD SourceRef
- All SourceRef entries reference both Level_of_Effort.csv (for hours) and Professional_Staff_Rates.csv (for rates)
- No missing-source offenders

## S7 — Status Reporting

**RUN_STATUS: OK**

Totals are meaningful. All line items are priced with traceable sources. No TBD amounts. No critical input gaps.

Minor advisory notes (do not affect OK status):
- All rates and hours carry MEDIUM confidence (inherent to the parametric source data)
- Estimate covers professional design services only, not physical construction costs

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 17 |
| Items with direct pricing in Detail.csv | 4 (ITEM-001 through ITEM-004) |
| Items priced as $0 (embedded in labor lines) | 13 (ITEM-005 through ITEM-017) |
| TBD amounts | 0 |
| Pricing coverage | 100% |

## Provenance Completeness

| Metric | Value |
|---|---|
| Detail.csv rows with SourceRef | 4/4 (100%) |
| Detail.csv rows with TBD SourceRef | 0 |

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE declared | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (4/4 lines) |
| Mixed methods? | No — 100% PARAMETRIC |
| ALLOW_MIXED_METHODS setting | TRUE (not exercised) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (not needed; all items priced) |
| **Consistent?** | **YES** |

## Quantity Takeoff Coverage

| Check | Result |
|---|---|
| Deliverables in scope | 1 (DEL-003-03) |
| Documents read | 4/4 (Datasheet, Specification, Guidance, Procedure) |
| Missing documents | 0 |
| Items extracted | 17 (4 priced labor lines + 13 scope traceability items) |
| Spaces covered in items | Main shop, wash bay, service pit, office, parts room, utility room, mezzanine |
| Systems covered in items | MUA distribution, air exchanger, high-recovery heating, wash bay ventilation, service pit ventilation |

## What to Fix for a Cleaner Rerun

1. No critical issues requiring fixing.
2. **Optional enhancement:** If construction cost data becomes available for ductwork materials and installation, a companion estimate could be produced for the physical construction scope to complement this design services estimate.
3. **Optional enhancement:** Once scope boundary decision CON-003-03-01 (DEL-003-03 vs. DEL-003-04) is resolved, hours could be re-validated to confirm the allocation is appropriate for the confirmed scope boundary.
