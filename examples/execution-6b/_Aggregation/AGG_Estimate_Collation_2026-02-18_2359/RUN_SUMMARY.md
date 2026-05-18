# RUN SUMMARY — AGG_Estimate_Collation_2026-02-18_2359

| Field | Value |
|-------|-------|
| **RUN_STATUS** | WARNINGS |
| **SnapshotID** | AGG_Estimate_Collation_2026-02-18_2359 |
| **PURPOSE** | Estimate_Collation |
| **PIPELINE_ID** | Proposal_Production_Estimate |
| **Scope** | 38 deliverables across 10 packages (DEL-01-01 through DEL-10-02) |
| **Source Snapshots** | 40 estimate snapshot directories under _Estimates/ |
| **Currency** | CAD |
| **Base Year** | 2024 |

## Key Results

### Project-Level Totals

| Category | Amount (CAD) | Hours |
|----------|-------------|-------|
| **Total Proposal Production Cost** | $111,000 | 786 |
| **Financial Allowances (bond/insurance premiums)** | $543,500 | -- |
| **Grand Total Proposal Effort** | $654,500 | 786 |
| **Construction Pricing Content (separately reported)** | $7,710,000 | -- |

### Package Production Costs

| Package | Production Cost (CAD) | Hours |
|---------|----------------------|-------|
| PKG-001 Compliance/Commercial/Team | $30,480 | 226 |
| PKG-002 Conceptual Design | $33,580 | 260 |
| PKG-003 Design Brief | $9,150 | 60 |
| PKG-004 Sustainability/Energy | $5,400 | 34 |
| PKG-005 Durability/Maintenance | $5,210 | 34 |
| PKG-006 Delivery Plan | $4,700 | 28 |
| PKG-007 Construction Methodology | $7,990 | 50 |
| PKG-008 Commissioning/Closeout | $4,550 | 30 |
| PKG-009 Schedule | $4,620 | 32 |
| PKG-010 Due Diligence | $5,320 | 32 |
| **TOTAL** | **$111,000** | **786** |

### Top Roles by Hours

| Role | Hours | Cost (CAD) |
|------|-------|------------|
| Project Manager | 118 | $20,650 |
| Architect (all levels) | 110 | $15,590 |
| CAD Technician | 76 | $7,220 |
| Estimator (Senior) | 72 | $10,440 |
| Proposal Coordinator | 48 | $5,040 |
| Mechanical Engineer (all levels) | 52 | $8,080 |
| Electrical Engineer (all levels) | 50 | $7,510 |
| Civil Engineer (all levels) | 56 | $8,200 |
| Structural Engineer (all levels) | 42 | $6,270 |
| Estimator (Intermediate) | 40 | $4,600 |

## Warnings

1. **RUN_STATUS = WARNINGS** (not FAILED_INPUTS) because all 38 Detail.csv files are present and valid, but:
   - No Risk_Register files found in any snapshot (0/38 coverage)
   - Bond premium calculation inconsistency between DEL-01-03 and DEL-01-04/05 (see Conflicts.csv)
   - DEL-01-04/05 construction pricing is intentionally duplicated (Schedule A/B dual views)

2. **Construction pricing ($7,710,000) is not a production cost.** It is the content of the pricing forms (what goes INTO the proposal), not the cost to produce the proposal. The production cost to compile Schedule A/B is $16,000 (DEL-01-04 $9,960 + DEL-01-05 $6,020).

3. **Financial allowances ($543,500) are percentage-based estimates** on an assumed $12M contract value (LOW confidence). These will change when actual Schedule A pricing is finalized.

## Artifacts Produced

- Brief.md, Plan.md, RUN_SUMMARY.md, QA_Report.md, Source_Index.csv, Decision_Log.md
- Extracts/ (empty -- raw data preserved in source snapshots)
- Aggregated/Conflicts.csv (2 conflicts)
- Aggregated/Duplicates.csv (41 intentional duplicate pairs)
- Aggregated/Estimate/Project_Detail.csv (consolidated detail with LineUID)
- Aggregated/Estimate/Project_Assumptions.csv
- Aggregated/Estimate/Project_Risks.csv
- Aggregated/Estimate/BasisOfEstimate_Index.csv
- Aggregated/Estimate/BasisOfEstimate_Collection.md
- Aggregated/Estimate/Project_Summary_CBS.csv
- Aggregated/Estimate/Project_Summary_WBS.csv
- Aggregated/Estimate/Project_WBS_CBS_Matrix.csv
- Aggregated/Estimate/Coverage.csv
- Aggregated/Estimate/Effort_Matrix.csv
- Aggregated/Estimate/Evaluation_Weight_View.csv
