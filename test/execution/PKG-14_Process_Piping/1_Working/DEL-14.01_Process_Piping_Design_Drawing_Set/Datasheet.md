# Datasheet: DEL-14.01 Process Piping Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-14.01 |
| Name | Process Piping Design Drawing Set |
| Package | PKG-14 Process Piping |
| Discipline | Mechanical |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Product Handled | CSD (Crude Super Degummed) canola oil — food-grade edible oil (source: Decomposition Section 1.1; material compatibility discussion: Guidance.md Principles item 3) |
| Design Throughput | 1,000,000 MT per annum (source: Decomposition Section 1.1; requirements: Specification.md FR-1; sizing basis: Procedure.md Step 1) |
| Piping Systems | Railcar unloading headers, marine loading export lines, product recycle lines, nitrogen distribution, tank farm connections (source: Decomposition PKG-14 Scope; functional requirements: Specification.md FR-1 through FR-4) |
| Drawing Types | P&IDs, piping GAs, piping isometrics, pipe support drawings, Phase 2 connection details (source: Decomposition DEL-14.01; development procedures: Procedure.md Steps 2-6) |
| Drawing Quantity | **TBD** — estimate: 10-15 P&IDs, 20-30 GAs, 100-200 isometrics, 10-20 support drawings (to be confirmed during design development per Procedure.md Step 2-5) |
| Drawing Number Prefix | **TBD** — per project numbering system (cross-reference: Specification.md QR-2; Procedure.md Step 4, Step 11) |
| Sheet Size | **TBD** — **ASSUMPTION**: ISO A1 or ANSI D typical for mechanical piping drawings; ISO A3 or ANSI B for isometrics (to be confirmed per project CAD standards — Specification.md QR-1; Procedure.md Prerequisites) |
| Scale | **TBD** — varies by drawing type: P&IDs typically NTS (not to scale), GAs typically 1:50 or 1:100, isometrics as noted (cross-reference: Guidance.md Examples section; Procedure.md Step 3, Step 4) |
| CAD Standard | **TBD** — per project CAD management plan (cross-reference: Specification.md QR-1; Procedure.md Prerequisites; Procedure.md Step 7) |
| CAD Software | **TBD** — **ASSUMPTION**: AutoCAD Plant 3D, PDMS, SmartPlant, or similar 3D piping design platform (cross-reference: Guidance.md Considerations item 2; Procedure.md Prerequisites; Procedure.md Step 3 for 3D modeling) |
| Revision Control | **TBD** — per project document control procedures (cross-reference: Specification.md QR-2; Procedure.md Step 11 for approval and issuance) |
| Classification | For Construction (source: Decomposition Section 1.1 - Design & Build contract) |
| Design Code | ASME B31.3 Process Piping (source: Specification.md Standards section; rationale: Guidance.md Principles item 1; verification: Procedure.md Step 10) |

## Conditions

**Operating / Environmental Context:**

- **Product:** CSD (Crude Super Degummed) canola oil (source: Decomposition Section 1.1) — food-grade edible oil, non-corrosive, low vapor pressure at ambient conditions (material compatibility rationale: Guidance.md Principles item 3; material selection trade-offs: Guidance.md Trade-offs item 1)
- **Operating temperature range:** **TBD** — **ASSUMPTION**: Typical canola oil handling range -10°C to +60°C (ambient to heated for viscosity reduction); confirm per process requirements (location TBD: ER Volume 2 Part 2) — impacts thermal expansion design per Specification.md PR-7, Guidance.md Trade-offs item 2, and Procedure.md Step 3 (expansion loop design)
- **Operating pressure:** **TBD** — varies by piping system (railcar unloading, marine loading, recycle, nitrogen) — **ASSUMPTION**: Typical range 150 psi (1,035 kPa) to 300 psi (2,070 kPa) for liquid transfer; nitrogen distribution may be lower pressure — requirements: Specification.md PR-3; design verification: Procedure.md Step 10
- **Flow rates:** **TBD** — to be determined based on throughput requirements (1,000,000 MT/annum) and operational modes (continuous vs batch, single vs multiple loading) — requirements: Specification.md PR-4; calculation: cross-reference DEL-14.03 (Design Calculations); design input: Procedure.md Step 1
- **Design flow velocities:** **TBD** — **ASSUMPTION**: Typical range 1.5 to 3.0 m/s for liquid piping to balance pressure drop and erosion; confirm per ASME B31.3 and process design basis (calculation: DEL-14.03)
- **Environmental classification:** Fraser Surrey Terminal, Surrey, BC — coastal/marine environment (source: Decomposition Section 1.1) — impacts corrosion allowance and material selection per Specification.md Standards section (salt air, moisture exposure)
- **Hazardous area classification:** **TBD** — **ASSUMPTION**: Non-classified or Zone 2/Division 2 for canola oil vapor (low vapor pressure at ambient); confirm per facility hazardous area classification study (location TBD: ER Volume 2 Part 2) — impacts equipment selection considerations (Guidance.md Considerations item 6)
- **Seismic requirements:** **TBD** — **ASSUMPTION**: NBC 2020 seismic design per BC location (seismic zone and site class to be confirmed); confirm design basis (location TBD: ER Volume 2 Part 1) — requirements: Specification.md PR-6; design rationale: Guidance.md Principles item 4; verification: Procedure.md Step 10
- **Wind loads:** **TBD** — **ASSUMPTION**: NBC 2020 wind loads for exposed piping; typically secondary to seismic for pipe support design in BC (design considerations: Guidance.md Principles item 4)
- **Design life:** **TBD** — **ASSUMPTION**: 25-year design life typical for industrial facilities; confirm per ER (location TBD: ER Volume 2 Part 1) — impacts material selection and corrosion allowance (Guidance.md Trade-offs item 1)
- **Corrosion allowance:** **TBD** — dependent on piping material selection and service conditions; **ASSUMPTION**: 3 mm typical for carbon steel in coastal environment — cross-reference DEL-14.02 (Piping Technical Specification); Specification.md Standards section
- **Ambient temperature range:** **TBD** — **ASSUMPTION**: -20°C to +35°C for Fraser Surrey, BC climate (impacts insulation requirements and cold-weather operations per Guidance.md Considerations item 5)

## Construction

**Materials / Configuration:**

Anticipated drawing artifacts (source: Decomposition DEL-14.01 — detailed descriptions: Guidance.md Examples section item 3; production procedures: Procedure.md Steps 2-6):

- **P&IDs (Process and Instrumentation Diagrams):** Process flow diagrams showing piping systems, equipment connections, instrumentation, control schemes, and safety devices (production: Procedure.md Step 2; content requirements: Specification.md FR-5; symbology standard: **ASSUMPTION** ISA 5.1 or equivalent per project standards — Specification.md Standards section; considerations: Guidance.md Considerations item 2)
- **Piping GAs (General Arrangements):** Plan and elevation drawings showing piping routing, spatial coordination with other disciplines, supports, and critical dimensions (production: Procedure.md Step 3; content requirements: Specification.md FR-6; coordination requirements: Specification.md IR-1, IR-2; 3D modeling approach: Guidance.md Considerations item 2)
- **Piping isometrics:** Detailed single-line drawings for fabrication and installation showing dimensions, welds, fittings, flanges, valves, material callouts, and bill of materials (production: Procedure.md Step 4; content requirements: Specification.md FR-7; typical quantity: 100-200 drawings; drawing conventions: Guidance.md Considerations item 2)
- **Pipe support drawings:** Details for pipe supports, hangers, anchors, guides, and restraints with support loads and structural attachment details (production: Procedure.md Step 5; content requirements: Specification.md FR-8; design rationale: Guidance.md Principles item 4; load verification: Procedure.md Step 10; cross-reference DEL-14.03)
- **Phase 2 connection details:** Interface provisions for future Phase 2 expansion (source: OBJ-8 Future Expandability; production: Procedure.md Step 6; content requirements: Specification.md FR-9; design rationale: Guidance.md Principles item 5; **TBD** Phase 2 scope and interface requirements — location TBD: ER Volume 2 Part 2)

**Key piping systems** (source: Decomposition PKG-14 Scope — functional requirements: Specification.md FR-1 through FR-4; system integration: Guidance.md Principles item 2):

- **Railcar unloading headers:** Piping from railcar unloading stations to storage tanks or direct to marine loading (interface requirements: Specification.md IR-9; coordination: Procedure.md Step 1, Step 8; transient analysis: cross-reference DEL-14.06 Transient Analysis Study Report – Railcar Unloading Line; Specification.md QR-7)
- **Marine loading export lines:** Piping from storage tanks or railcar headers to marine loading arms at berth (interface requirements: Specification.md IR-10; coordination: Procedure.md Step 1, Step 8; transient analysis: cross-reference DEL-14.07 Transient Analysis Study Report – Marine Loading Line; Specification.md QR-7)
- **Product recycle lines:** Piping for product recirculation during operations (operational flexibility per OBJ-4; typical use: tank blending, pump priming, system flushing; functional requirement: Specification.md FR-2)
- **Nitrogen distribution piping:** Piping from Employer-supplied nitrogen skid to tank blanketing and equipment purging points (interface requirements: Specification.md IR-8; interface coordination: Procedure.md Step 1; material considerations: Guidance.md Principles item 3; scope boundary per Decision DEC-07 — Contractor scope limited to connection piping)
- **Tank farm piping connections:** Piping to/from three 15,000 MT storage tanks (interface requirements: Specification.md IR-6; interface coordination: Procedure.md Step 1, Step 8; storage capacity per OBJ-3)
- **Metering connections:** Piping tie-ins for custody transfer metering (interface requirements: Specification.md IR-11; interface coordination: Procedure.md Step 1, Step 8; accuracy requirements per OBJ-10)

**Materials:** **TBD** — **ASSUMPTION**: Carbon steel (ASTM A106 Grade B or equivalent) typical for CSD canola oil liquid service; stainless steel (ASTM A312 Grade 304 or 316) for nitrogen distribution, clean-in-place systems, or where food-grade contact requirements apply; confirm per DEL-14.02 (Piping Technical Specification) and DEL-14.04 (Data Sheet Package) — material selection rationale: Guidance.md Principles item 3; trade-offs: Guidance.md Trade-offs item 1; specifications: Specification.md Standards section

**Piping sizes:** **TBD** — to be determined by hydraulic calculations (DEL-14.03); **ASSUMPTION**: typical range DN 50 (2") to DN 400 (16") for liquid transfer; DN 25 (1") to DN 100 (4") for nitrogen distribution (sizing basis: Procedure.md Step 1; requirements: Specification.md PR-4)

**Special interface** (source: Decomposition Decision DEC-07 — requirements: Specification.md IR-8; coordination: Procedure.md Step 1):
- Nitrogen skid supplied by Employer; Contractor responsible for connection piping only — **TBD** interface drawing and connection details from Employer (considerations: Guidance.md Considerations item 1)

**Construction constraints:**
- **Terminal continuity:** Design must minimize disturbance to existing Terminal operations (source: OBJ-5) — requirements: Specification.md FR-4; considerations: Guidance.md Considerations item 4; constructability evaluation: Procedure.md Step 3
- **Constructability:** **TBD** — coordination with structural, electrical, and instrumentation disciplines — requirements: Specification.md IR-1, IR-2, IR-3; coordination procedure: Procedure.md Step 8 (IDC)
- **Modularization:** **TBD** — evaluate opportunities for pre-fabrication and skid-mounted assemblies — considerations: Guidance.md Considerations item 4; trade-offs: Guidance.md Trade-offs item 3
- **Access for maintenance:** Design shall provide access for valve operation, maintenance, and future replacement — **ASSUMPTION**: minimum clearances per ASME B31.3 and good engineering practice (requirements: Specification.md Standards section; considerations: Guidance.md Considerations item 5)

## References

**Project References:**
- Decomposition file: /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md
- Context file: `_CONTEXT.md`
- Employer's Requirements Volume 2 Part 1 — General Requirements (location: test/Volume_2_Part_1_Employers_Requirements.pdf; referenced in: Procedure.md Prerequisites; Specification.md Standards section)
- Employer's Requirements Volume 2 Part 2 — Civil & Process Mechanical Works (location: test/Volume_2_Part_2_Employers_Requirements.pdf; referenced in: Procedure.md Step 1; Specification.md Standards section)

**Applicable Standards:**
- ASME B31.3 — Process Piping (detailed in Specification.md Standards section; rationale: Guidance.md Principles item 1; verification: Procedure.md Step 10)
- **TBD** — Additional codes per ER (location TBD: ER Volume 2 Part 2) — Specification.md Standards section
- **ASSUMPTION**: MSS SP-58 (Pipe Hangers and Supports — Materials, Design, Manufacture) likely applicable (Guidance.md Principles item 4; Specification.md Standards section)
- **ASSUMPTION**: MSS SP-69 (Pipe Hangers and Supports — Selection and Application) likely applicable (Guidance.md Principles item 4; Specification.md Standards section)
- **ASSUMPTION**: ISA 5.1 (Instrumentation Symbols and Identification) for P&ID symbology (Specification.md Standards section; Procedure.md Step 2)
- **ASSUMPTION**: CSA Z662 (Oil and Gas Pipeline Systems) may apply to nitrogen distribution; confirm scope boundaries (Guidance.md Principles section; Specification.md Standards section)
- **ASSUMPTION**: NBC 2020 for seismic and structural loads; confirm design basis (Specification.md PR-6; Guidance.md Principles item 4)

**Cross-references (related deliverables):**
- DEL-14.02 (Process Piping Technical Specification) — for material and workmanship requirements (Specification.md Standards section; Guidance.md Principles item 3; Procedure.md Prerequisites)
- DEL-14.03 (Process Piping Design Calculations) — for sizing, stress analysis, and flexibility analysis basis (Specification.md PR-4, PR-5, PR-6, PR-7, QR-5, QR-6; Guidance.md Trade-offs item 2; Procedure.md Step 10)
- DEL-14.04 (Process Piping Data Sheet Package) — for line list and piping material data (Specification.md IR-4 through IR-7; Procedure.md Step 4)
- DEL-14.05 (Process Piping Installation & Test Records) — for fabrication, installation, and testing documentation
- DEL-14.06 (Transient Analysis Study Report — Railcar Unloading Line) — for surge analysis and mitigation (Specification.md QR-7; Procedure.md Step 10)
- DEL-14.07 (Transient Analysis Study Report — Marine Loading Line) — for surge analysis and mitigation (Specification.md QR-7; Procedure.md Step 10)
- DEL-14.08 (Valve Closing Time Verification Summary) — for valve timing verification (Procedure.md Step 10)
- DEL-10.01 (Railcar Unloading System Design Drawings) — for railcar unloading interface (Specification.md IR-9; Procedure.md Step 1, Step 8)
- DEL-11.01 (Marine Loading System Design Drawings) — for marine loading interface (Specification.md IR-10; Procedure.md Step 1, Step 8)
- DEL-13.01 (Storage Tank Design Drawings) — for tank nozzle locations and sizes (Specification.md IR-6; Procedure.md Step 1, Step 8)
- DEL-15.01 (Pump Design Drawings) and DEL-15.04 (Pump Data Sheets) — for pump nozzle connections (Specification.md IR-4, IR-5; Procedure.md Step 1, Step 8)
- DEL-16.01 (Valve Design Drawings) — for valve specifications (Specification.md IR-7; Procedure.md Step 1, Step 8)
- PKG-19 (Control Systems) — for P&ID instrumentation and control logic (Specification.md IR-3; Procedure.md Step 2, Step 8)
- PKG-05 (Concrete Structures) and PKG-06 (Structural Steelwork) — for pipe support attachment points (Specification.md IR-2; Procedure.md Step 1, Step 5, Step 8)
- See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)

**Related Project Objectives** (source: Decomposition Section 6 — requirements: Specification.md Functional Requirements):
- OBJ-2: Throughput Capacity (1,000,000 MT/annum) — Specification.md FR-1, FR-5, PR-4
- OBJ-4: Operational Flexibility (tank storage and direct rail-to-ship transfer) — Specification.md FR-2; Guidance.md Principles item 2
- OBJ-8: Future Expandability (Phase 2 expansion provisions) — Specification.md FR-3, FR-9; Guidance.md Principles item 5; Procedure.md Step 6
