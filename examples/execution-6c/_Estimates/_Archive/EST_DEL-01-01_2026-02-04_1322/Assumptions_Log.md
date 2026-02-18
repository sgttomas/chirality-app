# Assumptions Log
## DEL-01-01: ComplianceMatrixAndChecklist Estimate

---

## Purpose

This log records all assumptions and allowances used in the estimate where:
- Explicit data was not available in source documents
- Pricing was based on allowance rather than quotes or rate tables
- Quantities were estimated rather than extracted from documents

---

## Assumption Register

### A-001: Proposal Manager Hourly Rate

| Property | Value |
|----------|-------|
| **Assumption ID** | A-001 |
| **Statement** | Proposal Manager fully-burdened rate is CAD $150/hour |
| **Why Needed** | No rate tables provided; need labour pricing basis |
| **Impacted WBS/CBS** | E, PM categories; Lines L-001 through L-003, L-005 through L-008, L-010 |
| **Cost Impact** | $5,550 (based on 37 PM hours) |
| **Confidence** | MEDIUM |
| **Resolution Path** | Provide project rate tables in _RateTables/ folder |

---

### A-002: Proposal Controls Specialist Hourly Rate

| Property | Value |
|----------|-------|
| **Assumption ID** | A-002 |
| **Statement** | Proposal Controls Specialist fully-burdened rate is CAD $100/hour |
| **Why Needed** | No rate tables provided; need labour pricing basis |
| **Impacted WBS/CBS** | E category; Lines L-004, L-009, L-011 |
| **Cost Impact** | $1,400 (based on 14 specialist hours) |
| **Confidence** | MEDIUM |
| **Resolution Path** | Provide project rate tables in _RateTables/ folder |

---

### A-003: Fully Burdened Rate Inclusion

| Property | Value |
|----------|-------|
| **Assumption ID** | A-003 |
| **Statement** | Hourly rates include all burdens: benefits, overhead, office costs, etc. |
| **Why Needed** | Need clarity on what rates include |
| **Impacted WBS/CBS** | All labour lines |
| **Cost Impact** | Determines total cost basis |
| **Confidence** | MEDIUM |
| **Resolution Path** | Confirm burden/overhead policy in _CONFIG.md |

---

### A-004: Requirement Extraction Effort

| Property | Value |
|----------|-------|
| **Assumption ID** | A-004 |
| **Statement** | Extracting and mapping each RFP requirement takes ~0.3 hours (18 minutes) average |
| **Why Needed** | No historical data; need parametric basis |
| **Impacted WBS/CBS** | E; Line L-001 |
| **Cost Impact** | $2,400 (16 hours for 51 requirements) |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track actuals; adjust for future estimates |

**Range:** 0.2-0.5 hours/requirement depending on complexity

---

### A-005: Addenda Item Extraction Effort

| Property | Value |
|----------|-------|
| **Assumption ID** | A-005 |
| **Statement** | Extracting and mapping each addendum item takes ~0.3 hours average |
| **Why Needed** | No historical data; need parametric basis |
| **Impacted WBS/CBS** | E; Line L-002 |
| **Cost Impact** | $1,200 (8 hours for 24 items) |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track actuals; adjust for future estimates |

---

### A-006: Risk Register Item Effort

| Property | Value |
|----------|-------|
| **Assumption ID** | A-006 |
| **Statement** | Documenting each high-risk item with owner and resolution path takes ~0.5 hours |
| **Why Needed** | No historical data; need parametric basis |
| **Impacted WBS/CBS** | E; Line L-003 |
| **Cost Impact** | $600 (4 hours for 8 risk items) |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track actuals; adjust for future estimates |

---

### A-007: Cross-Reference Verification Effort

| Property | Value |
|----------|-------|
| **Assumption ID** | A-007 |
| **Statement** | Cross-referencing compliance matrix with decomposition scope ledger takes 4 hours |
| **Why Needed** | Task complexity estimated; no historical data |
| **Impacted WBS/CBS** | E; Line L-004 |
| **Cost Impact** | $400 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track actuals; adjust for future estimates |

---

### A-008: Package Coordination Effort

| Property | Value |
|----------|-------|
| **Assumption ID** | A-008 |
| **Statement** | Coordinating deliverable mapping with each of 9 package leads takes ~0.6 hours average |
| **Why Needed** | Estimate coordination overhead; no historical data |
| **Impacted WBS/CBS** | E; Line L-005 |
| **Cost Impact** | $900 (6 hours total) |
| **Confidence** | LOW |
| **Resolution Path** | Depends on team size and communication efficiency |

**Range:** 0.3-1.0 hours/package depending on complexity

---

### A-009: Milestone Review Meeting Duration

| Property | Value |
|----------|-------|
| **Assumption ID** | A-009 |
| **Statement** | Milestone review meetings average 2-3 hours including prep |
| **Why Needed** | Estimate review overhead; no specific guidance |
| **Impacted WBS/CBS** | PM; Lines L-006, L-007, L-008 |
| **Cost Impact** | $1,050 (7 hours total) |
| **Confidence** | MEDIUM |
| **Resolution Path** | Align with project meeting cadence |

---

### A-010: Living Document Maintenance Factor

| Property | Value |
|----------|-------|
| **Assumption ID** | A-010 |
| **Statement** | Ongoing maintenance effort is approximately 20% of initial creation effort |
| **Why Needed** | Estimate update cycles; no historical data |
| **Impacted WBS/CBS** | E; Line L-009 |
| **Cost Impact** | $800 (8 hours) |
| **Confidence** | LOW |
| **Resolution Path** | Track actual update effort; varies by RFP changes |

**Range:** 10-30% depending on proposal volatility

---

### A-011: Truth-Testing and Sign-Off Effort

| Property | Value |
|----------|-------|
| **Assumption ID** | A-011 |
| **Statement** | Final verification and sign-off by Proposal Manager takes 4 hours |
| **Why Needed** | Estimate verification overhead; no historical data |
| **Impacted WBS/CBS** | PM; Line L-010 |
| **Cost Impact** | $600 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track actuals; adjust for future estimates |

---

### A-012: Documentation and Record Keeping

| Property | Value |
|----------|-------|
| **Assumption ID** | A-012 |
| **Statement** | Administrative documentation (extraction logs, audit trail) takes 2 hours |
| **Why Needed** | Estimate admin overhead; no historical data |
| **Impacted WBS/CBS** | E; Line L-011 |
| **Cost Impact** | $200 |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track actuals; adjust for future estimates |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Assumptions | 12 |
| Rate Assumptions | 3 |
| Effort Assumptions | 9 |
| Total Cost Impact | $7,250 (base estimate) |
| Average Confidence | MEDIUM |

---

## Assumptions by Confidence Level

| Confidence | Count | Cost Impact |
|------------|-------|-------------|
| HIGH | 0 | $0 |
| MEDIUM | 10 | $6,050 |
| LOW | 2 | $1,200 |

---

## Document Control

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-01-01_2026-02-04_1322 |
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
