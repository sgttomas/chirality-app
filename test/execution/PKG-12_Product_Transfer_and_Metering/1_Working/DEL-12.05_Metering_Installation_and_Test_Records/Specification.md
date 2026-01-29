# Specification: DEL-12.05 Metering Installation & Test Records

## Scope

### Deliverable Definition

This specification defines the requirements for the **Metering Installation & Test Records** deliverable within **PKG-12 Product Transfer & Metering**.

DEL-12.05 provides evidence of completion, inspection, and testing for custody transfer metering (Source: Decomposition:360).

### Package Scope Context

PKG-12 scope covers custody transfer flow meters (rail unloading and marine loading) and metering instrumentation (Source: Decomposition:350).

The facility transfers CSD (Crude Super Degummed) canola oil from rail tank cars to storage tanks (via rail unloading metering) and from storage tanks to liquid bulk carriers for export (via marine loading metering), with a permitted throughput of 1,000,000 MT per annum (Source: Decomposition:41, 43).

### Inclusions

The record package shall include, at minimum:

| Artifact | Description | Source |
|----------|-------------|--------|
| Calibration Certificates | Factory and/or field calibration certificates for custody transfer flow meters (rail unloading and marine loading) and associated transmitters (temperature, pressure, density if applicable) with traceability to national measurement standards | Decomposition:360 |
| Accuracy Verification Records | Proving results or accuracy verification records demonstrating meter performance meets specification requirements; includes proving run data, meter factor calculation, acceptance verification | Decomposition:360 |

**Note:** Decomposition specifies minimum artifacts; additional records may be required per ER, DEL-12.02 specification, or project Quality Management Plan (e.g., FAT records, SAT records, installation inspection records, material certificates).

### Exclusions

The following are outside the scope of DEL-12.05:

- General field instrumentation test records for non-metering instruments (covered in PKG-20 Field Instrumentation)
- Control system commissioning records (covered in PKG-19 Control Systems; may include metering signal integration testing but system-level commissioning is PKG-19)
- Piping pressure test and leak test records (covered in PKG-14 Process Piping; metering piping may be included in PKG-14 pressure tests)
- Electrical testing records for power distribution (covered in PKG-17 Electrical; metering equipment electrical testing is in this deliverable)

## Requirements

### Functional Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-01 | The record package shall include calibration certificates and accuracy verification records for all custody transfer metering equipment per Decomposition:360; minimum record set: (1) calibration certificates for flow meters (rail and marine), (2) accuracy verification/proving records for flow meters, (3) calibration certificates for temperature transmitters, (4) calibration certificates for pressure transmitters if applicable | Decomposition:360 | Checklist review per Procedure.md Step 1; record index completeness check |
| REQ-02 | Records shall be traceable to equipment tag numbers (per project tag numbering system; coordinate with PKG-14 P&IDs and DEL-12.04 data sheets) and equipment serial numbers (from equipment nameplates and vendor documentation) | TBD; ER Vol 2 Part 1, location TBD; ASSUMPTION based on QA traceability requirements | Equipment traceability check per Procedure.md Step 2; verify tag numbers and serial numbers match DEL-12.04 |
| REQ-03 | Records shall be traceable to DEL-12.04 data sheet parameters; record package shall include cross-reference mapping records to data sheets; verify equipment in records matches equipment in data sheets (tag numbers, serial numbers, manufacturers, models) | ASSUMPTION; cross-deliverable traceability | Cross-reference review per Procedure.md Step 5.2; verify consistency with DEL-12.04 |
| REQ-04 | Record package shall include record index or traceability map listing all included records with: equipment tag number, serial number, service description, record type, record date, record reference (file name or document number), witness information, status (complete/pending/N/A) | ASSUMPTION; record organization requirement | Record index review per Procedure.md Step 2; verify index completeness |

### Performance Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-05 | Accuracy verification records shall demonstrate compliance with DEL-12.02 specification acceptance criteria: meter accuracy meets specified accuracy class (e.g., ±0.15%, ±0.25%; TBD from DEL-12.02), proving repeatability meets specified repeatability (e.g., ±0.02% for in-line prover, ±0.05% for portable prover; TBD from DEL-12.03), meter factor is within acceptable range (e.g., 0.995-1.005; TBD from DEL-12.03) | ASSUMPTION; compliance demonstration requirement | Technical review per Procedure.md Step 5.4; verify proving results meet acceptance criteria from DEL-12.03 |
| REQ-06 | Calibration certificates shall demonstrate traceability to national measurement standards: certificates shall include traceability statement (e.g., "Traceable to Measurement Canada", "Traceable to NIST"), calibration standard identification (reference standard used with calibration certificate number), calibration uncertainty statement (calibration uncertainty documented; typically ≤1/3 of measurement uncertainty per ISO/IEC 17025) | ASSUMPTION; calibration traceability requirement for custody transfer | Certificate review per Procedure.md Step 3.3; verify traceability statements complete |
| REQ-07 | Calibration certificates shall document calibration date, calibration range, as-found values, as-left values (if adjusted), calibration uncertainty, calibrator identification (calibrating organization, technician name, certifications), next calibration due date or interval | ASSUMPTION; calibration certificate content requirements | Certificate completeness review per Procedure.md Step 3.2 |
| REQ-08 | Proving/accuracy verification records shall document proving method (in-line prover, portable prover, master meter per DEL-12.02), proving date, proving conditions (flow rate, temperature, pressure during proving), proving run data (individual run volumes or meter readings), meter factor calculation (meter factor = true volume / indicated volume), proving repeatability (repeatability of proving runs; e.g., ±0.02%, ±0.05%), acceptance criteria (from DEL-12.03), acceptance verification (pass/fail determination with signature) | ASSUMPTION; proving record content requirements per API MPMS Chapter 4 or OIML R117 | Proving record completeness review per Procedure.md Step 4.2 |
| REQ-09 | Performance acceptance criteria are TBD pending ER Vol 2 Part 2 extraction, DEL-12.02 specification finalization, and DEL-12.03 calculation completion; acceptance criteria for FAT, SAT, calibration verification, and proving shall be clearly stated in each test record | TBD; ER Vol 2 Part 2, location TBD | Technical review; verify acceptance criteria are stated in test records |

### Traceability Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-10 | Each calibration certificate shall be traceable to specific equipment: certificate shall include equipment tag number, serial number, manufacturer, model matching DEL-12.04 data sheets | ASSUMPTION; equipment traceability | Traceability check per Procedure.md Step 3.3; cross-reference to DEL-12.04 |
| REQ-11 | Each proving/accuracy verification record shall be traceable to specific flow meter: record shall include equipment tag number, serial number, service (rail unloading or marine loading) matching DEL-12.04 data sheets | ASSUMPTION; equipment traceability | Traceability check per Procedure.md Step 4.2; cross-reference to DEL-12.04 |
| REQ-12 | Record package shall include cross-reference to related deliverables: DEL-12.01 drawings (installation per drawings), DEL-12.02 specification (acceptance criteria per spec), DEL-12.03 calculations (proving criteria per calculations), DEL-12.04 data sheets (equipment parameters per data sheets) | ASSUMPTION; cross-deliverable traceability | Cross-reference review; verify related deliverables are referenced in record package |

### Documentation Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-13 | Record package shall align with project document control and submission conventions: record numbering per project system, revision control per project procedures, filing per project archive structure, distribution per project distribution list | TBD; ER Vol 2 Part 1, location TBD | Document control review per Procedure.md Step 7; verify compliance with project procedures |
| REQ-14 | Records shall be organized in structured record package with cover sheet, record index, sections for each record type (calibration certificates, FAT, installation verification, SAT, proving records, MTRs, NCRs), and appendices per Datasheet.md record package structure | ASSUMPTION; record organization requirement | Package structure review; verify organization per Datasheet.md structure |

### Interface Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-15 | Interface coordination with adjacent packages is managed externally per dependency mode NOT_TRACKED; however, record package may reference interface verification: electrical connection testing (PKG-17), control system signal integration testing (PKG-19), instrumentation loop checks (PKG-20), piping pressure testing (PKG-14 if metering piping included) | _DEPENDENCIES.md; ASSUMPTION | Coordination meeting; verify interface tests are completed and results available |

### Quality Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-16 | Records shall include required signatures and witnessing as applicable: test performer signature (technician who performed test), reviewer signature (independent reviewer who verified test results), approver signature (QA/QC lead or engineering approval), witness signature (third-party or client witness for hold points: FAT witness if required, installation inspection witness if required, proving witness if required per ER or Measurement Canada) | TBD; ER Vol 2 Part 1, location TBD; ASSUMPTION based on QA requirements | Signature review per Procedure.md Step 5.5; verify all required signatures present |
| REQ-17 | Records shall be complete, legible, and archived in approved formats: records shall be complete (all required fields populated, no blank critical fields, all signatures obtained), legible (readable text, clear scans if hardcopy records scanned to electronic format), approved format (PDF, scanned image, or per project document control procedures; TBD) | TBD; ER Vol 2 Part 1, location TBD | Completeness and legibility check per Procedure.md Step 5.6 |
| REQ-18 | Nonconformance reports (NCRs) shall be included if any issues identified during installation or testing: NCR shall document issue description, root cause if determined, corrective action taken, verification of corrective action effectiveness, client acceptance of disposition (if significant NCR); NCRs demonstrate all quality issues were identified and resolved before system acceptance | ASSUMPTION; QA nonconformance handling | NCR review per Procedure.md Step 5.7; verify NCRs are resolved |
| REQ-19 | All work shall comply with project Quality Management Plan | ASSUMPTION | QA/QC audit |

## Standards

### Governing References

| Standard/Reference | Applicability | Source |
|--------------------|---------------|--------|
| Employer's Requirements Vol 2 Part 1 | General requirements, document control, QA procedures, witnessing requirements, records retention, archive format | TBD |
| Employer's Requirements Vol 2 Part 2 | Process mechanical requirements, metering testing requirements, accuracy verification requirements, regulatory compliance (Measurement Canada), FAT/SAT requirements | TBD |
| Project Quality Management Plan | QA/QC procedures, inspection and test plan (ITP), hold points and witness points, record formats and templates, nonconformance handling, records management and retention | TBD |
| Project Document Control Procedures | Record package numbering, revision control, distribution, archival | TBD |

### Custody Transfer Metering Standards (TBD — ASSUMPTION)

Applicable standards may define calibration, proving, and record requirements for custody transfer metering:

| Standard | Description | Potential Applicability |
|----------|-------------|------------------------|
| API MPMS Chapter 4 (Proving Systems) | Proving procedures, proving run data requirements, meter factor calculation, proving repeatability, acceptance criteria, proving record format | Applicable if API MPMS is governing standard; defines proving record requirements and format |
| OIML R117 (Dynamic Measuring Systems for Liquids Other Than Water) | Calibration and verification requirements, testing procedures, accuracy verification, record requirements for legal metrology | Likely applicable for vegetable oil custody transfer; may define required calibration and verification documentation |
| ISO/IEC 17025 (General Requirements for the Competence of Testing and Calibration Laboratories) | Calibration laboratory accreditation requirements; calibration certificate requirements; traceability requirements; measurement uncertainty documentation | Applicable to calibration laboratory; calibration certificates should be from ISO/IEC 17025 accredited lab for custody transfer traceability |
| Measurement Canada (Weights and Measures Act, Regulations, and Specifications) | Canadian regulatory requirements for custody transfer measurement; meter approval requirements, calibration traceability, proving requirements, periodic verification, record retention | Applicable for custody transfer in Canada; may require specific calibration and proving records for regulatory compliance; Measurement Canada approval certificate may be required record |
| ISO 9001 (Quality Management Systems) | General QA record requirements; document control, traceability, record retention, records management, nonconformance handling | Applicable to project QA system; general framework for record management |

**Note:** Standard applicability and specific record requirements to be confirmed from ER Vol 2 Part 2, DEL-12.02 specification, project Quality Management Plan, and Measurement Canada regulations if applicable.

## Verification

### Verification Methods

| Method | Description | Applicable Requirements |
|--------|-------------|------------------------|
| Checklist Review | Verify presence of all required records per record index: calibration certificates for all equipment (flow meters, transmitters), accuracy verification/proving records for flow meters, FAT records if applicable, SAT records if applicable, installation verification if applicable, MTRs if required, NCRs if any | REQ-01 |
| Equipment Traceability Check | Verify records are traceable to equipment tag numbers and serial numbers; cross-reference record index to DEL-12.04 data sheets; verify tag numbers and serial numbers match | REQ-02, REQ-10, REQ-11 |
| Data Sheet Cross-Reference | Verify records are traceable to DEL-12.04 data sheet parameters; verify equipment in records (tag, serial, manufacturer, model) matches equipment in data sheets | REQ-03 |
| Acceptance Criteria Review | Review accuracy verification/proving records against acceptance criteria from DEL-12.02 specification and DEL-12.03 calculations; verify proving results meet criteria (meter factor within range, proving repeatability acceptable, accuracy verified) | REQ-05, REQ-09 |
| Calibration Traceability Review | Review calibration certificates for traceability to national standards (Measurement Canada, NIST, or equivalent); verify traceability statements are complete and unbroken; verify calibration standards are identified with certificate numbers | REQ-06, REQ-07 |
| Calibration Certificate Completeness | Verify calibration certificates include all required information: equipment ID (tag, serial), calibration date, calibration range, as-found/as-left values, calibration uncertainty, calibrator ID, next calibration due | REQ-07 |
| Proving Record Completeness | Verify proving records include all required information: proving method, date, conditions (flow rate, temperature, pressure), proving run data, meter factor calculation, repeatability, acceptance criteria, acceptance statement (pass/fail), signatures | REQ-08 |
| Signature and Witnessing Review | Verify required signatures are present: test performer, reviewer, approver, witness (if required); verify signatures are authorized per project procedures | REQ-16 |
| Legibility and Format Check | Verify records are complete, legible, and in approved format; no critical blank fields, readable text, acceptable electronic or hardcopy format | REQ-17 |
| NCR Review | If nonconformances occurred, verify NCRs are included documenting issue, corrective action, verification, and acceptance; verify all NCRs are closed before package issue | REQ-18 |
| Document Control Check | Verify record package complies with project document control procedures: record numbering, revision control, filing location, distribution list | REQ-13 |

### Acceptance Criteria

| Criterion | Description | Source |
|-----------|-------------|--------|
| Record Completeness | All required records present per record index for all metering equipment (flow meters ×2, temperature transmitters, pressure transmitters if applicable) | Decomposition:360; REQ-01 |
| Equipment Traceability | Records traceable to equipment tags and serial numbers per DEL-12.04 data sheets; tag and serial numbers consistent across records and data sheets | REQ-02, REQ-03, REQ-10, REQ-11 |
| Calibration Traceability | Calibration certificates demonstrate traceability to national standards (Measurement Canada, NIST, or equivalent); traceability statements complete and unbroken | REQ-06 |
| Calibration Certificate Completeness | Calibration certificates include all required fields (equipment ID, date, range, results, uncertainty, calibrator, next calibration) | REQ-07 |
| Accuracy Compliance | Accuracy verification/proving results meet acceptance criteria from DEL-12.02 and DEL-12.03; meter factors within acceptable range, proving repeatability acceptable, accuracy verified | REQ-05, REQ-09 |
| Proving Record Completeness | Proving records include all required fields (method, date, conditions, run data, meter factor, repeatability, acceptance criteria, acceptance statement, signatures) | REQ-08 |
| Signatures Complete | Required signatures present and authorized: test performer, reviewer, approver, witness (if required per ER or Measurement Canada) | REQ-16 |
| Records Legible and Complete | Records complete (no critical blank fields), legible (readable), approved format (PDF, electronic, or per project standard) | REQ-17 |
| NCRs Closed | If NCRs exist, all are closed with verified corrective actions and client acceptance | REQ-18 |
| Document Control Compliance | Record package complies with project document control procedures (numbering, revision, filing, distribution) | REQ-13 |
| Cross-Deliverable Consistency | Record package references DEL-12.01, DEL-12.02, DEL-12.03, DEL-12.04; demonstrates installation and testing per design intent | REQ-12 |

## Documentation

### Required Documentation Outputs

| Output | Description | Source |
|--------|-------------|--------|
| Calibration Certificate — Flow Meter Rail Unloading | Factory calibration certificate for rail unloading custody transfer flow meter with traceability to national standards | Decomposition:360; REQ-01, REQ-06, REQ-07 |
| Calibration Certificate — Flow Meter Marine Loading | Factory calibration certificate for marine loading custody transfer flow meter with traceability to national standards | Decomposition:360; REQ-01, REQ-06, REQ-07 |
| Calibration Certificates — Temperature Transmitters | Calibration certificates for temperature transmitters (rail and marine services) | Decomposition:360; REQ-01, REQ-06, REQ-07 |
| Calibration Certificates — Pressure Transmitters | Calibration certificates for pressure transmitters if applicable (rail and marine services) | Decomposition:360; REQ-01, REQ-06, REQ-07 |
| Proving Record — Rail Unloading Flow Meter | Initial proving upon commissioning for rail unloading flow meter; proving run data, meter factor, acceptance verification | Decomposition:360; REQ-01, REQ-05, REQ-08 |
| Proving Record — Marine Loading Flow Meter | Initial proving upon commissioning for marine loading flow meter; proving run data, meter factor, acceptance verification | Decomposition:360; REQ-01, REQ-05, REQ-08 |
| Record Index / Traceability Map | Index listing all records with equipment tags, serials, record types, dates, references, witness info, status | REQ-04 |
| FAT Records (if applicable) | Factory acceptance test protocols and results; FAT witness reports; FAT NCRs and resolutions | TBD; if required by ER Vol 2 Part 2 or DEL-12.02 |
| Installation Verification Records (optional but recommended) | Installation checklists, inspection reports, dimensional verification, as-built verification | ASSUMPTION; best practice |
| SAT Records (if applicable) | Site acceptance test protocols and results; functional testing; proving upon installation; SAT acceptance | TBD; if required by ER Vol 2 Part 2 or DEL-12.02 |
| Material Certificates (if required) | Material test reports (MTRs) for critical components | TBD; if required by DEL-12.02 for food-grade or high-integrity service |
| Nonconformance Reports (if any) | NCRs documenting issues during installation/testing; corrective actions; verification; client acceptance | REQ-18; if issues occurred |

### Record Package Structure

The record package should be organized per Datasheet.md record package structure with the following components:

| Section | Content | Requirements Addressed |
|---------|---------|----------------------|
| **Cover Sheet** | Project identification (project name, project number, contractor name), deliverable identification (DEL-12.05 Metering Installation & Test Records), package revision (00 initial, A/B/C or 01/02/03 subsequent), issue date, QA/QC lead signature, approver signature, revision history | REQ-13, REQ-14, REQ-16 |
| **Record Index** | Table with columns: Equipment Tag Number, Equipment Serial Number, Service (Rail/Marine), Equipment Description, Record Type (Cal Cert, Proving, FAT, SAT, MTR, NCR), Record Date, Record Reference (section or file name), Witness (if applicable), Status (Complete, Pending, N/A); index provides traceability and quick location of records | REQ-04 |
| **Section 1: Calibration Certificates** | 1.1 Flow Meter Calibration Certificates (rail and marine); 1.2 Temperature Transmitter Calibration Certificates; 1.3 Pressure Transmitter Calibration Certificates (if applicable); 1.4 Density Transmitter Calibration Certificates (if separate from Coriolis meter); 1.5 Field Calibration Records (if field calibration verification performed) | REQ-01, REQ-06, REQ-07, REQ-10 |
| **Section 2: Factory Acceptance Test (FAT) Records** (if applicable) | FAT protocols and results for flow meters and transmitters; FAT witness reports (if FAT witnessed); FAT NCRs and resolutions (if issues during FAT) | TBD; if required by ER or DEL-12.02 |
| **Section 3: Installation Verification Records** (optional but recommended) | Installation checklists (verify installation per DEL-12.01 drawings); installation inspection reports; dimensional verification (straight-run measurements, orientation verification, elevation measurements); piping connection verification (flange torques per spec, gasket installation, alignment); electrical connection verification (power supply, signal wiring, grounding, continuity checks) | ASSUMPTION; best practice for QA |
| **Section 4: Site Acceptance Test (SAT) Records** (if applicable) | SAT protocols and results; functional testing (flow measurement, temperature measurement, pressure measurement, signal transmission to DCS, totalizing function, alarm functions); proving upon installation (initial proving to establish baseline); SAT acceptance verification with signatures | TBD; if required by ER or DEL-12.02 |
| **Section 5: Accuracy Verification / Proving Records** | 5.1 Initial Proving (Commissioning): Proving records upon installation for rail and marine flow meters; 5.2 Periodic Proving (if applicable): Subsequent proving records if periodic proving performed before handover | REQ-01, REQ-05, REQ-08, REQ-09, REQ-11 |
| **Section 6: Material Certificates** (if required) | Material test reports (MTRs) for wetted components (flow meter body, internals); chemical composition, mechanical properties, heat lot traceability | TBD; if required by DEL-12.02 |
| **Section 7: Nonconformance Reports (NCRs)** (if any) | NCRs for issues during installation/testing; corrective actions; verification; client acceptance | REQ-18 |
| **Section 8: Witness Signatures** | Consolidated witness signature pages for witnessed activities; FAT witness signatures, installation inspection witness signatures, proving witness signatures, final acceptance witness signature | REQ-16 |
| **Appendices** | Appendix A: Cross-reference to related deliverables (DEL-12.01, DEL-12.02, DEL-12.03, DEL-12.04); Appendix B: Vendor data sheet references; Appendix C: Applicable standard excerpts (if proving procedure references standard) | REQ-12 |

### Documentation Requirements

| Requirement | Description | Source |
|-------------|-------------|--------|
| Equipment Index | Index mapping each record to tag number and serial number per REQ-04 | ASSUMPTION |
| Traceability Documentation | Clear traceability chain for calibration from equipment to national standard per REQ-06 | ASSUMPTION |
| Acceptance Documentation | Clear statement of acceptance criteria (from DEL-12.02 and DEL-12.03) and test results demonstrating compliance per REQ-05 | ASSUMPTION |
| Revision Control | Record package revision history per project document control procedures per REQ-13 | TBD; ER Vol 2 Part 1 |
| Cross-Reference | Reference to related deliverables (DEL-12.01, DEL-12.02, DEL-12.03, DEL-12.04) per REQ-12 | ASSUMPTION |

## Cross-Document Traceability

| Document | Traceability Points |
|----------|---------------------|
| Datasheet.md | Identification section defines record package attributes (number, category, retention period, classification); Conditions section lists design context (service application, record scope, equipment covered, services) and record requirements context (calibration standard, accuracy verification method, proving frequency, acceptance criteria, witnessing, archive format — all TBD sources); Construction section lists anticipated record content (calibration certificates, accuracy verification records) matching REQ-01 and defines record package structure (cover sheet, record index, calibration certificates, FAT, installation verification, SAT, proving records, MTRs, NCRs, witness signatures, appendices) matching Documentation section structure above; Construction section also defines equipment-to-record traceability matching REQ-02, REQ-10, REQ-11 |
| Guidance.md | Purpose section explains records serve as auditable evidence that custody transfer metering was properly installed, calibrated, and accuracy-verified; demonstrates compliance with specification and regulatory requirements (per REQ-05, REQ-06); Principles section explains record development rationale (evidence of compliance per REQ-05, traceability per REQ-02/REQ-03/REQ-06, auditability per REQ-17, regulatory support for Measurement Canada) and custody transfer record principles (calibration traceability per REQ-06, proving documentation per REQ-08, witnessing per REQ-16); Considerations section identifies record content considerations (minimum content per Decomposition:360, equipment coverage, acceptance criteria documentation per REQ-05, witnessing per REQ-16), calibration certificate field considerations (matching REQ-07 content requirements), proving record field considerations (matching REQ-08 content requirements) |
| Procedure.md | Steps section defines record collection and compilation workflow aligned to requirements: Step 1 (Define required record set per REQ-01), Step 2 (Establish traceability map per REQ-02, REQ-04), Step 3 (Collect calibration certificates per REQ-01, REQ-06; verify traceability per REQ-06, verify completeness per REQ-07, verify equipment traceability per REQ-10), Step 4 (Collect proving records per REQ-01, REQ-05; verify completeness per REQ-08, verify equipment traceability per REQ-11, verify acceptance per REQ-05), Step 5 (Verify completeness per REQ-17, validity per REQ-05/REQ-06, signatures per REQ-16, NCRs per REQ-18), Step 6 (Compile record package per Documentation section structure), Step 7 (Issue with approvals per REQ-16); Verification section confirms requirement satisfaction per Acceptance Criteria; Records section identifies record outputs matching Documentation section |
