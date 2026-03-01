# Decision Log — EST_DEL-004-01_2026-02-26_2043

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| ED-001 | Used Level_of_Effort.csv (parametric hours) as primary pricing source rather than Professional_Design_Fees.csv (fee-percentage model) | LOE-based pricing provides role-level traceability and is consistent with the PARAMETRIC basis of estimate. Fee-percentage model requires a construction value which is not yet confirmed. | Primary pricing method for all 4 Detail.csv lines |
| ED-002 | Classified Items 5–25 as scope verification lines with costs embedded in labour (Items 1–4) | DEL-004-01 is a professional design deliverable. The priceable output is the engineer's time, not separate physical items. The systems listed (lighting, receptacles, circuits, etc.) are the scope the engineer addresses, not separately procurable items. | 21 items in Items.csv are LUMP_SUM with Qty=1/Unit=LS; not separately priced in Detail.csv |
| ED-003 | Assigned CBS categories: Design-Management (PM + Estimator), Design-Production (BIM Tech), Design-Engineering (Electrical Engineer) | Standard CBS taxonomy for professional design deliverables; separates management overhead, production/drafting, and lead engineering effort | WBS_CBS_Matrix.csv rollups reflect this split |
| ED-004 | Did not apply FALLBACK_POLICY | All items were priceable from primary PARAMETRIC sources. No fallback was needed. | No impact |
| ED-005 | Did not update _LATEST.md pointer | UPDATE_LATEST_POINTER = FALSE per run brief | No pointer file modified |
