# Decision Log

**RunID:** EST_DEL-03-02_2026-02-18_1955

---

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS mapped to `PROF_SERVICES` for all DEL-03-02 line items | No explicit CBSHint in decomposition. Deterministic rule applied: design brief narratives (PKG-003) are professional services labor. Documented in Run_Context.md. |
| EST-DEC-002 | Method set to `RATE_TABLE` for all lines (no fallback used) | `BASIS_OF_ESTIMATE = RATE_TABLE`, `FALLBACK_POLICY = STRICT`, `ALLOW_MIXED_METHODS = FALSE`. Hours from Level_of_Effort.csv priced at rates from Professional_Staff_Rates.csv. No missing evidence requiring fallback. |
| EST-DEC-003 | Level_of_Effort.csv "PARAMETRIC" basis label treated as hour-quantity input (not as estimating method) | The LoE file self-labels its basis as PARAMETRIC (how the hours were originally derived). The estimating method applied here is RATE_TABLE (hours x rate). This distinction is documented in Run_Context.md Method Note. |
| EST-DEC-004 | Rounding applied: DOLLAR | Per brief. Amount $1,550 is already a whole dollar; no rounding adjustment needed. |
| EST-DEC-005 | Assumed_Project_Parameters.csv read but not used for line-item pricing | Parameters provide project context (site area, building area) but DEL-03-02 pricing is purely hours x rate. Parameters confirmed for contextual awareness only. |
