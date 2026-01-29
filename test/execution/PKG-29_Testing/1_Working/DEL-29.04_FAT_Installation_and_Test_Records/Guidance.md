# Guidance: DEL-29.04 FAT Installation & Test Records

## Purpose

Guidance for managing **FAT Installation & Test Records** for **PKG-29 Testing**.

**Deliverable Purpose:** Provides evidence of completion, inspection, and testing for FAT. **Source:** Decomposition line 649

**Type:** Record | **Discipline:** T&C | **Responsible:** D&B Contractor (QA/QC)

## Principles

### Value of Factory Acceptance Testing

**"Test early, test often"** is a fundamental quality principle. FATs provide:

1. **Early Defect Detection:** Finding problems at vendor facility is 10-100× less costly than finding them after installation
2. **Specification Verification:** Proof equipment meets purchase requirements before shipment and payment
3. **Risk Reduction:** Reduces site commissioning time and startup problems
4. **Personnel Training:** Operations staff can see equipment operation in controlled environment
5. **Relationship Building:** Face-to-face interaction with vendor builds partnership for future support

**Source:** General FAT benefits in EPC projects **ASSUMPTION**

### FAT vs. SAT Philosophy

**FAT (Factory Acceptance Test):**
- Individual equipment testing in controlled factory environment
- Vendor controls test conditions
- Focus on equipment performance per specification
- Conducted before shipment

**SAT (Site Acceptance Test):**
- Integrated system testing in actual installation
- Project site conditions (power quality, ambient, interconnections)
- Focus on system functionality and interfaces
- Conducted after installation

**Both are complementary:** FAT proves equipment, SAT proves system.

## Considerations

**1. Equipment Selection for FAT**

Not all equipment requires FAT. Consider FAT for:
- **High value** (cost >$50k typical threshold **ASSUMPTION**)
- **Complex/custom** (engineered systems, not catalog items)
- **Critical to operations** (single point of failure, no redundancy)
- **Long lead time** (difficult to replace if defective)
- **Performance-critical** (pumps, metering, control systems)

Routine commercial equipment (valves, instruments, motors) typically do not require FAT unless specified.

**2. FAT Timing and Logistics**

- Schedule FATs well in advance (3-4 weeks notice typical)
- Coordinate with vendor production schedule
- Plan travel for Contractor and Employer witnesses
- Some FATs may be combined (multiple equipment at same vendor)
- Remote witnessing (video conference) may be acceptable for some equipment **ASSUMPTION**

**3. FAT Procedure Adequacy**

Vendor FAT procedures should cover:
- All specification performance requirements
- Functional tests for all controls and safety features
- Test conditions representative of operating conditions (or justified deviations)
- Clear acceptance criteria (quantitative where possible)
- Adequate duration (not rushed to meet schedule)

**4. Deficiency Management**

**Categories:**
- **Critical:** Prevents equipment function or creates safety hazard → Must be corrected before shipment
- **Major:** Impacts performance but equipment operable → Correct before shipment or add to punch list with Employer concurrence
- **Minor:** Cosmetic or documentation issues → Punch list acceptable

**Document all deficiencies and resolution plans.**

**5. Custody Transfer Metering Special Requirements**

Metering systems for custody transfer (product sales) have enhanced requirements:
- Calibration traceable to national standards (Measurement Canada)
- Proving (meter factor determination) per regulatory requirements
- Witness by regulatory authority or their delegate may be required
- Special security seals on adjustments

**TBD:** Specific Measurement Canada requirements for canola oil metering **ASSUMPTION**

## Trade-offs

**1. Comprehensive FAT vs. Schedule Pressure**
- Comprehensive testing takes time; vendors may pressure to abbreviate
- **Recommendation:** Don't compromise test scope to meet vendor schedule; defects found later are more costly

**2. Witness All FATs vs. Cost of Travel**
- Witnessing all FATs is ideal but expensive (travel, personnel time)
- **Recommendation:** Prioritize: Witness critical equipment, high-value equipment, first articles; accept vendor test reports for routine items

**3. Correct All Deficiencies vs. Accept Punch List**
- Holding shipment for minor deficiencies delays project
- **Recommendation:** Critical and major deficiencies corrected; minor items on punch list with documented acceptance by Contractor and Employer

## Examples

**Example FAT Report Structure (Transfer Pump):**

```
FACTORY ACCEPTANCE TEST REPORT
Equipment: P-201A Transfer Pump
Manufacturer: XYZ Pumps Inc. | Model: ABC-1000 | S/N: 123456
PO: 2024-MP-001 | Spec: MP-201 | FAT Date: 2024-07-15

1. Equipment Identification
   - Nameplate data verified against PO
   - Dimensions verified against certified drawing

2. Pre-Test Inspection
   - Casing: Cast iron, no defects observed
   - Impeller: Bronze, balanced per API 610
   - Shaft: SS316, runout <0.002" TIR
   - Seals: Mechanical seal, Type 21, verified
   - Motor: 50 HP, 1780 RPM, verified insulation >100 MΩ

3. Performance Test (per API 610)
   Test Medium: Water at 20°C

   | Flow (m3/h) | Head (m) Spec | Head (m) Actual | Efficiency Spec | Efficiency Actual | Result |
   |-------------|---------------|-----------------|-----------------|-------------------|--------|
   | 0 (shutoff) | 42 min        | 44.2            | N/A             | N/A               | Pass   |
   | 90 (rated)  | 38 ±5%        | 39.1            | 72% min         | 74.3%             | Pass   |
   | 110 (max)   | 35 min        | 36.8            | N/A             | N/A               | Pass   |

   Vibration: 2.8 mm/s (Spec: <4.5 mm/s per API 610) | Pass
   Seal Leakage: None observed during 2-hour run | Pass

4. Functional Tests
   - Motor rotation: Correct direction | Pass
   - Start/Stop controls: Functioning correctly | Pass
   - Vibration switch: Trips at setpoint | Pass

5. Deficiencies: None

6. Acceptance: Equipment accepted for shipment

Tested by: J. Vendor, Test Engineer (Sign/Date)
Witnessed by: A. Contractor, QC Inspector (Sign/Date)
Witnessed by: B. Employer, Mechanical Engineer (Sign/Date)

Photographs: FAT-P201A-001 through 015 (attached)
```

**Source:** Typical pump FAT report per API 610 **ASSUMPTION**

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | — | — | — | — | — | **TBD** |
