# Procedure: DEL-04.01 Pavement Design Drawing Set

## Purpose

This procedure defines the workflow for producing, reviewing, coordinating, and issuing the Pavement Design Drawing Set (DEL-04.01) to ensure:
- All four documents (Datasheet, Specification, Guidance, Procedure) remain aligned throughout the drafting and review process
- Traceability is maintained to DEL-04.02 (specification), DEL-04.03 (calculations), and Employer's Requirements
- **ASSUMPTION** and **TBD** items are logged, tracked, and resolved prior to final issuance
- Cross-package coordination (PKG-03, PKG-05, PKG-07, PKG-08) occurs at defined gates
- OBJ-8 future expansion provisions are validated and clearly annotated

## Prerequisites

### Dependencies
**Mode**: NOT_TRACKED (per `_DEPENDENCIES.md`)
**Note**: Dependencies are coordinated externally by humans. The following inputs are typically required but scheduling is human-managed:
- Site survey data (coordinate control, existing topography, existing utilities)
- Geotechnical investigation report (soil bearing capacity, CBR, groundwater levels) – **TBD**
- Employer's Requirements Volume 2 Part 1 & 2 (drawing standards, pavement requirements) – accessible but detailed review **location TBD**
- DEL-04.03 preliminary calculation outputs (layer thickness ranges, loading assumptions)
- Interface data from PKG-03 (drainage invert elevations), PKG-05 (structure finished floor elevations), PKG-07 (track elevations), PKG-08 (berth elevations) – to be coordinated per workflow steps

### Reference Materials
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- **Datasheet (DEL-04.01)**: Current version with Attributes, Conditions, Construction, Assumptions & TBDs
- **Specification (DEL-04.01)**: Current version with Requirements R1.1–R3.3
- **Guidance (DEL-04.01)**: Current version with Review Checklist, Principles, Coordination Guidance
- **Package Reference Index**: `test/execution/PKG-04_Pavement_and_Surfacing/0_References/_REFERENCE_INDEX.md`

### Personnel & Roles
- **Civil Lead Engineer**: Responsible for drawing technical content, interface coordination, and approval
- **DEL-04.02 Specification Author**: Provides material and workmanship references for drawing annotations
- **DEL-04.03 Calculation Engineer**: Provides pavement section thickness outputs and design parameter validation
- **DEL-04.04 QA/QC Lead**: Reviews drawings for testability and receives final issued set for field verification planning
- **QA Reviewer**: Performs cross-document consistency checks, traceability audits, and assumption log maintenance
- **Package Coordinators (PKG-03, PKG-05, PKG-07, PKG-08)**: Provide interface data and review interface drawings

### Tools & Systems (**TBD** – pending project standards confirmation)
- **CAD software**: AutoCAD or equivalent per project CAD standards
- **Document management system**: For revision control and drawing distribution
- **Assumption tracking log**: Spreadsheet or database for logging **ASSUMPTION** and **TBD** items (template provided in Step 1)

## Steps

### Step 1: Initialize Deliverable and Capture Scope

**Objective**: Establish deliverable scope, identify inputs, and create tracking infrastructure

**Tasks**:
1.1. Review Datasheet "Attributes" and "Drawing Scope" sections to understand deliverable extent (asphalt zones, concrete zones, curbs, sidewalks, parking, line marking, interfaces)

1.2. Review Decomposition Section PKG-04 and OBJ-8 mapping to confirm:
- Phase 2 expansion corridor requirements (dimensions, assumed elevations)
- Interface deliverables (PKG-03, PKG-05, PKG-07, PKG-08)
- Anticipated artifacts (paving layout plans, pavement sections, parking layout, curb details, line marking plans)

1.3. Review Datasheet "Assumptions & TBDs" section and create **Assumption Tracking Log** with columns:
- Assumption/TBD ID (format: A-04.01-NNN for assumptions, T-04.01-NNN for TBDs)
- Description
- Location (document/sheet reference)
- Category (geotechnical, interface, material, loading, Phase 2, etc.)
- Impacted deliverables (DEL-04.02, DEL-04.03, DEL-04.04, adjacent packages)
- Resolution path (who resolves, required input, target date)
- Status (open, in-progress, resolved, closed)
- Resolution notes

1.4. Log initial **TBD** items from Datasheet into Assumption Tracking Log:
- T-04.01-001: Site-specific geotechnical data (soil bearing capacity, CBR, groundwater elevation)
- T-04.01-002: Employer's Requirements specific clause references for pavement design criteria
- T-04.01-003: Exact drawing sheet count and numbering system
- T-04.01-004: CAD standards and title block requirements
- T-04.01-005: Line marking color and reflectivity standards (pending DEL-04.02 advancement)

1.5. Log initial **ASSUMPTION** items from Datasheet into Assumption Tracking Log:
- A-04.01-001: 25-year design life for industrial pavement
- A-04.01-002: Phase 2 expansion corridors and tie-in elevations pending Phase 2 design input
- A-04.01-003: Applicable standards (OPSS/MMCD, TAC)
- A-04.01-004: Heavy vehicle loading class (e.g., AASHTO H-20 equivalent or industrial axle loads)

**Verification**: Assumption Tracking Log is created and populated with initial items from Datasheet

**Records**: Assumption Tracking Log (file name: `DEL-04.01_Assumption_Log.xlsx` or similar, stored in deliverable folder)

---

### Step 2: Draft Plan and Section Sheets with Traceability

**Objective**: Produce initial drawing set with full traceability to specifications and calculations

**Tasks**:
2.1. Obtain inputs:
- Site survey base map (coordinate grid, existing topography, existing features)
- DEL-04.03 preliminary pavement section thicknesses (if available; otherwise use Datasheet typical ranges and flag as **TBD**)
- DEL-04.02 draft specification clauses for material call-outs
- Interface data requests sent to PKG-03, PKG-05, PKG-07, PKG-08 coordinators (see Step 3 coordination tasks)

2.2. Draft **Plan Sheets** per Specification R1.1:
- Show asphalt paving extents, concrete surfacing zones, curbs, gutters, sidewalks, parking layout, line marking
- Annotate Phase 2 expansion corridors per OBJ-8 with dimensional envelopes
- Add coordinate grid and benchmark references
- Mark interface tie-in points to PKG-03 (drainage), PKG-05 (structures), PKG-07 (rail), PKG-08 (marine) – initial locations based on available data; flag as **TBD** if interface elevations are pending
- Include title block, scale, north arrow, legend

2.3. Draft **Section & Detail Sheets** per Specification R1.2:
- Create typical pavement sections for each zone (heavy duty asphalt, light duty asphalt, concrete, parking, etc.)
- Annotate layer thicknesses: Reference DEL-04.03 calculation sheets if available; if pending, use Datasheet typical ranges and flag as **TBD**
- Annotate material call-outs: Reference DEL-04.02 specification clauses (e.g., "Asphalt Concrete Wearing Course per DEL-04.02 Clause 3.2.1")
- Add subgrade preparation requirements, drainage slopes, joint details
- State tolerances (thickness, grade, smoothness) consistent with DEL-04.02 or industry standards (**ASSUMPTION** if not yet specified in DEL-04.02)

2.4. Draft **Line Marking Plans** per Specification R1.3:
- Show traffic control striping, parking stall striping, safety markings
- Create line marking legend with material references to DEL-04.02 (paint vs. thermoplastic, color, reflectivity)
- Add application notes referencing DEL-04.02 environmental constraints

2.5. Draft **Notes & Document Control Sheets** per Specification R1.5:
- General notes sheet with abbreviations, symbols, standard details
- Drawing list/index sheet
- Revision history table (initial entry: Rev 0, date, "Initial Issue for Review")
- Reference table listing DEL-04.02, DEL-04.03, Employer's Requirements sections

2.6. Create **Traceability Matrix** (spreadsheet or table) linking:
- Drawing sheet number / detail reference
- Specification clause (DEL-04.02)
- Calculation sheet (DEL-04.03)
- Employer's Requirements reference (if applicable)
- Assumption/TBD ID (if element is based on assumption or pending data)

**Verification**:
- All drawing sheets conform to Specification R1.1–R1.5 content requirements
- Traceability Matrix is complete and cross-references are correct
- **TBD** flags are added to drawing notes for any elements pending input

**Records**:
- Draft drawing set (CAD files and PDF plot set)
- Traceability Matrix (file name: `DEL-04.01_Traceability_Matrix.xlsx` or similar, stored in deliverable folder)

---

### Step 3: Perform Guidance Review and Log Issues

**Objective**: Verify drawing completeness and consistency using Guidance Review Checklist; document findings in Assumption Tracking Log

**Tasks**:
3.1. **Pre-review preparation**:
- Update Datasheet Assumptions & TBDs if new items discovered during drafting
- Obtain latest DEL-04.03 calculation outputs (coordinate with DEL-04.03 engineer)
- Obtain latest DEL-04.02 specification draft (coordinate with DEL-04.02 author)

3.2. **Execute Guidance Review Checklist** (from Guidance document):
- Step 1: Plan Completeness (verify coverage, extents, Phase 2 provisions, coordinate references, scale)
- Step 2: Section Verification (validate thicknesses vs. DEL-04.03, check material call-outs vs. DEL-04.02, verify tolerances, check joint details and drainage provisions)
- Step 3: Line Marking & Notes (check legend completeness, material specs, dimensions, application notes)
- Step 4: Interface & OBJ-8 Callouts (verify PKG-03/05/07/08 interface coordination, Phase 2 callouts, assumption logging)
- Step 5: Document Control Review (verify title block, drawing list, revision history, reference table, legend & notes)
- Step 6: Traceability Audit (verify specification references, calculation references, test record references, cross-document consistency)

3.3. **Document review findings**:
- For each checklist item that fails or is incomplete: Create an issue entry with description, affected sheets, required action
- For each new **ASSUMPTION** or **TBD** discovered: Add to Assumption Tracking Log with ID, description, resolution path
- For each interface coordination need: Add coordination action item (see Step 4)

3.4. **Coordination actions** (cross-package interface verification):
- **PKG-03 coordination**: Request surface drainage tie-in elevations (catch basin rim and invert elevations from DEL-03.01); verify pavement slopes accommodate drainage conveyance
- **PKG-05 coordination**: Request structure finished floor elevations and pad elevations (from DEL-05.01); verify pavement grades at building perimeters are compatible
- **PKG-07 coordination**: Request track top-of-rail elevations and clearance envelopes (from DEL-07.01); verify pavement elevations at rail crossings maintain clearances
- **PKG-08 coordination**: Request berth elevations and wharf edge details (from DEL-08.01); verify pavement termination limits and loading arm swing radii clearances

3.5. **Reviewer comment management**:
- Collect comments from Civil Lead, QA Reviewer, and Package Coordinators
- Log comments in reviewer comment log (spreadsheet or document management system)
- Assign each comment to responsible party (Civil Lead for technical, DEL-04.02 author for material specs, DEL-04.03 engineer for calculation revisions, etc.)
- Track comment resolution status (open, addressed, closed)

**Verification**:
- Guidance Review Checklist is completed with all items checked or flagged
- Assumption Tracking Log is updated with new **ASSUMPTION** and **TBD** items
- Reviewer comment log is created and populated
- Coordination action items are assigned to responsible parties

**Records**:
- Completed Guidance Review Checklist (annotated with findings)
- Updated Assumption Tracking Log
- Reviewer comment log (file name: `DEL-04.01_Review_Comments.xlsx` or similar)
- Coordination meeting notes or email records (for interface data requests)

---

### Step 4: Coordinate with DEL-04.03 and Revise Drawings

**Objective**: Ensure drawing section thicknesses and design parameters align with DEL-04.03 calculation outputs; update drawings and traceability accordingly

**Tasks**:
4.1. **Coordination meeting with DEL-04.03 engineer**:
- Review DEL-04.03 calculation results: pavement layer thicknesses, design load assumptions, subgrade bearing capacity assumptions, sensitivity analysis findings
- Identify any discrepancies between drawing sections and calculation outputs
- Discuss impact of geotechnical data updates (if new site investigation results are available)
- Confirm calculation sheet numbering for drawing cross-references

4.2. **Update drawing sections** (if calculation results differ from initial draft):
- Revise layer thicknesses on section drawings to match DEL-04.03 outputs
- Update drawing notes to reference correct DEL-04.03 calculation sheet numbers
- Update Traceability Matrix to reflect new calculation references

4.3. **Update Assumption Tracking Log**:
- If geotechnical **TBD** items are resolved (e.g., T-04.01-001), mark as "Resolved" and add resolution notes
- If calculation reveals new design assumptions, add to log as **ASSUMPTION** entries
- If calculation identifies sensitivity to pending inputs, add **TBD** entries for those inputs

4.4. **Sensitivity study consideration**:
- If major layout changes are proposed (e.g., relocating pavement zones, adding/removing expansion corridors), request DEL-04.03 engineer to re-run calculations or perform sensitivity study
- Document layout change rationale in Procedure notes and update Datasheet accordingly

4.5. **Notify DEL-04.02 if material specifications need updates**:
- If DEL-04.03 calculations indicate different material requirements (e.g., higher strength concrete, different asphalt mix), notify DEL-04.02 author to update specification
- Update drawing material call-outs to reference revised DEL-04.02 clauses

**Verification**:
- Drawing sections match DEL-04.03 calculation outputs (verified by cross-checking Traceability Matrix)
- Assumption Tracking Log reflects resolution of calculation-dependent **TBD** items
- DEL-04.02 author is notified of any material specification changes

**Records**:
- Coordination meeting minutes with DEL-04.03 engineer
- Revised drawing set (CAD files and PDF, updated revision number if significant changes)
- Updated Traceability Matrix
- Updated Assumption Tracking Log

---

### Step 5: Perform Final QA Review and Release Drawing Set

**Objective**: Ensure drawing set is complete, consistent, and ready for issuance; hand off to DEL-04.04 for field verification planning

**Tasks**:
5.1. **Final QA review**:
- Re-run Guidance Review Checklist to confirm all previous findings are addressed
- Verify Traceability Matrix is complete and all cross-references are correct
- Verify Assumption Tracking Log shows all open **TBD** items have resolution paths or are flagged for issuance with notification to stakeholders
- Verify all reviewer comments are resolved or formally deferred (with justification)

5.2. **Cross-document consistency check**:
- Verify terminology, entity names, and values are consistent across Datasheet, Specification, Guidance, and Procedure
- Verify drawing content aligns with Specification Requirements R1.1–R1.5
- Verify Guidance Review Checklist items all pass or are documented as acceptable deviations (with justification)

5.3. **Approval sign-off**:
- Civil Lead Engineer reviews and signs title block (or digital approval per project document management system)
- QA Reviewer signs off on traceability audit and cross-document consistency check
- Package Manager or Project Engineer provides final approval for issuance

5.4. **Update drawing revision status**:
- Update revision history table on drawings (e.g., "Rev 1, [Date], Issued for Construction")
- Update drawing list/index sheet with current revision status for all sheets
- Update document management system with issued drawing set

5.5. **Handoff to DEL-04.04**:
- Provide final issued drawing set (CAD files and PDF) to DEL-04.04 QA/QC lead
- Provide Traceability Matrix and Assumption Tracking Log for reference
- Schedule handoff meeting to review:
  - Critical test locations (heavy load zones, transition areas, interface zones)
  - Acceptance criteria (tolerances, material specifications) from drawings and DEL-04.02
  - Test planning requirements (compaction testing, core sampling, thickness verification)

5.6. **Distribution**:
- Distribute drawing set per project distribution matrix (Owner, Engineer, Contractor, Package Coordinators)
- Notify DEL-04.02 and DEL-04.03 teams of final issuance (for their records and future reference)

**Verification**:
- Guidance Review Checklist fully passes (or acceptable deviations documented)
- Traceability Matrix is complete and audited
- Assumption Tracking Log shows all **TBD** items have resolution paths or are flagged for stakeholder notification
- Approval signatures (or digital approvals) are obtained
- DEL-04.04 handoff meeting is completed

**Records**:
- Final issued drawing set (CAD files and PDF, with revision history)
- Completed Guidance Review Checklist (final version)
- Final Traceability Matrix
- Final Assumption Tracking Log
- Approval sign-off records (title block signatures, email approvals, or document management system records)
- DEL-04.04 handoff meeting minutes

---

### Step 6: Manage Revisions (Post-Issuance)

**Objective**: Control drawing revisions to maintain traceability and cross-document consistency

**Tasks**:
6.1. **Revision triggers**:
- DEL-04.03 calculation updates (revised geotechnical data, design load changes)
- DEL-04.02 specification updates (material specification changes, new testing requirements)
- Interface coordination changes (PKG-03/05/07/08 elevation or layout changes)
- Construction phase changes (contractor RFI responses, field condition adaptations)
- Phase 2 input received (OBJ-8 tie-in elevations and layouts confirmed)

6.2. **Revision process**:
- Update affected drawing sheets (CAD files)
- Update revision history table on affected sheets (new revision number, date, description of changes)
- Update drawing list/index sheet with new revision status
- Re-run Guidance Review Checklist for affected sheets to confirm cross-document consistency is maintained
- Update Traceability Matrix if new specification or calculation references are added
- Update Assumption Tracking Log if **ASSUMPTION** or **TBD** items are resolved or new items are added

6.3. **Approval and distribution**:
- Obtain Civil Lead and QA Reviewer sign-off on revised sheets
- Issue revised drawing set per project distribution matrix
- Notify DEL-04.04 team if revisions affect field testing acceptance criteria

**Verification**:
- Revised sheets include updated revision history and correct revision number
- Traceability Matrix reflects any new cross-references
- Assumption Tracking Log is current
- Approval sign-offs are obtained

**Records**:
- Revised drawing set (CAD files and PDF, with updated revision history)
- Updated Traceability Matrix (if applicable)
- Updated Assumption Tracking Log (if applicable)
- Approval records for revised sheets

---

## Verification

### Verification Checkpoints

| Checkpoint | Verification Method | Acceptance Criteria |
|------------|-------------------|---------------------|
| Step 1 complete | Review Assumption Tracking Log | Log is created and populated with initial Datasheet **TBD** and **ASSUMPTION** items |
| Step 2 complete | Review draft drawing set and Traceability Matrix | All sheets per Specification R1.1–R1.5 are drafted; Traceability Matrix links all elements to DEL-04.02/DEL-04.03/ER |
| Step 3 complete | Review Guidance Review Checklist and Assumption Tracking Log | Checklist is completed; new **ASSUMPTION**/**TBD** items are logged; reviewer comments are documented |
| Step 4 complete | Review coordination meeting minutes and updated Traceability Matrix | Drawing sections match DEL-04.03 outputs; Traceability Matrix is updated; Assumption Tracking Log reflects calculation-based resolutions |
| Step 5 complete | Review approval records and DEL-04.04 handoff minutes | Approvals obtained; drawing set issued; DEL-04.04 handoff completed |
| Step 6 (revisions) | Review revision history table and updated Traceability Matrix | Revised sheets have correct revision number and description; Traceability Matrix is current |

### Overall Acceptance Criteria
- Drawing set conforms to all Specification Requirements (R1.1–R3.3)
- Guidance Review Checklist fully passes (or acceptable deviations documented with justification)
- Traceability Matrix demonstrates complete linkage to DEL-04.02, DEL-04.03, and Employer's Requirements
- Assumption Tracking Log shows all **TBD** items either resolved or flagged with resolution paths
- Approval sign-offs obtained from Civil Lead and QA Reviewer
- DEL-04.04 handoff completed with test planning requirements communicated

## Records

### Deliverable Records (Produced by This Procedure)
1. **Drawing Set (DEL-04.01)**: CAD files and PDF plot set with all plan, section, detail, line marking, and notes sheets
2. **Traceability Matrix**: Spreadsheet linking drawing elements to specification clauses, calculation sheets, and ER references
3. **Assumption Tracking Log**: Spreadsheet logging **ASSUMPTION** and **TBD** items with resolution paths and status
4. **Guidance Review Checklist (completed)**: Annotated checklist documenting review findings
5. **Reviewer Comment Log**: Spreadsheet or document management system record of review comments and resolutions
6. **Coordination Meeting Minutes**: Records of coordination meetings with DEL-04.03 engineer, Package Coordinators, and DEL-04.04 team
7. **Approval Records**: Title block signatures, email approvals, or document management system records confirming final approval

### File Naming Conventions (**TBD** – pending project drawing management plan)
- CAD files: `DEL-04.01-C-[Sheet Number]-[Sheet Title].dwg` (example: `DEL-04.01-C-001-PLAN.dwg`)
- PDF files: `DEL-04.01-C-[Sheet Number]-[Sheet Title]_R[Rev].pdf` (example: `DEL-04.01-C-001-PLAN_R1.pdf`)
- Traceability Matrix: `DEL-04.01_Traceability_Matrix.xlsx`
- Assumption Log: `DEL-04.01_Assumption_Log.xlsx`
- Guidance Checklist: `DEL-04.01_Guidance_Checklist_[Date].pdf`

### Storage Locations
- **Working files**: `test/execution/PKG-04_Pavement_and_Surfacing/1_Working/DEL-04.01_Pavement_Design_Drawing_Set/`
- **Issued files**: `test/execution/PKG-04_Pavement_and_Surfacing/3_Issued/` (with deliverable ID and revision in file name)
- **Reference files**: `test/execution/PKG-04_Pavement_and_Surfacing/0_References/` (geotechnical reports, survey data, ER excerpts)

## References

### Source Documents
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-04, DEL-04.01, OBJ-8
- **Datasheet (DEL-04.01)**: Attributes, Conditions, Construction, Assumptions & TBDs, Cross-document Coordination
- **Specification (DEL-04.01)**: Requirements R1.1–R3.3, Verification Methods, Standards
- **Guidance (DEL-04.01)**: Review Checklist, Principles, Considerations, Trade-offs, Coordination Guidance, Examples
- **Employer's Requirements Volume 2 Part 1**: General requirements, drawing standards (**location TBD**)
- **Employer's Requirements Volume 2 Part 2**: Civil & Process Mechanical Works, pavement requirements (**location TBD**)

### Related Deliverables
- **DEL-04.02**: Pavement Technical Specification (material and workmanship requirements)
- **DEL-04.03**: Pavement Design Calculations (analytical basis for section thicknesses)
- **DEL-04.04**: Pavement Installation & Test Records (field verification basis)
- **PKG-03 deliverables**: Underground Utilities (drainage interface elevations)
- **PKG-05 deliverables**: Concrete Structures (structure-to-pavement interfaces)
- **PKG-07 deliverables**: Rail Works (track elevations, rail crossing details)
- **PKG-08 deliverables**: Marine Structures (pavement termination boundaries)
