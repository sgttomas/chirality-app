# Datasheet: DEL-30.04 Commissioning Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-30.04 |
| Name | Commissioning Installation & Test Records |
| Package | PKG-30 Commissioning |
| Discipline | T&C (Testing & Commissioning) |
| Type | Record |
| Responsible | D&B Contractor (Commissioning Team) |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |

**Source:** `_CONTEXT.md`; Decomposition §5 PKG-30

## Attributes

| Attribute | Value |
|-----------|-------|
| Record Type | System Commissioning Test and Verification Records |
| Applicable Systems | All facility systems by discipline: Mechanical, Electrical, I&C |
| Record Format | Commissioning datasheets, test records, loop check sheets, functional test records |
| Approval Requirements | Commissioning engineer, discipline lead, QC inspector, operations sign-offs |
| Submittal Timing | Upon individual system commissioning completion; prerequisite for integrated systems test (DEL-30.05) |
| Retention Period | **TBD** — Permanent project records |

**Source:** **ASSUMPTION** — Record attributes; **location TBD**

## Conditions

**Commissioning Phase Context:**

Provides evidence of completion, inspection, and testing for commissioning. Individual system commissioning verifies each discipline (mechanical, electrical, I&C) operates per design before integrated systems testing.

**Facility Context:**
- 32 railcar unloading stations with pumps, valves, instrumentation
- 3×15,000 MT storage tanks with level instrumentation and temperature monitoring
- Product transfer piping with metering systems (custody transfer accuracy critical)
- Marine loading arms with control systems
- Electrical power distribution, motor control centers, lighting
- SCADA/PLC control systems, field instrumentation, safety interlocks, alarms
- Fire protection and security systems

**Source:** Decomposition §1.1 (Key Parameters), §5 PKG-30 (Scope: system commissioning)

## Construction

**Anticipated Artifacts:**

1. **Mechanical Commissioning Records:**
   - Pump commissioning: Alignment checks, rotation verification, vibration baseline, performance curves, seal integrity
   - Valve commissioning: Stroke tests, seat leak tests, actuator settings, fail-safe verification
   - Tank commissioning: Level instrumentation calibration, temperature sensors, mixing systems (if applicable)
   - Piping system commissioning: Pressure boundary verification, support inspections, expansion verification
   - Equipment run-in records: Initial operation data, break-in procedures

2. **Electrical Commissioning Records:**
   - Power distribution commissioning: Energization records, protective relay settings, coordination studies verification
   - Motor commissioning: Megger tests, rotation verification, no-load/load test data, thermal overload settings
   - Transformer commissioning: Insulation resistance, turns ratio, power-on verification
   - Lighting commissioning: Circuit energization, illumination level verification, emergency lighting tests
   - Grounding and bonding verification

3. **I&C Commissioning Records:**
   - Instrument calibration records: Field instruments (pressure, temperature, level, flow transmitters)
   - Loop check sheets: IEC 62382 loop checking for all control loops
   - Control system commissioning: SCADA/PLC functional tests, HMI verification, data logging verification
   - Safety interlock verification: Logic testing, trip testing, fail-safe verification
   - Alarm verification: Alarm setpoints, annunciation testing, alarm response verification
   - Metering system commissioning: Custody transfer meter commissioning (critical for accuracy - OBJ-10)

**Source:** Decomposition §5 DEL-30.04; **ASSUMPTION** — Expanded commissioning record types by discipline

## References

- DEL-30.01 Commissioning Procedures — Commissioning execution procedures
- DEL-30.02 Commissioning Plan — Commissioning schedule and approach
- DEL-30.03 Pre-commissioning Records — Prerequisite for commissioning
- DEL-30.05 Integrated Systems Test Records — Downstream use of commissioning records
- System design documents (PKG-10 through PKG-24) — Design basis and acceptance criteria
- IEC 62382 — I&C loop checking methodology — **location TBD**
- CSA Z662 — Pipeline commissioning — **location TBD**
- NFPA 70 (NEC) — Electrical commissioning — **ASSUMPTION: likely applicable** — **location TBD**

**Source:** Decomposition §4, §5; **ASSUMPTION: likely applicable** standards

---

## Document Cross-References

- **→ Specification.md:** Requirements for commissioning record content by discipline
- **→ Guidance.md:** Rationale for systematic commissioning by discipline
- **→ Procedure.md:** Process for generating and submitting commissioning records
