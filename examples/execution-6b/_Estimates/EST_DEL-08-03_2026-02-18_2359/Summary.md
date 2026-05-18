# Estimate Summary -- DEL-08-03 (Warranty Requirements Narrative)

**RunID:** EST_DEL-08-03_2026-02-18_2359
**Basis of Estimate:** RATE_TABLE
**Currency:** CAD
**Rounding:** DOLLAR

---

## Totals

| Package | Deliverable | CBS | Amount (CAD) | Line Count |
|---|---|---|---:|---:|
| PKG-008 | DEL-08-03 | PROFESSIONAL_SERVICES | $1,260 | 2 |
| | | **TOTAL** | **$1,260** | **2** |

## Breakdown by Role

| Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---:|---:|---:|
| R-02 Project Manager | 4 | $175 | $700 |
| R-21 Commissioning Lead | 4 | $140 | $560 |
| **Total** | **8** | | **$1,260** |

## Basis of Estimate Used

- **Method:** RATE_TABLE for all lines (no mixed methods; ALLOW_MIXED_METHODS=FALSE).
- **Hours source:** `Level_of_Effort.csv` -- 2 rows for DEL-08-03 (R-02 @ 4 hrs, R-21 @ 4 hrs).
- **Rates source:** `Professional_Staff_Rates.csv` -- R-02 @ $175/hr, R-21 @ $140/hr.
- **Computation:** Amount = Qty (hours) x UnitRate (hourly rate), rounded to nearest dollar.

## Key Warnings and Blockers

- **No pricing warnings.** All lines fully priced with evidence.
- **Dependency blocker (informational):** DEL-08-01 (Commissioning Training Closeout Narrative) is listed as a prerequisite for DEL-08-03 with `SatisfactionStatus=TBD` (DEP-08-03-003). DEL-08-02 (Deficiencies Management Narrative) is also a prerequisite with `SatisfactionStatus=TBD` (DEP-08-03-004). These do not affect cost estimation but indicate that authoring readiness for DEL-08-03 depends on upstream deliverable maturity.
- **CCDC 14-2013 GC 12.5 base text:** DEP-08-03-007 notes that the full text of the base warranty article is not yet accessible (`location TBD`). This is a content-readiness concern, not a pricing concern.

## Cost Drivers

The cost of DEL-08-03 is driven entirely by professional staff hours for narrative authoring. The deliverable covers: 12-month all-inclusive warranty from occupancy permit date, manufacturer warranties to O&M manual, and Supplementary Conditions warranty provisions (SC54-SC55). The PM leads authoring (4 hrs) while the Commissioning Lead provides warranty-commissioning integration input (4 hrs). Total effort is 8 person-hours.
