# Assumptions Log

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-03-01_2026-02-04_1453 |
| **Deliverable** | DEL-03-01 Design Methodology Narrative |

---

## Assumptions Register

### A-001: Design Manager/PM Hourly Rate

| Field | Value |
|-------|-------|
| **Assumption ID** | A-001 |
| **Statement** | Design Manager/PM hourly rate is $175 CAD/hour (fully burdened) |
| **Why Needed** | No rate tables available; labor rate required for pricing |
| **Impacted WBS/CBS** | E-001, E-002, E-003, E-004; PM-002 |
| **Cost Impact** | $5,950 CAD direct labor; significant driver of total estimate |
| **Range** | $150-$200 CAD/hr typical for Alberta senior PM/Design Manager |
| **Confidence** | MEDIUM |
| **Resolution Path** | Provide actual billing rate in `_RateTables/labor_rates.csv` |

---

### A-002: Lead Architect Hourly Rate

| Field | Value |
|-------|-------|
| **Assumption ID** | A-002 |
| **Statement** | Lead Architect hourly rate is $185 CAD/hour (fully burdened) |
| **Why Needed** | No rate tables available; architect input required per Prerequisites |
| **Impacted WBS/CBS** | E-005 |
| **Cost Impact** | $740 CAD |
| **Range** | $160-$210 CAD/hr typical for Alberta registered architect |
| **Confidence** | MEDIUM |
| **Resolution Path** | Provide actual billing rate in `_RateTables/labor_rates.csv` |

---

### A-003: Discipline Lead Average Hourly Rate

| Field | Value |
|-------|-------|
| **Assumption ID** | A-003 |
| **Statement** | Discipline Leads (Civil/Structural/Mechanical/Electrical) average hourly rate is $165 CAD/hour |
| **Why Needed** | No rate tables available; discipline input required per Prerequisites |
| **Impacted WBS/CBS** | E-006 |
| **Cost Impact** | $1,320 CAD (8 hours total across 4 disciplines) |
| **Range** | $140-$190 CAD/hr typical for Alberta P.Eng. discipline leads |
| **Confidence** | MEDIUM |
| **Resolution Path** | Provide actual billing rates by discipline in `_RateTables/labor_rates.csv` |

---

### A-004: Construction Manager Hourly Rate

| Field | Value |
|-------|-------|
| **Assumption ID** | A-004 |
| **Statement** | Construction Manager hourly rate is $160 CAD/hour (fully burdened) |
| **Why Needed** | No rate tables available; CM input required for constructability integration |
| **Impacted WBS/CBS** | E-007 |
| **Cost Impact** | $480 CAD |
| **Range** | $140-$180 CAD/hr typical for Alberta CM roles |
| **Confidence** | MEDIUM |
| **Resolution Path** | Provide actual billing rate in `_RateTables/labor_rates.csv` |

---

### A-005: Scheduler Hourly Rate

| Field | Value |
|-------|-------|
| **Assumption ID** | A-005 |
| **Statement** | Scheduler hourly rate is $140 CAD/hour (fully burdened) |
| **Why Needed** | No rate tables available; scheduler input required per Prerequisites |
| **Impacted WBS/CBS** | E-008 |
| **Cost Impact** | $280 CAD |
| **Range** | $120-$160 CAD/hr typical for Alberta scheduling professionals |
| **Confidence** | MEDIUM |
| **Resolution Path** | Provide actual billing rate in `_RateTables/labor_rates.csv` |

---

### A-006: Graphics/CAD Technician Hourly Rate

| Field | Value |
|-------|-------|
| **Assumption ID** | A-006 |
| **Statement** | Graphics/CAD Technician hourly rate is $95 CAD/hour (fully burdened) |
| **Why Needed** | No rate tables available; visual aids production required per Step 6 |
| **Impacted WBS/CBS** | E-009 |
| **Cost Impact** | $760 CAD |
| **Range** | $75-$115 CAD/hr typical for Alberta CAD/graphics technicians |
| **Confidence** | MEDIUM |
| **Resolution Path** | Provide actual billing rate in `_RateTables/labor_rates.csv` |

---

### A-007: Administrative/QC Support Hourly Rate

| Field | Value |
|-------|-------|
| **Assumption ID** | A-007 |
| **Statement** | Administrative/QC Support hourly rate is $85 CAD/hour (fully burdened) |
| **Why Needed** | No rate tables available; admin support required for formatting and QC |
| **Impacted WBS/CBS** | E-010 |
| **Cost Impact** | $340 CAD |
| **Range** | $65-$100 CAD/hr typical for Alberta admin/tech support |
| **Confidence** | MEDIUM |
| **Resolution Path** | Provide actual billing rate in `_RateTables/labor_rates.csv` |

---

### A-008: Stakeholder Review Cycle Count

| Field | Value |
|-------|-------|
| **Assumption ID** | A-008 |
| **Statement** | Two (2) stakeholder review cycles will be required before final approval |
| **Why Needed** | Number of review iterations not specified in deliverable documents |
| **Impacted WBS/CBS** | PM-002 |
| **Cost Impact** | $700 CAD (4 hours at $175/hr) |
| **Range** | 1-4 cycles typical depending on team QA maturity and stakeholder alignment |
| **Confidence** | LOW |
| **Resolution Path** | Define review cycle requirements in proposal production plan |

---

### A-009: Narrative Authoring Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-009 |
| **Statement** | Primary narrative authoring (Steps 1-3) requires 16 hours of Design Manager/PM time |
| **Why Needed** | No historical effort data; effort must be estimated from procedure complexity |
| **Impacted WBS/CBS** | E-001 |
| **Cost Impact** | $2,800 CAD |
| **Range** | 12-24 hours depending on author experience and content complexity |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track actual effort on this or similar deliverables; provide historical data |

---

### A-010: Cross-Deliverable Coordination Effort

| Field | Value |
|-------|-------|
| **Assumption ID** | A-010 |
| **Statement** | Cross-deliverable coordination (Step 4) requires 4 hours of Design Manager/PM time |
| **Why Needed** | Coordination effort with DEL-04-01, DEL-08-01, DEL-03-02 not quantified |
| **Impacted WBS/CBS** | E-002 |
| **Cost Impact** | $700 CAD |
| **Range** | 2-8 hours depending on deliverable maturity and team communication |
| **Confidence** | MEDIUM |
| **Resolution Path** | Track coordination meeting time; adjust based on actual proposal workflow |

---

### A-011: Graphics Production Scope

| Field | Value |
|-------|-------|
| **Assumption ID** | A-011 |
| **Statement** | Visual aids production requires 8 hours for 3-4 diagrams (flowchart, timeline, matrices) |
| **Why Needed** | Visual aids listed as recommended in Procedure.md Step 6; specific scope not defined |
| **Impacted WBS/CBS** | E-009 |
| **Cost Impact** | $760 CAD |
| **Range** | 4-16 hours depending on complexity and proposal presentation standards |
| **Confidence** | LOW |
| **Resolution Path** | Define required graphics in proposal style guide; provide templates if available |

---

### A-012: Full Team Engagement

| Field | Value |
|-------|-------|
| **Assumption ID** | A-012 |
| **Statement** | All discipline leads (4) will provide input; Construction Manager and Scheduler will participate |
| **Why Needed** | Procedure.md Prerequisites lists required input from multiple team members |
| **Impacted WBS/CBS** | E-005 through E-008 |
| **Cost Impact** | $2,540 CAD combined |
| **Range** | May reduce if fewer disciplines engaged; may increase if more iterations |
| **Confidence** | MEDIUM |
| **Resolution Path** | Confirm team availability; adjust roles based on actual proposal team structure |

---

## Assumptions Summary Statistics

| Metric | Value |
|--------|-------|
| Total Assumptions Logged | 12 |
| Rate Assumptions | 7 (A-001 to A-007) |
| Effort Assumptions | 5 (A-008 to A-012) |
| HIGH Confidence | 0 |
| MEDIUM Confidence | 10 |
| LOW Confidence | 2 (A-008, A-011) |
| Total Cost Impact from Assumptions | $13,546 CAD (100% of base estimate) |

---

## Rate Assumptions Summary Table

| Role | Rate (CAD/hr) | Assumption ID | Confidence |
|------|-------------:|---------------|------------|
| Design Manager/PM | $175 | A-001 | MEDIUM |
| Lead Architect | $185 | A-002 | MEDIUM |
| Discipline Lead (avg) | $165 | A-003 | MEDIUM |
| Construction Manager | $160 | A-004 | MEDIUM |
| Scheduler | $140 | A-005 | MEDIUM |
| Graphics/CAD Tech | $95 | A-006 | MEDIUM |
| Admin/QC Support | $85 | A-007 | MEDIUM |

---

**Generated:** 2026-02-04
**Agent:** ESTIMATING (Type 2)
