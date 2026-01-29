# Guidance: DEL-29.03 Test Installation & Test Records

## Purpose

This guidance supports the collection, review, and management of **Test Installation & Test Records** for **PKG-29 Testing**.

**Deliverable Purpose:** Provides evidence of completion, inspection, and testing for test. **Source:** Decomposition line 648

**Type:** Record | **Discipline:** T&C | **Responsible:** D&B Contractor (QA/QC)

## Principles

### Objective Evidence Philosophy

Test records serve as **objective evidence** in quality management:

1. **Legal/Contractual:** Prove contractual obligations met
2. **Regulatory:** Satisfy authority requirements for operating permits
3. **Insurance:** Support insurance coverage and claims
4. **Liability:** Defend against future claims of defective work
5. **Operational:** Provide baseline data for O&M and troubleshooting

**Source:** ISO 9001 (documented quality evidence), general EPC practice **ASSUMPTION**

**Key Principle:** "If it isn't documented, it didn't happen." Records prove work was done correctly.

### Record Quality Attributes

**Accuracy:** Data recorded correctly as measured/observed
**Completeness:** All required fields populated
**Legibility:** Readable and reproducible (especially handwritten records)
**Traceability:** Linkable to procedures, drawings, ITPs
**Authenticity:** Signed by qualified personnel, witnessed as required
**Durability:** Maintained for facility lifetime in controlled conditions

**Source:** ISO 9001, ISO 17025 (calibration records) **ASSUMPTION**

## Considerations

**1. Record Format Selection**
- **Pre-printed forms** (from procedures): Ensure consistency, reduce errors, but less flexible
- **Electronic forms** (tablets, laptops): Easier data entry, automatic calculations, but require equipment in field
- **Narrative reports**: More detail, but time-consuming and subjective
- **Recommendation:** Use pre-printed data sheets from test procedures (DEL-29.01) for field data collection; supplement with narrative reports where engineering judgment is needed **ASSUMPTION**

**2. Data Recording Best Practices**
- Record data in real-time (not from memory)
- Record raw data (not calculated or "massaged")
- Cross out errors (don't erase); initial corrections
- Use indelible ink for permanent records
- Include ambient conditions if relevant (temperature for hydrostatic tests, humidity for electrical tests)
- Photograph test setup, gages, and results

**3. Hold/Witness Point Documentation**
- Hold points: Cannot proceed without Employer release signature
- Obtain signature on test record and/or separate release form
- If Employer not available, work stops; document delay
- Witness points: Provide advance notice; if Employer doesn't attend, document notification and proceed (per agreement)

**4. Failed Test Documentation**
- Document failure mode (leak location, out-of-tolerance reading, etc.)
- Photograph defects
- Issue non-conformance report (NCR)
- Document repair or corrective action
- Re-test and document as new test (cross-reference to original test and NCR)

**5. Calibration Traceability**
- All test instruments and calibration standards shall have current calibration
- Calibration certificates traceable to national standards (NIST, NRC, or equivalent)
- Document test instrument ID and calibration due date on test record
- If instrument found out-of-calibration, all tests since last valid calibration may need to be repeated **ASSUMPTION**

## Trade-offs

**1. Paper vs. Electronic Records**
- **Paper:** Durable, no batteries, legal admissibility established | Bulky, hard to search, degradation over time
- **Electronic:** Searchable, compact storage, easy distribution | Requires backups, format obsolescence, authentication concerns
- **Recommendation:** Collect on paper in field, scan to electronic archive, retain both **ASSUMPTION**

**2. Detailed vs. Summary Records**
- **Detailed:** Complete data, supports future analysis | Voluminous, expensive to produce and store
- **Summary:** Concise, highlights key results | May lack detail for troubleshooting
- **Recommendation:** Detailed data sheets for all tests; summary report for overall testing campaign **ASSUMPTION**

**3. Real-Time Signature vs. Batch Signature**
- **Real-time:** Witnesses sign immediately after test | Requires witness availability throughout test duration
- **Batch:** Compile records, submit for batch signature | More efficient but less authentic (witness didn't observe)
- **Recommendation:** Witness signatures obtained in real-time for hold points; batch review acceptable for routine records **ASSUMPTION**

## Examples

**Hydrostatic Test Record Example:**

---
**HYDROSTATIC TEST RECORD**

System: TK-101 Storage Tank
Test Procedure: DEL-29.01-HT-01
ITP Activity: H-013
Test Date: 2024-06-15

Test Parameters:
- Test Pressure: 72 kPa (1.5 × design)
- Hold Duration: 24 hours
- Test Medium: Potable water
- Ambient Temperature: 18°C

Test Data:
- Start Pressure: 72.0 kPa (Time 08:00)
- Final Pressure: 71.8 kPa (Time 08:00 +24hr)
- Pressure Drop: 0.2 kPa (0.28%)

Acceptance: <5% pressure drop per API 650 (✓ Pass)
No visible leakage observed.

Inspected by: J. Smith, QC Inspector (Sign/Date)
Witnessed by: A. Johnson, Employer Rep (Sign/Date)
Approved by: M. Lee, P.Eng (Sign/Date)

Photos: IMG_2024-06-15_001 through 015

---

**Source:** Typical API 650 hydrostatic test report format **ASSUMPTION**

**Instrument Calibration Record Example:**

---
**CALIBRATION CERTIFICATE**

Instrument: PT-201A Pressure Transmitter
Tag: PT-201A | S/N: 123456 | Range: 0-1000 kPa
Calibration Date: 2024-05-10
Calibrator: Dead Weight Tester S/N 7890 (Cal due 2024-08-01)

As-Found | Applied (kPa) | Output (mA) | Error (%) |
|---------|---------------|-------------|-----------|
| 0       | 4.02          | +0.05       |
| 250     | 8.01          | +0.03       |
| 500     | 12.00         | 0           |
| 750     | 15.99         | -0.03       |
| 1000    | 20.01         | +0.03       |

As-Left: Within ±0.1% (Spec: ±0.25%) | Pass ✓

Calibrated by: T. Brown, Instrument Tech (Sign/Date)
Reviewed by: D. White, P.Eng (Sign/Date)

Calibration sticker affixed: Due 2025-05-10

---

**Source:** Typical calibration certificate format per IEC 62382 **ASSUMPTION**

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | — | — | — | — | — | **TBD** |

---

## Cross-Document Linkage

| Document | Key Sections | Relationship |
|----------|--------------|--------------|
| Datasheet.md | §Attributes, §Construction | Provides factual context for record types and content structure |
| Specification.md | §Requirements (FR, PR, IR, QR), §Standards, §Verification | Defines normative requirements that this Guidance supports |
| Procedure.md | §Steps 1-7 | Implements this Guidance through specific record management steps |

**Guidance-to-Specification Traceability:**
- §Principles (Objective Evidence Philosophy) → Supports Specification FR-1, FR-3
- §Principles (Record Quality Attributes) → Supports Specification PR-1 (Accuracy)
- §Considerations → Supports Specification FR-2 (Content), QR-1 (Review)
- §Trade-offs → Informs engineering decisions for Specification QR-2 (Retention)
- §Examples → Provides implementation patterns for Specification §Documentation

**Guidance-to-Procedure Traceability:**
- §Considerations Item 1 (Format Selection) → Procedure Step 1 (Prepare Forms)
- §Considerations Item 2 (Data Recording) → Procedure Step 2 (Conduct Tests)
- §Considerations Item 3 (Hold/Witness Documentation) → Procedure Step 2
- §Considerations Item 4 (Failed Test Documentation) → Procedure Step 4 (Manage NCRs)
- §Considerations Item 5 (Calibration Traceability) → Procedure Step 3 (Verify)
- §Trade-offs (Paper vs. Electronic) → Procedure Step 7 (Archive)
