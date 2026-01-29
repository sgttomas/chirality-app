# Procedure: DEL-22.01 Building MEP Design Drawing Set

## Purpose

This procedure defines the process for producing and managing **Building MEP Design Drawing Set** within **PKG-22 Building Interior & MEP**.

**Deliverable Purpose:** Defines the design arrangement and details for building MEP per Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.01 entry; _CONTEXT.md

### Scope of This Procedure

This procedure covers:
- **Production workflow**: Steps to produce MEP design drawings from concept through issued-for-construction
- **Quality control**: Checking and review processes
- **Coordination**: Interdisciplinary coordination requirements
- **Documentation**: Records and deliverable management

**Deliverable Classification:**
- **Type:** Drawing
- **Responsible Party:** D&B Contractor

**Source:** _CONTEXT.md; standard drawing production workflow

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`)

**Source:** _DEPENDENCIES.md

**Upstream Inputs Required** (ASSUMPTION: typical MEP design inputs; to be confirmed):

1. **Building Architecture and Structure** (PKG-21):
   - Architectural floor plans and elevations
   - Structural framing plans and details
   - Building envelope details
   - Room layouts and occupancy types

2. **Electrical Power Distribution** (PKG-17):
   - Main power distribution scheme
   - Panel locations and sizes
   - Voltage and fault current levels

3. **Control Systems** (PKG-19):
   - BAS architecture and interfaces
   - Control system requirements for HVAC
   - Communication protocols

4. **Site Services** (PKG-03):
   - Fire water supply availability (pressure, flow)
   - Domestic water service connection
   - Sanitary sewer connection

5. **Design Basis**:
   - Employer's Requirements — **TBD** (location TBD)
   - Design basis memorandum or criteria document — **TBD** (location TBD)
   - Load calculations and equipment sizing — documented in DEL-22.03

**Installation Sequencing Note (DEC-06)**: "MCC building equipment installed on-site after building erection" — Building structure must be substantially complete before MEP installation can begin. This affects construction sequencing shown on drawings but does not block design.

**Source:** Package interface descriptions; Decomposition DEC-06; ASSUMPTION: standard design input requirements

### Reference Materials

**Required References**:
- See `_REFERENCES.md` for applicable reference documents
- See `execution/PKG-22_Building_Interior_and_MEP/0_References/` for reference materials

**Key Reference Documents** (to be confirmed):
- Employer's Requirements Volume 2 — **TBD** (location TBD)
- NBC 2020 (National Building Code of Canada)
- ASHRAE 90.1, ASHRAE 62.1
- NFPA 13 (sprinkler system design)
- CEC (Canadian Electrical Code)
- CSA B64 series (plumbing)
- Project CAD Manual — **TBD** (location TBD)
- Project Quality Management Plan — **TBD** (location TBD)

**Source:** Specification.md Standards section; _REFERENCES.md

### Personnel Requirements

**Minimum Qualifications** (ASSUMPTION: to be confirmed per project Quality Plan):

| Role | Qualification |
|------|--------------|
| Lead MEP Designer | Professional Engineer (P.Eng.) registered in British Columbia; minimum 5 years MEP design experience |
| HVAC Designer | Engineering degree or technologist with HVAC design experience |
| Plumbing Designer | Engineering degree or technologist with plumbing design experience |
| Electrical (Building Services) Designer | Engineering degree or technologist with building electrical experience |
| Fire Protection Designer | NICET Level III or P.Eng. with fire protection experience (for NFPA 13 compliance) |
| CAD Technician | Proficiency in project CAD software (AutoCAD or similar) |
| Checker | Independent qualified engineer, not involved in original design |

**Professional Seal Requirement**: Drawings must be sealed by Professional Engineer registered in BC per NBC 2020.

**Source:** NBC 2020 professional requirements; ASSUMPTION: standard EPC personnel qualifications

### Tools and Software

**Required Software** (ASSUMPTION: to be confirmed):
- CAD software per project standards (e.g., AutoCAD, Revit, or similar)
- HVAC load calculation software (e.g., Carrier HAP, Trane TRACE, or similar)
- Hydraulic calculation software for fire protection (e.g., HydraCAD, AutoSPRINK, or similar)
- Lighting design software if required (e.g., AGi32, DIALux)

**Source:** ASSUMPTION: standard MEP design software suite

## Steps

### Step 1: Design Basis and Criteria Development

**Objective**: Establish design parameters and criteria before detailed design begins.

**Requirements Addressed**: This step supports all requirements in Specification.md by establishing the design basis. Specifically addresses PR-01 (design life), PR-02 (seismic), PR-03 (energy efficiency), PR-04 (lifecycle cost), and establishes basis for all functional requirements (FR-HVAC-01/02/03, FR-PLUMB-01/02/03, FR-ELEC-01/02/03, FR-FIRE-01/02/03).

**Activities**:

1.1. **Review Employer's Requirements** — Extract MEP-specific requirements, constraints, and performance criteria. **TBD** — ER location and review findings (location TBD)

1.2. **Confirm Building Parameters**:
   - Building occupancy classification (NBC 2020 Part 3) — **TBD**
   - Design temperatures (indoor/outdoor) for Surrey, BC — **TBD**
   - Space heating/cooling loads (coordinate with DEL-22.03 calculations)
   - Occupancy for ventilation requirements (ASHRAE 62.1) — **TBD**

1.3. **Establish Design Criteria Document**:
   - Document design temperatures, load criteria, code compliance approach
   - Document equipment selection criteria and standards
   - Document coordination requirements with other disciplines
   - **TBD** — Design criteria document location and format (location TBD)

1.4. **Coordination Meeting**: Hold kickoff coordination meeting with architectural (PKG-21), structural (PKG-21), electrical (PKG-17), and controls (PKG-19) disciplines to establish interfaces and coordination protocols.

**Verification**: Design criteria approved by discipline lead and project management.

**Source:** ASSUMPTION: standard design basis development process; specific requirements TBD

### Step 2: Preliminary Design (Concept/30% Stage)

**Objective**: Develop preliminary MEP system concepts and layouts for review.

**Requirements Addressed**: Develops preliminary design to address all functional requirements (FR-HVAC-01/02/03, FR-PLUMB-01/02/03, FR-ELEC-01/02/03, FR-FIRE-01/02/03) and interface requirements (IF-01 through IF-05) from Specification.md.

**Activities**:

2.1. **HVAC Preliminary Design**:
   - Determine HVAC system type (e.g., rooftop units, split systems, VAV, etc.) — **TBD**
   - Establish preliminary equipment locations
   - Size equipment based on preliminary load calculations (DEL-22.03)
   - Develop preliminary ductwork routing
   - Identify control zones and BAS interfaces (coordinate PKG-19)

2.2. **Plumbing Preliminary Design**:
   - Establish fixture locations (coordinate with architectural layout)
   - Size domestic water service (coordinate with PKG-03)
   - Develop preliminary piping routing
   - Establish sanitary drainage routing to site connection (PKG-03)

2.3. **Electrical (Building Services) Preliminary Design**:
   - Develop preliminary lighting layout with fixture types
   - Establish panel locations and preliminary load distribution
   - Identify receptacle locations
   - Coordinate with main power distribution (PKG-17)

2.4. **Fire Protection Preliminary Design**:
   - Establish sprinkler system type (wet pipe, dry pipe, etc.) based on building type — **TBD**
   - Develop preliminary sprinkler head layout
   - Size fire water service connection (coordinate with PKG-03)
   - Identify fire pump requirements if needed — **TBD**

2.5. **Coordination**:
   - Overlay MEP preliminary layouts on architectural/structural base drawings
   - Identify conflicts and resolve
   - Conduct preliminary IDC (Interdisciplinary Check)

2.6. **30% Design Review**: Present preliminary design to project team and Employer for review and approval.

**Verification**: 30% design review completed and comments incorporated.

**Source:** ASSUMPTION: standard EPC design stage process

### Step 3: Detailed Design (60% Stage)

**Objective**: Develop detailed design with all major equipment selected and systems fully coordinated.

**Requirements Addressed**: Finalizes all functional requirements (FR-HVAC-01/02/03, FR-PLUMB-01/02/03, FR-ELEC-01/02/03, FR-FIRE-01/02/03), performance requirements (PR-01 through PR-07), and quality requirements (QR-01 through QR-07) from Specification.md. Produces detailed design supporting data for Datasheet.md attributes.

**Activities**:

3.1. **HVAC Detailed Design**:
   - Finalize equipment selection with manufacturer data (document in DEL-22.04)
   - Complete ductwork sizing and layout
   - Develop control sequences and BAS integration details (coordinate PKG-19)
   - Prepare equipment schedules
   - Complete load calculations and sizing calculations (DEL-22.03)

3.2. **Plumbing Detailed Design**:
   - Finalize piping sizes and routing
   - Complete equipment selection (water heaters, pumps, etc.) — document in DEL-22.04
   - Prepare fixture and equipment schedules
   - Complete hydraulic calculations if required

3.3. **Electrical (Building Services) Detailed Design**:
   - Finalize lighting fixture selection and layout
   - Complete circuit design and panel schedules
   - Finalize receptacle and equipment power distribution
   - Complete load calculations (DEL-22.03)

3.4. **Fire Protection Detailed Design**:
   - Finalize sprinkler head layout and spacing (NFPA 13)
   - Complete hydraulic calculations (document separately or reference in DEL-22.03)
   - Finalize piping sizing and routing
   - Prepare equipment schedules

3.5. **Coordination**:
   - Complete full IDC with all disciplines
   - Resolve all conflicts and interferences
   - Update drawings to reflect coordination changes

3.6. **60% Design Review**: Present detailed design for review and approval.

**Verification**: 60% design review completed and all comments resolved.

**Source:** ASSUMPTION: standard EPC design stage process

### Step 4: Final Design (90% / IFC Stage)

**Objective**: Complete all design details and prepare for issue for construction.

**Requirements Addressed**: Completes all requirements from Specification.md and ensures all quality requirements (QR-01 through QR-07) are met, including independent check (QR-03, QR-04) and professional seal (QR-05). Finalizes all Datasheet.md attributes and anticipated artifacts.

**Activities**:

4.1. **Complete All Details**:
   - Add all connection details, sections, and enlarged plans
   - Complete all schedules and legends
   - Add all notes and specifications references
   - Finalize equipment tags and coordinate with DEL-22.04 data sheets

4.2. **Independent Check**:
   - Submit drawings to independent checker (not involved in original design)
   - Checker reviews for:
     - Design adequacy and code compliance
     - Calculation support (DEL-22.03)
     - Coordination with other disciplines
     - Drawing completeness and clarity
     - CAD standards compliance

4.3. **Incorporate Check Comments**:
   - Review checker comments with design team
   - Incorporate required changes
   - Obtain checker sign-off

4.4. **Final IDC**:
   - Conduct final interdisciplinary coordination check
   - Ensure all disciplines are aligned
   - Resolve any remaining minor coordination items

4.5. **90% / IFC Review**: Present for final review before issue for construction.

**Verification**: All checks completed, all review comments resolved, ready for professional seal and issue.

**Source:** ASSUMPTION: standard EPC design finalization process

### Step 5: Issue for Construction (IFC)

**Objective**: Issue drawings for construction use.

**Activities**:

5.1. **Final Quality Check**:
   - Verify all title block information is complete and correct
   - Verify drawing numbers and revision status
   - Verify all cross-references are correct
   - Verify all consultant and contractor information is included

5.2. **Professional Seal**:
   - Submit drawings to Professional Engineer (P.Eng. BC) for review and seal
   - Engineer reviews for compliance with NBC 2020 and professional practice
   - Engineer applies seal and signature

5.3. **Issue Process**:
   - Export drawings to PDF format per project standards
   - Apply IFC revision mark and date
   - Submit to project document control for distribution
   - File native CAD files and issued PDFs per document control procedure

5.4. **Record Issued Version**:
   - Copy issued package to `3_Issued/` folder
   - Update `_STATUS.md` to ISSUED with date and revision information
   - Retain working files in `1_Working/` for future revisions

**Verification**: Drawings issued with professional seal, distributed to construction team.

**Source:** ASSUMPTION: standard IFC issue process; professional seal per NBC 2020

### Step 6: Construction Support and As-Built Updates

**Objective**: Support construction and maintain drawings current with field changes.

**Activities**:

6.1. **RFI Response**:
   - Respond to Requests for Information (RFIs) from construction contractor
   - Issue clarification sketches or revised details as needed
   - Maintain revision control per project procedures

6.2. **Field Change Management**:
   - Review and approve field changes proposed by contractor
   - Issue revised drawings for significant changes
   - Document changes for as-built record

6.3. **As-Built Updates**:
   - Incorporate contractor redlines and field changes into drawing set
   - Issue final as-built drawings for owner operations and maintenance use
   - Archive as-built drawings per project closeout procedures

**Verification**: As-built drawings issued and accepted by owner.

**Source:** ASSUMPTION: standard construction support and closeout process

## Verification

### Quality Control Checkpoints

**Self-Check (Originator)**:
- [ ] Design meets all requirements in Specification.md
- [ ] All calculations documented and support design (DEL-22.03)
- [ ] All equipment selections documented (DEL-22.04)
- [ ] Drawing complies with CAD standards
- [ ] All cross-references and tags are correct

**Independent Check (Checker)**:
- [ ] Design is adequate for intended purpose
- [ ] Design complies with all applicable codes and standards
- [ ] Design is coordinated with other disciplines
- [ ] Calculations are correct and support design
- [ ] Drawing is complete, clear, and constructible
- [ ] CAD standards and project procedures followed

**Interdisciplinary Check (IDC Coordinator)**:
- [ ] No conflicts with architectural layout
- [ ] No conflicts with structural framing
- [ ] Interfaces with electrical power distribution (PKG-17) defined
- [ ] Interfaces with control systems (PKG-19) defined
- [ ] Interfaces with site services (PKG-03) defined

**Design Review (Design Manager / Employer)**:
- [ ] Design meets Employer's Requirements
- [ ] Design is constructible within project schedule
- [ ] Design is within project budget
- [ ] Design optimizes lifecycle cost per OBJ-9

**Professional Engineer Review (P.Eng.)**:
- [ ] Design complies with NBC 2020 and applicable codes
- [ ] Design meets professional standard of care
- [ ] All engineering assumptions are reasonable and documented
- [ ] Ready for professional seal

**Source:** Specification.md Verification section; ASSUMPTION: standard EPC quality control checkpoints

### Sign-Off Requirements

**ASSUMPTION: Standard sign-off protocol to be confirmed per project Quality Management Plan**

| Milestone | Required Sign-Offs |
|-----------|-------------------|
| 30% Design Review | Discipline Lead, Project Manager |
| 60% Design Review | Discipline Lead, Project Manager, Employer (optional) |
| Independent Check Complete | Checker (P.Eng. or qualified engineer) |
| Final IDC Complete | IDC Coordinator, all affected discipline leads |
| 90% / IFC Review | Discipline Lead, Project Manager, Employer |
| Issue for Construction | Professional Engineer Seal (P.Eng. BC), Document Control Manager |

**Source:** ASSUMPTION: standard EPC sign-off requirements

## Records

### Documentation Outputs

**Primary Deliverable** (per Decomposition DEL-22.01):
- **HVAC layout drawings**
- **Plumbing layout drawings**
- **Interior electrical layout drawings**
- **Fire suppression layout drawings**

**Source:** Decomposition REVISED_v2.md, DEL-22.01 anticipated artifacts

**Supporting Documentation**:
- Design calculations: DEL-22.03 Building MEP Design Calculations
- Equipment data sheets: DEL-22.04 Building MEP Data Sheet Package
- Technical specifications: DEL-22.02 Building MEP Technical Specification
- Installation and test records: DEL-22.05 (produced during construction)
- Shop drawings: DEL-22.06 (produced by suppliers/contractors)

**Source:** Decomposition REVISED_v2.md, PKG-22 deliverable list

### Record Management

**File Storage Locations**:

| Stage | Location | Contents |
|-------|----------|----------|
| Working | `1_Working/` | Active design files, native CAD, work-in-progress |
| Checking | `2_Checking/To/` | Copies submitted for review (with DEL-ID + date + rev) |
| Issued | `3_Issued/` | Issued-for-construction and as-built drawings (PDF + native CAD) |

**Source:** README.md Section 6 (review and issue conventions)

**File Naming Convention** (ASSUMPTION: to be confirmed):
- Native CAD: `[Drawing Number]_[Rev].dwg`
- Issued PDF: `DEL-22.01_[Drawing Number]_[Rev]_[Date].pdf`
- Review package: `DEL-22.01_[Stage]_[Date].zip`

**Version Control**:
- All revisions tracked in drawing title block
- Revision clouds and triangles per CAD standards
- Revision history maintained in project document management system

**Retention Requirements**:
- Working files: Retain through project closeout, archive per project procedures
- Issued drawings: Retain in project archives per company and regulatory requirements — **TBD** (retention period per project records management plan)
- As-built drawings: Deliver to owner, retain copy in project archives

**Source:** ASSUMPTION: standard document control and records management; specific project procedures TBD

### Audit Trail

**Design Development Records to Maintain**:
- Design basis and criteria documents
- Coordination meeting minutes
- Design review meeting minutes and comment/response logs
- Checker comments and resolution records
- RFI log and responses
- Change order log for field changes

**Purpose**: Demonstrate due diligence, support professional liability, enable future modifications.

**Source:** ASSUMPTION: standard engineering records management practice
