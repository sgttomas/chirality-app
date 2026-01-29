# Specification: DEL-13.04 Storage Tank Data Sheet Package

## Scope

This specification defines the requirements for **Storage Tank Data Sheet Package** within **PKG-13 Storage Tanks**.

### Deliverable Description

Defines and substantiates storage tank in accordance with ER requirements.

**Source:** _CONTEXT.md, Decomposition document DEL-13.04

### Coverage

**Included:**
- Tank data sheets (3) for 3 × 15,000 MT CSD canola oil storage tanks
- Agitator data sheets (3) for tank mixing equipment
- Overflow protection data sheets for tank overfill protection systems
- Equipment tags, service descriptions, operating parameters
- Dimensional and performance data
- Material specifications and vendor information
- Electrical and control interfaces

**Source:** _CONTEXT.md (Anticipated Artifacts), Decomposition PKG-13 Scope

**Excluded:**
- Detailed design calculations (covered by DEL-13.03)
- Detailed design drawings (covered by DEL-13.01)
- Technical specifications for equipment design (covered by DEL-13.02)
- Installation and test records (covered by DEL-13.05)
- Fabrication quality documentation (covered by DEL-13.06)
- Process flow diagrams (covered by process design deliverables)

**Source:** ASSUMPTION based on deliverable type (Data Sheet) and decomposition package structure

---

## Requirements

### Functional Requirements

**FR-01: Tank Data Sheet Content**
- Each tank data sheet shall provide complete technical data for one storage tank
- Minimum content: Tag number, service, capacity, dimensions, materials, nozzle summary, operating conditions
- Data sheet shall reference design drawings (DEL-13.01), calculations (DEL-13.03), and specification (DEL-13.02)
- **TBD** — Specific data fields and template format per project standards
- **Source:** Typical tank data sheet practice; _CONTEXT.md (Anticipated Artifacts)

**FR-02: Agitator Data Sheet Content**
- Each agitator data sheet shall provide complete technical data for one agitator unit
- Minimum content: Tag number, service, tank tag, type, manufacturer/model, impeller data, motor data, mounting, electrical interface
- Agitator data sheet shall incorporate vendor-supplied information
- **TBD** — Specific data fields and vendor data requirements per specification (DEL-13.02)
- **Source:** Typical agitator data sheet practice; _CONTEXT.md (Anticipated Artifacts)

**FR-03: Overflow Protection Data Sheet Content**
- Overflow protection data sheet(s) shall provide complete technical data for overfill protection system
- Minimum content: System type, set points, alarm configuration, instrumentation, interlock logic, overflow capacity
- **TBD** — Single system data sheet or one per tank
- **Source:** Typical overflow protection documentation; Decomposition PKG-13 Scope

**FR-04: Equipment Identification**
- All data sheets shall include unique equipment tag numbers per project tagging system
- Tag numbers shall be consistent with P&IDs, drawings, and other project documentation
- **TBD** — Project tagging system and numbering convention
- **Source:** ASSUMPTION based on typical project tagging requirements

**FR-05: Cross-Reference Integrity**
- Data sheets shall cross-reference related equipment (e.g., agitator data sheet references tank tag)
- Data sheets shall reference source documents (drawings, calculations, specifications)
- **TBD** — Cross-reference format and referencing protocol
- **Source:** Typical data sheet practice

### Performance Requirements

**PR-01: Data Accuracy**
- All technical data shall be accurate and verified against design documents
- Dimensional data shall be consistent with design calculations (DEL-13.03) and drawings (DEL-13.01)
- Material specifications shall be consistent with specification (DEL-13.02)
- Operating parameters shall be consistent with process design
- **Source:** Typical data sheet accuracy requirements

**PR-02: Data Completeness**
- All required data fields shall be populated (no blank fields for required information)
- Missing data shall be clearly marked **TBD** with explanation
- **TBD** — Required vs. optional field definitions per project standards
- **Source:** Typical data sheet quality requirements

**PR-03: Units and Nomenclature**
- All units shall be consistent with project standards
- Nomenclature shall be consistent with project conventions
- **TBD** — Project unit system (SI, Imperial, or mixed) and nomenclature standards
- **Source:** ASSUMPTION based on typical project requirements

**PR-04: Vendor Data Integration**
- Vendor-supplied data for agitators shall be integrated into data sheets
- Vendor data shall be validated against specification (DEL-13.02) requirements
- Discrepancies between vendor data and project requirements shall be identified and resolved
- **Source:** Typical vendor data coordination workflow

### Data Sheet Format and Quality Requirements

**DR-01: Data Sheet Format**
- Data sheets shall be produced using project-approved template
- Format shall comply with project document management requirements
- **TBD** — Data sheet template format (Excel, PDF form, database export, etc.)
- **Source:** ASSUMPTION based on typical project requirements

**DR-02: Revision Control**
- Data sheets shall be revision controlled per project document control procedures
- Revision history shall be maintained on each data sheet
- **TBD** — Revision numbering system and change tracking protocol
- **Source:** ASSUMPTION based on typical project requirements

**DR-03: Data Sheet Numbering**
- Data sheet numbers shall follow project numbering system
- **TBD** — Project data sheet numbering convention
- **Source:** ASSUMPTION based on typical project requirements

**DR-04: Data Sheet Quality**
- Data sheets shall be checked and approved per project quality procedures
- Minimum checking requirements: Self-check, interdisciplinary check (piping, instrumentation, electrical)
- **Source:** Typical engineering data sheet quality control process

**DR-05: Vendor Data Integration**
- Agitator vendor data shall be obtained from qualified vendors
- Vendor data shall include manufacturer's certification and compliance statements
- **TBD** — Vendor data submission requirements and format
- **Source:** Typical vendor data coordination process

### Interface Requirements

**IR-01: Design Drawing Interface**
- Tank data sheets shall be consistent with tank general arrangements (DEL-13.01)
- Nozzle data shall match nozzle schedules (DEL-13.01)
- Dimensional data shall match foundation drawings
- **Source:** DEL-13.01 relationship

**IR-02: Design Calculation Interface**
- Tank capacity and sizing data shall be consistent with design calculations (DEL-13.03)
- Operating parameters shall be consistent with process design basis
- **Source:** DEL-13.03 relationship

**IR-03: Technical Specification Interface**
- Material specifications shall be consistent with specification (DEL-13.02)
- Performance requirements shall be consistent with specification (DEL-13.02)
- **Source:** DEL-13.02 relationship

**IR-04: Piping Interface**
- Nozzle data shall be consistent with piping design (PKG-14)
- Line numbers and service descriptions shall match P&IDs
- **TBD** — Piping interface verification protocol
- **Source:** Typical tank-piping interface coordination

**IR-05: Instrumentation Interface**
- Instrumentation connections and tag numbers shall be consistent with instrumentation design (PKG-20)
- Level, temperature, pressure instrumentation shall match instrument data sheets
- **TBD** — Instrumentation interface verification protocol
- **Source:** Typical tank-instrumentation interface coordination

**IR-06: Electrical Interface**
- Agitator electrical supply data shall be consistent with electrical design (PKG-17)
- Motor data shall match motor control center schedules
- **TBD** — Electrical interface verification protocol
- **Source:** Typical electrical interface coordination

**IR-07: Control Systems Interface**
- Agitator control interface and overflow protection alarm/interlock logic shall be consistent with control system design (PKG-19)
- Tag numbers shall match control system database
- **TBD** — Control systems interface verification protocol
- **Source:** Typical control systems interface coordination

---

## Standards

### Primary Standards

| Standard | Title | Application |
|----------|-------|-------------|
| **API 650** | Welded Tanks for Oil Storage | Tank design basis and data sheet content (Source: Decomposition PKG-13 Scope) |

### Supporting Standards

| Standard | Title | Application |
|----------|-------|-------------|
| **ASME B31.3** | Process Piping | Nozzle rating and piping interface data (Source: ASSUMPTION) |
| **IEEE / NEMA** | Electrical Equipment Standards | Agitator motor data (Source: ASSUMPTION) |

**Note:** All standards marked ASSUMPTION require confirmation during design development and ER extraction.

### Employer's Requirements

- Volume 2 Part 2: Employer's Requirements - Civil & Process Mechanical Works — **Location TBD**
- **TBD** — Specific ER clauses applicable to equipment data sheets require extraction

---

## Verification

### Data Sheet Verification Methods

**V-01: Self-Check**
- Originator reviews data sheet for completeness, accuracy, and compliance with template
- **TBD** — Self-check checklist and criteria per project quality procedures

**V-02: Design Document Cross-Check**
- Verify data sheet content against design drawings (DEL-13.01), calculations (DEL-13.03), and specifications (DEL-13.02)
- Identify and resolve discrepancies
- **TBD** — Cross-check protocol and documentation

**V-03: Interdisciplinary Check (IDC)**
- Affected disciplines review data sheets for interface coordination
- Minimum disciplines: Process (piping), Electrical, Instrumentation & Control
- **TBD** — IDC process and sign-off requirements

**V-04: Vendor Data Verification**
- Verify agitator vendor data against specification (DEL-13.02) requirements
- Confirm vendor compliance statements
- **TBD** — Vendor data acceptance criteria

**V-05: Units and Nomenclature Check**
- Verify all units are correct and consistent
- Verify nomenclature is consistent with project conventions
- **TBD** — Units and nomenclature checklist

### Acceptance Criteria

**AC-01: Completeness**
- All required data sheets are produced (3 tank, 3 agitator, overflow protection)
- All required fields are populated or marked TBD with explanation
- All cross-references are complete

**AC-02: Accuracy**
- Data is accurate and verified against source documents
- Dimensions and parameters match design calculations and drawings
- Material specifications match technical specification

**AC-03: Consistency**
- Data sheets are internally consistent (e.g., nozzle summary matches individual nozzle entries)
- Data sheets are consistent with other project documents
- Tag numbers and nomenclature are consistent across all data sheets

**AC-04: Vendor Data Integration**
- Agitator vendor data is complete and compliant with specification
- Vendor data discrepancies are identified and resolved

**AC-05: Approval**
- All required checks completed and signed off
- Discipline lead approval obtained
- **TBD** — Client review and approval requirements per ER

---

## Documentation

### Required Data Sheet Outputs

| Data Sheet Type | Quantity | Description |
|-----------------|----------|-------------|
| **Tank Data Sheets** | 3 | One per tank (TK-101, TK-102, TK-103 — tags TBD) |
| **Agitator Data Sheets** | 3 | One per agitator (AGI-101, AGI-102, AGI-103 — tags TBD) |
| **Overflow Protection Data Sheet(s)** | **TBD** | Single system or one per tank |

**Source:** _CONTEXT.md (Anticipated Artifacts)

### Data Sheet Management

**DM-01: Document Control**
- All data sheets shall be managed per project document control procedures
- Electronic master copies maintained in project document management system
- **TBD** — Document management system and procedures

**DM-02: Issuance**
- Data sheets issued for review: Filed in `2_Checking/To/` with transmittal
- Data sheets issued for construction: Filed in `3_Issued/` with issue record
- **TBD** — Issuance workflow and approval matrix

**DM-03: Revision Management**
- Revisions tracked with revision history on each data sheet
- Superseded revisions archived per project retention policy
- **TBD** — Revision tracking and archival procedures

**DM-04: Archive and Retention**
- Final as-built data sheets maintained for facility lifecycle
- **TBD** — Retention requirements per project procedures and ER

---

## Cross-Document References

**For entity attributes and values:** See `Datasheet.md`
- Tank Data Sheet Content → Referenced in FR-01
- Agitator Data Sheet Content → Referenced in FR-02
- Overflow Protection Data Sheet Content → Referenced in FR-03
- Package Configuration → Referenced in DR-01

**For data sheet development principles:** See `Guidance.md`
- DP-01: Equipment Documentation Philosophy → Supports FR-01, FR-02, FR-03
- DP-02: Vendor Data Integration → Supports FR-02, PR-04, DR-05
- DP-03: Cross-Discipline Coordination → Supports IR-01 through IR-07
- Trade-offs → Support data sheet format and content selections

**For verification and production:** See `Procedure.md`
- Section: Verification → Implements V-01 through V-05 (self-check, cross-check, IDC, vendor data verification, units check)
- Steps 1-3 → Develop data sheets to meet requirements specified here
- Steps 4-5 → Verify compliance with requirements specified here

---

**Document Status:** Pass 3 (Final) — Enrichment complete. Functional, performance, and interface requirements defined and linked to Datasheet attributes and Guidance rationale. Verification methods specified and aligned with Procedure. All TBDs marked. ASSUMPTIONs labeled. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
