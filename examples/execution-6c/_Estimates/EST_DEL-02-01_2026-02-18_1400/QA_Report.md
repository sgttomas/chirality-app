# QA Report — EST_DEL-02-01_2026-02-18_1400

## RUN_STATUS: OK

---

## S1 — Write Quarantine

**PASS.** All files written under `_Estimates/EST_DEL-02-01_2026-02-18_1400/`. No files outside the estimating tool root were modified.

---

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-02-01_2026-02-18_1400` created under `_Estimates/`.

---

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = RATE_TABLE` is a valid enum value.

---

## S4 — Required Artifacts Exist

**PASS.** All required files present:
- [x] Run_Context.md
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (recommended; produced)
- [x] Blockers.md (optional; produced)

---

## S5 — Detail Schema Integrity

**PASS.**

| Check | Result |
|---|---|
| Detail.csv parseable | YES |
| All required columns present | YES (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid | YES (all 12 rows = RATE_TABLE) |
| Allowance/parametric convention | N/A (no ALLOWANCE or PARAMETRIC method rows) |
| Amount = Qty x UnitRate | YES (verified all 12 rows) |
| Currency consistent | YES (all CAD) |
| Rounding | YES (all amounts are whole dollars) |

### Arithmetic Verification

| LineID | Qty | UnitRate | Expected | Actual | Match |
|---|---|---|---|---|---|
| L-001 | 44 | 145 | 6380 | 6380 | YES |
| L-002 | 24 | 120 | 2880 | 2880 | YES |
| L-003 | 64 | 95 | 6080 | 6080 | YES |
| L-004 | 20 | 155 | 3100 | 3100 | YES |
| L-005 | 12 | 125 | 1500 | 1500 | YES |
| L-006 | 12 | 155 | 1860 | 1860 | YES |
| L-007 | 6 | 125 | 750 | 750 | YES |
| L-008 | 12 | 160 | 1920 | 1920 | YES |
| L-009 | 6 | 130 | 780 | 780 | YES |
| L-010 | 12 | 155 | 1860 | 1860 | YES |
| L-011 | 6 | 125 | 750 | 750 | YES |
| L-012 | 10 | 175 | 1750 | 1750 | YES |
| **TOTAL** | **228** | | **29610** | **29610** | **YES** |

---

## S6 — Provenance Discipline

**PASS.**

| Metric | Value |
|---|---|
| Total priced rows | 12 |
| Rows with SourceRef | 12 |
| Rows with "location TBD" | 0 |
| **Provenance completeness** | **100%** |

All SourceRef values point to specific file + row identifiers (e.g., "Professional_Staff_Rates.csv R-04 + Level_of_Effort.csv row 8").

---

## S7 — Status Reporting

**RUN_STATUS: OK**

Rationale:
- All 12 line items priced with complete provenance
- No TBD amounts
- No fallback methods used
- Basis consistency: 12/12 lines use RATE_TABLE (matches BASIS_OF_ESTIMATE)
- No critical input gaps

---

## S8 — Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or bounded WARNINGS | OK |
| Basis-consistency checks pass | PASS (100% RATE_TABLE) |
| Provenance completeness reported | PASS (100%) |
| Scope coverage explicit | PASS (1/1 deliverable covered; 0 excluded; 0 blocked) |
| No writes outside _Estimates/ | PASS |

---

## Coverage Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-02-01) |
| Deliverables covered | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items | 12 |
| Total hours | 228 |
| Total amount | $29,610 CAD |

---

## Basis Consistency

| Method | Count | % |
|---|---|---|
| RATE_TABLE | 12 | 100% |

**PASS.** All methods match BASIS_OF_ESTIMATE=RATE_TABLE. ALLOW_MIXED_METHODS=FALSE is satisfied.

---

## Blocker Summary (from Dependencies)

| Category | Count |
|---|---|
| Estimate blockers | 0 |
| Execution readiness blockers (informational) | 6 (upstream documents PENDING) |
| Total dependency rows loaded | 16 |

---

## What to Fix for a Cleaner Rerun

1. **No critical fixes required.** This is a clean OK run.
2. **Optional improvements:**
   - Resolve 3D rendering decision (include or exclude) to eliminate ASM-004 assumption
   - Confirm actual firm hourly rates to narrow confidence from MEDIUM to HIGH
   - Confirm LOE hours against actual comparable proposal efforts
   - Resolve upstream document PENDING statuses (informational; does not affect estimate)
