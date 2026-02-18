# Decision Log

**RunID:** EST_DEL-01-09_2026-02-18_1500

| DecisionID | Decision | Rationale |
|---|---|---|
| EDEC-001 | CBS assigned as `LABOUR` for all DEL-01-09 line items | All cost drivers are professional staff hours (PM coordination + administrative support). No materials, equipment, or subcontract costs are present for this administrative deliverable. |
| EDEC-002 | Method set to `RATE_TABLE` for all lines | Hours sourced from Level_of_Effort.csv and multiplied by rates from Professional_Staff_Rates.csv. This matches the brief-specified BASIS_OF_ESTIMATE = RATE_TABLE. The underlying Level_of_Effort.csv notes its basis as PARAMETRIC, but the estimating method applied here is a direct rate table lookup (hours x rate), which is consistent with RATE_TABLE. |
| EDEC-003 | Scope boundary: subtrade list compilation only; subconsultant management narrative excluded | Per INIT-TASK brief cost ownership rules: subtrade list compilation belongs to DEL-01-09; subconsultant management approach narrative belongs to DEL-07-03. This prevents double-counting. |
| EDEC-004 | Rounding applied: DOLLAR | All computed amounts are already whole-dollar values (1400, 320). No rounding adjustment needed. |
| EDEC-005 | FALLBACK_POLICY = STRICT enforced; no fallback needed | All line items have direct pricing evidence from rate tables and level-of-effort data. No TBD amounts or fallback methods were required. |
