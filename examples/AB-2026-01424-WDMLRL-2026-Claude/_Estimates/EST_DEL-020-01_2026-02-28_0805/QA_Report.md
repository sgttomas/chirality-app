# QA Report — EST_DEL-020-01_2026-02-28_0805

## RUN_STATUS: OK

All 18 line items are fully priced. No TBD amounts remain. The estimate total of $20,790 CAD is complete and internally consistent across labour (parametric rate x hours) and third-party fee components.

---

## S1 — Write Quarantine Respected

**PASS.** All output files written exclusively under `_Estimates/EST_DEL-020-01_2026-02-28_0805/`. No files outside `_Estimates/` were modified. No files in the prior snapshot `EST_DEL-020-01_2026-02-27_0700/` were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-020-01_2026-02-28_0805` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts present:

| Artifact | Status |
|---|---|
| Run_Context.md | Created |
| Items.csv | Copied from prior snapshot (18 rows, unchanged) |
| Detail.csv | Created (18 rows, 2 TBDs resolved) |
| Summary.md | Created |
| QA_Report.md | Created (this file) |
| Source_Index.md | Created |
| Decision_Log.md | Created |
| Assumptions_Log.md | Created |
| WBS_CBS_Matrix.csv | Created |

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | Yes -- all 9 columns present |
| All rows trace to source document and section | Yes -- all 18 rows have SourceDoc and SourceSection populated |
| PricingMode values valid | Yes -- all values are UNIT_RATE or LUMP_SUM |
| Lump-sum convention (Qty=1, Unit=LS) | Yes -- all LUMP_SUM rows have Qty=1, Unit=LS |

### Detail.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | Yes -- all 15 columns present |
| Method values valid | Yes -- all values are PARAMETRIC |
| Allowance/parametric convention | Yes -- all LS items have Qty=1, Unit=LS; UnitRate=Amount for priced LS items |
| All ItemIDs trace back to Items.csv | Yes -- all 18 ItemIDs match |
| No TBD values in UnitRate or Amount | Yes -- 0 TBD values (resolved from 2 in prior snapshot) |

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total rows in Detail.csv | 18 |
| Rows with non-TBD SourceRef | 18 (100%) |
| Rows with `location TBD` SourceRef | 0 (0%) |

**Provenance completeness: 100%** (improved from 89% in prior snapshot).

## S7 — Arithmetic Verification

| Check | Result |
|---|---|
| Sum of all Detail.csv Amount values | $20,790 |
| Labour subtotal (DL-001 through DL-008) | $11,290 (matches 80 hr x blended rate) |
| Third-party fees subtotal (DL-011, DL-018) | $9,500 |
| Labour + fees | $11,290 + $9,500 = $20,790 |
| UnitRate x Qty = Amount (all rows) | PASS -- verified for all 18 rows |

## S8 — Status Reporting

**RUN_STATUS: OK**

Justification:
- All 18 line items are fully priced with no TBD amounts.
- Total of $20,790 CAD is complete (labour $11,290 + third-party fees $9,500).
- All rows have valid SourceRef entries (100% provenance completeness).
- All rows use Method=PARAMETRIC consistent with BASIS_OF_ESTIMATE=PARAMETRIC.
- 2 items have LOW confidence (crane testing, Safety Code fees); all others MED.

## S9 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK | PASS | All TBDs resolved; totals are complete |
| Items.csv reviewed for completeness | PASS | 18 items carried forward from prior snapshot; no scope changes |
| Basis-consistency checks pass | PASS | All 18 Detail.csv rows use Method=PARAMETRIC, consistent with BASIS_OF_ESTIMATE=PARAMETRIC |
| Provenance completeness reported | PASS | 100% provenance completeness (improved from 89%) |
| Scope coverage explicit | PASS | 1 deliverable (DEL-020-01) in scope; all documents read; 0 missing documents |
| No writes outside _Estimates/ | PASS | Confirmed |
| Arithmetic cross-check | PASS | Sum verified: $20,790 |
| Prior snapshot comparison | PASS | Delta of +$9,500 from 2 resolved TBDs; no unexplained changes |
