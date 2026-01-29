# Datasheet: DEL-20.02 Instrumentation Technical Specification

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-20.02 |
| Name | Instrumentation Technical Specification |
| Package | PKG-20 Field Instrumentation |
| Discipline | I&C |
| Type | Specification |
| Responsible | D&B Contractor |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |

## Attributes

| Attribute | Value |
|-----------|-------|
| Specification Type | Technical (performance, materials, workmanship) |
| Document Number | **TBD** — Per project document numbering system |
| Specification Format | **TBD** — **ASSUMPTION**: CSI MasterFormat or discipline-specific format |
| Revision Control | **TBD** — Per project document control procedures |
| Specification Scope | Field instrumentation (transmitters, switches, local indicators, instrument accessories) |
| Classification | **TBD** — **ASSUMPTION**: Procurement and construction specification |
| Applicable Use | Equipment procurement, construction execution, quality verification |

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-20, DEL-20.02 (line 497)

## Conditions

**Project Context:**

This technical specification supports the Canola Oil Transload Facility Phase 1 where Crude Super Degummed (CSD) grade canola oil transfers from rail tank cars to liquid bulk carriers for export.

**Source:** Decomposition document, Section 1.1 Project Overview

**Key Project Parameters:**

| Parameter | Value | Source |
|-----------|-------|--------|
| Permitted Throughput | 1,000,000 MT per annum | Decomposition, Section 1.1 |
| Storage Capacity | 45,000 MT (3 × 15,000 MT tanks) | Decomposition, Section 1.1 |
| Product Grade | CSD (Crude Super Degummed) canola oil | Decomposition, Section 1.1 |
| Railcar Capacity | 32 unloading stations on 2 tracks | Decomposition, Section 1.1 |

**Operating / Environmental Conditions:**

These conditions establish the basis for instrument performance and material selection:

- **Process Fluid:** CSD canola oil — **TBD**: Specific fluid properties (viscosity, density, vapor pressure) from Employer's Requirements
  - **Material Compatibility:** Stainless steel wetted parts typical for food-grade oil service — **ASSUMPTION**
  - **Temperature Sensitivity:** Canola oil viscosity varies with temperature (heating may be required for pumping)

- **Operating Temperature Range:** **TBD** — **ASSUMPTION**: -30°C to +50°C ambient (outdoor BC coastal climate); process temperature TBD from P&IDs

- **Operating Pressure Range:** **TBD** — From atmospheric (tank vents) to pump discharge pressures; to be confirmed from P&IDs and process design

- **Environmental Classification:** Marine/coastal environment
  - **Corrosion:** Salt air exposure requires corrosion-resistant materials and coatings
  - **Weathering:** Outdoor instruments require weatherproof enclosures (NEMA 4X typical)
  - **Temperature Cycling:** Freeze-thaw cycles, UV exposure, rain intrusion

**Source:** Project location (Fraser Surrey Terminal) and **ASSUMPTION** based on coastal BC environmental conditions

- **Hazardous Area Classification:** **TBD** — To be determined per facility hazardous area classification study
  - CSD canola oil is combustible (flash point typically >200°C) — may result in Class I, Division 2 / Zone 2 classification in vapor release areas
  - Electrical instrumentation shall comply with CSA C22.1 hazardous area requirements

**Source:** **ASSUMPTION** based on canola oil combustibility; **TBD**: Facility-specific hazardous area classification drawing

- **Seismic Requirements:** **TBD** — Per NBC 2015 and BC Building Code for Surrey, BC
  - Instrument mounting and support shall be seismically qualified

**Source:** **ASSUMPTION** based on Canadian regulatory requirements for BC jurisdiction

- **Design Life:** **TBD** — **ASSUMPTION**: 25 years minimum per typical industrial facility standards
  - Instrument selection shall consider lifecycle cost and maintainability (OBJ-9: Lifecycle Cost Optimization)

**Source:** Decomposition Section 2, OBJ-9 (line 66)

**Instrumentation Scope (PKG-20):**

Package includes field instruments, transmitters, switches, instrument cabling, and junction boxes.

**Source:** Decomposition document, PKG-20 Scope (line 490)

## Construction

**Specification Scope — Instrument Types:**

Based on facility function and anticipated artifacts, this technical specification addresses the following instrument categories:

### 1. Level Instruments

Application areas:
- **Storage tanks:** 3 × 15,000 MT tanks (tank gauging, high/low level alarms, overfill protection)
- **Process vessels:** Railcar unloading pits, pump sumps, day tanks
- **Marine loading:** Loading arm ullage monitoring

Typical technologies:
- Radar (non-contact, suitable for viscous fluids)
- Guided wave radar (contact, reliable for interface detection)
- Float-and-tape (mechanical backup)
- Level switches (high/low alarm points)

**Source:** Decomposition Key Parameters (storage tanks line 40, railcar stations line 43); **ASSUMPTION** based on typical bulk liquid terminal instrumentation

### 2. Pressure Instruments

Application areas:
- **Pump performance:** Suction and discharge pressure monitoring
- **Piping systems:** Pressure monitoring and control for safe operation
- **Loading operations:** Marine loading arm pressure control
- **Safety systems:** High/low pressure alarms and interlocks

Typical technologies:
- Pressure transmitters (4-20 mA analog, HART digital)
- Pressure switches (local alarm/interlock)
- Differential pressure transmitters (filter monitoring, flow measurement)

**Source:** **ASSUMPTION** based on facility pumping, transfer, and safety requirements

### 3. Temperature Instruments

Application areas:
- **Product quality:** Storage tank temperature monitoring (canola oil viscosity control)
- **Heating systems:** Tank heating control (if provided for viscosity management)
- **Equipment protection:** Pump bearing temperature, motor winding temperature
- **Environmental monitoring:** Ambient temperature for winterization

Typical technologies:
- RTDs (Pt100/Pt1000, high accuracy for custody transfer applications)
- Thermocouples (K-type for high-temperature applications)
- Temperature switches (local alarm/interlock)

**Source:** **ASSUMPTION** based on canola oil temperature sensitivity and typical process monitoring requirements

### 4. Flow Instruments (Supporting Role)

**Note:** Primary flow metering for custody transfer is addressed in PKG-12 (Product Transfer and Metering). This specification may address:
- Process control flow measurement (non-custody transfer)
- Flow switches for pump protection and flow verification
- Coordination with custody transfer metering requirements

**Source:** Cross-reference to PKG-12 per decomposition (lines 259-268); **ASSUMPTION** on scope boundary

### 5. Instrument Accessories

Supporting components specified herein:
- Instrument valves (isolation, drain, vent, calibration)
- Instrument tubing and fittings (stainless steel, marine-grade)
- Instrument enclosures and junction boxes (NEMA/IP rated)
- Cable glands and sealing (hazardous area compliance)
- Mounting hardware and supports (seismic qualification)

**Source:** **ASSUMPTION** based on typical instrumentation package scope

**Anticipated Specification Artifacts:**

1. **Level Instrument Specification**
   - Level transmitter types, ranges, accuracies
   - Level switch types and alarm point requirements
   - Tank gauging system requirements (if applicable)
   - **TBD**: Specification section structure and content detail

2. **Pressure Instrument Specification**
   - Pressure transmitter types, ranges, accuracies
   - Pressure switch types and setpoint requirements
   - Differential pressure instrument applications
   - **TBD**: Specification section structure and content detail

3. **Temperature Specification**
   - Temperature element types (RTD, thermocouple) and accuracies
   - Temperature switch types and setpoint requirements
   - Thermowell requirements and installation
   - **TBD**: Specification section structure and content detail

**Source:** Decomposition DEL-20.02 Anticipated Artifacts (line 497); `_CONTEXT.md`

**Material Requirements (General):**

- **Wetted Parts:** Stainless steel (316/316L typical) for canola oil compatibility and corrosion resistance
- **Enclosures:** Stainless steel or aluminum with marine-grade coating, NEMA 4X / IP66 minimum
- **Wiring/Cable:** Per CSA C22.1 for hazardous area installations (IS barriers or XP enclosures)
- **Instrument Tubing:** Stainless steel (316/316L), seamless, pressure-rated per application
- **Gaskets/Seals:** Food-grade materials compatible with canola oil (if process contact)

**Source:** **ASSUMPTION** based on marine environment, canola oil service, and typical bulk terminal material standards

**Workmanship Requirements (General):**

- Installation per manufacturer instructions and industry standards (ISA, API)
- Welding and threaded connections per applicable piping codes (CSA Z662, ASME B31.3 — **TBD**)
- Hazardous area installations per CSA C22.1 (conduit sealing, cable gland selection)
- Calibration and testing per manufacturer requirements and project commissioning procedures (see DEL-20.05)

**Source:** **ASSUMPTION** based on typical technical specification content for EPC projects

## References

**Primary References:**

- Decomposition document: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (Section PKG-20)
- `_CONTEXT.md` — Deliverable identity and scope
- `_REFERENCES.md` — Additional reference materials (currently: no references identified)
- Employer's Requirements — **TBD**: Specific sections to be identified from Vol 2 Parts 1-3

**Applicable I&C Standards:**

- **ISA 5.1** — Instrumentation Symbols and Identification — **ASSUMPTION**: Tagging and identification conventions
- **ISA 84 / IEC 61511** — Functional Safety (SIS) — **ASSUMPTION**: If safety instrumented functions are required
- **API 554** — Process Instrumentation and Control — **ASSUMPTION**: Industry good practice for instrument selection and installation
- **CSA C22.1** — Canadian Electrical Code — **ASSUMPTION**: Hazardous area installations, wiring requirements
- **NFPA 70** (NEC) — National Electrical Code — **ASSUMPTION**: Referenced by CSA C22.1 for some requirements

**Instrument-Specific Standards:**

- **API 2350** — Overfill Protection for Storage Tanks — **ASSUMPTION**: Applicable for tank level instrumentation and overfill prevention
- **OIML R117** / **API MPMS Chapter 3** — Tank gauging and custody transfer — **ASSUMPTION**: If custody transfer measurement is included in scope (coordinate with PKG-12)

**Note:** Standards applicability to be confirmed based on Employer's Requirements and project specification. Specific clause-level requirements **TBD** pending access to standard documents.

**Related Deliverables:**

- **DEL-20.01** — Instrumentation Design Drawing Set (installation arrangements implement this specification)
- **DEL-20.03** — Instrumentation Design Calculations (calculations verify specification compliance)
- **DEL-20.04** — Instrumentation Data Sheet Package (equipment data sheets demonstrate specification compliance)
- **DEL-20.05** — Instrumentation Installation & Test Records (commissioning verifies specification compliance)

**Source:** Decomposition document, PKG-20 deliverables (lines 496-500)

**Dependencies:**

See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies coordinated externally by humans per project coordination plan.

**Project Objective Alignment:**

This deliverable supports **OBJ-1: Safe & Reliable Operation** — Proper specification of instrument performance, materials, and workmanship ensures safe and reliable facility operations.

**Source:** Decomposition document, Section 6 Objective-to-Deliverable Mapping (line 780)
