# Source Index — PKG-18 Lighting Estimate

**Snapshot ID:** EST_PKG18_DRAFT_2026-01-28_2400
**Date:** 2026-01-28

---

## Purpose

This index documents all pricing and quantity sources discovered and used during the estimating process, listed in priority order per the pricing hierarchy (Quote → Rate Table → Historical → Allowance/Parametric).

---

## Source Discovery Summary

| Source Type | Discovered | Used | Percentage of Base Estimate |
|-------------|------------|------|----------------------------|
| Vendor Quotes / Budgetary Quotes | 0 | 0 | 0% |
| Project Rate Tables | 0 | 0 | 0% |
| Historical Pricing Data | 0 | 0 | 0% |
| Allowance / Parametric (Fallback Model) | Yes | 25 line items | 100% |

**Conclusion:** No project-specific pricing sources were available. All pricing is allowance-based using the Fallback Typical Model per Decision D-1803.

---

## Section 1: Vendor Quotes and Budgetary Quotes

**Search Performed:**
- Reviewed all 5 deliverable `_REFERENCES.md` files in PKG-18 Lighting
- Searched for vendor quotes, budgetary quotes, proposals, or pricing letters
- Searched project workspace for files matching: `quote`, `proposal`, `budget`, `pricing`

**Results:** None found

**Recommendation:** Obtain budgetary quotes from lighting vendors for:
- LED lighting fixtures (exterior and interior, various types)
- Lighting poles (steel or aluminum, marine-grade, 30-40 ft)
- Lighting controls (sensors, switches, panels, integration)
- Emergency lighting equipment (battery-backed fixtures, exit signs)

**Potential Vendors (typical for Canadian market):**
- Philips Lighting / Signify
- GE Current (a Daintree company)
- Eaton Lighting
- Hubbell Lighting
- Lithonia Lighting (Acuity Brands)
- Cooper Lighting Solutions
- Lumenpulse (Canadian LED manufacturer)

---

## Section 2: Project Rate Tables

**Search Performed:**
- Checked `execution/_Estimates/_RateTables/` directory
- Searched deliverable documents for embedded rate tables or unit pricing
- Searched project workspace for files matching: `rate`, `unit cost`, `cost`, `pricing`

**Results:** No rate tables found for:
- LED lighting fixtures (by type and wattage)
- Lighting poles (by height and material)
- Lighting controls equipment
- Electrical installation labor (per fixture or per hour)
- Testing and commissioning labor

**Recommendation:** Create rate tables in `execution/_Estimates/_RateTables/` with columns:
- `Item` (description)
- `Unit` (EA, LF, HR, LS)
- `UnitRate` (CAD)
- `Currency` (CAD)
- `Date` (pricing date)
- `Source` (vendor, historical project, cost index)

**Suggested Rate Table Files:**
- `Lighting_Fixtures_CAD_2026-01.csv` — LED fixtures by type
- `Lighting_Poles_CAD_2026-01.csv` — Poles by height and material
- `Electrical_Labor_CAD_2026-01.csv` — Installation labor rates
- `Controls_Equipment_CAD_2026-01.csv` — Control devices and systems

---

## Section 3: Historical Pricing Data

**Search Performed:**
- Searched deliverable documents for references to historical projects or precedent pricing
- Searched for "historical", "precedent", "benchmark", "comparable" in workspace

**Results:** None found

**Recommendation:** If available, reference historical lighting projects with:
- Similar scope (industrial facility lighting, marine environment)
- Similar technology (LED fixtures, lighting controls)
- Recent pricing (within 12-24 months)
- Documented actual costs and lessons learned

---

## Section 4: Deliverable Document Content (Quantities and Scope)

**Quantity Sources Status:**

| Deliverable | Status | Quantity Data Available | Notes |
|-------------|--------|------------------------|-------|
| DEL-18.01 Lighting Design Drawing Set | INITIALIZED | No | Fixture schedules, pole layouts TBD |
| DEL-18.02 Lighting Technical Specification | INITIALIZED | No | Fixture types and quantities TBD |
| DEL-18.03 Lighting Design Calculations | INITIALIZED | No | Fixture selections and counts TBD |
| DEL-18.04 Lighting Data Sheet Package | INITIALIZED | No | Equipment data sheets TBD |
| DEL-18.05 Lighting Installation & Test Records | INITIALIZED | No | Testing scope defined but quantities TBD |

**Conclusion:** All deliverables at INITIALIZED state with TBD placeholders. No explicit quantities available for:
- Fixture counts by type
- Pole quantities and locations
- Wiring and conduit lengths
- Control device quantities

**Cost Drivers Identified (qualitative scope):**

From Datasheet and Specification documents:
- **Exterior lighting:** Process areas, roadways, parking, perimeter security (Guidance DEL-18.01 E-3.1)
- **Interior lighting:** Warehouse/process high-bay, office/control rooms, utility areas (Guidance DEL-18.01 E-3.2)
- **Emergency lighting:** Egress paths, exit doors, stairwells per NFPA 101 (Guidance DEL-18.01 E-3.3)
- **Controls:** Occupancy sensing, daylight harvesting, time scheduling, integration with PKG-19 (Datasheet DEL-18.01)
- **Testing:** Illumination field testing (exterior and interior), emergency duration testing, control functional testing (Datasheet DEL-18.05)

**Engineering Deliverables:**
- 5 deliverables: 1 Drawing Set, 1 Specification, 1 Calculation, 1 Data Sheet Package, 1 Test Records
- Engineering effort estimated per deliverable type and complexity (see Assumptions A-1801 through A-1831)

---

## Section 5: Fallback Typical Model Application

**Usage:** 100% of estimate pricing (all 25 line items)

**Model Basis:**
- Industry-typical unit pricing for LED commercial/industrial lighting fixtures and equipment
- Typical electrical installation labor rates for BC industrial projects
- Parametric factors for indirects, management, procurement, commissioning per AGENT_ESTIMATING.md STRUCTURE Fallback Model

**Model Transparency:**
- All fallback model usage documented with `Method=ALLOWANCE` or `Method=PARAMETRIC` in Detail.csv
- All fallback-based line items marked `Confidence=LOW` or `Confidence=MED` (for parametric factors)
- All fallback decisions referenced in `SourceRef` column (D-1803, D-1806, D-1807)

**Model Limitations:**
- Not project-specific; does not reflect actual vendor pricing or contractor rates
- Does not account for project-specific requirements from ER
- Fixture counts estimated without illumination calculations or lighting layouts
- Hazardous area fixture requirements estimated without classification drawings

---

## Source Priority for Next Estimate Iteration

**Priority 1 — Vendor Quotes (target 50%+ of MAT base):**
- LED fixtures (exterior, interior, emergency) — budgetary quotes
- Lighting poles (steel or aluminum, marine-grade) — budgetary quotes
- Lighting controls (sensors, panels, integration) — budgetary quotes

**Priority 2 — Rate Tables (target 30%+ of CD base):**
- Electrical installation labor rates (per fixture, per hour)
- Testing and commissioning labor rates
- Engineering manhour rates (for E bucket)

**Priority 3 — Design Quantities (from deliverable development):**
- Lighting design drawings (DEL-18.01) with fixture schedules
- Illumination calculations (DEL-18.03) with fixture selections and quantities
- Control system design with device counts and integration scope

---

## References

**Deliverable Folders Reviewed:**
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-18_Lighting/1_Working/DEL-18.01_Lighting_Design_Drawing_Set/`
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-18_Lighting/1_Working/DEL-18.02_Lighting_Technical_Specification/`
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-18_Lighting/1_Working/DEL-18.03_Lighting_Design_Calculations/`
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-18_Lighting/1_Working/DEL-18.04_Lighting_Data_Sheet_Package/`
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-18_Lighting/1_Working/DEL-18.05_Lighting_Installation_and_Test_Records/`

**Files Read per Deliverable:**
- `_CONTEXT.md`, `_REFERENCES.md`, `_STATUS.md`
- `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`

---

**END OF SOURCE INDEX**
