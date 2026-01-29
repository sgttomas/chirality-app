# Specification: DEL-32.06 Code Compliance Installation & Test Records

## Scope

Defines requirements for **Code Compliance Installation & Test Records** within **PKG-32**.

**Purpose:** Provides evidence of code compliance. (Source: _CONTEXT.md; Decomposition Section 5)
**Coverage:** Compliance with building, fire, electrical, plumbing, gas code permit conditions
**Artifacts:** Code compliance certificates, inspection records (Source: Decomposition Section 5)
**Objective:** OBJ-6: Regulatory Compliance

## Requirements

### Functional Requirements

**FR-01: Building/Fire/Code Permit and Condition Identification** — Building/fire/code permits obtained (DEL-32.02); conditions extracted | **Verification:** Procedure Step 1

**FR-02: Compliance Tracking System** — Tracking system for code permit conditions established | **Verification:** Procedure Step 2

**FR-03: Compliance Evidence Collection** — Evidence collected per condition requirements (building inspections, fire system tests, electrical inspections, code compliance measures) | **Verification:** Procedure Steps 3, 4

**FR-04: Authority Inspection Coordination** — Authority inspections coordinated per permit conditions | **Verification:** Procedure Step 4

**FR-05: Occupancy Permit and Final Certification** — Occupancy permits and final certifications obtained | **Verification:** Procedure Step 5

**FR-06: Compliance Register Maintenance** — Register maintained and updated | **Verification:** Procedure Step 6

**FR-07: Compliance Record Compilation** — Records compiled and filed for authority inspections | **Verification:** Procedure Step 7

### Performance Requirements

**PR-01: Compliance Completeness** — 100% of code permit conditions demonstrated compliant | **Acceptance:** All conditions satisfied; occupancy permit obtained
**PR-02: Timeliness** — Per code permit condition schedules (inspection schedules, occupancy deadlines) | **Acceptance:** **TBD**

### Interface Requirements

**IR-01: DEL-32.02 (Permits)** — Building/fire/code permits (DEL-32.02) contain conditions requiring demonstration (DEL-32.06) | **Coordination:** Extract and assign conditions
**IR-02: DEL-32.07, DEL-32.08** — Authority inspection records logged and filed | **Coordination:** Log all authority inspections
**IR-03: Construction Packages (all)** — Construction generates compliance evidence; building packages (PKG-22-26) especially relevant | **Coordination:** **TBD**

### Quality Requirements

**QR-01: Record Quality** — Records accurate, complete, legible | **Verification:** QA/QC review
**QR-02: Record Retention** — Filed per document control; accessible for authority inspections | **Verification:** Document control procedures

## Standards

**Regulatory Codes:**
- BC Building Code / National Building Code — **TBD**
- BC Fire Code / NFPA standards — **TBD**
- Canadian Electrical Code — **TBD**
- Plumbing codes — **TBD**
- Gas codes (if applicable) — **TBD**
- Local amendments — **TBD**

**Project:** Employer's Requirements — **location TBD**
**Quality:** ISO 9001:2015 — **ASSUMPTION**; Project QMP — **TBD**

## Verification

| Activity | Method | Responsible | Acceptance | Procedure Ref |
|----------|--------|-------------|------------|---------------|
| Conditions extracted | Extract from building/fire/code permits | QA/QC Manager | All conditions identified | Step 1 |
| Tracking established | Create compliance register | QA/QC Manager | All conditions tracked | Step 2 |
| Evidence collected | Building inspections, fire tests, electrical inspections | QA/QC team | Evidence per conditions | Steps 3, 4 |
| Authority inspections coordinated | Coordinate inspections with authorities | QA/QC Manager / construction | Inspections passed | Step 4 |
| Occupancy permit obtained | Occupancy permit issued | QA/QC Manager | Occupancy permit received | Step 5 |
| Register updated | Update as activities complete | QA/QC Manager | Register current | Step 6 |
| Records filed | File per document control | QA/QC Manager | Records accessible | Step 7 |

## Documentation

**Outputs:** Code compliance certificates, inspection records
**Format:** **TBD** — Authority inspection forms, test certificates, as-built drawings, occupancy permit
**Retention:** **TBD** — Per authority and contract requirements
