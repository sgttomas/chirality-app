# Guidance: DEL-20.03 Instrumentation Design Calculations

## Purpose

This guidance supports development of **Instrumentation Design Calculations** for **PKG-20 Field Instrumentation** on the Canola Oil Transload Facility Phase 1 project.

**Deliverable Objective:** Provides the engineering basis and sizing/verification calculations for instrumentation.

**Source:** Decomposition document, DEL-20.03 (line 498)

**Cross-Document Context:**

This Guidance provides engineering rationale for Specification.md requirements. Calculations verify DEL-20.02 specifications and support DEL-20.04 data sheets. See Procedure.md for calculation development workflow.

## Principles

**Principle 1: Calculations Provide Design Verification**

Calculations verify that specified instruments (DEL-20.02) are suitable for their applications by demonstrating:
- Ranges accommodate operating conditions with adequate margin
- Accuracy meets measurement requirements (control, safety, custody transfer)
- Physical sizing is appropriate (thermowells, flow elements, mounting)

**Principle 2: Fit-for-Purpose Accuracy**

Accuracy requirements vary by application:
- **Custody transfer:** ±0.15% typical (commercial accountability)
- **Process control:** ±0.5-1% typical (adequate for stable control)
- **Safety alarms:** ±1-2% acceptable (with adequate setpoint margin)
- **Monitoring:** ±2-5% acceptable (indication only)

Total loop uncertainty (TLU) analysis verifies specified instruments meet application requirements.

**Principle 3: Design Margin**

Instrument sizing includes appropriate margins:
- **Range selection:** Operating point at 30-70% of span for optimal accuracy
- **Overpressure:** Minimum 2× range or piping MAWP
- **Accuracy budget:** Include calibration drift over time (50-100% of initial accuracy for 2-year calibration interval)

**Source:** **ASSUMPTION** based on ISA 84, API 554, typical engineering practice

## Considerations

**Project-Specific:**

- **Canola oil properties:** Viscosity (temperature-dependent), density (≈0.92 kg/L), low vapor pressure
- **Marine environment:** Outdoor instruments in coastal BC climate (-30°C to +50°C ambient)
- **Storage tanks:** 3 × 15,000 MT (large tanks require accurate level measurement for inventory)
- **Custody transfer:** Accurate metering required (coordinate with PKG-12)

**Source:** Decomposition Key Parameters (lines 38-44)

**Technical Considerations:**

**Level Calculations:**
- Tank geometry (level-to-volume conversion for inventory accuracy)
- Transmitter range (0-100% coverage with margin)
- Overfill protection setpoints per API 2350

**Pressure Calculations:**
- Range selection (normal/design/maximum pressures from piping design)
- Overpressure rating (≥2× range or MAWP)
- Orifice plate sizing per API 14.3 (if used for flow)

**Temperature Calculations:**
- Element type (RTD for accuracy, thermocouple for cost/response)
- Thermowell stress analysis per ASME PTC 19.3 (high-velocity applications)
- Response time (thermal mass and heat transfer)

**Source:** **ASSUMPTION** based on typical instrumentation calculations

## Trade-offs

**Trade-off 1: Calculation Detail vs. Engineering Efficiency**

- **Detailed calculations:** Every instrument individually sized (high effort, optimal accuracy)
- **Representative calculations:** Typical calculations with scaling for similar instruments (lower effort, adequate for most applications)

**Recommendation:** Representative approach for standard instruments; detailed calculations for critical/unusual applications (custody transfer, safety, large thermowells).

**Trade-off 2: Software Tools**

- **Spreadsheet (Excel):** Simple, transparent, easy to review — suitable for most calculations
- **Specialty software:** More capable (orifice sizing, thermowell FEA) — requires validation and training

**Recommendation:** Excel for tabular calculations; specialty software for complex applications where industry-standard tools exist.

**Source:** **ASSUMPTION** based on typical EPC calculation practices

## Examples

**Example: Level Transmitter Range Calculation**

```
Tank: 15,000 MT capacity, diameter 20 m, height 15 m (approximate)
Normal operating range: 20% - 90% full
Design range: 0% - 100% full

Transmitter range selection: 0 to 15 m (covers full tank height)
Normal operating range: 3 m to 13.5 m (20% to 90% of 15 m span)
Operating point: 3-13.5 m = 20-90% of transmitter span ✓ (within 30-70% optimal range)

Accuracy requirement: ±0.1% of full scale for inventory = ±15 mm
Transmitter specified accuracy: ±3 mm (DEL-20.02 specification)
Total loop uncertainty (TLU): ±10 mm including installation effects ✓ (meets requirement)
```

**Source:** **ASSUMPTION** — Example calculation format and typical values

**Project Objective Alignment:**

Supports **OBJ-1: Safe & Reliable Operation** — Calculations verify instruments are correctly sized for safe and reliable measurement.

**Source:** Decomposition Section 6 (line 780)
