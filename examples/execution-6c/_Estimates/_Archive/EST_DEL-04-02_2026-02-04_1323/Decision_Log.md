# Decision Log
## DEL-04-02: Budget Control and Change Management Plan

---

## Decision Index

| ID | Decision | Trigger | Impact |
|----|----------|---------|--------|
| D-001 | Currency set to CAD | Operator directive | Baseline |
| D-002 | Pricing date 2026-02 | Default (today) | Baseline |
| D-003 | CBS mapping to E + PM | Document type (Plan) | Structure |
| D-004 | Contingency 15% by bucket | Default method | $1,247 |
| D-005 | Escalation NONE | Short-duration work | Baseline |
| D-006 | Rounding to nearest $100 | Estimate maturity | Presentation |
| D-007 | Effort allocation per section | Procedure.md structure | Quantities |

---

## Decision Details

### D-001: Currency Selection

| Property | Value |
|----------|-------|
| **Decision** | Currency set to CAD (Canadian Dollars) |
| **Trigger** | Operator directive specified CAD |
| **Evidence** | Task assignment: "Currency: CAD" |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | Baseline currency for all pricing |
| **How to Override** | Specify different currency in _CONFIG.md or task brief |

---

### D-002: Pricing Date

| Property | Value |
|----------|-------|
| **Decision** | Pricing date set to 2026-02 (February 2026) |
| **Trigger** | No explicit pricing date in documents; default to today |
| **Evidence** | No pricing date found in Datasheet.md or Specification.md |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | Establishes "dollars of" baseline |
| **How to Override** | Specify pricing_date in _CONFIG.md |

---

### D-003: CBS Mapping

| Property | Value |
|----------|-------|
| **Decision** | Deliverable mapped to Engineering & Design (E) and Project Management (PM) CBS categories |
| **Trigger** | Document type classification required |
| **Evidence** | Datasheet.md Type: "Plan Document"; Discipline: "Construction Management / Commercial" |
| **Impacted WBS/CBS** | DEL-04-02 line items assigned to E and PM |
| **Estimate Impact** | Structural; drives contingency allocation by bucket |
| **How to Override** | Provide explicit CBS mapping in deliverable documents |

---

### D-004: Contingency Method and Rate

| Property | Value |
|----------|-------|
| **Decision** | Contingency calculated at 15% by CBS bucket using PCT_BY_BUCKET method |
| **Trigger** | Default contingency method per AGENT_ESTIMATING protocol |
| **Evidence** | No explicit contingency guidance in deliverable documents; moderate uncertainty due to RFP Section 7 TBD |
| **Impacted WBS/CBS** | CONT category (L-021, L-022) |
| **Estimate Impact** | $1,247 contingency added (15% of $8,320 base) |
| **How to Override** | Set contingency_method and contingency rates in _CONFIG.md; or provide risk-based contingency inputs |

---

### D-005: Escalation Mode

| Property | Value |
|----------|-------|
| **Decision** | Escalation mode set to NONE |
| **Trigger** | Short-duration proposal work; no extended schedule |
| **Evidence** | Procedure.md describes proposal phase work; no multi-year duration |
| **Impacted WBS/CBS** | All line items (no escalation applied) |
| **Estimate Impact** | Zero escalation adjustment |
| **How to Override** | Set escalation_mode = EXPLICIT in _CONFIG.md; provide escalation factors |

---

### D-006: Rounding Policy

| Property | Value |
|----------|-------|
| **Decision** | Estimate rounded to nearest CAD $100 |
| **Trigger** | Default rounding per AGENT_ESTIMATING protocol |
| **Evidence** | No explicit rounding guidance; Class 5/4 estimate maturity appropriate |
| **Impacted WBS/CBS** | Summary totals only (detail lines not rounded) |
| **Estimate Impact** | Presentation; $9,567 presented as $9,600 |
| **How to Override** | Set rounding value in _CONFIG.md |

---

### D-007: Effort Allocation by Section

| Property | Value |
|----------|-------|
| **Decision** | Effort allocated based on plan structure from Procedure.md Step 3 |
| **Trigger** | Need to break down plan development effort into traceable line items |
| **Evidence** | Procedure.md Step 3 defines 7 main sections; Specification.md defines 12 REQs |
| **Impacted WBS/CBS** | E category line items (L-001 through L-014) |
| **Estimate Impact** | Section 3 (Change Management Workflow) allocated highest effort (8 hrs) due to complexity |
| **How to Override** | Provide detailed task breakdown or historical effort data |

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
| **Total Decisions** | 7 |
