# Guidance: DEL-14.08 Valve Closing Time Verification Summary

## Purpose

Verify valve closing times comply with surge mitigation requirements from transient analyses (DEL-14.06 Railcar Unloading, DEL-14.07 Marine Loading).

**Project context:** CSD canola oil transload facility, 1,000,000 MT/annum, Fraser Surrey Terminal BC.

## Principles

**1. Valve Closing Time Defined:**
- **Closing time:** Time for valve to travel from fully open (100%) to fully closed (0%)
- Measured in seconds
- Depends on valve type, size, actuator type, and actuator power

**2. Surge Mitigation and Valve Closing Time:**
- **Joukowsky equation:** ΔP = ρ × c × ΔV
  - Surge pressure (ΔP) proportional to velocity change (ΔV)
  - Slower valve closing → smaller ΔV/Δt (rate of velocity change) → lower surge pressure
- **Transient analyses (DEL-14.06, DEL-14.07) specify:**
  - **Minimum closing time:** To limit surge pressure below design pressure (e.g., "valve must close in minimum 10 seconds to limit surge to acceptable level")
  - **Maximum closing time:** (Less common) For emergency shutdown requirements (e.g., "valve must close within 30 seconds for emergency isolation")

**3. Valve Actuator Types:**
- **Motor-operated valve (MOV):** Electric motor drives valve stem; closing time typically 10-60 seconds (slow, controllable); good for surge control
- **Pneumatic actuator:** Compressed air drives valve; closing time typically 2-10 seconds (fast); higher surge risk but good for emergency shutdown
- **Hydraulic actuator:** Hydraulic pressure drives valve; closing time typically 5-20 seconds (medium speed)
- **Manual valve:** Hand-operated; closing time variable (not typically used for surge-critical applications)

**4. Verification Approach:**
- **Extract requirements:** From DEL-14.06 and DEL-14.07 transient analysis reports (e.g., "Valve V-101 must close in minimum 15 seconds")
- **Obtain actuator data:** From PKG-16 valve specifications or vendor data (e.g., "Valve V-101 has motor-operated actuator with 20-second stroke time")
- **Verify compliance:** Compare actuator closing time vs. required closing time (20 sec ≥ 15 sec minimum → compliant)
- **Document:** Table showing valve tag, required time, actual time, compliance status

## Considerations

**Valve Sizing and Selection:**
- Valve size affects closing time: Larger valves require more torque → larger actuator or longer closing time
- Valve type affects torque requirement: Ball valves (high torque near closed position), butterfly valves (lower torque), gate valves (moderate torque throughout stroke)
- Actuator sizing by valve manufacturer or engineer: Considers valve size, type, differential pressure, friction, safety factors

**Operating Conditions:**
- Differential pressure across valve affects torque: Higher ΔP → higher torque → may require larger actuator or longer closing time
- Fluid viscosity affects drag: Canola oil more viscous than water → slightly higher torque
- Temperature affects actuator performance: Cold temperature may slow pneumatic/hydraulic actuators (air/fluid viscosity increase)

**Safety vs. Surge Control:**
- **Conflict:** Safety may require fast valve closing (emergency shutdown); surge control requires slow valve closing
- **Resolution:**
  - Option 1: Use slower closing time (prioritize surge control) if safety analysis permits
  - Option 2: Use fast closing time (prioritize safety) and add surge relief valve for surge mitigation
  - Option 3: Use two-speed or modulating actuator (slow closing for normal shutdown, fast closing for emergency with surge relief backup)

**Vendor Data:**
- Valve manufacturers provide actuator stroke time data based on standard conditions
- Verify manufacturer data applies to project conditions (differential pressure, fluid, temperature)
- If project conditions deviate significantly, may need custom actuator sizing calculation

## Trade-offs

**1. Actuator Type Selection:**
- **Motor-operated (MOV):** Slow, controllable, low surge; higher cost, requires electrical power
- **Pneumatic:** Fast, simple, lower cost; higher surge risk, requires compressed air supply
- **Hydraulic:** Medium speed, good control; moderate cost, requires hydraulic power unit
- **Guidance:** For surge-critical valves, prefer MOV (slow, controllable); for emergency shutdown where surge relief valve provided, pneumatic acceptable

**2. Single-Speed vs. Two-Speed Actuator:**
- **Single-speed:** Simplest, one closing time for all scenarios; may not optimize for both normal and emergency conditions
- **Two-speed or modulating:** More complex and expensive; allows slow closing for normal operations (surge control) and fast closing for emergencies (safety)
- **Guidance:** Two-speed justified for critical applications where both surge control and fast emergency shutdown required; most valves use single-speed with appropriate closing time selected

**3. Valve Closing Time vs. Surge Relief Valve:**
- **Slow valve closing:** Reduces surge, avoids need for surge relief valve; but may not meet emergency shutdown time requirements
- **Fast valve closing + surge relief valve:** Meets emergency shutdown time, surge relief valve protects against surge; adds cost and complexity (relief valve, discharge piping, maintenance)
- **Guidance:** Optimize per transient analysis results; typically use slow closing where feasible, add surge relief where fast closing required for safety

## Examples

**Example 1: Compliant Valve**
- **Valve:** V-201 on marine loading line (8" ball valve)
- **Required closing time:** Minimum 10 seconds (from DEL-14.07 transient analysis to limit surge)
- **Valve actuator:** Motor-operated, 15-second stroke time (from PKG-16 valve specification or vendor data)
- **Verification:** 15 sec ≥ 10 sec minimum → **Compliant**
- **Conclusion:** Valve V-201 meets surge mitigation requirement; no action required

**Example 2: Non-Compliant Valve**
- **Valve:** V-105 on railcar unloading line (10" butterfly valve)
- **Required closing time:** Minimum 20 seconds (from DEL-14.06 transient analysis to limit surge)
- **Valve actuator:** Pneumatic, 8-second stroke time (from preliminary valve selection)
- **Verification:** 8 sec < 20 sec minimum → **Non-Compliant** (closes too fast, surge risk)
- **Recommendation:**
  - Option 1: Change actuator to motor-operated (slower, meets 20-second requirement)
  - Option 2: Keep pneumatic actuator (fast for operational reasons) and install surge relief valve (mitigate surge from fast closure)
  - Decision: Coordinate with operations and transient analysis engineer

**Example 3: Emergency Shutdown Valve (ESD) with Surge Relief**
- **Valve:** V-301 marine loading arm ESD valve (12" ball valve)
- **Required closing time:** Maximum 5 seconds (emergency shutdown requirement for ship disconnect safety)
- **Valve actuator:** Pneumatic, 3-second stroke time (fast for safety)
- **Surge concern:** 3-second closure generates high surge per DEL-14.07 analysis
- **Mitigation:** Surge relief valve installed at berth (per DEL-14.07 recommendation), sized to relieve surge pressure spike
- **Verification:** 3 sec ≤ 5 sec maximum → **Compliant** for emergency shutdown time; surge mitigated by relief valve (not by closing time control)
- **Conclusion:** Valve V-301 meets safety requirement; surge mitigation provided by relief valve (separate equipment)

**Typical Verification Table Format:**

| Valve Tag | Location | Size/Type | Actuator Type | Required Time (sec) | Actual Time (sec) | Status |
|-----------|----------|-----------|---------------|---------------------|-------------------|--------|
| V-101 | Railcar Header | 6" Ball | MOV | ≥ 15 | 20 | Compliant |
| V-105 | Railcar Line | 10" Butterfly | Pneumatic | ≥ 20 | 8 | Non-Compliant (recom: change to MOV or add relief) |
| V-201 | Marine Loading | 8" Ball | MOV | ≥ 10 | 15 | Compliant |
| V-301 | Loading Arm ESD | 12" Ball | Pneumatic | ≤ 5 | 3 | Compliant (surge relief valve provided) |
