# Procedure: DEL-12.04 Metering Data Sheet Package

## Purpose

This procedure defines the process for producing and managing the **Metering Data Sheet Package** within **PKG-12 Product Transfer & Metering**.

### Deliverable Definition

DEL-12.04 defines and substantiates metering in accordance with Employer's Requirements (Source: Decomposition:359).

| Attribute | Value |
|-----------|-------|
| Deliverable Type | Data Sheet |
| Discipline | Process |
| Responsible Party | D&B Contractor |
| Service Application | Custody transfer metering for CSD canola oil at rail unloading and marine loading; associated instrumentation (temperature, pressure transmitters) |

### Procedure Scope

This procedure covers the complete lifecycle for producing metering data sheets:

1. **Development** — identifying required data sheets, establishing templates, populating design basis fields
2. **Vendor data incorporation** — obtaining and incorporating vendor-certified data
3. **Review and checking** — cross-checking consistency, independent review
4. **Issue and revision management** — document control, approvals, issuance

This procedure applies to all data sheets: flow meters (2), temperature transmitters, pressure transmitters.

## Prerequisites

### Dependencies

| Prerequisite | Status | Notes |
|--------------|--------|-------|
| Dependency Mode | NOT_TRACKED | Dependencies coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`); coordinate with PKG-14 for P&IDs and tag numbers, PKG-17 for electrical, PKG-19 for controls, PKG-20 for instrumentation |

### Recommended Upstream Inputs

The following inputs should be obtained before commencing data sheet development (ASSUMPTION based on typical data sheet workflow):

| Input | Source | Purpose | Timing |
|-------|--------|---------|--------|
| Metering Technical Specification | DEL-12.02 | Performance requirements (accuracy, repeatability, turndown), materials, proving requirements, calibration requirements; provides specification parameters for data sheets | Before Step 3 (Populate Design Basis) |
| Metering Design Calculations | DEL-12.03 | Sizing parameters (flow ranges, meter sizes), uncertainty budget (expanded uncertainty), proving criteria (meter factor limits); provides calculated parameters for data sheets | Before Step 3 (Populate Design Basis) |
| Employer's Requirements | ER Vol 2 Part 2 | Operating conditions (temperature, pressure), fluid properties (CSD canola oil), accuracy requirements, regulatory requirements (Measurement Canada) | Before Step 3 (Populate Design Basis) |
| P&IDs | PKG-14 | Tag numbers, service descriptions, line numbers, P&ID drawing references; provides tag numbering for data sheets | Before Step 1 (Identify Required Data Sheets) |
| Vendor Data | Equipment suppliers | Manufacturer specifications, certified performance data, dimensional data, material certificates, calibration certificates; provides vendor-certified parameters for data sheets | During Step 4 (Vendor Data Incorporation); obtained after vendor selection |

### Reference Materials

| Reference | Location | Purpose |
|-----------|----------|---------|
| `_REFERENCES.md` | Deliverable folder | Applicable reference documents; list of ER clauses, specifications, calculations, P&IDs |
| `0_References/` | Package directory | Reference materials for PKG-12 (ER excerpts, standards, vendor literature, product data) |
| Employer's Requirements Vol 2 Part 1 | ER document set | General requirements, document control, tag numbering system, data sheet format standards | TBD |
| Employer's Requirements Vol 2 Part 2 | ER document set | Process mechanical requirements, metering requirements, operating conditions, fluid properties, accuracy requirements, hazardous area classification | TBD |
| Decomposition | Project root | PKG-12 scope (line 350), DEL-12.04 definition (line 359), objective mappings (lines 781, 789), facility parameters (throughput line 41, unloading stations line 44) |
| Specification.md | Deliverable folder | Requirements to be satisfied (REQ-01 through REQ-17); defines data sheet scope, content requirements, quality requirements |
| Guidance.md | Deliverable folder | Data sheet development considerations, principles, trade-offs, field-specific guidance, service-specific considerations, data sheet timing |
| Datasheet.md | Deliverable folder | Design context, design basis parameters (TBD items), anticipated data sheet content, data sheet field categories |

### Personnel Requirements

| Role | Qualification | Responsibility | Source |
|------|---------------|----------------|--------|
| Originator | Qualified Process discipline engineer; familiarity with custody transfer metering and instrumentation | Technical content, data sheet development, vendor data review, cross-reference verification | ASSUMPTION; project quality procedures |
| Checker | Independent Process discipline engineer (not the originator) or senior engineer | Independent review of data sheets for completeness, accuracy, consistency | ASSUMPTION; project quality procedures |
| Approver | Authorized per project procedures (typically Process Lead or Engineering Manager) | Authorization for issue; confirm data sheets satisfy ER and project requirements | TBD; ER Vol 2 Part 1 |

### Tools and Systems

| Tool/System | Purpose | Source |
|-------------|---------|--------|
| Data Sheet Software | Data sheet creation and management (Excel, database, specialized data sheet software, or per project standard) | TBD; ER Vol 2 Part 1 |
| Document Management System | Data sheet storage, revision control, distribution | TBD; ER Vol 2 Part 1 |

## Steps

### Step 1: Identify Required Data Sheets and Assign Tag Numbers

**Objective:** Determine all data sheets required per decomposition and assign tag numbers per project tag numbering system.

| Action | Description | Output |
|--------|-------------|--------|
| 1.1 | Confirm required data sheets per Specification.md REQ-01 and Decomposition:359: (1) flow meter for rail unloading, (2) flow meter for marine loading, (3) temperature transmitter(s) for custody transfer compensation, (4) pressure transmitter(s) for compensation if applicable (TBD; may not be required if canola oil compressibility is negligible); if density transmitters are separate from flow meters, add density transmitter data sheets | Data sheet requirement list |
| 1.2 | Coordinate with PKG-14 P&IDs to obtain tag numbers per Specification.md REQ-04: verify tag numbering system is established (e.g., FT-XXXX for flow transmitters/meters, TT-XXXX for temperature transmitters, PT-XXXX for pressure transmitters); obtain or assign tag numbers for each metering instrument; tag numbers must be consistent with P&IDs | Tag number assignments |
| 1.3 | Assign data sheet numbers per project document control procedures (TBD; ER Vol 2 Part 1): data sheet numbering may follow tag numbers (e.g., data sheet for FT-1201 is numbered DS-FT-1201) or sequential numbering per package (e.g., DS-12-001, DS-12-002); verify numbering system with document control | Data sheet number assignments |
| 1.4 | Create data sheet index per Specification.md Documentation section: list all data sheets with tag numbers, equipment descriptions, data sheet numbers, revisions; index serves as checklist for completeness verification per REQ-01 | Data sheet index |

**Output:** Data sheet index with tag numbers and document numbers for all required data sheets

**Verification:** All decomposition-listed artifacts included per Specification.md REQ-01; tag numbers coordinated with PKG-14 P&IDs per REQ-04

---

### Step 2: Establish Data Sheet Template

**Objective:** Define data sheet template with all required field categories per Specification.md field requirements.

| Action | Description | Output |
|--------|-------------|--------|
| 2.1 | Define required data field categories per Specification.md field requirements and Datasheet.md Construction section: **Flow meters**: Identification, Process Conditions, Performance, Materials, Electrical/Controls, Physical, Calibration/Proving, Vendor, Verification Basis; **Transmitters**: Identification, Process Conditions, Performance, Electrical, Physical, Calibration, Vendor, Verification Basis | Field category list |
| 2.2 | For each field category, list specific fields per Datasheet.md field tables: see Datasheet.md Construction section for detailed field lists (e.g., Process Conditions includes: service, product, normal flow, design flow, min flow, max flow, operating temperature, operating pressure, product density, product viscosity) | Detailed field lists |
| 2.3 | Include verification basis column or notes section per Specification.md REQ-10: for each critical field, include space to document source (ER clause, specification section, calculation, vendor certified, assumption, or TBD) | Verification basis structure |
| 2.4 | Establish template format per project standards (TBD; ER Vol 2 Part 1): may be spreadsheet (Excel), database form, structured document (Word table), or specialized data sheet software; format should support tabular data, multiple columns, notes, and revision history | Template format |
| 2.5 | Create separate templates for flow meters and transmitters (field categories differ) per Specification.md field requirements | Flow meter template; transmitter template |

**Output:** Data sheet templates with all required field categories and verification basis structure

**Verification:** Template includes all field categories per Specification.md field requirements; verification basis structure per REQ-10

---

### Step 3: Populate Design Basis Fields

**Objective:** Populate data sheets with design basis information from ER, DEL-12.02, and DEL-12.03 before vendor data is available.

| Action | Description | Output |
|--------|-------------|--------|
| 3.1 | Enter identification fields per Specification.md REQ-02: tag number (from Step 1), service description (e.g., "Rail Unloading Custody Transfer Metering", "Marine Loading Custody Transfer Metering"), P&ID reference (PKG-14 P&ID drawing number and sheet; coordinate with PKG-14), location (e.g., "Rail Unloading Metering Skid", "Marine Loading Metering Skid"; coordinate with DEL-12.01 drawings), equipment description (e.g., "Custody Transfer Coriolis Mass Flowmeter", "Custody Transfer Temperature Transmitter") | Identification fields populated |
| 3.2 | Enter process condition fields from ER Vol 2 Part 2, DEL-12.03, and design basis: **Service**: Rail unloading or marine loading; **Product**: CSD canola oil (Decomposition:43); **Flow rates**: Normal, design, minimum, maximum from DEL-12.03 calculations (TBD); **Temperature**: Operating temperature normal and range from ER Vol 2 Part 2 (TBD); **Pressure**: Operating pressure normal and range from ER Vol 2 Part 2 or PKG-14 piping (TBD); **Product properties**: Density at reference temperature and vs. temperature curve (TBD), viscosity at operating temperature (TBD); mark TBD with source needed per Specification.md REQ-12 | Process condition fields populated or TBD |
| 3.3 | Enter performance fields from DEL-12.02 specification and DEL-12.03 calculations per Specification.md REQ-05, REQ-06: **Meter type**: Coriolis, ultrasonic, turbine, or other from DEL-12.02 (TBD); **Accuracy class**: From DEL-12.02 (e.g., ±0.15%; TBD); **Repeatability**: From DEL-12.02 (e.g., ±0.05%; TBD); **Turndown ratio**: From DEL-12.03 (e.g., 20:1; calculated based on max/min flow); **Expanded uncertainty**: From DEL-12.03 uncertainty budget (e.g., ±0.14% at 95% confidence); **Flow range**: From DEL-12.03 (min to max with accuracy maintained); **Pressure drop**: From DEL-12.03 (at max flow); mark TBD for fields pending DEL-12.02 or DEL-12.03 completion | Performance fields populated or TBD |
| 3.4 | Enter material fields from DEL-12.02 specification per Specification.md REQ-05: wetted materials (body material: SS316L, carbon steel, or other; TBD from DEL-12.02), internals material, seals and gaskets (Viton, PTFE, or other), housing material, pressure rating (ANSI class, PN rating), temperature rating; mark TBD with source DEL-12.02 | Material fields populated or TBD |
| 3.5 | Enter interface fields per Specification.md REQ-03, REQ-13: **Electrical**: Power supply (voltage, frequency; TBD from PKG-17 or DEL-12.02), signal outputs (4-20 mA, pulse, digital; TBD from PKG-19), communication protocol (Modbus, HART, other; TBD from PKG-19), area classification (Division 1/2, non-classified; TBD from ER Vol 2 Part 2), electrical certification (CSA, UL, ATEX, IECEx; TBD); **Physical**: Process connections (size, rating, facing; TBD from DEL-12.03 sizing and PKG-14 piping), mounting orientation (horizontal, vertical; TBD from DEL-12.02 or manufacturer), straight-run requirements (for flow meters; TBD from DEL-12.02 or manufacturer; e.g., "10D upstream, 5D downstream"); mark TBD for fields pending interface coordination or vendor data | Interface fields populated or TBD |
| 3.6 | Enter calibration fields per Specification.md REQ-11: **Calibration range**: Typically same as measurement range; **Calibration traceability**: "Traceable to Measurement Canada" or "Traceable to NIST" or equivalent; **Calibration interval**: Per Measurement Canada regulations, ER requirements, or project QA plan (TBD); **Certificates required**: Calibration certificate, material certificates (MTRs), Measurement Canada approval (if applicable for custody transfer in Canada); **Proving** (for flow meters): Proving method from DEL-12.02 (in-line prover, portable prover, master meter; TBD), proving frequency from DEL-12.02 (quarterly, semi-annually, annually; TBD), meter factor range from DEL-12.03 (e.g., 0.995-1.005), meter factor drift limit from DEL-12.03 (e.g., ±0.05%); mark TBD for fields pending DEL-12.02, DEL-12.03, or regulatory requirements | Calibration fields populated or TBD |
| 3.7 | Document verification basis for each populated field per Specification.md REQ-10: in verification basis column or notes, indicate source for each field value: "ER Vol 2 Part 2 Clause X.X.X" for ER-derived, "DEL-12.02 Section Y.Y" for specification-derived, "DEL-12.03 Section Z.Z Table N" for calculation-derived, "ASSUMPTION — [rationale]" for inferred values, "TBD — [source needed]" for unknown values | Verification basis documented |
| 3.8 | Mark vendor-specific fields TBD until vendor data available: manufacturer name, model number, vendor data sheet reference, serial number, vendor-certified dimensions (length, weight), vendor-certified performance data; these fields will be populated in Step 4 after vendor selection and data receipt | Vendor fields marked TBD |

**Output:** Data sheets with design basis fields populated from ER, DEL-12.02, DEL-12.03; verification basis documented; vendor fields marked TBD

**Verification:** Design basis fields populated per Specification.md REQ-02, REQ-05, REQ-06; verification basis documented per REQ-10; TBD fields flagged per REQ-12

---

### Step 4: Obtain and Incorporate Vendor Data

**Objective:** Obtain vendor-certified data and incorporate into data sheets; update vendor fields.

| Action | Description | Output |
|--------|-------------|--------|
| 4.1 | Request vendor certified data for selected equipment: issue vendor data request (VDR) or request for information (RFI) to equipment vendors; specify required data: manufacturer data sheets, performance curves, dimensional drawings, material certificates, calibration certificates, installation manuals; typical vendor data package includes: certified data sheet with performance specifications, outline dimensional drawing, installation manual, operation manual, spare parts list | Vendor data request issued |
| 4.2 | Review vendor data for compliance with data sheet requirements per Specification.md REQ-05, REQ-06: **Performance**: Verify vendor-certified accuracy meets or exceeds data sheet accuracy requirement from DEL-12.02 (e.g., vendor certifies ±0.15%, requirement is ±0.15% or looser); **Flow range**: Verify vendor-certified flow range encompasses data sheet flow range from DEL-12.03 (e.g., vendor range 50-1000 m³/h encompasses required 50-500 m³/h); **Materials**: Verify vendor materials match data sheet material requirements from DEL-12.02 (e.g., body SS316L); **Electrical**: Verify vendor power supply and signals match data sheet interface requirements; **Physical**: Verify vendor dimensions are acceptable (meter length, weight, connections); identify any vendor deviations from data sheet requirements for resolution | Vendor data compliance review |
| 4.3 | Enter vendor-certified values into data sheets per Specification.md vendor data fields: **Manufacturer**: Vendor company name; **Model number**: Vendor model designation; **Vendor data sheet reference**: Manufacturer document number; **Serial number**: Equipment serial number (enter when equipment is delivered); **Vendor-certified performance**: Actual certified accuracy, flow range, pressure drop (if vendor values differ from design basis, document both: design basis value and vendor-certified value); **Vendor-certified physical**: Actual meter length, weight, connection sizes from vendor dimensional drawings | Vendor fields populated |
| 4.4 | Mark vendor-certified fields with verification basis per Specification.md REQ-10: "Vendor Certified Data — [Vendor Name] Data Sheet [Document Number]"; distinguish vendor-certified values from design basis values; if vendor value differs from design basis, document both and flag for resolution: "Design basis: [value] per DEL-12.03; Vendor certified: [value] per [Vendor] Data Sheet [Ref]; Difference: [explain]; Resolution: [TBD or resolution action]" | Verification basis for vendor fields |
| 4.5 | Attach or reference vendor data sheets per Specification.md vendor data documentation: attach vendor PDF data sheets to data sheet package, or reference vendor data sheet location in document management system; vendor data sheets provide detailed backup for data sheet values; required for DEL-12.05 QA records and future reference | Vendor data sheets attached or referenced |
| 4.6 | Update data sheet revision per vendor data incorporation per Specification.md REQ-16: if vendor data changes data sheet parameters, issue revised data sheet; document revision description (e.g., "Rev A: Incorporated vendor certified data from [Vendor] proposal dated [Date]"); update revision history | Data sheet revision if vendor data incorporated |

**Output:** Data sheets with vendor-certified values incorporated; vendor data sheets attached or referenced; verification basis documented for vendor fields

**Verification:** Vendor data reviewed for compliance per Specification.md REQ-05, REQ-06; vendor-certified fields marked per REQ-10; vendor deviations identified and resolved

---

### Step 5: Cross-Check Consistency

**Objective:** Verify data sheet parameters are consistent with related deliverables per Specification.md REQ-04, REQ-05, REQ-06.

| Action | Description | Verification |
|--------|-------------|--------------|
| 5.1 | Cross-check with DEL-12.02 Metering Technical Specification per Specification.md REQ-05: verify data sheet accuracy class matches specification accuracy requirement (e.g., data sheet shows ±0.15%, DEL-12.02 requires ±0.15% or looser); verify data sheet repeatability matches specification; verify data sheet materials match specification material requirements; verify data sheet proving method and frequency match specification; verify data sheet calibration requirements match specification; identify any inconsistencies for resolution | DEL-12.02 consistency check |
| 5.2 | Cross-check with DEL-12.03 Metering Design Calculations per Specification.md REQ-06: verify data sheet flow ranges match calculation flow rates (design, normal, min, max); verify data sheet meter sizes match calculation sizing results (e.g., data sheet shows 6" meter, DEL-12.03 calculated 6" meter); verify data sheet pressure drop matches calculation pressure drop (at max flow); verify data sheet expanded uncertainty matches calculation uncertainty budget result; verify data sheet meter factor limits and proving criteria match calculation proving section; identify inconsistencies | DEL-12.03 consistency check |
| 5.3 | Cross-check with DEL-12.01 Metering Design Drawing Set per Specification.md REQ-04: verify data sheet tag numbers match drawing tag numbers; verify data sheet meter sizes match drawing equipment sizes; verify data sheet orientations match drawing orientations (horizontal, vertical); verify data sheet straight-run requirements match drawing straight-run dimensions; identify tag number or sizing inconsistencies | DEL-12.01 consistency check |
| 5.4 | Cross-check interface fields with interfacing packages per Specification.md REQ-13: coordinate with PKG-14 for P&ID consistency (tag numbers, line numbers, service descriptions); coordinate with PKG-17 for electrical parameters (power supply voltage/frequency, area classification); coordinate with PKG-19 for control parameters (signal types, communication protocols); coordinate with PKG-20 for transmitter specifications (if transmitters in PKG-20 scope vs. this deliverable); verify interface parameters are mutually consistent | Interface consistency check |
| 5.5 | Identify and document inconsistencies: if inconsistencies are found between data sheets and related deliverables, document in table: Data Sheet Field, Data Sheet Value, Related Deliverable, Related Deliverable Value, Conflict Description; examples: "Flow range: Data sheet shows 50-600 m³/h, DEL-12.03 calculated 50-500 m³/h; Conflict: max flow mismatch"; "Tag number: Data sheet FT-1201, Drawing FT-1202; Conflict: tag number mismatch" | Inconsistency table |
| 5.6 | Resolve inconsistencies: coordinate with originators of related deliverables (DEL-12.01, DEL-12.02, DEL-12.03) to resolve conflicts; determine correct value (may require specification update, calculation revision, drawing correction, or data sheet correction); update data sheets with resolved values; document resolution in verification basis or notes | Inconsistency resolution |
| 5.7 | Record unresolved conflicts in Guidance.md Conflict Table per Specification.md conflict handling: if conflicts cannot be resolved from available information, document in Conflict Table with citations requesting human ruling | Unresolved conflicts documented |

**Output:** Cross-checked data sheets with consistency verified or conflicts documented

**Verification:** Data sheets consistent with DEL-12.01, DEL-12.02, DEL-12.03 per Specification.md REQ-04, REQ-05, REQ-06; inconsistencies resolved or flagged

---

### Step 6: Independent Check and Issue

**Objective:** Independent reviewer checks data sheets; resolve comments; obtain approvals; issue per Specification.md REQ-15.

| Action | Description | Output |
|--------|-------------|--------|
| 6.1 | Independent checker reviews data sheets for completeness per Specification.md REQ-01, REQ-02, REQ-03: verify all required data sheets present per data sheet index (flow meters ×2, temperature transmitters, pressure transmitters); verify all required field categories populated or marked TBD (Identification, Process Conditions, Performance, Materials, Electrical, Physical, Calibration, Vendor); verify no blank fields without TBD or N/A designation per REQ-12 | Completeness check |
| 6.2 | Checker verifies verification basis documentation per Specification.md REQ-10: verify critical fields have verification basis documented (ER clause, specification section, calculation, vendor certified, assumption, or TBD); verify sources are correctly cited (clause numbers, section numbers, document references); verify TBD items are flagged with source needed | Verification basis check |
| 6.3 | Checker verifies cross-document consistency per Specification.md REQ-04, REQ-05, REQ-06: verify tag numbers consistent with P&IDs and drawings; verify performance parameters consistent with specification; verify sizing parameters consistent with calculations; verify no unresolved inconsistencies (or inconsistencies documented in Conflict Table) | Consistency check |
| 6.4 | Checker verifies calibration fields per Specification.md REQ-11: verify calibration range, traceability, interval, certificates required are documented; verify proving requirements documented for flow meters (method, frequency, meter factor limits, acceptance criteria); verify calibration fields enable DEL-12.05 compliance demonstration | Calibration field check |
| 6.5 | Checker verifies units, nomenclature, and formatting: verify units are consistent and clearly stated (SI vs. Imperial per project convention; TBD); verify nomenclature is consistent with project standards; verify formatting follows project data sheet standards; verify no typographical errors | Quality check |
| 6.6 | Checker documents review comments: prepare check comment list with comment number, data sheet (tag number), field or section, comment description, severity (critical if error, advisory if clarification), recommended action | Check comment list |
| 6.7 | Originator and checker coordinate to resolve comments: review comments together, agree on resolutions (correct errors, clarify verification basis, update cross-references), originator implements agreed resolutions, checker verifies resolutions | Comment resolution |
| 6.8 | Checker records independent check completion per Specification.md REQ-15: date, checker name, summary of review (data sheets reviewed, key items verified), confirmation that all comments are resolved, checker signature confirming review complete | Independent check record |
| 6.9 | Obtain approval signatures per project procedures (TBD; ER Vol 2 Part 1): originator signature (confirming data sheet accuracy and check resolution), checker signature (confirming independent review completion), approver signature (authorizing issue; typically Process Lead or Engineering Manager) | Approval signatures |
| 6.10 | Issue per project document control process (TBD; ER Vol 2 Part 1): submit to document management system, assign final document numbers if not assigned in Step 1, assign revision (00 for initial issue, A/B/C or 01/02/03 for subsequent revisions per project convention; TBD), distribute to required recipients (project team, procurement, vendors, DEL-12.01/DEL-12.05 originators; distribution list TBD) | Document management system entry; distribution |
| 6.11 | Place issued copy in deliverable folder structure: place issued data sheet package in `2_Checking/` for review issue or `3_Issued/` for final/construction issue — per project convention and lifecycle state | Filed issue copy |
| 6.12 | Update deliverable status: if issuing for review, update `_STATUS.md` to CHECKING with note "Issued for Review, Rev 00, Date YYYY-MM-DD"; if issuing final, update `_STATUS.md` to ISSUED with note "Issued, Rev 00, Date YYYY-MM-DD"; record issue date, revision, and issue purpose in status history | Status update |

**Output:** Independently checked data sheet package with all comments resolved; check record with checker signature; issued data sheets with all approvals; deliverable status updated

**Verification:** Independent check complete per Specification.md REQ-15; check record documents verification; all approval signatures obtained; data sheets issued per document control procedures

---

## Verification

### Verification Activities

| Activity | Requirement Verified | Method | Record |
|----------|---------------------|--------|--------|
| Artifact completeness check | REQ-01 | Checklist against Decomposition:359 and data sheet index — verify all data sheets present (flow meters ×2, temperature transmitters, pressure transmitters) | Data sheet index Step 1.4; check record Step 6.1 |
| Field completeness check | REQ-02, REQ-03, REQ-12 | Document review — verify all required field categories populated or marked TBD; verify no blank fields | Check record Step 6.1 |
| Tag consistency check | REQ-04 | Cross-reference check — verify tag numbers match P&IDs and DEL-12.01 drawings | Consistency check Step 5.3; check record Step 6.3 |
| Specification consistency check | REQ-05 | Cross-reference check — verify parameters match DEL-12.02 specification requirements | Consistency check Step 5.1; check record Step 6.3 |
| Calculation consistency check | REQ-06 | Cross-reference check — verify parameters match DEL-12.03 calculations | Consistency check Step 5.2; check record Step 6.3 |
| Verification basis check | REQ-10 | Document review — verify verification basis documented for critical fields | Check record Step 6.2 |
| Calibration field check | REQ-11 | Document review — verify calibration and proving fields documented | Check record Step 6.4 |
| Interface field check | REQ-13 | Document review and IDC — verify interface fields documented; coordinate with interfacing packages | Interface check Step 5.4; check record |
| Vendor data verification | REQ-09, vendor data | Document review — verify vendor-certified values documented and referenced | Vendor data review Step 4.2; check record |
| OBJ alignment check | REQ-07, REQ-08 | Review — verify data sheets support OBJ-2 (flow ranges adequate for throughput) and OBJ-10 (accuracy, calibration, proving documented) | Check record Step 6 |
| Independent check | REQ-15 | Independent reviewer verifies all above items | Check record Step 6.8 |

### Acceptance Criteria

| Criterion | Verification Method | Source |
|-----------|---------------------|--------|
| All data sheets present | Data sheet index review Step 1.4; checklist Step 6.1 | Specification.md REQ-01; Decomposition:359 |
| All required fields populated or TBD | Field completeness review Step 6.1 | Specification.md REQ-02, REQ-03, REQ-12 |
| Tag numbers consistent | Tag consistency check Step 5.3; check record Step 6.3 | Specification.md REQ-04 |
| Specification consistency | Specification consistency check Step 5.1; check record Step 6.3 | Specification.md REQ-05 |
| Calculation consistency | Calculation consistency check Step 5.2; check record Step 6.3 | Specification.md REQ-06 |
| Verification basis documented | Verification basis check Step 6.2 | Specification.md REQ-10 |
| Calibration fields documented | Calibration field check Step 6.4 | Specification.md REQ-11 |
| Interface fields documented | Interface field check Step 5.4 | Specification.md REQ-13 |
| Vendor data incorporated | Vendor data review Step 4; check record | Specification.md REQ-09 |
| Check record complete | Check record review Step 6.8 | Specification.md REQ-15 |

### Sign-off Requirements

| Role | Responsibility | Verification | Source |
|------|----------------|--------------|--------|
| Originator | Technical content accuracy, field verification basis documentation, consistency with related deliverables | Originator signature on data sheets confirming accuracy and check resolution | ASSUMPTION; project quality procedures |
| Checker | Independent review completion, completeness verification, consistency verification | Checker signature on data sheets and check record confirming review complete | ASSUMPTION; project quality procedures; Specification.md REQ-15 |
| Approver | Authorization for issue, compliance with ER and project requirements | Approver signature on data sheets authorizing issue | TBD; ER Vol 2 Part 1 |

## Records

### Documentation Outputs

| Output | Description | Source |
|--------|-------------|--------|
| Flow Meter Data Sheet — Rail Unloading | Custody transfer flow meter data sheet for rail unloading service with all field categories populated or TBD | Decomposition:359; Specification.md REQ-01, REQ-02; Steps 1-4 |
| Flow Meter Data Sheet — Marine Loading | Custody transfer flow meter data sheet for marine loading service with all field categories populated or TBD | Decomposition:359; Specification.md REQ-01, REQ-02; Steps 1-4 |
| Temperature Transmitter Data Sheet(s) | Temperature measurement data sheet(s); separate for rail and marine if specifications differ, or combined if identical | Decomposition:359; Specification.md REQ-01, REQ-02; Steps 1-4 |
| Pressure Transmitter Data Sheet(s) | Pressure measurement data sheet(s) if applicable; separate for rail and marine if specifications differ | Decomposition:359; Specification.md REQ-01, REQ-02; Steps 1-4 |
| Data Sheet Index | Index listing all data sheets with tag numbers, equipment descriptions, data sheet numbers, revisions | Specification.md Documentation section; Step 1.4 |
| Independent Check Record | Record documenting independent check completion with checker signature, check comments, resolutions | Specification.md REQ-15; Step 6.8 |

### Record Management

| Attribute | Value | Source |
|-----------|-------|--------|
| Filing Location (Working) | `1_Working/DEL-12.04_Metering_Data_Sheet_Package/` | Current location |
| Filing Location (Review) | `2_Checking/` (for review issue) | Project convention |
| Filing Location (Issued) | `3_Issued/` (for final/construction issue) | Project convention |
| Document Management System | Per project document control procedures (TBD; ER Vol 2 Part 1) | TBD |
| Retention Period | Per project quality procedures; typically life of facility for custody transfer equipment data sheets | TBD |
| Format | Electronic files (Excel, PDF, database, or per project standard); electronic distribution | ASSUMPTION |
| Backup and Version Control | Per project IT procedures; data sheet files under version control in document management system | TBD |

### Status Transitions

Status transitions are managed per `_STATUS.md` in the deliverable folder:

| From State | To State | Trigger | Responsible |
|------------|----------|---------|-------------|
| INITIALIZED | IN_PROGRESS | Data sheet development commences (Step 1) | Process Engineer (originator) |
| IN_PROGRESS | CHECKING | Data sheets submitted for review (Step 6 for review issue) | Process Engineer (originator) |
| CHECKING | IN_PROGRESS | Review comments or vendor data updates require revision | Process Engineer (originator) |
| CHECKING | ISSUED | Approved for construction; vendor data finalized (Step 6 for final issue) | Approver |

**Note:** Status state transitions are recorded in `_STATUS.md` with date, state change, and brief description. Data sheets may cycle between IN_PROGRESS and CHECKING multiple times as vendor data is incorporated and revisions issued.

### Revision Management

| Revision | Purpose | Typical Trigger | Approval Required |
|----------|---------|-----------------|-------------------|
| 00 | Initial issue for vendor inquiry | First issue for RFQ; functional requirements and performance targets; vendor-specific fields TBD | Process Lead |
| A, B, C... | Subsequent issues incorporating vendor data | Vendor bid data received and incorporated; vendor-confirmed parameters updated; serial numbers added upon delivery | Process Lead |
| 01, 02, 03... | Issued for construction or as-built | Final vendor-certified data incorporated; all vendor fields populated; equipment ordered or delivered; ready for installation and commissioning | Engineering Manager |
| As-built | Final as-built revision | Equipment installed; installation verified; final serial numbers, final calibration certificates, any field modifications documented | As-built process per project procedures (TBD) |

**Note:** Revision numbering convention TBD from ER Vol 2 Part 1 project document control procedures. Data sheets typically have multiple revisions as vendor data is progressively incorporated from RFQ through delivery.
