# Procedure: DEL-30.04 Commissioning Installation & Test Records

## Purpose

Defines the process for generating, reviewing, and submitting **Commissioning Installation & Test Records** for the Canola Oil Transload Facility.

**Context:** Provides evidence of completion, inspection, and testing for commissioning.

**Source:** Decomposition §5 PKG-30, DEL-30.04

## Prerequisites

**Dependencies:** NOT_TRACKED mode — See `_DEPENDENCIES.md`

**Upstream Requirements:**
- DEL-30.01 Commissioning Procedures — Commissioning execution procedures
- DEL-30.02 Commissioning Plan — Commissioning schedule
- DEL-30.03 Pre-commissioning Records — Prerequisite complete
- System design documents (PKG-10 through PKG-24) — Design basis and acceptance criteria
- As-built drawings and O&M manuals (PKG-31)

**Personnel:** Commissioning technicians (mechanical, electrical, I&C), commissioning engineer, discipline leads, QC inspector, operations representative

**Tools:**
- Commissioning record forms by discipline — **TBD**
- Test equipment (vibration analyzer, megger, multimeter, calibrators, etc.)
- Loop check equipment per IEC 62382
- Camera for documentation photos

**Source:** DEL-30.01, DEL-30.02, DEL-30.03; **ASSUMPTION**

## Steps

**Step 1: Verify Prerequisites Complete**
- Verify pre-commissioning records complete for system (DEL-30.03)
- Verify as-built drawings available
- Verify O&M manuals and vendor documentation available
- Verify system ready for commissioning per DEL-30.02 schedule

**Step 2: Prepare for Commissioning**
- Obtain approved commissioning procedure (DEL-30.01)
- Obtain blank commissioning record forms (mechanical, electrical, or I&C as applicable)
- Review system design parameters and acceptance criteria
- Conduct pre-commissioning briefing with commissioning team
- Assemble test equipment and tools

**Step 3: Execute Commissioning per Discipline**

**For Mechanical Systems:**
- Execute mechanical commissioning per DEL-30.01 procedure
- Record: Pump performance (flow, head, vibration), valve stroke tests, equipment run-in data
- Verify acceptance criteria met
- Take photos of critical equipment during commissioning

**For Electrical Systems:**
- Execute electrical commissioning per DEL-30.01 procedure
- Record: Megger test results, motor rotation/load tests, relay settings, energization data
- Verify acceptance criteria met
- Document protective device settings

**For I&C Systems:**
- Execute I&C commissioning per DEL-30.01 procedure and IEC 62382 methodology
- Record: Loop check sheets, calibration data, functional test results, interlock verification, alarm verification
- For custody transfer metering: comprehensive commissioning and proving records
- Verify acceptance criteria met

**Step 4: Document Non-Conformances**
- If acceptance criteria not met: document non-conformance (NCR)
- NCR includes: description, impact assessment, resolution plan, responsible party, target date
- Track NCR through resolution and closure
- Re-test after NCR closure and document acceptance

**Step 5: Obtain Sign-offs**
- Commissioning engineer reviews record and signs
- Discipline lead (mechanical, electrical, or I&C) reviews and signs
- QC inspector verifies and signs
- Operations representative signs for critical systems — **TBD**

**Step 6: Submit Record**
- Submit completed commissioning record to document control
- File in `3_Issued/DEL-30.04/` organized by system and discipline
- Update commissioning completion tracking per DEL-30.02
- Notify integrated systems test team (DEL-30.05) of system readiness

**Source:** **ASSUMPTION** — Standard commissioning record generation process

## Verification

- Completeness check: All required fields and tests completed
- Data accuracy: Test data recorded correctly
- Acceptance verification: Criteria met and documented
- NCR closure: All non-conformances resolved
- Sign-offs: Required signatures obtained

**Source:** Specification.md §Verification

## Records

**Outputs:**
- Mechanical commissioning records (by system)
- Electrical commissioning records (by system)
- I&C commissioning records (by system)
- Non-conformance reports (NCRs) and resolutions

**Management:**
- Filed in `3_Issued/DEL-30.04/` by system and discipline
- Retention: **TBD** — Permanent project records

**Source:** Decomposition §5 DEL-30.04; Specification.md

---

## Document Cross-References

- **← Datasheet / Specification / Guidance:** Procedure implements commissioning requirements and principles
- DEL-30.01 provides commissioning procedures to execute
- DEL-30.03 provides prerequisite pre-commissioning records
- DEL-30.05 uses commissioning records as prerequisite for integrated systems test
