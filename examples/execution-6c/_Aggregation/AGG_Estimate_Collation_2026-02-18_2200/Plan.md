# Aggregation Plan

## What Was Done

1. **Bootstrap** -- Created aggregation snapshot folder `AGG_Estimate_Collation_2026-02-18_2200` with required directory structure.

2. **Locate Estimate Artifacts** -- Located all 21 estimate snapshots from `_Estimates/` (2026-02-18 run series). Each snapshot contains a valid `Detail.csv`, `Run_Context.md`, `Assumptions_Log.md`, `Summary.md`, and `QA_Report.md`.

3. **Validate Format and Provenance** -- Verified all 21 Detail.csv files contain the canonical columns (`LineID`, `CBS`, `WBS_PackageID`, `WBS_DeliverableID`, `Description`, `Qty`, `Unit`, `UnitRate`, `Amount`, `Currency`, `Method`, `SourceRef`, `Confidence`, `Notes`). All passed schema validation.

4. **Collate Into Project-Level Artifacts**:
   - Combined all line items into `Project_Detail.csv` with `LineUID = {DeliverableID}::{LineID}` namespacing
   - Collected assumptions from all 21 Assumptions_Log files into `Project_Assumptions.csv`
   - Collected risks into `Project_Risks.csv`
   - Captured basis-of-estimate data from Run_Context files into `BasisOfEstimate_Index.csv` and `BasisOfEstimate_Collection.md`
   - Applied double-counting guards per brief:
     - DEL-01-03 bond/insurance premiums ($537,534) excluded from additive production totals
     - DEL-05-01 and DEL-05-02 construction content ($10,729,000) counted ONCE
   - Produced rollup summaries by WBS, CBS, and WBS x CBS matrix
   - Produced effort matrix (hours by role x package)
   - Produced evaluation-weight-adjusted view per BOE Section 7.4

5. **Publish** -- Wrote all required snapshot artifacts.

## Key Decisions

- DEL-05-02 construction content lines L-095 and L-096 are GR transparency rows (not additive); excluded from construction total per the estimate's own notes.
- DEL-01-03 bond/insurance premiums are reported separately; only production cost ($2,060) and broker fee ($3,500) counted as PKG-01 additive cost.
- Construction pricing content reported from DEL-05-01 summary lines (not DEL-05-02 detail lines, which provide the same $10,729,000 at greater granularity). DEL-05-02 detail preserved in Project_Detail.csv for audit.
- DEL-05-02 L-078 environmental compliance adjusted per estimate notes: $9,500 regulatory fees (not $74,000 which includes consultant fees that overlap with L-106). The Detail.csv as written carries $74,000; this aggregation accepts the value as written in the source Detail.csv and flags the overlap in QA.
