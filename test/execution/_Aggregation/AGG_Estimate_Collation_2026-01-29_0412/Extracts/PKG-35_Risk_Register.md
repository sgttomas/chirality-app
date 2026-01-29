# Risk Register — PKG-35 Training & Handover Estimate

**Snapshot ID:** EST_PKG35_DRAFT_2026-01-29_1200
**Package:** PKG-35 Training & Handover
**Date:** 2026-01-29

---

## Risk Summary

| Risk Level | Count | Total Exposure |
|------------|-------|----------------|
| High | 3 | $350,000+ |
| Medium | 5 | $150,000 - $300,000 |
| Low | 2 | $50,000 - $100,000 |
| **Total** | **10** | **$550,000 - $750,000** |

---

## Risk Register

| R-ID | Risk Driver | Cause → Consequence | Affected CBS/WBS | Probability | Impact | Severity | Mitigation | Contingency Handling |
|------|-------------|---------------------|------------------|-------------|--------|----------|------------|---------------------|
| R-001 | Training scope expansion | Employer requires more comprehensive training than assumed → increased development and delivery costs | E, COM | Medium | High | HIGH | Early scope definition with Employer | 30% contingency on COM |
| R-002 | OEM training cost overrun | OEM training quotes higher than allowances → budget shortfall | COM | Medium | Medium | MEDIUM | Obtain OEM quotes early | 30% contingency on COM |
| R-003 | Site reinstatement scope | Extensive temp facilities or contamination discovered → increased reinstatement costs | CD, CI | Medium | High | HIGH | Confirm PKG-00 scope, conduct site assessment | 30% contingency on CD |
| R-004 | Defects liability workload | High defect volume during warranty period → increased support costs | PM | Low | High | MEDIUM | Quality focus during construction | 20% contingency on PM |
| R-005 | Training schedule compression | Compressed commissioning schedule → premium costs for accelerated training | COM | Medium | Medium | MEDIUM | Coordinate training schedule early | 30% contingency on COM |
| R-006 | Employer staffing delays | Employer personnel not available for training → rescheduling, extended delivery | COM, PM | Low | Medium | LOW | Coordinate training schedule with Employer | Included in allowances |
| R-007 | Language/translation requirements | Additional language requirements → translation costs | E | Low | Low | LOW | Confirm language requirements early | 20% contingency on E |
| R-008 | Escalation exposure | Training occurs 24-36 months from pricing date → labor cost increases | All | Medium | Medium | MEDIUM | Enable escalation in future estimates | Not applied (D-009) |
| R-009 | Terminal operations conflicts | Site reinstatement conflicts with terminal operations → delays, premium costs | CD, CI | Medium | Medium | MEDIUM | Coordinate with terminal per OBJ-5 | 25-30% contingency on CD/CI |
| R-010 | Documentation completeness | Incomplete as-built documentation → training material delays | E, PM | Low | Medium | LOW | Coordinate with PKG-31 documentation | 20% contingency on E |

---

## Risk Details

### R-001: Training Scope Expansion (HIGH)

**Risk Driver:** Training scope expansion

**Cause → Consequence:**
Employer requires more comprehensive training than assumed (more systems, more personnel, more depth) → significantly increased training development and delivery costs.

**Affected CBS/WBS:** Engineering (E) — training materials; Commissioning (COM) — training delivery

**Probability:** Medium (30-50%)
- Training scope often expands as commissioning approaches
- Employer may identify additional training needs

**Impact:** High ($100k - $200k+)
- Additional training modules to develop
- Extended training delivery period
- Additional OEM training sessions

**Severity:** HIGH

**Mitigation:**
1. Define training scope and curriculum early with Employer
2. Identify all systems requiring training in equipment packages
3. Confirm training population and competency requirements
4. Establish training acceptance criteria

**Contingency Handling:** 30% contingency on COM reflects scope uncertainty

---

### R-002: OEM Training Cost Overrun (MEDIUM)

**Risk Driver:** OEM training costs

**Cause → Consequence:**
OEM training quotes higher than allowances (specialized equipment, factory training requirements, travel) → budget shortfall for training delivery.

**Affected CBS/WBS:** Commissioning (COM)

**Probability:** Medium (30-50%)
- OEM training often underestimated at early estimate stages
- Some OEMs require factory training with travel
- Specialized equipment may require extended training

**Impact:** Medium ($50k - $100k)
- 8 major systems × $10-15k variance = $80k-$120k potential overrun

**Severity:** MEDIUM

**Mitigation:**
1. Obtain budgetary OEM training quotes early
2. Include training requirements in equipment purchase specifications
3. Negotiate training as part of equipment procurement
4. Identify which systems require factory vs. site training

**Contingency Handling:** 30% contingency on COM includes OEM cost uncertainty

---

### R-003: Site Reinstatement Scope (HIGH)

**Risk Driver:** Site reinstatement scope uncertainty

**Cause → Consequence:**
Extensive temporary facilities installed (more than assumed) or contamination discovered during site clearance → significantly increased reinstatement costs.

**Affected CBS/WBS:** Construction Directs (CD); Construction Indirects (CI)

**Probability:** Medium (30-50%)
- Temp facilities scope depends on construction approach
- Contamination discovery possible at active terminal
- Environmental closure requirements may exceed assumptions

**Impact:** High ($100k - $200k+)
- Extended demobilization period
- Remediation costs if contamination found
- Additional restoration requirements

**Severity:** HIGH

**Mitigation:**
1. Confirm PKG-00 Site Establishment scope (defines temp facilities)
2. Conduct baseline site assessment before construction
3. Define reinstatement acceptance criteria with Employer
4. Include environmental closeout requirements

**Contingency Handling:** 30% contingency on CD reflects scope uncertainty

---

### R-004: Defects Liability Workload (MEDIUM)

**Risk Driver:** Warranty period defect volume

**Cause → Consequence:**
Higher than expected defect volume during 12-month warranty period → increased defects liability support costs.

**Affected CBS/WBS:** Project Management (PM) — defects liability management

**Probability:** Low (10-30%)
- Quality-focused construction typically results in low defect rates
- New systems may have early-life failures

**Impact:** High ($80k - $150k)
- Increased site visits and coordination
- Defect rectification labor and materials
- Extended support period if disputes

**Severity:** MEDIUM

**Mitigation:**
1. Maintain quality focus during construction and commissioning
2. Conduct thorough testing before handover
3. Address punch list items before Taking Over
4. Establish clear defect classification criteria

**Contingency Handling:** 20% contingency on PM + high allowance range (A-005)

---

### R-005: Training Schedule Compression (MEDIUM)

**Risk Driver:** Compressed training schedule

**Cause → Consequence:**
Compressed commissioning schedule or delayed training start → premium costs for accelerated training delivery (overtime, multiple sessions, additional trainers).

**Affected CBS/WBS:** Commissioning (COM)

**Probability:** Medium (30-50%)
- Project schedules often compress near completion
- Training often squeezed between commissioning and handover

**Impact:** Medium ($40k - $80k)
- Overtime premiums
- Additional trainer mobilization
- Parallel training sessions

**Severity:** MEDIUM

**Mitigation:**
1. Establish training schedule early in commissioning planning
2. Coordinate training with commissioning milestones
3. Allow adequate float for training activities
4. Consider phased training approach (pre-commissioning, commissioning, handover)

**Contingency Handling:** 30% contingency on COM includes schedule risk

---

### R-006: Employer Staffing Delays (LOW)

**Risk Driver:** Employer personnel availability

**Cause → Consequence:**
Employer personnel not available for scheduled training (hiring delays, other commitments) → rescheduling, extended training period, repeat sessions.

**Affected CBS/WBS:** Commissioning (COM); Project Management (PM)

**Probability:** Low (10-30%)
- Employer responsibility to provide trainees
- Typically well-coordinated for major facility handover

**Impact:** Medium ($30k - $60k)
- Rescheduled training sessions
- Trainer standby costs
- Extended training administration

**Severity:** LOW

**Mitigation:**
1. Confirm training schedule with Employer early
2. Require Employer commitment to provide trainees
3. Build schedule flexibility into training plan

**Contingency Handling:** Included in training delivery allowance range

---

### R-007: Language/Translation Requirements (LOW)

**Risk Driver:** Multi-language requirements

**Cause → Consequence:**
Employer requires training materials in multiple languages → additional translation and localization costs.

**Affected CBS/WBS:** Engineering (E) — training materials

**Probability:** Low (10-30%)
- BC location typically English-primary
- Some workforces may require French or other languages

**Impact:** Low ($20k - $40k)
- Translation costs per language
- Multi-language review cycles

**Severity:** LOW

**Mitigation:**
1. Confirm language requirements with Employer early
2. Include translation in training materials specification
3. Budget for translation if required

**Contingency Handling:** 20% contingency on E includes minor scope variations

---

### R-008: Escalation Exposure (MEDIUM)

**Risk Driver:** Cost escalation over time

**Cause → Consequence:**
Training and handover activities occur 24-36 months from pricing date → labor and material cost increases not captured in estimate.

**Affected CBS/WBS:** All

**Probability:** Medium (30-50%)
- Training and handover occur at project end
- Labor escalation typical 2-3% annually

**Impact:** Medium ($60k - $90k)
- 4-6% cumulative escalation on $1.5M base

**Severity:** MEDIUM

**Mitigation:**
1. Enable escalation in future estimate updates
2. Monitor market conditions
3. Include escalation contingency if project extends

**Contingency Handling:** Not applied per D-009; identified as future estimate improvement

---

### R-009: Terminal Operations Conflicts (MEDIUM)

**Risk Driver:** Active terminal operations

**Cause → Consequence:**
Site reinstatement activities conflict with ongoing terminal operations (per OBJ-5: Terminal Continuity) → work restrictions, delays, premium costs.

**Affected CBS/WBS:** Construction Directs (CD); Construction Indirects (CI)

**Probability:** Medium (30-50%)
- Active terminal requires coordination
- Work windows may be restricted
- Operations may take priority over reinstatement

**Impact:** Medium ($40k - $80k)
- Off-hours work premiums
- Extended reinstatement duration
- Additional coordination costs

**Severity:** MEDIUM

**Mitigation:**
1. Coordinate reinstatement schedule with terminal operations
2. Define work windows and restrictions early
3. Plan reinstatement activities to minimize terminal disruption
4. Include coordination requirements in reinstatement planning

**Contingency Handling:** 25-30% contingency on CD/CI includes operations coordination

---

### R-010: Documentation Completeness (LOW)

**Risk Driver:** As-built documentation quality

**Cause → Consequence:**
Incomplete or delayed as-built documentation from other packages → delays in training materials development, rework of training content.

**Affected CBS/WBS:** Engineering (E); Project Management (PM)

**Probability:** Low (10-30%)
- PKG-31 Documentation & Deliverables coordinates documentation
- As-built documentation typically available before training

**Impact:** Medium ($30k - $50k)
- Training materials development delays
- Rework of training content
- Extended review cycles

**Severity:** LOW

**Mitigation:**
1. Coordinate with PKG-31 documentation schedule
2. Prioritize training-critical documentation
3. Develop training materials in parallel with final documentation

**Contingency Handling:** 20% contingency on E includes rework allowance

---

## Contingency Adequacy Assessment

### Contingency Applied

| CBS | Base (CAD) | Contingency Rate | Contingency (CAD) |
|-----|------------|------------------|-------------------|
| E | $285,000 | 20% | $57,000 |
| PM | $297,000 | 20% | $59,400 |
| P | $17,000 | 15% | $2,550 |
| CD | $350,000 | 30% | $105,000 |
| CI | $134,000 | 25% | $33,500 |
| COM | $395,000 | 30% | $118,500 |
| **Total** | **$1,478,000** | **25.0%** | **$369,000** |

### Assessment

**Adequate For:**
- Normal project risks (R-005 through R-010)
- Moderate scope adjustments within assumed ranges
- Typical OEM training cost variations

**May Be Insufficient For:**
- Significant training scope expansion (R-001) — could require +$100k-$200k
- Major site contamination discovery (R-003) — could require +$100k-$200k
- High defects liability workload (R-004) — could require +$80k-$150k

**Recommendation:**
- Update estimate as training scope is defined (reduces R-001)
- Conduct site assessment before site reinstatement (reduces R-003)
- Maintain construction quality focus (reduces R-004)

---

**Risk Register Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Snapshot:** EST_PKG35_DRAFT_2026-01-29_1200
