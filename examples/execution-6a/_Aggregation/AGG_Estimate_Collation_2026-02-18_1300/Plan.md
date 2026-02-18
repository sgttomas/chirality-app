# Aggregation Plan

## What Was Done

This aggregation run collated 30 deliverable-level estimate snapshots into a project-level estimate package for the Penhold Public Services Building (PSB) project.

### Steps Performed

1. **Bootstrap.** Created the aggregation tool root at `{EXECUTION_ROOT}/_Aggregation/` with required subdirectories (`_Archive/`, `_Templates/`, `_Pipelines/PENHOLD_PSB_6a/`).

2. **Brief interpretation.** Read the INIT-TASK brief specifying 30 deliverables across PKG-001 through PKG-005, with DEL-06-01 excluded (no cost content).

3. **Artifact location.** Located 30 estimate snapshots under `{EXECUTION_ROOT}/_Estimates/`, one per deliverable. Each snapshot named `EST_{DEL-ID}_{DATE}_{TIME}/`. All 30 snapshots contain valid Detail.csv files.

4. **Schema validation.** Validated each Detail.csv against the canonical schema (14 required columns). All 30 files passed schema validation with full column coverage.

5. **Basis-of-estimate capture.** Extracted `BASIS_OF_ESTIMATE`, `FALLBACK_POLICY`, `ALLOW_MIXED_METHODS`, and `RUN_STATUS` from each snapshot's Run_Context.md and QA_Report.md.

6. **Detail collation.** Merged all 266 line items from 30 Detail.csv files into `Project_Detail.csv`, assigning `LineUID = {FromDeliverableID}::{LineID}` for each row. Preserved all provenance fields (`SourceRef`, `Confidence`, `Method`).

7. **Assumptions and risks collation.** Parsed 57 assumptions from Assumptions_Log.md files and 40 risks from Risk_Register.md files across all snapshots. Assigned UIDs (`{FromDeliverableID}::{ASM-ID}` and `{FromDeliverableID}::{RSK-ID}`).

8. **Aggregation.** Produced:
   - WBS rollups (package subtotals and deliverable totals)
   - CBS rollups (cost breakdown structure totals)
   - Combined WBS/CBS matrix
   - Coverage report (all 30 deliverables covered, schema valid)
   - Conflict and duplicate reports

9. **Cross-check.** Verified computed totals against the brief's known deliverable totals. All 30 deliverable totals match exactly. One noted item: DEL-05-05 carries two mutually exclusive scenarios ($12,000 non-illuminated primary, $22,000 illuminated alternate); the primary scenario is used in project totals.

10. **Publication.** Wrote snapshot folder `AGG_Estimate_Collation_2026-02-18_1300/` with all required artifacts. Updated `_LATEST.md` pointer and pipeline pointer.

### Key Decisions

- DEL-05-05 has two mutually exclusive line items. Primary scenario ($12,000 non-illuminated) used in project totals. Both rows preserved in Project_Detail.csv for audit. See Decision_Log.md DEC-AGG-001.
- 12 TBD line items (across DEL-01-02, DEL-01-03, DEL-01-06, DEL-02-01) excluded from totals because pricing evidence was unavailable. These are surfaced in QA_Report.md.
- Cash allowances (DEL-03-04 utility tie-in $35,000, DEL-05-07 FF&E $20,000) are separately identified in the project summary per the brief's Section 7.2 requirements.
