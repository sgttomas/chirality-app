# Assumptions Log -- EST_DEL-09-02_2026-02-18_1600

## Active Assumptions

### ASM-001: Hourly Rates Are Market Parametric

**Assumption:** The hourly rates in Professional_Staff_Rates.csv (R-02: $175/hr, R-07: $155/hr, R-29: $155/hr) are Alberta 2024 market-based parametric estimates, not firm-specific actual rates.

**Source:** Professional_Staff_Rates.csv, Basis=MARKET, Confidence=MEDIUM for all applicable roles.

**Impact if wrong:** If actual firm rates differ by +/-20%, the deliverable estimate could range from ~$2,360 to ~$3,540 (vs. current $2,950).

**Mitigation:** Replace with firm-specific rates when available and rerun.

### ASM-002: Level of Effort Is a Planning Estimate

**Assumption:** The hours in Level_of_Effort.csv (R-02: 8h, R-07: 6h, R-29: 4h) are planning estimates based on comparable proposal efforts for $15-20M municipal DB projects, not actuals from a specific project.

**Source:** Level_of_Effort.csv, Basis=PARAMETRIC, Confidence=MEDIUM (implied +/-20-30% per INDEX.md).

**Impact if wrong:** If actual hours differ by +/-30%, the deliverable estimate could range from ~$2,065 to ~$3,835.

**Mitigation:** Track actual hours during proposal production and compare to estimate at closeout.

### ASM-003: DEL-09-02 Scope Is Proposal Production Only

**Assumption:** This estimate covers only the proposal production cost of writing the Site Conditions & Due Diligence Summary for the RFP response. It does not include the cost of conducting new site investigations, obtaining new surveys, or commissioning new reports.

**Source:** Decomposition Section 8 (DEL-09-02 output = "Summary of reference studies... and implications for concept/price"). BOE Context states "files after award per Addendum 03."

**Impact if wrong:** If new investigation work is required during proposal phase, costs would be materially higher.

**Mitigation:** N/A -- scope is correctly scoped to proposal production per decomposition.

### ASM-004: Three Roles Are Sufficient

**Assumption:** Only 3 roles (PM, Senior Civil, Geotechnical Engineer) are needed to produce DEL-09-02. No additional roles (e.g., environmental consultant R-28, proposal coordinator R-22) are required.

**Source:** Level_of_Effort.csv lists only 3 rows for DEL-09-02 in execution 6c.

**Impact if wrong:** If additional specialist review is needed (e.g., environmental consultant for wetland/contamination sections), hours and cost would increase.

**Mitigation:** Level_of_Effort.csv should be updated if scope changes.
