# Specification: DEL-13.05 Storage Tank Installation & Test Records

## Scope

This specification defines the requirements for **Storage Tank Installation & Test Records** within **PKG-13 Storage Tanks**.

### Deliverable Description

Provides evidence of completion, inspection, and testing for storage tank.

**Source:** _CONTEXT.md, Decomposition document DEL-13.05

### Coverage

**Included:**
- Material certificates (Mill Test Reports) for all tank materials (shell, bottom, roof, nozzles, structural steel)
- Weld maps showing all weld joints with traceability to NDE reports and welder qualifications
- NDE reports (radiographic, ultrasonic, magnetic particle, vacuum box) for all examined welds per API 650
- Hydrostatic test records documenting successful completion of tank water pressure testing
- Traceability between records (material heat → weld joint → NDE report → acceptance)
- As-built documentation of repairs and modifications

**Source:** _CONTEXT.md (Anticipated Artifacts), API 650 quality documentation requirements

**Excluded:**
- Fabrication quality documentation (WPS/PQR/WPQ, shop inspection reports, impact test results) — covered by DEL-13.06
- Design calculations and drawings — covered by DEL-13.01, DEL-13.02, DEL-13.03
- Commissioning records — covered by PKG-30
- Operational records — not part of construction deliverables

**Source:** ASSUMPTION based on deliverable scope and decomposition package structure

---

## Requirements

### Functional Requirements

**FR-01: Material Certificate Requirements**
- Material certificates (MTRs) shall be provided for all pressure-retaining and structural materials
- Minimum materials requiring certification:
  - Shell plates (all heats used)
  - Bottom plates (all heats used)
  - Roof plates (all heats used)
  - Nozzle forgings and pipes
  - Structural steel (roof structure, stiffeners, wind girders, if applicable)
  - Bolts and fasteners (anchor bolts, roof bolts)
- Each certificate shall include: Material specification, heat number, chemical composition, mechanical properties (yield, tensile, elongation), impact test results (if applicable), supplier/mill certification
- Certificates shall be traceable to specific tank components via weld map heat tracking
- **TBD** — Specific material grades and ASTM standards per specification (DEL-13.02)
- **Source:** API 650 Section 2.2; typical material certification requirements

**FR-02: Weld Map Requirements**
- One comprehensive weld map shall be provided for each tank (3 total)
- Weld map shall show all welded joints including:
  - Vertical shell seams
  - Horizontal shell seams (circumferential)
  - Bottom-to-shell weld (annular plate and bottom plate welds)
  - Roof welds (roof plate seams, roof-to-shell weld)
  - Nozzle-to-shell welds
  - Structural attachment welds (if applicable)
- For each weld joint, weld map shall identify:
  - Weld joint unique identification number
  - Weld procedure specification (WPS) number
  - Welder identification
  - Weld date
  - Material heat numbers (both sides of joint)
  - NDE report reference number
- Weld map shall be updated as-built to reflect repair welds and field modifications
- **Source:** API 650 Section 8; CSA W59 welding documentation; typical QA practice

**FR-03: NDE Report Requirements**
- NDE shall be performed per API 650 Section 8 requirements:
  - Vertical shell joints: Spot radiographic or full radiographic examination per API 650 Table 8-1
  - Horizontal shell joints: Spot radiographic or full radiographic examination per API 650 Table 8-1
  - Bottom-to-shell weld: Full vacuum box or liquid penetrant examination
  - Roof welds: Visual examination (radiographic if required by design or ER)
  - Nozzle welds: Magnetic particle or liquid penetrant examination
- Each NDE report shall include:
  - NDE method (RT, UT, MT, PT, vacuum box)
  - Procedure reference
  - Weld joint identification (traceable to weld map)
  - Acceptance criteria reference (API 650 or project specification)
  - Examination results (accept/reject, defect description if applicable)
  - Repair actions (if defects found)
  - NDE technician name, certification level, signature
- Defects requiring repair shall be documented with repair procedure and re-examination results
- **TBD** — NDE extent (spot vs. full examination) per project specification (DEL-13.02) and ER
- **Source:** API 650 Section 8; typical NDE documentation practice

**FR-04: Hydrostatic Test Record Requirements**
- Each tank shall be hydrostatically tested per API 650 Section 7.4
- One hydrostatic test record shall be produced for each tank (3 total)
- Test pressure: **TBD** — Per API 650 Section 7.4.1 (typically shell design height plus additional head)
- Test duration: Minimum 24 hours hold time at test pressure (typical per API 650 Section 7.4.3)
- Each hydrostatic test record shall include:
  - Tank tag number
  - Test date (start and end)
  - Test pressure (applied and duration)
  - Water source and water quality (coordination with DEL-29.06)
  - Settlement measurements:
    - Baseline (before filling)
    - During filling
    - At test pressure
    - After draining
  - Visual inspection results (leaks, distortion, structural issues)
  - Acceptance statement
  - Inspector signature (D&B Contractor QA and client witness — **TBD**)
- Settlement shall be within API 650 allowable limits
- No leaks, visible distortion, or structural damage shall be observed
- **TBD** — Client witness requirements per ER and ITP (DEL-29.02)
- **Source:** API 650 Section 7.4; typical hydrotest documentation practice

**FR-05: Traceability Requirements**
- Records shall provide complete traceability from material procurement through testing:
  - Material heat number → Shell plate location (weld map) → Weld joint ID → NDE report → Acceptance
- Tank dossier index shall provide cross-reference between all record types
- **Source:** Typical quality assurance traceability requirements

**FR-06: As-Built Documentation**
- Records shall reflect as-built conditions including all repairs, modifications, and deviations from design
- Weld map shall be updated with repair weld locations and re-examination results
- NDE reports shall document all repair cycles until acceptance
- **TBD** — Design change documentation and deviation approval process
- **Source:** Typical as-built documentation requirements

### Performance Requirements

**PR-01: Material Compliance**
- All materials shall meet specification (DEL-13.02) requirements as evidenced by MTRs
- Material properties (yield, tensile, elongation, chemical composition) shall be within specified limits
- Impact test results (if required) shall meet specification requirements
- **Source:** API 650 Section 2.2; specification (DEL-13.02)

**PR-02: Weld Quality**
- All welds shall meet API 650 Section 8 acceptance criteria as evidenced by NDE reports
- Defects exceeding acceptance criteria shall be repaired and re-examined
- **Source:** API 650 Section 8

**PR-03: Hydrostatic Test Acceptance**
- Tank shall hold test pressure for specified duration without leaks
- Settlement shall be within API 650 allowable limits
- No visible distortion or structural damage
- **Source:** API 650 Section 7.4

### Quality Requirements

**QR-01: Record Completeness**
- All required records shall be provided (no missing MTRs, weld maps, NDE reports, or hydrotest records)
- All data fields on each record shall be completed (no blank required fields)
- **TBD** — Completeness checklist per project quality procedures

**QR-02: Record Accuracy**
- All data shall be accurate and verified
- Signatures shall be authentic and from qualified personnel
- Dates and timestamps shall be accurate

**QR-03: Personnel Qualification**
- NDE technicians shall be certified per ASNT SNT-TC-1A or ISO 9712 Level II minimum
- Welders shall be qualified per WPQ records (DEL-13.06)
- Inspectors shall be qualified per project quality procedures
- **TBD** — Inspector qualification requirements per ER

**QR-04: Document Control**
- All records shall be revision-controlled
- Superseded records (e.g., before-repair NDE reports) shall be retained but clearly marked as superseded
- Final as-built record package shall be clearly identified

---

## Standards

### Primary Standards

| Standard | Title | Application |
|----------|-------|-------------|
| **API 650** | Welded Tanks for Oil Storage | Material, welding, NDE, and hydrostatic testing requirements (Source: Decomposition PKG-13 Scope; Section 2.2, 7.4, 8) |

### Supporting Standards

| Standard | Title | Application |
|----------|-------|-------------|
| **CSA W59** | Welded Steel Construction (Metal Arc Welding) | Weld documentation and inspection requirements (Source: ASSUMPTION) |
| **ASNT SNT-TC-1A** or **ISO 9712** | NDE Personnel Qualification and Certification | NDE technician qualification (Source: ASSUMPTION) |
| **ASTM Material Standards** | Various (e.g., A36, A283, A572 for plates) | Material specifications and testing requirements (Source: ASSUMPTION based on typical API 650 materials) |

**Note:** All standards marked ASSUMPTION require confirmation during design development and ER extraction.

### Employer's Requirements

- Volume 2 Part 2: Employer's Requirements - Civil & Process Mechanical Works — **Location TBD**
- **TBD** — Specific ER clauses applicable to quality records and testing

---

## Verification

### Record Verification Methods

**V-01: Completeness Check**
- Verify all required records are present per checklist
- Verify all data fields on each record are completed
- Identify missing records or incomplete records
- **TBD** — Completeness checklist per project quality procedures

**V-02: Data Accuracy Verification**
- Cross-check material certificates against material specification (DEL-13.02)
- Cross-check weld map against design drawings (DEL-13.01) and NDE reports
- Cross-check NDE reports against API 650 acceptance criteria
- Cross-check hydrotest records against API 650 test requirements
- **TBD** — Data verification checklist per project quality procedures

**V-03: Traceability Verification**
- Verify traceability from material heat number → weld map → NDE report
- Verify all weld joints shown on weld map have corresponding NDE reports
- Verify all NDE reports reference valid weld joint IDs from weld map
- **TBD** — Traceability verification protocol

**V-04: Witness Signature Verification**
- Verify all required signatures are present
- Verify signatories are qualified per project requirements
- **TBD** — Signature verification and qualification check protocol

**V-05: Archival Format Compliance**
- Verify records are in acceptable archival format (legible, durable, reproducible)
- Verify electronic records are in approved file formats
- **TBD** — Archival format requirements per project document management procedures

### Acceptance Criteria

**AC-01: Completeness**
- All required records are provided
- All data fields are completed or marked N/A with justification
- Traceability is complete

**AC-02: Compliance**
- Materials comply with specification (DEL-13.02) per MTRs
- Welds comply with API 650 acceptance criteria per NDE reports
- Hydrostatic test complies with API 650 requirements per hydrotest records

**AC-03: Qualification**
- All NDE technicians are certified per ASNT SNT-TC-1A or ISO 9712
- All welders are qualified per WPQ records (DEL-13.06)
- All inspectors are qualified per project requirements

**AC-04: Quality**
- Records are legible, accurate, and authentic
- Signatures are present and verified
- Revisions and repairs are properly documented

**AC-05: Approval**
- D&B Contractor QA has reviewed and accepted record package
- Client has reviewed and accepted record package (if required per ER)
- **TBD** — Client acceptance requirements per ER

---

## Documentation

### Required Record Outputs

| Record Type | Quantity | Description |
|-------------|----------|-------------|
| **Material Certificates (MTRs)** | **TBD** (estimated 50-100 total) | All pressure-retaining and structural materials |
| **Weld Maps** | 3 | One per tank showing all welds with traceability |
| **NDE Reports** | **TBD** (estimated 60-150 total) | All NDE examinations per API 650 |
| **Hydrostatic Test Records** | 3 | One per tank documenting successful hydrotest |

**Source:** _CONTEXT.md (Anticipated Artifacts); API 650 requirements

### Record Package Organization

**RP-01: Tank Dossiers**
- Organize records by tank (Tank TK-101 dossier, Tank TK-102 dossier, Tank TK-103 dossier)
- Each dossier contains all records for that tank

**RP-02: Dossier Index**
- Each tank dossier shall include comprehensive index cross-referencing all records
- Index shall support traceability (material heat → weld joint → NDE report)

**RP-03: Electronic and Hard Copy**
- **TBD** — Electronic format requirements (PDF dossier, document management system folder, etc.)
- **TBD** — Hard copy requirements (bound book, three-ring binder, etc.)
- **Source:** Project document management procedures

### Record Management

**RM-01: Document Control**
- All records shall be managed per project document control procedures
- Electronic master copies maintained in project document management system
- **TBD** — Document management system and procedures

**RM-02: Submission**
- Record package submitted for client acceptance per ER requirements
- **TBD** — Submission timing (before commissioning, before handover, etc.) and format

**RM-03: Archive and Retention**
- Final as-built record package archived for facility lifetime
- **TBD** — Archive location (client archive, project archive, third-party archive)
- **TBD** — Retention period per ER (typically facility lifetime)

---

## Cross-Document References

**For entity attributes and values:** See `Datasheet.md`
- Material Certificates, Weld Maps, NDE Reports, Hydrostatic Test Records attributes → Referenced in FR-01 through FR-04
- Record Package Configuration → Referenced in RP-01 through RP-03

**For record generation principles:** See `Guidance.md`
- DP-01: Quality Evidence Philosophy → Supports FR-01 through FR-06
- DP-02: Traceability → Supports FR-05, V-03
- DP-03: API 650 Compliance Documentation → Supports all functional requirements
- Trade-offs → Support record detail level and format selections

**For verification and production:** See `Procedure.md`
- Section: Verification → Implements V-01 through V-05 (completeness, accuracy, traceability, signature, archival format checks)
- Steps 1-4 → Produce material certificates, weld maps, NDE reports, hydrotest records to meet requirements specified here
- Step 5 → Compile and validate record package per requirements here
- Step 6 → Submit for acceptance per requirements here

---

**Document Status:** Pass 3 (Final) — Enrichment complete. Functional, performance, and quality requirements defined and linked to Datasheet attributes and Guidance rationale. Verification methods specified and aligned with Procedure. All TBDs marked. ASSUMPTIONs labeled. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
