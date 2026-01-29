# Guidance: DEL-17.01 Electrical Power Design Drawing Set

## Purpose

This guidance document supports the development of **Electrical Power Design Drawing Set** for **PKG-17 Electrical Power Distribution**.

**Deliverable Purpose** (Source: Decomposition DEL-17.01 entry): Defines the design arrangement and details for electrical power per ER requirements.

**Downstream Use**:
- Construction contractor uses drawings for equipment procurement, installation, and wiring
- Electrical inspectors (BC Safety Authority) use drawings for permit review and inspection approval
- Commissioning team uses drawings for system energization and functional testing
- Operations and maintenance personnel use drawings for system understanding and troubleshooting
- Future expansion planning references drawings for existing system capacity and routing

**Deliverable Classification**:
- **Type**: Drawing
- **Discipline**: Electrical
- **Responsible**: D&B Contractor
- **Project Phase**: Design & Build — Phase 1

## Principles

**Engineering Rationale** (Electrical Power Distribution):

**1. Hierarchical Distribution Architecture**
- Industrial electrical distribution follows a hierarchical architecture: Utility → Primary Distribution (MV) → Transformation → Secondary Distribution (LV) → End-Use Loads.
- **Rationale**: Hierarchical design provides fault isolation, selective coordination, maintainability, and efficient power delivery to diverse load types.
- **Source**: IEEE Std 141 (Red Book) — industrial power distribution best practices.

**2. Voltage Level Selection**
- **Medium Voltage (MV)**: Service from utility at MV level (typically 25 kV or 13.8 kV in BC) minimizes utility service costs and allows on-site transformation flexibility.
- **Low Voltage (LV)**: Multiple secondary voltage levels serve different load categories:
  - 600V: Large motors (pumps, fans) — higher voltage reduces cable size and losses
  - 480V: Process equipment, moderate motor loads
  - 208V-120V: Lighting, receptacles, small loads
- **Rationale**: Multi-voltage design optimizes equipment cost, cable sizing, and operational efficiency.
- **Source**: CEC voltage class definitions; IEEE Std 141 voltage selection guidance.

**3. Protection and Coordination**
- Electrical distribution system design shall incorporate selective coordination of protective devices (fuses, circuit breakers, relays) to ensure only the faulted circuit is isolated during fault conditions.
- **Rationale**: Selective coordination minimizes disruption to non-faulted portions of the facility, supporting OBJ-1 (Safe & Reliable Operation).
- **Source**: CEC Section 14 (protection); IEEE Std 242 (protection and coordination practices).
- **Reference**: DEL-17.03 (Design Calculations) includes protection coordination study.

**4. Grounding and Bonding**
- All electrical equipment, metallic structures, tanks, and piping shall be effectively grounded and bonded to a common grounding system.
- **Rationale**: Effective grounding provides personnel safety (limiting step/touch potentials), equipment protection (fault clearing), and lightning protection.
- **Source**: CEC Section 10 (grounding and bonding); IEEE Std 80 (grounding grid design); IEEE Std 142 (Green Book).
- Grounding grid design shall limit step and touch potentials to safe levels per IEEE Std 80 during ground fault conditions.

**5. Hazardous Area Compliance**
- Electrical equipment and wiring in areas where flammable vapors may be present (e.g., tank vents, loading arms, spill containment areas) shall comply with CEC Section 18 (hazardous locations).
- **Rationale**: Canola oil has a flash point above 200°C (not flammable at normal temperatures), but vapors during heating or spill scenarios require area classification assessment.
- **Source**: CEC Section 18; NFPA 497 (hazardous area classification).
- **TBD**: Hazardous area classification study to define zone/division boundaries — pending ER or separate study deliverable.

**6. Future Expandability (OBJ-8)**
- Electrical distribution equipment (switchgear, MCCs, panels) shall include spare capacity and spare ways to accommodate Phase 2 expansion.
- **Rationale**: Providing spares during initial installation is far more cost-effective than adding equipment or modifying systems later.
- **Source**: OBJ-8 (Future Expandability) — Decomposition Section 2.
- **ASSUMPTION**: Typical practice: 20-25% spare capacity in transformers and switchgear, 20-30% spare ways in panels and MCCs — **TBD** per ER requirements.

**Applicable Standards Context**:

| Standard | Key Principles |
|----------|----------------|
| **CSA C22.1 (CEC)** | Safety-focused prescriptive code; mandatory compliance for BC installations; governs conductor sizing, protection, grounding, wiring methods |
| **CSA C22.3 No. 7** | Underground systems and seismic requirements; governs duct bank design and equipment anchorage in high seismic zones (coastal BC) |
| **IEEE C2 (NESC)** | Utility coordination; governs clearances and safety for overhead and underground utility systems |
| **IEEE Std 80** | Grounding grid design methodology; step/touch potential analysis for personnel safety during fault conditions |
| **IEEE Std 141 (Red Book)** | Comprehensive guidance on industrial power distribution; voltage selection, load analysis, short circuit, protection coordination |
| **CSA Z462 / NFPA 70E** | Electrical workplace safety; arc flash hazard analysis, safety labeling, personal protective equipment (PPE) requirements |

## Considerations

**Factors to Consider During Development**:

**1. Load Characterization and Demand Factors**
- Identify all facility loads: motor loads (pumps, fans, heating circulation), process control, lighting, HVAC, marine loading arms, railcar unloading equipment.
- Apply appropriate demand factors (not all loads operate simultaneously) — typical industrial demand factor: 0.7-0.85.
- **Consideration**: Oversizing electrical distribution is costly; undersizing risks overloads and future limitations. Load analysis (DEL-17.03) is critical input.
- **Reference**: CEC Table 14 (demand factors); IEEE Std 141 Chapter 4 (load characteristics).

**2. Voltage Drop and Power Quality**
- Cable sizing must consider not only ampacity (current-carrying capacity per CEC Section 4) but also voltage drop.
- **Guideline**: Maximum voltage drop: 3% for feeders, 5% total (feeder + branch circuits) per IEEE recommendations; CEC permits up to 5% total but lower is preferable for motor starting and power quality.
- **Consideration**: Long cable runs (site is large — rail unloading area to tanks to marine loading) may require voltage drop analysis to avoid undersized cables.
- **Reference**: DEL-17.03 (Design Calculations — voltage drop analysis).

**3. Short Circuit and Fault Current**
- Available fault current at each point in the distribution system must be calculated to ensure protective devices and equipment can safely interrupt or withstand fault conditions.
- **Consideration**: MV service from utility may have very high available fault current (50-100 kA or more) — equipment must be rated accordingly (interrupting capacity, withstand ratings).
- **Reference**: DEL-17.03 (Design Calculations — short circuit analysis); IEEE Std 141 Chapter 4; CEC Section 14.

**4. Cable Routing and Installation Methods**
- Coordinate cable routing with civil (underground duct banks), structural (cable tray support), and other disciplines (avoid conflicts with piping, HVAC, etc.).
- **Consideration**: Underground vs. overhead vs. cable tray routing — trade-offs of cost, maintainability, flexibility, and physical constraints.
- **Assumption**: Industrial facility typically uses underground duct banks for major feeders (MV and large LV), cable tray for secondary distribution, conduit for branch circuits.
- **Reference**: CEC Section 12 (wiring methods).

**5. Seismic and Environmental Conditions**
- Coastal BC is high seismic zone — equipment anchorage and cable/conduit support must comply with seismic requirements.
- Marine/industrial environment — outdoor equipment must be rated for corrosive atmosphere (C4 or C5 per ISO 12944).
- **Consideration**: Seismic restraints add cost but are mandatory for code compliance and personnel safety.
- **Reference**: CSA C22.3 No. 7 (seismic); BC Building Code seismic provisions.

**6. Redundancy and Reliability (OBJ-1)**
- **TBD**: Determine critical loads that require backup power (emergency generator, UPS, or redundant feeders).
- **Consideration**: Facility throughput is 1,000,000 MT/a (OBJ-2) — extended electrical outages may impact commercial operations. Evaluate cost/benefit of standby generation for critical process loads (pumps, control systems, marine loading).
- **Assumption**: Utility service reliability in Fraser Surrey area is generally high (BC Hydro grid) — backup power may be limited to life safety systems (emergency lighting, fire alarm) unless ER specifies otherwise.

**7. Arc Flash Hazard and Electrical Safety (CSA Z462 / NFPA 70E)**
- Arc flash hazard analysis must be performed to determine incident energy levels at each electrical equipment location.
- **Consideration**: High available fault currents at MV switchgear and LV main distribution equipment can result in high arc flash hazard levels (requiring extensive PPE or remote operation).
- **Mitigation strategies**: Protective device settings optimization (fast tripping), arc-resistant switchgear (expensive but safer), remote racking/switching, PPE requirements.
- **Reference**: CSA Z462 (arc flash hazard analysis methodology); **TBD** — arc flash study may be separate deliverable or included in DEL-17.03.

**8. Coordination with Utility (BC Hydro)**
- Early coordination with BC Hydro is critical to determine:
  - Available service voltage and fault current
  - Service entrance location and metering requirements
  - Utility protection requirements (reclosing coordination, fault interruption time)
  - Service installation lead time (utility may require 6-12+ months for new MV service)
- **TBD**: Utility service agreement and technical requirements — **location TBD**.

**9. Constructability and Phasing**
- Design must consider construction sequencing and temporary power requirements during installation.
- **Consideration**: Facility construction may require temporary power for construction equipment before permanent electrical service is energized.
- **TBD**: Temporary power plan and construction sequencing — coordinate with construction manager.

**10. Lifecycle Cost (OBJ-9)**
- Electrical design decisions impact future operating and maintenance costs:
  - Equipment selection: Higher quality/reliability equipment has higher initial cost but lower maintenance and replacement costs
  - Cable sizing: Oversizing cables (beyond code minimum) reduces energy losses over facility life
  - Standardization: Using common equipment types/sizes reduces spare parts inventory
- **Consideration**: Balance initial capital cost against lifecycle operational cost per OBJ-9 (Lifecycle Cost Optimization).

## Trade-offs

**Competing Concerns to Evaluate**:

**1. Initial Cost vs. Reliability and Redundancy**
- **Trade-off**: Redundant transformers, backup generation, and N+1 configurations increase initial capital cost but improve reliability and reduce downtime risk.
- **Decision Factors**: Criticality of loads, cost of downtime, utility service reliability, Employer's risk tolerance.
- **TBD**: Redundancy requirements per Employer's Requirements — **location TBD**.

**2. Equipment Quality vs. Cost**
- **Trade-off**: Industrial-grade vs. commercial-grade equipment; premium brands vs. budget options.
- **Decision Factors**: Design life (25+ years), maintenance availability, harsh environment (marine/industrial), lifecycle cost (OBJ-9).
- **Recommendation**: Industrial-grade equipment suitable for continuous duty and corrosive environment — justified by 25-year facility life and maintenance cost savings.

**3. Voltage Drop Optimization vs. Cable Cost**
- **Trade-off**: Oversizing cables to reduce voltage drop below code maximum improves power quality and efficiency but increases cable material and installation costs.
- **Decision Factors**: Length of cable runs, load criticality (motors sensitive to low voltage), energy cost over facility life.
- **Recommendation**: Design for 3% feeder voltage drop (more conservative than 5% CEC maximum) for motor feeders and long runs — energy savings and motor performance justify additional cable cost.

**4. Underground vs. Overhead vs. Cable Tray Routing**
- **Trade-off**: Underground duct banks are expensive and inflexible (difficult to modify) but provide physical protection and clean appearance. Overhead or cable tray is cheaper and flexible but more visually intrusive and subject to weather/corrosion.
- **Decision Factors**: Site aesthetics, future modification needs, physical constraints (roadways, rail tracks), corrosion environment.
- **Assumption**: Industrial transload facility — functionality prioritized over aesthetics; cable tray for secondary distribution (flexibility), underground duct banks for MV and major LV feeders (protection and routing under roadways/rail).

**5. Standardization vs. Optimization**
- **Trade-off**: Standardizing equipment types (e.g., single MCC manufacturer, common panel sizes) simplifies procurement, training, and spare parts but may not be optimal for every application.
- **Decision Factors**: Operations and maintenance preference, spare parts inventory cost, construction schedule (single equipment supplier may have longer lead times if capacity is constrained).
- **Recommendation**: Standardize where practical (common equipment families) but allow optimization for unique or large equipment (transformers, main switchgear).

**6. Arc Flash Mitigation Strategies**
- **Trade-off**: Arc-resistant switchgear is significantly more expensive than standard switchgear but reduces arc flash hazard and improves personnel safety.
- **Alternative strategies**: Optimized protective device settings, remote operation (reduces personnel exposure), PPE requirements (lower cost but inconvenient for maintenance).
- **Decision Factors**: Available fault current, incident energy levels, frequency of maintenance/switching operations, safety culture, budget.
- **TBD**: Arc flash mitigation approach per Employer's safety requirements and CSA Z462 compliance strategy.

**7. Spare Capacity Allocation (OBJ-8)**
- **Trade-off**: Providing spare capacity for future expansion increases initial equipment cost but avoids costly future modifications.
- **Decision Factors**: Phase 2 expansion plans (scope, timeline, likelihood), cost of future modifications vs. initial oversizing.
- **Recommendation**: Design transformers and switchgear for Phase 1 + Phase 2 combined load (continuous rating); provide spare breaker/feeder positions (20-30% spares) for flexibility — moderate initial cost increase, significant future cost savings.

## Examples

**Reference Examples and Precedents**:

**1. Typical Industrial Electrical Distribution Architecture**

**ASSUMPTION** — example single line diagram (SLD) hierarchy for canola oil transload facility:

```
Utility Service (BC Hydro 25 kV or 13.8 kV)
  └─ MV Switchgear (metal-clad, arc-resistant)
      ├─ Feeder 1: Unit Substation #1 (1000-1500 kVA transformer, MV/600V)
      │   └─ LV Switchgear → MCCs → Railcar Unloading Pumps, Tank Heating Circulation Pumps
      ├─ Feeder 2: Unit Substation #2 (1000-1500 kVA transformer, MV/600V)
      │   └─ LV Switchgear → MCCs → Transfer Pumps, Marine Loading Pumps
      ├─ Feeder 3: Distribution Transformer (300-500 kVA, MV/480V)
      │   └─ 480V Switchgear → Distribution Panels → HVAC, miscellaneous loads
      ├─ Feeder 4: Lighting/Receptacle Transformer (150-300 kVA, MV/208V-120V)
      │   └─ 208V-120V Panelboards → Lighting, receptacles, small loads
      └─ Spare Feeder (future expansion)
```

**Note**: Actual configuration depends on load analysis (DEL-17.03) and Employer's Requirements — this is illustrative only.

**2. Cable Schedule Example**

| Circuit ID | Description | Voltage | Cable Size | Cable Type | Length (m) | Source | Destination | Protection | Conduit/Tray |
|------------|-------------|---------|------------|------------|-----------|--------|-------------|------------|--------------|
| MV-F1 | MV Feeder to Unit SS#1 | 25 kV | 1/C 4/0 AWG (3 conductors) | MV-105 EPR | 150 | MV Switchgear Bus A | Unit SS#1 Primary | 200A Fuse | Underground Duct Bank #1 |
| LV-F1-01 | Pump P-101 Feeder | 600V | 3/C 250 kcmil + 1/C 4 AWG (Gnd) | RW90 XLPE | 75 | MCC-1A, Starter 01 | Pump P-101 Motor Terminal Box | 150A Breaker | Cable Tray CT-1 |
| LP-101 | Lighting Panel LP-101 | 208V-120V | 3/C 2 AWG + 1/C 6 AWG (Gnd) | RW90 XLPE | 45 | LV Panelboard PNL-1 | Lighting Panel LP-101 | 100A Breaker | Conduit (underground) |

**3. Grounding Grid Layout Example**

**ASSUMPTION** — typical industrial facility grounding grid:
- Grid conductor: Bare copper 2/0 AWG or 4/0 AWG, buried 0.5-0.6 m depth
- Grid spacing: 10-20 m typical (closer spacing near equipment)
- Ground rods: Copper-clad steel, 3 m length, driven at grid intersections and equipment locations
- Connections: Exothermic welds (Cadweld or equivalent) for permanent, low-resistance connections
- Ground resistance target: < 5 ohms (typical industrial standard); verify by IEEE Std 80 analysis

**4. Hazardous Area Classification Example**

**ASSUMPTION** — canola oil facility (subject to site-specific study):
- **General areas**: Unclassified (canola oil flash point > 200°C, not flammable at ambient)
- **Tank vent areas**: Class I Division 2 or Zone 2 (15 m radius from vent openings) — possible flammable vapors during heating or venting
- **Spill containment areas**: Class I Division 2 or Zone 2 (within containment, extending 1 m above grade)
- **Marine loading arms**: Class I Division 2 or Zone 2 (15 m radius from connection points during product transfer)
- **Indoor pump rooms**: May require classification if inadequate ventilation
- **TBD**: Confirm with hazardous area classification study per CEC Section 18 and NFPA 497.

**5. Single Line Diagram (SLD) Best Practices**

**IEEE Std 141 (Red Book) recommendations**:
- Show all major equipment: switchgear, transformers, circuit breakers, fuses, MCCs, large motor starters
- Indicate equipment ratings: voltage, current, interrupting capacity (AIC or kA)
- Show protective device settings: breaker trip settings, fuse ratings, relay settings
- Indicate cable/conductor sizes for major feeders
- Show metering and instrumentation (CTs, PTs, kWh meters)
- Include equipment identification tags and drawing cross-references
- Provide one-line legend with symbols and abbreviations

**Reference Sources**:
- **Employer's Requirements**: **TBD** — Volume 2 Parts 1-3 (electrical sections) — **location TBD** — may include project-specific requirements, precedent drawings, or standards
- **IEEE Std 141 (Red Book)**: Comprehensive guidance with examples of industrial power distribution SLDs, equipment sizing, protection coordination
- **Similar facilities**: Other bulk liquid transload terminals (vegetable oil, petroleum products) — **TBD** — lessons learned and precedent designs
- Anticipated artifacts listed in _CONTEXT.md provide drawing set structure
