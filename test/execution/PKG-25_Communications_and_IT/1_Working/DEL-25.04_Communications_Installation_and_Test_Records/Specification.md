# Specification: DEL-25.04 Communications Installation & Test Records

## Scope

This specification defines the requirements for **Communications Installation & Test Records** within **PKG-25 Communications & IT**.

**Purpose:** Provides evidence of completion, inspection, and testing for communications infrastructure.

**Source:** `_CONTEXT.md` Description; Decomposition Table PKG-25 DEL-25.04

**Anticipated deliverable artifacts:**
- Fiber test records
- Network test records (copper cabling)

**Source:** Decomposition Table PKG-25 DEL-25.04

**Package Scope Context:**

PKG-25 covers:
- Communications network
- Fiber infrastructure
- Patch panels
- Workstation connectivity

**Source:** Decomposition Section 5 PKG-25 (Scope)

**Important Note — Record Generation Phase:**

This deliverable defines the requirements for test records. The actual records are generated during the construction/installation phase. During design phase, this deliverable:
- Establishes what records are required (scope)
- Defines test methods and acceptance criteria (requirements)
- Specifies record format and content (documentation)
- Establishes the procedure for record generation (procedure)

**Source:** **ASSUMPTION** — Standard construction record deliverable approach

**Inclusions:**
- Fiber optic cable link test records
- Copper network cable link test records
- Test equipment calibration documentation
- Test summary reports
- Deficiency tracking and resolution records

**Exclusions:**
- CCTV and access control system testing (see PKG-24)
- Control system network testing (see PKG-19)
- System-level functional testing (see PKG-30 Commissioning)

**Source:** Decomposition Section 7 DEC-05; inference from package scope

## Requirements

### Functional Requirements

#### FR-1: Fiber Test Records

**FR-1.1 100% Link Testing:**
- All installed fiber links shall be tested per TIA-568.3-D field testing requirements
- Both directions tested (bidirectional) for insertion loss
- **ASSUMPTION**: OTDR testing for backbone cables

**FR-1.2 Test Parameters:**
- Insertion loss (optical power loss) at applicable wavelengths:
  - Multimode: 850nm and 1300nm
  - Single-mode: 1310nm and 1550nm
- OTDR trace (for backbone/long cables) showing:
  - Length
  - Events (connectors, splices, anomalies)
  - End-to-end attenuation
- Polarity verification

**FR-1.3 Acceptance Criteria:**
- Insertion loss within budget per DEL-25.02 Specification.md §PR-1.1
- **ASSUMPTION**: Per TIA-568.3-D limits for link configuration
- **TBD** — Project-specific acceptance criteria if different from TIA defaults

**FR-1.4 Record Content:**
- Link identification (tag number, from-to locations per DEL-25.01)
- Fiber type and grade (per DEL-25.02)
- Test date, time, and environmental conditions
- Test equipment identification and calibration date
- Test results (numeric values and pass/fail)
- Tester identification and signature
- Witness signature (if required)

**Source:** TIA-568.3-D, TIA-526-7, TIA-526-14; DEL-25.02 §PR-1.3; **ASSUMPTION** for content

#### FR-2: Network Test Records (Copper)

**FR-2.1 100% Link Testing:**
- All installed copper links shall be tested per TIA-568.2-D field testing requirements
- Test configuration: permanent link or channel as specified
- **ASSUMPTION**: Permanent link testing for installed cabling

**FR-2.2 Test Parameters:**
- Wire map (continuity, shorts, opens, crossed pairs, reversed pairs)
- Length
- Insertion loss
- NEXT (Near-End Crosstalk) and PS-NEXT
- Return loss
- ACR-F (ELFEXT) and PS-ACR-F
- Propagation delay and delay skew
- DC loop resistance (optional)

**FR-2.3 Acceptance Criteria:**
- All parameters within TIA-568.2-D limits for specified category
- **ASSUMPTION**: Category 6 (Class E) or Category 6A (Class EA) per DEL-25.02
- Pass/fail determination per TIA-568.2-D Tables 6-12 through 6-23
- **TBD** — Project-specific acceptance criteria if different from TIA defaults

**FR-2.4 Record Content:**
- Link identification (tag number, from-to locations per DEL-25.01)
- Cable category (per DEL-25.02)
- Test configuration (permanent link or channel)
- Test date, time, and environmental conditions
- Test equipment identification and calibration date
- Test results (all parameters, numeric values, margin, and pass/fail)
- Tester identification and signature
- Witness signature (if required)

**Source:** TIA-568.2-D field testing; DEL-25.02 §PR-1.3; **ASSUMPTION** for content

#### FR-3: Test Equipment Requirements

**FR-3.1 Equipment Standards:**
- Test equipment shall meet TIA-568 accuracy requirements:
  - Copper: Level III or higher accuracy per TIA-1152
  - Fiber: Per TIA-526 measurement accuracy requirements
- **ASSUMPTION**: Fluke Networks, Ideal Networks, or equivalent qualified test equipment

**FR-3.2 Calibration:**
- Test equipment shall be calibrated per manufacturer requirements
- Calibration current (within 12 months) at time of testing
- Calibration certificates included in record package

**Source:** TIA-568, TIA-1152; **ASSUMPTION** for equipment

### Performance Requirements

**PR-1: Testing Coverage:**
- 100% of installed fiber links tested for insertion loss
- 100% of installed copper links tested for all TIA-568.2-D parameters
- **TBD** — Sample testing vs. 100% testing (recommend 100%)

**PR-2: Deficiency Resolution:**
- All failed links shall be identified and corrected
- Re-testing required after correction
- All deficiencies tracked to resolution
- Final record package shall show all links passing

**PR-3: Timeliness:**
- Testing completed prior to system energization and commissioning (PKG-30)
- Records submitted within **TBD** days of test completion
- **ASSUMPTION**: Progressive testing during installation, final records upon completion

**Source:** **ASSUMPTION** — Standard construction testing practice

### Interface Requirements

**Coordination Required With:**

- **DEL-25.01 Communications Design Drawing Set:**
  - Link identification (tag numbers, from-to designations)
  - As-built drawing updates if deviations found

- **DEL-25.02 Communications Technical Specification:**
  - Test methods and acceptance criteria
  - Cable category and fiber type for test configuration

- **DEL-25.03 Communications Data Sheet Package:**
  - Equipment identification for terminated links

- **PKG-29 Testing:**
  - Overall project testing strategy and coordination
  - Test procedure integration

- **PKG-30 Commissioning:**
  - Test record handover for commissioning activities
  - System-level functional testing prerequisites

- **Project Quality Plan:**
  - Record format and content requirements
  - Witness and approval requirements
  - Record retention and archival

**Source:** Logical dependencies; cross-references to PKG-25 deliverables and adjacent packages

### Quality Requirements

**QR-1: Record Completeness:**
- All required test records present for all installed links
- No missing data fields (TBD items resolved before acceptance)
- Test summary report showing overall results

**QR-2: Record Accuracy:**
- Test results accurately reflect actual test measurements
- Equipment calibration current at time of testing
- Tester qualifications documented

**QR-3: Record Traceability:**
- Link identification traceable to DEL-25.01 drawings
- Cable specifications traceable to DEL-25.02
- Test methods traceable to TIA-568 standards

**QR-4: Record Format:**
- **ASSUMPTION**: Electronic format (test equipment export files plus summary reports)
- **TBD** — Project EDMS format requirements
- **TBD** — Hardcopy requirements (if any)

**Source:** **ASSUMPTION** — Standard quality record requirements

## Standards

**Applicable Codes and Standards:**

**Testing Standards:**
- TIA-568.2-D (copper cable field testing requirements and procedures)
- TIA-568.3-D (fiber cable field testing requirements and procedures)
- TIA-526-7 (single-mode fiber optical power loss measurement)
- TIA-526-14 (multimode fiber optical power loss measurement)
- TIA-1152 (test equipment accuracy levels)

**Cable Performance Standards:**
- TIA-568.2-D Tables 6-12 through 6-23 (copper performance limits)
- TIA-568.3-D (fiber performance limits)

**Documentation Standards:**
- **TBD** — Project quality plan record requirements
- **TBD** — Project EDMS requirements

**Project-Specific Requirements:**
- Employer's Requirements: **TBD** — Test documentation sections
- **TBD** — Contractor QA/QC procedures

**Source:** Industry standard references; **TBD** for project-specific

## Verification

**Verification Methods for Record Deliverables:**

1. **Completeness Check:**
   - All required links tested (cross-reference to DEL-25.01 cable schedule)
   - All required test parameters present
   - No blank or missing data fields
   - **Acceptance Criteria:** 100% coverage

2. **Data Accuracy Verification:**
   - Test equipment calibration valid
   - Test results within plausible ranges
   - Spot-check sample links for data integrity
   - **Acceptance Criteria:** No data anomalies or inconsistencies

3. **Acceptance Criteria Verification:**
   - All links show "Pass" status or deficiencies resolved
   - Test results within TIA-568 limits
   - **Acceptance Criteria:** All links passing final test

4. **Witness Signature Verification:**
   - Required signatures present (tester, witness if required)
   - Signature dates consistent with test dates
   - **Acceptance Criteria:** All required signatures present

5. **Format Compliance:**
   - Records in required format per project EDMS
   - Files properly named and organized
   - **Acceptance Criteria:** Format compliant

**Source:** Specification.md requirements; **ASSUMPTION** — Standard record verification

**Acceptance Criteria:**
- All installed links tested and passing
- Record package complete with all required documentation
- Test equipment calibration certificates included
- Deficiency tracking showing all issues resolved
- **TBD** — Approval authorities and sign-off

**Source:** **ASSUMPTION** — Standard acceptance criteria

## Documentation

**Required Documentation Outputs:**

Per Decomposition Table PKG-25 DEL-25.04:
- **Fiber test records**
- **Network test records** (copper cabling)

**Record Package Contents:**
1. Test Summary Report — Overall results, pass rates, deficiency summary
2. Individual Link Test Reports — Detailed test data for each link
3. Test Equipment Calibration Certificates
4. Deficiency Log and Resolution Records (if any deficiencies occurred)
5. Tester Qualifications Documentation (if required)

**Source:** Decomposition Table PKG-25 DEL-25.04; **ASSUMPTION** for package contents

**Documentation Format:**
- **ASSUMPTION**: Electronic test reports exported from test equipment
- Summary report in PDF or project standard format
- Individual test files in native test equipment format (Fluke, etc.)
- **TBD** — Project EDMS format requirements

**Documentation Requirements:**
- All documents per project document control procedures
- Revision control per project numbering system: **TBD**
- File naming convention: **TBD**

**Source:** **ASSUMPTION** for format; **TBD** for project-specific requirements

**Cross-Reference to Related Deliverables:**
- DEL-25.01 — Link identification and cable schedules
- DEL-25.02 — Test methods and acceptance criteria
- DEL-25.03 — Equipment identification
- PKG-30 — Commissioning handover documentation

**Source:** Logical relationship between PKG-25 deliverables

---

## Cross-Document Consistency Check

**This section verifies alignment between the four documents for DEL-25.04:**

| Requirement/Entity | Datasheet § | Specification § | Guidance § | Procedure Step |
|-------------------|-------------|-----------------|------------|----------------|
| Fiber test records | Construction §Fiber | FR-1 | Principles §1, Examples | Steps 1-3 |
| Network test records | Construction §Copper | FR-2 | Principles §1, Examples | Steps 1-3 |
| Test parameters | Construction | FR-1.2, FR-2.2 | Considerations §1 | Step 2 |
| Acceptance criteria | Construction, References | FR-1.3, FR-2.3 | Principles §2 | Step 3 |
| Test equipment | References | FR-3 | Considerations §2 | Prerequisites |
| Record content | Construction §Format | FR-1.4, FR-2.4, QR-1 | Considerations §3 | Steps 2-4 |
| 100% testing | Attributes | PR-1 | Principles §1 | Step 1 |
| Deficiency resolution | — | PR-2 | Considerations §4 | Step 3 |
| DEL-25.01 coordination | References §Cross-refs | Interface Req. | Considerations §5 | Step 1 |
| DEL-25.02 coordination | References §Cross-refs | Interface Req. | Considerations §5 | Steps 1-3 |
| TIA-568 standards | References §Standards | Standards | Principles §2 | Prerequisites |
| Verification methods | — | Verification | — | Verification |

**Pass 3 Verification Summary:**

| Check | Status |
|-------|--------|
| Terminology consistency (TIA standards, test terminology) | ✓ Verified |
| Entity coverage across documents | ✓ Verified |
| Source citations complete | ✓ Verified |
| TBD/ASSUMPTION labeling | ✓ Verified |

**Source:** Cross-document consistency check (Pass 3 enrichment)
