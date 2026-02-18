# Assumptions Log -- EST_DEL-02-03_2026-02-18_1500

## Assumptions Made During This Run

### ASM-001: Staff Rates Reflect Alberta 2024 Market Conditions

- **Assumption:** Hourly rates in Professional_Staff_Rates.csv are representative of typical Design-Build firm internal rates for Alberta in 2024.
- **Source:** Professional_Staff_Rates.csv (Basis = MARKET, Confidence = MEDIUM for all used roles)
- **Impact if wrong:** All line item amounts scale linearly with rate changes. A +/-20% rate variance would move the total from $3,816 to $5,724 (range: -$954 to +$954 on $4,770 base).
- **Risk level:** MEDIUM

### ASM-002: Level of Effort Hours Are Adequate for Scope

- **Assumption:** The 30 total hours allocated to DEL-02-03 (12 + 8 + 6 + 4) in Level_of_Effort.csv are sufficient to produce the Sustainability & Energy Narrative deliverable.
- **Source:** Level_of_Effort.csv (Basis = PARAMETRIC, 6c execution row set)
- **Impact if wrong:** Hours may need to increase if scope complexity is higher than estimated (e.g., LEED certification narrative, detailed energy modelling descriptions, extensive code compliance analysis). A +/-30% hours variance would move the total from $3,339 to $6,201.
- **Risk level:** MEDIUM

### ASM-003: PM Coordination Overhead Captured Upstream

- **Assumption:** No Project Manager (R-02) hours are allocated to DEL-02-03 in the LOE. This is accepted because DEL-02-03 is a T2 deliverable (dependent on DEL-02-01 and DEL-02-02), and PM coordination overhead for PKG-04 is assumed to be captured in the PM hours allocated to those upstream deliverables (DEL-02-01: 10 PM hours; DEL-02-02: 6 PM hours).
- **Source:** Level_of_Effort.csv (no R-02 row for DEL-02-03); brief BOE context (Tier T2)
- **Impact if wrong:** If DEL-02-03 requires dedicated PM coordination (e.g., 2-4 hours), the estimate would increase by $350-$700 (R-02 @ $175/hr).
- **Risk level:** LOW

### ASM-004: No External Consulting or Software Costs

- **Assumption:** DEL-02-03 production requires only professional staff labour. No external energy modelling software licenses, third-party sustainability consulting, or specialized analysis tools are required beyond what is embedded in the hourly rates.
- **Source:** INDEX.md notes PS-10/PS-11 state software costs are embedded in hourly rates.
- **Impact if wrong:** External energy modelling or sustainability certification consulting could add $2,000-$10,000 depending on scope.
- **Risk level:** LOW (for proposal-stage narrative; would be higher for detailed design phase)

### ASM-005: Single Iteration -- No Rework Cycle

- **Assumption:** Hours assume a single production pass with minor internal review. No major rework cycle from client feedback is included (this is a proposal deliverable, not a post-award design document).
- **Source:** Implied by Level_of_Effort.csv PARAMETRIC basis; consistent with proposal production workflow.
- **Impact if wrong:** A rework cycle could add 30-50% to hours ($1,431-$2,385 additional).
- **Risk level:** LOW (proposal deliverable; limited revision cycle expected)
