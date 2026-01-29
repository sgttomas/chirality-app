# Guidance: DEL-16.03 Valve Design Calculations

## Purpose

This guidance document supports the development of **Valve Design Calculations** for **PKG-16 Valves & Specialty Equipment**.

**Deliverable Purpose:** Provides the engineering basis and sizing/verification calculations for valves per ER requirements for the Canola Oil Transload Facility.

**Source:** `_CONTEXT.md`

**Deliverable Classification:**
- **Type:** Calculation
- **Discipline:** Mechanical
- **Responsible Party:** D&B Contractor

**Project Context:**
This deliverable supports **OBJ-1: Safe & Reliable Operation** by providing technically sound valve sizing calculations that ensure valves perform their intended functions safely and reliably throughout the facility design life.

**Source:** Decomposition document Section 6 (Objective-to-Deliverable Mapping), OBJ-1 includes PKG-16 (DEL-16.01–DEL-16.05)

## Principles

**Engineering Rationale:**

**1. Control Valve Sizing Philosophy**

Control valve sizing is a balance between control performance and cost (see also Specification.md — Functional Requirements for calculation methodology):

**Governing Equations (ISA-75.01):**

For liquid flow (non-choked conditions):
- **Imperial units:** Cv = Q × sqrt(SG / ΔP)
  - Where: Cv = flow coefficient, Q = flow rate (gpm), SG = specific gravity, ΔP = pressure drop (psi)
- **SI units:** Kv = Q × sqrt(ρ / (ΔP × 1000))
  - Where: Kv = flow coefficient, Q = flow rate (m³/h), ρ = density (kg/m³), ΔP = pressure drop (bar)
- **Conversion:** Kv = Cv / 1.156

**Key Principles:**
- **Pressure Drop Allocation:** Control valve should consume significant portion of system pressure drop (typically 25–50%) to provide good control authority and minimize sensitivity to system changes (see Trade-offs section for pressure drop allocation decisions)
- **Rangeability (Turndown Ratio):** Select valve size and trim to provide adequate rangeability (typical 50:1 for control valves); avoid oversizing which reduces turndown
- **Cavitation Avoidance:** Cavitation damages valve trim and creates noise/vibration; check cavitation index σ = (P1 - Pv) / (P1 - P2) and compare to valve-specific σc (see Datasheet.md — Construction for cavitation check methodology)
- **Noise Mitigation:** High-velocity flow through small valve trim creates noise; predict noise level per IEC 60534-8-3 and apply noise mitigation if >85 dBA at 1 meter (anti-cavitation trim, noise attenuation trim, downstream diffusers)

**Source:** ISA-75.01 control valve sizing principles; industry best practices for control valve selection

**Viscosity Effects on Control Valve Sizing (Critical for Canola Oil):**

Canola oil viscosity varies significantly with temperature, affecting valve sizing:
- **High Viscosity (Low Temperature):** Viscous fluids have low Reynolds number; require viscosity correction factor Fv per ISA-75.01
- **Reynolds Number:** Re = (N1 × Fd² × Q × SG) / (ν × Cv) where ν = kinematic viscosity (cSt)
- **Viscosity Correction:** For Re < 10,000, apply Fv correction factor; Cv_required = Cv_calculated / Fv (increases required Cv)
- **Design Point Selection:** Size valve at lowest expected operating temperature (highest viscosity) to ensure adequate capacity

**Practical Implication for Canola Oil Facility:**
- Product heated to 40–60°C for pumping and loading operations (reduces viscosity)
- If product temperature drops below 20°C, viscosity increases significantly; valve may be undersized
- **Recommendation:** Verify valve sizing at minimum expected product temperature; consider heat tracing for critical lines (see Datasheet.md — Conditions for product temperature ranges)

**Source:** ISA-75.01 viscosity correction methodology; canola oil viscosity-temperature characteristics from industry data

**2. Relief Valve Sizing Philosophy**

Relief valve sizing is governed by code requirements (ASME, API, CSA B51) with goal of protecting equipment from overpressure while minimizing relief valve size and cost (see also Specification.md — Functional Requirements for calculation methodology):

**Governing Relief Scenarios (per API 521):**

**Thermal Expansion (Most Common for Liquid Systems):**
- Scenario: Liquid trapped between closed isolation valves; temperature increase causes volumetric expansion; pressure rises rapidly
- Relief Load Calculation: Q = β × V × (T2 - T1) / t where β = volumetric expansion coefficient, V = trapped volume, T = temperature, t = time
- Mitigation: Provide thermal relief valve or eliminate blocked-in condition (operator procedures, interlocks)
- **Typical for Canola Oil Facility:** Product lines with isolation valves on both ends; solar heating or ambient temperature rise causes expansion

**External Fire (Critical for Storage Tanks):**
- Scenario: External fire heats vessel contents; liquid vaporizes; vapor generation rate determines relief capacity
- Relief Load Calculation: Q = C × F × A^0.82 where C = constant, F = environmental factor, A = wetted surface area
- Code Basis: API 521 fire case; ASME Section VIII requires fire case for vessels containing flammable/combustible liquids
- **Typical for Canola Oil Facility:** Storage tanks (DEL-13.01, DEL-13.02) require fire-case relief valves

**Blocked Discharge (Pumps and Compressors):**
- Scenario: Pump discharge valve closed; pump dead-heads; pressure rises to pump shutoff head
- Relief Load Calculation: Relief valve sized for pump minimum flow at shutoff head
- Mitigation: Pump minimum flow recirculation system; thermal relief valve on pump discharge
- **Typical for Canola Oil Facility:** Transfer pumps (PKG-12) require blocked discharge protection

**Control Valve Failure (Full-Open Case):**
- Scenario: Control valve fails full-open; downstream pressure rises due to excess flow
- Relief Load Calculation: Process simulation determines downstream pressure at maximum flow
- Mitigation: High-pressure shutdown interlock; downstream pressure relief valve
- **Not Typical for Canola Oil Facility:** Low-pressure system; control valve failure unlikely to cause overpressure

**Source:** API 521 relief scenarios; typical scenarios for liquid storage and transfer facilities

**Set Pressure Selection (per ASME Section VIII and CSA B51):**

**Code Requirements:**
- Set pressure ≤ MAWP of protected equipment (ASME Section VIII UG-125)
- For single relief valve: Set pressure typically 0.95–1.0× MAWP (to maximize operating pressure range)
- For multiple relief valves: First valve at MAWP; additional valves at higher set pressures (staggered setting)
- Accumulated pressure during relief: ≤ 1.1× MAWP (10% overpressure) for operating case; ≤ 1.21× MAWP (21% overpressure) for fire case

**Set Pressure Tolerance (per API 526):**
- Pressures ≤ 70 psig: ±3 psi
- Pressures > 70 psig: ±2% of set pressure
- Cold differential test pressure (CDTP) adjusted for temperature effects

**Practical Considerations:**
- Set pressure selection affects relief valve size; lower set pressure = smaller relief capacity = smaller valve
- Trade-off: Lower set pressure allows smaller relief valve but reduces usable pressure range for operation
- **Recommendation:** Set pressure = 0.95× MAWP for single relief valve (see Trade-offs section for set pressure optimization)

**Source:** ASME Section VIII UG-125 through UG-136; API 526 set pressure tolerance; CSA B51 Section 4.11

**3. Actuator Sizing Philosophy**

Actuator sizing ensures valve can be opened/closed under all operating conditions with adequate safety margin (see also Specification.md — Functional Requirements for calculation methodology):

**Torque Calculation for Quarter-Turn Valves (Ball, Butterfly):**

**Breakaway Torque (Maximum):**
- Torque required to overcome static friction and unseat valve at maximum differential pressure
- T_breakaway = T_bearing + T_seal + T_unseating
- Typically highest torque (may be 2–3× running torque)

**Running Torque:**
- Torque required to move valve during operation
- Lower than breakaway torque due to dynamic (lower) friction coefficient

**Seating Torque:**
- Torque required to achieve tight shutoff per leakage class
- May be specified by valve manufacturer (e.g., "minimum closing torque to achieve Class IV shutoff")

**Actuator Sizing:**
- Select actuator with output torque ≥ max(T_breakaway, T_seating) × safety factor
- Safety factor: 1.5 typical for pneumatic actuators; 1.25 for electric actuators
- **Source:** ISA-75.25 actuator sizing methodology; manufacturer recommendations

**Fail-Safe Mode Selection (Critical for Safety):**

**Fail-Closed (FC):**
- Spring-return actuator closes valve on loss of air/power
- **Use for:** Isolation valves on hazardous services; ESD valves; valves where closed position is safe state
- **Example (Canola Oil Facility):** Marine loading arm isolation valve (close on emergency shutdown to prevent spill)

**Fail-Open (FO):**
- Spring-return actuator opens valve on loss of air/power
- **Use for:** Valves where open position is safe state; valves providing cooling or pressure relief
- **Example:** Pump minimum flow recirculation valve (open on power loss to prevent pump damage)

**Fail-As-Is (FL) or Fail-Last Position (FLP):**
- Double-acting actuator or electric actuator; valve remains in last position on loss of air/power
- **Use for:** Non-critical isolation valves; valves where neither open nor closed is clearly safer
- **Example:** Manual isolation valve with electric actuator for remote operation

**Decision Basis:** Fail-safe mode determined by HAZOP (DEL-27.02) or Layers of Protection Analysis (LOPA); failure mode should drive system to safe state (see Procedure.md — Step 1 for fail-safe mode input source)

**Source:** ISA-75 actuator standards; typical fail-safe mode selection principles

**Applicable Standards Context:**

**ISA-75 Series (Control Valves):**
- **ISA-75.01:** Provides universally accepted equations for control valve sizing; basis for vendor sizing software
- **ISA-75.11:** Defines inherent flow characteristics (equal percentage, linear, quick-opening); selection depends on control objective and process gain
- **IEC 60534-8-3:** Noise prediction method; important for high-velocity gas/steam service (less critical for liquid canola oil service)
- **IEC 60534-8-4:** Cavitation prediction method; critical for liquid services with high pressure drop

**API 520/521 (Relief Valves):**
- **API 520:** Part I (Sizing and Selection) provides equations for liquid, vapor, and two-phase relief; Part II (Installation) provides piping and installation requirements
- **API 521:** Provides guidance on relief scenarios (fire, thermal expansion, etc.); widely used for identifying credible overpressure events
- **Note:** API 520/521 are design guidelines, not mandatory codes; ASME Section VIII and CSA B51 are mandatory codes in Canada

**CSA B51 (Canadian Code):**
- CSA B51 is mandatory in BC for pressure vessels and pressure piping
- Relief valve requirements in Section 4.11; generally consistent with ASME Section VIII but with some Canadian-specific provisions
- Relief valves protecting registered pressure vessels must be registered with BC Safety Authority (Technical Safety BC)
- **Source:** CSA B51 applicability in BC jurisdiction; Technical Safety BC regulatory requirements

**Product-Specific Considerations:**

**CSD Canola Oil Properties:**
- **Viscosity:** Major factor for control valve sizing; high viscosity at low temperature reduces flow coefficient (requires larger valve)
- **Density:** ~920 kg/m³ at 15°C; relatively constant with temperature (±2–3%)
- **Vapor Pressure:** Very low (<0.1 kPa at 100°C); cavitation not typically a concern for canola oil service
- **Flammability:** Combustible liquid (flash point ~316°C); not flammable under normal operating conditions but fire case still required for storage tanks per ASME Section VIII and NFPA 30
- **Food-Grade Requirements:** Valve materials must be food-grade (stainless steel preferred); valve design should minimize dead-legs and provide drainability

**Source:** Canola oil thermophysical properties from industry data; food-grade requirements for edible oil handling

## Considerations

**Factors to consider during development:**

**1. Project-Specific Factors**

- **Package Scope:** PKG-16 Valves & Specialty Equipment — includes control valves, isolation valves, relief valves, strainers, specialty items
- **Facility Type:** Transload facility (railcar unloading, storage, marine loading) — different valve service requirements and sizing criteria
- **Throughput:** 1,000,000 MT/annum capacity — valve sizing must support design flow rates (approximately 2,740 MT/day or 114 MT/h average; peak rates TBD)
- **Location:** Fraser Surrey Terminal, Surrey, BC — marine/coastal environment; CSA B51 and Technical Safety BC jurisdiction

**Source:** Decomposition document Sections 1.1 and 5 (PKG-16 scope)

**2. Deliverable Type Considerations (Calculation)**

- **Calculation Format:** Structured format with inputs, assumptions, calculations, results, conclusions (see Specification.md — Functional Requirements for calculation structure)
- **Calculation Software:** Excel spreadsheets, MathCAD, or vendor software (Fisher, Emerson, etc.) — software validation required (see Specification.md — Quality Requirements for software validation)
- **Traceability:** All input data must be traceable to source documents (P&IDs, process data, vendor catalogs)
- **Reproducibility:** Calculations must be reproducible by independent checker (sufficient detail and intermediate steps)

**3. Coordination Requirements**

- **Upstream Deliverables (provide inputs to valve calculations):**
  - Process design (P&IDs, PFDs, process datasheets) — flow rates, pressures, temperatures
  - Piping design (DEL-14.01 line list) — line sizes, pressure classes, piping layout
  - HAZOP study (DEL-27.02) — relief valve scenarios, fail-safe mode recommendations
  - Control philosophy — control valve turndown requirements, fail-safe modes, stroking times
- **Downstream Deliverables (use valve calculation results):**
  - Valve datasheets (DEL-16.04) — populated with calculated Cv, set pressure, actuator size
  - Valve drawings (DEL-16.01) — valve arrangement based on selected valve sizes
  - Valve specifications (DEL-16.02) — specification requirements informed by sizing calculations
- **Parallel Deliverables (iterative coordination):**
  - Piping stress analysis — valve pressure drops affect piping flexibility
  - Pump sizing — valve pressure drops affect pump head requirements
  - Instrument sizing — flow meter sizing may affect control valve sizing

**Source:** Dependencies inferred from package structure; NOT_TRACKED per `_DEPENDENCIES.md`

**4. Regulatory and Compliance**

- **Employer's Requirements:** **TBD** — Review Volume 2 Parts 1–3 for valve sizing criteria and acceptance requirements
- **CSA B51 Compliance:** Relief valves protecting pressure vessels or piping systems must comply with CSA B51 Section 4.11
- **Technical Safety BC Registration:** Relief valves protecting registered pressure vessels may require registration — **TBD**
- **NFPA 30 (Flammable and Combustible Liquids Code):** Storage tank relief valves must comply with NFPA 30 fire case requirements (canola oil is combustible liquid per NFPA 30 classification)

**Source:** Regulatory requirements for relief valves in BC; NFPA 30 applicability for combustible liquid storage

**5. Design Conservatism and Uncertainty**

- **Design Margins:** Apply appropriate margins to account for uncertainty in input data (see Specification.md — Performance Requirements for design margin criteria)
- **Sensitivity Analysis:** For critical valves, assess sensitivity to input data uncertainty (±20% flow rate variation, ±10% pressure variation)
- **TBD Items:** Clearly flag input data marked as "estimated" or "TBD"; provide recommendations for confirming assumptions (field measurements, vendor data, commissioning verification)
- **Future Expansion:** Consider future capacity expansion when sizing valves (or provision for adding valves in future); trade-off between upfront cost and future flexibility

**6. Operability and Maintainability**

- **Control Valve Operability:** Control valve turndown ratio must support expected operating range (normal, minimum, maximum flow)
- **Relief Valve Accessibility:** Relief valve set pressure testing requires periodic testing; consider accessibility for removing and reinstalling relief valves
- **Actuator Maintenance:** Pneumatic actuators require compressed air system; electric actuators require power supply and MCC; consider O&M requirements
- **Spare Parts:** Large or long-lead-time valves may require spare parts inventory; consider in valve selection

**Source:** Operability and maintainability considerations typical for process facilities

## Trade-offs

**Competing concerns to evaluate:**

**1. Control Valve Pressure Drop Allocation**

| Factor | Low Pressure Drop (10–20% of system ΔP) | High Pressure Drop (40–60% of system ΔP) |
|--------|----------------------------------------|------------------------------------------|
| **Control Authority** | Poor; control valve has little influence on flow | Good; control valve dominates flow resistance |
| **Valve Size** | Larger valve (higher Cv required) | Smaller valve (lower Cv required) |
| **Valve Cost** | Higher (larger valve, actuator) | Lower (smaller valve, actuator) |
| **Pump Energy** | Lower pump head required (energy savings) | Higher pump head required (energy cost) |
| **System Sensitivity** | High sensitivity to piping changes, fouling | Low sensitivity; robust control |

**Guidance:** Allocate 25–50% of available system pressure drop to control valve for good control authority. For canola oil (high viscosity), err toward higher pressure drop allocation to improve turndown and control stability.

**Source:** ISA-75 control valve sizing guidance; industry best practices

**2. Relief Valve Set Pressure Selection**

| Set Pressure | Advantages | Disadvantages |
|--------------|------------|---------------|
| **Low (0.90–0.95× MAWP)** | Smaller relief capacity → smaller valve → lower cost | Less margin for pressure control; more frequent lifting |
| **Medium (0.95–1.0× MAWP)** | Balanced approach; adequate margin | Standard selection for most applications |
| **High (1.0× MAWP)** | Maximum operating pressure range | Larger relief capacity → larger valve → higher cost |

**Guidance:** Set pressure = 0.95–1.0× MAWP for single relief valve (typical). If multiple relief valves, stagger set pressures (first at MAWP, second at 1.05× MAWP, etc.). Coordinate set pressure with pressure vessel/piping MAWP selection to optimize overall system cost.

**Source:** ASME Section VIII relief valve sizing guidance; typical EPC practices

**3. Actuator Type Selection**

| Actuator Type | Advantages | Disadvantages | Typical Applications |
|---------------|------------|---------------|---------------------|
| **Pneumatic (Spring-Return)** | Fast-acting, fail-safe capability, simple, low cost | Requires compressed air system; limited torque | Control valves, ESD valves (fail-safe required) |
| **Pneumatic (Double-Acting)** | Higher torque than spring-return, fast-acting | No fail-safe (stays in last position on air loss) | Large isolation valves (fail-safe not required) |
| **Electric (Motor Operator)** | Precise positioning, high torque, no air supply needed | Slower than pneumatic, higher cost, no inherent fail-safe | Large gate valves, infrequent operation |
| **Manual (Handwheel/Gearbox)** | Simple, reliable, no utilities required | Requires operator presence, slow operation | Infrequently operated isolation valves |

**Guidance:** Use pneumatic spring-return actuators for control valves and ESD valves requiring fail-safe operation. Use electric actuators for large isolation valves where fail-safe not required and high torque needed. Use manual valves for infrequent isolation (maintenance, seasonal).

**Source:** Typical actuator selection trade-offs; specific decisions TBD pending control philosophy and P&ID development

**4. Actuator Safety Factor**

| Safety Factor | Advantages | Disadvantages |
|---------------|------------|---------------|
| **1.25× (Electric)** | Smaller actuator, lower cost | Less margin for uncertainty; may be undersized if torque higher than calculated |
| **1.5× (Pneumatic)** | Standard practice; adequate margin | Slightly larger actuator |
| **2.0× (Severe Service)** | Large margin for uncertainty, fouling, wear | Oversized actuator; higher cost; may cause control issues (overly fast stroking) |

**Guidance:** Use 1.5× safety factor for pneumatic actuators (standard practice per ISA-75.25). Use 1.25× for electric actuators (inherently more predictable torque). Use 2.0× for severe service (high temperature, abrasive fluids, frequent cycling) — **not typical for canola oil service**.

**Source:** ISA-75.25 actuator sizing recommendations; manufacturer guidelines

**5. Relief Valve Type: Conventional vs. Balanced-Bellows vs. Pilot-Operated**

| Type | Back Pressure Limit | Advantages | Disadvantages | Cost |
|------|---------------------|------------|---------------|------|
| **Conventional** | <10% set pressure (built-up) | Simple, low cost, direct-acting | Sensitive to back pressure | $ |
| **Balanced-Bellows** | <50% set pressure (built-up) | Less sensitive to back pressure | More complex, higher cost | $$ |
| **Pilot-Operated** | <90% set pressure (superimposed + built-up) | Handles high back pressure, tight shutoff | Most complex, highest cost, requires pilot supply | $$$ |

**Guidance:** Use conventional relief valves for low back pressure applications (<10% set pressure). Use balanced-bellows for moderate back pressure (10–50%). Use pilot-operated for high back pressure or where tight shutoff required. Calculate back pressure from discharge piping design (DEL-16.01); if excessive, either increase discharge piping size or select balanced-bellows/pilot-operated type.

**Source:** API 520 relief valve type selection guidance; typical relief system design practices

**6. Calculation Method: Hand Calculation vs. Software vs. Vendor Sizing**

| Method | Advantages | Disadvantages | When to Use |
|--------|------------|---------------|-------------|
| **Hand Calculation** | Transparent, reproducible, no software license cost | Time-consuming, error-prone for complex cases | Simple cases, independent check, sensitivity analysis |
| **Generic Software (Excel, MathCAD)** | Flexible, customizable, reusable | Requires validation, may not include all vendor-specific factors | Standard cases, consistent project approach |
| **Vendor Software (Fisher, Emerson, etc.)** | Accurate (includes vendor-specific trim factors), widely accepted | Vendor-specific; may lock in vendor selection early | Detailed sizing, vendor quotation coordination |

**Guidance:** Use generic software (Excel templates) for preliminary sizing and independent check. Use vendor software for detailed sizing after vendor selection (or for "or equal" sizing across multiple vendors). Include vendor sizing results as calculation appendices to demonstrate third-party verification.

**Source:** Typical EPC calculation practices; vendor software use for detailed valve sizing

## Examples

**Reference examples and precedents:**

**1. Employer's Requirements**

Refer to Employer's Requirements (Volume 2 Parts 1–3) for project-specific expectations:
- Valve sizing criteria and design margins
- Relief valve set pressure requirements
- Actuator safety factors and fail-safe modes
- Calculation format and deliverable requirements
- Software validation requirements

**Location:** `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf` — **TBD** (not yet available in `_REFERENCES.md`)

**2. Industry Precedents**

**Typical valve sizing for similar facilities:**

**Control Valves (Flow Control):**
- **Application:** Product transfer line flow control (railcar to storage tank, storage tank to marine loading)
- **Sizing Basis:** Design flow rate = 1.2× normal flow rate; turndown ratio = 50:1 to handle turndown to 2% of design flow
- **Typical Result:** NPS 4–6 control valves with equal-percentage trim; pneumatic spring-return actuators (fail-closed for product lines)
- **Source:** Typical transload facility control valve applications

**Relief Valves (Thermal Expansion):**
- **Application:** Product piping thermal relief (blocked-in line segment between isolation valves)
- **Sizing Basis:** Thermal expansion scenario; line heated from minimum to maximum ambient temperature over 8-hour period
- **Typical Result:** Small relief valves (NPS 1–2 with API 526 orifice D or E); set pressure = 1.5× line pressure rating; discharge to containment system
- **Source:** Typical liquid piping thermal relief sizing

**Relief Valves (Storage Tank Fire Case):**
- **Application:** Storage tank overpressure protection (external fire scenario)
- **Sizing Basis:** API 521 fire case; wetted surface area of tank exposed to fire; heat input per API 521 Table 4
- **Typical Result:** Large relief valves (NPS 6–8 with API 526 orifice M, N, or larger); set pressure = 1.05× tank design pressure (atmospheric tanks: set pressure = 2–5 psig); discharge to atmosphere via vent stack
- **Source:** API 521 storage tank relief valve sizing for fire case

**3. Calculation Templates and Tools**

**Fisher Control Valve Handbook:**
- Industry-standard reference for control valve sizing
- Provides detailed sizing equations, correction factors, and examples
- Includes noise prediction and cavitation analysis methods
- **Available online:** Emerson Automation Solutions website

**API 520 Sizing Software:**
- Various vendors provide API 520 sizing software (Emerson PRV2SIZE, Spirax Sarco ReliefSIZE, etc.)
- Calculates orifice area for liquid, vapor, two-phase relief scenarios
- Includes fire case per API 521
- **TBD:** Project standard relief valve sizing software

**ISA-75 Sizing Spreadsheets:**
- Generic Excel spreadsheets implementing ISA-75.01 equations
- Useful for preliminary sizing and independent check calculations
- **TBD:** Project standard control valve sizing spreadsheet/template

**Source:** Industry-standard references and tools for valve sizing

**4. Related Deliverables**

- **DEL-16.01 (Valve Design Drawing Set):** Valve arrangement drawings show valve locations and orientations; informed by valve sizes from calculations
- **DEL-16.02 (Valve Technical Specification):** Procurement specifications reference sizing calculation methodology and criteria
- **DEL-16.04 (Valve Data Sheet Package):** Individual valve datasheets populated with calculation results (Cv, set pressure, actuator size)
- **DEL-16.05 (Valve Installation & Test Records):** Relief valve set pressure test records verify relief valves set per calculations

**Source:** PKG-16 deliverable structure from decomposition Section 5

**5. Typical Calculation Outputs**

**Control Valve Sizing Calculation Example (Excerpt):**

```
VALVE SIZING CALCULATION
Tag: FV-1234 (Product Transfer Flow Control Valve)
Service: Canola Oil Transfer from Tank to Loading Arm

INPUT DATA:
- Flow rate (design): 150 m³/h (normal: 120 m³/h; min: 10 m³/h)
- Inlet pressure: 8 barg
- Outlet pressure: 3 barg
- Pressure drop available: 5 bar
- Fluid: Canola oil (ρ = 920 kg/m³; ν = 35 cSt at 40°C)

CALCULATIONS:
- Required Kv = Q × sqrt(ρ / (ΔP × 1000)) = 150 × sqrt(920 / (5 × 1000)) = 64.4
- Viscosity correction: Re = ... < 10,000 → apply Fv correction → Kv_corrected = 64.4 / 0.85 = 75.8
- Select valve: DN 80 (3") globe valve with Kv = 100 (> 75.8 required) ✓
- Turndown ratio: Kv_max / Kv_min = 100 / (10 m³/h design) = 50:1 ✓

RESULTS:
- Valve size: DN 80 (3")
- Valve type: Globe valve, equal-percentage trim
- Actuator: Pneumatic spring-return, fail-closed
- Cv required: 87.7 (Kv × 1.156)
- Cv selected: 116 (Kv 100 × 1.156)
- Sizing margin: 32% (acceptable)
```

**Relief Valve Sizing Calculation Example (Excerpt):**

```
RELIEF VALVE SIZING CALCULATION
Tag: PSV-5678 (Storage Tank Overpressure Protection)
Protected Equipment: Tank TK-001 (Canola Oil Storage)

RELIEF SCENARIO EVALUATION:
1. Thermal expansion: Not applicable (atmospheric tank with vent)
2. Fire case (governing): External fire per API 521
3. Overfilling: Prevented by level control and high-level alarm

FIRE CASE CALCULATION (per API 521):
- Tank diameter: 15 m; height: 12 m
- Wetted surface area: A = π × D × (H × 0.9) = 509 m²
- Heat input: Q = 43,200 × F × A^0.82 = 43,200 × 1.0 × 509^0.82 = 4,850,000 kcal/h
- Latent heat of vaporization: 50 kcal/kg (est. for canola oil)
- Relief capacity: W = 4,850,000 / 50 = 97,000 kg/h

ORIFICE SIZING (per API 520):
- Required orifice area: A = W / (Kd × P × Kb × sqrt(ρ)) = ... = 3,250 mm²
- Selected orifice: API 526 Orifice N (4,340 mm²) ✓
- Set pressure: 0.21 barg (3 psig) = 1.05× tank design pressure ✓
- Valve size: NPS 6 × 8 (6" inlet × 8" outlet)

RESULTS:
- Relief valve size: NPS 6 × 8
- Orifice designation: N (4,340 mm²)
- Set pressure: 3 psig (0.21 barg)
- Relief capacity: 97,000 kg/h (fire case)
```

**Source:** Typical calculation output format; specific values illustrative only (TBD pending actual design data)

**6. Lessons Learned (Typical Issues)**

**Common valve sizing issues to avoid:**
- **Control Valve Oversized:** Selecting valve too large reduces turndown ratio; valve operates near closed position (poor control); **Solution:** Size valve for design flow, not maximum conceivable flow
- **Relief Valve Undersized:** Failure to consider all credible relief scenarios; **Solution:** Perform thorough scenario evaluation per API 521; coordinate with HAZOP (DEL-27.02)
- **Actuator Undersized:** Using generic torque factors instead of manufacturer data; actual torque may be higher; **Solution:** Use manufacturer torque curves where available; apply adequate safety factor
- **Viscosity Neglected:** Failing to apply viscosity correction for high-viscosity fluids like canola oil; valve undersized; **Solution:** Always check Reynolds number and apply Fv correction for Re < 10,000
- **Back Pressure Underestimated:** Relief valve discharge piping too small; excessive back pressure; relief valve underperformance; **Solution:** Calculate discharge piping pressure drop; coordinate relief valve type selection with discharge piping design

**Source:** **ASSUMPTION**: Typical valve sizing issues from industry experience; project-specific lessons TBD
