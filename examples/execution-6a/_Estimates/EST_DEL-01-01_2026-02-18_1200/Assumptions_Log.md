# Assumptions Log

## Run: EST_DEL-01-01_2026-02-18_1200

### ASM-001: Project Duration

- **Assumption:** Construction duration is 18 months (NTP to Substantial Performance).
- **Source:** Assumed_Project_Parameters.csv, PP-01 (Source=ASSUMPTION, Confidence=MEDIUM).
- **Impact:** Drives PM hours (120 hr at ~7 hr/wk over 18 months) and Admin hours (60 hr at ~3.5 hr/wk over 18 months).
- **Risk if wrong:** If project duration extends beyond 18 months, PM and Admin hours would increase proportionally. A 20% duration increase would add approximately $5,200 to the estimate.

### ASM-002: Design Phase Duration

- **Assumption:** Design phase duration is 4 months.
- **Source:** Assumed_Project_Parameters.csv, PP-02 (Source=ASSUMPTION, Confidence=MEDIUM).
- **Impact:** Drives Design Manager hours (80 hr over 4 months of active design + periodic review during construction).
- **Risk if wrong:** If design phase extends, Design Manager hours would increase. Moderate sensitivity.

### ASM-003: Staff Rates Are Market-Basis Estimates

- **Assumption:** Hourly rates in Professional_Staff_Rates.csv are representative market rates for Alberta, not negotiated/contracted rates.
- **Source:** Professional_Staff_Rates.csv, Basis=MARKET for all roles, Confidence=MEDIUM.
- **Impact:** All amounts are based on these rates. Actual contracted rates may differ.
- **Risk if wrong:** Rate variance of +/-15% would change the total by approximately +/-$6,700.

### ASM-004: Level of Effort Is Parametric

- **Assumption:** Hour estimates in Level_of_Effort.csv are parametric (based on typical project effort distribution), not based on detailed task-level work breakdown.
- **Source:** Level_of_Effort.csv, Basis=PARAMETRIC for all rows.
- **Impact:** Hours are reasonable approximations but may not reflect actual project complexity.
- **Risk if wrong:** Hour variance of +/-20% would change the total by approximately +/-$8,960.

### ASM-005: No Escalation or Inflation Factor

- **Assumption:** Rates are current (no escalation applied for future periods).
- **Source:** Professional_Staff_Rates.csv contains no escalation column or date-based adjustment.
- **Impact:** If the project spans multiple years, rates may need escalation adjustment.
- **Risk if wrong:** Typical professional fee escalation of 2-4% per year could add $900-$1,800 for an 18-month project.
