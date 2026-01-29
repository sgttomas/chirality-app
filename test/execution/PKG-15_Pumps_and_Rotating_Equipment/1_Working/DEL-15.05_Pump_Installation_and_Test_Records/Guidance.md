# Guidance: DEL-15.05 Pump Installation & Test Records

## Purpose

This guidance document supports the installation and commissioning of pumps and the development of installation and test records for **PKG-15 Pumps & Rotating Equipment** within the Canola Oil Transload Facility project.

**Deliverable purpose:** Provides evidence of completion, inspection, and testing for pumps per ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.05 entry

### Role in Project Delivery

The Pump Installation & Test Records serve as:

1. **Quality assurance** — Demonstrates pumps are installed and performing per specifications
2. **Warranty support** — Provides baseline records for equipment warranty and troubleshooting
3. **Operations baseline** — Establishes initial performance data for future comparison
4. **Regulatory compliance** — Satisfies permit and inspection requirements

**Source:** Standard role of commissioning records

### Contribution to Project Objectives

This deliverable supports:

- **OBJ-1 (Safe & Reliable Operation):** Verified installation and performance ensures reliable operation
- **OBJ-2 (Throughput Capacity):** Performance testing confirms pumps meet capacity requirements
- **OBJ-9 (Lifecycle Cost Optimization):** Baseline performance data enables future performance trending and maintenance optimization

**Source:** Decomposition Section 2 (Objectives)

## Principles

### Principle 1: Proper Alignment is Critical

**Shaft alignment** between pump and motor is one of the most critical installation activities.

**Why alignment matters:**
- Misalignment causes excessive vibration → bearing failure, seal leakage, shaft breakage
- Misalignment reduces equipment life (50% misalignment can reduce bearing life by 80%)
- Proper alignment ensures long-term reliability (OBJ-1)

**Alignment process per API 610 Section 6.3:**
1. **Rough alignment:** During initial equipment set (before grouting)
2. **Final alignment:** After grout curing (7+ days) and before piping connection
3. **Final check:** After piping connection (verify piping has not imposed misalignment)

**Alignment methods:**
- **Dial indicator method:** Traditional, accurate to 0.05mm typical
- **Laser alignment:** Modern, faster, accurate to 0.01mm typical (preferred)

**Typical API 610 alignment tolerances:**
- Parallel offset: < 0.05mm (0.002 inches)
- Angular offset: < 0.05mm per 100mm diameter (0.002 inches per inch)

**Source:** API 610 Section 6.3 (alignment); industry experience on alignment importance

### Principle 2: Grouting Must Cure Before Final Operations

**Grouting sequence per API 610 Section 6.1.4:**
1. Equipment set and rough-aligned
2. Non-shrink grout poured (25–75mm thickness typical)
3. **Curing period: Minimum 7 days** per ACI 318 before final alignment and startup
4. Final alignment after curing

**Common grouting mistakes:**
- **Too thin:** < 25mm grout may crack or not provide adequate support
- **Too thick:** > 75mm grout may not cure properly (heat buildup)
- **Inadequate curing:** Starting up before 7 days can cause grout failure and misalignment
- **Voids:** Improper pouring leaves voids under baseplate → uneven support

**Prevention:**
- Use non-shrink grout per manufacturer instructions
- Pour from one side to avoid voids
- Maintain proper curing conditions (temperature, moisture)
- Wait full curing period before final alignment

**Source:** API 610 Section 6.1.4 (grouting); ACI 318 (grout curing)

### Principle 3: Performance Testing Should Match Design Conditions

**Objective:** Verify pump performs per specification (DEL-15.02) and calculations (DEL-15.03)

**Challenge:** Field conditions may differ from design conditions:
- System may not be at full capacity during commissioning
- Flow rate may be limited by incomplete piping systems
- Fluid properties may differ from design (temperature, viscosity)

**Approach:**
1. **Test at rated conditions** if possible (preferred per API 610 Section 6.9)
2. **If rated conditions unavailable:** Test at multiple points and use pump affinity laws to project performance at rated conditions
3. **Document test conditions:** Clearly record what conditions were tested so results can be properly interpreted

**Pump affinity laws** (for same impeller diameter):

- Q₂ = Q₁ × (N₂ / N₁) [Flow proportional to speed]
- H₂ = H₁ × (N₂ / N₁)² [Head proportional to speed squared]
- P₂ = P₁ × (N₂ / N₁)³ [Power proportional to speed cubed]

Where N = pump speed (RPM), Q = flow, H = head, P = power

**Source:** API 610 Section 6.9 (field performance test); pump affinity laws

## Considerations

### Installation Sequence and Schedule

**Typical installation duration:**
- Equipment set and rough alignment: 1–2 days
- Grouting: 1 day
- **Grout curing: 7 days minimum** (schedule constraint)
- Final alignment: 1 day
- Piping connection and flush: 2–3 days
- Electrical connection: 1–2 days
- Pre-start checks: 1 day
- Performance testing: 1–2 days
- **Total: 2–3 weeks per pump**

**Schedule considerations:**
- **Weather dependency:** Outdoor grouting requires suitable weather (no rain, temperature > 5°C)
- **Crane availability:** Heavy equipment may require mobile crane (coordinate with site logistics)
- **Piping readiness:** Piping system must be complete and flushed before pump startup
- **Power availability:** Electrical power must be energized and verified before motor startup

**Source:** Typical pump installation schedule; API 610 installation requirements

### Performance Test Planning

**Pre-test preparation:**
- Verify all installation complete (alignment, grouting, piping, electrical)
- Verify system is clean (piping flushed per piping specification)
- Verify instrumentation is installed and calibrated (flow meter, pressure gauges, power meter)
- Prepare test data sheets and procedures
- Coordinate with operations personnel

**Test execution:**
- Start pump at low flow (minimum stable flow)
- Gradually increase flow to rated conditions
- Record measurements at multiple operating points (50%, 75%, 100%, 110% of rated flow if possible)
- Monitor vibration continuously during test
- Monitor for abnormal noise, leaks, or other issues

**Post-test:**
- Analyze test data and compare to design (DEL-15.03) and vendor data (DEL-15.04)
- If performance unacceptable, investigate causes (blockage, wrong rotation, air in system, etc.)
- If performance acceptable, obtain acceptance sign-offs

**Source:** API 610 Section 6.9 (field performance test procedure)

### Common Installation and Testing Issues

| Issue | Symptoms | Likely Cause | Resolution |
|-------|----------|--------------|------------|
| **High vibration** | Vibration > API 610 limits | Misalignment, unbalance, resonance | Re-check alignment; verify balancing; check for resonance |
| **Low flow** | Flow < expected | Blockage, wrong rotation, air entrainment | Check strainer; verify rotation; vent system |
| **High power** | Power > expected | High system resistance, wrong impeller diameter | Check for blockages; verify impeller diameter |
| **Seal leakage** | Visible leakage at seal | Improper installation, damaged seal, misalignment | Check seal installation; verify alignment; inspect seal |
| **Cavitation noise** | Rattling/popping sound | Insufficient NPSH, air in suction | Verify NPSH (compare to DEL-15.03); vent suction piping |

**Source:** API 610 troubleshooting guidance; industry commissioning experience

### Cross-Discipline Coordination

**Coordination requirements:**

| Discipline | Coordination Item | Timing |
|------------|-------------------|--------|
| **Civil/Structural (PKG-05)** | Foundation ready, cured, inspected | Before equipment set |
| **Piping (DEL-14)** | Piping complete, flushed, ready for connection | Before pump startup |
| **Electrical (PKG-19/20)** | Power available, motor connected and tested | Before pump startup |
| **I&C (PKG-29/30)** | Instruments installed, calibrated, operational | Before performance test |
| **Operations** | Personnel available for commissioning support | During testing |

**Source:** Typical commissioning coordination requirements

## Trade-offs

### Trade-off: FAT vs. No FAT

**Factory Acceptance Test (FAT):** Shop test before shipment

| Option | Advantages | Disadvantages |
|--------|-----------|---------------|
| **Perform FAT** | Verifies performance before shipment; identifies issues early; reduces field commissioning risk | Higher cost; schedule delay for testing; Contractor/Owner travel to vendor shop |
| **No FAT** | Lower cost; faster delivery | Performance not verified until field commissioning; higher risk of field issues |

**Guidance:** FAT recommended for critical or large pumps (e.g., marine loading pumps). May be waived for small or non-critical pumps (e.g., sump pumps) if vendor has good track record.

**Source:** API 610 Section 7 (shop tests optional unless specified)

### Trade-off: Detailed vs. Simplified Field Testing

| Approach | When to Use | Advantages | Disadvantages |
|----------|-------------|-----------|---------------|
| **Detailed field test** (full API 610 Section 6.9) | Critical pumps; high-energy pumps; contractual requirement | High confidence in performance; detailed baseline data | More time and cost; requires calibrated instruments |
| **Simplified field test** (basic flow/pressure check) | Non-critical pumps; small pumps; schedule constraints | Faster, less expensive | Less confidence; limited baseline data |

**Guidance:** Full API 610 field test recommended for railcar unloading and marine loading pumps (critical to OBJ-2 throughput). Simplified test may be acceptable for sump pumps.

**Source:** Engineering judgment; balance between risk and schedule/cost

## Examples

### Example: Alignment Tolerance Check

**Given:**
- Coupling diameter: 150mm
- Dial indicator readings: 0.08mm parallel offset, 0.12mm angular offset

**Check:**
- Parallel offset tolerance: < 0.05mm (API 610 typical) → **0.08mm EXCEEDS tolerance**
- Angular offset tolerance: < 0.05mm per 100mm = 0.075mm for 150mm diameter → **0.12mm EXCEEDS tolerance**

**Action:** Re-align pump until within tolerance.

**Source:** API 610 Section 6.3 alignment tolerances

### Example: Performance Test Acceptance

**Given:**
- Design flow (DEL-15.03): 150 m³/hr
- Test measured flow: 145 m³/hr
- Tolerance: ±7% (ISO 9906 Grade 2) = ±10.5 m³/hr

**Check:**
- Deviation: 150 - 145 = 5 m³/hr
- Allowable deviation: ±10.5 m³/hr
- **Result: ACCEPTABLE** (within tolerance)

**Source:** ISO 9906 Grade 2 tolerance

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Cross-References:**
- Datasheet.md — Installation and testing requirements
- Specification.md — Acceptance criteria for installation and performance
- Procedure.md — Step-by-step installation and testing procedures
- DEL-15.01 — Pump Design Drawing Set (installation per drawings)
- DEL-15.02 — Pump Technical Specification (performance requirements)
- DEL-15.03 — Pump Design Calculations (design performance for comparison)
- DEL-15.04 — Pump Data Sheet Package (vendor data baseline)
