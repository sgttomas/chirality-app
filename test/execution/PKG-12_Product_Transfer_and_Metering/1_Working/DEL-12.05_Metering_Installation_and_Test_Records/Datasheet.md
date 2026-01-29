# Datasheet: DEL-12.05 Metering Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-12.05 |
| Name | Metering Installation & Test Records |
| Package | PKG-12 Product Transfer & Metering |
| Discipline | Process |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Record Package Number | To be issued per project numbering system (TBD; Source: ER Vol 2 Part 1, location TBD) |
| Record Category | QA/QC — Custody Transfer Metering Installation and Test Records |
| Retention Period | TBD — per project records retention requirements and regulatory requirements (Source: ER Vol 2 Part 1, location TBD); custody transfer records typically retained for life of facility or per regulatory requirement (Measurement Canada may specify retention period) |
| Revision | 00 (initial issue) |
| Classification | Process — Metering Installation and Test Records |
| Record Count (Anticipated) | Minimum record set per Decomposition:360 plus supporting records: calibration certificates (flow meters ×2, temperature transmitters ×2 or more, pressure transmitters if applicable), accuracy verification/proving records (flow meters ×2), installation verification records (optional but recommended), FAT records (factory acceptance test if applicable), SAT records (site acceptance test if applicable), material certificates (MTRs for critical components), nonconformance reports (NCRs if any issues during installation/testing); total count TBD based on equipment quantity and test scope |

## Conditions

### Design Context

| Condition | Value / Description | Source |
|-----------|---------------------|--------|
| Service Application | Custody transfer metering for CSD canola oil at rail unloading and marine loading transfer points | Decomposition:350 |
| Record Scope | Evidence of completion, inspection, and testing for metering; demonstrates that installed custody transfer metering meets specification requirements and is suitable for commercial custody transfer service | Decomposition:360 |
| Equipment Covered | Custody transfer flow meters (2): rail unloading and marine loading; temperature transmitters (2 or more): rail and marine services; pressure transmitters (if applicable): rail and marine services | Decomposition:350, 359; DEL-12.04 data sheets |
| Services | Rail unloading custody transfer metering (product receipt from rail tank cars); marine loading custody transfer metering (product export to liquid bulk carriers) | Decomposition:350 |

### Record Requirements Context

Record requirements TBD from ER Vol 2 Part 1 (QA requirements), ER Vol 2 Part 2 (metering testing requirements), DEL-12.02 specification (acceptance criteria), and applicable custody transfer standards (API MPMS, OIML R117, Measurement Canada):

| Parameter | Value | Source |
|-----------|-------|--------|
| Calibration Standard | TBD — traceability requirements per applicable standard (Measurement Canada for custody transfer in Canada, or NIST, or equivalent national metrology institute) | ER Vol 2 Part 2, location TBD; DEL-12.02 specification; Measurement Canada regulations |
| Accuracy Verification Method | TBD — proving method per DEL-12.02 specification and DEL-12.03 calculations (in-line prover, portable prover, or master meter) | DEL-12.02 specification; DEL-12.03 calculations |
| Proving Frequency | TBD — per DEL-12.02 specification and Measurement Canada regulations (quarterly, semi-annually, annually) | DEL-12.02 specification; Measurement Canada regulations |
| Proving Acceptance Criteria | TBD — meter factor limits and drift limits per DEL-12.03 calculations (e.g., meter factor 0.995-1.005, drift <±0.05%) | DEL-12.03 calculations; applicable standard (API MPMS Chapter 4, OIML R117) |
| Witnessing Requirements | TBD — client witness required for calibration or proving, or third-party inspection required (per ER Vol 2 Part 1 or Measurement Canada) | ER Vol 2 Part 1, location TBD; Measurement Canada if applicable |
| Archive Format | TBD — electronic and/or hardcopy requirements, archive location, retention period (per ER Vol 2 Part 1 document control procedures) | ER Vol 2 Part 1, location TBD |
| FAT Requirements | TBD — factory acceptance test witnessing and documentation requirements (per ER or DEL-12.02 specification) | ER Vol 2 Part 2, location TBD; DEL-12.02 specification |
| SAT Requirements | TBD — site acceptance test procedures and acceptance criteria (per ER or DEL-12.02 specification) | ER Vol 2 Part 2, location TBD; DEL-12.02 specification |

### Objective Alignment

| Objective | Relevance to This Deliverable |
|-----------|-------------------------------|
| OBJ-10 Custody Transfer Accuracy | Records provide auditable evidence of calibration and accuracy verification supporting custody transfer compliance; calibration certificates demonstrate measurement traceability to national standards (Measurement Canada, NIST); proving/accuracy verification records demonstrate meters meet accuracy requirements per DEL-12.02 and DEL-12.03; records enable commercial confidence and regulatory compliance for custody transfer transactions (Source: Decomposition:789; Specification.md REQ-04, REQ-05) |
| OBJ-6 Regulatory Compliance | Records may be required for Measurement Canada approval or other regulatory compliance for custody transfer in Canada; calibration traceability, proving records, and accuracy verification demonstrate compliance with regulatory requirements (ASSUMPTION based on Canadian location and custody transfer application) |

## Construction

### Anticipated Record Content

| Record Type | Description | Source |
|-------------|-------------|--------|
| Calibration Certificates | Factory and/or field calibration certificates for custody transfer flow meters and transmitters; certificates demonstrate calibration traceability to national measurement standards (Measurement Canada, NIST, or equivalent); certificates document calibration date, calibration range, as-found and as-left values, calibration uncertainty, calibrator identification, and next calibration due date | Decomposition:360; Specification.md REQ-01, REQ-05 |
| Accuracy Verification / Proving Records | Proving results or accuracy verification records demonstrating meter performance meets specification requirements; proving records document proving method (in-line prover, portable prover, master meter per DEL-12.02), proving conditions (flow rate, temperature, pressure during proving), proving runs (individual run data), meter factor calculation, proving repeatability, acceptance criteria (from DEL-12.03), acceptance verification (pass/fail with signature), witness signatures if required | Decomposition:360; Specification.md REQ-01, REQ-04 |

### Record Package Structure

Expected record package structure per Specification.md Documentation section (ASSUMPTION based on typical QA/QC record packages; specific structure may vary per project standards):

| Component | Description | Purpose |
|-----------|-------------|---------|
| **Cover Sheet** | Project identification (project name, project number), deliverable identification (DEL-12.05, Metering Installation & Test Records), package revision (00, A, B, or 01, 02; per project convention), issue date, QA/QC lead signature, approver signature | Identifies record package; provides approval documentation |
| **Record Index / Traceability Map** | Table listing all included records with columns: Equipment Tag Number, Equipment Serial Number, Service (Rail Unloading or Marine Loading), Equipment Description, Record Type (Calibration Certificate, Proving Record, FAT Record, SAT Record, MTR, NCR), Record Date, Record Reference (file name or document number), Witness (if applicable), Status (Complete, Pending, N/A) | Enables quick location of records; demonstrates completeness; provides traceability from equipment to records |
| **Section 1: Calibration Certificates** | **1.1 Flow Meter Calibration Certificates**: Factory calibration certificates for rail unloading and marine loading flow meters; **1.2 Temperature Transmitter Calibration Certificates**: Calibration certificates for temperature transmitters (rail and marine); **1.3 Pressure Transmitter Calibration Certificates**: Calibration certificates for pressure transmitters if applicable; **1.4 Density Transmitter Calibration Certificates**: If separate density transmitters (vs. Coriolis integral density); **Field Calibration Records**: Site calibration verification if performed | Demonstrates calibration traceability per Specification.md REQ-05 |
| **Section 2: Factory Acceptance Test (FAT) Records** (if applicable) | FAT protocols and results for flow meters; FAT witness reports; FAT nonconformance reports (NCRs) and resolutions if any issues identified during FAT; FAT may include flow testing at multiple flow rates, accuracy verification, functional testing of signals and communications, visual inspection | Demonstrates factory testing per DEL-12.02 specification FAT requirements; optional depending on ER and specification requirements |
| **Section 3: Installation Verification Records** (optional but recommended) | Installation checklists verifying installation per DEL-12.01 drawings; installation inspection reports; dimensional verification (straight-run compliance, orientation, elevations); piping connection verification (flange torques, gaskets, alignment); electrical connection verification (power supply, signal wiring, grounding); as-built verification (verify installed configuration matches design) | Demonstrates installation per drawings and specification; provides confidence that installation quality supports measurement accuracy |
| **Section 4: Site Acceptance Test (SAT) Records** (if applicable) | SAT protocols and results; functional testing of installed system (flow measurement, temperature compensation, pressure compensation, signal transmission to control system, totalizing function); proving upon installation (initial proving to establish baseline meter factor); SAT acceptance verification with signatures | Demonstrates site testing per DEL-12.02 specification SAT requirements; verifies integrated system functionality |
| **Section 5: Accuracy Verification / Proving Records** | **5.1 Initial Proving (Commissioning)**: Proving performed upon installation to establish baseline meter factor; proving method per DEL-12.02 (in-line prover, portable prover, master meter); proving run data (multiple runs for repeatability verification), meter factor calculation, proving repeatability, acceptance verification per DEL-12.03 criteria (meter factor within acceptable range, repeatability acceptable, witness signature); **5.2 Periodic Proving** (if applicable): Subsequent proving records per DEL-12.02 proving frequency (quarterly, semi-annually, annually); demonstrates ongoing accuracy maintenance | Demonstrates meter accuracy per Specification.md REQ-04; satisfies Decomposition:360 accuracy verification requirement |
| **Section 6: Material Certificates** (if required) | Material test reports (MTRs) for critical wetted components (flow meter body, internals if required); chemical composition and mechanical properties; heat lot traceability; may be required for food-grade service or high-integrity applications (TBD from ER or DEL-12.02) | Demonstrates material compliance if required by specification |
| **Section 7: Nonconformance Reports (NCRs)** (if any) | NCRs documenting any issues identified during installation or testing; corrective actions taken; verification of corrective action effectiveness; client acceptance of NCR disposition if significant issues | Documents quality issues and resolutions; demonstrates all issues were resolved before acceptance |
| **Section 8: Witness Signatures** | Third-party or client witness signatures for witnessed hold points: FAT witness (if required), installation inspection witness (if required), proving witness (if required per ER or Measurement Canada), final acceptance witness; witness signatures demonstrate client or regulatory approval of critical activities | Demonstrates witnessed verification per ER requirements or Measurement Canada |
| **Appendices** | Vendor data sheet references (cross-reference to DEL-12.04), specification references (cross-reference to DEL-12.02), calculation references (cross-reference to DEL-12.03 for acceptance criteria), applicable standard excerpts (if referenced in proving procedures or acceptance criteria) | Provides supporting documentation and references |

### Equipment-to-Record Traceability

Each equipment item requires specific records per Specification.md REQ-02, REQ-03:

| Equipment | Tag Number | Required Records | Source |
|-----------|------------|------------------|--------|
| Flow Meter — Rail Unloading | TBD (e.g., FT-1201; from DEL-12.04 and PKG-14 P&IDs) | Calibration certificate (factory), FAT record (if applicable), installation verification, SAT record (if applicable), initial proving record (commissioning), periodic proving records (ongoing operation per proving frequency) | Decomposition:360; Specification.md REQ-01 |
| Flow Meter — Marine Loading | TBD (e.g., FT-1202; from DEL-12.04 and PKG-14 P&IDs) | Calibration certificate, FAT record, installation verification, SAT record, initial proving record, periodic proving records | Decomposition:360; Specification.md REQ-01 |
| Temperature Transmitter(s) — Rail | TBD (e.g., TT-1201, TT-1201A if multiple; from DEL-12.04) | Calibration certificate (factory or field) | Decomposition:360 implied; temperature transmitters are part of metering system |
| Temperature Transmitter(s) — Marine | TBD (e.g., TT-1202; from DEL-12.04) | Calibration certificate | Decomposition:360 implied |
| Pressure Transmitter(s) — Rail (if applicable) | TBD (e.g., PT-1201; from DEL-12.04) | Calibration certificate | Decomposition:360 implied if pressure transmitters are part of system |
| Pressure Transmitter(s) — Marine (if applicable) | TBD (e.g., PT-1202; from DEL-12.04) | Calibration certificate | Decomposition:360 implied |

**Note:** Record requirements for each equipment item depend on equipment type, service criticality, and ER/specification requirements. Flow meters (custody transfer critical) require comprehensive records including calibration and proving. Transmitters (custody transfer compensation) require calibration certificates at minimum.

## References

### Primary Sources

| Reference | Content | Location |
|-----------|---------|----------|
| Decomposition | PKG-12 scope definition, DEL-12.05 definition, objective mapping, facility parameters | Lines 350, 360, 789 |
| ER Vol 2 Part 1 | General requirements, document control, QA requirements, witnessing requirements, records retention | TBD |
| ER Vol 2 Part 2 | Process mechanical requirements, metering testing requirements, accuracy verification requirements, regulatory compliance (Measurement Canada) | TBD |

### Related Deliverables (PKG-12)

| Deliverable | Relationship |
|-------------|--------------|
| DEL-12.01 Metering Design Drawing Set | Drawings define installation arrangement; installation verification records demonstrate installation per drawings (orientation, straight-runs, elevations, connections per drawings) |
| DEL-12.02 Metering Technical Specification | Specification defines acceptance criteria for testing and verification; test records demonstrate compliance with specification requirements (accuracy per spec, calibration traceability per spec, proving per spec, FAT/SAT criteria per spec) |
| DEL-12.03 Metering Design Calculations | Calculations define proving methodology and acceptance criteria; proving records use acceptance criteria from calculations (meter factor limits, proving repeatability, drift limits from DEL-12.03) |
| DEL-12.04 Metering Data Sheet Package | Data sheets provide equipment tags, serial numbers, and parameters for record traceability; records reference data sheet parameters and verify equipment per data sheets (tag numbers, serial numbers, performance specifications) |

### Applicable Standards (TBD — ASSUMPTION)

The following standards may define record requirements for custody transfer metering:

| Standard | Potential Applicability |
|----------|------------------------|
| API MPMS Chapter 4 (Proving Systems) | Proving record requirements: proving run data format, meter factor calculation, acceptance criteria, required documentation | Applicable if API MPMS is governing standard for proving |
| OIML R117 (Dynamic Measuring Systems for Liquids Other Than Water) | Calibration and verification requirements; record format for legal metrology | Likely applicable for vegetable oil custody transfer; may specify required calibration documentation |
| Measurement Canada (Weights and Measures Act and Regulations) | Regulatory record requirements for custody transfer in Canada: calibration traceability, proving records, periodic verification records, approval certificates | Applicable for custody transfer in Canada; meters may require Measurement Canada approval; specific record requirements TBD |
| ISO 9001 (Quality Management Systems) | General QA record requirements: document control, traceability, retention, records management | Applicable to project QA system; general framework for record management |
| Project Quality Management Plan | Project-specific QA/QC procedures: inspection and test plan (ITP), hold points, witness points, record formats, retention | TBD; project quality procedures |

**Note:** Standard applicability and specific record requirements to be confirmed from ER Vol 2 Part 2, DEL-12.02 specification, and project Quality Management Plan.

## Cross-Document Traceability

| Document | Section | Link Points |
|----------|---------|-------------|
| Specification.md | § Scope | Defines inclusions (calibration certificates, accuracy verification records) and exclusions (general instrumentation, control system, piping, electrical) |
| Specification.md | § Requirements | REQ-01 through REQ-19: functional (REQ-01-04 record presence and traceability), performance (REQ-05-09 acceptance criteria and content), traceability (REQ-10-12 equipment and cross-document), documentation (REQ-13-14 control and structure), interface (REQ-15), quality (REQ-16-19 signatures and completeness) |
| Specification.md | § Standards | Governing references (ER Vol 2 Part 1/2, Quality Plan); custody transfer standards (API MPMS Chapter 4, OIML R117, ISO/IEC 17025, Measurement Canada, ISO 9001) |
| Specification.md | § Verification | Verification methods (checklist, traceability, acceptance criteria, certificate completeness, proving completeness, signature/witnessing, legibility, NCR, document control) and acceptance criteria |
| Specification.md | § Documentation | Record package structure matching Construction section (cover sheet, record index, sections 1-8, appendices) |
| Guidance.md | § Purpose | Records as auditable evidence (properly specified, installed, calibrated, verified); downstream use (project closeout, regulatory compliance, commercial confidence, operational reference, audit trail, warranty) |
| Guidance.md | § Principles | Development rationale (evidence of compliance REQ-05, traceability REQ-02/03/06, auditability REQ-17, regulatory support, no fabrication); custody transfer principles (calibration traceability REQ-06, proving documentation REQ-08, witnessing REQ-16) |
| Guidance.md | § Considerations | Content (minimum per Decomposition:360, equipment coverage, acceptance criteria, witnessing); calibration certificate fields (matching REQ-07); proving record fields (matching REQ-08); service-specific (rail batch, marine export); timing (FAT through handover) |
| Guidance.md | § Trade-offs | Proving depth vs. schedule; vendor certificates vs. project templates; witnessing vs. cost; comprehensive vs. minimum records |
| Procedure.md | § Step 1 | Define required record set per REQ-01; review ER/DEL-12.02/Quality Plan for additional requirements; identify equipment from DEL-12.04 |
| Procedure.md | § Step 2 | Establish traceability map (record index) per REQ-04; map equipment to records |
| Procedure.md | § Step 3 | Collect calibration certificates per REQ-01/06/07; verify traceability per REQ-06; cross-reference to DEL-12.04 per REQ-03/10 |
| Procedure.md | § Step 4 | Collect proving records per REQ-01/05/08; verify acceptance per REQ-05; cross-reference to DEL-12.04 per REQ-03/11 |
| Procedure.md | § Step 5 | Verify completeness per REQ-01/17; traceability per REQ-02/03/06; acceptance per REQ-05; signatures per REQ-16; NCRs per REQ-18 |
| Procedure.md | § Step 6 | Compile record package per Documentation section structure; organize per REQ-14 |
| Procedure.md | § Step 7 | Issue with approvals per REQ-16; document control per REQ-13; archive per retention requirements |
| DEL-12.01 | Drawings | Installation verification records demonstrate installation per drawings (orientation, straight-runs, connections per DEL-12.01) |
| DEL-12.02 | Specification | Acceptance criteria for testing (accuracy, FAT/SAT, calibration, proving per DEL-12.02); records demonstrate specification compliance |
| DEL-12.03 | Calculations | Proving methodology and acceptance criteria (meter factor limits, proving repeatability, drift limits per DEL-12.03); records use calculation-derived criteria |
| DEL-12.04 | Data Sheets | Equipment tags, serial numbers, parameters for record traceability; records reference and verify data sheet parameters
