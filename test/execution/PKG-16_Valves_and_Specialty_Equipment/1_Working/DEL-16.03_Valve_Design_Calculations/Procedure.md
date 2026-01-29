# Procedure: DEL-16.03 Valve Design Calculations

## Purpose

This procedure defines the process for producing and managing **Valve Design Calculations** within **PKG-16 Valves & Specialty Equipment**.

**Deliverable Purpose:** Provides the engineering basis and sizing/verification calculations for valves per ER requirements for the Canola Oil Transload Facility.

**Source:** `_CONTEXT.md`

**Deliverable Type:** Calculation
**Responsible Party:** D&B Contractor
**Discipline:** Mechanical

**Scope:** This procedure covers the development of valve sizing calculations from initial input data collection through independent check and approval, for three valve categories: control valves, relief valves, and actuators.

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED
- Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)
- Upstream deliverables and input data to be confirmed prior to commencement

**Source:** `_DEPENDENCIES.md`

**Typical Upstream Inputs (advisory only — not formally tracked):**

**For Control Valve Sizing:**
- Process design (P&IDs, PFDs) — valve service, tag numbers, normal/design/minimum flow rates
- Process datasheets or simulation — fluid properties (density, viscosity, vapor pressure), operating temperatures and pressures
- Piping design (DEL-14.01 line list, DEL-14.02 piping specification) — line sizes, pressure classes, piping material
- Control philosophy document — control valve turndown requirements, fail-safe modes, response time requirements

**For Relief Valve Sizing:**
- P&IDs — protected equipment, relief valve locations and tag numbers
- Equipment datasheets (pressure vessels, heat exchangers, tanks) — MAWP, design pressure, volume, geometry
- HAZOP study (DEL-27.02) — identified relief scenarios and recommendations
- Process hazard analysis — credible overpressure scenarios (thermal expansion, fire case, blocked discharge, etc.)
- Piping design — relief valve discharge piping layout and sizing

**For Actuator Sizing:**
- Valve datasheets (DEL-16.04) — valve size, type, pressure class, seat material, differential pressure
- P&IDs or control philosophy — actuator type (pneumatic, electric), fail-safe mode (FC, FO, FL)
- Utility design basis — compressed air supply pressure (typically 5–7 barg for pneumatic actuators)
- Control requirements — valve stroking time requirements (for control performance or safety shutdown)

**Source:** Inputs inferred from valve calculation requirements; specific coordination TBD

### Reference Materials

**Required References:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials

**Key References (to be obtained):**
- Employer's Requirements (Volume 2 Parts 1–3) — **TBD** — valve sizing criteria, design margins, acceptance requirements
- Project Engineering Standards — **TBD** — calculation format, sign-off requirements, software validation requirements
- Applicable codes and standards (see Specification.md, Section "Standards")
  - ISA-75.01 (Control Valve Sizing Equations)
  - API 520 (Relief Valve Sizing, Part I)
  - API 521 (Relief Scenarios and Fire Case)
  - ISA-75.25 (Actuator Sizing)
  - ASME Section VIII (Pressure Vessel Relief Requirements)
  - CSA B51 (Canadian Pressure Equipment Code)

**Source:** Reference requirements inferred from deliverable type; `_REFERENCES.md` indicates no references identified yet

**Vendor Data (as available):**
- Valve manufacturer catalogs (Cv tables, torque curves, dimensional data)
- Actuator manufacturer catalogs (output torque/thrust tables, air consumption data)
- Relief valve manufacturer catalogs (orifice areas, capacity certification data)

**Note:** Vendor data typically available after valve procurement; preliminary sizing uses generic data or vendor-neutral sizing methods.

**Fluid Property Data:**
- Canola oil properties (density, viscosity-temperature curve, specific heat, vapor pressure) — **TBD** — from process design basis or industry data
- NIST Chemistry WebBook or similar database (for thermophysical property lookup)
- Viscosity conversion tools (kinematic ↔ absolute viscosity)

### Personnel Requirements

**Qualifications:**
- **Design Engineer (Originator):** Mechanical engineer with experience in valve sizing for process facilities; familiarity with ISA-75, API 520/521, and actuator sizing
- **Checker:** Senior mechanical engineer (not the originator), qualified to perform independent check calculations; understanding of valve sizing codes and standards
- **Discipline Lead (Approver):** Professional Engineer (P.Eng.) authorized to approve mechanical calculations per project authority matrix

**Source:** Typical personnel requirements for mechanical calculations; specific qualifications TBD per project quality procedures

**Competency Requirements:**
- Familiarity with ISA-75.01 control valve sizing equations and methodology
- Understanding of API 520/521 relief valve sizing and scenario evaluation
- Knowledge of actuator types (pneumatic, electric) and sizing methods
- Proficiency in calculation software (Excel, MathCAD, or specialized valve sizing software)
- **ASSUMPTION:** Personnel competency per project quality procedures

## Steps

### Step 1: Input Data Collection

**Action:** Collect and verify all input data required for valve sizing calculations.

**Input Data Checklist:**

**Control Valve Sizing Inputs:**
- Valve tag number and service description (from P&ID)
- Flow rates: Normal, design, minimum (from process design)
  - **Units:** m³/h (SI) or gpm (Imperial) — confirm unit system with project
- Inlet pressure: Operating and design conditions (from process design)
  - **Units:** barg (SI) or psig (Imperial)
- Outlet pressure: Operating and design conditions (from process design)
- Differential pressure across valve: Calculated or specified
- Fluid properties (from process data):
  - Density (kg/m³ or lb/ft³)
  - Kinematic viscosity (cSt or SSU) — **critical for canola oil sizing**
  - Vapor pressure (kPa or psia)
  - Temperature (°C or °F)
- Piping data (from DEL-14.01, DEL-14.02):
  - Inlet line size (DN or NPS)
  - Outlet line size (DN or NPS)
  - Piping schedule (wall thickness)
  - Flange rating (Class 150, 300, etc.)
- Control requirements (from control philosophy):
  - Required turndown ratio (rangeability)
  - Fail-safe mode (FC, FO, FL)
  - Stroking time requirement (if specified)

**Relief Valve Sizing Inputs:**
- Relief valve tag number and protected equipment (from P&ID)
- Protected equipment data (from equipment datasheets):
  - MAWP (Maximum Allowable Working Pressure)
  - Design pressure and temperature
  - Volume (for thermal expansion scenario)
  - Geometry (diameter, height for fire case scenario)
- Relief scenarios (from HAZOP or process hazard analysis):
  - Thermal expansion (blocked-in line)
  - External fire (fire case per API 521)
  - Cooling water failure or utility loss
  - Control valve failure (full-open case)
  - Blocked discharge (pump dead-heading)
  - **Action:** Evaluate all credible scenarios; identify governing scenario
- Fluid properties (from process data):
  - Density (kg/m³ or lb/ft³)
  - Specific heat (kJ/kg·K or BTU/lb·°F) — for fire case
  - Latent heat of vaporization (kJ/kg or BTU/lb) — for fire case
  - Vapor pressure and compressibility (for vapor/two-phase relief)
- Discharge system data (from piping design):
  - Discharge piping size, length, routing
  - Back pressure (from discharge header or atmospheric discharge)
- Set pressure basis: Typically 0.95–1.0× MAWP (to be confirmed with pressure vessel/piping design)

**Actuator Sizing Inputs:**
- Valve data (from DEL-16.04 datasheets or preliminary valve selection):
  - Valve tag number and type (ball, butterfly, gate, globe)
  - Valve size (DN or NPS)
  - Pressure class (ANSI 150, 300, etc.)
  - Maximum differential pressure (design condition)
  - Seat material (soft-seated or metal-seated)
- Actuator requirements (from P&ID or control philosophy):
  - Actuator type: Pneumatic (spring-return or double-acting), electric, manual
  - Fail-safe mode: FC (fail-closed), FO (fail-open), FL (fail-as-is)
  - Stroking time requirement (seconds to full stroke)
- Utility data (from utility design basis):
  - Compressed air supply pressure (typically 5–7 barg for pneumatic actuators)
  - Electric power supply (voltage, phase, frequency for electric actuators)
- Manufacturer data (if available):
  - Valve torque curves or torque factors (from valve manufacturer)
  - Actuator output torque/thrust tables (from actuator manufacturer)

**Data Verification:**
- Confirm all input data is from approved sources (issued-for-design P&IDs, approved process datasheets, etc.)
- Check for consistency (e.g., valve line size matches piping line list)
- Identify any "TBD" or "estimated" data; flag for confirmation during detailed design
- Document data sources (P&ID number/revision, datasheet number, vendor document number, etc.)

**Source:** Typical input data requirements for valve sizing calculations

### Step 2: Methodology Selection and Design Basis

**Action:** Select appropriate calculation methodology and establish design basis for valve sizing.

**Methodology Selection:**

**Control Valve Sizing:**
- **Method:** ISA-75.01 (IEC 60534-2-1) sizing equations for liquid flow (see Guidance.md — Principles for governing equations)
- **Software:** **TBD** — Vendor sizing software (Fisher, Emerson) or generic spreadsheet per ISA-75.01
  - If using vendor software: Document software name, version, and validation status
  - If using generic spreadsheet: Document spreadsheet file name, version, and validation/benchmark status
- **Design Basis:**
  - Size valve for design flow rate (typically 1.2× normal flow rate)
  - Allocate 25–50% of available system pressure drop to control valve (see Guidance.md — Trade-offs for pressure drop allocation)
  - Select valve size with available Cv ≥ 1.1× required Cv (10% margin)
  - Verify turndown ratio ≥ required rangeability (typically 50:1 for control valves)
  - Check cavitation index and apply anti-cavitation trim if required
  - Predict noise level and apply noise mitigation if >85 dBA at 1 meter

**Relief Valve Sizing:**
- **Method:** API 520 sizing equations (liquid, vapor, or two-phase) with scenarios per API 521 (see Guidance.md — Principles for relief scenarios)
- **Software:** **TBD** — API 520 sizing software (Emerson PRV2SIZE, Spirax Sarco ReliefSIZE, etc.) or generic spreadsheet
- **Design Basis:**
  - Identify all credible relief scenarios per API 521
  - Calculate required relief capacity for each scenario
  - Select governing scenario (maximum relief capacity)
  - Size orifice per API 520 equations with 10% margin (or per code overpressure allowance)
  - Select API 526 standard orifice designation (D, E, F, G, H, J, K, L, M, N, P, Q, R, T)
  - Verify accumulated pressure during relief ≤ 1.1× MAWP (operating case) or ≤ 1.21× MAWP (fire case)
  - Calculate back pressure from discharge system; select valve type (conventional, balanced-bellows, pilot-operated)
  - Verify inlet piping loss <3% of set pressure

**Actuator Sizing:**
- **Method:** ISA-75.25 or manufacturer-specific sizing methodology (see Guidance.md — Principles for torque calculation)
- **Software:** **TBD** — Manufacturer sizing tools or generic spreadsheet
- **Design Basis:**
  - Calculate breakaway, running, and seating torque/thrust (use manufacturer torque curves if available; generic equations if not)
  - Select actuator with output torque/thrust ≥ max calculated torque/thrust × safety factor
  - Safety factor: 1.5 for pneumatic actuators, 1.25 for electric actuators (or per manufacturer recommendation)
  - For spring-return actuators: Verify spring can close/open valve on loss of air supply (fail-safe verification)
  - Calculate stroking time and verify meets control/safety requirements
  - Calculate air consumption per stroke (for pneumatic actuators)

**Design Code and Standards:**
- Document applicable codes and standards in calculation (see Specification.md — Standards section)
- Specify edition/revision of each code (e.g., "API 520 Part I, 9th Edition, 2014")
- In case of conflict between codes, establish precedence (typically: Employer's Requirements > mandatory codes > industry standards > manufacturer recommendations)

**Source:** Methodology selection per applicable codes and industry best practices

### Step 3: Calculation Execution

**Action:** Perform valve sizing calculations per selected methodology.

**Calculation Format:**

All calculations shall be presented in structured format (see Specification.md — Functional Requirements for calculation structure):

1. **Cover Sheet:** Calculation number, title, project name, revision, originator, checker, approver, dates
2. **Table of Contents:** For multi-page calculations (>5 pages)
3. **Purpose and Scope:** Brief description of calculation objective (e.g., "Control valve sizing for product transfer line FV-1234")
4. **Design Basis:** List applicable codes, standards, reference documents, and key design criteria
5. **Input Data:** Tabulated input data with sources (P&ID rev., datasheet number, vendor document, etc.)
6. **Assumptions:** Clearly state all engineering assumptions; flag items requiring confirmation (TBD)
7. **Calculations:** Step-by-step calculations with equations, units, intermediate results, and final results
8. **Results Summary:** Tabulated results with acceptance criteria and pass/fail assessment
9. **Conclusions and Recommendations:** Key findings, design recommendations, and any follow-up actions required
10. **References:** List of reference documents, data sources, and vendor catalogs
11. **Appendices:** Supporting data (fluid property tables, vendor catalog excerpts, software input/output files, etc.)

**Control Valve Sizing Calculation Steps (per ISA-75.01):**

1. **Calculate Required Flow Coefficient (Cv or Kv):**
   - For liquid flow (non-choked): Cv = Q × sqrt(SG / ΔP) or Kv = Q × sqrt(ρ / (ΔP × 1000))
   - Units: Q (gpm or m³/h), SG (dimensionless), ρ (kg/m³), ΔP (psi or bar)

2. **Apply Viscosity Correction (if required):**
   - Calculate Reynolds number: Re = (N1 × Fd² × Q × SG) / (ν × Cv)
   - If Re < 10,000: Apply viscosity correction factor Fv from IEC 60534-2-1 Figure 6
   - Corrected Cv = Cv_calculated / Fv

3. **Apply Piping Geometry Factor (Fp):**
   - If inlet/outlet reducers present: Calculate Fp per ISA-75.01 equation
   - Required Cv = Cv_corrected / Fp

4. **Select Valve Size:**
   - Select valve size (DN or NPS) with available Cv ≥ 1.1× required Cv
   - Verify turndown ratio: Cv_max / Cv_min ≥ required rangeability
   - Select valve body style (globe, ball, butterfly) appropriate for service
   - Select trim characteristic (equal percentage for flow control, linear for pressure control)

5. **Check Cavitation:**
   - Calculate cavitation index: σ = (P1 - Pv) / (P1 - P2)
   - Compare to valve-specific critical cavitation index σc (from vendor data or IEC 60534-8-4)
   - If σ < σc: Cavitation likely; select anti-cavitation trim or increase outlet pressure

6. **Predict Noise Level (if required):**
   - Calculate predicted noise level per IEC 60534-8-3 (complex; typically use vendor software)
   - If predicted noise >85 dBA at 1 meter: Apply noise mitigation (noise attenuation trim, downstream diffuser, acoustic insulation)

7. **Summarize Results:**
   - Valve tag, service, size, type, trim, Cv required, Cv selected, sizing margin
   - Cavitation assessment, noise prediction (if calculated)

**Relief Valve Sizing Calculation Steps (per API 520/521):**

1. **Identify and Evaluate Relief Scenarios:**
   - List all credible overpressure scenarios per API 521 (see Guidance.md — Principles for typical scenarios)
   - For each scenario, estimate relief load (qualitative assessment initially)
   - Identify governing scenario (maximum relief load)

2. **Calculate Relief Load for Governing Scenario:**
   - **Thermal Expansion:** Q = β × V × (T2 - T1) / t (volumetric expansion rate)
   - **Fire Case:** Q = 43,200 × F × A^0.82 (API 521 fire heat input equation)
   - **Blocked Discharge (Pump):** Q = Pump minimum flow at shutoff head
   - **Control Valve Failure:** Q from process simulation at full-open control valve condition
   - **Other Scenarios:** Calculate per API 521 guidance or first-principles heat/mass balance

3. **Calculate Required Orifice Area:**
   - **Liquid Relief:** A = (Q / (Kd × P × Kb)) × sqrt(ρ / ΔP) (API 520 liquid equation)
   - **Vapor Relief:** A = (W × T × Z) / (C × Kd × P × Kb × sqrt(M)) (API 520 vapor equation)
   - **Two-Phase Relief:** Use API 520 two-phase methods or specialized software
   - Units: A (mm² or in²), Q (m³/h or gpm), W (kg/h or lb/h), P (bar or psi), ρ (kg/m³), T (K), M (molecular weight)

4. **Select API 526 Standard Orifice:**
   - Select API 526 orifice designation with area ≥ required area
   - Standard orifices: D (71 mm²), E (126 mm²), F (198 mm²), G (314 mm²), H (506 mm²), J (804 mm²), K (1,140 mm²), L (1,650 mm²), M (2,800 mm²), N (4,340 mm²), P (6,290 mm²), Q (11,100 mm²), R (16,800 mm²), T (26,000 mm²)

5. **Select Set Pressure:**
   - Set pressure = 0.95–1.0× MAWP (typical for single relief valve)
   - Coordinate with pressure vessel/piping MAWP
   - Specify set pressure tolerance per API 526 (±3 psi for pressures ≤70 psig; ±2% for pressures >70 psig)

6. **Verify Accumulated Pressure:**
   - Calculate accumulated pressure during relief (requires iterative calculation or simulation)
   - Verify: Accumulated pressure ≤ 1.1× MAWP (operating case) or ≤ 1.21× MAWP (fire case)

7. **Calculate Back Pressure and Select Valve Type:**
   - Size discharge piping (coordinate with piping designer)
   - Calculate built-up back pressure from discharge piping friction loss
   - If back pressure <10% set pressure: Conventional relief valve acceptable
   - If back pressure 10–50% set pressure: Balanced-bellows relief valve required
   - If back pressure >50% set pressure: Pilot-operated relief valve required (or increase discharge piping size)

8. **Verify Inlet Piping Loss:**
   - Calculate inlet piping pressure loss from protected equipment to relief valve inlet
   - Verify inlet loss <3% of set pressure per API 520 (if excessive, increase inlet piping size)

9. **Summarize Results:**
   - Relief valve tag, protected equipment, governing scenario, relief capacity, set pressure, orifice designation, valve type, inlet/outlet size

**Actuator Sizing Calculation Steps (per ISA-75.25 or manufacturer data):**

1. **Calculate Required Valve Torque/Thrust:**
   - **Quarter-Turn Valves (Ball, Butterfly):** Calculate torque (Nm or ft-lb)
     - Breakaway torque: T_break = f_s × P × A × R (static friction × differential pressure × seat area × moment arm)
     - Running torque: T_run = f_d × P × A × R (dynamic friction × differential pressure × seat area × moment arm)
     - Seating torque: Per manufacturer recommendation for required shutoff class
   - **Linear Valves (Gate, Globe):** Calculate thrust (kN or lb)
     - Breakaway thrust: F_break = P × A + f_s × (stem friction)
     - Running thrust: F_run = P × A + f_d × (stem friction)
   - **Note:** Use manufacturer torque curves if available (preferred); use generic equations if manufacturer data not available

2. **Select Actuator Size:**
   - Maximum required torque/thrust = max(T_break, T_seating) for torque; max(F_break) for thrust
   - Required actuator output = Maximum required torque/thrust × safety factor
   - Safety factor: 1.5 for pneumatic, 1.25 for electric (or per manufacturer recommendation)
   - Select actuator from manufacturer catalog with output ≥ required output

3. **Verify Fail-Safe Capability (for Spring-Return Actuators):**
   - For fail-closed (FC): Verify spring force at minimum air pressure can close valve against maximum differential pressure
   - For fail-open (FO): Verify spring force can open valve against maximum differential pressure
   - Calculate spring force: F_spring = k × x (spring rate × deflection)
   - Verify: F_spring ≥ Required closing/opening force

4. **Calculate Stroking Time:**
   - Stroking time = f(actuator spring rate, air supply flow rate, valve travel)
   - Use manufacturer data or empirical equations
   - Verify stroking time meets control/safety requirements

5. **Calculate Air Consumption (for Pneumatic Actuators):**
   - Air consumption per stroke = Actuator volume × (P_supply - P_atm) / P_atm
   - Units: Liters or SCFM
   - Total air consumption = Air per stroke × Number of strokes per hour (for compressor sizing)

6. **Summarize Results:**
   - Valve tag, actuator type, actuator size/model, output torque/thrust, safety factor achieved, stroking time, air consumption

**Software Use:**
- If using software (Excel, MathCAD, vendor software): Include software input file and output file as calculation appendices
- Document software name, version, and validation status in calculation
- Perform order-of-magnitude hand calculation to verify software results are reasonable

**Source:** Calculation execution steps per ISA-75, API 520/521, and ISA-75.25 methodologies

### Step 4: Self-Check

**Action:** Originator performs self-check of calculations prior to submitting for independent check (see Specification.md — Verification section for verification methods).

**Self-Check Items:**

1. **Completeness:**
   - All required sections present (cover sheet, input data, assumptions, calculations, results, conclusions, references)
   - All input data documented with sources
   - All assumptions clearly stated; TBD items flagged

2. **Accuracy:**
   - All arithmetic correct (spot-check key calculations)
   - All equations correct (verify against code/standard)
   - All units consistent and clearly indicated
   - Numerical precision appropriate (2–3 significant figures)

3. **Consistency:**
   - Valve sizes consistent with P&ID line sizes
   - Set pressures consistent with equipment MAWP
   - Actuator sizes consistent with valve selections
   - Calculation results consistent with DEL-16.04 datasheets (if datasheets prepared in parallel)

4. **Engineering Judgment:**
   - Results are reasonable (order-of-magnitude check)
   - Design margins are appropriate (not overly conservative or unconservative)
   - Assumptions are reasonable and supportable

5. **Presentation:**
   - Calculation is clear and well-organized
   - Figures and tables are clearly labeled
   - Cross-references are correct
   - No typographical errors

**Documentation:**
- Complete self-check checklist (if project provides standard form) — **TBD**
- Correct any errors or omissions identified during self-check
- Mark calculation as "Ready for Independent Check"
- Prepare calculation for checker (print or distribute electronically per project procedures)

**Source:** Typical engineering self-check process; checklist TBD per project quality procedures

### Step 5: Independent Check and Interdisciplinary Check (IDC)

**Action:** Qualified checker performs independent check calculation, and coordinate with other disciplines for interface verification.

**Independent Check (see Specification.md — Verification section for check methods):**

**Checker Selection:**
- Checker shall be qualified mechanical engineer (not the originator)
- Checker shall have equivalent or greater experience than originator
- Checker assignment per project authority matrix — **TBD**

**Check Method (select based on valve criticality):**

**Method A: Full Independent Calculation (for critical valves):**
- Checker performs independent calculation using same methodology and input data
- Compare checker's results to originator's results
- Investigate any discrepancies >5%; resolve before proceeding
- Document check method and comparison results in checker's notes

**Critical Valves Requiring Method A:**
- All relief valves (safety-critical)
- ESD (emergency shutdown) valves
- Control valves >NPS 8 (large, expensive)
- Valves identified as safety-critical in HAZOP (DEL-27.02) — **TBD**

**Method B: Detailed Review with Spot-Check (for non-critical valves):**
- Checker reviews calculation for completeness, methodology, and input data correctness
- Checker performs spot-check calculations (10–20% of calculation steps) to verify arithmetic
- Checker verifies critical results using alternative method or hand calculation
- Document review findings and spot-check results in checker's notes

**Method C: Software Output Verification (for software-based calculations):**
- Checker reviews software input data for correctness
- Checker verifies software output is reasonable (order-of-magnitude check)
- Checker performs benchmark calculation using alternative method (hand calculation or different software) for representative case
- Checker verifies software version is validated for intended use

**Check Documentation:**
- Checker annotates calculation with comments using redline/markup tools (or separate checker's notes)
- Originator addresses checker comments and updates calculation
- Checker verifies comment resolution and signs/dates calculation as "Checked"

**Interdisciplinary Check (IDC):**

Coordinate calculations with other disciplines to verify interface assumptions (see Specification.md — Interface Requirements for coordination needs):

**Disciplines to Coordinate:**
1. **Process:** Verify flow rates, pressures, temperatures are consistent with latest process design (P&ID revision, process simulation case)
2. **Piping (DEL-14.01, DEL-14.02):** Verify line sizes, pressure classes, piping geometry factors; provide valve pressure drop data for piping stress analysis and pump sizing
3. **Instrumentation (DEL-20.01):** Verify control valve rangeability meets control requirements; verify control signal types (4–20 mA, HART, etc.)
4. **Control Systems (DEL-19.01):** Verify control valve fail-safe modes consistent with control logic; verify stroking time requirements
5. **Pressure Vessels (PKG-13, others):** Verify relief valve set pressures consistent with vessel MAWP; coordinate fire case relief with tank design
6. **Safety (DEL-27.02 HAZOP):** Verify relief valve scenarios consistent with HAZOP recommendations; verify ESD valve fail-safe modes per HAZOP

**IDC Process:**
- Distribute calculation summary for IDC via project document management system — **TBD**
- Allow review period (typically 5–10 working days) — **TBD**
- Collect IDC comments via project comment management system — **TBD**
- Categorize comments per project convention (Category A = must resolve, Category B = incorporate if possible, Category C = noted)
- Resolve Category A comments; respond to Category B/C comments
- Update calculation if significant changes result from IDC

**Source:** Typical independent check and IDC process for multi-discipline projects; specific procedures TBD per project quality plan

### Step 6: Approval and Issue

**Action:** Obtain discipline lead approval and issue calculation per project procedures.

**Approval Process:**

**Approval Signatories:**
- **Originator:** Design engineer who prepared the calculation (signed at completion of self-check)
- **Checker:** Independent checker who reviewed the calculation (signed after check complete and comments resolved)
- **Approver:** Discipline lead (P.Eng.) authorized to approve mechanical calculations (signs after review of calculation and checker's comments)

**Approver Review:**
- Discipline lead reviews calculation for technical adequacy and compliance with project standards
- Approver verifies all checks complete (self-check, independent check, IDC)
- Approver verifies calculation conclusions and recommendations are appropriate
- Approver may request revisions or additional analysis before approval

**Calculation Issue:**
- Assign calculation number per project calculation numbering system — **TBD**
  - **ASSUMPTION:** Format "CALC-PKG16-DEL03-001" (sequential numbering within deliverable)
- Assign revision code (Rev 0 or A for initial issue; increment per project convention) — **TBD**
- Update calculation cover sheet with approval signatures and issue date
- Issue calculation via project document management system — **TBD**
- Update calculation register/index

**Issue Purpose Codes (typical):**
- **IFD (Issued for Design):** Calculation approved for use in design development
- **IFC (Issued for Construction):** Calculation approved for construction (final issue)
- **IFR (Issued for Review):** Calculation issued for review/comment (30%, 60%, 90% submittals)
- **IFA (Issued for Approval):** Calculation issued to Employer or Authority for approval (if required)

**Source:** Typical calculation approval and issue process; specific codes and procedures TBD per project document control procedures

### Step 7: Post-Procurement Verification (Vendor Data Incorporation)

**Action:** After valve procurement, verify vendor-supplied data matches calculation assumptions; update calculations if required.

**Vendor Data Review:**

**Control Valves:**
- Receive valve vendor certified Cv tables and trim data
- Compare vendor Cv to calculated required Cv; verify selected valve has adequate capacity
- Verify vendor-supplied cavitation index (σc) and noise prediction match calculation assumptions
- If vendor data significantly different from assumptions (>10% difference): Update calculation and re-issue

**Relief Valves:**
- Receive relief valve vendor capacity certification data (ASME stamped capacity, orifice area, set pressure tolerance)
- Verify vendor capacity certification ≥ required relief capacity from calculation
- Verify set pressure and tolerance per API 526
- Verify inlet/outlet connection sizes match piping design
- Relief valves are ASME stamped; capacity certification is legally binding; no calculation update required unless error identified

**Actuators:**
- Receive actuator vendor certified torque/thrust data and air consumption data
- Verify vendor output torque/thrust ≥ required (from calculation) × safety factor
- Verify stroking time meets requirements
- If actuator undersized: Reject and require larger actuator; update calculation to document issue

**Calculation Update:**
- If vendor data requires calculation revision: Update calculation with vendor data, re-check, re-approve, and re-issue (Rev 1 or B)
- Document revision reason (e.g., "Updated with vendor XYZ certified data per submittal 2024-03-15")
- Archive superseded calculation revision

**Source:** Typical vendor data incorporation process for EPC projects; specific process TBD per project execution plan

## Verification

**Verification activities for Calculation deliverables:**

### Self-Check (Step 4)
- Originator reviews for completeness, accuracy, consistency, engineering judgment, and presentation quality
- Sign-off: Originator initials and dates calculation cover sheet "Calculated By" field — **TBD**

### Independent Check (Step 5)
- Qualified checker performs full independent calculation (Method A), detailed review with spot-check (Method B), or software output verification (Method C) based on valve criticality
- Sign-off: Checker signs and dates calculation cover sheet "Checked By" field — **TBD**

### Interdisciplinary Check (Step 5)
- Multi-discipline coordination to verify interface assumptions and provide feedback
- Sign-off: IDC complete when Category A comments resolved and calculation updated

### Design Code Compliance Check
- Checker verifies calculations comply with applicable design codes (ISA-75, API 520/521, ISA-75.25, ASME Section VIII, CSA B51)
- Verify correct equations, code rules, and methodology applied

### Approval (Step 6)
- Discipline lead (P.Eng.) reviews and approves calculation for issue
- Sign-off: Approver signs and stamps calculation cover sheet "Approved By" field with P.Eng. seal — **TBD**

**Acceptance Criteria:**
- All verification steps completed per project quality procedures
- Zero unresolved checker comments (or approved waivers for minor comments)
- IDC Category A comments resolved; Category B/C comments responded to
- Design code compliance verified
- Originator, checker, and approver signatures obtained per project authority matrix — **TBD**
- Calculation format complies with project calculation standards — **TBD**
- Calculation results are reasonable and consistent with engineering judgment

**Source:** Verification activities typical for engineering calculations; specific sign-off requirements TBD per project quality procedures and authority matrix

## Records

**Documentation outputs:**

### Primary Deliverables
- **Control Valve Sizing Calculations:** Individual calculations for each control valve (or grouped by system); multiple calculations anticipated
- **Relief Valve Sizing Calculations:** Individual calculations for each relief valve; multiple calculations anticipated
- **Actuator Sizing Calculations:** Individual calculations for each automated valve (or integrated into control valve sizing calculations)

**Format:** **TBD** — **ASSUMPTION:** PDF calculation packages with supporting native files (Excel, MathCAD, etc.)

### Supporting Records
- **Calculation Register/Index:** List of all valve sizing calculations with document numbers, titles, valve tags, and revision status
- **Input Data Summary:** Consolidated summary of key input data (flow rates, pressures, fluid properties) with sources
- **Assumptions Log:** Consolidated list of engineering assumptions and TBD items requiring confirmation
- **Checker's Notes:** Independent check documentation (comparison results, spot-check calculations, review comments)
- **IDC Comment/Response Log:** Record of interdisciplinary comments and resolutions
- **Software Validation Records:** Software validation documentation (if calculation software used) — **TBD**
- **Vendor Data Comparison:** Post-procurement comparison of vendor data vs. calculation assumptions

**Record Management:**

**During Development (Working Status):**
- Working files maintained in `1_Working/` folder in deliverable directory
- Native calculation files (Excel, MathCAD, etc.) and PDF drafts
- **Source:** Folder structure per README.md Section "What lives where"

**During Review (CHECKING Status):**
- Calculation package placed in `2_Checking/To/` folder for independent check
- Include cover sheet, calculation sheets, and appendices (software files, vendor data, etc.)
- Track checker comments and resolutions
- **Source:** Recommended convention per README.md Section 6 (Review and issue)

**Upon Issue (ISSUED Status):**
- Issued calculations placed in `3_Issued/` folder
- Include PDF and native files
- Archive superseded revisions (if calculation revised)
- Update calculation register
- **Source:** Recommended convention per README.md Section 6 (Review and issue)

**Retention Requirements:**
- Retention period: **TBD** — **ASSUMPTION:** Project life + 25 years typical for design calculations (permanent record)
- Archival format: **TBD** — **ASSUMPTION:** PDF/A for long-term preservation; retain native files for future revisions
- Backup and disaster recovery: **TBD** — Per project IT/document management procedures

**Electronic Document Management:**
- **ASSUMPTION:** Electronic records managed in project document management system (e.g., Aconex, ProjectWise, SharePoint, or equivalent)
- Document control procedures: **TBD** — Per project document control plan
- Access permissions: **TBD** — Per project data security requirements

**Source:** Record management practices typical for EPC projects; specific requirements TBD per project procedures

## Revision History and Configuration Management

**Calculation Revisions:**
- Initial issue: Rev 0 (or Rev A) — **TBD** per project convention
- Subsequent revisions: Incremental (Rev 1, 2, 3... or Rev B, C, D...) — **TBD**
- Revision description noted in calculation cover sheet revision table
- Revision bars or highlighting mark changed pages/sections per project standards — **TBD**

**Reasons for Calculation Revision:**
- Input data change (process design update, P&ID revision, etc.)
- Vendor data incorporation (post-procurement)
- Design change (valve size or type change)
- Error correction (checker or IDC comment requiring revision)
- Code or standard update

**Configuration Control:**
- Calculation supersedes previous revision upon issue
- Prior revision archived but retained for record (traceability)
- Calculation register maintains current and superseded revision status
- No working from superseded calculations (document management system controls) — **TBD**

**Source:** Configuration management typical for engineering calculations; specific procedures TBD per project document control plan
