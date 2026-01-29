# Datasheet: DEL-29.03 Test Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-29.03 |
| Name | Test Installation & Test Records |
| Package | PKG-29 Testing |
| Discipline | T&C |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

**Source:** _CONTEXT.md, Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md line 648

## Attributes

| Attribute | Value |
|-----------|-------|
| Record Category | Test Records (Evidence of Testing Completion) |
| Record Types | Hydrostatic test records, Electrical test records, Instrument calibration records |
| Applicable Systems | Storage tanks, piping, electrical distribution, control systems |
| Applicable Phase | Construction testing through commissioning |
| Retention Period | Permanent (facility lifetime) **ASSUMPTION** |
| Format | Completed test data sheets, test reports, certifications, photographs |

**Source:** _CONTEXT.md; typical EPC record retention **ASSUMPTION**

**ASSUMPTION:** Test records are permanent quality records retained per ISO 9001 and facility asset management requirements

## Conditions

**Operating / Environmental Context:**

Provides evidence of completion, inspection, and testing for test. **Source:** Decomposition line 648

**Record Purpose:**

Test records serve as objective evidence that:
1. Testing was performed per approved test procedures (DEL-29.01)
2. Test results met specified acceptance criteria
3. Equipment and systems were witnessed/released per ITP (DEL-29.02)
4. Systems are ready for commissioning and operation

**Project Objectives Supported:**
- OBJ-1: Safe & Reliable Operation (test records prove systems are safe)
- OBJ-6: Regulatory Compliance (test records required for authority approvals)

**Source:** Decomposition Section 2 (Project Objectives), Section 6 Objective Mapping

**Record Generation Context:**

Test records are generated during:
- **Construction testing:** Hydrostatic tests, electrical tests, I&C calibration
- **Pre-commissioning:** System flushes, cleaning, initial energization
- **Commissioning:** Functional tests, performance verification (cross-ref PKG-30)

Records are collected, reviewed, and compiled into deliverable packages per this specification.

## Construction

**Record Types and Content:**

### 1. Hydrostatic Test Records

**For each hydrostatic test performed:**
- **Test identification:** System/equipment tag, test date, test number
- **Test data:** Test pressure, hold duration, pressure chart/log, ambient temperature
- **Test results:** Pass/fail, leak observations, pressure drop measurements
- **Inspection data:** ITP activity number (from DEL-29.02), inspector name, witness signatures
- **Supporting documentation:** Test setup photos, leak location photos (if applicable), test water disposal records (cross-ref DEL-29.06-29.08)
- **Acceptance certification:** QC sign-off, Engineer approval, Employer release (if hold point)

**Applicable codes:** ASME B31.3, API 650, CSA Z662 **location TBD**

**Source:** DEL-29.01 (Test Procedures), typical hydrostatic test report format **ASSUMPTION**

### 2. Electrical Test Records

**For each electrical test performed:**
- **Equipment identification:** Equipment tag, system, test date
- **Test type:** Insulation resistance, continuity, protection relay, grounding, energization
- **Test equipment:** Instrument type, calibration due date
- **Test data:** Measured values (resistance, voltage, current, timing)
- **Acceptance criteria:** Specified values per specification or code
- **Test results:** Pass/fail, deviations noted
- **Inspection data:** ITP activity number, inspector, witness
- **Certifications:** QC/Electrician sign-off, Engineer approval, Employer release (if hold point)

**Applicable codes:** NFPA 70, IEEE 43, NETA **location TBD**

**Source:** DEL-29.01 (Test Procedures), typical electrical test report format **ASSUMPTION**

### 3. Instrument Calibration Records

**For each instrument calibrated:**
- **Instrument identification:** Tag number, type, manufacturer, model, serial number
- **Calibration data:** Calibration date, technician name, calibration standard used (with cert/traceability)
- **As-found condition:** Initial readings before adjustment
- **Calibration points:** Applied input vs. measured output (0%, 25%, 50%, 75%, 100% typical)
- **As-left condition:** Final readings after adjustment
- **Accuracy:** Measured accuracy vs. required accuracy
- **Results:** Pass/fail, out-of-tolerance noted
- **Calibration sticker:** Affixed to instrument with calibration date and due date
- **Certifications:** Technician sign-off, Engineer review, Employer witness (if required)

**Applicable standards:** IEC 62382, ISA standards, manufacturer requirements **location TBD**

**Source:** DEL-29.01 (Test Procedures), typical calibration certificate format **ASSUMPTION**

## References

**Decomposition & Context:**
- Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 5, PKG-29, line 648)
- _CONTEXT.md (deliverable identity)
- _REFERENCES.md (reference materials)

**Applicable Standards:**
- ISO 9001: Quality Management Systems (record requirements)
- ASME B31.3: Process Piping (test record requirements)
- API 650: Welded Tanks for Oil Storage (test documentation)
- NFPA 70: National Electrical Code (test records)
- IEC 62382: Electrical and instrumentation loop check (calibration records)
- Project Quality Management Plan: **location TBD** (record formats and retention)

**Cross-References:**

**Upstream (Input) Deliverables:**
- DEL-29.01: Test Procedures — provides procedures followed to generate records
- DEL-29.02: ITP — provides hold/witness designations and acceptance criteria

**Lateral (Related) Deliverables:**
- DEL-29.04: FAT Records — factory test records (subset of testing records)
- DEL-29.05: SAT Records — site acceptance test records (subset of testing records)
- DEL-29.06-29.08: Hydrotest water management records (supporting hydrotest records)

**Downstream (Output) Use:**
- PKG-30 Commissioning: Test records are prerequisites for commissioning
- Facility O&M manuals: Test records provide baseline data
- Regulatory approvals: Test records submitted for operating permits
- Asset records: Test records retained in facility quality files

**ASSUMPTION:** Cross-deliverable relationships based on typical EPC project flow

See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)

---

## Cross-Document Linkage

| Document | Key Sections | Relationship |
|----------|--------------|--------------|
| Specification.md | §Requirements (FR-1 to FR-3, PR-1 to PR-2, IR-1 to IR-2, QR-1 to QR-2) | Defines requirements for record completeness, content, and retention |
| Guidance.md | §Principles, §Considerations, §Trade-offs, §Examples | Provides rationale and examples for record collection and management |
| Procedure.md | §Steps 1-7 | Defines process for preparing, collecting, reviewing, and archiving records |

**Cross-Deliverable Consistency Notes:**
- Test records implement and document results of DEL-29.01 (Test Procedures)
- Test records document completion of ITP activities from DEL-29.02
- Test records parallel FAT records (DEL-29.04) and SAT records (DEL-29.05)
- Hydrostatic test records cross-reference water management records (DEL-29.06 through DEL-29.08)
- Record package is prerequisite for commissioning (PKG-30)
- Objectives OBJ-1 (Safe & Reliable Operation) and OBJ-6 (Regulatory Compliance) are supported through documented evidence
