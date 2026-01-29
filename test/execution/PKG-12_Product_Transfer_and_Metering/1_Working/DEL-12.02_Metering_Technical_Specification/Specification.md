# Specification: DEL-12.02 Metering Technical Specification

## Scope

### Deliverable Definition

This document is the specification for the **Metering Technical Specification** deliverable within **PKG-12 Product Transfer & Metering**.

DEL-12.02 defines performance, materials, and workmanship requirements for custody transfer metering per Employer's Requirements (Source: Decomposition:357).

### Package Scope Context

PKG-12 scope covers custody transfer flow meters (rail unloading and marine loading) and metering instrumentation (Source: Decomposition:350).

The facility transfers CSD (Crude Super Degummed) canola oil from rail tank cars to storage tanks (via rail unloading metering) and from storage tanks to liquid bulk carriers for export (via marine loading metering), with a permitted throughput of 1,000,000 MT per annum (Source: Decomposition:41, 43).

### Inclusions

The deliverable shall include, at minimum:

| Artifact | Description | Source |
|----------|-------------|--------|
| Custody Transfer Flow Meter Specification | Performance, materials, installation, and testing requirements for custody transfer flow meters serving rail unloading and marine loading | Decomposition:357 |
| Metering System Specification | System-level requirements including instrumentation (temperature, pressure, density), proving system, control integration, data logging, and QA requirements | Decomposition:357 |

### Exclusions

The following are outside the scope of DEL-12.02:

- Control system architecture (covered in PKG-19 Control Systems)
- Field instrumentation general requirements (covered in PKG-20 Field Instrumentation, except metering-specific instruments which are in this specification)
- Process piping specifications (covered in PKG-14 Process Piping; metering specification defines interface requirements only)
- Electrical power distribution (covered in PKG-17; metering specification defines power requirements as interface)

## Requirements

### Functional Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-01 | The deliverable shall define requirements for custody transfer metering for both rail unloading and marine loading services | Decomposition:350, 357 | Document review per Procedure.md Step 5.1 |
| REQ-02 | The deliverable shall include two specification artifacts: (1) Custody Transfer Flow Meter Specification and (2) Metering System Specification | Decomposition:357 | Checklist review per Procedure.md Step 5.1; Verification section below |
| REQ-03 | The specification shall define metering instrumentation requirements including temperature measurement, pressure measurement, and density measurement (if applicable) for custody transfer flow compensation | Decomposition:350; ASSUMPTION based on custody transfer requirements | Document review; Datasheet.md Instrumentation topic |
| REQ-04 | The specification shall define proving requirements including proving method (in-line prover, portable prover, or master meter), proving frequency, and acceptance criteria for proving | ASSUMPTION based on OBJ-10 custody transfer accuracy | Document review; Datasheet.md Proving Requirements topic |
| REQ-05 | The specification shall define meter technology selection criteria and requirements (e.g., Coriolis, ultrasonic, turbine, positive displacement) appropriate for CSD canola oil service | ASSUMPTION based on deliverable type | Technical review per Procedure.md Step 5.1 |

### Performance Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-06 | The specification shall define accuracy class and uncertainty budget for custody transfer measurement (e.g., accuracy ±0.15%, ±0.25%, or as required by ER) | TBD; ER Vol 2 Part 2, location TBD | Technical review; comparison to custody transfer standards (API MPMS, OIML R117, Measurement Canada) |
| REQ-07 | The specification shall define turndown ratio (flow range) requirements for both rail unloading and marine loading services; minimum measurable flow to maximum measurable flow | TBD; ER Vol 2 Part 2, location TBD | Technical review; verification against DEL-12.03 flow rate calculations |
| REQ-08 | The specification shall define repeatability requirements (e.g., ±0.05%, ±0.1%, or as required by ER) | TBD; ER Vol 2 Part 2, location TBD | Technical review; comparison to custody transfer standards |
| REQ-09 | The specification shall support OBJ-2 (1,000,000 MT/a throughput) by defining flow capacity requirements that do not constrain design throughput; flow ranges for rail unloading and marine loading shall accommodate design flow rates per DEL-12.03 | Decomposition:781 | Design review; cross-check with DEL-12.03 calculations |
| REQ-10 | The specification shall support OBJ-10 (Custody Transfer Accuracy) by defining explicit accuracy class, repeatability, proving criteria, and uncertainty budget appropriate for commercial custody transfer transactions | Decomposition:789 | Design review; verification that specification enables DEL-12.05 accuracy demonstration |

### Material Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-11 | The specification shall define wetted parts materials compatible with CSD canola oil including body material, internal components, seals, and gaskets | ASSUMPTION based on service application | Material compatibility review; vendor data verification |
| REQ-12 | The specification shall define environmental ratings for outdoor installation at Fraser Surrey Terminal (temperature range, humidity, corrosion resistance, seismic requirements) | ASSUMPTION based on installation location | Environmental suitability review; ER Vol 2 Part 1 requirements |

### Installation Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-13 | The specification shall define installation requirements including straight-run lengths upstream and downstream, orientation (horizontal, vertical, inclined), mounting and support requirements, and instrument tap locations | ASSUMPTION based on custody transfer metering requirements | Installation review; consistency with DEL-12.01 drawings |
| REQ-14 | The specification shall reference manufacturer installation requirements and allow for site-specific adaptation as shown in DEL-12.01 drawings | ASSUMPTION | Cross-document check; Procedure.md Step 3.4 |

### Interface Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-15 | The specification shall define metering system interfaces including: (a) piping connections (size, rating, material) to PKG-14, (b) isolation and bypass valve requirements, (c) vents and drains, (d) electrical power requirements to PKG-17, (e) control/communication signals to PKG-19, (f) instrumentation integration to PKG-20, (g) proving connections | ASSUMPTION based on Decomposition:350 | IDC review per Procedure.md Step 6 |
| REQ-16 | Interface coordination with adjacent packages (PKG-14 Process Piping, PKG-17 Electrical, PKG-19 Control Systems, PKG-20 Field Instrumentation) is managed externally per dependency mode NOT_TRACKED | _DEPENDENCIES.md | Coordination meeting; IDC per Procedure.md Step 6 |

### Proving Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-17 | The specification shall define proving method: in-line prover (sphere or piston), portable prover, master meter, or combination; method selection affects space requirements in DEL-12.01 drawings | ASSUMPTION based on REQ-04 | Technical review; coordination with DEL-12.01 proving connection details |
| REQ-18 | The specification shall define proving frequency (e.g., quarterly, semi-annually, annually, after maintenance, or operational schedule-based) | TBD; ER Vol 2 Part 2, location TBD; may be based on Measurement Canada requirements | Operational review; regulatory compliance check |
| REQ-19 | The specification shall define acceptance criteria for proving (e.g., meter factor drift within ±0.05%, or per applicable standard) | TBD; custody transfer standard (API MPMS, OIML R117, Measurement Canada) | Technical review; standard compliance verification |

### Quality Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-20 | The specification shall define QA deliverables including: (a) calibration certificates traceable to national standards (Measurement Canada, NIST, or equivalent), (b) material certificates (MTRs) for wetted components, (c) factory acceptance test (FAT) requirements and acceptance criteria, (d) site acceptance test (SAT) requirements, (e) inspection and test plan (ITP) | ASSUMPTION; ties to DEL-12.05 | Document review; verification that requirements enable DEL-12.05 compliance demonstration |
| REQ-21 | The specification shall define acceptance criteria for each testable requirement to enable DEL-12.05 installation and test records to demonstrate compliance | Decomposition:360 | Testability review per Procedure.md Step 4.2 |
| REQ-22 | All work shall comply with project Quality Management Plan | ASSUMPTION | QA/QC audit |

### Documentation Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-23 | The specification shall define documentation submittals including: (a) data sheets (DEL-12.04), (b) drawings (DEL-12.01), (c) calculations (DEL-12.03), (d) certificates and test records (DEL-12.05), (e) operation and maintenance manuals, (f) as-built documentation | ASSUMPTION based on typical EPC deliverables | Document review; cross-check with related deliverables |
| REQ-24 | The specification shall include a requirements traceability matrix mapping specification clauses to Employer's Requirements sources | ASSUMPTION; epistemic traceability requirement | Traceability matrix review per Procedure.md Step 4.4 |

## Standards

### Governing References

| Standard/Reference | Applicability | Source |
|--------------------|---------------|--------|
| Employer's Requirements Vol 2 Part 1 | General requirements, document control, quality procedures, design life, seismic requirements, environmental conditions | TBD |
| Employer's Requirements Vol 2 Part 2 | Process mechanical requirements, metering technical requirements, accuracy criteria, flow rates, fluid properties (CSD canola oil density, viscosity, temperature), operating pressure and temperature, hazardous area classification | TBD |
| Project Document Control Procedures | Document numbering, revision control, approval requirements | TBD |
| Project Quality Management Plan | QA requirements, inspection and test procedures, hold points, nonconformance handling | TBD |

### Custody Transfer Metering Standards (TBD — ASSUMPTION)

Applicable custody transfer metering standards are TBD pending ER Vol 2 Part 2 clause extraction. The following standards may be applicable:

| Standard | Description | Potential Applicability |
|----------|-------------|------------------------|
| API MPMS (Manual of Petroleum Measurement Standards) | Comprehensive custody transfer measurement standards for petroleum products; multiple chapters covering proving, metering technologies, physical properties, and uncertainty | May be applicable to vegetable oil custody transfer even though primarily petroleum-focused; commonly referenced for custody transfer best practices; specific chapters TBD: Chapter 4 (Proving Systems), Chapter 5 (Metering technologies), Chapter 11 (Physical Properties), Chapter 13 (Statistical Aspects) |
| OIML R117 | International Recommendation for dynamic measuring systems for liquids other than water; covers accuracy classes (0.3, 0.5, 1.0, 1.5, 2.5), installation requirements, testing, and verification | Likely applicable as primary standard for vegetable oil custody transfer metering; provides framework for accuracy, proving, and installation requirements |
| Measurement Canada | Canadian legal metrology requirements for custody transfer measurement; meters used for commercial custody transfer in Canada may require Measurement Canada approval | Applicable for custody transfer in Canada; specific requirements TBD (approval process, periodic verification, sealing requirements) |
| ISO 5024 | Petroleum liquids and gases — Measurement — Standard reference conditions | May be applicable for defining standard reference conditions for volume/mass correction |
| IEC 60079 series | Electrical apparatus for explosive atmospheres (if metering is in hazardous area) | Applicable if hazardous area classification requires explosion-proof or intrinsically safe equipment; governs electrical equipment selection and installation |

**Note:** Standard applicability and specific clause requirements to be confirmed from ER Vol 2 Part 2 and contractual requirements. Specification shall cite applicable standards and identify specific clauses that govern requirements.

## Verification

### Verification Methods

| Method | Description | Applicable Requirements |
|--------|-------------|------------------------|
| Document Review | Review specification for completeness, technical content, and compliance with ER requirements | REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-20, REQ-21, REQ-23 |
| Technical Review | Review specification against ER technical requirements, applicable custody transfer standards, and project objectives | REQ-06, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11, REQ-12, REQ-17, REQ-18, REQ-19 |
| Cross-Document Check | Verify consistency with related deliverables (DEL-12.01 drawings, DEL-12.03 calculations, DEL-12.04 data sheets) | REQ-09, REQ-13, REQ-14, REQ-23 |
| IDC Review | Interdisciplinary check with impacted packages (PKG-14, PKG-17, PKG-19, PKG-20) to verify interface definitions | REQ-15, REQ-16 |
| Checklist Review | Verify presence of all decomposition-listed artifacts (custody transfer flow meter specification, metering system specification) | REQ-02 |
| Traceability Matrix Review | Verify all specification clauses are traceable to ER sources or labeled TBD/ASSUMPTION | REQ-24 |
| Testability Review | Verify each requirement has defined verification method to enable DEL-12.05 compliance demonstration | REQ-21 |
| QA/QC Audit | Verify compliance with project Quality Management Plan | REQ-22 |

### Acceptance Criteria

| Criterion | Description | Source |
|-----------|-------------|--------|
| Artifact Completeness | Both specification artifacts present: (1) Custody Transfer Flow Meter Specification, (2) Metering System Specification | Decomposition:357; REQ-02 |
| Service Coverage | Specification covers both rail unloading and marine loading metering services with service-specific requirements (flow ranges, operational considerations) | REQ-01 |
| Requirements Traceability | All specification clauses traceable to ER sources or labeled TBD/ASSUMPTION; traceability matrix complete per REQ-24 | Epistemic rule; Procedure.md Step 4.4 |
| Testability | Each requirement has defined verification method (review, inspection, test, certificate) enabling DEL-12.05 compliance demonstration | REQ-21 |
| Interface Coverage | All metering system interfaces defined (piping, electrical, controls, instrumentation, proving) | REQ-15 |
| Standard Compliance | Applicable custody transfer standards identified and specification requirements aligned with standard requirements | REQ-06, REQ-07, REQ-08, REQ-18, REQ-19 |
| Performance Alignment | Specification performance requirements support OBJ-2 (throughput) and OBJ-10 (accuracy) | REQ-09, REQ-10 |
| Cross-Document Consistency | Specification requirements consistent with DEL-12.01 drawings, DEL-12.03 calculations, and DEL-12.04 data sheets | REQ-09, REQ-13, REQ-14, REQ-23 |

## Documentation

### Required Documentation Outputs

| Output | Description | Source |
|--------|-------------|--------|
| Custody Transfer Flow Meter Specification | Technical specification document defining performance, materials, installation, and testing requirements for custody transfer flow meters | Decomposition:357; REQ-02 |
| Metering System Specification | System-level specification document defining instrumentation, proving, control integration, data logging, and QA requirements | Decomposition:357; REQ-02 |
| Requirements Traceability Matrix | Matrix mapping specification clauses to Employer's Requirements source clauses | REQ-24; Procedure.md Step 4.4 |

### Specification Structure (ASSUMPTION)

The specification document(s) should include the following sections to satisfy requirements:

| Section | Content | Requirements Addressed |
|---------|---------|----------------------|
| 1. Scope and Service Description | Rail unloading and marine loading metering scope; CSD canola oil product; custody transfer application; system boundaries (included/excluded) | REQ-01, REQ-02 |
| 2. Definitions and Abbreviations | Custody transfer terminology (accuracy, repeatability, proving, meter factor, uncertainty, turndown); abbreviations (FAT, SAT, MTR, ITP, etc.) | General specification content |
| 3. Reference Documents and Standards | ER references, applicable custody transfer standards (API MPMS, OIML R117, Measurement Canada), codes and regulations | Standards section above |
| 4. Technical Requirements | Performance (accuracy REQ-06, repeatability REQ-08, uncertainty, turndown REQ-07), flow range and sizing (REQ-09), meter technology (REQ-05), materials (REQ-11), environmental ratings (REQ-12), hazardous area classification | REQ-05 through REQ-12 |
| 5. Design and Installation | Meter selection and sizing basis (reference DEL-12.03), installation requirements (straight-run REQ-13, orientation, mounting, supports), instrument tap locations (REQ-03), piping arrangement (bypass, isolation, proving connections REQ-15) | REQ-03, REQ-09, REQ-13, REQ-14, REQ-15 |
| 6. Proving Requirements | Proving method and equipment (REQ-17), proving frequency (REQ-18), acceptance criteria (REQ-19), prover calibration and traceability | REQ-04, REQ-17, REQ-18, REQ-19 |
| 7. Electrical and Controls | Power supply, signal outputs and protocols, integration with control system (PKG-19), data logging and totalizing, alarm and interlock functions | REQ-15 (electrical interface) |
| 8. Inspection, Testing, and Acceptance | FAT procedures and criteria, SAT procedures and criteria, calibration procedures, proving procedures, installation inspection, acceptance criteria (REQ-21) | REQ-20, REQ-21 |
| 9. Documentation and Submittals | Data sheets (DEL-12.04), drawings (DEL-12.01), calculations (DEL-12.03), certificates and test records (DEL-12.05), operation and maintenance manuals | REQ-23 |
| 10. Quality Assurance | Quality plan and ITP, hold points and witness points, nonconformance handling, material traceability | REQ-20, REQ-22 |
| 11. Appendices | Requirements traceability matrix (REQ-24), flow diagrams, proving schematics, data sheet templates |REQ-24 |

### Documentation Requirements

| Requirement | Description | Source |
|-------------|-------------|--------|
| Requirements Traceability | Map specification clauses to ER references; label TBD for items pending ER review; label ASSUMPTION for inferred requirements | REQ-24; epistemic rule |
| Cross-Reference | Reference DEL-12.01 drawings for installation details, DEL-12.03 calculations for sizing verification, DEL-12.04 data sheets for equipment parameters, DEL-12.05 for compliance records | REQ-14, REQ-23 |
| Revision Control | Per project document control procedures; revision history, approval signatures | TBD; ER Vol 2 Part 1 |
| Standard Citations | Cite specific clauses of applicable standards (API MPMS Chapter/Section, OIML R117 clause, Measurement Canada regulation) | Standards section |

## Cross-Document Traceability

| Document | Section | Traceability Points |
|----------|---------|---------------------|
| Datasheet.md | § Identification | Deliverable ID (DEL-12.02), name, package (PKG-12), discipline (Process), type (Specification), responsible party (D&B Contractor) |
| Datasheet.md | § Attributes | Specification attributes (document number, specification type, revision, classification, format, estimated length) |
| Datasheet.md | § Conditions | Design context (service application, product CSD canola oil, throughput 1M MT/a, metering points, operating conditions, objective alignment OBJ-2/OBJ-10/OBJ-6) |
| Datasheet.md | § Construction | Key specification topics: performance (REQ-05 through REQ-10), flow range (REQ-07/REQ-09), materials (REQ-11/REQ-12), installation (REQ-13/REQ-14), proving (REQ-04/REQ-17-19), instrumentation (REQ-03), electrical/controls (REQ-15), QA (REQ-20-22); anticipated specification structure (11 sections) |
| Guidance.md | § Purpose | Specification drives DEL-12.01 drawings, DEL-12.03 calculations, DEL-12.04 data sheets, procurement, DEL-12.05 QA records; downstream use (engineering basis, procurement basis, installation basis, testing basis, compliance basis, operational basis) |
| Guidance.md | § Principles | Contract alignment (REQ-24 traceability), objective support (REQ-09/REQ-10 for OBJ-2/OBJ-10), testability (REQ-21), traceability (TBD/ASSUMPTION labeling), technology neutrality (REQ-05 meter technology selection); custody transfer principles (accuracy/uncertainty REQ-06, repeatability REQ-08, proving REQ-04/17-19, compensation REQ-03) |
| Guidance.md | § Considerations | Technology selection (Coriolis, ultrasonic, turbine, positive displacement per REQ-05; product properties per REQ-11; flow range per REQ-07/09; proving method per REQ-17); service-specific (rail 32 stations, marine high flow per REQ-01); specification content (performance, materials, installation, proving, QA per § Requirements); interfaces (PKG-14/17/19/20 per REQ-15/16); canola oil properties |
| Guidance.md | § Trade-offs | Accuracy vs. cost (REQ-06), accuracy vs. pressure drop (REQ-09), standardization vs. optimization (REQ-05), robustness vs. sensitivity (REQ-12), proving frequency vs. operational impact (REQ-18), in-line vs. portable prover (REQ-17) |
| Guidance.md | § Conflict Table | Local conflicts pending resolution (accuracy vs. cost, proving frequency, meter technology, space constraints) |
| Procedure.md | § Step 1 | Gather basis: ER Vol 2 Part 2 (REQ-06/07/08/18/19), standards (API MPMS, OIML R117, Measurement Canada), design basis (flow rates per REQ-09), objectives (OBJ-2/OBJ-10 per REQ-09/10) |
| Procedure.md | § Step 2 | Define scope: both services (REQ-01), system boundaries, artifacts (REQ-02) |
| Procedure.md | § Step 3 | Draft requirements: 3.1 performance (REQ-05-10), 3.2 materials (REQ-11-12), 3.3 installation (REQ-13-14), 3.4 proving (REQ-04/17-19), 3.5 instrumentation (REQ-03), 3.6 electrical/controls (REQ-15), 3.7 QA (REQ-20-22), 3.8 documentation (REQ-23-24) |
| Procedure.md | § Step 4 | Verification hooks: verification methods (REQ-21), acceptance criteria, traceability matrix (REQ-24) |
| Procedure.md | § Step 5 | Discipline check: completeness (REQ-02), consistency, testability (REQ-21), objective alignment (REQ-09/10), standard compliance, traceability (REQ-24) |
| Procedure.md | § Step 6 | IDC: PKG-14 piping, PKG-17 electrical, PKG-19 controls, PKG-20 instrumentation per REQ-15/16 |
| Procedure.md | § Step 7 | Issue: document control, approvals, issue package, status update |
| Procedure.md | § Records | Outputs: custody transfer flow meter specification, metering system specification (REQ-02), traceability matrix (REQ-24), check records (REQ-22)
