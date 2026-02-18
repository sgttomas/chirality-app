# Decision Log
## DEL-06-01: CommissioningTrainingCloseoutWarrantyNarrative

---

## Snapshot Information

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-06-01_2026-02-04_1323 |
| **Created** | 2026-02-04 |

---

## Decision Register

### D-001: Currency Selection

| Property | Value |
|----------|-------|
| **Decision ID** | D-001 |
| **Decision Statement** | Use CAD as the single currency for this estimate snapshot |
| **Trigger** | Operator directive specified CAD; no config file exists |
| **Evidence** | Task brief: "Currency: CAD" |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | All amounts reported in CAD |
| **Override for Next Run** | Set `currency: CAD` in `_CONFIG.md` |

---

### D-002: Pricing Date Selection

| Property | Value |
|----------|-------|
| **Decision ID** | D-002 |
| **Decision Statement** | Use 2026-02 as pricing date ("dollars of February 2026") |
| **Trigger** | No explicit pricing date in documents; default to current month |
| **Evidence** | No evidence; default per AGENT_ESTIMATING protocol |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | Rates assumed valid as of 2026-02 |
| **Override for Next Run** | Set `pricing_date: YYYY-MM` in `_CONFIG.md` |

---

### D-003: Deliverable Scope Definition

| Property | Value |
|----------|-------|
| **Decision ID** | D-003 |
| **Decision Statement** | Scope limited to proposal deliverable production (narrative document), not post-award commissioning execution |
| **Trigger** | Deliverable is a narrative for RFP submission, not commissioning services |
| **Evidence** | Procedure.md: "Dual-use note: This procedure focuses on producing the proposal deliverable"; _CONTEXT.md: Type = "Narrative Document" |
| **Impacted WBS/CBS** | CBS mapping excludes COM (Commissioning execution) |
| **Estimate Impact** | Estimate covers professional services for narrative creation only |
| **Override for Next Run** | N/A - scope determination follows deliverable definition |

---

### D-004: WBS to CBS Mapping

| Property | Value |
|----------|-------|
| **Decision ID** | D-004 |
| **Decision Statement** | Map DEL-06-01 to CBS categories E (Engineering & Design) and PM (Project Management) |
| **Trigger** | Deliverable is a proposal narrative requiring professional services effort |
| **Evidence** | _CONTEXT.md: Type = "Narrative Document"; Responsible = "Commissioning Lead / PM"; Procedure.md Steps 1-13 describe document development activities |
| **Impacted WBS/CBS** | Line items assigned to E or PM |
| **Estimate Impact** | 92% E, 8% PM |
| **Override for Next Run** | N/A - CBS mapping follows deliverable type |

---

### D-005: Contingency Method and Rate

| Property | Value |
|----------|-------|
| **Decision ID** | D-005 |
| **Decision Statement** | Apply 15% contingency on base estimate using PCT_BY_BUCKET method |
| **Trigger** | Default contingency method per AGENT_ESTIMATING protocol; rate selected based on uncertainty factors |
| **Evidence** | No project-specific contingency guidance; uncertainty factors include: (1) five integrated narrative components, (2) cross-deliverable coordination, (3) potential quality review iterations |
| **Impacted WBS/CBS** | CONT category |
| **Estimate Impact** | CAD $1,170 contingency on $7,800 base (~$8,900 rounded total) |
| **Override for Next Run** | Set `contingency_method: RISK_BASED` in `_CONFIG.md` for detailed risk-based contingency |

---

### D-006: Effort Basis Selection

| Property | Value |
|----------|-------|
| **Decision ID** | D-006 |
| **Decision Statement** | Use Procedure.md estimated durations as primary basis for effort quantities |
| **Trigger** | No detailed task breakdown or project-specific productivity data available |
| **Evidence** | Procedure.md Steps 1-13 include "Estimated Duration" for each step ranging from 1 to 6 hours |
| **Impacted WBS/CBS** | All labour line items (L-001 through L-016) |
| **Estimate Impact** | 40 hours Commissioning Lead based on summed step estimates |
| **Override for Next Run** | Provide detailed task breakdown or historical actuals for similar narratives |

---

### D-007: Commissioning Lead Role and Rate

| Property | Value |
|----------|-------|
| **Decision ID** | D-007 |
| **Decision Statement** | Price Commissioning Lead at CAD $175/hr as senior technical professional |
| **Trigger** | No rate tables available; need rate for primary author role |
| **Evidence** | _CONTEXT.md: Responsible = "Commissioning Lead / PM"; Procedure.md Prerequisites require commissioning experience; rate allowance A-001 |
| **Impacted WBS/CBS** | All Commissioning Lead line items (L-001 through L-013) |
| **Estimate Impact** | CAD $7,000 Commissioning Lead labour |
| **Override for Next Run** | Provide rate table with commissioning professional rates |

---

### D-008: Technical Lead Support Inclusion

| Property | Value |
|----------|-------|
| **Decision ID** | D-008 |
| **Decision Statement** | Include 4 hours of Technical Lead support (2 hrs mechanical, 2 hrs electrical/fire) |
| **Trigger** | Datasheet and Specification identify critical systems requiring technical input for credible narrative |
| **Evidence** | Datasheet: "Critical systems: Generator supporting ICP, fire apparatus exhaust systems, vehicle bay systems"; Specification R-003: Critical Systems Commissioning requirement; Addendum 03 technical impacts |
| **Impacted WBS/CBS** | L-014, L-015 (E category) |
| **Estimate Impact** | CAD $600 Technical Lead support |
| **Override for Next Run** | Define specific technical review scope and hours based on team composition |

---

### D-009: Proposal Manager Oversight Inclusion

| Property | Value |
|----------|-------|
| **Decision ID** | D-009 |
| **Decision Statement** | Include 4 hours of Proposal Manager oversight and integration review |
| **Trigger** | Procedure.md Steps 10, 13 reference Proposal Manager involvement; deliverable must integrate with full proposal |
| **Evidence** | Procedure.md: Step 10 verification includes "Commissioning Lead + Proposal Manager"; Step 13 output includes "Proposal Manager confirmation" |
| **Impacted WBS/CBS** | L-016 (PM category) |
| **Estimate Impact** | CAD $600 Proposal Manager effort |
| **Override for Next Run** | Define Proposal Manager integration effort based on proposal assembly process |

---

### D-010: Rounding Policy

| Property | Value |
|----------|-------|
| **Decision ID** | D-010 |
| **Decision Statement** | Round summary totals to nearest CAD $100 |
| **Trigger** | Default rounding policy per AGENT_ESTIMATING protocol; no config override |
| **Evidence** | AGENT_ESTIMATING.md: "rounding: nearest 1,000 (default)"; adjusted to $100 for proportionality with estimate size |
| **Impacted WBS/CBS** | Summary totals only; Detail.csv maintains full precision |
| **Estimate Impact** | Summary shows $8,900 vs Detail sum of ~$8,870 |
| **Override for Next Run** | Set `rounding: 100` in `_CONFIG.md` |

---

## Document Control

| Property | Value |
|----------|-------|
| **Total Decisions** | 10 |
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
