# Assumptions Log

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-07-03_2026-02-04_1323 |
| **Deliverable** | DEL-07-03 Appendix I - Subtrade and Consultant List |

---

## Assumptions

### A-001: Proposal Manager Labor Rate

| Field | Value |
|-------|-------|
| **Assumption ID** | A-001 |
| **Statement** | Proposal Manager fully burdened labor rate = CAD 150/hr |
| **Why Needed** | No rate table or quote available for labor pricing |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; CBS: E |
| **Cost Impact** | PM hours (19 hrs) x CAD 150 = CAD 2,850 |
| **Confidence** | LOW |
| **Resolution Path** | Provide actual PM rate in `_RateTables/LaborRates.csv` |

---

### A-002: HR/Team Admin Labor Rate

| Field | Value |
|-------|-------|
| **Assumption ID** | A-002 |
| **Statement** | HR/Team Admin fully burdened labor rate = CAD 85/hr |
| **Why Needed** | No rate table or quote available for labor pricing |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; CBS: E |
| **Cost Impact** | Admin hours (17 hrs) x CAD 85 = CAD 1,445 |
| **Confidence** | LOW |
| **Resolution Path** | Provide actual Admin rate in `_RateTables/LaborRates.csv` |

---

### A-003: Document Assembly Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-003 |
| **Statement** | Total document assembly effort estimated at 36 hours (19 PM + 17 Admin) |
| **Why Needed** | Procedure.md provides process steps but no effort estimates |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; all line items |
| **Cost Impact** | Base estimate = CAD 4,450 |
| **Confidence** | LOW |
| **Resolution Path** | Track actual hours on similar proposals for calibration |

---

### A-004: Quality Review Cycles

| Field | Value |
|-------|-------|
| **Assumption ID** | A-004 |
| **Statement** | Assume 1 quality review cycle (2 hrs PM) with no major rework required |
| **Why Needed** | Number of review iterations not specified in Procedure.md |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-011 |
| **Cost Impact** | L-011 = CAD 300 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Add contingency for potential multiple review cycles |

---

### A-005: Coordination Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-005 |
| **Statement** | Cross-deliverable coordination (DEL-07-01, DEL-07-02, DEL-05-02) requires 6 hours PM time |
| **Why Needed** | Procedure Steps 4, 5, 6 require coordination but no effort estimate provided |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-007, L-008, L-009 |
| **Cost Impact** | CAD 900 (6 hrs x CAD 150/hr) |
| **Confidence** | MEDIUM |
| **Resolution Path** | Depends on status of upstream deliverables when work begins |

---

### A-006: Template Acquisition Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-006 |
| **Statement** | Template acquisition and review (Procedure Step 1) requires 2 hrs PM time |
| **Why Needed** | RFP Appendix I template noted as TBD in Procedure.md |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-001 |
| **Cost Impact** | L-001 = CAD 300 |
| **Confidence** | MEDIUM |
| **Resolution Path** | If template readily available, effort may reduce |

---

### A-007: Scope Checklist Development Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-007 |
| **Statement** | Scope category checklist development (Procedure Step 2) requires 3 hrs PM time |
| **Why Needed** | Checklist requires review of Decomposition, Addendum 03, and program requirements |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-002 |
| **Cost Impact** | L-002 = CAD 450 |
| **Confidence** | MEDIUM |
| **Resolution Path** | May reduce if similar checklist exists from prior proposals |

---

### A-008: Design Consultant Identification Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-008 |
| **Statement** | Identifying 12 design consultant firms requires 2 hrs PM + 4 hrs Admin |
| **Why Needed** | 12 design disciplines per Specification REQ-02 coverage checklist |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-003 |
| **Cost Impact** | L-003 = CAD 600 |
| **Confidence** | LOW |
| **Resolution Path** | Effort depends on whether firms are pre-committed or require outreach |

---

### A-009: Construction Subtrade Identification Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-009 |
| **Statement** | Identifying 10+ construction subtrades requires 2 hrs PM + 2 hrs Admin |
| **Why Needed** | Construction trades required per Design-Build model (REQ-06) |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-004 |
| **Cost Impact** | L-004 = CAD 510 |
| **Confidence** | LOW |
| **Resolution Path** | Effort depends on whether subtrades are pre-committed |

---

### A-010: Specialty Systems Identification Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-010 |
| **Statement** | Identifying 6 specialty system suppliers requires 1.5 hrs PM + 2 hrs Admin |
| **Why Needed** | Addendum 03 specifies 6 specialty systems (doors, exhaust, generator, fuel, sumps, security) |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-005 |
| **Cost Impact** | L-005 = CAD 380 |
| **Confidence** | LOW |
| **Resolution Path** | Specialty systems may require more outreach than standard disciplines |

---

### A-011: Personnel Detail Collection Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-011 |
| **Statement** | Collecting key personnel details for 25-30 firms requires 4 hrs Admin time |
| **Why Needed** | REQ-05 requires key personnel identification for each firm |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-006 |
| **Cost Impact** | L-006 = CAD 340 |
| **Confidence** | LOW |
| **Resolution Path** | Effort varies with firm responsiveness and data availability |

---

### A-012: Cost Breakdown Cross-Check Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-012 |
| **Statement** | Cross-checking with DEL-05-02 cost breakdown requires 2 hrs PM time |
| **Why Needed** | Procedure Step 4 requires alignment with Appendix H Schedule B |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-007 |
| **Cost Impact** | L-007 = CAD 300 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Depends on DEL-05-02 availability and complexity |

---

### A-013: Addenda Compliance Review Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-013 |
| **Statement** | Addenda compliance review requires 1 hr PM time |
| **Why Needed** | Procedure Step 5 requires verification against Addendum 03 |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-008 |
| **Cost Impact** | L-008 = CAD 150 |
| **Confidence** | HIGH |
| **Resolution Path** | Straightforward compliance check; low variance expected |

---

### A-014: Cross-Deliverable Consistency Check Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-014 |
| **Statement** | Cross-referencing DEL-07-01 and DEL-07-02 requires 3 hrs PM time |
| **Why Needed** | Procedure Step 6 and REQ-08 require consistency across PKG-03 deliverables |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-009 |
| **Cost Impact** | L-009 = CAD 450 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Depends on DEL-07-01 and DEL-07-02 status |

---

### A-015: Table Formatting Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-015 |
| **Statement** | Formatting final Appendix I table requires 4 hrs Admin time |
| **Why Needed** | Procedure Step 7 requires formatting per RFP template |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-010 |
| **Cost Impact** | L-010 = CAD 340 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Depends on template complexity and formatting requirements |

---

### A-016: Quality Review Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-016 |
| **Statement** | Quality review and approval (Procedure Step 8) requires 2 hrs PM time |
| **Why Needed** | REQ-07 scoring criteria review required before approval |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-011 |
| **Cost Impact** | L-011 = CAD 300 |
| **Confidence** | MEDIUM |
| **Resolution Path** | May increase if issues found requiring rework |

---

### A-017: PDF Integration Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-017 |
| **Statement** | Final PDF integration requires 2 hrs Admin time |
| **Why Needed** | Procedure Step 9 requires integration into DEL-01-02 |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-012 |
| **Cost Impact** | L-012 = CAD 170 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Depends on PDF assembly workflow complexity |

---

### A-018: Compliance Matrix Update Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-018 |
| **Statement** | Compliance matrix update requires 1 hr Admin + 0.5 hr PM time |
| **Why Needed** | Procedure Step 10 requires DEL-01-01 update |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; L-013 |
| **Cost Impact** | L-013 = CAD 160 |
| **Confidence** | HIGH |
| **Resolution Path** | Standard administrative task |

---

## Assumptions Summary

| Category | Count | Total Impact (CAD) |
|----------|-------|-------------------|
| Labor Rates | 2 | 4,295 |
| Effort Estimates | 16 | 4,450 |
| **Total Assumptions** | **18** | |
