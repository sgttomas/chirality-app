# Assumptions Log

## Snapshot Identification

| Attribute | Value |
|---|---|
| **Snapshot ID** | EST_DEL-05-03_2026-02-04_1323 |
| **Deliverable** | DEL-05-03 Pricing Narrative and Assumptions |

---

## Assumptions

### A-001: Contract Type Assumption

| Field | Value |
|---|---|
| **Assumption ID** | A-001 |
| **Statement** | Fixed-price Design-Build RFP proposal context assumed |
| **Why Needed** | Contract type affects pricing structure and risk allocation; not explicitly stated in source documents |
| **Impacted WBS/CBS** | All line items |
| **Cost Impact** | Defines overall scope and pricing approach |
| **Confidence** | MED |
| **Resolution Path** | Verify contract type in RFP documents; update pricing approach if GMP or cost-plus |

---

### A-002: Professional Services Rate

| Field | Value |
|---|---|
| **Assumption ID** | A-002 |
| **Statement** | Professional services (Estimator / Commercial Lead) billed at approximately $150/hr blended rate |
| **Why Needed** | No rate tables provided; rate required to price narrative production effort |
| **Impacted WBS/CBS** | E (Engineering & Design) |
| **Cost Impact** | ~$8,600 for document production line items (L-001 through L-008) |
| **Confidence** | LOW |
| **Resolution Path** | Provide rate tables in _RateTables/ with actual professional billing rates |

**Basis:** Central Alberta professional services market; Design-Build proposal estimating and commercial roles typically $120-$180/hr for senior professional staff.

---

### A-003: Value Alternatives Scope

| Field | Value |
|---|---|
| **Assumption ID** | A-003 |
| **Statement** | Value alternatives (Section 7, SOW-028) may be minimal or omitted if no alternatives are being proposed |
| **Why Needed** | Source documents indicate value alternatives are optional; scope uncertain |
| **Impacted WBS/CBS** | E (L-007) |
| **Cost Impact** | $800 allowance; could be $0 if no alternatives or higher if extensive alternatives |
| **Confidence** | LOW |
| **Resolution Path** | Confirm with Estimator / Commercial Lead whether value alternatives will be included and to what extent |

---

### A-004: Schedules A/B Availability

| Field | Value |
|---|---|
| **Assumption ID** | A-004 |
| **Statement** | Schedules A (DEL-05-01) and B (DEL-05-02) will be available in draft or final form for cross-reference |
| **Why Needed** | R-8 requires consistency between narrative and schedules; cross-reference effort depends on availability |
| **Impacted WBS/CBS** | PM (L-009) |
| **Cost Impact** | $1,000 allowance for cross-reference; if schedules unavailable, effort deferred or reduced |
| **Confidence** | MED |
| **Resolution Path** | Confirm status of DEL-05-01 and DEL-05-02; adjust effort if unavailable |

---

### A-005: Related Deliverables Availability

| Field | Value |
|---|---|
| **Assumption ID** | A-005 |
| **Statement** | Related deliverables (DEL-02-01, DEL-04-01, DEL-08-01, DEL-09-01, DEL-09-02) will be available in draft form for cross-reference |
| **Why Needed** | Procedure Step 5 requires cross-deliverable consistency check; effort depends on availability |
| **Impacted WBS/CBS** | PM (L-010) |
| **Cost Impact** | $1,200 allowance; if deliverables unavailable, cross-check deferred |
| **Confidence** | MED |
| **Resolution Path** | Confirm status of related deliverables; adjust scope if unavailable |

---

### A-006: Specification Verification Effort

| Field | Value |
|---|---|
| **Assumption ID** | A-006 |
| **Statement** | Specification requirement verification (R-1 through R-10) requires approximately 4-5 hours of effort |
| **Why Needed** | Must price verification checklist completion |
| **Impacted WBS/CBS** | PM (L-011) |
| **Cost Impact** | $800 allowance |
| **Confidence** | MED |
| **Resolution Path** | Track actual effort during production; update estimate for future runs |

---

### A-007: Review and Approval Cycle

| Field | Value |
|---|---|
| **Assumption ID** | A-007 |
| **Statement** | One review cycle with minor revisions assumed; no major rewrites |
| **Why Needed** | Review effort depends on revision scope |
| **Impacted WBS/CBS** | PM (L-012) |
| **Cost Impact** | $1,000 allowance; could increase significantly with multiple revision cycles |
| **Confidence** | LOW |
| **Resolution Path** | Actual effort depends on review feedback; allowance may need adjustment |

**Risk:** If major revisions required, review cycle cost could double or triple.

---

### A-008: Document Integration Effort

| Field | Value |
|---|---|
| **Assumption ID** | A-008 |
| **Statement** | Final PDF integration requires approximately 2-3 hours of formatting and assembly effort |
| **Why Needed** | Deliverable must be integrated into proposal PDF per PKG-01 |
| **Impacted WBS/CBS** | PM (L-013) |
| **Cost Impact** | $400 allowance |
| **Confidence** | MED |
| **Resolution Path** | Standard proposal production task; confidence adequate |

---

## Assumptions Index

| ID | Summary | Confidence | Cost Impact |
|---|---|---|---|
| A-001 | Fixed-price Design-Build context | MED | Scope definition |
| A-002 | Professional rate ~$150/hr | LOW | $8,600 |
| A-003 | Value alternatives may be minimal | LOW | $800 (+/- variable) |
| A-004 | Schedules A/B available | MED | $1,000 |
| A-005 | Related deliverables available | MED | $1,200 |
| A-006 | Verification effort ~4-5 hrs | MED | $800 |
| A-007 | One review cycle assumed | LOW | $1,000 (+/- variable) |
| A-008 | Integration effort ~2-3 hrs | MED | $400 |

---

## TBD Items from Source Documents

The following TBD items from Datasheet.md and Specification.md affect estimate accuracy:

| Source | TBD Item | Impact on Estimate |
|---|---|---|
| Datasheet - Key Narrative Elements | Site servicing allowance value | Affects Section 5 content complexity |
| Datasheet - Key Narrative Elements | Market pricing date | Affects Section 8 content |
| Datasheet - Key Narrative Elements | Labor and material availability assumptions | Affects Section 8 content |
| Datasheet - Key Narrative Elements | Site access and logistics assumptions | Affects Section 8 content |
| Datasheet - Key Narrative Elements | Long-lead procurement items | Affects Section 8 content |
| Datasheet - Key Narrative Elements | Contingency percentage and rationale | Affects Section 8 content |
| Specification R-5 | Additional Options scope descriptions | Affects Section 6 effort |
| Specification R-4 (OI-004) | FF&E treatment decision | Affects Section 4 content |

**Note:** These TBD items represent estimator inputs required for narrative production. Until resolved, effort estimates for affected sections remain uncertain.

---

**Note:** All assumptions documented here are professional judgment-based due to absence of rate tables and historical data. Provide rate tables or actual project data to improve estimate accuracy in future runs.
