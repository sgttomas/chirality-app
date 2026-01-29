# Procedure: DEL-14.08 Valve Closing Time Verification Summary

## Purpose

Procedure for verifying valve closing times comply with surge mitigation requirements from DEL-14.06 and DEL-14.07 transient analyses (scope: Specification.md Scope; attributes: Datasheet.md Report Type, Purpose; rationale: Guidance.md Purpose).

## Prerequisites

**Dependencies:** NOT_TRACKED (coordinated externally; see `_DEPENDENCIES.md`)

**Inputs Required** (interface: Specification.md Interface Requirements; rationale: Guidance.md Principles item 4; conditions: Datasheet.md Verification Approach):
- Required valve closing times from DEL-14.06 (Transient Analysis — Railcar Unloading Line) (conditions: Datasheet.md Valve Closing Time Requirements; construction: Datasheet.md Construction item 1 - Required closing time; requirements: Specification.md FR-2; interface: Specification.md IR-1; rationale: Guidance.md Principles items 2, 4; Step 1 below; examples: Guidance.md Examples items 1, 2; cross-reference DEL-14.06)
- Required valve closing times from DEL-14.07 (Transient Analysis — Marine Loading Line) (conditions: Datasheet.md Valve Closing Time Requirements; construction: Datasheet.md Construction item 1 - Required closing time; requirements: Specification.md FR-2; interface: Specification.md IR-2; rationale: Guidance.md Principles items 2, 4; considerations: Guidance.md Considerations - Safety vs. Surge Control; Step 1 below; examples: Guidance.md Examples item 3; cross-reference DEL-14.07)
- Valve data from PKG-16 (valve sizes, types, actuator types, actuator specifications) (construction: Datasheet.md Construction item 1 - Valve size/type, Actuator type, Actual closing time; requirements: Specification.md FR-3; interface: Specification.md IR-3; rationale: Guidance.md Principles items 3, 4; considerations: Guidance.md Considerations - Valve Sizing and Selection, Vendor Data; performance: Specification.md PR-1, PR-2; Step 2 below; examples: Guidance.md Examples items 1, 2, 3; cross-reference PKG-16)
- Valve tag numbers from DEL-14.01 P&IDs (construction: Datasheet.md Construction item 1 - Valve tag number; requirements: Specification.md FR-1; interface: Specification.md IR-4; Step 1 below; examples: Guidance.md Examples Table; cross-reference DEL-14.01)

**Personnel** (quality: Specification.md QR-3):
- Piping or mechanical engineer (familiar with valve sizing and surge mitigation) (quality: Specification.md QR-3; rationale: Guidance.md Principles items 1, 2, 3, 4)
- Independent reviewer (qualified piping or process engineer) (quality: Specification.md QR-3; Step 5 below; verification: Specification.md Verification - Independent review)

## Steps

### Step 1: Identify Critical Valves and Extract Requirements

**Objective:** Identify all valves requiring closing time verification and extract required closing times from transient analyses (conditions: Datasheet.md Critical Valves; requirements: Specification.md FR-1, FR-2; interface: Specification.md IR-1, IR-2; rationale: Guidance.md Principles item 4; examples: Guidance.md Examples items 1, 2, 3).

**Actions:**
1. Review DEL-14.06 transient analysis report:
   - Identify valves on railcar unloading lines where closing time limits specified (conditions: Datasheet.md Critical Valves - ESD valves railcar; construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1; interface: Specification.md IR-1; examples: Guidance.md Examples items 1, 2; cross-reference DEL-14.06)
   - Extract required closing time for each valve (minimum and/or maximum seconds) (construction: Datasheet.md Construction item 1 - Required closing time; requirements: Specification.md FR-2; interface: Specification.md IR-1; rationale: Guidance.md Principles items 2, 4; examples: Guidance.md Principles item 4, Guidance.md Examples items 1, 2; cross-reference DEL-14.06)
2. Review DEL-14.07 transient analysis report:
   - Identify valves on marine loading lines where closing time limits specified (including loading arm ESD valves) (conditions: Datasheet.md Critical Valves - ESD valves marine, Loading arm ESD; construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1; interface: Specification.md IR-2; examples: Guidance.md Examples item 3; cross-reference DEL-14.07, PKG-11)
   - Extract required closing time for each valve (minimum and/or maximum seconds) (construction: Datasheet.md Construction item 1 - Required closing time; requirements: Specification.md FR-2; interface: Specification.md IR-2; rationale: Guidance.md Principles items 2, 4; considerations: Guidance.md Considerations - Safety vs. Surge Control; examples: Guidance.md Principles item 4, Guidance.md Examples item 3; cross-reference DEL-14.07)
3. Compile master list of critical valves with required closing times from both transient analyses (requirements: Specification.md FR-1, FR-2; quality: Specification.md QR-1; procedure: noted here; documentation: Specification.md Documentation - Verification table; examples: Guidance.md Examples Table)

**Outputs:**
- List of critical valves with required closing times (construction: Datasheet.md Construction item 1 - partial; requirements: Specification.md FR-1, FR-2; used in Step 3)

---

### Step 2: Obtain Valve Actuator Data

**Objective:** Collect valve actuator specifications and closing times (construction: Datasheet.md Construction item 1 - Valve size/type, Actuator type, Actual closing time; requirements: Specification.md FR-3; interface: Specification.md IR-3; rationale: Guidance.md Principles items 3, 4; examples: Guidance.md Examples items 1, 2, 3).

**Actions:**
1. For each critical valve (from Step 1):
   - Obtain valve size and type from PKG-16 or DEL-14.01 P&IDs (construction: Datasheet.md Construction item 1 - Valve size/type; requirements: Specification.md FR-1, FR-3; interface: Specification.md IR-3, IR-4; rationale: Guidance.md Considerations - Valve Sizing and Selection; examples: Guidance.md Examples items 1, 2, 3; cross-reference DEL-14.01, PKG-16)
   - Obtain actuator type (motor-operated, pneumatic, hydraulic) from PKG-16 valve specification (construction: Datasheet.md Construction item 1 - Actuator type; requirements: Specification.md FR-3; interface: Specification.md IR-3; rationale: Guidance.md Principles item 3; trade-offs: Guidance.md Trade-offs item 1; examples: Guidance.md Principles item 3, Guidance.md Examples items 1, 2, 3; cross-reference PKG-16)
   - Obtain actuator stroke time from PKG-16 vendor data or actuator sizing calculation (construction: Datasheet.md Construction item 1 - Actual closing time; requirements: Specification.md FR-3; interface: Specification.md IR-3; performance: Specification.md PR-1, PR-2; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations - Vendor Data, Operating Conditions; examples: Guidance.md Considerations - Vendor Data, Guidance.md Examples items 1, 2, 3; cross-reference PKG-16)
2. Verify actuator data accounts for project operating conditions:
   - Differential pressure across valve (from DEL-14.03 design data or process conditions) (performance: Specification.md PR-2; considerations: Guidance.md Considerations - Operating Conditions; examples: Guidance.md Considerations - Operating Conditions; cross-reference DEL-14.03)
   - Fluid properties (canola oil viscosity) (performance: Specification.md PR-2; considerations: Guidance.md Considerations - Operating Conditions; cross-reference DEL-14.02)
   - Temperature range (ambient conditions for Fraser Surrey, BC) (construction: Datasheet.md Construction item 2 - Assumptions; performance: Specification.md PR-2; requirements: Specification.md FR-6; considerations: Guidance.md Considerations - Operating Conditions; cross-reference DEL-14.02)
3. Document assumptions used in actuator data (e.g., standard operating conditions, manufacturer standard data applies) (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-6; quality: Specification.md QR-2; considerations: Guidance.md Considerations - Vendor Data; documentation: Specification.md Documentation - Assumptions; examples: Guidance.md Considerations sections)

**Outputs:**
- Valve actuator data for all critical valves (construction: Datasheet.md Construction item 1 - partial; requirements: Specification.md FR-3; used in Step 3)

---

### Step 3: Verify Compliance

**Objective:** Compare actual valve closing times to required closing times and determine compliance (construction: Datasheet.md Construction item 1 - Compliance status; requirements: Specification.md FR-4; performance: Specification.md PR-3, PR-4; quality: Specification.md QR-1; rationale: Guidance.md Principles item 4; verification: Specification.md Verification - Compliance verification; examples: Guidance.md Examples items 1, 2, 3).

**Actions:**
1. For each valve, compare actual actuator closing time vs. required closing time:
   - **Minimum closing time requirement:** Verify actual time ≥ required minimum (for surge control) (conditions: Datasheet.md Valve Closing Time Requirements - Minimum; construction: Datasheet.md Construction item 1 - Compliance status; requirements: Specification.md FR-4; performance: Specification.md PR-3; rationale: Guidance.md Principles item 2; procedure: noted here; examples: Guidance.md Principles item 4, Guidance.md Examples items 1, 2)
   - **Maximum closing time requirement:** Verify actual time ≤ required maximum (for emergency shutdown) where applicable (conditions: Datasheet.md Valve Closing Time Requirements - Maximum; construction: Datasheet.md Construction item 1 - Compliance status; requirements: Specification.md FR-4; performance: Specification.md PR-4; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Safety vs. Surge Control; procedure: noted here; examples: Guidance.md Examples item 3)
2. Mark compliance status:
   - **Compliant:** Actual closing time meets required closing time (construction: Datasheet.md Construction item 1 - Compliance status; requirements: Specification.md FR-4; quality: Specification.md QR-1; examples: Guidance.md Examples items 1, 3)
   - **Non-Compliant:** Actual closing time does not meet required closing time (construction: Datasheet.md Construction items 1, 3; requirements: Specification.md FR-4, FR-5; quality: Specification.md QR-1, QR-2; verification: Specification.md Verification - Non-compliant valve resolution; examples: Guidance.md Examples item 2)
3. Populate verification table with all data (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1, FR-2, FR-3, FR-4; quality: Specification.md QR-1; documentation: Specification.md Documentation - Verification table; examples: Guidance.md Examples Table)

**Outputs:**
- Complete valve closing time verification table (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1 through FR-4; quality: Specification.md QR-1; documentation: Specification.md Documentation - Verification table; records: Records section; examples: Guidance.md Examples Table)

---

### Step 4: Prepare Compliance Summary and Recommendations

**Objective:** Summarize verification results and provide recommendations for non-compliant valves (construction: Datasheet.md Construction items 2, 3; requirements: Specification.md FR-5, FR-6; quality: Specification.md QR-2; documentation: Specification.md Documentation - Compliance summary, Assumptions; examples: Guidance.md Examples item 2).

**Actions:**
1. Prepare compliance summary:
   - Total number of critical valves verified (requirements: Specification.md FR-5; quality: Specification.md QR-1; construction: Datasheet.md Construction item 3; documentation: Specification.md Documentation - Compliance summary)
   - Number compliant (quality: Specification.md QR-1; examples: Guidance.md Examples items 1, 3)
   - Number non-compliant (quality: Specification.md QR-2; examples: Guidance.md Examples item 2)
2. For each non-compliant valve, document recommendations:
   - Actuator resizing (change from pneumatic to motor-operated for slower closing) (construction: Datasheet.md Construction item 3 - Recommendations; requirements: Specification.md FR-5; performance: Specification.md PR-4; rationale: Guidance.md Principles item 3; trade-offs: Guidance.md Trade-offs item 1; examples: Guidance.md Examples item 2 - Option 1; cross-reference PKG-16)
   - Valve type change (change valve type if actuator sizing not feasible) (requirements: Specification.md FR-5; performance: Specification.md PR-4; considerations: Guidance.md Considerations - Valve Sizing and Selection; cross-reference PKG-16)
   - Surge mitigation adjustment (add surge relief valve instead of changing actuator; or revise transient analysis with different mitigation approach) (construction: Datasheet.md Construction item 3 - Recommendations; requirements: Specification.md FR-5; performance: Specification.md PR-4; considerations: Guidance.md Considerations - Safety vs. Surge Control; trade-offs: Guidance.md Trade-offs items 2, 3; examples: Guidance.md Examples item 2 - Option 2, Guidance.md Examples item 3 - Mitigation; cross-reference DEL-14.06, DEL-14.07, PKG-16)
3. Document assumptions and uncertainties:
   - Actuator operating condition assumptions (differential pressure, temperature, fluid properties) (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-6; performance: Specification.md PR-2; considerations: Guidance.md Considerations - Operating Conditions, Vendor Data; documentation: Specification.md Documentation - Assumptions; examples: Guidance.md Considerations sections)
   - Vendor data applicability (verify manufacturer data applies to project conditions) (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-6; performance: Specification.md PR-1, PR-2; considerations: Guidance.md Considerations - Vendor Data; documentation: Specification.md Documentation - Assumptions)
   - Uncertainties requiring confirmation during detailed design or procurement (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-6; quality: Specification.md QR-2; documentation: Specification.md Documentation - Assumptions)

**Outputs:**
- Compliance summary with recommendations (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-5; documentation: Specification.md Documentation - Compliance summary; records: Records section)
- Assumptions documentation (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-6; documentation: Specification.md Documentation - Assumptions; records: Records section)

---

### Step 5: Independent Review and Approval

**Objective:** Independent verification and approval of valve closing time verification summary (quality: Specification.md QR-3; verification: Specification.md Verification - Independent review).

**Actions:**
1. Assign independent reviewer (qualified piping or process engineer) (personnel: Prerequisites section; quality: Specification.md QR-3; verification: Specification.md Verification - Independent review; verification table)
2. Reviewer verifies:
   - All critical valves from DEL-14.06 and DEL-14.07 included (no omissions) (requirements: Specification.md FR-1; quality: Specification.md QR-1; interface: Specification.md IR-1, IR-2; verification: Specification.md Verification - Compliance verification; cross-reference DEL-14.06, DEL-14.07)
   - Required closing times correctly extracted from transient analyses (requirements: Specification.md FR-2; interface: Specification.md IR-1, IR-2; rationale: Guidance.md Principles item 4; cross-reference DEL-14.06, DEL-14.07)
   - Actuator data correct (sizes, types, closing times) (requirements: Specification.md FR-3; interface: Specification.md IR-3; performance: Specification.md PR-1, PR-2; cross-reference PKG-16)
   - Compliance determinations correct (requirements: Specification.md FR-4; performance: Specification.md PR-3, PR-4; quality: Specification.md QR-1; verification: Specification.md Verification - Compliance verification)
   - Recommendations for non-compliant valves appropriate (requirements: Specification.md FR-5; quality: Specification.md QR-2; verification: Specification.md Verification - Non-compliant valve resolution)
3. Reviewer signs off or issues comments (quality: Specification.md QR-3; verification: Specification.md Verification - Independent review; verification table)
4. Address reviewer comments and update report
5. Discipline lead approves final report (quality: Specification.md QR-3; verification: Specification.md Verification - Acceptance; verification table)

**Outputs:**
- Approved valve closing time verification summary ready for issue (verification: Specification.md Verification - Acceptance; verification table; records: Records section)

---

## Verification

**Verification activities summary:**

| Step | Verification Method | Acceptance Criteria |
|------|---------------------|---------------------|
| 1. Identify Valves and Requirements | Cross-check vs. DEL-14.06, DEL-14.07 | All critical valves identified; required closing times extracted (requirements: Specification.md FR-1, FR-2; quality: Specification.md QR-1; verification: Specification.md Verification - Compliance verification) |
| 2. Obtain Actuator Data | Vendor data review | Actuator data complete for all valves (requirements: Specification.md FR-3; performance: Specification.md PR-1, PR-2; verification: Specification.md Verification) |
| 3. Verify Compliance | Closing time comparison | Compliance status determined for all valves (requirements: Specification.md FR-4; performance: Specification.md PR-3, PR-4; quality: Specification.md QR-1; verification: Specification.md Verification - Compliance verification) |
| 4. Compliance Summary | Review of results | Summary complete; recommendations for non-compliant valves (requirements: Specification.md FR-5, FR-6; quality: Specification.md QR-2; verification: Specification.md Verification - Non-compliant valve resolution) |
| 5. Independent Review | Qualified engineer review | Reviewer sign-off; discipline lead approval (quality: Specification.md QR-3; verification: Specification.md Verification - Independent review, Acceptance) |

**Overall acceptance criteria** (verification: Specification.md Verification - Acceptance; verification table):
- All critical valves from DEL-14.06 and DEL-14.07 verified (requirements: Specification.md FR-1; quality: Specification.md QR-1; interface: Specification.md IR-1, IR-2; verification table)
- Compliance summary complete with recommendations for non-compliant valves (requirements: Specification.md FR-5; quality: Specification.md QR-2; construction: Datasheet.md Construction item 3; verification table)
- Report approved (quality: Specification.md QR-3; verification table)

---

## Records

**Outputs** (construction: Datasheet.md Construction section; scope: Specification.md Scope; documentation: Specification.md Documentation section):
- Valve closing time verification table (Excel or PDF) (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1 through FR-4; documentation: Specification.md Documentation - Verification table; Step 3 above; examples: Guidance.md Examples Table)
- Assumptions documentation (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-6; documentation: Specification.md Documentation - Assumptions; Step 4 above)
- Compliance summary with recommendations (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-5; documentation: Specification.md Documentation - Compliance summary; Step 4 above)

**Storage:** `2_Checking/` → `3_Issued/` (attributes: Datasheet.md Revision Control; documentation: Specification.md Documentation - Storage; Step 5 above)

**Format:** PDF for issued report; Excel for verification table (documentation: Specification.md Documentation - Format)

**Distribution:**
- Valve design and procurement (PKG-16) — for implementation of actuator requirements (cross-reference PKG-16)
- Piping design team — for coordination with surge mitigation measures (cross-reference DEL-14.01, DEL-14.06, DEL-14.07)
- Operations — for operational procedures and valve operation requirements (cross-reference PKG-33, PKG-34)
- Project file (permanent record) (quality: Specification.md QR-3)
