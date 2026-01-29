# Datasheet: DEL-14.08 Valve Closing Time Verification Summary

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-14.08 |
| Name | Valve Closing Time Verification Summary |
| Package | PKG-14 Process Piping |
| Discipline | Mechanical |
| Type | Report |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Report Type | Valve closing time verification and compliance summary (scope: Specification.md Scope; rationale: Guidance.md Purpose; procedure: Procedure.md Purpose) |
| Scope | Critical valves in railcar unloading and marine loading piping systems (attributes: noted here; scope: Specification.md Scope; requirements: Specification.md FR-1; procedure: Procedure.md Step 1; cross-reference DEL-14.06, DEL-14.07) |
| Purpose | Verify valve closing times meet surge mitigation requirements from transient analyses (attributes: noted here; scope: Specification.md Scope; rationale: Guidance.md Purpose, Principles item 2; requirements: Specification.md FR-2; procedure: Procedure.md Step 2; cross-reference DEL-14.06, DEL-14.07) |
| Verification Method | Valve actuator sizing calculations and vendor data review (attributes: noted here; rationale: Guidance.md Principles item 4; requirements: Specification.md PR-1, PR-2; procedure: Procedure.md Step 2; examples: Guidance.md Examples items 1, 2, 3) |

## Conditions

**Purpose and Context:**

This report verifies that valve closing times comply with requirements from DEL-14.06 (Transient Analysis — Railcar Unloading Line) and DEL-14.07 (Transient Analysis — Marine Loading Line) (scope: Specification.md Scope; rationale: Guidance.md Purpose, Principles item 2; requirements: Specification.md FR-2; interface: Specification.md IR-1, IR-2; procedure: Procedure.md Prerequisites, Step 1; examples: Guidance.md Examples items 1, 2, 3; cross-reference DEL-14.06, DEL-14.07).

**Critical Valves:**
- Emergency shutdown (ESD) valves on railcar unloading lines (scope: Specification.md Scope; requirements: Specification.md FR-1; construction: Construction item 1; interface: Specification.md IR-1; procedure: Procedure.md Step 1; examples: Guidance.md Examples items 1, 2; cross-reference DEL-14.01, DEL-14.06, PKG-16)
- Emergency shutdown (ESD) valves on marine loading lines (including loading arm ESD valves) (scope: Specification.md Scope; requirements: Specification.md FR-1; construction: Construction item 1; interface: Specification.md IR-2; considerations: Guidance.md Considerations - Safety vs. Surge Control; procedure: Procedure.md Step 1; examples: Guidance.md Examples item 3; cross-reference DEL-14.01, DEL-14.07, PKG-11, PKG-16)
- Isolation valves on long pipeline runs where transient analysis identified closing time limits (scope: Specification.md Scope; requirements: Specification.md FR-1; construction: Construction item 1; procedure: Procedure.md Step 1; cross-reference DEL-14.06, DEL-14.07)

**Valve Closing Time Requirements:**
- **Minimum closing time:** To limit surge pressure (slower closing = lower surge per Joukowsky equation ΔP = ρ × c × ΔV) (rationale: Guidance.md Principles items 1, 2; requirements: Specification.md FR-2; construction: Construction item 1 - Required closing time; performance: Specification.md PR-3; procedure: Procedure.md Step 1; examples: Guidance.md Principles item 2 - Joukowsky equation, Guidance.md Examples items 1, 2; cross-reference DEL-14.06, DEL-14.07)
- **Maximum closing time:** To meet emergency shutdown time requirements (safety requirement for rapid isolation) (rationale: Guidance.md Principles item 2, Considerations - Safety vs. Surge Control; requirements: Specification.md FR-2; construction: Construction item 1 - Required closing time; considerations: Guidance.md Considerations - Safety vs. Surge Control; trade-offs: Guidance.md Trade-offs item 3; procedure: Procedure.md Step 1; examples: Guidance.md Examples item 3)
- Requirements determined by DEL-14.06 and DEL-14.07 transient analyses (conditions: noted above; interface: Specification.md IR-1, IR-2; rationale: Guidance.md Principles item 4; procedure: Procedure.md Prerequisites, Step 1; cross-reference DEL-14.06, DEL-14.07)

**Verification Approach:**
- Extract required closing times from DEL-14.06 and DEL-14.07 transient analysis reports (requirements: Specification.md FR-2; interface: Specification.md IR-1, IR-2; rationale: Guidance.md Principles item 4; procedure: Procedure.md Prerequisites, Step 1; examples: Guidance.md Principles item 4; cross-reference DEL-14.06, DEL-14.07)
- Obtain valve actuator data from PKG-16 (Valves & Specialty Equipment) — valve sizes, actuator types (motor-operated, pneumatic, hydraulic), stroke times (requirements: Specification.md FR-3; interface: Specification.md IR-3; rationale: Guidance.md Principles item 3, item 4; considerations: Guidance.md Considerations - Vendor Data; procedure: Procedure.md Prerequisites, Step 2; examples: Guidance.md Principles item 4, Guidance.md Examples items 1, 2, 3; cross-reference PKG-16)
- Verify actuator closing time meets required closing time (minimum and/or maximum) (requirements: Specification.md FR-4; performance: Specification.md PR-3, PR-4; rationale: Guidance.md Principles item 4; quality: Specification.md QR-1; procedure: Procedure.md Step 3; verification: Specification.md Verification - Compliance verification; examples: Guidance.md Principles item 4, Guidance.md Examples items 1, 2, 3)
- Document compliance or identify deviations requiring mitigation (construction: Construction items 1, 3; requirements: Specification.md FR-4, FR-5; quality: Specification.md QR-2; procedure: Procedure.md Step 3, Step 4; verification: Specification.md Verification - Compliance verification; examples: Guidance.md Examples items 2, 3)

## Construction

**Anticipated artifacts** (source: Decomposition DEL-14.08; scope: Specification.md Scope; procedure: Procedure.md Steps 1-4; documentation: Specification.md Documentation):

**1. Valve Closing Time Verification:**
- Table listing critical valves with: (construction: noted here; requirements: Specification.md FR-1; rationale: Guidance.md Principles item 4; procedure: Procedure.md Step 3; documentation: Specification.md Documentation - Verification table; examples: Guidance.md Examples - Typical Verification Table)
  - Valve tag number (from P&IDs) (construction: item 1; requirements: Specification.md FR-1; interface: Specification.md IR-4; procedure: Procedure.md Step 1; examples: Guidance.md Examples items 1, 2, 3, Table; cross-reference DEL-14.01)
  - Valve location (railcar unloading line, marine loading line, etc.) (construction: item 1; requirements: Specification.md FR-1; procedure: Procedure.md Step 1; examples: Guidance.md Examples Table; cross-reference DEL-14.06, DEL-14.07)
  - Valve size and type (gate, ball, butterfly, etc.) (construction: item 1; requirements: Specification.md FR-1, FR-3; interface: Specification.md IR-3; rationale: Guidance.md Considerations - Valve Sizing and Selection; procedure: Procedure.md Step 2; examples: Guidance.md Examples items 1, 2, 3, Table; cross-reference PKG-16)
  - Actuator type (motor-operated, pneumatic, hydraulic) (construction: item 1; requirements: Specification.md FR-3; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Valve Sizing and Selection; trade-offs: Guidance.md Trade-offs item 1; procedure: Procedure.md Step 2; examples: Guidance.md Principles item 3, Guidance.md Examples items 1, 2, 3, Table; cross-reference PKG-16)
  - Required closing time from transient analysis (minimum seconds for surge control) (construction: item 1; requirements: Specification.md FR-2; interface: Specification.md IR-1, IR-2; conditions: Valve Closing Time Requirements - Minimum; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 1; examples: Guidance.md Examples items 1, 2, Table; cross-reference DEL-14.06, DEL-14.07)
  - Actual actuator closing time (from vendor data or sizing calculation) (construction: item 1; requirements: Specification.md FR-3; interface: Specification.md IR-3; performance: Specification.md PR-2; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations - Vendor Data; procedure: Procedure.md Step 2; examples: Guidance.md Examples items 1, 2, 3, Table; cross-reference PKG-16)
  - Compliance status (compliant / non-compliant) (construction: item 1; requirements: Specification.md FR-4; quality: Specification.md QR-1; procedure: Procedure.md Step 3; verification: Specification.md Verification - Compliance verification; examples: Guidance.md Examples items 1, 2, Table)

**2. Assumptions:**
- Assumptions used in verification (e.g., actuator operating conditions, power supply assumptions, valve friction factors) (construction: item 2; requirements: Specification.md FR-6; performance: Specification.md PR-1, PR-2; quality: Specification.md QR-2; rationale: Guidance.md Considerations - Operating Conditions, Vendor Data; procedure: Procedure.md Step 2; documentation: Specification.md Documentation - Assumptions; examples: Guidance.md Considerations sections)
- Identification of any uncertainties requiring confirmation during detailed design or procurement (construction: item 2; requirements: Specification.md FR-6; quality: Specification.md QR-2; procedure: Procedure.md Step 4; documentation: Specification.md Documentation - Assumptions)

**3. Compliance Summary:**
- Summary of verification results (number of valves verified, number compliant, number non-compliant) (construction: item 3; requirements: Specification.md FR-5; quality: Specification.md QR-1, QR-2; procedure: Procedure.md Step 4; verification: Specification.md Verification - Compliance verification; documentation: Specification.md Documentation - Compliance summary; examples: Guidance.md Examples item 2)
- Recommendations for non-compliant valves (actuator resizing, valve type change, or surge mitigation adjustment) (construction: item 3; requirements: Specification.md FR-5; performance: Specification.md PR-4; quality: Specification.md QR-2; rationale: Guidance.md Considerations - Safety vs. Surge Control; trade-offs: Guidance.md Trade-offs items 1, 2, 3; procedure: Procedure.md Step 4; documentation: Specification.md Documentation - Compliance summary; examples: Guidance.md Examples item 2 - Recommendation; cross-reference DEL-14.06, DEL-14.07, PKG-16)

## References

**Project References:**
- Decomposition file: /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md
- ER Volume 2 Part 1 (General Requirements), Part 2 (Civil & Process Mechanical Works) (procedure: Procedure.md Prerequisites; cross-reference DEL-14.01, DEL-14.02)

**Applicable Standards:**
- Valve actuator sizing per manufacturer data and industry practice (rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Valve Sizing and Selection, Vendor Data; procedure: Procedure.md Prerequisites, Step 2; cross-reference PKG-16)
- Surge analysis requirements per DEL-14.06, DEL-14.07 (interface: Specification.md IR-1, IR-2; requirements: Specification.md FR-2; rationale: Guidance.md Principles item 2; procedure: Procedure.md Prerequisites, Step 1; cross-reference DEL-14.06, DEL-14.07)

**Cross-references:**
- DEL-14.06 (Transient Analysis Study Report — Railcar Unloading Line) — source of required valve closing times for railcar unloading system (conditions: Critical Valves - ESD valves railcar; requirements: Specification.md FR-2; interface: Specification.md IR-1; rationale: Guidance.md Principles item 4; procedure: Procedure.md Prerequisites, Step 1; verification: Specification.md Verification - Compliance verification; examples: Guidance.md Principles item 4, Guidance.md Examples items 1, 2)
- DEL-14.07 (Transient Analysis Study Report — Marine Loading Line) — source of required valve closing times for marine loading system (conditions: Critical Valves - ESD valves marine; requirements: Specification.md FR-2; interface: Specification.md IR-2; rationale: Guidance.md Principles item 4; procedure: Procedure.md Prerequisites, Step 1; verification: Specification.md Verification - Compliance verification; examples: Guidance.md Principles item 4, Guidance.md Examples item 3)
- PKG-16 (Valves & Specialty Equipment) — valve data (sizes, types, actuator specifications, vendor data) (construction: Construction item 1 - Valve size/type, Actuator type, Actual closing time; requirements: Specification.md FR-3; interface: Specification.md IR-3; rationale: Guidance.md Principles item 3, item 4; considerations: Guidance.md Considerations - Valve Sizing and Selection, Vendor Data; procedure: Procedure.md Prerequisites, Step 2; examples: Guidance.md Principles items 3, 4; Guidance.md Examples items 1, 2, 3)
- DEL-14.01 (Process Piping Design Drawing Set) — P&IDs showing valve locations and tag numbers (construction: Construction item 1 - Valve tag number; requirements: Specification.md FR-1; interface: Specification.md IR-4; procedure: Procedure.md Step 1; examples: Guidance.md Examples Table; cross-reference DEL-14.01)
- PKG-11 (Marine Loading System) — loading arm ESD valve requirements and configuration (conditions: Critical Valves - Loading arm ESD; construction: Construction item 1 - Valve location, Actual closing time; requirements: Specification.md FR-1, FR-2; interface: Specification.md IR-2, IR-3; considerations: Guidance.md Considerations - Safety vs. Surge Control; procedure: Procedure.md Step 1, Step 2; examples: Guidance.md Examples item 3; cross-reference PKG-11, DEL-14.07)

**Related Project Objectives:**
- OBJ-1: Safe & Reliable Operation — valve closing time verification ensures surge mitigation measures effective and valves perform as required for safe operation (rationale: Guidance.md Purpose; requirements: Specification.md FR-4, FR-5; procedure: Procedure.md Purpose; examples: Guidance.md Examples items 2, 3)
- OBJ-2: Throughput Capacity — proper valve operation supports reliable 1,000,000 MT/annum throughput without surge-related disruptions (requirements: Specification.md FR-1; procedure: Procedure.md Prerequisites)
