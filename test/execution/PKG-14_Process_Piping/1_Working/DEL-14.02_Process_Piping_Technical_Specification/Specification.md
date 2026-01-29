# Specification: DEL-14.02 Process Piping Technical Specification

## Scope

This specification defines the requirements for **Process Piping Technical Specification** within **PKG-14 Process Piping**.

**Description** (source: Decomposition DEL-14.02; attributes: Datasheet.md Specification Type; rationale: Guidance.md Purpose): Defines performance, materials, and workmanship requirements for process piping per ER requirements.

**Deliverable outputs** (source: Decomposition DEL-14.02; attributes: Datasheet.md Specification Sections; procedure: Procedure.md Step 2):
- Piping material specification (construction: Datasheet.md Construction item 1; procedure: Procedure.md Step 2a; examples: Guidance.md Examples item 1)
- Pipe support specification (construction: Datasheet.md Construction item 2; procedure: Procedure.md Step 2b; examples: Guidance.md Examples item 2)
- Insulation specification (construction: Datasheet.md Construction item 3; procedure: Procedure.md Step 2c; examples: Guidance.md Examples item 3)

**Piping systems covered** (source: Decomposition PKG-14 Scope; applicability: Datasheet.md Conditions; referenced in DEL-14.01):
- Railcar unloading headers
- Marine loading export lines
- Product recycle lines
- Nitrogen distribution piping
- Tank farm piping connections
- All associated pipe supports and insulation

**Product context** (source: Decomposition Section 1.1; applicability: Datasheet.md Conditions; rationale: Guidance.md Purpose):
- CSD (Crude Super Degummed) canola oil (requirements: FR-1; rationale: Guidance.md Principles item 1)
- 1,000,000 MT per annum throughput (requirements: FR-4; referenced in DEL-14.01)
- Food-grade service requirements (requirements: FR-1, PR-2, PR-4; considerations: Datasheet.md Special considerations - Food-grade service; rationale: Guidance.md Principles item 1)

## Requirements

### Functional Requirements

**Piping Material Specification** (construction: Datasheet.md Construction item 1; rationale: Guidance.md Principles item 1, item 2; procedure: Procedure.md Step 2a):
- FR-1: Specification shall define piping materials suitable for CSD canola oil service (food-grade compatibility, non-toxic, non-contaminating) (product: Datasheet.md Product Handled; rationale: Guidance.md Principles item 1; considerations: Datasheet.md Special considerations - Food-grade service; procedure: Procedure.md Step 2a; verification: Verification - Material verification; cross-reference DEL-14.04)
- FR-2: Specification shall define materials for operating temperature range **TBD** (location TBD: ER Volume 2 Part 2) — **ASSUMPTION**: -10°C to +60°C (conditions: Datasheet.md Operating temperature range; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 1, Step 2a; referenced in DEL-14.01)
- FR-3: Specification shall define materials for operating pressure range **TBD** (varies by system; cross-reference DEL-14.03) (conditions: Datasheet.md Operating pressure; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 1, Step 2a; materials: Datasheet.md Typical materials - Flanges)
- FR-4: Specification shall support throughput capacity of 1,000,000 MT/annum (source: OBJ-2) through appropriate pipe sizes and pressure ratings (applicability: Datasheet.md Throughput; rationale: Guidance.md Principles item 1; procedure: Procedure.md Step 1, Step 2a; verification: Verification - Specification review; referenced in DEL-14.01)
- FR-5: Specification shall define materials suitable for coastal/marine environment (corrosion resistance, protective coatings) (conditions: Datasheet.md Environmental classification; rationale: Guidance.md Principles item 1; considerations: Datasheet.md Special considerations - Corrosion protection; procedure: Procedure.md Step 2a; trade-offs: Guidance.md Trade-offs item 1)

**Pipe Support Specification** (construction: Datasheet.md Construction item 2; rationale: Guidance.md Principles item 3; procedure: Procedure.md Step 2b):
- FR-6: Specification shall define pipe support types and design criteria to support piping under operational loads, thermal expansion, and seismic loads (rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations item 1; procedure: Procedure.md Step 2b; verification: Verification - Fabrication verification; cross-reference DEL-14.03)
- FR-7: Specification shall define support materials suitable for coastal/marine environment (conditions: Datasheet.md Environmental classification; rationale: Guidance.md Principles item 1, item 3; considerations: Datasheet.md Special considerations - Corrosion protection; procedure: Procedure.md Step 2b; examples: Guidance.md Examples item 2)
- FR-8: Support design shall comply with ASME B31.3 requirements and **TBD** seismic criteria (**ASSUMPTION**: NBC 2020; location TBD: ER Volume 2 Part 1) (code: Datasheet.md Applicable Standard; conditions: Datasheet.md Seismic requirements; rationale: Guidance.md Principles item 3; procedure: Procedure.md Step 2b; standards: Standards - Pipe supports)

**Insulation Specification** (construction: Datasheet.md Construction item 3; rationale: Guidance.md Principles item 4; procedure: Procedure.md Step 2c):
- FR-9: Specification shall define insulation requirements for personnel protection (hot surfaces) and/or energy conservation — **TBD** extent and philosophy (location TBD: ER Volume 2 Part 2) (considerations: Datasheet.md Construction item 3 - ASSUMPTION; rationale: Guidance.md Principles item 4; trade-offs: Guidance.md Trade-offs item 4; procedure: Procedure.md Step 2c)
- FR-10: Insulation materials shall be suitable for coastal/marine environment (weather-resistant jacketing) (conditions: Datasheet.md Environmental classification; rationale: Guidance.md Principles item 4; procedure: Procedure.md Step 2c; examples: Guidance.md Examples item 3)

### Performance Requirements

**Material performance** (rationale: Guidance.md Principles item 1, item 2; procedure: Procedure.md Step 2a):
- PR-1: Piping materials shall withstand design pressure and temperature per ASME B31.3 without failure or leakage (code: Datasheet.md Applicable Standard; requirements: FR-2, FR-3; rationale: Guidance.md Principles item 2; verification: Verification - Installation verification)
- PR-2: Materials shall be compatible with CSD canola oil (no corrosion, no contamination, no product degradation) (product: Datasheet.md Product Handled; requirements: FR-1; rationale: Guidance.md Principles item 1; considerations: Datasheet.md Special considerations - Food-grade service; procedure: Procedure.md Step 2a; verification: Verification - Material verification)
- PR-3: Materials shall have appropriate corrosion allowance for design life **TBD** — **ASSUMPTION**: 25 years (location TBD: ER Volume 2 Part 1) (conditions: Datasheet.md Design life, Corrosion allowance; requirements: FR-5; rationale: Guidance.md Principles item 1; trade-offs: Guidance.md Trade-offs item 1; procedure: Procedure.md Step 2a)
- PR-4: Gasket materials shall provide leak-tight seals under operating conditions and be food-grade compatible (materials: Datasheet.md Typical materials - Gaskets; requirements: FR-1; rationale: Guidance.md Principles item 1; procedure: Procedure.md Step 2a; examples: Guidance.md Examples item 1)

**Fabrication and workmanship** (rationale: Guidance.md Principles item 5; procedure: Procedure.md Step 2):
- PR-5: Welding shall comply with ASME B31.3 and AWS D1.1 (or equivalent) — **TBD** welding procedures and qualifications (location TBD: ER Volume 2 Part 2) (code: Datasheet.md Applicable Standard; rationale: Guidance.md Principles item 5; standards: Standards - Welding and fabrication; verification: Verification - Fabrication verification; cross-reference DEL-14.05)
- PR-6: Pipe supports shall be fabricated and installed to design loads with appropriate tolerances — **TBD** fabrication and installation tolerances (requirements: FR-6; construction: Datasheet.md Construction item 2 - Installation requirements; procedure: Procedure.md Step 2b; verification: Verification - Installation verification)
- PR-7: Insulation installation shall achieve specified thermal performance and weather protection — **TBD** insulation performance criteria (requirements: FR-9; construction: Datasheet.md Construction item 3 - Application methods; procedure: Procedure.md Step 2c; verification: Verification - Installation verification)

**Quality and testing** (rationale: Guidance.md Principles item 5; procedure: Procedure.md Step 2a, Step 7):
- PR-8: Piping materials shall be supplied with material test reports (MTRs) and certificates of compliance (construction: Datasheet.md Construction item 1 - Material testing; rationale: Guidance.md Principles item 5; quality requirements: QR-5; procedure: Procedure.md Step 2a, Step 7; verification: Verification - Material verification; examples: Guidance.md Examples item 1)
- PR-9: Fabricated piping shall undergo non-destructive examination (NDE) per ASME B31.3 — **TBD** NDE extent and methods (radiography, ultrasonic, etc.) (code: Datasheet.md Applicable Standard; rationale: Guidance.md Principles item 5; standards: Standards - Testing and inspection; verification: Verification - Fabrication verification; cross-reference DEL-14.05)
- PR-10: Completed piping shall undergo hydrostatic testing per ASME B31.3 — **TBD** test pressure and duration (typically 1.5 times design pressure) (code: Datasheet.md Applicable Standard; rationale: Guidance.md Principles item 5; standards: Standards - Testing and inspection; verification: Verification - Installation verification; cross-reference DEL-14.05)

### Interface Requirements

**Interdisciplinary coordination** (considerations: Guidance.md Considerations item 2; procedure: Procedure.md Step 3):
- IR-1: Piping material specification shall coordinate with piping drawings (DEL-14.01) — material callouts on drawings match specification (cross-reference DEL-14.01, DEL-14.04; considerations: Guidance.md Considerations item 2; procedure: Procedure.md Prerequisites; examples: Guidance.md Examples item 4)
- IR-2: Pipe support specification shall coordinate with structural design (PKG-05, PKG-06) — support loads and attachment details (requirements: FR-6; construction: Datasheet.md Construction item 2 - Attachment details; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations item 2; procedure: Procedure.md Step 2b, Step 3; cross-reference PKG-05, PKG-06)
- IR-3: Insulation specification shall coordinate with piping layout for access and maintenance clearances (requirements: FR-9; considerations: Guidance.md Considerations item 2, item 5; procedure: Procedure.md Step 3; cross-reference DEL-14.01)

**Equipment interfaces** (considerations: Guidance.md Considerations item 2; procedure: Procedure.md Step 1, Step 3):
- IR-4: Piping materials shall be compatible with pump materials and ratings (cross-reference PKG-15 Pumps; considerations: Guidance.md Considerations item 2; procedure: Procedure.md Prerequisites, Step 1, Step 3)
- IR-5: Piping materials shall be compatible with valve materials and ratings (construction: Datasheet.md Construction item 1 - Valve materials; cross-reference PKG-16 Valves; considerations: Guidance.md Considerations item 2; procedure: Procedure.md Prerequisites, Step 2a, Step 3)
- IR-6: Piping materials shall match tank nozzle materials and ratings (cross-reference PKG-13 Storage Tanks; considerations: Guidance.md Considerations item 2; procedure: Procedure.md Prerequisites, Step 3)

**System interfaces** (considerations: Datasheet.md Special considerations - Nitrogen distribution; procedure: Procedure.md Step 1):
- IR-7: Nitrogen distribution piping materials shall be suitable for nitrogen service and coordinate with Employer-supplied nitrogen skid (Decision DEC-07) — **TBD** nitrogen pressure and purity requirements (construction: Datasheet.md Construction item 1; considerations: Datasheet.md Special considerations - Nitrogen distribution; procedure: Procedure.md Prerequisites, Step 1; referenced in DEL-14.01)

### Quality Requirements

**Specification development** (rationale: Guidance.md Principles item 2, item 5; procedure: Procedure.md Steps 1-6):
- QR-1: Specification shall comply with ASME B31.3 material requirements (Chapter II — Materials) (code: Datasheet.md Applicable Standard; rationale: Guidance.md Principles item 2; standards: Standards - Process piping design; procedure: Procedure.md Step 1, Step 2a; verification: Verification - Specification review; examples: Guidance.md Examples item 5)
- QR-2: Specification shall comply with Employer's Requirements — **TBD** ER material and quality requirements (location TBD: ER Volume 2 Part 2) (conditions: Datasheet.md Applicability; procedure: Procedure.md Prerequisites, Step 1; verification: Verification - Specification review)
- QR-3: Specification shall be reviewed and approved per project quality procedures — **TBD** review and approval matrix (attributes: Datasheet.md Revision; procedure: Procedure.md Steps 3-6; verification: Verification - Specification review)

**Material procurement** (rationale: Guidance.md Principles item 5; considerations: Guidance.md Considerations item 4; procedure: Procedure.md Step 7):
- QR-4: All piping materials shall be procured from qualified suppliers with appropriate certifications and traceability (rationale: Guidance.md Principles item 5; procedure: Procedure.md Step 7; verification: Verification - Material verification)
- QR-5: Material test reports (MTRs) shall be submitted for all pressure-containing components (pipe, fittings, flanges, bolting) (performance: PR-8; rationale: Guidance.md Principles item 5; construction: Datasheet.md Construction item 1 - Material testing; procedure: Procedure.md Step 2a, Step 7; verification: Verification - Material verification; examples: Guidance.md Examples item 1)
- QR-6: Materials shall be identified and traceable from receipt through installation (rationale: Guidance.md Principles item 5; procedure: Procedure.md Step 2a, Step 7; verification: Verification - Material verification)

**Fabrication and installation quality** (rationale: Guidance.md Principles item 5; procedure: Procedure.md Step 2, Step 7):
- QR-7: Welding procedures and welder qualifications shall comply with ASME B31.3 and project quality plan — **TBD** qualification requirements (performance: PR-5; rationale: Guidance.md Principles item 5; standards: Standards - Welding and fabrication; procedure: Procedure.md Step 2a; verification: Verification - Fabrication verification)
- QR-8: Inspection and testing shall comply with ASME B31.3 and project quality plan (performance: PR-9, PR-10; rationale: Guidance.md Principles item 5; standards: Standards - Testing and inspection; verification: Verification - Fabrication verification, Installation verification; cross-reference DEL-14.05)

## Standards

**Applicable codes and standards:**

**Process piping design and materials** (code: Datasheet.md Applicable Standard; rationale: Guidance.md Principles item 2; procedure: Procedure.md Prerequisites, Step 1, Step 2a):
- ASME B31.3 — Process Piping (governing code for design, materials, fabrication, assembly, erection, examination, inspection, testing) (requirements: QR-1, PR-1, PR-5, PR-9, PR-10; rationale: Guidance.md Principles item 2; examples: Guidance.md Examples item 5; referenced in DEL-14.01)
- ASME B16.5 — Pipe Flanges and Flanged Fittings (flange dimensions, pressure-temperature ratings) (materials: Datasheet.md Typical materials - Flanges; procedure: Procedure.md Prerequisites, Step 2a; examples: Guidance.md Examples item 1, item 5)
- ASME B16.9 — Factory-Made Wrought Butt-Welding Fittings (fitting dimensions and tolerances) (materials: Datasheet.md Typical materials - Fittings; procedure: Procedure.md Prerequisites, Step 2a; examples: Guidance.md Examples item 1, item 5)
- ASME B16.11 — Forged Fittings, Socket-Welding and Threaded (small-bore fitting dimensions) (materials: Datasheet.md Typical materials - Fittings; procedure: Procedure.md Prerequisites, Step 2a; examples: Guidance.md Examples item 1)
- ASME B16.20 — Metallic Gaskets for Pipe Flanges (gasket dimensions and materials) (materials: Datasheet.md Typical materials - Gaskets; procedure: Procedure.md Step 2a; examples: Guidance.md Examples item 1)
- ASME B16.21 — Nonmetallic Flat Gaskets for Pipe Flanges (gasket materials and dimensions) (materials: Datasheet.md Typical materials - Gaskets; procedure: Procedure.md Step 2a; examples: Guidance.md Examples item 1)

**Piping materials** (construction: Datasheet.md Construction item 1; procedure: Procedure.md Prerequisites, Step 2a; examples: Guidance.md Examples item 1):
- ASTM A106 — Seamless Carbon Steel Pipe for High-Temperature Service (materials: Datasheet.md Typical materials - Pipe; procedure: Procedure.md Step 2a)
- ASTM A53 — Pipe, Steel, Black and Hot-Dipped, Zinc-Coated, Welded and Seamless (materials: Datasheet.md Typical materials - Pipe; procedure: Procedure.md Step 2a)
- ASTM A312 — Seamless, Welded, and Heavily Cold Worked Austenitic Stainless Steel Pipes (if stainless steel required) (materials: Datasheet.md Typical materials - Pipe; procedure: Procedure.md Step 2a)
- ASTM A193 / A194 — Alloy-Steel and Stainless Steel Bolting Materials (bolts and nuts) (materials: Datasheet.md Typical materials - Bolting; procedure: Procedure.md Step 2a; examples: Guidance.md Examples item 1)
- **TBD** — Additional material standards per ER and service requirements (location TBD: ER Volume 2 Part 2; requirements: QR-2; procedure: Procedure.md Step 1)

**Pipe supports** (construction: Datasheet.md Construction item 2; rationale: Guidance.md Principles item 3; procedure: Procedure.md Prerequisites, Step 2b):
- **TBD** — MSS SP-58 (Pipe Hangers and Supports — Materials, Design, Manufacture) — **ASSUMPTION**: likely applicable (rationale: Guidance.md Principles item 3; procedure: Procedure.md Prerequisites; examples: Guidance.md Examples item 2, item 5; referenced in DEL-14.01)
- **TBD** — MSS SP-69 (Pipe Hangers and Supports — Selection and Application) — **ASSUMPTION**: likely applicable (rationale: Guidance.md Principles item 3; procedure: Procedure.md Prerequisites; examples: Guidance.md Examples item 2; referenced in DEL-14.01)
- AISC 360 — Specification for Structural Steel Buildings (if applicable to support design) (procedure: Procedure.md Step 2b; examples: Guidance.md Examples item 2)

**Insulation** (construction: Datasheet.md Construction item 3; rationale: Guidance.md Principles item 4; procedure: Procedure.md Prerequisites, Step 2c):
- **TBD** — ASTM C547 (Mineral Fiber Pipe Insulation) or equivalent (location TBD: ER Volume 2 Part 2; procedure: Procedure.md Prerequisites, Step 2c; examples: Guidance.md Examples item 3)
- **TBD** — ASTM C552 (Cellular Glass Thermal Insulation) or equivalent (procedure: Procedure.md Prerequisites, Step 2c; examples: Guidance.md Examples item 3)
- **TBD** — ASTM C1136 (Flexible, Low Permeance Vapor Retarders for Thermal Insulation) (procedure: Procedure.md Step 2c; examples: Guidance.md Examples item 3)

**Welding and fabrication** (performance: PR-5; rationale: Guidance.md Principles item 5; procedure: Procedure.md Step 2a; considerations: Guidance.md Considerations item 4):
- AWS D1.1 — Structural Welding Code — Steel (or equivalent) (performance: PR-5; requirements: QR-7; procedure: Procedure.md Step 2a)
- ASME Section IX — Welding and Brazing Qualifications (welder and procedure qualifications) (performance: PR-5; rationale: Guidance.md Principles item 5; requirements: QR-7; verification: Verification - Fabrication verification)

**Testing and inspection** (performance: PR-9, PR-10; rationale: Guidance.md Principles item 5; verification: Verification sections):
- ASME B31.3 Chapter VI — Inspection, Examination, and Testing (hydrostatic testing, NDE requirements) (performance: PR-9, PR-10; requirements: QR-8; rationale: Guidance.md Principles item 5; verification: Verification - Fabrication verification, Installation verification)
- **TBD** — NDT methods and acceptance criteria (location TBD: ER Volume 2 Part 2; performance: PR-9; verification: Verification - Fabrication verification)

**Project-specific requirements** (requirements: QR-2; procedure: Procedure.md Prerequisites, Step 1):
- Employer's Requirements Volume 2 Part 1 — General Requirements (procedure: Procedure.md Prerequisites)
- Employer's Requirements Volume 2 Part 2 — Civil & Process Mechanical Works (requirements: QR-2; procedure: Procedure.md Prerequisites, Step 1)
- Project Quality Management Plan — **TBD** (location TBD; requirements: QR-3, QR-7, QR-8; procedure: Procedure.md Prerequisites)

## Verification

**Verification methods:**

**Specification review** (requirements: QR-1, QR-2, QR-3; procedure: Procedure.md Steps 3-5):
- Technical review by discipline lead (mechanical/piping engineer) (procedure: Procedure.md Step 6; verification table row: Step 1)
- Interdisciplinary review (coordination with structural, process, instrumentation disciplines) (interfaces: IR-1, IR-2, IR-3; considerations: Guidance.md Considerations item 2; procedure: Procedure.md Step 3; verification table row: Step 3)
- Compliance review against ASME B31.3 and ER requirements (requirements: QR-1, QR-2; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 1, Step 4; verification table rows: Steps 1, 4)
- Employer review and approval — **TBD** submittal and approval requirements (location TBD: ER Volume 2 Part 1; requirements: QR-3; procedure: Procedure.md Step 5; verification table row: Step 5)

**Material verification** (performance: PR-2, PR-8; quality: QR-4, QR-5, QR-6; rationale: Guidance.md Principles item 5; procedure: Procedure.md Step 7):
- Material test reports (MTRs) reviewed and approved prior to fabrication (performance: PR-8; quality: QR-5; rationale: Guidance.md Principles item 5; procedure: Procedure.md Step 7; verification table row: Step 7)
- Material traceability verified (heat numbers, certifications) (quality: QR-6; rationale: Guidance.md Principles item 5; procedure: Procedure.md Step 7)
- Material inspection at receipt (dimensional, visual, documentation) (procedure: Procedure.md Step 7)

**Fabrication verification** (performance: PR-5, PR-6, PR-9; quality: QR-7; rationale: Guidance.md Principles item 5):
- Welding procedure specifications (WPS) and procedure qualification records (PQR) reviewed and approved (performance: PR-5; quality: QR-7; rationale: Guidance.md Principles item 5; standards: Standards - Welding and fabrication)
- Welder qualifications verified (performance: PR-5; quality: QR-7; rationale: Guidance.md Principles item 5)
- In-process inspection (fit-up, weld quality, dimensions) (quality: QR-8)
- Non-destructive examination (NDE) per ASME B31.3 — **TBD** extent and methods (performance: PR-9; quality: QR-8; standards: Standards - Testing and inspection)

**Installation verification** (performance: PR-1, PR-6, PR-7, PR-10; quality: QR-8; cross-reference DEL-14.05):
- Pipe support installation inspection (loads, locations, tolerances) (performance: PR-6; requirements: FR-6; procedure: Procedure.md Step 2b)
- Insulation installation inspection (thickness, jacketing, weather protection) (performance: PR-7; requirements: FR-9, FR-10; procedure: Procedure.md Step 2c)
- Hydrostatic testing per ASME B31.3 (test pressure, duration, acceptance criteria) (performance: PR-10; rationale: Guidance.md Principles item 5; standards: Standards - Testing and inspection; cross-reference DEL-14.05)
- Final inspection and acceptance (quality: QR-8; cross-reference DEL-14.05 Installation & Test Records)

**Acceptance criteria:**
- Specification approved by Employer (if required) — **TBD** approval requirements (requirements: QR-3; procedure: Procedure.md Step 5; verification table row: Step 5)
- All materials comply with specification and have required certifications (quality: QR-4, QR-5; verification: Material verification above)
- All fabrication and installation comply with specification and pass inspection/testing (performance: PR-5, PR-6, PR-7, PR-9, PR-10; quality: QR-7, QR-8; verification: Fabrication and Installation verification above)
- **TBD** — Additional acceptance criteria per project quality procedures (requirements: QR-3; procedure: Procedure.md verification table)

## Documentation

**Required documentation outputs:**

**Specification documents** (source: Decomposition DEL-14.02; attributes: Datasheet.md Specification Sections; procedure: Procedure.md Records section):
- Piping Material Specification (pipe, fittings, flanges, gaskets, bolting, valves, special items, testing requirements) (construction: Datasheet.md Construction item 1; requirements: FR-1 through FR-5; procedure: Procedure.md Step 2a; examples: Guidance.md Examples item 1)
- Pipe Support Specification (support types, materials, design criteria, installation requirements) (construction: Datasheet.md Construction item 2; requirements: FR-6, FR-7, FR-8; procedure: Procedure.md Step 2b; examples: Guidance.md Examples item 2)
- Insulation Specification (insulation materials, thicknesses, jacketing, application methods) (construction: Datasheet.md Construction item 3; requirements: FR-9, FR-10; procedure: Procedure.md Step 2c; examples: Guidance.md Examples item 3)

**Supporting documentation** (procedure: Procedure.md Records section):
- Material selection basis (rationale for material choices, service conditions, compatibility) (rationale: Guidance.md Principles item 1; procedure: Procedure.md Step 2a; examples: Guidance.md Examples item 4)
- Material standards and specifications index (listing of all applicable ASTM, ASME, etc.) (standards: Standards section; procedure: Procedure.md Step 2a; examples: Guidance.md Examples item 1)
- Typical details and standard specifications (for supports, insulation, etc.) (construction: Datasheet.md Construction items 2-3; procedure: Procedure.md Step 2b, Step 2c; examples: Guidance.md Examples items 2-3)

**Documentation requirements:**
- All specification documents shall comply with project document control procedures (attributes: Datasheet.md Document Number, Revision; requirements: QR-3; procedure: Procedure.md Step 6)
- Revision control per project numbering system — **TBD** (location TBD: project procedures; attributes: Datasheet.md Revision; requirements: QR-3; procedure: Procedure.md Step 6, Records section)
- Electronic format: **TBD** — **ASSUMPTION**: PDF for issued specifications, Word/native format for working copies (procedure: Procedure.md Records section)
- Storage location: `2_Checking/` (during review) → `3_Issued/` (upon approval) (procedure: Procedure.md Step 6, Records section)
- Submittal requirements: **TBD** — submittal schedule and approval workflow (location TBD: ER Volume 2 Part 1; requirements: QR-3; verification: Verification - Specification review; procedure: Procedure.md Step 5)
- Integration with procurement: Specifications shall be referenced in procurement documents and purchase orders (considerations: Guidance.md Considerations item 4; procedure: Procedure.md Step 7)
- As-built documentation: **TBD** — requirements for as-built updates based on actual materials procured and installed (procedure: Procedure.md Records section; cross-reference DEL-14.05)
