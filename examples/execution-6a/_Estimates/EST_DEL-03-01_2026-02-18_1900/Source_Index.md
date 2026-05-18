# Source Index — EST_DEL-03-01_2026-02-18_1900

## Price Sources

| SourceID | File | Type | Relevant Items for DEL-03-01 | Parsing Notes |
|---|---|---|---|---|
| SRC-01 | _PriceSources/Earthwork_Civil_Rates.csv | Rate table (PARAMETRIC basis) | EC-11 (Construction survey and staking, $12,000 LS) | 11 items; CSV parseable. Items EC-01 through EC-10 relate to earthworks/grading/drainage — these belong to DEL-03-02, not DEL-03-01 per cost ownership rules. EC-11 (survey/staking) is relevant to DEL-03-01 for initial layout work. |
| SRC-02 | _PriceSources/Paving_Surfacing_Rates.csv | Rate table (PARAMETRIC basis) | None directly — pavement construction belongs to DEL-03-03 | 9 items; CSV parseable. All items (PS-01 through PS-09) are construction costs belonging to DEL-03-03 per cost ownership rules. |
| SRC-03 | _PriceSources/Underground_Utility_Rates.csv | Rate table (PARAMETRIC/ALLOWANCE basis) | None directly — utility distribution belongs to DEL-03-04 | 12 items; CSV parseable. All items belong to DEL-03-04 per cost ownership rules. |
| SRC-04 | _PriceSources/Fees_Permits_Insurance.csv | Rate table (MARKET/PARAMETRIC/ALLOWANCE basis) | None directly — fees/permits are project-wide (PKG-001) or per-discipline | 19 items; CSV parseable. No items specifically attributable to DEL-03-01 design scope. Building permit (FP-06) applies to overall project, not individual deliverables. |
| SRC-05 | _PriceSources/Professional_Design_Fees.csv | Rate table (MARKET basis) | DF-02 (Civil engineering design fees, 2.5% of site/civil construction cost) | 8 items; CSV parseable. DF-02 is the primary design fee source for civil engineering. Fee is expressed as percentage of construction cost — requires a construction cost base estimate. |
| SRC-06 | _PriceSources/Construction_Labour_Rates.csv | Rate table (MARKET basis) | T-15 (Surveyor/Instrument Person, $69/hr fully burdened) | 15 items; CSV parseable. T-15 supports survey labour costing if hourly approach is used. Other trades not relevant to DEL-03-01 (design deliverable). |
| SRC-07 | _PriceSources/Assumed_Project_Parameters.csv | Parameters (various basis) | PP-23 ($1,800,000 CAD site/civil construction value — PARAMETRIC, LOW confidence) | 29 items; CSV parseable. PP-23 provides the construction cost base for DF-02 percentage fee calculation. PP-10 (4.5 acres developed) and PP-19 (40 parking stalls) provide quantity context. |

## Decomposition Source

| Source | Path | Notes |
|---|---|---|
| Decomposition | _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md | v1.0 (Phase 7: Published). DEL-03-01 confirmed in PKG-003. Scope items: SOW-0100 through SOW-0104. Objectives: OBJ-005, OBJ-007. |

## Dependency Source

| Source | Path | Notes |
|---|---|---|
| Dependencies.csv | PKG-003_Site & Civil Works/1_Working/DEL-03-01_Site Plan, Circulation, Parking & Operational Layout/Dependencies.csv | v3.1 schema; 21 dependency rows. Used for blocker identification only — not for pricing. |
