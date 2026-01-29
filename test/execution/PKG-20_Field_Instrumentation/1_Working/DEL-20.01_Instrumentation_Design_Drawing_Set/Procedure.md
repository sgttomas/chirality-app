# Procedure: DEL-20.01 Instrumentation Design Drawing Set

## Purpose

This procedure defines the process for **producing** the Instrumentation Design Drawing Set within **PKG-20 Field Instrumentation** for the Canola Oil Transload Facility Phase 1 project.

**Deliverable Scope:**

Defines the design arrangement and details for instrumentation per ER requirements.

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, DEL-20.01 (line 496)

**Deliverable Classification:**

| Field | Value | Datasheet § | Specification § |
|-------|-------|-------------|-----------------|
| Type | Drawing | Identification | Scope |
| Discipline | I&C | Identification | Scope |
| Responsible Party | D&B Contractor | Identification | Scope |

**Source:** `_CONTEXT.md`

**Procedure Application:**

This procedure addresses the **production workflow** for creating the drawing set, from initial design through to final issuance for construction. It covers:

| Activity | Specification § | Guidance § |
|----------|-----------------|------------|
| Design development steps | FR-1 to FR-6, PR-1 to PR-4 | Principles, Considerations |
| Interdisciplinary coordination | INT-1, INT-2 | Coordination Considerations |
| Review and verification activities | QR-1 to QR-4, Verification | Quality Considerations |
| Drawing issuance and revision control | Documentation | — |

**Note:** For **operational use** of the drawings (i.e., how construction personnel use these drawings for field installation), refer to construction work packages and installation procedures developed by the construction team.

## Prerequisites

### Dependencies

**Dependency Coordination:**

See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies are coordinated externally by humans per project coordination plan (`execution/_Coordination/_COORDINATION.md`).

**Source:** `_DEPENDENCIES.md` file content

**Typical Upstream Inputs Required (Coordination):**

The following inputs are typically required before instrumentation design drawings can be developed:

| Input Category | Inputs Required | Specification § | Guidance § |
|----------------|-----------------|-----------------|------------|
| Process Engineering | P&IDs with instrument tag list; PFDs and heat & material balances; Instrument index and control philosophy | FR-5, INT-2 | Upstream Dependencies |
| Layout and Equipment | Plot plan and equipment layouts; Piping arrangements and isometrics; Structural platform and access arrangements | FR-5, INT-2 | Upstream Dependencies |
| Electrical and Control | Hazardous area classification drawings; Control system architecture and I/O allocation; Cable tray and duct bank routing plans | FR-3, FR-4, INT-1, INT-2 | Upstream Dependencies |
| Specification and Data | DEL-20.02, DEL-20.03, DEL-20.04 deliverables | INT-2 | Technical Considerations |
| Project Basis | Employer's Requirements; Project design basis and standards; Project CAD standards; Project quality procedures | Standards, QR-1 to QR-4 | Standards Context |

**TBD**: Specific deliverable references and sequencing to be confirmed per project execution plan

**Source:** **ASSUMPTION** based on typical EPC workflow dependencies for instrumentation drawing development; cross-references to other packages per decomposition structure

### Reference Materials

**Required References:**

| Reference | Location | Status | Specification § | Guidance § |
|-----------|----------|--------|-----------------|------------|
| Decomposition document | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | Available | Scope | Purpose |
| `_REFERENCES.md` | Deliverable folder | **Currently empty**: References to be populated | — | — |
| Package `0_References/` | PKG-20 folder | **TBD**: Reference materials to be provided | — | — |
| Employer's Requirements Vol 2 Parts 1-3 | **TBD** | **TBD**: Access to be provided | Standards | Standards Context |

**Source:** `_REFERENCES.md` content; Decomposition Section 3 (lines 75-79)

**Applicable Standards and Codes:**

| Standard | Description | Specification § | Guidance § |
|----------|-------------|-----------------|------------|
| ISA 5.1 | Instrumentation Symbols and Identification | PR-2, Standards | ISA 5.1 Context |
| ISA 84 / IEC 61511 | Functional Safety — if applicable | Standards | ISA 84 Context |
| CSA C22.1 | Canadian Electrical Code | Standards | CSA C22.1 Context |
| API 554 | Process Instrumentation and Control | Standards | API 554 Context |

**TBD**: Additional standards per project specification

**Source:** Datasheet.md References section; **ASSUMPTION** based on I&C discipline typical applicable standards

**Manufacturer Documentation:**

| Documentation | Purpose | Specification § | Guidance § |
|---------------|---------|-----------------|------------|
| Instrument manufacturer installation manuals | Mounting and connection details | FR-3 | Technical Considerations |
| Mounting hardware and accessories data | Support and bracket details | FR-3 | Technical Considerations |
| Cable and termination specifications | Cable schedule development | FR-4 | Technical Considerations |

**Source:** **ASSUMPTION** based on typical instrumentation drawing detail requirements; coordinate with DEL-20.04 for vendor documentation

### Personnel Requirements

**Design Team Roles:**

| Role | Qualification | Responsibility | Specification § |
|------|---------------|----------------|-----------------|
| I&C Lead Engineer | P.Eng. (Electrical/Control Systems) | Overall deliverable responsibility, approval authority | QR-1 |
| I&C Design Engineer | Engineering degree + I&C experience | Design development, drawing production | FR-1 to FR-6 |
| CAD Technician/Designer | CAD certification + I&C drawing experience | Drafting, CAD standards compliance | PR-1, PR-2 |
| I&C Checker | P.Eng. or senior engineer (independent) | Peer review, independent verification | QR-1 |
| Interdisciplinary Coordinator | Engineering background | IDC coordination, comment resolution | INT-1, QR-1 |

**Source:** **ASSUMPTION** based on typical EPC engineering team structure and professional practice requirements (P.Eng. for BC jurisdiction)

**Competency Requirements:**

| Competency | Description | Specification § |
|------------|-------------|-----------------|
| I&C discipline knowledge | Instrumentation types, installation practices, standards | FR-1 to FR-6, Standards |
| Project CAD software proficiency | **TBD**: CAD platform (AutoCAD, MicroStation, etc.) | PR-1, PR-2 |
| Bulk liquid terminal operations | **ASSUMPTION**: Relevant to canola oil transload facility | FR-6 |
| Hazardous area classification | CSA C22.1 Section 18 | FR-3, Standards |

**Source:** **ASSUMPTION** based on deliverable technical requirements and project context

### Tools and Resources

**Software/Systems:**

| Tool | Purpose | Status |
|------|---------|--------|
| CAD software | Drawing production | **TBD**: Specific platform and version per project standards |
| Document management system | Drawing registration, revision control | **TBD**: System and access protocols |
| Instrument database | Tag management, cable schedule generation | **TBD**: If applicable |

**Physical Resources:**

| Resource | Purpose |
|----------|---------|
| Site access | Field verification (as-built conditions, constructibility review) |
| Reference standards | Library or online subscriptions |

**Source:** **ASSUMPTION** based on typical engineering work environment requirements

## Steps

### Overview: Requirements Implementation

This procedure implements the requirements defined in Specification.md and produces the deliverable artifacts documented in Datasheet.md. Guidance.md provides the engineering rationale and decision-making context for the steps below.

**Key Requirement Mappings:**

| Step | Implements Specification § | Guidance § |
|------|---------------------------|------------|
| Step 1 | Scope, FR-1, Standards | Purpose, Standards Context |
| Step 2 | FR-2, FR-5, FR-6 | Principles 1, 4, 5; Examples |
| Step 3 | FR-3, FR-4, PR-1 to PR-4 | Principles 2, 3; Technical Considerations |
| Step 4 | QR-1 to QR-3, INT-1 | Quality Considerations; IDC Process |
| Step 5 | Documentation, QR-2 | Downstream Use |
| Step 6 | QR-4 | — |

### Step 1: Design Initiation and Planning

**Objective:** Establish design basis, scope, and work plan.

**Implements:** Specification Scope section and FR-1 (Drawing Content)

**Guidance Reference:** Purpose, Standards Context, Facility Type considerations

**Activities:**

| Activity | Description | Specification § | Guidance § | Datasheet § |
|----------|-------------|-----------------|------------|-------------|
| 1.1 Review Design Basis | Review Employer's Requirements for instrumentation design criteria (**TBD**: Specific ER sections); Review P&IDs and instrument list for scope definition; Review process conditions and equipment specifications; Identify critical instrumentation (safety, custody transfer, regulatory compliance) | Scope, FR-6, Standards | Standards Context, Facility Type | Conditions |
| 1.2 Define Drawing List | Develop preliminary drawing list (by area, system, or drawing type); Assign drawing numbers per project numbering convention (**TBD**: Project drawing numbering system); Establish drawing release schedule aligned with construction needs | Documentation | Trade-off 4 | Construction |
| 1.3 Establish Design Criteria | Confirm environmental conditions (temperature, hazardous area classification, seismic); Confirm applicable standards and code requirements; Confirm CAD standards and drawing conventions; Identify any project-specific requirements or deviations | FR-6, PR-1, PR-2, Standards | Principles 2, 3; Standards Context | Conditions, Attributes |

**Deliverable:** Design initiation package (design basis summary, drawing list, schedule)

**Verification:** I&C Lead Engineer review and approval

**Source:** **ASSUMPTION** based on typical EPC design initiation process

### Step 2: Design Development (Concept Phase)

**Objective:** Develop preliminary instrument locations and routing concepts.

**Implements:** Specification FR-2 (Instrument Location Plans) and FR-5 (Coordination with Process Design)

**Guidance Reference:** Principles 1, 4, 5; Upstream Dependencies; Examples 1-3

**Activities:**

| Activity | Description | Specification § | Guidance § | Datasheet § |
|----------|-------------|-----------------|------------|-------------|
| 2.1 Develop Instrument Location Concepts | Locate instruments on equipment layout and piping arrangement drawings; Consider process requirements (measurement point locations per P&IDs); Consider installation and maintenance access requirements; Consider hazardous area boundaries and electrical protection requirements; Identify mounting requirements (pipe-mounted, vessel-mounted, structure-mounted) | FR-2, FR-5, FR-6 | Principles 1, 4, 5; Project-Specific Examples | Construction, Instrumentation Types |
| 2.2 Develop Cable Routing Concepts | Identify cable tray and duct bank routing from instrument locations to termination points; Identify junction box locations (grouping by area, minimizing cable lengths); Consider segregation requirements (IS barriers, power vs. signal); Coordinate with electrical infrastructure design (PKG-23) | FR-4, INT-1 | Cable Routing, Junction Box Locations | Installation Requirements |
| 2.3 Develop Installation Detail Concepts | Identify typical vs. specific detail requirements; Review manufacturer installation recommendations; Develop standard details for common installations (instrument supports, cable glands, etc.) | FR-3 | Trade-off 3, Example 2 | Installation Requirements |
| 2.4 30% Design Review (**ASSUMPTION**) | Issue concept drawings for internal review and interdisciplinary coordination; Resolve major conflicts and confirm design approach; Obtain approval to proceed to detailed design | QR-1, INT-1 | Design Review Stages | — |

**Deliverable:** Concept drawings (30% completeness) — **TBD**: Project-specific design review stages

**Verification:** Design review meeting, IDC coordination, I&C Lead approval

**Source:** **ASSUMPTION** based on typical EPC phased design approach (30/60/90/IFC)

### Step 3: Detailed Design Development

**Objective:** Develop detailed drawings suitable for construction and procurement.

**Implements:** Specification FR-3 (Installation Details), FR-4 (Cable Schedules), PR-1 to PR-4

**Guidance Reference:** Principles 2, 3; Technical Considerations; Examples 1-3

**Activities:**

| Activity | Description | Specification § | Guidance § | Datasheet § |
|----------|-------------|-----------------|------------|-------------|
| 3.1 Produce Detailed Instrument Location Plans | Finalize instrument locations with dimensions and elevations; Add instrument tag numbers, service descriptions, and notes; Coordinate with piping isometrics for exact connection points; Coordinate with structural drawings for platform access and support locations | FR-2, PR-1, PR-2 | Example 1 | Construction |
| 3.2 Produce Detailed Installation Details | Develop detailed mounting arrangements and connection diagrams; Reference manufacturer installation drawings where applicable; Include hazardous area sealing details per CSA C22.1; Include material specifications and bill of materials | FR-3, Standards | Principles 2, 3; Example 2 | Installation Requirements |
| 3.3 Produce Cable Schedules | Develop comprehensive cable schedule with: Cable tag numbers, From/To termination points, Cable specifications (type, size, conductor count, shielding), Cable lengths and routing references, Termination details (junction box numbers, terminal strips); Coordinate with control system I/O allocation (PKG-22); Verify cable types and routing comply with hazardous area requirements | FR-4, INT-1, Standards | Example 3, Cable Routing | Construction |
| 3.4 60% Design Review (**ASSUMPTION**) | Issue detailed drawings for formal review; Conduct interdisciplinary check (IDC) with all affected disciplines; Resolve comments and incorporate feedback | QR-1, INT-1 | Design Review Stages | — |

**Deliverable:** Detailed drawings (60% completeness) — **TBD**: Project-specific design review stages

**Verification:** IDC sign-off, design review approval, comment resolution

**Source:** **ASSUMPTION** based on typical EPC detailed design process

### Step 4: Final Design and Verification

**Objective:** Finalize drawings for construction issuance.

**Implements:** Specification QR-1 to QR-3, INT-1

**Guidance Reference:** Quality and Verification Considerations; IDC Process

**Activities:**

| Activity | Description | Specification § | Guidance § |
|----------|-------------|-----------------|------------|
| 4.1 Complete Drawing Finalization | Incorporate all review comments from 60% review; Add final details, notes, and specifications; Verify all cross-references and drawing coordination; Complete title blocks, revision blocks, and drawing stamps | PR-1, PR-2, QR-3 | — |
| 4.2 Self-Check | Design engineer performs self-check using project checklist: Completeness (all instruments from P&IDs are located and detailed), Accuracy (dimensions, elevations, tag numbers verified), Coordination (no conflicts with other disciplines), Standards compliance (CAD standards, code requirements), Clarity (drawings are clear and suitable for construction use) | QR-1, Verification | Verification Activities |
| 4.3 Independent Check | Independent checker (qualified I&C engineer, not the originator) performs peer review: Verify design compliance with Employer's Requirements and standards, Verify calculations and sizing (cross-check with DEL-20.03), Verify equipment data (cross-check with DEL-20.04), Identify errors, omissions, or improvement opportunities, Document review findings on check sheets | QR-1, INT-2, Verification | Verification Activities |
| 4.4 Interdisciplinary Check (IDC) | Issue drawings to affected disciplines for final coordination: Process/Piping: Instrument connections, line numbers, operating conditions; Structural: Mounting supports, platform access, seismic bracing; Electrical: Power supply, cable routing, hazardous area compliance; Control Systems: I/O allocation, signal types, network architecture; Resolve all IDC comments and obtain discipline sign-offs | QR-1, INT-1, Verification | IDC Process |
| 4.5 90% Design Review (**ASSUMPTION**) | Formal design review meeting with project team; Confirm readiness for IFC (Issued for Construction); Obtain approval for final issuance | QR-1 | Design Review Stages |

**Deliverable:** Final drawings (90% completeness, ready for IFC)

**Verification:** Self-check sign-off, independent check sign-off, IDC sign-offs, design review approval

**Source:** **ASSUMPTION** based on typical EPC verification process and quality assurance requirements

### Step 5: Drawing Approval and Issuance

**Objective:** Issue approved drawings for construction use.

**Implements:** Specification Documentation section, QR-2

**Guidance Reference:** Downstream Use, Downstream Impacts

**Activities:**

| Activity | Description | Specification § | Guidance § |
|----------|-------------|-----------------|------------|
| 5.1 Drawing Approval | I&C Lead Engineer reviews and approves drawings; Professional Engineer stamp and signature (per provincial requirements for BC) — **TBD**: P.Eng. seal requirements; Document Control reviews for completeness and compliance with document control procedures | QR-1, Documentation | — |
| 5.2 Issued for Construction (IFC) | Issue drawings with IFC status and revision identifier; Distribute per project distribution matrix: Construction team (for field installation), Procurement team (for equipment purchasing, if applicable), Quality assurance (for inspection planning), Commissioning team (for system checkout planning) — **TBD**: Project-specific distribution requirements | Documentation | Downstream Impacts |
| 5.3 Drawing Registration | Register drawings in project document management system; Create as-built placeholder records (to be updated during construction); Archive superseded revisions per document retention requirements | QR-2, Documentation | — |

**Deliverable:** IFC drawings, distribution records

**Verification:** Document control approval, distribution confirmation

**Source:** **ASSUMPTION** based on typical EPC drawing issuance process and document control requirements

### Step 6: Drawing Maintenance and Revision

**Objective:** Manage drawing changes and maintain as-built documentation.

**Implements:** Specification QR-4 (As-Built Documentation)

**Activities:**

| Activity | Description | Specification § | Guidance § |
|----------|-------------|-----------------|------------|
| 6.1 Change Management | Process field change requests and RFIs (Requests for Information); Evaluate impact of changes on design and downstream work; Issue revised drawings with revision identifier and revision description; Maintain revision history and change log | QR-2 | Trade-off 4 |
| 6.2 As-Built Updates | Incorporate field modifications and deviations during construction; Incorporate commissioning findings and adjustments; Coordinate as-built updates with construction site team (red-line markups); Issue final as-built drawings upon project completion | QR-4 | — |
| 6.3 Lessons Learned Capture | Document design issues, construction challenges, and improvement opportunities; Feed lessons learned into future project design standards and typical details; Contribute to continuous improvement of drawing production process | — | Lessons Learned |

**Deliverable:** Revised drawings, as-built drawings, lessons learned documentation

**Verification:** Revision approval per same process as Step 5, as-built verification by construction team

**Source:** **ASSUMPTION** based on typical EPC change management and as-built documentation process

## Verification

### Design Verification Activities

**Verification Matrix:**

| Verification Type | Method | Performer | Timing | Documentation | Specification § | Guidance § |
|-------------------|--------|-----------|--------|---------------|-----------------|------------|
| Self-check | Checklist review | Design engineer | After drawing completion | Check sheet (originator signature) | QR-1, Verification | Verification Activities |
| Independent check | Peer review | Independent I&C engineer | After self-check | Check sheet (checker signature) | QR-1, Verification | Verification Activities |
| Interdisciplinary check | Coordination review | All affected disciplines | At design milestones (30/60/90%) | IDC comments and sign-offs | QR-1, INT-1, Verification | IDC Process |
| Design review | Formal review meeting | Project team | At design milestones | Design review minutes, action log | QR-1, Verification | Design Review Stages |
| Standards compliance | Code compliance check | QA or Lead Engineer | Before IFC issuance | Compliance checklist | QR-3, Verification | Quality Considerations |
| CAD standards audit | Drawing standards check | CAD Manager or QA | Before IFC issuance | CAD standards checklist | PR-2, QR-3, Verification | — |

**Source:** **ASSUMPTION** based on typical EPC verification requirements and quality assurance practices

### Acceptance Criteria

**Drawing Acceptance Criteria:**

The drawing set is acceptable for issuance when:

| Criterion | Description | Verification Method | Specification § | Guidance § |
|-----------|-------------|---------------------|-----------------|------------|
| Completeness | All instruments from P&IDs are located and detailed; All anticipated artifacts are produced (location plans, installation details, cable schedules); All drawing sheets are complete with no TBD placeholders (or TBDs explicitly approved by Lead Engineer) | Completeness check, self-check | FR-1, FR-2, FR-3, FR-4, Verification | — |
| Accuracy | Instrument tag numbers match P&IDs and instrument index; Instrument locations are dimensioned and coordinated with piping/equipment arrangements; Installation details reflect manufacturer requirements and code compliance; Cable schedules match control system I/O allocation | Self-check, independent check | PR-3, PR-4, Verification | Technical Considerations |
| Coordination | All interdisciplinary check (IDC) comments are resolved and disciplines have signed off; No open conflicts with other discipline drawings; Hazardous area classifications are correctly reflected and compliant with CSA C22.1 | IDC sign-off | QR-1, INT-1, Verification | IDC Process |
| Standards Compliance | Drawings comply with project CAD standards (symbology, layering, title blocks, revision control); Instrumentation symbology complies with ISA 5.1; Installation details comply with applicable codes (CSA C22.1, manufacturer requirements) | Standards audit | PR-2, QR-3, Standards, Verification | Standards Context |
| Approval | Self-check and independent check are complete with sign-offs; I&C Lead Engineer has approved drawings; Professional Engineer seal applied (if required per provincial regulations); Document control has confirmed compliance with document control procedures | Sign-offs, approval | QR-1, Verification | — |

**Source:** **ASSUMPTION** based on typical EPC drawing acceptance criteria and quality gate requirements

### Hold Points and Witness Points

**Potential Hold Points (TBD):**

| Hold Point | Purpose | Specification § | Guidance § |
|------------|---------|-----------------|------------|
| 30% design review | Concept approval | QR-1 | Design Review Stages |
| 90% design review | Pre-IFC approval | QR-1 | Design Review Stages |
| IFC issuance | Employer acceptance before construction use | QR-1, Documentation | — |

**TBD** — Hold points for Employer review to be identified per project execution plan and Employer's Requirements

**Witness Points (if applicable):**

- **TBD** — Witness points for Employer or third-party verification (e.g., regulatory authority review for safety-critical instrumentation)

**Source:** **ASSUMPTION** based on typical EPC quality plan structure; specific hold/witness points to be confirmed per project quality procedures and Employer's Requirements

## Records

### Documentation Outputs

**Primary Deliverable Outputs:**

| Output | Format | Content | Specification § | Guidance § | Datasheet § |
|--------|--------|---------|-----------------|------------|-------------|
| Instrument Location Plans | CAD drawings (PDF + native DWG/DGN) — **TBD**: Project CAD platform | Spatial arrangement of instruments | FR-2, Documentation | Example 1 | Construction |
| Instrument Installation Details | CAD drawings (PDF + native DWG/DGN) | Typical and specific mounting/connection details | FR-3, Documentation | Example 2 | Construction |
| Cable Schedules | Tabular schedules (embedded in drawings or separate database export) — **TBD**: Project preference | Cable identification, routing, specifications, terminations | FR-4, Documentation | Example 3 | Construction |

**Naming convention:** **TBD** — Per project drawing numbering system
**Storage location:** Project document management system

**Source:** Decomposition DEL-20.01 Anticipated Artifacts (line 496)

### Supporting Records

**Design and Verification Records:**

| Record | Purpose | Specification § | Guidance § |
|--------|---------|-----------------|------------|
| Design calculations and analysis | Sizing and verification basis | INT-2 | Technical Considerations |
| Equipment data sheets and vendor information | Equipment data | INT-2 | Technical Considerations |
| Design review minutes and action logs | Design review documentation | QR-1, Verification | Design Review Stages |
| Self-check and independent check sheets (signed) | Verification documentation | QR-1, Verification | Verification Activities |
| Interdisciplinary check comment logs and sign-offs | IDC documentation | QR-1, INT-1, Verification | IDC Process |
| Code compliance checklists | Standards compliance verification | QR-3, Verification | Standards Context |
| CAD standards audit records | CAD standards verification | PR-2, QR-3, Verification | — |

**Source:** **ASSUMPTION** based on typical EPC quality record requirements

**Change Management Records:**

| Record | Purpose | Specification § |
|--------|---------|-----------------|
| Field change requests and RFIs | Change documentation | QR-2 |
| Revision logs and change descriptions | Revision tracking | QR-2 |
| As-built markup drawings (red-lines from construction) | Field modification documentation | QR-4 |
| Lessons learned documentation | Continuous improvement | — |

**Source:** **ASSUMPTION** based on typical EPC change control and as-built documentation process

### Record Management

**Filing and Storage:**

| Location | Content | Description |
|----------|---------|-------------|
| `1_Working/` | Working files | Stored during design development |
| `2_Checking/To/` | Checking files | Copies placed for formal review |
| `2_Checking/From/` | Review comments | Returned with comments |
| `3_Issued/` | Issued files | Final approved drawings with revision identifier and issuance date |
| Archive | Superseded revisions | Per project document retention plan |

**Source:** README.md description of lifecycle folder structure (lines 115-124)

**Retention Requirements:**

| Retention Period | Record Type | Basis |
|------------------|-------------|-------|
| Design warranty period | Design records | Contract requirements |
| Facility lifecycle (permanent) | As-built drawings | Operational requirements |
| 7 years | Quality records | Professional practice requirements |

**TBD** — Retention period per project contract requirements and regulatory obligations

**Access Control:**
- Electronic records managed per project document management system access controls
- Distribution controlled per project distribution matrix
- Confidentiality and security per project contract terms

**Source:** **ASSUMPTION** based on typical EPC document management and professional practice requirements

### Integration with Other Deliverables

**Cross-References:**

This deliverable's records integrate with:

| Deliverable | Relationship | Specification § | Datasheet § |
|-------------|--------------|-----------------|-------------|
| DEL-20.02 | Instrumentation Technical Specification — Drawings implement specification requirements | INT-2 | Related Deliverables |
| DEL-20.03 | Instrumentation Design Calculations — Drawings reflect calculation results (sizing, verification) | INT-2 | Related Deliverables |
| DEL-20.04 | Instrumentation Data Sheet Package — Drawings reference equipment data sheet information | INT-2 | Related Deliverables |
| DEL-20.05 | Instrumentation Installation & Test Records — Drawings support commissioning and testing activities | INT-2 | Related Deliverables |

**Source:** Decomposition PKG-20 deliverables (lines 496-500); deliverable cross-reference relationships

### Handover to Operations

**Facility Turnover:**

Upon project completion, the following documentation shall be provided to the facility operations team:

| Documentation | Purpose | Specification § | Guidance § |
|---------------|---------|-----------------|------------|
| Final as-built drawings (all revisions) | Facility reference | QR-4, Documentation | Downstream Use |
| Electronic files (CAD native files for future modifications) | Future modifications | Documentation | Downstream Use |
| Instrument location reference | Maintenance planning | FR-2, Documentation | Downstream Use |
| Asset management system integration | **TBD**: System and data format requirements | Documentation | — |

**Source:** **ASSUMPTION** based on typical facility turnover requirements and OBJ-9 (Lifecycle Cost Optimization) objective supporting maintainability

**Source (OBJ-9):** Decomposition Section 2 Project Objectives (line 66)

## Project Objective Alignment

This procedure supports the following project objectives:

| Objective | Description | How Supported | Specification § |
|-----------|-------------|---------------|-----------------|
| OBJ-1 | Safe & Reliable Operation | Rigorous design and verification process ensures instrumentation is properly designed and installed; Quality checks reduce errors and improve system reliability; Clear documentation supports safe construction and commissioning | FR-1 to FR-6, QR-1 to QR-4 |
| OBJ-6 | Regulatory Compliance | Procedure ensures compliance with electrical code (CSA C22.1) and professional practice requirements (P.Eng. review) | Standards, QR-3 |
| OBJ-9 | Lifecycle Cost Optimization | Quality design reduces construction rework and supports efficient operations/maintenance | QR-1 to QR-4 |
| OBJ-5 | Terminal Continuity | Phased drawing release (if applicable) can support construction schedule and minimize terminal disruption | — |

**Source:** Decomposition Section 6 Objective-to-Deliverable Mapping — PKG-20 supports OBJ-1 (line 780); secondary objectives based on **ASSUMPTION** regarding procedure's role in quality assurance, compliance, and efficient project execution

## Cross-Document Traceability

This Procedure defines the production workflow for DEL-20.01. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Datasheet.md | Factual identification, attributes, conditions, references | Identification § provides deliverable identity; Attributes § provides drawing standards; Conditions § provides project context |
| Specification.md | Requirements and verification criteria | FR-1 to FR-6 define what to produce; QR-1 to QR-4 define quality requirements; Verification § defines acceptance criteria |
| Guidance.md | Engineering rationale and decision context | Principles explain design approach; Considerations inform technical decisions; Trade-offs address key design choices |

**Procedure-to-Specification Mapping:**

| Procedure Step | Specification Requirement | What Is Implemented |
|----------------|--------------------------|---------------------|
| Step 1.1 | Scope, FR-6, Standards | Design basis, project-specific requirements, applicable standards |
| Step 1.2 | Documentation | Drawing list and release schedule |
| Step 1.3 | FR-6, PR-1, PR-2, Standards | Design criteria, CAD standards |
| Step 2.1 | FR-2, FR-5, FR-6 | Instrument location concepts |
| Step 2.2 | FR-4, INT-1 | Cable routing concepts |
| Step 2.3 | FR-3 | Installation detail concepts |
| Step 3.1 | FR-2, PR-1, PR-2 | Detailed instrument location plans |
| Step 3.2 | FR-3, Standards | Detailed installation details |
| Step 3.3 | FR-4, INT-1, Standards | Cable schedules |
| Step 4.2, 4.3 | QR-1, Verification | Self-check and independent check |
| Step 4.4 | QR-1, INT-1, Verification | Interdisciplinary check |
| Step 5.1, 5.2 | Documentation, QR-1 | Drawing approval and issuance |
| Step 6.1, 6.2 | QR-2, QR-4 | Change management and as-built updates |
