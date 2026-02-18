# Source Index

**RunID:** EST_DEL-01-04_2026-02-18_1400

## Indexed Price Sources

| # | File | Source Type | Parsing Notes | Supports | Limitations |
|---|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate table | 30 roles; CSV with RoleID, Role, HourlyRate_CAD | Hourly rates for all staff roles (R-01 through R-30). Used for RATE_TABLE method pricing. | Rates are MARKET basis / MEDIUM confidence. Does not include productivity factors or overhead multipliers. |
| 2 | Level_of_Effort.csv | Level of effort (hours by deliverable) | 18 rows for Execution 6a; CSV with DeliverableID, RoleID, EstimatedHours | Hours allocation per deliverable per role. DEL-01-04 has 2 rows: R-02 (40h), R-24 (12h). | Hours are PARAMETRIC basis; represent a single point estimate, not a range. |
| 3 | Assumed_Project_Parameters.csv | Project parameters | 29 rows; CSV with ParameterID, Value, Unit | PP-24 (estimated total construction value = $8,700,000) used as denominator for building permit percentage. | PP-24 is PARAMETRIC / LOW confidence. Changes to construction value directly affect building permit fee calculation. |
| 4 | Fees_Permits_Insurance.csv | Fee/permit/insurance schedule | 19 rows; CSV with ItemID, Category, RecommendedRate | Permit fees FP-06 through FP-10 used for this estimate. FP-06 is percentage-based; FP-07 through FP-10 are lump sums. | Confidence ranges from LOW to MEDIUM. Penhold-specific fee schedules are TBD. FP-11 through FP-19 (utility connections, environmental, legal) are not in scope for DEL-01-04. |

## Decomposition Source

| File | Usage |
|---|---|
| Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md | Package/deliverable IDs, scope item mapping (SOW-0009), objective mapping (OBJ-005, OBJ-008). Read-only. |

## Dependency Source

| File | Usage |
|---|---|
| DEL-01-04/Dependencies.csv | 11 dependency rows read (DEP-01-04-001 through DEP-01-04-010 + header). Used for blocker/readiness analysis. No pricing evidence extracted from dependencies. |
