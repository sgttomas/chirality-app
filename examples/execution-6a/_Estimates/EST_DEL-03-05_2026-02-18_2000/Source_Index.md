# Source Index

## Run: EST_DEL-03-05_2026-02-18_2000

### Price Sources Used for DEL-03-05

| # | Source File | Source Type | Items Used | Parsing Notes | Supports |
|---|---|---|---|---|---|
| 1 | Fees_Permits_Insurance.csv | Rate table + Allowance | FP-16, FP-17, FP-18 | 19 rows total; CSV parseable; ItemID/Category/Description/Unit/RateMin/RateMax/RecommendedRate/Basis/Confidence/Notes schema | Environmental consultant fees (FP-17), AEPA Water Act application fee (FP-16), ESC plan preparation (FP-18) |
| 2 | Professional_Design_Fees.csv | Rate table (percentage-based) | DF-07 | 8 rows total; CSV parseable; cross-references FP-17 for environmental consulting | Environmental consulting lump sum reference |
| 3 | Assumed_Project_Parameters.csv | Parameter table | PP-09, PP-10 | 29 rows total; CSV parseable; used for site area context only | Context: total parcel 12 acres, developed area 4.5 acres |

### Price Sources NOT Used (per cost ownership rules)

| # | Source File | Reason Not Used |
|---|---|---|
| 4 | Earthwork_Civil_Rates.csv | Earthwork costs belong to DEL-03-02 per cost ownership rules. No line items for DEL-03-05. |
| 5 | Paving_Surfacing_Rates.csv | Paving costs belong to DEL-03-03 per cost ownership rules. No line items for DEL-03-05. |
| 6 | Underground_Utility_Rates.csv | Utility costs belong to DEL-03-04 per cost ownership rules. No line items for DEL-03-05. |
| 7 | Construction_Labour_Rates.csv | Physical construction labour belongs to executing deliverables per cost ownership rules. No line items for DEL-03-05. |

### Non-Price Sources (Dependency Evidence)

| # | Source | Type | Used For |
|---|---|---|---|
| 8 | Dependencies.csv (DEL-03-05 folder) | Dependency register (v3.1) | Blocker identification; 19 rows; 5 ANCHOR + 14 EXECUTION edges |
| 9 | _DEPENDENCIES.md (DEL-03-05 folder) | Dependency summary | Run notes and validation context |
| 10 | Datasheet.md (DEL-03-05 folder) | Deliverable datasheet | Scope, attributes, wetland replacement fee ($10,769.54), and conditions |

### Key Evidence Cross-References

| LineID in Detail.csv | SourceRef | Evidence Description |
|---|---|---|
| L-01 | Fees_Permits_Insurance.csv row FP-17 | Environmental consultant fees: $15,000-$30,000; Recommended $22,000 |
| L-02 | Fees_Permits_Insurance.csv row FP-16 | AEPA Water Act application fee: $3,000-$8,000; Recommended $5,000 |
| L-03 | Datasheet.md > Wetland/Waterbody Characteristics > ABWRET-A | Wetland replacement fee: $10,769.54 (from Wetland Assessment Executive Summary) |
| L-04 | Fees_Permits_Insurance.csv row FP-18 | Erosion and sediment control plan preparation: $3,000-$6,000; Recommended $4,500 |
| L-05 | Fees_Permits_Insurance.csv row FP-07 | Development permit (flood fringe approval component): $500-$2,000; Recommended $1,200 |
