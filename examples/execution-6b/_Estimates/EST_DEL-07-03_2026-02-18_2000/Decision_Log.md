# Decision Log

**RunID:** EST_DEL-07-03_2026-02-18_2000

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS mapped to MGMT for all line items | R-02 (Project Manager) has Category=Management in Professional_Staff_Rates.csv. Deterministic mapping rule: Management -> MGMT. |
| EST-DEC-002 | Only R-02 (Project Manager) hours included; no Construction Manager hours | Level_of_Effort.csv contains exactly one row for DEL-07-03: R-02 at 8 hours. Although the brief mentions "PM/construction manager hours" as cost drivers, the authoritative source (Level_of_Effort.csv) assigns Construction Manager hours to DEL-07-01 and DEL-07-02 instead. Under STRICT fallback policy, no hours are added beyond what the source provides. |
| EST-DEC-003 | Cost ownership boundary: DEL-07-03 (approach narrative) vs DEL-01-09 (subtrade list) | Per brief instructions, DEL-07-03 costs cover the subconsultant management APPROACH narrative. DEL-01-09 covers the Appendix I subtrade LIST form. These are distinct deliverables with separate cost ownership. |
| EST-DEC-004 | No fallback pricing used | FALLBACK_POLICY=STRICT. All required hours and rates are available from price sources. No TBD amounts generated. |
