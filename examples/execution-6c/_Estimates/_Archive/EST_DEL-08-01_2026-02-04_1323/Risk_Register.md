# Risk Register
## DEL-08-01: DetailedProjectSchedule

---

## Purpose

This register documents risks identified during estimate development that may affect the accuracy or completeness of the estimate, and forms the basis for contingency allocation.

---

## Risks

### R-001: Labour Rate Uncertainty

| Field | Value |
|-------|-------|
| **Risk ID** | R-001 |
| **Risk Driver** | Price |
| **Cause** | No rate tables provided; hourly rates based on market assumptions |
| **Consequence** | Actual firm rates may be higher or lower than assumed, affecting estimate accuracy |
| **Affected CBS** | E, PM |
| **Affected WBS** | PKG-08, DEL-08-01 |
| **Probability** | Medium |
| **Impact** | Medium |
| **Suggested Mitigation** | Provide actual firm billing rates in _RateTables/ |
| **Contingency Handling** | Included in 15% contingency on base estimate |

---

### R-002: RFP Section 7.1.9 Unknown Requirements

| Field | Value |
|-------|-------|
| **Risk ID** | R-002 |
| **Risk Driver** | Scope |
| **Cause** | RFP Section 7.1.9 marked as "location TBD" - specific schedule requirements unknown |
| **Consequence** | Additional effort may be required to meet RFP-specific format, software, or content requirements |
| **Affected CBS** | E |
| **Affected WBS** | PKG-08, DEL-08-01 |
| **Probability** | Medium |
| **Impact** | Medium |
| **Suggested Mitigation** | Obtain and review RFP Section 7.1.9 before schedule development |
| **Contingency Handling** | Included in 15% contingency; specific requirement may trigger scope change |

---

### R-003: Cross-Deliverable Coordination Complexity

| Field | Value |
|-------|-------|
| **Risk ID** | R-003 |
| **Risk Driver** | Interface |
| **Cause** | Schedule must align with 5+ other deliverables (DEL-02-01, DEL-04-01, DEL-05-01/02, DEL-06-01, DEL-09-01) |
| **Consequence** | Inconsistencies discovered during coordination may require schedule rework |
| **Affected CBS** | PM, E |
| **Affected WBS** | PKG-08, DEL-08-01 |
| **Probability** | Medium |
| **Impact** | Low-Medium |
| **Suggested Mitigation** | Early coordination meetings; establish baseline assumptions before detailed development |
| **Contingency Handling** | 20% rework factor (L-019) covers coordination-driven revisions |

---

### R-004: Peer Review Rework

| Field | Value |
|-------|-------|
| **Risk ID** | R-004 |
| **Risk Driver** | Productivity |
| **Cause** | QA peer review (REQ-SCH-002) may identify duration or logic issues requiring revision |
| **Consequence** | Additional scheduler effort to address review comments |
| **Affected CBS** | E |
| **Affected WBS** | PKG-08, DEL-08-01 |
| **Probability** | High |
| **Impact** | Low |
| **Suggested Mitigation** | Use historical project data for duration benchmarking; involve reviewer early |
| **Contingency Handling** | 20% rework factor (L-019) covers review-driven revisions |

---

### R-005: Schedule Software Compatibility

| Field | Value |
|-------|-------|
| **Risk ID** | R-005 |
| **Risk Driver** | Productivity |
| **Cause** | RFP may require specific scheduling software (P6 vs MS Project); firm may need to adapt |
| **Consequence** | Additional time for software learning curve or conversion between platforms |
| **Affected CBS** | E |
| **Affected WBS** | PKG-08, DEL-08-01 |
| **Probability** | Low |
| **Impact** | Low |
| **Suggested Mitigation** | Confirm RFP Section 7.1.9 software requirements; maintain capability in both platforms |
| **Contingency Handling** | Included in 15% contingency |

---

### R-006: Historical Data Availability

| Field | Value |
|-------|-------|
| **Risk ID** | R-006 |
| **Risk Driver** | Scope |
| **Cause** | Duration benchmarking relies on firm historical data for comparable municipal Design-Build projects |
| **Consequence** | If no comparable projects, duration justification may be weaker; evaluator scrutiny |
| **Affected CBS** | E, PM |
| **Affected WBS** | PKG-08, DEL-08-01 |
| **Probability** | Low-Medium |
| **Impact** | Low |
| **Suggested Mitigation** | Compile firm project archive before schedule development; use industry benchmarks as backup |
| **Contingency Handling** | Included in peer review verification effort |

---

## Contingency Summary

| Risk-Based Factor | Applied Rate | Rationale |
|-------------------|--------------|-----------|
| **Base Contingency** | 15% | Moderate uncertainty from rate assumptions, RFP unknowns, coordination complexity |
| **Rework Factor** | 20% of development | High probability of review-driven revisions |

**Total Contingency Allocation:** CAD $1,500 (15% of $10,550 base)

---

## Risk Matrix

| Risk ID | Probability | Impact | Risk Level |
|---------|-------------|--------|------------|
| R-001 | Medium | Medium | Medium |
| R-002 | Medium | Medium | Medium |
| R-003 | Medium | Low-Medium | Low-Medium |
| R-004 | High | Low | Low-Medium |
| R-005 | Low | Low | Low |
| R-006 | Low-Medium | Low | Low |

---

## Document Control

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-08-01_2026-02-04_1323 |
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
