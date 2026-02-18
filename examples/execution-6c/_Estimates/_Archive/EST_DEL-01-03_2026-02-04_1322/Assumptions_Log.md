# Assumptions Log

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-01-03_2026-02-04_1322 |
| **Deliverable** | DEL-01-03 BondingAndInsuranceEvidence |

---

## Assumption Register

### A-001: Surety Relationship Status

| Field | Value |
|-------|-------|
| **Assumption ID** | A-001 |
| **Statement** | Proponent has an existing, established surety relationship |
| **Why Needed** | Datasheet marks surety relationship status as TBD; timeline and effort depend on this |
| **Impacted WBS/CBS** | PKG-01/DEL-01-03; L-002 (PM/Surety Coordination) |
| **Cost Impact** | If new relationship: +8-16 hours PM effort (CAD $1,200-$2,400 increase) |
| **Confidence** | MED |
| **Resolution Path** | Proposal Manager to confirm surety relationship status |

---

### A-002: Alberta Professional Services Rates

| Field | Value |
|-------|-------|
| **Assumption ID** | A-002 |
| **Statement** | Labor rates reflect typical Alberta professional services market (Proposal Manager CAD $150/hr, Estimator CAD $175/hr, Document Control CAD $100/hr) |
| **Why Needed** | No rate table provided; labor rates required for effort-based costing |
| **Impacted WBS/CBS** | All labor-based line items |
| **Cost Impact** | +/- 20% rate variance = +/- CAD $1,000 base cost impact |
| **Confidence** | MED |
| **Resolution Path** | Provide actual proponent rates in `_RateTables/` |

---

### A-003: RFP Requirements Extraction Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-003 |
| **Statement** | RFP Section 5.3.1 requirements extraction requires 4 hours of Proposal Manager time |
| **Why Needed** | Step 1 of Procedure requires RFP review; PDF not currently accessible |
| **Impacted WBS/CBS** | PKG-01/DEL-01-03; L-001 (PM) |
| **Cost Impact** | Range: 2-8 hours (CAD $300-$1,200) depending on RFP complexity |
| **Confidence** | MED |
| **Resolution Path** | Refine after RFP Section 5.3.1 is extracted |

---

### A-004: Surety Coordination Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-004 |
| **Statement** | Surety coordination and Agreement to Bond acquisition requires 8 hours of Proposal Manager time |
| **Why Needed** | Step 2 of Procedure requires engagement with surety/broker |
| **Impacted WBS/CBS** | PKG-01/DEL-01-03; L-002 (PM) |
| **Cost Impact** | Range: 4-16 hours (CAD $600-$2,400) depending on surety responsiveness |
| **Confidence** | MED |
| **Resolution Path** | Historical data from similar proposals; surety relationship status confirmation |

---

### A-005: Bond Cost Statement Preparation Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-005 |
| **Statement** | Bond cost inclusion statement preparation requires 4 hours of Proposal Manager time |
| **Why Needed** | Step 3 of Procedure requires statement drafting and reconciliation |
| **Impacted WBS/CBS** | PKG-01/DEL-01-03; L-003 (PM) |
| **Cost Impact** | Range: 2-6 hours (CAD $300-$900) |
| **Confidence** | MED |
| **Resolution Path** | Historical data from similar proposals |

---

### A-006: Insurance Summary Effort (Conditional)

| Field | Value |
|-------|-------|
| **Assumption ID** | A-006 |
| **Statement** | Insurance approach summary preparation requires 4 hours of Proposal Manager time, if required |
| **Why Needed** | Step 4 of Procedure is conditional on RFP Section 5.3.1 requirements |
| **Impacted WBS/CBS** | PKG-01/DEL-01-03; L-004 (PM) |
| **Cost Impact** | CAD $0-$600 depending on whether insurance summary is required |
| **Confidence** | LOW |
| **Resolution Path** | Extract RFP Section 5.3.1 to determine if insurance summary is required |

---

### A-007: Package Assembly Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-007 |
| **Statement** | Deliverable package assembly and cross-referencing requires 4 hours of Proposal Manager time |
| **Why Needed** | Step 5 of Procedure requires assembly and coordination with DEL-01-01 and DEL-01-02 |
| **Impacted WBS/CBS** | PKG-01/DEL-01-03; L-005 (PM) |
| **Cost Impact** | Range: 2-6 hours (CAD $300-$900) |
| **Confidence** | MED |
| **Resolution Path** | Historical data from similar proposals |

---

### A-008: Final QC Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-008 |
| **Statement** | Final QC and approval process requires 4 hours of Proposal Manager time |
| **Why Needed** | Step 6 of Procedure requires comprehensive QC checklist completion |
| **Impacted WBS/CBS** | PKG-01/DEL-01-03; L-006 (PM) |
| **Cost Impact** | Range: 2-6 hours (CAD $300-$900) |
| **Confidence** | MED |
| **Resolution Path** | Historical data from similar proposals |

---

### A-009: Estimator Support Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-009 |
| **Statement** | Estimator support for bond cost estimation and Appendix H coordination requires 4 hours |
| **Why Needed** | Step 3 requires Estimator input for bond cost inclusion in pricing documents |
| **Impacted WBS/CBS** | PKG-01/DEL-01-03; L-007 (E) |
| **Cost Impact** | Range: 2-8 hours (CAD $350-$1,400) |
| **Confidence** | MED |
| **Resolution Path** | Historical data; complexity of pricing reconciliation |

---

### A-010: Surety Processing Fee

| Field | Value |
|-------|-------|
| **Assumption ID** | A-010 |
| **Statement** | Surety/broker may charge administrative fee of CAD $500 for Agreement to Bond letter issuance |
| **Why Needed** | Some sureties/brokers charge administrative fees for proposal-stage letters |
| **Impacted WBS/CBS** | PKG-01/DEL-01-03; L-008 (P) |
| **Cost Impact** | Range: CAD $0-$1,000 (may be waived or higher depending on surety) |
| **Confidence** | LOW |
| **Resolution Path** | Confirm with surety/broker if fees apply |

---

### A-011: Insurance Broker Consultation Fee

| Field | Value |
|-------|-------|
| **Assumption ID** | A-011 |
| **Statement** | Insurance broker consultation fee of CAD $300 for insurance approach confirmation |
| **Why Needed** | Step 4 may require insurance broker input; conditional on RFP requirements |
| **Impacted WBS/CBS** | PKG-01/DEL-01-03; L-009 (P) |
| **Cost Impact** | Range: CAD $0-$500 (may be waived; may not be required) |
| **Confidence** | LOW |
| **Resolution Path** | Confirm RFP requirements and broker fee structure |

---

### A-012: Document Control Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-012 |
| **Statement** | Document control and filing requires 2 hours at administrative rate |
| **Why Needed** | Procedure requires records retention and surety license verification documentation |
| **Impacted WBS/CBS** | PKG-01/DEL-01-03; L-010 (PM) |
| **Cost Impact** | Range: 1-4 hours (CAD $100-$400) |
| **Confidence** | MED |
| **Resolution Path** | Historical data from similar proposals |

---

## Summary

| Assumptions Logged | 12 |
|--------------------|---|
| LOW Confidence | A-006, A-010, A-011 |
| MED Confidence | A-001 through A-005, A-007 through A-009, A-012 |
| HIGH Confidence | None |

**Note:** All assumptions are effort-based or fee-based allowances. No material quantity assumptions (this is an administrative deliverable, not construction work).
