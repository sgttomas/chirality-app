# Decision Log -- EST_DEL-01-05_2026-02-18_2359

| DecisionID | Decision | Rationale |
|---|---|---|
| D-01 | Schedule B construction content lines are derived from the same rate sources and quantities as DEL-01-04 | Schedule B is the detailed breakdown of Schedule A; both must use identical pricing basis to ensure zero-variance reconciliation |
| D-02 | CBS codes reorganized from DEL-01-04 CBS scheme (CON.STR, CON.ENV, etc.) to Schedule B categories (CON.GR, CON.BLD, CON.SIT, OPT.*) | Schedule B has a different structural hierarchy (General Requirements / Buildings / Sitework / Additional Items) than Schedule A's discipline-based view; CBS codes adapted to match form structure |
| D-03 | LineIDs use prefix convention: A- for production, B-GR- for general requirements, B-BLD- for buildings, B-SIT- for sitework, C- for options | Enables clear identification of Schedule B section and cost group; consistent with DEL-01-04 A-/B-/C- scheme but with finer categorization |
| D-04 | Options broken into sub-items (e.g., wash bay = system + plumbing + environmental) while DEL-01-04 showed single lump sums | Schedule B requires more granular breakdown than Schedule A summary lines; sub-item totals match Schedule A lump sums exactly |
| D-05 | Security monitoring ($5,000/yr) shown as separate sub-line C-410 from camera system capital C-400 | Per DEL-01-05 Specification requirement: security monitoring must be listed as a separate sub-line; the combined total ($55,000) matches Schedule A |
| D-06 | Cold storage PEMB (B-BLD-700) classified under CON.BLD (Public Services Buildings) rather than a separate section | The RFP Schedule B template has three main sections (GR, Buildings, Sitework); cold storage is a building and belongs in Section 2 |
| D-07 | Temporary facilities and temp power (B-BLD-710, B-BLD-720) classified under CON.BLD | These are project-level costs that enable building construction; grouped with buildings rather than sitework or general requirements per construction accounting convention |
| D-08 | FALLBACK_POLICY=ALLOW_ALLOWANCE exercised for 4 lines: utility connection fees (B-GR-180), workshop equipment (B-BLD-598), municipal tie-in (B-SIT-360), FF&E (C-600) | These items have insufficient basis for unit-rate pricing; allowance treatment is appropriate and consistent with DEL-01-04 |
| D-09 | Production hours sourced from Level_of_Effort.csv rather than estimated independently | LoE file provides the authoritative allocation for DEL-01-05: 24 hrs senior estimator, 16 hrs intermediate, 4 hrs PM = 44 total hours |
