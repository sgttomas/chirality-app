# Risk Register

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-03-01_2026-02-04_1453 |
| **Deliverable** | DEL-03-01 Design Methodology Narrative |

---

## Risk Register

### R-001: Labor Rate Variance

| Field | Value |
|-------|-------|
| **Risk ID** | R-001 |
| **Risk Driver** | Price |
| **Cause** | All labor rates are assumed allowances; actual team rates may differ significantly from assumptions |
| **Consequence** | Estimate could be understated or overstated by 20-30% based on actual billing rates |
| **Affected CBS** | E (Engineering), PM (Project Management) |
| **Affected WBS** | PKG-05, DEL-03-01 |
| **Likelihood** | HIGH |
| **Impact** | MEDIUM |
| **Suggested Mitigation** | Provide actual team billing rates in `_RateTables/`; validate rates with finance/HR |
| **Contingency Handling** | 20% contingency applied to E bucket; 15% to PM bucket |

---

### R-002: Scope Creep - Narrative Content

| Field | Value |
|-------|-------|
| **Risk ID** | R-002 |
| **Risk Driver** | Scope |
| **Cause** | 30 requirements in Specification.md may expand during production; stakeholders may request additional content |
| **Consequence** | Additional authoring hours required; estimate could understate effort by 25-50% |
| **Affected CBS** | E (Engineering) |
| **Affected WBS** | PKG-05, DEL-03-01 |
| **Likelihood** | MEDIUM |
| **Impact** | MEDIUM |
| **Suggested Mitigation** | Define content boundaries clearly before production; limit scope to RFP Section 7.1 requirements; use Specification.md as checklist |
| **Contingency Handling** | 20% contingency on E bucket covers moderate scope expansion |

---

### R-003: Visual Aids Complexity

| Field | Value |
|-------|-------|
| **Risk ID** | R-003 |
| **Risk Driver** | Scope/Qty |
| **Cause** | Graphics scope assumed at 8 hours for 3-4 diagrams; actual complexity and presentation standards may require more |
| **Consequence** | Graphics production could require 2-3x estimated hours if high-quality presentation graphics needed |
| **Affected CBS** | E (Engineering) |
| **Affected WBS** | PKG-05, DEL-03-01 (E-009) |
| **Likelihood** | MEDIUM |
| **Impact** | LOW-MEDIUM |
| **Suggested Mitigation** | Define graphic complexity requirements upfront; use templates if available; consider simple diagrams over elaborate graphics |
| **Contingency Handling** | 20% contingency partially covers; may need adjustment if scope expands |

---

### R-004: Cross-Deliverable Inconsistency

| Field | Value |
|-------|-------|
| **Risk ID** | R-004 |
| **Risk Driver** | Interface |
| **Cause** | DEL-03-01 must be consistent with DEL-04-01, DEL-08-01, DEL-03-02, DEL-02-01; coordination effort may exceed estimate |
| **Consequence** | Additional coordination meetings and revision cycles; rework if inconsistencies discovered late |
| **Affected CBS** | E (Engineering), PM (Project Management) |
| **Affected WBS** | PKG-05, DEL-03-01 |
| **Likelihood** | MEDIUM |
| **Impact** | MEDIUM |
| **Suggested Mitigation** | Establish shared terminology register early; conduct coordination review before QC (Step 4); parallel development with regular sync |
| **Contingency Handling** | 15% PM contingency covers coordination overhead |

---

### R-005: Stakeholder Review Delays

| Field | Value |
|-------|-------|
| **Risk ID** | R-005 |
| **Risk Driver** | Schedule |
| **Cause** | Stakeholder review cycles assumed at 2; actual may be more; review feedback may require significant rework |
| **Consequence** | Additional review effort not in base estimate; potential schedule delay affecting proposal submission |
| **Affected CBS** | PM (Project Management) |
| **Affected WBS** | PKG-05, DEL-03-01 (PM-002) |
| **Likelihood** | MEDIUM |
| **Impact** | LOW-MEDIUM |
| **Suggested Mitigation** | Align stakeholders early on content direction; conduct informal reviews before formal cycles; set clear review turnaround expectations |
| **Contingency Handling** | 15% PM contingency; may need schedule buffer |

---

### R-006: Team Availability

| Field | Value |
|-------|-------|
| **Risk ID** | R-006 |
| **Risk Driver** | Productivity |
| **Cause** | Estimate assumes all required team members (PM, Architect, Discipline Leads, CM, Scheduler) available when needed |
| **Consequence** | Delays if key team members unavailable; substitution with less experienced staff may affect quality |
| **Affected CBS** | E (Engineering) |
| **Affected WBS** | PKG-05, DEL-03-01 |
| **Likelihood** | LOW-MEDIUM |
| **Impact** | MEDIUM |
| **Suggested Mitigation** | Confirm team availability before production; identify backup resources; schedule input sessions in advance |
| **Contingency Handling** | 20% contingency on E bucket partially covers |

---

### R-007: Quality Threshold Not Met

| Field | Value |
|-------|-------|
| **Risk ID** | R-007 |
| **Risk Driver** | Scope/Quality |
| **Cause** | Specification.md notes 80-100% score requires "innovation" and "exceptional thoroughness"; baseline estimate may not achieve target quality |
| **Consequence** | Additional effort required to elevate narrative from compliant to exceptional; rework if QC identifies quality gaps |
| **Affected CBS** | E (Engineering) |
| **Affected WBS** | PKG-05, DEL-03-01 |
| **Likelihood** | MEDIUM |
| **Impact** | MEDIUM |
| **Suggested Mitigation** | Define innovation elements upfront; allocate specific effort for differentiation; conduct quality-focused review before final |
| **Contingency Handling** | 20% contingency on E bucket; may need additional allowance if targeting exceptional score |

---

### R-008: Underestimated Technical Input

| Field | Value |
|-------|-------|
| **Risk ID** | R-008 |
| **Risk Driver** | Qty |
| **Cause** | Technical input from Architect and Discipline Leads estimated at 2-4 hours each; actual involvement may be higher |
| **Consequence** | Cost increase of $500-$1,500 CAD if technical input doubles |
| **Affected CBS** | E (Engineering) |
| **Affected WBS** | PKG-05, DEL-03-01 (E-005, E-006) |
| **Likelihood** | LOW |
| **Impact** | LOW |
| **Suggested Mitigation** | Prepare focused questions for technical input sessions; limit scope of technical review to key sections |
| **Contingency Handling** | 20% contingency on E bucket covers |

---

## Risk Summary Matrix

| Risk ID | Risk Driver | Likelihood | Impact | Risk Level |
|---------|-------------|------------|--------|------------|
| R-001 | Price | HIGH | MEDIUM | HIGH |
| R-002 | Scope | MEDIUM | MEDIUM | MEDIUM |
| R-003 | Scope/Qty | MEDIUM | LOW-MEDIUM | MEDIUM |
| R-004 | Interface | MEDIUM | MEDIUM | MEDIUM |
| R-005 | Schedule | MEDIUM | LOW-MEDIUM | LOW-MEDIUM |
| R-006 | Productivity | LOW-MEDIUM | MEDIUM | LOW-MEDIUM |
| R-007 | Scope/Quality | MEDIUM | MEDIUM | MEDIUM |
| R-008 | Qty | LOW | LOW | LOW |

---

## Contingency Summary

| CBS Bucket | Base Amount | Contingency % | Contingency $ | Primary Risks Covered |
|------------|------------:|--------------:|--------------:|----------------------|
| E (Engineering) | $11,170 | 20% | $2,234 | R-001, R-002, R-003, R-006, R-007, R-008 |
| PM (Project Management) | $2,376 | 15% | $356 | R-001, R-004, R-005 |
| **TOTAL** | **$13,546** | **19.1%** | **$2,590** | |

---

## Top Risk Actions

| Priority | Risk | Recommended Action | Owner |
|----------|------|-------------------|-------|
| 1 | R-001 (Rate Variance) | Provide actual billing rates before finalizing estimate | Finance/PM |
| 2 | R-002 (Scope Creep) | Lock content outline before production begins | Design Manager |
| 3 | R-004 (Cross-Deliverable) | Establish terminology register; schedule coordination reviews | Proposal Manager |
| 4 | R-007 (Quality Threshold) | Define innovation strategy for narrative | Design Manager |

---

**Generated:** 2026-02-04
**Agent:** ESTIMATING (Type 2)
