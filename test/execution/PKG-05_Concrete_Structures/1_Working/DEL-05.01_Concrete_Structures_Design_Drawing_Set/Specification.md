# Specification: DEL-05.01 Concrete Structures Design Drawing Set

## Scope

This specification governs development of the **Concrete Structures Design Drawing Set** for **PKG-05 Concrete Structures**. The drawing set defines the design arrangement and details for concrete structures per the Employer's Requirements. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232.)

**Package scope context:** foundations, containment walls, equipment pads, thrust blocks, ground liner system. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226.)

**Project context:** Canola Oil Transload Facility Phase 1, Fraser Surrey Terminal, Surrey, BC. Design & Build contract. Storage capacity 45,000 MT (3 × 15,000 MT tanks). (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:10; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:44; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:41-42.)

**Anticipated artifacts within this drawing set:**
- Foundation plans (tank foundations, equipment pads, building foundations, thrust blocks)
- Containment wall plans (secondary containment for tank farm)
- Equipment pad details (anchor bolt layouts, grout pockets, mounting details)
- Reinforcement drawings (plans/sections/schedules/bar bending details)
- Typical details (joints, embedments, standard reinforcement)

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; Datasheet.md: Construction.)

**Exclusions:**
- Employer-responsible items except for interface connections. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49.)
- Building interior concrete work (covered under PKG-21/PKG-22 if applicable).
- Marine structures concrete (covered under PKG-08 if applicable).

## Requirements

### Functional Requirements

**FR-01: Artifact Coverage**
The drawing set shall cover all anticipated artifacts: foundation plans, containment wall plans, equipment pad details, and reinforcement drawings. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; Datasheet.md: Construction.)

**FR-02: Foundation Details**
The drawing set shall include foundation plans showing:
- Tank foundation layouts for 3 × 15,000 MT storage tanks
- Equipment pad foundation layouts (pumps, metering, railcar unloading equipment)
- Building/control room foundation interfaces (**TBD** extent within PKG-05 scope)
- Thrust block locations and sizing for underground piping systems
- Dimensions, elevations, sections, and construction notes sufficient for construction and QA/QC
(Source: Datasheet.md: Construction; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:41-42.)

**FR-03: Containment Wall Details**
The drawing set shall include containment wall plans and details showing:
- Tank farm secondary containment wall layouts (support OBJ-7 Environmental Protection)
- Wall sections with joint details (construction joints, control joints, expansion joints)
- Waterstop details and penetration sealing requirements
- Ground liner system interface details and coordination notes
- Dimensions, elevations, and notes sufficient for achieving containment performance
(Source: Datasheet.md: Construction; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; Guidance.md: Principles.)

**FR-04: Equipment Pad Details**
The drawing set shall include equipment pad details showing:
- Anchor bolt layouts and embedment details (coordinate with equipment vendor GAs — **TBD**)
- Grout pocket/shim details and mounting elevation control
- Vibration isolation requirements if applicable (**TBD**)
- Sufficient detail for equipment installation and QA/QC verification
(Source: Datasheet.md: Construction; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232.)

**FR-05: Reinforcement Presentation**
The drawing set shall provide reinforcement presentation suitable for fabrication and installation, including:
- Reinforcement plans for foundations, containment walls, and equipment pads
- Bar bending schedules with bar marks and quantities
- Lap splice and coupler specifications
- Clear cover requirements by exposure zone
- Reinforcement congestion details and pour sequence notes
Alternatively, clearly reference a controlled rebar schedule package if maintained elsewhere (**TBD**).
(Source: Datasheet.md: Construction; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232.)

**FR-06: Typical Details**
The drawing set shall include typical details for repetitive elements (**ASSUMPTION** subject to project drafting standards):
- Standard foundation details (footings, pile caps)
- Standard joint details (construction joints, control joints, expansion joints)
- Standard embedment details (anchor bolts, sleeves, blockouts)
- Standard reinforcement details (bar laps, couplers, corner reinforcement)
(Source: Datasheet.md: Construction; Guidance.md: Examples.)

### Performance Requirements

**PR-01: Design Basis Alignment**
Drawings shall reflect the governing design basis as defined in Employer's Requirements and project design basis documents (**TBD** until clauses are extracted):
- Design loads (dead/live/equipment/thermal/storage loads for 45,000 MT capacity)
- Settlement criteria and serviceability limits
- Seismic design parameters (seismic zone, site class, importance factors, R values)
- Durability/exposure requirements (freeze-thaw, de-icing salts, sulfates, chlorides)
- Bearing capacity and settlement tolerances from geotechnical investigation
(Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; Datasheet.md: Conditions.)

**PR-02: Containment Performance**
Containment-related concrete detailing shall support environmental protection intent (OBJ-7):
- Joints designed to prevent leakage (waterstops, sealants as appropriate)
- Liner interfaces detailed to prevent contamination pathways
- Penetrations and embedments sealed to maintain containment integrity
- Construction notes emphasizing quality control for containment elements
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; Guidance.md: Principles.)

**PR-03: Constructability**
Drawings shall consider constructability factors (**ASSUMPTION** — standard structural practice):
- Reinforcement congestion minimized through detailing and sequencing
- Pour sequencing and formwork access noted where critical
- Construction joint locations chosen for structural and construction efficiency
(Source: Guidance.md: Considerations.)

### Interface Requirements

**IR-01: Dependency Coordination**
Interfaces and sequencing dependencies are coordinated externally by humans in NOT_TRACKED mode. Required inputs shall be confirmed before freezing layouts (**TBD** inputs list):
- Equipment loads and anchor bolt layouts from equipment vendors (PKG-10, PKG-11, PKG-13, PKG-15)
- Tank nozzle and anchor layouts from storage tank design (PKG-13)
- Piping support loads and locations (PKG-14)
- Underground utilities and drainage clash avoidance (PKG-03)
- Geotechnical parameters from geotechnical reports (PKG-02)
(Source: `_DEPENDENCIES.md`; test/execution/_Coordination/_COORDINATION.md; Guidance.md: Considerations; Procedure.md: Prerequisites.)

**IR-02: Interface Identification**
The drawing set shall clearly identify interface points and coordination requirements:
- Embedded items (plates/sleeves/blockouts) for other disciplines
- Hold points required for interface verification before concrete placement
- Interface elevations and connection details
- Coordination notes referencing other discipline drawings (**TBD** until interdisciplinary inputs are available)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49; Datasheet.md: Construction; Guidance.md: Considerations.)

### Quality Requirements

**QR-01: Document Control**
Apply project document control and QA/QC requirements as defined in Employer's Requirements (**TBD** pending clause extraction):
- Drawing numbering per project document control system
- Revision tracking and issue status management
- Title block conventions and metadata consistency with Datasheet
- Issue format (PDF and native CAD files per project standards)
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes.)

**QR-02: Checking Process**
Perform checks prior to issue as defined in Procedure.md Steps 6-7:
- Originator self-check (completeness, accuracy, consistency)
- Independent/peer check (technical review, code compliance)
- Interdisciplinary check (IDC) with adjacent disciplines (coordinate interfaces)
- Check evidence retained per QA/QC requirements
(Source: Procedure.md: Steps; Procedure.md: Verification; test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD.)

**QR-03: Technical Consistency**
Maintain consistency with related deliverables:
- Drawing notes and detailing align with DEL-05.03 (Design Calculations) (**TBD** until developed to design maturity)
- Concrete specifications align with DEL-05.02 (Technical Specification) (**TBD** until developed to design maturity)
- Drawing metadata matches Datasheet once project conventions are established
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; Datasheet.md: Attributes.)

## Standards

**Governing requirements:** Employer's Requirements volumes; specific concrete/structural code clauses must be extracted and listed when available. (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD.)

**Applicable design codes and standards (**TBD** — to be confirmed from Employer's Requirements and design basis):**
- Concrete design standard (likely CSA A23.1, CSA A23.3, or applicable BC Building Code references)
- Seismic design standard (likely NBCC or applicable seismic provisions)
- Reinforcing steel standard (likely CSA G30.18 or equivalent)
- Durability and exposure classifications
- Foundation design standards
- Containment and environmental protection standards
- CAD and drafting standards for structural drawings

**ASSUMPTION:** British Columbia location suggests Canadian codes/standards (NBCC, CSA); to be confirmed from ERs.

## Verification

**Completeness Verification:**
- Verify each anticipated artifact listed in Scope exists and is internally consistent (plans/sections/schedules).
- Verify drawing list/sheet index is complete and matches issued drawings.
- Verify general notes, legend, and typical details are present and adequate.
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; Procedure.md: Verification.)

**Document Control Verification:**
- Verify drawing numbering, revisions, and issue status conform to project document control system.
- Verify title blocks match Datasheet metadata (drawing number, revision, status, classification).
- Verify issue format meets project requirements (PDF + native CAD).
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes; Procedure.md: Verification.)

**Technical Alignment Verification:**
- Verify drawing notes and detailing align with DEL-05.03 (Design Calculations) (**TBD** until developed).
- Verify concrete specifications align with DEL-05.02 (Technical Specification) (**TBD** until developed).
- Verify dimensions, loads, and design parameters match design basis documents.
- Verify containment details support OBJ-7 Environmental Protection intent.
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; Procedure.md: Verification; Guidance.md: Principles.)

**Interface Verification:**
- Verify interfaces with other disciplines are identified and coordinated (IDC records).
- Verify embedded items, hold points, and interface elevations are clearly noted.
- Verify coordination notes reference correct discipline drawings.
(Source: Procedure.md: Steps; Procedure.md: Verification; Guidance.md: Considerations.)

**Requirement Coverage Verification:**
- Verify each requirement in this Specification (FR-01 through QR-03) has a corresponding drawing note/detail.
- Verify each requirement has a corresponding check/IDC step in Procedure.md.
(Source: Procedure.md: Verification; Procedure.md: Steps.)

## Documentation

**Drawing Set Deliverables:**
- Foundation plans (tank foundations, equipment pads, building foundations, thrust blocks)
- Containment wall plans (secondary containment layouts, sections, details)
- Equipment pad details (anchor bolt layouts, grout pockets, mounting details)
- Reinforcement drawings (plans, sections, schedules, bar bending details)
- Typical details (joints, embedments, standard reinforcement)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; Datasheet.md: Construction.)

**Supporting Documentation:**
- Drawing list / sheet index
- General notes and legend
- Typical details index (**TBD** pending project drafting standards)
(Source: Specification.md previous version; **ASSUMPTION**: standard structural drawing set practice.)

**QA/QC Records:**
- Originator check records
- Independent/peer check records
- Interdisciplinary check (IDC) records
- Review comment/response tracking
- Issue evidence per project QA/QC and document control process (**TBD**)
(Source: Procedure.md: Records; test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD.)

## Cross-Document Notes

- **Datasheet:** Holds the metadata expectations for the drawing set (document number/revision/status/classification). Specification requirements must align with Datasheet attributes and construction details. (Source: Datasheet.md: Attributes; Datasheet.md: Construction.)
- **Guidance:** Captures the intent and priorities (containment/environmental focus OBJ-7, interfaces, constructability) that should be reflected in drawing details and annotations. Specification requirements must reflect Guidance principles. (Source: Guidance.md: Principles; Guidance.md: Considerations.)
- **Procedure:** Defines the production workflow (Steps 1-7) and verifications that demonstrate compliance with this Specification. Each Specification requirement should have a corresponding Procedure step and verification check. (Source: Procedure.md: Steps; Procedure.md: Verification.)
- **Related Deliverables:** DEL-05.02 (Technical Specification) and DEL-05.03 (Design Calculations) provide design basis and material requirements that must be reflected in drawings. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234.)
