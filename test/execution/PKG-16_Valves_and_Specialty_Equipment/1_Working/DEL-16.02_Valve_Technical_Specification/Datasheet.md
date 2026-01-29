# Datasheet: DEL-16.02 Valve Technical Specification

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-16.02 |
| Name | Valve Technical Specification |
| Package | PKG-16 Valves & Specialty Equipment |
| Discipline | Mechanical |
| Type | Specification |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md`

## Attributes

| Attribute | Value |
|-----------|-------|
| Document Number | **TBD** — Per project specification numbering system |
| Specification Type | Technical/Procurement Specification (performance, materials, workmanship) |
| Valve Categories | Control valves, isolation valves, relief valves, strainers, specialty items |
| Specification Format | **TBD** — **ASSUMPTION**: Separate specifications per valve category or unified specification with sections |
| Revision | **TBD** — Initial issue for procurement |
| Classification | **TBD** — **ASSUMPTION**: Contractor's Use or For Procurement |
| Applicable Systems | Railcar unloading, marine loading, product transfer, storage tank systems |

**Source:** `_CONTEXT.md` (anticipated artifacts); PKG-16 scope from decomposition (location TBD — Section 5, PKG-16)

## Conditions

**Operating / Environmental Context:**

This specification supports valve procurement for the canola oil transload facility (1,000,000 MT/annum throughput) at Fraser Surrey Terminal, Surrey, BC.

**Source:** Decomposition document Section 1.1 (Project Overview)

**Process Fluid:**
- Product: CSD (Crude Super Degummed) canola oil
- Operating temperature: **TBD** — Typical range for canola oil handling **ASSUMPTION**: -10°C to +50°C ambient, heated product lines where required (40–60°C typical for viscosity control)
- Operating pressure: **TBD** — To be defined per system:
  - Railcar unloading: Gravity feed + pump suction/discharge (TBD)
  - Marine loading: Pump discharge to loading arm (TBD)
  - Storage tanks: Atmospheric to low pressure (TBD)
- Viscosity: **TBD** — Canola oil viscosity varies with temperature (higher at lower temperatures)

**Source:** Decomposition document Section 1.1 (product grade); temperature/pressure/viscosity ranges TBD pending system design

**Environmental:**
- Location: Fraser Surrey Terminal (marine/industrial environment)
- Environmental classification: **TBD** — **ASSUMPTION**: Coastal/marine atmosphere, corrosion category C4 or C5-M per ISO 12944
- Ambient temperature range: **TBD** — Fraser Surrey climate (typical: -10°C to +30°C)
- Seismic zone: **TBD** — **ASSUMPTION**: High seismic zone per NBCC (BC location)
- Design life: **TBD** — **ASSUMPTION**: 25 years typical for industrial facility

**Source:** Decomposition document Section 1.1 (location); environmental/seismic parameters TBD pending design basis

**Hazardous Area:**
- Classification: **TBD** — To be confirmed per facility hazardous area classification study
- **ASSUMPTION**: Process areas likely Class I, Division 2 or Zone 2 (Group D); actuators and accessories shall be rated accordingly

**Service Categories:**
1. **Control Valve Service:** Modulating flow, pressure, and level control; frequent operation; automated actuation
2. **Isolation Valve Service:** Infrequent operation (maintenance isolation, seasonal startup/shutdown); manual or automated
3. **Relief Valve Service:** Safety-critical pressure relief; automatic operation on overpressure
4. **Strainer Service:** Continuous service; infrequent cleaning/maintenance

**Source:** Service categories inferred from PKG-16 scope and typical transload facility operations

## Construction

**Specification Content (Anticipated Artifacts):**

Per `_CONTEXT.md`, this deliverable includes three valve specifications:

### 1. Control Valve Specification

**Scope:**
- Flow control valves (modulating service)
- Pressure control valves (pressure reducing, back-pressure)
- Level control valves (tank level control applications)

**Key Requirements (typical):**
- Valve body style: Globe, ball, butterfly (TBD per application)
- Trim style: Characterized (equal percentage, linear) per control application
- Body material: **TBD** — **ASSUMPTION**: Stainless steel for product contact (316SS typical for food-grade canola oil)
- Trim material: **TBD** — **ASSUMPTION**: Stainless steel or hardened stainless for erosion resistance
- Actuation: Pneumatic (spring-return or double-acting), electric (modulating)
- Fail-safe mode: Per HAZOP (DEL-27.02) — **TBD**
- Positioner: Smart positioner with 4–20 mA input and HART or Foundation Fieldbus communication — **TBD**
- Rangeability: **TBD** — Minimum 50:1 typical for control valves
- Leakage class: **TBD** — ANSI/FCI 70-2 Class IV or better for tight shutoff applications
- Actuator sizing: 1.5× calculated torque/thrust minimum safety factor — **TBD**

**Source:** Typical control valve specification requirements; specific requirements TBD pending process control philosophy and P&ID development

### 2. Isolation Valve Specification

**Scope:**
- Manual isolation valves (gate, ball, butterfly)
- Automated isolation valves (ESD, seasonal isolation)
- Block valves for equipment isolation

**Key Requirements (typical):**
- Valve types:
  - **Gate valves:** Full-port, rising stem, for tight shutoff and minimal pressure drop
  - **Ball valves:** Full-port, floating or trunnion-mounted, for quick shutoff
  - **Butterfly valves:** Wafer or lug style, for large diameter low-pressure applications
- Body material: **TBD** — **ASSUMPTION**: Carbon steel or stainless steel per service
- Seat material: **TBD** — Soft-seated (PTFE, RTFE) or metal-seated per temperature/pressure
- End connections: Flanged per ASME B16.5 (150# or 300# rating TBD)
- Operation: Manual (handwheel, gearbox) or automated (pneumatic, electric) — **TBD**
- Fail-safe mode (for automated valves): Per HAZOP — **TBD**
- Leakage class: **TBD** — API 598 or ISO 5208 (Rate A for tight shutoff)
- Fire-safe design: **TBD** — API 607 fire-safe certification required for critical services

**Source:** Typical isolation valve specification requirements; specific types and materials TBD pending line list and service conditions

### 3. Relief Valve Specification

**Scope:**
- Pressure relief valves (PRVs) for overpressure protection
- Thermal relief valves for blocked-in line protection
- Vacuum relief valves (if required)

**Key Requirements (typical):**
- Valve type: Spring-loaded safety relief valve per API 526
- Sizing basis: Per API 520/521 (DEL-16.03 provides calculations) — **TBD**
- Set pressure: **TBD** — Per ASME Section VIII and system MAWP
- Set pressure tolerance: ±3 psi for pressures ≤70 psig; ±2% for pressures >70 psig per API 526
- Capacity certification: ASME Stamped (UV or "V" stamp)
- Body material: **TBD** — **ASSUMPTION**: Carbon steel or stainless steel per service temperature
- Spring material: **TBD** — Corrosion-resistant material for coastal environment
- Seat material: **TBD** — Soft-seated (elastomer) for low-pressure, metal-seated for high-temperature
- Discharge arrangement: **TBD** — Discharge piping to safe location per DEL-16.01 (Valve Design Drawing Set)
- Back pressure: **TBD** — Conventional, balanced-bellows, or pilot-operated per back pressure conditions
- Test certificate: Valve set pressure test certificate required with each valve

**Source:** Typical relief valve specification requirements per API 526/527; specific sizing and set pressures TBD pending DEL-16.03 (Valve Design Calculations)

### 4. Strainer Specification (if separate)

**Scope:**
- Y-type strainers for inline installation
- Basket-type strainers for easy cleaning
- Temporary startup strainers

**Key Requirements (typical):**
- Body material: **TBD** — **ASSUMPTION**: Stainless steel for product contact
- Screen material: **TBD** — Stainless steel mesh or perforated plate
- Screen mesh size: **TBD** — To protect downstream equipment (pumps, meters)
- Pressure drop: **TBD** — Maximum allowable pressure drop across clean strainer
- Blowdown provision: **TBD** — Quick-opening blowdown valve for basket strainers

**Source:** Typical strainer specification requirements; specific details TBD

### 5. Specialty Items

**Scope:** **TBD** — May include:
- Check valves (prevent backflow)
- Pressure regulators (gas service)
- Special service valves (cryogenic, high-temperature, etc.)

**Materials Summary:**

- **Product-Contact Materials (CSD Canola Oil Service):**
  - **Preferred:** Stainless steel (316SS or 304SS) for food-grade cleanliness and corrosion resistance
  - **Acceptable:** Carbon steel with suitable internal coating (epoxy, phenolic) if approved
  - **Gaskets/Seals:** PTFE, RTFE, or EPDM (food-grade elastomers) — **TBD**

- **Non-Product Materials (Utilities, Nitrogen, etc.):**
  - Carbon steel acceptable with external coating/painting per environmental conditions
  - Stainless steel preferred for coastal environment to reduce maintenance

**Source:** Material selection principles for food-grade service and coastal environment; specific materials TBD pending DEL-16.02 specification document

**Interface Deliverables (see also Specification.md — Interface Requirements; Guidance.md — Section 3 "Interface Coordination"):**
- DEL-16.01 (Valve Design Drawing Set) — Valve arrangement informs specification (size, type, service) (see Procedure.md — Step 1 for design input coordination)
- DEL-16.03 (Valve Design Calculations) — Valve sizing calculations inform specification requirements (Cv, set pressure, flow capacity)
- DEL-16.04 (Valve Data Sheet Package) — Individual valve datasheets reference this specification (see Guidance.md — Section 4 "Considerations" for datasheet relationship)
- DEL-14.02 (Process Piping Technical Specification) — Piping material compatibility (see Procedure.md — Step 6 IDC for piping coordination)
- DEL-20.02 (Instrumentation Technical Specification) — Control valve instrumentation (positioners, limit switches) (see Specification.md — Interface Requirements)

**Source:** Interface requirements inferred from package structure; formal dependencies NOT_TRACKED per `_DEPENDENCIES.md`

**For specification development procedure and verification process, see Procedure.md. For specification philosophy and trade-offs, see Guidance.md.**

## References

**Reference Documents:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials

**Applicable Standards:**

**Valve Design and Manufacturing:**
- API 600 — Steel Gate Valves (Flanged and Butt-welding Ends)
- API 6D — Pipeline Valves (Gate, Plug, Ball, and Check Valves)
- API 526 — Flanged Steel Pressure-Relief Valves
- API 527 — Seat Tightness of Pressure Relief Valves
- API 598 — Valve Inspection and Testing
- ASME B16.34 — Valves – Flanged, Threaded, and Welding End
- ASME B16.5 — Pipe Flanges and Flanged Fittings (end connections)
- ISO 5208 — Industrial Valves – Pressure Testing of Metallic Valves
- MSS-SP-61 — Pressure Testing of Steel Valves
- MSS-SP-25 — Standard Marking System for Valves, Fittings, Flanges, and Unions

**Control Valves:**
- IEC 60534 (ISA-75 series) — Industrial-Process Control Valves
  - ISA-75.01 — Control Valve Sizing Equations
  - ISA-75.05 — Control Valve Terminology
  - ISA-75.11 — Inherent Flow Characteristic and Rangeability
  - ISA-75.13 — Method of Evaluating the Performance of Positioners with Analog Input Signals
  - ISA-75.25 — Test Procedure for Control Valve Actuators

**Relief Valves:**
- ASME BPVC Section VIII — Pressure Vessels (relief valve requirements)
- API 520 — Sizing, Selection, and Installation of Pressure-Relieving Devices (Part I – Sizing and Selection)
- API 521 — Pressure-Relieving and Depressuring Systems

**Materials:**
- NACE MR0175/ISO 15156 — Materials for Sour Service (if applicable)
- ASTM A105/A350 — Carbon Steel Forgings for Piping Applications
- ASTM A182 — Forged or Rolled Alloy and Stainless Steel Pipe Flanges
- ASTM A351 — Castings, Austenitic, for Pressure-Containing Parts
- ASME SA-479 — Stainless Steel Bars and Shapes

**Testing and Quality:**
- API 607 — Fire Test for Quarter-Turn Valves
- API 608 — Metal Ball Valves – Flanged, Threaded, and Welding Ends
- API 609 — Butterfly Valves: Double-Flanged, Lug- and Wafer-Type
- ISO 15848 — Fugitive Emissions Measurement (valve stem seals)

**Canadian Codes:**
- CSA B51 — Boiler, Pressure Vessel and Pressure Piping Code (relief valve requirements)
- CGA B149 — Natural Gas and Propane Installation Code (gas service valves, if applicable)

**Project-Specific:**
- Employer's Requirements — **TBD** — **ASSUMPTION**: Volume 2 Parts 1–3 contain valve requirements
- Project Engineering Standards — **TBD**
- Project Quality Management Plan — **TBD**

**Source:** Standards inferred from Mechanical discipline and valve scope; applicability to be confirmed during specification development

**Cross-references:**
- See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
- Decomposition document: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section 5, PKG-16, DEL-16.02

**For specification content and requirements, see Specification.md. For specification development procedure, see Procedure.md.**
