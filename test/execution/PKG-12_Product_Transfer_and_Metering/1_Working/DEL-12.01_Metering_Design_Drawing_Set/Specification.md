# Specification: DEL-12.01 Metering Design Drawing Set

## Scope

### Deliverable Definition

This specification defines the requirements for the **Metering Design Drawing Set** within **PKG-12 Product Transfer & Metering**.

DEL-12.01 defines the design arrangement and details for custody transfer metering per Employer's Requirements (Source: Decomposition:356).

### Package Scope Context

PKG-12 scope covers custody transfer flow meters (rail unloading and marine loading) and metering instrumentation (Source: Decomposition:350).

The facility transfers CSD (Crude Super Degummed) canola oil from rail tank cars to storage tanks and from storage tanks to liquid bulk carriers for export, with a permitted throughput of 1,000,000 MT per annum (Source: Decomposition:41, 43).

### Inclusions

The drawing set shall include, at minimum:

| Artifact | Description | Source |
|----------|-------------|--------|
| Metering Skid GAs | General arrangement drawings for custody transfer metering skid(s) at rail unloading and marine loading locations | Decomposition:356 |
| Flow Meter Installation Details | Installation details for custody transfer flow meters including orientation, straight-run requirements, flow conditioning, and instrument taps | Decomposition:356 |
| Proving Connection Details | Details for meter proving connections including prover tie-in points, isolation, drainage, and access provisions | Decomposition:356 |

### Exclusions

The following are outside the scope of DEL-12.01:

- Control system architecture drawings (covered in PKG-19)
- Electrical power distribution drawings (covered in PKG-17)
- P&IDs (covered in PKG-14; metering drawings show local detail and reference P&IDs for process context)
- Civil/structural foundation drawings (covered in PKG-05, PKG-06)
- Piping isometrics for process piping beyond meter runs (covered in PKG-14)

## Requirements

### Functional Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-01 | The drawing set shall depict metering arrangements for custody transfer service at both rail unloading and marine loading locations | Decomposition:350, 356 | Drawing review against scope |
| REQ-02 | The drawing set shall include all decomposition-listed artifacts: metering skid GAs, flow meter installation details, and proving connection details | Decomposition:356 | Checklist review per Procedure.md Step 4.1 |
| REQ-03 | Drawings shall show sufficient detail for construction, installation, and commissioning of custody transfer metering systems including dimensions, elevations, tag numbers, and interface points | ASSUMPTION based on deliverable type | Discipline review per Procedure.md Step 5 |
| REQ-04 | Tag numbers on drawings shall be consistent with metering specification (DEL-12.02), data sheets (DEL-12.04), and P&IDs (PKG-14) | ASSUMPTION; cross-document consistency requirement | Cross-document check per Procedure.md Step 4.3 |

### Performance Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-05 | Drawings shall support development of metering capable of meeting OBJ-2 (1,000,000 MT/a throughput) without introducing flow constraints; meter sizing and piping geometry shall be per DEL-12.03 calculations | Decomposition:781 | Design review per Procedure.md Step 5.2 |
| REQ-06 | Drawings shall support OBJ-10 (Custody Transfer Accuracy) by clearly depicting: (a) meter run geometry and orientation, (b) straight-run requirements upstream and downstream, (c) flow conditioning devices if any, (d) instrument tap locations, (e) proving connections | Decomposition:789 | Design review; accuracy verification per Guidance.md principles |
| REQ-07 | Straight-run dimensions shown on drawings shall comply with meter manufacturer requirements and DEL-12.03 calculations | ASSUMPTION; manufacturer and calculation alignment | Calculation cross-check per Procedure.md Step 4.3 |
| REQ-08 | Drawing legibility, CAD standards, line weights, text heights, and revision control shall comply with project document control requirements | TBD; ER Vol 2 Part 1, location TBD | Document control check per Procedure.md Step 4.5 |

### Interface Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-09 | Drawings shall identify all interface points including: (a) piping tie-ins to PKG-14, (b) instrument connections to PKG-20, (c) electrical power connections to PKG-17, (d) control/communications to PKG-19, (e) structural supports to PKG-06, (f) access/maintenance provisions, (g) proving connections | ASSUMPTION based on Decomposition:350 and typical metering system interfaces | IDC review per Procedure.md Step 6 |
| REQ-10 | Interface coordination with adjacent packages (PKG-06, PKG-14, PKG-17, PKG-19, PKG-20) is managed externally per dependency mode NOT_TRACKED | _DEPENDENCIES.md | Coordination meeting per Procedure.md Step 6 |
| REQ-11 | Proving connection details shall accommodate the proving method specified in DEL-12.02 (in-line prover, portable prover, or master meter; TBD) | DEL-12.02 (TBD) | Specification cross-check |

### Quality Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-12 | Drawing set shall be subject to originator self-check, independent check (IC), and interdisciplinary check (IDC) prior to issue | ASSUMPTION; ER Vol 2 Part 1, location TBD | Check records per Procedure.md Steps 4-6 |
| REQ-13 | Tag numbering, line numbering, and document metadata shall comply with project document control procedures | TBD; ER Vol 2 Part 1, location TBD | Document control review per Procedure.md Step 4.5 |
| REQ-14 | All work shall comply with project Quality Management Plan | ASSUMPTION | QA/QC audit |
| REQ-15 | Drawings shall include title block with project information, drawing title, drawing number, revision, date, originator, checker, and approver signatures per project standards | TBD; ER Vol 2 Part 1, location TBD | Document control check per Procedure.md Step 7.1 |

### Content Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-16 | Metering skid GA drawings shall show: plan and elevation views, meter run arrangements, piping, instruments, structural supports, access provisions, dimensions, and tag numbers | Datasheet.md Construction section | Drawing completeness review |
| REQ-17 | Flow meter installation detail drawings shall show: meter orientation, straight-run dimensions upstream and downstream, flow conditioning devices (if any), instrument tap positions (temperature, pressure, density if applicable), and mounting details | Datasheet.md Construction section | Drawing completeness review |
| REQ-18 | Proving connection detail drawings shall show: prover connection points, isolation valves, drainage provisions, and access for proving equipment connection | Datasheet.md Construction section | Drawing completeness review |

## Standards

### Governing References

| Standard/Reference | Applicability | Source |
|--------------------|---------------|--------|
| Employer's Requirements Vol 2 Part 1 | General requirements, drawing standards, document control, CAD standards, quality procedures | TBD |
| Employer's Requirements Vol 2 Part 2 | Process mechanical requirements, metering technical requirements, operating conditions, fluid properties | TBD |
| Project Document Control Procedures | Drawing numbering, revision control, title block format, signature requirements, issue procedures | TBD |
| Project CAD Standards | CAD conventions, layering, symbology, line weights, text styles, dimensioning | TBD |
| Project Quality Management Plan | Check procedures (self-check, IC, IDC), approval authorities, record requirements | TBD |

### Custody Transfer Metering Standards (ASSUMPTION)

Applicable custody transfer metering standards are TBD pending ER clause extraction. The following standards may be applicable to vegetable oil custody transfer:

- **API MPMS (Manual of Petroleum Measurement Standards)** — if applicable to vegetable oil custody transfer (commonly used for liquid hydrocarbons; applicability to vegetable oils TBD)
- **OIML R117** — Dynamic measuring systems for liquids other than water (international legal metrology standard)
- **Measurement Canada requirements** — Canadian custody transfer regulations and approval requirements
- **ISO 9001** — Quality management systems (general QMS requirements)
- **Manufacturer installation requirements** — Meter-specific installation standards per vendor documentation (TBD; varies by selected meter technology)

**Note:** Standard applicability and specific clause requirements to be confirmed from ER Vol 2 Part 2 and project basis documents. Drawing content shall comply with applicable custody transfer standards as specified in DEL-12.02.

## Verification

### Verification Methods

| Method | Description | Applicable Requirements |
|--------|-------------|------------------------|
| Drawing Review | Discipline lead reviews drawings for technical content, accuracy, and completeness | REQ-01, REQ-03, REQ-05, REQ-06, REQ-07, REQ-16, REQ-17, REQ-18 |
| Checklist Review | Verify presence of all decomposition-listed artifacts and required drawing content | REQ-02 |
| Document Control Check | Verify compliance with project document control procedures (numbering, revision, title block, signatures) | REQ-08, REQ-13, REQ-15 |
| Cross-Document Check | Verify consistency with DEL-12.02, DEL-12.03, DEL-12.04, and PKG-14 P&IDs | REQ-04, REQ-07, REQ-11 |
| IDC Review | Interdisciplinary check with impacted packages (PKG-06, PKG-14, PKG-17, PKG-19, PKG-20) | REQ-09, REQ-10 |
| Check Records Review | Verify self-check, IC, and IDC completion and comment resolution | REQ-12 |
| QA/QC Audit | Verify compliance with Quality Management Plan | REQ-14 |

### Acceptance Criteria

| Criterion | Description | Source |
|-----------|-------------|--------|
| Artifact Completeness | All three artifact types (metering skid GAs, flow meter installation details, proving connection details) present and covering both rail unloading and marine loading services | Decomposition:356; REQ-02 |
| Technical Accuracy | Meter arrangements, dimensions, and details consistent with DEL-12.02 specification, DEL-12.03 calculations, and DEL-12.04 data sheets | REQ-04, REQ-07 |
| Interface Coverage | All custody transfer metering interfaces identified and coordinated with interfacing packages | REQ-09 |
| Check Completion | Self-check, IC, IDC records complete with all comments resolved | REQ-12 |
| Document Control Compliance | Drawing numbering, title blocks, revision control, and signatures comply with project procedures | REQ-08, REQ-13, REQ-15 |
| Custody Transfer Intent | Drawing clarity supports accurate custody transfer measurement per OBJ-10 | REQ-06; Guidance.md principles |

## Documentation

### Required Documentation Outputs

| Output | Description | Source |
|--------|-------------|--------|
| Metering Skid GAs | General arrangement drawing(s) for rail unloading and marine loading metering skids | Decomposition:356; REQ-16 |
| Flow Meter Installation Details | Installation detail drawing(s) for custody transfer flow meters | Decomposition:356; REQ-17 |
| Proving Connection Details | Proving connection detail drawing(s) | Decomposition:356; REQ-18 |
| Drawing List / Sheet Index | Index identifying all drawing sheets with drawing numbers, titles, and revisions | ASSUMPTION; Procedure.md Step 1.3 |

### Documentation Requirements

| Requirement | Description | Source |
|-------------|-------------|--------|
| Title Block | Standard project title block with revision history, originator, checker, approver signatures | TBD; ER Vol 2 Part 1; REQ-15 |
| Tag/Line Numbering | Tag numbers consistent with metering specification (DEL-12.02), data sheets (DEL-12.04), and P&IDs (PKG-14) | REQ-04 |
| Equipment Identification | Tag numbers match P&IDs and instrument index | REQ-04 |
| Revision Control | Per project document control procedures; revision history in title block | REQ-08, REQ-13 |
| Notes and References | General notes, material callouts, and references to specifications and data sheets | ASSUMPTION |

## Cross-Document Traceability

| Document | Section | Traceability Points |
|----------|---------|---------------------|
| Datasheet.md | § Identification | Deliverable ID (DEL-12.01), name, package (PKG-12), discipline (Process), type (Drawing), responsible party (D&B Contractor) |
| Datasheet.md | § Attributes | Drawing attributes (number series, sheet size, scale, CAD standard, revision, classification, drawing count) |
| Datasheet.md | § Conditions | Design context (service application, product, throughput, metering points, design conditions, objective alignment) |
| Datasheet.md | § Construction | Anticipated drawing content (metering skid GAs, flow meter installation details, proving connection details), expected features and callouts |
| Guidance.md | § Purpose | Deliverable intent (geometric definition for custody transfer), downstream use (fabrication, installation, commissioning, operations, regulatory) |
| Guidance.md | § Principles | Custody-transfer measurement intent (meter run geometry clarity, instrument tap locations, proving connection accessibility, installation precision); drawing content principles (completeness, constructability, maintainability, interface clarity, measurement precision); objective alignment (OBJ-2 throughput, OBJ-10 accuracy, OBJ-6 regulatory) |
| Guidance.md | § Considerations | Design factors affecting drawing content: meter technology, straight-run requirements, flow conditioning, proving method, environmental conditions, hazardous area classification, seismic design, product characteristics; service-specific considerations (rail unloading, marine loading); interface considerations (PKG-06, PKG-14, PKG-17, PKG-19, PKG-20) |
| Guidance.md | § Trade-offs | Competing factors: accuracy vs. pressure drop, accessibility vs. footprint, standardization vs. optimization, integrated vs. modular skid, in-line vs. portable proving |
| Procedure.md | § Step 1 | Confirm scope and drawing list (1.1-1.7) — establishes artifact checklist and drawing numbers |
| Procedure.md | § Step 2 | Collect inputs (2.1-2.8) — gathers DEL-12.02, DEL-12.03, DEL-12.04, PKG-14 P&IDs, vendor data, drafting standards, layout drawings |
| Procedure.md | § Step 3 | Draft drawings (3.1-3.4) — produces metering skid GAs, flow meter installation details, proving connection details, standard drawing elements |
| Procedure.md | § Step 4 | Self-check (4.1-4.9) — verifies REQ-01 through REQ-18, cross-document consistency, interface coverage, document control compliance |
| Procedure.md | § Step 5 | Independent check (5.1-5.9) — technical correctness, constructability, maintainability, objective compliance |
| Procedure.md | § Step 6 | Interdisciplinary check (6.1-6.6) — interface coordination with PKG-06, PKG-14, PKG-17, PKG-19, PKG-20 |
| Procedure.md | § Step 7 | Issue (7.1-7.6) — document control metadata, approvals, issue package, status update |
| Procedure.md | § Records | Drawing outputs (Metering Skid GAs, Flow Meter Installation Details, Proving Connection Details, Drawing List), check records (self-check, IC, IDC, issue)
