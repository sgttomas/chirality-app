# Specification: DEL-13.01 Storage Tank Design Drawing Set

## Scope

This specification defines the requirements for **Storage Tank Design Drawing Set** within **PKG-13 Storage Tanks**.

### Deliverable Description

Defines the design arrangement and details for storage tank per ER requirements.

**Source:** _CONTEXT.md, Decomposition document DEL-13.01

### Coverage

**Included:**
- Tank general arrangements for 3 × 15,000 MT atmospheric storage tanks
- Foundation drawings and anchor bolt details
- Nozzle schedules showing all connections and orientations
- Roof details including structure, support, access, and venting
- Agitator mounting and support details
- Tank appurtenances (overflow protection, water draw-off, Phase 2 connections)
- Interface drawings with adjacent systems (piping, instrumentation, foundations)

**Source:** _CONTEXT.md (Anticipated Artifacts), Decomposition PKG-13 Scope

**Excluded:**
- Detailed fabrication drawings (responsibility of tank fabricator per typical design-build split — **ASSUMPTION**)
- Process flow diagrams (covered by process design deliverables — **ASSUMPTION**)
- Detailed piping design beyond tank nozzle interfaces (covered by PKG-14 Process Piping)
- Instrumentation details beyond mounting provisions (covered by PKG-20 Field Instrumentation)
- Foundation structural design calculations (covered by DEL-13.03 and PKG-05 Concrete Structures)
- Coating application procedures (covered by PKG-26 Protective Coatings & Painting)

**Source:** ASSUMPTION based on typical design-build responsibility splits and decomposition package structure

---

## Requirements

### Functional Requirements

**FR-01: Storage Capacity**
- The tank design shall provide 3 tanks with 15,000 MT capacity each for a total of 45,000 MT storage capacity
- Capacity basis: CSD (Crude Super Degummed) canola oil
- **Verification:** Tank volume calculations in DEL-13.03 shall demonstrate compliance
- **Datasheet Link:** Tank Configuration — Number of Tanks, Capacity per Tank, Total Storage Capacity
- **Source:** Decomposition document, Section 1.1 (Key Parameters); OBJ-3 (Storage Capacity)

**FR-02: Product Compatibility**
- Tanks shall be suitable for storage of CSD canola oil
- Material selection shall ensure compatibility with canola oil properties (temperature, chemical composition)
- **TBD** — Specific product properties (specific gravity, viscosity, corrosivity) and compatibility requirements require ER extraction (Volume 2 Part 2) or product specification
- **Verification:** Material compatibility analysis and coating selection in DEL-13.02
- **Datasheet Link:** Tank Configuration — Product; Materials — Coating System (Internal)
- **Source:** Decomposition document, Section 1.1 (Key Parameters)

**FR-03: Throughput Support**
- Tank design shall support facility throughput of 1,000,000 MT per annum
- **TBD** — Specific filling/discharge rates require coordination with PKG-10 (Railcar Unloading System) and PKG-11 (Marine Loading System)
- **Verification:** Hydraulic analysis and nozzle sizing in DEL-13.03
- **Datasheet Link:** Operating Conditions — Filling Rate, Turnover Rate
- **Source:** Decomposition document, Section 1.1 (Key Parameters); OBJ-2 (Throughput Capacity)

**FR-04: Operational Flexibility**
- Tank design shall support both tank storage operations and direct rail-to-ship transfer scenarios
- **TBD** — Specific operational modes and sequencing require ER extraction (Volume 2 Part 2)
- **Verification:** Operational analysis in process design documentation
- **Datasheet Link:** Operating Conditions — Product Compatibility, Turnover Rate
- **Source:** OBJ-4 (Operational Flexibility)

**FR-05: Future Expandability**
- Tank design shall include provisions for Phase 2 connections and expansion
- Phase 2 interface points shall be clearly identified and protected on drawings
- **TBD** — Specific Phase 2 connection requirements (sizes, locations, services) require ER extraction (Volume 2 Part 2)
- **Verification:** Phase 2 provisions shown on Tank GAs and documented in DEL-31.08 (O&M Manuals)
- **Datasheet Link:** Internals and Appurtenances — Phase 2 Connections
- **Source:** Decomposition PKG-13 Scope; OBJ-8 (Future Expandability)

### Performance Requirements

**PR-01: Design Standard**
- Tanks shall be designed in accordance with API 650: Welded Tanks for Oil Storage
- **TBD** — Edition and addenda to be specified per ER (Volume 2 Part 2)
- **Verification:** Design calculations (DEL-13.03) shall reference applicable API 650 clauses
- **Datasheet Link:** Tank Configuration — Tank Standard
- **Source:** Decomposition PKG-13 Scope

**PR-02: Seismic Design**
- Tank design shall comply with seismic requirements for Fraser Surrey Terminal location (Surrey, BC)
- Seismic design per API 650 Appendix E and NBC 2020
- **TBD** — Site-specific seismic parameters (PGA, spectral acceleration, site class) require ER extraction (Volume 2 Part 2) or site-specific seismic study
- **Verification:** Seismic calculations in DEL-13.03 per API 650 Appendix E; foundation anchorage design if required
- **Datasheet Link:** Design Conditions — Seismic Design, Seismic Parameters; Structural Details — Anchor Chairs, Foundation Anchor Bolts
- **Source:** ASSUMPTION based on BC location; Datasheet.md Conditions section

**PR-03: Environmental Loads**
- Tank design shall account for wind, snow, and temperature loads per local conditions (Surrey, BC)
- **TBD** — Specific design wind speed, snow load, and temperature range require ER extraction (Volume 2 Part 2) and NBC 2020
- **Verification:** Wind, snow, and thermal analysis in DEL-13.03
- **Datasheet Link:** Design Conditions — Design Wind Speed, Snow Load, Design Temperature Range
- **Source:** ASSUMPTION based on location and API 650 requirements

**PR-04: Foundation Performance**
- Foundation design shall limit settlement within API 650 allowable limits
- **TBD** — Specific settlement criteria (maximum total, maximum differential) and foundation type require geotechnical report (DEL-02.04) and design calculations (DEL-13.03)
- **Verification:** Foundation settlement analysis in DEL-13.03 and PKG-05 foundation design
- **Datasheet Link:** Foundation — Foundation Type, Bearing Capacity
- **Source:** API 650 foundation requirements (Appendix B)

**PR-05: Agitator Performance**
- Agitators shall maintain product uniformity and prevent settling
- **TBD** — Agitator type, power, mixing requirements, mixing cycle require ER extraction (Volume 2 Part 2) and vendor data
- **Verification:** Agitator selection and performance verification in DEL-13.04 (agitator data sheets)
- **Datasheet Link:** Internals and Appurtenances — Agitators, Agitator Type
- **Source:** Decomposition PKG-13 Scope (agitators)

**PR-06: Overflow Protection**
- Overflow protection system shall prevent tank overfilling beyond safe capacity
- **TBD** — Overflow protection type (overflow nozzle, spillway), capacity, and interface requirements require ER extraction (Volume 2 Part 2)
- **Verification:** Overflow system design shown on Tank GAs and nozzle schedules; coordination with PKG-19 (high-level alarms)
- **Datasheet Link:** Internals and Appurtenances — Overflow Protection; Nozzles and Connections — Overflow Connections
- **Source:** Decomposition PKG-13 Scope (overflow protection)

**PR-07: Water Draw-off**
- Water draw-off system shall enable removal of water accumulation from tank bottom
- **TBD** — Water draw-off design requirements (nozzle size, location, drainage routing) require ER extraction (Volume 2 Part 2)
- **Verification:** Water draw-off details shown on Tank GAs and nozzle schedules
- **Datasheet Link:** Internals and Appurtenances — Water Draw-off; Nozzles and Connections — Drain Connections
- **Source:** Decomposition PKG-13 Scope (water draw-off)

### Interface Requirements

**IR-01: Foundation Interface**
- Tank design shall coordinate with foundation design (PKG-05 Concrete Structures)
- Foundation drawings shall show anchor bolt layout, foundation loading (dead load, seismic, wind overturning), and interface details
- **TBD** — Foundation type (ring wall, mat, piles) and design criteria require coordination with DEL-05.01 and DEL-13.03
- **Verification:** Foundation interface coordination documented in IDC records; foundation drawings issued to PKG-05
- **Datasheet Link:** Foundation — Foundation Type, Foundation Design Standard, Bearing Capacity
- **Source:** Anticipated Artifacts (foundation drawings); typical tank-foundation interface

**IR-02: Piping Interface**
- Nozzle schedule shall define all nozzle sizes, ratings, orientations, elevations, and connection types
- Nozzle locations shall coordinate with piping layout (PKG-14 Process Piping) and P&IDs
- **TBD** — Specific nozzle requirements (inlet/outlet sizes, vent sizes, drain sizes) and piping interfaces require P&ID development and PKG-14 coordination
- **Verification:** Nozzle schedule coordination with P&IDs and PKG-14 documented in IDC records
- **Datasheet Link:** Nozzles and Connections — all nozzle attributes
- **Source:** Anticipated Artifacts (nozzle schedules); typical tank-piping interface

**IR-03: Instrumentation Interface**
- Tank design shall provide mounting points, nozzles, and access for instrumentation (PKG-20 Field Instrumentation)
- **TBD** — Specific instrumentation requirements (level type, temperature points, pressure monitoring) require coordination with PKG-20
- **Verification:** Instrumentation nozzles and mounting provisions shown on Tank GAs and nozzle schedules; coordination documented in IDC records
- **Datasheet Link:** Internals and Appurtenances — Level Instrumentation, Temperature Instrumentation; Nozzles and Connections — Instrumentation Connections
- **Source:** Typical tank instrumentation requirements

**IR-04: Fire Protection Interface**
- Tank spacing and layout shall coordinate with fire protection requirements (PKG-23 Fire Protection)
- **TBD** — Tank spacing (shell-to-shell), foam system interfaces, fire water connections require coordination with PKG-23
- **Verification:** Tank spacing and fire protection interfaces documented in site layout drawings and IDC records
- **Datasheet Link:** Limiting Conditions — Tank Spacing (Fire Protection); Configuration — Tank Spacing
- **Source:** ASSUMPTION based on typical fire protection requirements for bulk storage facilities

**IR-05: Coating Interface**
- Tank internal and external surfaces shall be prepared for coating application (PKG-26 Protective Coatings & Painting)
- **TBD** — Coating system selection (internal food-grade, external atmospheric) and surface preparation requirements require coordination with PKG-26
- **Verification:** Coating requirements specified in DEL-13.02; surface preparation details coordinated with PKG-26
- **Datasheet Link:** Materials — Coating System (Internal), Coating System (External)
- **Source:** Typical storage tank coating requirements

**IR-06: Dyke/Bunding Interface**
- Tank layout shall coordinate with dyke/bunding design (PKG-05 Concrete Structures)
- **TBD** — Dyke capacity (110% of largest tank typical), configuration, and drainage require coordination with PKG-05 and PKG-03 (drainage)
- **Verification:** Dyke/bunding coordination documented in site layout drawings and IDC records
- **Datasheet Link:** Configuration — Dyke/Bunding
- **Source:** ASSUMPTION based on typical environmental protection requirements; OBJ-7 (Environmental Protection)

### Drawing Standards and Quality Requirements

**DR-01: CAD Standards**
- All drawings shall comply with project CAD standards
- **TBD** — Specific CAD standard (software version, layer conventions, symbology, line weights, text styles) require project CAD manual
- **Verification:** CAD standards check per Procedure.md Step 5 (Self-Check) and Step 6 (IDC)
- **Datasheet Link:** Drawing Set Attributes — CAD Standard
- **Source:** ASSUMPTION based on typical project requirements

**DR-02: Drawing Numbering**
- Drawing numbers shall follow project numbering system
- **TBD** — Project drawing numbering system (format, discipline codes, sequence) requires project document control procedures
- **Verification:** Drawing numbering verified during discipline lead approval (Procedure.md Step 9)
- **Datasheet Link:** Drawing Set Attributes — Drawing Numbers
- **Source:** ASSUMPTION based on typical project requirements

**DR-03: Drawing Format**
- Drawing sheet size, format, and title block shall comply with project standards
- **TBD** — Specific drawing format requirements (sheet size, title block content, revision block format) require project CAD manual and document control procedures
- **Verification:** Drawing format verified during self-check (Procedure.md Step 5)
- **Datasheet Link:** Drawing Set Attributes — Sheet Size, Drawing Format
- **Source:** ASSUMPTION based on typical project requirements

**DR-04: Drawing Quality**
- Drawings shall be checked and approved per project quality procedures
- Minimum checking requirements: self-check, interdisciplinary check (IDC), independent check
- **Verification:** Quality checks documented per Procedure.md Steps 5-7; approval per Step 9
- **Source:** Typical engineering drawing quality control process

**DR-05: Revision Control**
- Drawing revisions shall be controlled per project document control procedures
- **TBD** — Revision tracking conventions (clouds, triangles), revision block format, and approval workflow require project document control procedures
- **Verification:** Revision management per Procedure.md Step 11
- **Datasheet Link:** Drawing Set Attributes — Classification
- **Source:** ASSUMPTION based on typical project requirements

---

## Standards

### Primary Design Standards

| Standard | Title | Application |
|----------|-------|-------------|
| **API 650** | Welded Tanks for Oil Storage | Primary tank design standard — shell, bottom, roof, appurtenances (Source: Decomposition PKG-13 Scope) |
| **API 650 Appendix E** | Seismic Design of Storage Tanks | Seismic design for BC location (Source: ASSUMPTION based on Surrey, BC seismic zone) |
| **API 650 Appendix F** | Atmospheric and Low-Pressure Storage Tank Venting | Normal and emergency venting design (Source: ASSUMPTION based on API 650 scope) |
| **NBC 2020** | National Building Code of Canada 2020 | Wind, snow, seismic loads for Surrey, BC location (Source: ASSUMPTION based on Canadian location) |

### Supporting Standards

| Standard | Title | Application |
|----------|-------|-------------|
| **API 653** | Tank Inspection, Repair, Alteration, and Reconstruction | Reference for future maintenance and inspection (Source: ASSUMPTION) |
| **CSA B51** | Boiler, Pressure Vessel and Pressure Piping Code | Potential application to agitators and pressure equipment (Source: ASSUMPTION) |
| **ASME B31.3** | Process Piping | Nozzle connections and piping interfaces (Source: ASSUMPTION) |
| **CSA G40.21** | Structural Quality Steel | Structural steel material specifications (Source: ASSUMPTION) |
| **CSA W47.1** | Certification of Companies for Fusion Welding of Steel | Fabricator qualification (Source: ASSUMPTION) |
| **CSA W59** | Welded Steel Construction (Metal Arc Welding) | Welding requirements (Source: ASSUMPTION) |
| **CSA Z259** | Fall Protection | Ladder, platform, and fall protection design (Source: ASSUMPTION) |

**Note:** All standards marked ASSUMPTION require confirmation during ER extraction and design development phase.

### Employer's Requirements

- Volume 2 Part 1: Employer's Requirements - General Requirements — **Location TBD**
- Volume 2 Part 2: Employer's Requirements - Civil & Process Mechanical Works — **Location TBD**
- **TBD** — Specific ER clauses applicable to storage tanks (capacity, materials, safety systems, coating, testing) require extraction

---

## Verification

### Design Verification Methods

**V-01: Self-Check**
- Originator reviews drawing for completeness, accuracy, and compliance with standards
- **TBD** — Self-check checklist and criteria require project quality procedures
- **Procedure Link:** Procedure.md Step 5 (Self-Check) defines detailed self-check activities
- **Acceptance Criteria:** AC-01 (Completeness), AC-02 (Accuracy), AC-04 (Standards Compliance)

**V-02: Interdisciplinary Check (IDC)**
- Affected disciplines review drawings for interface coordination and conflicts
- Minimum disciplines: Civil/Structural (PKG-05 foundations), Process (PKG-14 piping), Electrical/I&C (PKG-20 instrumentation), Fire Protection (PKG-23), Coatings (PKG-26)
- **TBD** — IDC process, distribution list, and sign-off requirements require project quality procedures
- **Procedure Link:** Procedure.md Step 6 (Interdisciplinary Check) defines IDC workflow
- **Acceptance Criteria:** AC-03 (Coordination)

**V-03: Independent Check**
- Qualified checker performs peer review of design basis, calculation reference, and drawing accuracy
- Checker shall be independent of originator (not involved in original design)
- **TBD** — Checker qualification requirements (P.Eng., API 650 experience) require project quality procedures
- **Procedure Link:** Procedure.md Step 7 (Independent Check) defines checker review activities
- **Acceptance Criteria:** AC-02 (Accuracy), AC-04 (Standards Compliance)

**V-04: Design Review**
- Formal design review meeting for major design decisions and interfaces
- **TBD** — Design review scope (what triggers review), participants (discipline leads, project manager), and frequency require project quality procedures
- **Procedure Link:** Procedure.md Step 8 (Design Review) defines design review process
- **Acceptance Criteria:** Major design decisions (tank sizing, roof type, foundation type, seismic design, Phase 2 provisions) reviewed and approved

**V-05: Dimensional Verification**
- Critical dimensions and interface points verified against source data (calculations, P&IDs, foundation design)
- **TBD** — Dimensional verification checklist (what dimensions are critical) require project quality procedures
- **Procedure Link:** Embedded in Procedure.md Step 5 (Self-Check) activity 5.2 (Verify accuracy)
- **Acceptance Criteria:** AC-02 (Accuracy)

**V-06: CAD Standards Check**
- Drawing compliance with CAD standards verified (layers, line weights, symbols, text)
- **TBD** — CAD standards checklist require project CAD manual
- **Procedure Link:** Embedded in Procedure.md Step 5 (Self-Check) activity 5.3 (Verify CAD standards compliance)
- **Acceptance Criteria:** AC-04 (Standards Compliance)

### Acceptance Criteria

**AC-01: Completeness**
- All anticipated drawing types are produced and complete per _CONTEXT.md:
  - Tank General Arrangements (3)
  - Foundation Drawings (TBD quantity)
  - Nozzle Schedules (3)
  - Roof Details (TBD quantity)
  - Agitator Drawings (TBD quantity)
- All required views, sections, and details are provided per drawing type
- All dimensions, notes, and annotations are complete (no TBD placeholders on issued drawings)

**AC-02: Accuracy**
- Dimensions and interface points are accurate and verified against design calculations (DEL-13.03)
- Design complies with API 650 and applicable standards (PR-01, PR-02, PR-03)
- Calculations (DEL-13.03) support design shown on drawings
- Nozzle schedule aligns with P&IDs and piping design (PKG-14)
- Foundation interface aligns with structural design (PKG-05)

**AC-03: Coordination**
- Interfaces with adjacent disciplines are coordinated and verified (IR-01 through IR-06)
- IDC comments from PKG-05, PKG-14, PKG-20, PKG-23, PKG-26 are resolved
- No unresolved interface conflicts

**AC-04: Standards Compliance**
- CAD standards compliance verified (DR-01)
- Drawing format and numbering per project standards (DR-02, DR-03, DR-05)
- Technical content complies with API 650 and referenced standards (PR-01)

**AC-05: Approval**
- All required checks completed and signed off (V-01 through V-04 as applicable)
- Discipline lead approval obtained (P.Eng. stamp)
- **TBD** — Client review and approval requirements per ER (Volume 2 Part 2)

---

## Documentation

### Required Drawing Outputs

| Drawing Type | Quantity | Description |
|-------------|----------|-------------|
| **Tank General Arrangements** | 3 | One GA per tank showing overall configuration, dimensions, elevations, nozzle locations, appurtenances |
| **Foundation Drawings** | **TBD** | Foundation plans, sections, anchor bolt layout, loading diagrams (quantity depends on foundation complexity) |
| **Nozzle Schedules** | 3 | Nozzle table for each tank with size, rating, orientation, elevation, service, connection type |
| **Roof Details** | **TBD** | Roof structure, support (rafters, columns), access ladder/platform, vent details (quantity depends on roof type) |
| **Agitator Drawings** | **TBD** | Agitator mounting details, support structure, clearances, loading (quantity depends on agitator configuration) |

**Source:** _CONTEXT.md (Anticipated Artifacts); Decomposition DEL-13.01

### Drawing Management

**DM-01: Document Control**
- All drawings shall be managed per project document control procedures
- Electronic master copies maintained in project document management system
- **TBD** — Document management system (software, access control) and procedures require project specification
- **Procedure Link:** Procedure.md Step 10 (Issuance) activity 10.4 (Manage in project document management system)

**DM-02: Issuance**
- Drawings issued for review: Filed in `2_Checking/To/` with transmittal
- Drawings issued for construction: Filed in `3_Issued/` with issue record
- **TBD** — Issuance workflow (who issues, who approves issuance) and approval matrix require project document control procedures
- **Procedure Link:** Procedure.md Step 10 (Issuance for Review or Construction)

**DM-03: Revision Management**
- Revisions tracked with revision clouds, triangles, and revision block updates
- Revision history maintained on each drawing (revision letter/number, date, description)
- **TBD** — Revision conventions (cloud style, triangle location) require project CAD manual
- **Procedure Link:** Procedure.md Step 11 (Revision Management)

**DM-04: Archive and Retention**
- Superseded revisions archived per project retention policy
- Final as-built drawings maintained for facility lifecycle (permanent record)
- **TBD** — Retention requirements (duration for superseded revisions) require project document control procedures and ER
- **Procedure Link:** Embedded in Procedure.md Step 11 (Revision Management) activity 11.4 (Archive superseded revisions)

---

## Cross-Document References

**For entity attributes and values:** See `Datasheet.md`
- Tank Configuration (3 × 15,000 MT tanks, CSD canola oil) → Referenced in FR-01, FR-02, FR-03
- Tank Standard (API 650) → Referenced in PR-01
- Seismic requirements (BC location) → Referenced in PR-02
- Agitators, Overflow Protection, Water Draw-off, Phase 2 Connections → Referenced in PR-05, PR-06, PR-07, FR-05
- All "Datasheet Link" fields in requirements → Map to specific Datasheet.md attributes

**For design rationale and principles:** See `Guidance.md`
- DP-01: Code Compliance First → Supports PR-01 (API 650 standard)
- DP-02: Safety and Reliability → Supports FR-01, PR-02, PR-06 (capacity, seismic, overflow protection)
- DP-03: Operability and Maintainability → Supports FR-04 (operational flexibility)
- DP-04: Interface Management → Supports IR-01 through IR-06 (all interface requirements)
- DP-05: Future-Proofing → Supports FR-05 (Phase 2 provisions)
- Trade-offs sections (TD-01 through TD-05) → Support performance requirement selections (PR-02, PR-04)

**For verification and production:** See `Procedure.md`
- Verification section → Implements V-01 through V-06 (all verification methods)
- Steps 2-4 → Develop design to meet requirements specified here
- Steps 5-8 → Verify compliance with requirements specified here (acceptance criteria AC-01 through AC-05)
- All "Procedure Link" fields in verification methods → Map to specific Procedure.md steps

---

**Document Status:** Pass 3 Complete (2026-01-28) — All functional, performance, and interface requirements defined with explicit verification methods and acceptance criteria. Requirements linked to Datasheet.md attributes, Guidance.md rationale, and Procedure.md verification steps. TBDs specify information source needed. ASSUMPTIONs labeled with basis. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
