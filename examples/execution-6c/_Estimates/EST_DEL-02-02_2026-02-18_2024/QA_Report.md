# QA Report — EST_DEL-02-02_2026-02-18_2024

**Snapshot:** EST_DEL-02-02_2026-02-18_2024
**Date:** 2026-02-18
**RUN_STATUS: OK**

---

## S1 — Write Quarantine Respected

| Check | Result |
|-------|--------|
| All files written under `_Estimates/EST_DEL-02-02_2026-02-18_2024/` | PASS |
| No deliverable working files modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition outputs modified | PASS |
| No dependency registers modified | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|-------|--------|
| Snapshot folder exists | PASS |
| Folder name follows convention `EST_{LABEL}_{DATE}_{TIME}` | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|-------|--------|
| `BASIS_OF_ESTIMATE` provided | PASS |
| Value = `RATE_TABLE` (valid enum) | PASS |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|----------|--------|
| Run_Context.md | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT (recommended; produced) |
| Blockers.md | PRESENT (optional; produced) |

---

## S5 — Detail Schema Integrity

| Check | Result | Notes |
|-------|--------|-------|
| Detail.csv is parseable | PASS | 8 data rows + header |
| All required columns present | PASS | LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes |
| `Method` values valid | PASS | All 8 rows = RATE_TABLE |
| Allowance/parametric convention | N/A | No ALLOWANCE or PARAMETRIC method rows |
| Amount = Qty x UnitRate (all rows) | PASS | Verified: 20x145=2900, 8x120=960, 8x155=1240, 10x155=1550, 10x160=1600, 10x155=1550, 8x165=1320, 6x175=1050 |
| Sum of line amounts = total | PASS | 2900+960+1240+1550+1600+1550+1320+1050 = 12170 |

---

## S6 — Provenance Discipline

| Metric | Value |
|--------|-------|
| Total priced rows | 8 |
| Rows with non-TBD SourceRef | 8 |
| **Provenance completeness** | **100%** |
| Rows with `location TBD` | 0 |
| Top missing-source offenders | None |

All 8 lines carry dual-source references (Professional_Staff_Rates.csv for rate + Level_of_Effort.csv for quantity).

---

## S7 — Status Determination

| Criterion | Assessment |
|-----------|------------|
| Totals meaningful | YES — $12,170 CAD based on 80 hours across 8 roles |
| Critical input gaps | NONE — all rates and hours sourced |
| TBD amounts | 0 of 8 lines |
| Basis consistency | 100% RATE_TABLE (matches BASIS_OF_ESTIMATE) |
| **RUN_STATUS** | **OK** |

---

## Coverage Report

| Metric | Value |
|--------|-------|
| Deliverables in SCOPE | 1 (DEL-02-02) |
| Deliverables with line items | 1 |
| Deliverables blocked | 0 |
| Deliverables missing/excluded | 0 |
| SOW items covered | 5 (SOW-010, SOW-011, SOW-013, SOW-014, SOW-015) |

---

## Basis-Consistency Check

| Check | Result |
|-------|--------|
| BASIS_OF_ESTIMATE = RATE_TABLE | PASS |
| All Detail.csv Method values = RATE_TABLE | PASS (8/8) |
| ALLOW_MIXED_METHODS = FALSE | PASS (no mixed methods) |
| FALLBACK_POLICY = STRICT | PASS (no fallback needed; all items priced) |

---

## Blocker Assessment (from dependency evidence)

| Metric | Value |
|--------|-------|
| Total dependency rows reviewed | 19 |
| Upstream prerequisites (documents) | 4 (RFP, ADD-01, ADD-03, Geotech Report) |
| Upstream interfaces (deliverables) | 1 (DEL-02-01 Concept Design Package) |
| **Estimate-blocking dependencies** | **0** |
| Production-sequencing dependencies | 5 (documents + DEL-02-01 must be available for production, not for pricing) |

---

## Arithmetic Verification

| LineID | Qty | UnitRate | Expected | Actual | Match |
|--------|-----|----------|----------|--------|-------|
| L-0202-01 | 20 | 145 | 2900 | 2900 | YES |
| L-0202-02 | 8 | 120 | 960 | 960 | YES |
| L-0202-03 | 8 | 155 | 1240 | 1240 | YES |
| L-0202-04 | 10 | 155 | 1550 | 1550 | YES |
| L-0202-05 | 10 | 160 | 1600 | 1600 | YES |
| L-0202-06 | 10 | 155 | 1550 | 1550 | YES |
| L-0202-07 | 8 | 165 | 1320 | 1320 | YES |
| L-0202-08 | 6 | 175 | 1050 | 1050 | YES |
| **TOTAL** | **80** | | **12170** | **12170** | **YES** |

---

## WBS/CBS Matrix Cross-Check

| CBS | Matrix Amount | Detail Sum | Match |
|-----|--------------|------------|-------|
| PROF_DESIGN | 9800 | 2900+960+1240+1550+1600+1550 = 9800 | YES |
| PROF_SPECIALTY | 1320 | 1320 | YES |
| PROF_MGMT | 1050 | 1050 | YES |
| **TOTAL** | **12170** | **12170** | **YES** |

---

## What to Fix for a Cleaner Rerun

Nothing required. This is a clean run with full provenance, consistent basis, and no TBD amounts.

Optional improvements for future runs:
1. **CBS codes from decomposition.** If the decomposition is updated with explicit `CBSHint` values, the deterministic category-based mapping could be replaced with authoritative codes.
2. **Rate confidence.** All rates are MARKET/MEDIUM confidence. Actual firm rates would increase confidence to HIGH.
3. **LOE confidence.** All hours are PARAMETRIC/MEDIUM. Actual time tracking from comparable proposals would increase confidence.
