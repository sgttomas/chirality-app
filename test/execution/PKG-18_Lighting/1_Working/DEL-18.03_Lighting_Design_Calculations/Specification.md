# Specification: DEL-18.03 Lighting Design Calculations

## Scope

This specification defines the requirements for the **Lighting Design Calculations** deliverable within **PKG-18 Lighting** for the Canola Oil Transload Facility.

**Purpose:** Provides the engineering basis and sizing/verification calculations for lighting. *(Source: _CONTEXT.md, Decomposition DEL-18.03 description)*

**Package Scope:** Interior and exterior LED lighting, lighting controls, emergency lighting. *(Source: Decomposition PKG-18 scope)*

**Deliverable Artifacts:**
- Illumination calculations (exterior)
- Illumination calculations (interior)

*(Source: _CONTEXT.md, Decomposition DEL-18.03 anticipated artifacts)*

**Inclusions:**
- Photometric calculations for all exterior lighting areas (process areas, roadways, parking, perimeter)
- Photometric calculations for all interior lighting areas (warehouse/process, offices, control rooms, utilities)
- Emergency lighting calculations demonstrating code compliance
- Illuminance contour plots and summary tables
- Fixture schedules showing types, quantities, locations, wattages
- Verification of illuminance levels against ER requirements and codes
- Calculation methodology, assumptions, and input data documentation
- Engineer and checker sign-offs

**Exclusions:**
- Lighting fixture procurement specifications (see DEL-18.02)
- Lighting layout drawings (see DEL-18.01 — calculations support and verify drawings)
- Electrical load calculations and panel sizing (see PKG-17 electrical power distribution)
- Energy modeling or lifecycle cost analysis (unless specifically required by ER)

## Requirements

### Functional Requirements

**FR-1: Calculation Coverage**
- Calculations shall cover all areas requiring lighting per design drawings (DEL-18.01) — **ASSUMPTION**
- Exterior areas: process areas, roadways, parking, perimeter security — **TBD** *(Specific areas per ER and design)*
- Interior areas: warehouse/process, offices, control rooms, maintenance, utility areas — **TBD**
- Emergency egress paths: corridors, exits, stairwells per NFPA 101 — **ASSUMPTION**

**FR-2: Calculation Methodology**
- Calculations shall use recognized photometric methods per IESNA — **ASSUMPTION**
- Point-by-point method for irregular areas and exterior applications — **ASSUMPTION**
- Zonal cavity (lumen) method for regular interior spaces (if applicable) — **TBD**
- Software-based calculations using IESNA-accepted software (AGi32, DIALux, Visual, or equivalent) — **TBD**

**FR-3: Input Data and Assumptions**
- All input data shall be documented:
  - Fixture photometric data (IES files per IESNA LM-63 format) from manufacturers — **ASSUMPTION**
  - Site geometry from architectural and civil drawings — **TBD**
  - Mounting heights per design drawings (DEL-18.01) — **ASSUMPTION**
  - Surface reflectances (ground, walls, ceilings) — **TBD** — **ASSUMPTION**: Typical values per IESNA Handbook
  - Maintenance factors accounting for dirt depreciation and lumen depreciation — **TBD** — **ASSUMPTION**: 0.85-0.90 typical
- All assumptions shall be clearly stated and justified — **ASSUMPTION**

**FR-4: Calculation Outputs**
- Calculations shall provide:
  - Illuminance values (lux or footcandles) at calculation grid points — **ASSUMPTION**
  - Average, minimum, maximum illuminance values for each area — **ASSUMPTION**
  - Uniformity ratios (max/min, avg/min) — **ASSUMPTION**
  - Illuminance contour plots overlaid on site/floor plans — **ASSUMPTION**
  - Fixture schedules (type, quantity, location, wattage, lumen output) — **ASSUMPTION**
  - Verification against required illuminance levels — **ASSUMPTION**

### Performance Requirements

**PR-1: Illuminance Levels**
- Calculated illuminance levels shall meet or exceed required levels per:
  - Employer's Requirements — **TBD** *(ER location TBD)*
  - IESNA recommended illuminance levels for task/area types — **TBD** *(IESNA Handbook edition TBD)*
  - CSA C22.1 requirements (if specified) — **TBD**
  - NFPA 101 emergency egress lighting requirements — **ASSUMPTION**

**Typical Required Levels (to be confirmed against ER and codes):**
- Exterior process areas: **TBD** — **ASSUMPTION**: 50-100 lux typical
- Exterior roadways and parking: **TBD** — **ASSUMPTION**: 10-20 lux typical
- Interior warehouse/process: **TBD** — **ASSUMPTION**: 200-500 lux typical depending on task
- Interior offices and control rooms: **TBD** — **ASSUMPTION**: 300-500 lux typical
- Emergency egress paths: **TBD** — **ASSUMPTION**: 10 lux average, 1 lux minimum per NFPA 101

**PR-2: Uniformity**
- Calculated uniformity ratios shall meet requirements per:
  - ER requirements — **TBD**
  - IESNA recommendations — **TBD** — **ASSUMPTION**: Maximum-to-minimum ratio typically 4:1 for general areas; 3:1 for task areas
- Areas with excessive non-uniformity shall be identified and resolved — **ASSUMPTION**

**PR-3: Calculation Accuracy**
- Calculations shall use manufacturer-certified photometric data (IES files from laboratory testing per IES LM-79) — **ASSUMPTION**
- Calculation software shall be current version with validated algorithms — **TBD**
- Calculation grid density sufficient to capture illuminance variation — **TBD** — **ASSUMPTION**: 1-3 meter grid spacing typical
- Obstructions and shading effects shall be modeled where significant — **ASSUMPTION**

**PR-4: Maintenance Factor**
- Maintenance factor shall account for:
  - Lumen depreciation over fixture life (per IES LM-80/TM-21 data for LED) — **TBD**
  - Dirt depreciation based on environment (clean, normal, dirty) — **TBD** — **ASSUMPTION**: "Normal" or "Dirty" for marine/industrial environment
  - Combined maintenance factor typically 0.80-0.90 — **TBD**
- Maintenance factor assumptions shall be justified and documented — **ASSUMPTION**

### Interface Requirements

**IR-1: Lighting Design Drawings (DEL-18.01)**
- Calculations shall be coordinated with lighting design drawings — **ASSUMPTION**
- Fixture types, quantities, locations, and mounting heights shall match between calculations and drawings — **ASSUMPTION**
- Calculation results (contour plots) may be shown on drawings for reference — **ASSUMPTION**

**IR-2: Lighting Technical Specification (DEL-18.02)**
- Fixture performance specifications (lumens, efficacy, distribution) shall match calculation inputs — **ASSUMPTION**
- IES photometric files used in calculations shall represent specified fixtures or acceptable equivalents — **ASSUMPTION**

**IR-3: Lighting Data Sheet Package (DEL-18.04)**
- IES photometric files from manufacturer data sheets shall be used in calculations — **ASSUMPTION**
- If proposed fixtures differ from calculated fixtures, recalculation may be required — **ASSUMPTION**

**IR-4: Employer's Requirements**
- Required illuminance levels from ER shall be incorporated into calculation criteria — **TBD** *(ER location TBD)*
- Calculation format and deliverable requirements per ER — **TBD**

**IR-5: Architectural and Civil Drawings (PKG-01, PKG-21, PKG-22)**
- Site plans and building floor plans used as base for calculation models — **TBD**
- Building dimensions, ceiling heights, surface finishes for reflectance assumptions — **TBD**

### Quality Requirements

**QR-1: Calculation Documentation**
- Calculations shall be documented in a formal calculation report including:
  - Cover sheet with project, deliverable ID, title, date, revision, signatures — **ASSUMPTION**
  - Design basis and criteria
  - Input data and assumptions
  - Methodology and software
  - Results (tables, plots, schedules)
  - Verification and conclusions
  - Appendices with software output files — **ASSUMPTION**

**QR-2: Independent Check**
- Calculations shall be independently checked by a qualified engineer (P.Eng.) not involved in original calculations — **TBD** — **ASSUMPTION**: Standard practice for engineering calculations
- Checker shall verify:
  - Input data correctness and appropriateness
  - Methodology and assumptions
  - Calculation results
  - Compliance with requirements and codes
- Checker sign-off required — **TBD**

**QR-3: Software and Files**
- Calculation software files shall be retained for future updates and revisions — **TBD**
- Software version shall be documented — **ASSUMPTION**
- IES photometric files shall be archived with calculation files — **ASSUMPTION**

**QR-4: Revision Control**
- Calculation revisions shall be controlled per project document control procedures — **TBD**
- Revision history shall be documented showing changes and reasons — **ASSUMPTION**

## Standards

**Applicable Codes and Standards:**

**Lighting Design Standards:**
- **IESNA Lighting Handbook** — Illumination design criteria, recommended levels, calculation methods — **TBD** *(Edition TBD)*
- **IES RP-33** — Lighting for Exterior Environments — **TBD**
- **IES RP-1** — Office Lighting (if applicable) — **TBD**
- **IES RP-7** — Industrial Lighting (if applicable) — **TBD**

**Photometric Data and Testing:**
- **IESNA LM-63** — IES file format for photometric data — **ASSUMPTION**
- **IES LM-79** — Approved method for photometric and electrical testing of SSL products — **TBD**
- **IES LM-80** — Approved method for lumen maintenance testing of LED light sources — **TBD**
- **IES TM-21** — Projecting long-term lumen maintenance of LED light sources — **TBD**

**Codes:**
- **CSA C22.1** (Canadian Electrical Code) — Illumination requirements (if specified) — **TBD**
- **NFPA 101** (Life Safety Code) — Emergency egress lighting requirements — **ASSUMPTION**
- **NBCC 2020** (National Building Code of Canada) — Building code lighting requirements — **TBD**

**Project-Specific:**
- **Employer's Requirements** — Project-specific illuminance levels and criteria — **TBD** *(Vol 2 Part 1, Part 2, Part 3)*

## Verification

**Verification Methods:**

**V-1: Input Data Verification**
- Verify IES photometric files are from manufacturer-certified testing per IES LM-79 — **ASSUMPTION**
- Verify site geometry matches architectural/civil drawings — **TBD**
- Verify mounting heights match design drawings (DEL-18.01) — **ASSUMPTION**
- Verify reflectance assumptions are appropriate for surface types — **ASSUMPTION**

**V-2: Methodology Verification**
- Verify calculation method is appropriate for application (point-by-point vs. lumen method) — **ASSUMPTION**
- Verify calculation grid density is adequate — **TBD**
- Verify obstructions and shading are modeled appropriately — **ASSUMPTION**
- Verify maintenance factors are justified and appropriate — **ASSUMPTION**

**V-3: Results Verification**
- Independent check of calculation results by qualified engineer — **TBD** — **ASSUMPTION**
- Verify calculated illuminance levels meet required levels — **ASSUMPTION**
- Verify uniformity ratios are acceptable — **ASSUMPTION**
- Verify fixture schedule matches design drawings — **ASSUMPTION**

**V-4: Code Compliance Verification**
- Verify illuminance levels meet ER requirements — **TBD**
- Verify illuminance levels meet IESNA recommended levels — **TBD**
- Verify emergency lighting meets NFPA 101 requirements — **ASSUMPTION**
- Verify compliance with CSA C22.1 (if illumination requirements specified) — **TBD**

**V-5: Cross-Deliverable Coordination**
- Verify coordination with DEL-18.01 (lighting drawings) — fixture types, quantities, locations consistent — **ASSUMPTION**
- Verify coordination with DEL-18.02 (specification) — fixture performance consistent — **ASSUMPTION**
- Verify coordination with DEL-18.04 (data sheets) — IES files match proposed fixtures — **ASSUMPTION**

**Acceptance Criteria:**
- All input data verified correct — **ASSUMPTION**
- Calculation methodology appropriate and documented — **ASSUMPTION**
- Calculated illuminance levels meet all requirements — **TBD**
- Uniformity ratios acceptable — **TBD**
- Independent check complete with sign-off — **TBD**
- Cross-deliverable coordination verified — **ASSUMPTION**
- Calculations approved by Electrical Discipline Lead — **TBD**

## Documentation

**Required Documentation Outputs:**

Per decomposition and _CONTEXT.md:
1. **Illumination calculations (exterior)** — Photometric calculation report for exterior lighting
2. **Illumination calculations (interior)** — Photometric calculation report for interior lighting

**Calculation Report Structure:**

**Cover Sheet:**
- Project name and location
- Deliverable ID and title
- Date and revision
- Prepared by (engineer name and P.Eng. number)
- Checked by (checker name and P.Eng. number)
- Approved by (discipline lead)
- Signatures and dates — **TBD**

**Section 1 — Design Basis:**
- Required illuminance levels per ER, IESNA, codes
- Uniformity requirements
- Design criteria and objectives
- Reference documents

**Section 2 — Input Data:**
- Fixture photometric data (IES files) — list with source/manufacturer
- Site geometry and base drawings
- Mounting heights
- Reflectance values
- Maintenance factors
- Environmental conditions

**Section 3 — Methodology:**
- Calculation method (point-by-point, lumen method)
- Software used and version
- Calculation grid layout and density
- Assumptions and limitations

**Section 4 — Results:**
- Illuminance summary tables (average, min, max, uniformity for each area)
- Illuminance contour plots overlaid on site/floor plans
- Fixture schedules
- Comparison to required levels

**Section 5 — Verification and Conclusions:**
- Verification that calculated levels meet requirements
- Code compliance demonstration
- Recommendations or notes

**Appendices:**
- Appendix A: Software output files and detailed results
- Appendix B: IES photometric data files
- Appendix C: Calculation grids and point layouts
- Appendix D: Base drawings (site plans, floor plans)

**Documentation Control:**
- Calculations managed per project document control procedures — **TBD**
- Calculation numbering per project system — **TBD**
- Revision tracking and distribution per project procedures — **TBD**

**Issuance:**
- Draft calculations to `2_Checking/To/` for review and check
- Approved calculations to `3_Issued/` — **ASSUMPTION**
- Native software files archived for future updates — **TBD**
