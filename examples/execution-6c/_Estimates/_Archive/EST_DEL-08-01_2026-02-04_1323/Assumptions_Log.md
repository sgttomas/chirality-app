# Assumptions Log
## DEL-08-01: DetailedProjectSchedule

---

## Purpose

This log records all assumptions and allowances used in the estimate where:
- A source document was not available
- A value was estimated parametrically
- An allowance was carried for undefined scope
- Industry benchmarks were applied

---

## Assumptions

### A-001: Scheduler Hourly Rate

| Field | Value |
|-------|-------|
| **Assumption ID** | A-001 |
| **Statement** | Scheduler hourly rate is CAD $125/hr (fully burdened) |
| **Why Needed** | No rate tables provided; professional services rate required |
| **Impacted WBS/CBS** | E category - all scheduler labour |
| **Cost Impact** | CAD $7,500 (60 hours at $125/hr) |
| **Confidence** | MEDIUM |
| **Resolution Path** | Provide firm billing rates in _RateTables/ |

---

### A-002: Senior Scheduler/PM Hourly Rate

| Field | Value |
|-------|-------|
| **Assumption ID** | A-002 |
| **Statement** | Senior Scheduler/PM hourly rate is CAD $150/hr (fully burdened) |
| **Why Needed** | No rate tables provided; review and approval labour required |
| **Impacted WBS/CBS** | PM category - peer review and sign-off |
| **Cost Impact** | CAD $1,650 (11 hours at $150/hr) |
| **Confidence** | MEDIUM |
| **Resolution Path** | Provide firm billing rates in _RateTables/ |

---

### A-003: Technical Lead Hourly Rate

| Field | Value |
|-------|-------|
| **Assumption ID** | A-003 |
| **Statement** | Technical Lead hourly rate is CAD $140/hr (fully burdened) |
| **Why Needed** | No rate tables provided; coordination meeting labour required |
| **Impacted WBS/CBS** | PM category - cross-deliverable coordination |
| **Cost Impact** | CAD $1,400 (10 hours at $140/hr) |
| **Confidence** | MEDIUM |
| **Resolution Path** | Provide firm billing rates in _RateTables/ |

---

### A-004: Fully Burdened Rates

| Field | Value |
|-------|-------|
| **Assumption ID** | A-004 |
| **Statement** | All hourly rates include benefits, overhead, and profit (fully burdened) |
| **Why Needed** | Standard consulting practice; simplifies estimate |
| **Impacted WBS/CBS** | All labour line items |
| **Cost Impact** | N/A (embedded in rates) |
| **Confidence** | HIGH |
| **Resolution Path** | N/A |

---

### A-005: WBS Development Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-005 |
| **Statement** | WBS development requires 8 hours for 6 major phases and Level 2/3 breakdown |
| **Why Needed** | Parametric estimate based on typical Design-Build project complexity |
| **Impacted WBS/CBS** | E category - L-001 |
| **Cost Impact** | CAD $1,000 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track actual effort on similar schedule deliverables |

---

### A-006: Duration Assignment Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-006 |
| **Statement** | Duration assignment requires ~0.1 hours per activity (12 hours for 100 activities + research) |
| **Why Needed** | Parametric estimate; includes historical benchmarking research |
| **Impacted WBS/CBS** | E category - L-002 |
| **Cost Impact** | CAD $1,500 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Refine based on actual activity count when WBS finalized |

---

### A-007: Dependency Logic Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-007 |
| **Statement** | Dependency logic mapping requires 8 hours for ~100 activities |
| **Why Needed** | Parametric estimate for CPM schedule logic development |
| **Impacted WBS/CBS** | E category - L-003 |
| **Cost Impact** | CAD $1,000 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track actual effort on similar schedules |

---

### A-008: Critical Path Analysis Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-008 |
| **Statement** | Critical path analysis requires 4 hours for calculation and verification |
| **Why Needed** | Standard scheduling activity using software tools |
| **Impacted WBS/CBS** | E category - L-004 |
| **Cost Impact** | CAD $500 |
| **Confidence** | HIGH |
| **Resolution Path** | N/A |

---

### A-009: Gantt Chart Production Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-009 |
| **Statement** | Gantt chart formatting and PDF export requires 4 hours |
| **Why Needed** | Visual formatting, critical path highlighting, proposal-quality output |
| **Impacted WBS/CBS** | E category - L-005 |
| **Cost Impact** | CAD $500 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Adjust based on software familiarity and output requirements |

---

### A-010: Milestone Summary Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-010 |
| **Statement** | Milestone extraction and documentation requires 4 hours for 12-15 milestones |
| **Why Needed** | Extract from schedule, format table, verify float status |
| **Impacted WBS/CBS** | E category - L-006 |
| **Cost Impact** | CAD $500 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Specification C-006 defines 12-15 milestones |

---

### A-011: Critical Path Narrative Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-011 |
| **Statement** | Critical path narrative (1-2 pages) requires 6 hours to draft |
| **Why Needed** | Technical writing explaining critical path logic and float management |
| **Impacted WBS/CBS** | E category - L-007 |
| **Cost Impact** | CAD $750 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Template from prior proposals could reduce effort |

---

### A-012: Schedule Assumptions Document Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-012 |
| **Statement** | Schedule assumptions compilation requires 6 hours |
| **Why Needed** | Consolidate weather, permitting, procurement, commissioning, addenda assumptions |
| **Impacted WBS/CBS** | E category - L-008 |
| **Cost Impact** | CAD $750 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Per REQ-SCH-008 requirements |

---

### A-013: Addendum Integration Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-013 |
| **Statement** | Addendum 03 integration documentation requires 2 hours |
| **Why Needed** | Document survey post-award constraint and pickled sand building removal |
| **Impacted WBS/CBS** | E category - L-009 |
| **Cost Impact** | CAD $250 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Per REQ-SCH-009 requirements |

---

### A-014: Pricing Coordination Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-014 |
| **Statement** | Coordination with DEL-05-01/02 (Pricing) requires 3 hours |
| **Why Needed** | Align schedule duration with general conditions and escalation per REQ-SCH-010 |
| **Impacted WBS/CBS** | PM category - L-010 |
| **Cost Impact** | CAD $420 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track actual coordination time |

---

### A-015: Methodology Coordination Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-015 |
| **Statement** | Coordination with DEL-04-01 (Construction Methodology) requires 2 hours |
| **Why Needed** | Verify sequencing alignment per Procedure Step 6.2 |
| **Impacted WBS/CBS** | PM category - L-011 |
| **Cost Impact** | CAD $280 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track actual coordination time |

---

### A-016: Commissioning Coordination Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-016 |
| **Statement** | Coordination with DEL-06-01 (Commissioning) requires 2 hours |
| **Why Needed** | Verify commissioning phase duration per REQ-SCH-005 |
| **Impacted WBS/CBS** | PM category - L-012 |
| **Cost Impact** | CAD $280 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track actual coordination time |

---

### A-017: Risk Coordination Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-017 |
| **Statement** | Coordination with DEL-09-01 (Risk Register) requires 2 hours |
| **Why Needed** | Align schedule buffers with identified risks per REQ-SCH-011 |
| **Impacted WBS/CBS** | PM category - L-013 |
| **Cost Impact** | CAD $280 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track actual coordination time |

---

### A-018: Design Coordination Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-018 |
| **Statement** | Coordination with DEL-02-01 (Concept Design) requires 1 hour |
| **Why Needed** | Verify scope alignment per Semantic Lensing F-003 |
| **Impacted WBS/CBS** | PM category - L-014 |
| **Cost Impact** | CAD $140 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track actual coordination time |

---

### A-019: QA Peer Review Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-019 |
| **Statement** | Duration reasonableness peer review requires 4 hours |
| **Why Needed** | REQ-SCH-002 verification per Semantic Lensing X-002 |
| **Impacted WBS/CBS** | PM category - L-015 |
| **Cost Impact** | CAD $600 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Gatekeeping requirement per Procedure Step 10 |

---

### A-020: Dependency Logic Verification Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-020 |
| **Statement** | CPM logic peer review requires 2 hours |
| **Why Needed** | Semantic Lensing D-004 requirement for dependency verification |
| **Impacted WBS/CBS** | PM category - L-016 |
| **Cost Impact** | CAD $300 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Per Procedure Step 4.4a |

---

### A-021: Specification Compliance Check Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-021 |
| **Statement** | REQ-SCH-000 through REQ-SCH-012 verification requires 3 hours |
| **Why Needed** | 13 specification requirements to verify |
| **Impacted WBS/CBS** | PM category - L-017 |
| **Cost Impact** | CAD $450 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Per Specification Verification table |

---

### A-022: Final Sign-off Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-022 |
| **Statement** | Proposal Manager final review and sign-off requires 2 hours |
| **Why Needed** | Final gatekeeping per Procedure Step 10 |
| **Impacted WBS/CBS** | PM category - L-018 |
| **Cost Impact** | CAD $300 |
| **Confidence** | MEDIUM |
| **Resolution Path** | N/A |

---

### A-023: Rework Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-023 |
| **Statement** | Revisions based on peer review feedback require 6 hours (~20% of development effort) |
| **Why Needed** | Typical rework factor for proposal deliverables |
| **Impacted WBS/CBS** | E category - L-019 |
| **Cost Impact** | CAD $750 |
| **Confidence** | LOW |
| **Resolution Path** | Track actual rework on similar deliverables |

---

## Assumptions Summary

| ID | Topic | Confidence | Cost Impact (CAD) |
|----|-------|------------|-------------------|
| A-001 | Scheduler rate | MED | $7,500 |
| A-002 | Senior PM rate | MED | $1,650 |
| A-003 | Technical Lead rate | MED | $1,400 |
| A-004 | Fully burdened rates | HIGH | N/A |
| A-005 | WBS development effort | MED | $1,000 |
| A-006 | Duration assignment effort | MED | $1,500 |
| A-007 | Dependency logic effort | MED | $1,000 |
| A-008 | Critical path analysis effort | HIGH | $500 |
| A-009 | Gantt chart production effort | MED | $500 |
| A-010 | Milestone summary effort | MED | $500 |
| A-011 | Critical path narrative effort | MED | $750 |
| A-012 | Schedule assumptions effort | MED | $750 |
| A-013 | Addendum integration effort | MED | $250 |
| A-014 | Pricing coordination effort | MED | $420 |
| A-015 | Methodology coordination effort | MED | $280 |
| A-016 | Commissioning coordination effort | MED | $280 |
| A-017 | Risk coordination effort | MED | $280 |
| A-018 | Design coordination effort | MED | $140 |
| A-019 | QA peer review effort | MED | $600 |
| A-020 | Dependency logic verification | MED | $300 |
| A-021 | Specification compliance check | MED | $450 |
| A-022 | Final sign-off effort | MED | $300 |
| A-023 | Rework effort | LOW | $750 |

---

## Document Control

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-08-01_2026-02-04_1323 |
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
