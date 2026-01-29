# Procedure: DEL-04.02 Pavement Technical Specification

## Purpose

This procedure defines the workflow for producing, reviewing, coordinating, and issuing the Pavement Technical Specification (DEL-04.02) to ensure specification clauses are enforceable, traceable to DEL-04.01 (drawings) and DEL-04.03 (calculations), and support DEL-04.04 (test records) quality control requirements, while maintaining OBJ-8 future expansion provisions.

## Prerequisites

### Dependencies
**Mode**: NOT_TRACKED (per `_DEPENDENCIES.md`)
**Note**: Dependencies are coordinated externally by humans. The following inputs are typically required:
- Employer's Requirements Volume 2 Part 1 & 2 (specification format, material requirements, QA/QC procedures) – **location TBD**
- DEL-04.01 draft drawing set (material call-outs and tolerances to be incorporated into specification)
- DEL-04.03 preliminary calculation results (material properties, pavement section thicknesses)
- Applicable standards (OPSS, MMCD, TAC, CSA, ASTM, AASHTO) – **TBD** which standards govern
- Interface coordination with PKG-03, PKG-05, PKG-07, PKG-08

### Reference Materials
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- **Datasheet (DEL-04.02)**: Current version with Attributes, Key Performance Requirements, Assumptions & TBDs
- **Specification (DEL-04.02)**: Current version with Requirements R1.1–R3.3
- **Guidance (DEL-04.02)**: Current version with Review Checklist, Principles, Trade-offs
- **Applicable standards**: OPSS, MMCD, TAC, CSA A23.1/A23.2, ASTM, AASHTO (**TBD** – obtain copies or confirm availability)

### Personnel & Roles
- **Civil Lead Engineer (Specification Author)**: Responsible for drafting specification clauses, coordinating with DEL-04.01/DEL-04.03, resolving technical issues
- **DEL-04.01 Drafter**: Provides material call-outs and tolerances from drawings for incorporation into specification
- **DEL-04.03 Calculation Engineer**: Provides material properties and design parameters for specification validation
- **DEL-04.04 QA/QC Lead**: Reviews specification QC section for testability and conformance with test record requirements
- **QA Reviewer**: Performs traceability audits, cross-document consistency checks, assumption log maintenance
- **Package Coordinators (PKG-03, PKG-05, PKG-07, PKG-08)**: Review interface coordination clauses

### Tools & Systems
- **Word processor or specification software**: For drafting specification document per project template
- **Assumption tracking log**: Coordinated with DEL-04.01 and DEL-04.03 (spreadsheet or database)
- **Traceability matrix**: Linking specification clauses to drawings, calculations, and test requirements (spreadsheet)

## Steps

### Step 1: Initialize Specification and Capture Scope

**Objective**: Establish specification scope, obtain template, and create tracking infrastructure

**Tasks**:
1.1. Review Datasheet "Attributes" and "Specification Scope" to understand deliverable extent

1.2. Obtain project specification template (**TBD** – confirm from project specification manual or ER):
- Section numbering system (e.g., CSI MasterFormat Division 32, or custom project numbering)
- Clause structure (General, Materials, Execution, Quality Control sections)
- Standard terminology and abbreviations
- Title page, table of contents, references section formats

1.3. Review Datasheet "Assumptions & TBDs" and create or update **Assumption Tracking Log** (coordinated with DEL-04.01 and DEL-04.03 logs):
- Use common format with columns: ID, Description, Location (clause reference), Category, Impacted deliverables, Resolution path, Status, Resolution notes
- Import DEL-04.01 assumptions relevant to specification (material types, loading assumptions, interface elevations)
- Import DEL-04.03 assumptions relevant to specification (design life, material properties, geotechnical parameters)

1.4. Log initial specification-specific **TBD** items:
- T-04.02-001: Project specification template and section numbering system
- T-04.02-002: Applicable standards (OPSS vs. MMCD for BC jurisdiction)
- T-04.02-003: Testing laboratory accreditation requirements
- T-04.02-004: Submittal approval lead times and procedures
- T-04.02-005: Line marking color codes and reflectivity standards

1.5. Log initial specification-specific **ASSUMPTION** items:
- A-04.02-001: Asphalt binder PG 58-34 for Fraser Surrey, BC climate
- A-04.02-002: Concrete 28-day strength 30-35 MPa
- A-04.02-003: Compaction densities (95% subgrade, 98% base, 95% asphalt TMD)
- A-04.02-004: Testing frequencies (compaction 1 per 500 m², cores 1 per 2000 m²)

1.6. Create **Traceability Matrix** (spreadsheet) with columns:
- Specification clause number/title
- DEL-04.01 drawing reference (sheet number, section/detail number)
- DEL-04.03 calculation reference (calculation sheet number)
- DEL-04.04 test record reference (test procedure, acceptance form)
- Employer's Requirement or standard reference
- Assumption/TBD ID (if clause is based on assumption or pending data)

**Verification**: Assumption Tracking Log is updated with specification items; Traceability Matrix template is created

**Records**: Updated Assumption Tracking Log, Traceability Matrix template

---

### Step 2: Draft Specification Clauses with Inline Traceability

**Objective**: Produce initial specification document with full traceability to drawings, calculations, and standards

**Tasks**:
2.1. Obtain inputs:
- DEL-04.01 draft drawing set (material call-outs, tolerances, section thicknesses)
- DEL-04.03 draft calculation results (design parameters, material properties, layer thicknesses)
- Applicable standards (OPSS, MMCD, TAC, CSA, ASTM, AASHTO – obtain copies or confirm online access)
- Employer's Requirements excerpts for pavement (Volume 2 Part 2 – **location TBD**)

2.2. Draft **General Requirements Section** per Specification R1.1 (typical content):
- Scope statement (what work is covered by this specification)
- Reference documents (list DEL-04.01, DEL-04.03, ER, standards)
- Submittals (mix designs, material certifications, QC plan, testing lab accreditation)
- Quality assurance (roles and responsibilities, inspection access, testing requirements overview)
- Definitions (key terms used in specification)

2.3. Draft **Materials Section** per Specification R1.1:
- Asphalt materials clauses (binder grade, aggregate gradation, filler, RAP, tack coat)
  - Reference DEL-04.01 drawing sections showing asphalt zones
  - Reference DEL-04.03 calculation sheet with mix design parameters
  - Reference applicable standard (OPSS, ASTM, AASHTO)
  - Flag **ASSUMPTION** or **TBD** items inline with assumption log ID
- Concrete materials clauses (cement, aggregates, admixtures, reinforcement, joint materials, curing compounds)
  - Reference DEL-04.01 drawing details for concrete zones
  - Reference DEL-04.03 calculation sheet with strength requirements
  - Reference CSA A23.1 or equivalent standard
  - Flag **ASSUMPTION** or **TBD** items inline
- Base/subbase materials clauses (aggregate gradation, plasticity, compaction properties)
  - Reference DEL-04.01 pavement sections
  - Reference DEL-04.03 subgrade bearing capacity assumptions
  - Reference OPSS/MMCD standard gradations
  - Flag **ASSUMPTION** or **TBD** items inline
- Line marking materials clauses (paint vs. thermoplastic, color, reflectivity, primer)
  - Reference DEL-04.01 line marking plans
  - Reference TAC or transportation authority standards (**TBD**)
  - Flag **ASSUMPTION** or **TBD** items inline

2.4. Draft **Execution/Workmanship Section** per Specification R1.2:
- Subgrade preparation clauses (clearing, grading, moisture conditioning, compaction, proof rolling)
- Base/subbase placement clauses (lift thickness, moisture control, compaction, surface preparation)
- Asphalt paving clauses (mix temperature, weather limitations, placement, compaction, joint construction)
- Concrete placement clauses (formwork, mixing, placing, finishing, joint construction, curing)
- Line marking application clauses (surface prep, application equipment, application rate, bead application, weather limitations)
- Interface coordination clauses (PKG-03 utility trenches, PKG-05 structure transitions, PKG-07 rail crossings, PKG-08 wharf edge)
- For each clause: Reference DEL-04.01 drawing tolerances, reference applicable standard workmanship section, flag **ASSUMPTION**/**TBD** inline

2.5. Draft **Quality Control Section** per Specification R1.3:
- Material testing clauses (aggregate gradation, asphalt mix verification, concrete strength, concrete air content)
- In-place testing clauses (subgrade/base/asphalt compaction, thickness verification cores, surface smoothness)
- For each test: Specify test method (ASTM standard), frequency (per m² or per volume), acceptance criteria (numerical limits)
- Non-conformance procedure clause (identification, documentation, corrective action, re-testing, disposition)
- Documentation requirements (daily QC reports, material certifications, test location plans, NCR forms) supporting DEL-04.04
- OBJ-8 enhanced testing clause (higher frequency or additional testing in Phase 2 expansion corridors)
- Flag **ASSUMPTION** items for testing frequencies if not confirmed from ER

2.6. Draft **OBJ-8 Future Expandability Section** per Specification R1.5:
- Design for ultimate loading clause (Phase 2 expansion corridor pavement designed for ultimate Phase 2 loading per DEL-04.03 design case)
- Construction joint protection clause (sawcut/formed joints at Phase 2 tie-ins, joint protection measures)
- Utility penetration documentation clause (coordinate with PKG-03)
- Enhanced as-built documentation clause (survey, material records, test locations with enhanced detail for expansion corridors)

2.7. Update **Traceability Matrix** as clauses are drafted:
- Enter specification clause number/title
- Enter corresponding DEL-04.01 drawing reference
- Enter corresponding DEL-04.03 calculation reference
- Enter DEL-04.04 test record reference (test procedure, form)
- Enter standard or ER reference
- Enter assumption/TBD ID if clause is based on pending data

**Verification**:
- All specification sections per Requirements R1.1–R1.5 are drafted
- Every clause has inline traceability reference to drawing, calculation, or standard
- **ASSUMPTION**/**TBD** items are flagged inline and cross-referenced to assumption log
- Traceability Matrix is populated for all drafted clauses

**Records**:
- Draft specification document
- Updated Traceability Matrix
- Updated Assumption Tracking Log (if new items discovered during drafting)

---

### Step 3: Perform Guidance Review and Log Issues

**Objective**: Verify specification completeness, enforceability, and consistency using Guidance Review Checklist

**Tasks**:
3.1. **Pre-review preparation**:
- Update Datasheet Assumptions & TBDs if new items discovered during drafting
- Obtain final DEL-04.01 drawing set (or latest revision) for cross-checking
- Obtain final DEL-04.03 calculation results (or latest revision) for validation
- Schedule coordination meetings with PKG-03, PKG-05, PKG-07, PKG-08 package leads to review interface clauses

3.2. **Execute Guidance Review Checklist** (from Guidance document):
- Step 1: Material Clause Review (verify completeness, standard references, cross-references to drawings/calculations, assumption flagging)
- Step 2: Workmanship Clause Review (verify procedure specifications, tolerances consistent with drawings, interface handling)
- Step 3: Quality Control Clause Review (verify testing methods, frequencies, acceptance criteria, feasibility, documentation requirements)
- Step 4: Interface Coordination Review (verify clauses for PKG-03/05/07/08 interfaces; conduct coordination meetings)
- Step 5: OBJ-8 Future Expandability Review (verify OBJ-8 provisions are clear, measurable, and enforceable)
- Step 6: Traceability Audit (verify all cross-references in Traceability Matrix are correct and bidirectional)
- Step 7: Assumption and TBD Tracking (verify all **ASSUMPTION**/**TBD** items are logged with resolution paths)

3.3. **Document review findings**:
- For each checklist item that fails or is incomplete: Create issue entry with description, affected clauses, required action
- For each new **ASSUMPTION** or **TBD** discovered: Add to Assumption Tracking Log with ID, description, resolution path
- For each cross-reference error: Correct in specification document and Traceability Matrix

3.4. **Coordination actions** (interface clause verification):
- **PKG-03 coordination meeting**: Review utility trench backfill compaction, pavement restoration, catch basin rim adjustment clauses; obtain PKG-03 lead sign-off
- **PKG-05 coordination meeting**: Review structure-to-pavement transition clauses; obtain PKG-05 lead sign-off
- **PKG-07 coordination meeting**: Review rail crossing embedment clauses; obtain PKG-07 lead sign-off
- **PKG-08 coordination meeting**: Review pavement-to-wharf interface clauses; obtain PKG-08 lead sign-off

3.5. **Reviewer comment management**:
- Collect comments from Civil Lead, QA Reviewer, DEL-04.04 QA/QC Lead, Package Coordinators
- Log comments in reviewer comment log
- Assign resolution responsibility
- Track comment status (open, addressed, closed)

**Verification**:
- Guidance Review Checklist is completed with all items checked or flagged
- Assumption Tracking Log is updated
- Reviewer comment log is created and populated
- Coordination meeting sign-offs obtained from PKG-03/05/07/08 leads

**Records**:
- Completed Guidance Review Checklist (annotated with findings)
- Updated Assumption Tracking Log
- Reviewer comment log
- Coordination meeting minutes with package lead sign-offs

---

### Step 4: Coordinate with DEL-04.01 and DEL-04.03 and Revise Specification

**Objective**: Ensure specification clauses align with finalized drawing and calculation content

**Tasks**:
4.1. **Coordination with DEL-04.01 drafter**:
- Review DEL-04.01 drawing material call-outs to verify they reference correct specification clause numbers
- Identify any drawing revisions since specification drafting (new materials, revised tolerances, added details)
- Update specification clauses if drawing changes require it
- Update Traceability Matrix if new drawing references are added

4.2. **Coordination with DEL-04.03 engineer**:
- Review DEL-04.03 final calculation results to verify material properties and design parameters match specification clauses
- Identify any calculation revisions since specification drafting (updated geotechnical data, revised layer thicknesses, changed material properties)
- Update specification clauses if calculation changes require it (e.g., increased concrete strength, different asphalt mix)
- Update Traceability Matrix if new calculation references are added

4.3. **Coordination with DEL-04.04 QA/QC lead**:
- Provide draft specification QC section to DEL-04.04 lead for review
- Verify testing requirements, frequencies, methods, and acceptance criteria are documented in DEL-04.04 test procedures and forms
- Update specification if DEL-04.04 lead identifies testing requirements that are not feasible or not documented

4.4. **Update Assumption Tracking Log**:
- If drawing or calculation revisions resolve **TBD** items, mark as "Resolved" and add resolution notes
- If coordination identifies new assumptions or TBDs, add to log

4.5. **Notify stakeholders of specification changes**:
- If material or workmanship clauses are significantly revised, notify DEL-04.01 drafter (may require drawing note updates)
- If testing requirements are revised, notify DEL-04.04 QA/QC lead (may require test procedure updates)

**Verification**:
- Specification clauses match DEL-04.01 drawing content (verified by Traceability Matrix audit)
- Specification clauses match DEL-04.03 calculation outputs (verified by Traceability Matrix audit)
- Specification QC section is reviewed and accepted by DEL-04.04 lead
- Assumption Tracking Log reflects coordination-based resolutions

**Records**:
- Coordination meeting minutes with DEL-04.01 drafter, DEL-04.03 engineer, DEL-04.04 lead
- Revised specification document (with revision marks or track changes)
- Updated Traceability Matrix
- Updated Assumption Tracking Log

---

### Step 5: Perform Final QA Review and Issue Specification

**Objective**: Ensure specification is complete, consistent, enforceable, and ready for issuance

**Tasks**:
5.1. **Final QA review**:
- Re-run Guidance Review Checklist to confirm all previous findings are addressed
- Verify Traceability Matrix is complete and all cross-references are correct
- Verify Assumption Tracking Log shows all open **TBD** items have resolution paths or are flagged for issuance with stakeholder notification
- Verify all reviewer comments are resolved or formally deferred (with justification)

5.2. **Cross-document consistency check**:
- Verify terminology, values, and references are consistent across Datasheet, Specification (this document), Guidance, Procedure
- Verify specification clauses align with Specification Requirements R1.1–R3.3
- Verify Guidance Review Checklist items all pass or have documented acceptable deviations

5.3. **Approval sign-off**:
- Civil Lead Engineer (specification author) reviews and approves specification
- QA Reviewer signs off on traceability audit and cross-document consistency check
- Package Manager or Project Engineer provides final approval for issuance

5.4. **Update specification revision status**:
- Update title page and revision history with issue date and revision number (e.g., "Rev 0, [Date], Issued for Construction")
- Update document management system with issued specification

5.5. **Distribution**:
- Distribute specification per project distribution matrix (Owner, Engineer, Contractor, Package Coordinators, DEL-04.01/04.03/04.04 leads)
- Provide specification with Traceability Matrix and Assumption Tracking Log to DEL-04.04 QA/QC lead for test planning

**Verification**:
- Guidance Review Checklist fully passes (or acceptable deviations documented)
- Traceability Matrix is complete and audited
- Assumption Tracking Log shows all **TBD** items have resolution paths or are flagged
- Approval signatures (or digital approvals) are obtained

**Records**:
- Final issued specification document with revision history
- Completed Guidance Review Checklist (final version)
- Final Traceability Matrix
- Final Assumption Tracking Log
- Approval sign-off records

---

### Step 6: Manage Revisions (Post-Issuance)

**Objective**: Control specification revisions to maintain traceability and consistency

**Tasks**:
6.1. **Revision triggers**:
- DEL-04.01 drawing updates (new materials, revised tolerances, added details)
- DEL-04.03 calculation updates (revised geotechnical data, design load changes, material property changes)
- Employer's Requirement clarifications or addenda
- Construction phase changes (contractor RFIs, field condition adaptations)
- Phase 2 input received (OBJ-8 tie-in requirements confirmed)

6.2. **Revision process**:
- Update affected specification clauses
- Update revision history and revision marks (track changes or revision bars)
- Re-run Guidance Review Checklist for affected clauses
- Update Traceability Matrix if new drawing/calculation references are added
- Update Assumption Tracking Log if **ASSUMPTION**/**TBD** items are resolved or new items added

6.3. **Approval and distribution**:
- Obtain Civil Lead and QA Reviewer sign-off on revised clauses
- Issue revised specification per project distribution matrix
- Notify DEL-04.04 team if revisions affect testing requirements or acceptance criteria

**Verification**:
- Revised specification includes updated revision history
- Traceability Matrix reflects new cross-references (if applicable)
- Assumption Tracking Log is current
- Approval sign-offs are obtained

**Records**:
- Revised specification document with revision history and revision marks
- Updated Traceability Matrix (if applicable)
- Updated Assumption Tracking Log (if applicable)
- Approval records for revised specification

---

## Verification

### Verification Checkpoints

| Checkpoint | Verification Method | Acceptance Criteria |
|------------|-------------------|---------------------|
| Step 1 complete | Review Assumption Tracking Log and Traceability Matrix template | Logs updated with specification items; matrix template created |
| Step 2 complete | Review draft specification and Traceability Matrix | All sections per R1.1–R1.5 drafted; matrix populated; inline traceability present |
| Step 3 complete | Review Guidance Review Checklist and coordination sign-offs | Checklist completed; coordination meetings held; package lead sign-offs obtained |
| Step 4 complete | Review coordination meeting minutes and updated matrix | Specification aligned with DEL-04.01/04.03/04.04; matrix updated; assumption log reflects resolutions |
| Step 5 complete | Review approval records and distribution confirmation | Approvals obtained; specification issued; distribution complete |
| Step 6 (revisions) | Review revision history and updated matrix | Revised specification correct; matrix current; approvals obtained |

### Overall Acceptance Criteria
- Specification conforms to all Requirements R1.1–R3.3
- Guidance Review Checklist fully passes (or acceptable deviations documented)
- Traceability Matrix demonstrates complete linkage to DEL-04.01, DEL-04.03, DEL-04.04, standards
- Assumption Tracking Log shows all **TBD** items either resolved or flagged with resolution paths
- Approval sign-offs obtained from Civil Lead and QA Reviewer
- Coordination sign-offs obtained from PKG-03/05/07/08 leads for interface clauses

## Records

### Deliverable Records
1. **Pavement Technical Specification (DEL-04.02)**: Complete specification document with all sections per R1.1–R1.5
2. **Traceability Matrix**: Spreadsheet linking specification clauses to drawings, calculations, test records, standards
3. **Assumption Tracking Log**: Coordinated with DEL-04.01 and DEL-04.03 logs
4. **Guidance Review Checklist (completed)**: Annotated checklist documenting review findings
5. **Reviewer Comment Log**: Comments and resolutions
6. **Coordination Meeting Minutes**: Records with PKG-03/05/07/08 leads and DEL-04.01/04.03/04.04 leads
7. **Approval Records**: Sign-offs confirming final approval

### File Naming Conventions (**TBD** – pending project document management plan)
- Specification document: `DEL-04.02_Pavement_Technical_Specification_R[Rev].pdf` (example: `DEL-04.02_Pavement_Technical_Specification_R0.pdf`)
- Traceability Matrix: `DEL-04.02_Traceability_Matrix.xlsx`
- Assumption Log: `DEL-04.02_Assumption_Log.xlsx` (or coordinated log: `PKG-04_Assumption_Log.xlsx`)
- Guidance Checklist: `DEL-04.02_Guidance_Checklist_[Date].pdf`

### Storage Locations
- **Working files**: `test/execution/PKG-04_Pavement_and_Surfacing/1_Working/DEL-04.02_Pavement_Technical_Specification/`
- **Issued files**: `test/execution/PKG-04_Pavement_and_Surfacing/3_Issued/` (with deliverable ID and revision in file name)
- **Reference files**: `test/execution/PKG-04_Pavement_and_Surfacing/0_References/` (standards, ER excerpts)

## References

### Source Documents
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-04, DEL-04.02, OBJ-8
- **Datasheet (DEL-04.02)**: Attributes, Key Performance Requirements, Conditions, Construction, Assumptions & TBDs, Cross-document Coordination
- **Specification (DEL-04.02)**: Requirements R1.1–R3.3, Verification Methods, Standards
- **Guidance (DEL-04.02)**: Review Checklist, Principles, Considerations, Trade-offs, Coordination Guidance
- **Employer's Requirements Volume 2 Part 1 & 2**: Specification requirements (**location TBD**)

### Related Deliverables
- **DEL-04.01**: Pavement Design Drawing Set (material call-outs and tolerances specified herein)
- **DEL-04.03**: Pavement Design Calculations (material properties and design parameters validated herein)
- **DEL-04.04**: Pavement Installation & Test Records (testing requirements defined herein)
- **PKG-03/05/07/08 deliverables**: Interface coordination
