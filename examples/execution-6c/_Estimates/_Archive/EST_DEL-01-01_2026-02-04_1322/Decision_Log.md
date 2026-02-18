# Decision Log
## DEL-01-01: ComplianceMatrixAndChecklist Estimate

---

## Purpose

This log records all decisions made during estimate preparation where:
- A default was applied due to missing input
- An ambiguity required interpretation
- A conflict required resolution
- A selection was made between alternatives

---

## Decision Register

### D-001: Currency Selection

| Property | Value |
|----------|-------|
| **Decision ID** | D-001 |
| **Decision** | Use CAD as estimate currency |
| **Trigger** | Operator directive specified CAD in task brief |
| **Evidence** | Task brief: "Currency: CAD" |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | All amounts in CAD |
| **Override Method** | Provide different currency directive in _CONFIG.md or task brief |

---

### D-002: Pricing Date Selection

| Property | Value |
|----------|-------|
| **Decision ID** | D-002 |
| **Decision** | Use 2026-02 as pricing date |
| **Trigger** | No explicit pricing date in documents |
| **Evidence** | Default per AGENT_ESTIMATING protocol: use current month |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | Rates reflect February 2026 dollars |
| **Override Method** | Specify pricing_date in _CONFIG.md |

---

### D-003: CBS Mapping - Engineering vs PM

| Property | Value |
|----------|-------|
| **Decision ID** | D-003 |
| **Decision** | Map document creation/extraction to Engineering (E); map oversight/reviews to PM |
| **Trigger** | Deliverable type is Compliance Document - could map to E or PM |
| **Evidence** | Datasheet.md: Type = Compliance Document; Discipline = Proposal Management |
| **Impacted WBS/CBS** | Lines L-001 through L-011 |
| **Estimate Impact** | 60% E, 18% PM split (before contingency) |
| **Override Method** | Provide CBS mapping guidance in _CONFIG.md |

---

### D-004: Contingency Method and Rate

| Property | Value |
|----------|-------|
| **Decision ID** | D-004 |
| **Decision** | Apply 15% contingency using PCT_BY_BUCKET method |
| **Trigger** | No contingency guidance in documents; default per protocol |
| **Evidence** | AGENT_ESTIMATING default: PCT_BY_BUCKET method |
| **Impacted WBS/CBS** | CONT category |
| **Estimate Impact** | +CAD $1,100 (15% of $7,250 base) |
| **Override Method** | Specify contingency_method and percentage in _CONFIG.md |

---

### D-005: Labour Rate Basis

| Property | Value |
|----------|-------|
| **Decision ID** | D-005 |
| **Decision** | Use fully-burdened hourly rates (no separate overhead) |
| **Trigger** | No rate tables available; need pricing basis |
| **Evidence** | Empty _RateTables/ folder; protocol fallback to allowances |
| **Impacted WBS/CBS** | All labour lines |
| **Estimate Impact** | Rates include overhead, benefits, etc. |
| **Override Method** | Provide rate tables in _RateTables/ folder |

---

### D-006: Effort Estimation Methodology

| Property | Value |
|----------|-------|
| **Decision ID** | D-006 |
| **Decision** | Use parametric approach: hours per requirement/item |
| **Trigger** | No detailed task breakdown available |
| **Evidence** | Specification.md provides requirement counts; typical proposal effort ratios |
| **Impacted WBS/CBS** | Lines L-001, L-002, L-003 |
| **Estimate Impact** | ~0.3 hrs/requirement for extraction/mapping |
| **Override Method** | Provide detailed task breakdown or historical data |

---

### D-007: Milestone Review Scope

| Property | Value |
|----------|-------|
| **Decision ID** | D-007 |
| **Decision** | Include 3 milestone reviews (50%, 90%, final) |
| **Trigger** | Procedure.md describes milestone reviews; need to estimate effort |
| **Evidence** | Procedure.md Steps 14, 17; Guidance.md Trade-off 2 |
| **Impacted WBS/CBS** | Lines L-006, L-007, L-008 |
| **Estimate Impact** | 7 hours for milestone reviews |
| **Override Method** | Specify review cadence in task brief |

---

### D-008: Living Document Maintenance Estimate

| Property | Value |
|----------|-------|
| **Decision ID** | D-008 |
| **Decision** | Estimate maintenance effort at 20% of initial creation |
| **Trigger** | Guidance.md Principle 5 describes living document; need to estimate updates |
| **Evidence** | Typical document maintenance ratio; no specific guidance |
| **Impacted WBS/CBS** | Line L-009 |
| **Estimate Impact** | 8 hours for ongoing updates |
| **Override Method** | Provide historical data on maintenance effort |

---

### D-009: Rounding Policy

| Property | Value |
|----------|-------|
| **Decision ID** | D-009 |
| **Decision** | Round to nearest CAD $100 |
| **Trigger** | Default per protocol |
| **Evidence** | AGENT_ESTIMATING default: appropriate for professional services |
| **Impacted WBS/CBS** | Summary totals |
| **Estimate Impact** | Minor rounding adjustments |
| **Override Method** | Specify rounding in _CONFIG.md |

---

### D-010: Escalation Mode

| Property | Value |
|----------|-------|
| **Decision ID** | D-010 |
| **Decision** | No escalation applied (NONE mode) |
| **Trigger** | Default per protocol for short-duration work |
| **Evidence** | Proposal phase work; completion before major cost escalation |
| **Impacted WBS/CBS** | N/A |
| **Estimate Impact** | No escalation adjustment |
| **Override Method** | Set escalation_mode=EXPLICIT in _CONFIG.md |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Decisions | 10 |
| Defaults Applied | 7 |
| Ambiguities Resolved | 2 |
| Conflicts Resolved | 1 |

---

## Document Control

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-01-01_2026-02-04_1322 |
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
