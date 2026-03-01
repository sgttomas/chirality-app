# Summary — EST_DEL-013-04_2026-02-27_0901

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **CURRENCY** | CAD |
| **Methods Used** | PARAMETRIC (16 lines), ALLOWANCE (5 lines) |

The estimate uses PARAMETRIC as the primary method. Where equipment pricing data was available only as ALLOWANCE-basis rates in Mechanical_System_Rates.csv, ALLOWANCE method was applied per FALLBACK_POLICY=ALLOW_PARAMETRIC and ALLOW_MIXED_METHODS=TRUE.

---

## Total Estimated Cost

| Scope | Currency | Amount |
|---|---|---|
| **DEL-013-04 — Heavy Equipment Exhaust System** | **CAD** | **$99,916.80** |

---

## Totals by CBS Category

| CBS | Amount (CAD) | Line Count | % of Total |
|---|---|---|---|
| MECHANICAL_EQUIPMENT | 58,050.00 | 5 | 58.1% |
| MECHANICAL_DUCTWORK | 11,900.00 | 3 | 11.9% |
| CONSTRUCTION_LABOUR | 11,776.80 | 3 | 11.8% |
| COMMISSIONING | 6,000.00 | 2 | 6.0% |
| MECHANICAL_CONTROLS | 5,500.00 | 1 | 5.5% |
| PROJECT_MANAGEMENT | 3,870.00 | 4 | 3.9% |
| CONSTRUCTION_SUPERVISION | 1,450.00 | 1 | 1.5% |
| QUALITY | 810.00 | 1 | 0.8% |
| SAFETY | 560.00 | 1 | 0.6% |
| **TOTAL** | **99,916.80** | **21** | **100.0%** |

---

## Totals by Package / Deliverable

| Package | Deliverable | Amount (CAD) |
|---|---|---|
| PKG-013 | DEL-013-04 | 99,916.80 |

---

## Key Warnings and Coverage Gaps

1. **Multiple TBD engineering parameters.** Exhaust volumes (TBD-DS-02), fan sizing, hose drop count (TBD-DS-01), ductwork material spec (TBD-DS-04), controls spec (TBD-DS-05), and formal equipment list (TBD-DS-03) are all unresolved. These TBDs directly affect equipment sizing and therefore cost.

2. **Filtration scope is conditional (CQ-002).** Line L-005 includes $8,500 for a filtration system. If direct discharge is confirmed acceptable (the more common approach for source-capture hose systems), this amount should be removed, reducing the total to $91,416.80.

3. **Hose drop quantity is assumed.** 4 hose drops (2 per bay) assumed. If 6 or more drops are required, MECHANICAL_EQUIPMENT costs will increase proportionally (~$9,850 per additional drop).

4. **ALLOWANCE-basis equipment rates (LOW confidence).** The MS-04 rate ($9,500/EA for vehicle exhaust hose + fan system) is an ALLOWANCE with a range of $6,000-$14,000. The actual cost depends heavily on system type (fixed vs. retractable reels), manufacturer, and sizing.

5. **No electrical scope included.** Fan power circuits are out-of-scope (covered under DEL-015-04, PKG-015).

6. **Labour hours are parametric.** Construction trade hours (80 hr ductwork + 32 hr hose/fan + 24 hr labourer) are parametric estimates, not derived from detailed task schedules.

7. **No contingency or escalation applied.** This estimate is a base-case parametric snapshot without contingency markups.
