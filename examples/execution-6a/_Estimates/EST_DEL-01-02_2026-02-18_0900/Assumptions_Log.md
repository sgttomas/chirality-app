# Assumptions Log — EST_DEL-01-02_2026-02-18_0900

## Assumptions

### ASM-001 — Scheduler Hours Based on 18-Month Duration

| Field | Value |
|---|---|
| Assumption | The Scheduler (R-17) LOE of 80 hours is based on: schedule development (40h) + monthly updates (2h/mo x 18mo = 36h) + closeout (~4h). This assumes an 18-month construction duration per PP-01. |
| Source | Level_of_Effort.csv row DEL-01-02 R-17 (Notes column); Assumed_Project_Parameters.csv PP-01 |
| Impact | If project duration changes, monthly update hours scale proportionally. A 24-month duration would add ~12 hours (~$1,560 CAD at R-17 rate). |
| Confidence | MEDIUM |

### ASM-002 — PM Hours for Schedule Oversight Are Incremental

| Field | Value |
|---|---|
| Assumption | The 20 hours of Project Manager (R-02) time allocated to DEL-01-02 represent the incremental PM effort specifically for schedule review and reporting oversight. The PM's broader project management hours are carried in other deliverables (e.g., DEL-01-01, DEL-01-05). |
| Source | Level_of_Effort.csv row DEL-01-02 R-02; Deliverable Context in brief: PKG-001 cost ownership rules |
| Impact | If PM schedule oversight hours are double-counted with DEL-01-01 or DEL-01-05, the total PKG-001 PM hours would be overstated. Aggregation-level review should verify no overlap. |
| Confidence | MEDIUM |

### ASM-003 — Staff Rates Are Blended/Market Rates

| Field | Value |
|---|---|
| Assumption | The hourly rates in Professional_Staff_Rates.csv represent market-rate estimates (Basis=MARKET), not contracted or confirmed rates. Actual rates may differ. |
| Source | Professional_Staff_Rates.csv (all rows Basis=MARKET, Confidence=MEDIUM) |
| Impact | Rate variance of +/- 15% on both roles would change the priced total by approximately +/- $2,085. |
| Confidence | MEDIUM |

### ASM-004 — Software/Tools Cost May Be Immaterial or Absorbed in Overhead

| Field | Value |
|---|---|
| Assumption | The "software/tools" cost driver may be immaterial if scheduling software is already licensed as part of the Design-Builder's overhead. If a separate purchase or subscription is required, the cost would need to be provided. |
| Source | Brief (cost drivers); no pricing source available |
| Impact | If software cost is zero (absorbed), L-003 can be removed. If $500-$2,000/yr for a scheduling tool, it adds 4-14% to the deliverable total. |
| Confidence | LOW |
