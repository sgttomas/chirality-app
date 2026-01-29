# Guidance: DEL-18.03 Lighting Design Calculations

## Purpose

This guidance document supports the development of **Lighting Design Calculations** for **PKG-18 Lighting** on the Canola Oil Transload Facility project.

**Deliverable Purpose:** Provides the engineering basis and sizing/verification calculations for lighting. *(Source: _CONTEXT.md, Decomposition DEL-18.03 description)*

**Role in Project:** These calculations provide the technical foundation for the lighting design, demonstrating that the proposed lighting system meets performance requirements and code compliance. The calculations support:
- Design optimization (fixture selection, spacing, mounting heights)
- Verification of compliance with ER illuminance requirements
- Code compliance demonstration (CSA C22.1, IESNA, NFPA 101)
- Coordination with lighting drawings (DEL-18.01), specification (DEL-18.02), and equipment data sheets (DEL-18.04)
- Field testing benchmarks (DEL-18.05)

**Deliverable Classification:**
- **Type:** Calculation
- **Discipline:** Electrical
- **Responsible Party:** D&B Contractor

## Principles

**Engineering Rationale (Photometric Calculations):**

**P-1: Photometric Calculation Methods**
- **Point-by-point method:** Calculates illuminance at specific grid points using inverse-square law and fixture photometry — most accurate for irregular areas and exterior applications — **ASSUMPTION**
- **Zonal cavity (lumen) method:** Calculates average illuminance in regular rooms using room cavity ratios and coefficients of utilization — faster for regular interior spaces — **ASSUMPTION**
- Software tools (AGi32, DIALux, Visual, etc.) automate these methods and provide graphical outputs — **TBD**

**P-2: Illuminance Requirements Basis**
- **Task-based illuminance:** IESNA recommends illuminance levels based on visual task difficulty and importance — **TBD** *(IESNA Handbook edition TBD)*
- **Code minimums:** CSA C22.1 and NFPA 101 specify minimum levels for safety (emergency egress) — **ASSUMPTION**
- **ER requirements:** Project-specific requirements may exceed code minimums for operational or safety reasons — **TBD** *(ER location TBD)*

**P-3: Uniformity Principles**
- **Visual comfort:** Excessive variation in illuminance causes discomfort and reduces visibility — **ASSUMPTION**
- **Typical uniformity criteria:** Maximum-to-minimum ratio ≤ 4:1 for general areas; ≤ 3:1 for task areas per IESNA — **TBD** — **ASSUMPTION**
- **Hot spots and dark spots:** Calculations identify areas needing fixture adjustment to improve uniformity — **ASSUMPTION**

**P-4: Maintenance Factor**
- **Lumen depreciation:** LED output decreases over life per LM-80/TM-21 data — L70 (70% output) at rated hours typical — **TBD**
- **Dirt depreciation:** Dust and dirt accumulation on fixtures reduces output — severity depends on environment — **ASSUMPTION**
- **Combined maintenance factor:** Typical range 0.80-0.90; marine/industrial environment may require lower factor — **TBD** — **ASSUMPTION**
- **Initial vs. maintained illuminance:** Calculations typically show maintained (end-of-life) illuminance to ensure long-term compliance — **ASSUMPTION**

**P-5: Modeling Accuracy**
- **Photometric data:** IES files from manufacturer testing (per IES LM-79) provide accurate fixture performance data — **ASSUMPTION**
- **Site geometry:** Accurate building and site models ensure realistic illuminance predictions — **TBD**
- **Reflectances:** Surface reflectance assumptions affect inter-reflected light; realistic values improve accuracy — **ASSUMPTION**
- **Obstructions:** Modeling buildings, equipment, and structures that block or reflect light improves accuracy for complex sites — **ASSUMPTION**

**Applicable Standards Context:**

**IESNA Standards:**
- **IESNA Lighting Handbook** — Recommended illuminance levels, calculation methods, quality criteria — **TBD** *(Edition TBD)*
- **IES RP-33** (Lighting for Exterior Environments) — Guidance for outdoor area lighting — **TBD**
- **IES RP-7** (Industrial Lighting) — Guidance for industrial facilities (if applicable) — **TBD**
- **IES LM-63** — IES file format standard for photometric data — **ASSUMPTION**

**Codes:**
- **NFPA 101** (Life Safety Code) — Emergency egress lighting: 10 lux (1 fc) average, 1 lux (0.1 fc) minimum — **TBD** — **ASSUMPTION**
- **CSA C22.1** — May specify illuminance requirements for certain applications — **TBD**

## Considerations

**Factors to Consider During Calculation Development:**

**C-1: Required Illuminance Levels**
- Illuminance requirements vary by area type and task:
  - **Exterior process areas:** Moderate levels for safe equipment operation and maintenance — **TBD** — **ASSUMPTION**: 50-100 lux typical
  - **Exterior roadways:** Lower levels sufficient for vehicle movement — **TBD** — **ASSUMPTION**: 10-20 lux typical
  - **Interior warehouse/process:** Moderate to high levels for material handling and process monitoring — **TBD** — **ASSUMPTION**: 200-500 lux depending on task
  - **Interior offices/control rooms:** Higher levels for detailed visual tasks — **TBD** — **ASSUMPTION**: 300-500 lux typical
  - **Emergency egress:** Code minimum per NFPA 101 — **TBD** — **ASSUMPTION**: 10 lux average minimum
- Verify requirements against ER, IESNA recommendations, and codes — **TBD**

**C-2: Calculation Grid and Modeling**
- **Grid spacing:** 1-3 meter spacing typical; finer grid for small areas or detailed analysis — **TBD** — **ASSUMPTION**
- **Calculation height:** Ground level (0.0 m) for exterior; work plane height (0.76-0.85 m typical) for interior — **ASSUMPTION**
- **Boundaries:** Extend calculation grid beyond lighted area to capture spill light and edge effects — **ASSUMPTION**
- **Obstructions:** Model buildings, tanks, racks, and major equipment that block or reflect light — **ASSUMPTION**

**C-3: Photometric Data Sources**
- **Manufacturer IES files:** Use certified photometric data from proposed fixtures or representative fixtures — **ASSUMPTION**
- **Generic vs. specific data:** Generic IES files may be used for preliminary calculations; final calculations require manufacturer-specific data — **ASSUMPTION**
- **Photometric testing standards:** IES files should be from IES LM-79 laboratory testing for accuracy — **ASSUMPTION**

**C-4: Reflectance Assumptions**
- **Exterior:**
  - Asphalt/pavement: 10-20% — **ASSUMPTION**
  - Concrete: 20-30% — **ASSUMPTION**
  - Gravel: 10-15% — **ASSUMPTION**
- **Interior:**
  - Walls: 40-60% depending on color and finish — **ASSUMPTION**
  - Ceilings: 70-80% for light-colored ceilings — **ASSUMPTION**
  - Floors: 20-30% typical for industrial floors — **ASSUMPTION**
- Use realistic values; verify with architectural finishes where available — **TBD**

**C-5: Maintenance Factor Selection**
- Consider:
  - **Environment:** Clean (0.90-0.95), Normal (0.85-0.90), Dirty (0.75-0.85) — **TBD** — **ASSUMPTION**: Marine/industrial environment likely "Dirty"
  - **Fixture IP rating:** Higher IP rating reduces dirt ingress and degradation — **ASSUMPTION**
  - **Cleaning schedule:** More frequent cleaning allows higher maintenance factor — **TBD**
  - **LED lumen maintenance:** Use L70 hours from manufacturer data (per IES LM-80/TM-21) — **TBD**
- Document maintenance factor selection and justification in calculation report — **ASSUMPTION**

**C-6: Emergency Lighting Calculations**
- Emergency lighting requires separate calculations to demonstrate NFPA 101 compliance — **ASSUMPTION**
- Use battery-backed fixture output (may be reduced from normal output) — **TBD**
- Calculate illuminance along egress paths (corridors, exits, stairwells) — **ASSUMPTION**
- Verify minimum 10 lux average and 1 lux minimum per NFPA 101 — **TBD** — **ASSUMPTION**

**C-7: Coordination with Other Deliverables**
- **DEL-18.01 (Drawings):** Fixture locations, types, mounting heights in calculations must match drawings — **ASSUMPTION**
- **DEL-18.02 (Specification):** Fixture performance (lumens, distribution) must match specification requirements — **ASSUMPTION**
- **DEL-18.04 (Data Sheets):** IES files from data sheets used in calculations; if proposed fixtures differ, recalculation may be needed — **ASSUMPTION**
- Iterative process: calculations inform design; design adjustments require recalculation — **ASSUMPTION**

**C-8: Sensitivity and Optimization**
- **Sensitivity analysis:** Test effect of mounting height, spacing, aiming angle adjustments on illuminance and uniformity — **TBD** — **ASSUMPTION**: Good practice for optimization
- **Fixture count vs. performance:** Trade-off between number of fixtures and fixture output/cost — see Trade-offs section
- **Pole height optimization:** Taller poles provide wider coverage (fewer poles) but higher cost and maintenance difficulty — see Trade-offs section

## Trade-offs

**Competing Concerns to Evaluate:**

**T-1: Illuminance Level vs. Energy Cost**
- **Higher illuminance** improves visibility and safety but increases fixture count, wattage, and energy cost
- **Lower illuminance** reduces energy and capital cost but may compromise safety or productivity
- **Resolution approach:**
  - Use IESNA recommended levels as starting point; adjust based on ER requirements and operational needs — **TBD**
  - Avoid over-lighting; use controls (occupancy, daylight harvesting) to reduce energy waste — **ASSUMPTION**

**T-2: Uniformity vs. Fixture Count**
- **Better uniformity** (lower max/min ratio) requires closer fixture spacing or more fixtures — increases cost
- **Poorer uniformity** (higher max/min ratio) acceptable for some applications — reduces fixture count and cost
- **Resolution approach:**
  - Balance uniformity requirements with cost; prioritize uniformity in task areas and safety-critical areas — **ASSUMPTION**
  - Use IESNA uniformity guidelines (typically 4:1 general, 3:1 task) as target — **TBD** — **ASSUMPTION**

**T-3: Pole Height vs. Coverage vs. Cost**
- **Taller poles** (40-50 ft) provide wider coverage (fewer poles, less clutter) but higher cost, more difficult maintenance, greater wind loading
- **Shorter poles** (25-30 ft) easier and cheaper to install and maintain, but require more poles for same coverage
- **Resolution approach:**
  - Optimize pole height using photometric calculations; balance coverage, cost, and maintenance access — **ASSUMPTION**
  - Typical range 30-40 ft for area lighting; adjust based on specific site conditions — **ASSUMPTION**

**T-4: Calculation Detail vs. Schedule**
- **Detailed calculations** (fine grid, obstructions modeled, sensitivity analysis) provide accurate results but require more time
- **Simplified calculations** (coarser grid, simplified geometry) faster but may miss hot spots or edge effects
- **Resolution approach:**
  - Use appropriate level of detail for application; preliminary design may use simplified calculations; final design requires detailed calculations — **ASSUMPTION**
  - Focus detail on critical areas (egress paths, high-traffic, hazardous areas) — **ASSUMPTION**

**T-5: Maintenance Factor Conservatism**
- **Low maintenance factor** (0.75-0.80) ensures long-term illuminance compliance but requires more fixtures initially (higher cost)
- **High maintenance factor** (0.90-0.95) reduces fixture count and cost but may result in inadequate illuminance later in life if maintenance is poor
- **Resolution approach:**
  - Use realistic maintenance factor based on environment and expected maintenance practices — **ASSUMPTION**
  - For marine/industrial environment, conservative factor (0.80-0.85) prudent — **TBD** — **ASSUMPTION**

**T-6: Generic vs. Manufacturer-Specific Data**
- **Generic IES files** allow calculations before equipment selection; flexible but may not accurately represent final fixtures
- **Manufacturer-specific IES files** provide accurate performance but lock in equipment selection or require recalculation if changed
- **Resolution approach:**
  - Use generic data for preliminary design and budgeting; update with manufacturer data when equipment is selected — **ASSUMPTION**
  - Final calculations must use manufacturer-certified IES files from proposed fixtures — **ASSUMPTION**

## Examples

**Reference Examples and Precedents:**

**E-1: Typical Calculation Inputs**

**Exterior Area Lighting:**
- Fixture type: LED area light, 20,000 lumens, Type III distribution (forward throw)
- Mounting height: 35 ft on poles
- Spacing: 80-100 ft typical (optimized in calculations)
- Reflectance: Asphalt 15%
- Maintenance factor: 0.85
- Required illuminance: 50 lux average — **TBD**

**Interior High-Bay Lighting:**
- Fixture type: LED high-bay, 25,000 lumens
- Mounting height: 25 ft
- Spacing: 25-30 ft typical
- Reflectances: Walls 50%, ceiling 80%, floor 30%
- Maintenance factor: 0.88
- Required illuminance: 300 lux average — **TBD**

**Emergency Egress Lighting:**
- Fixture type: LED emergency fixture with battery backup, 1,000 lumens
- Mounting height: 8-10 ft on walls
- Spacing: Per calculations to achieve code minimums
- Required illuminance: 10 lux average, 1 lux minimum per NFPA 101 — **ASSUMPTION**

**E-2: Typical Calculation Results Format**

**Illuminance Summary Table Example:**

| Area | Avg (lux) | Min (lux) | Max (lux) | Max/Min | Avg/Min | Required (lux) | Status |
|------|-----------|-----------|-----------|---------|---------|----------------|--------|
| Process Area East | 75 | 35 | 110 | 3.1 | 2.1 | 50 | PASS |
| Roadway A | 15 | 8 | 22 | 2.8 | 1.9 | 10 | PASS |
| Warehouse Interior | 320 | 180 | 450 | 2.5 | 1.8 | 300 | PASS |
| Egress Corridor 1 | 12 | 5 | 18 | 3.6 | 2.4 | 10 avg, 1 min | PASS |

**E-3: Calculation Report Sections**

**Cover Sheet:**
- Project: Canola Oil Transload Facility
- Deliverable: DEL-18.03 Lighting Design Calculations
- Title: Exterior Illumination Calculations
- Date: [Date]
- Revision: A
- Prepared by: [Engineer Name], P.Eng. [Number]
- Checked by: [Checker Name], P.Eng. [Number]
- Approved by: [Discipline Lead]

**Design Basis Example:**
"This calculation determines illuminance levels for exterior process areas, roadways, and perimeter security lighting. Required illuminance levels are per Employer's Requirements Section X.X and IESNA RP-33. Calculations use point-by-point method with AGi32 software version X.X. Maintenance factor 0.85 accounts for marine environment dirt accumulation and LED lumen depreciation per IES LM-80 data."

**E-4: Software Output Examples**
- **Illuminance contour plot:** Site plan overlaid with color-coded illuminance contours (e.g., 0-10 lux, 10-20 lux, 20-50 lux, 50-100 lux, >100 lux)
- **3D rendering:** Perspective view of site showing lighting effect and fixture locations
- **Calculation grid:** Point-by-point illuminance values at each grid node
- **Fixture schedule:** Table of fixture tags, types, locations, mounting heights, wattages, lumen outputs

**E-5: Anticipated Artifacts**

Per decomposition and _CONTEXT.md:
1. **Illumination calculations (exterior)** — Photometric calculation report covering all exterior lighting areas with contour plots, summary tables, verification
2. **Illumination calculations (interior)** — Photometric calculation report covering all interior lighting areas with contour plots, summary tables, verification

**E-6: Industry Best Practices**
- **Maintained illuminance:** Calculate maintained (end-of-life) illuminance to ensure long-term compliance; initial illuminance will be higher — **ASSUMPTION**
- **Uniformity verification:** Check max/min ratio in addition to average illuminance; excessive variation causes visual discomfort — **ASSUMPTION**
- **Emergency lighting:** Calculate emergency lighting separately using battery-backed lumen output; verify both average and minimum code requirements — **ASSUMPTION**
- **Sensitivity checks:** Test effect of ±10% fixture output variation to ensure design is robust — **TBD** — **ASSUMPTION**: Good practice
- **Archive software files:** Save native calculation files for future updates when design changes or different fixtures are proposed — **ASSUMPTION**

**References for Examples:**
- IESNA Lighting Handbook — **TBD** *(Edition and location TBD)*
- IES RP-33 (Exterior Lighting) — **TBD**
- Manufacturer photometric data and IES files — **TBD**
- Employer's Requirements — **TBD** *(Vol 2 Part 1, Part 2, Part 3 — location TBD)*
