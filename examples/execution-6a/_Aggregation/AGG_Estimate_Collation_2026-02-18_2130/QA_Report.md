# QA Report -- AGG_Estimate_Collation_2026-02-18_2130

## RUN_STATUS: WARNINGS

All 30 deliverable snapshots collated successfully. 0 TBD line items remain (down from 12 in prior snapshot). ALLOWANCE and PARAMETRIC-grade pricing remains across multiple deliverables.

---

## Snapshot Validity Checks

### V1 -- Write Quarantine Respected

**PASS.** All outputs written under `{EXECUTION_ROOT}/_Aggregation/AGG_Estimate_Collation_2026-02-18_2130/`. No source files modified. No files written outside `_Aggregation/`. Prior snapshot `AGG_Estimate_Collation_2026-02-18_1300/` is unmodified.

### V2 -- Snapshot Created

**PASS.** Snapshot folder `AGG_Estimate_Collation_2026-02-18_2130/` created under `{AGGREGATION_ROOT}/`.

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
| Aggregated/Estimate/Project_Assumptions.csv | PRESENT |
| Aggregated/Estimate/Project_Risks.csv | PRESENT |
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
| Qty/Unit/UnitRate present for all rows | PASS for 266/266 rows (0 TBD rows; all priced) |
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

### Method Distribution (266 total lines; all priced)

| Method | Count | % of Lines | Amount (CAD) | % of Total |
|---|---|---|---|---|
| RATE_TABLE | 220 | 82.7% | $6,216,696 | 86.1% |
| ALLOWANCE | 36 | 13.5% | $692,150 | 9.6% |
| PARAMETRIC | 4 | 1.5% | $292,400 | 4.1% |
| QUOTE | 6 | 2.3% | $18,600 | 0.3% |
| TBD (unpriced) | 0 | 0% | N/A | N/A |

Note: Total priced amount ($7,219,846) includes both DEL-05-05 scenarios; using primary only adjusts total by -$22,000.

### SourceRef Completeness

| Metric | Value |
|---|---|
| Priced rows with non-TBD SourceRef | 266/266 (100.0%) |
| Priced rows with "location TBD" SourceRef | 0 |
| TBD rows (unpriced) | 0 |

**Provenance completeness: 100%** for all 266 lines.

### Confidence Distribution (266 priced lines)

| Confidence | Count | Amount (CAD) |
|---|---|---|
| HIGH | 2 | $30,770 |
| MED / MEDIUM | 216 | $6,118,156 |
| LOW | 48 | $1,070,920 |

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

Updated deliverable totals verified against source snapshots:

| Deliverable | Source Snapshot Total | Computed | Match |
|---|---|---|---|
| DEL-01-02 | $17,400 | $17,400 | PASS |
| DEL-01-03 | $15,240 | $15,240 | PASS |
| DEL-01-06 | $263,700 | $263,700 | PASS |
| DEL-02-01 | $168,329 | $168,329 | PASS |

All other 26 deliverable totals unchanged and verified from prior snapshot.

Package totals:

| Package | Expected | Computed | Match |
|---|---|---|---|
| PKG-001 | $464,450 | $464,450 | PASS |
| PKG-002 | $4,239,304 | $4,239,304 | PASS |
| PKG-003 | $1,657,342 | $1,657,342 | PASS |
| PKG-004 | $464,750 | $464,750 | PASS |
| PKG-005 (primary scenarios) | $372,000 | $372,000 | PASS |

---

## What to Improve

1. **Obtain vendor quotes** for PKG-005 optional items currently at ALLOWANCE/PARAMETRIC confidence.

2. **Resolve DEL-05-05 illumination decision** to collapse the two-scenario structure.

3. **Obtain Town branding guidelines** to finalize DEL-05-05 signage design and pricing.

4. **Validate ALLOWANCE-grade items** (5 newly resolved lines in DEL-01-02, DEL-01-03, DEL-01-06) against actual market pricing or competitive quotes when available.

5. **Validate DEL-02-01 new pricing** based on Interior_Architectural_Rates.csv against actual design development quantities once floor plan is finalized.
