# Risk Register
## DEL-03-02: DetailedDesignAndConstructionDocsPlan
## Snapshot: EST_DEL-03-02_2026-02-04_1323

---

## Risk Summary

| Metric | Value |
|--------|-------|
| **Total Risks Identified** | 6 |
| **High Impact** | 1 |
| **Medium Impact** | 4 |
| **Low Impact** | 1 |
| **Contingency Method** | PCT_BY_BUCKET |
| **Contingency Amount** | CAD $1,100 (15% of base) |

---

## R-001: Rate Assumption Variance

| Property | Value |
|----------|-------|
| **Risk ID** | R-001 |
| **Risk Driver** | PRICE |
| **Cause** | Professional rates assumed without project-specific rate tables |
| **Consequence** | Actual costs may vary +/- 25% from assumed rates |
| **Affected CBS/WBS** | All E and PM line items |
| **Probability** | MEDIUM |
| **Impact** | MEDIUM |
| **Suggested Mitigation** | Obtain actual project rate schedules; update _RateTables/ folder |
| **Contingency Handling** | Partially covered by 15% contingency |

---

## R-002: Effort Estimation Uncertainty

| Property | Value |
|----------|-------|
| **Risk ID** | R-002 |
| **Risk Driver** | QTY |
| **Cause** | Effort hours estimated parametrically without detailed task breakdown |
| **Consequence** | Actual effort may exceed or fall short of estimates |
| **Affected CBS/WBS** | All line items in E and PM |
| **Probability** | MEDIUM |
| **Impact** | MEDIUM |
| **Suggested Mitigation** | Track actual effort on this and similar deliverables; refine estimates for future runs |
| **Contingency Handling** | Partially covered by 15% contingency |

---

## R-003: TBD Item Scope Changes

| Property | Value |
|----------|-------|
| **Risk ID** | R-003 |
| **Risk Driver** | SCOPE |
| **Cause** | Multiple TBD items in source documents (landscape scope, third-party code review, RFP Section 7.1.8 specifics) |
| **Consequence** | Scope may expand or contract when TBD items are resolved |
| **Affected CBS/WBS** | L001 (Discipline Matrix), L006 (Code Compliance) |
| **Probability** | MEDIUM |
| **Impact** | LOW |
| **Suggested Mitigation** | Resolve TBD items through human ruling; update estimate when resolved |
| **Contingency Handling** | Minor scope changes covered by 15% contingency |

---

## R-004: Cross-Deliverable Coordination Complexity

| Property | Value |
|----------|-------|
| **Risk ID** | R-004 |
| **Risk Driver** | INTERFACE |
| **Cause** | DEL-03-02 requires coordination with DEL-03-01, DEL-08-01, DEL-09-01 |
| **Consequence** | Iteration cycles may increase effort if related deliverables change |
| **Affected CBS/WBS** | L008 (Schedule Alignment), L012 (DM Review) |
| **Probability** | LOW |
| **Impact** | MEDIUM |
| **Suggested Mitigation** | Establish coordination protocols; freeze related deliverables before final review |
| **Contingency Handling** | Partially covered by 15% contingency |

---

## R-005: RFP Section 7.1.8 Requirements Gap

| Property | Value |
|----------|-------|
| **Risk ID** | R-005 |
| **Risk Driver** | SCOPE |
| **Cause** | RFP Section 7.1.8 specific requirements not directly accessible; requirements inferred from decomposition |
| **Consequence** | Plan may not fully address all RFP requirements; rework may be needed |
| **Affected CBS/WBS** | All proposal phase line items |
| **Probability** | MEDIUM |
| **Impact** | HIGH |
| **Suggested Mitigation** | Obtain and review actual RFP Section 7.1.8 text; validate plan against specific requirements |
| **Contingency Handling** | Major rework risk partially covered by 15% contingency |

---

## R-006: Post-Award Execution Exclusion

| Property | Value |
|----------|-------|
| **Risk ID** | R-006 |
| **Risk Driver** | SCOPE |
| **Cause** | Estimate explicitly excludes post-award design execution costs |
| **Consequence** | Total project design cost significantly higher than this estimate |
| **Affected CBS/WBS** | Entire estimate scope |
| **Probability** | HIGH (certainty) |
| **Impact** | LOW (for this estimate - understood exclusion) |
| **Suggested Mitigation** | Create separate estimate for post-award design execution if required |
| **Contingency Handling** | Not applicable - acknowledged scope exclusion |

---

## Contingency Calculation

### Method: PCT_BY_BUCKET

| CBS | Base Amount | Contingency % | Contingency Amount |
|-----|-------------|---------------|-------------------|
| E | $6,250 | 15% | $938 |
| PM | $1,000 | 15% | $150 |
| **Total** | **$7,250** | **15%** | **$1,088** |

**Rounded Contingency:** CAD $1,100

### Contingency Rationale

15% contingency applied based on:
1. **Rate uncertainty (R-001):** Allowance-based rates without project-specific validation
2. **Effort uncertainty (R-002):** Parametric estimates without detailed task breakdowns
3. **TBD scope items (R-003):** Multiple unresolved items in source documents
4. **RFP requirements gap (R-005):** Specific RFP Section 7.1.8 requirements not directly verified

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
| **Snapshot** | EST_DEL-03-02_2026-02-04_1323 |
