# Procedure: DEL-12.05 Metering Installation & Test Records

## Purpose

This procedure defines the process for producing and managing **Metering Installation & Test Records** within **PKG-12 Product Transfer & Metering**.

### Deliverable Definition

DEL-12.05 provides evidence of completion, inspection, and testing for custody transfer metering (Source: Decomposition:360).

| Attribute | Value |
|-----------|-------|
| Deliverable Type | Record |
| Discipline | Process |
| Responsible Party | D&B Contractor (QA/QC) |
| Service Application | Custody transfer metering for CSD canola oil at rail unloading and marine loading; associated instrumentation |

### Procedure Scope

This procedure covers the complete lifecycle for producing the metering installation and test record package:

1. **Planning** — identifying required records, establishing traceability map
2. **Collection** — collecting calibration certificates, test records, proving records, vendor documentation
3. **Verification** — verifying completeness, validity, signatures, traceability
4. **Compilation** — organizing records into structured package
5. **Issue and archival** — obtaining approvals, issuing package, archiving per retention requirements

This procedure applies to all custody transfer metering equipment: flow meters (rail unloading and marine loading), temperature transmitters, pressure transmitters, and associated proving equipment.

## Prerequisites

### Dependencies

| Prerequisite | Status | Notes |
|--------------|--------|-------|
| Dependency Mode | NOT_TRACKED | Dependencies coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`); coordinate with installation and commissioning teams for record collection; coordinate with vendors for certificates |

### Required Completion Status

Record package can only be completed after certain project milestones are achieved (logical prerequisites, not tracked dependencies):

| Milestone | Significance | Records Dependent |
|-----------|--------------|-------------------|
| Equipment Procurement Complete | Vendor selection finalized; equipment ordered; serial numbers assigned | Calibration certificates (vendor provides after manufacturing); equipment serial numbers needed for traceability |
| Equipment Delivery | Equipment delivered to site; receiving inspection complete | Receiving inspection records; verify serial numbers match purchase order and calibration certificates |
| Installation Complete | Equipment installed per DEL-12.01 drawings; installation inspected | Installation verification records; as-built verification; ready for commissioning |
| Commissioning Complete | System functional; initial proving performed; SAT complete (if applicable) | SAT records, initial proving records; commissioning establishes baseline meter factors |

### Recommended Upstream Inputs

The following inputs are necessary for record collection and verification (ASSUMPTION based on typical QA record workflow):

| Input | Source | Purpose | Timing |
|-------|--------|---------|--------|
| Metering Technical Specification | DEL-12.02 | Acceptance criteria for verification; FAT/SAT requirements; calibration traceability requirements; proving requirements | Before record collection; provides acceptance criteria for comparison |
| Metering Design Calculations | DEL-12.03 | Proving methodology and acceptance criteria (meter factor limits, proving repeatability, drift limits); provides detailed acceptance criteria | Before proving; provides proving acceptance criteria |
| Metering Data Sheet Package | DEL-12.04 | Equipment tags, serial numbers, manufacturers, models; provides equipment identification for record traceability | Before record collection; provides equipment list and traceability basis |
| Vendor Calibration Certificates | Equipment vendors | Factory calibration certificates with traceability to national standards | During FAT or before shipment; collected during procurement/delivery phase |
| Proving Results | Commissioning team | Proving run data, meter factors, acceptance verification; provides accuracy verification evidence | During commissioning; collected after initial proving is performed |
| Project Quality Management Plan | Project Quality | QA/QC procedures, inspection and test plan (ITP), hold points, witness points, record formats, retention requirements | Before record collection; defines QA requirements and record standards |

### Reference Materials

| Reference | Location | Purpose |
|-----------|----------|---------|
| `_REFERENCES.md` | Deliverable folder | Applicable reference documents; list of ER clauses, specifications, calculations, data sheets, QA plan |
| `0_References/` | Package directory | Reference materials for PKG-12 (ER excerpts, standards, vendor literature, product data) |
| Employer's Requirements Vol 2 Part 1 | ER document set | General requirements, document control, QA procedures, witnessing requirements, records retention, archive format | TBD |
| Employer's Requirements Vol 2 Part 2 | ER document set | Process mechanical requirements, metering testing requirements, accuracy verification requirements, regulatory compliance (Measurement Canada), FAT/SAT requirements | TBD |
| Decomposition | Project root | PKG-12 scope (line 350), DEL-12.05 definition (line 360), objective mapping (line 789) |
| Specification.md | Deliverable folder | Requirements to be satisfied (REQ-01 through REQ-19); defines record package scope, content requirements, quality requirements |
| Guidance.md | Deliverable folder | Record development considerations, principles, trade-offs, calibration certificate field guidance, proving record field guidance, service-specific considerations, timing considerations |
| Datasheet.md | Deliverable folder | Design context, record requirements context (TBD items), anticipated record content, record package structure, equipment-to-record traceability |

### Personnel Requirements

| Role | Qualification | Responsibility | Source |
|------|---------------|----------------|--------|
| QA/QC Lead | Qualified QA/QC professional; familiarity with custody transfer QA requirements and record management | Record package planning, record collection coordination, completeness verification, compilation, approval coordination, issuance | ASSUMPTION; project quality procedures |
| Test Performers | Qualified technicians for calibration, installation, proving (may be vendor technicians, contractor technicians, or third-party inspection); certifications may be required (Measurement Canada authorized persons, manufacturer-trained, certified calibration technician) | Perform tests (calibration, installation, proving); document test results; sign test records confirming results are accurate | ASSUMPTION; qualifications TBD from ER or Measurement Canada |
| Independent Reviewer | Independent engineer or QA personnel (not the test performer) | Review test records for completeness and correctness; verify test results meet acceptance criteria; sign records confirming review | ASSUMPTION; project quality procedures |
| Approver | Authorized per project procedures (typically QA/QC Manager or Project Manager) | Approve record package for issue; confirm all records are complete and compliant | TBD; ER Vol 2 Part 1 |
| Witness | Third-party inspector, client representative, or Measurement Canada representative (if witnessing required) | Witness critical tests (FAT, installation inspection, proving); sign witness statements confirming tests were performed per procedure and results are valid | TBD; witnessing requirements from ER Vol 2 Part 1 or Measurement Canada |

### Tools and Systems

| Tool/System | Purpose | Source |
|-------------|---------|--------|
| Document Management System | Record package storage, archival, distribution; electronic record management | TBD; ER Vol 2 Part 1 |
| Proving Equipment | In-line prover, portable prover, or master meter per DEL-12.02 | Accuracy verification; proving equipment must be calibrated and traceable |
| Calibration Equipment | Temperature calibrators, pressure calibrators (if field calibration performed) | Field calibration verification (if applicable) |

## Steps

### Step 1: Define Required Record Set

**Objective:** Determine all records required for metering installation and test record package per Specification.md REQ-01.

| Action | Description | Output |
|--------|-------------|--------|
| 1.1 | Confirm minimum required records per Decomposition:360 and Specification.md REQ-01: (1) Calibration certificates for flow meters (rail unloading and marine loading), (2) Accuracy verification/proving records for flow meters, (3) Calibration certificates for temperature transmitters (rail and marine services), (4) Calibration certificates for pressure transmitters if applicable | Minimum record list from decomposition |
| 1.2 | Review ER Vol 2 Part 1 for additional QA record requirements: review QA section for inspection and test requirements, witnessing requirements, record submission requirements; identify any additional required records beyond decomposition minimum (e.g., FAT records, installation inspection, SAT records, material certificates) | Additional records from ER Vol 2 Part 1 (TBD) |
| 1.3 | Review ER Vol 2 Part 2 for metering-specific test requirements: review metering section for testing requirements, accuracy verification requirements, proving requirements, regulatory compliance requirements (Measurement Canada); identify metering-specific test records | Additional records from ER Vol 2 Part 2 (TBD) |
| 1.4 | Review DEL-12.02 Metering Technical Specification for specified test and documentation requirements: review FAT requirements (if FAT specified, FAT records required), SAT requirements (if SAT specified, SAT records required), proving requirements (proving method, frequency), calibration requirements (traceability, interval), material certificate requirements (if MTRs specified) | Test records from DEL-12.02 specification |
| 1.5 | Review project Quality Management Plan for ITP and record requirements: review inspection and test plan for metering equipment; identify hold points (records require witness signature), witness points (optional witness), and required inspection/test records | Test records from Quality Management Plan (TBD) |
| 1.6 | Identify all metering equipment requiring records from DEL-12.04 data sheet package: flow meter for rail unloading (tag number, serial number from DEL-12.04), flow meter for marine loading (tag, serial from DEL-12.04), temperature transmitter(s) for rail service (tags, serials), temperature transmitter(s) for marine service, pressure transmitter(s) if applicable (tags, serials); equipment list provides basis for record completeness verification | Equipment list from DEL-12.04 |
| 1.7 | Confirm witnessing requirements from ER Vol 2 Part 1 and Measurement Canada (if applicable): identify which tests require client witness, third-party witness, or Measurement Canada witness; witnessing requirements may include FAT (client witness), installation inspection (third-party witness), proving (Measurement Canada witness for regulatory approval); coordinate witness availability during testing | Witnessing requirements (TBD) |
| 1.8 | Document complete required record set in preliminary record index: list all record types required, map to equipment (which equipment requires which records), note witnessing requirements, note timing (when record will be available: FAT, delivery, installation, commissioning) | Complete required record list |

**Output:** Complete required record list with equipment mapping, witnessing requirements, and timing

**Verification:** Record list includes decomposition minimum per REQ-01; additional records from ER, DEL-12.02, and Quality Management Plan identified; all metering equipment from DEL-12.04 included

---

### Step 2: Establish Traceability Map (Record Index)

**Objective:** Create record index mapping each equipment item to required records per Specification.md REQ-04.

| Action | Description | Output |
|--------|-------------|--------|
| 2.1 | Obtain equipment list from DEL-12.04 data sheets per Specification.md REQ-03: extract tag numbers, serial numbers (if available; may be TBD until delivery), services (rail unloading or marine loading), equipment descriptions (Coriolis flow meter, RTD temperature transmitter, pressure transmitter), manufacturers and models (if vendor selected; may be TBD); equipment list provides basis for record traceability | Equipment list from DEL-12.04 |
| 2.2 | Create record index table with columns per Specification.md REQ-04: **Equipment Tag Number** (from DEL-12.04 and P&IDs), **Equipment Serial Number** (from DEL-12.04 vendor data or equipment nameplate; may be TBD until delivery), **Service** (Rail Unloading or Marine Loading), **Equipment Description** (type and manufacturer/model from DEL-12.04), **Record Type** (Cal Cert, FAT, Install Verify, SAT, Proving, MTR, NCR), **Record Date** (date record was created; TBD until test performed), **Record Reference** (section number, file name, or document number where record is located in package), **Witness** (witness name and organization if witnessing required; TBD until test performed), **Status** (Complete when record is collected, Pending if awaiting test, N/A if record type not applicable to this equipment) | Record index template |
| 2.3 | Populate record index with expected records for each equipment item: for each equipment tag number from DEL-12.04, add rows for all required record types (from Step 1 required record list); example: FT-1201 (rail unloading flow meter) requires: calibration certificate, FAT record (if applicable), installation verification, SAT record (if applicable), initial proving record, periodic proving records (if proving performed before handover) | Populated record index with expected records |
| 2.4 | Assign record tracking numbers if needed per project document control procedures (TBD): some projects assign tracking numbers to records (e.g., REC-12-001, REC-12-002); tracking numbers facilitate record location and retrieval; may not be needed if records are identified by tag number and record type | Record tracking numbers (if applicable) |
| 2.5 | Review record index for completeness: verify all equipment from DEL-12.04 is included; verify all required record types from Step 1 are included for applicable equipment (e.g., flow meters require proving, transmitters do not); verify index structure per Specification.md REQ-04 | Record index completeness verification |

**Output:** Complete record index / traceability map listing all expected records for all equipment

**Verification:** Index includes all equipment from DEL-12.04 per Specification.md REQ-03; index structure per REQ-04; all required record types per REQ-01 are mapped to applicable equipment

---

### Step 3: Collect Calibration Certificates

**Objective:** Collect calibration certificates for all custody transfer metering equipment per Specification.md REQ-01, REQ-06, REQ-07.

| Action | Description | Output |
|--------|-------------|--------|
| 3.1 | Request vendor calibration certificates from procurement or vendors: coordinate with procurement to obtain factory calibration certificates for all equipment (flow meters, temperature transmitters, pressure transmitters, density transmitters if applicable); calibration certificates should be provided by vendor before or with equipment shipment; if certificates not provided, issue vendor data request (VDR) to obtain | Vendor certificate request |
| 3.2 | Verify calibration certificates include required information per Specification.md REQ-07: **Equipment identification**: Tag number (may need to be added to vendor certificate if vendor does not know project tag numbers; cross-reference serial number), serial number (must match equipment nameplate), manufacturer, model; **Calibration date**: Date calibration performed; **Calibration standard**: Reference standard identification (prover serial number, master meter serial number, or other) with reference standard calibration certificate number; **Traceability statement**: "Traceable to Measurement Canada Certificate [Number]" or "Traceable to NIST Certificate [Number]" or equivalent; **Calibration range**: Range calibrated (verify encompasses operating range from DEL-12.04); **As-found and as-left**: Accuracy before and after calibration adjustment; **Calibration uncertainty**: Measurement uncertainty of calibration (should be ≤1/3 of measurement uncertainty per ISO/IEC 17025); **Calibrator identification**: Calibrating organization, technician name and certification, laboratory accreditation (ISO/IEC 17025); **Next calibration**: Due date or interval | Certificate completeness checklist |
| 3.3 | Verify calibration traceability is complete and valid per Specification.md REQ-06: verify traceability statement is present and specific (includes certificate number of reference standard); verify reference standard is appropriate for custody transfer (prover, master meter, or other traceable to national standard); verify calibrating laboratory is accredited (ISO/IEC 17025 accredited preferred for custody transfer); verify traceability chain is unbroken (equipment → reference standard → national standard; each link documented); **Traceability validation**: If traceability is questionable (e.g., vague statement "traceable to national standards" without certificate numbers, or non-accredited laboratory), flag for vendor clarification or re-calibration from accredited lab | Traceability verification |
| 3.4 | Cross-reference calibration certificates to DEL-12.04 data sheets per Specification.md REQ-03, REQ-10: verify equipment serial numbers on certificates match serial numbers in DEL-12.04 (if serial numbers in data sheets; may be TBD until delivery); verify manufacturers and models on certificates match DEL-12.04; verify calibration ranges on certificates match or exceed specified ranges in DEL-12.04; identify any mismatches (wrong equipment, wrong serial number, range mismatch) for resolution | Cross-reference to DEL-12.04 |
| 3.5 | Obtain field calibration records if site calibration performed: if field calibration verification is performed during commissioning (not common for factory-calibrated custody transfer meters but may be done for transmitters), obtain field calibration records; verify field calibration records include similar information as factory certificates (equipment ID, date, standard used, results, uncertainty, technician, witness if required) | Field calibration records (if applicable) |
| 3.6 | Flag missing or incomplete certificates: if calibration certificates are missing for any equipment, document in record index status as "Pending" and issue VDR to vendor; if certificates are incomplete (missing required fields, traceability unclear), request vendor clarification or supplemental documentation; missing or incomplete certificates must be resolved before record package can be issued | Missing certificate tracking |
| 3.7 | File collected calibration certificates in Section 1 of record package per Datasheet.md record package structure: organize by equipment type (flow meters, temperature transmitters, pressure transmitters); within each type, organize by service (rail unloading, marine loading); include vendor certificates as provided (PDF or hardcopy scanned); add project cover sheet or transmittal form if needed to map vendor certificate to project requirements | Filed calibration certificates |

**Output:** Collected calibration certificates for all equipment; certificates verified for completeness and traceability; certificates cross-referenced to DEL-12.04; certificates filed in record package Section 1

**Verification:** Calibration certificates collected per Specification.md REQ-01; certificates include required fields per REQ-07; traceability verified per REQ-06; equipment traceability verified per REQ-10; cross-reference to DEL-12.04 verified per REQ-03

---

### Step 4: Collect Accuracy Verification / Proving Records

**Objective:** Collect proving or accuracy verification records for custody transfer flow meters per Specification.md REQ-01, REQ-05, REQ-08.

| Action | Description | Output |
|--------|-------------|--------|
| 4.1 | Coordinate with commissioning team to obtain proving records: coordinate proving schedule (proving typically performed during commissioning after installation and loop checks are complete); provide proving acceptance criteria from DEL-12.03 to commissioning team (meter factor limits, proving repeatability, drift limits from baseline if baseline exists); coordinate witness if required per ER or Measurement Canada; proving may be performed by vendor technician, contractor technician, or third-party service provider depending on proving method and project requirements | Proving coordination |
| 4.2 | Verify proving records include required information per Specification.md REQ-08: **Equipment identification**: Tag number (e.g., FT-1201), serial number (must match DEL-12.04 and equipment nameplate), service (rail unloading or marine loading); **Proving method**: In-line prover, portable prover, or master meter per DEL-12.02; **Prover identification**: Prover serial number, prover calibration certificate number (prover must be calibrated and traceable); **Proving date**: Date proving performed; **Proving personnel**: Technician who performed proving (name, organization, certification if required); **Proving conditions**: Flow rate during proving (m³/h or kg/h), product temperature (°C; affects density), product pressure (bar or kPa), product (verify CSD canola oil; proving with different product may not be valid); **Proving run data**: Individual proving runs (typical 3-5 runs per API MPMS Chapter 4): for each run, document prover volume or indicated volume, meter indicated volume, calculated meter factor for run (MF = true volume / indicated volume), temperature and pressure during run; **Average meter factor**: Average meter factor from accepted runs; **Proving repeatability**: Repeatability of proving runs (standard deviation or range of meter factors; e.g., ±0.02%); **Acceptance criteria**: Clearly state acceptance criteria from DEL-12.03 (proving repeatability limit, meter factor range, meter factor drift limit if comparing to baseline); **Acceptance verification**: Compare actual results to acceptance criteria; state "PASS — Meter meets acceptance criteria" or "FAIL — Meter does not meet criteria; see NCR [Number]"; **Signatures**: Test performer signature, reviewer signature, approver signature, witness signature (if required) | Proving record completeness checklist |
| 4.3 | Verify proving results meet acceptance criteria per Specification.md REQ-05: **Proving repeatability**: Verify actual proving repeatability (e.g., ±0.018%) meets required repeatability from DEL-12.03 (e.g., ≤±0.05% for portable prover); if repeatability not achieved, proving is invalid and must be repeated; **Meter factor range**: Verify average meter factor (e.g., 0.9987) is within acceptable range from DEL-12.03 (e.g., 0.995-1.005); if meter factor is outside range, investigate (meter calibration issue, prover issue, proving procedure issue) and take corrective action (re-calibrate meter, re-prove, document NCR); **Meter factor drift** (for periodic proving): If baseline meter factor exists (from previous proving), verify drift is within acceptable limit from DEL-12.03 (e.g., <±0.05% drift); excessive drift indicates meter degradation; **Pass/fail**: Verify record includes clear acceptance statement; if proving failed, verify NCR exists documenting corrective action | Proving acceptance verification |
| 4.4 | Cross-reference proving records to DEL-12.04 data sheets per Specification.md REQ-03, REQ-11: verify equipment tag numbers and serial numbers on proving records match DEL-12.04 data sheets; verify services match (rail unloading, marine loading); verify proving method on proving records matches proving method in DEL-12.04 data sheets (from DEL-12.02 specification); identify any mismatches for resolution | Cross-reference to DEL-12.04 |
| 4.5 | Obtain FAT accuracy verification records if FAT was performed per DEL-12.02: if FAT includes accuracy verification (flow testing at multiple flow rates), obtain FAT records as supplemental accuracy verification in addition to site proving; FAT records may include flow tests at vendor facility using vendor test bench or portable prover; FAT provides early accuracy verification before shipment | FAT accuracy records (if applicable) |
| 4.6 | Flag missing or incomplete proving records: if proving has not been performed, document in record index status as "Pending" and coordinate with commissioning team to schedule proving; if proving records are incomplete (missing acceptance statement, missing signatures, missing witness), obtain missing information; proving records must be complete before record package can be issued for custody transfer operations | Missing proving record tracking |
| 4.7 | File collected proving records in Section 5 of record package per Datasheet.md record package structure: organize proving records by equipment (rail unloading flow meter proving, marine loading flow meter proving); include initial proving (commissioning) and periodic proving (if performed before handover); include proving run data sheets, meter factor calculation sheets, acceptance verification, witness signatures | Filed proving records |

**Output:** Collected proving records for flow meters; records verified for completeness and acceptance; records cross-referenced to DEL-12.04; records filed in record package Section 5

**Verification:** Proving records collected per Specification.md REQ-01; records include required fields per REQ-08; proving results meet acceptance criteria per REQ-05; equipment traceability verified per REQ-11; cross-reference to DEL-12.04 verified per REQ-03

---

### Step 5: Verify Completeness and Validity

**Objective:** Verify all records are complete, valid, traceable, and compliant before compiling final package.

| Action | Description | Verification |
|--------|-------------|--------------|
| 5.1 | Review all records against required record list from Step 1: for each equipment item, verify all required records are present (calibration certificate, FAT if applicable, installation verification if applicable, SAT if applicable, proving record); mark record index status "Complete" for collected records, "Pending" for missing records, "N/A" for non-applicable records; verify all critical records are Complete (calibration certificates and proving records are critical per Decomposition:360; other records may be Pending if not yet performed) | Record completeness check per REQ-01 |
| 5.2 | Verify equipment tag and serial traceability for all records per Specification.md REQ-02, REQ-03: cross-reference record index to DEL-12.04 data sheets; verify tag numbers in records match DEL-12.04 tag numbers; verify serial numbers in records match DEL-12.04 serial numbers (and match equipment nameplates if equipment delivered); verify services match (rail/marine); identify any tag or serial number mismatches (may indicate wrong equipment or data entry error); resolve mismatches before finalizing package | Traceability check per REQ-02, REQ-03 |
| 5.3 | Verify calibration traceability statements are complete per Specification.md REQ-06: for each calibration certificate, verify traceability statement is present and specific (includes national standard reference and certificate number); verify calibration standard is identified; verify calibrating laboratory is accredited (ISO/IEC 17025 preferred); verify traceability chain is logical and unbroken; flag any questionable traceability for vendor clarification | Calibration traceability verification per REQ-06 |
| 5.4 | Verify accuracy verification results meet acceptance criteria per Specification.md REQ-05: for each proving record, verify proving results meet acceptance criteria from DEL-12.03 (proving repeatability acceptable, meter factor within range, meter factor drift acceptable); verify acceptance statement is clear ("PASS" or "FAIL"); if any proving failed, verify NCR exists documenting issue and corrective action; verify corrective action was effective (re-proving after corrective action shows PASS) | Acceptance criteria verification per REQ-05 |
| 5.5 | Verify required signatures and witnessing are complete per Specification.md REQ-16: for each record, verify signatures are present: test performer signature (confirms test was performed and results are accurate), reviewer signature (confirms independent review; may not be on original test sheet but on check record), approver signature (confirms acceptance; may be on package-level approval rather than individual records); for witnessed activities, verify witness signatures are present (FAT witness if required, installation inspection witness if required, proving witness if required); verify witness qualifications if specified (Measurement Canada authorized person, certified inspector); flag missing signatures for completion | Signature and witnessing verification per REQ-16 |
| 5.6 | Verify records are legible and in approved format per Specification.md REQ-17: verify records are complete (no critical blank fields; if field is not applicable, marked N/A); verify records are legible (readable text, clear scans if hardcopy records scanned to PDF); verify format is acceptable (PDF, scanned image, or per project document control; TBD from ER Vol 2 Part 1); if records are illegible (poor scan quality, faded handwriting), obtain clearer copies; if records are incomplete, obtain missing information | Legibility and format verification per REQ-17 |
| 5.7 | Document nonconformances and verify closure per Specification.md REQ-18: review all test records for nonconformances (test failures, equipment defects, installation defects); verify NCRs exist for all nonconformances; verify NCRs document: issue description, root cause (if determined), corrective action taken (re-test, re-calibrate, repair, replace), verification of corrective action (re-test after corrective action shows compliance), client acceptance of disposition (client signature accepting NCR resolution); verify all NCRs are closed (corrective actions complete and verified) before record package issue; open NCRs prevent package issue | NCR verification and closure per REQ-18 |
| 5.8 | Identify any missing records or issues: create punchlist of missing records (equipment with Pending status in record index), incomplete records (missing required fields), missing signatures (unsigned records), unresolved NCRs (NCRs not closed); punchlist identifies items to be resolved before package can be issued | Punchlist of missing items |
| 5.9 | Coordinate resolution of missing items: for missing records, coordinate with responsible parties (vendors for certificates, commissioning team for proving, installation team for installation verification); for missing signatures, obtain signatures from authorized personnel; for unresolved NCRs, coordinate NCR closure; update record index as items are completed | Punchlist resolution |

**Output:** Verified record set with completeness, traceability, acceptance, signatures, legibility confirmed; punchlist of missing items; coordination for missing item resolution

**Verification:** Record completeness verified per Specification.md REQ-01, REQ-17; traceability verified per REQ-02, REQ-03, REQ-06, REQ-10, REQ-11; acceptance criteria met per REQ-05; signatures complete per REQ-16; NCRs closed per REQ-18

---

### Step 6: Compile Record Package

**Objective:** Organize records into structured package per Datasheet.md record package structure and Specification.md Documentation section.

| Action | Description | Output |
|--------|-------------|--------|
| 6.1 | Prepare package cover sheet per Specification.md REQ-14: **Project identification**: Project name (Canola Oil Transload Facility), project number, contractor name (D&B Contractor); **Deliverable identification**: Deliverable ID (DEL-12.05), deliverable name (Metering Installation & Test Records), package revision (00 for initial, A/B/C or 01/02/03 for subsequent per project convention; TBD), issue date; **Signatures**: QA/QC lead signature (confirms package completeness and quality), approver signature (authorizes package issue; typically Project Manager or QA/QC Manager); **Revision history**: Table with revision number, date, description of changes, QA/QC lead, approver | Package cover sheet |
| 6.2 | Finalize record index with all record references: update record index from Step 2 with actual record information: actual record dates (dates tests were performed), actual record references (section numbers or file names where records are located in package), actual witness information (witness names and organizations from signed records), status updated to "Complete" for all collected records (verify all critical records are Complete; Pending items should be resolved before issue); record index provides table of contents and traceability map for package | Finalized record index |
| 6.3 | Organize records into sections per Datasheet.md record package structure and Specification.md Documentation section: **Section 1: Calibration Certificates** (flow meters, temperature transmitters, pressure transmitters, field calibration if applicable), **Section 2: FAT Records** (if applicable), **Section 3: Installation Verification Records** (if applicable), **Section 4: SAT Records** (if applicable), **Section 5: Accuracy Verification / Proving Records** (initial proving for rail and marine flow meters, periodic proving if applicable), **Section 6: Material Certificates** (MTRs if required), **Section 7: Nonconformance Reports** (NCRs if any), **Section 8: Witness Signatures** (consolidated witness signature pages); within each section, organize by equipment tag number for easy reference | Organized record package sections |
| 6.4 | Include nonconformance and corrective action records if applicable per Specification.md REQ-18: compile all NCRs raised during installation and testing (equipment defects, installation defects, test failures); verify NCRs are closed (corrective actions complete, verification of effectiveness, client acceptance if significant); include NCR records in Section 7; if no NCRs, include statement "No nonconformances identified during installation and testing" in Section 7 | NCR section (Section 7) |
| 6.5 | Add appendices per Specification.md REQ-12 and Datasheet.md record package structure: **Appendix A: Cross-Reference to Related Deliverables** — list related deliverables with brief description: DEL-12.01 (drawings define installation), DEL-12.02 (specification defines acceptance criteria), DEL-12.03 (calculations define proving criteria), DEL-12.04 (data sheets define equipment parameters); **Appendix B: Vendor Data Sheet References** — list vendor data sheets and document numbers for cross-reference; **Appendix C: Applicable Standard Excerpts** — if proving procedures or acceptance criteria reference specific standard clauses, include excerpts (e.g., API MPMS Chapter 4 proving acceptance criteria, OIML R117 accuracy class definitions); appendices provide supporting documentation | Appendices |
| 6.6 | Apply record package numbering and revision control per project document control procedures (TBD; ER Vol 2 Part 1): assign package document number per project numbering system (e.g., REC-PKG-12-05 or per project convention), assign package revision (00 initial, A/B/C or 01/02/03 subsequent), add package metadata (title, revision, date, originator, approver) | Package numbering and metadata |

**Output:** Compiled record package with cover sheet, record index, all record sections, appendices; package organized per structure; package numbered and revision controlled

**Verification:** Package structure per Datasheet.md record package structure and Specification.md Documentation section; package organization per REQ-14; cross-references per REQ-12

---

### Step 7: Issue for Review and Acceptance

**Objective:** Obtain independent review, approvals, and issue record package; archive per retention requirements.

| Action | Description | Output |
|--------|-------------|--------|
| 7.1 | Independent review of record package for completeness and compliance: independent reviewer (not QA/QC lead who compiled package; may be senior QA/QC engineer, engineering manager, or designated checker) reviews complete record package; verify all required records present per record index; verify equipment traceability complete; verify calibration traceability complete; verify proving results meet acceptance criteria; verify signatures and witnessing complete; verify records are legible and properly formatted; verify NCRs are closed; prepare review comments if any issues identified | Independent review; review comment list (if issues) |
| 7.2 | Resolve review comments: coordinate with reviewer to resolve comments (obtain missing records, clarify traceability, obtain missing signatures); update record package as needed to resolve comments; obtain reviewer confirmation that comments are resolved | Comment resolution |
| 7.3 | Obtain QA/QC lead and approver signatures per Specification.md REQ-16: **QA/QC lead signature** on package cover sheet confirming package is complete and compliant (all required records present, all equipment covered, all traceability verified, all acceptance criteria met, all signatures obtained); **Approver signature** on package cover sheet authorizing package issue (typically Project Manager or QA/QC Manager; approval authority per project procedures TBD from ER Vol 2 Part 1); approver confirms package satisfies ER and project requirements and is suitable for client handover | Package approvals |
| 7.4 | Obtain client acceptance if required per project procedures: if ER requires client review and acceptance of QA records before project handover, submit record package to client for review; client may review for completeness, traceability, compliance; client may accept package or provide comments; resolve client comments before final issue; obtain client acceptance signature or letter | Client acceptance (if required) |
| 7.5 | Issue record package per project document control process per Specification.md REQ-13: submit to document management system, assign final document number and revision if not assigned in Step 6.6, assign issue status ("Issued for Review" for client review issues, "Issued for Project Closeout" for final handover, "Issued for Record" for archive; TBD per project convention), distribute to required recipients per distribution list (client, project management, operations team if applicable, regulatory authority if applicable; distribution list TBD) | Document management system entry; distribution |
| 7.6 | Archive in approved format and location per Specification.md REQ-13 and retention requirements: file record package in approved archive location per ER Vol 2 Part 1 document control procedures (may be document management system, physical file room, or both); verify archive format is compliant (PDF, scanned hardcopy, or per project standard); verify retention period is set per ER requirements and regulatory requirements (Measurement Canada may require long-term retention; typical custody transfer records retained for life of facility or per regulatory requirement); ensure archived records are backed up and retrievable for future reference, audit, or dispute resolution | Archived record package |
| 7.7 | Place issued copy in deliverable folder structure: place complete record package in `3_Issued/` folder within DEL-12.05 deliverable directory; filed copy provides local access to issued records | Filed issue copy in `3_Issued/` |
| 7.8 | Update deliverable status: update `_STATUS.md` to ISSUED with note "Record package issued, Rev 00, Date YYYY-MM-DD; records cover [equipment count] custody transfer metering equipment for rail unloading and marine loading services; all calibration certificates and proving records complete"; record status update in `_STATUS.md` history section | Status update to ISSUED |

**Output:** Issued record package with all approvals; package distributed per distribution list; package archived per retention requirements; deliverable status updated to ISSUED

**Verification:** Independent review complete; all approvals obtained; package issued per document control procedures per Specification.md REQ-13; package archived per retention requirements

---

## Verification

### Verification Activities

| Activity | Requirement Verified | Method | Record |
|----------|---------------------|--------|--------|
| Record completeness check | REQ-01 | Checklist against Decomposition:360 and record index — verify calibration certificates and proving records for all equipment | Record index Step 2; completeness check Step 5.1 |
| Equipment traceability check | REQ-02, REQ-10, REQ-11 | Cross-reference records to DEL-12.04 data sheets — verify tag numbers and serial numbers match | Traceability check Step 5.2; cross-reference Step 3.4, Step 4.4 |
| Data sheet cross-reference | REQ-03 | Cross-reference record equipment to DEL-12.04 parameters — verify consistency | Cross-reference Step 3.4, Step 4.4 |
| Record index completeness | REQ-04 | Verify record index includes all required fields (tag, serial, service, record type, date, reference, witness, status) | Record index Step 2.5 |
| Proving acceptance check | REQ-05, REQ-09 | Review proving results against acceptance criteria from DEL-12.03 — verify pass/fail determination | Proving acceptance verification Step 4.3 |
| Calibration traceability check | REQ-06 | Review calibration certificates for traceability statements and unbroken chain to national standards | Traceability verification Step 3.3 |
| Calibration certificate completeness | REQ-07 | Verify certificates include all required fields (equipment ID, date, standard, range, results, uncertainty, calibrator, next calibration) | Certificate completeness check Step 3.2 |
| Proving record completeness | REQ-08 | Verify proving records include all required fields (method, date, conditions, runs, meter factor, acceptance, signatures) | Proving record completeness check Step 4.2 |
| Signature and witnessing check | REQ-16 | Verify all required signatures present (performer, reviewer, approver, witness if required) | Signature check Step 5.5 |
| Legibility and format check | REQ-17 | Verify records complete, legible, approved format | Legibility check Step 5.6 |
| NCR closure check | REQ-18 | If NCRs exist, verify all are closed with corrective actions and client acceptance | NCR verification Step 5.7 |
| Document control compliance | REQ-13 | Verify package numbering, revision control, distribution per project procedures | Document control check Step 6.6, Step 7.5 |
| Independent review | Step 7.1 | Independent reviewer verifies all above items before package issue | Review record Step 7.1 |

### Acceptance Criteria

| Criterion | Verification Method | Source |
|-----------|---------------------|--------|
| All required records present | Record index completeness check Step 5.1 | Specification.md REQ-01; Decomposition:360 |
| Equipment traceability complete | Tag and serial number verification Step 5.2 | Specification.md REQ-02, REQ-10, REQ-11 |
| Data sheet cross-reference verified | Cross-reference check Step 3.4, Step 4.4 | Specification.md REQ-03 |
| Record index complete | Record index verification Step 2.5 | Specification.md REQ-04 |
| Calibration certificates traceable | Traceability verification Step 3.3 | Specification.md REQ-06 |
| Calibration certificates complete | Certificate completeness check Step 3.2 | Specification.md REQ-07 |
| Proving results meet acceptance criteria | Proving acceptance check Step 4.3 | Specification.md REQ-05 |
| Proving records complete | Proving record completeness check Step 4.2 | Specification.md REQ-08 |
| Signatures and witnessing complete | Signature check Step 5.5 | Specification.md REQ-16 |
| Records legible and formatted | Legibility check Step 5.6 | Specification.md REQ-17 |
| NCRs closed | NCR verification Step 5.7 | Specification.md REQ-18 |
| Package organized per structure | Package structure check Step 6 | Specification.md REQ-14 |
| Cross-deliverable references | Cross-reference check | Specification.md REQ-12 |
| Document control compliance | Document control check Step 7.5 | Specification.md REQ-13 |
| Independent review complete | Review record Step 7.1 | Specification.md independent review |

### Sign-off Requirements

| Role | Responsibility | Verification | Source |
|------|----------------|--------------|--------|
| QA/QC Lead | Record collection, compilation, completeness verification, package approval | QA/QC lead signature on package cover sheet confirming package completeness and compliance | ASSUMPTION; project quality procedures |
| Independent Reviewer | Independent review of complete package before issue | Review record documenting independent review completion | ASSUMPTION; project quality procedures |
| Approver | Authorization for package issue; confirm records satisfy ER and project requirements | Approver signature on package cover sheet authorizing issue | TBD; ER Vol 2 Part 1 |
| Client (if required) | Client acceptance of QA records for project handover | Client acceptance signature or letter | TBD; if required by ER or contract |

## Records

### Documentation Outputs

| Output | Description | Source |
|--------|-------------|--------|
| Calibration Certificate — Flow Meter Rail Unloading | Factory calibration certificate for rail unloading flow meter with traceability to national standards (Measurement Canada, NIST, or equivalent) | Decomposition:360; Specification.md REQ-01, REQ-06, REQ-07; Step 3 |
| Calibration Certificate — Flow Meter Marine Loading | Factory calibration certificate for marine loading flow meter with traceability to national standards | Decomposition:360; Specification.md REQ-01, REQ-06, REQ-07; Step 3 |
| Calibration Certificates — Temperature Transmitters | Calibration certificates for temperature transmitters (rail and marine services) | Decomposition:360; Specification.md REQ-01, REQ-06, REQ-07; Step 3 |
| Calibration Certificates — Pressure Transmitters (if applicable) | Calibration certificates for pressure transmitters (rail and marine services) if pressure transmitters are part of system | Decomposition:360; Specification.md REQ-01, REQ-06, REQ-07; Step 3 |
| Proving Record — Rail Unloading Flow Meter | Initial proving record upon commissioning for rail unloading flow meter; proving run data, meter factor, acceptance verification per DEL-12.03 criteria | Decomposition:360; Specification.md REQ-01, REQ-05, REQ-08; Step 4 |
| Proving Record — Marine Loading Flow Meter | Initial proving record upon commissioning for marine loading flow meter; proving run data, meter factor, acceptance verification per DEL-12.03 criteria | Decomposition:360; Specification.md REQ-01, REQ-05, REQ-08; Step 4 |
| Record Index / Traceability Map | Complete index listing all records with equipment tags, serials, record types, dates, references, witnesses, status | Specification.md REQ-04; Step 2; finalized Step 6.2 |
| FAT Records (if applicable) | Factory acceptance test protocols and results; FAT witness reports; FAT NCRs and resolutions | TBD; if required by ER Vol 2 Part 2 or DEL-12.02; collected during procurement/FAT phase |
| Installation Verification Records (if applicable) | Installation checklists, inspection reports, dimensional verification, as-built verification | ASSUMPTION; best practice QA; collected during installation phase |
| SAT Records (if applicable) | Site acceptance test protocols and results; functional testing; SAT acceptance | TBD; if required by ER Vol 2 Part 2 or DEL-12.02; collected during commissioning phase |
| Material Certificates (if required) | Material test reports (MTRs) for critical components | TBD; if required by DEL-12.02; collected during procurement/FAT phase |
| Nonconformance Reports (if any) | NCRs documenting issues during installation/testing; corrective actions; verification; client acceptance | Specification.md REQ-18; collected during installation/testing phases if issues occur |
| Independent Review Record | Record of independent review before package issue | Step 7.1 |

### Record Management

| Attribute | Value | Source |
|-----------|-------|--------|
| Filing Location (Working) | `1_Working/DEL-12.05_Metering_Installation_and_Test_Records/` | Current location during compilation |
| Filing Location (Review) | `2_Checking/` (if package issued for review before final) | Project convention |
| Filing Location (Issued) | `3_Issued/` (for final issued package) | Project convention |
| Document Management System | Per project document control procedures (TBD; ER Vol 2 Part 1); electronic record management system for storage, retrieval, distribution | TBD |
| Retention Period | Per project quality procedures and regulatory requirements (TBD; ER Vol 2 Part 1); custody transfer records typically retained for life of facility or per Measurement Canada regulations; long-term retention required for commercial and regulatory compliance | TBD; likely life of facility |
| Archive Format | Electronic format (PDF scans of hardcopy records, native electronic records; per ER Vol 2 Part 1 document control); hardcopy archival may also be required for critical records (TBD) | TBD |
| Backup and Security | Per project IT procedures; backup for business continuity; access control for commercial sensitive data (custody transfer records may contain commercial transaction data) | TBD |

### Status Transitions

Status transitions are managed per `_STATUS.md` in the deliverable folder:

| From State | To State | Trigger | Responsible |
|------------|----------|---------|-------------|
| INITIALIZED | IN_PROGRESS | Record collection commences (Step 1); record index established; record collection begins during procurement/FAT phase | QA/QC Lead |
| IN_PROGRESS | CHECKING | Record package compiled and submitted for independent review (Step 7.1); all critical records collected (calibration certificates and proving records per Decomposition:360) | QA/QC Lead |
| CHECKING | IN_PROGRESS | Review comments require revision; additional records required; missing information to be obtained | QA/QC Lead |
| CHECKING | ISSUED | Independent review complete; all approvals obtained; package issued for project closeout (Step 7.8); archived per retention requirements | Approver |

**Note:** Status state transitions are recorded in `_STATUS.md` with date, state change, and brief description. Record package typically remains IN_PROGRESS for extended period (from FAT through commissioning) as records are collected progressively. Package transitions to CHECKING when compilation is complete and ready for final review. Package transitions to ISSUED upon final approval and archival.

### Revision Management

| Revision | Purpose | Typical Trigger | Approval Required |
|----------|---------|-----------------|-------------------|
| 00 | Initial record package issue | First compilation of records; may include factory records (calibration certificates, FAT) before site records (installation, SAT, proving) are available; initial issue for progress tracking | QA/QC Manager |
| A, B, C... | Subsequent issues adding records | Additional records obtained (site records after installation and commissioning); vendor data updates; periodic proving records added; progressive compilation | QA/QC Manager |
| 01, 02, 03... | Final issued package for project closeout | All records complete (factory and site records); all approvals obtained; ready for client handover and archival; final issue typically at project substantial completion or closeout | Project Manager or client acceptance |
| Operational updates | Periodic proving records added during operations | Ongoing operation; periodic proving records per DEL-12.02 proving frequency (quarterly, semi-annually, annually); records may be appended to package or filed separately in operational records | Operations Manager |

**Note:** Revision numbering convention TBD from ER Vol 2 Part 1 project document control procedures. Record packages typically have multiple revisions as records are collected progressively from procurement through commissioning.
