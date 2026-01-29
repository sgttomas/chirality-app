# Guidance: DEL-16.01 Valve Design Drawing Set

## Purpose

This guidance document supports the development of **Valve Design Drawing Set** for **PKG-16 Valves & Specialty Equipment**.

**Deliverable Purpose:** Defines the design arrangement and details for valves per ER requirements for the Canola Oil Transload Facility.

**Source:** `_CONTEXT.md`

**Deliverable Classification:**
- **Type:** Drawing
- **Discipline:** Mechanical
- **Responsible Party:** D&B Contractor

**Project Context:**
This deliverable supports **OBJ-1: Safe & Reliable Operation** by documenting valve arrangements and actuator details to enable safe, efficient, and reliable facility operation.

**Source:** Decomposition document Section 6 (Objective-to-Deliverable Mapping), OBJ-1 includes PKG-16 (DEL-16.01–DEL-16.05)

## Principles

**Engineering Rationale:**

**1. Valve Selection and Arrangement Philosophy**

Valve drawings communicate the physical arrangement and installation requirements that enable valves to perform their intended functions safely and reliably. Key principles (see also Specification.md — Functional Requirements for drawing content requirements):

- **Accessibility:** Valve arrangement shall provide adequate access for operation, maintenance, and emergency response (see Specification.md — Section "Drawing Content" for access requirements; see Procedure.md — Step 2 for access layout considerations)
- **Operability:** Manual valves shall be positioned within operator reach; automated valves shall have local manual override capability (see Datasheet.md — Conditions for operating context)
- **Maintainability:** Valve location shall permit removal and replacement without extensive disassembly (see Procedure.md — Step 5 "Interdisciplinary Check" for constructability verification)
- **Safety:** Isolation valve placement shall enable safe isolation for maintenance; relief valves shall discharge safely away from personnel and equipment (see Specification.md — Performance Requirements for environmental design; see Procedure.md — Step 7 for design review of critical valves)

**Source:** General engineering principles for valve arrangement in process facilities; **ASSUMPTION**: To be confirmed with project design philosophy

**2. Actuator Integration**

Actuator selection and mounting affects valve performance, reliability, and operability:

- **Actuation Type Selection:**
  - **Pneumatic:** Fast-acting, fail-safe capability, common for control valves and ESDs
  - **Electric:** Precise positioning, suitable for modulating control, higher torque capability
  - **Hydraulic:** Very high force capability, less common (specialty applications)
  - **Manual:** Simple, reliable, no utilities required (suitable for infrequently operated isolation valves)

- **Failure Mode:** Critical to safety (fail-open vs fail-closed determined by process hazard analysis)
- **Speed of Operation:** Control response time affects process stability; ESD closure time affects safety

**Source:** Typical actuator selection principles; specific requirements TBD pending process design and HAZOP (see DEL-27.02)

**3. Interface Coordination**

Valve drawings are inherently multi-discipline:

- **Piping Interface:** Valve orientation affects piping flexibility and stress; coordinate with DEL-14.01
- **Structural Interface:** Large valves require support structures; coordinate with DEL-06.01
- **Instrumentation Interface:** Control valves require positioners and limit switches; coordinate with DEL-20.01
- **Electrical Interface:** Electric actuators require power and control wiring; coordinate with DEL-17.01 and DEL-19.01

**Source:** Interface requirements inferred from multi-discipline nature of valve installations

**Applicable Standards Context:**

**Valve Standards:**
- **API 600/6D:** Establishes minimum design requirements for gate and ball valves (pressure-temperature ratings, materials, testing)
- **API 526/527:** Defines pressure relief valve sizing, set pressure tolerance, and seat tightness requirements
- **ISA-75 series:** Control valve standards (sizing, performance, testing)

**Canadian Regulatory Context:**
- **CSA B51:** Governs pressure-retaining components in BC; valves may require registration if pressure vessels upstream/downstream are registered
- **NBCC:** Seismic requirements for equipment anchorage (valves on structural supports)

**Source:** Standards inferred from Mechanical discipline and valve scope; applicability to be confirmed during design development

**Product-Specific Considerations:**

**CSD Canola Oil Service:**
- **Viscosity:** Canola oil viscosity varies with temperature (higher viscosity at lower temperatures affects valve sizing and actuator torque)
- **Temperature Control:** Product may require heating to maintain pumpability; valve body heat tracing considerations
- **Cleanliness:** Food-grade product handling requires cleanable valve internals; dead-leg elimination
- **Fire Safety:** Vegetable oils can auto-ignite if overheated; temperature monitoring and relief valve protection

**Source:** Product grade (CSD canola oil) from decomposition Section 1.1; product properties **ASSUMPTION**: Typical canola oil characteristics, TBD pending process design basis

## Considerations

**Factors to consider during development:**

**1. Project-Specific Factors**

- **Package Scope:** PKG-16 Valves & Specialty Equipment — includes control valves, isolation valves, relief valves, strainers, specialty items
- **Facility Type:** Transload facility (railcar unloading, storage, marine loading) — different valve service requirements
- **Throughput:** 1,000,000 MT/annum capacity — valve sizing must support design flow rates
- **Location:** Fraser Surrey Terminal, Surrey, BC — marine/coastal environment, seismic zone

**Source:** Decomposition document Sections 1.1 and 5 (PKG-16 scope)

**2. Deliverable Type Considerations (Drawing)**

- **Drawing Scale:** Arrangement drawings typically 1:50 or 1:100; detail drawings as required for clarity
- **CAD Standards:** Compliance with project CAD standards manual — **TBD**
- **Drawing Numbering:** Per project drawing register — **TBD**
- **Revision Control:** Drawing revision protocol per project procedures — **TBD**

**3. Coordination Requirements**

- **Upstream Deliverables:** Process design (P&IDs, line sizing) informs valve selection and arrangement
- **Downstream Deliverables:** Valve drawings inform procurement (DEL-16.02 specifications, DEL-16.04 datasheets)
- **Parallel Deliverables:** Coordinate with piping (DEL-14.01), instrumentation (DEL-20.01), control systems (DEL-19.01), electrical (DEL-17.01)

**Source:** Dependencies inferred from package structure; NOT_TRACKED per `_DEPENDENCIES.md`

**4. Regulatory and Compliance**

- **Employer's Requirements:** **TBD** — Review Volume 2 Parts 1–3 for valve-specific requirements
- **Permit Conditions:** **TBD** — VFPA, DFO, Transport Canada may have requirements
- **Code Compliance:** CSA B51 (pressure equipment), NBCC (seismic anchorage)

**5. Constructability and Operability**

- **Construction Sequencing:** Valve installation sequence affects piping erection; consider modular assembly where practical
- **Access During Construction:** Adequate laydown and rigging access required for large valves
- **Operational Access:** Operator reach zones, platform access, lighting requirements
- **Maintenance Access:** Valve removal clearances, actuator maintenance access, relief valve testing provisions

**6. Safety and Environmental**

- **Relief Valve Discharge:** Safe discharge location (away from platforms, ignition sources)
- **Emergency Isolation:** ESD valve accessibility during emergency scenarios
- **Containment:** Valve packing leaks shall drain to containment system
- **Fire Protection:** Valve body fire protection (insulation, deluge, fireproofing) — **TBD**

**Source:** Safety considerations typical for process facilities; specific requirements TBD pending HAZOP (DEL-27.02) and fire protection design (PKG-23)

## Trade-offs

**Competing concerns to evaluate:**

**1. Manual vs. Automated Valves**

| Factor | Manual Valves | Automated Valves |
|--------|---------------|------------------|
| **Cost** | Lower capital cost | Higher capital cost (actuator, controls, utilities) |
| **Reliability** | Simple, fewer failure modes | More complex, requires maintenance |
| **Operability** | Requires operator presence | Remote operation capability |
| **Response Time** | Slow (operator travel time) | Fast (immediate response) |
| **Safety** | Requires operator in field | Safer (remote isolation) |

**Guidance:** Automate valves where fast response or remote operation is required (ESDs, frequent operation, process control). Use manual valves for infrequent isolation (maintenance isolation, seasonal operations).

**Source:** Typical valve selection trade-offs; specific decisions TBD pending operability study and P&ID development

**2. Fail-Safe Mode (Fail-Open vs. Fail-Closed)**

**Fail-Closed (FC):** Valve closes on loss of actuation power
- **Advantages:** Provides isolation on utility failure (safer for hazardous releases)
- **Disadvantages:** Can interrupt process flow, may cause pressure surge

**Fail-Open (FO):** Valve opens on loss of actuation power
- **Advantages:** Maintains process continuity
- **Disadvantages:** May allow uncontrolled flow on utility failure

**Guidance:** Failure mode selection driven by process hazard analysis (HAZOP). Err on the side of safety (fail-closed for isolation valves on hazardous services).

**Source:** Typical fail-safe selection principles; specific modes TBD pending HAZOP (DEL-27.02)

**3. Valve Body Material Selection**

| Material | Advantages | Disadvantages | Typical Application |
|----------|------------|---------------|---------------------|
| **Carbon Steel** | Low cost, widely available | Corrosion susceptibility | Non-corrosive service, coated or painted |
| **Stainless Steel** | Corrosion resistance, cleanable | Higher cost | Food-grade service, coastal environment |
| **Special Alloys** | Specific corrosion/temperature resistance | High cost, long lead time | Severe service (rare in canola oil facility) |

**Guidance:** Stainless steel likely preferred for product-contact valves (food-grade CSD canola oil). Carbon steel acceptable for non-product services (nitrogen, utilities) with appropriate coatings.

**Source:** Material selection principles for food-grade service; specific materials TBD pending DEL-16.02 (Valve Technical Specification)

**4. Valve Arrangement: Inline vs. Bypass vs. Manifold**

- **Inline:** Simple, low cost, but requires process shutdown for maintenance
- **Bypass Arrangement:** Allows online maintenance, but higher cost and complexity
- **Manifold Arrangement:** Multiple valves in parallel, provides redundancy, but highest cost

**Guidance:** Use bypass arrangements for critical service where online maintenance is required. Use inline for non-critical, easy-to-replace valves.

**Source:** Typical arrangement trade-offs; specific arrangements TBD pending operability requirements

**5. Drawing Detail Level: Generic vs. Vendor-Specific**

- **Generic Details:** Contractor-issued drawings show generic valve outlines and mounting requirements; suitable for early design phases
- **Vendor-Specific Details:** After valve procurement, vendor drawings provide exact dimensions and mounting details; required for final construction

**Guidance:** Issue generic arrangement drawings at IFC stage with envelope dimensions. Incorporate vendor-specific details in "Approved Vendor Drawing" or addendum drawings post-procurement.

**Source:** Typical EPC drawing workflow; specific phasing TBD pending project execution plan

## Examples

**Reference examples and precedents:**

**1. Employer's Requirements**

Refer to Employer's Requirements (Volume 2 Parts 1–3) for project-specific expectations:
- Valve standards and specifications
- Valve arrangement and accessibility requirements
- Actuator and failure mode requirements
- Drawing format and deliverable requirements

**Location:** `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf` — **TBD** (not yet available in `_REFERENCES.md`)

**2. Industry Precedents**

**Typical valve drawing content for similar facilities:**
- **Railcar Unloading Systems:** Gravity-fed unloading with isolation valves at each railcar position; manual valves common (32 stations per PKG-10 scope)
- **Marine Loading Systems:** Automated loading arm with ESD valves, quick-closing capability, fail-closed on utility loss
- **Storage Tank Systems:** Tank isolation valves (manual or automated), relief valves with safe discharge, overflow protection valves

**Source:** Typical configurations inferred from PKG-10, PKG-11, PKG-13 scope; specific details TBD pending P&ID development

**3. Anticipated Artifacts for Reference**

Per `_CONTEXT.md`, this deliverable includes:
- **Valve arrangement drawings:** Overall valve location plans, elevations, sections showing valve-to-piping interfaces
- **Actuator details:** Typical mounting details for pneumatic, electric, and manual actuators; torque/thrust basis, manual override provisions

**4. Related Deliverables**

- **DEL-16.02 (Valve Technical Specification):** Defines valve performance, materials, and workmanship requirements
- **DEL-16.03 (Valve Design Calculations):** Provides valve sizing and relief valve set pressure calculations
- **DEL-16.04 (Valve Data Sheet Package):** Individual valve datasheets with specifications
- **DEL-16.05 (Valve Installation & Test Records):** Installation and testing documentation

**Source:** PKG-16 deliverable structure from decomposition Section 5

**5. Lessons Learned (Typical Issues)**

**Common valve arrangement issues to avoid:**
- **Inadequate Maintenance Clearance:** Valve bonnet removal interferes with piping, platforms, or adjacent equipment
- **Poor Access:** Manual valve handwheel positioned out of operator reach or in hazardous location
- **Relief Valve Discharge Hazard:** Relief discharge directed at platforms, electrical equipment, or ignition sources
- **Piping Stress:** Heavy valve weight or thermal expansion causes excessive piping stress; requires structural support
- **Actuator Interference:** Actuator fouls adjacent piping, cable trays, or structure

**Source:** **ASSUMPTION**: Typical valve arrangement issues from industry experience; project-specific lessons TBD
