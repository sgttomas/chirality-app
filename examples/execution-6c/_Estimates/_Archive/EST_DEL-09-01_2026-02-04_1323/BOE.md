# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| **Snapshot ID** | EST_DEL-09-01_2026-02-04_1323 |
| **Estimate Label** | DEL-09-01_RiskRegisterAndMitigationPlan |
| **Pricing Date** | 2026-02 (dollars of this month) |
| **Currency** | CAD |
| **Run Status** | WARNINGS |

## Deliverable Summary

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-09-01 |
| **Name** | Risk Register and Mitigation Plan |
| **Package** | PKG-09 Due Diligence & Risk Register |
| **Type** | Register + Plan Document |
| **Responsible** | PM + Technical Leads |
| **Discipline** | Risk Management |

## Scope Inclusions

This estimate covers the preparation of DEL-09-01 Risk Register and Mitigation Plan for the Penhold Public Services Building Design-Build proposal:

1. **Risk Register Development (7 Categories)**
   - Design risks (concept adequacy, program fit, code compliance)
   - Site risks (geotechnical, wetlands, environmental, flood, grading)
   - Cost risks (estimation accuracy, allowances, market conditions, bond costs)
   - Schedule risks (permitting delays, procurement lead times, weather)
   - Procurement risks (subtrade availability, material supply chains)
   - Environmental risks (contamination, wetland permitting, compliance)
   - Permitting risks (building code, development, utility, environmental permits)

2. **Mitigation Plan Development**
   - Preventive actions for each identified risk
   - Contingency plans if risks materialize
   - Monitoring approach and trigger points
   - Risk owner assignment and status tracking

3. **Quality Management Plan (4 QC Areas)**
   - Design QC procedures (5 checkpoints: Concept through 100% CD)
   - Construction QC procedures (4 inspection points: Foundation through Finishes)
   - Commissioning QC requirements (3 verification points)
   - Documentation QC standards (4 review points)

4. **Documentation and Integration**
   - Risk register formatting and compilation
   - QMP formatting and compilation
   - Cross-deliverable consistency review
   - Proposal package integration

**Source:** _CONTEXT.md Description and Anticipated Artifacts; Specification.md Scope

## Scope Exclusions

- Site Conditions and Due Diligence Summary (DEL-09-02)
- Detailed schedule development (DEL-08-01)
- Pricing development or cost estimating (PKG-02 deliverables)
- Design methodology or construction methodology (PKG-05 and PKG-06)
- Post-award risk management execution (estimate covers proposal-phase effort only)

**Source:** Specification.md Out of Scope; D-001

## Contracting Assumptions

| Assumption | Basis | Decision ID |
|------------|-------|-------------|
| Work performed by in-house PM and Technical Leads | _CONTEXT.md Responsible parties | D-002 |
| Proposal-phase effort only; post-award execution excluded | Specification.md scope boundary | D-001 |
| PM acts as risk register coordinator and owner | Procedure.md Personnel and Roles | D-002 |
| Technical Leads provide discipline-specific input part-time | Procedure.md Personnel and Roles | D-002 |
| No external risk management consultant required | ASSUMPTION: typical D-B proposal team capability | A-001 |

## Location / Productivity Assumptions

| Assumption | Basis | Decision ID |
|------------|-------|-------------|
| Work performed in office environment | Standard proposal development setting | D-003 |
| Alberta-based team; no travel required | Project location is Penhold, Alberta; proposal work is office-based | D-003 |
| Productivity assumes experienced D-B proposal team | ASSUMPTION: team familiarity with risk management frameworks | A-002 |

## Pricing Sources Hierarchy

This estimate uses the following pricing approach in priority order:

1. **QUOTE** — Not available (no vendor quotes for professional services)
2. **RATE_TABLE** — Not available (no rate tables in _RateTables/)
3. **ALLOWANCE** — Used for all line items; professional judgment based on scope complexity

**Decision:** All line items priced using ALLOWANCE method with LS (lump sum) convention per D-004.

## Indirects Model

| Category | Treatment | Rationale |
|----------|-----------|-----------|
| Engineering & Design (E) | Direct labor included in line items | Risk register is part of proposal engineering effort |
| Project Management (PM) | Included via PM labor line items | PM coordinates risk identification |
| Overhead (OHP) | Not separately itemized | ASSUMPTION: OH&P embedded in professional services allowances |

**Decision:** Simplified CBS for document deliverable; no construction directs/indirects applicable (D-005).

## Contingency Method

| Method | Value | Rationale |
|--------|-------|-----------|
| **PCT_BY_BUCKET** | 15% | Default contingency for ALLOWANCE-heavy estimate |

**Application:**
- Base estimate uncertainty is MEDIUM due to reliance on professional judgment for effort estimation
- 15% contingency applied to base estimate total
- Higher contingency (15% vs typical 10%) reflects 100% ALLOWANCE pricing basis

**Source:** AGENT_ESTIMATING.md default contingency method; D-006

## Escalation Method

| Method | Treatment |
|--------|-----------|
| **NONE** | Escalation not applied |

**Rationale:** Proposal-phase effort is short duration (< 1 month); no escalation warranted.

## Rounding Policy

- All amounts rounded to nearest CAD $100
- Summary totals rounded to nearest CAD $1,000

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Lines priced by QUOTE | 0% |
| Lines priced by RATE_TABLE | 0% |
| Lines priced by ALLOWANCE | 100% |
| Deliverables with explicit quantities | 0% (quantities derived from scope interpretation) |
| Overall Estimate Confidence | LOW-MEDIUM |

## Known Gaps

| Gap | Impact | Resolution Path |
|-----|--------|-----------------|
| No rate tables for professional services | Must use allowances | Provide PM/Technical Lead hourly rates if available |
| No explicit LOE defined in deliverable docs | Effort estimated from scope complexity | Define expected effort in project brief |
| Workshop duration not specified | Estimated 4 hours based on Procedure.md | Confirm with PM |
| QMP detail level not specified | Estimated moderate detail for proposal | Clarify QMP depth requirement |

## Reference Documents

- Decision_Log.md — All defaulted items and ambiguity resolutions
- Assumptions_Log.md — All allowances and their basis
- Source_Index.md — Discovered pricing/quantity sources
- Risk_Register.md — Cost estimate risks
- QA_Report.md — Quality checks and completeness scoring

---

**Generated:** 2026-02-04 13:23
**Agent:** ESTIMATING (Type 2)
**Status:** WARNINGS (100% ALLOWANCE basis; no rate tables available)
