# Specification: DEL-14.08 Valve Closing Time Verification Summary

## Scope

Verification that valve closing times comply with surge mitigation requirements from DEL-14.06 and DEL-14.07 transient analyses (source: Decomposition DEL-14.08; attributes: Datasheet.md Report Type, Purpose; rationale: Guidance.md Purpose).

**Report outputs** (source: Decomposition DEL-14.08; construction: Datasheet.md Construction section; procedure: Procedure.md Steps 1-4):
- Valve closing time verification table (construction: Datasheet.md Construction item 1; procedure: Procedure.md Step 3; examples: Guidance.md Examples - Typical Verification Table)
- Assumptions documentation (construction: Datasheet.md Construction item 2; procedure: Procedure.md Step 4; examples: Guidance.md Considerations sections)
- Compliance summary with recommendations (construction: Datasheet.md Construction item 3; procedure: Procedure.md Step 4; examples: Guidance.md Examples item 2)

## Requirements

### Functional Requirements

(construction: Datasheet.md Construction section; rationale: Guidance.md Principles items 2, 4; procedure: Procedure.md Steps 1-4):
- FR-1: Identify all critical valves requiring closing time verification from transient analyses (attributes: Datasheet.md Scope; conditions: Datasheet.md Critical Valves; construction: Datasheet.md Construction item 1; interface: IR-1, IR-2; rationale: Guidance.md Principles item 4; procedure: Procedure.md Step 1; examples: Guidance.md Examples items 1, 2, 3; cross-reference DEL-14.06, DEL-14.07, DEL-14.01)
- FR-2: Extract required valve closing times from DEL-14.06 and DEL-14.07 transient analysis reports (conditions: Datasheet.md Valve Closing Time Requirements; construction: Datasheet.md Construction item 1 - Required closing time; interface: IR-1, IR-2; rationale: Guidance.md Principles items 2, 4; procedure: Procedure.md Prerequisites, Step 1; documentation: Documentation - Verification table; examples: Guidance.md Principles item 4, Guidance.md Examples items 1, 2, 3; cross-reference DEL-14.06, DEL-14.07)
- FR-3: Obtain valve actuator data (sizes, types, stroke times) from PKG-16 or vendor data (construction: Datasheet.md Construction item 1 - Valve size/type, Actuator type, Actual closing time; interface: IR-3; rationale: Guidance.md Principles items 3, 4; considerations: Guidance.md Considerations - Valve Sizing and Selection, Vendor Data; performance: PR-2; procedure: Procedure.md Prerequisites, Step 2; examples: Guidance.md Examples items 1, 2, 3; cross-reference PKG-16)
- FR-4: Verify actuator closing time complies with required closing time (minimum and/or maximum) (conditions: Datasheet.md Verification Approach; construction: Datasheet.md Construction item 1 - Compliance status; performance: PR-3, PR-4; quality: QR-1; rationale: Guidance.md Principles item 4; procedure: Procedure.md Step 3; verification: Verification - Compliance verification; examples: Guidance.md Principles item 4, Guidance.md Examples items 1, 2, 3)
- FR-5: Document non-compliant valves and recommend corrective actions (construction: Datasheet.md Construction item 3; performance: PR-4; quality: QR-2; rationale: Guidance.md Considerations - Safety vs. Surge Control; trade-offs: Guidance.md Trade-offs items 1, 2, 3; procedure: Procedure.md Step 4; documentation: Documentation - Compliance summary; examples: Guidance.md Examples items 2, 3; cross-reference DEL-14.06, DEL-14.07, PKG-16)
- FR-6: Document assumptions and uncertainties for confirmation during detailed design (construction: Datasheet.md Construction item 2; quality: QR-2; procedure: Procedure.md Step 4; documentation: Documentation - Assumptions; examples: Guidance.md Considerations sections)

### Performance Requirements

(rationale: Guidance.md Principles items 3, 4; considerations: Guidance.md Considerations - Valve Sizing and Selection, Operating Conditions, Vendor Data; procedure: Procedure.md Step 2):
- PR-1: Verification shall use manufacturer data or industry-standard actuator sizing methods (attributes: Datasheet.md Verification Method; requirements: FR-3; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Vendor Data; procedure: Procedure.md Step 2; examples: Guidance.md Considerations - Vendor Data)
- PR-2: Actuator data shall account for project operating conditions (differential pressure, temperature, fluid properties) (requirements: FR-3; rationale: Guidance.md Considerations - Operating Conditions, Vendor Data; performance: noted here; procedure: Procedure.md Step 2; examples: Guidance.md Considerations - Operating Conditions; cross-reference DEL-14.02, DEL-14.03)
- PR-3: Verification shall confirm actuator closing time meets minimum closing time requirement (for surge control) (conditions: Datasheet.md Valve Closing Time Requirements - Minimum; construction: Datasheet.md Construction item 1 - Compliance status; requirements: FR-4; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 3; verification: Verification - Compliance verification; examples: Guidance.md Examples items 1, 2; cross-reference DEL-14.06, DEL-14.07)
- PR-4: Verification shall confirm actuator closing time meets maximum closing time requirement (for emergency shutdown) where applicable (conditions: Datasheet.md Valve Closing Time Requirements - Maximum; construction: Datasheet.md Construction items 1, 3; requirements: FR-4, FR-5; rationale: Guidance.md Considerations - Safety vs. Surge Control; procedure: Procedure.md Step 3, Step 4; verification: Verification - Compliance verification; examples: Guidance.md Examples item 3)

### Interface Requirements

(conditions: Datasheet.md Verification Approach; rationale: Guidance.md Principles item 4; procedure: Procedure.md Prerequisites, Steps 1-2):
- IR-1: Required valve closing times from DEL-14.06 (Transient Analysis — Railcar Unloading) (conditions: Datasheet.md Valve Closing Time Requirements; construction: Datasheet.md Construction item 1 - Required closing time; requirements: FR-2; rationale: Guidance.md Principles items 2, 4; procedure: Procedure.md Prerequisites, Step 1; examples: Guidance.md Examples items 1, 2; cross-reference DEL-14.06)
- IR-2: Required valve closing times from DEL-14.07 (Transient Analysis — Marine Loading) (conditions: Datasheet.md Valve Closing Time Requirements; construction: Datasheet.md Construction item 1 - Required closing time; requirements: FR-2; rationale: Guidance.md Principles items 2, 4; considerations: Guidance.md Considerations - Safety vs. Surge Control; procedure: Procedure.md Prerequisites, Step 1; examples: Guidance.md Examples item 3; cross-reference DEL-14.07)
- IR-3: Valve actuator data from PKG-16 (valve sizes, types, actuator specifications, vendor stroke times) (construction: Datasheet.md Construction item 1 - Valve size/type, Actuator type, Actual closing time; requirements: FR-3; rationale: Guidance.md Principles items 3, 4; considerations: Guidance.md Considerations - Valve Sizing and Selection, Vendor Data; performance: PR-1, PR-2; procedure: Procedure.md Prerequisites, Step 2; examples: Guidance.md Examples items 1, 2, 3; cross-reference PKG-16)
- IR-4: Valve tag numbers from DEL-14.01 (P&IDs) (construction: Datasheet.md Construction item 1 - Valve tag number; requirements: FR-1; procedure: Procedure.md Step 1; examples: Guidance.md Examples Table; cross-reference DEL-14.01)

### Quality Requirements

(quality: noted here; rationale: Guidance.md Principles item 4; procedure: Procedure.md Steps 3-5):
- QR-1: All critical valves from transient analyses shall be verified (no omissions) (requirements: FR-1, FR-4; construction: Datasheet.md Construction item 3 - Summary; interface: IR-1, IR-2; procedure: Procedure.md Step 1, Step 3; verification: Verification - Compliance verification; examples: Guidance.md Examples items 1, 2, 3)
- QR-2: Non-compliant valves shall have documented recommendations for resolution (requirements: FR-5, FR-6; construction: Datasheet.md Construction items 2, 3; performance: PR-4; trade-offs: Guidance.md Trade-offs items 1, 2, 3; procedure: Procedure.md Step 4; verification: Verification - Compliance verification; documentation: Documentation - Compliance summary; examples: Guidance.md Examples item 2)
- QR-3: Report shall be reviewed and approved by qualified engineer (procedure: Procedure.md Step 5; verification: Verification - Independent review)

## Standards

(rationale: Guidance.md Principles items 2, 3, 4; procedure: Procedure.md Prerequisites):
- Valve actuator sizing per manufacturer data and industry practice (performance: PR-1, PR-2; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Vendor Data; procedure: Procedure.md Step 2; cross-reference PKG-16)
- Surge analysis requirements per DEL-14.06, DEL-14.07 (requirements: FR-2; interface: IR-1, IR-2; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 1; cross-reference DEL-14.06, DEL-14.07)
- ASME B31.3 — surge mitigation context (rationale: Guidance.md Principles item 2; cross-reference DEL-14.06, DEL-14.07)

## Verification

(quality: QR-1, QR-2, QR-3; procedure: Procedure.md Steps 3-5; verification table):
- **Compliance verification:** All critical valves verified; compliant/non-compliant status documented (requirements: FR-4; quality: QR-1; construction: Datasheet.md Construction item 1 - Compliance status; procedure: Procedure.md Step 3; verification table; examples: Guidance.md Examples items 1, 2, 3)
- **Non-compliant valve resolution:** Recommendations provided for all non-compliant valves (requirements: FR-5; quality: QR-2; construction: Datasheet.md Construction item 3; performance: PR-4; procedure: Procedure.md Step 4; verification table; examples: Guidance.md Examples item 2)
- **Independent review:** Qualified engineer review and sign-off (quality: QR-3; procedure: Procedure.md Step 5; verification table)

**Acceptance:**
- All critical valves from DEL-14.06 and DEL-14.07 verified (requirements: FR-1; quality: QR-1; interface: IR-1, IR-2; verification table)
- Compliance summary complete with recommendations for non-compliant valves (requirements: FR-5; quality: QR-2; construction: Datasheet.md Construction item 3; verification table)
- Report approved (quality: QR-3; verification table)

## Documentation

**Verification table** (construction: Datasheet.md Construction item 1; requirements: FR-1, FR-2, FR-3, FR-4; procedure: Procedure.md Step 3; examples: Guidance.md Examples - Typical Verification Table):
- Valve tag number, location, size/type, actuator type (requirements: FR-1, FR-3; procedure: Procedure.md Step 1, Step 2)
- Required closing time from transient analysis, actual actuator closing time (requirements: FR-2, FR-3; interface: IR-1, IR-2, IR-3; procedure: Procedure.md Step 1, Step 2)
- Compliance status (compliant / non-compliant) (requirements: FR-4; quality: QR-1; procedure: Procedure.md Step 3; verification: Verification - Compliance verification)

**Assumptions** (construction: Datasheet.md Construction item 2; requirements: FR-6; quality: QR-2; procedure: Procedure.md Step 4):
- Actuator operating condition assumptions (performance: PR-1, PR-2; considerations: Guidance.md Considerations - Operating Conditions, Vendor Data)
- Uncertainties requiring confirmation (requirements: FR-6; quality: QR-2; procedure: Procedure.md Step 4)

**Compliance summary** (construction: Datasheet.md Construction item 3; requirements: FR-5; quality: QR-2; procedure: Procedure.md Step 4):
- Number of valves verified, compliant, non-compliant (quality: QR-1; procedure: Procedure.md Step 4; verification: Verification - Compliance verification)
- Recommendations for non-compliant valves (requirements: FR-5; performance: PR-4; quality: QR-2; procedure: Procedure.md Step 4; examples: Guidance.md Examples item 2)

**Storage:** `2_Checking/` → `3_Issued/` (attributes: Datasheet.md Revision Control; procedure: Procedure.md Records section)

**Format:** PDF for issued report; Excel for verification table (procedure: Procedure.md Records section)
