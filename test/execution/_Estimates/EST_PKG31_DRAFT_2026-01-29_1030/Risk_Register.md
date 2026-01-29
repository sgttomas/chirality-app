# Risk Register

**Snapshot ID:** EST_PKG31_DRAFT_2026-01-29_1030

**Package:** PKG-31 Documentation & Deliverables

**Date:** 2026-01-29

---

## Purpose

This register identifies risks that could impact the estimate accuracy or the actual cost of PKG-31 Documentation & Deliverables. Each risk entry includes cause, consequence, affected buckets, and suggested mitigation.

---

## Risk Entries

### R-001: Drawing Count Variance

**Risk Driver:** Scope / Quantity

**Cause → Consequence:**
- **Cause:** Actual drawing count may differ significantly from 275-sheet estimate (±30% variance likely until design is mature)
- **Consequence:** Engineering effort (drafting, as-built incorporation) and printing costs could vary by $20k-$30k base (±30%)

**Affected Buckets:**
- CBS: E (Engineering), MAT (Materials)
- WBS: DEL-31.01, DEL-31.02
- Line Items: L001, L002, L012, L013

**Likelihood:** HIGH (design not yet mature; no confirmed drawing register)

**Impact:** MEDIUM ($20k-30k base variance; 3-4% of total estimate)

**Suggested Mitigation:**
1. Confirm drawing count estimate at 30% design milestone
2. Obtain preliminary drawing register from engineering team (PKG-27)
3. Review VFPA drawing standards to validate typical sheet counts
4. Update estimate if variance exceeds ±15% from baseline

**Contingency Handling:** Covered by 10% Engineering contingency (partially); material variance covered by 25% Materials contingency.

---

### R-002: Equipment Count Variance

**Risk Driver:** Scope / Quantity

**Cause → Consequence:**
- **Cause:** Actual major equipment count may differ from 90-item estimate (70-110 item range likely)
- **Consequence:** Maintenance manual effort and vendor documentation compilation could vary by $80k-$120k base (±35%)

**Affected Buckets:**
- CBS: E (Engineering), PM (Project Management), MAT (Materials)
- WBS: DEL-31.04, DEL-31.05
- Line Items: L004, L005, L015

**Likelihood:** HIGH (equipment list not yet finalized)

**Impact:** HIGH ($80k-120k base variance; 11-16% of total estimate)

**Suggested Mitigation:**
1. Obtain preliminary equipment list from engineering (PKG-27)
2. Cross-check against procurement scope (PKG-15 Pumps, PKG-16 HVAC, etc.)
3. Clarify with Employer what level of equipment requires individual maintenance manuals
4. Update estimate once equipment list is confirmed (target: 60% design milestone)

**Contingency Handling:** Covered by 10% Engineering and PM contingency (partially); significant variance may require estimate update.

---

### R-003: System Breakdown Variance

**Risk Driver:** Scope / Interface

**Cause → Consequence:**
- **Cause:** Operational system breakdown may differ from 12-system estimate (10-15 systems likely)
- **Consequence:** Operation manual development effort could vary by $40k-$80k base (±25-50%)

**Affected Buckets:**
- CBS: E (Engineering), MAT (Materials)
- WBS: DEL-31.03
- Line Items: L003, L014

**Likelihood:** MEDIUM-HIGH (system boundaries not yet defined; interface with commissioning scope PKG-30)

**Impact:** MEDIUM-HIGH ($40k-80k base variance; 5-11% of total estimate)

**Suggested Mitigation:**
1. Review commissioning deliverables (PKG-30) for system breakdown alignment
2. Confirm with Employer what constitutes a "system" for O&M purposes (vs subsystem or component)
3. Coordinate with control systems scope (PKG-19) for control system boundaries
4. Update estimate if actual system count differs by >20%

**Contingency Handling:** Covered by 10% Engineering contingency (partially).

---

### R-004: VFPA Standards Compliance Effort

**Risk Driver:** Productivity / Scope

**Cause → Consequence:**
- **Cause:** VFPA (Vancouver Fraser Port Authority) drawing standards may be more stringent than assumed, requiring additional drafting effort
- **Consequence:** Drawing production rates could decrease (increase hours/sheet), adding $10k-$20k base effort

**Affected Buckets:**
- CBS: E (Engineering)
- WBS: DEL-31.01, DEL-31.02
- Line Items: L001, L002

**Likelihood:** MEDIUM (VFPA standards not yet reviewed; typical port authority standards can be detailed)

**Impact:** LOW-MEDIUM ($10k-20k base variance; 1-3% of total estimate)

**Suggested Mitigation:**
1. Obtain VFPA drawing standards and templates early in design phase
2. Review standards for special requirements (symbology, layering, title blocks, approvals)
3. Adjust production rates if standards require >15% additional effort
4. Engage VFPA early if clarifications needed

**Contingency Handling:** Covered by 10% Engineering contingency.

---

### R-005: As-Built Markup Complexity

**Risk Driver:** Scope / Productivity

**Cause → Consequence:**
- **Cause:** Volume and complexity of field changes during construction may be higher than typical, increasing as-built incorporation effort
- **Consequence:** As-built drawing update effort could increase by $10k-$25k base (+30-80%)

**Affected Buckets:**
- CBS: E (Engineering)
- WBS: DEL-31.02
- Line Items: L002

**Likelihood:** MEDIUM (depends on construction phase change management; design-build typically has fewer changes than design-bid-build)

**Impact:** MEDIUM ($10k-25k base variance; 1-3% of total estimate)

**Suggested Mitigation:**
1. Implement robust field change control process (minimize unnecessary changes)
2. Require field personnel to provide clear, complete markups (reduce rework)
3. Conduct as-built updates progressively during construction (not all at end)
4. Allocate adequate QA review for as-built accuracy

**Contingency Handling:** Covered by 10% Engineering contingency.

---

### R-006: Vendor Documentation Quality/Completeness

**Risk Driver:** Interface / Productivity

**Cause → Consequence:**
- **Cause:** Vendor-supplied documentation may be incomplete, low quality, or require significant reformatting/supplementing
- **Consequence:** PM compilation effort and engineering supplementation effort could increase by $20k-$40k base (+15-30%)

**Affected Buckets:**
- CBS: PM (Project Management), E (Engineering)
- WBS: DEL-31.05
- Line Items: L005

**Likelihood:** MEDIUM-HIGH (vendor documentation quality is variable; some vendors provide minimal docs)

**Impact:** MEDIUM ($20k-40k base variance; 3-5% of total estimate)

**Suggested Mitigation:**
1. Include detailed documentation requirements in equipment purchase specifications (PKG-27)
2. Require vendor documentation submittal and approval before shipment (procurement hold point)
3. Conduct vendor documentation reviews during FAT/shop inspections
4. Budget contingency for supplementing inadequate vendor docs

**Contingency Handling:** Covered by 10% PM and Engineering contingency.

---

### R-007: Asset Hierarchy / CMMS Requirements Complexity

**Risk Driver:** Scope / Interface

**Cause → Consequence:**
- **Cause:** Employer's asset hierarchy and CMMS integration requirements may be more complex than assumed (custom data model, complex integrations)
- **Consequence:** PM effort and software/integration costs could increase by $10k-$30k base (+50-150%)

**Affected Buckets:**
- CBS: PM (Project Management), MAT (Materials)
- WBS: DEL-31.06
- Line Items: L006, L016

**Likelihood:** MEDIUM (requirements not yet detailed by Employer)

**Impact:** LOW-MEDIUM ($10k-30k base variance; 1-4% of total estimate)

**Suggested Mitigation:**
1. Clarify Employer's CMMS platform and data requirements early (kickoff or mobilization)
2. Request Employer's asset hierarchy template/schema if available
3. Confirm data export format (CSV, XML, SQL, API, etc.)
4. Engage CMMS specialist early if integration is complex

**Contingency Handling:** Covered by 10% PM contingency and 25% Materials contingency.

---

### R-008: Printing/Binding Cost Escalation

**Risk Driver:** Price

**Cause → Consequence:**
- **Cause:** Printing/binding market costs may be higher than allowance estimates (no quotes obtained yet)
- **Consequence:** Materials costs could increase by $5k-$15k base (+10-30%)

**Affected Buckets:**
- CBS: MAT (Materials)
- WBS: DEL-31.01, DEL-31.02, DEL-31.03, DEL-31.04
- Line Items: L012, L013, L014, L015

**Likelihood:** LOW-MEDIUM (market typically stable; but large-format printing has limited competition)

**Impact:** LOW ($5k-15k base variance; 1-2% of total estimate)

**Suggested Mitigation:**
1. Obtain budgetary quotes from multiple vendors early
2. Lock in pricing with preferred vendor (advance agreement or framework contract)
3. Consider in-house printing if large volumes justify equipment purchase
4. Confirm delivery schedules to avoid rush charges

**Contingency Handling:** Covered by 25% Materials contingency.

---

## Risk Summary Matrix

| Risk ID | Description | Likelihood | Impact | Affected $ | CBS |
|---------|-------------|------------|--------|------------|-----|
| R-001 | Drawing Count Variance | HIGH | MEDIUM | $20k-30k | E, MAT |
| R-002 | Equipment Count Variance | HIGH | HIGH | $80k-120k | E, PM, MAT |
| R-003 | System Breakdown Variance | MED-HIGH | MED-HIGH | $40k-80k | E, MAT |
| R-004 | VFPA Standards Compliance | MEDIUM | LOW-MED | $10k-20k | E |
| R-005 | As-Built Markup Complexity | MEDIUM | MEDIUM | $10k-25k | E |
| R-006 | Vendor Doc Quality | MED-HIGH | MEDIUM | $20k-40k | E, PM |
| R-007 | CMMS Requirements Complexity | MEDIUM | LOW-MED | $10k-30k | PM, MAT |
| R-008 | Printing Cost Escalation | LOW-MED | LOW | $5k-15k | MAT |

**Total Risk Exposure (base estimate):** $195k to $360k (26% to 48% of base estimate)

**Note:** Risks are not additive (not all will materialize). Contingency allocation ($84k, 11% of base) covers moderate combined risk realization.

---

## Contingency Adequacy Assessment

### Current Contingency Allocation

| CBS Bucket | Base | Contingency % | Contingency $ | Primary Risks Covered |
|------------|------|---------------|---------------|-----------------------|
| Engineering (E) | $472k | 10% | $47k | R-001, R-002, R-003, R-004, R-005, R-006 (partial) |
| PM | $224k | 10% | $22k | R-002, R-006, R-007 |
| MAT | $59k | 25% | $15k | R-001, R-002, R-003, R-007, R-008 |
| **Total** | **$755k** | **11%** | **$84k** | **All risks** |

### Adequacy Analysis

**Scenario 1: Optimistic (Low Risk Realization)**
- Drawing count within ±10%: ~$10k variance
- Equipment/systems within ±15%: ~$40k variance
- Other risks minimal: ~$10k variance
- **Total variance:** ~$60k
- **Contingency adequacy:** ADEQUATE ($84k contingency > $60k variance)

**Scenario 2: Expected (Moderate Risk Realization)**
- Drawing count within ±20%: ~$20k variance
- Equipment/systems within ±25%: ~$80k variance
- VFPA/as-built/vendor doc moderate: ~$30k variance
- **Total variance:** ~$130k
- **Contingency adequacy:** MARGINAL ($84k contingency < $130k variance; ~$50k gap)

**Scenario 3: Pessimistic (High Risk Realization)**
- Drawing count +30%: ~$30k variance
- Equipment/systems +35%: ~$120k variance
- Multiple compounding risks: ~$80k variance
- **Total variance:** ~$230k
- **Contingency adequacy:** INSUFFICIENT ($84k contingency << $230k variance; ~$150k gap)

**Recommendation:**
- Current 11% contingency is adequate for optimistic scenario
- For expected scenario, consider increasing contingency to 15-18% (~$110k-$135k) once equipment/system counts are confirmed
- For pessimistic scenario, estimate update recommended once design matures to 30-60%

---

## Risk Mitigation Plan (Summary)

### Immediate Actions (Before Estimate Update)
1. Engage engineering team to provide preliminary drawing count and equipment list estimates
2. Obtain VFPA drawing standards for review
3. Clarify Employer's CMMS and asset hierarchy requirements
4. Obtain budgetary quotes for printing/binding services

### Short-Term Actions (0-3 Months / Pre-30% Design)
1. Lock in equipment purchase specifications with documentation requirements
2. Confirm system breakdown with commissioning team (PKG-30 alignment)
3. Establish vendor documentation review process

### Medium-Term Actions (30-60% Design Milestone)
1. Update estimate with confirmed drawing counts and equipment lists
2. Adjust contingency based on actual scope variance
3. Re-assess risk register for new/changed risks

---

**Document Control:**
- **Snapshot ID:** EST_PKG31_DRAFT_2026-01-29_1030
- **Author:** ESTIMATING Agent
- **Date:** 2026-01-29 10:30
- **Risk Entries:** R-001 through R-008
- **Total Risk Exposure:** $195k to $360k (26-48% of base)
- **Contingency Allocation:** $84k (11% of base)
