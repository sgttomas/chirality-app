# Guidance: DEL-14.06 Transient Analysis Study Report – Railcar Unloading Line

## Purpose

Transient analysis (surge/water hammer) to ensure railcar unloading piping system designed to withstand pressure transients from pump and valve operations (scope: Specification.md Scope; attributes: Datasheet.md Report Type; rationale: noted below).

**Project context:** CSD canola oil transload facility, 1,000,000 MT/annum, Fraser Surrey Terminal BC (conditions: Datasheet.md System Description; cross-reference DEL-14.01, DEL-14.02).

## Principles

**1. Water Hammer / Surge Fundamentals:**
- **Phenomenon:** Rapid velocity change in piping causes pressure wave (surge) that propagates at acoustic wave speed (rationale: Specification.md Purpose; rationale: noted here; examples: below - Joukowsky equation)
- **Joukowsky equation:** ΔP = ρ × c × ΔV (rationale: noted here; standards: Specification.md Standards - Transient analysis references; examples: below)
  - ΔP = pressure change (surge pressure) (construction: Datasheet.md Construction item 2 - Maximum surge pressures; requirements: Specification.md FR-6; procedure: Procedure.md Step 2)
  - ρ = fluid density (kg/m³) (construction: Datasheet.md Construction item 1 - Fluid properties; requirements: Specification.md FR-3; considerations: below - Fluid Properties; procedure: Procedure.md Step 1)
  - c = acoustic wave speed in pipe (m/s) — typically ~1,000 m/s for liquid in steel pipe (rationale: noted here; rationale: item 4 below; considerations: below - System Characteristics)
  - ΔV = velocity change (m/s) (rationale: noted here; considerations: below - Operational Considerations)
- **Example:** Valve closes in 1 second, flow velocity changes from 2 m/s to 0 → ΔV = 2 m/s → ΔP ≈ 2,000 kPa (20 bar) surge pressure (rationale: noted here; conditions: Datasheet.md Transient Scenarios - Valve closing; trade-offs: below item 1; examples: noted here)

**2. Transient Scenarios:**
- **Pump startup:** Gradual flow increase → low surge risk (controlled acceleration) (conditions: Datasheet.md Transient Scenarios; requirements: Specification.md FR-5; procedure: Procedure.md Step 2; examples: below item 2)
- **Pump trip / power failure:** Sudden flow stoppage → negative surge (sub-atmospheric pressure, cavitation risk) and subsequent positive surge (water column reversal) (conditions: Datasheet.md Transient Scenarios; requirements: Specification.md FR-5, PR-3; rationale: noted here; considerations: below - Operational Considerations; procedure: Procedure.md Step 2; verification: Specification.md Verification - Results validation; examples: below item 2)
- **Valve closing:** Flow deceleration → positive surge (overpressure risk); faster closing = higher surge (conditions: Datasheet.md Transient Scenarios; requirements: Specification.md FR-5; rationale: noted here; trade-offs: below item 1; procedure: Procedure.md Step 2; examples: below item 2)
- **Emergency shutdown:** Fastest transient, highest surge pressures (conditions: Datasheet.md Transient Scenarios; requirements: Specification.md FR-5; rationale: noted here; considerations: below - Operational Considerations; trade-offs: below item 1; procedure: Procedure.md Step 2; examples: below item 2)

**3. Surge Mitigation Strategies:**
- **Surge relief valves:** Open when pressure exceeds set point, relieve excess pressure; effective for overpressure protection; require maintenance (construction: Datasheet.md Construction item 3 - Surge relief valves; requirements: Specification.md FR-9, FR-10; rationale: noted here; trade-offs: below item 2; procedure: Procedure.md Step 4; verification: Specification.md Verification - Mitigation verification; examples: below item 3; cross-reference PKG-16)
- **Slow valve closing:** Reduce ΔV by increasing closing time, directly reduces surge per Joukowsky equation; simple and reliable; may conflict with emergency shutdown time requirements (construction: Datasheet.md Construction item 3 - Valve closing time limits; requirements: Specification.md FR-9, FR-10; interface: Specification.md IR-6; rationale: noted here and item 1 above; trade-offs: below item 1; procedure: Procedure.md Step 4; verification: Specification.md Verification - Mitigation verification; examples: below item 3; cross-reference DEL-14.08, PKG-16)
- **Accumulators or surge tanks:** Absorb pressure wave energy through gas compression; very effective but expensive and complex (construction: Datasheet.md Construction item 3 - Accumulators; requirements: Specification.md FR-9; rationale: noted here; trade-offs: below item 3; procedure: Procedure.md Step 4; examples: below item 3)
- **Increased pipe design pressure:** Design piping for higher pressure (thicker walls); increases capital cost; may be necessary if other mitigation not feasible (construction: Datasheet.md Construction item 3 - Pipe design pressure increase; requirements: Specification.md FR-9; rationale: noted here; trade-offs: below item 4; procedure: Procedure.md Step 4; cross-reference DEL-14.01, DEL-14.03)

**4. Wave Propagation and Reflection:**
- Pressure wave travels at acoustic speed (~1,000 m/s in liquid) (rationale: item 1 above; considerations: below - System Characteristics)
- Wave reflects at boundaries (closed valve, pump, tank) (rationale: noted here; requirements: Specification.md FR-6; procedure: Procedure.md Step 2)
- Long pipelines → multiple reflections → complex pressure vs. time behavior (conditions: Datasheet.md Piping length; requirements: Specification.md FR-6; considerations: below - System Characteristics; procedure: Procedure.md Step 2; examples: below item 2)
- Transient analysis software models wave propagation and reflection (attributes: Datasheet.md Analysis Software; requirements: Specification.md FR-1, PR-4; standards: Specification.md Standards - Software; rationale: noted here; procedure: Procedure.md Step 1, Step 2; examples: below item 1)

## Considerations

**System Characteristics:**
- **Pipeline length:** Long pipelines (several hundred meters) more susceptible to surge due to larger mass of fluid decelerating (conditions: Datasheet.md Piping length; requirements: Specification.md FR-1, FR-2; rationale: above item 4; procedure: Procedure.md Step 1; cross-reference DEL-14.01)
- **Elevation profile:** High points susceptible to cavitation (negative surge); low points see highest positive surge (construction: Datasheet.md Construction item 1 - Piping geometry elevations; requirements: Specification.md FR-2, FR-6; performance: Specification.md PR-3; rationale: above item 4; procedure: Procedure.md Step 1; verification: Specification.md Verification - Results validation; examples: below item 2)
- **Pipe size and wall thickness:** Larger diameter = lower wave speed (more flexible pipe); thinner walls = more flexible = lower wave speed (requirements: Specification.md FR-2; rationale: above items 1, 4; procedure: Procedure.md Step 1; cross-reference DEL-14.01, DEL-14.03)

**Fluid Properties:**
- **Density (ρ):** CSD canola oil density ~920 kg/m³ (slightly less than water ~1,000 kg/m³) (construction: Datasheet.md Construction item 1 - Fluid properties; requirements: Specification.md FR-3; rationale: above item 1; quality: Specification.md QR-1; procedure: Procedure.md Step 1; examples: above item 1 - Joukowsky equation)
- **Bulk modulus (K):** Affects acoustic wave speed; canola oil bulk modulus lower than water → slightly lower wave speed (construction: Datasheet.md Construction item 1 - Fluid properties; requirements: Specification.md FR-3; rationale: above item 1; procedure: Procedure.md Step 1)
- **Viscosity:** Affects friction losses and damping of pressure waves; canola oil more viscous than water (construction: Datasheet.md Construction item 1 - Fluid properties; requirements: Specification.md FR-3; procedure: Procedure.md Step 1; cross-reference DEL-14.02, DEL-14.03)

**Operational Considerations:**
- **Valve closing time:** Critical parameter; faster closing = higher surge; emergency shutdown requirements may dictate minimum closing time (construction: Datasheet.md Construction item 3 - Valve closing time limits; conditions: Datasheet.md Transient Scenarios; requirements: Specification.md FR-9; interface: Specification.md IR-6; rationale: above item 3; trade-offs: below item 1; quality: Specification.md QR-2; procedure: Procedure.md Step 2, Step 4; verification: Specification.md Verification - Sensitivity analysis; cross-reference DEL-14.08)
- **Pump characteristics:** Pump inertia affects coastdown time after trip; higher inertia = slower deceleration = lower surge (construction: Datasheet.md Construction item 1 - Boundary conditions; requirements: Specification.md FR-4; interface: Specification.md IR-3; rationale: above; quality: Specification.md QR-2; procedure: Procedure.md Step 1; verification: Specification.md Verification - Sensitivity analysis; cross-reference PKG-15)
- **Multiple pumps:** Simultaneous trip of multiple pumps → higher surge than single pump trip (conditions: Datasheet.md Transient Scenarios; requirements: Specification.md FR-5; rationale: noted here; procedure: Procedure.md Step 2; cross-reference PKG-15)
- **Tank levels:** Low tank level → less back pressure → higher surge potential (construction: Datasheet.md Construction item 1 - Boundary conditions; requirements: Specification.md FR-4; interface: Specification.md IR-4; rationale: noted here; procedure: Procedure.md Step 1; cross-reference PKG-13)

## Trade-offs

**1. Valve Closing Time:**
- **Fast closing (e.g., 2-5 seconds):** Quick shutdown (safety benefit), high surge risk (conditions: Datasheet.md Transient Scenarios - Emergency rate; requirements: Specification.md FR-5, FR-9; rationale: above items 1, 2, 3; procedure: Procedure.md Step 2, Step 4; examples: below item 2)
- **Slow closing (e.g., 10-20 seconds):** Low surge, longer shutdown time (safety concern in emergencies) (construction: Datasheet.md Construction item 3 - Valve closing time limits; requirements: Specification.md FR-9; interface: Specification.md IR-6; rationale: above item 3; procedure: Procedure.md Step 4; verification: Specification.md Verification - Mitigation verification; cross-reference DEL-14.08)
- **Guidance:** Balance surge control vs. emergency shutdown requirements; typical minimum closing time 8-12 seconds for large valves (requirements: Specification.md FR-9, FR-10; rationale: above item 3; procedure: Procedure.md Step 4; cross-reference DEL-14.08, PKG-16)

**2. Surge Relief Valves:**
- **With surge relief:** Effective overpressure protection, adds equipment cost and maintenance (construction: Datasheet.md Construction item 3 - Surge relief valves; requirements: Specification.md FR-9, FR-10; rationale: above item 3; procedure: Procedure.md Step 4; examples: below item 3; cross-reference PKG-16)
- **Without surge relief:** Lower cost, but requires slower valve closing or higher pipe design pressure (requirements: Specification.md FR-9; rationale: above item 3; trade-offs: item 1 above, item 4 below; procedure: Procedure.md Step 4)
- **Guidance:** Surge relief valves recommended for critical systems with fast-acting emergency shutdown valves (requirements: Specification.md FR-9; rationale: above item 3; procedure: Procedure.md Step 4; cross-reference PKG-16)

**3. Accumulators vs. Other Mitigation:**
- **Accumulators:** Very effective, but expensive and complex (construction: Datasheet.md Construction item 3 - Accumulators; requirements: Specification.md FR-9; rationale: above item 3; procedure: Procedure.md Step 4)
- **Surge relief valves or slow valve closing:** Simpler and cheaper, but may be less effective for some scenarios (rationale: above item 3; trade-offs: items 1, 2 above; procedure: Procedure.md Step 4)
- **Guidance:** Use simpler mitigation (valve timing, relief valves) where possible; accumulators for cases where simpler methods insufficient (requirements: Specification.md FR-9; rationale: above item 3; procedure: Procedure.md Step 4)

**4. Pipe Design Pressure Increase:**
- **Higher design pressure:** Accommodates surge without mitigation devices; increases pipe cost (thicker walls, higher flange class) (construction: Datasheet.md Construction item 3 - Pipe design pressure increase; requirements: Specification.md FR-9; rationale: above item 3; procedure: Procedure.md Step 4; cross-reference DEL-14.01, DEL-14.03)
- **Lower design pressure with mitigation:** Lower pipe cost, but adds mitigation equipment cost/complexity (requirements: Specification.md FR-9; rationale: above item 3; trade-offs: items 1, 2, 3 above; procedure: Procedure.md Step 4)
- **Guidance:** Lifecycle cost optimization; typically more economical to add mitigation than significantly increase pipe design pressure (source: OBJ-9; requirements: Specification.md FR-9; rationale: above item 3; procedure: Procedure.md Step 4)

## Examples

**1. Transient model example:**
- Software: AFT Impulse or WANDA (attributes: Datasheet.md Analysis Software; construction: Datasheet.md Construction item 1 - Software input file; requirements: Specification.md PR-4; standards: Specification.md Standards - Software; rationale: above item 4; procedure: Procedure.md Prerequisites, Step 1)
- Piping geometry: 500m pipeline, DN 300 (12"), elevations from +2m to +8m (construction: Datasheet.md Construction item 1 - Piping geometry; requirements: Specification.md FR-2; interface: Specification.md IR-1; quality: Specification.md QR-1; procedure: Procedure.md Step 1; verification: Specification.md Verification - Model verification; cross-reference DEL-14.01)
- Fluid: CSD canola oil (ρ=920 kg/m³, K=1,500 MPa, μ varies with temperature) (construction: Datasheet.md Construction item 1 - Fluid properties; requirements: Specification.md FR-3; rationale: above item 1; considerations: above - Fluid Properties; quality: Specification.md QR-1; procedure: Procedure.md Step 1; verification: Specification.md Verification - Model verification)
- Boundary conditions: Centrifugal pump (100 m head, 200 m³/h), storage tank (5m level), motor-operated valves (10 second closing time) (construction: Datasheet.md Construction item 1 - Boundary conditions; requirements: Specification.md FR-4; interface: Specification.md IR-3, IR-4, IR-5; quality: Specification.md QR-1; procedure: Procedure.md Step 1; verification: Specification.md Verification - Model verification; cross-reference PKG-13, PKG-15, PKG-16)

**2. Surge results example:**
- Scenario: Emergency valve closure (valve closes in 5 seconds) (conditions: Datasheet.md Transient Scenarios - Emergency rate; requirements: Specification.md FR-5; rationale: above item 2; procedure: Procedure.md Step 2; examples: noted here)
- Maximum surge pressure: 1,800 kPa at valve location (construction: Datasheet.md Construction item 2 - Maximum surge pressures; requirements: Specification.md FR-6, FR-7; performance: Specification.md PR-1; procedure: Procedure.md Step 2, Step 3; verification: Specification.md Verification - Results validation; examples: noted here)
- Design pressure: 1,550 kPa (conditions: Datasheet.md Design Criteria; performance: Specification.md PR-1; interface: Specification.md IR-2; verification: Specification.md Verification - Acceptance; cross-reference DEL-14.03)
- **Conclusion:** Surge pressure (1,800 kPa) exceeds design pressure (1,550 kPa) → mitigation required (requirements: Specification.md FR-8, FR-9; performance: Specification.md PR-1; procedure: Procedure.md Step 3, Step 4; verification: Specification.md Verification - Acceptance)

**3. Mitigation recommendation example:**
- **Option 1:** Install surge relief valve at valve location, set pressure 1,400 kPa, capacity **TBD** (construction: Datasheet.md Construction item 3 - Surge relief valves; requirements: Specification.md FR-9, FR-10; rationale: above item 3; trade-offs: above item 2; procedure: Procedure.md Step 4; verification: Specification.md Verification - Mitigation verification; examples: noted here; cross-reference PKG-16)
- **Option 2:** Increase valve closing time to minimum 8 seconds → reduces surge to 1,400 kPa (within design pressure) (construction: Datasheet.md Construction item 3 - Valve closing time limits; requirements: Specification.md FR-9, FR-10; interface: Specification.md IR-6; rationale: above item 3; trade-offs: above item 1; procedure: Procedure.md Step 4; verification: Specification.md Verification - Mitigation verification; examples: noted here; cross-reference DEL-14.08, PKG-16)
- **Recommendation:** Option 2 (increase valve closing time) preferred for reliability and lifecycle cost (source: OBJ-9; requirements: Specification.md FR-9; rationale: above item 3; trade-offs: above items 1, 2, 4; procedure: Procedure.md Step 4; examples: noted here)
