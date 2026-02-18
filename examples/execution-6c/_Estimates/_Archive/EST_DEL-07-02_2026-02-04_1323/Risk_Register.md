# Risk Register: DEL-07-02 Key Team Members and Resumes

**Snapshot ID:** EST_DEL-07-02_2026-02-04_1323

---

## Risk Summary

| Risk ID | Risk Driver | Likelihood | Impact | Contingency Handling |
|---------|-------------|------------|--------|---------------------|
| R-001 | Scope (team size) | MEDIUM | MEDIUM | Included in 20% contingency |
| R-002 | Productivity (content gathering) | HIGH | MEDIUM | Included in 20% contingency |
| R-003 | Price (labor rates) | MEDIUM | LOW | Included in 20% contingency |
| R-004 | Interface (cross-deliverable) | LOW | LOW | Included in 20% contingency |
| R-005 | Schedule (personnel availability) | MEDIUM | MEDIUM | Not costed; schedule risk |

---

## Detailed Risk Register

### R-001: Team Size Uncertainty
**Risk Driver:** Scope/Quantity

**Cause:** Number of key team members is TBD (Datasheet.md Section 2.5 notes B-003: "Planned Team Size: TBD")

**Consequence:** Labor hours for resume preparation could be +/- 30% from estimate
- Low case: 9 members = ~20% less effort
- High case: 13 members = ~30% more effort

**Affected Buckets:**
- CBS: E (Engineering & Design)
- WBS: DEL-07-02 (L-002 through L-007)

**Suggested Mitigation:**
1. Finalize key team member count before detailed scheduling
2. Identify "probable" vs. "possible" additional roles
3. Prioritize core 9 roles; add others only if capacity permits

**Contingency Handling:** Quantitative - ~CAD 500-800 of contingency allocated to team size risk

---

### R-002: Content Gathering Variability
**Risk Driver:** Productivity

**Cause:** Resume content gathering depends on individual personnel responsiveness (Procedure.md Step 3; Assumption A-008 notes LOW confidence)

**Consequence:**
- Best case: Personnel provide complete, high-quality content promptly = 50% less coordination effort
- Worst case: Multiple follow-ups, incomplete content, rewriting required = 100% more effort

**Affected Buckets:**
- CBS: E (Engineering & Design)
- WBS: DEL-07-02 (L-003, L-004)

**Suggested Mitigation:**
1. Start content gathering early in proposal timeline
2. Provide clear templates and examples to personnel
3. Set firm deadlines with management escalation path
4. Have backup personnel identified for critical roles

**Contingency Handling:** Quantitative - ~CAD 400-600 of contingency allocated to productivity risk

---

### R-003: Labor Rate Uncertainty
**Risk Driver:** Price

**Cause:** No rate tables provided; labor rates are assumptions (A-016)

**Consequence:**
- Actual firm rates may be +/- 20% from assumed rates
- Higher rates for senior staff could increase costs by ~CAD 500-1,000

**Affected Buckets:**
- CBS: E, PM
- WBS: DEL-07-02 (all labor lines)

**Suggested Mitigation:**
1. Provide firm-specific rate tables for future estimates
2. Confirm rates with finance/HR before finalizing budgets

**Contingency Handling:** Quantitative - ~CAD 200-400 of contingency allocated to rate risk

---

### R-004: Cross-Deliverable Coordination Risk
**Risk Driver:** Interface

**Cause:** DEL-07-02 must coordinate with DEL-07-01, DEL-07-03, DEL-08-01 (Procedure.md Step 6)

**Consequence:**
- If related deliverables are incomplete or inconsistent, additional rework effort required
- Potential delays if dependencies are not managed

**Affected Buckets:**
- CBS: E (Engineering & Design)
- WBS: DEL-07-02 (L-006)

**Suggested Mitigation:**
1. Establish shared project reference naming convention (B-007 in Specification.md)
2. Coordinate deliverable production schedules within PKG-03
3. Conduct iterative cross-checks rather than single final check

**Contingency Handling:** Qualitative - minor additional effort already in cross-check hours

---

### R-005: Personnel Availability for Input
**Risk Driver:** Schedule

**Cause:** Key personnel must be available to provide resume content and review drafts

**Consequence:**
- If personnel are unavailable (travel, other projects), schedule delays may occur
- Not a cost risk directly, but may compress production timeline

**Affected Buckets:**
- CBS: Not directly costed
- WBS: DEL-07-02 timeline

**Suggested Mitigation:**
1. Identify backup content providers for each role
2. Start personnel outreach early
3. Escalate through management if personnel unresponsive

**Contingency Handling:** Schedule contingency, not cost contingency - flag for project schedule

---

## Contingency Calculation

**Method:** PCT_BY_BUCKET (Decision D-004)

| Risk Category | Base Cost Exposed | Risk Factor | Contingency Allocated |
|--------------|-------------------|-------------|----------------------|
| Scope (R-001) | CAD 4,800 | 15% | CAD 720 |
| Productivity (R-002) | CAD 4,600 | 12% | CAD 552 |
| Price (R-003) | CAD 9,000 | 5% | CAD 450 |
| Interface (R-004) | CAD 600 | 10% | CAD 60 |
| **Total Risk-Based** | | | **CAD 1,782** |
| **Applied (rounded)** | | | **CAD 1,805** |

**Total Contingency:** CAD 1,805 (20% of base estimate, reconciles with risk-based calculation)

---

**End of Risk Register**
