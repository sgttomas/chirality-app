# Specification: DEL-04.01 Pavement Design Drawing Set

## Scope

### Included
This specification defines the deliverable controls, content requirements, review gates, and verification criteria that ensure the Pavement Design Drawing Set (DEL-04.01) satisfies the PKG-04 scope, complies with Employer's Requirements, and supports OBJ-8 Future Expandability requirements.

The drawing set shall document:
- Horizontal and vertical geometry for all pavement zones
- Pavement section details (layer thicknesses, materials, construction sequences)
- Interface conditions with adjacent packages (PKG-03, PKG-05, PKG-07, PKG-08)
- Line marking and traffic control features
- Future Phase 2 expansion provisions per OBJ-8

### Excluded
- Detailed pavement structural calculations (covered by DEL-04.03)
- Material specifications and workmanship requirements (covered by DEL-04.02)
- Field testing and inspection records (covered by DEL-04.04)
- Off-site roadway improvements or public right-of-way works (Owner responsibility per **ASSUMPTION** – to be confirmed from ER Scope Focus/Decisions Captured)

## Requirements

### R1: Drawing Content Requirements

#### R1.1: Plan Sheets
**Requirement**: Plan sheets shall show:
- Asphalt paving extents with area calculations
- Concrete surfacing zones with boundary delineation
- Curbs, gutters, and sidewalk locations with horizontal alignment
- Parking area layout with stall dimensions and circulation patterns
- Line marking with legend and material callout references to DEL-04.02
- Future Phase 2 expansion corridors and tie-in points (per OBJ-8)
- Coordinate grid and benchmark references
- Interface tie-in points to PKG-03 (drainage), PKG-05 (structures), PKG-07 (rail), PKG-08 (marine)

**Source**: Decomposition Section PKG-04, DEL-04.01 description; Datasheet Attributes section
**Verification**: Guidance checklist item "Plan completeness" (see DEL-04.01 Guidance); Procedure traceability matrix

#### R1.2: Section & Detail Sheets
**Requirement**: Section and detail sheets shall show:
- Typical pavement sections for each pavement type (asphalt, concrete, transition zones)
- Layer thicknesses for wearing course, binder course, base, subbase (validated by DEL-04.03)
- Material call-outs referencing DEL-04.02 specification clauses
- Subgrade preparation requirements (compaction, proof rolling, moisture conditioning)
- Joint details (construction joints, expansion joints, control joints, isolation joints)
- Drainage features (cross-slopes, longitudinal slopes, interface with PKG-03 catch basins)
- Reinforcement details (if applicable to concrete pavement zones)
- Tolerances for thickness, grade, and smoothness (consistent with DEL-04.02 acceptance criteria)

**Source**: Decomposition anticipated artifacts; Datasheet Construction section
**Verification**: Cross-document consistency check (Specification R1.2 ↔ Datasheet Construction ↔ DEL-04.03 calculation outputs); Procedure Step 2 traceability

#### R1.3: Line Marking Plans
**Requirement**: Line marking plans shall include:
- Traffic control striping (centerlines, edge lines, lane delineation)
- Parking stall striping with dimensions
- Safety markings (pedestrian crossings, restricted zones, directional arrows)
- Material specifications (paint vs. thermoplastic) referencing DEL-04.02
- Color and reflectivity requirements per DEL-04.02
- Application method and environmental constraints (temperature, humidity) per DEL-04.02

**Source**: Datasheet Attributes "Line marking"; DEL-04.02 material requirements (**cross-reference required**)
**Verification**: Guidance checklist item "Line marking & notes"; cross-check legend against DEL-04.02 materials

#### R1.4: Interface & Future-Expansion Annotations
**Requirement**: Drawings shall annotate:
- Interface elevations and horizontal tie-in points to adjacent packages (PKG-03, PKG-05, PKG-07, PKG-08)
- Assumptions regarding adjacent structure elevations or rail edge tolerances (labeled as **ASSUMPTION** in drawing notes)
- Reserved corridors for Phase 2 expansion per OBJ-8 (with dimensional envelopes and assumed grades)
- Callouts flagging **TBD** items (e.g., final Phase 2 tie-in elevations, pending geotechnical data)

**Source**: Datasheet "Interface Constraints" and "Phase 2 expansion"; OBJ-8 mapping (Decomposition Section 6)
**Verification**: Guidance checklist item "Interface & OBJ-8 callouts"; Procedure Step 3 assumption tracking log

#### R1.5: Document Control Requirements
**Requirement**: Each drawing sheet shall include:
- Title block with project name, deliverable ID (DEL-04.01), sheet number, revision number, date
- Drawing list/index sheet with all sheet titles and current revision status
- Revision history table showing revision number, date, description of changes, approval signatures
- Reference table listing applicable specifications (DEL-04.02), calculations (DEL-04.03), and Employer's Requirements sections
- Legend and general notes sheet(s) with material symbols, abbreviations, and standard details

**Source**: Datasheet "Drawing Set Composition"; Employer's Requirements Volume 2 Part 1 drawing standards (**location TBD**)
**Verification**: Procedure Step 5 QA approval checklist; Guidance "Document control review"

### R2: Traceability Requirements

#### R2.1: Specification Cross-References
**Requirement**: Every material, tolerance, and construction requirement shown on drawings shall reference the corresponding clause in DEL-04.02 Pavement Technical Specification.

**Source**: Cross-document coordination principle (Datasheet "Cross-document Coordination" section)
**Verification**: Procedure traceability matrix (Step 2); Guidance coordination guidance item

#### R2.2: Calculation Cross-References
**Requirement**: Pavement layer thicknesses and design parameters shown on section drawings shall reference the corresponding calculation sheet in DEL-04.03.

**Source**: Datasheet linkages to DEL-04.03
**Verification**: Procedure Step 4 coordination with DEL-04.03; cross-document consistency check during Guidance review

#### R2.3: Test Record References
**Requirement**: Drawing notes shall identify which elements require field verification per DEL-04.04 (e.g., "Compaction testing per DEL-04.04", "Thickness verification per DEL-04.04").

**Source**: Datasheet linkages to DEL-04.04
**Verification**: Guidance checklist confirms test record callouts are present; Procedure Step 5 handoff to DEL-04.04

### R3: Review & Approval Requirements

#### R3.1: Internal Review Gates
**Requirement**: Drawings shall undergo:
- Discipline check (Civil lead engineer review for technical accuracy)
- Cross-discipline coordination review (PKG-03, PKG-05, PKG-07, PKG-08 interface confirmation)
- QA review per Procedure (checking for completeness, traceability, assumption logging)

**Source**: Procedure "Workflow Steps" and "Controls"; Guidance "Review Checklist"
**Verification**: Procedure Step 3 reviewer comment log; Guidance coordination guidance

#### R3.2: Assumption & TBD Tracking
**Requirement**: All **ASSUMPTION** and **TBD** items noted on drawings shall be logged in the Procedure assumption tracking log with:
- Assumption/TBD ID
- Description and location (sheet number, detail reference)
- Impacted deliverables (DEL-04.02, DEL-04.03, DEL-04.04, adjacent packages)
- Resolution path (who resolves, by when)
- Status (open, resolved)

**Source**: Datasheet "Assumptions & TBDs"; Procedure "Controls" tracking requirements
**Verification**: Procedure Step 3 log maintenance; Guidance Step 4 assumption validation

#### R3.3: Revision Control
**Requirement**: Each drawing revision shall:
- Update revision number per project numbering system (**TBD** – confirm from drawing management plan)
- Record revision description in drawing title block and revision history table
- Trigger re-check per Guidance checklist to confirm cross-document consistency is maintained
- Update Procedure traceability matrix to reflect new calculation or specification references (if revised)

**Source**: Specification R1.5 document control requirements; Procedure Step 3 revision management
**Verification**: Procedure "After each revision" control; Guidance Step 5 document control review

## Standards

### Drawing Standards (**ASSUMPTION** – pending ER confirmation)
- **Employer's Requirements Volume 2 Part 1**: General drawing requirements, title block format, sheet numbering (**location TBD** – requires ER detailed review)
- **CAD Standards**: Line weights, layer naming, symbol library (**TBD** – confirm project CAD manual or ER appendix)
- **BC provincial standards**: MMCD (Master Municipal Construction Documents) or equivalent for civil drawing conventions (**ASSUMPTION**)

### Technical Standards (Referenced from DEL-04.03 and DEL-04.02)
- **TAC Pavement Design Manual**: Design methodology reference (if used by DEL-04.03)
- **OPSS or MMCD**: Material and construction specifications (if referenced by DEL-04.02)
- **CSA A23.1/A23.2**: Concrete materials and testing (if concrete pavement zones present)

## Verification

### Verification Methods

| Requirement | Verification Method | Responsible Party | Timing |
|-------------|-------------------|-------------------|--------|
| R1.1: Plan content | Guidance checklist (plan completeness) | Civil lead + QA reviewer | Pre-approval review |
| R1.2: Section details | Cross-check against DEL-04.03 outputs + DEL-04.02 materials | Civil lead + DEL-04.03 author | After calculation completion |
| R1.3: Line marking | Cross-check legend vs. DEL-04.02 specification | Civil lead + DEL-04.02 author | Coordination review |
| R1.4: Interface annotations | Coordination meeting with PKG-03/05/07/08 leads | Civil lead + Package leads | Cross-discipline review |
| R1.5: Document control | Procedure QA checklist (Step 5) | QA reviewer | Final approval gate |
| R2.1: Specification refs | Procedure traceability matrix audit | QA reviewer | Pre-issuance |
| R2.2: Calculation refs | Procedure traceability matrix audit | QA reviewer | After DEL-04.03 issued |
| R2.3: Test record refs | Handoff meeting with DEL-04.04 team | Civil lead + QA/QC lead | Pre-construction |
| R3.1: Review gates | Procedure Step 3 reviewer sign-off | Discipline/QA reviewers | Per review schedule |
| R3.2: Assumption tracking | Procedure assumption log audit | QA reviewer | Each review cycle |
| R3.3: Revision control | Procedure revision checklist | Civil lead + QA reviewer | Each revision issuance |

### Acceptance Criteria
- All plan sheets show complete coverage per R1.1 with no unlabeled zones
- All section drawings reference DEL-04.03 calculation sheets per R2.2
- All material call-outs reference DEL-04.02 specification clauses per R2.1
- All **ASSUMPTION** and **TBD** items are logged per R3.2 with resolution paths identified
- All interface tie-in points are coordinated with adjacent package leads per R1.4
- All OBJ-8 future expansion provisions are clearly annotated per R1.4
- Document control elements (title block, revision history, reference table) are complete per R1.5
- QA reviewer sign-off confirms Guidance checklist is satisfied

## Documentation

### Required Documentation Outputs
1. **Drawing Set (DEL-04.01)**: Complete set of plan, section, detail, and line marking drawings per R1.1–R1.5
2. **Procedure Traceability Matrix**: Linking each drawing sheet to specification clauses and calculation references (maintained per Procedure Step 2)
3. **Procedure Assumption Log**: Tracking **ASSUMPTION** and **TBD** items per R3.2 (maintained per Procedure Step 3)
4. **Guidance Review Checklist (completed)**: Documenting review findings and resolutions (per Guidance section)
5. **Revision History Record**: Capturing revision changes and approval signatures per R3.3

### Document Handoff Requirements
- **To DEL-04.03**: Share layout assumptions and loading scenarios for calculation validation (Procedure Step 4 coordination)
- **To DEL-04.04**: Provide final issued drawing set (with revision number) as basis for field testing and as-built verification (Procedure Step 5)
- **To adjacent packages**: Share interface drawings (plan sheets showing tie-in points) with PKG-03, PKG-05, PKG-07, PKG-08 leads for coordination (Guidance coordination guidance)

## References

### Source Documents
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-04, DEL-04.01, OBJ-8 mapping
- **Datasheet (DEL-04.01)**: Attributes, Conditions, Construction, Assumptions & TBDs, Cross-document Coordination sections
- **Guidance (DEL-04.01)**: Review Checklist, Coordination Guidance
- **Procedure (DEL-04.01)**: Workflow Steps, Controls, traceability matrix and assumption log
- **Employer's Requirements Volume 2 Part 1**: General requirements, drawing standards (**location TBD**)
- **Employer's Requirements Volume 2 Part 2**: Civil & Process Mechanical Works, pavement requirements (**location TBD**)

### Related Deliverables
- **DEL-04.02**: Pavement Technical Specification (material and workmanship requirements referenced in drawing annotations)
- **DEL-04.03**: Pavement Design Calculations (analytical basis for section thicknesses and design parameters)
- **DEL-04.04**: Pavement Installation & Test Records (field verification basis)
- **PKG-03 deliverables**: Underground Utilities (drainage interface elevations)
- **PKG-05 deliverables**: Concrete Structures (structure-to-pavement interfaces)
- **PKG-07 deliverables**: Rail Works (track elevations, rail crossing details)
- **PKG-08 deliverables**: Marine Structures (pavement termination boundaries)
