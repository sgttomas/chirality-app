# Risk Register — PKG-00 Site Establishment Estimate

**Snapshot ID:** EST_PKG00_DRAFT_2026-01-28_2315
**Package Scope:** PKG-00 Site Establishment
**Date:** 2026-01-28

---

## Risk Summary

This register identifies key risks to the PKG-00 estimate accuracy and cost outcomes. Risks are categorized by driver type: scope, quantity, price, productivity, schedule, and interface.

**Contingency Method:** PCT_BY_BUCKET (percentage by CBS bucket with allowance-heavy adjustment)

**Total Contingency Allocated:** $293,020 CAD (20.4% of base)

---

## R-001: Lack of Project-Specific Pricing Sources

**Risk Driver:** Price

**Cause → Consequence:**
- **Cause:** No vendor quotes, budgetary proposals, or project rate tables available at time of estimate
- **Consequence:** All line items rely on fallback allowances with wide uncertainty ranges (±30% to ±100%)

**Affected Buckets:** All CBS buckets (E, PM, P, MAT, CD, CI)

**Affected WBS:** All PKG-00 deliverables (DEL-00.01 through DEL-00.08)

**Probability:** HIGH (100% of line items affected)

**Impact:** HIGH ($867k - $1,772k range on $1.26M allowance base = ±39% swing)

**Suggested Mitigation:**
1. Obtain budgetary vendor quotes for major cost drivers:
   - Modular office trailer rentals (multi-year)
   - Security fencing and gates installation
   - Temporary electrical and water utilities
   - Security gate staffing services
2. Develop project-specific rate tables for engineering and construction labor
3. Re-run estimate with improved pricing sources

**Contingency Handling:** Elevated contingency percentages applied (15-25% by bucket) to account for pricing uncertainty. Allowance share >80% in E, MAT, CD buckets triggers additional contingency per D-008.

---

## R-002: Missing Physical Quantities (Site Facilities & Infrastructure)

**Risk Driver:** Quantity + Scope

**Cause → Consequence:**
- **Cause:** Employer's Requirements not yet available; deliverable documents mark physical quantities as "TBD" (office count, laydown area size, fencing length, utility capacities)
- **Consequence:** A-012 allowance ($850k, 59% of base) is a high-level placeholder without detailed quantity takeoff; actual costs could vary significantly based on ER requirements

**Affected Buckets:** MAT, CD

**Affected WBS:** DEL-00.01, DEL-00.02 (site layout and specifications drive facility sizing)

**Probability:** HIGH (scope refinement expected once ER available)

**Impact:** HIGH ($600k - $1.2M range on $850k allowance = ±41% swing)

**Suggested Mitigation:**
1. Obtain Employer's Requirements (Volume 2 Part 1) to extract specific site establishment criteria:
   - Number and size of office trailers required
   - Laydown area dimensions and surfacing requirements
   - Security fencing linear footage and gate count
   - Temporary utility capacities and service sizes
2. Develop preliminary site layout (DEL-00.01) to quantify areas and infrastructure
3. Break down A-012 into detailed line items by component once quantities known

**Contingency Handling:** 20-25% contingency on MAT/CD buckets provides buffer for scope growth, but large magnitude of allowance means contingency may be insufficient if scope significantly exceeds assumptions.

---

## R-003: Construction Duration and Schedule Uncertainty

**Risk Driver:** Schedule

**Cause → Consequence:**
- **Cause:** Detailed project schedule not available; duration assumptions based on "multi-year EPC project" and example equipment mobilization (52 weeks)
- **Consequence:** Time-based costs (security gate staffing, office trailer rentals, equipment rentals) have high uncertainty; actual duration could range from 18 months to 36+ months

**Affected Buckets:** CI (gate staffing), MAT (trailer rentals within A-012)

**Affected WBS:** DEL-00.04 (equipment schedule), DEL-00.05 (gate operations)

**Probability:** MED (schedule refinement expected during project planning)

**Impact:** MED ($180k gate staffing + portion of $300k trailer rental = ~$480k exposed to duration variance)

**Suggested Mitigation:**
1. Obtain construction schedule with key milestones and project duration
2. Refine time-based cost estimates (gate staffing hours, trailer rental months, equipment rental durations)
3. Consider schedule-driven scenarios (e.g., 18-month fast-track vs. 30-month base vs. 36-month extended)

**Contingency Handling:** CI contingency (25%) provides some buffer for extended duration, but major schedule overruns would require estimate revision.

---

## R-004: Terminal Operational Constraints and Interface Complexity

**Risk Driver:** Interface + Productivity

**Cause → Consequence:**
- **Cause:** Project objective OBJ-5 (Terminal Continuity) requires minimizing disruption to existing terminal commercial operations; specific operational constraints not yet detailed in deliverables
- **Consequence:** Construction productivity and sequencing may be significantly impacted by terminal traffic coordination, restricted work hours, or access limitations; costs for traffic management, scheduling complexity, and coordination could exceed allowances

**Affected Buckets:** CD, CI, PM

**Affected WBS:** DEL-00.03 (traffic management), DEL-00.05 (access control), general site works

**Probability:** MED-HIGH (operational terminal interface is inherent to project)

**Impact:** MED (productivity factors could add 10-20% to CD/CI costs = $74k - $148k)

**Suggested Mitigation:**
1. Conduct site visit and terminal operations coordination meeting to understand constraints
2. Obtain terminal operating schedule and traffic patterns
3. Develop detailed traffic management plan (DEL-00.03) early to quantify coordination impacts
4. Consider off-hours work premiums if required

**Contingency Handling:** CD/CI contingency (25%) provides buffer for productivity impacts, but severe restrictions could require allowance adjustment.

---

## R-005: Authority Approvals and Permitting Delays

**Risk Driver:** Schedule + Interface

**Cause → Consequence:**
- **Cause:** DEL-00.05 references approvals from TransLink, City of Surrey, Port Authority; approval timelines and requirements not yet defined
- **Consequence:** Delays in road access configuration approval or utility connection permits could extend schedule and increase time-based costs (gate staffing, office rentals)

**Affected Buckets:** CI, PM

**Affected WBS:** DEL-00.05 (road access approvals), DEL-00.08 (water utility connection approval)

**Probability:** MED (typical for industrial projects in BC with multiple authorities)

**Impact:** LOW-MED (schedule delay impact on time-based costs: potential +10% to CI/PM = $36k)

**Suggested Mitigation:**
1. Initiate early engagement with TransLink, City of Surrey, Port Authority
2. Include permit procurement schedule in DEL-00.04
3. Identify long-lead approvals and plan early submissions
4. Consider contingency for extended approval cycles

**Contingency Handling:** PM/CI contingency (15-25%) provides buffer for schedule extensions; escalation not applied in this estimate (could be triggered by major delays).

---

## R-006: Road Damage and Restoration Scope Uncertainty

**Risk Driver:** Scope + Quantity

**Cause → Consequence:**
- **Cause:** Pre-works road survey (DEL-00.06) not yet performed; baseline road condition unknown; construction traffic loading and damage potential uncertain
- **Consequence:** Road restoration allowance (A-008: $25k) is a placeholder; actual restoration could range from minimal patching to major resurfacing depending on baseline condition and traffic impacts

**Affected Buckets:** CD

**Affected WBS:** DEL-00.07 (post-works survey and restoration)

**Probability:** HIGH (construction traffic will cause some road damage)

**Impact:** LOW-MED ($25k allowance could range from $10k to $50k = ±100% variance, but magnitude is small relative to total)

**Suggested Mitigation:**
1. Complete pre-works road survey (DEL-00.06) early to establish baseline
2. Coordinate with Employer and authorities on acceptable condition standards
3. Implement traffic management controls to minimize road damage (load limits, routing restrictions)
4. Establish road maintenance fund or bonding requirements if needed

**Contingency Handling:** CD contingency (25%) provides buffer; road restoration is relatively small cost item in context of total estimate.

---

## R-007: Scope Creep — Site Establishment Requirements Growth

**Risk Driver:** Scope

**Cause → Consequence:**
- **Cause:** Site establishment scope defined at high level; detailed Employer requirements not yet available; actual facility counts, sizes, and standards may exceed typical assumptions
- **Consequence:** Scope growth in temporary facilities (e.g., more office trailers, larger laydown areas, upgraded utilities) could add 20-40% to physical works allowances

**Affected Buckets:** MAT, CD, CI

**Affected WBS:** DEL-00.02 (specifications may reveal higher standards than assumed), general site works

**Probability:** MED (typical for design-build projects where ER are refined during design phase)

**Impact:** MED-HIGH (20-40% growth on $1.37M physical works + indirects = $274k - $548k potential addition)

**Suggested Mitigation:**
1. Obtain Employer's Requirements early in design phase
2. Conduct value engineering review if ER requirements exceed budget
3. Establish change management process for scope additions
4. Maintain clear delineation between Contractor minimum requirements and Employer optional upgrades

**Contingency Handling:** Contingency allocation ($293k) provides buffer for moderate scope growth (21% of base), but major scope additions would require estimate revision and potential change order.

---

## R-008: Currency and Escalation Exposure

**Risk Driver:** Price

**Cause → Consequence:**
- **Cause:** Estimate uses January 2026 CAD pricing; no escalation applied (per D-009); project duration is multi-year
- **Consequence:** Cost escalation over 24-30 month construction period could add 3-6% annually to costs; CAD/USD exchange rate fluctuations could affect imported materials/equipment

**Affected Buckets:** All buckets (escalation affects all cost categories)

**Affected WBS:** All deliverables

**Probability:** HIGH (escalation is typical over multi-year projects)

**Impact:** MED (3-6% annual escalation × 2-2.5 years = 6-15% potential addition = $86k - $215k on $1.43M base)

**Suggested Mitigation:**
1. Update estimate periodically to current pricing
2. Consider enabling escalation in future estimates (set escalation_mode = EXPLICIT in _CONFIG.md)
3. Develop cashflow curve and apply escalation factors by CBS bucket and time period
4. Monitor CAD exchange rates if importing equipment/materials

**Contingency Handling:** Contingency ($293k = 20.4%) provides some buffer for moderate escalation, but is not a substitute for formal escalation calculation on long-duration projects.

---

## Risk Summary Table

| Risk ID | Risk Driver | Probability | Impact | Affected CBS | Mitigation Priority | Contingency Coverage |
|---------|-------------|-------------|--------|--------------|---------------------|----------------------|
| R-001 | Price | HIGH | HIGH | All | HIGH | Partial |
| R-002 | Quantity + Scope | HIGH | HIGH | MAT, CD | HIGH | Partial |
| R-003 | Schedule | MED | MED | CI | MED | Adequate |
| R-004 | Interface + Productivity | MED-HIGH | MED | CD, CI, PM | MED | Adequate |
| R-005 | Schedule + Interface | MED | LOW-MED | CI, PM | LOW | Adequate |
| R-006 | Scope + Quantity | HIGH | LOW-MED | CD | LOW | Adequate |
| R-007 | Scope | MED | MED-HIGH | MAT, CD, CI | HIGH | Partial |
| R-008 | Price | HIGH | MED | All | MED | Partial |

---

## Contingency Adequacy Assessment

**Total Contingency:** $293,020 CAD (20.4% of base)

**Risk Exposure:**
- **HIGH risks (R-001, R-002, R-007):** Address pricing uncertainty, quantity gaps, and scope growth potential; cumulative impact could be +30-60% on affected buckets
- **MED risks (R-003, R-004, R-005, R-008):** Address schedule, productivity, and escalation; cumulative impact ~10-20%

**Assessment:**
- Contingency is **ADEQUATE** for normal project risks and moderate scope/pricing adjustments
- Contingency is **INSUFFICIENT** if multiple high-impact risks materialize simultaneously (e.g., major scope growth + significant escalation + low productivity)
- Estimate maturity is **Draft/Conceptual** — expect refinement as ER and quotes become available

**Recommendation:** Update estimate as soon as Employer's Requirements and vendor quotes are available to reduce uncertainty and refine contingency allocation.

---

**Risk Register Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete
