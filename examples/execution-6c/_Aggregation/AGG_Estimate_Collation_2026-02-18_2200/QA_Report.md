# QA Report

**Snapshot:** AGG_Estimate_Collation_2026-02-18_2200
**Date:** 2026-02-18
**RUN_STATUS: WARNINGS**

---

## 1. Snapshot Validity

| Check | Status | Notes |
|---|---|---|
| Written under AGGREGATION_ROOT | PASS | All files under `_Aggregation/AGG_Estimate_Collation_2026-02-18_2200/` |
| No source files modified | PASS | Read-only access to `_Estimates/` and `_PriceSources/` |
| Required audit artifacts exist | PASS | Brief.md, Plan.md, RUN_SUMMARY.md, QA_Report.md, Source_Index.csv, Decision_Log.md |
| Estimate collation artifacts exist | PASS | All 10 required files under `Aggregated/Estimate/` |
| Extracts/ directory exists | PASS | Created (empty -- raw extracts not needed; source snapshots are available) |
| Conflicts.csv exists | PASS | 3 conflicts documented |
| Duplicates.csv exists | PASS | 2 duplicates documented |

## 2. Coverage

| Metric | Value | Status |
|---|---|---|
| Deliverables in scope | 21 | -- |
| Deliverables with Detail.csv | 21 | PASS (100%) |
| Deliverables with valid schema | 21 | PASS (100%) |
| Deliverables with Run_Context.md | 21 | PASS (100%) |
| Deliverables with Assumptions_Log.md | 21 | PASS (100%) |
| Deliverables with Risk_Register.md | 1 | WARNING (5%) |
| Deliverables with QA_Report.md | 21 | PASS (100%) |
| Schema status: OK | 21 | -- |
| Schema status: INVALID | 0 | -- |
| Schema status: MISSING | 0 | -- |

## 3. Schema Validation

All 21 Detail.csv files contain the canonical columns:
- LineID: PRESENT in all
- CBS: PRESENT in all
- WBS_PackageID: PRESENT in all
- WBS_DeliverableID: PRESENT in all
- Description: PRESENT in all
- Qty: PRESENT in all (numeric, >0)
- Unit: PRESENT in all
- UnitRate: PRESENT in all (numeric, >0)
- Amount: PRESENT in all (numeric, >0; verified Qty x UnitRate = Amount for all lines)
- Currency: PRESENT in all (CAD)
- Method: PRESENT in all (valid enum values: RATE_TABLE, PARAMETRIC, ALLOWANCE)
- SourceRef: PRESENT in all (no `location TBD` entries)
- Confidence: PRESENT in all (valid values: HIGH, MEDIUM, MED, LOW)
- Notes: PRESENT in all

**Provenance completeness: 100%** -- All rows have non-TBD SourceRef values.

## 4. Basis Consistency

| Check | Status | Notes |
|---|---|---|
| All deliverables have BASIS_OF_ESTIMATE recorded | PASS | 21/21 via Run_Context.md |
| Primary basis is RATE_TABLE | PASS | 18/21 pure RATE_TABLE; 3/21 mixed (authorized per BOE) |
| Mixed methods only where ALLOW_MIXED_METHODS=TRUE | PASS | DEL-01-03, DEL-05-01, DEL-05-02 have ALLOW_MIXED=TRUE |
| FALLBACK_POLICY respected | PASS | Only DEL-01-03, DEL-05-01, DEL-05-02 use ALLOW_ALLOWANCE |

## 5. Double-Counting Validation

| Guard | Status | Notes |
|---|---|---|
| G-001: Bond/insurance premiums | APPLIED | DEL-01-03 premiums ($537,534) excluded from additive totals |
| G-002: Construction content counted once | APPLIED | $10,729,000 counted once despite appearing in both DEL-05-01 and DEL-05-02 |
| G-003: GR transparency rows | APPLIED | DEL-05-02 L-095/L-096 excluded |
| G-004: Environmental overlap | FLAGGED | DEL-05-02 L-078/L-106 potential $22k overlap within construction content |

## 6. Arithmetic Verification

### Production Cost Totals

| Package | Sum of Detail Lines | Reported Total | Variance | Status |
|---|---|---|---|---|
| PKG-01 | $840 + $2,170 + $2,060 + $3,500 = $8,570 | $8,570 | $0 | PASS |
| PKG-02 | $9,960 + $6,020 + $3,260 = $19,240 | $19,240 | $0 | PASS |
| PKG-03 | $2,380 + $1,860 + $1,720 = $5,960 | $5,960 | $0 | PASS |
| PKG-04 | $29,610 + $12,170 + $4,770 = $46,550 | $46,550 | $0 | PASS |
| PKG-05 | $2,350 + $2,350 = $4,700 | $4,700 | $0 | PASS |
| PKG-06 | $2,870 + $2,020 + $1,670 = $6,560 | $6,560 | $0 | PASS |
| PKG-07 | $3,290 | $3,290 | $0 | PASS |
| PKG-08 | $4,620 | $4,620 | $0 | PASS |
| PKG-09 | $3,410 + $2,950 = $6,360 | $6,360 | $0 | PASS |
| **PROJECT** | **$105,850** | **$105,850** | **$0** | **PASS** |

### Construction Content Total

| Source | Amount | Status |
|---|---|---|
| DEL-05-01 construction lines (L-010 through L-041) | $10,729,000 | -- |
| DEL-05-02 construction lines (L-010 through L-181) | $10,729,000 | -- |
| Schedule A / Schedule B reconciliation | $0 variance | PASS |
| **Reported construction content** | **$10,729,000** | **PASS** |

### Grand Total

| Component | Amount |
|---|---|
| Production | $105,850 |
| Construction Content | $10,729,000 |
| **Grand Total** | **$10,834,850** |

### Hours Verification

| Package | Sum of Qty (hr) Lines | Reported Hours | Variance | Status |
|---|---|---|---|---|
| PKG-01 | 8+14+4+4+4+2 = 36 | 36 | 0 | PASS |
| PKG-02 | 40+24+8+24+16+4+12+8 = 136 | 136 | 0 | PASS |
| PKG-03 | 16+4+12+8+8+4 = 52 | 52 | 0 | PASS |
| PKG-04 | 44+24+64+20+12+12+6+12+6+12+6+10+20+8+8+10+10+10+8+6+12+8+6+4 = 338 | 338 | 0 | PASS |
| PKG-05 | 10+4+10+4 = 28 | 28 | 0 | PASS |
| PKG-06 | 14+4+8+4+6+4 = 40 | 40 | 0 | PASS |
| PKG-07 | 16+6 = 22 | 22 | 0 | PASS |
| PKG-08 | 20+8+4 = 32 | 32 | 0 | PASS |
| PKG-09 | 10+8+4+8+6+4 = 40 | 40 | 0 | PASS |
| **TOTAL** | **724** | **724** | **0** | **PASS** |

## 7. Warnings Summary

| ID | Severity | Description |
|---|---|---|
| W-001 | MATERIAL | All construction pricing is PARAMETRIC/ALLOWANCE (no vendor quotes); +/-20-50% accuracy |
| W-002 | MATERIAL | Professional rates are market estimates, not actual firm rates; +/-20-30% accuracy |
| W-003 | MINOR | OI-004 (FF&E) implemented as recommended but formally OPEN |
| W-004 | MINOR | OI-001 (Intent to Propose) assumed not submitted |
| W-005 | MODERATE | Bond/insurance rates are market estimates; actual quotes needed |
| W-006 | MINOR | DEL-05-02 L-078/L-106 potential $22k overlap in construction content |
| W-007 | INFORMATIONAL | Risk_Register.md sparse (1 of 21 snapshots) |

## 8. RUN_STATUS Determination

**RUN_STATUS = WARNINGS**

Rationale:
- All 21 deliverables collated successfully with valid schema (OK for production totals)
- Provenance completeness is 100%
- Double-counting guards applied and verified
- However, material TBDs remain: construction pricing is parametric (no vendor quotes), professional rates are market estimates, OI-004 still formally open, bond/insurance rates are estimates
- These material warnings prevent an OK status but do not constitute FAILED_INPUTS
