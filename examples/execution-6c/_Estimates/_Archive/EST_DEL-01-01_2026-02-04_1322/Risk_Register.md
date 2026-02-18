# Risk Register
## DEL-01-01: ComplianceMatrixAndChecklist Estimate

---

## Purpose

This register documents cost risks that inform the contingency calculation and identifies actions that could reduce estimate uncertainty.

---

## Risk Register

### R-001: Effort Estimation Uncertainty

| Property | Value |
|----------|-------|
| **Risk ID** | R-001 |
| **Risk Driver** | Scope/Qty |
| **Cause** | Parametric estimation without historical data |
| **Consequence** | Actual effort may differ significantly from estimate |
| **Affected CBS** | E, PM |
| **Affected WBS** | DEL-01-01 |
| **Probability** | MEDIUM |
| **Impact** | MEDIUM |
| **Suggested Mitigation** | Track actual hours; calibrate future estimates |
| **Contingency Handling** | Included in 15% contingency |

---

### R-002: RFP Interpretation Complexity

| Property | Value |
|----------|-------|
| **Risk ID** | R-002 |
| **Risk Driver** | Scope |
| **Cause** | RFP requirements may require more interpretation than assumed |
| **Consequence** | Additional effort for clarification, cross-referencing |
| **Affected CBS** | E |
| **Affected WBS** | DEL-01-01 |
| **Probability** | MEDIUM |
| **Impact** | LOW |
| **Suggested Mitigation** | Early start on extraction; leverage Decomposition document |
| **Contingency Handling** | Included in 15% contingency |

---

### R-003: Addenda Integration Scope Growth

| Property | Value |
|----------|-------|
| **Risk ID** | R-003 |
| **Risk Driver** | Scope |
| **Cause** | Addendum 03 has 21 items with cross-deliverable impacts |
| **Consequence** | Integration tracking more complex than estimated |
| **Affected CBS** | E |
| **Affected WBS** | DEL-01-01 |
| **Probability** | LOW |
| **Impact** | LOW |
| **Suggested Mitigation** | Structured checklist approach per Procedure.md |
| **Contingency Handling** | Included in 15% contingency |

---

### R-004: Cross-Deliverable Coordination Delays

| Property | Value |
|----------|-------|
| **Risk ID** | R-004 |
| **Risk Driver** | Interface |
| **Cause** | Compliance matrix depends on input from 9 package leads |
| **Consequence** | Delays in getting deliverable mappings confirmed |
| **Affected CBS** | E, PM |
| **Affected WBS** | DEL-01-01 |
| **Probability** | MEDIUM |
| **Impact** | MEDIUM |
| **Suggested Mitigation** | Early kickoff meeting; clear owner assignments |
| **Contingency Handling** | Schedule risk; cost contingency minimal |

---

### R-005: Rework Cycles

| Property | Value |
|----------|-------|
| **Risk ID** | R-005 |
| **Risk Driver** | Productivity |
| **Cause** | Changes to proposal structure or deliverable scope |
| **Consequence** | Compliance matrix requires significant updates |
| **Affected CBS** | E |
| **Affected WBS** | DEL-01-01 |
| **Probability** | MEDIUM |
| **Impact** | MEDIUM |
| **Suggested Mitigation** | Maintain as living document; regular sync with proposal team |
| **Contingency Handling** | Included in 15% contingency; A-010 includes maintenance |

---

### R-006: Labour Rate Variance

| Property | Value |
|----------|-------|
| **Risk ID** | R-006 |
| **Risk Driver** | Price |
| **Cause** | Assumed rates may not match actual project rates |
| **Consequence** | Cost over/underrun if rates differ |
| **Affected CBS** | E, PM |
| **Affected WBS** | DEL-01-01 |
| **Probability** | LOW |
| **Impact** | MEDIUM |
| **Suggested Mitigation** | Provide rate tables in _RateTables/ folder |
| **Contingency Handling** | Included in 15% contingency |

---

## Risk Matrix Summary

| Risk ID | Probability | Impact | Risk Level | In Contingency? |
|---------|-------------|--------|------------|-----------------|
| R-001 | MEDIUM | MEDIUM | MEDIUM | YES |
| R-002 | MEDIUM | LOW | LOW | YES |
| R-003 | LOW | LOW | LOW | YES |
| R-004 | MEDIUM | MEDIUM | MEDIUM | PARTIAL |
| R-005 | MEDIUM | MEDIUM | MEDIUM | YES |
| R-006 | LOW | MEDIUM | LOW | YES |

---

## Contingency Calculation

### Method: PCT_BY_BUCKET

| CBS Category | Base Amount | Risk Profile | Contingency % | Contingency Amount |
|--------------|-------------|--------------|---------------|-------------------|
| Engineering (E) | $5,600 | MEDIUM (all allowance-based) | 15% | $840 |
| Project Management (PM) | $1,650 | MEDIUM (all allowance-based) | 15% | $248 |
| **TOTAL** | **$7,250** | | **15%** | **$1,088 (rounded to $1,100)** |

### Contingency Rationale

The 15% contingency is justified by:

1. **Pricing Method Risk** - 100% of estimate is by allowance (no quotes or rate tables)
2. **Effort Estimation Risk** - Parametric approach without historical calibration
3. **Living Document Risk** - Maintenance effort difficult to predict
4. **Coordination Risk** - Cross-deliverable dependencies introduce variability

A 15% contingency is appropriate for a Class 4/5 estimate with moderate uncertainty.

---

## Contingency Adequacy Assessment

| Factor | Assessment |
|--------|------------|
| **Estimate Maturity** | Class 4/5 (Conceptual/Study) |
| **Typical Contingency Range** | 15-30% |
| **Applied Contingency** | 15% |
| **Assessment** | At lower end of range; appropriate for professional services with defined scope |

---

## Risk Mitigation Actions (Human)

| Action ID | Risk | Mitigation Action | Owner | Status |
|-----------|------|-------------------|-------|--------|
| MIT-001 | R-001 | Track actual hours during execution | Proposal Manager | OPEN |
| MIT-002 | R-004 | Schedule kickoff meeting with package leads | Proposal Manager | OPEN |
| MIT-003 | R-006 | Provide rate tables for future estimates | Project Controls | OPEN |

---

## Document Control

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-01-01_2026-02-04_1322 |
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
