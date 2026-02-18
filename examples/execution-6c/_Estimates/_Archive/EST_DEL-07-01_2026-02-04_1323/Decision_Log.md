# Decision Log

## Purpose
This log records all decisions made during the estimate generation process for DEL-07-01. Each decision includes the trigger, evidence, impact, and how to override in future runs.

---

## D-001: Scope Exclusions

| Field | Value |
|-------|-------|
| **Decision ID** | D-001 |
| **Decision Statement** | Excluded from estimate: Owner's costs, firm's internal database maintenance, marketing collateral development, legal review, proposal printing/submission logistics |
| **Trigger** | Scope boundary definition required for estimate |
| **Evidence** | _CONTEXT.md identifies DEL-07-01 scope; printing/submission covered in DEL-01-02; no legal review mentioned in documents |
| **Impacted WBS/CBS** | PKG-03 / DEL-07-01; all CBS buckets |
| **Estimate Impact** | Reduces estimate scope; costs for excluded items not carried |
| **How to Override** | Add explicit scope items to _CONFIG.md include_scopes list |

---

## D-002: Contracting Assumptions

| Field | Value |
|-------|-------|
| **Decision ID** | D-002 |
| **Decision Statement** | Work performed by internal proposal team; no external consultants; standard proposal timeline; existing project database available |
| **Trigger** | Contracting basis needed for labor estimate |
| **Evidence** | _CONTEXT.md "Responsible: Proposal Manager + HR/Team Admin" indicates internal team; Procedure §Prerequisites lists internal firm records |
| **Impacted WBS/CBS** | PKG-03 / DEL-07-01; E (Engineering & Design), PM (Project Management) |
| **Estimate Impact** | Internal labor rates assumed (~$150/hr Proposal Manager, ~$100/hr Admin); no external consultant markup |
| **How to Override** | Provide external consultant quotes or specify consultant engagement in _CONFIG.md |

---

## D-003: Location and Productivity

| Field | Value |
|-------|-------|
| **Decision ID** | D-003 |
| **Decision Statement** | Work performed at Alberta office; standard productivity; no travel; remote/hybrid work assumed |
| **Trigger** | Location/productivity basis needed for labor estimate |
| **Evidence** | Decomposition §1 identifies Town of Penhold (Alberta) as owner; no travel mentioned in Procedure |
| **Impacted WBS/CBS** | PKG-03 / DEL-07-01; all labor line items |
| **Estimate Impact** | No location adjustment factor applied; standard 8-hour productive day assumed |
| **How to Override** | Add location_factor or productivity_factor to _CONFIG.md |

---

## D-004: Pricing Basis Selection

| Field | Value |
|-------|-------|
| **Decision ID** | D-004 |
| **Decision Statement** | All line items priced using ALLOWANCE methodology; no rate tables or quotes available |
| **Trigger** | No pricing sources found in _RateTables/ or source documents |
| **Evidence** | _RateTables/ directory is empty; no vendor quotes in _Sources/ or deliverable folder |
| **Impacted WBS/CBS** | PKG-03 / DEL-07-01; all CBS buckets |
| **Estimate Impact** | LOW confidence on all pricing; allowance amounts based on typical proposal effort estimates |
| **How to Override** | Provide rate tables in _RateTables/ (e.g., ProposalLaborRates.csv) or vendor quotes |

---

## D-005: Indirects Model

| Field | Value |
|-------|-------|
| **Decision ID** | D-005 |
| **Decision Statement** | 0% EPCM/PM overhead applied; no construction indirects |
| **Trigger** | Indirects methodology needed |
| **Evidence** | DEL-07-01 is a proposal preparation cost, not project delivery cost; Datasheet identifies Type as "Qualifications Document" |
| **Impacted WBS/CBS** | PKG-03 / DEL-07-01; CI (Construction Indirects) not applicable |
| **Estimate Impact** | No indirect markup on labor; costs represent direct proposal effort only |
| **How to Override** | Set indirect_factor in _CONFIG.md if firm applies overhead to proposal costs |

---

## D-006: Contingency Method and Rate

| Field | Value |
|-------|-------|
| **Decision ID** | D-006 |
| **Decision Statement** | 20% contingency applied using PCT_BY_BUCKET method |
| **Trigger** | Contingency methodology required per PROTOCOL |
| **Evidence** | 100% allowance-based pricing with LOW confidence; RFP requirements TBD; scope uncertainty |
| **Impacted WBS/CBS** | PKG-03 / DEL-07-01; CONT (Contingency) |
| **Estimate Impact** | $1,920 CAD contingency added to base estimate |
| **How to Override** | Set contingency_method and contingency_rate in _CONFIG.md |

---

## D-007: Currency Selection

| Field | Value |
|-------|-------|
| **Decision ID** | D-007 |
| **Decision Statement** | Currency set to CAD (Canadian Dollars) |
| **Trigger** | Currency selection required; specified in task brief |
| **Evidence** | Task brief specified "Currency: CAD"; Decomposition §1 identifies Town of Penhold (Alberta, Canada) as owner |
| **Impacted WBS/CBS** | All |
| **Estimate Impact** | All amounts in CAD |
| **How to Override** | Set currency in _CONFIG.md |

---

## D-008: CBS Mapping

| Field | Value |
|-------|-------|
| **Decision ID** | D-008 |
| **Decision Statement** | DEL-07-01 mapped to CBS bucket E (Engineering & Design) as primary; PM (Project Management) as secondary |
| **Trigger** | WBS to CBS mapping required |
| **Evidence** | Datasheet Type: "Qualifications Document"; Discipline: "Proposal Management"; document preparation is design/engineering work |
| **Impacted WBS/CBS** | PKG-03 / DEL-07-01; E, PM |
| **Estimate Impact** | Line items assigned to E or PM based on activity type |
| **How to Override** | Provide CBS mapping override in _CONFIG.md |

---

## D-009: Labor Hour Estimates

| Field | Value |
|-------|-------|
| **Decision ID** | D-009 |
| **Decision Statement** | Labor hours estimated based on typical proposal effort for qualifications documents |
| **Trigger** | No historical data available for proposal costs |
| **Evidence** | Procedure §Steps 1-10 define activities; typical proposal preparation effort estimated at 40-80 hours total for this deliverable type |
| **Impacted WBS/CBS** | PKG-03 / DEL-07-01; all labor line items |
| **Estimate Impact** | 58 total labor hours estimated across all roles |
| **How to Override** | Provide historical proposal cost data or detailed task-level estimates |

---

**Log Status:** Complete for snapshot EST_DEL-07-01_2026-02-04_1323
