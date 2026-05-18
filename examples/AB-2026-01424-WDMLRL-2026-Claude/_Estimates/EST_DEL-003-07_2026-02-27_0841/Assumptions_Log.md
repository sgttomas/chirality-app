# Assumptions Log — EST_DEL-003-07_2026-02-27_0841

## Assumptions Applied During This Run

| AssumptionID | Assumption | Source / Basis | Impact | Risk if Wrong |
|---|---|---|---|---|
| ASM-001 | Staff hourly rates from Professional_Staff_Rates.csv are valid for 2026 pricing | Rates are marked PARAMETRIC / MEDIUM confidence in source file; PP-18 confirms base year = 2026 | Rates applied directly to LOE hours | If actual negotiated rates differ, total could change proportionally; Mechanical Engineer rate ($165/hr) has highest sensitivity at 42 hours |
| ASM-002 | Level-of-effort hours for DEL-003-07 (70 total: 6+4+18+42) are reasonable for a mechanical specification deliverable for a ~13,000 sq ft industrial shop | Hours are marked PARAMETRIC / MEDIUM confidence in Level_of_Effort.csv | Total is computed as $10,170 based on these hours | If specification scope is more complex than assumed (e.g., additional systems, code complications), hours could increase |
| ASM-003 | This estimate covers professional design services (specification authoring) only; no material, equipment, or construction costs are included | DEL-003-07 is a Specification deliverable under PKG-003 (Mechanical Design); physical installation is PKG-013 | Estimate scope is limited to staff time | No risk; scope boundary is clear per decomposition |
| ASM-004 | Currency is CAD per run brief and PP-17 (Assumed_Project_Parameters.csv) | Alberta, Canada context; all rate tables denominated in CAD | All amounts in CAD | Low risk; project is in Alberta |
| ASM-005 | No escalation or contingency is applied to the parametric estimate | Run brief does not specify escalation or contingency; PARAMETRIC basis represents a point estimate | Total is a base cost without contingency | If contingency is required for proposal pricing, it must be added separately |
