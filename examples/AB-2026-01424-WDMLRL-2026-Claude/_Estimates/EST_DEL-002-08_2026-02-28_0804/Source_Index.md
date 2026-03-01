# Source Index — EST_DEL-002-08_2026-02-28_0804

**RunID:** EST_DEL-002-08_2026-02-28_0804
**AsOf:** 2026-02-28T08:04:00-07:00

---

## Price Sources Used

| # | Source File | Path | Type | Role in Estimate |
|---|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv | PARAMETRIC (rate table) | Hourly rates by role in CAD; 25 roles defined. Used for R-01 ($165/hr), R-08 ($135/hr), R-13 ($95/hr), R-14 ($170/hr). Confidence: MEDIUM. |
| 2 | Level_of_Effort.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv | PARAMETRIC (hours model) | Per-deliverable hours allocation by role. Provides hours for DEL-002-08 across R-01 (6 hrs), R-08 (4 hrs), R-13 (36 hrs), R-14 (84 hrs). Confidence: MEDIUM. |
| 3 | Assumed_Project_Parameters.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv | PARAMETRIC (parameters) | 19 project parameters used for context validation and scope framing. Not directly consumed for unit pricing. |
| 4 | Professional_Design_Fees.csv | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv | PARAMETRIC (fee model) | Percentage-based design fee schedules. Listed as available source but not used for DEL-002-08 pricing; LOE hours-based pricing was preferred. |

---

## Source-to-Line Traceability

| LineID | Source File(s) | Keys / Sections Referenced |
|---|---|---|
| LN-001 | Professional_Staff_Rates.csv, Level_of_Effort.csv | R-01 rate ($165/hr); DEL-002-08/R-01 hours (6 hrs) |
| LN-002 | Professional_Staff_Rates.csv, Level_of_Effort.csv | R-08 rate ($135/hr); DEL-002-08/R-08 hours (4 hrs) |
| LN-003 | Professional_Staff_Rates.csv, Level_of_Effort.csv | R-13 rate ($95/hr); DEL-002-08/R-13 hours (36 hrs) |
| LN-004 | Professional_Staff_Rates.csv, Level_of_Effort.csv | R-14 rate ($170/hr); DEL-002-08/R-14 hours (84 hrs) |
| LN-005 | Procedure (Step 7) | Coordination review — no incremental cost; effort captured within LN-004 |
| LN-006 | Professional_Staff_Rates.csv, Decision_Log (DEC-R01) | R-14 rate ($170/hr); 8 hrs allocated per Decision_Log DEC-R01 for peer review |

---

## Notes

- All priced line items (LN-001 through LN-004, LN-006) use the PARAMETRIC method with dual-source pricing (rate table + hours model).
- LN-005 is a zero-cost coordination line; its effort is embedded in LN-004 Structural Engineer hours.
- LN-006 peer review hours (8 hrs) are sourced from Decision_Log DEC-R01, not from Level_of_Effort.csv.
