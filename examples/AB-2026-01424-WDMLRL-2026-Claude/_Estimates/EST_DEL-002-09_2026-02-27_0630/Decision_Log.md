# Decision Log — EST_DEL-002-09_2026-02-27_0630

## Decisions Made During This Run

### DEC-001 — Pricing Method Selection

**Decision:** Use Level-of-Effort (LOE) parametric method with hourly rates rather than percentage-of-construction-value design fee method.

**Rationale:** The LOE model (Level_of_Effort.csv) provides role-specific hours for DEL-002-09, and the rate table (Professional_Staff_Rates.csv) provides matching hourly rates. This granularity is superior to the Professional_Design_Fees.csv percentage method for a single-deliverable estimate because:
- It prices at the role level, allowing verification of effort distribution.
- It avoids the need to determine total construction value (which is TBD).
- It aligns directly with the PARAMETRIC basis of estimate.

The design fee benchmark (DF-02) is retained as a cross-check in Summary.md.

### DEC-002 — Activity Line Items as Sub-Components

**Decision:** ITM-005 through ITM-016 (procedure step activities) are extracted in Items.csv for takeoff completeness but are not separately priced in Detail.csv. Their costs are fully captured within the four labour line items (ITM-001 through ITM-004).

**Rationale:** The LOE model provides aggregate hours per role per deliverable, not per activity within a deliverable. Attempting to allocate hours across 12 sub-activities would require assumptions beyond the available data and would not change the total. The Items.csv preserves the activity-level detail for scope verification without double-counting.

### DEC-003 — CBS Category Assignment

**Decision:** Assigned two CBS categories:
- "Professional Services — Management" for R-01 (PM) and R-08 (Cost Estimator)
- "Professional Services — Design" for R-13 (BIM Technician) and R-14 (Structural Engineer)

**Rationale:** Based on the Category column in Professional_Staff_Rates.csv: R-01 and R-08 are categorized as "Management"; R-13 and R-14 are categorized as "Design". This mapping provides a meaningful cost breakdown without inventing categories.

### DEC-004 — Scope Boundary

**Decision:** This estimate covers professional design services only (drawing set production). Construction costs for stair fabrication and installation are excluded (PKG-011 scope).

**Rationale:** DEL-002-09 is a Drawing Set deliverable within PKG-002 (Structural Design). The Specification explicitly places construction execution in PKG-011 (Out of Scope). The LOE model and rate table provide design service costs only.

### DEC-005 — No Overhead or Disbursement Markup

**Decision:** Estimate reflects direct labour cost only at parametric hourly rates. No overhead multiplier, profit margin, or disbursement allowance is applied.

**Rationale:** No overhead or disbursement rates were provided in PRICE_SOURCES. Per non-negotiable invariant "No invention," the agent does not fabricate markup factors.

### DEC-006 — FALLBACK_POLICY Not Invoked

**Decision:** FALLBACK_POLICY (ALLOW_PARAMETRIC) was not required because all items were directly priced from the parametric sources.

**Rationale:** The Level_of_Effort.csv and Professional_Staff_Rates.csv together provided complete coverage for all priced line items. No fallback was needed.
