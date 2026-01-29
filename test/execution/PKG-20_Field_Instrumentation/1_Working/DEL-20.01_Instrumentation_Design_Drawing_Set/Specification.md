# Specification: DEL-20.01 Instrumentation Design Drawing Set

## Scope

This specification defines the requirements for the **Instrumentation Design Drawing Set** within **PKG-20 Field Instrumentation** for the Canola Oil Transload Facility Phase 1 at Fraser Surrey Terminal, Surrey, BC.

**Deliverable Purpose:**

Defines the design arrangement and details for instrumentation per ER requirements.

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, DEL-20.01 description (line 496)

**Package Scope:**

PKG-20 Field Instrumentation includes field instruments, transmitters, switches, instrument cabling, and junction boxes.

**Source:** Decomposition document, PKG-20 Scope (line 490)

**Deliverable Artifacts:**

This drawing set shall include:

| Artifact | Description | Datasheet § | Guidance § | Procedure Step |
|----------|-------------|-------------|------------|----------------|
| Instrument location plans | Spatial arrangement of field instruments on facility layout | Construction | Example 1 | 2.1, 3.1 |
| Instrument installation details | Mounting, support, and connection details for field instruments | Construction | Example 2 | 2.3, 3.2 |
| Cable schedules | Instrument cable routing, termination, and specifications | Construction | Example 3 | 2.2, 3.3 |

**Source:** Decomposition document, DEL-20.01 Anticipated Artifacts (line 496); `_CONTEXT.md`

**Inclusions:**
- Field instrument locations and elevations
- Instrument mounting and support details
- Instrument cable routing arrangements
- Junction box locations and schedules
- Instrument hook-up details (typical and specific)
- Cable schedule tables with termination information

**Exclusions:**
- Control system architecture (see PKG-22 Control Systems & SCADA)
- Electrical power distribution (see PKG-17 Electrical Power Distribution)
- Instrument procurement specifications (see DEL-20.02 Instrumentation Technical Specification)
- Instrument data sheets (see DEL-20.04 Instrumentation Data Sheet Package)

**Source:** **ASSUMPTION** based on deliverable type (Drawing) and typical EPC package boundaries

## Requirements

### Functional Requirements

**FR-1: Drawing Content**

The Instrumentation Design Drawing Set shall provide sufficient detail to support:

| Purpose | Description | Datasheet § | Guidance § | Procedure Step |
|---------|-------------|-------------|------------|----------------|
| Equipment procurement | Instrument mounting requirements | Attributes | Downstream Use | 5.2 |
| Construction and installation | Field installation guidance | Construction | Downstream Impacts | 3.1, 3.2, 3.3 |
| Commissioning and testing | Loop verification, as-built records | Construction | Downstream Impacts | 6.2 |
| Operations and maintenance | Instrument location reference | Construction | Downstream Use | Records |

**Source:** **ASSUMPTION** based on typical drawing deliverable purpose for design-build projects

**FR-2: Instrument Location Plans**

The drawing set shall include instrument location plans showing:

| Element | Description | Datasheet § | Guidance § | Procedure Step |
|---------|-------------|-------------|------------|----------------|
| Tag numbers | All field instruments by tag number (per ISA 5.1 tagging convention — **TBD**: Project tagging standard) | Construction | ISA 5.1 Context | 3.1 |
| Elevations | Instrument elevations and orientations | Construction | Example 1 | 3.1 |
| Access | Access requirements for installation and maintenance | Construction | Principle 4 | 3.1 |
| Coordination | Coordination with structural, piping, and electrical disciplines | Construction | Principle 5 | 4.4 |

**Source:** Anticipated artifacts (line 496) and **ASSUMPTION** based on ISA 5.1 instrumentation practices

**FR-3: Installation Details**

The drawing set shall include installation details showing:

| Element | Description | Datasheet § | Guidance § | Procedure Step |
|---------|-------------|-------------|------------|----------------|
| Mounting | Instrument mounting arrangements (pipe-mounted, vessel-mounted, structure-mounted) | Installation Requirements | Example 2 | 3.2 |
| Support | Support and bracket details | Installation Requirements | Example 2 | 3.2 |
| Connections | Tubing and wiring connection details | Installation Requirements | Example 2 | 3.2 |
| Weatherproofing | Weatherproofing and environmental protection | Installation Requirements | Principle 2 | 3.2 |
| Hazardous area | Hazardous area seal and cable gland details (**TBD**: per facility hazardous area classification) | Installation Requirements | Principle 3 | 3.2 |

**Source:** Anticipated artifacts (line 496) and **ASSUMPTION** based on typical I&C installation requirements

**FR-4: Cable Schedules**

The drawing set shall include cable schedules showing:

| Element | Description | Datasheet § | Guidance § | Procedure Step |
|---------|-------------|-------------|------------|----------------|
| Identification | Cable identification and tagging | Construction | Example 3 | 3.3 |
| Routing | Cable routing from field instruments to termination points | Construction | Cable Routing | 3.3 |
| Specifications | Cable specifications (conductor size, insulation, shielding) | Construction | Example 3 | 3.3 |
| Terminations | Termination details (junction boxes, marshalling cabinets, control panels) | Construction | Junction Box Locations | 3.3 |

**Source:** Anticipated artifacts (line 496) and **ASSUMPTION** based on typical I&C cable documentation

**FR-5: Coordination with Process Design**

Instrument locations shall be coordinated with:

| Coordination Item | Description | Related Package | Guidance § | Procedure Step |
|-------------------|-------------|-----------------|------------|----------------|
| P&IDs | Process instrument tagging and loop identification | Process Engineering | Upstream Dependencies | 1.1 |
| Piping arrangements | Connection points, accessibility | PKG-14 Process Piping | Principle 5 | 2.1 |
| Equipment layouts | Vessel nozzles, tank penetrations | PKG-13, PKG-15 | Principle 5 | 2.1 |
| Structural design | Platform access, cable tray routing | Structural packages | Principle 5 | 2.1 |

**Source:** **ASSUMPTION** based on interdisciplinary coordination requirements for design-build projects

**FR-6: Project-Specific Requirements**

Drawings shall address project-specific facility context:

| Context | Description | Datasheet § | Guidance § | Procedure Step |
|---------|-------------|-------------|------------|----------------|
| Canola oil service | Material compatibility, process conditions | Conditions | Facility Type | 1.1 |
| Marine terminal | Corrosion protection, weathering | Conditions | Location: Marine Terminal | 1.1 |
| Railcar unloading | 32 stations, instrument coverage | Key Project Parameters | Railcar Unloading Example | 3.1 |
| Storage tanks | 3 × 15,000 MT tanks, level/temperature monitoring | Key Project Parameters | Storage Tanks Example | 3.1 |
| Custody transfer | Accurate measurement for export loading | Key Project Parameters | Marine Loading Example | 3.1 |

**Source:** Decomposition Section 1.1 Project Overview (Key Parameters) and **ASSUMPTION** based on facility function

### Performance Requirements

**PR-1: Drawing Attributes and Standards**

All drawings shall comply with the following attributes (see Datasheet.md Attributes section for detailed specifications):

| Attribute | Value | Datasheet § | Guidance § | Procedure Step |
|-----------|-------|-------------|------------|----------------|
| Drawing Scale | **TBD** — **ASSUMPTION**: Typical scales 1:50, 1:100 for plans; NTS for details | Attributes | Trade-off 3 | 3.1 |
| Sheet Size | **TBD** — **ASSUMPTION**: ISO A1 or ANSI D per project CAD standards | Attributes | — | 3.1 |
| CAD Standard | **TBD** — To be confirmed per project document management plan | Attributes | CAD Standards | 1.3 |
| Drawing Format | **TBD** — **ASSUMPTION**: Electronic PDF/DWG per project requirements | Attributes | — | 5.2 |
| Revision Control | Per project document control procedures (see Procedure.md Step 6) | Attributes | Quality Considerations | 6.1 |
| Classification | **TBD** — **ASSUMPTION**: Contractor's Design Documents (for construction) | Attributes | — | 5.2 |

**PR-2: Symbology and Conventions**

| Element | Requirement | Datasheet § | Guidance § | Procedure Step |
|---------|-------------|-------------|------------|----------------|
| Instrumentation symbology | Shall comply with ISA 5.1 | References | ISA 5.1 Context | 3.1 |
| Discipline drawing standards | **TBD**: I&C drawing conventions to be defined | Attributes | — | 1.3 |
| Project CAD standards | **TBD**: Layer naming, line weights, text styles per project standards | Attributes | — | 1.3 |

**PR-3: Information Completeness**

Drawings shall be sufficiently complete for:

| Purpose | Completeness Level | Guidance § | Procedure Step |
|---------|-------------------|------------|----------------|
| Construction bidding | If applicable | Trade-off 4 | 5.2 |
| Field installation | Without additional engineering input | Downstream Impacts | 5.2 |
| Commissioning | Tag identification, termination verification | Downstream Impacts | 6.2 |

**Source:** **ASSUMPTION** based on design-build deliverable maturity expectations

**PR-4: Drawing Accuracy**

| Accuracy Element | Requirement | Guidance § | Procedure Step |
|------------------|-------------|------------|----------------|
| Instrument locations | Dimensioned and coordinated with as-designed piping and equipment arrangements | Upstream Dependencies | 3.1 |
| Installation details | Reflect manufacturer requirements and site conditions | Technical Considerations | 3.2 |
| Cable schedules | Match control system I/O allocation (**TBD**: coordinate with PKG-22 Control Systems) | Coordination Considerations | 3.3 |

**Source:** **ASSUMPTION** based on typical drawing accuracy requirements

### Interface Requirements

**INT-1: Interdisciplinary Coordination**

This deliverable interfaces with:

| Package | Interface Description | Datasheet § | Guidance § | Procedure Step |
|---------|----------------------|-------------|------------|----------------|
| PKG-12 Product Transfer and Metering | Custody transfer instrumentation | Interface Packages | Marine Loading Example | 2.1 |
| PKG-13 Storage Tanks | Tank instrumentation (level, temperature) | Interface Packages | Storage Tanks Example | 2.1 |
| PKG-14 Process Piping | Instrument connections to process piping | Interface Packages | Principle 5 | 2.1 |
| PKG-15 Pumps and Rotating Equipment | Equipment instrumentation (pressure, flow, vibration) | Interface Packages | Principle 5 | 2.1 |
| PKG-17 Electrical Power Distribution | Power supply to instruments | Interface Packages | Power Supply | 3.2 |
| PKG-22 Control Systems & SCADA | Control system I/O and network architecture | Interface Packages | Principle 5 | 3.3 |
| PKG-23 Electrical Infrastructure | Power supply to instruments, cable routing infrastructure | Interface Packages | Cable Routing | 2.2 |

**Source:** **ASSUMPTION** based on typical I&C interfaces and decomposition package structure

**INT-2: Deliverable Dependencies**

See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies coordinated externally by humans.

**Typical upstream inputs** (coordination required):

| Input | Source | Guidance § | Procedure Step |
|-------|--------|------------|----------------|
| P&IDs and instrument lists | Process Engineering | Upstream Dependencies | 1.1 |
| Equipment layouts and piping arrangements | PKG-14, Layout | Upstream Dependencies | 2.1 |
| Hazardous area classification drawings | PKG-17 | Upstream Dependencies | 1.1 |
| Control system architecture and I/O requirements | PKG-22 | Upstream Dependencies | 3.3 |

**Typical downstream users:**

| User | Purpose | Guidance § | Procedure Step |
|------|---------|------------|----------------|
| Construction contractors | Field installation | Downstream Impacts | 5.2 |
| Commissioning team | Loop verification | Downstream Impacts | 6.2 |
| Operations | As-built reference | Downstream Use | Records |

**Source:** **ASSUMPTION** based on typical EPC workflow

### Quality Requirements

**QR-1: Design Review**

All drawings shall undergo:

| Review Type | Reviewer | Guidance § | Procedure Step |
|-------------|----------|------------|----------------|
| Self-check | Originator | Verification Activities | 4.2 |
| Interdisciplinary check (IDC) | Affected disciplines | Verification Activities | 4.4 |
| Independent peer review | Qualified I&C engineer | Verification Activities | 4.3 |
| Approval | Discipline lead | Verification Activities | 5.1 |

**Source:** **ASSUMPTION** based on typical EPC quality procedures

**QR-2: Drawing Revision Control**

| Requirement | Description | Datasheet § | Guidance § | Procedure Step |
|-------------|-------------|-------------|------------|----------------|
| Revision control | All drawings shall be revision-controlled per project document control procedures | Attributes | Quality Considerations | 6.1 |
| Change tracking | Drawing changes shall be tracked and marked on revised drawings | Attributes | Quality Considerations | 6.1 |
| Archive | Superseded drawings shall be archived per project document management plan | — | Quality Considerations | 6.1 |

**TBD**: Project numbering and revision system

**Source:** **ASSUMPTION** based on typical document control requirements

**QR-3: Compliance Verification**

Drawings shall be verified for compliance with:

| Compliance Item | Source | Guidance § | Procedure Step |
|-----------------|--------|------------|----------------|
| Project design basis and Employer's Requirements | **TBD**: Specific ER sections to be identified | Standards Context | 4.1 |
| Applicable codes and standards | See Standards section below | Standards Context | 4.1 |
| Project quality management plan | **TBD**: Project QA/QC procedures | Quality Considerations | 4.1 |

**Source:** **ASSUMPTION** based on typical quality assurance requirements

**QR-4: As-Built Documentation**

Drawing set shall be updated to reflect as-built conditions:

| Update | Description | Guidance § | Procedure Step |
|--------|-------------|------------|----------------|
| Field modifications | During construction | — | 6.2 |
| Commissioning findings | Adjustments | — | 6.2 |
| Final locations | Final instrument locations and cable routing | — | 6.2 |

**Source:** **ASSUMPTION** based on typical design-build as-built requirements

## Standards

**I&C Discipline Standards (Applicable):**

| Standard | Description | Applicability | Datasheet § | Guidance § |
|----------|-------------|---------------|-------------|------------|
| ISA 5.1 | Instrumentation Symbols and Identification | **ASSUMPTION**: Governs instrument tagging, symbology, and drawing conventions; **TBD**: Specific clauses to be referenced pending access to standard | References | ISA 5.1 Context |
| ISA 84 / IEC 61511 | Functional Safety of Safety Instrumented Systems | **ASSUMPTION**: Applicable if safety instrumented functions (SIF) are included in facility design; **TBD**: Applicability to be confirmed based on process safety requirements | References | ISA 84 Context |
| API 554 | Process Instrumentation and Control | **ASSUMPTION**: Applicable for process industry instrumentation design practices; **TBD**: Specific sections relevant to drawing preparation | References | API 554 Context |

**Electrical and Hazardous Area Standards:**

| Standard | Description | Applicability | Datasheet § | Guidance § |
|----------|-------------|---------------|-------------|------------|
| CSA C22.1 | Canadian Electrical Code | **ASSUMPTION**: Governs hazardous area installation, wiring methods, and cable specifications for BC location; **TBD**: Specific requirements for instrumentation wiring in hazardous areas | References | CSA C22.1 Context |
| CSA C22.2 No. 30 / IEC 60079 | Explosive Atmospheres | **ASSUMPTION**: Applicable for hazardous area classification and instrument enclosure selection; **TBD**: Facility hazardous area classification to be confirmed | — | Principle 3 |

**Design and Construction Standards:**

| Standard | Description | Applicability | Datasheet § | Guidance § |
|----------|-------------|---------------|-------------|------------|
| NBC 2015 | National Building Code of Canada | **ASSUMPTION**: Governs structural loads, seismic design for instrument supports; **TBD**: Seismic design parameters for Surrey, BC location | Conditions | Location: Marine Terminal |
| CSA Z662 | Oil and Gas Pipeline Systems | **ASSUMPTION**: May be applicable for instrument connections to process piping; **TBD**: Applicability to be confirmed based on piping system classification | — | — |

**Project-Specific Standards:**

- **Employer's Requirements** — Project-specific design criteria and performance standards
  - **TBD**: Specific sections to be identified from Volume 2 Parts 1-3
  - **Source:** Decomposition Section 3 Reference Documents (lines 75-79) — Employer's Requirements volumes listed

**Note:** Standards applicability and specific clause-level requirements **TBD** pending access to standard documents and Employer's Requirements. Current standard list is **ASSUMPTION** based on I&C discipline typical practice and Canadian regulatory context.

## Verification

**Verification Methods:**

| Requirement | Verification Method | Responsibility | Datasheet § | Guidance § | Procedure Step |
|-------------|---------------------|----------------|-------------|------------|----------------|
| FR-1: Drawing content completeness | Design review checklist | I&C Lead Engineer | Construction | Design Review Stages | 4.2, 4.3 |
| FR-2: Instrument location coordination | Interdisciplinary check (IDC) | All affected disciplines | Construction | IDC Process | 4.4 |
| FR-3: Installation detail accuracy | Manufacturer data review | I&C Engineer | Installation Requirements | Technical Considerations | 3.2 |
| FR-4: Cable schedule consistency | Control system I/O cross-check | I&C + Electrical | Construction | Coordination Considerations | 3.3 |
| PR-2: Standards compliance | Code compliance review | I&C Lead + QA | References | Standards Context | 4.1 |
| PR-1: CAD standards compliance | Drawing standards audit | CAD Manager | Attributes | — | 4.1 |

**Implementation:** See Procedure.md Section "Verification" for detailed verification activities and acceptance criteria.

**Source:** **ASSUMPTION** based on typical EPC verification methods for drawing deliverables

**Acceptance Criteria:**

| Criterion | Verification | Guidance § | Procedure Step |
|-----------|--------------|------------|----------------|
| All instruments from P&IDs are located and detailed on drawings | Completeness check | Design Review Stages | 4.2 |
| All interdisciplinary coordination issues are resolved (no open IDC comments) | IDC sign-off | IDC Process | 4.4 |
| Drawings are approved by discipline lead (signed and stamped per professional requirements) | Approval | Verification Activities | 5.1 |
| Drawings comply with project CAD standards and naming conventions | Standards audit | Quality Considerations | 4.1 |
| All hazardous area installations comply with electrical code requirements | Code compliance review | Principle 3 | 4.1 |

**TBD**: Project-specific criteria, hazardous area classification

**Source:** **ASSUMPTION** based on typical drawing deliverable acceptance criteria

**Hold Points:**

- **TBD** — Hold points for Employer review to be identified per project execution plan
- **ASSUMPTION**: Typical hold points may include 30%, 60%, 90% design reviews and IFC (Issued for Construction)

## Documentation

**Required Documentation Outputs:**

| Output | Format | Content | Datasheet § | Guidance § | Procedure Step |
|--------|--------|---------|-------------|------------|----------------|
| Instrument Location Plans | **TBD** — **ASSUMPTION**: CAD drawings (PDF + native DWG/DGN) | Spatial arrangement of instruments | Construction | Example 1 | 3.1, Records |
| Instrument Installation Details | **TBD** — **ASSUMPTION**: CAD drawings (PDF + native DWG/DGN) | Typical and specific mounting/connection details | Construction | Example 2 | 3.2, Records |
| Cable Schedules | **TBD** — **ASSUMPTION**: Tabular schedules embedded in drawings or separate database export | Cable identification, routing, specifications, terminations | Construction | Example 3 | 3.3, Records |

**Naming convention:** **TBD** — Per project document numbering system
**Revision control:** Per project document control procedures

**Source:** Decomposition DEL-20.01 Anticipated Artifacts (line 496)

**Documentation Management:**

| Requirement | Description | Guidance § | Procedure Step |
|-------------|-------------|------------|----------------|
| Document control | All documentation shall be managed per project document control procedures | Quality Considerations | 5.3 |
| Storage | Drawings shall be stored in project document repository with access control | Quality Considerations | Records |
| Distribution | Revisions shall be tracked and distributed per project change management procedures | Quality Considerations | 5.2, 6.1 |
| Archive | Final issue shall be archived as as-built documentation per project closeout requirements | Quality Considerations | 6.2 |

**TBD**: Document management system and protocols

**Source:** **ASSUMPTION** based on typical EPC document management requirements

**Supporting Documentation:**

| Document | Relationship | Deliverable |
|----------|--------------|-------------|
| Design calculation records | Sizing and verification basis | DEL-20.03 Instrumentation Design Calculations |
| Instrument data sheets | Equipment data | DEL-20.04 Instrumentation Data Sheet Package |
| Installation test records | Commissioning documentation | DEL-20.05 Instrumentation Installation & Test Records |

**Source:** Cross-reference to related PKG-20 deliverables per decomposition (lines 497-500)

**Project Objective Alignment:**

This deliverable supports **OBJ-1: Safe & Reliable Operation** — ensuring field instrumentation is properly designed, located, and installed for safe and reliable facility operations.

**Source:** Decomposition Section 6 Objective-to-Deliverable Mapping (line 780)

## Cross-Document Traceability

This Specification defines the requirements for DEL-20.01. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Datasheet.md | Factual identification, attributes, conditions, references | Attributes § provides values for PR-1; Conditions § provides context for FR-6; References § lists standards |
| Guidance.md | Engineering rationale and decision context | Principles explain "why" behind requirements; Trade-offs address design options; Examples illustrate application |
| Procedure.md | Production workflow and verification steps | Steps 1-6 implement requirements; Verification section implements QR-1 to QR-4; Records section implements Documentation |

**Requirement-to-Guidance Mapping:**

| Requirement | Guidance Section | Rationale Summary |
|-------------|------------------|-------------------|
| FR-1 Drawing Content | Downstream Use | Drawings serve procurement, construction, commissioning, operations |
| FR-2 Instrument Location Plans | Example 1 | Location plans show spatial arrangement with tag numbers and elevations |
| FR-3 Installation Details | Principles 2, 3, 4 | Details must address environment, hazardous areas, accessibility |
| FR-4 Cable Schedules | Example 3 | Cable schedules link instruments to control system I/O |
| FR-5 Coordination | Principle 5 | Instrumentation design is inherently cross-disciplinary |
| FR-6 Project-Specific | Facility Type, Examples | Canola oil transload facility context drives specific requirements |
