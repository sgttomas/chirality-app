# QA Report — EST_DEL-002-01_2026-02-27_0539

**RUN_STATUS: OK**

---

## S1 — Write Quarantine Respected

**PASS.** All outputs written under `_Estimates/EST_DEL-002-01_2026-02-27_0539/`. No files outside the estimating tool root were modified.

---

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-002-01_2026-02-27_0539` created under `_Estimates/`.

---

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | Present |
| Items.csv | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Detail.csv | Present (optional; produced) |
| WBS_CBS_Matrix.csv | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |

**PASS.** All required and recommended artifacts produced.

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to a source document and section | PASS — 11 rows; all have SourceDoc and SourceSection populated |
| PricingMode values valid | PASS — 4 UNIT_RATE, 7 LUMP_SUM |
| Row count | 11 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid | PASS — all 4 rows = PARAMETRIC |
| Allowance/parametric convention | N/A — all rows are UNIT_RATE with explicit Qty/Unit/UnitRate; no lump-sum parametric lines in Detail.csv |
| Row count | 4 priced lines |

**PASS.**

---

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows in Detail.csv | 4 |
| Rows with non-TBD SourceRef | 4 |
| Provenance completeness | **100%** |
| Missing-source offenders | None |

**PASS.** All 4 priced lines have complete source references pointing to specific files and row identifiers in the pricing sources.

---

## S7 — Status Reporting

**RUN_STATUS: OK**

Justification:
- All totals are meaningful (no TBD amounts).
- All 4 priced lines have complete provenance.
- Basis consistency is fully met (all PARAMETRIC).
- No critical input gaps.
- All required documents (Datasheet, Specification, Guidance, Procedure) were read and used for quantity takeoff.

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK | No gaps |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 11 items covering all procedure steps and specification artifacts |
| Basis-consistency checks pass | PASS | All lines PARAMETRIC; matches BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% |
| Scope coverage explicit | PASS | 1 deliverable (DEL-002-01); 4 labour roles priced; 7 scope-traceability items embedded in labour |
| No writes outside _Estimates/ | PASS | Confirmed |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Notes |
|---|---|---|---|
| DEL-002-01 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 11 (4 priced labour lines + 7 scope traceability entries) | Full coverage |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Items in Items.csv | 11 |
| Items with explicit pricing in Detail.csv | 4 (the 4 labour role lines) |
| Items that are scope-traceability entries (effort embedded in labour lines) | 7 |
| Items with TBD pricing | 0 |
| Pricing coverage | **100%** |

---

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (4/4 lines) |
| Fallback methods used | None |
| Mixed methods present | No — all PARAMETRIC |
| Consistency | **PASS** |

---

## What to Fix for a Cleaner Rerun

Nothing critical. The estimate is complete as-is. Potential improvements for future iterations:

1. **Rate confidence upgrade:** If firm-specific rates are available (replacing the MEDIUM-confidence parametric rates), pricing confidence could be elevated to HIGH.
2. **Hour estimate validation:** The 70-hour total for a preliminary structural design presentation could be validated against the firm's historical data for similar Alberta industrial buildings.
3. **Fee cross-check quantification:** If a construction value estimate is available, the fee-based cross-check (Professional_Design_Fees.csv DF-02, 1.8% of construction value) could be computed numerically.
