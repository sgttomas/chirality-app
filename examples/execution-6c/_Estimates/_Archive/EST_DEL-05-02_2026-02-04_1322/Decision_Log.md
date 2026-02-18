# Decision Log

## Snapshot Information

| Field | Value |
|-------|-------|
| **Snapshot ID** | EST_DEL-05-02_2026-02-04_1322 |
| **Deliverable** | DEL-05-02 AppendixH ScheduleB CostBreakdown |

---

## Decisions

### D-001: Pickled Sand Storage Building Exclusion
| Field | Value |
|-------|-------|
| **Decision ID** | D-001 |
| **Decision Statement** | Exclude pickled sand storage building from all base scope cost estimates |
| **Trigger** | Addendum 03 explicitly removed building from RFP scope |
| **Evidence** | Decomposition Section 4 (Addendum 03 impacts); Specification.md R-007 |
| **Impacted WBS/CBS** | PKG-02/DEL-05-02; Building (B) category |
| **Estimate Impact** | Reduces base building cost; prevents disqualification risk |
| **Override Path** | N/A - Mandatory per RFP Addendum 03 |

---

### D-002: 12-Acre Developable Site Constraint
| Field | Value |
|-------|-------|
| **Decision ID** | D-002 |
| **Decision Statement** | Limit sitework scope to 12-acre developable area (not full 20-acre parcel) |
| **Trigger** | Addendum 03 clarified developable area; 8 acres allocated to dog park/storm pond in flood fringe |
| **Evidence** | Decomposition Section 4; Specification.md R-008 |
| **Impacted WBS/CBS** | PKG-02/DEL-05-02; Sitework (SW) category |
| **Estimate Impact** | Reduces sitework costs by ~40% vs full parcel assumption |
| **Override Path** | N/A - Mandatory per RFP Addendum 03 |

---

### D-003: General Requirements Factor
| Field | Value |
|-------|-------|
| **Decision ID** | D-003 |
| **Decision Statement** | Apply 10% of direct construction (Building + Sitework) for General Requirements |
| **Trigger** | No explicit GR breakdown in source documents; need runnable basis |
| **Evidence** | Guidance.md (typical allocation 8-12%); industry standard |
| **Impacted WBS/CBS** | PKG-02/DEL-05-02; General Requirements (GR) category |
| **Estimate Impact** | ~$500,000-$700,000 depending on direct construction total |
| **Override Path** | Provide detailed GR breakdown or adjust percentage in _CONFIG.md |

---

### D-004: Contractor OH&P Markup
| Field | Value |
|-------|-------|
| **Decision ID** | D-004 |
| **Decision Statement** | Assume 15% contractor overhead and profit markup embedded in unit rates |
| **Trigger** | No firm-specific markup guidance available |
| **Evidence** | Guidance.md Trade-off 2 (contingency visibility); industry standard 15-25% |
| **Impacted WBS/CBS** | All categories |
| **Estimate Impact** | Approximately 15% of all direct costs |
| **Override Path** | Provide firm-specific markup policy |

---

### D-005: Design Contingency Application
| Field | Value |
|-------|-------|
| **Decision ID** | D-005 |
| **Decision Statement** | Apply 10% design contingency as explicit line item |
| **Trigger** | Early-stage Design-Build proposal; concept design not complete |
| **Evidence** | Guidance.md Principle 5; standard early-stage estimating practice |
| **Impacted WBS/CBS** | All categories; Contingency (CONT) CBS |
| **Estimate Impact** | ~$600,000-$800,000 |
| **Override Path** | Adjust contingency percentage based on design maturity |

---

### D-006: Currency Selection
| Field | Value |
|-------|-------|
| **Decision ID** | D-006 |
| **Decision Statement** | Use CAD (Canadian dollars) as estimate currency |
| **Trigger** | Project located in Penhold, Alberta, Canada |
| **Evidence** | Decomposition (Alberta location); AGENT_ESTIMATING.md default rules |
| **Impacted WBS/CBS** | All categories |
| **Estimate Impact** | All values expressed in CAD |
| **Override Path** | Override currency in _CONFIG.md if required |

---

### D-007: Building Area Allowance
| Field | Value |
|-------|-------|
| **Decision ID** | D-007 |
| **Decision Statement** | Assume 20,000 SF building gross floor area for parametric costing |
| **Trigger** | DEL-02-01 Concept Design not available; need runnable basis |
| **Evidence** | Typical fire hall + public works facility size; ASSUMPTION |
| **Impacted WBS/CBS** | PKG-02/DEL-05-02; Building (B) category |
| **Estimate Impact** | Primary driver for building cost estimate |
| **Override Path** | Update with actual GFA from DEL-02-01 when available |

---

### D-008: Building Unit Cost Rate
| Field | Value |
|-------|-------|
| **Decision ID** | D-008 |
| **Decision Statement** | Use $300/SF parametric rate for combined fire hall + public works building |
| **Trigger** | No rate tables available; need runnable basis |
| **Evidence** | Typical Alberta municipal facility costs 2025-2026; ASSUMPTION |
| **Impacted WBS/CBS** | PKG-02/DEL-05-02; Building (B) category |
| **Estimate Impact** | Building base cost = 20,000 SF x $300/SF = $6,000,000 |
| **Override Path** | Provide project rate tables or vendor quotes |

---

### D-009: Sitework Unit Cost Rate
| Field | Value |
|-------|-------|
| **Decision ID** | D-009 |
| **Decision Statement** | Use $12/SF parametric rate for 12-acre (522,720 SF) site development |
| **Trigger** | No site plans or quantity takeoffs available; need runnable basis |
| **Evidence** | Typical Alberta sitework costs; limited development on functional areas only; ASSUMPTION |
| **Impacted WBS/CBS** | PKG-02/DEL-05-02; Sitework (SW) category |
| **Estimate Impact** | Site development allowance based on partial site coverage |
| **Override Path** | Provide detailed site plans and quantity takeoffs |

---

### D-010: Additional Options Scope Assumptions
| Field | Value |
|-------|-------|
| **Decision ID** | D-010 |
| **Decision Statement** | Price Additional Options 1-6 as lump-sum allowances based on typical scope |
| **Trigger** | Detailed scope for each option not defined |
| **Evidence** | Decomposition Section 5 (Vocabulary Map); Datasheet.md Additional Options table |
| **Impacted WBS/CBS** | PKG-02/DEL-05-02; Options 1-6 |
| **Estimate Impact** | Options total ~$350,000 capital + monitoring fee |
| **Override Path** | Provide detailed scope and specifications for each option |

---

## Document Information

| Field | Value |
|-------|-------|
| Created | 2026-02-04 |
| Total Decisions | 10 |
