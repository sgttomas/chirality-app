# Decision Log — EST_DEL-008-02_2026-02-26_2232

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Used PARAMETRIC method for all line items | BASIS_OF_ESTIMATE=PARAMETRIC; all pricing sources are parametric (rates + hours) | Consistent with brief; no mixed methods required |
| DEC-002 | Estimated Surveyor (R-21) hours parametrically at 90 hr total | Level_of_Effort.csv has DEL-008-02 Surveyor hours as TBD; FALLBACK_POLICY=ALLOW_PARAMETRIC authorizes parametric estimation | Surveyor labour ($12,600) is 89% of total estimate; hours need validation by licensed surveyor |
| DEC-003 | Allocated Surveyor hours across 11 activity line items based on Procedure steps | Procedure.md defines 7 discrete steps plus prerequisites; mapped each to a line item with proportional effort | Provides activity-level traceability; individual line allocations are estimates |
| DEC-004 | Used single CBS category "Professional Services" for all lines | All priceable items are professional staff labour; no materials, equipment, or construction activities identified as priceable with available sources | CBS rollup is a single row; future estimates may split by sub-category |
| DEC-005 | Set ITEM-013 (Data Backup) at 0 hours | Data backup and security protocols are included in the field and processing effort (ITEM-003, ITEM-006) per Guidance description; avoids double-counting | Zero-cost line retained for traceability to Guidance document |
| DEC-006 | Assumed single-person survey crew | No crew size parameter in sources; single surveyor is common for small-site preliminary surveys | If two-person crew required, field hours approximately double |
| DEC-007 | Assumed approximate boundary (not full legal ALS survey) | Boundary scope described as TBD with Owner in multiple source documents; approximate boundary is lower-cost default | If ALS legal survey required, ITEM-004 effort increases substantially |
| DEC-008 | Excluded equipment, travel, materials, subconsultant costs | No rate sources provided for these cost categories; cannot price without basis | Estimate covers professional labour only; total is understated relative to full survey cost |
