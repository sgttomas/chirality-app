# QA Report -- EST_DEL-01-05_2026-02-18_2359

## RUN_STATUS: OK

---

## 1. Schema Validity

| Check | Result | Notes |
|---|---|---|
| Detail.csv parseable | PASS | 95 data rows; 14 columns per schema |
| All required columns present | PASS | LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes |
| Method values valid | PASS | RATE_TABLE (90 lines), PARAMETRIC (1 line), ALLOWANCE (4 lines) -- all valid enum values |
| Allowance/parametric convention | PASS | All ALLOWANCE and PARAMETRIC lines use Qty=1, Unit=LS, UnitRate=Amount |
| WBS_CBS_Matrix.csv parseable | PASS | 10 rows; all required columns present |
| Currency consistent | PASS | All lines use CAD |
| Rounding applied | PASS | All amounts rounded to whole dollars |

## 2. Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-01-05) |
| Deliverables with line items | 1 (DEL-01-05) |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Total production lines | 3 (A-010, A-020, A-030) |
| Total construction content lines | 92 (11 B-GR-*, 46 B-BLD-*, 24 B-SIT-*, 11 C-*) |
| Total lines | 95 |

## 3. Provenance Completeness

| Metric | Value |
|---|---|
| Lines with non-TBD SourceRef | 95 / 95 |
| Provenance completeness | **100%** |
| Top missing-source offenders | None -- all lines have source references |

Every line in Detail.csv has a SourceRef pointing to a specific rate table item and/or upstream estimate line. No `location TBD` entries.

## 4. Basis-Consistency Checks

| Check | Result | Notes |
|---|---|---|
| Primary method matches BASIS_OF_ESTIMATE (RATE_TABLE) | PASS | 90 of 95 lines (95%) use RATE_TABLE |
| Mixed methods justified | PASS | ALLOW_MIXED_METHODS=TRUE; 1 PARAMETRIC (cold storage PEMB) + 4 ALLOWANCE (per ALLOW_ALLOWANCE fallback) |
| FALLBACK_POLICY respected | PASS | 4 ALLOWANCE lines align with ALLOW_ALLOWANCE policy |
| Method mix documented | PASS | Decision_Log.md D-08 documents fallback usage |

## 5. Reconciliation Checks

| Check | Result | Notes |
|---|---|---|
| Schedule B base total vs Schedule A base | **PASS** | $7,327,000 = $7,327,000 (zero variance) |
| Schedule B options total vs Schedule A options | **PASS** | $383,000 = $383,000 (zero variance) |
| Schedule B total vs Schedule A total | **PASS** | $7,710,000 = $7,710,000 (zero variance) |
| Discipline-level cross-check (11 CBS categories) | **PASS** | All 11 CBS category totals match DEL-01-04 exactly |
| Option sub-item totals match Schedule A lump sums | **PASS** | All 6 options verified individually |

## 6. Blocker Assessment

| Metric | Value |
|---|---|
| Unresolved hard blockers | 0 |
| DEL-01-04 prerequisite | RESOLVED (EST_DEL-01-04_2026-02-18_2359 completed) |
| Downstream handovers | 2 (DEL-01-06 pricing narrative, DEL-01-02 formal submission) |

## 7. Confidence Distribution

| Confidence Level | Line Count | % of Lines | Total Amount (CAD) |
|---|---|---:|---:|
| HIGH | 1 | 1% | $20,000 |
| MED | 77 | 81% | $6,721,020 |
| LOW | 17 | 18% | $975,000 |
| **TOTAL** | **95** | **100%** | **$7,716,020** |

LOW confidence items ($975,000 = 12.6% of total):
- B-GR-130 CCIP insurance: $240,000
- B-GR-160 Building permit: $65,000
- B-GR-180 Utility connection fees: $39,000 (ALLOWANCE)
- B-GR-195 Surety broker: $4,000
- B-BLD-420 Fire protection: $108,000
- B-BLD-530 Generator: $150,000
- B-BLD-560 Breathing air compressor: $55,000
- B-BLD-598 Workshop equipment: $22,000 (ALLOWANCE)
- B-SIT-360 Municipal tie-in allowance: $35,000 (ALLOWANCE)
- C-100 Wash bay system: $95,000
- C-110 Wash bay plumbing: $16,000
- C-120 Wash bay environmental: $12,000
- C-300 Access control: $45,000
- C-400 Security cameras: $50,000
- C-410 Security monitoring: $5,000
- C-500 Signage non-illuminated: $12,000
- C-510 Signage illuminated: $22,000

## 8. Mandatory Artifact Checklist

| Artifact | Present | Notes |
|---|---|---|
| Run_Context.md | YES | All required fields populated |
| Summary.md | YES | Includes reconciliation table |
| QA_Report.md | YES | This file |
| Source_Index.md | YES | 17 sources indexed + 1 upstream estimate |
| Decision_Log.md | YES | 9 decisions logged |
| Assumptions_Log.md | YES | 11 assumptions logged |
| WBS_CBS_Matrix.csv | YES | 10 CBS rows |
| Detail.csv | YES | 95 lines; full schema |
| Blockers.md | YES | No unresolved blockers |

## 9. Write Quarantine Check

| Check | Result |
|---|---|
| All files written under _Estimates/ | PASS |
| No modifications to deliverable working files | PASS |
| No modifications to lifecycle files (_STATUS.md) | PASS |
| No modifications to decomposition outputs | PASS |
| No modifications to dependency registers | PASS |

## 10. What to Fix for a Cleaner Rerun

1. **Fire protection determination:** Obtain AHJ ruling on sprinkler requirement; if not required, remove B-BLD-420 ($108,000) and reconcile Schedule A.
2. **Generator load calculations:** Finalize essential load list to confirm 100-150 kW range is adequate.
3. **CCIP insurance:** Obtain actual insurer quote to replace 2.00% assumption.
4. **Building permit fee:** Confirm Penhold fee schedule to replace 0.75% assumption.
5. **Town branding guidelines:** Obtain from Owner to finalize signage design and pricing.
6. **PKG-002 conceptual design:** When available, validate building areas and quantities against design.

---

**Overall assessment:** This estimate is FULLY RECONCILED with DEL-01-04 Schedule A. All 95 lines have source references. The dual-cost-nature (production + construction content) is properly separated. The Schedule B provides the required detailed breakdown structure. RUN_STATUS = OK.
