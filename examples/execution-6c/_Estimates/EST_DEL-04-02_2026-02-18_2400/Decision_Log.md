# Decision Log -- EST_DEL-04-02_2026-02-18_2400

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-EST-001 | CBS assigned as `PROF_SERVICES` for all line items | No `CBSHint` present in decomposition. DEL-04-02 is a proposal production deliverable; all costs are professional staff hours. Deterministic mapping rule documented in Run_Context.md. |
| DEC-EST-002 | LOE hours taken directly from Level_of_Effort.csv without adjustment | LOE source (PS-02) provides hours per role for DEL-04-02 in execution 6c: R-02 = 8h, R-15 = 4h. No basis to adjust; STRICT fallback policy prohibits invention. |
| DEC-EST-003 | Hourly rates taken directly from Professional_Staff_Rates.csv without adjustment | Rate table (PS-01) provides market-based Alberta 2024 rates. No override or adjustment factor specified in brief. |
| DEC-EST-004 | Upstream dependencies (DEL-05-01/02/03, DEL-04-01/03, DEL-08-01, DEL-09-01) do not block estimating | Cost is driven by staff effort allocation, not by upstream content. Dependencies affect deliverable execution readiness but not the cost estimate. BOE context note confirms: "production hours can be estimated without final pricing -- the budget control METHODOLOGY doesn't require knowing the actual numbers." |
| DEC-EST-005 | No fallback pricing applied | All line items have complete basis evidence from rate table sources. STRICT fallback policy not triggered. |
| DEC-EST-006 | Rounding applied at DOLLAR level | Per brief instruction. All computed amounts are already whole dollar amounts (175 x 8 = 1400; 155 x 4 = 620), so rounding had no effect. |
| DEC-EST-007 | BASIS_OF_ESTIMATE resolved as RATE_TABLE from BOE document | Brief provides a file path to BASIS_OF_ESTIMATE.md. BOE Section 4 PKG-06 table specifies `RATE_TABLE` for DEL-04-02. This is a valid enum value per SPEC S3. |
| DEC-EST-008 | SOW-020 scope assignment accepted from _CONTEXT.md despite scope ledger ambiguity | Dependencies.csv Anchor Validation Notes document that SOW-020 maps to DEL-04-01 in the scope ledger but _CONTEXT.md explicitly assigns it to DEL-04-02. The LOE allocation treats DEL-04-02 as budget control/change management (distinct from DEL-04-01 methodology). No double-counting risk detected: LOE rows for DEL-04-01 and DEL-04-02 are independently specified. |
