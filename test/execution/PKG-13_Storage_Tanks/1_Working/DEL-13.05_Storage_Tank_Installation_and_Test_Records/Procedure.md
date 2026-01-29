# Procedure: DEL-13.05 Storage Tank Installation & Test Records

## Purpose

This procedure defines the process for collecting, verifying, and managing **Storage Tank Installation & Test Records** within **PKG-13 Storage Tanks**.

**Deliverable Description:** Provides evidence of completion, inspection, and testing for storage tank.

**Source:** _CONTEXT.md, Decomposition document DEL-13.05

### Scope of This Procedure

This procedure describes the workflow for:
1. Collecting material certificates from suppliers
2. Developing and maintaining weld maps during fabrication
3. Collecting NDE reports during fabrication and after repairs
4. Documenting hydrostatic test execution and results
5. Compiling complete record package (tank dossier) for each tank
6. Verifying record completeness, accuracy, and traceability
7. Submitting record package for client acceptance

**Deliverable type:** Record
**Responsible party:** D&B Contractor (QA/QC)

---

## Prerequisites

### Dependencies

**Dependency tracking:** See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Upstream deliverables required:**

| Deliverable | Content Needed | Status |
|-------------|----------------|--------|
| DEL-13.01: Storage Tank Design Drawing Set | Tank GAs, nozzle schedules, weld joint identification basis | **TBD** — Verify availability |
| DEL-13.02: Storage Tank Technical Specification | Material specifications, NDE requirements, testing requirements | **TBD** — Verify availability |
| DEL-13.03: Storage Tank Design Calculations | Hydrotest pressure, settlement limits | **TBD** — Verify availability |
| DEL-13.06: Storage Tank Fabrication Quality Documentation Package | WPS/PQR/WPQ for weld map cross-reference | **TBD** — Verify availability |
| DEL-29.02: Inspection and Test Plan With Hold/Witness Points | Hold/witness points for material inspection, NDE, hydrotest | **TBD** — Verify availability |

**Source:** Typical quality record input requirements

### Reference Materials

**Required references:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials
- Employer's Requirements (Volume 2 Part 2) — **Location TBD**
- API 650: Welded Tanks for Oil Storage — **Location TBD** (Sections 2.2, 7.4, 8)
- CSA W59: Welded Steel Construction — **Location TBD**
- Project quality procedures — **TBD**

**Source:** Typical quality record production references

### Personnel Requirements

**Required personnel:**
- **QA/QC Manager:** Overall responsibility for quality records collection and compilation
- **QA Inspector:** Collects and reviews records during fabrication, erection, and testing
- **NDE Technician:** Performs NDE and generates NDE reports (Level II minimum per ASNT SNT-TC-1A or ISO 9712)
- **Surveyor:** Performs settlement measurements during hydrostatic test
- **Client Inspector:** Witnesses hold/witness point activities per ITP (DEL-29.02)

**TBD** — Specific personnel qualifications per project quality procedures

**Source:** Typical QA team for storage tank construction

### Tools and Materials

**Required tools:**
- Document management system access for record storage and retrieval
- Material certificate review checklist
- Weld map template (drawing format)
- NDE report forms (or NDE vendor report format)
- Hydrostatic test record form
- Surveying equipment for settlement measurements
- Tank dossier template (index and organization)

**Source:** Typical QA tools for record management

---

## Steps

### Step 1: Collect Material Certificates

**Objective:** Obtain and verify material certificates (MTRs) for all tank materials.

**Actions:**

1.1. **Identify required materials:**
- Review material take-off from design drawings (DEL-13.01) and specification (DEL-13.02)
- Identify all pressure-retaining and structural materials requiring certification:
  - Shell plates
  - Bottom plates
  - Roof plates
  - Nozzle forgings/pipes
  - Structural steel
  - Bolts and fasteners

1.2. **Receive material certificates from suppliers:**
- Material procurement process includes requirement for MTRs with material shipment
- QA inspector receives MTRs from receiving inspection or procurement team
- **TBD** — Material receiving inspection process and MTR submittal protocol

1.3. **Review material certificates:**
- For each MTR, verify:
  - Material specification matches specification (DEL-13.02)
  - Heat number is legible and unique
  - Chemical composition is within specification limits
  - Mechanical properties (yield, tensile, elongation) are within specification limits
  - Mill or supplier stamp/signature is present
  - Certificate is legible and reproducible (for archival)

1.4. **Accept or reject material certificates:**
- If MTR is complete and compliant: Accept and file in working folder
- If MTR is incomplete or non-compliant: Reject and request corrected certificate from supplier before material is used

1.5. **Organize material certificates:**
- File MTRs by heat number or material type
- Prepare preliminary index of material certificates
- Cross-reference MTRs to material shipments and purchase orders

**Verification:** QA Manager spot-checks MTR review results

**Source:** Typical material receiving inspection and certificate review process

---

### Step 2: Develop Weld Maps

**Objective:** Create comprehensive weld maps showing all weld joints with traceability to materials, welders, and NDE reports.

**Actions:**

2.1. **Prepare preliminary weld map (before fabrication):**
- Using tank general arrangements (DEL-13.01), create weld map drawing showing:
  - Tank elevation (unrolled shell view)
  - Shell course boundaries
  - Anticipated vertical seam locations
  - Bottom-to-shell weld
  - Roof welds
  - Nozzle weld locations
- Assign preliminary weld joint identification numbers (e.g., W-101, W-102, W-103, etc.)

2.2. **Update weld map during fabrication:**
- As fabrication proceeds, update weld map with actual information:
  - Material heat numbers for each shell plate (from MTRs and fabricator material tracking)
  - Weld procedure specification (WPS) number for each weld (from WPS in DEL-13.06)
  - Welder identification for each weld
  - Weld date
- Coordinate with fabricator QA to obtain weld information
- **TBD** — Fabricator QA interface and weld information submittal protocol

2.3. **Update weld map with NDE results:**
- As NDE reports are generated (Step 3), add NDE report reference number to each weld joint on weld map
- Track repair welds: If weld is repaired, add repair weld information (repair WPS, welder, date, re-examination NDE report number)

2.4. **Finalize as-built weld map:**
- After fabrication and all repairs are complete, finalize weld map as as-built document
- Verify all weld joints have complete information (material heat, WPS, welder, NDE report)
- Issue weld map as controlled document

2.5. **Produce weld maps for all three tanks:**
- Repeat Steps 2.1-2.4 for Tank TK-101, TK-102, TK-103

**Verification:** QA Manager reviews weld maps for completeness and traceability

**Source:** Typical weld map development workflow

---

### Step 3: Collect NDE Reports

**Objective:** Collect NDE reports documenting examination of all welds per API 650 requirements.

**Actions:**

3.1. **Coordinate NDE examination:**
- NDE shall be performed per API 650 Section 8 requirements and specification (DEL-13.02)
- Coordinate NDE technician mobilization and examination schedule with fabricator
- **TBD** — NDE extent (spot vs. full examination) per specification (DEL-13.02)

3.2. **Receive NDE reports:**
- NDE technician generates NDE report for each examination (weld joint or section)
- QA inspector receives NDE reports from NDE technician
- Typical NDE report turnaround: 24-48 hours after examination

3.3. **Review NDE reports:**
- For each NDE report, verify:
  - NDE method and procedure reference
  - Weld joint identification (matches weld map)
  - Acceptance criteria reference (API 650 or specification)
  - Examination results (accept/reject)
  - If defects identified: Defect description, size, location
  - NDE technician name, certification level (Level II minimum), signature, date

3.4. **Disposition NDE results:**
- **If weld accepted:** File NDE report in tank dossier; update weld map with NDE report reference
- **If weld rejected (defects exceed acceptance criteria):**
  - Notify fabricator of defect requiring repair
  - Coordinate repair activities (grinding, re-welding per approved repair WPS)
  - Schedule re-examination after repair
  - Receive and review post-repair NDE report
  - Verify post-repair examination shows acceptance
  - File both initial (defect) and post-repair (acceptance) NDE reports in tank dossier
  - Update weld map with repair information and post-repair NDE report reference

3.5. **Track NDE completion:**
- Maintain NDE tracking log showing all weld joints requiring examination and NDE completion status
- Verify all weld joints shown on weld map have corresponding NDE reports before declaring fabrication complete

3.6. **Collect NDE reports for all three tanks:**
- Repeat Steps 3.1-3.5 for Tank TK-101, TK-102, TK-103

**Verification:** QA Manager reviews NDE reports for compliance with acceptance criteria and completeness

**Source:** API 650 Section 8 NDE requirements; typical NDE workflow

---

### Step 4: Document Hydrostatic Test

**Objective:** Perform hydrostatic test per API 650 and document results.

**Actions:**

4.1. **Prepare for hydrostatic test:**
- Verify tank fabrication and erection are complete
- Verify all NDE reports show acceptance (no open defects)
- Coordinate hydrotest timing with client per ITP (DEL-29.02) — typically a hold point requiring client witness
- Review hydrotest water management plan (DEL-29.06) for water source, quality, and disposal

4.2. **Establish baseline settlement measurements:**
- Before filling tank with water, surveyor measures foundation elevations at multiple points around tank perimeter (typically 8 points minimum)
- Record baseline elevation measurements on hydrotest record form

4.3. **Fill tank to test pressure:**
- Test pressure: **TBD** — Per API 650 Section 7.4.1 (typically shell design height plus additional head) and design calculations (DEL-13.03)
- Fill tank with water to achieve test pressure
- Monitor filling rate to avoid overpressure or rapid filling causing foundation settlement issues
- **TBD** — Filling rate and procedure per hydrotest test plan

4.4. **Measure settlement during filling:**
- At intermediate fill levels and at full test pressure, surveyor measures foundation elevations at same points as baseline
- Record settlement measurements on hydrotest record form
- Monitor settlement for excessive or differential settlement indicating foundation problems

4.5. **Hold test pressure:**
- Hold tank at test pressure for minimum 24 hours (typical per API 650 Section 7.4.3)
- During hold period:
  - Monitor settlement for continued movement
  - Perform visual inspection of all welds, nozzles, and shell for leaks
  - Inspect for shell distortion or structural issues
- Client inspector witnesses hold period and inspection
- **TBD** — Hold duration per API 650 and project specification (DEL-13.02)

4.6. **Visual inspection:**
- QA inspector and client inspector perform visual inspection of:
  - All welds (shell, bottom-to-shell, roof, nozzles) for leaks
  - Shell and roof for visible distortion or buckling
  - Foundation for cracking or heaving
- Document inspection results on hydrotest record form

4.7. **Drain tank:**
- After successful hold period and inspection, drain tank
- Monitor draining rate
- Measure final settlement after draining (to verify elastic recovery)

4.8. **Evaluate test results:**
- Evaluate settlement: Maximum differential settlement shall be within API 650 allowable limits (API 650 Section 7.4.4)
- Evaluate visual inspection: No leaks, distortion, or structural damage
- If test is successful: Tank passes hydrotest; complete hydrotest record with acceptance statement
- If test fails (leaks or excessive settlement): Identify and repair defects; re-test after repairs

4.9. **Sign hydrotest record:**
- QA inspector signs hydrotest record certifying test execution and acceptance
- Client inspector signs hydrotest record witnessing test and acceptance
- File completed hydrotest record in tank dossier

4.10. **Perform hydrotest for all three tanks:**
- Repeat Steps 4.1-4.9 for Tank TK-101, TK-102, TK-103

**Verification:** QA Manager reviews hydrotest records for compliance with API 650 requirements

**Source:** API 650 Section 7.4 hydrostatic testing requirements; typical hydrotest procedure

---

### Step 5: Compile Tank Dossiers

**Objective:** Compile all quality records for each tank into organized tank dossier.

**Actions:**

5.1. **Establish dossier structure:**
- Create tank dossier folder for each tank (Tank TK-101 dossier, TK-102 dossier, TK-103 dossier)
- Within each dossier, create sections:
  - Section 1: Material Certificates (MTRs)
  - Section 2: Weld Map
  - Section 3: NDE Reports
  - Section 4: Hydrostatic Test Record
  - Section 5: Cross-Reference Index

5.2. **Compile material certificates:**
- Collect all MTRs for materials used in each specific tank
- Organize MTRs by heat number or material type
- File MTRs in Section 1 of tank dossier

5.3. **File weld map:**
- File final as-built weld map in Section 2 of tank dossier

5.4. **Compile NDE reports:**
- Collect all NDE reports for welds in each specific tank
- Organize NDE reports by weld joint ID (matching weld map)
- Include both initial and post-repair NDE reports (if applicable)
- File NDE reports in Section 3 of tank dossier

5.5. **File hydrostatic test record:**
- File completed hydrotest record in Section 4 of tank dossier

5.6. **Prepare cross-reference index:**
- Create comprehensive index cross-referencing all records in tank dossier:
  - Material heat number → Shell plate location (from weld map) → Weld joint ID → NDE report number
  - Weld joint ID → WPS number → Welder ID → NDE report number
- File index in Section 5 of tank dossier

5.7. **Repeat for all three tanks:**
- Complete tank dossier for Tank TK-101, TK-102, TK-103

**Verification:** QA Manager reviews each tank dossier for completeness and organization

**Source:** Typical as-built documentation compilation practice

---

### Step 6: Verify Record Package

**Objective:** Verify record package completeness, accuracy, and traceability before submission.

**Actions:**

6.1. **Completeness check:**
- For each tank dossier, verify using completeness checklist:
  - All required MTRs are present (all material heats used in tank)
  - Weld map is present and complete (all welds shown)
  - All required NDE reports are present (all weld joints requiring examination have NDE reports)
  - Hydrostatic test record is present and complete
  - Cross-reference index is present
- Identify any missing records
- Obtain missing records before proceeding

6.2. **Accuracy verification:**
- Cross-check material certificates against specification (DEL-13.02):
  - Verify material grades are correct
  - Verify mechanical properties are within specification limits
- Cross-check weld map against design drawings (DEL-13.01):
  - Verify weld joint locations match design
  - Verify nozzle welds are included
- Cross-check NDE reports against API 650 acceptance criteria:
  - Verify all NDE reports show acceptance (no open defects)
- Cross-check hydrotest records against API 650 requirements:
  - Verify test pressure is correct
  - Verify settlement is within allowable limits
  - Verify no leaks or defects observed

6.3. **Traceability verification:**
- Verify traceability chain for sample weld joints:
  - Select 5-10 weld joints per tank (random sampling)
  - Trace material heat number (MTR) → Shell plate location (weld map) → Weld joint ID (weld map) → NDE report number (NDE report)
  - Verify traceability is complete and correct
- If traceability issues are found, correct weld map or index

6.4. **Personnel qualification verification:**
- Verify NDE technician certifications (ASNT Level II or ISO 9712) are current and on file
- Verify welder qualifications (WPQ from DEL-13.06) are current and applicable to WPS used
- **TBD** — Personnel qualification verification checklist

6.5. **Signature verification:**
- Verify all required signatures are present:
  - MTRs: Mill or supplier signature
  - NDE reports: NDE technician signature
  - Hydrotest records: QA inspector and client inspector signatures
- Verify signatures are legible and dated

**Verification:** QA Manager performs independent review of verification results

**Source:** Typical QA record verification process

---

### Step 7: Submit Record Package for Acceptance

**Objective:** Submit completed record package to client for review and acceptance.

**Actions:**

7.1. **Prepare submission package:**
- Compile tank dossiers for all three tanks (TK-101, TK-102, TK-103)
- Prepare cover letter or transmittal summarizing record package content
- Include statement of compliance with API 650, CSA W59, and project specification (DEL-13.02)

7.2. **Internal review and approval:**
- QA Manager reviews complete record package
- Discipline lead (Mechanical) reviews and approves record package for submission

7.3. **Submit to client:**
- Submit record package to client per project submission procedures
- **TBD** — Submission format (electronic PDF dossier, hard copy bound book, both)
- **TBD** — Submission timing (before commissioning, before handover, etc.)
- **Source:** Project document control procedures

7.4. **Address client comments:**
- Receive client review comments (if any)
- Address comments by obtaining missing records, correcting errors, or providing clarifications
- Resubmit revised record package

7.5. **Obtain client acceptance:**
- Receive client acceptance of record package
- File client acceptance letter in project file

**Verification:** QA Manager verifies client acceptance is obtained

**Source:** Typical quality record submission and acceptance process

---

### Step 8: Archive Record Package

**Objective:** Archive final as-built record package for facility lifetime.

**Actions:**

8.1. **Prepare archival package:**
- Finalize tank dossiers with client acceptance
- Verify archival format requirements:
  - **Electronic:** PDF/A format (archival-quality PDF), searchable text, indexed
  - **Hard copy:** Bound books, durable binding, acid-free paper
- **TBD** — Archival format per ER and project document management procedures

8.2. **File in project document management system:**
- Upload final tank dossiers to project document management system
- Categorize as "Quality Records" and "As-Built Documentation"
- Set retention period to facility lifetime

8.3. **Provide archival copies to client:**
- Provide client with archival copies (electronic and/or hard copy per ER)
- **TBD** — Client archival requirements

8.4. **Retain project copy:**
- Retain project copy in D&B Contractor project archive per company records retention policy

**Verification:** QA Manager verifies archival is complete

**Source:** Typical record archival process

---

## Verification

### Verification Activities

**Material Certificate Review (Step 1):**
- Verify material specifications, properties, and certifications

**Weld Map Review (Step 2):**
- Verify completeness and traceability to materials and NDE reports

**NDE Report Review (Step 3):**
- Verify acceptance criteria compliance and technician qualifications

**Hydrotest Record Review (Step 4):**
- Verify test parameters, settlement, inspection results, acceptance

**Completeness Check (Step 6.1):**
- Verify all required records are present

**Accuracy Verification (Step 6.2):**
- Verify record data is accurate and compliant with specifications and codes

**Traceability Verification (Step 6.3):**
- Verify traceability chain from material heat to NDE acceptance

**Source:** Specification.md V-01 through V-05

### Sign-off Requirements

**QA Inspector sign-off:**
- Certifies records are collected, reviewed, and compliant

**QA Manager sign-off:**
- Certifies record package is complete and accurate

**Client Inspector sign-off:**
- Witnesses hydrostatic test and accepts record package

**Discipline Lead sign-off:**
- Approves record package for submission

**Source:** Typical quality record approval workflow

---

## Records

### Documentation Outputs

**Primary outputs:**
- Tank dossiers (3) — One per tank containing all quality records
  - Material certificates (MTRs) — **TBD** quantity (estimated 50-100 total)
  - Weld maps (3) — One per tank
  - NDE reports — **TBD** quantity (estimated 60-150 total)
  - Hydrostatic test records (3) — One per tank

**Supporting records:**
- Completeness checklists
- Accuracy verification checklists
- Traceability verification records
- Personnel qualification records (NDE technician certs, welder certs)
- Client acceptance letter

**Source:** _CONTEXT.md (Anticipated Artifacts); API 650 requirements

### Record Management

**Filing locations:**
- `1_Working/DEL-13.05/` — Work-in-progress records collection
- `2_Checking/To/` — Record package issued for client review (awaiting acceptance)
- `2_Checking/From/` — Record package returned from client review with comments
- `3_Issued/` — Accepted record package (final as-built)
- Project document management system — Electronic archival copies

**Retention requirements:**
- **TBD** — Retention period per ER (typically facility lifetime for quality records)

**Source:** ASSUMPTION based on typical project document control procedures and API 650 record retention requirements

---

## Cross-Document References

**For detailed requirements:** See `Specification.md`
- FR-01 through FR-06 → Implemented in Steps 1-4
- PR-01 through PR-03, QR-01 through QR-04 → Verified in Step 6
- RP-01 through RP-03 → Implemented in Steps 5, 8

**For principles and guidance:** See `Guidance.md`
- DP-01: Quality Evidence Philosophy → Applied throughout all steps
- DP-02: Traceability → Implemented in Steps 2, 5, 6
- DP-03: API 650 Compliance Documentation → Applied in Steps 1, 3, 4, 6
- DP-04: As-Built Documentation → Implemented in Steps 2, 5
- DP-05: Hold and Witness Points → Implemented in Step 4
- Considerations → Inform workflow decisions

**For entity attributes:** See `Datasheet.md`
- Material Certificates, Weld Maps, NDE Reports, Hydrostatic Test Records attributes → Documented in Steps 1-4

---

**Document Status:** Pass 3 (Final) — Enrichment complete. Procedure steps defined with verification points and cross-document references. All TBDs marked. ASSUMPTIONs labeled. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
