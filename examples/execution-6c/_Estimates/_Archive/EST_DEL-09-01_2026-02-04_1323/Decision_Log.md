# Decision Log

## Snapshot Identification

| Field | Value |
|-------|-------|
| **Snapshot ID** | EST_DEL-09-01_2026-02-04_1323 |
| **Deliverable** | DEL-09-01 Risk Register and Mitigation Plan |

---

## D-001: Scope Boundary - Proposal Phase Only

| Field | Value |
|-------|-------|
| **Decision ID** | D-001 |
| **Decision** | Estimate covers proposal-phase effort only; post-award risk management execution is excluded |
| **Trigger** | Specification.md explicitly excludes post-award activities and states scope is for "proposal integration" |
| **Evidence** | Specification.md Out of Scope section; Procedure.md purpose statement |
| **Impacted WBS/CBS** | PKG-09 / DEL-09-01 (all CBS) |
| **Estimate Impact** | Significant - limits effort to ~$20K vs potential $100K+ for full project risk management |
| **Override** | Include post-award risk management scope in deliverable brief if full lifecycle estimate needed |

---

## D-002: Personnel Assignment

| Field | Value |
|-------|-------|
| **Decision ID** | D-002 |
| **Decision** | Work performed by in-house PM and Technical Leads per deliverable responsibility assignment |
| **Trigger** | _CONTEXT.md Responsible: "PM + Technical Leads" |
| **Evidence** | _CONTEXT.md; Procedure.md Personnel and Roles table |
| **Impacted WBS/CBS** | PKG-09 / DEL-09-01 / E, PM |
| **Estimate Impact** | Moderate - in-house rates assumed vs external consultant rates |
| **Override** | Specify if external risk management consultant is required |

---

## D-003: Location/Productivity Assumptions

| Field | Value |
|-------|-------|
| **Decision ID** | D-003 |
| **Decision** | Work performed in office environment; Alberta-based team; no travel required |
| **Trigger** | No location specified in deliverable documents |
| **Evidence** | Standard proposal development context; project location is Penhold, Alberta |
| **Impacted WBS/CBS** | PKG-09 / DEL-09-01 (all) |
| **Estimate Impact** | Low - no travel or remote work premium applied |
| **Override** | Specify if travel to client site required for risk workshops |

---

## D-004: Pricing Method - Allowance Convention

| Field | Value |
|-------|-------|
| **Decision ID** | D-004 |
| **Decision** | All line items priced using ALLOWANCE method with Qty=1, Unit=LS, UnitRate=Amount |
| **Trigger** | No rate tables available in _RateTables/; no vendor quotes for professional services |
| **Evidence** | _Estimates/_RateTables/ not populated; AGENT_ESTIMATING.md pricing hierarchy |
| **Impacted WBS/CBS** | PKG-09 / DEL-09-01 (all) |
| **Estimate Impact** | High - 100% allowance basis increases uncertainty; confidence rated LOW-MEDIUM |
| **Override** | Provide PM/Technical Lead hourly rates in _RateTables/ for rate-based pricing |

---

## D-005: Simplified CBS Structure

| Field | Value |
|-------|-------|
| **Decision ID** | D-005 |
| **Decision** | Use simplified CBS (E, PM, CONT only) for document deliverable; no construction directs/indirects |
| **Trigger** | Deliverable is a professional services document, not construction work |
| **Evidence** | Datasheet.md Type: "Register + Plan Document"; no field work involved |
| **Impacted WBS/CBS** | PKG-09 / DEL-09-01 |
| **Estimate Impact** | Low - CBS simplification appropriate for deliverable type |
| **Override** | N/A - deliverable type does not warrant construction CBS categories |

---

## D-006: Contingency Rate Selection

| Field | Value |
|-------|-------|
| **Decision ID** | D-006 |
| **Decision** | Apply 15% contingency to base estimate (elevated from typical 10%) |
| **Trigger** | 100% ALLOWANCE pricing basis; no rate tables or quotes available |
| **Evidence** | AGENT_ESTIMATING.md contingency method: "allow higher % for ALLOWANCE-heavy buckets" |
| **Impacted WBS/CBS** | PKG-09 / DEL-09-01 / CONT |
| **Estimate Impact** | $3,000 contingency on $20,500 base |
| **Override** | Reduce contingency to 10% if rate tables provided and estimate confidence improves |

---

## D-007: Workshop Duration Assumption

| Field | Value |
|-------|-------|
| **Decision ID** | D-007 |
| **Decision** | Risk identification workshop assumed to be 4 hours duration |
| **Trigger** | Procedure.md Step 1 recommends "2-4 hours"; no specific duration mandated |
| **Evidence** | Procedure.md Step 1: "Schedule risk identification workshop with PM + Technical Leads (recommended 2-4 hours)" |
| **Impacted WBS/CBS** | PKG-09 / DEL-09-01 / E (L-001, L-002) |
| **Estimate Impact** | Moderate - 4 hours selected as upper bound for thorough coverage of 7 categories |
| **Override** | Specify workshop duration in project brief if different |

---

## D-008: Technical Lead Count Assumption

| Field | Value |
|-------|-------|
| **Decision ID** | D-008 |
| **Decision** | Assumed 6 Technical Leads participate (Architect, Structural, Mechanical, Electrical, Civil, Construction Manager) |
| **Trigger** | Procedure.md Personnel table lists multiple discipline roles but does not specify exact count |
| **Evidence** | Procedure.md Personnel and Roles; typical D-B team structure |
| **Impacted WBS/CBS** | PKG-09 / DEL-09-01 / E (L-002, L-003) |
| **Estimate Impact** | Moderate - 6 leads at avg $150/hr affects labor cost |
| **Override** | Specify actual team composition if different |

---

## D-009: Risk Count Assumption

| Field | Value |
|-------|-------|
| **Decision ID** | D-009 |
| **Decision** | Assumed ~20 risks total across 7 categories, with ~5 high-priority (score >=15) |
| **Trigger** | Specification.md notes "Minimum 20 risks expected across 7 categories" as ASSUMPTION |
| **Evidence** | Specification.md Documentation section; Guidance.md recommends "Target 15-25 risks total" |
| **Impacted WBS/CBS** | PKG-09 / DEL-09-01 / E (L-004 through L-006) |
| **Estimate Impact** | Moderate - risk count drives assessment and mitigation effort |
| **Override** | Specify expected risk count if different |

---

## D-010: QMP Detail Level Assumption

| Field | Value |
|-------|-------|
| **Decision ID** | D-010 |
| **Decision** | QMP developed to moderate detail level appropriate for proposal (not full operational procedures) |
| **Trigger** | No explicit QMP detail requirement in deliverable documents |
| **Evidence** | Deliverable purpose is proposal submission, not project execution; Procedure.md describes procedural framework |
| **Impacted WBS/CBS** | PKG-09 / DEL-09-01 / E (L-007 through L-010) |
| **Estimate Impact** | Moderate - proposal-level QMP vs detailed operational QMP |
| **Override** | Specify if full operational QMP detail required |

---

**Generated:** 2026-02-04 13:23
**Agent:** ESTIMATING (Type 2)
