# Decision Log -- EST_DEL-07-02_2026-02-18_2359

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS assigned as `PROF_SERVICES.CONSTRUCTION_MGMT` | No CBSHint in decomposition. Deterministic rule: sole contributing role is R-15 (Construction Manager, Category=Construction); deliverable type is "Construction / Narrative"; all hours are professional services for narrative authoring. |
| EST-DEC-002 | Single line item in Detail.csv (no sub-line decomposition by topic) | Level_of_Effort.csv provides a single row for DEL-07-02 (R-15, 8 hrs). The BOE context identifies multiple sub-topics (supervision, document management, shop drawings, cleaning, transport/storage, site services), but the pricing source does not decompose hours by sub-topic. Creating sub-lines would require inventing hour splits not supported by evidence. Per no-invention invariant, one line item is produced. |
| EST-DEC-003 | Method = RATE_TABLE (not PARAMETRIC) despite LOE Basis column showing "PARAMETRIC" | The LOE file's "Basis" column describes how the *hours* were derived (parametric estimation of effort). The *pricing method* for this estimate run uses those hours with explicit rate-table rates ($155/hr from Professional_Staff_Rates.csv). The pricing method is therefore RATE_TABLE, consistent with BASIS_OF_ESTIMATE. The parametric origin of the hours is noted in the Detail.csv Notes column. |
| EST-DEC-004 | No fallback pricing required | FALLBACK_POLICY = STRICT. All in-scope items have both hours (S-02) and rates (S-01). No TBD amounts. |
| EST-DEC-005 | ROUNDING applied as DOLLAR (nearest whole dollar) | 8 hrs x $155/hr = $1,240.00 exactly. No rounding adjustment needed. Documented for auditability. |
