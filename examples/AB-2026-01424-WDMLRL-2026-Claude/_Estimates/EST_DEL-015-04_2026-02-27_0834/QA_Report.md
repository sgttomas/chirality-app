# QA Report — EST_DEL-015-04_2026-02-27_0834

**RUN_STATUS: WARNINGS**

---

## S1 — Write Quarantine Respected

**PASS.** All files written under `_Estimates/EST_DEL-015-04_2026-02-27_0834/`. No files outside `_Estimates/` were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-015-04_2026-02-27_0834` created.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts produced:
- [x] `Run_Context.md`
- [x] `Items.csv`
- [x] `Summary.md`
- [x] `QA_Report.md`
- [x] `Source_Index.md`
- [x] `Detail.csv`
- [x] `WBS_CBS_Matrix.csv`
- [x] `Decision_Log.md`
- [x] `Assumptions_Log.md`

## S5 — CSV Schema Integrity

### Items.csv
**PASS.**
- Columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- 25 rows; all `PricingMode` values are `UNIT_RATE` or `LUMP_SUM` (valid)
- All rows trace to a SourceDoc and SourceSection
- No TBD quantities in Qty column (all quantified, though some quantities are parametric assumptions)

### Detail.csv
**PASS.**
- Columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- 25 rows; all `Method` values are `PARAMETRIC` or `RATE_TABLE` (valid)
- Lump-sum items (ITEM-001, ITEM-002, ITEM-012 through ITEM-017) correctly use Qty=1, Unit=LS, UnitRate=Amount

### WBS_CBS_Matrix.csv
**PASS.**
- Columns present: WBS_PackageID, WBS_DeliverableID, CBS, Currency, Amount_Total, LineCount, ProvenanceCompletenessPct, Notes
- Totals verified: 54,650 + 5,590 + 14,124 = 74,364.00 CAD

## S6 — Provenance Discipline

**PASS.** Provenance completeness: 25 of 25 rows (100%) have non-TBD SourceRef in Detail.csv.

Top source references by frequency:
| Source | Line Count |
|---|---|
| Electrical_System_Rates.csv (ES-06) | 7 |
| Level_of_Effort.csv + Professional_Staff_Rates.csv | 6 |
| Construction_Labour_Rates.csv | 2 |
| Parametric benchmark (no direct rate table) | 10 |

**Note:** 10 of 25 lines rely on parametric benchmarks without a direct rate table match. These are flagged as parametric estimates and carry MED confidence. No lines have `location TBD` SourceRef.

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Rationale for WARNINGS (not OK):
- 2 line items (L-001, L-002 — crane circuits) carry LOW confidence due to TBD equipment specifications
- Overhead door count (4) and exhaust fan count (2) are parametric assumptions, not confirmed quantities
- No bill of materials exists; all material pricing is parametric
- Unresolved scope boundary conflict (CON-015-04-001) for exhaust fans vs PKG-013

Rationale for not FAILED_INPUTS:
- All 4 engineering documents are present and substantive
- 6 price source files are available and usable
- All 25 items are priced (no TBD amounts)
- Professional staff and construction labour have direct rate table support

## S8 — Operator Acceptance Checklist

| Check | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS — WARNINGS with 6 clearly identified gaps |
| Items.csv reviewed for completeness | PASS — 25 items extracted from all 4 documents |
| Basis-consistency checks pass | PASS — PARAMETRIC primary with RATE_TABLE where rate tables exist; ALLOW_MIXED_METHODS=TRUE |
| Provenance completeness reported | PASS — 100% SourceRef coverage |
| Scope coverage explicit | PASS — 1 deliverable, 4/4 documents read, 0 missing |
| No writes outside _Estimates/ | PASS |

---

## Basis-Consistency Check

| Method | Line Count | Amount (CAD) | % of Total |
|---|---|---|---|
| PARAMETRIC | 17 | 54,650.00 | 73.5% |
| RATE_TABLE | 8 | 19,714.00 | 26.5% |
| **Total** | **25** | **74,364.00** | **100.0%** |

Mixed methods are authorized per `ALLOW_MIXED_METHODS=TRUE`. RATE_TABLE usage is limited to items with direct rate table support (professional staff hours x rates, construction labour hours x rates). All other items use PARAMETRIC, consistent with the primary `BASIS_OF_ESTIMATE`.

---

## What to Fix for a Cleaner Rerun

1. **Obtain crane manufacturer electrical requirements** (DEL-016-01) to replace parametric allowances for crane circuits (L-001, L-002) with quote-based or specification-based pricing.
2. **Confirm overhead door count** from IFC architectural drawings to replace the assumed count of 4.
3. **Resolve exhaust fan scope boundary** (CON-015-04-001) with Project Manager to confirm fan count and scope split with PKG-013.
4. **Obtain a bill of materials** or material takeoff from the IFC electrical design to replace parametric material quantities (conduit, wire, breakers, disconnects).
5. **Obtain equipment nameplate data** for compressor, fire hose pump, and pressure washer to confirm circuit voltages and refine conductor sizing estimates.
6. **Obtain specific material quotes** for conductor bar/festoon systems, circuit breakers, and motor disconnects to replace parametric benchmarks.
