# QA Report — EST_DEL-002-10_2026-02-26_2239

**RUN_STATUS: OK**

---

## S1 — Write Quarantine Respected

- **PASS.** All files written exclusively under `_Estimates/EST_DEL-002-10_2026-02-26_2239/`. No project truth files modified.

## S2 — Snapshot Created

- **PASS.** Snapshot folder `EST_DEL-002-10_2026-02-26_2239` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

- **PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

- **PASS.** All required files present:
  - [x] Run_Context.md
  - [x] Items.csv
  - [x] Summary.md
  - [x] QA_Report.md
  - [x] Source_Index.md
  - [x] Detail.csv (recommended; produced)
  - [x] WBS_CBS_Matrix.csv
  - [x] Decision_Log.md
  - [x] Assumptions_Log.md

## S5 — CSV Schema Integrity

### Items.csv

- **PASS.** 16 rows; all required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes).
- **PricingMode values:** UNIT_RATE (4 rows), LUMP_SUM (12 rows) — all valid.
- **All rows have SourceDoc and SourceSection populated.**
- **No TBD quantities.** All quantities populated from Level_of_Effort.csv or as LS=1.

### Detail.csv

- **PASS.** 16 rows; all required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes).
- **Method values:** All PARAMETRIC — valid and consistent with BASIS_OF_ESTIMATE.
- **Allowance/parametric convention:** Scope-trace lines (DL-005 through DL-016) use Qty=1, Unit=LS, UnitRate=0, Amount=0 — consistent with convention (zero-amount scope traceability lines, not priced items).
- **All priced lines (DL-001 through DL-004):** Qty x UnitRate = Amount verified.
  - DL-001: 6 x 165 = 990 -- PASS
  - DL-002: 4 x 135 = 540 -- PASS
  - DL-003: 24 x 95 = 2,280 -- PASS
  - DL-004: 56 x 170 = 9,520 -- PASS
  - Sum: 990 + 540 + 2,280 + 9,520 = 13,330 -- PASS

## S6 — Provenance Discipline

- **Provenance completeness: 100%.** All 16 rows in Detail.csv have non-TBD SourceRef values.
- **Top missing-source offenders:** None.
- Every priced row traces to a specific row in Professional_Staff_Rates.csv (rate) and Level_of_Effort.csv (hours).
- Scope-trace rows reference the specific Datasheet section, Procedure step, or Specification requirement.

## S7 — Status Reporting

- **RUN_STATUS: OK**
- Totals are meaningful. No critical input gaps.
- All 4 labor items fully priced from parametric sources.
- 12 scope-trace items carry $0 to avoid double-counting while maintaining traceability to engineering content.
- Overall confidence: MEDIUM (consistent across all sources).

## S8 — Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Items.csv reviewed for completeness | 16 items covering all 8 structural subsystems + 4 labor roles + key procedural activities |
| Basis-consistency checks pass | All methods = PARAMETRIC; consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | 100% — no gaps |
| Scope coverage explicit | 1 deliverable, 4 documents read, 8 structural subsystems traced |
| No writes outside _Estimates/ | Confirmed |

---

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|---|---|---|
| Datasheet | 8 items (ITEM-006 through ITEM-013) | All 8 structural subsystems from Scope of Calculations table |
| Specification | 1 item (ITEM-016) | P.Eng. stamp requirement (REQ-011) |
| Guidance | 0 items | Principles and trade-offs inform scope but do not generate additional priceable items |
| Procedure | 3 items (ITEM-005, ITEM-014, ITEM-015) | Design kickoff, QA review, discipline coordination |

**Missing documents:** None. All 4 documents present and read.

---

## Pricing Coverage

| Category | Count | Amount (CAD) | % Priced |
|---|---|---|---|
| Priced labor lines | 4 | 13,330 | 100% |
| Scope-trace lines ($0) | 12 | 0 | N/A (traceability only) |
| TBD lines | 0 | 0 | 0% |

---

## What to Fix for a Cleaner Rerun

1. **No critical fixes needed.** The estimate is complete and fully priced.
2. **Optional improvements:**
   - If firm rate quotes become available for the structural engineering subconsultant, re-run with METHOD=QUOTE for higher confidence.
   - If actual hours tracking data becomes available from similar past projects, a HISTORICAL basis would improve confidence.
   - The foundation reconciliation and crane reconciliation efforts (Procedure Steps 7-8) are not separately estimated. If these are expected to be significant, consider adding explicit hour allocations.
