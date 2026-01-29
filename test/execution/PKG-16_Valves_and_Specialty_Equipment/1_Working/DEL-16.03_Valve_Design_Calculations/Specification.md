# Specification: DEL-16.03 Valve Design Calculations

## Scope

This specification defines the requirements for producing **Valve Design Calculations** within **PKG-16 Valves & Specialty Equipment**.

**Purpose:** Provides the engineering basis and sizing/verification calculations for valves per ER requirements for the Canola Oil Transload Facility at Fraser Surrey Terminal.

**Source:** `_CONTEXT.md`

**Anticipated deliverable artifacts:**
- Control valve sizing calculations (Cv/Kv per ISA-75.01)
- Relief valve sizing calculations (per API 520/521)
- Actuator sizing calculations (per ISA-75.25)

**Source:** `_CONTEXT.md` (anticipated artifacts expanded based on typical valve calculation requirements)

**Valve Categories (per PKG-16 scope):**
- Control valves (flow, pressure, level control)
- Isolation valves (automated isolation requiring actuator sizing)
- Relief valves (pressure and thermal relief)
- Specialty items (check valves, pressure regulators, etc.)

**Source:** Decomposition document Section 5, PKG-16 scope (location TBD)

**Inclusions:**
- Control valve flow coefficient (Cv/Kv) calculations per ISA-75.01
- Control valve pressure drop, cavitation, and noise analysis
- Relief valve capacity and orifice sizing per API 520/521
- Relief valve set pressure selection and back pressure analysis
- Actuator torque/thrust calculations per ISA-75.25
- Actuator sizing and safety factor verification
- Supporting calculations (fluid properties, pressure-temperature corrections, etc.)
- Calculation basis and assumptions documentation

**Exclusions:**
- Valve arrangement and installation drawings (see DEL-16.01 Valve Design Drawing Set)
- Valve procurement specifications (see DEL-16.02 Valve Technical Specification)
- Individual valve datasheets (see DEL-16.04 Valve Data Sheet Package) — datasheets reference these calculations
- Valve installation and testing procedures (see DEL-16.05)
- Piping stress analysis (see PKG-14 Process Piping) — piping provides input data for valve sizing
- Process flow calculations (provided by process discipline) — process provides flow rates, pressures, temperatures

**Source:** Scope definition inferred from deliverable type and package structure

## Requirements

### Functional Requirements

**Calculation Package Content:**

The valve design calculations shall be organized per valve type and shall include the following (see also Procedure.md — Steps for calculation development workflow):

**1. Control Valve Sizing Calculations (per ISA-75.01):**

Calculations shall determine the required valve flow coefficient (Cv or Kv) and select appropriate valve size for each control valve application (see also Datasheet.md — Construction section for methodology details).

**Required Calculations:**
- **Flow Coefficient (Cv/Kv):** Calculate required Cv or Kv using ISA-75.01 equations for liquid flow (see Guidance.md — Principles for governing equations)
- **Valve Sizing:** Select valve size (DN or NPS) with available Cv ≥ required Cv; consider valve turndown ratio (rangeability typically 50:1)
- **Pressure Drop Analysis:** Allocate appropriate pressure drop to control valve (typically 25–50% of available system ΔP for good control authority) (see Guidance.md — Trade-offs for pressure drop allocation decisions)
- **Cavitation Check:** Calculate cavitation index (σ) and compare to valve-specific critical cavitation index (σc); select anti-cavitation trim if required
- **Flashing Check:** For fluids near saturation, verify outlet pressure exceeds vapor pressure to avoid flashing
- **Noise Level Prediction:** Calculate predicted noise level per IEC 60534-8-3; apply noise mitigation if predicted noise >85 dBA at 1 meter
- **Viscosity Correction:** Apply viscosity correction factor (Fv) for high-viscosity fluids (Reynolds number <10,000)
- **Piping Geometry Factor:** Apply piping geometry factor (Fp) to account for inlet/outlet reducers and fittings

**Input Data Required (see Procedure.md — Step 1 for input data collection):**
- Flow rates: Normal, design, minimum (from P&IDs and process design)
- Inlet pressure: Operating and design conditions (from process design)
- Outlet pressure: Operating and design conditions (from process design)
- Fluid properties: Density, viscosity, vapor pressure (from process data)
- Piping data: Inlet/outlet line size, schedule (from DEL-14.01, DEL-14.02)
- Control requirements: Turndown ratio, fail-safe mode, response time (from control philosophy)

**Calculation Outputs (see Guidance.md — Examples for typical output format):**
- Valve tag number and service description
- Required Cv or Kv (at design conditions)
- Selected valve size (DN or NPS)
- Valve body style (globe, ball, butterfly) — with justification
- Trim characteristic (equal percentage, linear, quick-opening)
- Pressure drop across valve: Normal and design conditions
- Cavitation index (σ) and assessment (acceptable / marginal / unacceptable)
- Noise level prediction (dBA at 1 meter)
- Recommended valve manufacturer/model (if specified)
- Sizing basis and key assumptions

**Source:** ISA-75.01 control valve sizing requirements; typical EPC calculation deliverable content

**2. Relief Valve Sizing Calculations (per API 520/521):**

Calculations shall determine the required relief capacity and orifice size for each pressure relief valve application (see also Datasheet.md — Construction section for methodology details).

**Required Calculations:**
- **Relief Scenario Identification:** Identify all credible overpressure scenarios per API 521 (see Guidance.md — Principles for typical scenarios):
  - Thermal expansion (blocked-in liquid between isolation valves)
  - External fire (fire case per API 521)
  - Cooling water failure or utility loss
  - Control valve failure (full-open case)
  - Blocked discharge (pump dead-heading)
  - Abnormal heat input (heat exchanger tube rupture, etc.)
- **Governing Scenario Selection:** Identify scenario requiring maximum relief capacity (see Guidance.md — Trade-offs for scenario evaluation)
- **Relief Load Calculation:** Calculate required relief mass flow or volumetric flow for governing scenario
- **Orifice Sizing:** Calculate required orifice area per API 520 equations (liquid, vapor, or two-phase flow)
- **Set Pressure Selection:** Select set pressure per ASME Section VIII rules (typically 1.05–1.1× MAWP); coordinate with pressure vessel/piping design (see Procedure.md — Step 5 IDC for coordination)
- **Overpressure Analysis:** Verify accumulated pressure during relief does not exceed code allowable (typically 1.1× MAWP for operating case, 1.21× MAWP for fire case)
- **Back Pressure Analysis:** Calculate built-up back pressure from discharge system; select conventional, balanced-bellows, or pilot-operated type
- **Discharge System Design:** Size discharge piping to limit back pressure (typically <10% set pressure for conventional PRVs, <50% for balanced-bellows)
- **Inlet Piping Loss:** Calculate inlet piping pressure loss; limit to 3% of set pressure per API 520

**Input Data Required (see Procedure.md — Step 1):**
- Protected equipment: Tag number, MAWP, volume (from P&IDs and equipment datasheets)
- Relief scenarios: From HAZOP (DEL-27.02) or process hazard analysis
- Fluid properties: Density, specific heat, vapor pressure, compressibility (from process data)
- Fire exposure: Wetted surface area for fire case (from vessel geometry)
- Discharge system: Header size, length, back pressure (from piping design)

**Calculation Outputs (see Guidance.md — Examples for typical output format):**
- Relief valve tag number and protected equipment
- Governing relief scenario (with justification)
- Required relief capacity (kg/h or SCFM)
- Set pressure (psig or barg) and overpressure allowance
- Calculated required orifice area (mm² or in²)
- Selected orifice designation (API 526 standard orifice: D, E, F, G, H, J, K, L, M, N, P, Q, R, T)
- Relief valve type (conventional, balanced-bellows, pilot-operated)
- Inlet/outlet connection size (NPS or DN)
- Calculated back pressure (%) and PRV type selection justification
- Discharge piping requirements (size, routing to safe location per DEL-16.01)
- Inlet piping loss calculation and acceptability check
- Applicable code (ASME Section VIII, ASME B31.3, CSA B51)

**Source:** API 520/521 relief valve sizing requirements; typical EPC calculation deliverable content

**3. Actuator Sizing Calculations (per ISA-75.25):**

Calculations shall determine the required actuator torque/thrust and select appropriate actuator size for each automated valve application (see also Datasheet.md — Construction section for methodology details).

**Required Calculations:**
- **Torque/Thrust Calculation:** Calculate required valve torque (quarter-turn valves: ball, butterfly) or thrust (linear valves: gate, globe):
  - Breakaway torque/thrust (to overcome static friction and unseating force at maximum differential pressure)
  - Running torque/thrust (to move valve during operation)
  - Seating torque/thrust (to achieve tight shutoff per leakage class)
- **Actuator Sizing:** Select actuator with output torque/thrust ≥ maximum calculated torque/thrust × safety factor (see Guidance.md — Trade-offs for safety factor selection)
- **Safety Factor Verification:** Verify safety factor ≥ 1.5 for pneumatic actuators, ≥ 1.25 for electric actuators (or per manufacturer recommendation)
- **Fail-Safe Verification:** For spring-return pneumatic actuators, verify spring can close/open valve on loss of air supply (see Guidance.md — Principles for fail-safe mode selection)
- **Stroking Time Calculation:** Calculate valve stroking time based on actuator spring rate and air supply; verify meets control/safety requirements
- **Air Consumption Calculation:** For pneumatic actuators, calculate air volume per stroke (for sizing air receiver and compressor capacity)
- **Manual Override Verification:** For automated valves with manual override, verify handwheel torque is within operator capability (<60 Nm typical)

**Input Data Required (see Procedure.md — Step 1):**
- Valve data: Tag number, size, type, pressure class, seat material (from DEL-16.04 datasheets)
- Operating conditions: Maximum differential pressure, temperature (from process design)
- Actuator type: Pneumatic (spring-return or double-acting), electric, hydraulic (from P&ID or control philosophy)
- Fail-safe mode: Fail-closed (FC), fail-open (FO), fail-as-is (FL) (from HAZOP recommendations or control philosophy)
- Air supply pressure: Typically 5–7 barg for pneumatic actuators (from utility design basis)
- Performance requirements: Stroking time, control accuracy (from control requirements)

**Calculation Outputs (see Guidance.md — Examples):**
- Valve tag number and service description
- Calculated breakaway torque/thrust (Nm or kN)
- Calculated running torque/thrust (Nm or kN)
- Calculated seating torque/thrust (Nm or kN)
- Selected actuator size and model
- Actuator output torque/thrust at rated air/power supply (Nm or kN)
- Safety factor achieved (actual / required)
- Stroking time (seconds to full open or full closed)
- Air consumption per stroke (liters or SCFM) for pneumatic actuators
- Manual override capability (yes/no; handwheel torque if applicable)
- Fail-safe mode verification (spring can close/open valve: yes/no)

**Source:** ISA-75.25 actuator sizing requirements; typical EPC calculation deliverable content

**Calculation Format and Structure:**

All calculations shall be presented in a clear, structured format (see Procedure.md — Step 3 for calculation execution requirements):

1. **Cover Sheet:** Calculation number, title, revision, originator, checker, approver, date
2. **Table of Contents:** For multi-page calculations
3. **Purpose and Scope:** Brief description of calculation objective
4. **Design Basis:** List of applicable codes, standards, and reference documents
5. **Input Data:** Tabulated input data with sources (P&ID, process data, vendor data, etc.)
6. **Assumptions:** Clearly state all engineering assumptions; flag items requiring confirmation (TBD)
7. **Calculations:** Step-by-step calculations with equations, units, and intermediate results
8. **Results Summary:** Tabulated results with acceptance criteria and pass/fail assessment
9. **Conclusions and Recommendations:** Key findings and design recommendations
10. **References:** List of reference documents and data sources
11. **Appendices:** Supporting data (fluid property tables, vendor catalog data, software output, etc.)

**Source:** Typical engineering calculation format; specific format TBD per project calculation standards

### Performance Requirements

**Calculation Accuracy and Conservatism:**

1. **Design Margin:** Calculations shall include appropriate design margins:
   - Control valve Cv: Select valve size with available Cv ≥ 1.1× required Cv (10% margin)
   - Relief valve capacity: Size for 110% of calculated relief load (or per ASME overpressure rules)
   - Actuator sizing: Safety factor ≥ 1.5 for pneumatic, ≥ 1.25 for electric
   - **TBD** — Project-specific design margins to be confirmed

2. **Calculation Precision:** Numerical precision appropriate to engineering accuracy:
   - Flow rates: 2 significant figures minimum
   - Pressures: 3 significant figures
   - Cv/Kv values: 2 decimal places
   - Dimensions: Per code requirements (typically 0.1 mm or 0.01")
   - **Source:** Engineering judgment; precision appropriate to input data accuracy

3. **Units Consistency:** All calculations shall use consistent units throughout; clearly indicate unit system (SI or Imperial)
   - **Preferred:** SI units (metric) for consistency with Canadian codes
   - **Acceptable:** Imperial units if required by project standards or vendor data
   - **Required:** Unit conversion factors clearly shown when converting between unit systems
   - **Source:** Canadian project location suggests SI units; TBD per project standards

**Design Code Compliance:**

1. **Control Valve Sizing:** Shall comply with ISA-75.01 (IEC 60534-2-1) equations and methodology
   - Liquid flow equations (non-choked, choked)
   - Cavitation and flashing criteria per IEC 60534-8-4
   - Noise prediction per IEC 60534-8-3
   - **Source:** ISA-75 series standards

2. **Relief Valve Sizing:** Shall comply with applicable code for protected equipment:
   - ASME Section VIII Division 1 (for ASME pressure vessels)
   - ASME B31.3 (for process piping systems)
   - CSA B51 (Canadian regulatory requirements)
   - API 520/521 methodology (widely accepted design practice)
   - **Source:** Applicable pressure equipment codes; CSA B51 mandatory in BC jurisdiction

3. **Actuator Sizing:** Shall comply with ISA-75.25 or manufacturer's sizing methodology
   - Use manufacturer torque data where available (preferred for accuracy)
   - Use generic equations (per ISA-75.25 or VDI/VDE 3845) if manufacturer data not available
   - **Source:** ISA-75.25 standard; manufacturer data preferred

**Sensitivity and Uncertainty:**

1. **Sensitivity Analysis:** For critical valves, perform sensitivity analysis to assess impact of input data uncertainty (see Guidance.md — Trade-offs for sensitivity analysis recommendations):
   - Vary flow rate ±20% and verify valve still acceptable
   - Vary differential pressure ±10% and verify performance
   - Assess impact of viscosity variation with temperature
   - **TBD** — Sensitivity analysis requirements per project risk management

2. **Uncertainty Documentation:** Clearly document sources of uncertainty and conservative assumptions:
   - Flag input data marked as "TBD" or "estimated"
   - State assumptions requiring confirmation during detailed design or commissioning
   - Provide recommendations for confirming assumptions (field measurements, vendor data, testing)
   - **Source:** Engineering judgment; uncertainty management per project risk procedures

### Interface Requirements

**Multi-Discipline Coordination:**

The valve design calculations shall be coordinated with the following disciplines/deliverables (see also Procedure.md — Step 5 IDC for coordination process):

1. **Process (PKG-10, PKG-11, PKG-12, PKG-13):**
   - Process design (P&IDs, PFDs) provides flow rates, pressures, temperatures (see Datasheet.md — Conditions for process parameters)
   - Valve sizing calculations verify process design assumptions (pressure drops, relief capacities)
   - Feedback loop: If calculated pressure drop excessive, request process to revise allocation

2. **Mechanical Piping (PKG-14):**
   - Piping design (DEL-14.01, DEL-14.02) provides line sizes, pressure classes, piping layout
   - Valve sizing provides pressure drop data for piping stress analysis and pump head calculations
   - Relief valve discharge piping designed to limit back pressure per calculations

3. **Instrumentation (PKG-20):**
   - Control valve calculations inform instrumentation requirements (positioner range, control signal type)
   - Flow measurement sizing (meters in DEL-12.04) may inform control valve sizing (if valve used for flow control)

4. **Control Systems (PKG-19):**
   - Control philosophy defines fail-safe modes for control valves
   - Control valve stroking time calculations inform control loop tuning
   - ESD logic defines closure time requirements for shutdown valves

5. **Pressure Vessels (PKG-13 Storage Tanks, others):**
   - Vessel MAWP defines relief valve set pressure
   - Vessel geometry provides fire exposure area for relief valve fire case
   - Relief valve sizing may influence vessel MAWP selection (trade-off between vessel thickness and relief valve size)

6. **Safety (DEL-27.02 HAZOP):**
   - HAZOP identifies relief valve scenarios and recommends fail-safe modes
   - Valve calculations verify HAZOP recommendations are adequate
   - If HAZOP scenario results in excessive relief capacity, recommend design changes to mitigate scenario

**Source:** Interface requirements inferred from multi-discipline nature of valve calculations; formal dependencies NOT_TRACKED per `_DEPENDENCIES.md`

**Vendor Coordination:**

- Valve sizing calculations based on generic methods (ISA, API) or vendor-specific data if available
- After valve procurement, verify vendor-supplied data (actual Cv, torque factors) matches calculation assumptions
- If significant discrepancy, revise calculations or request vendor to modify design
- **TBD** — Vendor data incorporation process per project procurement procedures

**Source:** Typical EPC vendor coordination process

### Quality Requirements

**Calculation Quality:**

1. **Completeness:** All calculations shall include:
   - Clear statement of purpose and scope
   - Complete input data with sources
   - All assumptions explicitly stated
   - Step-by-step calculations (or software input/output if using software)
   - Results summary with acceptance criteria
   - Conclusions and recommendations
   - **Source:** Typical engineering calculation requirements

2. **Traceability:** All input data shall be traceable to source:
   - P&IDs (document number, revision, sheet number)
   - Process datasheets or simulations (document number, case ID)
   - Vendor data (vendor, document number, date)
   - Codes and standards (edition/revision)
   - **Source:** Quality management traceability requirements

3. **Reproducibility:** Calculations shall be sufficiently detailed that an independent engineer can reproduce results:
   - All equations and constants clearly shown
   - Software input files included (if using software)
   - Sufficient intermediate steps shown (not just final result)
   - **Source:** Independent check requirements

4. **Clarity:** Calculations shall be clear and well-organized:
   - Consistent notation and symbols throughout
   - Units indicated for all numerical values
   - Tables and figures clearly labeled
   - Cross-references to other calculations or documents where applicable
   - **Source:** Document quality standards

**Checking and Approval:**

1. **Self-Check:** Originator shall perform self-check prior to submitting for independent check (see Procedure.md — Step 4 for self-check process)
2. **Independent Check:** Qualified checker (not the originator) shall perform independent check calculation (see Specification — Verification section for check methods)
3. **Approval:** Discipline lead (P.Eng.) shall review and approve calculations (see Procedure.md — Step 6 for approval process)

**Sign-Off Requirements:**
- All calculations shall bear original signatures (or electronic approval) of originator, checker, and approver
- Sign-off dates shall be indicated
- Checker shall document check method (hand calculation, independent software run, detailed review of originator's work)
- **TBD** — Sign-off protocol per project quality procedures and authority matrix

**Software Validation:**

If calculation software is used (Excel, MathCAD, vendor software):
- Software shall be validated for intended use (software validation plan) — **TBD**
- Software version shall be documented in calculation
- Software input and output files shall be included as calculation appendices
- Hand calculation or benchmark comparison required for first use or significant software revision
- **TBD** — Software validation requirements per project quality procedures

**Source:** Typical software validation requirements for engineering calculations

## Standards

**Applicable codes and standards:**

**Control Valve Sizing:**
- IEC 60534 / ISA-75 series — Industrial-Process Control Valves
  - ISA-75.01 (IEC 60534-2-1) — Control Valve Sizing Equations
  - ISA-75.11 (IEC 60534-2-3) — Inherent Flow Characteristic and Rangeability
  - IEC 60534-8-3 — Noise Prediction Method
  - IEC 60534-8-4 — Prediction of Cavitation

**Relief Valve Sizing:**
- ASME BPVC Section VIII Division 1 — Pressure Vessels (relief valve requirements)
- API 520 — Sizing, Selection, and Installation of Pressure-Relieving Devices (Part I — Sizing and Selection)
- API 521 — Pressure-Relieving and Depressuring Systems (relief scenarios and fire case)
- ISO 4126 — Safety Devices for Protection Against Excessive Pressure (alternative to API)

**Actuator Sizing:**
- ISA-75.25 — Test Procedure for Control Valve Actuators
- VDI/VDE 3845 — Control Valves (German standard for actuator sizing; widely used internationally)

**Piping and Pressure Systems:**
- ASME B31.3 — Process Piping (pressure-temperature ratings, allowable stresses)
- CSA B51 — Boiler, Pressure Vessel and Pressure Piping Code (Canadian regulatory requirements for relief devices)

**Fluid Properties:**
- ASME Steam Tables — Thermodynamic properties of water and steam (if applicable)
- NIST Chemistry WebBook — Thermophysical properties of fluids
- Industry data — Canola oil properties (viscosity-temperature curves, density, specific heat)

**Project-Specific:**
- Employer's Requirements — **TBD** — **ASSUMPTION**: Volume 2 Parts 1–3 contain valve sizing criteria and acceptance requirements
- Project Engineering Standards — **TBD** — Project-specific calculation format, margins, and sign-off requirements
- Project Quality Management Plan — **TBD** — Calculation checking and approval procedures

**Source:** Standards inferred from valve sizing scope; applicability to be confirmed during calculation development

## Verification

**Verification methods for Calculation deliverables:**

### 1. Self-Check (Originator)

Originator shall perform self-check prior to submitting for independent check (see Procedure.md — Step 4 for self-check process):
- Verify all input data is correct and from approved sources
- Check all equations and units for consistency
- Verify all calculations are arithmetically correct
- Check results against engineering judgment (order-of-magnitude check)
- Verify conclusions and recommendations are supported by calculations

### 2. Independent Check Calculation

Qualified checker (not the originator) shall perform independent check using one of the following methods (see Procedure.md — Step 5 for check process):

**Method A: Full Independent Calculation (preferred for critical valves):**
- Checker performs independent calculation using same methodology and input data
- Compare checker's results to originator's results; investigate any discrepancies >5%
- Document check method and comparison results in checker's notes

**Method B: Detailed Review with Spot-Check Calculations:**
- Checker reviews originator's calculation for completeness, methodology, and input data
- Checker performs spot-check calculations (10–20% of calculation steps) to verify arithmetic accuracy
- Checker verifies critical results using alternative method or hand calculation
- Document review findings and spot-check results

**Method C: Software Output Verification (for software-based calculations):**
- Checker reviews software input data for correctness
- Checker verifies software output is reasonable (order-of-magnitude check)
- Checker performs benchmark calculation using alternative method (hand calculation or different software)
- Checker verifies software version is validated for intended use

**Critical Valves Requiring Method A (full independent check):**
- All relief valves (safety-critical)
- ESD (emergency shutdown) valves
- Control valves >NPS 8 (large, expensive)
- Valves identified as safety-critical in HAZOP (DEL-27.02)
- **TBD** — Critical valve criteria per project risk assessment

**Source:** Typical independent check methods for engineering calculations; Method A preferred for safety-critical equipment

### 3. Design Code Compliance Check

Checker shall verify calculations comply with applicable design codes:
- Control valve sizing: Verify ISA-75.01 equations used correctly
- Relief valve sizing: Verify API 520/521 methodology applied correctly; verify compliance with ASME Section VIII or B31.3 rules
- Actuator sizing: Verify torque/thrust factors from manufacturer or ISA-75.25
- **Source:** Code compliance verification per project quality procedures

### 4. Sensitivity Analysis Review (for critical valves)

For valves identified as critical, checker shall review sensitivity of results to input data uncertainty:
- Verify appropriate design margins applied
- Assess impact of conservative assumptions
- Recommend confirmation of uncertain input data (vendor data, field measurements, testing)
- **TBD** — Sensitivity analysis requirements per project risk management

### 5. Interdisciplinary Check (IDC) (see Procedure.md — Step 5)

Coordinate calculations with other disciplines to verify interface assumptions:
- Process: Verify flow rates, pressures, temperatures are consistent with process design
- Piping: Verify line sizes, pressure classes, piping geometry factors
- Instrumentation: Verify control valve rangeability meets control requirements
- Safety: Verify relief valve scenarios consistent with HAZOP recommendations

**Acceptance Criteria:**

Calculations are acceptable for approval when:
- Self-check complete; originator confirms readiness for independent check
- Independent check complete; checker confirms calculations are correct (or comments resolved)
- Design code compliance verified
- Sensitivity analysis performed for critical valves (if required)
- IDC comments resolved (Category A comments mandatory; Category B incorporated where practicable)
- All TBDs identified and flagged for resolution during detailed design
- Originator, checker, and approver sign-offs obtained per project authority matrix — **TBD**

**Source:** Typical calculation acceptance criteria; specific criteria TBD per project quality procedures

## Documentation

**Required documentation outputs:**

### Primary Deliverables (per _CONTEXT.md)
- **Control Valve Sizing Calculations:** Sizing calculations for all control valves (flow, pressure, level control applications)
- **Relief Valve Sizing Calculations:** Sizing calculations for all pressure relief valves and thermal relief valves
- **Actuator Sizing Calculations:** Sizing calculations for all pneumatic and electric actuators (typically integrated into control valve sizing calculations)

**Format:** **TBD** — **ASSUMPTION**: PDF calculation packages with supporting Excel/MathCAD files or vendor software output files

### Supporting Documentation
- **Calculation Register/Index:** List of all valve sizing calculations with document numbers, titles, valve tags, and revision status
- **Input Data Summary:** Consolidated summary of key input data (flow rates, pressures, fluid properties) with sources
- **Assumptions Log:** Consolidated list of engineering assumptions and TBD items requiring confirmation
- **Software Validation Records:** Software validation documentation (if software used) — **TBD**
- **Checker's Notes:** Independent check documentation (comparison results, spot-check calculations, review comments)
- **IDC Comment/Response Log:** Record of interdisciplinary comments and resolutions

**Documentation Requirements:**

**Document Control:**
- All documents shall comply with project document control procedures
- Document numbering per project calculation numbering system — **TBD**
  - **ASSUMPTION**: Format "CALC-PKG16-DEL03-###" where ### = sequential number
- Revision control: Initial issue Rev 0 or A; subsequent revisions per project convention — **TBD**
- Distribution list: **TBD** — Engineering disciplines, project management, QA/QC

**Format:**
- **TBD** — **ASSUMPTION**: PDF for issued calculations; native files (Excel, MathCAD, etc.) for working calculations
- Page size: **TBD** — Letter (8.5" × 11") or A4
- Header/footer: Project title, calculation number, revision, page number, originator, checker, approver
- Cover sheet: Calculation title, purpose, revision history, sign-off table

**Submittal Requirements:**
- 30% Design submittal — **TBD** — Preliminary sizing calculations for representative valves
- 60% Design submittal — **TBD** — Revised calculations incorporating process design updates
- 90% Design submittal — **TBD** — Near-final calculations for all valves
- IFC (Issued for Construction) — **TBD** — Final calculations with all checks complete

**Source:** Submittal milestones inferred from decomposition Section 5, PKG-27, DEL-27.04 (Design Submission Packages); specific requirements TBD

**Records Retention:**
- Retention period: **TBD** — **ASSUMPTION**: Project life + 25 years typical for design calculations (permanent record)
- Archival format: **TBD** — **ASSUMPTION**: PDF/A for long-term preservation; retain native files for future revisions
- Backup and disaster recovery: **TBD** — Per project IT/document management procedures

**Source:** Records retention typical for EPC projects; specific requirements TBD per project procedures
