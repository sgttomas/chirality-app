# Datasheet: DEL-20.01 Instrumentation Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-20.01 |
| Name | Instrumentation Design Drawing Set |
| Package | PKG-20 Field Instrumentation |
| Discipline | I&C |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |

## Attributes

| Attribute | Value |
|-----------|-------|
| Drawing Type | Instrumentation arrangement and installation details |
| Drawing Scale | **TBD** — **ASSUMPTION**: Typical scales 1:50, 1:100 for plans; NTS for details |
| Sheet Size | **TBD** — **ASSUMPTION**: ISO A1 or ANSI D per project CAD standards |
| CAD Standard | **TBD** — To be confirmed per project document management plan |
| Drawing Format | **TBD** — **ASSUMPTION**: Electronic PDF/DWG per project requirements |
| Revision Control | **TBD** — Per project document control procedures |
| Classification | **TBD** — **ASSUMPTION**: Contractor's Design Documents (for construction) |

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-20, DEL-20.01 (line 496)

## Conditions

**Project Context:**

This drawing set supports the Canola Oil Transload Facility Phase 1 where Crude Super Degummed (CSD) grade canola oil transfers from rail tank cars to liquid bulk carriers for export.

**Source:** Decomposition document, Section 1.1 Project Overview

**Key Project Parameters:**

| Parameter | Value | Source |
|-----------|-------|--------|
| Permitted Throughput | 1,000,000 MT per annum | Decomposition, Section 1.1 |
| Storage Capacity | 45,000 MT (3 × 15,000 MT tanks) | Decomposition, Section 1.1 |
| Product Grade | CSD (Crude Super Degummed) canola oil | Decomposition, Section 1.1 |
| Railcar Capacity | 32 unloading stations on 2 tracks | Decomposition, Section 1.1 |

**Operating / Environmental Context:**

- **Location:** Marine terminal environment, British Columbia coast — **TBD**: Specific environmental design parameters from Employer's Requirements
- **Operating temperature range:** **TBD** — **ASSUMPTION**: Outdoor instrumentation rated for -30°C to +50°C (typical BC coastal range)
- **Environmental classification:** **TBD** — Marine/coastal exposure with corrosion considerations
- **Hazardous area classification:** **TBD** — To be determined per facility hazardous area classification study (CSD canola oil vapor considerations)
- **Seismic requirements:** **TBD** — **ASSUMPTION**: Per NBC 2015 and BC Building Code for Surrey, BC location
- **Design life:** **TBD** — **ASSUMPTION**: 25 years minimum per typical industrial facility standards

**Instrumentation Scope:**

Package PKG-20 scope includes field instruments, transmitters, switches, instrument cabling, and junction boxes.

**Source:** Decomposition document, Section PKG-20 Scope (line 490)

## Construction

**Anticipated Drawing Artifacts:**

The following drawing types shall be produced as part of this deliverable:

1. **Instrument location plans** — Show spatial arrangement of field instruments on facility plans
   - **TBD**: Drawing list and numbering to be established per project standards

2. **Instrument installation details** — Provide installation mounting and connection details for field instruments
   - **TBD**: Detail drawing standards and typical details library

3. **Cable schedules** — Define instrument cable routing, terminations, and specifications
   - **TBD**: Cable schedule format and database integration

**Source:** Decomposition document, DEL-20.01 Anticipated Artifacts (line 496); `_CONTEXT.md`

**Instrumentation Types (Typical):**

Based on facility scope, instrumentation drawings will address:
- Level transmitters (storage tanks, process vessels)
- Pressure transmitters (piping systems, loading arms)
- Flow instruments (custody transfer metering, process control)
- Temperature instruments (product monitoring, tank heating)
- Switches and local indicators

**Source:** **ASSUMPTION** based on PKG-20 scope (field instruments, transmitters, switches) and facility function (storage, transfer, metering)

**Installation Requirements:**

- Instrument mounting: **TBD** — Per manufacturer requirements and ISA standards
- Cable routing: **TBD** — Underground duct banks, cable trays, conduit systems (coordinate with PKG-23 Electrical Infrastructure)
- Junction boxes: **TBD** — Locations and environmental ratings per hazardous area classification
- Weatherproofing: **TBD** — Outdoor instrument enclosures and environmental protection

**Commissioning Interface:**

Installation details shall support loop checking and calibration activities per DEL-20.05 Instrumentation Installation & Test Records.

**Source:** Cross-reference to DEL-20.05 per decomposition (line 500)

## References

**Primary References:**

- Decomposition document: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (Section PKG-20)
- `_CONTEXT.md` — Deliverable identity and scope
- `_REFERENCES.md` — Additional reference materials (currently: no references identified)
- Employer's Requirements — **TBD**: Specific sections to be identified from Vol 2 Parts 1-3

**Applicable I&C Standards:**

- **ISA 5.1** — Instrumentation Symbols and Identification — **ASSUMPTION**: Applicable for P&ID and instrumentation drawing symbology
- **ISA 84** / **IEC 61511** — Functional Safety (SIS) — **ASSUMPTION**: Applicable if safety instrumented systems are included in facility design
- **CSA C22.1** — Canadian Electrical Code — **ASSUMPTION**: Applicable for instrument wiring and hazardous area installations in BC
- **API 554** — Process Instrumentation and Control — **ASSUMPTION**: Applicable for process industry instrumentation practices

**Note:** Standards applicability to be confirmed based on Employer's Requirements and project specification. Specific clause-level requirements **TBD** pending access to standard documents.

**Related Deliverables:**

- DEL-20.02 — Instrumentation Technical Specification (performance and material requirements)
- DEL-20.03 — Instrumentation Design Calculations (sizing and verification basis)
- DEL-20.04 — Instrumentation Data Sheet Package (equipment data sheets)
- DEL-20.05 — Instrumentation Installation & Test Records (commissioning documentation)

**Source:** Decomposition document, PKG-20 deliverables (lines 496-500)

**Dependencies:**

See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies coordinated externally by humans per project coordination plan.

**Project Objective Alignment:**

This deliverable supports **OBJ-1: Safe & Reliable Operation** — The facility is suitable for safe, efficient, reliable, and continuous use under actual operational conditions.

**Source:** Decomposition document, Section 6 Objective-to-Deliverable Mapping (line 780)
