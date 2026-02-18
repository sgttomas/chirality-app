# Risk Register (Estimate Risks)

## Snapshot Identification

| Field | Value |
|-------|-------|
| **Snapshot ID** | EST_DEL-09-01_2026-02-04_1323 |
| **Deliverable** | DEL-09-01 Risk Register and Mitigation Plan |

---

## Estimate Risk Summary

| Risk ID | Category | Description | P | I | Score | Mitigation | Owner |
|---------|----------|-------------|---|---|-------|------------|-------|
| R-001 | Pricing | 100% ALLOWANCE pricing basis | 5 | 3 | 15 | 15% contingency applied; flag for rate table development | PM |
| R-002 | Scope | Workshop duration may exceed 4 hours | 3 | 2 | 6 | Monitor actual duration; adjust if exceeds | PM |
| R-003 | Scope | Risk count may exceed assumed 20 | 3 | 2 | 6 | Procedure allows for scaled effort | PM |
| R-004 | Resource | Technical Lead availability during proposal crunch | 3 | 3 | 9 | Schedule workshop early in proposal cycle | PM |
| R-005 | Coordination | Cross-deliverable consistency check depends on sibling deliverable availability | 3 | 2 | 6 | Sequence DEL-09-01 after DEL-09-02, DEL-05-03, DEL-08-01 | PM |

---

## Detailed Risk Entries

### R-001: 100% ALLOWANCE Pricing Basis

| Field | Value |
|-------|-------|
| **Risk ID** | R-001 |
| **Category** | Pricing |
| **Description** | All line items priced using ALLOWANCE method due to absence of rate tables; actual costs may vary significantly from estimates |
| **Probability** | 5 (Very High) - Certainty that allowances are used |
| **Impact** | 3 (Medium) - Professional services cost variance typically 10-30% |
| **Score** | 15 (High Priority) |
| **Cause** | No rate tables available in _RateTables/; no vendor quotes for professional services |
| **Consequence** | Actual costs may be 10-30% higher or lower than estimate |
| **Mitigation - Preventive** | Flag for rate table development; request PM/Technical Lead hourly rates |
| **Mitigation - Contingency** | 15% contingency applied to absorb variance |
| **Owner** | PM |
| **Status** | Active |

---

### R-002: Workshop Duration Overrun

| Field | Value |
|-------|-------|
| **Risk ID** | R-002 |
| **Category** | Scope |
| **Description** | Risk identification workshop may exceed assumed 4-hour duration due to complexity of 7 risk categories |
| **Probability** | 3 (Medium) - Some workshops extend; depends on team efficiency |
| **Impact** | 2 (Low) - Additional 1-2 hours would add ~$500-$1,000 |
| **Score** | 6 (Low Priority) |
| **Cause** | 7 risk categories to cover; comprehensive discussion expected |
| **Consequence** | Additional workshop time increases labor cost |
| **Mitigation - Preventive** | Pre-workshop preparation to ensure efficient use of workshop time |
| **Mitigation - Contingency** | Monitor actual duration; accept minor overrun within contingency |
| **Owner** | PM |
| **Status** | Active |

---

### R-003: Risk Count Exceeds Assumption

| Field | Value |
|-------|-------|
| **Risk ID** | R-003 |
| **Category** | Scope |
| **Description** | Actual risk count may exceed assumed ~20 risks, increasing assessment and mitigation effort |
| **Probability** | 3 (Medium) - Comprehensive risk ID often yields more risks than expected |
| **Impact** | 2 (Low) - Marginal effort increase per additional risk |
| **Score** | 6 (Low Priority) |
| **Cause** | Comprehensive coverage of 7 categories plus hard constraints |
| **Consequence** | Additional effort for assessment and mitigation documentation |
| **Mitigation - Preventive** | Procedure allows scaling effort based on actual risk count |
| **Mitigation - Contingency** | Use summary mitigation for additional low-priority risks |
| **Owner** | PM |
| **Status** | Active |

---

### R-004: Technical Lead Availability

| Field | Value |
|-------|-------|
| **Risk ID** | R-004 |
| **Category** | Resource |
| **Description** | Technical Leads may have limited availability during proposal crunch period, delaying or compressing risk workshop |
| **Probability** | 3 (Medium) - Common during proposal deadlines |
| **Impact** | 3 (Medium) - Delay could affect proposal assembly timeline |
| **Score** | 9 (Medium Priority) |
| **Cause** | Multiple deliverables competing for Technical Lead time |
| **Consequence** | Workshop compressed or rescheduled; quality may suffer |
| **Mitigation - Preventive** | Schedule workshop early in proposal cycle before deadline pressure |
| **Mitigation - Contingency** | PM can lead with subset of leads; others provide async input |
| **Owner** | PM |
| **Status** | Active |

---

### R-005: Cross-Deliverable Consistency Dependency

| Field | Value |
|-------|-------|
| **Risk ID** | R-005 |
| **Category** | Coordination |
| **Description** | Cross-deliverable consistency check depends on sibling deliverables (DEL-09-02, DEL-05-03, DEL-08-01) being available |
| **Probability** | 3 (Medium) - Sibling deliverables may not be ready when DEL-09-01 is complete |
| **Impact** | 2 (Low) - Consistency check can be deferred; minor rework if needed |
| **Score** | 6 (Low Priority) |
| **Cause** | Deliverables developed in parallel; sequence not formally tracked |
| **Consequence** | May need iteration on DEL-09-01 after sibling deliverables available |
| **Mitigation - Preventive** | Coordinate deliverable sequencing; develop DEL-09-01 after key sibling drafts |
| **Mitigation - Contingency** | Accept minor rework; include review buffer in schedule |
| **Owner** | PM |
| **Status** | Active |

---

## Contingency Calculation

| Method | PCT_BY_BUCKET |
|--------|---------------|
| **Base Estimate** | $20,500 |
| **Contingency Rate** | 15% |
| **Contingency Amount** | $3,000 (rounded) |
| **Rationale** | Elevated contingency (15% vs 10%) due to R-001 (100% ALLOWANCE basis) |

---

## Risk Register Summary

| Metric | Value |
|--------|-------|
| Total Risks Identified | 5 |
| High Priority (>=15) | 1 |
| Medium Priority (8-14) | 1 |
| Low Priority (<8) | 3 |
| Contingency Coverage | 15% |

---

**Generated:** 2026-02-04 13:23
**Agent:** ESTIMATING (Type 2)
