# Basis of Estimate (BOE)

## Snapshot Identification

| Attribute | Value |
|---|---|
| **Snapshot ID** | EST_DEL-05-03_2026-02-04_1323 |
| **Estimate Label** | DEL-05-03_PricingNarrativeAndAssumptions |
| **Deliverable** | DEL-05-03 Pricing Narrative and Assumptions |
| **Package** | PKG-02 Financial Proposal (Appendix H) |
| **Pricing Date** | 2026-02 (February 2026 dollars) |
| **Currency** | CAD |
| **RUN_STATUS** | WARNINGS |

## Currency and Conversion

- **Currency:** CAD (Canadian Dollars)
- **Evidence:** Currency specified in INIT-TASK brief
- **Conversion assumptions:** None required (single currency snapshot)
- **Decision:** D-001

## Scope Inclusions

This estimate covers the professional services effort to produce the Pricing Narrative and Assumptions document (DEL-05-03), including:

1. **Document Production**
   - Narrative drafting for 8 canonical sections per Datasheet Content Structure
   - Addenda integration documentation (3 addenda)
   - Allowance explanation and justification
   - Exclusion documentation
   - Additional Options (1-6) pricing basis documentation
   - Value alternatives documentation (SOW-028)
   - Pricing assumptions documentation

2. **Quality and Coordination**
   - Cross-reference to Schedules A/B (DEL-05-01, DEL-05-02)
   - Cross-reference to related deliverables (DEL-02-01, DEL-04-01, DEL-08-01, DEL-09-01, DEL-09-02)
   - Specification requirement verification (R-1 through R-10)
   - Review and approval cycle

## Scope Exclusions

| Exclusion | Rationale | Source |
|---|---|---|
| Numerical pricing (Schedules A/B content) | Separate deliverables DEL-05-01 and DEL-05-02 | Specification Out of Scope |
| Detailed cost breakdowns by trade | Belongs in Schedule B | Specification Out of Scope |
| Design narratives or technical methodology | PKG-04, PKG-05, PKG-06 scope | Specification Out of Scope |
| Team qualifications content | PKG-03 scope | Specification Out of Scope |
| Owner's costs, land, financing | Standard estimating exclusions | D-002 |

## Contracting Assumptions

- **Contract Type:** Design-Build RFP response (fixed-price proposal assumed)
- **Basis:** A-001 - Assumed fixed-price Design-Build proposal per RFP context
- **Delivery:** Part of PKG-02 Financial Proposal submission

## Location and Productivity Assumptions

- **Location:** Alberta, Canada (Central Alberta - Penhold region)
- **Professional rates:** Based on Alberta commercial/estimating professional services market
- **Productivity:** Standard professional services productivity assumed
- **Decision:** D-003

## Pricing Sources Hierarchy

1. **QUOTE:** Not available (no vendor quotes for professional services narrative production)
2. **RATE_TABLE:** Not available (_RateTables directory empty)
3. **ALLOWANCE:** All pricing based on allowance approach
   - Allowances derived from typical Design-Build proposal production effort
   - Confidence: LOW (no rate tables or historical project data available)

## Indirects Model

- **Method:** Factor-based (included in professional services allowances)
- **Indirects included:** Overhead, administrative support, document production
- **Decision:** D-004

## Contingency Method and Rationale

- **Method:** PCT_BY_BUCKET (default)
- **Contingency rate:** 15% applied to base estimate
- **Rationale:** Higher contingency due to:
  - All pricing based on allowances (no rate tables)
  - Multiple TBD items requiring estimator input per documents
  - Scope uncertainty in value alternatives and cross-reference effort
- **Decision:** D-005

## Escalation Method

- **Mode:** NONE (default)
- **Rationale:** Professional services proposal production - short duration, escalation not material
- **Decision:** D-006

## Rounding Policy

- **Rounding:** Nearest CAD $100 (adjusted from default $1,000 due to small deliverable scope)
- **Decision:** D-007

## Completeness Metrics Summary

| Metric | Value |
|---|---|
| % priced by QUOTE | 0% |
| % priced by RATE_TABLE | 0% |
| % priced by ALLOWANCE | 100% |
| % of deliverables with explicit quantities | 30% (narrative sections quantifiable; effort uncertain) |
| **Overall confidence** | LOW |

## Known Gaps

1. **No rate tables available** - All pricing based on professional judgment allowances
2. **TBD items in source documents** - Multiple items marked TBD requiring estimator input:
   - Site servicing allowance value
   - Market pricing date
   - Labor and material availability assumptions
   - Site access and logistics assumptions
   - Long-lead procurement items
   - Contingency percentage and rationale
   - Specific Additional Options scope descriptions
   - Value alternatives content
3. **Cross-deliverable dependencies** - Related deliverables (DEL-05-01, DEL-05-02, DEL-02-01, etc.) status unknown

## References

- **Decision Log:** See Decision_Log.md for all decisions (D-001 through D-007)
- **Assumptions Log:** See Assumptions_Log.md for all assumptions (A-001 through A-008)
- **Risk Register:** See Risk_Register.md for identified risks (R-001 through R-005)
- **Source Index:** See Source_Index.md for source documents and priority
- **QA Report:** See QA_Report.md for quality checks and completeness scoring

---

**Note:** This estimate is a draft scaffold. All line items are priced using allowances due to absence of rate tables. Values require validation by Estimator / Commercial Lead.
