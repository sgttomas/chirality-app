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

### Procedure Scope

This procedure covers:
- Identification of required records
- Collection and verification of records
- Compilation and issue of record package

## Prerequisites

### Dependencies

| Prerequisite | Status | Notes |
|--------------|--------|-------|
| Dependency Mode | NOT_TRACKED | Dependencies coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`) |

### Recommended Upstream Inputs (ASSUMPTION)

| Input | Source | Purpose |
|-------|--------|---------|
| Metering Technical Specification | DEL-12.02 | Acceptance criteria for verification |
| Metering Design Calculations | DEL-12.03 | Proving methodology and acceptance criteria basis |
| Metering Data Sheet Package | DEL-12.04 | Equipment tags, serials, parameters for traceability |
| Vendor Calibration Certificates | Procurement / Vendor | Factory calibration data |
| Proving Results | Commissioning | Accuracy verification data |

### Reference Materials

| Reference | Location | Purpose |
|-----------|----------|---------|
| `_REFERENCES.md` | Deliverable folder | Applicable reference documents |
| `0_References/` | Package directory | Reference materials |
| Employer's Requirements | ER Vol 2 Part 1, Part 2 | QA, records, testing requirements (TBD) |
| Decomposition | Line 350, 360 | Scope and artifact definitions |
| Specification.md | Deliverable folder | Requirements to be satisfied |
| Guidance.md | Deliverable folder | Record development considerations |

### Personnel Requirements

| Role | Qualification | Source |
|------|---------------|--------|
| QA/QC Lead | Qualified QA/QC personnel | ASSUMPTION; project quality procedures |
| Checker | Independent reviewer | ASSUMPTION; project quality procedures |
| Approver | Authorized per project procedures | TBD; ER Vol 2 Part 1 |
| Witness | Third-party or client representative (if required) | TBD; ER Vol 2 Part 1 |

## Steps

### Step 1: Define Required Record Set

| Action | Description |
|--------|-------------|
| 1.1 | Confirm minimum required records: calibration certificates and accuracy verification records (Decomposition:360) |
| 1.2 | Identify all metering equipment requiring records (flow meters, temperature transmitters, pressure transmitters) |
| 1.3 | Confirm witnessing requirements from ER and specification (TBD) |
| 1.4 | Document required record set in record index template |

**Output:** Required record list

### Step 2: Establish Traceability Map

| Action | Description |
|--------|-------------|
| 2.1 | Obtain equipment list from DEL-12.04 data sheets (tags, serials, services) |
| 2.2 | Create record index mapping each equipment item to required records |
| 2.3 | Include columns for: tag, serial, service, record type, record date, witness (if required) |
| 2.4 | Assign record tracking numbers as needed |

**Output:** Record index / traceability map

### Step 3: Collect Calibration Certificates

| Action | Description |
|--------|-------------|
| 3.1 | Obtain vendor calibration certificates from procurement |
| 3.2 | Verify certificates include: equipment identification, calibration date, traceability statement, results, uncertainty |
| 3.3 | Verify certificates cover equipment serial numbers in DEL-12.04 |
| 3.4 | Obtain field calibration records if site calibration performed |
| 3.5 | Flag any missing or incomplete certificates |

**Output:** Collected calibration certificates

### Step 4: Collect Accuracy Verification / Proving Records

| Action | Description |
|--------|-------------|
| 4.1 | Obtain proving records from commissioning (if proving performed) |
| 4.2 | Verify records include: proving method, conditions, run data, meter factor, acceptance criteria, acceptance statement |
| 4.3 | Verify records are signed by authorized personnel |
| 4.4 | Verify third-party/client witness signatures if required |
| 4.5 | Flag any missing or incomplete records |

**Output:** Collected accuracy verification records

### Step 5: Verify Completeness and Validity

| Action | Description |
|--------|-------------|
| 5.1 | Review all records against required record list |
| 5.2 | Verify equipment tag/serial traceability for all records |
| 5.3 | Verify calibration traceability statements are complete |
| 5.4 | Verify accuracy verification results meet acceptance criteria (per DEL-12.02) |
| 5.5 | Verify required signatures and witnessing are complete |
| 5.6 | Verify records are legible and in approved format |
| 5.7 | Document any nonconformances and corrective actions |

**Output:** Verified record set; nonconformance records (if any)

### Step 6: Compile Record Package

| Action | Description |
|--------|-------------|
| 6.1 | Prepare cover sheet (project ID, deliverable ID, revision, issue date) |
| 6.2 | Finalize record index with all record references |
| 6.3 | Organize records by equipment or record type per project convention |
| 6.4 | Include nonconformance/corrective action records if applicable |
| 6.5 | Apply document control numbering and revision |

**Output:** Compiled record package

### Step 7: Issue for Review and Acceptance

| Action | Description |
|--------|-------------|
| 7.1 | Independent review of record package for completeness |
| 7.2 | Obtain QA/QC lead and checker signatures |
| 7.3 | Obtain approvals per project procedures (TBD) |
| 7.4 | Issue per project document control process |
| 7.5 | Archive in approved format and location |

**Output:** Issued record package; issue record

## Verification

### Verification Activities

| Activity | Requirement Verified | Method | Record |
|----------|---------------------|--------|--------|
| Record completeness check | REQ-01 | Checklist against Decomposition:360 | Record index |
| Traceability check | REQ-02, REQ-03 | Cross-reference to DEL-12.04 | Record index |
| Accuracy compliance check | REQ-04, REQ-06 | Technical review | Verification records |
| Calibration traceability check | REQ-05 | Certificate review | Calibration certificates |
| Signature check | REQ-09 | Signature review | Check record |
| Format compliance check | REQ-10 | Document control review | Check record |

### Acceptance Criteria

| Criterion | Verification | Source |
|-----------|--------------|--------|
| All required records present | Record index complete | Specification.md REQ-01 |
| Equipment traceability complete | Cross-reference verified | Specification.md REQ-02, REQ-03 |
| Accuracy criteria met | Verification results reviewed | Specification.md REQ-04 |
| Calibration traceable | Certificates verified | Specification.md REQ-05 |
| Signatures complete | Signature review | Specification.md REQ-09 |
| Archive compliant | Format and filing verified | Specification.md REQ-10 |

### Sign-off Requirements

| Role | Responsibility | Source |
|------|----------------|--------|
| QA/QC Lead | Record compilation, completeness verification | ASSUMPTION |
| Checker | Independent review | ASSUMPTION |
| Approver | Authorization for issue | TBD; ER Vol 2 Part 1 |

## Records

### Documentation Outputs

| Output | Description | Source |
|--------|-------------|--------|
| Calibration Certificates | Factory/field calibration certificates | Decomposition:360 |
| Accuracy Verification Records | Proving / accuracy verification records | Decomposition:360 |
| Record Index | Index mapping records to equipment | Step 2 |
| Check Records | Review and verification records | Step 7 |

### Record Management

| Attribute | Value |
|-----------|-------|
| Filing Location (Review) | `2_Checking/` |
| Filing Location (Issued) | `3_Issued/` |
| Document Management | Per project document control procedures |
| Retention | TBD; per project quality procedures and regulatory requirements |
| Format | ASSUMPTION: Electronic records in project document management system |

### Status Transitions

| From State | To State | Trigger |
|------------|----------|---------|
| INITIALIZED | IN_PROGRESS | Record collection commences |
| IN_PROGRESS | CHECKING | Record package submitted for review |
| CHECKING | ISSUED | Approved for issue |

**Note:** Status transitions are managed per `_STATUS.md` and project lifecycle procedures.
