# Procedure: DEL-24.03 Security System Data Sheet Package

## Purpose

This procedure defines the process for **assembling and submitting** the **Security System Data Sheet Package** within **PKG-24 Security Systems** for the Canola Oil Transload Facility.

**Deliverable objective:** Defines and substantiates security system in accordance with ER requirements by providing equipment datasheets demonstrating compliance with DEL-24.02 (Technical Specification).

*Source: `_CONTEXT.md`; Decomposition Section 5 — PKG-24 (line 568)*

**Deliverable type:** Data Sheet (Equipment Submittal Package)
**Responsible party:** D&B Contractor
**Discipline:** Specialty (Security Systems)

**Procedure scope:** This procedure covers the workflow from equipment selection through submittal approval, including datasheet compilation, compliance verification, submittal preparation, review, and resubmittal (if required).

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

*Source: `_DEPENDENCIES.md`*

**Upstream deliverables required:**
- **DEL-24.01** — Security System Design Drawing Set (equipment locations, types, quantities, tag numbers)
- **DEL-24.02** — Security System Technical Specification (equipment requirements basis)
- **TBD** — Approved procurement budget and schedule

**Information required:**
- Equipment quantities and locations from DEL-24.01 design drawings
- Performance requirements from DEL-24.02 specification
- Terminal integration requirements per DEC-05 **TBD** — from Employer/Terminal IT
- Approved manufacturers list (if specified in DEL-24.02) **TBD**

*Source: DEL-24.01 and DEL-24.02 as design and specification basis; DEC-05*

### Reference Materials

**Required references:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials

**Expected reference materials:**
- DEL-24.01 (Security System Design Drawing Set) — design basis
- DEL-24.02 (Security System Technical Specification) — specification basis
- Employer's Requirements Volume 2 **TBD** — equipment standards
- **TBD** — DP World Fraser Surrey Terminal equipment standards and approved manufacturers
- **TBD** — Project submittal procedures and templates

*Source: DEL-24.01, DEL-24.02; `_REFERENCES.md`*

### Personnel Requirements

**Qualifications:**
- **Procurement specialist:** Experience with security systems equipment procurement and submittals
- **Technical reviewer:** Security systems specialist to verify equipment compliance
- **Submittal coordinator:** Responsibility for submittal compilation, organization, and transmittal

**Competency requirements:**
- Understanding of security system equipment (CCTV, access control, network infrastructure)
- Ability to read and interpret equipment datasheets and specifications
- Knowledge of applicable certifications and standards (UL/CSA, IP/IK, ONVIF, OSDP)
- Familiarity with submittal procedures and document control

*Source: Standard equipment submittal competency requirements*

### Tools and Resources

**Software and tools:**
- **TBD** — PDF compilation software (Adobe Acrobat, Bluebeam) for package assembly
- **TBD** — Spreadsheet software (Excel) for compliance matrices and equipment schedules
- **TBD** — Project document management system for submittal transmittal and tracking

**Manufacturer resources:**
- Access to manufacturer websites for current datasheets and literature
- Manufacturer technical support contacts for specification clarifications
- Manufacturer certification and testing documentation

## Steps

### Step 1: Equipment Selection and Sourcing

**Objective:** Select equipment meeting DEL-24.02 specification and DEL-24.01 design requirements.

**Activities:**
1.1. Review DEL-24.01 design drawings
   - Extract equipment list with tag numbers, locations, quantities
   - Identify equipment types (camera models, reader types, controller architecture, etc.)
   - Understand mounting methods and installation constraints

1.2. Review DEL-24.02 technical specification
   - Identify all equipment performance requirements
   - Note approved manufacturers list (if specified) **TBD**
   - Understand environmental, certification, and integration requirements
   - Review submittal requirements (what must be included in datasheets)

1.3. Research and evaluate equipment options
   - Identify manufacturers and models meeting specifications
   - Obtain preliminary datasheets and pricing
   - Verify equipment availability and lead times
   - Consider Terminal integration requirements per DEC-05 **TBD**

1.4. Select equipment for submittal
   - Choose equipment meeting or exceeding specifications
   - Prioritize reliability, proven performance, manufacturer support
   - Verify cost and schedule compatibility
   - Coordinate with procurement team on pricing and availability

**Outputs:**
- Preliminary equipment list with selected manufacturers and models
- Preliminary datasheets for review

**Verification:** Internal technical review of preliminary selections before formal submittal

*Source: DEL-24.01, DEL-24.02 as basis; standard equipment selection process*

---

### Step 2: Datasheet and Documentation Collection

**Objective:** Collect all required datasheets and supporting documentation.

**Activities:**
2.1. Obtain current manufacturer datasheets
   - Download current literature from manufacturer websites
   - Verify datasheets are current (not obsolete or superseded models)
   - Collect datasheets for all equipment in equipment list

2.2. Collect certification documentation
   - UL/CSA listings and certificates
   - IP/IK rating test reports or certifications
   - ONVIF certifications for IP cameras
   - OSDP certifications for access control readers (if required)
   - FCC compliance for RF devices
   - Hazardous area certifications (if required) **TBD**

2.3. Collect integration documentation (for Terminal integration per DEC-05)
   - Protocol specifications and API documentation
   - Compatibility statements or test results
   - Configuration guides for integration
   - Manufacturer support documentation

2.4. Collect installation and warranty documentation
   - Installation instructions (summary or reference to full manual)
   - Warranty terms and conditions
   - Manufacturer support contact information

**Outputs:**
- Complete set of datasheets and supporting documentation for all equipment

**Verification:** Check that all required documentation collected per DEL-24.02 submittal requirements

*Source: Specification.md — Submittal content requirements*

---

### Step 3: Compliance Verification and Matrix Development

**Objective:** Verify equipment compliance with DEL-24.02 and prepare compliance matrices.

**Activities:**
3.1. Create equipment schedule
   - List all equipment with tag numbers (from DEL-24.01), quantities, locations
   - Include manufacturer, model number for each equipment item
   - Organize by category (CCTV, access control, network, power/UPS, accessories)

3.2. Develop compliance matrices
   - For each major equipment category, create compliance matrix
   - List each requirement from DEL-24.02 specification
   - Compare equipment specification to requirement
   - Indicate compliance status (meets, exceeds, or requires justification)
   - Add comments explaining how equipment meets requirement or justifying deviations

3.3. Verify compliance for all critical requirements
   - Performance specifications (resolution, capacity, speed)
   - Environmental ratings (IP, IK, operating temperature)
   - Certifications and approvals
   - Integration compatibility (ONVIF, OSDP, Terminal systems)
   - Materials and construction (corrosion resistance, vandal resistance)

3.4. Identify and justify any deviations or "approved equivalent" claims
   - If proposing substitution from specified equipment, prepare technical justification
   - Demonstrate equal or superior performance
   - Explain cost, schedule, or performance advantages

**Outputs:**
- Equipment schedule with tag numbers, quantities, manufacturers, models
- Compliance matrices for each equipment category
- Justification documentation for any deviations or substitutions

**Verification:** Technical review of compliance matrices — ensure all requirements addressed

*Source: Guidance.md — Compliance matrix examples; Specification.md — Compliance requirements*

---

### Step 4: Submittal Package Assembly

**Objective:** Compile all datasheets and documentation into organized submittal package.

**Activities:**
4.1. Organize package structure (per Guidance.md example structure)
   - Introduction and submittal summary
   - Equipment schedule (master list)
   - Section 1: CCTV System (compliance matrix, datasheets)
   - Section 2: Access Control System (compliance matrix, datasheets)
   - Section 3: Network Infrastructure (compliance matrix, datasheets)
   - Section 4: Power and UPS (datasheets)
   - Section 5: Accessories (datasheets)
   - Appendices: Certifications, FAT docs (if applicable), integration docs

4.2. Compile datasheets by section
   - Group similar equipment together (e.g., all camera models in camera section)
   - Include equipment tag numbers on or with each datasheet
   - Ensure datasheets are legible and complete

4.3. Prepare table of contents and index
   - Detailed table of contents with page numbers
   - Equipment index cross-referencing tag numbers to datasheet page numbers
   - Appendix index for certifications and supporting documents

4.4. Add submittal cover letter and summary
   - Project identification and submittal information
   - Summary of equipment being submitted (categories, quantities)
   - Statement of compliance with DEL-24.02 specification
   - Note any deviations or "approved equivalent" items requiring special attention
   - Request for approval/acceptance

4.5. Compile into PDF package
   - Combine all sections and appendices into single PDF (or organized multi-file package)
   - Add bookmarks for easy navigation
   - Ensure page numbering consistent
   - Final quality check (legibility, completeness, organization)

**Outputs:**
- Complete data sheet package in PDF format
- Organized, professional submittal ready for transmittal

**Verification:** Internal quality check — review package for completeness, organization, professional presentation

---

### Step 5: Internal Review and Approval

**Objective:** Internal contractor review before formal submittal to designer/Employer.

**Activities:**
5.1. Technical review by security systems specialist
   - Verify equipment selections meet DEL-24.01 design intent
   - Verify equipment specifications meet or exceed DEL-24.02 requirements
   - Check compliance matrices for accuracy
   - Verify all required certifications included

5.2. Procurement/cost review
   - Verify equipment pricing within budget
   - Confirm equipment availability and lead times
   - Identify any long-lead items requiring expedited approval

5.3. Quality check
   - Verify package organization and completeness
   - Check that all datasheets current and legible
   - Verify all tag numbers from DEL-24.01 included
   - Proofread for errors (spelling, formatting, page numbers)

5.4. Revise and finalize package
   - Address internal review comments
   - Make final edits and corrections
   - Obtain internal sign-off for submittal

**Outputs:**
- Internally reviewed and approved submittal package
- Internal review comments resolved

**Verification:** Internal sign-off obtained; package ready for formal submittal

---

### Step 6: Formal Submittal to Designer/Employer

**Objective:** Submit data sheet package for formal review and approval.

**Activities:**
6.1. Prepare submittal transmittal
   - Complete submittal cover sheet or transmittal form per project procedures **TBD**
   - Include project information (project name, package, deliverable ID)
   - List items submitted (equipment categories, document count, appendices)
   - Identify submittal purpose (approval, information, as-noted)
   - Indicate required review and approval parties (designer, Employer)
   - Request return date **TBD** — per project schedule

6.2. Submit via project document management system **TBD**
   - Upload submittal package and transmittal form
   - Route to designer and Employer reviewers per project workflow
   - Obtain transmittal receipt confirmation
   - Record submittal in tracking log (date submitted, submittal number, status)

6.3. Coordinate review if needed
   - Be available to answer questions during review period
   - Provide clarifications or additional information if requested
   - Coordinate Terminal integration review with Employer/Terminal IT (if required)

**Outputs:**
- Formal submittal transmitted to designer/Employer
- Submittal tracking record

**Verification:** Submittal receipt confirmation obtained; submittal logged in tracking system

---

### Step 7: Review and Comment Resolution

**Objective:** Respond to designer/Employer review comments and revise submittal if needed.

**Activities:**
7.1. Receive and review comments
   - Obtain returned submittal with review comments and status (Approved, Approved as Noted, Revise and Resubmit, Rejected)
   - Review all comments carefully
   - Categorize comments (approval conditions, requests for information, non-compliances, clarifications)

7.2. Prepare response to comments
   - For each comment, prepare written response:
     - Accepted: "Acknowledged, will comply" or "Noted, no action required"
     - Revised: "Revised datasheet attached" or "Updated compliance matrix"
     - Clarification: "Equipment meets requirement per [explanation]"
     - Substitution request: "Request acceptance of equivalent per [justification]"

7.3. Revise submittal if required
   - If status is "Approved as Noted" with minor comments:
     - Make noted revisions
     - Provide revised pages or updated package as required
     - No resubmittal needed if comments minor (per project procedures **TBD**)

   - If status is "Revise and Resubmit":
     - Address all non-compliances and significant comments
     - Revise datasheets, compliance matrices, or equipment selections as needed
     - Prepare full resubmittal package
     - Include comment response matrix showing how each comment was addressed
     - Clearly mark revised sections/pages

7.4. Coordinate with designer/Employer if needed
   - If comments unclear or significant issues, coordinate with reviewer for clarification
   - Discuss alternatives if proposed equipment rejected
   - Seek guidance on acceptable solutions

**Outputs:**
- Comment response matrix with written responses to all comments
- Revised submittal package (if required)

**Verification:** All comments addressed; responses reviewed internally before resubmittal

---

### Step 8: Resubmittal (if required)

**Objective:** Resubmit revised data sheet package for approval.

**Activities:**
8.1. Prepare resubmittal package
   - Include full revised submittal or revised sections per project procedures **TBD**
   - Include comment response matrix showing resolutions
   - Clearly identify resubmittal (Revision 1, Resubmittal, etc.)
   - Highlight changes from previous submittal (revision marks, summary of changes)

8.2. Resubmit via project document management system
   - Follow Step 6 (Formal Submittal) process for resubmittal
   - Note resubmittal status in transmittal
   - Reference original submittal number/date

8.3. Await final approval
   - Designer/Employer reviews resubmittal
   - Final status: Approved, Approved as Noted, or further Revise and Resubmit (repeat as needed)

**Outputs:**
- Resubmitted data sheet package
- Final approval status

**Verification:** Approval status obtained

---

### Step 9: Final Approval and Procurement Authorization

**Objective:** Obtain final approval and authorize equipment procurement.

**Activities:**
9.1. Receive final approval
   - Obtain returned submittal with "Approved" or "Approved as Noted" status
   - Verify all conditions of approval (if "Approved as Noted")
   - Obtain formal approval letter or stamp if required **TBD**

9.2. File approved submittal
   - File approved submittal in project document management system
   - Archive in deliverable folder `3_Issued/DEL-24.03_YYYYMMDD_RevX/`
   - Distribute to project team (procurement, construction, QA/QC)

9.3. Authorize procurement
   - Approved submittal authorizes equipment purchase
   - Issue purchase orders based on approved equipment
   - Maintain approved datasheets as procurement and installation reference
   - No substitutions allowed without formal change process

**Outputs:**
- Approved data sheet package (final)
- Procurement authorization based on approved equipment

**Verification:** Final approval obtained and filed; procurement may proceed

---

### Step 10: Change Management (if required during project)

**Objective:** Manage equipment changes or substitutions after submittal approval.

**Activities:**
10.1. Identify need for equipment change
   - Equipment unavailability or long lead time
   - Cost overrun requiring value engineering
   - Design change requiring different equipment
   - Installation issue requiring equipment modification

10.2. Prepare substitution request or revised submittal
   - Document reason for change
   - Provide proposed substitute equipment datasheet and compliance verification
   - Demonstrate equal or superior performance
   - Indicate cost and schedule impact

10.3. Submit for approval per project change management procedures **TBD**
   - Follow formal change request process
   - Obtain designer/Employer approval before proceeding
   - Update approved submittal records

**Outputs:**
- Approved equipment change or substitution
- Updated approved submittal package

**Verification:** Change approval obtained; records updated

---

## Verification

### Verification Activities Summary

| Verification Activity | Responsible Party | Acceptance Criteria |
|-----------------------|-------------------|---------------------|
| **Equipment selection review** | Internal Technical Reviewer | Equipment meets DEL-24.01 design and DEL-24.02 specifications |
| **Compliance verification** | Internal Technical Reviewer | Compliance matrices demonstrate compliance for all requirements |
| **Datasheet completeness** | Submittal Coordinator | All datasheets, certifications, integration docs included |
| **Internal quality check** | Submittal Coordinator | Package organized, professional, complete |
| **Designer review** | Designer / Discipline Lead | Equipment complies with design and specification |
| **Employer review** | Employer / Terminal IT | Equipment acceptable and Terminal-compatible per DEC-05 |
| **Final approval** | Designer + Employer | Submittal status "Approved" or "Approved as Noted" |

*Source: Specification.md — Verification section*

### Submittal Status Definitions

**Approval statuses (typical — TBD per project procedures):**
- **Approved:** No exceptions; proceed with procurement and installation
- **Approved as Noted:** Approved with minor comments; address noted items, no resubmittal required
- **Revise and Resubmit:** Significant issues; revise and resubmit for re-review
- **Rejected:** Not acceptable; major non-compliance, select different equipment

### Completion Criteria

Submittal is complete when:
- ✓ All equipment datasheets and supporting documentation included
- ✓ Compliance matrices demonstrate compliance with DEL-24.02
- ✓ All required certifications included
- ✓ Terminal integration compatibility verified (per DEC-05)
- ✓ Designer review completed and comments addressed
- ✓ Employer acceptance obtained
- ✓ Final approval status: "Approved" or "Approved as Noted"
- ✓ Approved submittal filed in project document management system and deliverable folder `3_Issued/`
- ✓ Procurement authorized based on approved equipment

*Source: Specification.md — Acceptance criteria*

## Records

### Documentation Outputs

**Primary deliverable:**
- **Security System Data Sheet Package** — complete equipment submittal package with:
  - Equipment schedules and compliance matrices
  - CCTV system equipment datasheets
  - Access control system equipment datasheets
  - Network infrastructure equipment datasheets
  - Power and UPS equipment datasheets
  - Certifications and supporting documentation appendices

*Source: `_CONTEXT.md` — Anticipated Artifacts*

**Supporting documentation:**
- Submittal transmittal forms and tracking records
- Review comment logs and response matrices
- Resubmittal packages (if applicable)
- Approval letters or stamps

### Record Management

**Filing locations:**
- **Working files (during preparation):** `1_Working/DEL-24.03_Security_System_Data_Sheet_Package/`
- **Review files (during review):** Submittal tracking in project document management system **TBD**
- **Approved files (upon approval):** `3_Issued/DEL-24.03_YYYYMMDD_RevX/`

**File formats:**
- Submittal package: PDF
- Compliance matrices: Excel or PDF
- Transmittals and tracking: Per project document management system **TBD**

**Retention requirements:**
- **TBD** — Per project records management plan
- Approved submittals are contract documents; retain for project duration + **TBD** years
- Approved datasheets used as reference for procurement, installation, testing, and O&M

**Document control:**
- Submittal tracking log maintained with status and approval dates
- Approved submittals clearly marked and filed
- Superseded submittals (if revised) archived and marked as superseded

*Source: Standard project document control and records management practices*

---

*Document status: Enriched draft — Pass 1*
*Enrichment date: 2026-01-28*
*Cross-references: Specification.md for submittal requirements; Guidance.md for equipment selection strategy; Datasheet.md for equipment scope*
