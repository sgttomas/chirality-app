# QA Report

## Run: EST_DEL-02-06_2026-02-18_1500

## RUN_STATUS: OK

---

### S1 -- Write Quarantine

- **Status:** PASS
- All files written under `_Estimates/EST_DEL-02-06_2026-02-18_1500/` only.
- No project truth files modified.

### S2 -- Snapshot Created

- **Status:** PASS
- Snapshot folder: `EST_DEL-02-06_2026-02-18_1500`

### S3 -- BASIS_OF_ESTIMATE Validated

- **Status:** PASS
- Value: `RATE_TABLE` (valid enum)

### S4 -- Required Artifacts Exist

- **Status:** PASS
- `Run_Context.md` -- present
- `Summary.md` -- present
- `QA_Report.md` -- present (this file)
- `Source_Index.md` -- present
- `Decision_Log.md` -- present
- `Assumptions_Log.md` -- present
- `WBS_CBS_Matrix.csv` -- present
- `Detail.csv` -- present (optional; included)

### S5 -- Detail Schema Integrity

- **Status:** PASS
- **Column check:** All 14 required columns present (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes)
- **Method values:** All 13 rows = `RATE_TABLE` (valid; consistent with BASIS_OF_ESTIMATE)
- **Allowance/parametric convention:** Not applicable (no ALLOWANCE or PARAMETRIC lines)
- **Amount verification:** All Qty x UnitRate = Amount (verified)
- **Rounding:** All amounts are whole dollars (DOLLAR rounding applied)

### S6 -- Provenance Discipline

- **Status:** PASS
- **Provenance completeness:** 13/13 rows (100%) have non-TBD SourceRef
- **Top missing-source offenders:** None
- All SourceRef values point to specific file + item ID combinations

### S7 -- Status Reporting

- **RUN_STATUS:** OK
- Totals are meaningful ($642,936 CAD).
- No critical input gaps.
- Two assumptions (ASM-001, ASM-002) are documented but do not create material uncertainty in the total.
- One scope decision (DEC-RC-02 re: fire alarm) is flagged for human review.

### S8 -- Operator Acceptance Checklist

| Check | Result | Notes |
|-------|--------|-------|
| RUN_STATUS is OK or WARNINGS | OK | |
| Basis-consistency passes | PASS | All 13 lines = RATE_TABLE; no mixed methods |
| Provenance completeness reported | 100% | No gaps |
| Scope coverage explicit | PASS | 1 deliverable; 13 lines; inclusions/exclusions documented |
| No writes outside _Estimates/ | PASS | |

---

## Coverage Analysis

### Deliverable Coverage

| DeliverableID | Status | Lines | Amount (CAD) |
|---------------|--------|-------|-------------|
| DEL-02-06 | COVERED | 13 | $642,936 |

### SOW Item Coverage (via decomposition traceability)

| SOW Item | Covered By Lines | Status |
|----------|-----------------|--------|
| SOW-0203 (partial -- electrical) | L-0602 (bay power distribution includes compressed air feed) | COVERED |
| SOW-0208 (partial -- IT/power) | L-0605 (15 EM workstation data drops within 45 total) | COVERED |
| SOW-0224 | L-0605, L-0606 (IT/telecom drops + backbone) | COVERED |
| SOW-0225 | L-0608 (apparatus bay displays) | COVERED |
| SOW-0226 | L-0607 (PA system) | COVERED |
| SOW-0227 | L-0601, L-0602 (power distribution) | COVERED |
| SOW-0228 | L-0603, L-0604, L-0609 (LED lighting + emergency lighting) | COVERED |

### Basis Consistency

- **Expected method:** RATE_TABLE
- **Actual methods:** 13/13 = RATE_TABLE
- **Deviations:** 0
- **ALLOW_MIXED_METHODS:** FALSE
- **Result:** PASS

### Dependency-Informed Blockers

- **Upstream prerequisites (TBD satisfaction):** 4 (DEL-02-01, DEL-02-02, DEL-02-05, Functional Program)
- **Upstream interfaces (TBD satisfaction):** 3 (DEL-02-07, DEL-03-04, DEL-02-04)
- **Blocking impact on estimate:** NONE -- rate-table pricing is based on area/quantity parameters and does not require resolved upstream inputs for pricing. Upstream dependencies will affect detailed design but not the parametric rate application.

---

## Improvement Actions (for cleaner rerun)

1. **Confirm bay vs. institutional area split** (ASM-001): When DEL-02-01 floor plan is available, replace the 12,800/5,200 sf assumption with actual take-off areas.
2. **Confirm commissioning hours** (ASM-002): When DEL-01-07 commissioning plan is available, replace the 100-hour assumption with planned labor.
3. **Resolve fire alarm scope ownership** (DEC-RC-02): Confirm whether fire alarm system is within DEL-02-06 or assigned elsewhere. If included, add ES-08 line (~$63,000).
4. **Update data drop count** (PP-27): When IT/telecom design is advanced, confirm 45 drops or update quantity.
