# QA Report

## Run: EST_DEL-03-05_2026-02-18_2000

### RUN_STATUS: WARNINGS

---

### S1 -- Write Quarantine Respected

| Check | Result |
|---|---|
| All output files written under _Estimates/ | PASS |
| No files modified outside _Estimates/ | PASS |

### S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists: EST_DEL-03-05_2026-02-18_2000/ | PASS |

### S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = RATE_TABLE | PASS (valid enum value) |

### S4 -- Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT |
| Blockers.md | PRESENT |

### S5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv parseable | PASS |
| All required columns present (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (RATE_TABLE, ALLOWANCE) | PASS |
| Allowance convention (Qty=1, Unit=LS, UnitRate=Amount) for ALLOWANCE rows | PASS (L-02: Qty=1, Unit=LS, UnitRate=5000, Amount=5000; L-05: Qty=1, Unit=LS, UnitRate=1200, Amount=1200) |
| RATE_TABLE rows using LS convention for lump-sum items | PASS (L-01: Qty=1, Unit=LS; L-03: Qty=1, Unit=LS; L-04: Qty=1, Unit=LS) |
| All Amount values are integers (ROUNDING=DOLLAR) | PASS |
| Currency = CAD for all rows | PASS |
| No TBD amounts | PASS |

### S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 5 |
| Rows with non-TBD SourceRef | 5 |
| Provenance completeness | **100%** |
| Rows with "location TBD" SourceRef | 0 |

**Top missing-source offenders:** None. All rows have evidence-linked SourceRef.

### S7 -- Basis-Consistency Checks

| Check | Result |
|---|---|
| Primary basis: RATE_TABLE | 3 of 5 rows (60%) |
| Fallback basis: ALLOWANCE | 2 of 5 rows (40%) |
| ALLOW_MIXED_METHODS = TRUE | Authorized |
| FALLBACK_POLICY = ALLOW_ALLOWANCE | Authorized |
| All ALLOWANCE rows have documented rationale in Decision_Log.md | PASS (DEC-EST-02) |

**Basis consistency verdict:** PASS with authorized deviations.

### Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-03-05) |
| Deliverables covered (at least 1 priced row) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items produced | 5 |

### Blocker Counts (from dependency evidence)

| Category | Count |
|---|---|
| External regulatory blockers | 4 (AEPA + Town approvals) |
| Upstream deliverable interfaces | 2 (DEL-03-02 outputs) |
| Document prerequisites (status unknown) | 5 (4 assumed available; 1 post-award) |
| **Total** | **11** |

### Confidence Assessment

| Risk Factor | Assessment |
|---|---|
| Professional service fees (L-01, L-04) | MED -- rates from published source; scope well-defined |
| ABWRET-A replacement fee (L-03) | HIGH -- exact amount from 2021 Wetland Assessment ($10,769.54) |
| Regulatory application fees (L-02, L-05) | LOW -- fee schedules TBD; amounts are allowances |
| AEPA conditions of approval | UNKNOWN -- may add costs not in this estimate |
| 2021 assessment validity | MEDIUM RISK -- assessments are ~5 years old; AEPA may require updates |

### Warnings Affecting RUN_STATUS

1. **AEPA Water Act approval PENDING** -- conditions of approval may impose additional costs (not quantifiable until approval issued).
2. **2 ALLOWANCE line items** ($6,200 / 14% of total) -- fee schedules uncertain.
3. **2021 assessment age** -- Wetland Assessment and Environmental Assessment are ~5 years old; if AEPA requires updated assessments, significant additional costs would apply.
4. **Upstream DEL-03-02 interface unresolved** -- stormwater and earthwork information may reveal additional environmental consulting scope.

**RUN_STATUS = WARNINGS** because:
- All line items have amounts (no TBD amounts).
- Provenance is 100% complete.
- However, AEPA approval is PENDING, 14% of the estimate is ALLOWANCE, and conditions of approval may add unmeasured costs.

### What to Fix for a Cleaner Rerun

1. Confirm AEPA Water Act application status and any conditions of approval (resolves 2 of 4 external blockers).
2. Confirm ABWRET-A fee has not been updated since 2021 (resolves ASM-03).
3. Obtain DEL-03-02 stormwater management approach and earthwork cut/fill volumes (resolves 2 upstream interfaces).
4. Confirm Town of Penhold development permit fee schedule (resolves L-05 from ALLOWANCE to RATE_TABLE).
5. Confirm whether 2021 Ghostpine assessments require updates (resolves ASM-01, ASM-02).
