# Source Index — PKG-22 Building Interior & MEP

**Snapshot ID:** EST_PKG22_DRAFT_2026-01-28_2358
**Package:** PKG-22 Building Interior & MEP
**Date:** 2026-01-28

---

## Purpose

This document lists discovered pricing and quantity sources in priority order per the estimating pipeline.

---

## Source Discovery Results

### Phase 1: Explicit Pricing Sources (Vendor Quotes, Budgets)

**Search scope:**
- Package folder: `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-22_Building_Interior_and_MEP/`
- All deliverable folders: DEL-22.01 through DEL-22.06
- Reference folders: `0_References/` (if present)

**Result:** No vendor quotes, budgetary quotes, or proposals found

**Decision:** D-008 (proceed without quotes; use allowances)

---

### Phase 2: Rate Tables / Cost Libraries

**Search scope:**
- `execution/_Estimates/_RateTables/`
- Workspace files matching: `rate`, `cost`, `unit cost`, `estimate`, `pricing`

**Result:** No rate tables found

**Decision:** D-008 (proceed without rate tables; use allowances)

---

### Phase 3: Quantity Sources (Design Documents)

**Search results:**

| Deliverable | Status | Quantities Extracted |
|-------------|--------|---------------------|
| DEL-22.01 | INITIALIZED | Artifact counts only; physical quantities TBD (HVAC equipment counts, duct lengths, plumbing fixture counts, piping runs, fire sprinkler head counts) |
| DEL-22.02 | INITIALIZED | Specification scope descriptions; no quantified requirements |
| DEL-22.03 | INITIALIZED | Calculation placeholder; load values and equipment sizes TBD |
| DEL-22.04 | INITIALIZED | Equipment data sheet placeholders; equipment counts TBD (HVAC units, water heaters, pumps, fixtures, sprinkler system components) |
| DEL-22.05 | INITIALIZED | Test record placeholders; testing scope TBD |
| DEL-22.06 | INITIALIZED | Shop drawing placeholders; fabrication scope TBD |

**Explicit quantities discovered:** 0 (all deliverables in INITIALIZED state with TBD values)

**Qualitative scope signals extracted:**
- HVAC: Heating, ventilation, and air conditioning for MCC building
- Plumbing: Domestic water, sanitary drainage, hot water system (if required)
- Fire Suppression: Automatic sprinkler system per NFPA 13
- Interior Electrical: Lighting, receptacles, small power distribution
- Interior Finishes: Flooring, wall finishes, ceilings (inferred from package scope)

**Decision:** D-011 (use allowances scaled to building size/complexity)

---

### Phase 4: Embedded Fallback Model (Used)

**Result:** Fallback typical model used for all pricing (100% allowance/parametric)

**Components applied:**
- Allowance placeholders for materials and construction (A-001 through A-022)
- Indirects factors: CI=18%, P=2%, PM=6%, COM=3% (D-009)
- Contingency baseline by bucket with allowance-heavy adjustment (D-010)

**Transparency:** All uses labeled ALLOWANCE or PARAMETRIC with LOW/MED confidence and traced to assumptions/decisions

**Source:** AGENT_ESTIMATING fallback model (lines 643-691)

---

## Source Priority Hierarchy Applied

| Priority | Source Type | Coverage | Result |
|----------|-------------|----------|--------|
| 1 | Vendor quotes | 0% | None available |
| 2 | Rate tables | 0% | None available |
| 3 | Design quantities | 0% | All deliverables INITIALIZED; quantities TBD |
| 4 | Fallback model | 100% | Used for all pricing |

---

## Building Size Estimation (for Allowance Scaling)

**MCC Building Size Estimate:**

Based on project context and typical industrial MCC building practice:
- **Floor area:** 200-400 m² (2,150-4,300 SF) estimated for MCC, operator spaces, support facilities
- **Basis:** Typical MCC building for 1,000,000 MT/a facility; 32 unloading stations; marine loading controls
- **Occupancy:** Low occupancy (5-10 operators/staff typical per shift)

**Sources consulted:**
- DEL-22.01 Datasheet.md (building type: MCC building)
- DEL-22.04 Datasheet.md (equipment types: HVAC, plumbing, fire suppression)
- Decomposition project parameters (throughput, storage, railcar/marine operations)

**Decision:** D-012 (assume 300 m² MCC building as baseline for MEP sizing)

**Assumption:** A-022 (building size used for allowance scaling)

---

## Recommended Sources for Next Iteration

**To improve estimate accuracy:**

1. **Building design documents from PKG-21:**
   - DEL-21.01 Building Design Drawing Set (floor plans, elevations, building size, room layouts)
   - DEL-21.04 Building Data Sheet Package (building area, occupancy, envelope specifications)

2. **Vendor budgetary quotes:**
   - HVAC packaged rooftop units or split systems (budgetary quotes for equipment and installation)
   - Plumbing fixtures and equipment (water heaters, pumps, fixtures)
   - Fire suppression system (sprinkler system design-build quote or equipment quote)
   - Interior finishes (flooring, wall panels, ceiling systems)

3. **Project rate tables:**
   - Engineering labor rates by discipline
   - Construction labor rates (plumber, HVAC technician, electrician, sprinkler fitter)
   - Equipment rental rates
   - Material unit costs (duct, pipe, sprinkler fittings, lighting fixtures, wiring)

4. **Employer's Requirements Volume 2 Part 3:**
   - Building Works requirements (expected at `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_3_Employers_Requirements.pdf`)
   - MEP system requirements, performance criteria, occupancy data

---

## Source Index Prepared By

**Agent:** Estimating Agent
**Date:** 2026-01-28
**Snapshot:** EST_PKG22_DRAFT_2026-01-28_2358
**Status:** Complete (no pricing sources found; fallback model used 100%)
