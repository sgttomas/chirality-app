# Assumptions Log — EST_DEL-07-02_2026-02-18_2130

## Assumptions

### ASM-07-02-001: Hourly Rates Are Market Estimates

- **Assumption:** The hourly rates in Professional_Staff_Rates.csv (R-22: $105/hr, R-26: $85/hr) are representative of Alberta 2024 market rates for proposal coordination and HR coordination roles.
- **Basis:** Professional_Staff_Rates.csv Basis column = "MARKET"; Confidence = "MEDIUM".
- **Impact if wrong:** +/-20-30% on total amount ($1,860). Range: ~$1,300 to ~$2,400.
- **Resolution:** Replace with actual firm rates when available.

### ASM-07-02-002: Level of Effort Hours Are Parametric Estimates

- **Assumption:** The hours in Level_of_Effort.csv (R-26: 12 hr, R-22: 8 hr) are adequate for resume compilation, formatting, availability coordination, and role descriptions for a Design-Build proposal team on a $15-20M municipal project.
- **Basis:** Level_of_Effort.csv Basis column = "PARAMETRIC"; Notes reference "Same scope as 6b DEL-01-08".
- **Impact if wrong:** +/-20-30% on hours, translating to +/-$370-$560 on total.
- **Resolution:** Validate against actual effort tracking from comparable proposals.

### ASM-07-02-003: Team Size Within Typical Range

- **Assumption:** The number of key team members requiring resumes is within the typical range for this project type (estimated 8-12 key personnel). The LOE hours are calibrated for this range.
- **Basis:** Decomposition Section 8 DEL-07-02 acceptance criteria: "Covers all key roles; credentials align with project type and scope." Professional_Staff_Rates.csv lists ~15 distinct proposal-active roles, of which 8-12 would typically be presented as key personnel.
- **Impact if wrong:** If significantly more personnel are required, hours would increase proportionally.
- **Resolution:** Confirm team roster size during proposal staffing.

### ASM-07-02-004: No External Resume Writing Services

- **Assumption:** Resume compilation and formatting is performed entirely by internal HR Coordinator and Proposal Coordinator staff. No external writing or graphic design services are included.
- **Basis:** Level_of_Effort.csv lists only R-26 and R-22 for DEL-07-02. No external service line items exist in the price sources for this deliverable.
- **Impact if wrong:** External resume writing/design services would add cost not captured here.
- **Resolution:** Confirm internal-only approach during proposal planning.
