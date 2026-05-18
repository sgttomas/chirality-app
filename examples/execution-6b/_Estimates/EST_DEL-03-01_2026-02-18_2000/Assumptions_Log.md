# Assumptions Log

**Snapshot:** EST_DEL-03-01_2026-02-18_2000

| AssumptionID | Assumption | Source / Basis | Impact if Wrong |
|---|---|---|---|
| ASM-001 | DEL-03-01 requires 12 hours of Architect (Project) time | Level_of_Effort.csv row DEL-03-01/R-04; PARAMETRIC basis | If actual hours differ, total changes by $145/hr per hour delta. At 12 hrs, a +/- 4 hr variance = +/- $580. |
| ASM-002 | Architect (Project) hourly rate is $145 CAD | Professional_Staff_Rates.csv row R-04; MARKET basis, MEDIUM confidence | If actual rate is higher/lower, total scales linearly. A +/- $20/hr variance on 12 hrs = +/- $240. |
| ASM-003 | No additional roles are required for DEL-03-01 beyond R-04 | Level_of_Effort.csv shows only R-04 for DEL-03-01; no PM review, no intermediate architect, no CAD support | If peer review or PM oversight hours are needed, those would be additional cost. Typical oversight might add 2-4 hrs at $120-$175/hr ($240-$700). |
| ASM-004 | DEL-03-01 scope is limited to the architectural discipline sub-brief of SOW-0011 | Decomposition v2.3 FINAL; brief context ("each DEL covers ONLY its discipline sub-brief") | If scope creeps to include content belonging to DEL-03-02 through DEL-03-06, hours would increase. |
| ASM-005 | No revision cycles beyond what is included in the 12-hour estimate | Level_of_Effort.csv does not itemize revision cycles separately | If significant revisions are required (e.g., after concept package changes), additional hours would be needed. |
