# Guidance: DEL-15.02 Pump Technical Specification

## Purpose

This guidance document supports the development of **Pump Technical Specification** for **PKG-15 Pumps & Rotating Equipment** within the Canola Oil Transload Facility project.

**Deliverable purpose:** Defines performance, materials, and workmanship requirements for pumps per ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.02 entry

### Role in Project Delivery

The Pump Technical Specification serves as:

1. **Procurement basis** — Defines requirements for equipment requisition and vendor bidding
2. **Evaluation tool** — Provides criteria for vendor proposal evaluation and selection
3. **Quality baseline** — Establishes acceptance criteria for shop testing and field commissioning
4. **Design coordination** — Informs downstream design activities (DEL-15.01 arrangement, DEL-15.03 calculations)

**Source:** Standard EPC procurement document hierarchy

### Contribution to Project Objectives

This deliverable directly supports:

- **OBJ-1 (Safe & Reliable Operation):** Specifies reliable pump design per API 610 and mechanical seal systems per API 682
- **OBJ-2 (Throughput Capacity):** Defines pump performance requirements to achieve 1,000,000 MT/annum throughput
- **OBJ-4 (Operational Flexibility):** Allows for duty/standby configurations and operational modes (tank storage + direct rail-to-ship)
- **OBJ-7 (Environmental Protection):** Requires seal systems to minimize leakage and environmental impact
- **OBJ-9 (Lifecycle Cost Optimization):** Specifies energy-efficient pumps and motors; maintainability provisions; standardization opportunities

**Source:** Decomposition Section 2 (Objectives), Section 6 (Objective-Deliverable Mapping for PKG-15)

## Principles

### Engineering Rationale for Pump Specifications

#### Principle 1: API 610 as Foundation Standard

API 610 (*Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries*) is the industry-standard specification for process pumps:

- **Design requirements:** Mechanical design, materials, fabrication, auxiliary equipment
- **Performance requirements:** Hydraulic performance curves, NPSH, efficiency
- **Testing requirements:** Hydrostatic test, performance test, vibration acceptance
- **Quality requirements:** Quality assurance, inspection, documentation

**Application to canola oil service:** API 610 applies directly. Canola oil is a low-viscosity, non-corrosive, food-grade vegetable oil (similar properties to light petroleum products). Material selection may require food-grade compatibility considerations.

**Source:** API 610 scope and application; canola oil properties (typical vegetable oil)

#### Principle 2: Performance Specification vs. Design Specification

Two approaches to pump procurement specifications:

| Approach | Description | Pros | Cons |
|----------|-------------|------|------|
| **Performance Specification** | Specify required performance (flow, head, NPSH), fluid properties, and applicable codes. Vendor selects pump model. | Vendor expertise utilized; competitive bidding; vendor assumes performance risk | Less control over specific design features; evaluation more complex |
| **Design Specification** | Specify pump model, materials, configuration in detail. Vendor provides per specification. | Tight control over design; easier evaluation; standardization across similar services | Limits vendor innovation; may not get optimal design; single-source risk |

**Recommendation:** **Performance specification** approach preferred for most services (railcar unloading, marine loading, sump pumps). Allows vendors to propose optimal solutions while meeting performance requirements.

**Source:** Industry practice; API 610 supports performance-based procurement

#### Principle 3: Material Selection for Canola Oil Service

Canola oil is non-corrosive and food-grade compatible. Material selection considerations:

| Component | Material Options | Considerations |
|-----------|------------------|----------------|
| **Casing/Impeller** | Cast iron (S-6), ductile iron, or carbon steel (S-1) | Non-corrosive service; cast iron cost-effective; food-grade compatibility **TBD** |
| **Shaft** | Carbon steel or 316 SS | 316 SS preferred for corrosion resistance in coastal environment |
| **Wear Rings** | Bronze or stainless steel | Replaceable wear component; dissimilar metal to casing reduces galling |
| **Mechanical Seal** | Silicon carbide or tungsten carbide faces | Hard faces for long life and low wear; food-grade compatible |

**Food-grade consideration:** If food-grade compliance required by regulations or Employer, avoid leaded materials (some bronzes) and specify food-grade-compatible coatings/materials. **TBD**: Confirm food-grade requirements per ER Part 2.

**Source:** API 610 Annex G (material designations); food-grade handling best practices

#### Principle 4: Seal Selection per API 682

Mechanical seal selection impacts reliability, maintenance, and environmental compliance:

| Seal Type | Application | Seal Support System | Considerations |
|-----------|-------------|---------------------|----------------|
| **Single Seal (API 682 Type 1 or 2)** | Non-hazardous, low-toxicity services | Plan 11 (recirculation) or Plan 32 (external flush) | Simpler, lower cost; some seal leakage acceptable; requires leak collection |
| **Dual Seal (API 682 Type 2 or 3)** | Hazardous, toxic, or zero-leakage services | Plan 53A, 53B, or 54 (pressurized barrier fluid) | More complex, higher cost; near-zero leakage; enhanced environmental protection |

**Recommendation for canola oil service:** Single mechanical seal likely adequate (non-toxic, food-grade service). Dual seal may be considered for marine loading pumps if environmental regulations require zero-leakage design (OBJ-7).

**Decision:** **TBD** — Confirm seal selection requirements per ER Part 2 environmental requirements and regulatory compliance (OBJ-6, OBJ-7).

**Source:** API 682 seal types and piping plans

#### Principle 5: NPSH Considerations

Net Positive Suction Head (NPSH) is critical for pump reliability:

- **NPSH Available (NPSHA):** Pressure head available at pump suction (calculated by system designer in DEL-15.03)
- **NPSH Required (NPSHR):** Minimum pressure head required by pump to avoid cavitation (provided by vendor)

**Requirement:** NPSHA must exceed NPSHR by adequate margin (typically 0.5m minimum; more for critical services).

**NPSH challenges in this facility:**

| Pump Service | NPSH Challenge | Mitigation |
|--------------|---------------|------------|
| **Railcar Unloading** | Railcar liquid level varies during unloading (affects NPSHA) | Position pump below railcar level; consider booster pump if needed |
| **Marine Loading** | Tank liquid level varies; long suction piping runs | Minimize suction piping length; consider pump elevation below tank bottom |
| **Sump Pumps** | Low suction head (sump level) | Vertical sump pumps eliminate NPSH concerns |

**Source:** API 610 Section 3 (NPSH requirements); DEL-15.03 will calculate NPSHA

## Considerations

### Pump Service-Specific Considerations

#### Railcar Unloading Pumps

**Service:** Transfer CSD canola oil from railcars to storage tanks or marine loading system

| Factor | Consideration |
|--------|---------------|
| **Capacity** | **TBD** — Design for typical railcar size and unloading time (e.g., 100m³ railcar in 30–60 minutes → 100–200 m³/hr per pump) |
| **Head** | **TBD** — Static head (elevation difference) + piping friction + tank pressure |
| **NPSH** | Railcar level varies; worst-case NPSHA at end of unloading when level is low |
| **Redundancy** | Duty/standby configuration likely for reliability (OBJ-1); 32 railcar stations may require multiple pumps |
| **Controls** | Automatic start/stop based on railcar liquid level and tank level; VFD may optimize unloading rate |
| **Viscosity** | Canola oil viscosity increases at low temperatures; heating may be required for winter operations |

**Source:** Typical railcar unloading system requirements; specific parameters TBD per process design and ER Part 2

#### Marine Loading Pumps

**Service:** Transfer CSD canola oil from storage tanks to marine loading arms for ship loading

| Factor | Consideration |
|--------|---------------|
| **Capacity** | **TBD** — Design for efficient ship loading (typical: 500–1,500 m³/hr depending on ship size and loading time) |
| **Head** | **TBD** — Static head (tank to ship deck) + piping friction + marine loading arm pressure drop |
| **NPSH** | Tank level varies; worst-case NPSHA at minimum tank level |
| **Redundancy** | Duty/standby configuration for operational flexibility (OBJ-4) and reliability (OBJ-1) |
| **Controls** | Flow rate control (fixed-speed + throttle valve, or VFD); custody transfer metering interface (OBJ-10) |
| **Emergency shutdown** | Quick-close valves and pump shutdown on ESD signal (coordinate with safety systems) |

**Source:** Typical marine loading system requirements; specific parameters TBD per DEL-11 (Marine Loading System) and ER Part 2

#### Sump Pumps

**Service:** Spill recovery, rainwater drainage, leak collection from containment sumps

| Factor | Consideration |
|--------|---------------|
| **Capacity** | **TBD** — Design for sump pump-down time and drainage requirements (typical: 10–100 m³/hr) |
| **Head** | **TBD** — Sump depth + discharge elevation + piping friction (typically low head, 10–30m) |
| **Configuration** | Vertical sump pump (eliminates NPSH concerns); submersible or dry-pit mounting |
| **Redundancy** | Consider duty/standby for critical spill recovery sumps (OBJ-7 environmental protection) |
| **Controls** | Automatic start/stop based on sump level (float switch or level transmitter); high-level alarm |
| **Hazardous area** | May require explosion-proof motor if sump is in hazardous area (Class I, Div 2 typical for canola oil) |

**Source:** Typical sump pump requirements; specific parameters TBD per PKG-03 (drainage design) and environmental requirements

### Standardization Considerations

**Trade-off:** Standardize pump models across services vs. optimize each pump for specific duty

| Factor | Standardized Pumps | Optimized Pumps |
|--------|-------------------|-----------------|
| **Performance** | May not be optimal for all duties | Each pump optimized for service |
| **Cost (capital)** | Volume discount; single procurement package | Multiple procurement packages |
| **Cost (lifecycle)** | Reduced spare parts inventory; simplified maintenance | Higher spare parts inventory |
| **Delivery** | Single vendor, faster delivery | Multiple vendors, coordination required |
| **Energy** | Some pumps may operate off best efficiency point | Each pump operates at best efficiency point |

**Guidance:** Pursue standardization where feasible (e.g., all railcar unloading pumps same model; all marine loading pumps same model) to support OBJ-9 (lifecycle cost optimization). Accept some performance trade-off for significant spare parts and maintenance simplification.

**Decision:** **TBD** — Evaluate during specification development and vendor proposal review.

**Source:** Industry practice; OBJ-9 (lifecycle cost optimization)

### Fixed-Speed vs. Variable-Speed (VFD) Trade-Off

**Consideration:** Electric motor drives (fixed-speed) vs. variable-frequency drives (VFD)

| Service | Fixed-Speed Recommendation | VFD Recommendation |
|---------|---------------------------|--------------------|
| **Railcar Unloading** | Consider VFD if unloading rate varies significantly | VFD allows optimized unloading rate and reduces energy at part-load |
| **Marine Loading** | Consider VFD if ship loading rates vary | VFD provides flow control without throttle valve losses; supports multiple ship sizes (OBJ-4) |
| **Sump Pumps** | Fixed-speed typical (on/off control) | VFD not justified for intermittent duty |

**Energy savings calculation required:** VFD justification depends on operating hours, load profile, and energy cost. See DEL-15.03 for lifecycle cost analysis.

**Source:** Industry practice; OBJ-9 (lifecycle cost optimization)

## Trade-offs

### Trade-off 1: Single vs. Dual Mechanical Seals

Addressed in Principle 4 (Seal Selection per API 682). Decision TBD based on environmental requirements and regulatory compliance.

### Trade-off 2: Horizontal vs. Vertical Pump Configuration

Addressed in DEL-15.01 Guidance.md (Equipment-Centric Design Coordination). Typically horizontal for process pumps, vertical for sump pumps.

### Trade-off 3: API 610 Edition Selection

| Option | Considerations |
|--------|---------------|
| **Latest Edition (11th Edition, 2010 or later)** | Most current requirements; may have more stringent (costly) requirements |
| **Earlier Edition (if allowed by ER)** | Less stringent requirements; lower cost; adequate for many services |

**Recommendation:** Use latest edition unless ER specifies earlier edition. Latest edition reflects current industry best practices.

**Source:** API 610 revision history; ER Part 1 TBD for edition requirement

## Examples

### Reference Specifications and Precedents

**Similar facility precedents:**
- **Richardson International (Vancouver):** Canola crushing facility — vegetable oil pumping systems
- **Vancouver Wharves:** Multi-commodity terminal — vegetable oil handling and marine loading
- **Cargill (Alberta):** Canola processing — rail and truck loading systems

**Typical pump specifications observed:**
- API 610 Type OH2 (horizontal, overhung impeller, single-stage, centerline support) for general transfer duties
- Cast iron or ductile iron construction for non-corrosive canola oil service
- Single mechanical seal with Plan 11 or Plan 32 seal support system
- Electric motor drive (fixed-speed or VFD)

**Relevance:** Fraser Surrey Terminal canola oil service similar to these precedents. Specifications can reference proven designs.

**Source:** Industry knowledge; publicly available facility information

### Anticipated Specification Documents

From `_CONTEXT.md`, the following specification documents are anticipated for DEL-15.02:

1. **Railcar Unloading Pump Specification** — Performance, materials, and testing requirements
2. **Marine Loading Pump Specification** — Performance, materials, and testing requirements
3. **Sump Pump Specification** — Performance, materials, and testing requirements

**Source:** `_CONTEXT.md` (anticipated artifacts)

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Cross-References:**
- Datasheet.md — Equipment attributes, fluid properties, operating conditions
- Specification.md — Requirements for pump performance, materials, quality, testing
- Procedure.md — Process for developing and verifying specifications
- DEL-15.01 — Pump Design Drawing Set (installation arrangement informed by specification)
- DEL-15.03 — Pump Design Calculations (sizing, NPSH, system curves inform specification)
- DEL-15.04 — Pump Data Sheet Package (vendor data resulting from specification procurement)
- DEL-15.05 — Pump Installation & Test Records (field testing per specification requirements)
