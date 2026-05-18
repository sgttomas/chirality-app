# Decision Log — EST_DEL-007-04_2026-02-27_0700

## Decisions

| Decision ID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Use Level_of_Effort.csv hours multiplied by Professional_Staff_Rates.csv rates as the primary pricing mechanism. | PARAMETRIC basis of estimate matches the LOE model basis. This is the most direct and traceable pricing approach for professional services. | All 3 priced line items use this approach. |
| DEC-002 | Do not use Professional_Design_Fees.csv for pricing. | No Landscape Architectural fee row exists in that source. Extrapolating from other disciplines would require assumptions not supported by the data. | Fee-based cross-check is not available. |
| DEC-003 | Items ITEM-004 through ITEM-012 are recorded as scope-tracking items (Qty=1, Unit=LS, PricingMode=LUMP_SUM) in Items.csv but are not separately priced in Detail.csv. | Their professional effort is fully embedded in the Landscape Architect's 70-hour allocation (ITEM-003). Separately pricing them would result in double-counting. | 9 items in Items.csv have no corresponding Detail.csv rows; this is intentional, not a coverage gap. |
| DEC-004 | CBS categories assigned as "Professional Services — Management" and "Professional Services — Design" based on role category in Professional_Staff_Rates.csv. | Project Manager and Cost Estimator are Management category; Landscape Architect is Design category. This follows the rate table's own categorization. | WBS_CBS_Matrix uses these two CBS categories. |
| DEC-005 | FALLBACK_POLICY (ALLOW_PARAMETRIC) was not exercised. | All items were priceable using the primary PARAMETRIC method. No fallback was needed. | Clean method consistency. |
| DEC-006 | UPDATE_LATEST_POINTER = FALSE; no pointer file modified. | Per brief instruction. | No _LATEST.md file created or updated. |
