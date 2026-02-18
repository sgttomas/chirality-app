# Basis of Estimate (BOE)

## Estimate Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-07-01_2026-02-04_1323 |
| **Estimate Label** | DEL-07-01 Design-Build Firm Experience Profile |
| **Pricing Date** | 2026-02 (Dollars of February 2026) |
| **Currency** | CAD |
| **RUN_STATUS** | WARNINGS |

## Scope Definition

### Scope Inclusions
- Professional services labor for proposal document preparation
- Document drafting (Proposal Manager)
- Data collection and verification (HR/Team Admin)
- Technical review (Senior PM/Principal)
- Reference coordination and verification
- Cross-deliverable coordination (DEL-07-02, DEL-07-03)
- Quality review and formatting
- Executive review and approval cycle

### Scope Exclusions (Decision D-001)
- Owner's costs for RFP review
- Firm's internal project database maintenance (pre-existing)
- Marketing collateral development (assumed existing)
- Legal review (unless required by firm policy)
- Proposal printing and submission logistics (covered in DEL-01-02)

**Source:** _CONTEXT.md; Decomposition DEL-07-01; D-001

## Contracting Assumptions (Decision D-002)

This estimate assumes:
- Work performed by internal proposal team (no external consultants)
- Standard proposal development timeline (~2-4 weeks for this deliverable within overall proposal schedule)
- Firm has existing project database with required data (access only, no new data entry)
- References are existing client relationships (no new business development required)

**Source:** D-002; Procedure §Prerequisites

## Location and Productivity Assumptions (Decision D-003)

- Work performed at firm's Alberta office(s)
- Standard office productivity rates apply
- No site visits or travel required for this deliverable
- Remote/hybrid work assumed (no location-specific adjustments)

**Source:** D-003

## Pricing Sources Hierarchy

| Priority | Source Type | Availability | Usage |
|----------|-------------|--------------|-------|
| 1 | Vendor quotes | NOT AVAILABLE | N/A |
| 2 | Rate tables | NOT AVAILABLE | N/A |
| 3 | Allowances | USED | All line items |

**Decision D-004:** No rate tables or quotes available. All line items priced using allowance methodology with explicit assumptions. Confidence is LOW for all pricing.

## Indirects Model (Decision D-005)

- Factor-based model applied
- EPCM/PM overhead: 0% (this is proposal cost, not project delivery cost)
- No construction indirects applicable (document preparation only)

## Contingency Method (Decision D-006)

- Method: PCT_BY_BUCKET
- Contingency: 20% applied to all allowance-based line items
- Rationale: High uncertainty due to lack of historical data for proposal preparation costs; scope ambiguity in RFP requirements (RFP not accessible)

## Escalation

- Mode: NONE
- Rationale: Short-duration proposal preparation; no escalation adjustment required

## Rounding Policy

- Rounding: Nearest $100 CAD
- Rationale: Appropriate precision for allowance-based estimate of proposal costs

## Completeness Metrics Summary

| Metric | Value |
|--------|-------|
| % lines priced by QUOTE | 0% |
| % lines priced by RATE_TABLE | 0% |
| % lines priced by ALLOWANCE | 100% |
| % deliverables with explicit quantities | 100% (labor hours estimated) |
| Overall Confidence | LOW |

## Known Gaps

1. **RFP Section 7.1.6 not accessible** - Cannot verify exact content requirements; requirements assumed from Specification
2. **Firm project database not provided** - Cannot verify data availability; labor hours for data collection are estimated
3. **No historical proposal cost data** - Allowances based on typical proposal effort assumptions
4. **Reference verification effort unknown** - Depends on number of references and client availability
5. **OSR (Appendix A) not accessible** - Cannot verify tailoring requirements

## References

- **Decision_Log.md** - All decisions recorded with rationale
- **Assumptions_Log.md** - All assumptions recorded with cost impact
- **Risk_Register.md** - Risks and contingency handling documented
- **Source_Index.md** - Sources for quantities and pricing

---

**Generated:** 2026-02-04
**Agent:** ESTIMATING (Type 2)
