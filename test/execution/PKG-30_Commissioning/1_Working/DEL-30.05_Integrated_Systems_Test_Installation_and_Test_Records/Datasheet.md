# Datasheet: DEL-30.05 Integrated Systems Test Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-30.05 |
| Name | Integrated Systems Test Installation & Test Records |
| Package | PKG-30 Commissioning |
| Discipline | T&C (Testing & Commissioning) |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |

**Source:** `_CONTEXT.md`; Decomposition §5 PKG-30

## Attributes

| Attribute | Value |
|-----------|-------|
| Record Type | Integrated Systems Test (IST) and End-to-End Test Records |
| Applicable Systems | Full facility end-to-end: railcar unloading → storage → marine loading |
| Record Format | IST test protocols, end-to-end test scenarios, functional verification records |
| Approval Requirements | QA/QC Manager, Commissioning Manager, Operations Manager, Employer witness sign-offs |
| Submittal Timing | Upon IST completion; prerequisite for start-up and performance test (DEL-30.06) |
| Retention Period | **TBD** — Permanent project records |

**Source:** **ASSUMPTION** — IST record attributes; **location TBD**

## Conditions

**Integrated Systems Test Context:**

Provides evidence of completion, inspection, and testing for integrated systems test. IST verifies multiple systems work together as designed in end-to-end scenarios before product introduction.

**IST Scope:**
- **Railcar-to-Tank:** Railcar unloading → product transfer → storage tank (verify full receive path)
- **Tank-to-Ship:** Storage tank → product transfer → metering → marine loading (verify full loading path)
- **Direct Rail-to-Ship:** Railcar unloading → product transfer → metering → marine loading (verify operational flexibility - OBJ-4)
- **Control system integration:** SCADA, interlocks, alarms, emergency shutdown verification
- **Safety systems integration:** Fire protection, high-level protection, emergency response

**Facility:** 32 railcar stations, 3×15,000 MT tanks, product transfer/metering, marine loading arms

**Source:** Decomposition §1.1, §2 OBJ-4 (Operational Flexibility); §5 PKG-30 (Scope: integrated systems commissioning)

## Construction

**Anticipated Artifacts:**

1. **IST Records (Integrated Systems Test):**
   - Test protocol and acceptance criteria
   - End-to-end scenario test records:
     - Railcar unloading to tank scenario
     - Tank to ship loading scenario
     - Direct rail-to-ship scenario (OBJ-4 verification)
   - Control system integration verification
   - Safety interlock integration testing
   - Emergency shutdown system verification
   - Data logging and trending verification
   - Operator interface (HMI) functional testing

2. **End-to-End Test Records:**
   - Complete transfer path verification (source to destination)
   - Metering system integration (custody transfer accuracy - OBJ-10)
   - Product quality verification (sampling points, temperature control)
   - Material balance verification
   - Throughput capacity demonstration (trending toward 1,000,000 MT/annum - OBJ-2)

**Source:** Decomposition §2 OBJ-2, OBJ-4, OBJ-10; §5 DEL-30.05; **ASSUMPTION** — IST scope

## References

- DEL-30.01 Commissioning Procedures — IST procedures
- DEL-30.02 Commissioning Plan — IST schedule and approach
- DEL-30.04 Commissioning Records — Prerequisite individual system commissioning complete
- DEL-30.06 Performance Test Records — Downstream use of IST records
- System design documents (PKG-10 through PKG-24) — End-to-end system design
- IEC 62382 — Commissioning methodology — **location TBD**

**Source:** Decomposition; **ASSUMPTION: likely applicable**

---

## Document Cross-References

- **→ Specification.md:** Requirements for IST scope and end-to-end testing
- **→ Guidance.md:** Rationale for integrated testing approach
- **→ Procedure.md:** Process for executing and documenting IST
