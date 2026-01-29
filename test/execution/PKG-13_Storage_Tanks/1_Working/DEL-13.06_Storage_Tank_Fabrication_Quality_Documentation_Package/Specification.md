# Specification: DEL-13.06 Storage Tank Fabrication Quality Documentation Package

## Scope

This specification defines the requirements for **Storage Tank Fabrication Quality Documentation Package** within **PKG-13 Storage Tanks**.

### Deliverable Description

Defines and substantiates storage tank fabrication quality documentation package in accordance with ER requirements.

**Source:** _CONTEXT.md, Decomposition document DEL-13.06

### Coverage

**Included:**
- Welding Procedure Specifications (WPS) — Qualified welding procedures for all weld types
- Procedure Qualification Records (PQR) — Test results qualifying welding procedures
- Welder Qualification Records (WPQ) — Test results qualifying individual welders
- Shop inspection reports documenting fabrication conformance
- Material Test Reports (MTRs) for all tank materials
- Impact test results (if required for low-temperature or seismic design)
- NDE reports documenting weld examinations during shop fabrication
- Weld inspection records documenting in-process visual inspections
- Fabricator qualification documentation (CSA W47.1 certification or equivalent — **TBD**)

**Source:** _CONTEXT.md (Anticipated Artifacts), API 650 and CSA W59 fabrication quality documentation requirements

**Excluded:**
- Field installation and erection records — covered by DEL-13.05 (some overlap with MTRs and NDE reports)
- Hydrostatic test records — covered by DEL-13.05
- Design calculations and drawings — covered by DEL-13.01, DEL-13.03
- As-built weld maps — covered by DEL-13.05 (weld maps reference WPS in this package)

**Source:** ASSUMPTION based on deliverable scope and decomposition package structure

---

## Requirements

### Functional Requirements

**FR-01: WPS/PQR/WPQ Requirements**

- **WPS (Welding Procedure Specifications):**
  - Fabricator shall develop and qualify WPS for all welding processes, materials, and joint configurations used in tank fabrication
  - Each WPS shall comply with API 650 Section 8.2 and/or CSA W59 Section 5
  - Minimum WPS content: Base metal specification and thickness range, filler metal, welding process, joint design, preheat/interpass temperature, heat input, PWHT (if applicable), PQR reference
  - WPS shall be reviewed and approved by D&B Contractor before use
  - **TBD** — Number of WPS required (estimated 3-10 depending on materials and configurations)
  - **Source:** API 650 Section 8.2; CSA W59 Section 5

- **PQR (Procedure Qualification Records):**
  - Each WPS shall be supported by valid PQR demonstrating procedure adequacy
  - PQR shall document actual welding parameters used in qualification test and test results
  - Minimum tests: Visual examination, NDE (RT or UT), tensile test, guided bend tests; impact tests if required
  - PQR shall meet API 650 Section 8.2.4 and/or CSA W59 Section 5.2 acceptance criteria
  - **TBD** — PQR testing laboratory qualification requirements
  - **Source:** API 650 Section 8.2.4; CSA W59 Section 5.2

- **WPQ (Welder Qualification Records):**
  - Each welder shall be qualified per API 650 Section 8.2.5 and/or CSA W59 Section 6 before performing production welding
  - WPQ shall document welder qualification test configuration and results
  - Minimum tests: Visual examination, NDE (RT or UT), guided bend test
  - WPQ shall meet API 650 Section 8.2.5 and/or CSA W59 Section 6 acceptance criteria
  - Welder qualifications shall remain current (no 6-month gap in welding activity)
  - **TBD** — Number of welders and WPQs required
  - **Source:** API 650 Section 8.2.5; CSA W59 Section 6

**FR-02: Shop Inspection Requirements**

- Shop inspections shall be conducted by D&B Contractor QA inspector or qualified third-party inspector during fabrication
- Inspection frequency: **TBD** — Per ITP (DEL-29.02); typically daily or weekly during active fabrication
- Shop inspection reports shall document:
  - Fabrication activities observed
  - Conformance to design drawings (DEL-13.01) and specification (DEL-13.02)
  - Non-conformances identified
  - Corrective actions taken
  - Inspector signature and date
- Non-conformances shall be tracked to closure with documented corrective action
- **TBD** — Inspector qualification requirements (CWB certified welding inspector or equivalent)
- **Source:** Typical shop inspection practice for API 650 tanks

**FR-03: Material Documentation Requirements**

- **MTRs (Material Test Reports):**
  - MTRs shall be provided for all pressure-retaining and structural materials per API 650 Section 2.2
  - MTR content requirements: Material specification, heat number, chemical composition, mechanical properties, test results, certifier signature
  - MTRs shall demonstrate material compliance with specification (DEL-13.02)
  - **Source:** API 650 Section 2.2

- **Impact Test Results (if required):**
  - Impact tests shall be performed if tank operates below -29°C or if required by ER for seismic design per API 650 Section 2.2.11 or Appendix E
  - Impact test content requirements: Heat number, test temperature, test specimen orientation, impact energy values (3 specimens per test), acceptance criteria, test lab certification
  - Impact tests shall meet API 650 Section 2.2.11 acceptance criteria
  - **TBD** — Applicability of impact testing per operating temperature and seismic design requirements
  - **Source:** API 650 Section 2.2.11; API 650 Appendix E

**FR-04: NDE Documentation Requirements**

- NDE reports from shop fabrication shall be included in fabrication quality documentation package
- NDE extent, methods, and acceptance criteria per API 650 Section 8 and specification (DEL-13.02)
- NDE report content: Method, procedure, weld joint ID, acceptance criteria, results, technician certification, signature
- **Note:** NDE reports are also part of DEL-13.05; included here to demonstrate fabrication process quality
- **Source:** API 650 Section 8

**FR-05: Weld Inspection Requirements**

- In-process visual weld inspections shall be performed during fabrication per API 650 Section 8 and CSA W59 Section 12
- Weld inspection records shall document visual inspection criteria (undercut, porosity, spatter, profile), acceptance/rejection, inspector signature, date
- Weld inspection records may be included in shop inspection reports or documented separately
- **Source:** API 650 Section 8; CSA W59 Section 12

### Performance Requirements

**PR-01: Fabricator Qualification**

- Fabricator shall be qualified to fabricate API 650 tanks
- **TBD** — Fabricator qualification requirements: CSA W47.1 certification (for Canadian project), API 650 experience, quality system certification (ISO 9001), shop audit by D&B Contractor
- **Source:** API 650 fabricator requirements; ASSUMPTION (CSA W47.1 for Canadian project)

**PR-02: Welding Procedure Adequacy**

- All WPS shall be qualified per API 650 Section 8.2 and/or CSA W59 Section 5
- PQRs shall demonstrate procedure adequacy through destructive testing
- **Source:** API 650 Section 8.2; CSA W59 Section 5

**PR-03: Welder Competency**

- All welders shall be qualified per API 650 Section 8.2.5 and/or CSA W59 Section 6
- Welder qualifications shall be current and applicable to work performed
- **Source:** API 650 Section 8.2.5; CSA W59 Section 6

**PR-04: Material Compliance**

- All materials shall meet specification (DEL-13.02) requirements as evidenced by MTRs
- Impact test results (if required) shall meet API 650 Section 2.2.11 acceptance criteria
- **Source:** API 650 Section 2.2

**PR-05: Fabrication Conformance**

- Fabrication shall conform to design drawings (DEL-13.01) and specification (DEL-13.02) as evidenced by shop inspection reports
- Non-conformances shall be dispositioned and closed before tank shipment
- **Source:** Typical fabrication quality requirements

### Quality Requirements

**QR-01: Document Completeness**

- All required documents shall be provided (WPS, PQR, WPQ, shop inspection reports, MTRs, impact tests if applicable, NDE reports, weld inspection records)
- All data fields on each document shall be completed
- **TBD** — Completeness checklist per project quality procedures

**QR-02: Document Accuracy**

- All data shall be accurate and verified
- Signatures shall be authentic and from qualified personnel
- Test results shall be from accredited laboratories or qualified technicians

**QR-03: Personnel Qualification**

- Welding engineers qualifying procedures shall be qualified per AWS or equivalent
- Welders shall be qualified per WPQ records
- NDE technicians shall be certified per ASNT SNT-TC-1A or ISO 9712
- Inspectors shall be qualified per project requirements (**TBD** — CWB certified welding inspector or equivalent)

**QR-04: Standards Compliance**

- All documentation shall demonstrate compliance with API 650, CSA W59, and project specification (DEL-13.02)

---

## Standards

### Primary Standards

| Standard | Title | Application |
|----------|-------|-------------|
| **API 650** | Welded Tanks for Oil Storage | Fabrication, welding, material, and quality requirements (Source: Decomposition PKG-13 Scope; Sections 2.2, 8) |
| **CSA W59** | Welded Steel Construction (Metal Arc Welding) | Welding procedure and welder qualification requirements for Canadian project (Source: ASSUMPTION) |

### Supporting Standards

| Standard | Title | Application |
|----------|-------|-------------|
| **CSA W47.1** | Certification of Companies for Fusion Welding of Steel | Fabricator certification requirement (Source: ASSUMPTION for Canadian project) |
| **AWS** | American Welding Society standards | Welding engineer qualification and procedure qualification (Source: ASSUMPTION) |
| **ASTM A370** | Standard Test Methods and Definitions for Mechanical Testing of Steel Products | Impact testing methods (Source: ASSUMPTION) |
| **ASNT SNT-TC-1A** or **ISO 9712** | NDE Personnel Qualification and Certification | NDE technician qualification (Source: ASSUMPTION) |
| **ISO 9001** | Quality Management Systems | Fabricator quality system certification (Source: ASSUMPTION) |

**Note:** All standards marked ASSUMPTION require confirmation during design development and ER extraction.

### Employer's Requirements

- Volume 2 Part 2: Employer's Requirements - Civil & Process Mechanical Works — **Location TBD**
- **TBD** — Specific ER clauses applicable to fabrication quality documentation

---

## Verification

### Document Package Verification Methods

**V-01: Completeness Check**
- Verify all required documents are present per checklist
- Identify missing documents or incomplete documents
- **TBD** — Completeness checklist per project quality procedures

**V-02: WPS/PQR/WPQ Technical Review**
- Welding engineer reviews WPS for compliance with API 650/CSA W59 and specification (DEL-13.02)
- Welding engineer reviews PQR for test adequacy and acceptance criteria compliance
- QA reviews WPQ for welder qualification compliance
- **TBD** — Technical review checklist

**V-03: Shop Inspection Report Review**
- QA manager reviews shop inspection reports for completeness and conformance tracking
- Verify all non-conformances are dispositioned and closed
- **TBD** — Non-conformance closure verification

**V-04: Material Documentation Review**
- QA engineer reviews MTRs for material specification compliance
- QA engineer reviews impact test results (if applicable) for acceptance criteria compliance
- **TBD** — Material acceptance checklist

**V-05: NDE and Weld Inspection Review**
- QA engineer reviews NDE reports for acceptance criteria compliance
- QA engineer reviews weld inspection records for conformance
- **TBD** — NDE and weld inspection review checklist

### Acceptance Criteria

**AC-01: Completeness**
- All required documents are provided
- All data fields are completed

**AC-02: Compliance**
- WPS/PQR/WPQ comply with API 650/CSA W59 requirements
- Materials comply with specification (DEL-13.02) per MTRs and impact tests
- Fabrication conforms to drawings and specification per shop inspection reports
- Welds comply with acceptance criteria per NDE reports and weld inspection records

**AC-03: Qualification**
- Fabricator is qualified per project requirements
- Welding procedures are qualified per PQRs
- Welders are qualified per WPQs
- NDE technicians are certified
- Inspectors are qualified

**AC-04: Traceability**
- WPS are traceable to PQRs
- Welds are traceable to WPS and welders (via weld map in DEL-13.05)
- Materials are traceable to MTRs (via weld map in DEL-13.05)

**AC-05: Approval**
- D&B Contractor QA and welding engineer have reviewed and approved documentation package
- Client has reviewed and accepted documentation package (if required per ER)
- **TBD** — Client acceptance requirements per ER

---

## Documentation

### Required Document Outputs

| Document Type | Quantity | Description |
|---------------|----------|-------------|
| **Welding Procedure Specifications (WPS)** | **TBD** (estimated 3-10) | Qualified welding procedures for all weld types |
| **Procedure Qualification Records (PQR)** | **TBD** (estimated 3-10) | Test results qualifying each WPS |
| **Welder Qualification Records (WPQ)** | **TBD** (estimated 10-40) | Test results qualifying each welder for each process/position |
| **Shop Inspection Reports** | **TBD** (estimated 30-90 total for 3 tanks) | Fabrication conformance documentation |
| **Material Test Reports (MTRs)** | **TBD** (estimated 50-100) | Mill test reports for all materials |
| **Impact Test Results** | **TBD** (if applicable) | Impact test results for low-temperature or seismic materials |
| **NDE Reports** | **TBD** (estimated 60-150 total for 3 tanks) | Shop fabrication NDE reports |
| **Weld Inspection Records** | **TBD** (may be included in shop inspection reports) | In-process visual weld inspection records |

**Source:** _CONTEXT.md (Anticipated Artifacts); API 650 and CSA W59 requirements

### Document Package Organization

**DP-01: Package Structure**
- Section 1: Fabricator Qualification Documentation (CSA W47.1 certificate or equivalent)
- Section 2: Welding Procedure Documentation (WPS, PQR)
- Section 3: Welder Qualification Documentation (WPQ)
- Section 4: Shop Inspection Reports (organized by tank)
- Section 5: Material Documentation (MTRs, impact test results organized by tank)
- Section 6: NDE and Weld Inspection Documentation (organized by tank)
- Section 7: Index and Cross-Reference

**DP-02: Document Management**
- All documents shall be managed per project document control procedures
- Electronic master copies maintained in project document management system
- **TBD** — Document management system and procedures

**DP-03: Submission**
- Pre-fabrication submission: WPS/PQR/WPQ for review and approval
- During-fabrication submission: Shop inspection reports, MTRs, impact tests, NDE reports submitted progressively
- Post-fabrication submission: Complete package compiled and submitted for final acceptance
- **TBD** — Submission timing and format per ER and project procedures

**DP-04: Archive and Retention**
- Final fabrication quality documentation package archived for facility lifetime
- **TBD** — Archive location (client archive, project archive) and format (electronic, hard copy, both)
- **TBD** — Retention period per ER (typically facility lifetime)

---

## Cross-Document References

**For entity attributes and values:** See `Datasheet.md`
- WPS, PQR, WPQ, Shop Inspection Reports, MTRs, Impact Test Results, NDE Reports, Weld Inspection Records attributes → Referenced in FR-01 through FR-05
- Document Package Configuration → Referenced in DP-01

**For fabrication quality documentation principles:** See `Guidance.md`
- DP-01: Fabricator Qualification Philosophy → Supports PR-01
- DP-02: Welding Procedure Qualification → Supports FR-01, PR-02, PR-03
- DP-03: API 650 and CSA W59 Compliance Documentation → Supports all functional requirements
- Trade-offs → Support documentation depth and third-party vs. self-inspection decisions

**For verification and production:** See `Procedure.md`
- Section: Verification → Implements V-01 through V-05
- Steps 1-6 → Produce WPS/PQR/WPQ, shop inspection reports, material documentation, NDE documentation, weld inspection records to meet requirements specified here
- Step 7 → Compile and validate document package per requirements here
- Step 8 → Submit for approval and archive per requirements here

---

**Document Status:** Pass 3 (Final) — Enrichment complete. Functional, performance, and quality requirements defined and linked to Datasheet attributes and Guidance rationale. Verification methods specified and aligned with Procedure. All TBDs marked. ASSUMPTIONs labeled. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
