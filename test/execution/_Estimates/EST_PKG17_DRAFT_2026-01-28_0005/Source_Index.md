# Source Index — PKG-17 Electrical Power Distribution

**Snapshot ID:** EST_PKG17_DRAFT_2026-01-28_0005
**Date:** 2026-01-28

---

This index lists all sources used for pricing and quantities in the estimate, organized by priority and type.

---

## 1. Explicit Pricing Sources (Highest Priority)

### Vendor Quotes

**Status:** None found

**Search Locations:**
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/` (no electrical quotes found)
- Deliverable `_REFERENCES.md` files (no PKG-17 deliverable folders exist)

**Recommendation:** Issue RFQs for:
- Transformers (2 units, 1000-1500 kVA, pad-mounted, oil-filled)
- MV Switchgear (5-bay metal-clad lineup, 5kV or 15kV class)
- LV Switchgear (main-tie-main configuration, 600V)
- Motor Control Centers (3 units, sizes TBD pending load calculations)

### Budgetary Quotes

**Status:** None found

**Recommendation:** Request budgetary quotes from electrical equipment manufacturers (ABB, Schneider Electric, Eaton, GE) for transformers, switchgear, MCCs

---

## 2. Rate Tables / Cost Libraries

### Project-Specific Rate Tables

**Status:** None found

**Search Locations:**
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/` (directory exists but no electrical rate tables)

**Recommendation:** Create electrical equipment rate table (`_RateTables/electrical_equipment_rates.csv`) with typical unit costs for:
- Transformers ($/kVA)
- Switchgear ($/bay or $/ampere)
- MCCs ($/starter or $/HP controlled)
- Cables ($/m by voltage and size)
- Cable tray ($/m by width)
- Conduit ($/m by size and type)

### External Cost Libraries

**Status:** Not used

**Note:** External cost databases (RSMeans, Richardson, etc.) were not referenced; all pricing is based on fallback typical model

---

## 3. Quantity Sources

### Deliverable Documents

**Status:** Not available (no deliverable folders exist)

**Expected Quantity Sources (future):**
- DEL-17.01 (Electrical Power Design Drawing Set) → cable schedules, equipment locations, grounding layout
- DEL-17.03 (Electrical Power Design Calculations) → load calculations, equipment sizing, cable sizing
- DEL-17.04 (Electrical Power Data Sheet Package) → equipment counts, sizes, ratings

**Current Status:** PKG-17 deliverable folders not yet scaffolded in execution workspace

### Decomposition

**Status:** Used (primary source for scope definition)

**Source:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`

**Content Used:**
- Lines 435-449: PKG-17 Electrical Power Distribution scope and deliverables
- Scope description: "MV/LV distribution, transformers, switchgear, MCC, panels, grounding, cable installation"
- 5 deliverables (DEL-17.01 through DEL-17.05)

**Limitations:** Decomposition provides high-level scope only; no quantities, equipment sizes, or layout information

### Equipment Packages (Interface Coordination)

**Status:** Not available

**Expected Coordination Sources (future):**
- PKG-10 Railcar Unloading System → motor loads for railcar unloading pumps and equipment
- PKG-11 Marine Loading System → motor loads for marine loading pumps and loading arm
- PKG-13 Storage Tanks → agitator motor loads, tank heating loads (if required)
- PKG-15 Pumps & Rotating Equipment → pump motor nameplate data, VFD requirements
- PKG-19 Control Systems → control system power requirements, UPS loads
- PKG-20 Field Instrumentation → instrument power requirements
- PKG-21 Building Structures & Envelope → MCC building sizing (affects electrical room layout)
- PKG-22 Building Interior & MEP → building HVAC and lighting loads

**Current Status:** Interface packages not yet developed; motor loads and equipment power requirements TBD

---

## 4. Embedded Fallback Model (Used as Last Resort)

**Status:** Used for 100% of pricing (all line items)

**Model Reference:** AGENT_ESTIMATING.md lines 645-713 (Fallback Typical Model)

**Usage Justification (per D-1703):**
- No vendor quotes available
- No rate tables available
- No historical data available
- No deliverable quantities available (folders do not exist)

**Model Application:**

### Engineering Allowances (E)
- Drawing production: Scaled by anticipated drawing count and complexity for electrical discipline
- Specifications: Scaled by specification types and page count estimates
- Calculations: Scaled by calculation complexity (load flow, short circuit, coordination, voltage drop)
- Data sheets: Scaled by equipment count
- Test records: Scaled by testing scope and documentation requirements

**Basis:** Comparable to other package engineering allowances, adjusted for electrical discipline complexity

### Materials Allowances (MAT)
- Transformers: Industry-typical $/kVA for pad-mounted oil-filled transformers
- Switchgear: Industry-typical $/bay for metal-clad switchgear
- MCCs: Industry-typical $/starter or $/HP controlled
- Cables: Industry-typical $/m by voltage level and conductor size
- Cable tray: Industry-typical $/m including fittings and supports
- Conduit: Industry-typical $/m by size and type (PVC, rigid)
- Grounding: Industry-typical for ground grid and electrode installation

**Basis:** Industrial electrical installation typical unit costs scaled to facility scope

### Construction Allowances (CD)
- Installation labor: Scaled by equipment size and complexity
- Cable pulling: Scaled by cable length and termination count
- Testing: Scaled by equipment count and testing requirements

**Basis:** Industrial electrical contractor labor productivity assumptions

### Parametric Factors (CI, PM, P, COM)
- CI = 18% of CD (supervision, safety, QA/QC)
- PM = 6% of (CD + CI + MAT + FRT) (EPCM allocation)
- P = 2% of (MAT + FRT) (procurement coordination)
- COM = 3% of (CD + CI + MAT) (commissioning and testing support)

**Basis:** Fallback Typical Model defaults per AGENT_ESTIMATING.md lines 666-673

---

## 5. Sources Not Available (Gaps)

### Critical Gaps (High Impact)

1. **Load calculations** — required to size transformers, switchgear, MCCs, cables
2. **Vendor budgetary quotes** — required for equipment pricing confidence
3. **Equipment layout drawings** — required for cable routing and length estimates
4. **ER requirements extraction** — required for design criteria, redundancy, standards
5. **Motor schedules from equipment packages** — required for load calculations

### Important Gaps (Medium Impact)

6. **Utility service parameters** — voltage, capacity, connection point
7. **Soil resistivity survey data** — required for grounding design
8. **Hazardous area classification** — affects equipment ratings and cable types
9. **Electrical contractor labor rates** — required for installation labor pricing
10. **Material supplier quotations** — required for cable, cable tray, conduit pricing

---

## 6. Source Priority Recommendations

**To improve estimate to Class 4 (Budget Authorization):**

1. **Develop load calculations** (DEL-17.03) — enables equipment sizing validation
2. **Obtain budgetary quotes** from 3 vendors for transformers, switchgear, MCCs
3. **Extract ER requirements** (Vol 2 Parts 1-3) for electrical design basis
4. **Develop preliminary electrical layout** (DEL-17.01) to measure cable routing lengths
5. **Coordinate with equipment packages** to obtain motor loads and control power requirements

**To improve estimate to Class 3 (Control Estimate):**

6. **Obtain firm vendor quotes** for transformers, switchgear, MCCs
7. **Develop detailed cable schedules** from 60%-90% design drawings
8. **Obtain electrical contractor labor rates** and productivity data
9. **Conduct soil resistivity survey** and complete grounding design
10. **Create project-specific electrical equipment rate table** in `_RateTables/`

---

## 7. Source Summary

| Source Category | Count | Usage | Confidence |
|-----------------|-------|-------|------------|
| Vendor Quotes | 0 | 0% | N/A |
| Rate Tables | 0 | 0% | N/A |
| Historical Data | 0 | 0% | N/A |
| Deliverable Documents | 0 | 0% | N/A |
| Decomposition | 1 | Scope definition only | HIGH (for scope) |
| Fallback Model | 1 | 100% pricing | LOW |

**Overall Source Quality:** LOW (no project-specific pricing sources)

**Estimate Class Limitation:** Class 5 maximum with current sources

---

**END OF SOURCE INDEX**
