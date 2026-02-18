# Decision Log — EST_DEL-01-07_2026-02-18_1500

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS code `PROP_PRODUCTION` assigned to all DEL-01-07 line items | All labor for this deliverable is proposal production work (writing + review). No design, construction, or external cost categories apply. Deterministic rule documented in Run_Context.md. |
| EST-DEC-002 | Assumed_Project_Parameters.csv listed in PRICE_SOURCES but not directly used for line-item pricing | DEL-01-07 is a qualifications narrative; its cost is driven by writing/review hours, not by project quantities (building area, bay counts, etc.). Parameters file provides project context only. |
| EST-DEC-003 | No fallback pricing applied | FALLBACK_POLICY = STRICT. All line items have complete basis evidence (hours from Level_of_Effort.csv, rates from Professional_Staff_Rates.csv). No TBD amounts required. |
| EST-DEC-004 | ROUNDING = DOLLAR applied; both line amounts are already whole-dollar values | 16 x $105 = $1,680; 4 x $175 = $700. No rounding adjustment needed. |
| EST-DEC-005 | PENDING external dependencies (DEP-0107-E006, DEP-0107-E007) classified as production blockers, not estimating blockers | These inputs affect what content goes into the document, not the level of effort required to produce it. The hours estimate is based on the task scope (research, write, review) regardless of specific portfolio content. |
