# QA Report -- EST_DEL-01-06_2026-02-18_2359

**RUN_STATUS: OK**

---

## S1 -- Write Quarantine Respected

**PASS.** All output files written exclusively under `_Estimates/EST_DEL-01-06_2026-02-18_2359/`. No project truth files modified.

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-01-06_2026-02-18_2359` created.

## S3 -- BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = RATE_TABLE` is a valid enum value.

## S4 -- Required Artifacts Exist

**PASS.** All required files produced:
- [x] Run_Context.md
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (optional; produced)

## S5 -- Detail Schema Integrity

**PASS.**
- Detail.csv contains all 14 required columns: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes.
- All `Method` values = `RATE_TABLE` (valid enum).
- No allowance/parametric convention rows present (not applicable; both rows are standard hourly pricing).
- Amount = Qty x UnitRate for all rows (verified: 12 x 175 = 2,100; 8 x 145 = 1,160).

## S6 -- Provenance Discipline

**PASS.**
- 2/2 priced rows (100%) include non-TBD `SourceRef` values.
- All SourceRefs point to specific files and row identifiers.
- Top missing-source offenders: None.

## S7 -- Status Reporting

**PASS.** `RUN_STATUS = OK`.
- Totals are meaningful ($3,260 CAD).
- No critical input gaps.
- No TBD amounts.

## S8 -- Operator Acceptance Checklist

| Check | Status |
|---|---|
| RUN_STATUS is OK or bounded WARNINGS | OK |
| Basis-consistency: all Methods match BASIS_OF_ESTIMATE | PASS (2/2 = RATE_TABLE) |
| Provenance completeness reported | PASS (100%) |
| Scope coverage explicit | PASS (1/1 priced; 0 blocked; 0 TBD) |
| No writes outside _Estimates/ | PASS |

---

## Detailed Checks

### Method Consistency

| Method | Count | Expected (per BASIS_OF_ESTIMATE) |
|---|---|---|
| RATE_TABLE | 2 | Yes |
| Other | 0 | N/A |

ALLOW_MIXED_METHODS = FALSE; no violations.

### Amount Verification

| LineID | Qty | Unit | UnitRate | Expected Amount | Actual Amount | Match |
|---|---|---|---|---|---|---|
| L-0106-01 | 12 | hr | 175 | 2,100 | 2,100 | YES |
| L-0106-02 | 8 | hr | 145 | 1,160 | 1,160 | YES |
| **Total** | | | | **3,260** | **3,260** | **YES** |

### Rounding Verification

ROUNDING = DOLLAR. All amounts are already whole-dollar values. No rounding adjustments required.

### Dependency/Blocker Summary (from Dependencies.csv)

| DependencyID | Target | Type | Status | Impact on Estimate |
|---|---|---|---|---|
| DEP-0106-005 | DEL-01-05 (Schedule B) | PREREQUISITE | PENDING | Execution sequencing only; does not affect production hour estimate |
| DEP-0106-006 | DEL-01-03 (Bonding/Insurance) | PREREQUISITE | PENDING | Execution sequencing only; does not affect production hour estimate |
| DEP-0106-007 | DEL-01-04 (Schedule A) | PREREQUISITE | PENDING | Execution sequencing only; does not affect production hour estimate |
| DEP-0106-010 | DEC-011/012/013 | PREREQUISITE | SATISFIED | All decisions closed; no impact |

---

## What to Fix for a Cleaner Rerun

Nothing. This run is clean. All checks pass. No warnings or gaps to address.
