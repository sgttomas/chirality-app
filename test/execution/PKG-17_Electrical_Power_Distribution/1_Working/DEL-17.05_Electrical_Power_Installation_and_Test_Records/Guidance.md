# Guidance: DEL-17.05 Electrical Power Installation & Test Records

## Purpose

This guidance document supports the development of **Electrical Power Installation & Test Records** for **PKG-17 Electrical Power Distribution**.

**Deliverable Purpose** (Source: Decomposition DEL-17.05 entry): Provides evidence of completion, inspection, and testing for electrical power.

**Downstream Use**: Regulatory compliance (BC Safety Authority), warranty claims, operations baseline, future troubleshooting, modifications/expansions

## Principles

**1. Testing as Verification (Not Discovery)**
- **Principle**: Testing verifies that equipment/installation meets design and specifications; testing is not intended to discover design errors
- **Rationale**: Design errors should be caught during design review and calculation check; testing confirms proper execution
- **Implication**: Test failures indicate installation errors, equipment defects, or (rarely) design errors — investigate and correct before retesting

**2. Test Before Energize (Safety First)**
- **Principle**: Insulation testing (Megger, Hi-Pot) must be performed before energization to detect installation defects (damaged cables, moisture, contamination)
- **Rationale**: Energizing equipment with insulation faults causes immediate failure (flashover, short circuit) — safety hazard and equipment damage
- **Source**: CEC requirements; industry best practice; OBJ-1 (Safe & Reliable Operation)

**3. Test Equipment Calibration**
- **Principle**: Test equipment (Meggers, relay test sets, multimeters) must have valid calibration
- **Rationale**: Uncalibrated test equipment produces unreliable results; test records with expired calibration may not be accepted by inspectors
- **Source**: ISO 17025 (testing laboratory standards); professional practice

**4. Document Everything (Test Records as Legal Evidence)**
- **Principle**: Test records are legal documents (regulatory compliance, warranty claims, liability); must be complete, accurate, signed
- **Rationale**: Incomplete or inaccurate test records have no value; may be rejected by inspector or manufacturer for warranty
- **Best Practice**: Test records signed and dated immediately after test; do not back-date or fabricate test results

**5. Witness Testing (Critical Tests)**
- **Principle**: Critical tests (FAT, energization, final acceptance) may be witnessed by Owner, engineer, or inspector
- **Rationale**: Witness testing provides independent verification and builds confidence; allows immediate issue resolution
- **Recommendation**: Invite BC Safety Authority inspector to witness final energization and system turnover

## Considerations

**1. Factory Acceptance Test (FAT) Witness**
- **Option**: Owner or engineer representative may travel to manufacturer factory to witness FAT
- **Trade-off**: Witness FAT adds travel cost and schedule time but provides early equipment verification (catch defects before shipment)
- **Recommendation**: Witness FAT for critical/expensive equipment (MV switchgear, large transformers); waive for standard equipment (small MCCs, standard transformers)

**2. Insulation Test Voltage Selection**
- **Megger Test**: Use 500V or 1000V for equipment rated ≤ 600V; use 1000V or 2500V for MV equipment — verify in equipment manual before testing
- **Hi-Pot Test**: Use 60-80% of factory test voltage for MV cables (full factory voltage may over-stress field-installed cables)
- **Caution**: Excessive test voltage can damage insulation; follow IEEE Std 43 and IEEE Std 400 guidance

**3. Protection Relay Testing Scope**
- **Full Functional Test**: Verify all relay functions (pickup, timing, instantaneous, ground, directional) — time-consuming but comprehensive
- **Settings Verification Only**: Verify relay settings match coordination study; perform spot-checks of key functions — faster but less thorough
- **Recommendation**: Full functional test for MV switchgear protective relays (critical for system protection); settings verification for LV trip units (lower risk)

**4. Test Failures and Retesting**
- **Common Failures**: Insulation test failures (moisture, contamination, cable damage), relay setting errors, breaker operation issues (mechanical binding, control circuit errors)
- **Investigation**: Determine root cause before retesting (do not simply retest and hope for pass)
- **Corrective Action**: Document corrective action taken (e.g., "cable dried, retested after 24 hours"; "relay settings corrected per coordination study")
- **Retest**: Perform full retest after corrective action; document retest results

**5. Coordination with BC Safety Authority**
- **Inspection Requirements**: BC Safety Authority requires electrical inspection before energization (rough-in inspection) and final inspection (system acceptance)
- **Test Record Review**: Inspector may review test records during inspection; incomplete or failed tests may delay permit closeout
- **Recommendation**: Coordinate inspection schedule with BC Safety Authority early; ensure all test records complete and approved before final inspection

## Trade-offs

**1. Test Thoroughness vs. Schedule**
- **Comprehensive Testing**: All tests per IEEE standards, multiple test points, full functional tests — high confidence but time-consuming
- **Streamlined Testing**: Minimum required tests, spot-checks, abbreviated functional tests — faster but lower confidence
- **Recommendation**: Comprehensive testing for critical equipment (MV switchgear, main transformers); streamlined testing for low-risk equipment (small distribution panels)

**2. In-House Testing vs. Third-Party Testing**
- **In-House**: Contractor performs all testing with own personnel and equipment — lower cost, faster schedule
- **Third-Party**: Independent testing firm performs critical tests — higher cost, adds schedule time, but independent verification and may be required by Employer
- **Recommendation**: In-house testing acceptable for most equipment; third-party testing for MV switchgear relay commissioning if Employer requires independent verification

**3. Test Record Detail Level**
- **Detailed Records**: Comprehensive test reports with photos, test curves, multiple data points — thorough documentation but high effort
- **Summary Records**: Brief test forms with key results only — efficient but less information for future troubleshooting
- **Recommendation**: Detailed records for FAT and critical field tests (relay tests, Hi-Pot); summary records for routine field tests (Megger, visual inspections)

## Examples

**Example Test Record Formats**:

**Insulation Resistance (Megger) Test Form**:
- Equipment: Transformer T-101
- Test Voltage: 1000 VDC
- Test Duration: 1 minute
- Results: Primary-to-ground: 5000 MΩ; Secondary-to-ground: 2500 MΩ; Primary-to-secondary: 3000 MΩ
- Acceptance Criteria: > 1000 MΩ
- Pass/Fail: PASS
- Test Equipment: Megger Model MIT515, S/N 12345, Cal Due: 2026-06-01
- Tested By: J. Smith, C.E.T., Date: 2026-03-15

**Protection Relay Test Form**:
- Relay: MV Switchgear Feeder 1 Relay (50/51)
- Relay Type: SEL-351
- Settings (per coordination study): Pickup = 300A, Time Dial = 3, Inst = 3000A
- Test Results: Pickup measured = 298A (within ±5%), Trip time @ 600A = 2.8 sec (expected 2.9 sec per TCC — within ±10%)
- Pass/Fail: PASS
- Test Equipment: Relay test set Doble F6150, S/N 67890, Cal Due: 2026-05-01
- Tested By: A. Johnson, Relay Technician, Date: 2026-03-20

**Reference Sources**: IEEE test standards (Std 43, 81, 400, C37.90); manufacturer test procedures; project commissioning plan
