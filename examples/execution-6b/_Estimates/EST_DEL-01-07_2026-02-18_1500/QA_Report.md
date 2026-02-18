# QA Report — EST_DEL-01-07_2026-02-18_1500

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

**PASS.** All files written under `_Estimates/EST_DEL-01-07_2026-02-18_1500/`. No files outside `_Estimates/` were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-01-07_2026-02-18_1500` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `RATE_TABLE` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required files present:
- [x] Run_Context.md
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv

Additional files produced:
- [x] Detail.csv
- [x] Blockers.md

## S5 — Detail Schema Integrity

**PASS.**
- Detail.csv contains all 14 required columns: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- Method values: all `RATE_TABLE` (valid enum)
- No allowance/parametric lines present, so allowance convention check is N/A
- 2 rows; both parseable; no empty required fields

## S6 — Provenance Discipline

**PASS.**
- Provenance completeness: **100%** (2/2 rows have non-TBD SourceRef)
- L-0107-01: references Level_of_Effort.csv row DEL-01-07/R-22 + Professional_Staff_Rates.csv R-22
- L-0107-02: references Level_of_Effort.csv row DEL-01-07/R-02 + Professional_Staff_Rates.csv R-02
- No `location TBD` entries

## S7 — Status Reporting

**RUN_STATUS: OK**
- All totals are meaningful (no TBD amounts)
- No critical input gaps
- All line items fully sourced

## S8 — Operator Acceptance Checklist

| Check | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Basis-consistency: all Method values match BASIS_OF_ESTIMATE | PASS (all RATE_TABLE) |
| Provenance completeness reported | PASS (100%) |
| Scope coverage explicit | PASS (1 deliverable in scope, 1 covered, 0 missing, 0 blocked) |
| No writes outside _Estimates/ | PASS |

---

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (priced) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items produced | 2 |
| Lines with TBD amounts | 0 |
| Lines with TBD SourceRef | 0 |

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Methods used in Detail.csv | RATE_TABLE (2/2 lines) |
| Mixed methods detected | No |
| ALLOW_MIXED_METHODS | FALSE |
| Consistency | PASS |

## Blocker Summary (from Dependencies)

| Metric | Value |
|---|---|
| Total dependencies reviewed | 11 |
| Hard blockers to estimating | 0 |
| PENDING external prerequisites | 2 (production-level, not estimate-level) |
| Internal interface dependencies | 3 (coordination, not blocking) |

## Arithmetic Verification

| LineID | Qty | UnitRate | Expected Amount | Actual Amount | Check |
|---|---|---|---|---|---|
| L-0107-01 | 16 | 105 | 1680 | 1680 | PASS |
| L-0107-02 | 4 | 175 | 700 | 700 | PASS |
| **Total** | **20** | -- | **2380** | **2380** | **PASS** |

## What to Fix for a Cleaner Rerun

Nothing required. This is a clean run with no warnings or gaps. To improve confidence:
1. Validate rates against actual contracted/payroll rates (currently MARKET estimates).
2. Validate hours against historical actuals for similar firm profile deliverables.
3. Confirm no external production costs (graphic design, photography) are expected.
