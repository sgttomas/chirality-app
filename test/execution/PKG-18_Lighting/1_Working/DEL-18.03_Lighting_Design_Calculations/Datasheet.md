# Datasheet: DEL-18.03 Lighting Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-18.03 |
| Name | Lighting Design Calculations |
| Package | PKG-18 Lighting |
| Discipline | Electrical |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Calculation Document Number | **TBD** — Per project calculation numbering system |
| Calculation Software | **TBD** — **ASSUMPTION**: AGi32, DIALux, or other photometric calculation software per IESNA methods |
| Calculation Format | **TBD** — **ASSUMPTION**: PDF report with input data, methodology, results, and software output files |
| Calculation Standard | IESNA calculation methods — **TBD** *(IESNA Lighting Handbook edition TBD)* |
| Design Code | CSA C22.1, IESNA, NFPA 101 for emergency lighting — **ASSUMPTION** |
| Revision Control | **TBD** — Per project document control procedures |
| Classification | **TBD** — **ASSUMPTION**: For Construction / Design Basis |

**Calculation Scope:**

| Attribute | Value |
|-----------|-------|
| Calculation Categories | Exterior illumination, Interior illumination per anticipated artifacts *(Source: _CONTEXT.md, Decomposition)* |
| Calculation Method | Point-by-point or zonal cavity (lumen method) per IESNA — **TBD** — **ASSUMPTION**: Point-by-point typical for photometric software |
| Input Data Sources | ER requirements, codes (CSA C22.1, IESNA), fixture photometric data (IES files) — **TBD** |
| Output | Illuminance levels (lux or footcandles), uniformity ratios, contour plots, fixture schedules — **ASSUMPTION** |

## Conditions

**Operating / Environmental Context:**

This deliverable provides the engineering basis and sizing/verification calculations for lighting. *(Source: _CONTEXT.md, Decomposition DEL-18.03 description)*

**Project Context:**
- **Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC *(Source: Decomposition Section 1)*
- **Facility Type:** Canola Oil Transload Facility *(Source: Decomposition Section 1)*
- **Environment:** Marine terminal with outdoor exposure and industrial process areas

**Design Basis:**

| Parameter | Value |
|-----------|-------|
| Required Illuminance Levels | **TBD** — Per ER requirements, IESNA recommendations, and CSA C22.1 — **ASSUMPTION**: Varies by area type (process, roadway, office, warehouse, emergency egress) |
| Uniformity Requirements | **TBD** — **ASSUMPTION**: Typical maximum-to-minimum ratio 4:1 for general areas; 3:1 for task areas per IESNA |
| Reflectance Values | **TBD** — **ASSUMPTION**: Ground/pavement 20-30%, walls 50%, ceilings 70-80% typical for calculation inputs |
| Maintenance Factor | **TBD** — **ASSUMPTION**: 0.85-0.90 typical to account for dirt depreciation and lumen maintenance |
| Design Conditions | **TBD** — Normal operating conditions; emergency lighting calculations separate |

**Calculation Inputs:**

| Input Category | Value |
|----------------|-------|
| Site Geometry | **TBD** — Site plans, building layouts from architectural/civil drawings (PKG-01, PKG-21, PKG-22) |
| Fixture Photometric Data | **TBD** — IES files from manufacturers per fixture selection (coordinated with DEL-18.02 and DEL-18.04) |
| Mounting Heights | **TBD** — Per design drawings (DEL-18.01) — **ASSUMPTION**: 30-40 ft for exterior poles; 20-30 ft for interior high-bay |
| Obstructions and Shading | **TBD** — Buildings, structures, equipment that may block light |

## Construction

**Calculation Deliverables:**

Anticipated artifacts per decomposition and _CONTEXT.md:
1. **Illumination calculations (exterior)** — Photometric calculations for all exterior lighting areas
2. **Illumination calculations (interior)** — Photometric calculations for all interior lighting areas

**Typical Calculation Package Contents:**

**Exterior Illumination Calculations:**
- **Site areas:** Process areas, roadways, parking, perimeter security lighting
- **Calculations:** Point-by-point illuminance calculations showing horizontal illuminance (lux or fc) at ground level
- **Results:** Illuminance contour plots overlaid on site plan, summary tables of average/minimum/maximum/uniformity values, fixture schedule
- **Verification:** Comparison to required illuminance levels per ER and codes — **TBD**

**Interior Illumination Calculations:**
- **Building areas:** Warehouse/process areas, control rooms, offices, maintenance areas
- **Calculations:** Point-by-point or zonal cavity calculations showing horizontal and/or vertical illuminance
- **Results:** Illuminance contour plots overlaid on floor plans, summary tables, fixture schedule
- **Verification:** Comparison to required illuminance levels per ER and codes — **TBD**

**Emergency Lighting Calculations (if separate):**
- **Egress paths:** Emergency illuminance calculations for exit routes, corridors, stairwells
- **Requirements:** Minimum 10 lux (1 fc) average, 1 lux (0.1 fc) minimum per NFPA 101 — **TBD** — **ASSUMPTION**
- **Results:** Illuminance values demonstrating code compliance

**Calculation Report Structure:**

- **Cover Sheet:** Project, deliverable ID, calculation title, date, revision, engineer, checker (see Procedure)
- **Design Basis:** Required illuminance levels, codes/standards, design criteria (see Specification)
- **Input Data:** Fixture photometric files, site geometry, reflectances, mounting heights
- **Methodology:** Calculation method (point-by-point, lumen method), software used, assumptions (see Guidance)
- **Results:** Illuminance summary tables, contour plots, uniformity analysis
- **Fixture Schedule:** Fixture types, quantities, locations, wattages (coordinated with DEL-18.01)
- **Verification:** Comparison to requirements, code compliance demonstration (see Specification)
- **Appendices:** Software output files, IES photometric data, site plans with calculation grid
- **Sign-Off:** Engineer and checker signatures — **TBD** (see Procedure)

**Calculation Software and Methods:**

| Aspect | Value |
|--------|-------|
| Software | **TBD** — **ASSUMPTION**: AGi32, DIALux, Visual, or other IESNA-accepted photometric software |
| Calculation Method | Point-by-point (for irregular areas), zonal cavity/lumen method (for regular spaces) — **TBD** — **ASSUMPTION**: Point-by-point typical |
| Photometric Data Format | IES files (IESNA LM-63 format) from manufacturers — **ASSUMPTION** |
| Output Format | **TBD** — **ASSUMPTION**: PDF calculation report + native software files for future updates |

**Interface Requirements:**

- **Lighting Design Drawings (DEL-18.01)** — Fixture locations, types, mounting heights from calculations match drawings — **ASSUMPTION**
- **Lighting Technical Specification (DEL-18.02)** — Fixture performance (lumens, distribution) specified matches calculation inputs — **ASSUMPTION**
- **Lighting Data Sheets (DEL-18.04)** — Photometric data (IES files) from data sheets used in calculations — **ASSUMPTION**
- **Architectural/civil base drawings (PKG-01, PKG-21, PKG-22)** — Site geometry for calculation models — **TBD**
- **Employer's Requirements** — Required illuminance levels and quality criteria — **TBD** *(ER location TBD)*

## References

**Primary References:**
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — PKG-18 scope, DEL-18.03 entry
- Context: `_CONTEXT.md` — Deliverable identity and anticipated artifacts
- Specification: `Specification.md` — Requirements for lighting calculations
- Guidance: `Guidance.md` — Calculation principles and methodology
- Procedure: `Procedure.md` — Calculation development process

**Applicable Standards:**
- **IESNA Lighting Handbook** — Illumination design criteria and calculation methods — **TBD** *(Edition and location TBD)*
- **IES RP-33** — Lighting for Exterior Environments — **TBD**
- **IES RP-1** — Office Lighting (if applicable for interior spaces) — **TBD**
- **NFPA 101** (Life Safety Code) — Emergency lighting requirements — **ASSUMPTION**
- **CSA C22.1** (Canadian Electrical Code) — Illumination requirements (if specified) — **ASSUMPTION**

**Project-Specific References:**
- Employer's Requirements Volume 2 Part 1, Part 2, Part 3 — Illuminance requirements — **TBD** — Location TBD in `0_References/`
- Site survey and base drawings — Site geometry for models — **TBD**
- Photometric calculation software user manual — **TBD**

**Cross-References (within PKG-18):**
- DEL-18.01 Lighting Design Drawing Set — Fixture layouts based on calculations; calculation results may be overlaid on drawings
- DEL-18.02 Lighting Technical Specification — Fixture performance specifications match calculation inputs
- DEL-18.04 Lighting Data Sheet Package — Photometric data (IES files) from data sheets used in calculations
- DEL-18.05 Lighting Installation & Test Records — Field illuminance testing verifies calculated predictions
