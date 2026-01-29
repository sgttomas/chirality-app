# Specification: DEL-17.01 Electrical Power Design Drawing Set

## Scope

This specification defines the requirements for **Electrical Power Design Drawing Set** within **PKG-17 Electrical Power Distribution**.

**Purpose** (Source: Decomposition DEL-17.01 entry): Defines the design arrangement and details for electrical power per ER requirements.

**Package Scope** (Source: Decomposition Section 4 — PKG-17): MV/LV distribution, transformers, switchgear, MCC, panels, grounding, cable installation.

**Anticipated deliverable artifacts** (Source: _CONTEXT.md):
- Single line diagrams (SLDs)
- MV/LV distribution drawings
- Cable schedules
- Grounding drawings

**Project Context** (Source: Decomposition Section 1):
- **Facility**: Canola oil transload facility at Fraser Surrey Terminal, Surrey, BC
- **Throughput**: 1,000,000 MT/a (OBJ-2)
- **Key Systems**: Railcar unloading (32 positions), storage tanks (3 × 15,000 MT), transfer pumps, marine loading system

## Requirements

### Functional Requirements

**FR-1: System Architecture Representation**
- Drawing set shall represent the complete electrical power distribution architecture from utility point of connection through all distribution levels to end-use equipment.
- **Source**: Decomposition PKG-17 scope (MV/LV distribution, transformers, switchgear, MCC, panels).
- **ASSUMPTION**: Single line diagrams (SLDs) shall show all major electrical equipment, protection devices, and distribution paths.
- **Rationale**: See Guidance.md — Principle 1 (Hierarchical Distribution Architecture).
- **Procedure**: See Procedure.md — Step 3 (Develop Single Line Diagrams).

**FR-2: Medium Voltage Distribution Documentation**
- Drawings shall document MV service incoming from utility (BC Hydro), MV switchgear lineup, sectionalizing and protection scheme, transformer primary connections.
- **Source**: PKG-17 scope (MV/LV distribution, transformers).
- **TBD**: Utility service voltage level (anticipated: 25 kV or 13.8 kV class) — confirm with BC Hydro coordination.
- **Rationale**: See Guidance.md — Principle 2 (Voltage Level Selection).
- **Procedure**: See Procedure.md — Step 4 (Develop MV/LV Distribution Drawings).

**FR-3: Low Voltage Distribution Documentation**
- Drawings shall document LV distribution from transformer secondary through switchgear/MCCs to load centers, motor control centers, and distribution panels.
- **Source**: PKG-17 scope (LV distribution, MCC, panels).
- **ASSUMPTION**: Typical voltage levels: 600V for large motors, 480V for process loads, 208V-120V for lighting and small loads.
- **Rationale**: See Guidance.md — Principle 2 (Voltage Level Selection), Principle 3 (Protection and Coordination).
- **Procedure**: See Procedure.md — Step 4 (Develop MV/LV Distribution Drawings).

**FR-4: Cable Routing and Sizing Documentation**
- Cable schedules shall identify all power cables with circuit designation, conductor size, insulation type, length, routing path, and termination points.
- **Source**: _CONTEXT.md anticipated artifacts (cable schedules); PKG-17 scope (cable installation).
- Cables shall be sized per CEC Section 4 (conductor ampacity) and voltage drop requirements (max 3% for feeders, 5% total per IEEE recommendations).
- **Reference**: See DEL-17.03 (Design Calculations) for cable sizing calculations.
- **Rationale**: See Guidance.md — Consideration 2 (Voltage Drop and Power Quality), Consideration 4 (Cable Routing and Installation Methods).
- **Procedure**: See Procedure.md — Step 5 (Develop Cable Schedules).

**FR-5: Grounding System Documentation**
- Grounding drawings shall document the facility grounding grid, equipment grounding connections, lightning protection system, and bonding of all metallic structures.
- **Source**: _CONTEXT.md anticipated artifacts (grounding drawings); CEC Section 10 (grounding and bonding).
- Grounding system shall comply with IEEE Std 80 (grounding grid design) and CEC requirements.
- **Rationale**: See Guidance.md — Principle 4 (Grounding and Bonding).
- **Procedure**: See Procedure.md — Step 6 (Develop Grounding Drawings).

**FR-6: Load Assignment and Circuit Identification**
- Drawings shall clearly identify all loads, their assigned circuits, protection devices, and power sources.
- Load data shall be consistent with DEL-17.03 (Design Calculations — load analysis).
- Circuit identification shall follow a consistent numbering scheme — **TBD** (per project standards).
- **Rationale**: See Guidance.md — Consideration 1 (Load Characterization and Demand Factors).
- **Procedure**: See Procedure.md — Step 2 (Electrical Load Analysis), Step 3 (Develop SLDs).

### Performance Requirements

**PR-1: Code Compliance**
- All drawings shall represent systems designed to comply with CSA C22.1 (Canadian Electrical Code) and BC Electrical Safety Regulation.
- **Source**: Regulatory requirement (OBJ-6: Regulatory Compliance — Decomposition Section 2).
- Design shall meet BC Safety Authority acceptance for permit and inspection.

**PR-2: Safety and Reliability (OBJ-1)**
- Electrical distribution system design shall provide safe and reliable operation under actual facility operating conditions.
- **Source**: OBJ-1 (Safe & Reliable Operation) — Decomposition Section 2.
- **ASSUMPTION**: Redundancy and N+1 considerations for critical loads — **TBD** per ER requirements (location TBD).
- **Rationale**: See Guidance.md — Principle 3 (Protection and Coordination), Consideration 6 (Redundancy and Reliability).

**PR-3: Capacity and Loading**
- Electrical distribution system shall support the facility throughput capacity of 1,000,000 MT/a.
- **Source**: OBJ-2 (Throughput Capacity) — Decomposition Section 2.
- Load analysis (DEL-17.03) shall confirm adequate capacity for all simultaneous operating scenarios.

**PR-4: Hazardous Area Compliance**
- Equipment and wiring in hazardous areas shall comply with CEC Section 18 (hazardous locations).
- **TBD**: Hazardous area classification boundaries and zone/division designations (to be established by hazardous area classification study).
- **Source**: OBJ-7 (Environmental Protection) — spill containment areas may have Class I Division 2 or Zone 2 classification.
- **Rationale**: See Guidance.md — Principle 5 (Hazardous Area Compliance), Example 4 (Hazardous Area Classification).

**PR-5: Future Expandability (OBJ-8)**
- Electrical distribution design shall facilitate Phase 2 expansion with minimal disruption.
- **Source**: OBJ-8 (Future Expandability) — Decomposition Section 2.
- **ASSUMPTION**: Spare capacity and spare ways in switchgear/MCCs for future loads — **TBD** (percentage of spares per ER).
- **Rationale**: See Guidance.md — Principle 6 (Future Expandability), Trade-off 7 (Spare Capacity Allocation).

### Interface Requirements

**IR-1: Utility Coordination**
- Drawings shall reflect coordination with BC Hydro for service voltage, metering location, protection requirements, and interconnection details.
- **TBD**: Utility service agreement and technical requirements — **location TBD**.

**IR-2: Interdisciplinary Coordination**
- Electrical drawings shall be coordinated with:
  - **PKG-02 (Site Civil Works)**: Underground duct bank routing, grounding grid installation, equipment pads and foundations
  - **PKG-05/PKG-06 (Structures)**: Equipment mounting, cable tray support, conduit penetrations
  - **PKG-13 (Storage Tanks)**: Tank heating loads, tank grounding and bonding
  - **PKG-14 (Process Piping)**: Heat tracing power requirements
  - **PKG-15 (Pumps)**: Motor power connections, motor control centers
  - **PKG-18 (Lighting)**: Lighting load allocations, panel assignments
  - **PKG-19 (Control & Instrumentation)**: Control system power, UPS requirements, instrument power distribution
- **Source**: Decomposition package interdependencies (Section 4) and project coordination requirements.
- Dependencies coordinated externally (per _DEPENDENCIES.md — NOT_TRACKED mode).

**IR-3: Equipment Data Sheet Consistency**
- Electrical equipment shown on drawings shall match equipment specifications in DEL-17.04 (Data Sheet Package).
- Equipment ratings, configurations, and features shall be consistent across drawing set, specifications, and data sheets.

### Quality Requirements

**QR-1: Drawing Standards**
- All drawings shall comply with project CAD manual and drawing standards — **TBD** (location TBD).
- **ASSUMPTION**: Typical requirements include: consistent title block, revision control, layer/line weight standards, text size and font, symbol library usage.

**QR-2: Checking and Review**
- All drawings shall undergo self-check (originator), interdisciplinary check (IDC), and independent check (peer review) before issue.
- **Source**: Project quality management plan (standard practice for design-build projects).
- Checking procedures detailed in Procedure.md.

**QR-3: Revision Control**
- Drawing revisions shall be tracked per project document control procedures.
- Revision clouds and revision descriptions shall clearly identify changes — **TBD** (per project document control manual).

**QR-4: Accuracy and Completeness**
- Drawings shall be dimensionally accurate, complete, and sufficiently detailed for construction purposes.
- Design information shall be traceable to approved calculations (DEL-17.03) and specifications (DEL-17.02).

## Standards

**Primary Codes and Standards** (Canadian jurisdiction):

| Standard | Title | Application |
|----------|-------|-------------|
| **CSA C22.1** | Canadian Electrical Code, Part I (CEC) | Mandatory — primary electrical safety code for BC installations |
| **CSA C22.2** | Canadian Electrical Equipment Standards | Equipment approval and certification requirements |
| **CSA C22.3 No. 7** | Underground Systems, Seismic Requirements | Underground duct banks, cable vaults, seismic anchorage |
| **IEEE C2** | National Electrical Safety Code (NESC) | Utility coordination and overhead/underground construction safety |
| **CSA Z462** | Workplace Electrical Safety | Arc flash hazard analysis, safety labeling, working clearances |

**Reference Standards** (industry practice):

| Standard | Title | Application |
|----------|-------|-------------|
| **IEEE Std 80** | Guide for Safety in AC Substation Grounding | Grounding grid design and step/touch potential analysis |
| **IEEE Std 141 (Red Book)** | Recommended Practice for Electric Power Distribution | Industrial power system design guidance |
| **IEEE Std 142 (Green Book)** | Recommended Practice for Grounding | Equipment and system grounding practices |
| **NFPA 70E** | Electrical Safety in the Workplace | Electrical safety program requirements |
| **ISO 12944** | Corrosion Protection of Steel Structures | Outdoor equipment corrosion protection (marine environment) |

**Regulatory Authority**:
- **BC Safety Standards Act** and **BC Electrical Safety Regulation**
- **BC Safety Authority** (electrical permit and inspection authority)

**Additional Standards**:
- **TBD**: Employer's Requirements (project-specific standards and specifications) — **location TBD** (Volume 2 Parts 1-3)
- **TBD**: BC Hydro service and interconnection standards
- **TBD**: Project-specific CAD and drawing standards

## Verification

**Verification methods for Drawing deliverables**:

| Verification Activity | Method | Acceptance Criteria | Responsibility |
|-----------------------|--------|---------------------|----------------|
| **Self-Check** | Originator review for completeness, accuracy, calculation consistency | No errors or omissions | Drawing originator |
| **Dimensional Verification** | Check all dimensions, elevations, coordinates against survey and civil drawings | Dimensions accurate within tolerance (**TBD**) | Checker |
| **Interdisciplinary Check (IDC)** | Review by affected disciplines for coordination and interface accuracy | No conflicts or missing interfaces | Discipline leads |
| **Code Compliance Check** | Verify design compliance with CEC, CSA, IEEE requirements | All code requirements met and documented | Electrical engineer (P.Eng.) |
| **Calculation Cross-Check** | Verify drawing content matches approved design calculations (DEL-17.03) | Consistency with load analysis, short circuit, voltage drop, protection coordination calcs | Checker / engineer |
| **CAD Standards Compliance** | Check layers, line weights, text, symbols, title block per CAD manual | CAD file complies with project standards | CAD technician / checker |
| **Independent Check** | Peer review by qualified checker (not originator) | Drawing suitable for construction, no significant errors | Independent checker (P.Eng. or certified tech) |

**Acceptance criteria**:
- All verification activities completed and signed off
- No outstanding comments or design issues
- Drawing approved by discipline lead (Professional Engineer stamp required for permit submission)
- **TBD**: Specific sign-off protocol per project quality procedures

## Documentation

**Required documentation outputs** (Source: _CONTEXT.md anticipated artifacts):

1. **Single Line Diagrams (SLDs)**
   - Overall electrical distribution architecture
   - MV and LV distribution one-line representations
   - Protection device coordination (breaker/relay settings shown)
   - Metering and CT/PT locations

2. **MV/LV Distribution Drawings**
   - Site electrical plan showing equipment locations
   - Equipment arrangement and spacing (plan and elevation views)
   - Conduit and cable tray routing
   - Equipment access and working clearances

3. **Cable Schedules**
   - Power cable tabulations (circuit ID, size, type, length, routing, terminations)
   - Cable tray and conduit fill calculations
   - Voltage drop and ampacity verification notes

4. **Grounding Drawings**
   - Site grounding grid layout
   - Equipment grounding connections and bonding details
   - Lightning protection system
   - Grounding electrode locations and connections

**Documentation requirements**:
- All drawings shall comply with project document control procedures
- Revision control per project numbering system — **TBD**
- Format: **ASSUMPTION**: Electronic files (CAD native format and PDF) managed in project document management system
- Hard copy issuance: **TBD** (number of copies for construction, as-built records)
- Drawing register/transmittal: **TBD** (per project document control procedures)

**Deliverable Maturity Stages** (typical design-build):
- **30% Design**: Preliminary single line diagrams, major equipment sizing, site layout concept
- **60% Design**: Detailed SLDs, equipment locations, cable routing, preliminary schedules
- **90% Design**: Complete drawing set for interdisciplinary review and permitting
- **IFC (Issued for Construction)**: Final approved drawings for construction and installation
- **As-Built**: Marked-up drawings reflecting actual installed conditions (post-construction)

**Cross-References**:
- **Datasheet.md**: Drawing set attributes, environmental conditions, and construction requirements
- **Guidance.md**: Engineering rationale for requirements (Principles 1-6), design considerations, and trade-off analysis
- **Procedure.md**: Step-by-step process for producing drawing set (Steps 1-14) and verification procedures matching this specification
- **DEL-17.02** (Electrical Power Technical Specification): Equipment performance and material specifications
- **DEL-17.03** (Electrical Power Design Calculations): Load analysis, short circuit, voltage drop, protection coordination
- **DEL-17.04** (Electrical Power Data Sheet Package): Equipment data sheets and manufacturer information
- **DEL-17.05** (Electrical Power Installation & Test Records): Commissioning test procedures and acceptance criteria

---
**Cross-Document Alignment Verified (Pass 3):** All functional requirements (FR-1 through FR-6), performance requirements (PR-1 through PR-5), and interface requirements (IR-1 through IR-3) are traceable to Datasheet.md attributes, Guidance.md principles/considerations, and Procedure.md steps. No conflicts identified.
