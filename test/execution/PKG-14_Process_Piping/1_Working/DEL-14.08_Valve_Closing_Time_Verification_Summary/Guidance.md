# Guidance: DEL-14.08 Valve Closing Time Verification Summary

## Purpose

Verify valve closing times comply with surge mitigation requirements from transient analyses (DEL-14.06 Railcar Unloading, DEL-14.07 Marine Loading) (scope: Specification.md Scope; attributes: Datasheet.md Purpose; rationale: noted below).

**Project context:** CSD canola oil transload facility, 1,000,000 MT/annum, Fraser Surrey Terminal BC (cross-reference DEL-14.01, DEL-14.02).

## Principles

**1. Valve Closing Time Defined:**
- **Closing time:** Time for valve to travel from fully open (100%) to fully closed (0%) (rationale: noted here; requirements: Specification.md FR-2; procedure: Procedure.md Step 2; examples: below items 1, 2, 3)
- Measured in seconds (construction: Datasheet.md Construction item 1 - Required closing time, Actual closing time; examples: below items 1, 2, 3)
- Depends on valve type, size, actuator type, and actuator power (rationale: noted here and item 3 below; considerations: below - Valve Sizing and Selection; trade-offs: below item 1; procedure: Procedure.md Step 2; examples: below items 1, 2, 3; cross-reference PKG-16)

**2. Surge Mitigation and Valve Closing Time:**
- **Joukowsky equation:** ΔP = ρ × c × ΔV (rationale: noted here; conditions: Datasheet.md Valve Closing Time Requirements - Minimum; standards: Specification.md Standards - Surge analysis requirements; examples: below; parallel: DEL-14.06, DEL-14.07)
  - Surge pressure (ΔP) proportional to velocity change (ΔV) (rationale: noted here; requirements: Specification.md FR-2; parallel: DEL-14.06 Guidance.md Principles item 1, DEL-14.07 Guidance.md Principles item 1)
  - Slower valve closing → smaller ΔV/Δt (rate of velocity change) → lower surge pressure (rationale: noted here; conditions: Datasheet.md Valve Closing Time Requirements - Minimum; requirements: Specification.md FR-2; performance: Specification.md PR-3; procedure: Procedure.md Step 1; examples: below; cross-reference DEL-14.06, DEL-14.07)
- **Transient analyses (DEL-14.06, DEL-14.07) specify:** (interface: Specification.md IR-1, IR-2; rationale: noted here and item 4 below; procedure: Procedure.md Prerequisites, Step 1; cross-reference DEL-14.06, DEL-14.07)
  - **Minimum closing time:** To limit surge pressure below design pressure (e.g., "valve must close in minimum 10 seconds to limit surge to acceptable level") (conditions: Datasheet.md Valve Closing Time Requirements - Minimum; construction: Datasheet.md Construction item 1 - Required closing time; requirements: Specification.md FR-2; performance: Specification.md PR-3; procedure: Procedure.md Step 1; examples: below items 1, 2)
  - **Maximum closing time:** (Less common) For emergency shutdown requirements (e.g., "valve must close within 30 seconds for emergency isolation") (conditions: Datasheet.md Valve Closing Time Requirements - Maximum; construction: Datasheet.md Construction item 1 - Required closing time; requirements: Specification.md FR-2; performance: Specification.md PR-4; considerations: below - Safety vs. Surge Control; trade-offs: below item 3; procedure: Procedure.md Step 1; examples: below item 3)

**3. Valve Actuator Types:**
- **Motor-operated valve (MOV):** Electric motor drives valve stem; closing time typically 10-60 seconds (slow, controllable); good for surge control (construction: Datasheet.md Construction item 1 - Actuator type; requirements: Specification.md FR-3; rationale: noted here; considerations: below - Valve Sizing and Selection; trade-offs: below item 1; procedure: Procedure.md Step 2; examples: below items 1, 2; cross-reference PKG-16)
- **Pneumatic actuator:** Compressed air drives valve; closing time typically 2-10 seconds (fast); higher surge risk but good for emergency shutdown (construction: Datasheet.md Construction item 1 - Actuator type; requirements: Specification.md FR-3; rationale: noted here; considerations: below - Safety vs. Surge Control; trade-offs: below item 1; procedure: Procedure.md Step 2; examples: below items 2, 3; cross-reference PKG-16)
- **Hydraulic actuator:** Hydraulic pressure drives valve; closing time typically 5-20 seconds (medium speed) (construction: Datasheet.md Construction item 1 - Actuator type; requirements: Specification.md FR-3; rationale: noted here; trade-offs: below item 1; procedure: Procedure.md Step 2; cross-reference PKG-16)
- **Manual valve:** Hand-operated; closing time variable (not typically used for surge-critical applications) (rationale: noted here; considerations: below - Valve Sizing and Selection)

**4. Verification Approach:**
- **Extract requirements:** From DEL-14.06 and DEL-14.07 transient analysis reports (e.g., "Valve V-101 must close in minimum 15 seconds") (conditions: Datasheet.md Verification Approach; construction: Datasheet.md Construction item 1 - Required closing time; requirements: Specification.md FR-2; interface: Specification.md IR-1, IR-2; rationale: noted here; procedure: Procedure.md Prerequisites, Step 1; examples: below items 1, 2, 3; cross-reference DEL-14.06, DEL-14.07)
- **Obtain actuator data:** From PKG-16 valve specifications or vendor data (e.g., "Valve V-101 has motor-operated actuator with 20-second stroke time") (conditions: Datasheet.md Verification Approach; construction: Datasheet.md Construction item 1 - Actual closing time; requirements: Specification.md FR-3; interface: Specification.md IR-3; performance: Specification.md PR-1, PR-2; rationale: noted here; considerations: below - Vendor Data; procedure: Procedure.md Prerequisites, Step 2; examples: below items 1, 2, 3; cross-reference PKG-16)
- **Verify compliance:** Compare actuator closing time vs. required closing time (20 sec ≥ 15 sec minimum → compliant) (conditions: Datasheet.md Verification Approach; construction: Datasheet.md Construction item 1 - Compliance status; requirements: Specification.md FR-4; performance: Specification.md PR-3, PR-4; quality: Specification.md QR-1; rationale: noted here; procedure: Procedure.md Step 3; verification: Specification.md Verification - Compliance verification; examples: below items 1, 2, 3)
- **Document:** Table showing valve tag, required time, actual time, compliance status (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1, FR-4; quality: Specification.md QR-1; procedure: Procedure.md Step 3; documentation: Specification.md Documentation - Verification table; examples: below - Typical Verification Table)

## Considerations

**Valve Sizing and Selection:**
- Valve size affects closing time: Larger valves require more torque → larger actuator or longer closing time (rationale: above item 1; considerations: noted here; trade-offs: below item 1; procedure: Procedure.md Step 2; cross-reference PKG-16)
- Valve type affects torque requirement: Ball valves (high torque near closed position), butterfly valves (lower torque), gate valves (moderate torque throughout stroke) (construction: Datasheet.md Construction item 1 - Valve size/type; requirements: Specification.md FR-1, FR-3; rationale: above items 1, 3; considerations: noted here; procedure: Procedure.md Step 2; cross-reference PKG-16)
- Actuator sizing by valve manufacturer or engineer: Considers valve size, type, differential pressure, friction, safety factors (requirements: Specification.md FR-3; performance: Specification.md PR-1, PR-2; rationale: above item 3; considerations: noted here; procedure: Procedure.md Step 2; cross-reference PKG-16)

**Operating Conditions:**
- Differential pressure across valve affects torque: Higher ΔP → higher torque → may require larger actuator or longer closing time (requirements: Specification.md FR-3; performance: Specification.md PR-2; rationale: above item 3; considerations: noted here; procedure: Procedure.md Step 2; cross-reference DEL-14.03)
- Fluid viscosity affects drag: Canola oil more viscous than water → slightly higher torque (performance: Specification.md PR-2; considerations: noted here; procedure: Procedure.md Step 2; cross-reference DEL-14.02)
- Temperature affects actuator performance: Cold temperature may slow pneumatic/hydraulic actuators (air/fluid viscosity increase) (construction: Datasheet.md Construction item 2 - Assumptions; performance: Specification.md PR-2; requirements: Specification.md FR-6; considerations: noted here; procedure: Procedure.md Step 2; cross-reference DEL-14.02)

**Safety vs. Surge Control:**
- **Conflict:** Safety may require fast valve closing (emergency shutdown); surge control requires slow valve closing (rationale: above item 2; conditions: Datasheet.md Valve Closing Time Requirements; considerations: noted here; trade-offs: below item 3; examples: below item 3; cross-reference DEL-14.06, DEL-14.07)
- **Resolution:** (construction: Datasheet.md Construction item 3 - Recommendations; requirements: Specification.md FR-5; performance: Specification.md PR-4; considerations: noted here; trade-offs: below items 2, 3; procedure: Procedure.md Step 4; examples: below item 2, item 3)
  - Option 1: Use slower closing time (prioritize surge control) if safety analysis permits (trade-offs: below item 3)
  - Option 2: Use fast closing time (prioritize safety) and add surge relief valve for surge mitigation (trade-offs: below items 2, 3; examples: below item 3; cross-reference PKG-16, DEL-14.06, DEL-14.07)
  - Option 3: Use two-speed or modulating actuator (slow closing for normal shutdown, fast closing for emergency with surge relief backup) (trade-offs: below item 2; cross-reference PKG-16)

**Vendor Data:**
- Valve manufacturers provide actuator stroke time data based on standard conditions (requirements: Specification.md FR-3; interface: Specification.md IR-3; performance: Specification.md PR-1; rationale: above item 4; considerations: noted here; procedure: Procedure.md Step 2; examples: below items 1, 2, 3; cross-reference PKG-16)
- Verify manufacturer data applies to project conditions (differential pressure, fluid, temperature) (performance: Specification.md PR-2; considerations: noted here and above - Operating Conditions; procedure: Procedure.md Step 2; examples: below)
- If project conditions deviate significantly, may need custom actuator sizing calculation (construction: Datasheet.md Construction item 2 - Assumptions; performance: Specification.md PR-2; requirements: Specification.md FR-6; considerations: noted here; procedure: Procedure.md Step 2; cross-reference PKG-16)

## Trade-offs

**1. Actuator Type Selection:**
- **Motor-operated (MOV):** Slow, controllable, low surge; higher cost, requires electrical power (construction: Datasheet.md Construction item 1 - Actuator type; requirements: Specification.md FR-3; rationale: above item 3; considerations: above - Valve Sizing and Selection; trade-offs: noted here; examples: below items 1, 2; cross-reference PKG-16)
- **Pneumatic:** Fast, simple, lower cost; higher surge risk, requires compressed air supply (construction: Datasheet.md Construction item 1 - Actuator type; requirements: Specification.md FR-3; rationale: above item 3; considerations: above - Safety vs. Surge Control; trade-offs: noted here; examples: below items 2, 3; cross-reference PKG-16)
- **Hydraulic:** Medium speed, good control; moderate cost, requires hydraulic power unit (construction: Datasheet.md Construction item 1 - Actuator type; rationale: above item 3; trade-offs: noted here; cross-reference PKG-16)
- **Guidance:** For surge-critical valves, prefer MOV (slow, controllable); for emergency shutdown where surge relief valve provided, pneumatic acceptable (requirements: Specification.md FR-4, FR-5; performance: Specification.md PR-3, PR-4; rationale: above item 3; considerations: above - Safety vs. Surge Control; trade-offs: noted here; procedure: Procedure.md Step 4; examples: below item 3; cross-reference DEL-14.06, DEL-14.07, PKG-16)

**2. Single-Speed vs. Two-Speed Actuator:**
- **Single-speed:** Simplest, one closing time for all scenarios; may not optimize for both normal and emergency conditions (requirements: Specification.md FR-3; rationale: above item 3; trade-offs: noted here; cross-reference PKG-16)
- **Two-speed or modulating:** More complex and expensive; allows slow closing for normal operations (surge control) and fast closing for emergencies (safety) (rationale: above item 3; considerations: above - Safety vs. Surge Control; trade-offs: noted here; cross-reference PKG-16)
- **Guidance:** Two-speed justified for critical applications where both surge control and fast emergency shutdown required; most valves use single-speed with appropriate closing time selected (requirements: Specification.md FR-4; trade-offs: noted here; procedure: Procedure.md Step 4)

**3. Valve Closing Time vs. Surge Relief Valve:**
- **Slow valve closing:** Reduces surge, avoids need for surge relief valve; but may not meet emergency shutdown time requirements (conditions: Datasheet.md Valve Closing Time Requirements - Minimum; requirements: Specification.md FR-2; performance: Specification.md PR-3; rationale: above item 2; considerations: above - Safety vs. Surge Control; trade-offs: noted here; examples: below items 1, 2; cross-reference DEL-14.06, DEL-14.07)
- **Fast valve closing + surge relief valve:** Meets emergency shutdown time, surge relief valve protects against surge; adds cost and complexity (relief valve, discharge piping, maintenance) (conditions: Datasheet.md Valve Closing Time Requirements - Maximum; requirements: Specification.md FR-2, FR-5; performance: Specification.md PR-4; rationale: above item 2; considerations: above - Safety vs. Surge Control; trade-offs: noted here; examples: below item 3; cross-reference DEL-14.06, DEL-14.07, PKG-16)
- **Guidance:** Optimize per transient analysis results; typically use slow closing where feasible, add surge relief where fast closing required for safety (requirements: Specification.md FR-4, FR-5; rationale: above item 2; considerations: above - Safety vs. Surge Control; trade-offs: noted here; procedure: Procedure.md Step 4; examples: below items 2, 3; cross-reference DEL-14.06, DEL-14.07)

## Examples

**1. Example 1: Compliant Valve**
- **Valve:** V-201 on marine loading line (8" ball valve) (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1; interface: Specification.md IR-4; procedure: Procedure.md Step 1; examples: noted here and Table below; cross-reference DEL-14.01, DEL-14.07, PKG-16)
- **Required closing time:** Minimum 10 seconds (from DEL-14.07 transient analysis to limit surge) (construction: Datasheet.md Construction item 1 - Required closing time; requirements: Specification.md FR-2; interface: Specification.md IR-2; rationale: above item 2; performance: Specification.md PR-3; procedure: Procedure.md Step 1; examples: noted here; cross-reference DEL-14.07)
- **Valve actuator:** Motor-operated, 15-second stroke time (from PKG-16 valve specification or vendor data) (construction: Datasheet.md Construction item 1 - Actuator type, Actual closing time; requirements: Specification.md FR-3; interface: Specification.md IR-3; rationale: above item 3; performance: Specification.md PR-1; considerations: above - Vendor Data; procedure: Procedure.md Step 2; examples: noted here; cross-reference PKG-16)
- **Verification:** 15 sec ≥ 10 sec minimum → **Compliant** (construction: Datasheet.md Construction item 1 - Compliance status; requirements: Specification.md FR-4; performance: Specification.md PR-3; quality: Specification.md QR-1; rationale: above item 4; procedure: Procedure.md Step 3; verification: Specification.md Verification - Compliance verification; examples: noted here)
- **Conclusion:** Valve V-201 meets surge mitigation requirement; no action required (requirements: Specification.md FR-4; quality: Specification.md QR-1; procedure: Procedure.md Step 3; examples: noted here)

**2. Example 2: Non-Compliant Valve**
- **Valve:** V-105 on railcar unloading line (10" butterfly valve) (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1; interface: Specification.md IR-4; procedure: Procedure.md Step 1; examples: noted here and Table below; cross-reference DEL-14.01, DEL-14.06, PKG-16)
- **Required closing time:** Minimum 20 seconds (from DEL-14.06 transient analysis to limit surge) (construction: Datasheet.md Construction item 1 - Required closing time; requirements: Specification.md FR-2; interface: Specification.md IR-1; performance: Specification.md PR-3; procedure: Procedure.md Step 1; examples: noted here; cross-reference DEL-14.06)
- **Valve actuator:** Pneumatic, 8-second stroke time (from preliminary valve selection) (construction: Datasheet.md Construction item 1 - Actuator type, Actual closing time; requirements: Specification.md FR-3; rationale: above item 3; trade-offs: above item 1; procedure: Procedure.md Step 2; examples: noted here; cross-reference PKG-16)
- **Verification:** 8 sec < 20 sec minimum → **Non-Compliant** (closes too fast, surge risk) (construction: Datasheet.md Construction items 1, 3; requirements: Specification.md FR-4, FR-5; quality: Specification.md QR-1, QR-2; procedure: Procedure.md Step 3; verification: Specification.md Verification - Compliance verification, Non-compliant valve resolution; examples: noted here)
- **Recommendation:** (construction: Datasheet.md Construction item 3 - Recommendations; requirements: Specification.md FR-5; performance: Specification.md PR-4; quality: Specification.md QR-2; rationale: above item 2; considerations: above - Safety vs. Surge Control; trade-offs: above items 1, 2, 3; procedure: Procedure.md Step 4; documentation: Specification.md Documentation - Compliance summary; examples: noted here)
  - Option 1: Change actuator to motor-operated (slower, meets 20-second requirement) (trade-offs: above item 1; examples: noted here; cross-reference PKG-16)
  - Option 2: Keep pneumatic actuator (fast for operational reasons) and install surge relief valve (mitigate surge from fast closure) (trade-offs: above items 2, 3; examples: noted here; cross-reference DEL-14.06, PKG-16)
  - Decision: Coordinate with operations and transient analysis engineer (procedure: Procedure.md Step 4; cross-reference DEL-14.06)

**3. Example 3: Emergency Shutdown Valve (ESD) with Surge Relief**
- **Valve:** V-301 marine loading arm ESD valve (12" ball valve) (conditions: Datasheet.md Critical Valves - Loading arm ESD; construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1; interface: Specification.md IR-4; procedure: Procedure.md Step 1; examples: noted here and Table below; cross-reference DEL-14.01, DEL-14.07, PKG-11, PKG-16)
- **Required closing time:** Maximum 5 seconds (emergency shutdown requirement for ship disconnect safety) (conditions: Datasheet.md Valve Closing Time Requirements - Maximum; construction: Datasheet.md Construction item 1 - Required closing time; requirements: Specification.md FR-2; interface: Specification.md IR-2; performance: Specification.md PR-4; rationale: above item 2; considerations: above - Safety vs. Surge Control; procedure: Procedure.md Step 1; examples: noted here; cross-reference DEL-14.07, PKG-11)
- **Valve actuator:** Pneumatic, 3-second stroke time (fast for safety) (construction: Datasheet.md Construction item 1 - Actuator type, Actual closing time; requirements: Specification.md FR-3; rationale: above item 3; trade-offs: above item 1; procedure: Procedure.md Step 2; examples: noted here; cross-reference PKG-16)
- **Surge concern:** 3-second closure generates high surge per DEL-14.07 analysis (rationale: above item 2; considerations: above - Safety vs. Surge Control; examples: noted here; cross-reference DEL-14.07)
- **Mitigation:** Surge relief valve installed at berth (per DEL-14.07 recommendation), sized to relieve surge pressure spike (construction: Datasheet.md Construction item 3 - Recommendations; requirements: Specification.md FR-5; trade-offs: above items 2, 3; examples: noted here; cross-reference DEL-14.07, PKG-16)
- **Verification:** 3 sec ≤ 5 sec maximum → **Compliant** for emergency shutdown time; surge mitigated by relief valve (not by closing time control) (construction: Datasheet.md Construction item 1 - Compliance status; requirements: Specification.md FR-4; performance: Specification.md PR-4; quality: Specification.md QR-1; procedure: Procedure.md Step 3; verification: Specification.md Verification - Compliance verification; examples: noted here)
- **Conclusion:** Valve V-301 meets safety requirement; surge mitigation provided by relief valve (separate equipment) (requirements: Specification.md FR-4; quality: Specification.md QR-1; examples: noted here; cross-reference DEL-14.07)

**Typical Verification Table Format:**

| Valve Tag | Location | Size/Type | Actuator Type | Required Time (sec) | Actual Time (sec) | Status |
|-----------|----------|-----------|---------------|---------------------|-------------------|--------|
| V-101 | Railcar Header | 6" Ball | MOV | ≥ 15 | 20 | Compliant |
| V-105 | Railcar Line | 10" Butterfly | Pneumatic | ≥ 20 | 8 | Non-Compliant (recom: change to MOV or add relief) |
| V-201 | Marine Loading | 8" Ball | MOV | ≥ 10 | 15 | Compliant |
| V-301 | Loading Arm ESD | 12" Ball | Pneumatic | ≤ 5 | 3 | Compliant (surge relief valve provided) |

(construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1, FR-2, FR-3, FR-4; quality: Specification.md QR-1; procedure: Procedure.md Step 3; documentation: Specification.md Documentation - Verification table; examples: noted here)
