# Datasheet: DEL-16.01 Valve Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-16.01 |
| Name | Valve Design Drawing Set |
| Package | PKG-16 Valves & Specialty Equipment |
| Discipline | Mechanical |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md`

## Attributes

| Attribute | Value |
|-----------|-------|
| Drawing Types | Valve arrangement drawings, actuator details |
| Valve Categories Covered | Control valves, isolation valves, relief valves, strainers, specialty items |
| Drawing Number Prefix | **TBD** — Per project drawing numbering system |
| Sheet Size | **TBD** — **ASSUMPTION**: ISO A1 or ANSI D typical for mechanical drawings |
| Scale | **TBD** — **ASSUMPTION**: As required per drawing type (arrangement typically 1:50 or 1:100, details as required) |
| CAD Standard | **TBD** — Per project CAD standards manual |
| Revision | **TBD** — Initial issue for construction |
| Classification | **TBD** — **ASSUMPTION**: For Construction or Contractor's Use based on project phase |
| Applicable Systems | Railcar unloading, marine loading, product transfer, storage tank systems |

**Source:** `_CONTEXT.md` (anticipated artifacts); PKG-16 scope from decomposition (location TBD — see Section 5, PKG-16 entry)

## Conditions

**Operating / Environmental Context:**

This drawing set supports the canola oil transload facility (1,000,000 MT/annum throughput) at Fraser Surrey Terminal, Surrey, BC.

**Source:** Decomposition document Section 1.1 (Project Overview)

**Process Fluid:**
- Product: CSD (Crude Super Degummed) canola oil
- Operating temperature: **TBD** — Typical range for canola oil handling **ASSUMPTION**: -10°C to +50°C ambient, heated product lines where required
- Operating pressure: **TBD** — To be defined per system (railcar unloading, marine loading, tank farm)

**Source:** Decomposition document Section 1.1 (product grade); temperature/pressure ranges TBD pending system design

**Environmental:**
- Location: Fraser Surrey Terminal (marine/industrial environment)
- Environmental classification: **TBD** — **ASSUMPTION**: Coastal/marine atmosphere, corrosion category C4 or C5-M per ISO 12944
- Seismic zone: **TBD** — **ASSUMPTION**: High seismic zone per NBCC (BC location)
- Design life: **TBD** — **ASSUMPTION**: 25 years typical for industrial facility

**Source:** Decomposition document Section 1.1 (location); environmental/seismic parameters TBD pending design basis

**Hazardous Area:**
- Classification: **TBD** — To be confirmed per facility hazardous area classification study
- **ASSUMPTION**: Valves in process areas likely Class I, Division 2 or Zone 2; non-hazardous in remote locations

## Construction

**Materials / Configuration:**

**Valve Types (per PKG-16 scope):**
- Control valves: Flow control, pressure control, level control applications
- Isolation valves: Manual and automated shutoff valves (gate, ball, butterfly)
- Relief valves: Pressure relief, thermal relief
- Strainers: Y-type, basket-type
- Specialty items: **TBD** — Special service valves, check valves, etc.

**Source:** Decomposition document Section 5, PKG-16 scope (location TBD)

**Drawing Content:**
- Valve arrangement drawings: Overall valve location and orientation within process systems
- Actuator details: Pneumatic, electric, hydraulic actuator installations and mounting arrangements
- Valve body materials: **TBD** — **ASSUMPTION**: Carbon steel, stainless steel per service requirements
- Trim materials: **TBD** — Per service conditions and process compatibility
- Actuation types: **TBD** — Pneumatic, electric, manual per application
- Piping connections: **TBD** — Flanged, threaded, welded per line size and pressure class

**Source:** `_CONTEXT.md` (anticipated artifacts); materials/actuation TBD pending design development

**Installation Requirements:**
- Foundation/support requirements: **TBD** — Per valve size and type
- Access requirements: **TBD** — Per operability and maintenance needs
- Commissioning requirements: **TBD** — Functional testing, set pressure verification (relief valves)

**Interface Deliverables (see also Specification.md — Interface Requirements):**
- DEL-14.01 (Process Piping Design Drawing Set) — Piping interface (see Procedure.md — Step 5 for piping coordination)
- DEL-14.02 (Process Piping Technical Specification) — Piping material specification
- DEL-19.01 (Control System Design Drawing Set) — Control valve interface (see Procedure.md — Step 5 for control systems coordination)
- DEL-20.01 (Instrumentation Design Drawing Set) — Instrumentation tie-ins (see Procedure.md — Step 5 for instrumentation coordination)

**Source:** Interface requirements inferred from package scope; formal dependencies NOT_TRACKED per `_DEPENDENCIES.md`

**For drawing production procedure, see Procedure.md. For drawing requirements and verification methods, see Specification.md.**

## References

**Reference Documents:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials

**Applicable Standards:**
- ASME B31.3 — Process Piping
- API 600/API 6D — Valves (gate, ball valves)
- API 526/API 527 — Pressure Relief Valves
- API 598 — Valve Inspection and Testing
- ASME Section VIII — Pressure Vessels (where applicable)
- CSA B51 — Boiler, Pressure Vessel and Pressure Piping Code
- ISA-75 — Control Valve Standards
- NACE MR0175/ISO 15156 — Materials for Sour Service (if applicable)

**Source:** Standards inferred from Mechanical discipline and valve scope; specific applicability TBD pending design basis

**Cross-references:**
- See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
- Decomposition document: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section 5, PKG-16, DEL-16.01
