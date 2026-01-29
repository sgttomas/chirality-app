# Datasheet: DEL-20.03 Instrumentation Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-20.03 |
| Name | Instrumentation Design Calculations |
| Package | PKG-20 Field Instrumentation |
| Discipline | I&C |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |

## Attributes

| Attribute | Value |
|-----------|-------|
| Calculation Type | Instrument sizing and verification |
| Calculation Number | **TBD** — Per project calculation numbering system |
| Software Used | **TBD** — **ASSUMPTION**: Excel, MathCAD, or discipline-specific software |
| Design Code | ISA, API, ASME standards applicable to instrumentation |
| Calculation Format | **TBD** — **ASSUMPTION**: Standard calculation sheet template with inputs/assumptions/calculations/results |
| Revision Control | **TBD** — Per project document control procedures |
| Professional Seal | **TBD** — P.Eng. seal requirements for BC jurisdiction (calculation verification) |
| Classification | **TBD** — **ASSUMPTION**: Design calculations (supporting documentation for specification and data sheets) |

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-20, DEL-20.03 (line 498)

## Conditions

**Project Context:**

This calculation package supports the Canola Oil Transload Facility Phase 1 where Crude Super Degummed (CSD) grade canola oil transfers from rail tank cars to liquid bulk carriers for export.

**Source:** Decomposition document, Section 1.1 Project Overview

**Key Project Parameters:**

| Parameter | Value | Source |
|-----------|-------|--------|
| Permitted Throughput | 1,000,000 MT per annum | Decomposition, Section 1.1 |
| Storage Capacity | 45,000 MT (3 × 15,000 MT tanks) | Decomposition, Section 1.1 |
| Product Grade | CSD (Crude Super Degummed) canola oil | Decomposition, Section 1.1 |
| Railcar Capacity | 32 unloading stations on 2 tracks | Decomposition, Section 1.1 |

**Design Basis Conditions:**

Calculations shall be based on the following design conditions:

- **Process Fluid:** CSD canola oil
  - **Density:** **TBD** — Approximately 0.92 kg/L (typical) — from process design basis
  - **Viscosity:** **TBD** — Temperature-dependent, from process design basis
  - **Operating Temperature:** **TBD** — From P&IDs and process data sheets
  - **Operating Pressure:** **TBD** — From P&IDs and piping design

- **Environmental Conditions:**
  - **Ambient Temperature:** **TBD** — **ASSUMPTION**: -30°C to +50°C (outdoor BC coastal climate)
  - **Marine Environment:** Salt air exposure, corrosion considerations
  - **Seismic:** **TBD** — Per NBC 2015 for Surrey, BC location

- **Hazardous Area:** **TBD** — Per facility hazardous area classification drawing (affects instrument enclosure and wiring calculations)

**Source:** **ASSUMPTION** based on project location and typical design basis parameters; **TBD**: Specific values from process engineering and environmental design basis

**Calculation Purpose:**

Instrumentation design calculations provide the engineering basis for:
1. **Instrument range selection** — Verify selected ranges accommodate normal, design, and limiting process conditions
2. **Instrument accuracy verification** — Verify specified accuracy meets measurement requirements (process control, safety, custody transfer)
3. **Instrument sizing** — Size instruments for specific applications (orifice plates, flow elements, thermowells)
4. **Performance verification** — Verify instrument response time, turndown, and other performance parameters
5. **Installation verification** — Verify mounting loads, impulse piping slope, winterization requirements

**Source:** **ASSUMPTION** based on typical instrumentation calculation scope; deliverable description "engineering basis and sizing/verification" (line 498)

## Construction

**Anticipated Calculation Artifacts:**

The following calculation types are anticipated for PKG-20 Field Instrumentation:

### 1. Level Instrument Sizing and Range Calculations

**Applications:**
- Storage tanks (3 × 15,000 MT): Level transmitter range selection and accuracy verification
- Process vessels: Level transmitter and switch range selection
- Overfill protection: Independent high-level alarm setpoint calculations per API 2350

**Typical Calculations:**
- Tank geometry and capacity (level-to-volume conversion)
- Transmitter range selection (0-100% span coverage of tank operating range)
- Accuracy budget (sensor + transmitter + installation effects)
- Alarm setpoint calculations (high/low alarms, overfill protection)

**Source:** Decomposition Key Parameters (storage capacity line 40); **ASSUMPTION** based on typical level instrumentation calculations for bulk storage

### 2. Pressure Instrument Sizing and Range Calculations

**Applications:**
- Pump performance monitoring: Transmitter range selection for suction/discharge pressure
- Piping system monitoring: Transmitter range selection for operating pressures
- Differential pressure: Flow element sizing (orifice plates if used), filter ΔP monitoring

**Typical Calculations:**
- Operating pressure range analysis (normal, design, maximum)
- Transmitter range selection (operating point at 30-70% of span for optimal accuracy)
- Overpressure rating verification (≥2× range or piping MAWP)
- Orifice plate sizing calculations (if flow measurement via DP) per API 14.3 or ISO 5167

**Source:** **ASSUMPTION** based on typical pressure instrumentation calculations for liquid transfer systems

### 3. Temperature Instrument Sizing and Range Calculations

**Applications:**
- Product temperature monitoring: RTD range selection for storage tanks and transfer lines
- Equipment protection: Thermocouple range selection for pump bearings, motor windings

**Typical Calculations:**
- Operating temperature range analysis (normal, design, maximum)
- Element type selection (RTD vs. thermocouple) based on accuracy requirements
- Thermowell sizing calculations (stress analysis per ASME PTC 19.3 for high-velocity applications)
- Response time calculations (time constant based on thermal mass and heat transfer)

**Source:** **ASSUMPTION** based on typical temperature instrumentation calculations

### 4. Flow Instrument Sizing Calculations (Coordination)

**Note:** Primary custody transfer flow metering is addressed in PKG-12 (Product Transfer and Metering). PKG-20 calculations may include:
- Process control flow measurement (non-custody transfer)
- Flow switch sizing for pump protection and flow verification

**Typical Calculations:**
- Flow rate range (minimum, normal, maximum)
- Flow element sizing (if applicable)
- Pressure drop calculations (impact on system hydraulics)

**Source:** Cross-reference to PKG-12 per decomposition (lines 259-268); **ASSUMPTION** on PKG-20 scope boundary

### 5. Instrument Accuracy and Uncertainty Calculations

**Applications:**
- Total loop uncertainty analysis (TLU) for critical measurements
- Custody transfer accuracy verification (if applicable — coordinate with PKG-12)
- Safety instrumented function (SIF) accuracy verification (if SIL-rated per ISA 84)

**Typical Calculations:**
- Individual error components (sensor accuracy, transmitter accuracy, installation effects, calibration drift)
- Root-sum-square (RSS) or worst-case summation
- Comparison to measurement requirement (process control tolerance, custody transfer requirement, SIF requirement)

**Source:** **ASSUMPTION** based on ISA 84, API MPMS, and typical measurement uncertainty analysis requirements

### 6. Impulse Piping and Installation Calculations

**Applications:**
- Impulse piping slope and support calculations
- Winterization requirements (heat tracing, insulation)
- Mounting load calculations for in-line instruments (weight, seismic, thermal expansion)

**Typical Calculations:**
- Piping support spacing (based on material and diameter)
- Heat loss calculations (winterization requirements for outdoor installations)
- Seismic restraint loads (for large in-line instruments)

**Source:** **ASSUMPTION** based on typical instrumentation installation calculations per ISA, API 554

**Calculation Format (Typical):**

Each calculation shall follow a standard format:
1. **Objective:** What is being calculated and why
2. **Design Basis:** Input data, assumptions, reference documents
3. **Calculations:** Step-by-step calculations with equations and intermediate results
4. **Results:** Summary of calculated values and conclusions
5. **References:** Codes, standards, data sources, related documents
6. **Verification:** Independent check sign-off

**Source:** **ASSUMPTION** based on typical engineering calculation format

**Calculation Software:**

- **TBD** — Software platform per project standards (Excel, MathCAD, specialty software)
- **ASSUMPTION**: Calculations shall be reviewable and reproducible (formulas visible, not black-box)
- Version control for calculation files per project document management procedures

## References

**Primary References:**

- Decomposition document: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (Section PKG-20)
- `_CONTEXT.md` — Deliverable identity and scope
- `_REFERENCES.md` — Additional reference materials (currently: no references identified)
- Employer's Requirements — **TBD**: Specific sections from Vol 2 Parts 1-3

**Design Input References:**

- P&IDs and instrument list (instrument tag numbers, service descriptions)
- Process data sheets (operating pressures, temperatures, flow rates, fluid properties)
- Equipment data sheets (pump curves, tank dimensions, vessel specifications)
- Piping design basis (design pressures, temperatures, materials)
- Environmental design basis (ambient conditions, seismic criteria)
- Hazardous area classification drawings

**Source:** **ASSUMPTION** based on typical calculation input requirements

**Applicable Standards and Codes:**

**Instrumentation Standards:**
- **ISA 5.1** — Instrumentation identification
- **ISA 84 / IEC 61511** — Functional safety (SIF accuracy verification)
- **API 554** — Process Instrumentation and Control (general guidance)
- **API 2350** — Overfill Protection (tank overfill calculations)

**Flow Measurement Standards:**
- **API 14.3 / ISO 5167** — Orifice plate sizing and calculations
- **API MPMS Chapter 5** — Metering (if custody transfer metering is included)

**Thermowell Design:**
- **ASME PTC 19.3** — Thermowell Design and Installation (stress and wake frequency calculations)

**General Engineering:**
- **ASME B31.3** — Process Piping (impulse piping design if applicable)
- **NBC 2015** — National Building Code (seismic loads)

**Note:** Standards applicability to be confirmed based on specific calculation requirements. Specific clause-level references **TBD** during calculation development.

**Related Deliverables:**

- **DEL-20.01** — Instrumentation Design Drawing Set (drawings reflect calculation results)
- **DEL-20.02** — Instrumentation Technical Specification (calculations verify specification requirements)
- **DEL-20.04** — Instrumentation Data Sheet Package (data sheets include calculated ranges and parameters)
- **DEL-20.05** — Instrumentation Installation & Test Records (test procedures verify calculated performance)

**Source:** Decomposition document, PKG-20 deliverables (lines 496-500)

**Dependencies:**

See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies coordinated externally by humans per project coordination plan.

**Project Objective Alignment:**

This deliverable supports **OBJ-1: Safe & Reliable Operation** — Proper sizing and verification calculations ensure instruments are correctly specified for safe and reliable facility operations.

**Source:** Decomposition document, Section 6 Objective-to-Deliverable Mapping (line 780)
