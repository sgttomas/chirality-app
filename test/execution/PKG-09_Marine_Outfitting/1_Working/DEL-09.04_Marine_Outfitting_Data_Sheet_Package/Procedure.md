# Procedure: DEL-09.04 Marine Outfitting Data Sheet Package

## Purpose

This procedure defines the process for producing and verifying **Marine Outfitting Data Sheet Package** within **PKG-09 Marine Outfitting**.

**Decomposition definition (authoritative):** Defines and substantiates marine outfitting in accordance with Employer's Requirements. (**Source:** Decomposition, DEL-09.04 row)

**Deliverable type:** Data Sheet
**Responsible party:** D&B Contractor

**Scope:** This procedure covers data sheet development from scope confirmation through issue preparation, including vendor data collection, data sheet population, consistency verification, and review activities.

## Prerequisites

### Dependencies

Dependencies are coordinated externally (NOT_TRACKED). See `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`.

**Required upstream inputs (confirm availability and maturity prior to commencement):**

| Input | Source | Specification § | Guidance § | Required For | Status |
|-------|--------|-----------------|------------|--------------|--------|
| Specification requirements | DEL-09.02 | SPEC § 2 | — | Data sheet fields and acceptance criteria | **TBD** |
| Calculation results | DEL-09.03 | SPEC § 4 | Guidance § Considerations (Calculation alignment) | Performance values to substantiate (fender energy/reaction, bollard SWL) | **TBD** |
| Equipment tags | DEL-09.01 | SPEC § 3 | Guidance § Considerations (Tag consistency) | Equipment identification and drawing references | **TBD** |
| Vendor/OEM data sheets | Vendor | SPEC § 2, 4 | Guidance § Principles | Product specs, physical/performance characteristics | **TBD** |
| Vendor certificates | Vendor | SPEC § 2 | Guidance § Principles | Compliance evidence (FAT, material certs, test reports) | **TBD** |
| Employer's Requirements | Employer | SPEC § Standards | — | Submittal requirements, data sheet content | **TBD** |
| Project tagging convention | Project | SPEC § 1.2 | — | Equipment tag format and numbering | **TBD** |

### Reference Materials

- See `_REFERENCES.md` for applicable reference documents.
- See `0_References/` in package directory for reference materials and vendor data.
- Employer's Requirements (Vol 2 Part 1–3) — **TBD** (submittal requirements).
- DEL-09.02 Marine Outfitting Technical Specification — field requirements.
- DEL-09.03 Marine Outfitting Design Calculations — performance values to substantiate.

### Personnel Requirements

| Role | Requirement |
|------|-------------|
| Originator (Document Control/Procurement Coordinator) | Qualified personnel with experience in equipment data sheets, vendor submittals, document control — **TBD** (qualifications per project quality plan) |
| Checker/Reviewer | Checker qualifications — **TBD** (independent of originator; qualified in Marine discipline or QA/QC experience) |
| Approver | **TBD** — per project authority matrix (typically Marine discipline lead or Package Manager) |

**ASSUMPTION:** Personnel competency and authority per project quality procedures and authority matrix.

### Tools and Resources

| Tool/Resource | Purpose | Status |
|---------------|---------|--------|
| Data sheet template | Structured format for data sheet package | **TBD** — project-standard template or vendor format with project header |
| Vendor data repository | Tracking and storage of vendor submittals | **TBD** — project document management system or vendor submittal portal |

## Steps

### Step 1: Confirm Scope

**Objective:** Establish the data sheet list and confirm equipment inventory.

**Actions:**
1. Review DEL-09.04 anticipated artifacts from the decomposition:
   - Fender data sheets
   - Bollard data sheets
2. Review `Datasheet.md` Content Checklist for minimum data sheet content requirements.
3. Obtain equipment list from DEL-09.01 drawings:
   - Fenders: count, types, locations, equipment tags
   - Bollards: count, types, locations, equipment tags
4. Confirm equipment grouping strategy:
   - One data sheet per individual equipment item (if each is unique)
   - One data sheet per equipment type/group (if multiple identical items)
   - **TBD:** Grouping strategy per project document control preferences
5. Document scope clarifications (if any).
6. Prepare preliminary data sheet list with equipment tags and drawing references.

**Inputs:** Decomposition, `Datasheet.md`, DEL-09.01 drawings.
**Outputs:** Confirmed data sheet list; equipment inventory with tags and drawing references; scope clarification notes (if any).
**Verification:** Data sheet list addresses all equipment shown on DEL-09.01 drawings; tags match drawings.

### Step 2: Define Required Fields

**Objective:** Establish data sheet template and required field list.

**Actions:**
1. Extract data sheet field requirements from:
   - Employer's Requirements submittal clauses (**TBD** — ER clauses for vendor submittals to be extracted)
   - DEL-09.02 specification requirements (§ 2.1 fender requirements, § 2.2 bollard requirements)
   - `Specification.md § 2` (content coverage requirements)
   - `Datasheet.md` Content Checklist (fender fields, bollard fields)
2. Create or confirm data sheet template/form:
   - Header format (project name, package, deliverable ID, equipment tag, drawing ref, revision, date)
   - Field structure per `Specification.md § 2.1, 2.2` and `Guidance.md § Examples`
   - Attachment provisions (vendor literature, curves, certificates)
3. Review template with Project Manager or Document Control lead for approval.

**Inputs:** Employer's Requirements, DEL-09.02, `Specification.md § 2`, `Datasheet.md` Content Checklist, `Guidance.md § Examples`.
**Outputs:** Data sheet template with required fields; field list with requirements traceability (ER clause, DEL-09.02 §, or `Specification.md §`).
**Verification:** Template includes all fields per `Datasheet.md` Content Checklist; template approved by Project Manager or Document Control lead.

### Step 3: Collect Vendor Data

**Objective:** Obtain vendor submittals and supporting documentation.

**Actions:**
1. Identify selected vendors/products for fenders and bollards:
   - Confirm vendor selection with Procurement or Project Manager
   - Obtain vendor contact information
2. Request vendor data sheets, product literature, and certificates:
   - **Fenders:** Vendor catalog sheets, deflection/reaction curves (with temperature/velocity conditions), FAT certificates, material certificates, compliance statements
   - **Bollards:** Vendor catalog sheets, capacity ratings, material certificates (MTRs), welding certificates (if fabricated), proof load test certificates (if applicable), compliance statements
3. Receive and organize vendor submittals:
   - Verify vendor document numbers, revisions, dates
   - Store in vendor data repository (project document management system or `0_References/` folder)
   - Log receipt in vendor submittal register
4. Identify missing vendor submittals:
   - Log missing items as **TBD** with follow-up actions
   - Assign action owners (typically Procurement or vendor coordinator)
   - Set target dates for submittal receipt
5. Prepare vendor data package organized by equipment type (fenders, bollards).

**Inputs:** Vendor selection (from Procurement), `Datasheet.md` Content Checklist (required vendor data list), `Specification.md § 2` (certificate requirements).
**Outputs:** Vendor data package (catalog sheets, curves, certificates); vendor submittal register with receipt status; missing submittals log with action owners and target dates.
**Verification:** Vendor data received and logged; missing submittals identified with follow-up actions; vendor document numbers/revisions/dates verified.

### Step 4: Populate Data Sheets

**Objective:** Populate data sheets using vendor data and project information.

**Actions:**

**4a. Populate Fender Data Sheets (per `Specification.md § 2.1` and `Datasheet.md § Fender Data Sheets`):**

1. **Identification section:**
   - Equipment tag: From DEL-09.01 drawings and equipment list (Step 1)
   - Drawing reference: DEL-09.01 drawing number(s) showing fender location
   - Location: Descriptive location (e.g., "Berth face Sta. 0+25.0, El. +3.5m")
2. **Manufacturer information:**
   - Vendor name, model/type designation, catalog reference
   - Source: Vendor catalog sheets (cite document number, revision, date)
3. **Physical characteristics:**
   - Dimensions (L × D × H), weight, rubber grade, steel backing material
   - Source: Vendor data
4. **Performance characteristics:**
   - Energy rating (kJ at rated deflection), reaction force at design deflection (kN), rated deflection (%)
   - Source: Vendor data and DEL-09.03 fender reaction calculations
   - **Cross-check:** Verify performance values match DEL-09.03 (defer to Step 5 for verification)
5. **Deflection curves:**
   - Attach manufacturer deflection/reaction curves (E vs δ, R vs δ)
   - Note temperature/velocity conditions for curves
   - Identify specific curve used for DEL-09.03 design calculations
6. **Hardware, corrosion protection, installation:**
   - Hardware: Chains, anchor pads, frontal frame, fixing bolts (from vendor data)
   - Corrosion protection: Coating system (type, DFT), service life, UV/ozone resistance (from vendor data; verify compliance with DEL-09.02 § 1.4)
   - Installation: Mounting method, tolerances, orientation (from vendor installation instructions)
7. **Certificates:**
   - Attach or reference FAT certificates, material certificates, compliance statements (from vendor submittals)
8. **Notes and deviations:**
   - Document any project-specific modifications or non-standard selections
   - Mark missing data as **TBD** with action owner
9. **Source documentation:**
   - Cite vendor source document for all data: document number/catalog reference, revision/edition, date

**4b. Populate Bollard Data Sheets (per `Specification.md § 2.2` and `Datasheet.md § Bollard Data Sheets`):**

1. **Identification section:**
   - Equipment tag, drawing reference, location (same process as fenders)
2. **Manufacturer information:**
   - Vendor name, model/type (Tee-head, horn, etc.), catalog reference
   - Source: Vendor catalog sheets
3. **Physical characteristics:**
   - Dimensions, weight, steel grade (cast or fabricated)
   - Source: Vendor data
4. **Capacity:**
   - SWL (kN or tonnes), design factors, ultimate capacity
   - Source: Vendor rating and DEL-09.03 bollard load calculations
   - **Cross-check:** Verify SWL ≥ required capacity from DEL-09.03 (defer to Step 5)
5. **Corrosion protection, fixing/anchorage, installation:**
   - Corrosion protection: Hot-dip galvanizing or coating (standard, thickness) (verify compliance with DEL-09.02 § 1.4)
   - Fixing/anchorage: Foundation type, anchor bolt specs, base plate details (coordinate with PKG-08 if on structure)
   - Installation: Mounting procedure, tolerances, grouting requirements (from vendor installation instructions)
6. **Proof load testing (if applicable):**
   - Test requirements per DEL-09.02 § 2.2 and codes (test load typically 1.5 × SWL)
   - Test certificates (if testing already performed)
   - **TBD:** If proof load testing not yet performed, note requirements for testing
7. **Certificates:**
   - Attach or reference material certificates (MTRs), welding certificates, compliance statements
8. **Notes and deviations:**
   - Document project-specific modifications, TBDs with action owners
9. **Source documentation:**
   - Cite vendor source document for all data

**Inputs:** Vendor data package (Step 3), equipment list with tags (Step 1), DEL-09.01 drawings, DEL-09.03 calculations, DEL-09.02 specification, data sheet template (Step 2).
**Outputs:** Draft data sheet package with populated data sheets (fenders, bollards); TBDs log with action owners for missing data.
**Verification:** All required fields per `Datasheet.md` Content Checklist addressed (completed or TBD); vendor source documents cited for all data.

### Step 5: Verify Consistency

**Objective:** Cross-check data sheets for consistency, accuracy, and completeness.

**Actions:**

**5a. Cross-check equipment tags vs DEL-09.01 drawings:**
- Verify each data sheet equipment tag matches DEL-09.01 drawings
- Verify drawing references are correct (drawing numbers, sheet numbers)
- Identify and resolve any tag discrepancies
- **Criterion:** Tags must match exactly (no discrepancies)

**5b. Cross-check performance values vs DEL-09.03 calculations:**
- **Fenders:** Verify fender energy rating and reaction force at design deflection match DEL-09.03 fender reaction calculation results
- **Bollards:** Verify bollard SWL meets or exceeds required capacity from DEL-09.03 bollard load calculation
- Document cross-check in verification record
- Resolve any discrepancies (update data sheet if error; coordinate with DEL-09.03 if calculation needs revision)
- **Criterion:** Data sheet values consistent with DEL-09.03 within acceptable tolerance

**5c. Verify vendor document references:**
- Check that all vendor data is correctly cited: vendor document number/catalog reference, revision/edition, date
- Verify vendor document numbers match actual vendor submittals received (no transcription errors)
- **Criterion:** All vendor references correct and verifiable

**5d. Verify completeness vs `Datasheet.md` Content Checklist:**
- Check that all Content Checklist fields are addressed for each data sheet (either completed or marked TBD)
- Verify all required attachments are included or referenced (deflection curves, certificates)
- **Criterion:** All Content Checklist items addressed; no missing fields without TBD notation

**5e. Check units and nomenclature consistency:**
- Verify consistent use of SI units (kN, kJ, mm, tonnes) across all data sheets
- Check terminology consistency (e.g., "Safe Working Load" vs "SWL" — use consistently)
- **Criterion:** Units and terminology consistent across all data sheets

**5f. Document verification findings:**
- Prepare verification record documenting cross-checks performed, findings, and resolutions
- Log any issues found and actions taken to resolve

**Inputs:** Draft data sheet package (Step 4), DEL-09.01 drawings, DEL-09.03 calculations, vendor submittals, `Datasheet.md` Content Checklist, `Specification.md § 4`.
**Outputs:** Verification record with cross-check results; updated data sheets (if corrections made); issues log with resolutions.
**Verification:** All cross-checks completed and documented; any discrepancies resolved or escalated; verification record signed by originator.

### Step 6: Review/Approval

**Objective:** Obtain peer review and approval of data sheet package.

**Actions:**
1. Assign peer reviewer (qualified engineer or QA/QC personnel; independent of originator per project quality procedures).
2. Provide reviewer with data sheet package and supporting materials:
   - Data sheet package (Step 5 output after verification)
   - Verification record (Step 5)
   - `Datasheet.md` Content Checklist
   - `Specification.md` requirements
   - DEL-09.03 calculations (for cross-check reference)
   - Vendor submittals (for source verification)
3. Reviewer performs review per `Specification.md § Verification` check criteria:
   - **All required data sheets included:** Equipment list from Step 1 complete
   - **All required fields populated or marked TBD:** Content Checklist items addressed
   - **Vendor data correctly referenced:** Vendor document numbers, revisions, dates correct
   - **Values consistent with calculations:** Cross-check with DEL-09.03 verified
   - **Tags match drawings:** Cross-check with DEL-09.01 verified
4. Reviewer documents findings (comments, questions, corrections).
5. Originator reviews reviewer comments and responds:
   - **Accept:** Incorporate correction; document acceptance
   - **Clarify:** Provide additional information; revise if needed for clarity
   - **Reject:** Provide justification (if comment not applicable); discuss with reviewer to resolve
6. Originator revises data sheet package to address reviewer comments.
7. Reviewer reviews revised package and confirms resolution of comments.
8. Reviewer provides sign-off (confirmation that data sheet package is complete, accurate, and acceptable).
9. Obtain approval per project authority matrix (typically Marine discipline lead or Package Manager).

**Inputs:** Data sheet package (Step 5 output), verification record, supporting materials.
**Outputs:** Reviewer comments; comment resolution log; revised data sheet package incorporating reviewer comments; reviewer sign-off; approval sign-off.
**Verification:** Reviewer sign-off obtained; all reviewer comments resolved and documented; approval obtained per project authority matrix.
**TBD:** Reviewer acceptance criteria and approval workflow per project quality procedures.

### Step 7: Issue Preparation

**Objective:** Prepare data sheet package for issue (review/approval or construction).

**Actions:**
1. Compile data sheet package with cover/index per `Specification.md § 1.1`:
   - Cover page (project name, package, deliverable ID, revision, date)
   - Index listing all data sheets (equipment tag, type, data sheet reference/page, revision, date)
   - Individual data sheets (fenders, bollards)
   - Attachments (vendor literature, curves, certificates)
2. Apply final document control:
   - Assign document number per project numbering system (if not already assigned)
   - Apply revision designation per project revision scheme (e.g., Rev 0 for first issue)
   - Update headers/footers with document number, revision, date, project information
3. Prepare issue package:
   - **Format:** PDF for issue/record; organize attachments (per `Specification.md § Documentation`)
   - **Transmittal:** Prepare transmittal cover sheet listing document number, title, revision, purpose of issue (e.g., "For Review," "For Approval," "For Construction")
4. Prepare issue records:
   - Vendor submittal register (Step 3)
   - Verification record (Step 5)
   - Reviewer sign-off and comment resolution log (Step 6)
   - TBDs log (if any TBDs remaining)
5. Update `_STATUS.md` when ready for CHECKING or ISSUED state:
   - **CHECKING:** Data sheet package issued for review/approval (placed in `2_Checking/To/`)
   - **ISSUED:** Data sheet package approved and issued for construction (placed in `3_Issued/`)
   - Update status with date, revision, and brief description of issue
6. Archive previous revisions (if applicable) per project records management procedures.

**Inputs:** Data sheet package (Step 6 output after review/approval), all supporting records, project document control procedures.
**Outputs:** Issue-ready data sheet package with cover/index; transmittal; supporting records (vendor submittal register, verification record, reviewer sign-off, TBDs log); updated `_STATUS.md`.
**Verification:** Data sheet package is complete and complies with project document control requirements; all review/approval records are complete; `_STATUS.md` updated correctly.
**TBD:** Project document control procedures and issue protocols.

## Verification

**Summary of verification activities performed throughout this procedure:**

| Activity | Step | Criteria | Sign-off |
|----------|------|----------|----------|
| Scope confirmation | Step 1 | Data sheet list addresses all equipment on DEL-09.01 drawings; tags match | Originator |
| Template definition | Step 2 | Template includes all fields per `Datasheet.md` Content Checklist; approved | Originator / PM or Doc Control |
| Vendor data collection | Step 3 | Vendor data received and logged; missing submittals identified with follow-up | Originator |
| Data sheet population | Step 4 | All fields addressed (completed or TBD); vendor sources cited | Originator |
| Consistency verification | Step 5 | Tags match DEL-09.01; values match DEL-09.03; vendor refs correct; Content Checklist complete | Originator |
| Peer review | Step 6 | All required data sheets included; fields complete or TBD; vendor data correct; values consistent | Reviewer |
| Issue readiness | Step 7 | Package complete with cover/index; complies with document control requirements | Approver |

**Sign-off requirements (per project quality procedures):**

| Role | Signature | Purpose |
|------|-----------|---------|
| Originator | Required | Confirms data sheets are complete and verified |
| Reviewer | Required | Confirms peer review completed; data sheets are accurate and acceptable |
| Approver | Required | Authorizes issue for intended purpose (review/approval/construction) |

**ASSUMPTION:** Sign-off protocol and authority matrix per project quality procedures.

## Records

**Documentation outputs (per `Specification.md § Documentation` and `Datasheet.md`):**
- Fender data sheets (one per fender or fender type)
- Bollard data sheets (one per bollard or bollard type)

**Record management:**

| Record | Location | Retention | Purpose |
|--------|----------|-----------|---------|
| Draft data sheets (in progress) | `1_Working/` | Per project procedures | Working files during development |
| Review package | `2_Checking/To/` | Per project procedures | Issue for review/approval |
| Issued data sheet package | `3_Issued/` | Per project procedures | Final issue for construction; project record |
| Vendor submittal register | Deliverable folder or project QA system | Per project procedures | Tracking of vendor data receipt and status |
| Verification record | Deliverable folder or project QA system | Per project procedures | Evidence of consistency verification |
| Reviewer sign-off and comment resolution log | Deliverable folder or project QA system | Per project procedures | Evidence of peer review |
| Vendor data package | Deliverable folder / `0_References/` | Per project procedures | Vendor submittals (catalog sheets, curves, certificates) |
| TBDs log (if applicable) | Deliverable folder | Per project procedures | Tracking of missing data with action owners |

**ASSUMPTION:** Electronic records managed in project document management system with appropriate access controls, backup/retention protocols, and audit trail.

**Cross-reference:** See `Datasheet.md § References` for related documents.
