# Risk Register — PKG-30 Commissioning Estimate

**Snapshot ID:** EST_PKG30_DRAFT_2026-01-29_0014
**Date:** 2026-01-29

This register identifies risks that affect the estimate accuracy, cost outcomes, and schedule for PKG-30 Commissioning.

---

## R-001: Terminal Continuity Constraints

**Risk Driver:** Schedule / Interface

**Cause → Consequence:**
- Existing terminal operations at Fraser Surrey Terminal limit commissioning work windows
- Night/weekend work may be required → premium time costs
- Marine loading commissioning must coordinate with terminal ship traffic → schedule delays
- Restricted access during peak terminal operations → extended commissioning duration

**Affected Buckets:** CD, CI (commissioning labor duration and premium time)

**Cost Impact:** HIGH — Terminal constraints embedded in 30-week duration assumption; potential additional $200-400k if constraints more severe than assumed

**Schedule Impact:** HIGH — Extends commissioning duration by ~20% vs unrestricted schedule

**Suggested Mitigation (Human Action):**
- Early coordination with Employer (DP World Fraser Surrey Inc.) and terminal operations team
- Develop detailed work window schedule in DEL-30.02 Commissioning Plan
- Build schedule contingency (15% float included in duration assumption)
- Pre-plan critical path activities for optimal work windows

**Contingency Handling:**
- 15% schedule float embedded in duration assumptions
- 28% contingency on CD and CI buckets includes terminal constraint uncertainty
- Qualitative: Terminal coordination risks captured in assumptions (A-010)

**Source:** Decomposition §1.1 (Location: Fraser Surrey Terminal - active operations); §2 OBJ-5 (Terminal Continuity); DEL-30.02 Guidance.md §C-3

---

## R-002: System Handover Schedule Delays

**Risk Driver:** Schedule / Interface

**Cause → Consequence:**
- Construction delays or changes to system handover sequence → commissioning start delays
- Systems not ready for commissioning on assumed schedule → idle commissioning team
- Accelerated handover requirements → compressed commissioning windows → increased labor costs

**Affected Buckets:** CD, CI, PM (commissioning schedule-dependent costs)

**Cost Impact:** MEDIUM-HIGH — Potential $300-600k if handover delays extend commissioning duration or require team demobilization/remobilization

**Schedule Impact:** HIGH — Critical path impact if key systems (tanks, metering, marine loading) delayed

**Suggested Mitigation (Human Action):**
- Integrate commissioning schedule with construction schedule early (DEL-30.02)
- Define clear system handover criteria and prerequisites
- Build commissioning schedule float
- Maintain commissioning team flexibility for schedule changes

**Contingency Handling:**
- Schedule float and duration contingency embedded in assumptions (A-008)
- Contingency on CD (28%) includes schedule variability
- Qualitative: Schedule integration risk captured; detailed mitigation requires construction schedule coordination

**Source:** Assumption A-008 (commissioning duration); typical construction-commissioning interface risks

---

## R-003: Metering System Proving Delays and Technical Issues

**Risk Driver:** Scope / Qty / Price / Productivity

**Cause → Consequence:**
- Custody transfer meter proving is specialized and technically demanding
- Meter proving failures require repeat runs → extended proving duration
- Proving equipment availability or technical issues → delays
- Acceptance criteria not met → additional work scope

**Affected Buckets:** CD (proving specialist labor), MAT (proving equipment rental)

**Cost Impact:** MEDIUM — Potential additional $50-150k if multiple proving cycles required or technical issues encountered

**Schedule Impact:** MEDIUM-HIGH — Metering proving on critical path for marine loading commissioning

**Suggested Mitigation (Human Action):**
- Pre-qualify meter proving contractor with proven custody transfer experience
- Define clear proving acceptance criteria early (DEL-30.06)
- Allow adequate schedule float for proving activities (3 weeks baseline + 1 week contingency)
- Coordinate proving schedule with metering system vendor commissioning support

**Contingency Handling:**
- 25% contingency on metering proving costs (higher than baseline CD contingency)
- Schedule float embedded in assumptions (A-018)
- Qualitative: High-confidence proving contractor selection reduces risk

**Source:** Decomposition §2 OBJ-10 (Custody Transfer Accuracy - critical); Assumption A-018; typical metering proving risks

---

## R-004: Vendor Commissioning Support Scope and Availability

**Risk Driver:** Scope / Schedule / Interface

**Cause → Consequence:**
- Specialized vendor commissioning support not included in equipment purchase terms → additional costs
- Vendor personnel not available on required schedule → commissioning delays
- Vendor support scope larger than estimated (additional systems require vendor commissioning) → cost overrun
- Vendor mobilization delays (travel, permits, work authorization) → schedule delays

**Affected Buckets:** CD (vendor support labor and travel)

**Cost Impact:** MEDIUM — Potential additional $50-200k if vendor scope larger than estimated or mobilization costs higher

**Schedule Impact:** MEDIUM — Vendor availability constraints can delay commissioning of critical systems

**Suggested Mitigation (Human Action):**
- Include vendor commissioning support in equipment purchase terms early (during procurement phase)
- Confirm vendor commissioning scope and availability during equipment bid evaluation
- Lock in vendor commissioning dates in equipment contracts
- Coordinate vendor support requirements with equipment packages (PKG-10, PKG-11, PKG-13, PKG-19)

**Contingency Handling:**
- Vendor support scope estimated conservatively (A-005)
- 28% contingency on CD includes vendor support uncertainty
- Qualitative: Early vendor coordination reduces risk

**Source:** Assumption A-005 (vendor support scope); typical vendor commissioning coordination risks

---

## R-005: Marine Loading Commissioning Weather and Tide Windows

**Risk Driver:** Schedule / Productivity

**Cause → Consequence:**
- Marine loading commissioning requires suitable weather conditions (calm seas, low wind)
- Marine loading requires suitable tide windows for vessel access
- Winter weather or poor sea conditions → commissioning delays
- Waiting for weather/tide windows → idle commissioning team → extended duration

**Affected Buckets:** CD (marine loading commissioning labor)

**Cost Impact:** LOW-MEDIUM — Potential additional $50-100k if extended delays due to unsuitable weather

**Schedule Impact:** MEDIUM — Marine loading commissioning on critical path for facility handover

**Suggested Mitigation (Human Action):**
- Plan marine loading commissioning for summer weather window (May-September)
- Build weather contingency into commissioning schedule (20% float for marine activities)
- Have backup commissioning dates pre-planned
- Coordinate with terminal for vessel availability during planned commissioning windows

**Contingency Handling:**
- 20% schedule contingency for marine commissioning embedded in duration assumptions
- 28% contingency on CD includes schedule variability
- Qualitative: Summer weather window planning reduces risk

**Source:** DEL-30.02 Guidance.md §C-5 (seasonal considerations); typical marine commissioning weather risks

---

## R-006: Hydrotest Water Treatment and Discharge Permit Compliance

**Risk Driver:** Scope / Price / Regulatory

**Cause → Consequence:**
- Hydrotest water discharge permit conditions more stringent than assumed → additional treatment costs
- Water quality testing failures → repeat treatment cycles → cost overrun and delay
- Discharge permit delays or restrictions → extended hydrotest duration → schedule delays

**Affected Buckets:** MAT (hydrotest water treatment and disposal)

**Cost Impact:** LOW-MEDIUM — Potential additional $30-80k if treatment requirements more extensive

**Schedule Impact:** LOW-MEDIUM — Hydrotest delays can delay subsequent commissioning activities

**Suggested Mitigation (Human Action):**
- Confirm discharge permit conditions early (coordinate with PKG-32 Regulatory & Permits)
- Develop detailed hydrotest water management plan (DEL-29.06)
- Pre-qualify water treatment contractor
- Plan water sampling and testing in advance

**Contingency Handling:**
- 25% contingency on hydrotest water costs (higher than baseline MAT contingency)
- Assumption A-012 includes permit compliance uncertainty
- Qualitative: Early permit coordination and planning reduces risk

**Source:** Assumption A-012 (hydrotest water treatment); DEL-29.06 (Hydrotest Water Management Plan); typical hydrotest water risks

---

## R-007: Commissioning Procedure Development Scope Underestimated

**Risk Driver:** Scope / Qty

**Cause → Consequence:**
- More commissioning procedures required than estimated (30 baseline) → additional engineering costs
- Procedure complexity higher than typical (safety-critical systems, regulatory requirements) → extended development time
- Multiple procedure review/revision cycles → extended engineering duration

**Affected Buckets:** E (Engineering - procedure development)

**Cost Impact:** LOW-MEDIUM — Potential additional $50-150k if procedure count or complexity higher than estimated

**Schedule Impact:** LOW — Engineering activities not typically on critical path

**Suggested Mitigation (Human Action):**
- Define commissioning procedure framework and outline early in DEL-30.01
- Align procedure scope with system commissioning requirements
- Leverage standard procedure templates where possible
- Conduct early safety and technical reviews to minimize revision cycles

**Contingency Handling:**
- 20% contingency on E (Engineering) includes scope uncertainty
- Assumption A-003 provides conservative procedure count estimate
- Qualitative: Procedure template standardization reduces scope variability

**Source:** Assumption A-003 (procedure development scope); typical procedure development risks

---

## R-008: Defect Rectification Scope Larger Than Allowed

**Risk Driver:** Scope / Qty

**Cause → Consequence:**
- Construction defects discovered during commissioning more extensive than $75k allowance
- Defect rectification delays system commissioning → extended commissioning duration
- Punch list items accumulate requiring extended rectification effort

**Affected Buckets:** CD (defect rectification)

**Cost Impact:** MEDIUM — Potential additional $50-200k if construction quality issues significant

**Schedule Impact:** MEDIUM — Extensive defects can delay commissioning completion and handover

**Suggested Mitigation (Human Action):**
- Implement strong construction QA/QC to minimize defects during construction
- Conduct early system turnover inspections to identify defects before commissioning starts
- Include defect rectification plan in commissioning plan (DEL-30.02)
- Track and manage punch list items systematically (DEL-30.07)

**Contingency Handling:**
- 30% contingency on defect rectification allowance (higher than baseline)
- $75k base allowance conservative for typical construction quality
- Qualitative: Construction QA/QC performance directly impacts defect scope

**Source:** Assumption A-024 (defect rectification allowance); typical construction defect risks

---

## R-009: Commissioning Team Productivity Lower Than Assumed

**Risk Driver:** Productivity / Scope

**Cause → Consequence:**
- Commissioning activities more complex or time-intensive than estimated → extended duration
- Learning curve for commissioning team (new facility, unique systems) → lower initial productivity
- Rework or repeat testing required → extended commissioning duration
- Site access or logistics constraints reduce productivity

**Affected Buckets:** CD, CI (commissioning labor hours and duration)

**Cost Impact:** MEDIUM-HIGH — Potential additional $200-500k if productivity 20-30% lower than assumed

**Schedule Impact:** HIGH — Productivity impacts overall commissioning duration and critical path

**Suggested Mitigation (Human Action):**
- Select experienced commissioning team with relevant liquid bulk facility experience
- Provide commissioning team training and orientation before field activities start
- Conduct commissioning procedure walkthroughs and dry runs
- Monitor productivity early in commissioning and adjust resource plan if needed

**Contingency Handling:**
- 28% contingency on CD and CI includes productivity uncertainty
- Resource loading assumptions (A-015) conservative for productivity variability
- Qualitative: Experienced team selection and early planning reduce productivity risk

**Source:** Assumption A-015 (commissioning team loading); typical commissioning productivity risks

---

## R-010: Regulatory Witness Points and Inspection Delays

**Risk Driver:** Schedule / Regulatory

**Cause → Consequence:**
- Regulatory inspections and witness points not scheduled on time → commissioning delays
- Inspection findings require additional work or re-testing → extended duration and costs
- Authority inspectors not available on required dates → waiting time
- Permit conditions require additional commissioning activities not currently included

**Affected Buckets:** CD, CI (extended duration due to inspection waits)

**Cost Impact:** LOW-MEDIUM — Potential additional $50-150k if inspection delays extend commissioning duration

**Schedule Impact:** MEDIUM — Regulatory milestones can be critical path constraints

**Suggested Mitigation (Human Action):**
- Coordinate with PKG-32 (Regulatory & Permits) to identify all witness points early
- Schedule authority inspections well in advance
- Build inspection schedule float into commissioning plan
- Conduct pre-inspection readiness reviews to minimize findings

**Contingency Handling:**
- Schedule float embedded in duration assumptions includes inspection coordination time
- 28% contingency on CD and CI includes regulatory schedule uncertainty
- Qualitative: Early regulatory coordination (DEL-30.02 Guidance.md §C-4) reduces risk

**Source:** DEL-30.02 Guidance.md §C-4 (Regulatory considerations); typical regulatory coordination risks

---

## R-011: Integrated Systems Test Failures Requiring Extended Testing

**Risk Driver:** Scope / Productivity / Interface

**Cause → Consequence:**
- IST end-to-end scenarios fail on first attempt → troubleshooting and repeat testing required
- Integration issues between systems not discovered until IST → extended debugging and re-work
- Control system integration issues (SCADA/PLC, interlocks) → extended troubleshooting
- IST acceptance criteria not met → additional testing cycles

**Affected Buckets:** COM (Commissioning - integrated testing)

**Cost Impact:** MEDIUM — Potential additional $75-200k if extensive IST troubleshooting and repeat testing required

**Schedule Impact:** HIGH — IST on critical path; failures extend commissioning completion

**Suggested Mitigation (Human Action):**
- Complete thorough individual system commissioning before starting IST (DEL-30.04 complete)
- Develop detailed IST test protocols with clear prerequisites and acceptance criteria (DEL-30.05)
- Conduct IST tabletop walkthroughs before execution
- Allow adequate schedule float for IST troubleshooting

**Contingency Handling:**
- 30% contingency on COM (Commissioning) includes IST uncertainty
- Assumption A-016 includes conservative IST scope estimate
- Qualitative: Phased commissioning approach (P-1) reduces integration risk

**Source:** Assumption A-016 (IST scope); DEL-30.02 Guidance.md P-1 (Phased Commissioning Strategy); typical IST risks

---

## R-012: Performance Test Acceptance Criteria Not Achievable

**Risk Driver:** Scope / Performance / Acceptance

**Cause → Consequence:**
- Facility performance does not meet acceptance criteria (throughput, capacity, accuracy)
- Design or construction issues discovered during performance testing → remediation required
- Performance test failures → extended testing cycles → delayed handover
- Acceptance criteria disputes between Contractor and Employer → commercial issues

**Affected Buckets:** COM (performance testing), CD (potential remediation work)

**Cost Impact:** MEDIUM-HIGH — Potential significant additional costs if major performance issues discovered

**Schedule Impact:** HIGH — Performance testing is final gate before handover; failures delay project completion

**Suggested Mitigation (Human Action):**
- Define clear, measurable performance test acceptance criteria early (DEL-30.06)
- Align acceptance criteria with contract requirements and Employer's Requirements
- Conduct pre-performance test readiness reviews
- Monitor performance trends during IST and start-up to identify issues early

**Contingency Handling:**
- 30% contingency on COM includes performance testing uncertainty
- Qualitative: Early performance criteria definition and pre-test readiness reviews reduce risk
- NOTE: Major design or construction performance deficiencies not covered by estimate contingency (would require change order / warranty claim)

**Source:** Assumption A-017 (performance test scope); Decomposition §2 (Project Objectives: OBJ-2 Throughput, OBJ-10 Accuracy)

---

## R-013: Commissioning Consumables Quantities Underestimated

**Risk Driver:** Qty / Scope

**Cause → Consequence:**
- Commissioning consumables (flushing, cleaning, nitrogen, test fluids) quantities higher than estimated
- Additional cleaning or flushing cycles required → increased consumables usage
- Consumable pricing higher than estimated → cost overrun

**Affected Buckets:** MAT (commissioning consumables)

**Cost Impact:** LOW-MEDIUM — Potential additional $30-100k if consumables requirements higher than estimated

**Schedule Impact:** LOW — Consumables procurement not typically critical path (unless procurement delayed)

**Suggested Mitigation (Human Action):**
- Develop detailed commissioning consumables list based on commissioning procedures (DEL-30.01)
- Obtain quotes for bulk consumables early
- Procure long-lead consumables in advance
- Monitor consumables usage during commissioning and adjust procurement as needed

**Contingency Handling:**
- 25% contingency on MAT includes consumables quantity uncertainty
- Assumption A-022 provides conservative consumables estimate
- Qualitative: Detailed procedure development refines consumables quantities

**Source:** Assumption A-022 (commissioning consumables); typical consumables usage variability

---

## R-014: Test Equipment Rental Duration Exceeds 6 Months

**Risk Driver:** Schedule / Scope

**Cause → Consequence:**
- Commissioning duration extends beyond 30 weeks (6+ months) → additional test equipment rental costs
- Test equipment required for extended period during defect rectification or performance testing
- Rental rates higher for extended rental periods

**Affected Buckets:** MAT (test equipment rental)

**Cost Impact:** LOW-MEDIUM — Potential additional $30-90k if rental duration extends 1-2 months beyond baseline

**Schedule Impact:** N/A (schedule risk consequence, not cause)

**Suggested Mitigation (Human Action):**
- Negotiate rental rates with flexible duration terms (e.g., monthly rate after initial 6-month period)
- Monitor commissioning schedule progress and adjust test equipment rental plan accordingly
- Return equipment promptly when commissioning activities complete

**Contingency Handling:**
- 25% contingency on MAT includes rental duration variability
- Schedule float embedded in duration assumptions provides buffer
- Qualitative: Test equipment rental plan aligned with commissioning schedule

**Source:** Assumption A-022 (test equipment rental - 6 months); commissioning duration uncertainty

---

## R-015: Currency Exchange Rate Fluctuations (If Vendor Support in USD)

**Risk Driver:** Price

**Cause → Consequence:**
- Some specialized vendor support may be priced in USD (if US-based vendors)
- CAD/USD exchange rate fluctuations between estimate date and vendor contract execution
- Strengthening USD increases vendor support costs in CAD terms

**Affected Buckets:** CD (vendor support, if priced in USD)

**Cost Impact:** LOW — Potential additional $10-50k if limited USD-priced vendor support (most costs CAD-based)

**Schedule Impact:** N/A

**Suggested Mitigation (Human Action):**
- Prefer CAD-based vendor support contractors where possible
- Include currency exchange rate assumptions in vendor contracts
- Consider currency hedging if significant USD exposure

**Contingency Handling:**
- Contingency on CD includes pricing uncertainty
- Estimate assumes primarily CAD-based pricing
- Qualitative: Limited USD exposure (vendor support is small portion of estimate ~$195k / $4.7M)

**Source:** Assumption A-005 (vendor support); Decision D-001 (CAD currency basis)

---

## Risk Summary Table

| Risk ID | Risk Title | Impact | Probability | Contingency Strategy |
|---------|------------|--------|-------------|---------------------|
| R-001 | Terminal Continuity Constraints | HIGH | HIGH | Schedule float; 28% CD/CI contingency |
| R-002 | System Handover Delays | MEDIUM-HIGH | MEDIUM | Schedule integration; contingency |
| R-003 | Metering Proving Issues | MEDIUM | MEDIUM | 25% metering contingency; experienced contractor |
| R-004 | Vendor Support Scope/Availability | MEDIUM | MEDIUM | Early vendor coordination; 28% CD contingency |
| R-005 | Marine Weather/Tide Windows | LOW-MEDIUM | MEDIUM | Summer scheduling; 20% marine float |
| R-006 | Hydrotest Water Permit | LOW-MEDIUM | LOW | 25% hydrotest contingency; early permit coordination |
| R-007 | Procedure Development Scope | LOW-MEDIUM | LOW-MEDIUM | 20% E contingency; template standardization |
| R-008 | Defect Rectification Scope | MEDIUM | MEDIUM | 30% defect contingency; strong construction QC |
| R-009 | Commissioning Productivity | MEDIUM-HIGH | MEDIUM | 28% CD/CI contingency; experienced team |
| R-010 | Regulatory Inspection Delays | LOW-MEDIUM | LOW-MEDIUM | Schedule float; early regulatory coordination |
| R-011 | IST Failures | MEDIUM | MEDIUM | 30% COM contingency; thorough preparation |
| R-012 | Performance Test Failures | MEDIUM-HIGH | LOW | 30% COM contingency; early criteria definition |
| R-013 | Consumables Quantities | LOW-MEDIUM | LOW-MEDIUM | 25% MAT contingency |
| R-014 | Test Equipment Rental Duration | LOW-MEDIUM | MEDIUM | 25% MAT contingency; flexible rental terms |
| R-015 | Currency Exchange Rate | LOW | LOW | Minimal USD exposure; CAD-based contracts |

**Overall Risk Profile:** MEDIUM-HIGH
- Schedule risks dominate (terminal constraints, handover coordination, marine weather)
- Commissioning productivity and scope definition uncertainties significant
- Specialized activities (metering proving, IST, performance testing) carry execution risk
- Contingency strategy: 26% blended contingency rate addresses identified risks

---

**End of Risk Register**
