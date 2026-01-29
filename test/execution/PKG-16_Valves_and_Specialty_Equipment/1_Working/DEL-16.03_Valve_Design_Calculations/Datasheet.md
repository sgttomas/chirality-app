# Datasheet: DEL-16.03 Valve Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-16.03 |
| Name | Valve Design Calculations |
| Package | PKG-16 Valves & Specialty Equipment |
| Discipline | Mechanical |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md`

## Attributes

| Attribute | Value |
|-----------|-------|
| Calculation Types | Control valve sizing (Cv/Kv), relief valve sizing, actuator sizing |
| Calculation Number Prefix | **TBD** — Per project calculation numbering system |
| Software Used | **TBD** — **ASSUMPTION**: Excel spreadsheets, MathCAD, or specialized software (e.g., Emerson PRV2SIZE, Fisher Control Valve Handbook) |
| Primary Design Codes | ISA-75.01 (control valves), API 520/521 (relief valves), ISA-75.25 (actuators) |
| Calculation Format | **TBD** — **ASSUMPTION**: Structured calculation sheets with inputs, methodology, calculations, results, and references |
| Revision | **TBD** — Initial issue for design basis |
| Classification | **TBD** — **ASSUMPTION**: For Construction or Design Basis |
| Applicable Systems | Railcar unloading, marine loading, product transfer, storage tank systems |

**Source:** `_CONTEXT.md` (anticipated artifacts); PKG-16 scope from decomposition (location TBD — Section 5, PKG-16)

## Conditions

**Operating / Environmental Context:**

This calculation package supports valve sizing and selection for the canola oil transload facility (1,000,000 MT/annum throughput) at Fraser Surrey Terminal, Surrey, BC.

**Source:** Decomposition document Section 1.1 (Project Overview)

**Process Fluid:**
- Product: CSD (Crude Super Degummed) canola oil
- Operating temperature: **TBD** — Typical range for canola oil handling **ASSUMPTION**: -10°C to +50°C ambient, heated product lines 40–60°C for viscosity control
- Operating pressure: **TBD** — To be defined per system:
  - Railcar unloading: Gravity feed + pump suction/discharge (typically 0–10 barg)
  - Marine loading: Pump discharge to loading arm (typically 5–15 barg)
  - Storage tanks: Atmospheric to low pressure (0–2 barg)
  - Relief valves: Set pressure per ASME Section VIII (typically 1.1× MAWP)
- Viscosity: **TBD** — Canola oil kinematic viscosity varies significantly with temperature:
  - At 20°C: ~50–70 cSt (high viscosity, requires heating)
  - At 40°C: ~30–40 cSt (typical pumping temperature)
  - At 60°C: ~15–20 cSt (low viscosity for loading operations)
- Density: **TBD** — **ASSUMPTION**: ~920 kg/m³ at 15°C (typical for canola oil)
- Vapor pressure: **TBD** — Very low vapor pressure (high boiling point ~300°C)

**Source:** Decomposition document Section 1.1 (product grade); temperature/pressure/viscosity ranges TBD pending system design; canola oil properties from industry data

**Environmental:**
- Location: Fraser Surrey Terminal (marine/industrial environment)
- Environmental classification: **TBD** — **ASSUMPTION**: Coastal/marine atmosphere, corrosion category C4 or C5-M per ISO 12944
- Ambient temperature range: **TBD** — Fraser Surrey climate (typical: -10°C to +30°C)
- Design life: **TBD** — **ASSUMPTION**: 25 years typical for industrial facility

**Source:** Decomposition document Section 1.1 (location); environmental parameters TBD pending design basis

**Hazardous Area:**
- Classification: **TBD** — To be confirmed per facility hazardous area classification study
- **ASSUMPTION**: Process areas likely Class I, Division 2 or Zone 2 (Group D); actuators rated accordingly

**Calculation Scope:**

This deliverable provides sizing calculations for three categories of valves (see also Specification.md — Functional Requirements for calculation content requirements):

1. **Control Valve Sizing (per ISA-75.01):**
   - Flow control valves (modulating flow in transfer lines)
   - Pressure control valves (pressure reducing, back-pressure regulation)
   - Level control valves (tank level control applications)
   - Calculation outputs: Required Cv or Kv, valve size, pressure drop, noise level, cavitation index

2. **Relief Valve Sizing (per API 520/521):**
   - Pressure relief valves for overpressure protection (thermal expansion, fire case, blocked discharge)
   - Vacuum relief valves (if required for storage tanks)
   - Calculation outputs: Required relief capacity (kg/h or m³/h), orifice area, set pressure, back pressure

3. **Actuator Sizing (per ISA-75.25):**
   - Pneumatic actuator sizing (spring-return and double-acting)
   - Electric actuator sizing (motor torque/thrust requirements)
   - Calculation outputs: Required torque/thrust, safety factor verification, stroking time

**Source:** Calculation types inferred from PKG-16 scope and typical transload facility requirements

## Construction

**Calculation Package Structure:**

Per `_CONTEXT.md`, this deliverable includes two primary calculation sets:

### 1. Control Valve Sizing Calculations

**Methodology (per ISA-75.01):**
- **Flow Coefficient Calculation (Cv or Kv):** Based on flow rate, pressure drop, fluid density, and viscosity
  - Liquid flow: Cv = Q × sqrt(SG / ΔP) where Q = flow (gpm), SG = specific gravity, ΔP = pressure drop (psi)
  - SI units: Kv = Q × sqrt(ρ / ΔP) where Q = flow (m³/h), ρ = density (kg/m³), ΔP = pressure drop (bar)
- **Valve Sizing:** Select valve size with Cv ≥ required Cv; consider rangeability (turndown ratio typically 50:1 for control valves)
- **Pressure Drop Allocation:** Typically 25–50% of available system pressure drop allocated to control valve for good control authority
- **Cavitation Check:** Calculate cavitation index (σ) and compare to valve-specific σc to avoid cavitation damage
- **Noise Level Prediction:** Calculate predicted noise level per IEC 60534-8-3; mitigate if >85 dBA at 1 meter

**Inputs Required (see Procedure.md — Step 1 for input data collection process):**
- Flow rates: Normal, design, minimum (from P&IDs and process design)
- Inlet/outlet pressures: Normal and design conditions (from process design)
- Fluid properties: Density, viscosity, vapor pressure (from process data)
- Piping data: Line size, schedule, material (from DEL-14.01, DEL-14.02)

**Outputs (see Specification.md — Performance Requirements for output acceptance criteria):**
- Valve tag number, service description
- Required Cv or Kv (at design conditions)
- Selected valve size (DN or NPS)
- Valve body style (globe, ball, butterfly)
- Trim characteristic (equal percentage, linear, quick-opening)
- Pressure drop across valve (normal and design conditions)
- Cavitation index and assessment (acceptable/not acceptable)
- Noise level prediction (dBA at 1 meter)
- Recommended valve manufacturer/model (if specified)

**Source:** ISA-75.01 control valve sizing methodology; typical calculation requirements for process facilities

### 2. Relief Valve Sizing Calculations

**Methodology (per API 520/521):**
- **Relief Scenario Identification:** Identify credible overpressure scenarios:
  - Thermal expansion (blocked-in liquid between isolation valves)
  - Fire case (external fire heating vessel contents)
  - Cooling water failure (loss of cooling causing vapor generation)
  - Control valve failure (full-open causing overpressure)
  - Blocked discharge (pump dead-heading)
- **Relief Load Calculation:** Calculate required relief mass flow or volumetric flow for each scenario
- **Orifice Sizing:** Calculate required orifice area per API 520 equations (liquid, vapor, or two-phase flow)
- **Set Pressure Selection:** Typically 1.05–1.1× MAWP per ASME Section VIII; coordinate with pressure vessel design
- **Back Pressure Analysis:** Conventional vs. balanced-bellows vs. pilot-operated selection based on back pressure
- **Discharge Piping Design:** Size discharge piping to limit back pressure (typically <10% set pressure for conventional PRVs)

**Inputs Required (see Procedure.md — Step 1):**
- Protected equipment: Vessel, piping section, heat exchanger (from P&IDs)
- MAWP (Maximum Allowable Working Pressure): From pressure vessel design or piping class
- Relief scenarios: From HAZOP (DEL-27.02) or process safety analysis
- Fluid properties: Density, specific heat, vapor pressure (from process data)
- Fire exposure area: For fire case scenario (from vessel geometry)

**Outputs (see Specification.md — Performance Requirements):**
- Relief valve tag number, protected equipment
- Governing relief scenario (thermal expansion, fire, etc.)
- Required relief capacity (kg/h or SCFM)
- Set pressure (psig or barg)
- Calculated orifice area (mm² or in²)
- Selected orifice designation (API 526 standard orifice: D, E, F, G, etc.)
- Relief valve type (conventional, balanced-bellows, pilot-operated)
- Inlet/outlet connection size
- Back pressure (built-up back pressure from discharge system)
- Discharge piping requirements (size, routing to safe location per DEL-16.01)

**Source:** API 520/521 relief valve sizing methodology; typical calculation requirements for process facilities

### 3. Actuator Sizing Calculations

**Methodology (per ISA-75.25):**
- **Torque/Thrust Calculation:** Calculate required torque (quarter-turn valves) or thrust (linear valves):
  - Breakaway torque (to overcome static friction and unseating force)
  - Running torque (to move valve during operation)
  - Seating torque (to achieve tight shutoff)
- **Actuator Selection:** Select actuator with output torque/thrust ≥ 1.5× maximum calculated torque/thrust (safety factor)
- **Stroking Time Verification:** Calculate stroking time based on actuator spring rate and air supply; verify meets control requirements
- **Air Supply Requirements:** Calculate required air volume and flow rate (SCFM) for pneumatic actuators
- **Fail-Safe Mode Verification:** Verify spring-return actuator can close/open valve on loss of air supply

**Inputs Required (see Procedure.md — Step 1):**
- Valve data: Size, type, differential pressure, seat material (from DEL-16.04 datasheets)
- Actuator type: Pneumatic (spring-return or double-acting), electric (from P&ID or control philosophy)
- Fail-safe mode: Fail-closed (FC), fail-open (FO), or fail-as-is (FL) (from HAZOP recommendations)
- Air supply pressure: Typically 5–7 barg for pneumatic actuators (from utility design basis)

**Outputs (see Specification.md — Performance Requirements):**
- Valve tag number
- Required breakaway, running, and seating torque/thrust
- Selected actuator size and model
- Actuator output torque/thrust (at rated air pressure)
- Safety factor verification (≥1.5 typical)
- Stroking time (seconds to full open or full closed)
- Air consumption per stroke (for sizing air supply system)
- Manual override capability (handwheel, declutching mechanism)

**Source:** ISA-75.25 actuator sizing methodology; typical calculation requirements for automated valves

**Calculation Software and Tools:**

- **Control Valve Sizing:** **TBD** — Vendor software (e.g., Fisher Control Valve Handbook, Emerson FlowCalc) or custom spreadsheets per ISA-75.01
- **Relief Valve Sizing:** **TBD** — API 520/521 calculation spreadsheets, vendor software (e.g., Emerson PRV2SIZE), or process simulation software
- **Actuator Sizing:** **TBD** — Vendor catalogs and sizing tools, or custom spreadsheets per ISA-75.25

**Source:** Typical calculation software for valve sizing; specific tools TBD per project standards

**Interface Deliverables (see also Specification.md — Interface Requirements):**
- DEL-16.01 (Valve Design Drawing Set) — Valve arrangement uses sizing calculation results (see Procedure.md — Step 5 for coordination)
- DEL-16.02 (Valve Technical Specification) — Specification references sizing calculation methodology and criteria
- DEL-16.04 (Valve Data Sheet Package) — Individual valve datasheets populated with calculation results (see Guidance.md — Section 4 "Considerations" for datasheet coordination)
- DEL-14.01/14.02 (Process Piping Design) — Piping design provides input data (line sizes, pressures, flows)
- DEL-27.02 (HAZOP Study) — HAZOP identifies relief valve scenarios and fail-safe mode requirements

**Source:** Interface requirements inferred from package structure and calculation dependencies; formal dependencies NOT_TRACKED per `_DEPENDENCIES.md`

**For calculation methodology and procedure, see Procedure.md. For calculation requirements and verification methods, see Specification.md. For sizing principles and trade-offs, see Guidance.md.**

## References

**Reference Documents:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials

**Applicable Standards:**

**Control Valve Sizing:**
- IEC 60534 / ISA-75 series — Industrial-Process Control Valves
  - ISA-75.01 — Control Valve Sizing Equations (flow coefficient calculation)
  - ISA-75.02 — Control Valve Capacity Test Procedures
  - ISA-75.05 — Control Valve Terminology
  - ISA-75.11 — Inherent Flow Characteristic and Rangeability
  - IEC 60534-8-3 — Noise Prediction Method
  - IEC 60534-8-4 — Prediction of Cavitation

**Relief Valve Sizing:**
- API 520 — Sizing, Selection, and Installation of Pressure-Relieving Devices (Part I — Sizing and Selection)
- API 521 — Pressure-Relieving and Depressuring Systems
- ASME BPVC Section VIII — Pressure Vessels (relief valve requirements and set pressure rules)
- ISO 4126 — Safety Devices for Protection Against Excessive Pressure (alternative to API for international projects)

**Actuator Sizing:**
- ISA-75.25 — Test Procedure for Control Valve Actuators
- VDI/VDE 3845 — Control Valves (German standard for actuator sizing)

**Piping and Pressure Systems:**
- ASME B31.3 — Process Piping (pressure-temperature ratings, allowable stresses)
- CSA B51 — Boiler, Pressure Vessel and Pressure Piping Code (Canadian regulatory requirements)

**Materials and Fluid Properties:**
- ASME Steam Tables — Thermodynamic properties of water and steam (if applicable)
- NIST Chemistry WebBook — Thermophysical properties of fluids
- Industry data — Canola oil properties (viscosity, density, specific heat)

**Project-Specific:**
- Employer's Requirements — **TBD** — **ASSUMPTION**: Volume 2 Parts 1–3 contain valve sizing criteria and acceptance requirements
- Project Engineering Standards — **TBD** — Project-specific calculation format and sign-off requirements
- Process Design Basis — **TBD** — Fluid properties, operating conditions, flow rates

**Source:** Standards inferred from Mechanical discipline and valve sizing scope; applicability to be confirmed during calculation development

**Cross-references:**
- See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
- Decomposition document: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section 5, PKG-16, DEL-16.03
