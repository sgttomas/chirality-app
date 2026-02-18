# Decision Log
## DEL-03-02: DetailedDesignAndConstructionDocsPlan
## Snapshot: EST_DEL-03-02_2026-02-04_1323

---

## D-001: Currency Selection

| Property | Value |
|----------|-------|
| **Decision ID** | D-001 |
| **Decision** | Use CAD as base currency |
| **Trigger** | Operator directive specified CAD; no currency indicators in source documents |
| **Evidence** | Operator instruction: "Currency: CAD" |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | All amounts expressed in CAD |
| **Override** | N/A - operator directive is binding |

---

## D-002: Pricing Basis Selection

| Property | Value |
|----------|-------|
| **Decision ID** | D-002 |
| **Decision** | Use ALLOWANCE method for all line items |
| **Trigger** | No vendor quotes available; _RateTables/ folder is empty |
| **Evidence** | Glob search of _RateTables/ returned empty |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | All pricing based on professional services allowance rates; confidence is LOW-MEDIUM |
| **Override** | Provide rate tables in _RateTables/ folder for next run |

---

## D-003: Estimate Scope - Proposal Phase Only

| Property | Value |
|----------|-------|
| **Decision ID** | D-003 |
| **Decision** | Estimate covers proposal phase plan document production only; excludes post-award execution |
| **Trigger** | DEL-03-02 is a Plan Document for RFP submission; post-award execution is separate scope |
| **Evidence** | _CONTEXT.md: "Anticipated Artifacts: Plan for producing detailed design and construction documents"; Procedure.md Part A vs Part B distinction |
| **Impacted WBS/CBS** | Entire estimate scope |
| **Estimate Impact** | Excludes significant post-award design/coordination costs (potentially $500K-$2M+ depending on project scale) |
| **Override** | If post-award costs required, create separate estimate or expand scope directive |

---

## D-004: Landscape Discipline Scope

| Property | Value |
|----------|-------|
| **Decision ID** | D-004 |
| **Decision** | Include landscape discipline in scope count (6 disciplines) but flag as TBD |
| **Trigger** | CONFLICT-01 in documents: Datasheet/Specification flag landscape as TBD; some Procedure steps assume inclusion |
| **Evidence** | Datasheet.md: "Landscape: Site landscaping - TBD: Scope inclusion requires confirmation"; Specification.md RQ-06: "TBD: Scope requires confirmation" |
| **Impacted WBS/CBS** | L001 (Discipline Scope Matrix) |
| **Estimate Impact** | Minor - approximately $100-200 additional effort if landscape is confirmed in scope |
| **Override** | Resolve CONFLICT-01 with human ruling; if landscape excluded, reduce discipline count to 5 |

---

## D-005: Contingency Percentage

| Property | Value |
|----------|-------|
| **Decision ID** | D-005 |
| **Decision** | Apply 15% contingency on E+PM base estimate |
| **Trigger** | Default contingency method (PCT_BY_BUCKET) with no config override |
| **Evidence** | AGENT_ESTIMATING protocol default; moderate uncertainty factors identified |
| **Impacted WBS/CBS** | CONT bucket |
| **Estimate Impact** | $1,100 contingency reserve (15% of $7,250 base) |
| **Override** | Set contingency_method and rates in _CONFIG.md for next run |

---

## D-006: Third-Party Code Review Position

| Property | Value |
|----------|-------|
| **Decision ID** | D-006 |
| **Decision** | Assume third-party code review is recommended but not mandatory; plan document describes strategy only |
| **Trigger** | CONFLICT-03 in documents: Specification RQ-07 does not mandate; Guidance recommends as best practice |
| **Evidence** | Guidance.md: "Recommend third-party code review at CD phase as best practice for Fire Hall facilities" |
| **Impacted WBS/CBS** | L006 (Code Compliance Strategy) |
| **Estimate Impact** | Effort reflects documenting the strategy; actual third-party fees (if applicable) would be post-award cost |
| **Override** | If third-party code review is mandated, estimate would need to include post-award fees |

---

## D-007: Professional Rate Allowances

| Property | Value |
|----------|-------|
| **Decision ID** | D-007 |
| **Decision** | Use tiered professional rate allowances: Design Manager $175/hr, Proposal Manager $150/hr, Technical Staff $100/hr |
| **Trigger** | No rate tables available; rates must be assumed |
| **Evidence** | Typical Canadian AEC professional services rates (ASSUMPTION) |
| **Impacted WBS/CBS** | All E and PM line items |
| **Estimate Impact** | Rate assumptions drive total estimate; actual rates may vary +/- 25% |
| **Override** | Provide project-specific rate tables in _RateTables/ folder |

---

## D-008: BIM vs 2D Approach

| Property | Value |
|----------|-------|
| **Decision ID** | D-008 |
| **Decision** | Plan document describes BIM-first approach per Guidance recommendation; no additional cost for BIM documentation |
| **Trigger** | Guidance.md recommends BIM-first position for proposal credibility |
| **Evidence** | Guidance.md [SL:B-005]: "recommend BIM if: (1) Owner has BIM requirement, (2) project complexity warrants 3D coordination" |
| **Impacted WBS/CBS** | L003 (Coordination Process Documentation) |
| **Estimate Impact** | BIM workflow documentation included in coordination effort; no separate BIM tooling costs in proposal phase |
| **Override** | If 2D-only approach specified, reduce coordination documentation effort slightly |

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
| **Snapshot** | EST_DEL-03-02_2026-02-04_1323 |
| **Total Decisions** | 8 |
