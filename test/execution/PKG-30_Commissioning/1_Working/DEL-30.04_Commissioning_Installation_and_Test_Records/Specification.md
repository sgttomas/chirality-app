# Specification: DEL-30.04 Commissioning Installation & Test Records

## Scope

Defines requirements for **Commissioning Installation & Test Records** for the Canola Oil Transload Facility — Phase 1.

**Purpose:** Provides evidence of completion, inspection, and testing for commissioning.

**Artifacts:** Mechanical commissioning records, electrical commissioning records, I&C commissioning records

**Source:** Decomposition §5 PKG-30, DEL-30.04

## Requirements

### Functional Requirements

**FR-1: Mechanical Commissioning Records**
- Records shall document all mechanical system commissioning per DEL-30.01 procedures
- Coverage: Pumps (alignment, vibration, performance), valves (stroke tests, seat leaks), tanks, piping, equipment
- **Source:** DEL-30.01; **ASSUMPTION** — Mechanical commissioning scope

**FR-2: Electrical Commissioning Records**
- Records shall document all electrical system commissioning per DEL-30.01 procedures
- Coverage: Power distribution, motors (megger, rotation, load tests), transformers, lighting, grounding
- **Source:** DEL-30.01; **ASSUMPTION** — Electrical commissioning scope

**FR-3: I&C Commissioning Records**
- Records shall document all I&C system commissioning per DEL-30.01 procedures
- Coverage: Instrument calibration, loop checks (IEC 62382), control system functional tests, safety interlocks, alarms, metering systems
- Critical: Custody transfer metering commissioning (OBJ-10: Custody Transfer Accuracy)
- **Source:** DEL-30.01; Decomposition §2 OBJ-10; IEC 62382

**FR-4: Commissioning Prerequisites Verification**
- Records shall verify pre-commissioning complete (DEL-30.03) before system commissioning
- Records shall verify as-built drawings and O&M manuals available
- **Source:** DEL-30.02 Commissioning Plan; DEL-30.03

**FR-5: Acceptance Criteria Documentation**
- Records shall document acceptance criteria from design documents and procedures
- Records shall document test results and verification that criteria met
- Non-conformances shall be documented with resolution tracking
- **Source:** **ASSUMPTION** — Acceptance governance

### Performance Requirements

**PR-1: Operational Readiness Verification**
- Commissioning records shall demonstrate systems ready for integrated systems test (DEL-30.05)
- Systems shall operate within design parameters and meet project objectives (OBJ-1: Safe & Reliable Operation)
- **Source:** Decomposition §2 OBJ-1; DEL-30.05

**PR-2: Record Quality and Traceability**
- Records shall be legible, complete, accurate, and traceable
- Records shall provide objective evidence of commissioning completion
- **Source:** **ASSUMPTION** — Quality record standards

### Interface Requirements

**IR-1: Pre-commissioning Interface**
- Commissioning records shall reference pre-commissioning records (DEL-30.03) as prerequisites
- **Source:** DEL-30.03

**IR-2: Integrated Systems Test Interface**
- Commissioning records are prerequisite for integrated systems test (DEL-30.05)
- **Source:** DEL-30.02 Commissioning Plan; DEL-30.05

**IR-3: Procedures Interface**
- Records shall reference specific commissioning procedures from DEL-30.01
- **Source:** DEL-30.01

### Quality Requirements

**QR-1: Approval and Sign-off**
- Records require commissioning engineer, discipline lead, QC inspector sign-offs
- Operations sign-off for critical systems — **TBD**
- **Source:** **ASSUMPTION** — QA governance

**QR-2: Non-Conformance Management**
- Non-conformances shall be documented, tracked, and resolved
- NCRs shall be closed before system acceptance
- **Source:** **ASSUMPTION** — NCR process

**QR-3: Archival and Retention**
- Records archived per project document control
- Retention: **TBD** — Permanent project records
- **Source:** **ASSUMPTION**

## Standards

- IEC 62382 — I&C loop checking — **location TBD**
- CSA Z662 — Pipeline commissioning — **location TBD**
- NFPA 70 (NEC) — Electrical installation and testing — **ASSUMPTION: likely applicable** — **location TBD**
- IEEE standards — Motor testing, transformer testing — **ASSUMPTION: likely applicable** — **location TBD**
- Employer's Requirements — **TBD: location**

**Source:** **ASSUMPTION: likely applicable**

## Verification

- Completeness check against commissioning procedures
- Data accuracy and acceptance criteria verification
- Witness signature verification
- Non-conformance closure verification

**Acceptance:** All commissioning activities documented, acceptance criteria met, NCRs closed, sign-offs obtained

## Documentation

**Outputs:** Mechanical commissioning records, electrical commissioning records, I&C commissioning records for all facility systems

**Format:** Commissioning datasheets, loop check sheets, test reports — **TBD**

**Submittal:** Upon system commissioning completion; stored in `3_Issued/DEL-30.04/` by system

**Source:** Decomposition §5 DEL-30.04

---

## Document Cross-References

- **← Datasheet.md:** Requirements for record types identified in Datasheet
- **→ Guidance.md:** Rationale for systematic commissioning approach
- **→ Procedure.md:** Process for generating commissioning records
