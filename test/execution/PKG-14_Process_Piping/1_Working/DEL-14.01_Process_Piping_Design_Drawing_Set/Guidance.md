# Guidance: DEL-14.01 Process Piping Design Drawing Set

## Purpose

This guidance document supports the development of **Process Piping Design Drawing Set** for **PKG-14 Process Piping**.

**Deliverable intent** (source: Decomposition DEL-14.01; scope: Specification.md Scope): Defines the design arrangement and details for process piping per ER requirements.

**Deliverable classification:**
- **Type:** Drawing (attributes: Datasheet.md Identification)
- **Discipline:** Mechanical (Process Piping)
- **Responsible:** D&B Contractor

**Project context** (source: Decomposition Section 1.1; attributes: Datasheet.md Conditions):
- **Facility:** Canola Oil Transload Facility — Phase 1 (Design & Build)
- **Product:** CSD (Crude Super Degummed) canola oil (requirements: Specification.md PR-1; attributes: Datasheet.md Product Handled)
- **Throughput:** 1,000,000 MT per annum (requirements: Specification.md FR-1; attributes: Datasheet.md Design Throughput)
- **Operation:** Transfer from rail tank cars to liquid bulk carriers for export
- **Location:** Fraser Surrey Terminal, Surrey, BC (attributes: Datasheet.md Environmental classification)

## Principles

**Engineering rationale (Mechanical — Process Piping discipline):**

**1. Process piping design philosophy:**
- Piping systems shall be designed for safe, reliable, and efficient transfer of CSD canola oil from railcar unloading to storage tanks and from storage tanks to marine loading (source: OBJ-1, OBJ-2; requirements: Specification.md FR-1, PR-1; procedure: Procedure.md Step 1-2)
- Design shall minimize pressure drop while maintaining acceptable velocities to avoid product degradation and erosion (source: ASME B31.3 design principles; requirements: Specification.md PR-4, PR-5; sizing: cross-reference DEL-14.03; procedure: Procedure.md Step 1)
- **ASSUMPTION**: Piping shall be designed to drain completely to minimize product loss and facilitate cleaning; confirm drainage philosophy (location TBD: ER Volume 2 Part 2; routing considerations: Procedure.md Step 3)

**2. System integration approach:**
- Process piping design integrates railcar unloading (PKG-10), storage tanks (PKG-13), marine loading (PKG-11), and metering (PKG-12) into a cohesive transfer system (systems: Datasheet.md Key piping systems; scope: Specification.md Scope; interfaces: Specification.md IR-9, IR-10, IR-11; coordination: Procedure.md Step 1, Step 8)
- Operational flexibility is achieved through header configurations allowing multiple flow paths (source: OBJ-4 — tank storage operations and direct rail-to-ship transfer; requirements: Specification.md FR-2; P&ID development: Procedure.md Step 2)
- **TBD** — Extent of redundancy and isolation valve placement philosophy

**3. Material selection rationale:**
- **ASSUMPTION**: Carbon steel is typical for CSD canola oil service due to non-corrosive nature of the product; stainless steel may be required for specific services (e.g., clean-in-place systems, nitrogen distribution) (product: Datasheet.md Product Handled; materials: Datasheet.md Materials; requirements: Specification.md PR-1, Standards - Materials and corrosion; trade-offs discussed below in item 1)
- Material selection shall consider product compatibility, temperature, pressure, and environmental conditions (source: ASME B31.3; requirements: Specification.md PR-1, PR-2, PR-3; conditions: Datasheet.md Conditions; cross-reference DEL-14.02)
- **TBD** — Confirm material philosophy and corrosion allowance requirements (cross-reference DEL-14.02 Piping Technical Specification; Specification.md Standards section)

**4. Piping support philosophy:**
- Supports shall be designed to accommodate thermal expansion, seismic loads, and operational loads (pump vibration, water hammer from transients) (source: ASME B31.3, NBC 2020; requirements: Specification.md PR-6, PR-7; support drawings: Datasheet.md Pipe support drawings; procedure: Procedure.md Step 5)
- Support spacing shall follow code requirements while considering practical installation and maintenance access (source: ASME B31.3 Table 321.7.4 or equivalent; requirements: Specification.md PR-6, QR-6; verification: Procedure.md Step 10; cross-reference DEL-14.03)
- **ASSUMPTION**: Spring hangers or expansion loops may be required for lines with significant temperature variation; confirm thermal expansion strategy (requirements: Specification.md PR-7; conditions: Datasheet.md Operating temperature range; trade-offs discussed below in item 2)

**5. Phase 2 expandability:**
- Design shall include provisions for future Phase 2 expansion with minimal disruption to Phase 1 operations (source: OBJ-8; requirements: Specification.md FR-3, FR-9; connection details: Datasheet.md Phase 2 connection details; procedure: Procedure.md Step 6)
- **TBD** — Phase 2 scope and interface requirements; typical provisions include capped stub-outs, oversized headers, or flanged connections at anticipated expansion points (location TBD: ER Volume 2 Part 2; procedure: Procedure.md Step 6)

**Applicable standards context:**

**ASME B31.3 — Process Piping:**
- Governs design, materials, fabrication, assembly, erection, examination, inspection, and testing of process piping (code: Datasheet.md Design Code; requirements: Specification.md PR-5, Standards section; verification: Procedure.md Step 10)
- Defines allowable stresses, pressure design thickness calculations, flexibility analysis requirements, and support criteria (requirements: Specification.md PR-5, QR-5, QR-6)
- Requires stress analysis for thermal expansion, weight, and pressure loads (verification: Specification.md QR-5; procedure: Procedure.md Step 10; cross-reference DEL-14.03)

**Additional standards** — **TBD** (location TBD: ER Volume 2 Part 2; Specification.md Standards section):
- **ASSUMPTION**: MSS SP-58 (Pipe Hangers and Supports — Materials, Design, Manufacture) likely applicable (requirements: Specification.md Standards - Piping supports; procedure: Procedure.md Step 5)
- **ASSUMPTION**: CSA Z662 (Oil and Gas Pipeline Systems) may apply to nitrogen distribution; confirm scope boundaries (systems: Datasheet.md Nitrogen distribution piping; Specification.md Standards section)
- **ASSUMPTION**: NBC 2020 for seismic and structural loads; confirm design basis (requirements: Specification.md PR-6, Standards - Piping supports; conditions: Datasheet.md Seismic requirements)

## Considerations

**Factors to consider during development:**

**1. Package scope boundaries** (source: Decomposition PKG-14 Scope; scope: Specification.md Scope):
- **Included:** All process piping including headers, export lines, recycle lines, nitrogen distribution, pipe supports (systems: Datasheet.md Key piping systems)
- **Interface:** Nitrogen skid supplied by Employer; Contractor responsible for connection piping only (source: Decision DEC-07; requirements: Specification.md IR-8; procedure: Procedure.md Step 1)
- **Coordination:** Piping interfaces with equipment in PKG-10 (Railcar Unloading), PKG-11 (Marine Loading), PKG-12 (Metering), PKG-13 (Storage Tanks), PKG-15 (Pumps), PKG-16 (Valves) (requirements: Specification.md IR-4 through IR-11; procedure: Procedure.md Step 1, Step 8)

**2. Drawing type-specific considerations:**

**P&IDs (Process and Instrumentation Diagrams):**
- Show process flow, equipment, piping, instrumentation, control logic, and safety systems (description: Datasheet.md Construction - P&IDs; requirements: Specification.md FR-5; procedure: Procedure.md Step 2)
- Basis for piping GAs, isometrics, and control system design (coordination: Specification.md IR-3; procedure: Procedure.md Step 2-3)
- **TBD** — P&ID symbology standard (location TBD: project CAD standards; Specification.md Standards - Drawing standards; procedure: Procedure.md Step 2) — **ASSUMPTION**: ISA 5.1 or equivalent

**Piping GAs (General Arrangement drawings):**
- Show piping routing in 3D space (plan and elevation views) (description: Datasheet.md Construction - Piping GAs; requirements: Specification.md FR-6; procedure: Procedure.md Step 3)
- Critical for spatial coordination with structural, electrical, instrumentation disciplines (requirements: Specification.md IR-1, IR-2; procedure: Procedure.md Step 3, Step 8; verification: Specification.md Verification - Technical verification)
- **TBD** — Coordination procedures and clash detection requirements (attributes: Datasheet.md CAD Software; procedure: Procedure.md Step 3)
- **ASSUMPTION**: 3D modeling (e.g., AutoCAD Plant 3D, PDMS, or similar) typically used; confirm project CAD platform (attributes: Datasheet.md CAD Software; requirements: Specification.md QR-1; procedure: Procedure.md Prerequisites)

**Piping isometrics:**
- Single-line fabrication drawings showing dimensions, fittings, welds, flanges, valves, supports (description: Datasheet.md Construction - Piping isometrics; requirements: Specification.md FR-7; procedure: Procedure.md Step 4)
- Used by fabricators for material takeoff, prefabrication, and field installation (procedure: Procedure.md Step 4; verification: Specification.md Verification - Technical verification)
- **TBD** — Isometric drawing conventions and level of detail (location TBD: project CAD standards; attributes: Datasheet.md Scale; requirements: Specification.md QR-1)

**Pipe support drawings:**
- Detail drawings for supports, hangers, anchors, guides, restraints (description: Datasheet.md Construction - Pipe support drawings; requirements: Specification.md FR-8; procedure: Procedure.md Step 5)
- Include support loads for structural coordination (requirements: Specification.md IR-2, QR-6; rationale: Principles item 4 above; procedure: Procedure.md Step 5; cross-reference DEL-14.03)
- **TBD** — Support standardization and typical detail library (location TBD: project standards; requirements: Specification.md Standards - Piping supports)

**Phase 2 connection details:**
- Show stub-outs, flanged connections, or capped ends for future expansion (description: Datasheet.md Construction - Phase 2 connection details; requirements: Specification.md FR-9; rationale: Principles item 5 above; procedure: Procedure.md Step 6)
- **TBD** — Phase 2 interface requirements and expansion scenarios (location TBD: ER Volume 2 Part 2; procedure: Procedure.md Step 6)

**3. Regulatory and code compliance:**
- Employer's Requirements define project-specific requirements beyond code minimums (location: ER Volume 2 Part 1, Part 2; requirements: Specification.md Standards - Project-specific requirements; procedure: Procedure.md Prerequisites, Step 1)
- **TBD** — Regulatory approvals and permitting requirements (location TBD: ER Volume 2 Part 1)
- **ASSUMPTION**: Transport Canada may have jurisdiction over rail-related piping; confirm regulatory scope

**4. Constructability and sequencing:**
- Design shall minimize disturbance to existing Terminal operations (source: OBJ-5 — Terminal Continuity; requirements: Specification.md FR-4; constraints: Datasheet.md Construction constraints - Terminal continuity; routing: Procedure.md Step 3)
- **TBD** — Construction sequencing and phasing requirements (location TBD: ER Volume 2 Part 1; procedure: Procedure.md Step 3)
- **ASSUMPTION**: Prefabrication and modularization opportunities should be evaluated to minimize field welding and installation time (constraints: Datasheet.md Construction constraints - Modularization; trade-offs discussed below in item 3; procedure: Procedure.md Step 3)

**5. Operability and maintainability:**
- Piping layout shall provide access for operation, inspection, and maintenance (source: OBJ-1 — Safe & Reliable Operation; constraints: Datasheet.md Construction constraints - Access for maintenance; routing: Procedure.md Step 3)
- **TBD** — Valve accessibility requirements, drain and vent placement philosophy, maintenance access clearances (procedure: Procedure.md Step 3)
- **ASSUMPTION**: Insulation requirements may apply for personnel protection or energy conservation; confirm (cross-reference DEL-14.02; conditions: Datasheet.md Operating temperature range)

**6. Environmental and safety:**
- Design shall include adequate containment and spill prevention (source: OBJ-7 — Environmental Protection; procedure: Procedure.md Step 1)
- **TBD** — Secondary containment requirements for piping (location TBD: ER Volume 2 Part 2)
- **TBD** — Fire protection and hazardous area classification implications (conditions: Datasheet.md Hazardous area classification; procedure: Procedure.md Prerequisites)

## Trade-offs

**Competing concerns to evaluate:**

**1. Material cost vs. long-term reliability:**
- **Trade-off:** Carbon steel is lower cost but may require greater corrosion allowance; stainless steel is higher cost but provides better corrosion resistance and lower maintenance (materials: Datasheet.md Materials; requirements: Specification.md PR-1, Standards - Materials and corrosion; rationale: Principles item 3 above)
- **Guidance:** Material selection should consider lifecycle cost (source: OBJ-9 — Lifecycle Cost Optimization), not just initial capital cost
- **ASSUMPTION**: CSD canola oil is generally non-corrosive, favoring carbon steel; confirm product characteristics and operating conditions (product: Datasheet.md Product Handled; conditions: Datasheet.md Conditions; procedure: Procedure.md Step 1)

**2. Piping flexibility vs. support complexity:**
- **Trade-off:** Long piping runs with expansion loops reduce support loads but consume more space; rigid piping with closely-spaced supports is more compact but requires more structural attachments and higher loads (requirements: Specification.md PR-7; rationale: Principles item 4 above; support loads: Specification.md QR-6; procedure: Procedure.md Step 3, Step 5)
- **Guidance:** Thermal expansion analysis (DEL-14.03) will determine optimal balance; consider available space and structural capacity (verification: Specification.md QR-5; procedure: Procedure.md Step 10; cross-reference DEL-14.03)
- **ASSUMPTION**: Temperature variation from ambient to operating temperature drives thermal expansion; confirm operating temperature range (conditions: Datasheet.md Operating temperature range; requirements: Specification.md PR-2, PR-7)

**3. Piping routing — direct vs. coordinated:**
- **Trade-off:** Direct routing minimizes pipe length and pressure drop but may conflict with other disciplines; coordinated routing avoids conflicts but may increase pipe length and complexity (requirements: Specification.md FR-6, IR-1; GA development: Procedure.md Step 3; clash detection: Procedure.md Step 3, Step 8)
- **Guidance:** Early interdisciplinary coordination (IDC) reduces rework; 3D modeling with clash detection is recommended (requirements: Specification.md QR-3; procedure: Procedure.md Step 8; verification: Specification.md Verification - IDC)
- **TBD** — Coordination procedures and clash resolution authority (Specification.md IR-1; procedure: Procedure.md Step 8)

**4. Standardization vs. optimization:**
- **Trade-off:** Standardized pipe sizes, materials, and support types simplify procurement and reduce inventory but may not be optimal for every service; custom optimization reduces material cost but increases complexity (materials: Datasheet.md Piping sizes; requirements: Specification.md PR-4; procedure: Procedure.md Step 1, Step 4)
- **Guidance:** Standardization is generally preferred for maintenance and lifecycle cost benefits (source: OBJ-9); optimize only where significant cost or performance benefit justifies complexity
- **TBD** — Project standardization philosophy (Specification.md Standards section)

**5. Design conservatism vs. material efficiency:**
- **Trade-off:** Conservative design (thicker walls, higher pressure ratings, larger safety factors) increases reliability but also increases material cost and weight; optimized design reduces cost but may reduce operational margin (code: Datasheet.md Design Code; requirements: Specification.md PR-3, PR-5; rationale: Principles item 1 above)
- **Guidance:** Follow code-minimum requirements (ASME B31.3) with additional conservatism only where justified by operational risk or uncertainty (requirements: Specification.md PR-5, Standards - Process piping design; verification: Specification.md QR-5; procedure: Procedure.md Step 10)
- **ASSUMPTION**: Critical services (e.g., high-pressure, high-consequence-of-failure lines) may warrant additional conservatism; confirm criticality criteria (verification: Specification.md QR-5, QR-7)

**6. Schedule — drawing issuance strategy:**
- **Trade-off:** Issue all drawings together ensures consistency but delays construction start; progressive issuance (e.g., P&IDs first, then GAs, then isometrics) enables early procurement and construction but requires careful change management (procedure: Procedure.md Step 11; documentation: Specification.md Documentation section)
- **Guidance:** Progressive issuance is typical for design-build projects to support fast-track schedules; requires disciplined change control (revision control: Datasheet.md Revision Control; requirements: Specification.md QR-2; procedure: Procedure.md Step 11)
- **TBD** — Drawing issuance strategy and submittal schedule (location TBD: ER Volume 2 Part 1; Specification.md Documentation - Submittal requirements; procedure: Procedure.md Step 11)

## Examples

**Reference examples and precedents:**

**1. Project-specific guidance:**
- Refer to Employer's Requirements Volume 2 Part 2 for process piping design requirements (location: test/Volume_2_Part_2_Employers_Requirements.pdf; requirements: Specification.md Standards - Project-specific requirements; procedure: Procedure.md Prerequisites, Step 1; **TBD** extract relevant clauses)
- **TBD** — Review project Quality Management Plan for drawing review and approval procedures (requirements: Specification.md QR-4, Standards - Project-specific requirements; procedure: Procedure.md Prerequisites, Step 7, Step 9)
- **TBD** — Review project CAD Management Plan for drawing standards and conventions (requirements: Specification.md QR-1, Standards - Drawing standards; attributes: Datasheet.md CAD Standard, CAD Software; procedure: Procedure.md Prerequisites, Step 7)

**2. Similar facility precedents:**
- **TBD** — Industry best practices for vegetable oil transload facilities
- **TBD** — Lessons learned from similar canola oil or edible oil handling facilities
- **ASSUMPTION**: Facilities handling similar food-grade products (soybean oil, palm oil, etc.) may provide relevant precedents for material selection, cleaning provisions, and operational philosophy (product: Datasheet.md Product Handled; requirements: Specification.md PR-1; rationale: Principles item 3 above)

**3. Anticipated artifacts for reference** (source: Decomposition DEL-14.01; attributes: Datasheet.md Drawing Types; construction: Datasheet.md Construction section; procedure: Procedure.md Steps 2-6):
- **P&IDs:** Show process flow, equipment connections, instrumentation, control schemes (requirements: Specification.md FR-5; considerations: item 2 above - P&IDs; procedure: Procedure.md Step 2)
- **Piping GAs:** Show piping routing in plan and elevation with spatial coordination (requirements: Specification.md FR-6; considerations: item 2 above - Piping GAs; procedure: Procedure.md Step 3)
- **Piping isometrics:** Provide fabrication-ready single-line drawings (requirements: Specification.md FR-7; considerations: item 2 above - Piping isometrics; procedure: Procedure.md Step 4)
- **Pipe support drawings:** Define support locations, types, and details (requirements: Specification.md FR-8; considerations: item 2 above - Pipe support drawings; procedure: Procedure.md Step 5)
- **Phase 2 connection details:** Show expansion interface provisions (requirements: Specification.md FR-9; considerations: item 2 above - Phase 2 connection details; procedure: Procedure.md Step 6)

**4. Related deliverables to review:**
- DEL-14.02 (Process Piping Technical Specification) — for material and workmanship requirements (requirements: Specification.md Standards - Materials and corrosion; rationale: Principles item 3 above; procedure: Procedure.md Prerequisites)
- DEL-14.03 (Process Piping Design Calculations) — for sizing, stress analysis, and flexibility analysis basis (requirements: Specification.md PR-4, PR-5, PR-7, QR-5, QR-6; trade-offs: item 2 above; procedure: Procedure.md Step 10)
- DEL-14.04 (Process Piping Data Sheet Package) — for line list and piping material data (requirements: Specification.md IR-7; procedure: Procedure.md Step 4)
- DEL-14.06, DEL-14.07 (Transient Analysis Study Reports) — for surge analysis and mitigation requirements (requirements: Specification.md QR-7; procedure: Procedure.md Step 10)
- DEL-10.01 (Railcar Unloading Design Drawings) — for railcar unloading system interface (systems: Datasheet.md Railcar unloading headers; requirements: Specification.md IR-9; procedure: Procedure.md Step 1, Step 8)
- DEL-11.01 (Marine Loading Design Drawings) — for marine loading system interface (systems: Datasheet.md Marine loading export lines; requirements: Specification.md IR-10; procedure: Procedure.md Step 1, Step 8)
- DEL-13.01 (Storage Tank Design Drawings) — for tank nozzle locations and sizes (systems: Datasheet.md Tank farm piping connections; requirements: Specification.md IR-6; procedure: Procedure.md Step 1, Step 8)
- DEL-15.01 (Pump Design Drawings) — for pump nozzle sizes and orientations (requirements: Specification.md IR-4, IR-5; procedure: Procedure.md Step 1, Step 8)

**5. Code and standard references:**
- ASME B31.3 — Process Piping (complete code text; critical sections: design pressure/temperature, allowable stresses, flexibility analysis, supports) (code: Datasheet.md Design Code; requirements: Specification.md PR-5, Standards - Process piping design; rationale: Principles item 1 above; verification: Specification.md QR-5; procedure: Procedure.md Step 10)
- **TBD** — MSS SP-58 (Pipe Hangers and Supports) if applicable (rationale: Principles item 4 above; requirements: Specification.md Standards - Piping supports; considerations: item 2 above - Pipe support drawings)
- **TBD** — Project-specific CAD and drawing standards (requirements: Specification.md QR-1, Standards - Drawing standards; attributes: Datasheet.md CAD Standard; procedure: Procedure.md Prerequisites, Step 7)
