# Decision Log

## Decisions Applied During This Run

| DecisionID | Decision | Rationale |
|---|---|---|
| DL-001 | Amount set to $20,000 CAD (fixed). | DEC-005 establishes FF&E as a $20,000 cash allowance. Price source OPT-18 confirms the same value with PriceMin=PriceMax=RecommendedPrice=$20,000. No range or uncertainty exists. |
| DL-002 | CBS code assigned as `FF&E`. | No explicit CBSHint in decomposition. Derived deterministically from the deliverable name ("Cash Allowance -- FF&E") and the OPT-18 category ("FF&E"). Documented in Run_Context.md. |
| DL-003 | Single line item used (no sub-allocations as separate lines). | The brief directs a single line in Detail.csv. The DB allocation (Meeting/Training $8k, Lunchroom $6k, Reception $3k, Misc $3k) is informational only and is recorded in Summary.md and Detail.csv Notes, not as separate priced lines. |
| DL-004 | Confidence set to HIGH. | Fixed allowance confirmed by two independent sources (DEC-005 decision and OPT-18 price source). No estimation uncertainty. |
| DL-005 | Scope boundary with DEL-05-06 enforced per brief. | Connected appliances (refrigerators, stove, dishwasher, laundry) and items requiring plumbing or dedicated electrical connection are excluded from DEL-05-07 and owned by DEL-05-06. This prevents double-counting. |
| DL-006 | No fallback policy invoked. | FALLBACK_POLICY=STRICT, but not triggered -- primary basis evidence was fully available. |
