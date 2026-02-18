# Risk Register

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-01-03_2026-02-04_1322 |
| **Deliverable** | DEL-01-03 BondingAndInsuranceEvidence |

---

## Contingency Summary

| Property | Value |
|----------|-------|
| **Method** | PCT_BY_BUCKET |
| **Contingency Rate** | 15% |
| **Base Estimate** | CAD $5,900 |
| **Contingency Amount** | CAD $870 |
| **Total with Contingency** | CAD $6,770 |

---

## Risk Register

### R-001: RFP Requirements Uncertainty

| Field | Value |
|-------|-------|
| **Risk ID** | R-001 |
| **Risk Driver** | Scope uncertainty |
| **Cause** | RFP Section 5.3.1 not extracted (PDF access issue); specific requirements unknown |
| **Consequence** | Scope may be larger or different than assumed; rework may be required |
| **Affected CBS/WBS** | PM (all line items); P (third-party fees) |
| **Probability** | MEDIUM |
| **Impact** | MEDIUM (CAD $500-$1,500 potential overrun) |
| **Suggested Mitigation** | Extract RFP Section 5.3.1 requirements as soon as PDF is accessible; update estimate |
| **Contingency Handling** | Included in 15% contingency |

---

### R-002: Surety Relationship Delays

| Field | Value |
|-------|-------|
| **Risk ID** | R-002 |
| **Risk Driver** | Schedule/productivity |
| **Cause** | If new surety relationship required (vs. assumed existing), coordination time increases |
| **Consequence** | 50-100% increase in surety coordination effort; potential proposal deadline risk |
| **Affected CBS/WBS** | PM (L-002 Surety Coordination) |
| **Probability** | LOW (assumed existing relationship) |
| **Impact** | MEDIUM (CAD $600-$1,200 additional if new relationship) |
| **Suggested Mitigation** | Confirm surety relationship status early; engage broker if new relationship needed |
| **Contingency Handling** | Partially included in 15% contingency |

---

### R-003: Insurance Scope Expansion

| Field | Value |
|-------|-------|
| **Risk ID** | R-003 |
| **Risk Driver** | Scope uncertainty |
| **Cause** | Insurance approach summary marked "as required"; RFP may require more detailed insurance evidence than assumed |
| **Consequence** | Additional effort for insurance documentation; broker fees may increase |
| **Affected CBS/WBS** | PM (L-004); P (L-009) |
| **Probability** | LOW |
| **Impact** | LOW (CAD $300-$600 additional) |
| **Suggested Mitigation** | Extract RFP Section 5.3.1 to clarify insurance requirements |
| **Contingency Handling** | Included in 15% contingency |

---

### R-004: Third-Party Fee Variability

| Field | Value |
|-------|-------|
| **Risk ID** | R-004 |
| **Risk Driver** | Price uncertainty |
| **Cause** | Surety/broker fees and insurance broker fees are allowances; actual fees may differ |
| **Consequence** | Fees may be higher or lower than estimated; some may be waived |
| **Affected CBS/WBS** | P (L-008, L-009) |
| **Probability** | MEDIUM |
| **Impact** | LOW (CAD $0-$500 variance) |
| **Suggested Mitigation** | Confirm fee structure with surety and insurance brokers |
| **Contingency Handling** | Included in 15% contingency |

---

### R-005: Cross-Document Reconciliation Issues

| Field | Value |
|-------|-------|
| **Risk ID** | R-005 |
| **Risk Driver** | Interface/coordination |
| **Cause** | Bond costs must reconcile with DEL-05-01/02 (Appendix H pricing); discrepancies require resolution |
| **Consequence** | Additional effort to resolve discrepancies; potential rework on multiple deliverables |
| **Affected CBS/WBS** | PM (L-003, L-005); E (L-007) |
| **Probability** | MEDIUM |
| **Impact** | LOW (CAD $200-$600 additional coordination) |
| **Suggested Mitigation** | Early coordination between Proposal Manager and Estimator; single source of truth for bond costs |
| **Contingency Handling** | Included in 15% contingency |

---

### R-006: Compliance Non-Conformance

| Field | Value |
|-------|-------|
| **Risk ID** | R-006 |
| **Risk Driver** | Scope/interface |
| **Cause** | DEL-01-03 is a high compliance risk item; deficiencies may result in proposal disqualification |
| **Consequence** | Proposal rejection; loss of bid opportunity |
| **Affected CBS/WBS** | All line items (compliance failure) |
| **Probability** | LOW (with proper execution) |
| **Impact** | CRITICAL (proposal disqualification) |
| **Suggested Mitigation** | Rigorous QC per Procedure Step 6; early extraction of RFP requirements; multiple review cycles |
| **Contingency Handling** | Cost contingency does not address schedule/compliance risk; mitigation through process quality |

---

## Risk Summary Matrix

| Risk ID | Probability | Impact | Risk Level |
|---------|-------------|--------|------------|
| R-001 | MEDIUM | MEDIUM | MODERATE |
| R-002 | LOW | MEDIUM | LOW-MODERATE |
| R-003 | LOW | LOW | LOW |
| R-004 | MEDIUM | LOW | LOW-MODERATE |
| R-005 | MEDIUM | LOW | LOW-MODERATE |
| R-006 | LOW | CRITICAL | MODERATE (due to severity) |

---

## Contingency Allocation Rationale

| Factor | Contribution to Contingency |
|--------|----------------------------|
| Scope uncertainty (RFP TBD items) | 7% |
| Effort variability (allowance-based) | 5% |
| Third-party fee uncertainty | 3% |
| **Total Contingency** | **15%** |

The 15% contingency is appropriate for a Class 5 estimate with multiple TBD items and no rate table support. If RFP requirements are fully extracted and scope is clarified, contingency could be reduced to 10% in future snapshots.
