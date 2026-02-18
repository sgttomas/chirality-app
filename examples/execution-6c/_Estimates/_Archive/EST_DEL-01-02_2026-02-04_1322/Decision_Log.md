# Decision Log

## Snapshot Identification

| Field | Value |
|-------|-------|
| **Snapshot ID** | EST_DEL-01-02_2026-02-04_1322 |
| **Deliverable** | DEL-01-02 FormalSubmissionPackage |

---

## Decisions

### D-001: Currency Selection

| Field | Value |
|-------|-------|
| **Decision ID** | D-001 |
| **Decision Statement** | Currency set to CAD (Canadian Dollars) |
| **Trigger** | Currency must be specified for estimate; user directive provided |
| **Evidence** | User task brief specified "Currency: CAD" |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | All amounts denominated in CAD |
| **How to Override** | Update `_CONFIG.md` with different currency setting |

---

### D-002: CBS Mapping

| Field | Value |
|-------|-------|
| **Decision ID** | D-002 |
| **Decision Statement** | DEL-01-02 mapped to CBS category PM (Project Management / EPCM) |
| **Trigger** | CBS assignment required for each line item |
| **Evidence** | Deliverable description: "Final PDF assembly plan, submission email package details, revision control statement" — administrative/coordination work typical of proposal management |
| **Impacted WBS/CBS** | PKG-01 / DEL-01-02 → PM |
| **Estimate Impact** | All direct labor categorized under PM |
| **How to Override** | Provide alternate CBS mapping in `_CONFIG.md` |

---

### D-003: Scope Exclusions

| Field | Value |
|-------|-------|
| **Decision ID** | D-003 |
| **Decision Statement** | Upstream content (DEL-02 through DEL-09), DEL-01-01, DEL-01-03, post-submission activities, Owner's costs, and taxes excluded from estimate |
| **Trigger** | Scope boundary definition required |
| **Evidence** | Specification.md "Out of Scope" section explicitly excludes content creation for other deliverables; _CONTEXT.md defines DEL-01-02 scope narrowly |
| **Impacted WBS/CBS** | Defines estimate boundary |
| **Estimate Impact** | Total reflects DEL-01-02 only; not full proposal cost |
| **How to Override** | Request aggregate estimate across all DEL-* |

---

### D-004: Allowance-Based Pricing

| Field | Value |
|-------|-------|
| **Decision ID** | D-004 |
| **Decision Statement** | All line items priced using allowances (no quotes or rate tables available) |
| **Trigger** | No pricing sources found in `_RateTables/` or `_REFERENCES.md` |
| **Evidence** | `_RateTables/` directory is empty; no vendor quotes referenced |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | LOW confidence on all pricing; 100% ALLOWANCE method |
| **How to Override** | Provide rate tables in `_RateTables/` with labor rates; provide vendor quotes |

---

### D-005: Indirects Model

| Field | Value |
|-------|-------|
| **Decision ID** | D-005 |
| **Decision Statement** | Indirects embedded in PM labor allowances (no separate indirects line) |
| **Trigger** | Indirects handling required per PROTOCOL |
| **Evidence** | Proposal management is inherently overhead/indirect cost; labor rates assumed to include burden |
| **Impacted WBS/CBS** | PM category |
| **Estimate Impact** | No separate CI or indirects markup |
| **How to Override** | Provide explicit indirect rate or factor in `_CONFIG.md` |

---

### D-006: Contingency at 15%

| Field | Value |
|-------|-------|
| **Decision ID** | D-006 |
| **Decision Statement** | Contingency set at 15% of base estimate ($1,600 on $10,700 base) |
| **Trigger** | Contingency required per PROTOCOL; method = PCT_BY_BUCKET (default) |
| **Evidence** | High uncertainty factors: (1) 100% allowance-based pricing, (2) No historical baseline, (3) Multiple TBD items in source documents, (4) LOW confidence overall |
| **Impacted WBS/CBS** | CONT category |
| **Estimate Impact** | $1,600 contingency reserve |
| **How to Override** | Provide contingency factor in `_CONFIG.md` or switch to RISK_BASED method |

---

### D-007: No Escalation

| Field | Value |
|-------|-------|
| **Decision ID** | D-007 |
| **Decision Statement** | Escalation mode = NONE |
| **Trigger** | Escalation handling required per PROTOCOL |
| **Evidence** | Proposal preparation is short-duration effort before Aug 30, 2024 deadline; no time-based cost growth applicable |
| **Impacted WBS/CBS** | N/A |
| **Estimate Impact** | No escalation adjustment applied |
| **How to Override** | Set `escalation_mode: EXPLICIT` in `_CONFIG.md` with factors |

---

### D-008: Rounding to $100

| Field | Value |
|-------|-------|
| **Decision ID** | D-008 |
| **Decision Statement** | Rounding set to nearest $100 CAD |
| **Trigger** | Precision policy required per PROTOCOL |
| **Evidence** | Allowance-based estimate does not support false precision; $100 rounding appropriate for ~$12K estimate |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | Line items rounded to nearest $100 |
| **How to Override** | Set `rounding` value in `_CONFIG.md` |

---

### D-009: Labor Rate Assumptions

| Field | Value |
|-------|-------|
| **Decision ID** | D-009 |
| **Decision Statement** | Assumed labor rates: Proposal Manager $200/hr, Graphics Coordinator $125/hr, Admin Support $100/hr |
| **Trigger** | No rate tables provided; rates required for allowance calculation |
| **Evidence** | Rates based on typical Alberta professional services market for proposal management roles; no project-specific rates available |
| **Impacted WBS/CBS** | All PM line items |
| **Estimate Impact** | Base estimate sensitive to rate assumptions; +/- 20% rate variance = +/- ~$2,000 |
| **How to Override** | Provide labor rate table in `_RateTables/` |

---

## Decision Index

| ID | Summary | Impact Level |
|----|---------|--------------|
| D-001 | Currency = CAD | Low (user-directed) |
| D-002 | CBS = PM | Low (clear mapping) |
| D-003 | Scope exclusions defined | Medium (boundary) |
| D-004 | Allowance-based pricing | High (confidence) |
| D-005 | Indirects embedded | Medium (structure) |
| D-006 | Contingency 15% | High ($1,600) |
| D-007 | No escalation | Low (short duration) |
| D-008 | Rounding $100 | Low (presentation) |
| D-009 | Labor rates assumed | High (basis) |
