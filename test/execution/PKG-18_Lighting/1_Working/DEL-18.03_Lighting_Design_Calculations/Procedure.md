# Procedure: DEL-18.03 Lighting Design Calculations

## Purpose

This procedure defines the process for producing and managing the **Lighting Design Calculations** within **PKG-18 Lighting** for the Canola Oil Transload Facility project.

**Deliverable Purpose:** Provides the engineering basis and sizing/verification calculations for lighting. *(Source: _CONTEXT.md, Decomposition DEL-18.03 description)*

**Deliverable Type:** Calculation
**Responsible Party:** D&B Contractor
**Discipline:** Electrical

**Scope of This Procedure:**
This procedure covers the process for developing photometric calculations that demonstrate lighting design compliance with ER requirements and codes.

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED
Dependencies are coordinated externally by humans per `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`.

**Typical Upstream Dependencies (to be confirmed by project coordination):**
- **Employer's Requirements** — Required illuminance levels, quality criteria — **TBD** *(Location TBD)*
- **Lighting Design Drawings (DEL-18.01)** — Preliminary fixture locations, types, mounting heights (iterative with calculations) — **ASSUMPTION**
- **Lighting Technical Specification (DEL-18.02)** — Fixture performance requirements (iterative with calculations) — **ASSUMPTION**
- **Architectural/civil base drawings (PKG-01, PKG-21, PKG-22)** — Site plans, building floor plans, ceiling heights for calculation models — **TBD**
- **Lighting Data Sheets (DEL-18.04)** — Manufacturer photometric data (IES files) for proposed fixtures — **ASSUMPTION**

**Downstream Deliverables (typical users of calculations):**
- **Lighting Design Drawings (DEL-18.01)** — Fixture layout optimized based on calculation results
- **Lighting Technical Specification (DEL-18.02)** — Performance requirements based on calculations
- **Lighting Installation & Test Records (DEL-18.05)** — Field testing compares measured illuminance to calculated values

### Reference Materials

**Required Inputs:**
- `_REFERENCES.md` — Applicable reference documents
- Package `0_References/` folder — Project reference materials
- **Employer's Requirements (Vol 2 Part 1, Part 2, Part 3)** — Illuminance requirements — **TBD** *(Location TBD)*
- **Site plans and building floor plans** — Base geometry for calculation models — **TBD**
- **Manufacturer photometric data (IES files)** — From proposed fixtures or representative fixtures — **TBD**

**Applicable Codes and Standards:**
- **IESNA Lighting Handbook** — Calculation methods, recommended illuminance levels — **TBD** *(Edition TBD)*
- **IES RP-33** (Lighting for Exterior Environments) — **TBD**
- **IES RP-1, RP-7** (Interior/industrial lighting) — **TBD** *(If applicable)*
- **IES LM-63** — IES file format standard — **ASSUMPTION**
- **NFPA 101** (Life Safety Code) — Emergency lighting requirements — **ASSUMPTION**
- **CSA C22.1** (Canadian Electrical Code) — Illumination requirements (if specified) — **TBD**

### Personnel Requirements

**Calculation Team:**
- **Lead Electrical Engineer (Lighting)** — P.Eng. licensed in British Columbia; performs or supervises calculations — **TBD**
- **Lighting Designer** — Proficient in photometric calculation software (AGi32, DIALux, etc.) — **TBD**

**Review Team:**
- **Independent Checker** — P.Eng. not involved in original calculations; verifies calculations — **TBD**

**Approval Authority:**
- **Electrical Discipline Lead** — **TBD** *(Per project organization)*

**Competency Requirements:**
- Familiarity with IESNA calculation methods and photometric software — **ASSUMPTION**
- Understanding of LED photometry and lumen maintenance — **ASSUMPTION**

### Software and Tools

**Photometric Calculation Software:**
- **TBD** — **ASSUMPTION**: AGi32, DIALux, Visual, or other IESNA-recognized software
- Software version and license — **TBD**
- Training on software use — **TBD**

## Steps

### Step 1: Define Calculation Scope and Criteria

**Objective:** Establish design basis and acceptance criteria for calculations.

**Activities:**
1. Review Employer's Requirements for required illuminance levels:
   - Exterior areas (process, roadways, parking, perimeter) — **TBD**
   - Interior areas (warehouse/process, offices, control rooms, utilities) — **TBD**
   - Emergency egress paths — **TBD**
2. Review applicable codes and standards (IESNA, CSA C22.1, NFPA 101) for minimum illuminance and uniformity requirements — **ASSUMPTION**
3. Define calculation areas:
   - Exterior lighting zones per site plan
   - Interior lighting zones per building floor plans
   - Emergency lighting zones per egress paths
4. Establish design criteria:
   - Required illuminance levels (average, minimum, uniformity) for each area — **TBD**
   - Maintenance factors based on environment and maintenance schedule — **TBD** — **ASSUMPTION**: 0.80-0.90 typical
   - Calculation grid spacing and height — **TBD** — **ASSUMPTION**: 1-3 meter grid typical
5. Document design basis in calculation report introduction — **ASSUMPTION**

**Deliverable from Step 1:**
- Design basis summary defining calculation scope, criteria, and assumptions — **ASSUMPTION**

### Step 2: Collect Input Data

**Objective:** Gather all data required for calculations.

**Activities:**

**Geometric Data:**
1. Obtain site plans and building floor plans in CAD format (DWG or DXF) for import into calculation software — **TBD**
2. Verify dimensions, orientations, and coordinate system — **ASSUMPTION**
3. Identify obstructions (buildings, tanks, equipment) that may block or reflect light — **ASSUMPTION**

**Photometric Data:**
1. Obtain IES photometric files for proposed fixtures:
   - From manufacturers of selected fixtures — **TBD**
   - Or from representative fixtures for preliminary calculations — **ASSUMPTION**
2. Verify IES files are from IES LM-79 laboratory testing — **ASSUMPTION**
3. Verify fixture lumen output, distribution type, and mounting compatibility — **ASSUMPTION**

**Fixture Layout (preliminary):**
1. Obtain preliminary fixture locations and mounting heights from lighting design drawings (DEL-18.01) or develop preliminary layout — **ASSUMPTION**
2. Coordinate fixture types with specification (DEL-18.02) — **ASSUMPTION**

**Surface Reflectances:**
1. Obtain surface finishes from architectural specifications or use typical values:
   - Exterior: pavement/concrete 15-30%, gravel 10-15% — **ASSUMPTION**
   - Interior: walls 40-60%, ceilings 70-80%, floors 20-30% — **ASSUMPTION**
2. Document reflectance assumptions in calculation report — **ASSUMPTION**

**Maintenance Factor:**
1. Determine maintenance factor based on:
   - Environment (clean, normal, dirty) — **TBD** — **ASSUMPTION**: Marine/industrial likely "dirty"
   - Fixture IP rating and cleanability
   - Expected maintenance/cleaning schedule — **TBD**
   - LED lumen maintenance (L70 hours from manufacturer data per IES LM-80/TM-21) — **TBD**
2. Document maintenance factor selection and justification — **ASSUMPTION**

**Deliverable from Step 2:**
- Compilation of all input data ready for entry into calculation software — **ASSUMPTION**

### Step 3: Build Calculation Model

**Objective:** Create photometric calculation model in software.

**Activities:**
1. Import site plans or building floor plans into calculation software as base layer — **TBD**
2. Define calculation area boundaries and grid:
   - Set calculation grid spacing (typically 1-3 meters) — **TBD** — **ASSUMPTION**
   - Set calculation height (0.0 m for exterior ground level; 0.76-0.85 m for interior work plane) — **ASSUMPTION**
   - Extend grid beyond lighted area to capture edge effects — **ASSUMPTION**
3. Model obstructions and reflecting surfaces:
   - Buildings, tanks, racks, equipment — **ASSUMPTION**
   - Assign surface reflectances to walls, ceilings, floors, ground — **ASSUMPTION**
4. Place fixtures in model:
   - Assign IES photometric files to fixture locations — **ASSUMPTION**
   - Set mounting heights, orientations, and aiming angles — **ASSUMPTION**
   - Assign fixture labels/tags matching lighting drawings (DEL-18.01) — **ASSUMPTION**
5. Apply maintenance factor to fixture outputs — **ASSUMPTION**
6. Verify model setup (fixture counts, locations, photometry) matches design intent — **ASSUMPTION**

**Deliverable from Step 3:**
- Calculation model ready for execution — **ASSUMPTION**

### Step 4: Execute Calculations

**Objective:** Run photometric calculations and generate results.

**Activities:**
1. Run point-by-point illuminance calculations for all defined areas — **ASSUMPTION**
2. Generate calculation outputs:
   - Illuminance values at each grid point — **ASSUMPTION**
   - Average, minimum, maximum illuminance for each area — **ASSUMPTION**
   - Uniformity ratios (max/min, avg/min) — **ASSUMPTION**
   - Illuminance contour plots overlaid on site/floor plans — **ASSUMPTION**
   - 3D renderings (optional) showing lighting effect — **TBD**
3. Generate fixture schedule showing fixture tags, types, quantities, locations, wattages, lumen outputs — **ASSUMPTION**
4. Save software files and outputs — **ASSUMPTION**

**Deliverable from Step 4:**
- Calculation results (illuminance tables, contour plots, fixture schedules) — **ASSUMPTION**

### Step 5: Analyze Results and Optimize

**Objective:** Verify calculated illuminance meets requirements and optimize as needed.

**Activities:**
1. Compare calculated illuminance levels to required levels:
   - Average illuminance ≥ required average — **ASSUMPTION**
   - Minimum illuminance ≥ required minimum — **ASSUMPTION**
   - Uniformity ratios ≤ maximum allowed — **ASSUMPTION**
2. Identify areas not meeting requirements:
   - Low illuminance areas (add fixtures or increase output) — **ASSUMPTION**
   - Hot spots (reduce fixtures or adjust aiming) — **ASSUMPTION**
   - Poor uniformity (adjust spacing or add fixtures) — **ASSUMPTION**
3. Optimize fixture layout:
   - Adjust fixture locations, mounting heights, aiming angles — **ASSUMPTION**
   - Change fixture types or outputs if needed — **ASSUMPTION**
   - Add or remove fixtures to achieve requirements — **ASSUMPTION**
4. Re-run calculations after adjustments — **ASSUMPTION**
5. Iterate until all areas meet requirements — **ASSUMPTION**
6. Document optimization iterations and final results — **ASSUMPTION**

**Deliverable from Step 5:**
- Optimized lighting layout meeting all requirements — **ASSUMPTION**

### Step 6: Prepare Calculation Report

**Objective:** Document calculations in formal report for review and approval.

**Activities:**
1. Prepare calculation report following structure in Specification Documentation section:
   - Cover sheet with project, deliverable ID, signatures — **ASSUMPTION**
   - Design basis and criteria
   - Input data and assumptions
   - Methodology and software
   - Results (tables, contour plots, fixture schedules)
   - Verification and compliance demonstration
   - Appendices (software outputs, IES files, base plans)
2. Include illuminance summary table comparing calculated vs. required values for all areas — **ASSUMPTION**
3. Include illuminance contour plots for all areas — **ASSUMPTION**
4. Include fixture schedule coordinated with lighting drawings (DEL-18.01) — **ASSUMPTION**
5. Prepare separate emergency lighting calculations (if not included in main calculations) demonstrating NFPA 101 compliance — **ASSUMPTION**
6. Format report per project calculation format standards — **TBD**

**Deliverable from Step 6:**
- Draft calculation report ready for check — **ASSUMPTION**

### Step 7: Independent Check

**Objective:** Independent review of calculations by qualified checker.

**Activities:**
1. Assign independent checker (P.Eng. not involved in original calculations) — **TBD**
2. Checker reviews:
   - Input data correctness (IES files, geometry, reflectances, maintenance factor) — **ASSUMPTION**
   - Methodology appropriateness (calculation method, grid, software) — **ASSUMPTION**
   - Calculation execution (spot-check results, verify software outputs) — **ASSUMPTION**
   - Results interpretation (compliance with requirements, uniformity) — **ASSUMPTION**
   - Coordination with other deliverables (DEL-18.01, DEL-18.02, DEL-18.04) — **ASSUMPTION**
3. Checker documents findings on review form or markup — **TBD**
4. Originator addresses checker comments and updates calculations/report — **ASSUMPTION**
5. Checker verifies comment resolution and provides sign-off — **TBD**

**Deliverable from Step 7:**
- Checked calculation report with sign-off — **TBD**

### Step 8: Approval and Issue

**Objective:** Obtain approval and issue calculations.

**Activities:**
1. Submit calculations to Electrical Discipline Lead for approval — **TBD**
2. Incorporate any final comments — **ASSUMPTION**
3. Finalize calculation report with approval signatures — **TBD**
4. Issue approved calculations:
   - Place PDF report in `3_Issued/` folder
   - Upload to project document management system — **TBD**
   - Distribute per distribution matrix — **TBD**
5. Archive native software files for future updates — **TBD**
6. Update deliverable status in `_STATUS.md` per project workflow (e.g., IN_PROGRESS → CHECKING → ISSUED) — **ASSUMPTION** *(Human decision)*

**Deliverable from Step 8:**
- Issued calculation report:
  - Illumination calculations (exterior)
  - Illumination calculations (interior)
- Archived software files — **TBD**

### Step 9: Revision Control (for changes after initial issue)

**Objective:** Manage calculation revisions when design changes or different fixtures are proposed.

**Activities:**
1. When changes are required (design changes, fixture substitutions, Employer requests):
   - Update calculation model with new data (IES files, fixture locations, etc.) — **ASSUMPTION**
   - Re-run calculations — **ASSUMPTION**
2. Update calculation report:
   - Revise affected sections
   - Add revision notes describing changes — **ASSUMPTION**
   - Update revision letter/number and date — **TBD**
3. Repeat Steps 7-8 (independent check, approval, issue) for revised calculations — **ASSUMPTION**
4. Issue revised calculations with new revision designation — **ASSUMPTION**
5. Maintain superseded revisions in archive per project records retention policy — **TBD**

**Deliverable from Step 9:**
- Revised calculations with revision tracking — **ASSUMPTION**

## Verification

**Verification Activities Throughout Procedure:**

**V-1: Input Data Verification (Step 2, Step 7)**
- Verify IES photometric files are manufacturer-certified per IES LM-79 — **ASSUMPTION**
- Verify site geometry matches architectural/civil drawings — **TBD**
- Verify mounting heights match design drawings (DEL-18.01) — **ASSUMPTION**
- Verify reflectance assumptions are appropriate — **ASSUMPTION**
- Verify maintenance factor is justified — **ASSUMPTION**

**V-2: Methodology Verification (Step 3, Step 7)**
- Verify calculation method (point-by-point, lumen method) is appropriate — **ASSUMPTION**
- Verify calculation grid spacing is adequate — **TBD**
- Verify obstructions are modeled where significant — **ASSUMPTION**
- Verify software is current and validated — **TBD**

**V-3: Results Verification (Step 5, Step 7)**
- Independent check of calculation results — **TBD** — **ASSUMPTION**
- Verify calculated illuminance levels meet requirements (ER, IESNA, codes) — **ASSUMPTION**
- Verify uniformity ratios are acceptable — **ASSUMPTION**
- Verify fixture schedule matches design drawings (DEL-18.01) — **ASSUMPTION**

**V-4: Code Compliance Verification (Step 5, Step 7)**
- Verify illuminance levels meet ER requirements — **TBD**
- Verify illuminance levels meet IESNA recommended levels — **TBD**
- Verify emergency lighting meets NFPA 101 requirements (10 lux avg, 1 lux min) — **ASSUMPTION**

**V-5: Cross-Deliverable Coordination (Step 7)**
- Verify coordination with DEL-18.01 (lighting drawings) — fixture types, quantities, locations consistent — **ASSUMPTION**
- Verify coordination with DEL-18.02 (specification) — fixture performance consistent — **ASSUMPTION**
- Verify coordination with DEL-18.04 (data sheets) — IES files match proposed fixtures — **ASSUMPTION**

**Sign-Off Requirements:**
- **Originator sign-off** (Step 6) — Engineer completes calculations — **TBD**
- **Checker sign-off** (Step 7) — Independent checker approves — **TBD**
- **Discipline Lead sign-off** (Step 8) — Electrical Discipline Lead approves — **TBD**

**Acceptance Criteria:**
- All input data verified correct — **ASSUMPTION**
- Calculation methodology appropriate — **ASSUMPTION**
- Calculated illuminance levels meet all requirements — **TBD**
- Uniformity ratios acceptable — **TBD**
- Independent check complete with sign-off — **TBD**
- Cross-deliverable coordination verified — **ASSUMPTION**
- Calculations approved by Electrical Discipline Lead — **TBD**

## Records

**Documentation Outputs:**

**Primary Deliverable Artifacts:**
Per decomposition and _CONTEXT.md:
1. **Illumination calculations (exterior)** — Photometric calculation report for all exterior lighting areas
2. **Illumination calculations (interior)** — Photometric calculation report for all interior lighting areas

**Supporting Documentation:**
- Design basis summary (Step 1) — **ASSUMPTION**
- Input data compilation (Step 2) — **ASSUMPTION**
- Calculation software files (native format) — **TBD**
- IES photometric data files — **TBD**
- Independent check review record (Step 7) — **TBD**
- Approval signatures and transmittals (Step 8) — **TBD**

**Record Management:**
- **Working files** stored in `1_Working/` folder during development
- **Review copies** placed in `2_Checking/To/` during review
- **Approved/issued copies** placed in `3_Issued/` folder upon approval — **ASSUMPTION**
- **Software files** archived for future updates — **TBD** *(System and location TBD)*
- **Retention requirements** per project records management plan — **TBD**
- **Superseded revisions** archived per retention policy — **TBD**

**Use of Calculations During Project Lifecycle:**

**During Design:**
- Calculations inform and verify lighting layout (DEL-18.01)
- Calculations support fixture selection and specification (DEL-18.02, DEL-18.04)
- Iterative optimization of design based on calculation results

**During Construction:**
- Calculations provide baseline for equipment procurement verification
- Calculations referenced if contractor proposes fixture substitutions (recalculation may be required)

**During Commissioning:**
- Calculations provide benchmark for field illuminance testing (DEL-18.05)
- Measured illuminance compared to calculated illuminance to verify installation correctness
- Significant deviations investigated (fixture aiming, dirt, lamp output issues)

**During Operations:**
- Calculations retained as design basis documentation
- Calculations referenced for future modifications or expansions
