# Decision Log

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-01-03_2026-02-04_1322 |
| **Deliverable** | DEL-01-03 BondingAndInsuranceEvidence |

---

## Decision Register

### D-001: Currency Selection

| Field | Value |
|-------|-------|
| **Decision ID** | D-001 |
| **Decision Statement** | Estimate currency set to CAD (Canadian Dollars) |
| **Trigger** | Currency specification required for snapshot; user task brief specified CAD |
| **Evidence** | User task brief: "Currency: CAD" |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | None - currency as specified |
| **Override for Next Run** | Set `currency` in `_CONFIG.md` if different currency required |

---

### D-002: Pricing Method Selection

| Field | Value |
|-------|-------|
| **Decision ID** | D-002 |
| **Decision Statement** | All line items priced using ALLOWANCE method |
| **Trigger** | No rate tables available in `_Estimates/_RateTables/`; no vendor quotes for administrative deliverable |
| **Evidence** | Glob search of `_Estimates/` returned no files; no quotes referenced in deliverable documents |
| **Impacted WBS/CBS** | All line items (PKG-01/DEL-01-03) |
| **Estimate Impact** | Lower confidence; estimate suitable for budgeting only (Class 5) |
| **Override for Next Run** | Provide professional services rate table in `_RateTables/` for improved accuracy |

---

### D-003: Indirects Treatment

| Field | Value |
|-------|-------|
| **Decision ID** | D-003 |
| **Decision Statement** | No separate indirects applied; allowances represent fully-burdened professional service costs |
| **Trigger** | This is an administrative/compliance deliverable, not construction work |
| **Evidence** | _CONTEXT.md identifies deliverable type as "Compliance Document"; no field work involved |
| **Impacted WBS/CBS** | N/A - no construction CBS categories |
| **Estimate Impact** | Simplifies estimate; appropriate for office-based professional services |
| **Override for Next Run** | If project-level overhead allocation is required, specify in `_CONFIG.md` |

---

### D-004: Contingency Rate Selection

| Field | Value |
|-------|-------|
| **Decision ID** | D-004 |
| **Decision Statement** | 15% contingency applied to base estimate |
| **Trigger** | Scope uncertainty from multiple TBD items; contingency required per SPEC |
| **Evidence** | Datasheet, Specification, Guidance, Procedure all contain TBD items for RFP Section 5.3.1 requirements |
| **Impacted WBS/CBS** | L-100 (CONT) |
| **Estimate Impact** | CAD $870 contingency on CAD $5,900 base |
| **Override for Next Run** | Reduce contingency % if RFP requirements are fully extracted and scope is clarified |

---

### D-005: WBS-to-CBS Mapping

| Field | Value |
|-------|-------|
| **Decision ID** | D-005 |
| **Decision Statement** | DEL-01-03 mapped to PM (primary), E (secondary), P (third-party fees) CBS buckets |
| **Trigger** | CBS assignment required for all line items |
| **Evidence** | _CONTEXT.md: Discipline = "Proposal Management"; Type = "Compliance Document"; Responsible = "Proposal Manager" |
| **Impacted WBS/CBS** | All line items for DEL-01-03 |
| **Estimate Impact** | None - appropriate mapping for administrative compliance work |
| **Override for Next Run** | N/A |

---

### D-006: Surety Relationship Assumption

| Field | Value |
|-------|-------|
| **Decision ID** | D-006 |
| **Decision Statement** | Assumed existing surety relationship (vs. new establishment) |
| **Trigger** | Datasheet marks surety relationship status as TBD; affects timeline and possibly cost |
| **Evidence** | Datasheet: "Surety Relationship Status: TBD"; Guidance notes 1-2 weeks for existing vs. longer for new |
| **Impacted WBS/CBS** | L-002 (Surety Coordination) |
| **Estimate Impact** | If new relationship required, effort may increase by 50-100% for surety coordination |
| **Override for Next Run** | Specify surety relationship status in `_CONFIG.md` or update assumption |

---

### D-007: Insurance Scope Inclusion

| Field | Value |
|-------|-------|
| **Decision ID** | D-007 |
| **Decision Statement** | Insurance approach summary preparation included in estimate (conditional scope) |
| **Trigger** | _CONTEXT.md states "as required"; Specification REQ-06 conditional on RFP Section 5.3.1 |
| **Evidence** | _CONTEXT.md: "Insurance approach summary (as required)"; RFP requirements TBD |
| **Impacted WBS/CBS** | L-004 (Insurance Summary), L-009 (Insurance Broker) |
| **Estimate Impact** | CAD $900 included for insurance-related effort; may be reduced to zero if not required |
| **Override for Next Run** | Once RFP Section 5.3.1 is extracted, remove these lines if insurance summary not required |

---

### D-008: Hourly Rate Assumptions

| Field | Value |
|-------|-------|
| **Decision ID** | D-008 |
| **Decision Statement** | Proposal Manager rate: CAD $150/hr; Estimator rate: CAD $175/hr; Document Control rate: CAD $100/hr |
| **Trigger** | No rate tables provided; professional services rates required for effort-based costing |
| **Evidence** | No evidence; default assumption based on typical Alberta professional services market |
| **Impacted WBS/CBS** | All labor-based line items |
| **Estimate Impact** | Moderate sensitivity; +/- 20% rate variance = +/- CAD $1,000 base cost impact |
| **Override for Next Run** | Provide rate table in `_RateTables/` with actual proponent labor rates |

---

## Summary

| Decisions Logged | 8 |
|------------------|---|
| Material Impact Decisions | D-002 (pricing method), D-004 (contingency), D-008 (rates) |
| Low Impact Decisions | D-001, D-003, D-005, D-006, D-007 |
