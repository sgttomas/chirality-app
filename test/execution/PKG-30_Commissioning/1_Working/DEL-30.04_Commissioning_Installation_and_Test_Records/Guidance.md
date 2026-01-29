# Guidance: DEL-30.04 Commissioning Installation & Test Records

## Purpose

Supports development of **Commissioning Installation & Test Records** for PKG-30 Commissioning.

**Context:** Provides evidence of completion, inspection, and testing for commissioning. Individual system commissioning by discipline (mechanical, electrical, I&C) verifies systems operate per design before integrated testing.

**Source:** Decomposition §5 PKG-30, DEL-30.04

## Principles

**P-1: Systematic Commissioning by Discipline**

Individual system commissioning follows a discipline-based approach:
- **Mechanical first:** Verify equipment operates mechanically (rotation, alignment, no binding)
- **Electrical second:** Verify power distribution and motor operation electrically sound
- **I&C third:** Verify control systems, instrumentation, interlocks, and automation

This sequence builds confidence systematically and enables troubleshooting at each layer before adding complexity.

**Source:** **ASSUMPTION** — Industry standard commissioning sequence; IEC 62382

**P-2: Design Verification Through Testing**

Commissioning records provide objective evidence that:
- Equipment installed per design drawings
- Systems operate within design parameters
- Safety systems function as intended (interlocks, alarms, trips)
- Performance meets design intent

This systematic verification supports operational readiness (OBJ-1) and regulatory compliance (OBJ-6).

**Source:** Decomposition §2 OBJ-1, OBJ-6

**P-3: Custody Transfer Metering Criticality**

Metering system commissioning is critical for commercial operations:
- Custody transfer accuracy directly affects revenue and contractual compliance (OBJ-10)
- Metering commissioning includes calibration, proving, flow computer verification
- Regulatory compliance required for custody transfer certification

Metering commissioning records receive heightened scrutiny and quality requirements.

**Source:** Decomposition §2 OBJ-10 (Custody Transfer Accuracy)

## Considerations

**C-1: System Complexity and Interdependencies**

Facility systems are interdependent:
- Pumps require electrical power and I&C control
- Control systems require field instruments and electrical signals
- Safety interlocks span multiple systems

Commissioning sequence must respect interdependencies. Ensure prerequisites complete before commissioning dependent systems.

**Source:** **ASSUMPTION** — System interdependency considerations

**C-2: Safety Interlock Verification**

Safety interlocks are critical for OBJ-1 (Safe & Reliable Operation):
- Emergency shutdown systems
- High-level alarms and trips
- Low-pressure protection
- Fire protection interlocks

Verify interlocks function correctly through systematic testing. Document trip testing and fail-safe verification.

**Source:** Decomposition §2 OBJ-1; **ASSUMPTION** — Safety system criticality

**C-3: Loop Checking Methodology (IEC 62382)**

I&C commissioning follows IEC 62382 loop checking methodology:
- Loop checks verify end-to-end signal path (field instrument → wiring → I/O → controller → HMI)
- Systematic approach reduces commissioning errors
- Loop check sheets provide standardized record format

Use IEC 62382 methodology for structured, repeatable I&C commissioning.

**Source:** IEC 62382; **ASSUMPTION: likely applicable**

## Trade-offs

**T-1: Commissioning Rigor vs. Schedule**

**Trade-off:** Comprehensive commissioning provides high confidence but takes time; expedited commissioning enables faster start-up but increases operational risk.

**Recommendation:** Do not compromise commissioning quality for safety-critical and revenue-critical systems (fire protection, safety interlocks, custody transfer metering). Risk-based approach for less critical systems.

**Source:** **ASSUMPTION**

**T-2: Witness Points vs. Efficiency**

**Trade-off:** Extensive witness points provide oversight but extend schedule; minimal witness points improve efficiency but reduce oversight.

**Recommendation:** Mandatory witness points for safety-critical commissioning (safety interlock testing, fire protection) and high-value commissioning (custody transfer metering proving). Streamlined for routine systems.

**Source:** **ASSUMPTION**

## Examples

**Anticipated Artifacts:**
- Mechanical commissioning records: Pump performance curves, valve stroke test data, vibration baseline data
- Electrical commissioning records: Motor megger test results, transformer insulation resistance, relay settings
- I&C commissioning records: Loop check sheets (IEC 62382 format), calibration certificates, functional test records, alarm verification

**Source:** Decomposition §5 DEL-30.04; Datasheet.md

## Conflict Table (for human ruling)

No conflicts identified during document enrichment. If conflicts arise during commissioning records compilation, they will be documented here:

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| (none) | | | | | | |

**Note:** Cross-deliverable conflicts are handled by RECONCILIATION agent when requested; this table captures only local conflicts within DEL-30.04 scope.

---

## Document Cross-References

- **← Datasheet.md / Specification.md:** Rationale for commissioning requirements by discipline
- **→ Procedure.md:** Considerations inform commissioning execution and record generation
