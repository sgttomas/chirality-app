# QA Report -- AGG_Estimate_Collation_2026-02-18_1300

## RUN_STATUS: WARNINGS

Totals are meaningful. All 30 deliverable snapshots collated successfully. 12 TBD line items remain unpriced. 22/30 source snapshots reported WARNINGS status. No FAILED_INPUTS.

---

## Snapshot Validity Checks

### V1 -- Write Quarantine Respected

**PASS.** All outputs written under `{EXECUTION_ROOT}/_Aggregation/AGG_Estimate_Collation_2026-02-18_1300/`. No source files modified. No files written outside `_Aggregation/`.

### V2 -- Snapshot Created

**PASS.** Snapshot folder `AGG_Estimate_Collation_2026-02-18_1300/` created under `{AGGREGATION_ROOT}/`.

### V3 -- Required Audit Artifacts Exist

| Artifact | Status |
|---|---|
| Brief.md | PRESENT |
| Plan.md | PRESENT |
| RUN_SUMMARY.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.csv | PRESENT |
| Decision_Log.md | PRESENT |
| Extracts/ | PRESENT (directory created) |
| Aggregated/Conflicts.csv | PRESENT |
| Aggregated/Duplicates.csv | PRESENT |

**PASS.**

### V4 -- Estimate Collation Artifacts Exist

| Artifact | Status |
|---|---|
| Aggregated/Estimate/Project_Detail.csv | PRESENT (266 rows) |
| Aggregated/Estimate/Project_Assumptions.csv | PRESENT (57 rows) |
| Aggregated/Estimate/Project_Risks.csv | PRESENT (40 rows) |
| Aggregated/Estimate/BasisOfEstimate_Index.csv | PRESENT (30 rows) |
| Aggregated/Estimate/BasisOfEstimate_Collection.md | PRESENT |
| Aggregated/Estimate/Project_Summary_CBS.csv | PRESENT |
| Aggregated/Estimate/Project_Summary_WBS.csv | PRESENT |
| Aggregated/Estimate/Project_WBS_CBS_Matrix.csv | PRESENT |
| Aggregated/Estimate/Coverage.csv | PRESENT (30 rows) |

**PASS.** All required estimate collation files present.

### V5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| Project_Detail.csv parseable | PASS |
| All required columns present | PASS (18 columns including LineUID, FromDeliverableID, FromPackageID, and SourceSnapshot) |
| Qty/Unit/UnitRate present for priced rows | PASS for 254/266 rows (12 TBD rows have TBD values as expected) |
| LineUID uniqueness | PASS (266 unique LineUIDs) |

**PASS.**

---

## Coverage Analysis

### Scope Coverage

| Metric | Value |
|---|---|
| Deliverables in brief scope | 30 |
| Deliverables with Detail.csv found | 30 |
| Deliverables with valid schema | 30 |
| Deliverables excluded (DEL-06-01) | 1 (no cost content; per brief) |
| **Coverage rate** | **100%** |

### Artifact Coverage (per deliverable)

| Artifact | Present In | Missing From |
|---|---|---|
| Detail.csv | 30/30 | 0 |
| Run_Context.md | 30/30 | 0 |
| QA_Report.md | 30/30 | 0 |
| Summary.md | 30/30 | 0 |
| Assumptions_Log.md | 30/30 | 0 |
| WBS_CBS_Matrix.csv | 30/30 | 0 |
| Source_Index.md | 30/30 | 0 |
| Decision_Log.md | 30/30 | 0 |
| Risk_Register.md | 16/30 | 14 |
| Blockers.md | 30/30 | 0 |

### RUN_STATUS Distribution (source snapshots)

| RUN_STATUS | Count | Deliverables |
|---|---|---|
| OK | 8 | DEL-01-01, DEL-01-07, DEL-02-05, DEL-02-06, DEL-04-01, DEL-04-02, DEL-04-04, DEL-05-07 |
| WARNINGS | 22 | All others |
| FAILED_INPUTS | 0 | -- |

---

## Provenance Analysis

### Method Distribution (266 total lines)

| Method | Count | % of Priced Lines | Amount (CAD) | % of Total |
|---|---|---|---|---|
| RATE_TABLE | 213 | 83.9% | $6,095,567 | 86.8% |
| ALLOWANCE | 31 | 12.2% | $620,650 | 8.8% |
| PARAMETRIC | 4 | 1.6% | $292,400 | 4.2% |
| QUOTE | 6 | 2.4% | $18,600 | 0.3% |
| TBD (unpriced) | 12 | N/A | N/A | N/A |

Note: Amounts exclude 12 TBD lines. Percentages of priced lines based on 254 priced rows. Total priced amount ($7,027,217) includes both DEL-05-05 scenarios; using primary only adjusts total by -$22,000.

### SourceRef Completeness

| Metric | Value |
|---|---|
| Priced rows with non-TBD SourceRef | 254/254 (100.0%) |
| Priced rows with "location TBD" SourceRef | 0 |
| TBD rows (unpriced; SourceRef = "location TBD") | 12 |

**Provenance completeness: 100%** for all priced lines. The 12 unpriced (TBD) lines have `location TBD` SourceRef because pricing evidence was unavailable.

**Top unpriced-line locations (cost drivers without pricing evidence):**
1. DEL-02-01 -- 7 TBD lines (partitions, finishes, ceiling, accessibility, signage, design fees, paint)
2. DEL-01-06 -- 2 TBD lines (temporary facilities, site cleaning)
3. DEL-01-03 -- 2 TBD lines (training costs, PPE/signage supplies)
4. DEL-01-02 -- 1 TBD line (scheduling software/tools)

### Confidence Distribution (254 priced lines)

| Confidence | Count | Amount (CAD) |
|---|---|---|
| HIGH | 2 | $30,770 |
| MED / MEDIUM | 209 | $5,925,527 |
| LOW | 43 | $1,070,920 |

---

## Conflict and Duplicate Analysis

### Conflicts

| ConflictID | Description | Resolution |
|---|---|---|
| CON-001 | DEL-05-05 carries two mutually exclusive signage scenarios ($12k vs $22k) | Both kept in detail; primary ($12k non-illuminated) used in project totals |

### Duplicates

No duplicates detected. All 266 LineUIDs are unique across the 30 deliverable snapshots.

---

## Cross-Check Verification

All 30 individual deliverable totals match the brief's cross-check values:

| Deliverable | Brief Expected | Computed | Match |
|---|---|---|---|
| DEL-01-01 | $44,800 | $44,800 | PASS |
| DEL-01-02 | $13,900 | $13,900 | PASS |
| DEL-01-03 | $7,240 | $7,240 | PASS |
| DEL-01-04 | $79,910 | $79,910 | PASS |
| DEL-01-05 | $19,750 | $19,750 | PASS |
| DEL-01-06 | $203,700 | $203,700 | PASS |
| DEL-01-07 | $23,650 | $23,650 | PASS |
| DEL-02-01 | $47,200 | $47,200 | PASS |
| DEL-02-02 | $279,279 | $279,279 | PASS |
| DEL-02-03 | $212,396 | $212,396 | PASS |
| DEL-02-04 | $1,721,269 | $1,721,269 | PASS |
| DEL-02-05 | $1,014,095 | $1,014,095 | PASS |
| DEL-02-06 | $642,936 | $642,936 | PASS |
| DEL-02-07 | $201,000 | $201,000 | PASS |
| DEL-03-01 | $18,500 | $18,500 | PASS |
| DEL-03-02 | $472,062 | $472,062 | PASS |
| DEL-03-03 | $896,380 | $896,380 | PASS |
| DEL-03-04 | $226,930 | $226,930 | PASS |
| DEL-03-05 | $43,470 | $43,470 | PASS |
| DEL-04-01 | $202,000 | $202,000 | PASS |
| DEL-04-02 | $51,812 | $51,812 | PASS |
| DEL-04-03 | $156,938 | $156,938 | PASS |
| DEL-04-04 | $54,000 | $54,000 | PASS |
| DEL-05-01 | $123,000 | $123,000 | PASS |
| DEL-05-02 | $98,000 | $98,000 | PASS |
| DEL-05-03 | $45,000 | $45,000 | PASS |
| DEL-05-04 | $55,400 | $55,400 | PASS |
| DEL-05-05 | $12,000 | $12,000 (primary) | PASS |
| DEL-05-06 | $18,600 | $18,600 | PASS |
| DEL-05-07 | $20,000 | $20,000 | PASS |

Package totals:
| Package | Brief Expected | Computed | Match |
|---|---|---|---|
| PKG-001 | $392,950 | $392,950 | PASS |
| PKG-003 | $1,657,342 | $1,657,342 | PASS |
| PKG-004 | $464,750 | $464,750 | PASS |
| PKG-005 (primary scenarios) | $372,000 | $372,000 | PASS |

---

## What to Fix for Improved Totals

1. **Expand rate tables** to cover the 12 TBD line items, particularly:
   - Interior architectural rates for partitions, ceiling systems, finishes, paint (DEL-02-01)
   - Temporary facility/fencing rates (DEL-01-06)
   - PPE supply and training costs (DEL-01-03)
   - Scheduling software costs (DEL-01-02)

2. **Obtain vendor quotes** for PKG-005 optional items currently at ALLOWANCE/PARAMETRIC confidence.

3. **Resolve DEL-05-05 illumination decision** to collapse the two-scenario structure.

4. **Obtain Town branding guidelines** to finalize DEL-05-05 signage design and pricing.

5. **Rerun DEL-02-01** once interior finish rates are available -- this is the most materially incomplete deliverable in the base scope.
