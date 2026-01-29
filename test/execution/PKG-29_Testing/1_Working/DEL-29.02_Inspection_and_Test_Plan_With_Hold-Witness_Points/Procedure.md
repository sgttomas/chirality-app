# Procedure: DEL-29.02 Inspection and Test Plan With Hold/Witness Points

## Purpose

This procedure defines the process for developing, reviewing, approving, and maintaining the **Inspection and Test Plan With Hold/Witness Points** within **PKG-29 Testing**.

**Deliverable Purpose:** Defines the planned approach and controls for inspection and test plan with hold/witness points to meet ER requirements. **Source:** Decomposition line 647

**Deliverable Type:** Plan
**Responsible Party:** D&B Contractor (QA/QC)

## Prerequisites

### Dependencies

**Dependency Tracking:** See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Upstream Deliverable Requirements:**

ITP development requires input from:
- **Design deliverables (all disciplines):** Drawings, specifications, calculations provide basis for identifying inspection activities and acceptance criteria
- **DEL-00.03: Quality Management Plan** **ASSUMPTION** — Defines ITP requirements, formats, and approval process
- **Project execution plan / schedule:** Provides timing for ITP submission and milestones
- **Employer's Requirements:** **location TBD** — Specifies hold/witness point requirements and inspection preferences

**Note:** Initial ITP can be developed at preliminary level and progressively detailed as design matures.

### Reference Materials

**Required Inputs:**

- Employer's Requirements (Volume 2 Parts 1-3) **location TBD** — Hold/witness requirements, acceptance criteria
- Project Quality Management Plan **location TBD** — ITP format, approval process
- Design drawings and specifications (all disciplines, as available)
- Applicable codes and standards (see Specification.md for list)
- Contract documents — Quality and inspection requirements
- Sub-contractor and vendor quality plans (as they become available)

**Source:** Typical ITP development inputs **ASSUMPTION**

### Personnel Requirements

**ITP Development Team:**
- **Lead:** QA/QC Manager or designated ITP Coordinator
- **Contributors:** Discipline engineers (Civil, Structural, Marine, Mechanical, Electrical, I&C), Construction Manager, Procurement Manager
- **Reviewers:** Engineering Manager, Construction Manager, HSE Manager, Employer representative
- **Approver:** D&B Contractor Project Manager or QA/QC Manager (per project authority matrix)

**Qualifications:**
- ITP lead should have EPC project quality management experience and familiarity with inspection standards
- Contributors should have competency in their respective disciplines
- **TBD:** Specific qualification requirements per project Quality Management Plan

### Tools and Resources

- ITP template or format (if available from project, Employer, or D&B Contractor standards)
- Project document management system for ITP storage and revision control
- Access to design documentation and codes/standards
- Spreadsheet or database tool for ITP matrix development (Excel, Access, or project-specific tool)

**TBD:** Specific ITP software tools or templates

## Steps

### Step 1: Define ITP Scope and Structure

**Objective:** Establish the scope, organization, and format for the ITP.

**Activities:**

1.1. Review contract requirements for ITP submittal timing and format

1.2. Review Employer's Requirements **location TBD** for hold/witness point requirements and preferences

1.3. Define ITP organization structure:
   - Single master ITP vs. multiple discipline/package ITPs
   - Typical for large projects: Master ITP index + discipline sub-ITPs

1.4. Define ITP matrix column structure (see Datasheet.md for typical columns)

1.5. Establish hold/witness/review designation criteria (see Guidance.md for examples)

1.6. Identify project phases to be covered (design, procurement, fabrication, construction, testing, commissioning)

**Outputs:**
- ITP scope definition and structure
- ITP template or format

**TBD:** Confirmation of ITP format with Employer

### Step 2: Identify Inspection Activities

**Objective:** Comprehensively identify all inspection and testing activities across the project.

**Activities:**

2.1. **Review design documentation by discipline:**
   - Civil: Earthworks, drainage, concrete structures, paving
   - Structural: Steel fabrication/erection, welding, fireproofing
   - Marine: Marine structures, fenders, mooring, loading arms
   - Mechanical: Tanks, piping, equipment, pressure testing
   - Electrical: Equipment installation, cable, grounding, testing
   - I&C: Instrument installation, calibration, loop testing

2.2. **Identify code-mandated inspections:**
   - ASME B31.3: Piping examination, pressure testing
   - API 650: Tank welding examination, hydrostatic testing
   - AWS D1.1: Welding inspection, NDT
   - ASME Section V: NDT procedures
   - CSA/NFPA: Electrical inspections
   - IEC: I&C loop checks
   - **TBD:** Other applicable code requirements

2.3. **Identify regulatory and third-party inspections:**
   - Building official inspections (structural, life safety)
   - Fire marshal inspections (fire protection systems)
   - Transport Canada (if applicable for regulated commodities)
   - Insurance surveyor inspections
   - Environmental authority inspections (stormwater, discharge permits)
   - **TBD:** Specific regulatory requirements as identified

2.4. **Identify vendor/sub-contractor inspections:**
   - Factory Acceptance Tests (FAT) — major equipment
   - Shop fabrication inspections — structural steel, piping spools
   - Vendor quality documentation — material certifications, test reports
   - **TBD:** Vendor inspection requirements per procurement documents

2.5. **Review project deliverables list (Decomposition Section 5) to ensure all packages are covered**

**Outputs:**
- Comprehensive list of inspection activities by discipline, phase, and package
- Typical output: 100s to 1000s of inspection activities for project of this scope **ASSUMPTION**

### Step 3: Assign Hold/Witness Designations

**Objective:** Designate each inspection activity as Hold (H), Witness (W), Review (R), or Contractor-only.

**Activities:**

3.1. Apply hold point criteria (see Guidance.md Principles):
   - Code-mandated inspections (pressure tests, critical welding)
   - Irreversible activities (concrete pours, backfill, tank bottom welding)
   - High-risk or high-consequence activities
   - Contract-specified hold points

3.2. Apply witness point criteria:
   - Important inspections where Employer wants observation option
   - First-article or qualification inspections
   - Activities where Contractor QC is primary but Employer wants oversight option

3.3. Apply review point criteria (if used):
   - Document reviews (calculations, vendor submittals, test reports)
   - Activities not requiring physical presence

3.4. Remaining activities: Contractor QC verification only

3.5. Coordinate hold/witness assignments with Employer during ITP development to achieve agreement before finalizing

**Outputs:**
- Hold/witness designations for all inspection activities
- Agreement record with Employer on hold/witness points

**TBD:** Employer preferences and negotiation outcomes

### Step 4: Define Acceptance Criteria and Documentation

**Objective:** Specify acceptance criteria and required documentation for each inspection.

**Activities:**

4.1. For each inspection activity, define acceptance criteria:
   - Reference to applicable specification clause or drawing note
   - Reference to code section (e.g., "API 650 Section 8.1.2")
   - Quantitative criteria (dimensional tolerances, test pressures, insulation resistance values)
   - Qualitative criteria ("no visible defects," "smooth finish")

4.2. Specify required documentation for each inspection:
   - Test reports (hydrostatic test, electrical test, calibration)
   - NDT reports (RT, UT, MT, PT)
   - Material certifications (mill certs, concrete test reports)
   - Photographs (before/during/after as applicable)
   - As-built mark-ups (if dimensional verification)

4.3. Specify notification requirements for hold/witness points:
   - Advance notice period (48 hrs, 72 hrs, 1 week — depends on activity)
   - Notification method (email, phone, online system)
   - Contact information for Employer representative

4.4. Include status tracking fields:
   - Date inspection performed
   - Inspector name
   - Employer witness name (if attended)
   - Result (pass/fail)
   - NCR number (if failed)

**Outputs:**
- Complete ITP matrix with all required information fields populated

### Step 5: Develop Inspection Matrix Summary

**Objective:** Create high-level summary document for communication and planning.

**Activities:**

5.1. Summarize ITP content by discipline or phase (see Guidance.md Example)

5.2. Calculate totals and percentages:
   - Total inspections by discipline
   - Count of hold/witness/contractor inspections
   - Percentage requiring Employer involvement

5.3. Develop visual summaries (bar charts, pie charts) if desired for presentation to Employer

5.4. Use inspection matrix for early coordination meetings with Employer to discuss hold/witness point philosophy

**Outputs:**
- Inspection matrix summary document
- Presentation materials (if needed for Employer meetings)

### Step 6: Conduct Internal Review

**Objective:** Verify ITP completeness and adequacy through multi-discipline review.

**Activities:**

6.1. Distribute draft ITP for review to:
   - Discipline engineers: Verify coverage and acceptance criteria
   - Construction Manager: Verify practicality and sequence
   - QA/QC personnel: Verify alignment with quality plan
   - HSE Manager: Verify safety considerations
   - Procurement Manager: Verify vendor/sub-contractor requirements

6.2. Conduct ITP review meeting to discuss comments and issues

6.3. Consolidate comments and revise ITP accordingly

6.4. Obtain internal sign-offs or concurrence records

**Outputs:**
- Reviewed and revised ITP
- Internal review comment resolution record

### Step 7: Submit to Employer for Review

**Objective:** Obtain Employer review and acceptance of ITP.

**Activities:**

7.1. Prepare ITP submittal package:
   - Transmittal letter
   - ITP matrix document (master and/or discipline sub-ITPs)
   - Inspection matrix summary
   - Hold/witness notification and release procedures
   - Sample inspection forms or checklists

7.2. Submit ITP to Employer per contract document submittal procedures

7.3. Schedule ITP review meeting with Employer (recommended for initial ITP submission)

7.4. Discuss hold/witness point designations, notification requirements, and acceptance criteria

7.5. Receive Employer comments

7.6. Address comments:
   - Incorporate accepted comments
   - Discuss and negotiate disputed items
   - Document agreements and resolutions

7.7. Resubmit revised ITP if necessary

7.8. Obtain Employer formal acceptance (approval stamp, letter, or per contract procedures)

**Outputs:**
- Employer-accepted ITP
- Comment resolution record
- Acceptance documentation

**TBD:** Employer review and acceptance process per contract

### Step 8: Issue and Distribute ITP

**Objective:** Issue ITP as a controlled document and distribute to all required parties.

**Activities:**

8.1. Issue ITP as a controlled document in project document management system

8.2. Assign document number per project numbering system

8.3. Apply revision control (initial issue typically "Rev 0" or "Rev A")

8.4. Distribute ITP to:
   - Project team (Engineering, Construction, QA/QC, HSE)
   - Sub-contractors and vendors (relevant portions)
   - Employer representative
   - Third-party inspectors (insurance, regulatory)

8.5. Conduct briefing or training session on ITP use, hold/witness procedures, and documentation requirements

8.6. Ensure test procedures (DEL-29.01) and test record forms (DEL-29.03 etc.) are updated to reference ITP activity numbers

**Outputs:**
- Issued ITP (controlled document)
- Distribution record
- ITP briefing/training record

### Step 9: Maintain and Update ITP

**Objective:** Keep ITP current as design and project scope evolve.

**Activities:**

9.1. Monitor design changes and scope additions that affect ITP:
   - Design change notices
   - Equipment additions or substitutions
   - Scope clarifications

9.2. Update ITP to reflect changes:
   - Add new inspection activities
   - Revise acceptance criteria if specifications change
   - Update references to revised drawings

9.3. Coordinate ITP updates with Employer:
   - Significant changes (new hold points, scope additions): Formal submittal for Employer review
   - Minor changes (drawing reference updates, clarifications): May be incorporated and noted in next revision

9.4. Issue revised ITP per revision control procedures:
   - Increment revision number
   - Mark changes (revision clouds, change log)
   - Distribute to all holders
   - Retrieve superseded revisions or mark as obsolete

9.5. Track ITP status during construction:
   - Update status fields as inspections are performed
   - Track open hold points and pending releases
   - Use ITP as source for inspection completion reporting

**Outputs:**
- Updated ITP revisions as needed throughout project
- ITP status reports (open hold points, inspection completion %)

**TBD:** ITP update and revision frequency per project requirements

## Verification

### Verification Activities

**V-1: Completeness Check**
- Verify ITP covers all equipment and systems identified in design deliverables
- Verify all code-mandated inspections are included
- Verify all Employer-specified hold/witness points are included
- Cross-check ITP against project deliverables list (36 packages, ~210 deliverables)

**Responsibility:** QA/QC Manager or ITP Lead

**V-2: Multi-Discipline Technical Review**
- Verify inspection activities and acceptance criteria are technically correct
- Verify hold/witness designations are appropriate for risk and requirements
- Verify notification periods are adequate and practical

**Responsibility:** Discipline leads, Construction Manager, HSE Manager

**V-3: Employer Review and Acceptance**
- Submit ITP to Employer per contract requirements
- Address Employer comments and negotiate hold/witness points as needed
- Obtain Employer formal acceptance

**Responsibility:** QA/QC Manager, Project Manager

**V-4: Integration Check**
- Verify ITP activity numbers are referenced in test procedures (DEL-29.01)
- Verify test record forms include ITP activity number field for traceability
- Verify sub-contractor quality plans align with ITP requirements

**Responsibility:** QA/QC Manager

### Acceptance Criteria

**ITP is acceptable when:**

**AC-1:** ITP covers all required inspection scope (100% of code-required and Employer-specified inspections identified)

**AC-2:** ITP includes all required information (item, activity, criteria, hold/witness, notification, documentation, status tracking)

**AC-3:** Hold/witness designations are agreed with Employer

**AC-4:** Internal multi-discipline reviews are complete and comments addressed

**AC-5:** Employer has reviewed and formally accepted the ITP

**AC-6:** ITP is issued as a controlled document and distributed

**Source:** Specification.md Sections AC-1, AC-2, AC-3

### Sign-off Requirements

| Role | Responsibility | Signature/Date |
|------|---------------|----------------|
| ITP Lead / QA/QC Manager | Development | **TBD** |
| Discipline Engineers | Technical Review | **TBD** |
| Construction Manager | Constructability Review | **TBD** |
| HSE Manager | Safety Review | **TBD** |
| Project Manager | Approval | **TBD** |
| Employer Representative | Acceptance | **TBD** |

**Note:** Specific sign-off requirements per project authority matrix and contract **location TBD**

## Records

### Documentation Outputs

**Primary Deliverables (per _CONTEXT.md):**

1. **Inspection and Test Plan (ITP) with Hold/Witness Points**
   - Master ITP document or discipline sub-ITP documents
   - Typically spreadsheet format (Excel) with matrix structure
   - May be 100s to 1000s of line items depending on project size
   - **TBD:** Specific format per Employer requirements or project standards

2. **Inspection Matrix**
   - Summary document showing inspection categories, counts, and hold/witness distribution
   - May include charts or visualizations
   - Typically shorter document (few pages) for communication and planning

**Source:** _CONTEXT.md Anticipated Artifacts, Decomposition line 647

### Supporting Documentation

**ITP Development Records:**
- ITP development worksheets and inputs
- Internal review comments and resolution records
- Employer submittal and comment resolution records
- Employer acceptance documentation
- ITP revision logs and change tracking

**ITP Usage Records (during construction):**
- Notification records (hold/witness point notifications to Employer)
- Release records (Employer releases of hold points)
- Inspection status reports (completion tracking)
- Non-conformance reports (failed inspections)
- Actual inspection records — filed per DEL-29.03 through DEL-29.08

**Source:** Typical EPC ITP documentation **ASSUMPTION**

### Record Management

**Filing Location:**
- Working drafts: `1_Working/DEL-29.02_Inspection_and_Test_Plan_With_Hold-Witness_Points/` (current location)
- ITP under Employer review: `2_Checking/To/` (when submitted for Employer review)
- Accepted ITP: `3_Issued/` (upon Employer acceptance)
- Project document management system (per project document control procedures)

**Retention Requirements:**
- ITP is permanent project record retained for facility life **ASSUMPTION**
- Retention schedule per project records retention plan **location TBD**

**Electronic Records:**
- Native format (Excel, database) for ITP matrix to allow updates and status tracking
- PDF format for issued/archived copies
- Version control per document management system

**Updates and Revisions:**
- ITP is a "living document" updated throughout project lifecycle
- Revisions tracked and distributed per document control procedures
- Status fields updated as inspections are performed and completed

**Deliverable Status Tracking:**

**Current Status:** See `_STATUS.md` in this deliverable folder

**Lifecycle States:**
- OPEN: Deliverable scope defined, not yet started
- INITIALIZED: Initial documents generated
- IN_PROGRESS: ITP development underway
- CHECKING: ITP submitted for Employer review
- ISSUED: ITP accepted by Employer and released for use

**Status Updates:** Per project working-items lifecycle

---

**Document Control:**
- This Procedure.md document describes the process for developing the ITP.
- The ITP deliverable itself (matrix and summary) will be developed following this process.
- For questions on ITP development, consult D&B Contractor QA/QC Manager.

---

## Cross-Document Linkage

| Document | Key Sections | Relationship |
|----------|--------------|--------------|
| Datasheet.md | §Attributes, §Construction, §References | Provides ITP structure and column definitions used in Steps 1, 4 |
| Specification.md | §Requirements (FR, PR, IR, QR), §Verification | Defines requirements this Procedure implements |
| Guidance.md | §Principles, §Considerations, §Trade-offs, §Examples | Provides rationale and examples for procedure steps |

**Procedure Step-to-Specification Traceability:**
| Procedure Step | Specification Section(s) | Verification |
|---------------|-------------------------|--------------|
| Step 1 (Define Scope/Structure) | §Scope, FR-2 (Designations) | V-1 |
| Step 2 (Identify Activities) | FR-1 (Comprehensive Coverage) | V-1 |
| Step 3 (Assign Designations) | FR-2 (Hold/Witness Designations) | V-2 |
| Step 4 (Define Criteria) | FR-3 (Acceptance Criteria), FR-4/FR-5 | V-2 |
| Step 5 (Inspection Matrix) | §Documentation (Secondary Deliverable) | V-1 |
| Step 6 (Internal Review) | QR-1, VM-2 | V-2 |
| Step 7 (Employer Review) | QR-1, VM-3 | V-3 |
| Step 8 (Issue/Distribute) | QR-2, AC-3 | AC-6 |
| Step 9 (Maintain/Update) | QR-2, PR-1 | V-4 |

**Procedure Step-to-Guidance Traceability:**
| Procedure Step | Guidance Section(s) |
|---------------|---------------------|
| Step 1 | §Trade-offs (Single vs. Multiple ITPs), §Examples (Structure) |
| Step 2 | §Considerations Item 1 (Scope), Item 2 (Code Requirements) |
| Step 3 | §Principles (Hold vs. Witness Philosophy), §Examples (Selection) |
| Step 4 | §Examples (ITP Matrix Entry), §Considerations Item 6 (Subcontractors) |
| Step 5 | §Examples (Inspection Matrix Summary) |
| Step 7 | §Considerations Item 3 (Employer Preferences) |
| Step 9 | §Trade-offs (Progressive Development) |
