# Assumptions Log -- EST_DEL-01-07_2026-02-18_1830

## Active Assumptions

### ASM-0107-001: Construction duration of 18 months

- **Statement:** The project construction duration is 18 months (NTP to Substantial Performance), as stated in PP-01 of Assumed_Project_Parameters.csv.
- **Impact on estimate:** The hour allocations in Level_of_Effort.csv for DEL-01-07 (particularly R-21 warranty admin at 20h) are predicated on this duration. A longer project could increase coordination hours.
- **Source:** Assumed_Project_Parameters.csv, row PP-01.
- **Confidence:** MEDIUM.

### ASM-0107-002: Commissioning Lead hours breakdown

- **Statement:** The 120 hours for R-21 (Commissioning Lead) are distributed as: Cx plan development (20h) + functional testing coordination (40h) + training delivery (20h) + as-built coordination (20h) + warranty admin (20h), per the Notes field in Level_of_Effort.csv.
- **Impact on estimate:** This breakdown is the basis for the single line item L-0107-01. If the scope of any sub-activity changes materially (e.g., more training sessions required), the hours would need revision.
- **Source:** Level_of_Effort.csv, row DEL-01-07/R-21, Notes column.
- **Confidence:** MEDIUM.

### ASM-0107-003: Warranty period of 12 months

- **Statement:** The warranty period is 12 months from occupancy permit issuance, per RFP section 7.6 and Datasheet.md.
- **Impact on estimate:** Warranty admin hours (20h within R-21 allocation) assume a 12-month period with periodic site visits and deficiency follow-up. Extended warranty obligations would increase hours.
- **Source:** Datasheet.md > Deficiency Process Attributes; RFP section 7.6.
- **Confidence:** HIGH (RFP-confirmed).

### ASM-0107-004: Document deliverables quantity

- **Statement:** As-built documentation includes 2 hard copies in 3-ring binders plus 1 complete digital copy, per RFP section 7.5 and Datasheet.md.
- **Impact on estimate:** The 20 hours for R-24 (Administrative / Document Control) assumes assembly of 2 hard copy sets and 1 digital set. Additional copies or more extensive binder organization would increase hours.
- **Source:** Datasheet.md > Delivery Format Requirements; RFP section 7.5.
- **Confidence:** HIGH (RFP-confirmed).

### ASM-0107-005: Rates are current and un-escalated

- **Statement:** Hourly rates from Professional_Staff_Rates.csv are assumed to be current (2026) market rates in CAD with no escalation or inflation adjustment applied.
- **Impact on estimate:** If the project extends into 2027 or 2028, rates may increase. No escalation factor has been applied.
- **Source:** Professional_Staff_Rates.csv, Basis=MARKET.
- **Confidence:** MEDIUM.

### ASM-0107-006: No disbursements or third-party costs included

- **Statement:** This estimate includes labor costs only (professional staff time at hourly rates). No disbursements, printing costs, travel, third-party testing fees, or external surveyor fees are included.
- **Impact on estimate:** The total of $23,650 is labor-only. If disbursements or third-party costs are to be included, additional line items would be needed.
- **Source:** PRICE_SOURCES contain only labor rates and hours; no disbursement schedule provided.
- **Confidence:** HIGH (explicit scope of provided inputs).
