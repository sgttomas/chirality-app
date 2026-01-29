# Guidance: DEL-24.04 Security System Installation & Test Records

## Purpose

This guidance document supports the development and management of **Security System Installation & Test Records** for **PKG-24 Security Systems** at the Canola Oil Transload Facility.

**Deliverable objective:** Provides evidence of completion, inspection, and testing for security system, demonstrating that the installed system meets design (DEL-24.01), specification (DEL-24.02), and approved equipment (DEL-24.03) requirements.

*Source: `_CONTEXT.md`; Decomposition Section 5 — PKG-24 (line 569)*

**Classification:** Record deliverable (QA/QC documentation) under Specialty discipline, produced by D&B Contractor (QA/QC)

**Project context:** Installation and test records provide the quality assurance documentation trail from design through installation, testing, and acceptance, supporting Employer handover and becoming permanent facility documentation for operations and maintenance.

*Source: Responsible party designation (QA/QC)*

## Principles

### Quality Assurance and Quality Control (QA/QC) Philosophy

#### Purpose of Installation and Test Records
Installation and test records serve multiple critical functions:

1. **Compliance verification:** Demonstrate that installed system complies with design, specification, and approved equipment
2. **Quality assurance:** Provide evidence that work was performed per standards and best practices
3. **Acceptance basis:** Form the objective basis for Employer acceptance of completed work
4. **Traceability:** Document the complete chain from design → specification → equipment → installation → testing → acceptance
5. **Permanent record:** Become facility documentation for future operations, maintenance, troubleshooting, and modifications

*Source: Standard QA/QC principles*

#### "If It Wasn't Documented, It Wasn't Done"
In construction and commissioning, the quality record is the evidence that work was performed correctly. Key principles:

- **Real-time documentation:** Records should be created during installation/testing, not reconstructed after the fact
- **Completeness:** All required tests and inspections must be documented; gaps are not acceptable
- **Accuracy:** Records must be truthful and accurate; falsifying records is a serious violation
- **Sign-offs:** Records require sign-offs by responsible personnel (tester, inspector, witness)
- **Deficiency management:** Problems must be documented, not hidden; deficiencies are expected and acceptable if properly resolved

*Source: Construction QA/QC best practices*

### Testing Hierarchy and Strategy

#### Progressive Testing Approach
Testing progresses from component level to system level:

**Level 1: Pre-Installation Verification**
- Purpose: Verify equipment is correct and functional before installation
- Catches: Wrong equipment, damaged equipment, equipment non-compliance with submittals
- Cost to fix: Low (equipment not yet installed)

**Level 2: Installation Verification**
- Purpose: Verify proper installation per design and standards
- Catches: Wrong location, improper mounting, poor workmanship, missing components
- Cost to fix: Medium (rework installation)

**Level 3: Individual Equipment Testing**
- Purpose: Verify each equipment item functions correctly
- Catches: Equipment damage during installation, wiring errors, configuration errors
- Cost to fix: Medium (troubleshoot and repair individual equipment)

**Level 4: System Integration Testing**
- Purpose: Verify system-level operation (CCTV, access control, integration)
- Catches: System configuration errors, compatibility issues, integration problems
- Cost to fix: Medium-High (may require reconfiguration, reprogramming)

**Level 5: Site Acceptance Testing (SAT)**
- Purpose: Formal verification that system meets specification requirements
- Catches: Performance deficiencies, missing functionality, specification non-compliance
- Cost to fix: High (formal deficiency resolution process, potential schedule impact)

**Level 6: Commissioning and Operational Testing**
- Purpose: Verify integrated operation under real-world conditions with Terminal systems
- Catches: Operational issues, integration problems, performance under load
- Cost to fix: High (may require system modifications, potential operational impact)

**Strategy:** Find and fix problems early (Levels 1-3) to avoid costly fixes later (Levels 5-6).

*Source: Standard commissioning testing hierarchy*

### Deficiency Management Philosophy

#### Deficiencies Are Normal and Acceptable (If Managed Properly)
Construction and commissioning always involve some deficiencies. What matters is how they are managed:

**Acceptable deficiency management:**
- Deficiencies are identified and documented promptly
- Root cause is understood (installation error, equipment issue, design issue)
- Corrective action plan is developed and scheduled
- Corrections are implemented and verified
- Deficiency is closed with sign-off
- All deficiencies are resolved before final acceptance

**Unacceptable deficiency management:**
- Hiding or not documenting deficiencies
- Incomplete deficiency descriptions (makes troubleshooting difficult)
- No corrective action plan or schedule
- Corrections not verified (problem may recur)
- Deficiencies left open at final acceptance

*Source: Standard construction deficiency management*

#### Prioritizing Deficiencies
Not all deficiencies are equal:

**Critical deficiencies:** Safety issues, non-functional systems, specification non-compliance
- Priority: Immediate resolution required, may block acceptance
- Example: Access control fail-safe operation incorrect (life safety issue)

**Major deficiencies:** Functional issues, performance below specification
- Priority: Must be resolved before final acceptance
- Example: Camera coverage does not meet design requirements

**Minor deficiencies:** Cosmetic issues, documentation gaps, minor workmanship issues
- Priority: Should be resolved before acceptance; may be accepted "as noted" with resolution plan
- Example: Cable labeling incomplete, installation photo missing

*Source: Standard deficiency prioritization*

## Considerations

### Factors to Consider During Installation and Testing

#### 1. Testing Preparation and Planning
**Plan testing in advance:**
- Develop test procedures before installation starts (coordinate with PKG-29)
- Prepare test forms and checklists
- Coordinate test schedule with construction schedule
- Identify test equipment and calibration requirements
- Coordinate witness requirements (designer, Employer, Terminal operations)
- Plan for deficiency resolution time in schedule

**Test prerequisites:**
- Installation must be complete before testing (don't test incomplete installations)
- Power and network infrastructure must be operational
- Testing must be safe (lockout/tagout, hot work permits for hazardous areas)
- Test equipment must be available and calibrated

*Source: Standard testing planning*

#### 2. Installation Quality and Workmanship
**Installation quality affects testing results:**
- Poor installation (wrong location, improper mounting, damaged equipment) will cause test failures
- Focus on getting installation right the first time
- Conduct installation inspections before testing
- Address installation deficiencies before functional testing

**Common installation issues to prevent:**
- Equipment mounted in wrong location or orientation
- Cameras aimed incorrectly (wrong field-of-view)
- Inadequate weatherproofing (moisture ingress, cable entry not sealed)
- Cable damage during installation (kinked, crushed, improperly terminated)
- Incorrect wiring (wrong polarity, crossed pairs, improper grounding)
- Missing or incorrect labeling

*Source: Common security system installation issues*

#### 3. CCTV Coverage Verification
**Coverage verification is subjective and objective:**

**Objective verification:**
- Camera locations match design (DEL-24.01)
- Field-of-view calculations match actual coverage
- Camera specifications match approved submittals (DEL-24.03)
- Image resolution adequate for intended use (identification, recognition, detection)

**Subjective verification:**
- Image quality acceptable (clarity, lighting, no distortion)
- Coverage "looks right" (no obvious blind spots, coverage feels complete)
- Operational usability (security operators can actually use the system effectively)

**Verification process:**
- Daytime coverage verification (adequate lighting, no glare)
- Nighttime coverage verification (adequate IR or lighting per PKG-18)
- Document coverage with screenshots from each camera
- Identify and resolve any coverage gaps or issues
- Obtain designer/Employer sign-off on coverage verification

*Source: DEL-24.01 coverage verification requirements*

#### 4. Access Control Functional Testing
**Access control testing must verify security and life safety:**

**Security functionality:**
- Card readers correctly grant/deny access per access levels
- Audit trail correctly logs all access events (timestamp, user, door, grant/deny)
- Alarms correctly triggered (unauthorized access, door forced open, door held open)
- Access schedule correctly enforces time-based restrictions (if implemented)

**Life safety functionality:**
- Fail-safe doors unlock on power loss or fire alarm (emergency egress maintained)
- Fail-secure doors remain locked (security maintained) where appropriate per code
- Crash bars/panic devices allow free egress without credential
- Fire alarm integration correctly unlocks all doors per life safety requirements

**Testing coordination:**
- Coordinate fire alarm integration testing with PKG-23 (Fire Protection)
- Witness testing with fire marshal or AHJ if required **TBD**

*Source: DEL-24.02 access control requirements; life safety code requirements*

#### 5. Terminal Integration Testing (DEC-05)
**Integration testing is critical and complex:**

**CCTV integration challenges:**
- Network connectivity and bandwidth (video streams are high bandwidth)
- VMS compatibility and configuration (ONVIF compliance helps but doesn't guarantee seamless integration)
- Video quality and latency (acceptable for Terminal monitoring purposes)
- User access and permissions (Terminal security operators need appropriate access)

**Access control integration challenges:**
- Credential synchronization (if Terminal manages credentials centrally)
- Event reporting and audit trail integration
- System boundaries and responsibilities (what is Phase 1 system vs. Terminal system)
- Firewall and network security (proper security while allowing integration)

**Integration testing coordination:**
- Early coordination with Terminal IT/security operations (don't wait until testing phase)
- Adequate time for troubleshooting integration issues
- Acceptance criteria agreed with Terminal operations
- Documentation of integration configuration for future maintenance

*Source: DEC-05 (Decomposition Section 7) — Terminal integration requirements*

#### 6. Record Management and Handover
**Records are permanent facility documentation:**
- Records must be legible, complete, and professional (will be used for years)
- Records should be indexed and easy to navigate (future users will thank you)
- Records should include enough detail for troubleshooting (descriptions, photos, measurements)
- As-built documentation must reflect actual installed configuration (critical for future work)

**Handover to Employer:**
- Final record package submitted as permanent facility documentation
- Training provided to Terminal operations/maintenance staff (PKG-35)
- Operations and maintenance manuals provided
- Warranty documentation and manufacturer support contacts provided
- System ready for operational use

*Source: Standard project handover requirements; PKG-35*

## Trade-offs

### Competing Concerns to Evaluate

#### 1. Testing Thoroughness vs. Schedule
**Trade-off:** Comprehensive testing finds more issues but takes more time; abbreviated testing is faster but may miss deficiencies.

**Considerations:**
- Minimum testing scope required per DEL-24.02 and PKG-29 is non-negotiable
- Additional testing beyond minimum may find issues but extends schedule
- Testing thoroughness should be risk-based (more critical systems get more thorough testing)
- Schedule pressure should not compromise testing quality (problems found during operations are more expensive to fix)

*Decision approach: Perform all required testing per DEL-24.02/PKG-29; risk-based additional testing where warranted*

#### 2. First-Time Pass vs. Deficiency Resolution
**Trade-off:** Rushing installation to meet schedule may result in more deficiencies; careful installation takes longer but reduces deficiencies.

**Considerations:**
- First-time quality (installation done right the first time) is faster overall than rework
- Installation deficiencies found during testing require corrective action and re-test (schedule impact)
- Critical path activities should prioritize quality to avoid rework delays
- Minor deficiencies may be acceptable "as noted" to avoid schedule delay

*Decision approach: Invest in quality installation to minimize deficiencies; manage minor deficiencies pragmatically*

#### 3. Individual Equipment Testing vs. System-Level Testing
**Trade-off:** Testing every individual component is thorough but time-consuming; system-level testing is faster but may miss component issues.

**Considerations:**
- Individual equipment testing finds problems early (before system integration)
- System-level testing is required regardless (tests integration and system performance)
- For large installations (many cameras, many doors), 100% individual testing may not be practical
- Risk-based sampling approach: Test all critical equipment + representative sample of others

*Decision approach: 100% testing of critical components; representative sampling for repetitive components; 100% system-level testing*

#### 4. Detailed Records vs. Record Preparation Time
**Trade-off:** Very detailed records (many photos, detailed observations) are valuable but take time to prepare; minimal records are faster but less useful.

**Considerations:**
- Minimum record content required per DEL-24.02 and project quality plan is non-negotiable
- Additional detail (photos, notes, measurements) aids future troubleshooting and modifications
- Balance: Enough detail to be useful without excessive time investment
- Critical or unusual installations warrant more detailed documentation

*Decision approach: Meet minimum requirements; add detail for critical items, unusual conditions, or field modifications*

## Examples

### Installation Checklist Example

**CCTV Camera Installation Checklist — Example**

| Item | Requirement | Verification | Pass/Fail | Notes |
|------|-------------|--------------|-----------|-------|
| **Camera:** CAM-12 | Location per DWG-SEC-001 | Installed at Grid B-4, elevation +5.5m | ✓ Pass | Location verified |
| | Manufacturer/Model | [Manufacturer] XYZ-4000 per approved submittal | ✓ Pass | Verified against DEL-24.03 |
| | Mounting | Securely mounted to structural steel per detail | ✓ Pass | Mounting inspected |
| | Orientation | Aimed per field-of-view diagram | ✓ Pass | Aimed by installer, to be verified in coverage test |
| | Weatherproofing | Cable entry sealed, gaskets in place, IP67 maintained | ✓ Pass | Cable gland tight, no moisture ingress |
| | Cable routing | Cat6A cable routed per design, supported every 1.5m | ✓ Pass | Cable secured, no sharp bends |
| | Cable labeling | Cable labeled "CAM-12" at both ends | ✓ Pass | Labels visible and legible |
| | Power | PoE+ from switch SW-01 port 12 | ✓ Pass | Verified in network documentation |

**Inspector:** [Name], [Date]
**Signature:** _______________

*Source: Example installation checklist content*

### Test Record Example

**Access Control Functional Test Record — Example**

**Door:** D-101 — Main Entrance
**Reader:** ACR-01 — HID proximity reader
**Controller:** ACP-01, Door relay 1
**Lock:** Electric strike, fail-safe

**Test Date:** 2026-02-15
**Tester:** [Name]
**Witness:** [Designer Name]

| Test Step | Procedure | Expected Result | Actual Result | Pass/Fail |
|-----------|-----------|-----------------|---------------|-----------|
| 1. Reader power | Verify reader LED on | Green LED steady | Green LED steady | ✓ Pass |
| 2. Card read | Present valid card | Beep + green LED flash | Beep + green LED flash | ✓ Pass |
| 3. Door unlock | Present valid card | Strike releases, door unlocks | Strike released, door opened | ✓ Pass |
| 4. Door position | Open door | Controller shows "door open" | Status correct | ✓ Pass |
| 5. REX operation | Press exit button | Strike releases, door unlocks | Strike released, door opened | ✓ Pass |
| 6. Access deny | Present invalid card | Beep + red LED, door stays locked | Beep + red LED, door locked | ✓ Pass |
| 7. Audit trail | Review access log | All events logged with timestamp, user | Events logged correctly | ✓ Pass |
| 8. Fire alarm test | Activate fire alarm (simulate) | Door unlocks (fail-safe) | Door unlocked on fire alarm | ✓ Pass |
| 9. Power loss test | Disconnect power | Door unlocks (fail-safe) | Door unlocked on power loss | ✓ Pass |

**Overall Result:** ✓ PASS — All tests passed, door operates correctly per specification

**Deficiencies:** None

**Tester Signature:** _______________
**Witness Signature:** _______________

*Source: Example access control functional test record*

### Deficiency Record Example

**Deficiency Log Entry — Example**

**Deficiency ID:** DEF-SEC-007
**Date Identified:** 2026-02-10
**Identified By:** QA Inspector [Name]

**Description:**
Camera CAM-25 field-of-view does not match design. Camera is aimed too low, missing upper portion of intended coverage area (tank farm access road). Design requires coverage of road from gate to tank 3; actual coverage stops at tank 2.

**Location:** Tank farm, camera CAM-25 mounted on pole P-5

**Priority:** Major — Coverage gap in critical security area

**Root Cause:** Camera mounting bracket angle incorrect; installer used wrong mounting bracket (Type A instead of Type B per design detail).

**Corrective Action Plan:**
1. Replace mounting bracket with correct Type B bracket (allows higher tilt angle)
2. Re-aim camera per design field-of-view
3. Verify coverage with test screenshots
4. Obtain designer approval of corrected coverage

**Scheduled Resolution Date:** 2026-02-12

**Corrective Action Taken:**
2026-02-12 — Correct mounting bracket installed, camera re-aimed, coverage verified

**Verification:**
Test screenshots reviewed by designer, coverage now meets design requirements, deficiency closed.

**Closed Date:** 2026-02-12
**Closed By:** [Designer Name]

**Status:** ✓ CLOSED

*Source: Example deficiency management record*

---

*Document status: Enriched draft — Pass 1*
*Enrichment date: 2026-01-28*
*Cross-references: Specification.md for testing requirements; Datasheet.md for record scope; Procedure.md for record compilation workflow*
