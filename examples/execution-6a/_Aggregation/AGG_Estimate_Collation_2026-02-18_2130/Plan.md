# Aggregation Plan

## What Was Done

This aggregation run is an **incremental update** to the prior snapshot `AGG_Estimate_Collation_2026-02-18_1300`. It incorporates 4 updated deliverable estimate snapshots that resolved all 12 previously-TBD line items.

### Steps Performed

1. **Read prior snapshot.** Loaded `AGG_Estimate_Collation_2026-02-18_1300/Aggregated/Estimate/Project_Detail.csv` (266 rows, 12 TBDs, $6,633,217 base).

2. **Read 4 new estimate snapshots.** Read updated Detail.csv, Assumptions_Log.md, and Run_Context.md from:
   - `EST_DEL-01-02_2026-02-18_2100/` (3 lines, $17,400)
   - `EST_DEL-01-03_2026-02-18_2100/` (4 lines, $15,240)
   - `EST_DEL-01-06_2026-02-18_2100/` (4 lines, $263,700)
   - `EST_DEL-02-01_2026-02-18_2100/` (10 lines, $168,329)

3. **Merge.** Replaced 21 old rows (for the 4 deliverables) with 21 new rows. Row count preserved at 266. All 12 TBD rows replaced with priced rows.

4. **Recompute summaries.** Generated:
   - `Project_Summary_WBS.csv` -- updated package and deliverable totals
   - `Project_Summary_CBS.csv` -- updated CBS totals (several CBS codes now priced that were previously $0)
   - `Project_WBS_CBS_Matrix.csv` -- updated cross-tabulation

5. **Update assumptions.** Replaced assumptions for the 4 deliverables with new assumptions from updated snapshots.

6. **Update basis of estimate.** Updated BasisOfEstimate_Index.csv and BasisOfEstimate_Collection.md to reflect the new snapshot references and method changes (some lines changed from RATE_TABLE/TBD to ALLOWANCE).

7. **Update source index.** Updated Source_Index.csv to reference the 4 new snapshot folders.

8. **Update coverage.** Updated Coverage.csv to reference the 4 new snapshot paths.

9. **Publication.** Wrote snapshot folder `AGG_Estimate_Collation_2026-02-18_2130/` with all required artifacts. Updated `_LATEST.md` pointer.

### Key Observations

- All 12 TBD line items are now resolved. TBD count = 0.
- The 12 resolved items added $192,629 to the project base price.
- Base price increased from $6,633,217 to $6,825,846 (+$192,629, +2.9%).
- 5 of the 12 resolved lines used ALLOWANCE method (parametric allowances for items without rate table evidence).
- 7 of the 12 resolved lines used RATE_TABLE method (new Interior_Architectural_Rates.csv pricing source PS-27).
- Total priced line count remains 266. All rows now have numeric amounts.
