# Decision Log
## DEL-04-01 Construction Methodology Narrative

**Snapshot ID:** EST_DEL-04-01_2026-02-04_1323

---

## Decision Register

### D-001: Scope Exclusions Established

| Field | Value |
|-------|-------|
| **Decision ID** | D-001 |
| **Decision Statement** | Scope exclusions established per decomposition document package boundaries. Physical construction work, post-award execution plans, and related deliverables (DEL-04-02, DEL-04-03, DEL-06-01, DEL-08-01, DEL-09-01, DEL-09-02) are excluded from this estimate. |
| **Trigger** | Need to define estimate boundary for narrative document production vs. construction execution |
| **Evidence** | Decomposition document Section 7 (Work Packages), Section 8 (Deliverables definitions); _CONTEXT.md (deliverable scope) |
| **Impacted WBS/CBS** | PKG-06 / DEL-04-01; Engineering & Design (E) |
| **Estimate Impact** | Constrains estimate to proposal production scope only; excludes construction costs |
| **Override for Next Run** | N/A - scope boundary is contract-defined |

---

### D-002: Currency Set to CAD

| Field | Value |
|-------|-------|
| **Decision ID** | D-002 |
| **Decision Statement** | Estimate currency set to CAD (Canadian Dollars) per user instruction |
| **Trigger** | User instruction specified CAD; project located in Alberta, Canada |
| **Evidence** | User instruction in task assignment; project location in Town of Penhold, Alberta (Datasheet.md) |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | All amounts expressed in CAD |
| **Override for Next Run** | Set `currency: USD` or other in `_CONFIG.md` if different currency required |

---

### D-003: Labor Rates Estimated as Allowances

| Field | Value |
|-------|-------|
| **Decision ID** | D-003 |
| **Decision Statement** | Labor rates estimated using allowances due to absence of project rate tables |
| **Trigger** | No rate tables found in `_RateTables/` directory; no vendor quotes available |
| **Evidence** | Empty `_RateTables/` directory; AGENT_ESTIMATING.md pricing hierarchy (Quote > Rate Table > Allowance) |
| **Impacted WBS/CBS** | All labor line items |
| **Estimate Impact** | Estimates are indicative; actual costs may vary based on actual rates |
| **Override for Next Run** | Provide professional services rate tables in `_RateTables/` directory with hourly rates by role |

---

### D-004: All Line Items Priced Using Allowances

| Field | Value |
|-------|-------|
| **Decision ID** | D-004 |
| **Decision Statement** | All line items priced using allowance method due to absence of rate tables and quotes |
| **Trigger** | No pricing sources available; straight-through pipeline requires completion |
| **Evidence** | AGENT_ESTIMATING.md Protocol Section 3.3 (Price Line Items: Quote > Rate Table > Allowance) |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | Confidence level set to MEDIUM; estimates are allowance-based |
| **Override for Next Run** | Provide rate tables or vendor quotes for improved accuracy |

---

### D-005: Indirects Embedded in Allowance Rates

| Field | Value |
|-------|-------|
| **Decision ID** | D-005 |
| **Decision Statement** | Indirect costs (overhead, burden) embedded in allowance rates rather than separately broken out |
| **Trigger** | Proposal production work is internal team effort; no separate indirects model required |
| **Evidence** | Deliverable type is professional services/document production; standard practice for internal proposal work |
| **Impacted WBS/CBS** | All labor line items |
| **Estimate Impact** | Simplifies estimate structure; indirects not visible as separate line items |
| **Override for Next Run** | If separate indirects required, provide indirects model in `_CONFIG.md` |

---

### D-006: Contingency at 10%

| Field | Value |
|-------|-------|
| **Decision ID** | D-006 |
| **Decision Statement** | Contingency applied at 10% of base estimate for professional services work |
| **Trigger** | Default contingency method (PCT_BY_BUCKET); professional services with defined scope |
| **Evidence** | AGENT_ESTIMATING.md default contingency method; low-risk document production work |
| **Impacted WBS/CBS** | Contingency (CONT) |
| **Estimate Impact** | Adds 10% contingency to base estimate total |
| **Override for Next Run** | Set `contingency_method: RISK_BASED` in `_CONFIG.md` for risk-based contingency |

---

### D-007: Escalation Not Applied

| Field | Value |
|-------|-------|
| **Decision ID** | D-007 |
| **Decision Statement** | Escalation not applied; work expected to be completed within pricing period |
| **Trigger** | Default escalation mode (NONE); short-duration proposal work |
| **Evidence** | AGENT_ESTIMATING.md default escalation mode; pricing date contemporaneous with execution |
| **Impacted WBS/CBS** | N/A |
| **Estimate Impact** | No escalation adjustment applied |
| **Override for Next Run** | Set `escalation_mode: EXPLICIT` in `_CONFIG.md` if escalation required |

---

### D-008: Effort Estimates Based on Document Complexity Assessment

| Field | Value |
|-------|-------|
| **Decision ID** | D-008 |
| **Decision Statement** | Effort estimates based on assessment of document complexity from four documents analysis |
| **Trigger** | Need to quantify labor hours for narrative production |
| **Evidence** | Datasheet.md (11 requirements R-01 through R-11), Specification.md (comprehensive requirements), Procedure.md (8-step production process with multiple review cycles) |
| **Impacted WBS/CBS** | All labor line items |
| **Estimate Impact** | Effort hours reflect moderate-high complexity narrative with multiple technical reviews |
| **Override for Next Run** | Provide historical effort data for similar deliverables to calibrate estimates |

---

### D-009: Blended Hourly Rate Assumption

| Field | Value |
|-------|-------|
| **Decision ID** | D-009 |
| **Decision Statement** | Blended hourly rate of $175/hr CAD assumed for professional services labor |
| **Trigger** | No rate tables available; need to price labor line items |
| **Evidence** | Industry typical range for construction management/proposal development professionals in Alberta ($150-$200/hr); mid-point selected |
| **Impacted WBS/CBS** | All labor line items |
| **Estimate Impact** | Rate assumption drives total labor cost; actual rates may vary |
| **Override for Next Run** | Provide role-specific hourly rates in `_RateTables/` directory |

---

**End of Decision Log**
