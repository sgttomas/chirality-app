# QA Report — EST_DEL-04-02_2026-02-18_1100

## RUN_STATUS: OK

---

## S1 -- Write Quarantine Respected
**PASS.** All files written exclusively under `_Estimates/EST_DEL-04-02_2026-02-18_1100/`. No files outside `_Estimates/` were modified.

## S2 -- Snapshot Created
**PASS.** Snapshot folder `EST_DEL-04-02_2026-02-18_1100` created under `_Estimates/`.

## S3 -- BASIS_OF_ESTIMATE Validated
**PASS.** `BASIS_OF_ESTIMATE = RATE_TABLE` is a valid enum value.

## S4 -- Required Artifacts Exist
**PASS.** All required files are present:
- [x] Run_Context.md
- [x] Summary.md
- [x] QA_Report.md (this file)
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv

Optional files also produced:
- [x] Detail.csv
- [x] Blockers.md

## S5 -- Detail Schema Integrity
**PASS.**
- Detail.csv contains all 14 required columns: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- All `Method` values are `RATE_TABLE` (valid enum)
- No ALLOWANCE or PARAMETRIC lines exist, so the allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount) is not applicable and does not need validation
- All Amount values are computed correctly from Qty x UnitRate

### Amount Verification

| LineID | Qty | UnitRate | Expected | Actual | Check |
|---|---|---|---|---|---|
| L-0402-01 | 2 | 13500 | 27000 | 27000 | PASS |
| L-0402-02 | 2 | 1800 | 3600 | 3600 | PASS |
| L-0402-03 | 2 | 600 | 1200 | 1200 | PASS |
| L-0402-04 | 2 | 600 | 1200 | 1200 | PASS |
| L-0402-05 | 2 | 5400 | 10800 | 10800 | PASS |
| L-0402-06 | 2 | 512 | 1024 | 1024 | PASS |
| L-0402-07 | 2 | 131 | 262 | 262 | PASS |
| L-0402-08 | 32 | 72 | 2304 | 2304 | PASS |
| L-0402-09 | 8 | 72 | 576 | 576 | PASS |
| L-0402-10 | 48 | 62 | 2976 | 2976 | PASS |
| L-0402-11 | 2 | 350 | 700 | 700 | PASS |
| L-0402-12 | 2 | 85 | 170 | 170 | PASS |
| **TOTAL** | | | **51,812** | **51,812** | **PASS** |

## S6 -- Provenance Discipline
**PASS (with notes).**
- **Total priced lines:** 12
- **Lines with direct rate table SourceRef:** 10 (83%)
- **Lines with `location TBD` SourceRef:** 2 (17%)

### Top Missing-Source Offenders

| LineID | Description | Amount | Issue |
|---|---|---|---|
| L-0402-11 | Emergency exit lights | $700 | No rate table entry for exit lights; unit rate from assumption ASM-10 |
| L-0402-12 | Weatherproof light switches | $170 | No rate table entry for switches; unit rate from assumption ASM-11 |

**Combined gap:** $870 (1.7% of total). These are minor accessory items. Under STRICT fallback policy, amounts are retained as reasonable estimates but flagged with `location TBD`.

## S7 -- Status Reporting
**RUN_STATUS = OK**

Justification:
- All 12 line items are priced (no TBD amounts)
- 83% provenance completeness; remaining 17% ($870) is bounded to minor accessory items
- Basis-consistency check passes: all lines use RATE_TABLE method
- No critical input gaps
- No blocking dependencies

## Basis-Consistency Check
**PASS.** All 12 lines use `Method = RATE_TABLE`, matching `BASIS_OF_ESTIMATE = RATE_TABLE`. No mixed methods. `ALLOW_MIXED_METHODS = FALSE` is respected.

## Blocker Summary
- **Total dependencies examined:** 9 (from DEL-04-02 Dependencies.csv)
- **Estimate-blocking dependencies:** 0
- **Design-phase coordination items:** 9 (do not prevent pricing at proposal stage)
- See Blockers.md for detail.

## Scope Coverage
| Metric | Count |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (at least 1 priced line) | 1 |
| Deliverables blocked | 0 |
| Deliverables missing/skipped | 0 |

## Rounding Check
**PASS.** `ROUNDING = DOLLAR` requested. All Amount values are whole-dollar integers.

## Cross-Reference Checks

### Cost Ownership Boundary Compliance
- **Door opener electrical feeds:** NOT included in this estimate (correctly owned by DEL-04-04 per brief)
- **Building shell/structure:** NOT included (correctly owned by DEL-04-01)
- **Overhead doors, person doors, hardware, aprons, weatherstripping:** ALL included (correctly owned by DEL-04-02)

### Quantity Consistency
- Overhead doors: 2 (matches PP-14 from Assumed_Project_Parameters.csv; matches EQ-02 Quantity_Assumed=2; matches SOW-0302 and Datasheet)
- Person doors: 2 (matches SOW-0302 and Datasheet)
- Concrete aprons: 2 (one per overhead door per REQ-4202-10)

---

## What to Fix for a Cleaner Rerun

1. **Add rate table entries for exit lights and weatherproof switches** to eliminate the 2 lines with `location TBD` SourceRef. This would bring provenance completeness to 100%.
2. **Confirm concrete apron dimensions** when site design (DEL-03-01) and building layout (DEL-04-01) are available; currently assumed at 50 m2 each per ASM-04.
3. **Confirm overhead door hardware scope overlap** with EQ-02 included items; current assumption (ASM-03) adds a hardware set per door beyond the EQ-02 supply price.
