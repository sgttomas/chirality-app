# Datasheet: DEL-16.04 Valve Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-16.04 |
| Name | Valve Data Sheet Package |
| Package | PKG-16 Valves & Specialty Equipment |
| Discipline | Mechanical |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md`

## Attributes

| Attribute | Value |
|-----------|-------|
| Data Sheet Types | Control valve data sheets, isolation valve data sheets, relief valve data sheets |
| Data Sheet Number Prefix | **TBD** — Per project datasheet numbering system |
| Format | **TBD** — **ASSUMPTION**: Standardized forms/templates per valve type (control, isolation, relief) |
| Quantity | **TBD** — Multiple datasheets (one per valve or grouped by service/system) |
| Revision | **TBD** — Initial issue for procurement; updated post-procurement with vendor data |
| Classification | **TBD** — **ASSUMPTION**: For Procurement (initial); As-Built (final with vendor data) |
| Applicable Systems | Railcar unloading, marine loading, product transfer, storage tank systems |

**Source:** `_CONTEXT.md` (anticipated artifacts); PKG-16 scope from decomposition (location TBD — Section 5, PKG-16)

## Conditions

**Operating / Environmental Context:**

This datasheet package defines and substantiates valve selections for the canola oil transload facility (1,000,000 MT/annum throughput) at Fraser Surrey Terminal, Surrey, BC.

**Source:** Decomposition document Section 1.1 (Project Overview)

**Process Fluid:**
- Product: CSD (Crude Super Degummed) canola oil
- Operating temperature: **TBD** — Typical range for canola oil handling **ASSUMPTION**: -10°C to +50°C ambient, heated product lines 40–60°C for viscosity control
- Operating pressure: **TBD** — To be defined per system (railcar unloading, marine loading, tank farm)
- Viscosity: **TBD** — Canola oil kinematic viscosity varies with temperature (50–70 cSt at 20°C; 30–40 cSt at 40°C; 15–20 cSt at 60°C)
- Density: **TBD** — **ASSUMPTION**: ~920 kg/m³ at 15°C (typical for canola oil)

**Source:** Decomposition document Section 1.1 (product grade); fluid properties TBD pending process design

**Environmental:**
- Location: Fraser Surrey Terminal (marine/industrial environment)
- Environmental classification: **TBD** — **ASSUMPTION**: Coastal/marine atmosphere, corrosion category C4 or C5-M per ISO 12944
- Ambient temperature range: **TBD** — Fraser Surrey climate (typical: -10°C to +30°C)
- Design life: **TBD** — **ASSUMPTION**: 25 years typical for industrial facility

**Source:** Decomposition document Section 1.1 (location); environmental parameters TBD pending design basis

**Hazardous Area:**
- Classification: **TBD** — To be confirmed per facility hazardous area classification study
- **ASSUMPTION**: Process areas likely Class I, Division 2 or Zone 2; actuators and accessories rated accordingly

**Datasheet Purpose:**

Valve datasheets serve as the technical specification for each individual valve, consolidating all design information in a standardized format for procurement, fabrication, installation, and operation (see also Specification.md — Functional Requirements for datasheet content requirements).

**Datasheet Uses:**
1. **Procurement:** Basis for vendor bidding and quotation
2. **Fabrication:** Vendor reference for valve manufacture and testing
3. **Installation:** Field reference for valve installation and piping interface
4. **Commissioning:** Basis for functional testing and set pressure verification (relief valves)
5. **Operation & Maintenance:** Reference for valve operation, maintenance, and spare parts

**Source:** Typical datasheet purpose for process facilities

## Construction

**Datasheet Package Structure:**

Per `_CONTEXT.md`, this deliverable includes three categories of valve datasheets:

### 1. Control Valve Data Sheets

**Typical Content (per ISA Form S20.50 or similar):**

**Identification Section:**
- Valve tag number (e.g., FV-1234, PCV-5678)
- Service description (e.g., "Product Transfer Flow Control," "Tank Pressure Control")
- P&ID number and reference
- Line number (from line list)
- Fail-safe action (FC = Fail Closed, FO = Fail Open, FL = Fail Last)

**Process Conditions:**
- Fluid: CSD canola oil (or other fluid)
- Operating/design flow rates: Normal, design, minimum (m³/h or gpm)
- Inlet pressure: Normal and design conditions (barg or psig)
- Outlet pressure: Normal and design conditions (barg or psig)
- Differential pressure across valve (bar or psi)
- Operating temperature (°C or °F)
- Fluid density (kg/m³ or lb/ft³)
- Viscosity (cSt or SSU)
- Vapor pressure (kPa or psia)

**Valve Sizing Data (from DEL-16.03 calculations):**
- Required Cv or Kv (at design conditions)
- Selected valve size (DN or NPS)
- Valve body style (globe, ball, butterfly)
- Trim type and characteristic (equal percentage, linear, quick-opening)
- Flow direction (flow-to-open or flow-to-close)
- Pressure drop at normal/design flow (bar or psi)
- Cavitation index (σ) and assessment
- Noise level prediction (dBA at 1 meter)
- Rangeability (turndown ratio)

**Valve Body Specifications:**
- Body material: **TBD** — **ASSUMPTION**: Stainless steel (316SS or 304SS) for canola oil service
- End connections: Flanged per ASME B16.5 (Class 150, 300, etc.)
- Flange facing: Raised face (RF) or ring-type joint (RTJ)
- Pressure-temperature rating: Per ASME B16.34
- Body style: Through-body (globe), rotary (ball, butterfly), angle

**Trim Specifications:**
- Trim material: **TBD** — Stainless steel or hardened stainless
- Seat material: **TBD** — Metal or soft-seated (PTFE, RTFE)
- Plug/disc material
- Stem material
- Packing material (graphite, PTFE)
- Leakage class: ANSI/FCI 70-2 Class IV (0.01% of Cv) or Class VI (tight shutoff)

**Actuator Specifications (from DEL-16.03 calculations):**
- Actuator type: Pneumatic (spring-return or double-acting), electric
- Actuator action: Air-to-open (ATO) or air-to-close (ATC)
- Fail-safe mode: FC, FO, or FL
- Actuator size/model (vendor-specific after procurement)
- Required torque/thrust (Nm or kN)
- Actuator output torque/thrust (Nm or kN)
- Safety factor achieved
- Air supply pressure (barg or psig) for pneumatic
- Stroking time (seconds)

**Instrumentation and Accessories:**
- Positioner: Smart digital positioner with 4–20 mA input; HART or Foundation Fieldbus communication — **TBD**
- Limit switches: Open/closed position indication (if required)
- Solenoid valve: For ESD function (if required)
- Air set: Filter, regulator, gauge (for pneumatic actuators)
- Manual override: Handwheel or declutching mechanism

**Standards and Codes:**
- Design code: IEC 60534 / ISA-75 series
- Flange standard: ASME B16.5
- Testing standard: IEC 60534-4 (control valve testing)
- Materials: ASTM standards for body, trim, bolting

**Manufacturer Data (post-procurement):**
- Manufacturer name
- Model number
- Serial number
- Certified Cv data
- Factory acceptance test (FAT) date and results
- Material certificates (MTRs)

**Source:** ISA Form S20.50 control valve datasheet format; typical content for EPC projects

### 2. Isolation Valve Data Sheets

**Typical Content:**

**Identification Section:**
- Valve tag number (e.g., XV-1234 for manual, MOV-5678 for motor-operated)
- Service description (e.g., "Product Line Isolation," "Pump Suction Isolation")
- P&ID number and reference
- Line number (from line list)
- Operation type: Manual, pneumatic, electric

**Process Conditions:**
- Fluid: CSD canola oil (or other fluid)
- Design flow rate (m³/h or gpm)
- Design pressure (barg or psig)
- Design temperature (°C or °F)
- Fluid density (kg/m³ or lb/ft³)
- Viscosity (cSt or SSU)

**Valve Specifications:**
- Valve type: Gate (rising stem, non-rising stem), ball (floating, trunnion-mounted), butterfly (wafer, lug, double-flanged)
- Valve size (DN or NPS)
- Pressure class: ASME Class 150, 300, etc.
- Body material: **TBD** — Stainless steel or carbon steel per service
- Trim material: **TBD** — Stainless steel or alloy
- Seat material: **TBD** — Soft-seated (PTFE, RTFE) or metal-seated
- End connections: Flanged, threaded, butt-weld, wafer
- Flange facing: Raised face (RF), flat face (FF)
- Stem type: Rising stem (gate), non-rising (butterfly), quarter-turn (ball)
- Packing: Graphite, PTFE
- Leakage class: API 598 or ISO 5208 Rate A (tight shutoff)
- Fire-safe: API 607 certification (if required for fire-critical services)

**Actuation (for automated isolation valves):**
- Actuator type: Pneumatic (spring-return, double-acting), electric (motor operator)
- Actuator action and fail-safe mode (if applicable)
- Actuator size/model (from DEL-16.03 calculations)
- Required torque (Nm or ft-lb)
- Actuator output torque
- Safety factor
- Stroking time (seconds)
- Air supply pressure (for pneumatic)
- Motor voltage and enclosure (for electric)

**Manual Operation (for manual valves):**
- Handwheel or gearbox
- Operating torque (Nm or ft-lb)
- Number of turns to open/close
- Open/closed position indication

**Standards and Codes:**
- Design code: API 600 (gate), API 608 (ball), API 609 (butterfly), API 6D (pipeline)
- Flange standard: ASME B16.5
- Testing standard: API 598 or ISO 5208
- Fire-safe standard: API 607 (if applicable)

**Manufacturer Data (post-procurement):**
- Manufacturer name and model
- Serial number
- Test certificates (pressure test, seat leakage test)
- Material certificates (MTRs)

**Source:** Typical isolation valve datasheet format for process facilities

### 3. Relief Valve Data Sheets

**Typical Content (per API 526 or ASME Section VIII requirements):**

**Identification Section:**
- Relief valve tag number (e.g., PSV-1234)
- Protected equipment tag (e.g., Tank TK-001, Vessel V-5678)
- P&ID number and reference
- Service description

**Protected Equipment Data:**
- Equipment type: Pressure vessel, piping section, heat exchanger, storage tank
- MAWP (Maximum Allowable Working Pressure): barg or psig
- Design pressure and temperature
- Volume (for thermal expansion scenario)
- Wetted surface area (for fire case scenario)

**Relief Scenario Data (from DEL-16.03 calculations):**
- Governing relief scenario: Thermal expansion, fire case, blocked discharge, etc.
- Required relief capacity: kg/h or lb/h (mass flow); m³/h or SCFM (volumetric flow)
- Relieving pressure: Set pressure + overpressure allowance
- Fluid state at relief: Liquid, vapor, two-phase

**Valve Sizing Data (from DEL-16.03 calculations):**
- Set pressure: psig or barg
- Set pressure tolerance: ±3 psi (for pressures ≤70 psig) or ±2% (for pressures >70 psig) per API 526
- Overpressure allowance: 10% (operating case) or 21% (fire case) per ASME Section VIII
- Accumulated pressure during relief
- Calculated required orifice area: mm² or in²
- Selected orifice designation: API 526 standard orifice (D, E, F, G, H, J, K, L, M, N, P, Q, R, T)
- Actual orifice area (from API 526 table)
- Relief valve capacity (certified capacity per ASME stamping)

**Valve Specifications:**
- Relief valve type: Conventional, balanced-bellows, pilot-operated
- Valve size: Inlet × outlet (e.g., NPS 3 × 4)
- Body material: **TBD** — Carbon steel or stainless steel per service temperature
- Spring material: Corrosion-resistant alloy (for coastal environment)
- Trim material: Stainless steel or special alloy
- Seat material: Metal or soft-seated (elastomer for low-pressure, metal for high-temperature)
- Inlet connection: Flanged per ASME B16.5; NPT threaded (small sizes)
- Outlet connection: Flanged or NPT
- Pressure-temperature rating: Per ASME B16.34
- ASME stamp: "UV" (pressure vessels) or "V" (piping) — **TBD** per protected equipment

**Discharge Arrangement (from DEL-16.01 valve arrangement drawings):**
- Discharge location: To atmosphere, to header, to containment system
- Discharge piping size (DN or NPS)
- Back pressure: Built-up back pressure from discharge piping (% of set pressure)
- Inlet piping loss: Pressure loss from equipment to relief valve inlet (% of set pressure)

**Testing and Certification:**
- Set pressure test: Cold differential test pressure (CDTP) adjusted for temperature
- Test medium: Air, nitrogen, water (for liquid service)
- Capacity certification: ASME stamped capacity per Section VIII
- Seat tightness: API 527 seat tightness test (if required)

**Standards and Codes:**
- Design code: ASME Section VIII Division 1 (pressure vessels), ASME B31.3 (piping), CSA B51 (Canadian code)
- Sizing standard: API 520/521
- Manufacturing standard: API 526 (flanged steel PRVs), API 527 (seat tightness)
- Testing standard: API 527

**Manufacturer Data (post-procurement):**
- Manufacturer name and model
- Serial number
- ASME National Board Number (stamped on valve)
- Set pressure test certificate (CDTP, test date, test medium, test results)
- Capacity certification (stamped capacity per ASME)
- Material certificates (MTRs for body, spring, trim)

**Regulatory Compliance:**
- CSA B51 registration: **TBD** — Relief valves protecting registered pressure vessels may require registration with Technical Safety BC
- National Board Registration: **TBD** — Per project requirements

**Source:** API 526 relief valve datasheet requirements; ASME Section VIII relief valve data requirements

**Materials Summary:**

- **Product-Contact Materials (CSD Canola Oil Service):**
  - **Preferred:** Stainless steel (316SS or 304SS) for food-grade cleanliness and corrosion resistance
  - **Body/Trim:** 316SS typical for product valves
  - **Gaskets/Seals:** PTFE, RTFE, or EPDM (food-grade elastomers)
  - **Bolting:** Stainless steel (ASTM A193 B8 or B8M)

- **Non-Product Materials (Utilities, Nitrogen, etc.):**
  - Carbon steel acceptable with external coating/painting per environmental conditions
  - Stainless steel preferred for coastal environment to reduce maintenance

**Source:** Material selection principles for food-grade service and coastal environment; specific materials TBD pending DEL-16.02 specification

**Interface Deliverables (see also Specification.md — Interface Requirements):**
- DEL-16.01 (Valve Design Drawing Set) — Valve arrangement drawings show valve locations and orientations per datasheets
- DEL-16.02 (Valve Technical Specification) — Procurement specifications define performance, materials, and workmanship requirements for valves in datasheets
- DEL-16.03 (Valve Design Calculations) — Sizing calculations provide Cv, set pressure, actuator size data for datasheets (see Procedure.md — Step 1 for data sources)
- DEL-16.05 (Valve Installation & Test Records) — Installation and test records reference valve datasheets for acceptance criteria
- DEL-14.01/14.02 (Process Piping Design) — Piping design provides line sizes, pressure classes, and piping interface data

**Source:** Interface requirements inferred from package structure; formal dependencies NOT_TRACKED per `_DEPENDENCIES.md`

**For datasheet development procedure, see Procedure.md. For datasheet requirements and verification methods, see Specification.md. For datasheet content guidance and examples, see Guidance.md.**

## References

**Reference Documents:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials

**Applicable Standards:**

**Datasheet Standards:**
- ISA Form S20.50 — Specification Forms for Process Measurement and Control Instruments (control valve datasheets)
- No equivalent standard form for isolation valves and relief valves; industry practice varies

**Valve Standards (for datasheet content):**
- API 600 — Steel Gate Valves
- API 608 — Metal Ball Valves
- API 609 — Butterfly Valves
- API 526 — Flanged Steel Pressure-Relief Valves
- IEC 60534 / ISA-75 series — Industrial-Process Control Valves
- ASME B16.34 — Valves – Flanged, Threaded, and Welding End

**Materials Standards:**
- ASTM A105/A350 — Carbon Steel Forgings
- ASTM A182 — Stainless Steel Forgings
- ASTM A351 — Stainless Steel Castings
- ASTM A193/A194 — Stainless Steel Bolting

**Canadian Codes:**
- CSA B51 — Boiler, Pressure Vessel and Pressure Piping Code (relief valve requirements)

**Project-Specific:**
- Employer's Requirements — **TBD** — **ASSUMPTION**: Volume 2 Parts 1–3 contain valve datasheet format and content requirements
- Project Engineering Standards — **TBD** — Datasheet templates and numbering system

**Source:** Standards inferred from Mechanical discipline and valve scope; applicability to be confirmed during datasheet development

**Cross-references:**
- See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
- Decomposition document: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section 5, PKG-16, DEL-16.04
