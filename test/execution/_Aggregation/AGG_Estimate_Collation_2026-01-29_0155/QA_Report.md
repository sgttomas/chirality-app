# QA Report

## Schema Checks
- Detail.csv required columns present for all packages processed in this snapshot.
- Project_Detail.csv includes Qty, Unit, and UnitRate for all included rows.

## Data Quality Checks
- Duplicate LineUIDs: 27 (caused by WBS_DeliverableID = N/A across packages); logged in Aggregated/Duplicates.csv.
- Missing artifacts: PKG-09 Risk_Register.md not found; logged in Coverage.csv.

## Coverage
- Coverage.csv populated for all packages with per-deliverable rows.
- BOE_Index.csv includes all packages with BOE.md extracts.

## Overall Assessment
- RUN_STATUS: WARNINGS (missing risk register + duplicate LineUIDs)
- Data is suitable for aggregation with noted gaps.
