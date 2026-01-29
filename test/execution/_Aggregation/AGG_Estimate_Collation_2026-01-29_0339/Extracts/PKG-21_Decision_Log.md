# Decision Log

## PKG-21: Building Structures & Envelope

**Snapshot ID:** EST_PKG21_DRAFT_2026-01-28_0030

---

## Decisions

### D-001: MCC Building Size Assumption

| Field | Value |
|-------|-------|
| Decision | Assumed MCC building footprint of 600 m² (approx. 6,500 ft²) |
| Trigger | Building size not defined in deliverable documents; all references marked TBD |
| Evidence | DEL-21.01 Datasheet line 82: "Size/footprint: **TBD**" |
| Impacted WBS/CBS | PKG-21 / MAT, CD |
| Estimate Impact | HIGH — Building size is primary cost driver; ±50% on building materials/labor |
| Override Path | Provide MCC equipment layout with space requirements; update MAT and CD line items |

---

### D-002: Building Construction Type

| Field | Value |
|-------|-------|
| Decision | Assumed Pre-Engineered Metal Building (PEMB) construction with insulated metal panels |
| Trigger | Construction type marked TBD in deliverables |
| Evidence | DEL-21.01 Datasheet line 82: "Construction type: **TBD** — **ASSUMPTION**: Pre-engineered metal building or modular construction typical for industrial MCC buildings" |
| Impacted WBS/CBS | PKG-21 / MAT, CD |
| Estimate Impact | MEDIUM — PEMB vs modular vs conventional construction affects cost structure |
| Override Path | Confirm preferred construction method in _CONFIG.md or provide vendor budget |

---

### D-003: Foundation Type

| Field | Value |
|-------|-------|
| Decision | Assumed pile foundations with concrete pile caps and slab-on-grade |
| Trigger | Foundation type not defined; geotechnical investigation not available |
| Evidence | DEL-21.03 Datasheet line 67: "Foundation type: **TBD** — Spread footings, piles, mat (based on geotechnical investigation)" |
| Impacted WBS/CBS | PKG-21 / MAT, CD |
| Estimate Impact | MEDIUM — Pile foundations vs spread footings can vary ±30% on foundation costs |
| Override Path | Provide geotechnical recommendations; update foundation line items |

---

### D-004: Operator Shelter Quantity

| Field | Value |
|-------|-------|
| Decision | Assumed 4 operator shelters to serve 32 railcar unloading stations |
| Trigger | Number of shelters not defined |
| Evidence | DEL-21.01 Datasheet line 86: "Number of shelters: **TBD** — **ASSUMPTION**: Related to 32 railcar unloading stations" |
| Impacted WBS/CBS | PKG-21 / MAT, CD |
| Estimate Impact | MEDIUM — Each shelter adds ~$70,000 (supply + install) |
| Override Path | Confirm shelter count per PKG-10 railcar unloading layout |

---

### D-005: No Vendor Quotes Available

| Field | Value |
|-------|-------|
| Decision | Proceeded with parametric/allowance pricing due to absence of vendor quotes |
| Trigger | No pricing sources found in workspace |
| Evidence | Source discovery searched deliverable folders and _RateTables/; no quotes found |
| Impacted WBS/CBS | All CBS buckets |
| Estimate Impact | HIGH — 100% allowance/parametric pricing triggers contingency uplift |
| Override Path | Obtain budget quotes from PEMB suppliers and building contractors |

---

### D-006: No Rate Tables Available

| Field | Value |
|-------|-------|
| Decision | Proceeded without project-specific rate tables |
| Trigger | _RateTables/ folder empty or not populated |
| Evidence | Rate table search returned no results |
| Impacted WBS/CBS | All CBS buckets |
| Estimate Impact | MEDIUM — Using industry benchmarks instead of project rates |
| Override Path | Provide building rate tables in `_RateTables/` |

---

### D-007: PM Factor Selection

| Field | Value |
|-------|-------|
| Decision | Applied 6% PM factor on (CD + CI + MAT) |
| Trigger | No project-specific PM rates or durations available |
| Evidence | Fallback Typical Model (AGENT_ESTIMATING.md line 673): "EPCM/PM (PM) = 0.06 × (CD + CI + MAT + FRT)" |
| Impacted WBS/CBS | PKG-21 / PM |
| Estimate Impact | LOW — PM calculated as $67,000 |
| Override Path | Provide PM level of effort or duration-based estimate |

---

### D-008: Procurement Factor Selection

| Field | Value |
|-------|-------|
| Decision | Applied 2% procurement factor on MAT |
| Trigger | No project-specific procurement scope or rates |
| Evidence | Fallback Typical Model (AGENT_ESTIMATING.md line 669): "Procurement services (P) = 0.02 × (MAT + FRT)" |
| Impacted WBS/CBS | PKG-21 / P |
| Estimate Impact | LOW — Procurement calculated as $14,000 |
| Override Path | Provide procurement scope of work or detailed estimate |

---

### D-009: Construction Indirects Factor Selection

| Field | Value |
|-------|-------|
| Decision | Applied 18% CI factor on Construction Directs |
| Trigger | No project-specific indirects breakdown or schedule |
| Evidence | Fallback Typical Model (AGENT_ESTIMATING.md line 667): "Construction indirects (CI) = 0.18 × Construction Directs (CD)" |
| Impacted WBS/CBS | PKG-21 / CI |
| Estimate Impact | LOW-MEDIUM — CI calculated as $62,000 |
| Override Path | Provide detailed indirects estimate or duration-based calculation |

---

### D-010: Currency Selection

| Field | Value |
|-------|-------|
| Decision | Used CAD (Canadian dollars) per _CONFIG.md |
| Trigger | Config file specifies currency |
| Evidence | _CONFIG.md line 9: "currency: CAD" |
| Impacted WBS/CBS | All |
| Estimate Impact | N/A — Currency is correct for project location |
| Override Path | N/A |

---

### D-011: Contingency Method

| Field | Value |
|-------|-------|
| Decision | Applied PCT_BY_BUCKET contingency method with allowance adjustment |
| Trigger | Config specifies PCT_BY_BUCKET; all items are allowance/parametric |
| Evidence | _CONFIG.md line 35: "contingency_method: PCT_BY_BUCKET"; 100% allowance share triggers +10% uplift |
| Impacted WBS/CBS | All CBS buckets (CONT) |
| Estimate Impact | Contingency = $410,000 (25.7% of base) |
| Override Path | Provide more detailed pricing to reduce allowance share and contingency |

---

### D-012: Operator Shelter Size

| Field | Value |
|-------|-------|
| Decision | Assumed 15 m² (160 ft²) per shelter |
| Trigger | Shelter size not defined |
| Evidence | DEL-21.01 Datasheet lines 85-88: shelter function and size marked TBD |
| Impacted WBS/CBS | PKG-21 / MAT, CD |
| Estimate Impact | LOW-MEDIUM — Size affects unit cost |
| Override Path | Define shelter size requirements per operator comfort and equipment needs |

---

**Total Decisions:** 12

**Prepared by:** ESTIMATING Agent
**Date:** 2026-01-28
