# Specification: DEL-26.04 Coating Installation & Test Records

## Scope

This specification defines requirements for coating installation and test records that provide evidence of coating quality and compliance with DEL-26.01 requirements.

**Source:** Decomposition DEL-26.04

### Inclusions

- Record templates (forms) for coating activities and inspections
- Completed records demonstrating coating compliance
- Record organization and filing per project requirements

## Requirements

**FR-1: Complete Record Coverage**
- Records shall be provided for all coating activities specified in DEL-26.02 Procedures:
  - Surface preparation (all areas coated)
  - Coating application (all coating systems applied)
  - DFT measurement (per inspection frequency in DEL-26.01)
  - Adhesion testing (per inspection frequency in DEL-26.01)
  - Holiday detection (for immersion service coatings)
  - Final acceptance (all areas accepted)
- **Source:** DEL-26.01 (QR-1, QR-2); DEL-26.02 (Documentation sections)

**FR-2: Traceability**
- Records shall provide traceability:
  - Date and time of work
  - Location/area
  - Personnel (applicator, inspector)
  - Materials (coating batch/lot numbers, abrasive type)
  - Environmental conditions
  - Measurements and test results
  - Acceptance (yes/no) with inspector signature
- **Source:** DEL-26.01 (QR-2); **ASSUMPTION** — Quality traceability requirements

**FR-3: Acceptance Criteria Documentation**
- Records shall document acceptance criteria and results:
  - Surface prep: SSPC standard achieved, profile measurement
  - DFT: Minimum DFT per DEL-26.01, readings vs. acceptance criteria
  - Adhesion: Test rating vs. acceptance criteria (typically 4B or 5B)
  - Holiday detection: Holidays detected, repaired, re-inspected
- **Source:** DEL-26.01 (PR-3, PR-4, PR-5, QR-1)

**QR-1: Legibility and Completeness**
- All records shall be legible, complete (all fields filled), and signed by responsible personnel (applicator, inspector)
- **Source:** **ASSUMPTION** — Standard record quality requirements

**QR-2: Archival and Retention**
- Records shall be managed per project record retention requirements
- Records shall be in archival format (paper or electronic per project standards)
- **Source:** **ASSUMPTION** — Project record management requirements

## Standards

- SSPC-PA 2: DFT measurement
- SSPC-VIS 1: Surface preparation visual acceptance
- ASTM D3359: Adhesion testing
- ASTM D4417: Surface profile measurement
- Project Quality Management Plan: Record requirements and retention

**Source:** DEL-26.01 (Standards section)

## Verification

- Verify records provided for all coating activities (complete coverage per FR-1)
- Verify records provide traceability (all required fields complete per FR-2)
- Verify acceptance criteria documented and results recorded (per FR-3)
- Verify records legible, complete, and signed (per QR-1)

## Documentation

**Required outputs:**
- Record templates (forms) for each record type (Datasheet.md — 6 record types)
- Completed records compiled and filed per project record management procedures

**Organization:**
- By coating application (tank internal, tank external, structural steel, marine)
- By record type (surface prep, application, DFT, adhesion, holiday detection, final acceptance)
- **Source:** **ASSUMPTION** — Logical record organization

**Filing location:** Per project record management system — `3_Issued/DEL-26.04_Coating_Installation_and_Test_Records/` or project DMS

**Distribution:**
- QA/QC for review and acceptance
- Commissioning team (PKG-30 for tank internal coating records)
- Project closeout documentation package

**Source:** Decomposition DEL-26.04 anticipated artifacts

---

## Cross-Document Verification Summary

| Specification Requirement | Datasheet § | Guidance § | Procedure § | Upstream DEL-26.01 § |
|---------------------------|-------------|------------|-------------|----------------------|
| FR-1 (Complete Coverage) | All record types | Record Timing | Steps 2–3 | QR-1, QR-2 |
| FR-2 (Traceability) | Record content (each type) | Records as Quality Evidence | Steps 1.2, 2.2 | QR-2 |
| FR-3 (Acceptance Criteria) | Record content (DFT, adhesion, holiday) | — | Step 2.2 | PR-3, PR-4, PR-5, QR-1 |
| QR-1 (Legibility/Completeness) | Attributes | Inspector Independence | Steps 2.2, 3.2 | — |
| QR-2 (Archival/Retention) | Attributes (Retention) | Trade-offs (Paper vs. Electronic) | Step 4 | — |
| Standards | References (Standards) | — | — | Standards |

**Verification status:** Pass 3 complete — All requirements traceable to Datasheet, Guidance, Procedure, and upstream DEL-26.01.
