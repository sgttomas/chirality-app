# Specification: DEL-17.04 Electrical Power Data Sheet Package

## Scope

This specification defines the requirements for **Electrical Power Data Sheet Package** within **PKG-17 Electrical Power Distribution**.

**Purpose** (Source: Decomposition DEL-17.04 entry): Defines and substantiates electrical power in accordance with ER requirements.

**Anticipated deliverable artifacts** (Source: _CONTEXT.md): Transformer data sheets, MCC data sheets, switchgear data sheets, UPS data sheet

## Requirements

### Functional Requirements

**FR-1: Equipment Data Sheet Completeness**
- Data sheets shall include: Nameplate ratings, construction details, performance data, accessories, test results, compliance certifications
- **Source**: Equipment procurement and verification requirements
- **Rationale**: Complete data sheets enable specification compliance verification and support installation/commissioning. See Guidance.md — Principle 1 (Data Sheet as Compliance Verification Tool).
- **Procedure**: See Procedure.md — Step 3 (Data Sheet Technical Review).

**FR-2: Specification Compliance Verification**
- Data sheets shall demonstrate equipment compliance with DEL-17.02 (Technical Specification) requirements
- Deviations from specifications shall be identified and flagged for review/approval
- **Source**: Quality assurance and procurement requirements
- **Rationale**: See Guidance.md — Consideration 1 (Data Sheet Review Focus).
- **Procedure**: See Procedure.md — Step 3 (Data Sheet Technical Review), Step 4 (Approval or Rejection).

**FR-3: Calculation Verification**
- Equipment ratings on data sheets shall match or exceed ratings in DEL-17.03 (Design Calculations)
- Transformer kVA, switchgear/MCC bus ratings, circuit breaker interrupting capacity shall be verified
- **Source**: Design verification requirements
- **Rationale**: See Guidance.md — Principle 1 (Data Sheet as Compliance Verification Tool).
- **Procedure**: See Procedure.md — Step 3 (Data Sheet Technical Review).

### Performance Requirements

**PR-1: Data Sheet Format and Organization**
- Data sheets shall follow manufacturer standard format supplemented with project-specific data requirements
- Equipment shall be identified by project tag number (per DEL-17.01 equipment list)
- **Format**: PDF format for distribution; native manufacturer format for record

**PR-2: Test Report Inclusion**
- Factory acceptance test (FAT) reports shall be included with data sheets
- Test results shall demonstrate compliance with applicable standards (CSA, IEEE, UL)
- **Source**: Quality assurance requirements

### Quality Requirements

**QR-1: Data Sheet Review and Approval**
- All data sheets shall undergo technical review (verify compliance with specifications and calculations)
- Approved data sheets required before equipment shipment
- **Source**: Procurement quality procedures

**QR-2: As-Installed Data Sheet Updates**
- Data sheets shall be updated post-installation to reflect actual installed conditions (relay settings as-left, serial numbers, installation date)
- **Source**: Commissioning and record documentation requirements

## Standards

**Primary Standards**: CSA C88, C802, C22.2 No. 31, C22.2 No. 254; IEEE C57 series, IEEE C37 series

## Verification

**Verification Methods**: Technical review (spec compliance check), calculation cross-check, test report review

## Documentation

**Required Outputs**: Transformer data sheets, switchgear data sheets, MCC data sheets (including bucket schedules), UPS data sheet

**Cross-References**:
- **Datasheet.md**: Equipment types and data sheet content requirements
- **Guidance.md**: Data sheet review criteria and compliance verification approach
- **Procedure.md**: Data sheet submittal, review, and approval process
- **DEL-17.02**: Specifications that data sheets must demonstrate compliance with
- **DEL-17.03**: Calculations that data sheets must verify
