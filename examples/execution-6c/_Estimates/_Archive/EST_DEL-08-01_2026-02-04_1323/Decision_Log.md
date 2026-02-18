# Decision Log
## DEL-08-01: DetailedProjectSchedule

---

## Purpose

This log records all decisions made during estimate development where:
- A default value was selected in the absence of explicit guidance
- An ambiguity required interpretation
- A conflict between sources required resolution
- A material choice affects the estimate outcome

---

## Decisions

### D-001: Currency Selection

| Field | Value |
|-------|-------|
| **Decision ID** | D-001 |
| **Decision** | Currency set to CAD |
| **Trigger** | Operator directive specified CAD for this estimate |
| **Evidence** | User instruction in task brief |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | All amounts in CAD; no conversion required |
| **Override Path** | Specify different currency in _CONFIG.md or task brief |

---

### D-002: Pricing Basis Selection

| Field | Value |
|-------|-------|
| **Decision ID** | D-002 |
| **Decision** | Use ALLOWANCE method for all line items (no rate tables or quotes available) |
| **Trigger** | _RateTables/ folder is empty; no vendor quotes for professional services |
| **Evidence** | File system check of _Estimates/_RateTables/ |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | 100% of estimate priced by allowance; confidence LOW-MEDIUM |
| **Override Path** | Populate _RateTables/ with firm rate data or provide vendor quotes |

---

### D-003: Labour Rate Assumptions

| Field | Value |
|-------|-------|
| **Decision ID** | D-003 |
| **Decision** | Scheduler rate $125/hr, Senior PM $150/hr, Technical Lead $140/hr |
| **Trigger** | No rate tables provided; professional services rates required |
| **Evidence** | Typical consulting/professional services rates in Alberta market (ASSUMPTION) |
| **Impacted WBS/CBS** | E, PM categories |
| **Estimate Impact** | Base estimate of $10,550 driven by these rates |
| **Override Path** | Provide actual firm billing rates in _RateTables/ |

---

### D-004: Contingency Method and Rate

| Field | Value |
|-------|-------|
| **Decision ID** | D-004 |
| **Decision** | Apply PCT_BY_BUCKET contingency at 15% of base estimate |
| **Trigger** | Default contingency method per AGENT_ESTIMATING protocol |
| **Evidence** | AGENT_ESTIMATING.md STRUCTURE section - default CBS and contingency method |
| **Impacted WBS/CBS** | CONT category |
| **Estimate Impact** | $1,500 contingency added to $10,550 base |
| **Override Path** | Specify contingency_method in _CONFIG.md; provide RISK_BASED inputs |

---

### D-005: Activity Count Assumption

| Field | Value |
|-------|-------|
| **Decision ID** | D-005 |
| **Decision** | Assume 100 schedule activities (midpoint of 50-150 range per Datasheet) |
| **Trigger** | Range provided in Datasheet.md but specific count not determined |
| **Evidence** | Datasheet.md Schedule Structure: "50-150 activities typical for proposal" |
| **Impacted WBS/CBS** | E category (duration assignment effort) |
| **Estimate Impact** | L-002 effort based on 100 activities at 0.1 hr/activity |
| **Override Path** | Provide actual activity count when WBS finalized |

---

### D-006: Cross-Deliverable Coordination Scope

| Field | Value |
|-------|-------|
| **Decision ID** | D-006 |
| **Decision** | Include coordination with 5 deliverables: DEL-02-01, DEL-04-01, DEL-05-01/02, DEL-06-01, DEL-09-01 |
| **Trigger** | Procedure.md Step 6 lists multiple coordination requirements |
| **Evidence** | Procedure.md Steps 6.1-6.5; REQ-SCH-005, REQ-SCH-010, REQ-SCH-011 |
| **Impacted WBS/CBS** | PM category (coordination hours) |
| **Estimate Impact** | 10 hours Technical Lead coordination effort ($1,400) |
| **Override Path** | N/A - coordination required per Specification |

---

### D-007: Rework Factor

| Field | Value |
|-------|-------|
| **Decision ID** | D-007 |
| **Decision** | Apply 20% rework factor for revisions based on peer review feedback |
| **Trigger** | QA peer review (REQ-SCH-002) likely to generate revision requests |
| **Evidence** | Typical proposal development rework rates; Procedure Step 10 gatekeeping requirement |
| **Impacted WBS/CBS** | E category |
| **Estimate Impact** | 6 hours ($750) for revisions |
| **Override Path** | Adjust based on actual firm experience with schedule deliverables |

---

### D-008: RFP Section 7.1.9 Not Accessible

| Field | Value |
|-------|-------|
| **Decision ID** | D-008 |
| **Decision** | Proceed with schedule requirements inferred from decomposition document |
| **Trigger** | RFP Section 7.1.9 marked as "location TBD" in all four documents |
| **Evidence** | Datasheet.md, Specification.md references to "location TBD" |
| **Impacted WBS/CBS** | E category (potential additional requirements) |
| **Estimate Impact** | Contingency captures uncertainty; may require revision if RFP requirements differ |
| **Override Path** | Obtain and review RFP Section 7.1.9 to confirm requirements |

---

## Decision Summary

| Decision ID | Topic | Impact Level |
|-------------|-------|--------------|
| D-001 | Currency (CAD) | Low |
| D-002 | Pricing basis (ALLOWANCE) | Medium |
| D-003 | Labour rates | High |
| D-004 | Contingency (15%) | Medium |
| D-005 | Activity count (100) | Low |
| D-006 | Coordination scope (5 deliverables) | Medium |
| D-007 | Rework factor (20%) | Low |
| D-008 | RFP Section 7.1.9 TBD | Medium |

---

## Document Control

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-08-01_2026-02-04_1323 |
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
