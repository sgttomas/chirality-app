# Source Index

## PKG-13 Storage Tanks Estimate

### Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG13_DRAFT_2026-01-28_2400 |
| Estimate Label | PKG13_DRAFT |
| Date | 2026-01-28 |

---

## Source Discovery Summary

| Category | Sources Found | Priority |
|----------|---------------|----------|
| Vendor Quotes | 0 | Highest |
| Rate Tables | 0 | High |
| Deliverable Documents | 24 | Medium |
| Decomposition | 1 | Medium |
| Fallback Model | 1 (embedded) | Lowest |

---

## Explicit Pricing Sources

### Vendor Quotes / Budgetary Quotes

**None found.**

Recommended sources to obtain:
- API 650 tank fabricator quotes (Matrix Service, CB&I, Tarsco, CST Industries)
- Agitator OEM quotes (SPX Flow, Chemineer, Philadelphia Mixing, Lightnin)
- Coating system quotes (food-grade epoxy suppliers)
- NDE contractor quotes (Level III NDE services)

### Rate Tables / Cost Libraries

**None found** in `execution/_Estimates/_RateTables/`.

Recommended rate tables to develop:
- Tank steel fabrication rates ($/tonne)
- Tank erection rates ($/tonne installed)
- Coating application rates ($/m²)
- Welding and NDE rates ($/weld, $/joint)

---

## Quantity Sources

### Decomposition Document

| Source | Location | Data Extracted |
|--------|----------|----------------|
| Project Decomposition | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-13 scope, 3 × 15,000 MT tanks, API 650, agitators, overflow protection, water draw-off, Phase 2 connections, 6 deliverables |

### Deliverable Documents

| Deliverable | Document | Data Extracted |
|-------------|----------|----------------|
| DEL-13.01 | Datasheet.md | Tank configuration (3 tanks, 15,000 MT each), geometry TBD, nozzle schedule TBD |
| DEL-13.01 | Specification.md | API 650 standard, seismic requirements, drawing set scope |
| DEL-13.02 | Datasheet.md | Specification scope (3 documents: tank, agitator, appurtenance) |
| DEL-13.02 | Specification.md | Standards (API 650, CSA W59, CSA W47.1), material categories |
| DEL-13.03 | Datasheet.md | Calculation package scope |
| DEL-13.04 | Datasheet.md | Data sheet package (3 tank, 3 agitator, overflow protection) |
| DEL-13.05 | Datasheet.md | Test record scope |
| DEL-13.06 | Datasheet.md | Fabrication QA package scope |

### Key Parameters Extracted

| Parameter | Value | Source |
|-----------|-------|--------|
| Number of tanks | 3 | Decomposition Section 1.1 |
| Capacity per tank | 15,000 MT | Decomposition Section 1.1 |
| Total storage | 45,000 MT | Decomposition Section 1.1 |
| Product | CSD canola oil | Decomposition Section 1.1 |
| Design standard | API 650 | Decomposition PKG-13 Scope |
| Agitators | 3 units | Decomposition PKG-13 Scope |
| Overflow protection | Required | Decomposition PKG-13 Scope |
| Water draw-off | Required | Decomposition PKG-13 Scope |
| Phase 2 connections | Required | Decomposition PKG-13 Scope |
| Deliverables | 6 | Decomposition PKG-13 |

---

## Fallback Typical Model

Since no vendor quotes or rate tables were found, all pricing relies on the **embedded fallback typical model**.

### Model Parameters Used

| Parameter | Value | Source |
|-----------|-------|--------|
| Tank steel (fabricated) | $7,600/tonne | Typical API 650 mid-range |
| Tank erection | $2,000/tonne | Field erection labor + equipment |
| Internal coating | $50/m² | Food-grade epoxy system |
| External coating | $20/m² | Environmental coating |
| Side-entry agitator | $125,000/unit | 75 HP with VFD |
| Engineering rate | $200-250/hr | Discipline engineer |
| CI factor | 18% of CD | Fallback typical |
| PM factor | 6% of base | Fallback typical |
| P factor | 2% of MAT | Fallback typical |
| COM factor | 3% of base | Fallback typical |

### Confidence Impact

All line items priced via fallback model are marked:
- `Method = ALLOWANCE` or `PARAMETRIC`
- `Confidence = LOW`
- `SourceRef = A-xxx` (assumption ID)

---

## Reference Documents (Not Yet Available)

The following reference documents are expected but not yet provided:

| Document | Expected Content | Impact |
|----------|------------------|--------|
| Volume 2 Part 1: ER General | Project requirements, quality standards | Specification basis |
| Volume 2 Part 2: ER Civil & Mechanical | Tank requirements, materials, testing | Design basis |
| API 650 | Tank design standard | Design requirements |
| API 650 Appendix E | Seismic design | Anchorage requirements |
| NBC 2020 | Environmental loads for BC | Wind, snow, seismic parameters |
| Geotechnical report (DEL-02.04) | Bearing capacity, settlement | Foundation design |

---

## Source Priority Hierarchy

For next estimate iteration, sources should be applied in this order:

1. **Vendor quotes** (firm or budgetary) — highest confidence
2. **Project rate tables** — if developed from similar projects
3. **Deliverable documents** — for quantities and scope
4. **Decomposition** — for scope definition
5. **Fallback model** — last resort, lowest confidence

---

## Recommendations for Source Improvement

| Priority | Action | Expected Impact |
|----------|--------|-----------------|
| HIGH | Obtain tank fabricator quotes | Replace $9.6M tank supply allowance |
| HIGH | Complete DEL-13.03 calculations | Confirm tank geometry and steel weight |
| MEDIUM | Obtain agitator OEM quotes | Replace $375k agitator allowance |
| MEDIUM | Develop project rate tables | Improve erection and installation pricing |
| MEDIUM | Obtain coating quotes | Replace $730k coating allowances |
| LOW | Obtain NDE quotes | Replace $280k NDE allowance |
