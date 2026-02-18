# Basis of Estimate (BOE)
## DEL-08-01: DetailedProjectSchedule

---

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-08-01_2026-02-04_1323 |
| **Estimate Label** | DEL-08-01_DetailedProjectSchedule |
| **Pricing Date** | 2026-02 (dollars of February 2026) |
| **Currency** | CAD |
| **RUN_STATUS** | WARNINGS |

---

## Scope Definition

### Included Scope

This estimate covers the cost of producing DEL-08-01 DetailedProjectSchedule for the Town of Penhold Public Services Building Design-Build proposal, including:

1. **Detailed Gantt Chart Schedule** (Primary Artifact)
   - Level 2/3 detail (50-150 activities)
   - All project phases: Pre-construction, Design, Procurement, Construction, Commissioning, Closeout
   - Critical path identification and highlighting
   - Dependency logic (Finish-to-Start relationships)
   - 18-24 month target duration per benchmark

2. **Milestone Summary** (12-15 milestones per Specification)
   - Contract award through warranty period start
   - Target dates, predecessors, float status
   - Table or timeline graphic format

3. **Critical Path Narrative** (1-2 pages)
   - Key driving activities explanation
   - Float management approach
   - Risk mitigation strategies for critical path

4. **Schedule Assumptions and Basis**
   - Weather constraints (Alberta climate)
   - Permitting assumptions (8 weeks + 2-week buffer)
   - Procurement lead times (14 weeks for long-lead items)
   - Commissioning duration (10-12 weeks)
   - Addendum 03 impacts (survey post-award, pickled sand building removed)

5. **Cross-Deliverable Coordination**
   - Alignment with DEL-05-01/02 (Pricing)
   - Alignment with DEL-04-01 (Construction Methodology)
   - Alignment with DEL-06-01 (Commissioning Narrative)
   - Alignment with DEL-09-01 (Risk Register)

6. **QA and Peer Review**
   - Duration reasonableness peer review
   - Critical path logic verification
   - REQ-SCH-000 through REQ-SCH-012 compliance check

### Excluded Scope

- Post-award detailed construction schedule (refinement)
- Resource loading / cost-loading the schedule
- Earned value management setup
- Schedule software licensing (firm expense, not project-specific)
- Owner's costs, land acquisition, financing

---

## Currency and Conversion

| Item | Value | Source |
|------|-------|--------|
| **Base Currency** | CAD | Operator directive |
| **Conversion Rate** | N/A | Single currency estimate |
| **Exchange Rate Assumption** | N/A | No foreign currency items |

**Decision Reference:** D-001 (Currency selection)

---

## Scope Inclusions / Exclusions

### Inclusions

| CBS Category | Included | Notes |
|--------------|----------|-------|
| Engineering & Design (E) | YES | Schedule development effort |
| Project Management / EPCM (PM) | YES | Scheduler/PM time, coordination, reviews |
| Procurement (P) | NO | No procurement for this deliverable |
| Equipment & Materials (MAT) | NO | No physical materials |
| Freight / Logistics (FRT) | NO | Not applicable |
| Construction Directs (CD) | NO | Not construction work |
| Construction Indirects (CI) | NO | Not construction work |
| Commissioning (COM) | NO | Not applicable |
| Contingency (CONT) | YES | Uncertainty reserve |

### Exclusions

- Physical construction or installation work
- Equipment procurement
- Site work
- Post-award schedule refinement and updates
- Schedule software licensing costs

---

## Contracting Assumptions

| Assumption | Value | Source |
|------------|-------|--------|
| **Scheduler hourly rate** | CAD $125/hr | A-001 (Scheduler rate allowance) |
| **Senior Scheduler/PM rate** | CAD $150/hr | A-002 (Senior PM rate allowance) |
| **Technical Lead rate** | CAD $140/hr | A-003 (Coordination meeting rate) |
| **Labour basis** | Fully burdened rates | A-004 |
| **Overhead/markup** | Included in hourly rates | A-004 |

---

## Location / Productivity Assumptions

| Factor | Value | Rationale |
|--------|-------|-----------|
| **Work location** | Office-based | Proposal development work |
| **Productivity factor** | 1.0 (standard) | No site or remote work adjustments |
| **Working hours** | 8 hrs/day | Standard office day |

---

## Pricing Sources Hierarchy

This estimate uses the following pricing hierarchy (per AGENT_ESTIMATING protocol):

1. **QUOTE** - Not available (no vendor quotes for professional services)
2. **RATE_TABLE** - Not available (_RateTables/ folder is empty)
3. **ALLOWANCE** - Used for all pricing (see Assumptions_Log.md)

**Pricing Method Distribution:**
- ALLOWANCE: 100%
- RATE_TABLE: 0%
- QUOTE: 0%

---

## Indirects Model

This is a professional services / proposal management deliverable. Indirects are embedded in the fully-burdened hourly rates. No separate construction indirects apply.

---

## Contingency Method and Rationale

| Property | Value |
|----------|-------|
| **Method** | PCT_BY_BUCKET |
| **Engineering/PM Contingency** | 15% |
| **Rationale** | Moderate uncertainty in effort due to: (1) RFP Section 7.1.9 requirements not accessible (TBD), (2) cross-deliverable coordination complexity with 5+ deliverables, (3) potential rework from peer review cycles |

**Decision Reference:** D-004

---

## Escalation Method

| Property | Value |
|----------|-------|
| **Mode** | NONE |
| **Rationale** | Short-duration work (proposal phase); no escalation adjustment needed |

---

## Rounding Policy

| Property | Value |
|----------|-------|
| **Rounding** | Nearest CAD $100 |
| **Rationale** | Appropriate precision for professional services estimate at Class 5/4 maturity |

---

## Completeness Metrics Summary

| Metric | Value |
|--------|-------|
| **Lines priced by QUOTE** | 0% |
| **Lines priced by RATE_TABLE** | 0% |
| **Lines priced by ALLOWANCE** | 100% |
| **Deliverables with explicit quantities** | 100% (1 of 1) |
| **Confidence Level** | LOW-MEDIUM |

---

## Known Gaps

1. **No rate tables available** - All pricing based on allowance assumptions
2. **RFP Section 7.1.9 not accessible** - Schedule requirements inferred from decomposition
3. **Historical project data TBD** - Duration benchmarking assumed from typical municipal Design-Build (18-24 months)
4. **Software licensing** - MS Project or Primavera P6 licensing not included (assumed firm asset)
5. **Cross-deliverable coordination effort** - Estimated based on 5+ interfacing deliverables

---

## References

- **Decision_Log.md** - All defaulted items and ambiguity resolutions
- **Assumptions_Log.md** - All allowance/assumption entries
- **Risk_Register.md** - Contingency basis
- **Source_Index.md** - Source documents used

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
| **Snapshot** | EST_DEL-08-01_2026-02-04_1323 |
