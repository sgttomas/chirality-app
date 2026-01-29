# Risk Register — PKG-33 HSE Management

**Snapshot ID:** EST_PKG33_DRAFT_2026-01-29_1100
**Date:** 2026-01-29
**Package:** PKG-33 HSE Management

---

## Risk Register Purpose

This register identifies risks that affect the estimate's accuracy, completeness, and validity. Each risk is documented with:
- Risk ID (`R-###`)
- Risk driver category (scope/qty/price/productivity/schedule/interface)
- Cause → Consequence
- Affected CBS/WBS buckets
- Suggested mitigation (human action)
- Contingency handling

---

## R-001: HSE Regulatory Requirements Uncertainty

**Risk Driver:** Scope / Regulatory

**Cause → Consequence:**
- VFPA (Vancouver Fraser Port Authority), Transport Canada, WorkSafeBC, and Metro Vancouver environmental requirements not fully detailed
- → HSE plan scope, risk assessment depth, and environmental monitoring frequency may be underestimated
- → Actual costs could exceed allowances if regulatory requirements are more stringent than assumed

**Affected Buckets:**
- E (HSE plans, assessments, method statements)
- CI (environmental monitoring, compliance records)
- COM (commissioning compliance monitoring)

**Probability:** Medium (regulatory requirements for port industrial projects are well-established, but project-specific requirements not confirmed)

**Impact:** Medium to High ($50k - $150k potential increase if requirements exceed assumptions)

**Mitigation:**
- Engage VFPA, WorkSafeBC, and Metro Vancouver early to clarify HSE and environmental compliance requirements
- Review Employer's Requirements Volumes 1-3 for HSE regulatory references
- Obtain pre-application meeting notes or similar projects' regulatory compliance costs

**Contingency Handling:**
- Included in baseline contingency (E: 20%, CI: 25%, COM: 25%)
- If requirements significantly exceed assumptions, contingency may be insufficient

---

## R-002: Environmental Monitoring Scope Creep

**Risk Driver:** Scope / Quantity

**Cause → Consequence:**
- CEMP and SPPP monitoring parameters, frequency, and duration not defined
- Marine operations (ship loading, berth construction) may require extensive water quality monitoring
- → Monitoring costs could increase if:
  - Water quality monitoring required (beyond stormwater)
  - Air quality monitoring required (fugitive dust, VOC emissions)
  - Noise monitoring required (marine piling, construction activities near residential areas)
  - Longer construction duration increases monitoring period

**Affected Buckets:**
- CI (DEL-33.04, DEL-33.05)
- COM (commissioning phase monitoring)

**Probability:** Medium-High (marine/port projects typically have extensive environmental monitoring requirements)

**Impact:** Medium ($30k - $100k increase if monitoring scope expands)

**Mitigation:**
- Define CEMP monitoring matrix (parameters, frequency, locations, duration)
- Obtain environmental consultant quote for monitoring services
- Review similar VFPA projects' environmental monitoring programs
- Clarify whether Employer provides baseline environmental data or Contractor must establish baseline

**Contingency Handling:**
- Partially addressed by CI and COM contingency (25%)
- Recommend explicit monitoring scope definition before finalizing budget

---

## R-003: Method Statement and Risk Assessment Volume

**Risk Driver:** Quantity

**Cause → Consequence:**
- Number of method statements and risk assessments estimated at 25-40 and 30-50 respectively
- Multi-discipline project (36 packages) with complex operations (marine, rail, tanks, confined spaces) may require more than estimated
- → If actual count exceeds 50 method statements or 60 risk assessments, costs could increase

**Affected Buckets:**
- E (DEL-33.02, DEL-33.03)

**Probability:** Medium (estimate uses typical industrial project benchmarks, but project has above-average complexity)

**Impact:** Low to Medium ($20k - $50k increase if volumes exceed by 30-50%)

**Mitigation:**
- Develop preliminary task/activity list from decomposition packages
- Identify high-risk activities requiring method statements (confined space, work at height, hot work, marine operations, heavy lifts, energized electrical)
- Clarify Employer's requirements for method statement approval and depth
- Use templated method statements where applicable to reduce development effort

**Contingency Handling:**
- Addressed by E contingency (20%)
- Low to moderate risk; contingency adequate for expected variance

---

## R-004: Waste Management Volume Uncertainty

**Risk Driver:** Quantity

**Cause → Consequence:**
- Waste volumes (construction debris, excavated soil, hazardous waste, scrap) not quantified
- Demolition scope (PKG-01) and earthworks (PKG-02) may generate significant waste volumes
- → If waste volumes are high or hazardous waste content exceeds assumptions, disposal costs and tracking effort increase

**Affected Buckets:**
- CI (DEL-33.06 waste tracking and manifesting)

**Probability:** Low-Medium (estimate covers tracking/records only; disposal costs assumed in other packages)

**Impact:** Low ($10k - $30k increase if tracking effort significantly exceeds assumptions)

**Mitigation:**
- Review PKG-01 (Demolition) and PKG-02 (Earthworks) estimates for waste volume projections
- Clarify whether waste disposal costs are included in construction packages or require separate allowance
- Develop waste management plan with estimated volumes by waste type
- Identify hazardous waste streams (oils, paints, solvents, contaminated soil) requiring special handling

**Contingency Handling:**
- Addressed by CI contingency (25%)
- Low risk impact; contingency adequate

---

## R-005: Emergency Response Plan Integration Complexity

**Risk Driver:** Scope / Interface

**Cause → Consequence:**
- Site is within Fraser Surrey Terminal (existing operating facility)
- ERP must integrate with:
  - Employer's site-wide emergency response plan
  - Port of Vancouver emergency protocols
  - Local emergency services (Surrey Fire, BC Ambulance, Coast Guard)
- → Integration complexity and approval cycles may increase ERP development effort beyond allowance

**Affected Buckets:**
- E, PM (DEL-33.07)

**Probability:** Medium (site integration always adds complexity, but typical for brownfield projects)

**Impact:** Low ($10k - $25k increase if integration requires extensive coordination/revisions)

**Mitigation:**
- Obtain Employer's site emergency response plan and integration requirements early
- Clarify approval process and iteration expectations
- Engage Port of Vancouver and local emergency services for coordination requirements
- Budget for 2-3 revision cycles in ERP development

**Contingency Handling:**
- Addressed by E and PM contingency (20%)
- Low to moderate risk; contingency adequate

---

## R-006: Construction Schedule Duration Variance

**Risk Driver:** Schedule

**Cause → Consequence:**
- Construction duration assumed at 24 months; commissioning at 3 months
- → If actual duration is longer:
  - Environmental monitoring costs increase (CEMP, SPPP) — linear with duration
  - Waste management tracking increases
  - HSE oversight allocation (CI) increases
- → If duration is shorter, costs may decrease but productivity/overlap risks increase

**Affected Buckets:**
- CI (monitoring, oversight)
- COM (commissioning monitoring)

**Probability:** Medium-High (schedule uncertainty is typical at conceptual phase)

**Impact:** Medium ($15k - $30k cost change per ±6 months schedule variance)

**Mitigation:**
- Develop project schedule with construction and commissioning durations
- Update estimate using time-based indirects model when schedule available (set D-006 to time-based)
- Consider phased environmental monitoring plan to align with actual construction sequence

**Contingency Handling:**
- Partially addressed by CI and COM contingency
- Schedule variance beyond ±6 months may exceed contingency coverage for time-based costs

---

## R-007: HSE Labor Market Escalation

**Risk Driver:** Price / Escalation

**Cause → Consequence:**
- Estimate uses January 2026 pricing basis; escalation not applied (D-009)
- HSE professional and environmental consultant labor rates subject to market escalation
- BC Lower Mainland labor market has experienced 3-5% annual escalation in recent years
- → If HSE services occur over 2-3 years from estimate date, costs subject to 6-15% cumulative escalation

**Affected Buckets:**
- E (HSE consultants, environmental consultants)
- PM (HSE coordination)

**Probability:** High (labor escalation is nearly certain over multi-year project)

**Impact:** Medium ($25k - $60k cumulative escalation on $545k E base over 2-3 years at 3-5% annual)

**Mitigation:**
- Enable escalation in estimate (set escalation_mode = EXPLICIT in config)
- Obtain fixed-price quotes from HSE/environmental consultants if possible
- Include escalation clause in consultant service agreements
- Update estimate periodically as project schedule and pricing dates become clearer

**Contingency Handling:**
- NOT addressed by contingency (contingency covers scope/quantity uncertainty, not time-based escalation)
- Recommend explicit escalation provision in budget

---

## R-008: Interface with Other Packages (HSE Dependencies)

**Risk Driver:** Interface

**Cause → Consequence:**
- PKG-33 HSE deliverables interface with all other packages (HSE oversight is cross-cutting)
- Method statements (DEL-33.03) depend on construction methods defined in PKG-05 through PKG-27
- Risk assessments (DEL-33.02) depend on scope clarity in all construction packages
- → If other packages' scope is unclear or changes significantly, PKG-33 effort increases due to rework/revisions

**Affected Buckets:**
- E (method statements, risk assessments)
- PM (coordination)

**Probability:** Medium (typical for cross-cutting packages; design-build contracts have iterative scope definition)

**Impact:** Low to Medium ($15k - $40k if significant rework required)

**Mitigation:**
- Sequence HSE deliverables to follow construction package scope definition (30% design milestone)
- Use templated/modular method statements and risk assessments that can be updated as scope evolves
- Include HSE coordination in design review cycles to minimize rework
- Clarify baseline scope for method statements (based on decomposition) vs. detailed scope (based on final design)

**Contingency Handling:**
- Addressed by E and PM contingency (20%)
- Low to moderate risk; contingency adequate for normal interface coordination

---

## Risk Summary Table

| Risk ID | Risk Description | Probability | Impact | Affected CBS | Contingency Adequacy |
|---------|------------------|-------------|--------|--------------|---------------------|
| R-001 | HSE regulatory requirements uncertainty | Medium | Med-High | E, CI, COM | Adequate for moderate variance; may be insufficient if requirements significantly exceed |
| R-002 | Environmental monitoring scope creep | Med-High | Medium | CI, COM | Partially adequate; recommend scope definition |
| R-003 | Method statement/risk assessment volume | Medium | Low-Med | E | Adequate |
| R-004 | Waste management volume uncertainty | Low-Med | Low | CI | Adequate |
| R-005 | ERP integration complexity | Medium | Low | E, PM | Adequate |
| R-006 | Construction schedule duration variance | Med-High | Medium | CI, COM | Adequate for ±6 months; insufficient for larger variance |
| R-007 | HSE labor market escalation | High | Medium | E, PM | NOT adequate (escalation not in contingency) |
| R-008 | Interface with other packages | Medium | Low-Med | E, PM | Adequate |

---

## Contingency Adequacy Assessment

**Baseline Contingency (by CBS):**
- E: 20% ($109,000 on $545k base)
- PM: 20% ($19,860 on $99.3k base)
- P: 15% ($1,635 on $10.9k base)
- CI: 25% ($76,212 on $305k base)
- COM: 25% ($16,812 on $67.25k base)

**Total Contingency:** $189,000 CAD (24.4% blended rate on $775k base)

**Adequacy Summary:**
- **Adequate for:** Normal scope/quantity variance (R-003, R-004, R-005, R-008), moderate regulatory requirements (R-001), moderate monitoring scope adjustments (R-002)
- **Marginal for:** Significant regulatory requirements increase (R-001), extensive monitoring scope creep (R-002), schedule variance >±6 months (R-006)
- **Inadequate for:** Multi-year escalation exposure (R-007 — escalation should be separate provision, not in contingency)

**Recommendations:**
1. **Immediate:** Clarify HSE regulatory requirements (R-001) and environmental monitoring scope (R-002) to reduce uncertainty
2. **Before budget approval:** Add explicit escalation provision for labor costs over project duration (R-007)
3. **Ongoing:** Update estimate as construction schedule is finalized (R-006) and other package scopes are defined (R-008)

---

**Risk Register Prepared By:** Estimating Agent (Phase 4.2)
**Date:** 2026-01-29
**Status:** Complete (8 risks identified)
