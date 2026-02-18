# Decision Log: EST_DEL-03-04_2026-02-18_2100

## Decisions Made During This Run

| DecisionID | Decision | Rationale | Impact |
|-----------|----------|-----------|--------|
| RD-001 | Use UU-12 recommended value of $35,000 for DEC-004 tie-in allowance | DEC-004 states "no value pre-set"; UU-12 in Underground_Utility_Rates.csv provides a recommended range of $25,000-$50,000 with $35,000 recommended. Used recommended value as placeholder. | Line L-0304-12 = $35,000. PENDING OWNER CONFIRMATION. |
| RD-002 | Apply ALLOW_ALLOWANCE fallback for utility connection fees (FP-11 through FP-15) | No RATE_TABLE evidence exists for provider connection fees; these are set by external entities. FALLBACK_POLICY=ALLOW_ALLOWANCE permits carrying them as ALLOWANCE. | 5 lines (L-0304-13 through L-0304-17) at ALLOWANCE method; $39,000 subtotal. |
| RD-003 | Compute civil design fee as 2.5% of distribution construction cost ($149,200) rather than full PP-23 site/civil value ($1,800,000) | PP-23 covers all site/civil scope (DEL-03-01 through DEL-03-05). DEL-03-04 is only the utility routing portion. Using the distribution line items subtotal as the fee base avoids overcounting design fees. | L-0304-18 = $3,730 (vs $45,000 if full PP-23 were used). |
| RD-004 | Include water service to Cold Storage Building as assumed requirement | Datasheet states Cold Storage water requirement is TBD. Including it provides a conservative estimate. Removal if not required reduces total by ~$12,500. | L-0304-02 ($8,000) + L-0304-04 ($4,500) = $12,500 at risk of not being needed. |
| RD-005 | Exclude sanitary sewer service to Cold Storage Building | Cold Storage is unheated with no plumbing fixtures identified. Sanitary service would only be needed if water/drainage fixtures are added. | No sanitary lines to Cold Storage. If required, add ~$13,000 (40m x $225/lm + $4,000 connection). |
| RD-006 | Exclude natural gas service to Cold Storage Building | Cold Storage is explicitly unheated per OSR 10.2 and DEC-001. No gas load identified. | No gas lines to Cold Storage. |
| RD-007 | Exclude telecom conduit to Cold Storage Building | Cold Storage is an unheated storage building. No telecom/data requirements identified in Datasheet. | No telecom lines to Cold Storage. |
| RD-008 | Use common trench assumption of 100 m for shared water/sewer/gas corridor | Standard civil practice: water, sanitary sewer, and gas are typically co-located in a common trench corridor where alignment permits. 100 m of the 120 m run to PSB assumed shared. | L-0304-11 = $10,000. Note: this cost is incremental to per-utility rates which include their own trench costs; the common trench line represents the shared excavation efficiency credit is NOT applied (conservative). |
| RD-009 | Demarcation point set at 1.5 m outside building foundation wall per brief | Brief specifies "1.5m outside building foundation wall" as the boundary between DEL-03-04 (PKG-003 side) and PKG-002 discipline deliverables. All distribution lengths terminate at this point. | All distribution line items stop at 1.5m outside building; building entry costs are excluded. |

## Defaults Applied

| Parameter | Default Used | Source |
|-----------|-------------|--------|
| FALLBACK_POLICY | ALLOW_ALLOWANCE | Brief input |
| ALLOW_MIXED_METHODS | TRUE | Brief input |
| ROUNDING | DOLLAR | Brief input |
| UPDATE_LATEST_POINTER | FALSE | Brief input |
| CBS mapping | Deterministic rule in Run_Context.md | Agent-derived; no CBSHint in decomposition |
