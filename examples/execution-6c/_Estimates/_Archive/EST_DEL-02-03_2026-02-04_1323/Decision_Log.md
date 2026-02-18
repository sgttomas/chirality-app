# Decision Log

## Snapshot: EST_DEL-02-03_2026-02-04_1323

This log documents all decisions made during estimate preparation. Each decision represents a choice made due to missing input, ambiguity, or conflict.

---

## Decision Entries

### D-001: Currency Selection
| Field | Value |
|-------|-------|
| **Decision ID** | D-001 |
| **Decision Statement** | Use CAD (Canadian Dollars) as the estimate currency |
| **Trigger** | Currency specified in task brief as CAD |
| **Evidence** | Task assignment specifies "Currency: CAD" |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | N/A - currency specification |
| **Override Method** | Update `_CONFIG.md` with different currency setting |

---

### D-002: Pricing Basis Selection
| Field | Value |
|-------|-------|
| **Decision ID** | D-002 |
| **Decision Statement** | Use allowance-based pricing for all line items (no rate tables available) |
| **Trigger** | `_RateTables/` directory is empty; no project-specific rate tables provided |
| **Evidence** | Directory scan shows empty `_RateTables/` folder |
| **Impacted WBS/CBS** | All line items (E - Engineering & Design) |
| **Estimate Impact** | Moderate uncertainty; actual costs may vary from allowances |
| **Override Method** | Provide rate tables in `_Estimates/_RateTables/` for future estimates |

---

### D-003: CBS Classification
| Field | Value |
|-------|-------|
| **Decision ID** | D-003 |
| **Decision Statement** | Classify deliverable under CBS bucket "Engineering & Design (E)" |
| **Trigger** | Deliverable is a narrative document requiring professional services; no procurement, construction, or commissioning activities |
| **Evidence** | _CONTEXT.md (Type: Narrative Document); Specification.md (documentation outputs) |
| **Impacted WBS/CBS** | PKG-04/DEL-02-03 -> CBS: E |
| **Estimate Impact** | Determines contingency rate (20% for E bucket) |
| **Override Method** | Adjust CBS mapping in WBS_CBS_Matrix.csv if project CBS differs |

---

### D-004: Effort Estimate Basis
| Field | Value |
|-------|-------|
| **Decision ID** | D-004 |
| **Decision Statement** | Base effort estimates on typical Design Brief narrative complexity for municipal Design-Build proposal |
| **Trigger** | No historical data or rate tables available for this specific project type |
| **Evidence** | Specification.md (4-6 pages target), Procedure.md (9-step process), Guidance.md (8 principles) |
| **Impacted WBS/CBS** | All labor line items |
| **Estimate Impact** | Effort estimates may be conservative (+/- 30%); actual effort depends on author experience and scope refinement |
| **Override Method** | Provide project-specific effort benchmarks or historical data |

---

### D-005: Optional Diagrams Inclusion
| Field | Value |
|-------|-------|
| **Decision ID** | D-005 |
| **Decision Statement** | Include allowance for optional diagrams (HVAC zoning, solar-ready roof plan) at reduced scope |
| **Trigger** | Procedure.md Step 7 indicates diagrams are optional; Guidance.md Consideration 4 notes file size constraints |
| **Evidence** | Specification.md REQ-008.4 (diagrams optional); Guidance.md (1-3 diagrams suggested) |
| **Impacted WBS/CBS** | Line items 6-7 (Graphics/Diagrams) |
| **Estimate Impact** | ~$2,000 CAD for 2 diagrams; may be reduced to $0 if text-only approach selected |
| **Override Method** | Confirm diagram scope with Proposal Manager before production |

---

### D-006: Contingency Rate Selection
| Field | Value |
|-------|-------|
| **Decision ID** | D-006 |
| **Decision Statement** | Apply 20% contingency rate to Engineering & Design bucket |
| **Trigger** | PCT_BY_BUCKET method selected; allowance-based estimate has moderate uncertainty |
| **Evidence** | AGENT_ESTIMATING.md (default contingency method); early project stage; allowance pricing |
| **Impacted WBS/CBS** | CBS: E (Engineering & Design) |
| **Estimate Impact** | Adds ~$2,000 CAD contingency to base estimate |
| **Override Method** | Update `_CONFIG.md` with `contingency_method: RISK_BASED` for Monte Carlo approach |

---

## Summary

| Decision ID | Category | Impact Level |
|-------------|----------|--------------|
| D-001 | Currency | Low (specification) |
| D-002 | Pricing Basis | High (affects all line items) |
| D-003 | CBS Classification | Medium (contingency rate) |
| D-004 | Effort Basis | High (affects all labor estimates) |
| D-005 | Scope (Diagrams) | Low-Medium (~$2,000 variance) |
| D-006 | Contingency | Medium (~$2,000 reserve) |

---

## Document History
- 2026-02-04 1323 - Initial decision log created (ESTIMATING Agent)
