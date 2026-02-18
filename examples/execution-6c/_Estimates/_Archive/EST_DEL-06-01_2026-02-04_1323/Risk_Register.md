# Risk Register
## DEL-06-01: CommissioningTrainingCloseoutWarrantyNarrative

---

## Snapshot Information

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-06-01_2026-02-04_1323 |
| **Created** | 2026-02-04 |
| **Contingency Method** | PCT_BY_BUCKET |
| **Contingency Rate** | 15% |
| **Contingency Amount** | CAD $1,170 |

---

## Risk Register

### R-001: RFP Requirements Differ from Decomposition

| Property | Value |
|----------|-------|
| **Risk ID** | R-001 |
| **Risk Driver** | Scope uncertainty |
| **Cause** | RFP Sections 7.3.6, 7.3.7, 7.6 text not directly accessible; requirements derived from decomposition document |
| **Consequence** | Additional effort to address undiscovered requirements; potential rework of narrative sections |
| **Affected CBS/WBS** | E (Engineering) - PKG-07/DEL-06-01 |
| **Probability** | MEDIUM |
| **Impact** | +20% effort (~$1,400) |
| **Suggested Mitigation** | Obtain RFP PDF access early; verify decomposition against actual RFP; complete Step 1 requirements extraction before drafting |
| **Contingency Handling** | Covered by 15% contingency reserve |

---

### R-002: Cross-Deliverable Inconsistencies

| Property | Value |
|----------|-------|
| **Risk ID** | R-002 |
| **Risk Driver** | Interface/coordination |
| **Cause** | DEL-06-01 must align with DEL-08-01 (schedule), DEL-04-01 (methodology), DEL-07-02 (team); these may change during proposal development |
| **Consequence** | Additional coordination effort; potential rework to align timelines, team references, methodology integration |
| **Affected CBS/WBS** | E (Engineering), PM - PKG-07/DEL-06-01 |
| **Probability** | MEDIUM |
| **Impact** | +15% effort (~$1,050) |
| **Suggested Mitigation** | Early coordination with other deliverable owners (Steps 3, 11); document assumptions clearly; flag for reconciliation |
| **Contingency Handling** | Covered by 15% contingency reserve |

---

### R-003: Multiple Quality Review Iterations

| Property | Value |
|----------|-------|
| **Risk ID** | R-003 |
| **Risk Driver** | Quality/rework |
| **Cause** | Step 12 quality review may identify issues requiring multiple revision cycles; senior reviewer feedback may require substantial changes |
| **Consequence** | Additional drafting and revision effort; potential schedule compression |
| **Affected CBS/WBS** | E (Engineering) - PKG-07/DEL-06-01 |
| **Probability** | MEDIUM |
| **Impact** | +25% effort (~$1,750) |
| **Suggested Mitigation** | Follow Procedure.md quality criteria; use evaluator perspective rubric; limit to 3 draft iterations per procedure guidance |
| **Contingency Handling** | Covered by 15% contingency reserve |

---

### R-004: Technical Input Delays

| Property | Value |
|----------|-------|
| **Risk ID** | R-004 |
| **Risk Driver** | Resource availability |
| **Cause** | Technical leads (mechanical, electrical/fire) may not be available when needed for critical systems input |
| **Consequence** | Commissioning Lead proceeds without input; reduced credibility of technical content; rework when input received |
| **Affected CBS/WBS** | E (Engineering) - PKG-07/DEL-06-01 |
| **Probability** | LOW-MEDIUM |
| **Impact** | +10% effort (~$700) |
| **Suggested Mitigation** | Engage technical leads early in Step 4; schedule input reviews; provide clear questions/scope |
| **Contingency Handling** | Partially covered by contingency; escalate if delays exceed 1 week |

---

### R-005: Five-Component Integration Complexity

| Property | Value |
|----------|-------|
| **Risk ID** | R-005 |
| **Risk Driver** | Scope complexity |
| **Cause** | Deliverable has five integrated components (commissioning, training, closeout, deficiencies, warranty) that must flow together coherently |
| **Consequence** | Additional integration effort; potential structural rework; inconsistent terminology across sections |
| **Affected CBS/WBS** | E (Engineering) - PKG-07/DEL-06-01 |
| **Probability** | MEDIUM |
| **Impact** | +10% effort (~$700) |
| **Suggested Mitigation** | Follow Guidance.md structure; use consistent terminology from Specification; allocate sufficient time for Step 9 integration |
| **Contingency Handling** | Covered by 15% contingency reserve |

---

### R-006: Commissioning Lead Availability

| Property | Value |
|----------|-------|
| **Risk ID** | R-006 |
| **Risk Driver** | Resource availability |
| **Cause** | Commissioning Lead may have competing priorities during proposal development |
| **Consequence** | Delayed completion; compressed schedule; potential quality reduction |
| **Affected CBS/WBS** | E (Engineering) - PKG-07/DEL-06-01 |
| **Probability** | LOW |
| **Impact** | Schedule delay; quality risk |
| **Suggested Mitigation** | Secure Commissioning Lead time commitment upfront; establish proposal development priority |
| **Contingency Handling** | Not a cost risk; schedule risk managed through planning |

---

### R-007: Addendum 03 Interpretation Issues

| Property | Value |
|----------|-------|
| **Risk ID** | R-007 |
| **Risk Driver** | Scope clarity |
| **Cause** | Addendum 03 technical clarifications (generator, fire apparatus exhaust, bay systems) may have implications not fully captured in decomposition |
| **Consequence** | Incomplete coverage of addendum requirements in commissioning approach |
| **Affected CBS/WBS** | E (Engineering) - PKG-07/DEL-06-01 |
| **Probability** | LOW-MEDIUM |
| **Impact** | +5% effort (~$350) |
| **Suggested Mitigation** | Review Addendum 03 directly (Step 1); complete local addenda integration checklist from Specification R-008 |
| **Contingency Handling** | Covered by 15% contingency reserve |

---

## Risk Summary

| Risk Level | Count | Potential Impact Range |
|------------|-------|------------------------|
| HIGH | 0 | - |
| MEDIUM | 5 | +10% to +25% effort each |
| LOW-MEDIUM | 2 | +5% to +10% effort each |
| LOW | 1 | Schedule risk only |

---

## Contingency Calculation

| Component | Value |
|-----------|-------|
| **Base Estimate** | CAD $7,800 |
| **Contingency Rate** | 15% |
| **Contingency Amount** | CAD $1,170 |
| **Risk-Weighted Impact (indicative)** | ~$2,000 (if all medium risks materialize) |

**Rationale:** 15% contingency provides coverage for 1-2 medium-probability risks materializing simultaneously. If multiple risks materialize, actual effort may exceed estimate by up to 25%. Contingency is conservative for Class 5/4 estimate maturity.

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
