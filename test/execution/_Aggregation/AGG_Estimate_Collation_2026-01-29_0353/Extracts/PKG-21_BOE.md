# Basis of Estimate (BOE)

## Estimate Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG21_DRAFT_2026-01-28_0030 |
| Estimate Label | PKG21_DRAFT |
| Package | PKG-21 Building Structures & Envelope |
| Pricing Date | 2026-01 (January 2026) |
| Currency | CAD |
| Estimate Class | Class 5 (Order of Magnitude) |
| RUN_STATUS | WARNINGS |

---

## Scope Definition

### Inclusions

**Package Scope (per Decomposition line 507):**
- MCC building structure
- Building cladding
- Roofing systems
- Doors and windows
- Operator shelters

**CBS Coverage:**
- Engineering & Design (E)
- Project Management (PM)
- Procurement (P)
- Equipment & Materials (MAT)
- Construction Directs (CD)
- Construction Indirects (CI)
- Commissioning (COM)

### Exclusions

- Building MEP systems (HVAC, plumbing, fire suppression) — covered under PKG-22
- Interior finishes beyond basic industrial finishes — covered under PKG-22
- Electrical equipment within MCC building — covered under PKG-17
- Owner's costs, land, financing
- Permits obtained by Employer
- Furniture, fixtures, and equipment (FF&E)
- Site civil work (grading, drainage) — covered under PKG-02, PKG-03, PKG-04

---

## Estimate Basis

### Building Scope Assumptions

**MCC Building:**
- **Assumed Footprint:** 600 m² (approx. 6,500 ft²) — D-001
- **Construction Type:** Pre-engineered metal building (PEMB) with insulated metal panel cladding — D-002
- **Stories:** Single story with high bay for electrical equipment
- **Foundation:** Slab-on-grade with thickened edges; piles assumed per geotechnical conditions — D-003
- **Roofing:** Standing seam metal roof with R-30 insulation
- **Doors:** Personnel doors (6), overhead roll-up door (1)
- **Windows:** Limited glazing (industrial building)
- **Design Life:** 25-50 years (ASSUMPTION per datasheets)

**Operator Shelters:**
- **Quantity:** 4 shelters to serve 32 railcar unloading stations — D-004
- **Size:** 15 m² each (approx. 160 ft² per shelter)
- **Construction Type:** Prefabricated insulated enclosures with heating
- **Features:** Weather protection, visibility windows, heating, electrical

**Source:** Decomposition PKG-21 scope (line 507); DEL-21.01 Datasheet (lines 80-88)

### Location Factors

| Factor | Value | Notes |
|--------|-------|-------|
| Location | Fraser Surrey Terminal, Surrey, BC | Coastal environment |
| Climate Zone | Coastal BC (marine climate) | Wet winters, freeze-thaw |
| Seismic Design | NBC 2020 Western Canada provisions | Higher seismic loads |
| Corrosion Environment | Marine/industrial | Requires enhanced protection |
| Labor Market | Greater Vancouver | Union rates assumed |
| Productivity Factor | 1.0 | Standard productivity assumed |

---

## Pricing Sources

### Priority Order

1. **Vendor Quotes:** None available — D-005
2. **Rate Tables:** None available in `_RateTables/` — D-006
3. **Parametric/Allowances:** Used for all line items

### Pricing Basis

All pricing is based on **parametric estimating** using industry benchmarks for industrial building construction in British Columbia, January 2026 pricing.

**Key Benchmarks (ASSUMPTION):**
- Pre-engineered metal building (complete): $800-$1,200/m² — A-001
- Prefabricated operator shelter (heated): $45,000-$65,000 each — A-002
- Building engineering/design: 10-12% of construction value — A-003

**Source:** Industry parametric data; no project-specific quotes available

---

## Contracting Assumptions

| Assumption | Value |
|------------|-------|
| Contracting Model | Design-Build (per contract type) |
| Building Supply | Subcontract to PEMB supplier/erector |
| Shelter Supply | Prefabricated enclosure supplier |
| Labor | Union rates (Greater Vancouver) |
| Procurement | Contractor-managed |

---

## Indirects Model

**Method:** Factor-based (no schedule data available)

| Category | Factor | Basis |
|----------|--------|-------|
| Construction Indirects (CI) | 18% | × Construction Directs (CD) |
| Procurement Services (P) | 2% | × Materials (MAT) |
| Commissioning (COM) | 3% | × (CD + CI + MAT) |
| Project Management (PM) | 6% | × (CD + CI + MAT) |

**Source:** Fallback Typical Model (AGENT_ESTIMATING.md)

---

## Contingency

### Method

`PCT_BY_BUCKET` (default per _CONFIG.md)

### Contingency Rates

| CBS Bucket | Base Rate | Allowance Adjustment | Applied Rate |
|------------|-----------|---------------------|--------------|
| E (Engineering) | 10% | +10% (100% allowance) | 20% |
| PM | 10% | +10% (100% allowance) | 20% |
| P (Procurement) | 10% | +10% (100% allowance) | 20% |
| MAT (Materials) | 15% | +10% (100% allowance) | 25% |
| CD (Construction Directs) | 20% | +10% (100% allowance) | 30% |
| CI (Construction Indirects) | 20% | +10% (100% allowance) | 30% |
| COM (Commissioning) | 25% | +10% (100% allowance) | 35% |

**Adjustment Rationale:** All line items priced by ALLOWANCE/PARAMETRIC method, triggering +10% contingency uplift per Fallback Typical Model.

---

## Escalation

**Mode:** NONE (per _CONFIG.md)

Pricing is in January 2026 dollars. No escalation applied.

---

## Rounding Policy

- Line items: Rounded to nearest $1,000
- Subtotals: Rounded to nearest $1,000
- Final total: Rounded to nearest $1,000

---

## Completeness Metrics

| Metric | Value |
|--------|-------|
| % Priced by QUOTE | 0% |
| % Priced by RATE_TABLE | 0% |
| % Priced by ALLOWANCE/PARAMETRIC | 100% |
| Deliverables with explicit quantities | 0/6 (0%) |
| Deliverables with cost coverage | 6/6 (100%) |

---

## Known Gaps

| Gap ID | Description | Impact | Resolution Path |
|--------|-------------|--------|-----------------|
| G-001 | MCC building size not defined | HIGH — Size drives material and labor costs | Obtain electrical equipment layout and space requirements |
| G-002 | Operator shelter quantity not confirmed | MEDIUM — Affects shelter scope | Confirm with PKG-10 railcar unloading layout |
| G-003 | No vendor quotes | HIGH — All pricing is parametric | Obtain budget quotes from PEMB suppliers |
| G-004 | Foundation type not defined | MEDIUM — Piles vs spread footings affects cost | Obtain geotechnical recommendations |
| G-005 | Hazardous area classification not confirmed | LOW-MEDIUM — May affect building features | Confirm facility classification per HAZOP |

---

## References

### Decision Log
See `Decision_Log.md` (D-001 through D-012)

### Assumptions Log
See `Assumptions_Log.md` (A-001 through A-015)

### Source Documents
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 503-519)
- DEL-21.01 Datasheet: Building Design Drawing Set
- DEL-21.02 Datasheet: Building Technical Specification
- DEL-21.03 Datasheet: Building Design Calculations
- DEL-21.04 Datasheet: Building Data Sheet Package
- DEL-21.05 Datasheet: Building Installation & Test Records
- DEL-21.06 Datasheet: Building Shop Design Drawing Set

---

**Prepared by:** ESTIMATING Agent
**Date:** 2026-01-28
**Snapshot:** EST_PKG21_DRAFT_2026-01-28_0030
