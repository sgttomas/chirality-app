# Guidance: DEL-20.05 Instrumentation Installation & Test Records

## Purpose

Supports development of **Instrumentation Installation & Test Records** for **PKG-20 Field Instrumentation**.

**Deliverable Objective:** Provides evidence of completion, inspection, and testing for instrumentation.

**Source:** Decomposition document, DEL-20.05 (line 500)

**Cross-Document Context:** Test records verify compliance with all previous PKG-20 deliverables (DEL-20.01 drawings, DEL-20.02 specifications, DEL-20.03 calculations, DEL-20.04 data sheets). See Procedure.md for commissioning test workflow.

## Principles

**Principle 1: Test Records Provide Acceptance Evidence**

Test records demonstrate that: instruments are correctly installed (per drawings), meet specifications (performance verified), and are functional (loops operational). Records are legal evidence of compliance for regulatory and contractual acceptance.

**Principle 2: Quality Gates Before Operations**

No instrument or system placed in service until test records complete and approved. This ensures safety and reliability before facility operations begin (supports OBJ-1).

**Principle 3: Calibration Baseline for Lifecycle**

Field commissioning calibration establishes baseline for future recalibration intervals. Calibration drift over time measured against commissioning baseline (supports OBJ-9: Lifecycle Cost Optimization).

**Source:** **ASSUMPTION** based on typical commissioning philosophy; Decomposition OBJ-1 (line 780), OBJ-9 (line 788)

## Considerations

**Project-Specific:**

- Large instrument population (100+ loops) requires efficient test procedures and record management
- Marine environment and hazardous areas require rigorous installation inspection (corrosion protection, electrical code compliance)
- Storage tank overfill protection critical for safety (API 2350 verification required)
- Custody transfer metering (PKG-12 coordination) requires high-accuracy calibration and certification

**Technical:**

**Calibration Methods:**
- **Wet calibration:** Use actual process conditions (e.g., fill tank to known levels, verify transmitter reading)
- **Dry calibration:** Use simulation (electronic simulators, pressure calibrators, RTD simulators)
- **Wet calibration preferred** for accuracy verification; **dry calibration acceptable** for routine checks

**Loop Check Strategy:**
- **Individual loop checks:** Each loop tested independently (sensor, wiring, control system input)
- **Integrated system tests:** Multiple loops tested together (control strategies, interlocks, sequences)
- **Performance tests:** System-level verification (throughput, accuracy, safety systems)

**Source:** **ASSUMPTION** based on typical commissioning test methods

## Trade-offs

**Trade-off: Dry Calibration vs. Wet Calibration**

| Aspect | Dry Calibration (Simulation) | Wet Calibration (Process Conditions) |
|--------|------------------------------|---------------------------------------|
| Accuracy verification | Simulates sensor input (does not verify full measurement chain) | Verifies full measurement chain (sensor, installation, process effects) |
| Schedule | Faster (can be done before process available) | Slower (requires process fluid, operating conditions) |
| Cost | Lower (uses portable calibrators) | Higher (requires process startup, may require product) |
| Typical use | Routine checks, pre-commissioning | Critical measurements (custody transfer, tank gauging, safety) |

**Recommendation:** Dry calibration for most instruments during pre-commissioning; wet calibration for critical measurements (tank gauging, custody transfer, overfill protection) during commissioning with product.

**Source:** **ASSUMPTION** based on typical commissioning practices; balance schedule/cost vs. accuracy verification

## Examples

**Example: Level Transmitter Loop Check**

```
Tag: LT-001 (Storage Tank #1 Level)
P&ID: P-001
Test Date: [Date]

1. Dry Calibration (Pre-commissioning):
   - Simulate 0%, 50%, 100% level (electronic simulator)
   - Verify control room reading (0 m, 7.5 m, 15 m)
   - Verify high alarm (13 m setpoint) ✓
   - Verify high-high alarm (14 m setpoint) ✓

2. Wet Calibration (Commissioning with product):
   - Fill tank to known levels (measured by tape)
   - Verify transmitter reading vs. tape measurement
   - Accuracy: ±5 mm ✓ (meets ±3 mm specification)

3. Loop Check Sign-offs:
   - Instrument Technician: [Name/Date]
   - Control Systems Tech: [Name/Date]
   - Commissioning Engineer: [Name/Date]
```

**Source:** **ASSUMPTION** — Example loop check record format

**Project Objective Alignment:**

Supports **OBJ-1: Safe & Reliable Operation** — Test records provide evidence that instrumentation is fit for safe operations before facility startup.

**Source:** Decomposition Section 6 (line 780)

## Cross-Document Traceability

This Guidance document provides engineering rationale for DEL-20.05. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Datasheet.md | Factual identification, attributes, conditions, references | Conditions § defines record lifecycle; Construction § defines record content |
| Specification.md | Requirements and verification criteria | FR-1 to FR-5 implement Principles; QR-1 to QR-3 implement quality approach |
| Procedure.md | Production workflow and verification steps | Steps 1-6 implement Principles 1-3 through commissioning lifecycle |

**Guidance-to-Specification Mapping:**

| Guidance Section | Specification Section | Rationale Provided |
|------------------|----------------------|-------------------|
| Principle 1 | FR-1 to FR-5 | Test records provide acceptance evidence |
| Principle 2 | PR-2 | Quality gates before operations |
| Principle 3 | INT-2 | Calibration baseline for lifecycle maintenance |
| Trade-off | FR-2 | Dry vs. wet calibration methods |
| Technical Considerations | FR-2, FR-3 | Calibration methods and loop check strategy |
