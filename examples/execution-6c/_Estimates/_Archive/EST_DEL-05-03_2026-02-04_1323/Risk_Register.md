# Risk Register

## Snapshot Identification

| Attribute | Value |
|---|---|
| **Snapshot ID** | EST_DEL-05-03_2026-02-04_1323 |
| **Deliverable** | DEL-05-03 Pricing Narrative and Assumptions |

---

## Risks

### R-001: No Rate Tables Available

| Field | Value |
|---|---|
| **Risk ID** | R-001 |
| **Risk Driver** | Price |
| **Cause** | _RateTables directory is empty; no project-specific or industry rate data available |
| **Consequence** | 100% of pricing based on allowances; estimate accuracy uncertain |
| **Affected CBS** | All (E, PM, CONT) |
| **Affected WBS** | PKG-02 / DEL-05-03 |
| **Suggested Mitigation** | Provide rate tables for professional services in _RateTables/; use historical project data if available |
| **Contingency Handling** | 15% contingency applied to account for pricing uncertainty; potential +/- 30% variance on actuals |

---

### R-002: Multiple TBD Items in Source Documents

| Field | Value |
|---|---|
| **Risk ID** | R-002 |
| **Risk Driver** | Scope |
| **Cause** | Datasheet and Specification contain multiple TBD items requiring estimator input |
| **Consequence** | Actual effort to produce narrative may differ significantly from estimate |
| **Affected CBS** | E (document production) |
| **Affected WBS** | PKG-02 / DEL-05-03 |
| **Suggested Mitigation** | Estimator / Commercial Lead to provide TBD inputs before narrative production begins |
| **Contingency Handling** | Allowances include buffer; 15% contingency provides additional coverage |

**TBD Items Identified:**
- Site servicing allowance value
- Market pricing date
- Labor/material availability assumptions
- Site access assumptions
- Long-lead procurement items
- Contingency percentage and rationale
- Additional Options scope descriptions
- FF&E treatment decision (OI-004)

---

### R-003: Value Alternatives Scope Uncertainty

| Field | Value |
|---|---|
| **Risk ID** | R-003 |
| **Risk Driver** | Scope |
| **Cause** | SOW-028 value alternatives are optional; unclear whether extensive alternatives will be proposed |
| **Consequence** | Section 7 effort could range from minimal ($0) to significant (+$2,000) |
| **Affected CBS** | E (L-007) |
| **Affected WBS** | PKG-02 / DEL-05-03 |
| **Suggested Mitigation** | Confirm with Estimator / Commercial Lead early whether value alternatives will be included |
| **Contingency Handling** | $800 allowance included; contingency provides upside coverage |

---

### R-004: Cross-Deliverable Dependency Delays

| Field | Value |
|---|---|
| **Risk ID** | R-004 |
| **Risk Driver** | Interface |
| **Cause** | Cross-reference effort (L-009, L-010) depends on availability of related deliverables |
| **Consequence** | If Schedules A/B or related deliverables not available, cross-check effort deferred or rework required |
| **Affected CBS** | PM |
| **Affected WBS** | PKG-02 / DEL-05-03 |
| **Suggested Mitigation** | Coordinate with DEL-05-01, DEL-05-02, and PKG-04/PKG-06/PKG-09 deliverable owners on availability timing |
| **Contingency Handling** | If deliverables delayed, cross-check can be deferred to enrichment pass with placeholder assumptions |

---

### R-005: Review Cycle Expansion

| Field | Value |
|---|---|
| **Risk ID** | R-005 |
| **Risk Driver** | Productivity |
| **Cause** | Review and approval cycle (L-012) assumed to be one cycle with minor revisions |
| **Consequence** | Major revisions or multiple review cycles could double or triple review effort |
| **Affected CBS** | PM |
| **Affected WBS** | PKG-02 / DEL-05-03 |
| **Suggested Mitigation** | Ensure clear scope agreement and checklist before drafting; use Specification R-1 through R-10 as acceptance criteria |
| **Contingency Handling** | $1,000 allowance includes some buffer; contingency provides additional coverage |

---

## Risk Summary Matrix

| Risk ID | Driver | Likelihood | Impact | Contingency Coverage |
|---|---|---|---|---|
| R-001 | Price | HIGH | HIGH | 15% contingency |
| R-002 | Scope | MED | MED | Allowances + 15% contingency |
| R-003 | Scope | MED | LOW | $800 allowance |
| R-004 | Interface | MED | MED | Deferral option available |
| R-005 | Productivity | LOW | MED | $1,000 allowance + contingency |

---

## Contingency Allocation

| Category | Base Amount | Contingency Rate | Contingency Amount |
|---|---|---|---|
| E (Engineering & Design) | $8,600 | 15% | ~$1,290 |
| PM (Project Management) | $4,400 | 15% | ~$660 |
| **Total** | **$13,000** | **15%** | **$1,650** |

**Note:** 15% contingency rate applied uniformly across categories. Higher rate justified due to:
- R-001: 100% allowance-based pricing
- R-002: Multiple TBD items creating scope uncertainty
- R-003 through R-005: Additional scope and productivity risks

---

## Risk Mitigation Actions for Next Run

1. **Provide rate tables** in `_RateTables/` for professional services hourly rates
2. **Resolve TBD items** in Datasheet and Specification before next estimate run
3. **Confirm value alternatives scope** early in production planning
4. **Coordinate cross-deliverable timing** with related deliverable owners
5. **Establish clear review criteria** using Specification requirements as checklist

---

**Note:** This risk register documents estimate-specific risks. Project delivery risks should be documented in DEL-09-01 (Risk Register deliverable) as part of PKG-09.
