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
| Report Type | Valve closing time verification and compliance summary |
| Scope | Critical valves in railcar unloading and marine loading piping systems |
| Purpose | Verify valve closing times meet surge mitigation requirements from transient analyses |
| Verification Method | Valve actuator sizing calculations and vendor data review |

## Conditions

**Purpose and Context:**

This report verifies that valve closing times comply with requirements from DEL-14.06 (Transient Analysis — Railcar Unloading Line) and DEL-14.07 (Transient Analysis — Marine Loading Line).

**Critical Valves:**
- Emergency shutdown (ESD) valves on railcar unloading lines
- Emergency shutdown (ESD) valves on marine loading lines (including loading arm ESD valves)
- Isolation valves on long pipeline runs where transient analysis identified closing time limits

**Valve Closing Time Requirements:**
- **Minimum closing time:** To limit surge pressure (slower closing = lower surge per Joukowsky equation ΔP = ρ × c × ΔV)
- **Maximum closing time:** To meet emergency shutdown time requirements (safety requirement for rapid isolation)
- Requirements determined by DEL-14.06 and DEL-14.07 transient analyses

**Verification Approach:**
- Extract required closing times from DEL-14.06 and DEL-14.07 transient analysis reports
- Obtain valve actuator data from PKG-16 (Valves & Specialty Equipment) — valve sizes, actuator types (motor-operated, pneumatic, hydraulic), stroke times
- Verify actuator closing time meets required closing time (minimum and/or maximum)
- Document compliance or identify deviations requiring mitigation

## Construction

**Anticipated artifacts** (source: Decomposition DEL-14.08):

**1. Valve Closing Time Verification:**
- Table listing critical valves with:
  - Valve tag number (from P&IDs)
  - Valve location (railcar unloading line, marine loading line, etc.)
  - Valve size and type (gate, ball, butterfly, etc.)
  - Actuator type (motor-operated, pneumatic, hydraulic)
  - Required closing time from transient analysis (minimum seconds for surge control)
  - Actual actuator closing time (from vendor data or sizing calculation)
  - Compliance status (compliant / non-compliant)

**2. Assumptions:**
- Assumptions used in verification (e.g., actuator operating conditions, power supply assumptions, valve friction factors)
- Identification of any uncertainties requiring confirmation during detailed design or procurement

**3. Compliance Summary:**
- Summary of verification results (number of valves verified, number compliant, number non-compliant)
- Recommendations for non-compliant valves (actuator resizing, valve type change, or surge mitigation adjustment)

## References

**Project References:**
- Decomposition file: /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md
- ER Volume 2 Part 1 (General Requirements), Part 2 (Civil & Process Mechanical Works)

**Applicable Standards:**
- Valve actuator sizing per manufacturer data and industry practice
- Surge analysis requirements per DEL-14.06, DEL-14.07

**Cross-references:**
- DEL-14.06 (Transient Analysis Study Report — Railcar Unloading Line) — source of required valve closing times for railcar unloading system
- DEL-14.07 (Transient Analysis Study Report — Marine Loading Line) — source of required valve closing times for marine loading system
- PKG-16 (Valves & Specialty Equipment) — valve data (sizes, types, actuator specifications, vendor data)
- DEL-14.01 (Process Piping Design Drawing Set) — P&IDs showing valve locations and tag numbers

**Related Project Objectives:**
- OBJ-1: Safe & Reliable Operation — valve closing time verification ensures surge mitigation measures effective and valves perform as required for safe operation
- OBJ-2: Throughput Capacity — proper valve operation supports reliable 1,000,000 MT/annum throughput without surge-related disruptions
