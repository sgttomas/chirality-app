# Decision Log -- EST_DEL-01-01_2026-02-18_1400

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS code `LABOUR.ADMIN` assigned to R-22 (Proposal Coordinator / Writer) based on Category=Administrative in Professional_Staff_Rates.csv | Deterministic mapping rule: role Category field drives CBS assignment. Documented in Run_Context.md. |
| EST-DEC-002 | Assumed_Project_Parameters.csv loaded but not used for pricing DEL-01-01 | DEL-01-01 is an administrative deliverable (compliance matrix); no construction quantities or areas apply. Parameters file indexed in Source_Index.md for completeness. |
| EST-DEC-003 | Rounding applied: DOLLAR. Amount $840 is already a whole dollar; no rounding adjustment needed. | Per brief: ROUNDING=DOLLAR. |
| EST-DEC-004 | Single line item produced for DEL-01-01 (one role only: R-22) | Level_of_Effort.csv contains exactly one row for DEL-01-01 (R-22, 8 hrs). No other roles allocated. One line item per role-deliverable pair. |
| EST-DEC-005 | Cost ownership boundary enforced: compliance checking and addenda integration in DEL-01-01; PDF assembly and submission logistics in DEL-01-02 | Per brief Cost Ownership Rules. No hours from DEL-01-02 are included here. |
