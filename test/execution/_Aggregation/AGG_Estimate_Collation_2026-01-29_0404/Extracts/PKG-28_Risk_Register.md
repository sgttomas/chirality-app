# Risk Register — PKG-28 Design Verification Estimate

**Snapshot ID:** EST_PKG28_DRAFT_2026-01-29_0830
**Package Scope:** PKG-28 Design Verification
**Date:** 2026-01-29

---

## Risk Summary

This register identifies key risks to the PKG-28 estimate accuracy and cost outcomes. Risks are categorized by driver type: scope, quantity, price, productivity, schedule, and interface.

**Contingency Method:** PCT_BY_BUCKET (percentage by CBS bucket with allowance-heavy adjustment)

**Total Contingency Allocated:** $164,000 CAD (22.5% of base)

---

## R-001: IDV Scope Uncertainty — Disciplines and Review Depth

**Risk Driver:** Scope

**Cause → Consequence:**
- **Cause:** IDV requirements not explicitly defined in decomposition; assumes 8 disciplines x 4 stages based on typical practice
- **Consequence:** Actual IDV scope could be significantly larger (more disciplines, deeper reviews, additional iterations) or smaller (fewer disciplines, lighter reviews)

**Affected Buckets:** Engineering (E)

**Affected WBS:** DEL-28.01 (IDV Reports)

**Probability:** HIGH (IDV scope definition expected during design kickoff)

**Impact:** HIGH ($250k - $500k range on $350k allowance = ±43% swing)

**Suggested Mitigation:**
1. Clarify IDV requirements with Employer early in design phase
2. Determine which disciplines require third-party vs. internal independent review
3. Define review depth expectations (calculation check, design review, full independent analysis)
4. Establish iteration expectations (first-pass approval vs. multiple rounds)

**Contingency Handling:** E bucket contingency (20%) provides buffer for moderate scope growth, but large scope expansion would require estimate revision.

---

## R-002: VFPA IP Review Iteration and Complexity

**Risk Driver:** Interface + Scope

**Cause → Consequence:**
- **Cause:** VFPA project review requirements not detailed; assumes 4-6 submission cycles based on typical port authority practice
- **Consequence:** VFPA review could require more iterations, more detailed responses, or longer review cycles than assumed

**Affected Buckets:** Engineering (E), Project Management (PM)

**Affected WBS:** DEL-28.02 (VFPA IP Review Responses)

**Probability:** MED-HIGH (VFPA reviews are inherently iterative)

**Impact:** MED ($60k - $140k range on $95k technical + $42k coordination = ±45% swing)

**Suggested Mitigation:**
1. Engage VFPA early to understand project review process and expectations
2. Review VFPA project permit requirements for similar projects
3. Establish clear submission schedule aligned with design milestones
4. Build early relationship with VFPA project reviewers

**Contingency Handling:** E and PM contingency (20% each) provides buffer for moderate iteration increase.

---

## R-003: Design Coordination Complexity — 210 Deliverables

**Risk Driver:** Scope + Productivity

**Cause → Consequence:**
- **Cause:** Project has 36 packages and 210 deliverables requiring inter-discipline coordination; assumes typical coordination effort per deliverable
- **Consequence:** Coordination complexity could be higher than typical due to project scale, marine/rail/process interfaces, or multi-phase construction

**Affected Buckets:** Project Management (PM)

**Affected WBS:** DEL-28.03 (Design Coordination Records)

**Probability:** MED (project scale is known; complexity is inherent)

**Impact:** MED ($100k - $200k range on $150k allowance = ±33% swing)

**Suggested Mitigation:**
1. Establish robust design coordination process early
2. Define coordination meeting cadence and participants
3. Implement BIM coordination tools and workflows
4. Assign dedicated coordination resources for complex interfaces (marine/rail, process/controls)

**Contingency Handling:** PM contingency (20%) provides buffer for moderate complexity increase.

---

## R-004: Lack of Project-Specific Pricing Sources

**Risk Driver:** Price

**Cause → Consequence:**
- **Cause:** No vendor quotes or rate tables available for design verification services at time of estimate
- **Consequence:** All line items rely on fallback allowances with wide uncertainty ranges

**Affected Buckets:** All CBS buckets (E, PM, P, CI)

**Affected WBS:** All PKG-28 deliverables

**Probability:** HIGH (100% of direct line items affected)

**Impact:** HIGH ($485k - $905k range on $664k allowance base = ±32% swing)

**Suggested Mitigation:**
1. Obtain budgetary quotes from independent design verification service providers
2. Develop engineering labor rate tables for in-house coordination effort
3. Clarify VFPA coordination cost basis from similar projects
4. Re-run estimate with improved pricing sources

**Contingency Handling:** Elevated contingency percentages (15-25% by bucket) applied to account for pricing uncertainty.

---

## R-005: Design Duration Extension

**Risk Driver:** Schedule

**Cause → Consequence:**
- **Cause:** Design duration assumed at 18-24 months; actual duration could extend due to design complexity, approval delays, or scope changes
- **Consequence:** Time-based coordination costs (A-002, A-004, A-005, A-006) would increase proportionally with extended duration

**Affected Buckets:** Project Management (PM)

**Affected WBS:** DEL-28.03 (Design Coordination Records), DEL-28.02 (VFPA Coordination)

**Probability:** MED (design extensions are common for design-build projects)

**Impact:** MED (±20% duration variance = $25k - $40k PM cost impact)

**Suggested Mitigation:**
1. Establish realistic design schedule with appropriate float
2. Monitor design progress against milestones
3. Identify early warning indicators for schedule extension
4. Build schedule contingency into coordination staffing plan

**Contingency Handling:** PM contingency (20%) provides buffer for moderate schedule extensions.

---

## R-006: IDV Provider Availability and Pricing

**Risk Driver:** Price + Interface

**Cause → Consequence:**
- **Cause:** IDV services typically provided by third-party engineering firms; availability and pricing depend on market conditions
- **Consequence:** IDV provider costs could be higher than assumed if market is tight or specialized expertise is required

**Affected Buckets:** Engineering (E)

**Affected WBS:** DEL-28.01 (IDV Reports)

**Probability:** MED (specialized IDV providers may have limited availability)

**Impact:** MED (IDV rates could vary ±20-30% from assumptions)

**Suggested Mitigation:**
1. Identify qualified IDV providers early and assess availability
2. Obtain budgetary quotes from multiple providers
3. Consider using internal independent review where allowed
4. Plan IDV procurement with adequate lead time

**Contingency Handling:** E contingency (20%) provides buffer for moderate price variance.

---

## R-007: Clash Detection Model Complexity

**Risk Driver:** Scope + Productivity

**Cause → Consequence:**
- **Cause:** BIM model complexity and clash detection requirements not defined; assumes typical industrial facility
- **Consequence:** Complex marine/process interfaces and multi-disciplinary systems could generate higher clash volumes and resolution effort

**Affected Buckets:** Project Management (PM)

**Affected WBS:** DEL-28.03 (Design Coordination Records — clash detection component)

**Probability:** MED-HIGH (marine/rail/process interfaces are inherently complex)

**Impact:** LOW-MED ($30k - $65k range on $45k clash detection allowance = ±44% swing, but small relative to total)

**Suggested Mitigation:**
1. Define BIM coordination requirements and LOD (Level of Development) expectations
2. Establish clash detection frequency and prioritization rules
3. Assign dedicated BIM coordinator for complex interfaces
4. Implement clash resolution tracking and closeout process

**Contingency Handling:** PM contingency (20%) provides buffer; clash detection is relatively small cost item.

---

## R-008: Escalation Exposure — Labor Rate Increases

**Risk Driver:** Price

**Cause → Consequence:**
- **Cause:** Estimate uses January 2026 pricing; no escalation applied; design verification is primarily labor-based
- **Consequence:** Engineering labor rate escalation over 18-24 month design period could add 2-4% annually to costs

**Affected Buckets:** All buckets (primarily E, PM)

**Affected WBS:** All deliverables

**Probability:** HIGH (labor escalation is typical over multi-year periods)

**Impact:** LOW-MED (2-4% annual escalation x 1.5-2 years = 3-8% = $22k - $58k on $728k base)

**Suggested Mitigation:**
1. Update estimate periodically to current pricing
2. Consider enabling escalation in future estimates
3. Monitor engineering labor market conditions
4. Consider fixed-price IDV contracts where feasible

**Contingency Handling:** Contingency ($164k = 22.5%) provides buffer for moderate escalation, but is not a substitute for formal escalation calculation.

---

## Risk Summary Table

| Risk ID | Risk Driver | Probability | Impact | Affected CBS | Mitigation Priority | Contingency Coverage |
|---------|-------------|-------------|--------|--------------|---------------------|----------------------|
| R-001 | Scope | HIGH | HIGH | E | HIGH | Partial |
| R-002 | Interface + Scope | MED-HIGH | MED | E, PM | HIGH | Adequate |
| R-003 | Scope + Productivity | MED | MED | PM | MED | Adequate |
| R-004 | Price | HIGH | HIGH | All | HIGH | Partial |
| R-005 | Schedule | MED | MED | PM | MED | Adequate |
| R-006 | Price + Interface | MED | MED | E | MED | Adequate |
| R-007 | Scope + Productivity | MED-HIGH | LOW-MED | PM | LOW | Adequate |
| R-008 | Price | HIGH | LOW-MED | All | LOW | Adequate |

---

## Contingency Adequacy Assessment

**Total Contingency:** $164,000 CAD (22.5% of base)

**Risk Exposure:**
- **HIGH risks (R-001, R-004):** Address IDV scope uncertainty and pricing uncertainty; cumulative impact could be +30-50% on affected buckets
- **MED risks (R-002, R-003, R-005, R-006):** Address VFPA iteration, coordination complexity, schedule extension, IDV provider pricing; cumulative impact ~10-25%

**Assessment:**
- Contingency is **ADEQUATE** for normal project risks and moderate scope/pricing adjustments
- Contingency is **INSUFFICIENT** if IDV scope is significantly larger than assumed or multiple high-impact risks materialize
- Estimate maturity is **Draft/Conceptual** — expect refinement as IDV scope and VFPA requirements are clarified

**Recommendation:** Update estimate as soon as IDV requirements and VFPA coordination expectations are defined to reduce uncertainty and refine contingency allocation.

---

**Risk Register Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Status:** Complete
