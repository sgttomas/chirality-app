# Procedure: DEL-13.06 Storage Tank Fabrication Quality Documentation Package

## Purpose

This procedure defines the process for collecting, reviewing, and managing **Storage Tank Fabrication Quality Documentation Package** within **PKG-13 Storage Tanks**.

**Deliverable Description:** Defines and substantiates storage tank fabrication quality documentation package in accordance with ER requirements.

**Source:** _CONTEXT.md, Decomposition document DEL-13.06

### Scope of This Procedure

This procedure describes the workflow for:
1. Reviewing and approving fabricator qualifications
2. Reviewing and approving welding procedures (WPS/PQR/WPQ)
3. Conducting shop inspections and generating shop inspection reports
4. Collecting material documentation (MTRs, impact test results)
5. Collecting NDE reports and weld inspection records during fabrication
6. Compiling complete fabrication quality documentation package
7. Verifying documentation completeness, accuracy, and compliance
8. Submitting documentation for approval and archiving

**Deliverable type:** Document Package
**Responsible party:** D&B Contractor

---

## Prerequisites

### Dependencies

**Dependency tracking:** See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Upstream deliverables required:**

| Deliverable | Content Needed | Status |
|-------------|----------------|--------|
| DEL-13.01: Storage Tank Design Drawing Set | Tank GAs, details for fabrication reference | **TBD** — Verify availability |
| DEL-13.02: Storage Tank Technical Specification | Material specifications, welding requirements, fabrication quality requirements | **TBD** — Verify availability |
| DEL-13.03: Storage Tank Design Calculations | Design basis for procedure qualification | **TBD** — Verify availability |
| DEL-29.02: Inspection and Test Plan With Hold/Witness Points | Hold/witness points for WPS/PQR/WPQ approval, shop inspections | **TBD** — Verify availability |

**Source:** Typical fabrication quality documentation input requirements

### Reference Materials

**Required references:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials
- Employer's Requirements (Volume 2 Part 2) — **Location TBD**
- API 650: Welded Tanks for Oil Storage — **Location TBD** (Sections 2.2, 8)
- CSA W59: Welded Steel Construction — **Location TBD** (ASSUMPTION)
- CSA W47.1: Certification of Companies for Fusion Welding of Steel — **Location TBD** (ASSUMPTION)
- Project quality procedures — **TBD**

**Source:** Typical fabrication quality documentation production references

### Personnel Requirements

**Required personnel:**
- **QA/QC Manager:** Overall responsibility for fabrication quality documentation
- **Welding Engineer:** Reviews and approves WPS/PQR/WPQ
- **QA Inspector:** Conducts shop inspections, reviews material documentation and NDE reports
- **Fabricator Personnel:** Fabricator's welding engineer, QA, welders, NDE technicians

**TBD** — Specific personnel qualifications per project quality procedures

**Source:** Typical QA team for storage tank fabrication quality documentation

### Tools and Materials

**Required tools:**
- Document management system access
- WPS/PQR/WPQ review checklist
- Shop inspection report form or template
- Material certificate review checklist
- NDE report review checklist
- Fabrication quality documentation package template (index and organization)

**Source:** Typical QA tools for fabrication quality documentation

---

## Steps

### Step 1: Review Fabricator Qualifications

**Objective:** Verify fabricator is qualified to fabricate API 650 tanks before awarding fabrication contract.

**Actions:**

1.1. **Request fabricator qualification documentation:**
- CSA W47.1 certification or equivalent (**TBD** — per ER requirements)
- ISO 9001 quality system certification (or equivalent)
- API 650 tank fabrication experience (references from previous projects)
- Fabricator's welding capability (list of qualified procedures and welders)

1.2. **Review fabricator documentation:**
- Verify certifications are current and applicable
- Review references for similar tank projects (capacity, design standard, material)
- Evaluate fabricator's welding capability (number of qualified welders, qualified processes)

1.3. **Conduct shop audit (if required):**
- **TBD** — Shop audit requirements per project risk assessment
- If required, visit fabricator shop to verify:
  - Shop equipment (welding machines, fit-up fixtures, handling equipment)
  - Quality systems (documented procedures, inspection equipment, records)
  - Personnel (interview welding engineer, QA manager, key welders)
  - Shop cleanliness and organization

1.4. **Accept or reject fabricator:**
- If qualifications are acceptable: Approve fabricator for tank fabrication
- If qualifications are deficient: Reject fabricator or identify qualification gaps requiring corrective action before approval

1.5. **Document fabricator qualification review:**
- Prepare fabricator qualification review report
- File report in fabrication quality documentation package (Section 1)

**Verification:** QA Manager and Discipline Lead approve fabricator qualification

**Source:** Typical fabricator pre-qualification process

---

### Step 2: Review and Approve WPS/PQR/WPQ (Pre-Fabrication)

**Objective:** Review and approve welding procedures and welder qualifications before fabrication begins.

**Actions:**

2.1. **Request WPS/PQR/WPQ from fabricator:**
- Fabricator submits WPS, supporting PQR, and WPQ for all welding processes, materials, and joint configurations planned for tank fabrication
- **TBD** — Submittal timing (typically 4-6 weeks before fabrication start)

2.2. **Review WPS (Welding Procedure Specifications):**
- For each WPS, verify using WPS review checklist:
  - Base metal specification and thickness range match project materials (per DEL-13.02)
  - Filler metal is compatible with base metal
  - Welding process is suitable (SMAW, GMAW, FCAW, SAW)
  - Joint design matches project drawings (DEL-13.01)
  - Preheat/interpass temperature are appropriate
  - PWHT (post-weld heat treatment) is specified if required
  - PQR reference is provided
- Verify WPS complies with API 650 Section 8.2 and/or CSA W59 Section 5
- **TBD** — WPS acceptance criteria per project specification (DEL-13.02)

2.3. **Review PQR (Procedure Qualification Records):**
- For each PQR, verify using PQR review checklist:
  - Test coupon configuration matches WPS essential variables
  - Welding parameters actually used are documented
  - Test results are provided: Visual, NDE (RT or UT), tensile test, guided bend tests, impact tests (if required)
  - Test results meet API 650 Section 8.2.4 and/or CSA W59 Section 5.2 acceptance criteria
  - Testing laboratory or technician is qualified
  - PQR is certified (signature and date)
- If PQR test results are marginal or deficient: Request re-testing or procedure revision

2.4. **Review WPQ (Welder Qualification Records):**
- For each WPQ, verify using WPQ review checklist:
  - Welder name and identification
  - Welding process, material, joint type, and position qualified
  - Test coupon configuration matches production welds planned
  - Test results are provided: Visual, NDE (RT or UT), guided bend test
  - Test results meet API 650 Section 8.2.5 and/or CSA W59 Section 6 acceptance criteria
  - WPQ is current (no 6-month gap in welding activity)

2.5. **Approve or reject WPS/PQR/WPQ:**
- **If acceptable:** Welding engineer approves WPS/PQR/WPQ for production use; issue approval letter to fabricator
- **If deficient:** Identify deficiencies; request corrective action (re-testing, procedure revision, additional welder qualification); re-review after corrections

2.6. **File approved WPS/PQR/WPQ:**
- File approved WPS in fabrication quality documentation package (Section 2)
- File supporting PQR in fabrication quality documentation package (Section 2)
- File approved WPQ in fabrication quality documentation package (Section 3)

2.7. **Establish pre-fabrication hold point release:**
- Confirm in ITP (DEL-29.02) that WPS/PQR/WPQ are approved before releasing fabricator to begin welding
- **TBD** — Hold point release authority per project procedures

**Verification:** Welding Engineer and QA Manager approve WPS/PQR/WPQ

**Source:** API 650 Section 8.2; CSA W59 Sections 5 and 6; typical welding procedure approval process

---

### Step 3: Conduct Shop Inspections

**Objective:** Conduct shop inspections during fabrication to verify conformance to design and specifications.

**Actions:**

3.1. **Establish shop inspection schedule:**
- Coordinate with fabricator to establish inspection frequency
- **TBD** — Inspection frequency (daily, weekly, or milestone-based per project quality plan)
- Coordinate inspector travel and fabricator access

3.2. **Conduct shop inspection:**
- QA inspector visits fabricator shop per schedule
- Observe fabrication activities:
  - Material handling and storage
  - Fit-up and tack welding
  - Production welding (verify welders and WPS match approved documentation)
  - Visual weld inspection
  - NDE activities
  - Surface preparation and coating (if shop-applied)
- Verify conformance to:
  - Design drawings (DEL-13.01)
  - Specification (DEL-13.02)
  - Approved WPS
  - Quality procedures
- Identify non-conformances:
  - Deviations from design
  - Unqualified welders or procedures
  - Workmanship defects
  - Quality procedure violations

3.3. **Document shop inspection:**
- Complete shop inspection report form documenting:
  - Inspection date and inspector name
  - Fabrication activities observed
  - Conformance observations
  - Non-conformances identified (with photos if applicable)
  - Corrective actions requested
  - Inspector signature
- Issue shop inspection report to fabricator and D&B Contractor QA Manager

3.4. **Track non-conformances to closure:**
- For each non-conformance, track corrective action by fabricator
- Verify corrective action closure on subsequent inspection or through documentation review
- Do not allow tank shipment until all non-conformances are closed

3.5. **File shop inspection reports:**
- File shop inspection reports in fabrication quality documentation package (Section 4, organized by tank and date)

3.6. **Repeat for all fabrication milestones:**
- Continue shop inspections through completion of all three tanks

**Verification:** QA Manager reviews shop inspection reports and non-conformance closure

**Source:** Typical shop inspection workflow

---

### Step 4: Collect Material Documentation

**Objective:** Collect and review material documentation (MTRs, impact test results).

**Actions:**

4.1. **Collect MTRs (Material Test Reports):**
- Fabricator receives MTRs from material suppliers with material shipments
- Fabricator provides copies of MTRs to D&B Contractor QA
- QA inspector collects MTRs progressively as materials are received

4.2. **Review MTRs:**
- For each MTR, verify using material certificate review checklist (same as DEL-13.05 Step 1):
  - Material specification matches specification (DEL-13.02)
  - Heat number is legible and unique
  - Chemical composition is within specification limits
  - Mechanical properties (yield, tensile, elongation) are within specification limits
  - Mill or supplier stamp/signature is present
  - Certificate is legible and reproducible
- **If acceptable:** File MTR in fabrication quality documentation package (Section 5, organized by tank)
- **If deficient:** Reject material or request corrected certificate before material is used

4.3. **Collect impact test results (if applicable):**
- **TBD** — Impact testing applicability per operating temperature and seismic design requirements
- If impact testing is required:
  - Material supplier or independent test lab performs Charpy V-notch impact tests per ASTM A370
  - Test results submitted with MTRs
  - QA inspector collects impact test results

4.4. **Review impact test results:**
- For each impact test result, verify:
  - Material heat number matches MTR
  - Test temperature is correct per API 650 Section 2.2.11 or specification (DEL-13.02)
  - Test specimen orientation is documented
  - Impact energy values (3 specimens per test) meet acceptance criteria
  - Test lab certification is provided
- **If acceptable:** File impact test results in fabrication quality documentation package (Section 5, organized by tank)
- **If deficient:** Reject material or request re-testing

**Verification:** QA Engineer reviews material documentation for completeness and compliance

**Source:** API 650 Section 2.2; typical material documentation collection workflow

---

### Step 5: Collect NDE Reports (Fabrication)

**Objective:** Collect NDE reports documenting weld examinations during shop fabrication.

**Actions:**

5.1. **Coordinate NDE during fabrication:**
- Fabricator's NDE technician or third-party NDE service performs examinations per API 650 Section 8 and specification (DEL-13.02)
- NDE technician generates NDE report for each examination
- QA inspector coordinates NDE schedule and reviews results

5.2. **Collect NDE reports:**
- QA inspector collects NDE reports from fabricator or NDE service progressively during fabrication
- Typical NDE report turnaround: 24-48 hours after examination

5.3. **Review NDE reports:**
- For each NDE report, verify using NDE report review checklist (same as DEL-13.05 Step 3):
  - NDE method and procedure reference
  - Weld joint identification (match to fabricator's weld tracking system)
  - Acceptance criteria reference (API 650 or specification)
  - Examination results (accept/reject)
  - If defects identified: Defect description, size, location
  - NDE technician name, certification level (Level II minimum), signature, date
- **If weld accepted:** File NDE report in fabrication quality documentation package (Section 6, organized by tank)
- **If weld rejected:**
  - Notify fabricator of defect requiring repair
  - Track repair and re-examination
  - File both initial (defect) and post-repair (acceptance) NDE reports

**Verification:** QA Engineer reviews NDE reports for compliance with acceptance criteria

**Source:** API 650 Section 8; typical NDE workflow during fabrication

---

### Step 6: Collect Weld Inspection Records

**Objective:** Collect in-process visual weld inspection records.

**Actions:**

6.1. **In-process visual weld inspections:**
- Fabricator's welding inspector or D&B Contractor QA inspector performs visual inspections of welds per API 650 Section 8 and CSA W59 Section 12
- Visual inspection criteria: Undercut, porosity, spatter, weld profile, crack indications
- Inspection results documented on weld inspection record or included in shop inspection report

6.2. **Collect weld inspection records:**
- If fabricator uses weld traveler forms or separate weld inspection records: QA inspector collects records
- If weld inspection is documented in shop inspection reports: No separate collection needed (covered in Step 3)

6.3. **Review weld inspection records:**
- Verify visual inspection criteria are documented
- Verify acceptance/rejection is clearly stated
- Verify inspector signature and date

6.4. **File weld inspection records:**
- File weld inspection records in fabrication quality documentation package (Section 6, organized by tank)
- If documented in shop inspection reports: Cross-reference in documentation package index

**Verification:** QA Engineer reviews weld inspection records for completeness

**Source:** API 650 Section 8; CSA W59 Section 12; typical weld inspection workflow

---

### Step 7: Compile Fabrication Quality Documentation Package

**Objective:** Compile all fabrication quality documents into organized package.

**Actions:**

7.1. **Establish package structure:**
- Section 1: Fabricator Qualification Documentation
- Section 2: Welding Procedure Documentation (WPS, PQR)
- Section 3: Welder Qualification Documentation (WPQ)
- Section 4: Shop Inspection Reports (organized by tank and date)
- Section 5: Material Documentation (MTRs, impact test results, organized by tank)
- Section 6: NDE and Weld Inspection Documentation (organized by tank)
- Section 7: Index and Cross-Reference

7.2. **Compile documents by section:**
- Collect all documents from Steps 1-6
- Organize documents per package structure
- Remove duplicates (if same document collected multiple times)

7.3. **Prepare index and cross-reference:**
- Create comprehensive index listing all documents in package
- Create cross-reference table:
  - WPS number → PQR number
  - Welder ID → WPQ number(s)
  - Tank → Shop inspection reports, MTRs, NDE reports
- File index in Section 7

7.4. **Format package for submission:**
- **TBD** — Electronic format (PDF dossier) or hard copy (bound book) per project document management procedures
- If electronic: Scan hard-copy documents; compile into single indexed PDF or folder structure
- If hard copy: Print, organize in binder with section dividers, index

**Verification:** QA Manager reviews compiled package for organization and completeness

**Source:** Typical documentation compilation workflow

---

### Step 8: Verify Fabrication Quality Documentation Package

**Objective:** Verify package completeness, accuracy, and compliance before submission.

**Actions:**

8.1. **Completeness check:**
- Verify all required documents are present using completeness checklist:
  - Fabricator qualifications (Section 1)
  - All WPS and supporting PQRs (Section 2)
  - All WPQs for welders used in production (Section 3)
  - Shop inspection reports covering full fabrication duration (Section 4)
  - MTRs for all materials (Section 5)
  - Impact test results if applicable (Section 5)
  - NDE reports for all examined welds (Section 6)
  - Weld inspection records or cross-reference to shop inspection reports (Section 6)
  - Index and cross-reference (Section 7)
- Identify any missing documents; obtain before proceeding

8.2. **Accuracy verification:**
- Spot-check documents for accuracy:
  - WPS/PQR/WPQ: Verify test results meet acceptance criteria
  - MTRs: Verify material properties are within specification limits
  - NDE reports: Verify all reports show acceptance (no open defects)
  - Shop inspection reports: Verify all non-conformances are closed
- Correct any errors identified

8.3. **Compliance verification:**
- Verify package demonstrates compliance with:
  - API 650 Sections 2.2 and 8 requirements
  - CSA W59 requirements (if applicable)
  - Project specification (DEL-13.02) requirements
- If compliance gaps are identified, obtain additional documentation or corrective action evidence

8.4. **Cross-reference verification:**
- Verify cross-references are correct:
  - WPS referenced in shop inspection reports match approved WPS in Section 2
  - Welder IDs in shop inspection reports have corresponding WPQs in Section 3
- Correct any cross-reference errors

**Verification:** QA Manager and Welding Engineer perform independent review of verification results

**Source:** Typical documentation verification process

---

### Step 9: Submit Documentation for Approval

**Objective:** Submit documentation package for internal approval and client acceptance.

**Actions:**

9.1. **Internal review and approval:**
- QA Manager reviews complete package
- Welding Engineer reviews WPS/PQR/WPQ sections
- Discipline Lead (Mechanical) reviews and approves package for submission

9.2. **Submit to client:**
- Submit fabrication quality documentation package to client per project submission procedures
- **TBD** — Submission timing (typically after fabrication complete, before or with tank shipment)
- **TBD** — Submission format per ER
- **Source:** Project document control procedures

9.3. **Address client comments:**
- Receive client review comments (if any)
- Address comments by obtaining additional documentation, providing clarifications, or correcting errors
- Resubmit revised package if needed

9.4. **Obtain client acceptance:**
- Receive client acceptance of package
- File client acceptance letter in project file

**Verification:** QA Manager verifies client acceptance is obtained

**Source:** Typical documentation submission and acceptance process

---

### Step 10: Archive Documentation Package

**Objective:** Archive final fabrication quality documentation package for facility lifetime.

**Actions:**

10.1. **Prepare archival package:**
- Finalize package with client acceptance
- Verify archival format requirements:
  - **Electronic:** PDF/A format (archival-quality), searchable text, indexed
  - **Hard copy:** Bound book, durable binding, acid-free paper
- **TBD** — Archival format per ER and project document management procedures

10.2. **File in project document management system:**
- Upload final package to project document management system
- Categorize as "Quality Records" and "Fabrication Documentation"
- Set retention period to facility lifetime

10.3. **Provide archival copies to client:**
- Provide client with archival copies (electronic and/or hard copy per ER)
- **TBD** — Client archival requirements

10.4. **Retain project copy:**
- Retain project copy in D&B Contractor project archive per company records retention policy

**Verification:** QA Manager verifies archival is complete

**Source:** Typical record archival process

---

## Verification

### Verification Activities

**Fabricator Qualification Review (Step 1):**
- Verify fabricator certifications and capabilities

**WPS/PQR/WPQ Technical Review (Step 2):**
- Welding engineer verifies procedure and welder qualifications

**Shop Inspection Review (Step 3):**
- QA manager verifies shop conformance and non-conformance closure

**Material Documentation Review (Step 4):**
- QA engineer verifies material compliance

**NDE and Weld Inspection Review (Steps 5, 6):**
- QA engineer verifies weld quality compliance

**Completeness Check (Step 8.1):**
- Verify all required documents are present

**Accuracy and Compliance Verification (Steps 8.2, 8.3):**
- Verify document data is accurate and demonstrates compliance with codes and specifications

**Source:** Specification.md V-01 through V-05

### Sign-off Requirements

**Welding Engineer sign-off:**
- Approves WPS/PQR/WPQ (Step 2)

**QA Inspector sign-off:**
- Certifies shop inspections conducted and documented (Step 3)

**QA Engineer sign-off:**
- Certifies material documentation, NDE reports, weld inspection records reviewed and compliant (Steps 4, 5, 6)

**QA Manager sign-off:**
- Certifies documentation package is complete, accurate, and compliant (Step 8)

**Discipline Lead sign-off:**
- Approves documentation package for submission (Step 9)

**Client sign-off:**
- Accepts documentation package (Step 9)

**Source:** Typical fabrication quality documentation approval workflow

---

## Records

### Documentation Outputs

**Primary outputs:**
- Fabrication Quality Documentation Package containing:
  - Section 1: Fabricator Qualification Documentation
  - Section 2: WPS and PQR (**TBD** quantity, estimated 3-10 each)
  - Section 3: WPQ (**TBD** quantity, estimated 10-40)
  - Section 4: Shop Inspection Reports (**TBD** quantity, estimated 30-90 total)
  - Section 5: MTRs (**TBD** quantity, estimated 50-100) and Impact Test Results (if applicable)
  - Section 6: NDE Reports (**TBD** quantity, estimated 60-150) and Weld Inspection Records
  - Section 7: Index and Cross-Reference

**Supporting records:**
- WPS/PQR/WPQ review checklists
- Material certificate review checklists
- NDE report review checklists
- Completeness and accuracy verification checklists
- Client acceptance letter

**Source:** _CONTEXT.md (Anticipated Artifacts); API 650 and CSA W59 requirements

### Record Management

**Filing locations:**
- `1_Working/DEL-13.06/` — Work-in-progress documentation collection
- `2_Checking/To/` — Documentation package issued for client review (awaiting acceptance)
- `2_Checking/From/` — Documentation package returned from client review with comments
- `3_Issued/` — Accepted documentation package (final)
- Project document management system — Electronic archival copies

**Retention requirements:**
- **TBD** — Retention period per ER (typically facility lifetime for fabrication quality documentation)

**Source:** ASSUMPTION based on typical project document control procedures

---

## Cross-Document References

**For detailed requirements:** See `Specification.md`
- FR-01 through FR-05 → Implemented in Steps 2-6
- PR-01 through PR-05, QR-01 through QR-04 → Verified in Steps 1, 2, 8
- DP-01 through DP-04 → Implemented in Steps 7, 9, 10

**For principles and guidance:** See `Guidance.md`
- DP-01: Fabricator Qualification Philosophy → Implemented in Step 1
- DP-02: Welding Procedure Qualification → Implemented in Step 2
- DP-03: API 650 and CSA W59 Compliance Documentation → Applied throughout all steps
- DP-05: Timing: Pre-Fabrication Approval Critical → Enforced in Step 2
- Considerations → Inform workflow decisions

**For entity attributes:** See `Datasheet.md`
- WPS, PQR, WPQ, Shop Inspection Reports, MTRs, Impact Test Results, NDE Reports, Weld Inspection Records attributes → Documented in Steps 2-6

---

**Document Status:** Pass 3 (Final) — Enrichment complete. Procedure steps defined with verification points and cross-document references. All TBDs marked. ASSUMPTIONs labeled. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
