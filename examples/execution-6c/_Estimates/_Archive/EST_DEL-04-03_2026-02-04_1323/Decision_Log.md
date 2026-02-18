# Decision Log
## DEL-04-03: Communications and Reporting Plan Estimate

---

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-04-03_2026-02-04_1323 |
| **Deliverable** | DEL-04-03 Communications and Reporting Plan |

---

## Decision Register

### D-001: Currency Selection

| Property | Value |
|----------|-------|
| **Decision ID** | D-001 |
| **Decision** | Use CAD as base currency for this estimate |
| **Trigger** | Operator directive specified CAD currency |
| **Evidence** | Task brief specified "Currency: CAD" |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | All amounts expressed in CAD; no conversion required |
| **Override Path** | Update _CONFIG.md with different currency setting |

---

### D-002: Pricing Method Selection

| Property | Value |
|----------|-------|
| **Decision ID** | D-002 |
| **Decision** | Use ALLOWANCE method for all line items |
| **Trigger** | No rate tables available in _RateTables/ folder; no vendor quotes for professional services |
| **Evidence** | Glob search of _Estimates/_RateTables/ returned no files |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | 100% ALLOWANCE-based pricing; confidence LOW-MEDIUM |
| **Override Path** | Provide rate tables in _RateTables/ for next estimate run |

---

### D-003: Responsible Party Rate Assignment

| Property | Value |
|----------|-------|
| **Decision ID** | D-003 |
| **Decision** | Assign Construction Manager at CAD 140/hr as primary resource |
| **Trigger** | _CONTEXT.md designates Construction Manager as responsible party |
| **Evidence** | _CONTEXT.md: "Responsible: Construction Manager" |
| **Impacted WBS/CBS** | E (Engineering), all development line items |
| **Estimate Impact** | 48 hours at CAD 140/hr = CAD 6,720 (76% of base) |
| **Override Path** | Update rate tables with actual Construction Manager rates |

---

### D-004: Contingency Method and Rate

| Property | Value |
|----------|-------|
| **Decision ID** | D-004 |
| **Decision** | Apply 15% contingency using PCT_BY_BUCKET method |
| **Trigger** | Default contingency method per AGENT_ESTIMATING protocol |
| **Evidence** | BOE.md contingency section; no project-specific contingency guidance |
| **Impacted WBS/CBS** | CONT (Contingency) |
| **Estimate Impact** | CAD 1,300 contingency on CAD 8,620 base |
| **Override Path** | Set contingency_method in _CONFIG.md; provide risk-based analysis for RISK_BASED method |

---

### D-005: CBS Mapping - Engineering vs Project Management

| Property | Value |
|----------|-------|
| **Decision ID** | D-005 |
| **Decision** | Map deliverable development work to E (Engineering); map review/oversight to PM |
| **Trigger** | Deliverable type is "Plan Document" requiring professional services effort |
| **Evidence** | _CONTEXT.md: "Type: Plan Document"; Datasheet.md content analysis |
| **Impacted WBS/CBS** | E, PM buckets |
| **Estimate Impact** | E = CAD 7,720 (90%); PM = CAD 900 (10%) of base |
| **Override Path** | Define CBS mapping rules in _CONFIG.md if different split required |

---

### D-006: Effort Estimate Basis

| Property | Value |
|----------|-------|
| **Decision ID** | D-006 |
| **Decision** | Base effort estimates on requirement complexity and deliverable scope analysis |
| **Trigger** | No historical effort data available for comparable deliverables |
| **Evidence** | Datasheet.md, Specification.md analysis; 12 requirements, 8 stakeholders, 6 artifact types |
| **Impacted WBS/CBS** | All E and PM line items |
| **Estimate Impact** | 64 total hours estimated; parametric basis |
| **Override Path** | Provide historical effort data from comparable projects |

---

### D-007: Cross-Deliverable Verification Scope

| Property | Value |
|----------|-------|
| **Decision ID** | D-007 |
| **Decision** | Include effort for consistency verification with 4 adjacent deliverables |
| **Trigger** | Guidance.md Section "Cross-Deliverable Communication Integration (B-009)" |
| **Evidence** | DEL-04-01, DEL-04-02, DEL-03-01, DEL-06-01 identified as requiring alignment |
| **Impacted WBS/CBS** | E (line item L-017) |
| **Estimate Impact** | 4 hours at CAD 100/hr = CAD 400 |
| **Override Path** | Remove if cross-deliverable verification is handled separately |

---

### D-008: Visual Artifact Scope

| Property | Value |
|----------|-------|
| **Decision ID** | D-008 |
| **Decision** | Include 6 hours for creation of 3 visual artifacts |
| **Trigger** | Procedure.md Step 13 item F-004 requires visual artifacts |
| **Evidence** | "Meeting structure diagram, reporting cadence timeline, escalation path flowchart" |
| **Impacted WBS/CBS** | E (line item L-016) |
| **Estimate Impact** | 6 hours at CAD 100/hr = CAD 600 |
| **Override Path** | Adjust if visual artifacts are handled by graphics specialist at different rate |

---

## Summary

| Decision Count | 8 |
|----------------|---|
| **Decisions affecting scope** | D-006, D-007, D-008 |
| **Decisions affecting pricing** | D-001, D-002, D-003, D-004, D-005 |
| **Decisions with material impact** | D-002 (all pricing), D-003 (76% of base) |

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
| **Snapshot** | EST_DEL-04-03_2026-02-04_1323 |
