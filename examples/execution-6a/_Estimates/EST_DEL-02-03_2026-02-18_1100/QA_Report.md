# QA Report

## Run: EST_DEL-02-03_2026-02-18_1100

## RUN_STATUS: WARNINGS

---

### S1 -- Write Quarantine: PASS

All files written under `_Estimates/EST_DEL-02-03_2026-02-18_1100/`. No files modified outside the estimating tool root.

### S2 -- Snapshot Created: PASS

Snapshot folder `EST_DEL-02-03_2026-02-18_1100` created under `_Estimates/`.

### S3 -- BASIS_OF_ESTIMATE Validated: PASS

`RATE_TABLE` is a valid enum value. Mixed methods (ALLOWANCE fallback) approved via `ALLOW_MIXED_METHODS=TRUE` and `FALLBACK_POLICY=ALLOW_ALLOWANCE`.

### S4 -- Required Artifacts Exist: PASS

| Artifact | Status |
|---|---|
| Run_Context.md | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |
| WBS_CBS_Matrix.csv | Present |
| Detail.csv | Present |
| Blockers.md | Present |

### S5 -- Detail Schema Integrity: PASS

| Check | Result |
|---|---|
| CSV parseable | Yes |
| All required columns present | Yes (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid | Yes (RATE_TABLE: 27 lines; ALLOWANCE: 5 lines) |
| Allowance convention respected | Yes (all 5 ALLOWANCE lines have Qty=1, Unit=LS, UnitRate=Amount) |
| Amount = Qty x UnitRate | Verified for all 32 lines |
| Currency consistent | Yes (all CAD) |

### S6 -- Provenance Discipline: PASS

| Metric | Value |
|---|---|
| Total priced rows | 32 |
| Rows with SourceRef provided | 32 |
| Rows with SourceRef = TBD | 0 |
| **Provenance completeness** | **100%** |

No missing-source offenders.

### S7 -- Status Reporting: WARNINGS

**RUN_STATUS = WARNINGS** for the following reasons:

1. **Mixed methods (material):** 5 of 32 lines (28.5% of total dollar value) use ALLOWANCE method rather than the primary RATE_TABLE basis. These items lack rate table support and are priced using professional judgment or explicit allowance values from Equipment_Pricing.csv.

2. **Area assumptions (material):** Support space areas (locker room, PPE room, office, washroom) are assumed based on functional program hints. No confirmed floor plan is available. Changes to areas would proportionally affect approximately 50% of the total estimate value.

3. **Scope boundary requires validation:** The boundary between DEL-02-03 (bay-specific fit-up) and DEL-02-01 (general interior) and DEL-02-04 (structural) has been applied per the brief's cost ownership rules but may require human confirmation, especially for the locker room and support spaces which serve both the PW shop bays and potentially other PW functions.

### Basis-Consistency Check

| Check | Result |
|---|---|
| Primary basis | RATE_TABLE |
| Lines matching primary | 27 / 32 (84.4%) |
| Lines using fallback | 5 / 32 (15.6%) |
| Fallback method | ALLOWANCE |
| Fallback policy | ALLOW_ALLOWANCE (approved) |
| Mixed methods flag | ALLOW_MIXED_METHODS=TRUE (approved) |
| **Verdict** | PASS (deviations approved and logged) |

### Coverage Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-02-03) |
| Deliverables estimated | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Scope items covered | SOW-0209, SOW-0210, SOW-0211, SOW-0212 |
| Scope items missing | 0 |

### Blocker Summary (from dependency evidence)

| Metric | Value |
|---|---|
| Total dependencies read | 17 |
| Execution prerequisites | 5 (DEL-02-01, DEL-02-04, DEL-02-05, DEL-02-06, DEL-02-07) |
| Critical blockers for estimating | 0 |
| Constraints noted | 2 (Owner wash bay decision; Alberta Building Code) |

### What to Fix for a Cleaner Rerun

1. **Provide confirmed floor plans** with measured areas for PW locker room, PPE room, shop office, and washroom. This would convert 8 area-assumption-driven lines from assumed to confirmed quantities.

2. **Obtain quotes for compressed air piping** to replace the $15,000 allowance (L-006) with a RATE_TABLE or QUOTE-based line item.

3. **Obtain quotes for warehouse shelving/racking** to replace the $12,000 allowance (L-009) with evidence-based pricing.

4. **Obtain quotes for shower rough-in** to replace the $8,000 allowance (L-032) with evidence-based pricing.

5. **Confirm PPE/first aid room scope** to replace the $3,500 allowance (L-020) with itemized fit-up.

6. **Validate scope boundary** between DEL-02-03 and DEL-02-01 for locker room/support space interior partitions -- currently included in DEL-02-03 per the "bay-specific fit-up" rule but could be claimed by either deliverable.
