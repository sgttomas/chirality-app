# Specification: DEL-32.05 Transport Canada Compliance Installation & Test Records

## Scope

Defines requirements for **Transport Canada Compliance Installation & Test Records** within **PKG-32**.

**Purpose:** Provides evidence of Transport Canada compliance. (Source: _CONTEXT.md; Decomposition Section 5)
**Coverage:** Compliance with Transport Canada approval conditions (rail and marine safety)
**Artifacts:** TC compliance documentation (Source: Decomposition Section 5)
**Objective:** OBJ-6: Regulatory Compliance

## Requirements

### Functional Requirements

**FR-01: Transport Canada Approval and Condition Identification** — Transport Canada approvals obtained (DEL-32.02); conditions extracted | **Verification:** Procedure Step 1

**FR-02: Compliance Tracking System** — Tracking system for Transport Canada conditions established | **Verification:** Procedure Step 2

**FR-03: Compliance Evidence Collection** — Evidence collected per condition requirements (rail inspections, marine safety compliance, notifications) | **Verification:** Procedure Steps 3, 4

**FR-04: Transport Canada Submittals** — Submittals to Transport Canada per approval conditions | **Verification:** Procedure Step 4

**FR-05: Compliance Register Maintenance** — Register maintained and updated | **Verification:** Procedure Step 5

**FR-06: Compliance Record Compilation** — Records compiled and filed for Transport Canada inspections | **Verification:** Procedure Step 6

### Performance Requirements

**PR-01: Compliance Completeness** — 100% of Transport Canada conditions demonstrated compliant | **Acceptance:** All conditions satisfied
**PR-02: Timeliness** — Per Transport Canada condition schedules (notification deadlines, inspection schedules) | **Acceptance:** **TBD**

### Interface Requirements

**IR-01: DEL-32.02 (Permits)** — Transport Canada approvals (DEL-32.02) contain conditions requiring demonstration (DEL-32.05) | **Coordination:** Extract and assign conditions
**IR-02: DEL-32.07, DEL-32.08** — Transport Canada submittals logged and filed | **Coordination:** Log all Transport Canada interactions
**IR-03: Construction Packages (PKG-10, 11)** — Rail and marine works generate compliance evidence | **Coordination:** **TBD**

### Quality Requirements

**QR-01: Record Quality** — Records accurate, complete, legible | **Verification:** QA/QC review
**QR-02: Record Retention** — Filed per document control; accessible for Transport Canada inspections | **Verification:** Document control procedures

## Standards

**Regulatory:** Transport Canada approvals and conditions — **TBD**; Transport Canada rail safety regulations — **TBD**; Transport Canada marine safety regulations — **TBD**
**Project:** Employer's Requirements — **location TBD**
**Quality:** ISO 9001:2015 — **ASSUMPTION**; Project QMP — **TBD**

## Verification

| Activity | Method | Responsible | Acceptance | Procedure Ref |
|----------|--------|-------------|------------|---------------|
| Conditions extracted | Extract from Transport Canada approvals | QA/QC Manager | All conditions identified | Step 1 |
| Tracking established | Create compliance register | QA/QC Manager | All conditions tracked | Step 2 |
| Evidence collected | Rail/marine inspections, notifications | QA/QC team | Evidence per conditions | Steps 3, 4 |
| Register updated | Update as activities complete | QA/QC Manager | Register current | Step 5 |
| Records filed | File per document control | QA/QC Manager | Records accessible | Step 6 |

## Documentation

**Outputs:** TC compliance documentation
**Format:** **TBD** — Per Transport Canada conditions (inspection reports, certifications, notification records)
**Retention:** **TBD** — Per Transport Canada and contract requirements
