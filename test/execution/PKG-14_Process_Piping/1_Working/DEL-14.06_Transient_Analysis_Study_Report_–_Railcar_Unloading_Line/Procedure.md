# Procedure: DEL-14.06 Transient Analysis Study Report – Railcar Unloading Line

## Purpose

Procedure for conducting transient analysis of railcar unloading piping system to verify surge pressures within design limits (scope: Specification.md Scope; attributes: Datasheet.md Report Type; rationale: Guidance.md Purpose).

## Prerequisites

**Dependencies:** NOT_TRACKED (coordinated externally; see `_DEPENDENCIES.md`)

**Inputs Required** (interface: Specification.md Interface Requirements; rationale: Guidance.md Principles item 4; quality: Specification.md QR-1):
- Piping geometry from DEL-14.01 (P&IDs, piping GAs, isometrics — lengths, diameters, elevations) (construction: Datasheet.md Construction item 1 - Piping geometry; requirements: Specification.md FR-2; interface: Specification.md IR-1; rationale: Guidance.md Considerations - System Characteristics; quality: Specification.md QR-1; Step 1 below; verification: Specification.md Verification - Model verification; examples: Guidance.md Examples item 1; cross-reference DEL-14.01)
- Design pressure and temperature from DEL-14.03 (design calculations) (conditions: Datasheet.md Design Criteria; requirements: Specification.md FR-7; interface: Specification.md IR-2; performance: Specification.md PR-1; Step 3 below; verification: Specification.md Verification - Acceptance; cross-reference DEL-14.03)
- Pump data from PKG-15 (pump curves, motor power, inertia, coastdown characteristics) (construction: Datasheet.md Construction item 1 - Boundary conditions; requirements: Specification.md FR-4; interface: Specification.md IR-3; rationale: Guidance.md Considerations - Operational Considerations; quality: Specification.md QR-2; Step 1 below; verification: Specification.md Verification - Sensitivity analysis; examples: Guidance.md Examples item 1; cross-reference PKG-15)
- Tank data from PKG-13 (tank levels, nozzle elevations, tank pressure ratings) (construction: Datasheet.md Construction item 1 - Boundary conditions; requirements: Specification.md FR-4; interface: Specification.md IR-4; performance: Specification.md PR-2; rationale: Guidance.md Considerations - Operational Considerations; Step 1 below; verification: Specification.md Verification - Model verification; examples: Guidance.md Examples item 1; cross-reference PKG-13)
- Valve data from PKG-16 (valve sizes, types, actuation methods, typical closing times) (construction: Datasheet.md Construction items 1, 3 - Boundary conditions, Valve closing time limits; requirements: Specification.md FR-4, FR-9; interface: Specification.md IR-5, IR-6; rationale: Guidance.md Considerations - Operational Considerations; Step 1, Step 4 below; verification: Specification.md Verification - Model verification, Mitigation verification; examples: Guidance.md Examples items 1, 3; cross-reference PKG-16, DEL-14.08)
- CSD canola oil properties (density, bulk modulus, viscosity) (construction: Datasheet.md Construction item 1 - Fluid properties; requirements: Specification.md FR-3; rationale: Guidance.md Considerations - Fluid Properties; quality: Specification.md QR-1; Step 1 below; **TBD** — location TBD: ER Volume 2 Part 2 or process data)
- Operational scenarios **TBD** (normal and emergency operating procedures) (conditions: Datasheet.md Transient Scenarios; requirements: Specification.md FR-5; Step 2 below)

**Software and Tools** (attributes: Datasheet.md Analysis Software; requirements: Specification.md PR-4; standards: Specification.md Standards - Software; quality: Specification.md QR-1):
- Transient analysis software: AFT Impulse, WANDA, or equivalent **TBD** (construction: Datasheet.md Construction item 1 - Software input file; rationale: Guidance.md Principles item 4; Step 1 below; examples: Guidance.md Examples item 1)
- Software license and training for analyst (quality: Specification.md QR-4)

**Personnel** (quality: Specification.md QR-4):
- Transient analysis engineer (experience with water hammer/surge analysis and software) (quality: Specification.md QR-4; rationale: Guidance.md Principles items 1, 2, 3, 4)
- Independent reviewer (qualified piping or process engineer) (quality: Specification.md QR-4; Step 6 below; verification: Specification.md Verification - Independent review)

## Steps

### Step 1: Build Transient Model

**Objective:** Create transient analysis model of railcar unloading piping system (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1, FR-2, FR-3, FR-4; rationale: Guidance.md Principles item 4; quality: Specification.md QR-1; examples: Guidance.md Examples item 1).

**Actions:**
1. Input piping geometry from DEL-14.01 drawings:
   - Pipe segments (lengths, diameters, wall thicknesses, elevations) (construction: Datasheet.md Construction item 1 - Piping geometry; requirements: Specification.md FR-2; interface: Specification.md IR-1; rationale: Guidance.md Considerations - System Characteristics; verification: Specification.md Verification - Model verification; examples: Guidance.md Examples item 1; cross-reference DEL-14.01)
   - Fittings (elbows, tees, reducers — minor loss coefficients) (requirements: Specification.md FR-2; examples: Guidance.md Examples item 1)
   - Elevation profile (high points and low points for cavitation check) (construction: Datasheet.md Construction item 1 - Elevations; requirements: Specification.md FR-2; performance: Specification.md PR-3; rationale: Guidance.md Considerations - System Characteristics; verification: Specification.md Verification - Results validation; examples: Guidance.md Examples item 1)
2. Input fluid properties for CSD canola oil:
   - Density: **TBD** — **ASSUMPTION**: ~920 kg/m³ (construction: Datasheet.md Construction item 1 - Fluid properties; requirements: Specification.md FR-3; rationale: Guidance.md Principles item 1, Considerations - Fluid Properties; quality: Specification.md QR-1; verification: Specification.md Verification - Model verification; examples: Guidance.md Considerations - Density, Guidance.md Examples item 1)
   - Bulk modulus: **TBD** — **ASSUMPTION**: ~1,500 MPa (typical for vegetable oils) (construction: Datasheet.md Construction item 1 - Fluid properties; requirements: Specification.md FR-3; rationale: Guidance.md Considerations - Fluid Properties; examples: Guidance.md Considerations - Bulk modulus, Guidance.md Examples item 1)
   - Viscosity: **TBD** — temperature-dependent (construction: Datasheet.md Construction item 1 - Fluid properties; requirements: Specification.md FR-3; rationale: Guidance.md Considerations - Fluid Properties; examples: Guidance.md Considerations - Viscosity)
3. Define boundary conditions:
   - Pumps: Input pump curves (head vs. flow), motor power, inertia (for coastdown calculation after trip) (construction: Datasheet.md Construction item 1 - Boundary conditions; requirements: Specification.md FR-4; interface: Specification.md IR-3; rationale: Guidance.md Considerations - Operational Considerations; quality: Specification.md QR-2; verification: Specification.md Verification - Sensitivity analysis; examples: Guidance.md Examples item 1; cross-reference PKG-15)
   - Tanks: Input tank levels (normal operating level), tank pressure (atmospheric or blanketed) (construction: Datasheet.md Construction item 1 - Boundary conditions; requirements: Specification.md FR-4; interface: Specification.md IR-4; rationale: Guidance.md Considerations - Operational Considerations; verification: Specification.md Verification - Model verification; examples: Guidance.md Examples item 1; cross-reference PKG-13)
   - Valves: Input valve locations, sizes, types (gate, ball, butterfly, etc.), actuation methods (motor, pneumatic, hydraulic) (construction: Datasheet.md Construction item 1 - Boundary conditions; requirements: Specification.md FR-4; interface: Specification.md IR-5; examples: Guidance.md Examples item 1; cross-reference PKG-16)
4. Verify model completeness and accuracy (geometry check against drawings, fluid properties reasonable) (requirements: Specification.md FR-2, FR-3, FR-4; performance: Specification.md PR-5; quality: Specification.md QR-1; verification: Specification.md Verification - Model verification; verification table)

**Verification:** Model geometry matches DEL-14.01 drawings; fluid properties within expected range for canola oil (requirements: Specification.md FR-2, FR-3; performance: Specification.md PR-5; quality: Specification.md QR-1; verification: Specification.md Verification - Model verification; verification table).

---

### Step 2: Run Transient Analysis

**Objective:** Analyze transient scenarios and calculate surge pressures (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-5, FR-6; attributes: Datasheet.md Analysis Scenarios; rationale: Guidance.md Principles item 2; examples: Guidance.md Examples item 2).

**Actions:**
1. Define transient scenarios to analyze:
   - Normal pump startup (conditions: Datasheet.md Transient Scenarios; requirements: Specification.md FR-5; rationale: Guidance.md Principles item 2; examples: Guidance.md Principles item 2)
   - Normal pump shutdown (conditions: Datasheet.md Transient Scenarios; requirements: Specification.md FR-5; rationale: Guidance.md Principles item 2)
   - Pump trip / power failure (conditions: Datasheet.md Transient Scenarios; requirements: Specification.md FR-5; performance: Specification.md PR-3; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Operational Considerations; examples: Guidance.md Principles item 2)
   - Valve closing — normal and emergency rates (conditions: Datasheet.md Transient Scenarios; requirements: Specification.md FR-5; rationale: Guidance.md Principles item 2; trade-offs: Guidance.md Trade-offs item 1; examples: Guidance.md Examples item 2, Guidance.md Principles item 2)
   - Operational upsets **TBD** (conditions: Datasheet.md Transient Scenarios; requirements: Specification.md FR-5; prerequisites above)
2. Run transient simulations for each scenario using software (attributes: Datasheet.md Analysis Software; construction: Datasheet.md Construction item 1 - Software; requirements: Specification.md PR-4; standards: Specification.md Standards - Software; rationale: Guidance.md Principles item 4; verification: Specification.md Verification - Results validation)
3. Generate pressure vs. time plots at critical locations (pump discharge, high points, valve locations, tank connections) (construction: Datasheet.md Construction item 2 - Pressure vs. time plots; requirements: Specification.md FR-6; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations - System Characteristics; documentation: Specification.md Documentation - Report content; examples: Guidance.md Examples item 2)
4. Extract maximum and minimum surge pressures for each scenario and location (construction: Datasheet.md Construction item 2 - Maximum and minimum surge pressures; requirements: Specification.md FR-6; performance: Specification.md PR-1, PR-2, PR-3; quality: Specification.md QR-3; verification: Specification.md Verification - Results validation; examples: Guidance.md Examples item 2)

**Outputs:**
- Surge results for all analyzed scenarios (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-6; documentation: Specification.md Documentation - Report content; records: Records section)

---

### Step 3: Evaluate Results Against Design Limits

**Objective:** Compare surge pressures to design pressure and identify mitigation needs (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-7, FR-8; conditions: Datasheet.md Design Criteria; performance: Specification.md PR-1, PR-2, PR-3; verification: Specification.md Verification - Acceptance).

**Actions:**
1. Compare maximum surge pressures to pipe design pressure (DEL-14.03) (construction: Datasheet.md Construction item 2 - Maximum surge pressures; requirements: Specification.md FR-7; interface: Specification.md IR-2; performance: Specification.md PR-1; conditions: Datasheet.md Design Criteria; verification: Specification.md Verification - Acceptance; verification table; examples: Guidance.md Examples item 2; cross-reference DEL-14.03)
2. Compare maximum surge pressures to equipment ratings (pumps, tanks, valves) (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-7; interface: Specification.md IR-3, IR-4, IR-5; performance: Specification.md PR-2; verification: Specification.md Verification - Acceptance; verification table; cross-reference PKG-13, PKG-15, PKG-16)
3. Check minimum pressures for cavitation risk (performance: Specification.md PR-3; rationale: Guidance.md Principles item 2, Considerations - System Characteristics; verification: Specification.md Verification - Results validation; verification table; examples: Guidance.md Principles item 2)
4. Identify scenarios where surge pressures exceed acceptable limits (construction: Datasheet.md Construction item 2 - Identification; requirements: Specification.md FR-8; performance: PR-1, PR-2; quality: Specification.md QR-3; verification: Specification.md Verification - Acceptance; verification table; examples: Guidance.md Examples item 2)
5. Perform sensitivity analysis on critical parameters (valve closing time, pump inertia) (quality: Specification.md QR-2; considerations: Guidance.md Considerations - Operational Considerations; trade-offs: Guidance.md Trade-offs item 1; verification: Specification.md Verification - Sensitivity analysis; verification table)

**Outputs:**
- Surge evaluation summary identifying acceptable and unacceptable scenarios (requirements: Specification.md FR-8; verification: Specification.md Verification - Acceptance; verification table)

---

### Step 4: Develop Mitigation Recommendations

**Objective:** Recommend surge mitigation measures for scenarios exceeding limits (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-9, FR-10; rationale: Guidance.md Principles item 3; trade-offs: Guidance.md Trade-offs items 1-4; examples: Guidance.md Examples item 3).

**Actions:**
1. Evaluate mitigation options for each unacceptable scenario:
   - **Surge relief valves:** Specify location, sizing, set pressure (construction: Datasheet.md Construction item 3 - Surge relief valves; requirements: Specification.md FR-9, FR-10; rationale: Guidance.md Principles item 3; trade-offs: Guidance.md Trade-offs item 2; verification: Specification.md Verification - Mitigation verification; examples: Guidance.md Examples item 3; cross-reference PKG-16)
   - **Valve closing time limits:** Specify minimum closing time to control surge (construction: Datasheet.md Construction item 3 - Valve closing time limits; requirements: Specification.md FR-9, FR-10; interface: Specification.md IR-6; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Operational Considerations; trade-offs: Guidance.md Trade-offs item 1; verification: Specification.md Verification - Mitigation verification; examples: Guidance.md Examples item 3; cross-reference DEL-14.08, PKG-16)
   - **Accumulators or surge tanks:** Specify size, location, pressure (construction: Datasheet.md Construction item 3 - Accumulators; requirements: Specification.md FR-9; rationale: Guidance.md Principles item 3; trade-offs: Guidance.md Trade-offs item 3; examples: Guidance.md Examples item 3)
   - **Pipe design pressure increase:** Specify new design pressure and wall thickness (construction: Datasheet.md Construction item 3 - Pipe design pressure increase; requirements: Specification.md FR-9; rationale: Guidance.md Principles item 3; trade-offs: Guidance.md Trade-offs item 4; examples: Guidance.md Principles item 3; cross-reference DEL-14.01, DEL-14.03)
2. Select preferred mitigation approach based on lifecycle cost, reliability, and feasibility (source: OBJ-9; requirements: Specification.md FR-9; rationale: Guidance.md Principles item 3; trade-offs: Guidance.md Trade-offs items 1-4; examples: Guidance.md Examples item 3 - Recommendation)
3. Verify mitigation effectiveness by re-running transient analysis with proposed mitigation (requirements: Specification.md FR-9, FR-10; performance: Specification.md PR-1, PR-2; verification: Specification.md Verification - Mitigation verification; verification table)
4. Document mitigation recommendations with implementation details (equipment specifications, locations, installation requirements) (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-10; documentation: Specification.md Documentation - Report content; examples: Guidance.md Examples item 3)

**Outputs:**
- Mitigation recommendations with implementation details (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-9, FR-10; verification: Specification.md Verification - Mitigation verification; documentation: Specification.md Documentation - Report content; records: Records section)

---

### Step 5: Prepare Final Report

**Objective:** Document analysis and recommendations in final report (construction: Datasheet.md Construction item 4; quality: Specification.md QR-4; documentation: Specification.md Documentation - Report content).

**Actions:**
1. Compile report sections:
   - Executive summary (construction: Datasheet.md Construction item 4; documentation: Specification.md Documentation - Report content)
   - System description (attributes: Datasheet.md System Analyzed; conditions: Datasheet.md System Description; requirements: Specification.md FR-1; documentation: Specification.md Documentation - Report content)
   - Analysis methodology (rationale: Guidance.md Principles items 1, 2, 4; documentation: Specification.md Documentation - Report content; examples: Guidance.md Principles sections)
   - Transient model description and validation (construction: Datasheet.md Construction items 1, 4; requirements: Specification.md FR-2, FR-3, FR-4; performance: Specification.md PR-5; quality: Specification.md QR-1; verification: Specification.md Verification - Model verification; documentation: Specification.md Documentation - Report content; examples: Guidance.md Examples item 1)
   - Transient scenarios analyzed (construction: Datasheet.md Construction item 4; requirements: Specification.md FR-5; conditions: Datasheet.md Transient Scenarios; documentation: Specification.md Documentation - Report content; examples: Guidance.md Examples item 2)
   - Results (pressure plots, maximum surge pressures, comparison to limits) (construction: Datasheet.md Construction items 2, 4; requirements: Specification.md FR-6, FR-7, FR-8; performance: PR-1, PR-2, PR-3; verification: Specification.md Verification - Results validation, Acceptance; documentation: Specification.md Documentation - Report content; examples: Guidance.md Examples item 2)
   - Mitigation recommendations and implementation (construction: Datasheet.md Construction items 3, 4; requirements: Specification.md FR-9, FR-10; verification: Specification.md Verification - Mitigation verification; documentation: Specification.md Documentation - Report content; examples: Guidance.md Examples item 3)
   - Conclusions and design verification statement (construction: Datasheet.md Construction item 4; performance: Specification.md PR-1, PR-2; quality: Specification.md QR-4; verification: Specification.md Verification - Acceptance; documentation: Specification.md Documentation - Report content)
2. Format report per project standards **TBD** (quality: Specification.md QR-4; documentation: Specification.md Documentation - Format)
3. Include appendices (model input files, detailed results, calculation sheets) (documentation: Specification.md Documentation - Report content)

**Outputs:**
- Complete transient analysis report (construction: Datasheet.md Construction item 4; scope: Specification.md Scope; documentation: Specification.md Documentation section; records: Records section)

---

### Step 6: Independent Review and Approval

**Objective:** Independent verification and approval of transient analysis (quality: Specification.md QR-4; verification: Specification.md Verification - Independent review).

**Actions:**
1. Assign independent reviewer (qualified piping or process engineer with transient analysis experience) (personnel: Prerequisites; quality: Specification.md QR-4; verification: Specification.md Verification - Independent review; verification table)
2. Reviewer verifies:
   - Model inputs correct (geometry, fluid properties, boundary conditions) (requirements: Specification.md FR-2, FR-3, FR-4; performance: Specification.md PR-5; quality: Specification.md QR-1; verification: Specification.md Verification - Model verification)
   - Methodology appropriate (requirements: Specification.md FR-1; performance: Specification.md PR-4; standards: Specification.md Standards section; rationale: Guidance.md Principles items 1, 2, 4)
   - Results reasonable (surge magnitudes consistent with Joukowsky equation and physical expectations) (requirements: Specification.md FR-6; quality: Specification.md QR-3; rationale: Guidance.md Principles item 1; verification: Specification.md Verification - Results validation; examples: Guidance.md Principles item 1)
   - Mitigation measures effective and feasible (requirements: Specification.md FR-9, FR-10; verification: Specification.md Verification - Mitigation verification)
   - Conclusions supported by analysis (verification: Specification.md Verification - Acceptance)
3. Reviewer signs off or issues comments (quality: Specification.md QR-4; verification: Specification.md Verification - Independent review; verification table)
4. Address reviewer comments and update report
5. Discipline lead approves final report (quality: Specification.md QR-4; verification: Specification.md Verification - Acceptance; verification table)

**Outputs:**
- Approved transient analysis report ready for issue (verification: Specification.md Verification - Acceptance; verification table; records: Records section)

---

## Verification

**Verification activities summary:**

| Step | Verification Method | Acceptance Criteria |
|------|---------------------|---------------------|
| 1. Build Model | Geometry check, boundary condition review | Model matches drawings; fluid properties reasonable (requirements: Specification.md FR-2, FR-3, FR-4; quality: Specification.md QR-1; verification: Specification.md Verification - Model verification) |
| 2. Run Analysis | Software simulation | All scenarios analyzed; results generated (requirements: Specification.md FR-5, FR-6; verification: Specification.md Verification - Results validation) |
| 3. Evaluate Results | Comparison to design limits | Surge pressures identified; exceedances flagged (requirements: Specification.md FR-7, FR-8; performance: Specification.md PR-1, PR-2, PR-3; verification: Specification.md Verification - Acceptance) |
| 4. Develop Mitigation | Re-analysis with mitigation | Mitigation reduces surge to acceptable levels (requirements: Specification.md FR-9, FR-10; performance: Specification.md PR-1, PR-2; verification: Specification.md Verification - Mitigation verification) |
| 5. Prepare Report | Report compilation | Report complete per project standards (quality: Specification.md QR-4; documentation: Specification.md Documentation) |
| 6. Independent Review | Qualified engineer review | Reviewer sign-off; discipline lead approval (quality: Specification.md QR-4; verification: Specification.md Verification - Independent review, Acceptance) |

**Overall acceptance criteria** (verification: Specification.md Verification - Acceptance; verification table):
- All surge scenarios analyzed (requirements: Specification.md FR-5; verification table)
- Surge pressures within acceptable limits (with mitigation if required) (performance: Specification.md PR-1, PR-2; requirements: Specification.md FR-8, FR-9; conditions: Datasheet.md Design Criteria; verification table)
- Mitigation measures defined and implementable (requirements: Specification.md FR-10; verification: Specification.md Verification - Mitigation verification; verification table)
- Report complete and approved (quality: Specification.md QR-4; documentation: Specification.md Documentation; verification table)

---

## Records

**Outputs** (construction: Datasheet.md Construction section; scope: Specification.md Scope; documentation: Specification.md Documentation section):
- Transient analysis report (PDF) (construction: Datasheet.md Construction item 4; quality: Specification.md QR-4; Step 5 above)
- Transient model files (software native format) (construction: Datasheet.md Construction item 1; attributes: Datasheet.md Analysis Software; Step 1 above)
- Pressure plots and results tables (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-6; Step 2 above)
- Mitigation recommendation summary (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-9, FR-10; Step 4 above)

**Storage:** `2_Checking/` → `3_Issued/` (attributes: Datasheet.md Revision Control; documentation: Specification.md Documentation - Storage; Step 6 above)

**Format:** PDF for issued report; native software files for transient model (attributes: Datasheet.md Analysis Software; documentation: Specification.md Documentation - Format)

**Distribution:**
- Piping design team (for implementation of mitigation measures) (cross-reference DEL-14.01, DEL-14.08)
- Valve procurement (for valve closing time requirements) (interface: Specification.md IR-6; cross-reference DEL-14.08, PKG-16)
- Project file (permanent record) (attributes: Datasheet.md Retention Period; quality: Specification.md QR-4)
