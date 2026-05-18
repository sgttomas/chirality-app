# Source Index: EST_DEL-05-03_2026-02-18_1430

## Price Sources Indexed

| Source File | Source Type | Items Used | Parsing Notes | Supports |
|---|---|---|---|---|
| Professional_Staff_Rates.csv | Rate Table | R-02 (PM, $175/hr), R-18 (Estimator Senior, $145/hr) | CSV; 30 roles total; 2 used for DEL-05-03 | Hourly rates for all production lines |
| Level_of_Effort.csv | Level of Effort | 2 rows for DEL-05-03: R-02 (12 hrs), R-18 (8 hrs) | CSV; 67 total rows; filtered to Execution=6c, DeliverableID=DEL-05-03 | Hours per role per deliverable |
| Assumed_Project_Parameters.csv | Project Parameters | PP-04 (6 weeks proposal timeline) used for context only | CSV; 29 parameters; not directly used for pricing calc | Context for coordination overhead and schedule assumptions |

---

## Dependency Sources Indexed

| Source File | Source Type | Items Used | Notes |
|---|---|---|---|
| DEL-05-03/Dependencies.csv | Dependency Register | 14 dependency rows (DEP-05-03-001 through DEP-05-03-014) | Used for blocker detection and readiness assessment; not for pricing evidence |

---

## Upstream Estimate References (context only; not pricing sources)

| Source | Used For | Notes |
|---|---|---|
| EST_DEL-05-01_2026-02-18_1400/Summary.md | Upstream context: Schedule A total ($10,738,960) | Referenced in brief; not used as pricing evidence for DEL-05-03 |
| EST_DEL-05-02_2026-02-18_1500/Summary.md | Upstream context: Schedule B total ($10,735,020) | Referenced in brief; not used as pricing evidence for DEL-05-03 |

---

## Sources NOT Used (available but not applicable)

| Source | Reason Not Used |
|---|---|
| Construction rate files (Structural_Concrete_Rates.csv, etc.) | DEL-05-03 is a pure narrative deliverable; no construction pricing content |
| Fees_Permits_Insurance.csv | Not applicable to narrative production cost |
| Optional_Items_Pricing.csv | Not applicable to narrative production cost |

---

## Evidence Coverage

- Total priced lines in Detail.csv: 2
- Lines with SourceRef: 2 (100%)
- Lines with location TBD: 0
- Provenance completeness: **100%**
