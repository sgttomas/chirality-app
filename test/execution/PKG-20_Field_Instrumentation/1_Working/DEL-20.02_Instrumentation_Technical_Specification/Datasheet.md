# Datasheet: DEL-20.02 Instrumentation Technical Specification

## Identification

| Field | Value | Specification § | Guidance § | Procedure Step |
|-------|-------|-----------------|------------|----------------|
| Deliverable ID | DEL-20.02 | Scope | Purpose | 1.1 |
| Name | Instrumentation Technical Specification | Scope | Purpose | 1.1 |
| Package | PKG-20 Field Instrumentation | Scope | Purpose | — |
| Discipline | I&C | Scope | Purpose | Prerequisites |
| Type | Specification | Scope | Downstream Use | 1.2 |
| Responsible | D&B Contractor | Scope | Purpose | Prerequisites |
| Status | INITIALIZED | — | — | — |
| Project | Canola Oil Transload Facility — Phase 1 | Scope | Purpose | 1.1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC | FR-3, FR-4 | Principle 3 | 1.3 |

## Attributes

| Attribute | Value | Specification § | Guidance § | Procedure Step |
|-----------|-------|-----------------|------------|----------------|
| Specification Type | Technical (performance, materials, workmanship) | Scope | Principle 1 | 1.2 |
| Document Number | **TBD** — Per project document numbering system | Documentation | — | 5.2 |
| Specification Format | **TBD** — **ASSUMPTION**: CSI MasterFormat or discipline-specific format | Documentation | — | 5.2 |
| Revision Control | **TBD** — Per project document control procedures | — | — | 5.6 |
| Specification Scope | Field instrumentation (transmitters, switches, local indicators, instrument accessories) | Scope | Principle 2 | 2.1-2.4 |
| Classification | **TBD** — **ASSUMPTION**: Procurement and construction specification | Documentation | Downstream Use | 5.1 |
| Applicable Use | Equipment procurement, construction execution, quality verification | INT-3, INT-4 | Downstream Use | 5.4, 5.5 |

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-20, DEL-20.02 (line 497)

## Conditions

**Project Context:**

This technical specification supports the Canola Oil Transload Facility Phase 1 where Crude Super Degummed (CSD) grade canola oil transfers from rail tank cars to liquid bulk carriers for export.

**Source:** Decomposition document, Section 1.1 Project Overview

**Key Project Parameters:**

| Parameter | Value | Source | Specification § | Guidance § |
|-----------|-------|--------|-----------------|------------|
| Permitted Throughput | 1,000,000 MT per annum | Decomposition, Section 1.1 | FR-2, FR-3 | Throughput and Storage Scale |
| Storage Capacity | 45,000 MT (3 × 15,000 MT tanks) | Decomposition, Section 1.1 | FR-2 | Storage Tanks Example |
| Product Grade | CSD (Crude Super Degummed) canola oil | Decomposition, Section 1.1 | FR-2, FR-3, FR-4 | Facility Type |
| Railcar Capacity | 32 unloading stations on 2 tracks | Decomposition, Section 1.1 | FR-2 | Railcar Unloading Example |

**Operating / Environmental Conditions:**

These conditions establish the basis for instrument performance and material selection:

| Condition | Value | Source | Specification § | Guidance § |
|-----------|-------|--------|-----------------|------------|
| Process Fluid | CSD canola oil — **TBD**: Specific fluid properties (viscosity, density, vapor pressure) | **TBD**: ER | FR-2 to FR-5 | Facility Type |
| Material Compatibility | Stainless steel wetted parts typical for food-grade oil service | **ASSUMPTION** | PR-2 | Principle 3, Level Instruments |
| Operating Temperature Range | **TBD** — **ASSUMPTION**: -30°C to +50°C ambient (outdoor BC coastal climate) | **ASSUMPTION** | PR-2 | Principle 3 |
| Operating Pressure Range | **TBD** — From atmospheric to pump discharge pressures | Process design | FR-3 | Pressure Instruments |
| Environmental Classification | Marine/coastal environment (salt air, weathering, temperature cycling) | Project location | PR-2 | Principle 3 |
| Hazardous Area Classification | **TBD** — CSD canola oil is combustible; Class I, Div 2 / Zone 2 likely | **TBD**: Classification study | PR-3 | Principle 4 |
| Seismic Requirements | **TBD** — Per NBC 2015 and BC Building Code for Surrey, BC | **ASSUMPTION** | PR-4 | — |
| Design Life | **TBD** — **ASSUMPTION**: 25 years minimum | **ASSUMPTION** | PR-5 | Principle 5 |

**Instrumentation Scope (PKG-20):**

Package includes field instruments, transmitters, switches, instrument cabling, and junction boxes.

**Source:** Decomposition document, PKG-20 Scope (line 490)

## Construction

**Specification Scope — Instrument Types:**

Based on facility function and anticipated artifacts, this technical specification addresses the following instrument categories:

### 1. Level Instruments

| Application Area | Description | Specification § | Guidance § |
|------------------|-------------|-----------------|------------|
| Storage tanks | 3 × 15,000 MT tanks (tank gauging, high/low level alarms, overfill protection) | FR-2 | Trade-off 1, Storage Tanks Example |
| Process vessels | Railcar unloading pits, pump sumps, day tanks | FR-2 | Level Instruments |
| Marine loading | Loading arm ullage monitoring | FR-2 | Marine Loading Example |

**Typical Technologies:**

| Technology | Characteristics | Guidance § |
|------------|-----------------|------------|
| Radar (non-contact) | Suitable for viscous fluids, no moving parts | Trade-off 1 |
| Guided wave radar (contact) | Reliable for interface detection | Trade-off 1 |
| Float-and-tape | Mechanical backup | Trade-off 1 |
| Level switches | High/low alarm points | Level Instruments |

**Source:** Decomposition Key Parameters (storage tanks line 40, railcar stations line 43); **ASSUMPTION** based on typical bulk liquid terminal instrumentation

### 2. Pressure Instruments

| Application Area | Description | Specification § | Guidance § |
|------------------|-------------|-----------------|------------|
| Pump performance | Suction and discharge pressure monitoring | FR-3 | Pressure Instruments |
| Piping systems | Pressure monitoring and control for safe operation | FR-3 | Pressure Instruments |
| Loading operations | Marine loading arm pressure control | FR-3 | Marine Loading Example |
| Safety systems | High/low pressure alarms and interlocks | FR-3 | Principle 4 |

**Typical Technologies:**

| Technology | Characteristics | Guidance § |
|------------|-----------------|------------|
| Pressure transmitters | 4-20 mA analog, HART digital | Pressure Instruments |
| Pressure switches | Local alarm/interlock | Pressure Instruments |
| Differential pressure transmitters | Filter monitoring, flow measurement | Pressure Instruments |

**Source:** **ASSUMPTION** based on facility pumping, transfer, and safety requirements

### 3. Temperature Instruments

| Application Area | Description | Specification § | Guidance § |
|------------------|-------------|-----------------|------------|
| Product quality | Storage tank temperature monitoring (canola oil viscosity control) | FR-4 | Temperature Instruments |
| Heating systems | Tank heating control (if provided for viscosity management) | FR-4 | Temperature Instruments |
| Equipment protection | Pump bearing temperature, motor winding temperature | FR-4 | Temperature Instruments |
| Environmental monitoring | Ambient temperature for winterization | FR-4 | — |

**Typical Technologies:**

| Technology | Characteristics | Guidance § |
|------------|-----------------|------------|
| RTDs (Pt100/Pt1000) | High accuracy for custody transfer applications | Temperature Instruments |
| Thermocouples (K-type) | High-temperature applications | Temperature Instruments |
| Temperature switches | Local alarm/interlock | Temperature Instruments |

**Source:** **ASSUMPTION** based on canola oil temperature sensitivity and typical process monitoring requirements

### 4. Flow Instruments (Supporting Role)

**Note:** Primary flow metering for custody transfer is addressed in PKG-12 (Product Transfer and Metering). This specification may address:
- Process control flow measurement (non-custody transfer)
- Flow switches for pump protection and flow verification
- Coordination with custody transfer metering requirements

**Source:** Cross-reference to PKG-12 per decomposition (lines 259-268); **ASSUMPTION** on scope boundary

### 5. Instrument Accessories

| Component | Description | Specification § | Guidance § |
|-----------|-------------|-----------------|------------|
| Instrument valves | Isolation, drain, vent, calibration | FR-5 | — |
| Instrument tubing | Stainless steel, marine-grade | FR-5 | Principle 3 |
| Instrument enclosures | NEMA/IP rated | FR-5, PR-2 | Principle 3 |
| Cable glands and seals | Hazardous area compliance | FR-5, PR-3 | Principle 4 |
| Mounting hardware | Seismic qualification | FR-5, PR-4 | — |

**Source:** **ASSUMPTION** based on typical instrumentation package scope

**Anticipated Specification Artifacts:**

| Artifact | Content | Specification § | Procedure Step |
|----------|---------|-----------------|----------------|
| Level Instrument Specification | Level transmitter types, ranges, accuracies; level switch types; tank gauging system requirements | FR-2, Documentation | 2.1 |
| Pressure Instrument Specification | Pressure transmitter types, ranges, accuracies; pressure switch types; differential pressure applications | FR-3, Documentation | 2.2 |
| Temperature Specification | Temperature element types and accuracies; temperature switch types; thermowell requirements | FR-4, Documentation | 2.3 |

**Source:** Decomposition DEL-20.02 Anticipated Artifacts (line 497); `_CONTEXT.md`

**Material Requirements (General):**

| Material | Application | Specification § | Guidance § |
|----------|-------------|-----------------|------------|
| 316/316L stainless steel | Wetted parts (canola oil compatibility, corrosion resistance) | PR-2 | Principle 3 |
| Stainless steel or marine aluminum | Enclosures (NEMA 4X / IP66 minimum) | PR-2 | Principle 3 |
| Per CSA C22.1 | Wiring/cable (hazardous area installations) | PR-3 | Principle 4 |
| Stainless steel seamless | Instrument tubing (pressure-rated per application) | PR-2 | — |
| Food-grade compatible | Gaskets/seals (if process contact) | PR-2 | Facility Type |

**Source:** **ASSUMPTION** based on marine environment, canola oil service, and typical bulk terminal material standards

**Workmanship Requirements (General):**

| Requirement | Standard | Specification § | Procedure Step |
|-------------|----------|-----------------|----------------|
| Installation | Per manufacturer instructions and industry standards (ISA, API) | QR-4 | 5.5 |
| Welding/connections | Per applicable piping codes (CSA Z662, ASME B31.3 — **TBD**) | QR-4 | 5.5 |
| Hazardous area | Per CSA C22.1 (conduit sealing, cable gland selection) | PR-3, QR-4 | 5.5 |
| Calibration/testing | Per manufacturer requirements and DEL-20.05 commissioning procedures | QR-2 | Verification |

**Source:** **ASSUMPTION** based on typical technical specification content for EPC projects

## References

**Primary References:**

| Reference | Location | Specification § | Guidance § |
|-----------|----------|-----------------|------------|
| Decomposition document | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (Section PKG-20) | Scope | Purpose |
| `_CONTEXT.md` | Deliverable folder | Scope | Purpose |
| `_REFERENCES.md` | Deliverable folder — currently: no references identified | — | — |
| Employer's Requirements | **TBD**: Specific sections from Vol 2 Parts 1-3 | Standards | Standards Context |

**Applicable I&C Standards:**

| Standard | Description | Applicability | Specification § | Guidance § |
|----------|-------------|---------------|-----------------|------------|
| ISA 5.1 | Instrumentation Symbols and Identification | **ASSUMPTION**: Tagging and identification conventions | Standards | Standards Context |
| ISA 84 / IEC 61511 | Functional Safety (SIS) | **ASSUMPTION**: If safety instrumented functions required | Standards | Standards Context |
| API 554 | Process Instrumentation and Control | **ASSUMPTION**: Industry good practice | Standards | Standards Context |
| API 2350 | Overfill Protection for Storage Tanks | **ASSUMPTION**: Tank overfill prevention | Standards | Standards Context |
| CSA C22.1 | Canadian Electrical Code | **ASSUMPTION**: Hazardous area installations | Standards | Standards Context |
| NFPA 70 (NEC) | National Electrical Code | **ASSUMPTION**: Referenced by CSA C22.1 | Standards | — |

**Note:** Standards applicability to be confirmed based on Employer's Requirements and project specification. Specific clause-level requirements **TBD** pending access to standard documents.

**Related Deliverables:**

| Deliverable | Relationship | Specification § |
|-------------|--------------|-----------------|
| DEL-20.01 | Instrumentation Design Drawing Set — installation arrangements implement this specification | INT-2 |
| DEL-20.03 | Instrumentation Design Calculations — calculations verify specification compliance | INT-2 |
| DEL-20.04 | Instrumentation Data Sheet Package — equipment data sheets demonstrate specification compliance | INT-2 |
| DEL-20.05 | Instrumentation Installation & Test Records — commissioning verifies specification compliance | INT-2 |

**Source:** Decomposition document, PKG-20 deliverables (lines 496-500)

**Interface Packages:**

| Package | Interface Description | Specification § |
|---------|----------------------|-----------------|
| PKG-12 Product Transfer and Metering | Custody transfer metering requirements | INT-1 |
| PKG-13 Storage Tanks | Tank instrumentation, nozzle sizes and locations | INT-1 |
| PKG-14 Process Piping | Instrument connections, taps, piping design pressures | INT-1 |
| PKG-15 Pumps and Rotating Equipment | Equipment instrumentation | INT-1 |
| PKG-17 Electrical Power Distribution | Instrument power supply requirements | INT-1 |
| PKG-22 Control Systems & SCADA | Signal types, I/O requirements, communication protocols | INT-1 |
| PKG-23 Electrical Infrastructure | Cable routing infrastructure, junction boxes | INT-1 |

**Dependencies:**

See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies coordinated externally by humans per project coordination plan.

**Project Objective Alignment:**

| Objective | Description | How Supported |
|-----------|-------------|---------------|
| OBJ-1 | Safe & Reliable Operation | Proper specification of instrument performance, materials, and workmanship ensures safe, reliable operations |
| OBJ-6 | Regulatory Compliance | Specifications ensure compliance with CSA C22.1, API 2350, and other requirements |
| OBJ-9 | Lifecycle Cost Optimization | Fit-for-purpose specifications balance capital cost with maintenance cost |
| OBJ-10 | Custody Transfer Accuracy | Specifications support accurate product metering (coordinate with PKG-12) |

**Source:** Decomposition document, Section 6 Objective-to-Deliverable Mapping (line 780)

## Cross-Document Traceability

This Datasheet provides the factual identification, attributes, conditions, and references for DEL-20.02. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Specification.md | Requirements and verification criteria | FR-1 to FR-5 define functional requirements; PR-1 to PR-5 define performance requirements; INT-1 to INT-4 define interfaces |
| Guidance.md | Engineering rationale and decision context | Principles 1-5 explain design rationale; Trade-offs 1-6 address key design decisions; Examples illustrate application |
| Procedure.md | Production workflow and verification steps | Steps 1-5 define production process; Verification section defines acceptance criteria; Records section defines outputs |

**Document Consistency Verification:**

- All instrument types listed in Datasheet appear in Specification FR-2 to FR-5 and Guidance Technical Considerations
- All interface packages listed in Datasheet appear in Specification INT-1 and Guidance Coordination Considerations
- All standards listed in Datasheet appear in Specification Standards section and Guidance Standards Context
- All related deliverables listed in Datasheet appear in Specification INT-2 and Procedure Integration section
- Material requirements in Datasheet align with Specification PR-2 and Guidance Principle 3
