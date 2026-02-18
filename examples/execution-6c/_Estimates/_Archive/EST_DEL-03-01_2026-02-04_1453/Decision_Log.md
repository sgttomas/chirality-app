# Decision Log

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-03-01_2026-02-04_1453 |
| **Deliverable** | DEL-03-01 Design Methodology Narrative |

---

## Decision Register

### D-001: Currency Selection

| Field | Value |
|-------|-------|
| **Decision ID** | D-001 |
| **Decision Statement** | Use CAD (Canadian Dollars) as the estimate currency |
| **Trigger** | Currency must be specified for estimate; instruction specified CAD |
| **Evidence** | INIT-TASK brief specified "Currency: CAD"; project location is Alberta, Canada (Town of Penhold) |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | N/A - currency selection, not amount |
| **How to Override** | Provide alternative currency in `_CONFIG.md` for next run |

---

### D-002: Rate Table Fallback to Allowances

| Field | Value |
|-------|-------|
| **Decision ID** | D-002 |
| **Decision Statement** | Use allowance-based pricing for all labor since no rate tables are available |
| **Trigger** | No rate tables found in `_Estimates/_RateTables/`; no vendor quotes for internal labor |
| **Evidence** | Glob search of `_Estimates/` folder returned no files; AGENT_ESTIMATING.md specifies fallback hierarchy: Quote > Rate Table > Allowance |
| **Impacted WBS/CBS** | All E (Engineering) and PM (Project Management) line items |
| **Estimate Impact** | HIGH - all pricing based on assumed typical rates; actual costs may vary +/- 30% |
| **How to Override** | Provide labor rate tables in `_Estimates/_RateTables/` with actual team billing rates |

---

### D-003: PM Overhead Factor

| Field | Value |
|-------|-------|
| **Decision ID** | D-003 |
| **Decision Statement** | Apply 15% Project Management coordination overhead to direct engineering labor |
| **Trigger** | Indirect costs must be allocated; no project-specific overhead rate specified |
| **Evidence** | AGENT_ESTIMATING.md STRUCTURE section default CBS includes PM overhead; 15% is typical for proposal/design work |
| **Impacted WBS/CBS** | PM bucket (line PM-001) |
| **Estimate Impact** | Adds $1,676 CAD to estimate |
| **How to Override** | Specify `overhead_rate` in `_CONFIG.md` or provide project-specific indirect rate structure |

---

### D-004: Contingency Method and Percentages

| Field | Value |
|-------|-------|
| **Decision ID** | D-004 |
| **Decision Statement** | Apply PCT_BY_BUCKET contingency method with 20% on Engineering and 15% on PM |
| **Trigger** | Contingency must be calculated; no risk-based analysis available; AGENT_ESTIMATING.md default is PCT_BY_BUCKET |
| **Evidence** | All pricing is allowance-based (100%); higher uncertainty warrants higher contingency; 20% for E reflects scope variability, 15% for PM reflects coordination uncertainty |
| **Impacted WBS/CBS** | CONT bucket (lines CONT-001, CONT-002) |
| **Estimate Impact** | Adds $2,590 CAD contingency (19.1% blended rate on base) |
| **How to Override** | Specify `contingency_method: RISK_BASED` in `_CONFIG.md` or provide project-specific contingency percentages |

---

### D-005: Effort Estimation Basis

| Field | Value |
|-------|-------|
| **Decision ID** | D-005 |
| **Decision Statement** | Estimate effort hours based on Procedure.md 8-step process mapped to team roles |
| **Trigger** | No historical effort data available for similar deliverables; quantities must be derived |
| **Evidence** | Procedure.md defines 8 production steps with specified roles; Specification.md contains 30 requirements; Guidance.md contains 8 principles, 10 considerations, 6 trade-offs; complexity analysis suggests 60-70 total hours |
| **Impacted WBS/CBS** | All labor line items (E-001 through E-010, PM-002) |
| **Estimate Impact** | Core driver of estimate; actual hours may vary significantly based on team experience |
| **How to Override** | Provide historical effort data for similar proposal sections or actual time tracking |

---

### D-006: Visual Aids Scope Assumption

| Field | Value |
|-------|-------|
| **Decision ID** | D-006 |
| **Decision Statement** | Assume 8 hours for graphics/visual aids production covering 3-4 diagrams |
| **Trigger** | Procedure.md Step 6 lists visual aids as recommended; specific count and complexity not defined |
| **Evidence** | Procedure.md Step 6 lists: design process flowchart, timeline diagram, coordination matrix, permitting sequence diagram (4 items); Guidance.md C-09 emphasizes visual aids for non-technical evaluators |
| **Impacted WBS/CBS** | E-009 (Graphics/CAD) |
| **Estimate Impact** | $760 CAD; actual may vary based on complexity and presentation standards |
| **How to Override** | Specify graphics scope and complexity in deliverable requirements or provide actual graphics effort tracking |

---

### D-007: Stakeholder Review Cycles

| Field | Value |
|-------|-------|
| **Decision ID** | D-007 |
| **Decision Statement** | Assume 2 stakeholder review cycles requiring 4 hours of Design Manager/PM time |
| **Trigger** | Procedure.md Step 8 requires stakeholder review; number of cycles not specified |
| **Evidence** | Typical proposal development involves 1-3 review cycles; 2 cycles assumed as moderate estimate; 2 hours per cycle for review meeting and feedback incorporation |
| **Impacted WBS/CBS** | PM-002 (Stakeholder Review Cycles) |
| **Estimate Impact** | $700 CAD; additional cycles would add ~$350 CAD each |
| **How to Override** | Define required review cycle count in proposal production plan or adjust based on team QA process |

---

### D-008: WBS to CBS Mapping

| Field | Value |
|-------|-------|
| **Decision ID** | D-008 |
| **Decision Statement** | Map DEL-03-01 primarily to Engineering (E) and Project Management (PM) CBS buckets |
| **Trigger** | CBS assignment required for cost categorization; deliverable is a narrative document |
| **Evidence** | DEL-03-01 is a Design Management narrative document (per _CONTEXT.md); authoring is Engineering/Design activity; coordination is PM activity; no Procurement, Construction, or Commissioning components |
| **Impacted WBS/CBS** | All line items; E and PM only |
| **Estimate Impact** | CBS structure affects contingency allocation and reporting |
| **How to Override** | Provide project-specific CBS mapping rules in `_CONFIG.md` |

---

## Decision Summary Statistics

| Metric | Value |
|--------|-------|
| Total Decisions Logged | 8 |
| Decisions with Evidence | 8 (100%) |
| Decisions with Override Path | 8 (100%) |
| High Impact Decisions | D-002, D-004, D-005 |

---

**Generated:** 2026-02-04
**Agent:** ESTIMATING (Type 2)
