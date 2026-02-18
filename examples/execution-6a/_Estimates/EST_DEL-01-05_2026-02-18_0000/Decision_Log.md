# Decision Log — EST_DEL-01-05_2026-02-18_0000

| DecisionID | Decision | Rationale | Affected Lines |
|---|---|---|---|
| DEC-EST-001 | CBS codes assigned deterministically from Professional_Staff_Rates.csv Category field: Management -> PM, Administrative -> ADMIN | No CBSHint provided in decomposition; a deterministic mapping rule was needed. Role Category is the most stable available attribute. | L-01, L-02 |
| DEC-EST-002 | Hours taken directly from Level_of_Effort.csv as given quantities; not independently re-derived | Level_of_Effort.csv provides explicit hour estimates per deliverable per role. Re-deriving hours from first principles is outside this run's scope. The LOE source notes document the parametric basis (e.g., biweekly meetings x 18 months). | L-01, L-02 |
| DEC-EST-003 | Document control system costs not priced (TBD) | Brief identifies "document control system costs" as a cost driver, but no pricing source provides DMS/software cost data. Under STRICT fallback policy, TBD items are not priced; they are surfaced in QA. | N/A (no line created) |
| DEC-EST-004 | No overhead, markup, or profit applied to bare labour rates | Professional_Staff_Rates.csv provides bare hourly rates. No overhead multiplier or fee schedule was provided in PRICE_SOURCES. Applying a markup without evidence would violate the no-invention invariant. | L-01, L-02 |
| DEC-EST-005 | Rounding applied at DOLLAR level per brief instruction | ROUNDING=DOLLAR specified in brief. All computed amounts are already whole-dollar values (90 x 175 = 15,750; 50 x 80 = 4,000), so no rounding adjustment was needed. | L-01, L-02 |
