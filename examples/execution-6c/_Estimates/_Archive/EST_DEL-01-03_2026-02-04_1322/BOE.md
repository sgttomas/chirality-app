# Basis of Estimate (BOE)

## Estimate Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-01-03_2026-02-04_1322 |
| **Estimate Label** | DEL-01-03_BondingAndInsuranceEvidence |
| **Pricing Date** | 2026-02 (dollars of February 2026) |
| **Currency** | CAD |
| **Run Status** | WARNINGS |

---

## Scope Inclusions

This estimate covers **DEL-01-03 Bonding and Insurance Evidence** from PKG-01 Compliance & Submission:

1. **Agreement to Bond (Proposal Stage)**
   - Surety commitment letter confirming capacity to bond the project
   - Coordination with surety company or broker
   - Document preparation and QC review

2. **Bond Cost Inclusion Statement**
   - Explicit statement confirming bond costs are included in proposal pricing
   - Reconciliation with Appendix H Schedule A and Schedule B

3. **Insurance Approach Summary (conditional)**
   - Summary of insurance coverage approach (if required by RFP Section 5.3.1)
   - Coordination with insurance broker

4. **Administrative and Compliance Activities**
   - Proposal Manager coordination time
   - Estimator/Commercial Lead time for bond cost estimation
   - Final QC and approval process

---

## Scope Exclusions

- Final bond issuance (post-award activity)
- Detailed insurance certificates (contract-stage deliverable)
- Subcontractor bonding or insurance
- **Actual bond premiums** (these are project-level costs in pricing deliverables DEL-05-01/02, not this administrative deliverable)
- Construction or engineering work

---

## Currency and Conversion

| Property | Value | Source |
|----------|-------|--------|
| **Estimate Currency** | CAD | User-specified in task brief |
| **Conversion Assumptions** | None | Single currency snapshot |

**Decision:** D-001 - Currency set to CAD per task brief.

---

## Contracting Assumptions

| Assumption | Value | Source |
|------------|-------|--------|
| **Proponent Role** | Prime Design-Builder | _CONTEXT.md |
| **Contract Type** | Design-Build | Decomposition document |
| **Bond Types** | Performance bond + Labor and material payment bond | Datasheet (ASSUMPTION) |
| **Surety Relationship** | Existing (established relationship assumed) | A-001 |

---

## Location / Productivity Assumptions

| Assumption | Value | Source |
|------------|-------|--------|
| **Project Location** | Penhold, Alberta, Canada | RFP 2024_004 |
| **Labor Market** | Alberta professional services rates | A-002 |
| **Surety Processing Time** | 1-2 weeks (existing relationship) | Guidance.md |

---

## Pricing Sources Hierarchy

For this deliverable, pricing sources are applied in the following priority order:

1. **QUOTE** - Not available (no vendor quotes for this administrative deliverable)
2. **RATE_TABLE** - Not available (no rate tables in _RateTables/)
3. **ALLOWANCE** - **Primary method used** (all line items priced via allowances)

**Decision:** D-002 - All line items priced using ALLOWANCE method due to absence of rate tables or quotes.

---

## Indirects Model

| Category | Treatment | Rationale |
|----------|-----------|-----------|
| **Construction Directs** | N/A | This is not a construction deliverable |
| **Construction Indirects** | N/A | This is not a construction deliverable |
| **EPCM/PM Overhead** | Not separately applied | Professional services allowances are fully-burdened |

**Decision:** D-003 - Indirects not separately applied; allowances represent fully-burdened professional service costs.

---

## Contingency Method and Rationale

| Property | Value |
|----------|-------|
| **Method** | PCT_BY_BUCKET (default) |
| **Contingency Rate** | 15% applied to base estimate |
| **Rationale** | Moderate uncertainty due to: (1) RFP Section 5.3.1 not fully extracted (TBD items), (2) Surety relationship status unknown, (3) Insurance requirements conditional |

**Decision:** D-004 - 15% contingency applied to account for scope uncertainty from unresolved TBD items.

---

## Escalation Method

| Property | Value |
|----------|-------|
| **Escalation Mode** | NONE |
| **Rationale** | Short-term proposal-stage work; escalation not material |

---

## Rounding Policy

| Property | Value |
|----------|-------|
| **Rounding** | Nearest CAD $100 |
| **Rationale** | Appropriate precision for small professional services scope |

---

## Completeness Metrics Summary

| Metric | Value |
|--------|-------|
| % of lines priced by QUOTE | 0% |
| % of lines priced by RATE_TABLE | 0% |
| % of lines priced by ALLOWANCE | 100% |
| % of deliverables with explicit quantities | 0% (no material quantities; effort-based) |

---

## Known Gaps

1. **RFP Section 5.3.1** - Not accessible (PDF read failed); specific bond percentages, insurance types, and format requirements marked TBD
2. **Surety Relationship Status** - Unknown whether established or new relationship (affects timeline and possibly cost)
3. **Contract Value Range** - Not provided; required for accurate bond cost estimation (though bond premiums are in pricing deliverables, not here)
4. **Insurance Requirements** - Conditional ("as required") - scope may change based on RFP extraction

---

## References

- **Decision Log:** `Decision_Log.md` - Records all choices made during estimate preparation
- **Assumptions Log:** `Assumptions_Log.md` - Records all assumptions underlying cost estimates
- **Source Index:** `Source_Index.md` - Lists all source documents referenced

---

## Prepared By

| Property | Value |
|----------|-------|
| **Agent** | ESTIMATING (Type 2) |
| **Date** | 2026-02-04 |
| **Version** | Initial snapshot |
