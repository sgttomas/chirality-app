# Assumptions Log — EST_DEL-02-02_2026-02-18_2024

**Snapshot:** EST_DEL-02-02_2026-02-18_2024
**Date:** 2026-02-18

---

## Active Assumptions

### ASM-0202-001: Hourly Rates Reflect Market Rates

**Assumption:** The hourly rates in Professional_Staff_Rates.csv are reasonable Alberta 2024 market rates for Design-Build professional staff.

**Source:** Professional_Staff_Rates.csv — all 8 matched roles have `Basis=MARKET` and `Confidence=MEDIUM`.

**Impact if wrong:** +/-20-30% on total estimate. If actual firm rates differ materially from market rates, the estimate would need adjustment. At MEDIUM confidence, the $12,170 total could range from approximately $8,500 to $15,800.

**Mitigation:** Replace with actual firm billing rates when available.

---

### ASM-0202-002: Level of Effort Hours Are Adequate

**Assumption:** The 80 hours allocated across 8 roles in Level_of_Effort.csv are adequate to produce a consolidated design brief narrative covering 5 SOW items with multi-discipline input.

**Source:** Level_of_Effort.csv — all 8 matched rows have `Basis=PARAMETRIC` (planning estimates based on comparable proposal efforts for $15-20M municipal DB projects).

**Impact if wrong:** +/-20-30% on total estimate. The 80-hour allocation is the largest single deliverable in the decomposition, reflecting the multi-scope consolidated nature. If coordination overhead is underestimated, hours could increase; if disciplines have strong templates, hours could decrease.

**Mitigation:** Track actual hours on comparable proposals to calibrate future estimates.

---

### ASM-0202-003: No Rework or Iteration Allowance

**Assumption:** The 80 hours include a single production cycle with coordination. No explicit rework or iteration allowance is included.

**Source:** Level_of_Effort.csv notes do not mention iteration cycles. The PM coordination hours (6 hours) are assumed to cover normal coordination but not major rework.

**Impact if wrong:** If significant rework is required (e.g., concept design changes after design brief is drafted), additional hours would be needed. The dependency on DEL-02-01 (concept design) means changes to concept could trigger rework.

**Mitigation:** Monitor DEL-02-01 concept stability before committing design brief narrative production.

---

### ASM-0202-004: All Disciplines Contribute Concurrently

**Assumption:** The 8 roles can contribute their inputs within the same proposal preparation window (PP-04: 6 weeks per Assumed_Project_Parameters.csv) without schedule conflicts.

**Source:** Assumed_Project_Parameters.csv PP-04 (6-week proposal preparation duration). Level_of_Effort.csv allocates hours per role but does not specify scheduling.

**Impact if wrong:** If discipline leads are unavailable during the proposal window, the narrative production could be delayed or require substitution at different rates.

**Mitigation:** Confirm key personnel availability before proposal production begins.
