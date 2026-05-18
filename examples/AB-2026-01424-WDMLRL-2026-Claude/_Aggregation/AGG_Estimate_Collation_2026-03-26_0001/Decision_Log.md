# Decision Log

**Snapshot:** AGG_Estimate_Collation_2026-03-26_0001

| # | Decision | Rationale |
|---|---|---|
| DEC-001 | Use latest snapshot per deliverable (by date/time in folder name) | Protocol requires most recent estimate; 4 deliverables have SCA-001 re-estimates superseding originals |
| DEC-002 | Exclude ItemID column when absent from newer Detail.csv schemas | SCA-001 re-estimate Detail.csv files omit ItemID; column included but left blank for those rows |
| DEC-003 | CBS normalization: map CBS-XX codes to L1/L2 hierarchy using project CBS taxonomy | Enables CBS rollup summaries; older snapshots with descriptive CBS text mapped to closest L1/L2 category |
| DEC-004 | Risks extracted from QA_Report.md when no Risk_Register.md present | Most snapshots store risk observations in QA report risk sections; this preserves provenance |
| DEC-005 | Prior pipeline results incorporated by full re-scan of all deliverable snapshots (not incremental merge) | Ensures consistency; all 107 deliverables re-collated with latest snapshots selected |
