# Decision Log

## Snapshot Identification

| Attribute | Value |
|---|---|
| **Snapshot ID** | EST_DEL-05-03_2026-02-04_1323 |
| **Deliverable** | DEL-05-03 Pricing Narrative and Assumptions |

---

## Decisions

### D-001: Currency Selection

| Field | Value |
|---|---|
| **Decision ID** | D-001 |
| **Decision Statement** | Currency set to CAD (Canadian Dollars) |
| **Trigger** | Currency must be specified for estimate; INIT-TASK brief specified CAD |
| **Evidence** | INIT-TASK brief: "Currency: CAD" |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | Defines currency for all amounts |
| **Override for Next Run** | Specify different currency in _CONFIG.md or INIT-TASK brief |

---

### D-002: Scope Exclusions

| Field | Value |
|---|---|
| **Decision ID** | D-002 |
| **Decision Statement** | Standard exclusions applied: Owner's costs, land, financing excluded |
| **Trigger** | Default exclusions must be documented |
| **Evidence** | No evidence; default per AGENT_ESTIMATING.md Phase 1.3 |
| **Impacted WBS/CBS** | N/A (excluded scope) |
| **Estimate Impact** | No direct cost impact (exclusions are out of scope) |
| **Override for Next Run** | Modify include_scopes/exclude_scopes in _CONFIG.md |

---

### D-003: Location and Productivity Basis

| Field | Value |
|---|---|
| **Decision ID** | D-003 |
| **Decision Statement** | Location set to Central Alberta (Penhold region); standard professional services productivity assumed |
| **Trigger** | Location affects labor rates and productivity factors |
| **Evidence** | Decomposition identifies project as Penhold Public Services Building, Alberta |
| **Impacted WBS/CBS** | All professional services line items (E, PM) |
| **Estimate Impact** | Alberta professional rates applied (~$150/hr blended) |
| **Override for Next Run** | Provide specific rate tables in _RateTables/ or specify location factors in _CONFIG.md |

---

### D-004: Indirects Model Selection

| Field | Value |
|---|---|
| **Decision ID** | D-004 |
| **Decision Statement** | Factor-based indirects model applied; indirects included within professional services allowances |
| **Trigger** | Must determine how to handle indirect costs for professional services |
| **Evidence** | No evidence; default approach per AGENT_ESTIMATING.md (factor-based) |
| **Impacted WBS/CBS** | All CBS categories |
| **Estimate Impact** | Overhead and administrative support implicitly included in hourly rates |
| **Override for Next Run** | Provide explicit indirects factors in _CONFIG.md or separate indirects line items |

---

### D-005: Contingency Method and Rate

| Field | Value |
|---|---|
| **Decision ID** | D-005 |
| **Decision Statement** | PCT_BY_BUCKET contingency method applied; 15% contingency rate selected |
| **Trigger** | Contingency must be documented; rate selection required |
| **Evidence** | No rate tables available; 100% allowance-based pricing; multiple TBD items in source documents |
| **Impacted WBS/CBS** | CONT |
| **Estimate Impact** | $1,650 contingency added (15% of $11,000 base) |
| **Override for Next Run** | Specify contingency_method and rate in _CONFIG.md |

**Rationale for 15% rate:**
- All line items priced by ALLOWANCE (no quotes or rate tables)
- Source documents contain multiple TBD items requiring estimator input
- Uncertainty in value alternatives scope and cross-reference effort
- Standard allowance contingency per AGENT_ESTIMATING fallback model: 10-20% for allowance-heavy estimates

---

### D-006: Escalation Mode

| Field | Value |
|---|---|
| **Decision ID** | D-006 |
| **Decision Statement** | Escalation mode set to NONE |
| **Trigger** | Must determine whether to apply escalation |
| **Evidence** | Default setting; professional services proposal production is short-duration scope |
| **Impacted WBS/CBS** | N/A (no escalation applied) |
| **Estimate Impact** | No escalation costs included |
| **Override for Next Run** | Set escalation_mode = EXPLICIT in _CONFIG.md and provide escalation factors |

---

### D-007: Rounding Policy

| Field | Value |
|---|---|
| **Decision ID** | D-007 |
| **Decision Statement** | Rounding set to nearest CAD $100 (adjusted from default $1,000) |
| **Trigger** | Default rounding of $1,000 too coarse for small professional services deliverable |
| **Evidence** | Base estimate ~$11,000; $1,000 rounding would obscure detail |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | Line items rounded to nearest $100 for readability |
| **Override for Next Run** | Specify rounding value in _CONFIG.md |

---

## Decision Index

| ID | Summary | Impact Level |
|---|---|---|
| D-001 | Currency = CAD | Low |
| D-002 | Standard exclusions applied | Low |
| D-003 | Location = Central Alberta; standard productivity | Medium |
| D-004 | Indirects included in allowances | Low |
| D-005 | Contingency = 15% (PCT_BY_BUCKET) | High |
| D-006 | Escalation = NONE | Low |
| D-007 | Rounding = $100 | Low |

---

**Note:** All decisions documented here are defaults or judgment calls made to enable straight-through pipeline completion. Override any decision in the next run by providing inputs via _CONFIG.md or rate tables.
