# Procedure: DEL-16.02 Valve Technical Specification

## Purpose

This procedure defines the process for producing and managing **Valve Technical Specification** within **PKG-16 Valves & Specialty Equipment**.

**Deliverable Purpose:** Defines performance, materials, and workmanship requirements for valves per ER requirements for the Canola Oil Transload Facility.

**Source:** `_CONTEXT.md`

**Deliverable Type:** Specification (Technical/Procurement)
**Responsible Party:** D&B Contractor
**Discipline:** Mechanical

**Scope:** This procedure covers the development of valve technical specifications from requirements gathering through final issue for procurement.

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED
- Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)
- Upstream deliverables and input data to be confirmed prior to commencement

**Source:** `_DEPENDENCIES.md`

**Typical Upstream Inputs (advisory only — not formally tracked):**
- Process design (P&IDs, PFDs, line list) — defines valve services, normal/design conditions
- Valve sizing calculations (DEL-16.03) — provides valve sizes, Cv/Kv, pressure drops, relief capacities
- Valve arrangement drawings (DEL-16.01) — defines valve types, locations, and configurations
- HAZOP study (DEL-27.02) — defines safety-critical valve requirements and fail-safe modes
- Piping specification (DEL-14.02) — provides piping material and flange rating requirements for compatibility
- Design basis documents (DEL-27.01) — provides design criteria and environmental conditions

**Source:** Inputs inferred from specification development requirements; specific coordination TBD

### Reference Materials

**Required References:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials

**Key References (to be obtained):**
- Employer's Requirements (Volume 2 Parts 1–3) — **TBD** — Primary requirements source
- Project Engineering Standards — **TBD** — Project-specific design criteria
- Project Specification Template — **TBD** — Standard format for specifications
- Applicable codes and standards (see Specification.md — Standards section)

**Source:** Reference requirements inferred from deliverable type; `_REFERENCES.md` indicates no references identified yet

**Industry References (for specification development):**
- API publications (API 600, 6D, 526, 527, 598, etc.)
- ISA standards (ISA-75 series)
- ASME standards (B16.34, B16.5, BPVC Section VIII)
- Valve vendor catalogs and technical literature

### Personnel Requirements

**Qualifications:**
- **Lead Specification Engineer:** Mechanical engineer with experience in valve selection and specification for process facilities
- **Technical Reviewer:** Senior mechanical engineer (not the originator), qualified to review valve specifications
- **Discipline Lead:** Professional Engineer (P.Eng.) authorized to approve mechanical specifications

**Source:** Typical personnel requirements for specification development; specific qualifications TBD per project quality procedures

**Competency Requirements:**
- Familiarity with applicable valve standards (API, ASME, ISA)
- Understanding of valve sizing, materials, and testing requirements
- Experience with procurement specifications for EPC projects
- **ASSUMPTION:** Personnel competency per project quality procedures

## Steps

### Step 1: Requirements Gathering

**Action:** Compile all applicable requirements from Employer's Requirements, codes, standards, and design inputs.

**Requirements Sources:**
1. **Employer's Requirements:**
   - Review Volume 2 Parts 1–3 for valve-specific requirements — **TBD**
   - Extract all "shall" requirements related to valves (performance, materials, testing, documentation)
   - Create compliance matrix mapping ER clauses to specification sections

2. **Codes and Standards:**
   - Identify applicable codes per valve type (API 600 for gate valves, API 526 for relief valves, ISA-75 for control valves, etc.)
   - Confirm edition/revision of each standard to be specified
   - Identify any conflicts between standards and establish precedence

3. **Design Inputs:**
   - Obtain valve sizing calculations (DEL-16.03) — valve sizes, Cv/Kv, pressure drops, relief capacities
   - Obtain valve arrangement drawings (DEL-16.01) — valve types and configurations
   - Obtain P&IDs and line list — valve services, normal/design/minimum conditions
   - Obtain HAZOP recommendations (DEL-27.02) — safety-critical valve requirements

4. **Project-Specific Requirements:**
   - Design basis (DEL-27.01) — environmental conditions, seismic, design life
   - Piping specification (DEL-14.02) — material compatibility, flange ratings
   - Instrumentation specification (DEL-20.02) — control valve instrumentation requirements

**Verification:**
- Confirm all valve types and services are identified
- Identify any missing inputs and issue RFI to responsible party
- Obtain approval to proceed from discipline lead

**Source:** Typical requirements gathering process for procurement specifications

### Step 2: Specification Outline Development

**Action:** Develop specification outline using project specification template or industry standard format.

**Recommended Outline (typical procurement specification structure):**

1. **Scope and Applicability**
2. **Reference Documents**
3. **Definitions and Abbreviations**
4. **Performance Requirements**
   - 4.1 General Requirements
   - 4.2 Control Valve Requirements
   - 4.3 Isolation Valve Requirements
   - 4.4 Relief Valve Requirements
   - 4.5 Strainer Requirements
5. **Design Requirements**
   - 5.1 Valve Types and Body Styles
   - 5.2 Pressure-Temperature Ratings
   - 5.3 End Connections
   - 5.4 Trim Design
6. **Materials of Construction**
   - 6.1 Body Materials
   - 6.2 Trim Materials
   - 6.3 Gasket and Packing Materials
   - 6.4 Bolting Materials
   - 6.5 Material Certifications
7. **Actuators and Accessories**
   - 7.1 Actuator Types
   - 7.2 Actuator Sizing
   - 7.3 Positioners and Controllers
   - 7.4 Limit Switches and Position Transmitters
   - 7.5 Solenoid Valves and Air Sets
   - 7.6 Manual Overrides
8. **Manufacturing and Workmanship**
   - 8.1 Manufacturing Process Requirements
   - 8.2 Welding Requirements
   - 8.3 Surface Finish
   - 8.4 Dimensional Tolerances
   - 8.5 Marking and Identification
9. **Testing and Inspection**
   - 9.1 Pressure Testing (Hydrostatic/Pneumatic)
   - 9.2 Seat Leakage Testing
   - 9.3 Relief Valve Set Pressure Testing
   - 9.4 Non-Destructive Examination (if applicable)
   - 9.5 Factory Acceptance Testing (FAT)
   - 9.6 Witness Hold Points
10. **Quality Assurance**
    - 10.1 Quality Management System
    - 10.2 Inspection and Test Plan
    - 10.3 Non-Conformance Reporting
    - 10.4 Traceability Requirements
11. **Documentation and Submittals**
    - 11.1 Vendor Drawing Submittals
    - 11.2 Material Certificates
    - 11.3 Test Certificates
    - 11.4 Operation and Maintenance Manuals
    - 11.5 Spare Parts Lists
12. **Packing, Shipping, and Storage**
13. **Warranty**

**Format Decision:**
- Decide whether to create separate specifications per valve category (control, isolation, relief) or unified specification with subsections — **TBD**
- Obtain approval for chosen format from discipline lead and project document control

**Source:** Typical procurement specification outline; specific format TBD per project template

### Step 3: Draft Preparation

**Action:** Write specification sections per approved outline, incorporating all requirements from Step 1.

**Drafting Guidelines:**
1. **Clarity and Precision:**
   - Use "shall" for mandatory requirements (legally binding)
   - Use "should" for recommended practices (advisory)
   - Use "may" for permissible options (vendor discretion)
   - Avoid ambiguous terms ("as required," "adequate," "suitable")

2. **Consistency:**
   - Use consistent terminology throughout (e.g., always "valve body" not "valve casing")
   - Ensure cross-references are accurate (e.g., "see Section 5.2" points to correct section)
   - Maintain consistency with other project specifications (piping, instrumentation)

3. **Completeness:**
   - Address all requirements from Employer's Requirements (check compliance matrix)
   - Include all valve types within PKG-16 scope (control, isolation, relief, strainers)
   - Specify all necessary testing and documentation requirements

4. **Traceability:**
   - Cite source for each requirement (ER clause, code section, or design calculation)
   - Example: "Valve body material shall be ASTM A351 Grade CF8M per ER Clause 12.3.4"

5. **Format:**
   - Follow project specification template format — **TBD**
   - Use numbered sections and subsections for easy reference
   - Include tables for valve schedules, material specifications, test requirements

**Key Sections to Develop:**

**Performance Requirements Section:**
- Operating conditions (pressure, temperature, flow) per valve datasheet
- Control valve rangeability and accuracy per ISA-75 standards
- Leakage class per API 598 or ISO 5208
- Fail-safe modes per HAZOP recommendations

**Materials Section:**
- Body materials: Stainless steel (316SS preferred) for product contact; carbon steel acceptable for utilities
- Trim materials: Stainless steel or hardened stainless for erosion resistance
- Gasket/seal materials: PTFE, RTFE, EPDM (food-grade)
- Material certificates (MTRs) required for pressure-retaining components

**Testing Section:**
- Pressure testing per API 598 (shell test, seat test)
- Relief valve set pressure testing per API 527 (tolerance ±3 psi or ±2%)
- Control valve stroking test (full stroke, response time verification)
- FAT requirements and witness hold points

**Source:** Specification drafting guidelines typical for procurement specifications

### Step 4: Self-Check

**Action:** Originator performs self-check of specification for completeness, accuracy, and compliance.

**Self-Check Items (see also Specification.md — Verification section):**
- **Completeness:** All outline sections complete; no "TBD" placeholders in final draft
- **Accuracy:** Valve sizes, ratings, and materials consistent with design calculations and datasheets
- **Consistency:** Requirements consistent with piping specification, instrumentation specification
- **Compliance:** All Employer's Requirements addressed (check compliance matrix 100% complete)
- **Clarity:** Requirements clearly stated; no ambiguous language
- **Format:** Specification complies with project template; proper section numbering and cross-references

**Documentation:**
- Complete self-check checklist (if project provides standard form) — **TBD**
- Correct any errors or omissions identified
- Prepare specification for technical review

**Source:** Typical self-check process for specifications

### Step 5: Technical Review

**Action:** Discipline lead or senior engineer performs technical review of specification.

**Technical Review Items:**
- **Technical Correctness:** Valve performance requirements appropriate for service conditions
- **Code Compliance:** Requirements comply with applicable codes (API, ASME, ISA, CSA B51)
- **Materials Appropriateness:** Specified materials suitable for CSD canola oil service and coastal environment
- **Testing Adequacy:** Testing requirements adequate to verify performance and quality
- **Procurement Suitability:** Specification provides sufficient detail for competitive bidding; not overly prescriptive
- **Constructability:** Requirements can be met by qualified valve vendors; no obsolete or unavailable models specified

**Reviewer Markups:**
- Reviewer annotates specification with comments using track changes or markup tools
- Originator addresses reviewer comments and updates specification
- Reviewer verifies comment resolution and approves specification for IDC

**Source:** Typical technical review process for specifications

### Step 6: Interdisciplinary Check (IDC)

**Action:** Coordinate specification with other disciplines to verify interfaces and consistency.

**Disciplines to Coordinate:**
1. **Process (PKG-10, PKG-11, PKG-12):**
   - Verify valve performance requirements match process design (flow rates, pressures, temperatures)
   - Confirm fail-safe modes align with process safety philosophy

2. **Piping (PKG-14):**
   - Verify valve materials compatible with piping materials (DEL-14.02)
   - Verify flange ratings match piping specification
   - Confirm valve weights and dimensions acceptable per piping stress analysis

3. **Instrumentation (PKG-20):**
   - Verify control valve instrumentation requirements (positioners, transmitters, limit switches) consistent with instrumentation specification (DEL-20.02)
   - Verify signal types and communication protocols (4–20 mA, HART, Foundation Fieldbus)

4. **Electrical (PKG-17):**
   - Verify electric actuator specifications (voltage, enclosure rating) consistent with electrical specification (DEL-17.02)
   - Verify hazardous area classification ratings for actuators and accessories

5. **Control Systems (PKG-19):**
   - Verify control valve fail-safe modes consistent with control philosophy
   - Verify communication protocols compatible with DCS/PLC system

6. **Safety / HAZOP (DEL-27.02):**
   - Verify safety-critical valve requirements (ESDs, relief valves) address HAZOP recommendations

**IDC Process:**
- Distribute specification for IDC via project document management system — **TBD**
- Allow review period (typically 10–15 working days) — **TBD**
- Collect IDC comments via project comment management system — **TBD**
- Categorize comments per project convention (Category A = must resolve, Category B = consider, Category C = noted)
- Resolve Category A comments; respond to Category B/C comments
- Update specification and reissue if significant changes result from IDC

**Source:** Typical IDC process for multi-discipline projects

### Step 7: Employer Review (if required)

**Action:** Submit specification to Employer for review and comment per contract requirements.

**Submittal Stages (typical):**
- **30% Submittal:** Preliminary specification for Employer review — **TBD**
- **60% Submittal:** Revised specification incorporating Employer comments — **TBD**
- **90% Submittal:** Near-final specification for final Employer review — **TBD**
- **IFP (Issued for Procurement):** Final specification approved for vendor bidding — **TBD**

**Employer Review Process:**
- Prepare submittal package (specification + compliance matrix + cover transmittal)
- Submit via project document management system — **TBD**
- Allow Employer review period per contract (typically 15–30 days) — **TBD**
- Receive Employer comments (typically categorized: Accept, Accept with Comments, Revise and Resubmit)
- Address Employer comments and resubmit revised specification

**Compliance Matrix:**
- Maintain compliance matrix mapping specification sections to Employer's Requirements clauses
- Update matrix with each revision to show how ER requirements are addressed
- Submit compliance matrix with specification for Employer verification

**Source:** Typical Employer review process for EPC contracts; specific requirements TBD per contract

### Step 8: Approval and Issue

**Action:** Obtain approval signatures and issue specification per project procedures.

**Approval Signatories:**
- **Originator:** Engineer who prepared the specification
- **Technical Reviewer:** Independent reviewer who performed technical review
- **Discipline Lead:** P.Eng. authorized to approve mechanical specifications
- **Employer (if required):** Employer representative approval for IFP issue

**Specification Issue:**
- Assign document number per project specification numbering system — **TBD**
- Assign revision code (Rev 0 or A for initial issue; increment per project convention) — **TBD**
- Update document header/footer with approval signatures and issue date
- Issue specification via project document management system — **TBD**
- Update specification register/index

**Issue Purpose Codes (typical):**
- **IFR (Issued for Review):** Specification issued for Employer or stakeholder review (30%, 60%, 90% submittals)
- **IFP (Issued for Procurement):** Specification approved for vendor bidding
- **IFC (Issued for Construction):** Specification approved for construction reference (if different from IFP)

**Distribution:**
- Employer — **TBD** (if contractually required)
- Procurement department — for vendor bid package preparation
- Project document control — for document register and archive
- Affected disciplines — for reference and coordination

**Source:** Typical specification issue process for EPC projects

### Step 9: Procurement Support

**Action:** Support procurement activities during vendor bidding and evaluation.

**Pre-Bid Activities:**
- Prepare bid package (specification + valve datasheet package from DEL-16.04)
- Conduct pre-bid meeting with vendors (if required) — **TBD**
- Respond to vendor pre-bid queries and issue addenda if specification clarifications required

**Bid Evaluation:**
- Review vendor technical proposals for compliance with specification
- Evaluate vendor-proposed alternates ("or equal" submissions)
- Prepare technical bid evaluation report with recommendations
- Support procurement in vendor selection

**Post-Award Activities:**
- Conduct kick-off meeting with selected vendor
- Review and approve vendor drawings and documentation per specification submittal requirements
- Witness factory acceptance tests (FATs) per specification hold points
- Support resolution of any specification interpretation issues during fabrication

**Source:** Typical procurement support activities for valve specifications

### Step 10: Specification Maintenance

**Action:** Maintain specification throughout project lifecycle; issue revisions as needed.

**Revision Triggers:**
- Design changes affecting valve requirements (process changes, system modifications)
- Employer-requested changes
- Vendor-requested deviations or alternates (if approved)
- Lessons learned from commissioning or early operation
- Code or standard updates (if contractually required to update)

**Revision Process:**
- Prepare revised specification with changes clearly marked (revision clouds, revision bars)
- Document reason for revision in revision history table
- Obtain approvals per original approval process (originator, reviewer, discipline lead, Employer if required)
- Reissue with incremented revision code
- Notify procurement and affected vendors of changes

**Configuration Control:**
- Specification supersedes previous revision upon issue
- Prior revision archived but retained for record
- Specification register maintains current and superseded revision status
- Vendor contracts reference specific specification revision (avoid "latest" references to prevent ambiguity)

**Source:** Specification maintenance typical for EPC projects

## Verification

**Verification activities for Specification deliverables (see also Specification.md — Verification section):**

### Self-Check (Step 4)
- Originator reviews for completeness, accuracy, consistency, compliance, clarity, and format
- Sign-off: Originator signature on document approval page — **TBD**

### Technical Review (Step 5)
- Senior engineer or discipline lead reviews technical correctness, code compliance, materials appropriateness, testing adequacy
- Sign-off: Technical reviewer signature on document approval page — **TBD**

### Interdisciplinary Check (Step 6)
- Multi-discipline coordination to verify interfaces and consistency with other specifications
- Sign-off: IDC complete when Category A comments resolved and specification updated

### Employer Review (Step 7, if required)
- Employer reviews specification for compliance with contract requirements
- Sign-off: Employer approval notation (Accept, Accept with Comments, or Revise and Resubmit)

### Approval (Step 8)
- Discipline lead (P.Eng.) approves specification for issue
- Sign-off: Discipline lead signature and P.Eng. seal on document approval page — **TBD**

**Acceptance Criteria:**
- All verification steps completed per project quality procedures
- Zero unresolved Category A comments from IDC and Employer review
- Compliance matrix complete with 100% coverage of Employer's Requirements
- Approval signatures obtained per project authority matrix — **TBD**
- Specification complies with project specification template and format requirements

**Source:** Verification activities typical for procurement specifications

## Records

**Documentation outputs:**

### Primary Deliverables (per _CONTEXT.md)
- **Control Valve Specification:** Technical requirements for control valves
- **Isolation Valve Specification:** Technical requirements for isolation valves
- **Relief Valve Specification:** Technical requirements for relief valves

**Format:** Single document (unified specification) or multiple documents (separate specifications) — **TBD**

### Supporting Records
- **Compliance Matrix:** Maps specification requirements to Employer's Requirements and codes/standards
- **IDC Comment/Response Log:** Record of interdisciplinary comments and resolutions
- **Employer Comment/Response Log:** Record of Employer review comments and resolutions (if applicable)
- **Specification Basis of Design Note:** Narrative explaining key specification decisions, trade-offs, and assumptions
- **Technical Review Markup Set:** Record of technical reviewer comments and resolutions
- **Revision History Log:** Record of all specification revisions, reasons, and approval dates

**Record Management:**

**During Development (Working Status):**
- Working files maintained in `1_Working/` folder in deliverable directory
- Draft specifications, compliance matrix, comment logs
- **Source:** Folder structure per README.md Section "What lives where"

**During Review (CHECKING Status):**
- Review package placed in `2_Checking/To/` folder
- Include cover transmittal, specification, compliance matrix
- Track Employer review comments and responses
- **Source:** Recommended convention per README.md Section 6 (Review and issue)

**Upon Issue (ISSUED Status):**
- Issued specifications placed in `3_Issued/` folder
- Include final specification (PDF), compliance matrix, approval records
- Archive superseded revisions (older issues)
- Update project specification register
- **Source:** Recommended convention per README.md Section 6 (Review and issue)

**Retention Requirements:**
- Retention period: **TBD** — **ASSUMPTION:** Project life + 25 years typical for procurement specifications
- Archival format: **TBD** — **ASSUMPTION:** PDF/A for long-term preservation
- Backup and disaster recovery: **TBD** — Per project IT/document management procedures

**Electronic Document Management:**
- **ASSUMPTION:** Electronic records managed in project document management system (e.g., Aconex, ProjectWise, SharePoint, or equivalent)
- Document control procedures: **TBD** — Per project document control plan
- Access permissions: **TBD** — Per project data security requirements

**Source:** Record management practices typical for EPC projects; specific requirements TBD per project procedures
