# Estimate Summary

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG22_DRAFT_2026-01-28_2358 |
| Estimate Label | PKG22_DRAFT |
| Package | PKG-22 Building Interior & MEP |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Date | 2026-01-28 |
| Run Status | WARNINGS |

## Cost Breakdown Structure (CBS) Summary

| CBS | Description | Base Cost | Contingency % | Contingency | Total Cost |
|-----|-------------|-----------|---------------|-------------|------------|
| E | Engineering & Design | $124,000 | 20% | $25,000 | $149,000 |
| MAT | Equipment & Materials | $675,000 | 25% | $169,000 | $844,000 |
| CD | Construction Directs | $632,000 | 30% | $190,000 | $822,000 |
| CI | Construction Indirects | $114,000 | 30% | $34,000 | $148,000 |
| P | Procurement Services | $14,000 | 15% | $2,000 | $16,000 |
| PM | EPCM / Project Management | $85,000 | 15% | $13,000 | $98,000 |
| COM | Commissioning | $43,000 | 30% | $13,000 | $56,000 |
| **SUBTOTAL** | | **$1,687,000** | | **$446,000** | **$2,133,000** |

**Rounded Estimate Total:** **$2,133,000 CAD** (rounded to nearest $1,000 per rounding policy)

---

## Work Breakdown Structure (WBS) Summary

| Deliverable ID | Name | CBS Buckets | Base Cost | Notes |
|----------------|------|-------------|-----------|-------|
| DEL-22.01 | Building MEP Design Drawing Set | E, MAT, CD | $586,000 | HVAC layout; plumbing layout; electrical layout; fire suppression layout; finishes |
| DEL-22.02 | Building MEP Technical Specification | E | $28,000 | HVAC spec; plumbing spec; fire suppression spec |
| DEL-22.03 | Building MEP Design Calculations | E | $22,000 | HVAC loads; plumbing sizing; fire sprinkler hydraulics |
| DEL-22.04 | Building MEP Data Sheet Package | E | $10,000 | HVAC data sheet; fire suppression data sheet |
| DEL-22.05 | Building MEP Installation & Test Records | CI, COM | Included in factors | QA/QC records; testing records (captured in CI and COM buckets) |
| DEL-22.06 | Building MEP Shop Design Drawing Set review | E | $16,000 | Shop drawing review for HVAC; sprinkler; plumbing equipment |
| **Directs/Indirects/Services** | Construction Indirects, Procurement, PM | CI, P, PM | $213,000 | Factor-based services supporting all deliverables |

---

## Key Cost Drivers

| Driver | Base Cost | % of Base | Notes |
|--------|-----------|-----------|-------|
| Equipment & Materials (MAT) | $675,000 | 40% | Largest cost driver; includes HVAC equipment ($295k), fire suppression ($110k), plumbing ($90k), electrical ($95k), finishes ($85k) |
| Construction Directs (CD) | $632,000 | 37% | Second largest driver; includes HVAC installation ($195k), plumbing ($125k), fire suppression ($115k), electrical ($105k), finishes ($92k) |
| Engineering & Design (E) | $124,000 | 7% | Design deliverables (6 total); drawings, specs, calculations, data sheets, shop review |
| Construction Indirects (CI) | $114,000 | 7% | Factor-based at 18% of CD |
| EPCM / PM | $85,000 | 5% | Factor-based at 6% of (CD+CI+MAT) |
| Commissioning (COM) | $43,000 | 3% | Factor-based at 3% of (CD+CI+MAT); includes HVAC TAB, plumbing/fire testing, functional performance testing |
| Procurement Services (P) | $14,000 | 1% | Factor-based at 2% of MAT |

---

## Cost by MEP System

| System | Materials (MAT) | Construction (CD) | Subtotal | % of MAT+CD |
|--------|-----------------|-------------------|----------|-------------|
| HVAC | $295,000 | $195,000 | $490,000 | 37% |
| Fire Suppression | $110,000 | $115,000 | $225,000 | 17% |
| Plumbing | $90,000 | $125,000 | $215,000 | 16% |
| Interior Electrical | $95,000 | $105,000 | $200,000 | 15% |
| Interior Finishes | $85,000 | $92,000 | $177,000 | 14% |
| **Total MAT + CD** | **$675,000** | **$632,000** | **$1,307,000** | **100%** |

---

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Total line items | 19 |
| Lines priced by QUOTE | 0% (0 lines) |
| Lines priced by RATE_TABLE | 0% (0 lines) |
| Lines priced by ALLOWANCE | 79% (15 lines) |
| Lines priced by PARAMETRIC (factors) | 21% (4 lines) |
| Deliverables with explicit quantities | 0% (0 of 6) |
| Overall confidence | LOW |

---

## Estimate Basis Summary

| Parameter | Value |
|-----------|-------|
| Estimate type | Order-of-magnitude allowance-based estimate |
| Pricing method | 100% allowances for directs/materials; factor-based for indirects/services |
| Quantity basis | Engineering judgment; building size assumption (300 m²); no design quantities available (all deliverables INITIALIZED status) |
| Pricing basis | Typical market rates for BC Lower Mainland; no vendor quotes |
| Indirects model | Factor-based per fallback typical model (CI=18%, P=2%, PM=6%, COM=3%) |
| Contingency method | PCT_BY_BUCKET with allowance-heavy adjustments (20-30% by bucket) |
| Escalation | None (current January 2026 dollars) |
| Accuracy class | Class 5 / Order of Magnitude (-30% to +50% typical range) |

---

## Next Estimate Iteration Requirements

To improve estimate accuracy for PKG-22:

1. **Complete design quantities:**
   - PKG-21 DEL-21.01 building design drawings to determine actual building floor area and room layouts
   - DEL-22.01 MEP design drawings with equipment schedules, piping/ductwork routing, fixture layouts, sprinkler head layout
   - DEL-22.03 calculations with HVAC loads, plumbing fixture counts, fire sprinkler hydraulics, electrical loads

2. **Obtain vendor pricing:**
   - HVAC equipment budgetary quotes (packaged rooftop units or split systems)
   - Fire suppression system budgetary quotes (sprinkler system design-build or equipment quote)
   - Plumbing equipment budgetary quotes (fixtures, water heater, pumps)
   - Interior finishes pricing (flooring, wall panels, ceiling systems)

3. **Provide project data:**
   - Engineering labor hours by discipline and deliverable
   - Construction labor and equipment rate tables
   - Building occupancy data (occupant count, occupancy classification per NBC 2020)
   - Control system interface requirements (PKG-19 coordination)
   - Electrical power interface requirements (PKG-17 coordination)
   - Fire water supply data (PKG-23 coordination)

4. **Expected accuracy improvement:** Class 4 (-20% to +30%) with design quantities and vendor quotes; Class 3 (-15% to +20%) with final design and firm quotes

---

## Reconciliation with Previous Packages

| Package | Deliverables | Base Total | Contingency | Estimate Total | Cost/Deliverable |
|---------|--------------|------------|-------------|----------------|------------------|
| PKG-19 Control Systems | 5 | $1,801,000 | $450,000 (25%) | $2,251,000 | $450k/deliverable |
| PKG-20 Field Instrumentation | 5 | $1,535,000 | $408,000 (27%) | $1,943,000 | $389k/deliverable |
| **PKG-22 Building Interior & MEP** | **6** | **$1,687,000** | **$446,000 (26%)** | **$2,133,000** | **$356k/deliverable** |

**Notes:**
- PKG-22 cost per deliverable ($356k) is lower than PKG-19 ($450k) and PKG-20 ($389k), consistent with smaller scope (building MEP for single MCC building vs. facility-wide systems)
- PKG-22 contingency rate (26%) is consistent with PKG-19/PKG-20 (25-27%) due to 100% allowance-based pricing
- PKG-22 includes significant equipment costs (HVAC, fire suppression) but smaller scope than facility-wide packages
- All three packages show elevated contingency rates due to lack of vendor quotes and design quantities

---

## Budget Comparison (If Applicable)

**No prior PKG-22 estimate available for comparison**

**Note:** This is the first estimate for PKG-22 Building Interior & MEP.

---

## Special Considerations for PKG-22

### Building Size Dependency

PKG-22 estimate is highly dependent on building size assumption (300 m²). Building size variation directly affects:
- HVAC equipment capacity and cost (±33% building size → ±25-35% HVAC cost)
- Plumbing fixture count and piping quantities
- Fire sprinkler head count and piping quantities
- Electrical lighting/receptacle counts
- Interior finishes quantities

**Recommendation:** Complete PKG-21 building design to determine actual floor area before proceeding with MEP design.

### Interface Coordination Critical

PKG-22 has critical interfaces with:
- **PKG-21 (Building Structure):** Building size, equipment supports, penetrations, clearances
- **PKG-19 (Control Systems):** HVAC equipment control interfaces, BAS integration
- **PKG-17 (Electrical Power):** Electrical load coordination, power distribution to building panels
- **PKG-23 (Fire Protection):** Fire water supply adequacy for building sprinkler system

**Recommendation:** Establish interdisciplinary coordination process early; hold coordination workshops before finalizing designs.

### Fire Suppression System Risk

Fire water supply adequacy not verified (PKG-23 coordination pending). If site fire water supply is insufficient for building sprinkler hydraulic demand, fire pump addition may be required (+$80k-$150k not included in base estimate).

**Recommendation:** Coordinate with PKG-23 early to verify fire water supply; complete DEL-22.03 hydraulic calculations to determine sprinkler demand.

---
