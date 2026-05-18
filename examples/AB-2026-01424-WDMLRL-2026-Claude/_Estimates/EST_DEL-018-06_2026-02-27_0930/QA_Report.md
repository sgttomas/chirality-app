# QA Report — EST_DEL-018-06_2026-02-27_0930

**RunID:** EST_DEL-018-06_2026-02-27_0930
**Date:** 2026-02-27
**RUN_STATUS: WARNINGS**

---

## S1 — Write Quarantine Respected

**PASS.** All output files are written under `_Estimates/EST_DEL-018-06_2026-02-27_0930/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-018-06_2026-02-27_0930` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts are present:

| Artifact | Status |
|----------|--------|
| Run_Context.md | Present |
| Items.csv | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |
| WBS_CBS_Matrix.csv | Present |
| Detail.csv | Present (optional; produced) |
| Risk_Register.md | Present (optional; produced) |

## S5 — CSV Schema Integrity

### Items.csv

**PASS.** 23 rows. All required columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes.

| Check | Result |
|-------|--------|
| All rows have ItemID | PASS (ITM-001 through ITM-023) |
| All rows have DeliverableID = DEL-018-06 | PASS |
| PricingMode values valid | PASS (UNIT_RATE or LUMP_SUM) |
| All rows trace to SourceDoc | PASS (Datasheet, Specification, Procedure) |
| All rows have SourceSection | PASS |
| Qty values present | PASS (no TBD quantities; all assumed) |

### Detail.csv

**PASS.** 23 rows. All required columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes.

| Check | Result |
|-------|--------|
| All rows have LineID | PASS (DL-001 through DL-023) |
| All ItemID values trace to Items.csv | PASS |
| Method values valid | PASS (all PARAMETRIC) |
| Allowance/parametric convention | PASS — lump-sum items (DL-007 through DL-009, DL-016 through DL-019) have Qty=1, Unit=LS, UnitRate=Amount |
| Currency = CAD for all rows | PASS |

## S6 — Provenance Discipline

### Provenance Completeness

| Category | Lines | With Source Ref | With TBD/ASSUMPTION Ref | Completeness |
|----------|-------|----------------|------------------------|-------------|
| Professional Services | 6 | 6 (CSV file + row) | 0 | 100% |
| Utility Service LS | 3 | 0 | 3 (ASSUMPTION) | 0% (parametric allowance) |
| Earthworks | 2 | 2 (CSV file + item) | 0 | 100% |
| Underground Utilities | 4 | 1 (UU-03 direct) | 3 (proxy/ASSUMPTION) | 25% |
| Permits and Admin | 2 | 0 | 2 (ASSUMPTION) | 0% |
| Testing and Commissioning | 1 | 0 | 1 (ASSUMPTION) | 0% |
| Documentation | 1 | 0 | 1 (ASSUMPTION) | 0% |
| Construction Labour | 4 | 4 (CSV file + trade) | 0 | 100% |
| **Overall** | **23** | **13** | **10** | **56.5%** |

### Top Missing-Source Offenders

1. **DL-008**: Electrical service tie-in ($45,000) — parametric allowance, no quote. Largest single line item.
2. **DL-007**: Natural gas service tie-in ($25,000) — parametric allowance, no quote.
3. **DL-009**: Communication lines tie-in ($8,000) — parametric allowance, no quote.
4. **DL-012**: Underground gas piping ($9,750) — proxy rate from water line (UU-01).
5. **DL-013**: Communication conduit ($4,875) — proxy rate from electrical conduit lower bound (UU-03).

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Rationale: Totals are meaningful as a parametric budget estimate, but material TBDs and assumptions remain:
- Three major lump-sum items totalling $78,000 (56% of total) are parametric allowances with LOW confidence and no direct evidence.
- Trench distance (75m) is assumed and unconfirmed.
- Transformer ownership resolution could add $30,000-$80,000.
- Gas main extension risk could add $50,000-$200,000+.
- No contingency is included.

The estimate is suitable as a preliminary budget placeholder but should not be used for firm pricing without utility provider quotes and civil design confirmation.

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|-------|--------|-------|
| RUN_STATUS is OK or WARNINGS | WARNINGS | Bounded gaps documented |
| Items.csv reviewed for completeness | 23 items extracted from all 4 documents | Comprehensive takeoff for the 3 utility systems |
| Basis-consistency checks | PASS | All lines are PARAMETRIC; consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | 56.5% overall | Top gaps are utility service LS items (no quotes available) |
| Scope coverage explicit | 1 deliverable, 3 SOWs, all covered | No excluded scope items |
| No writes outside _Estimates/ | PASS | Write quarantine respected |

---

## What to Fix for a Cleaner Rerun

1. **Obtain utility provider quotes** for gas, electrical, and communications service connections. This would convert the three largest LS items from PARAMETRIC (LOW confidence) to QUOTE (HIGH confidence) and move 56% of the estimate cost to solid evidence.
2. **Confirm trench distance** from civil design (PKG-005) utility routing drawings. This affects all linear-metre items (trenching, conduit, piping, backfill).
3. **Resolve transformer ownership** (utility-owned vs. customer-owned) per Specification REQ-02.9.
4. **Confirm gas main proximity** and whether a main extension is required.
5. **Confirm communications scope** with County (antenna only vs. full telecom).
6. **Add contingency** — recommend 15-25% given the number of LOW confidence items.
