# Decision Log — EST_DEL-019-02_2026-02-27_0630

## Decisions Applied During This Run

### DEC-001: LOE hours interpreted as total project hours
- **Context:** Level_of_Effort.csv provides a single set of hours per role for DEL-019-02 without a frequency column. DEL-019-02 is a recurring weekly deliverable spanning the full project duration.
- **Decision:** Hours are taken as total project hours (not per-occurrence) since the CSV schema does not include a frequency multiplier and other deliverables in the file appear to use the same convention.
- **Impact:** If the hours were intended as per-occurrence values, the estimate would be understated by a factor of approximately 39x (weeks of project duration).
- **Reversibility:** Fully reversible — rerun with corrected LOE if interpretation is wrong.

### DEC-002: Phase A and Phase D effort not separately priced
- **Context:** The Procedure document defines Phase A (initialization), Phase B/C (ongoing operations), and Phase D (closeout) as distinct work phases. The LOE source provides only role-level totals without phase breakdown.
- **Decision:** Informational line items (ITM-019-02-007, ITM-019-02-008) created with $0 amounts, noting that effort is included in the role-hour totals. This preserves traceability to the Procedure without inventing a phase allocation.
- **Impact:** No cost impact (effort is captured in L-019-02-001 through L-019-02-006). Phase-level cost visibility is not available.

### DEC-003: CBS categories assigned as LABOUR-MGMT and LABOUR-CONST
- **Context:** No CBS mapping was provided in the brief or pricing sources. DEL-019-02 is a management deliverable with both management and construction field roles.
- **Decision:** Assigned LABOUR-MGMT to management/admin roles (PM, Cost Estimator, QA/QC Lead, and informational items) and LABOUR-CONST to field/construction roles (Construction PM, Site Superintendent, HSE Manager), based on the Category column in Professional_Staff_Rates.csv.
- **Impact:** CBS rollup reflects the management vs. construction split in the rate table. If the project uses different CBS codes, the matrix would need remapping.

### DEC-004: Fees_Permits_Insurance.csv not applied to DEL-019-02
- **Context:** Fees_Permits_Insurance.csv contains 5 items (bonding, insurance, permits) that are project-level commercial costs.
- **Decision:** None of these items are attributable to DEL-019-02 (they belong to PKG-021). No line items generated from this source.
- **Impact:** None for this deliverable.

### DEC-005: FALLBACK_POLICY not invoked
- **Context:** FALLBACK_POLICY is ALLOW_PARAMETRIC. All items had matching PARAMETRIC evidence from Level_of_Effort.csv and Professional_Staff_Rates.csv.
- **Decision:** No fallback pricing was required. All line items priced using primary PARAMETRIC method.
- **Impact:** None.

### DEC-006: UPDATE_LATEST_POINTER = FALSE respected
- **Context:** Brief specifies UPDATE_LATEST_POINTER = FALSE.
- **Decision:** No pointer file (_LATEST.md) was created or modified.
- **Impact:** None.
