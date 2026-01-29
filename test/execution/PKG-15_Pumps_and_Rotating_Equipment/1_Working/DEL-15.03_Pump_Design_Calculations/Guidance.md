# Guidance: DEL-15.03 Pump Design Calculations

## Purpose

This guidance document supports the development of **Pump Design Calculations** for **PKG-15 Pumps & Rotating Equipment** within the Canola Oil Transload Facility project.

**Deliverable purpose:** Provides the engineering basis and sizing/verification calculations for pumps per ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.03 entry

### Role in Project Delivery

The Pump Design Calculations serve as:

1. **Technical basis for procurement** — Defines pump requirements for DEL-15.02 (specification) and vendor selection
2. **Design verification tool** — Confirms vendor pump proposals meet system requirements (NPSH margin, operating point)
3. **Coordination baseline** — Provides pump performance data to piping, electrical, and I&C disciplines
4. **Commissioning reference** — Provides expected performance for field testing verification (DEL-15.05)

**Source:** Standard role of pump sizing calculations in EPC projects

### Contribution to Project Objectives

This deliverable directly supports:

- **OBJ-2 (Throughput Capacity):** Pump sizing ensures 1,000,000 MT/annum throughput is achievable
- **OBJ-4 (Operational Flexibility):** Calculations verify pumps can operate in both tank storage and direct rail-to-ship modes
- **OBJ-9 (Lifecycle Cost Optimization):** Proper pump sizing ensures operation near best efficiency point, minimizing energy costs

**Source:** Decomposition Section 2 (Objectives), Section 6 (Objective-Deliverable Mapping for PKG-15)

## Principles

### Principle 1: Conservative NPSH Calculation

NPSH (Net Positive Suction Head) is critical for preventing cavitation and ensuring reliable pump operation.

**NPSH Available (NPSHA) must be calculated for worst-case conditions:**
- **Minimum liquid level** in suction vessel (lowest NPSHA)
- **Maximum fluid temperature** (highest vapor pressure reduces NPSHA)
- **Maximum suction piping friction** (longest piping run, highest flow rate)

**Equation:**
NPSHA = Hatm + Hs - Hvp - Hf(suction)

Where:
- Hatm = Atmospheric pressure head (~10.3m at sea level)
- Hs = Static head at suction (positive if liquid above pump, negative if below)
- Hvp = Vapor pressure head of fluid
- Hf(suction) = Friction losses in suction piping

**NPSH Margin requirement:** NPSHA must exceed vendor NPSHR by ≥0.5m (API 610 recommendation). For critical services or high-energy pumps, larger margin may be prudent (1.0–1.5m).

**Source:** API 610 Section 3.8 (NPSH); engineering best practices

**Common NPSH Issues:**

| Issue | Cause | Mitigation |
|-------|-------|------------|
| **Cavitation at startup** | Cold startup increases fluid viscosity and friction losses | Calculate NPSHA at startup conditions; provide heating if needed |
| **Cavitation at low tank level** | Static head decreases as tank empties | Size pump for minimum tank level; provide low-level shutdown |
| **Cavitation in hot service** | High temperature increases vapor pressure | Locate pump below suction vessel; use inducer impellers if needed |

**Source:** API 610 troubleshooting guidance; industry experience

### Principle 2: System Curve and Pump Operating Point

**System curve** represents total head required vs. flow rate:
H(Q) = Hs + K × Q²

Where:
- Hs = Static head (constant with flow)
- K = System resistance coefficient (from friction and equipment losses)

**Pump curve** (from vendor) shows pump head vs. flow at constant speed.

**Operating point** = Intersection of pump curve and system curve.

**Preferred operating region:** 70–120% of pump best efficiency point (BEP) per API 610.

**Common operating point issues:**

| Issue | Cause | Solution |
|-------|-------|----------|
| **Operating point too far left** (low flow) | System resistance lower than calculated | Increase system resistance (throttle valve, orifice) or reduce pump speed (VFD) |
| **Operating point too far right** (high flow) | System resistance higher than calculated | Check for blockage, undersized piping; may need larger pump |
| **Multiple operating points** (unstable) | Pump curve too flat or drooping | Select pump with steeper curve; avoid pumps with drooping curves |

**Source:** API 610 Section 3 (performance requirements); hydraulic system analysis

### Principle 3: Friction Loss Calculation Accuracy

Friction losses in piping are calculated using Darcy-Weisbach equation:

hf = f × (L/D) × (V²/2g)

Where:
- f = Darcy friction factor (from Moody diagram or Colebrook equation)
- L = Pipe length
- D = Pipe internal diameter
- V = Flow velocity
- g = Gravitational acceleration

**Key considerations:**

1. **Pipe roughness:** Use conservative values (ε = 0.046mm for commercial steel; higher for aged/fouled pipe)
2. **Reynolds number:** Calculate Re = (V × D) / ν to determine flow regime (laminar Re < 2,300; turbulent Re > 4,000)
3. **Minor losses:** Fittings and valves contribute significant losses; use K-factor method: hm = K × (V²/2g)
4. **Control valve pressure drop:** Often the largest single pressure drop; use valve Cv and flow rate to calculate

**Alternative: Hazen-Williams equation** (simpler but less accurate for viscous fluids):
hf = 10.67 × L × Q^1.85 / (C^1.85 × D^4.87)  [SI units]

Where C = Hazen-Williams coefficient (C = 140 for new steel, C = 100–120 for aged steel)

**Source:** Crane Technical Paper No. 410 (friction loss calculations); fluid mechanics references

### Principle 4: Pump Power Calculation and Motor Sizing

**Pump brake horsepower (BHP):**
BHP = (ρ × g × Q × TDH) / (η × 1,000)  [SI: result in kW]

Where:
- ρ = Fluid density (kg/m³)
- g = Gravitational acceleration (9.81 m/s²)
- Q = Flow rate (m³/s)
- TDH = Total dynamic head (m)
- η = Pump efficiency (decimal)

**Pump efficiency estimation:**
- Small pumps (< 50 HP): η ~ 60–75%
- Medium pumps (50–200 HP): η ~ 75–85%
- Large pumps (> 200 HP): η ~ 85–90%

Use API 610 typical efficiency curves or vendor data for more accurate estimates.

**Motor sizing:** Motor rated power ≥ 1.15 × BHP at rated flow (15% margin typical).

Additional motor margin may be required for:
- High starting torque
- Frequent starts/stops
- VFD applications (consider harmonics and derating)

**Source:** API 610 Section 3 (efficiency), Section 5.6 (drivers); electrical motor sizing standards

## Considerations

### Pump Service-Specific Considerations

#### Railcar Unloading Pumps

**Sizing considerations:**
- **Variable suction head:** Railcar liquid level varies from full to nearly empty during unloading
- **NPSHA at end of unloading:** Worst case when railcar is nearly empty (lowest static head)
- **Flow rate:** Balance between unloading time and pump size (typical: 100–200 m³/hr per railcar)
- **System curve:** May have two distinct curves (tank filling mode vs. direct-to-ship mode per OBJ-4)

**Calculation approach:** Size for worst-case NPSH (end of railcar unloading, maximum temperature) and verify operating point for both operating modes.

**Source:** Typical railcar unloading system requirements

#### Marine Loading Pumps

**Sizing considerations:**
- **High flow rate:** Efficient ship loading requires high capacity (typical: 500–1,500 m³/hr)
- **Variable discharge head:** Ship deck elevation varies with tide and loading state
- **Long piping runs:** Marine loading arms may be 100+ meters from pump house
- **Control valve pressure drop:** Significant (may be 50–100 kPa for flow control)

**Calculation approach:** Calculate for maximum discharge head (worst-case tide and ship draft) and verify NPSH at minimum tank level.

**Source:** Typical marine loading system requirements

#### Sump Pumps

**Sizing considerations:**
- **Low NPSH required:** Vertical sump pumps eliminate NPSH concerns
- **Intermittent duty:** Size for pump-down time, not continuous operation
- **Solids handling:** May need to pass small solids (consider open impeller or solids-handling design)
- **Head requirements:** Typically low (10–30m) — sump depth plus discharge elevation

**Calculation approach:** Calculate for pump-down time (sump volume / flow rate) and verify adequate submergence for vertical pump.

**Source:** Typical sump pump requirements

### Common Calculation Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| **Underestimating friction losses** | Pump undersized, low flow | Use conservative pipe roughness; include all fittings and valves |
| **Optimistic NPSH calculation** | Cavitation, pump damage | Use worst-case liquid levels and temperatures |
| **Ignoring control valve pressure drop** | Pump operates far from BEP, inefficient | Include realistic control valve ΔP (50–100 kPa typical) |
| **Not checking multiple operating scenarios** | Pump unsuitable for one operating mode | Calculate for all modes (tank filling, direct transfer, minimum/maximum flow) |
| **Using incorrect fluid properties** | Wrong pump size | Verify fluid properties at operating temperature (viscosity is highly temperature-dependent for oils) |

**Source:** Engineering lessons learned; common pump sizing errors

### Design Margins and Conservatism

**Where to be conservative:**
- **NPSH available:** Use worst-case conditions (minimum level, maximum temperature)
- **Pipe roughness:** Use higher roughness values to account for fouling
- **Future expansion:** Consider adding 10–20% flow margin if Phase 2 expansion is likely (OBJ-8)

**Where NOT to be overly conservative:**
- **Don't oversize pumps excessively:** Operating far from BEP reduces efficiency and increases energy cost (conflicts with OBJ-9)
- **Don't stack multiple safety factors:** Apply margin once at appropriate location (e.g., motor sizing margin), not at every calculation step

**Source:** Engineering judgment; balancing reliability with efficiency per OBJ-9

## Trade-offs

### Trade-off 1: Pump Speed Selection

| Speed | Advantages | Disadvantages |
|-------|-----------|---------------|
| **High speed** (3,600 RPM) | Smaller pump, lower capital cost | Higher NPSHR, more wear, higher vibration, shorter bearing life |
| **Medium speed** (1,800 RPM) | Good balance of size and NPSHR | Most common choice |
| **Low speed** (1,200 RPM) | Lower NPSHR, longer life, less maintenance | Larger pump, higher capital cost |

**Guidance:** Medium speed (1,800 RPM) typical for most process pumps. Low speed (1,200 RPM) may be justified for critical services or difficult NPSH conditions.

**Source:** API 610 pump speed considerations; lifecycle cost analysis

### Trade-off 2: Pipe Sizing for Suction Piping

**Larger pipe diameter:**
- Reduces friction losses (improves NPSHA)
- Reduces flow velocity (reduces erosion, noise)
- Increases capital cost (larger pipe, valves, fittings)
- May increase plot space requirements

**Smaller pipe diameter:**
- Higher friction losses (reduces NPSHA)
- Higher flow velocity (may cause erosion if > 3 m/s)
- Lower capital cost
- More compact layout

**Guidance:** Suction piping typically sized for 1.0–2.0 m/s velocity (balance between NPSH and cost). Discharge piping can tolerate higher velocities (2–4 m/s).

**Source:** API 610 recommendations; piping design practice

## Examples

### Example Calculation: Railcar Unloading Pump Sizing

**Given:**
- Flow rate: Q = 150 m³/hr (41.7 L/s)
- Railcar liquid level: 3.0m above pump centerline (full) to 0.5m above pump centerline (nearly empty)
- Discharge: Storage tank at +8.0m elevation, atmospheric pressure
- Suction piping: 150mm (6") × 10m length, 2 elbows, 1 gate valve
- Discharge piping: 100mm (4") × 50m length, 4 elbows, 1 check valve, 1 control valve
- Fluid: Canola oil, SG = 0.92, viscosity = 50 mm²/s @ 20°C

**Calculate:**

1. **Static head:** Hs = 8.0m - 0.5m (worst case) = 7.5m

2. **Suction friction losses:** (using Darcy-Weisbach)
   - Velocity: V_suction = Q / A = 0.0417 / (π × 0.075²) = 2.36 m/s
   - Reynolds number: Re = V × D / ν = 2.36 × 0.15 / (50 × 10^-6) = 7,080 (turbulent)
   - Friction factor: f ≈ 0.025 (from Moody diagram)
   - Pipe friction: hf_pipe = 0.025 × (10/0.15) × (2.36²/2g) = 0.47m
   - Fittings (2 elbows, 1 gate valve): K_total ≈ 1.5, hf_fittings = 1.5 × (2.36²/2g) = 0.43m
   - **Total suction losses: 0.47 + 0.43 = 0.90m**

3. **Discharge friction losses:**
   - Velocity: V_discharge = 0.0417 / (π × 0.05²) = 5.31 m/s
   - Pipe friction: hf_pipe ≈ 0.025 × (50/0.10) × (5.31²/2g) ≈ 1.79m
   - Fittings (4 elbows, 1 check valve): K_total ≈ 5.0, hf_fittings = 5.0 × (5.31²/2g) ≈ 7.19m
   - Control valve: ΔP ≈ 50 kPa → 5.5m
   - **Total discharge losses: 1.79 + 7.19 + 5.5 = 14.48m**

4. **Total Dynamic Head:** TDH = 7.5 + 0.90 + 14.48 = **22.88m (≈ 23m)**

5. **NPSH Available (worst case):**
   - NPSHA = 10.3m (atm) + 0.5m (static) - 0.1m (vapor pressure, est.) - 0.90m (friction) = **9.8m**
   - Vendor NPSHR must be < 9.8 - 0.5 = **9.3m maximum**

6. **Pump Power:**
   - Assume pump efficiency η = 75%
   - BHP = (920 × 9.81 × 0.0417 × 23) / (0.75 × 1,000) = **11.6 kW** (~16 HP)
   - Motor size: 1.15 × 11.6 = **13.3 kW** → Select 15 kW motor (standard size)

**Source:** Example calculation using methods from Datasheet.md and Specification.md

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Cross-References:**
- Datasheet.md — Calculation methodology and equations
- Specification.md — Calculation requirements and acceptance criteria
- Procedure.md — Step-by-step calculation process
- DEL-15.01 — Pump Design Drawing Set (elevation data, piping layout)
- DEL-15.02 — Pump Technical Specification (calculation outputs used for spec requirements)
- DEL-15.04 — Pump Data Sheet Package (vendor data verification against calculations)
- DEL-15.05 — Pump Installation & Test Records (field test comparison)
