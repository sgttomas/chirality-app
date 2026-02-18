# Decision Log

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-07-03_2026-02-04_1323 |
| **Deliverable** | DEL-07-03 Appendix I - Subtrade and Consultant List |

---

## Decisions

### D-001: Pricing Method Selection

| Field | Value |
|-------|-------|
| **Decision ID** | D-001 |
| **Decision** | Use ALLOWANCE method for all line items |
| **Trigger** | No vendor quotes or project rate tables available in `_Estimates/_RateTables/` |
| **Evidence** | Glob search of `_Estimates/**/*` returned no files |
| **Impacted WBS/CBS** | PKG-03/DEL-07-03; CBS: E (Engineering & Design) |
| **Estimate Impact** | 100% of base estimate relies on allowances; LOW confidence |
| **Override Path** | Provide rate tables to `_Estimates/_RateTables/` containing labor rates for Proposal Manager and HR/Team Admin roles |

---

### D-002: Indirects Embedding

| Field | Value |
|-------|-------|
| **Decision ID** | D-002 |
| **Decision** | Embed indirects in fully burdened labor rates rather than applying separate indirect percentage |
| **Trigger** | Proposal preparation scope is primarily labor-driven with minimal material/equipment costs |
| **Evidence** | Procedure.md shows 10 labor-intensive steps with no material procurement |
| **Impacted WBS/CBS** | All line items; CBS: E |
| **Estimate Impact** | Simplifies estimate structure; indirects captured in CAD 150/hr (PM) and CAD 85/hr (Admin) rates |
| **Override Path** | If unburdened rates are required, adjust labor rates and add separate CI (Construction Indirects) line items |

---

### D-003: Contingency Percentage

| Field | Value |
|-------|-------|
| **Decision ID** | D-003 |
| **Decision** | Apply 15% contingency to base estimate |
| **Trigger** | 100% allowance-based pricing creates higher uncertainty than mixed-method estimates |
| **Evidence** | No quotes or rate tables available; all pricing based on assumed labor rates and effort |
| **Impacted WBS/CBS** | All CBS buckets |
| **Estimate Impact** | Contingency = CAD 670 (15% of CAD 4,450 base) |
| **Override Path** | Adjust contingency percentage in `_CONFIG.md` if project risk profile differs |

---

### D-004: Currency Selection

| Field | Value |
|-------|-------|
| **Decision ID** | D-004 |
| **Decision** | Use CAD (Canadian Dollars) as estimate currency |
| **Trigger** | User instruction specified "Currency: CAD" |
| **Evidence** | Task brief explicitly stated "Currency: CAD" |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | All amounts denominated in CAD |
| **Override Path** | Override in `_CONFIG.md` currency field |

---

### D-005: Labor Rate Assumptions

| Field | Value |
|-------|-------|
| **Decision ID** | D-005 |
| **Decision** | Assume Proposal Manager rate = CAD 150/hr; HR/Team Admin rate = CAD 85/hr (fully burdened) |
| **Trigger** | No rate tables or quotes available to establish actual rates |
| **Evidence** | Rates assumed based on typical Alberta professional services market for municipal projects |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | Total labor value = CAD 4,295 based on these rates |
| **Override Path** | Provide actual labor rates in `_Estimates/_RateTables/LaborRates.csv` |

---

### D-006: Team Size Assumption

| Field | Value |
|-------|-------|
| **Decision ID** | D-006 |
| **Decision** | Assume Appendix I will list approximately 25-30 firms/consultants |
| **Trigger** | Specification REQ-02 coverage checklist implies 12+ design disciplines, 10+ construction trades, 6+ specialty systems |
| **Evidence** | Specification.md REQ-02 coverage checklist; Guidance.md Example 1 scope categories |
| **Impacted WBS/CBS** | L-003 through L-006 (team identification effort) |
| **Estimate Impact** | Effort scaled for 25-30 firms; smaller team reduces effort, larger team increases effort |
| **Override Path** | Adjust line item quantities if actual team size is known |

---

### D-007: Scope Classification (CBS)

| Field | Value |
|-------|-------|
| **Decision ID** | D-007 |
| **Decision** | Classify all DEL-07-03 costs under CBS "E" (Engineering & Design) |
| **Trigger** | DEL-07-03 is a proposal preparation deliverable (documentation/compliance), not construction work |
| **Evidence** | Datasheet.md Type = "Compliance Document"; Procedure.md steps are office-based document production |
| **Impacted WBS/CBS** | All line items assigned CBS = E |
| **Estimate Impact** | No impact on total; affects CBS rollup categorization |
| **Override Path** | Reclassify to PM (Project Management) if preferred for proposal preparation costs |

---

## Decision Summary

| Decision ID | Short Description | Confidence Impact |
|-------------|-------------------|-------------------|
| D-001 | ALLOWANCE pricing method | LOW |
| D-002 | Embedded indirects | MEDIUM |
| D-003 | 15% contingency | MEDIUM |
| D-004 | CAD currency | HIGH |
| D-005 | Labor rate assumptions | LOW |
| D-006 | 25-30 firms assumed | MEDIUM |
| D-007 | CBS = E (Engineering) | HIGH |
