# Guidance: DEL-17.03 Electrical Power Design Calculations

## Purpose

This guidance document supports the development of **Electrical Power Design Calculations** for **PKG-17 Electrical Power Distribution**.

**Deliverable Purpose** (Source: Decomposition DEL-17.03 entry): Provides the engineering basis and sizing/verification calculations for electrical power.

**Downstream Use**:
- Equipment sizing (transformers, switchgear, MCCs, cables) for drawings (DEL-17.01) and specifications (DEL-17.02)
- Equipment procurement (calculations verify proposed equipment meets requirements)
- Equipment rating verification (data sheets checked against calculations)
- Regulatory compliance (BC Safety Authority permit review)
- Safety analysis (arc flash labels, protection coordination)

**Deliverable Classification**: Calculation, Electrical, D&B Contractor

## Principles

**1. Load Diversity and Demand Factors**
- **Principle**: Not all electrical loads operate simultaneously; demand factors account for load diversity
- **Rationale**: Sizing electrical distribution for 100% connected load is overly conservative and costly; applying realistic demand factors optimizes equipment sizing
- **Source**: IEEE Std 141 Chapter 4, CEC Table 14
- **Example**: 10 pumps × 100 HP each = 1000 HP connected load; with 0.75 demand factor = 750 HP demand load (typical for pumping stations where not all pumps run simultaneously)

**2. Fault Current Determination**
- **Principle**: Available fault current at each bus must be calculated to ensure protective devices can safely interrupt faults
- **Rationale**: Undersized protective devices (insufficient interrupting capacity) can fail catastrophically during fault conditions (personnel injury, equipment damage, fire)
- **Source**: IEEE Std 141 Chapter 4, ANSI/IEEE C37 series
- **Safety Margin**: Circuit breaker interrupting capacity typically 125% of calculated fault current

**3. Selective Coordination**
- **Principle**: Protective devices must be coordinated so only the device closest to the fault operates (isolates faulted circuit without affecting healthy circuits)
- **Rationale**: Selective coordination maximizes system reliability by minimizing outage extent (supports OBJ-1: Safe & Reliable Operation)
- **Source**: IEEE Std 242, IEEE Std 141 Chapter 5
- **Coordination Interval**: Minimum 0.2-0.3 seconds between upstream and downstream device operation

**4. Voltage Regulation**
- **Principle**: Voltage drop from source to load must be limited to ensure proper equipment operation
- **Rationale**: Excessive voltage drop causes motor overheating, reduced efficiency, starting problems; lighting flicker; control system malfunction
- **Source**: IEEE Std 141 Chapter 4, CEC Section 8
- **Limits**: 3% feeder, 5% total (IEEE recommendation; CEC permits 5% total but lower is better)

**5. Independent Verification**
- **Principle**: All engineering calculations must undergo independent check by qualified checker
- **Rationale**: Calculation errors can result in undersized equipment (safety hazard, code violation) or oversized equipment (cost waste)
- **Source**: Professional engineering practice, project quality standards
- **Check Methods**: Independent calculation (preferred) or detailed review

## Considerations

**1. Software vs. Hand Calculations**
- **Software (ETAP, SKM)**: Required for complex systems (short circuit with multiple sources, protection coordination, arc flash); faster and more accurate for iterative design
- **Hand Calculations**: Acceptable for simple circuits (single-source voltage drop, basic load summaries); good for verification spot-checks
- **Consideration**: Software requires model validation (verify model matches one-line diagram); hand calculations provide confidence check
- **Recommendation**: Use software for short circuit, coordination, arc flash; use Excel for load summaries and simple voltage drop

**2. Design Conservatism (Safety Margins)**
- **Transformer Sizing**: 20-25% spare capacity beyond calculated demand load (accommodates Phase 2 expansion per OBJ-8, load growth, future changes)
- **Circuit Breaker Ratings**: Interrupting capacity ≥ 125% of calculated fault current (industry practice)
- **Cable Sizing**: Size for both ampacity (CEC) and voltage drop (IEEE); use appropriate derating factors (temperature, conduit fill, grouping)
- **Trade-off**: Over-conservative design wastes cost; under-conservative design risks failure
- **Recommendation**: Follow IEEE Std 141 guidance (industry consensus on appropriate margins)

**3. Motor Starting and Inrush Current**
- **Consideration**: Motor starting inrush current (6× FLA for 6-10 seconds) must not trip protective devices
- **Impact**: Affects protective device settings (time delay required to ride through starting), voltage drop during starting (may require larger cables or reduced-voltage starters)
- **Solution**: Coordinate motor starter overload with upstream breaker; verify voltage drop during starting acceptable (typically 15-20% allowed for starting, returns to normal after motor accelerates)

**4. Power Factor and Reactive Power**
- **Consideration**: Inductive loads (motors, transformers) have lagging power factor (0.85-0.90 typical); affects transformer and cable sizing (kVA > kW)
- **Impact**: Lower power factor increases current for same kW load (I = kW / (√3 × V × PF)); may require larger cables and transformers
- **Solution**: Size equipment for kVA (apparent power) not just kW (real power); consider power factor correction (capacitors) if PF < 0.85 (reduces utility demand charges, improves voltage regulation)
- **TBD**: Confirm if power factor correction required per utility tariff

**5. Utility Coordination**
- **Critical Input**: BC Hydro available fault current and service voltage — required for short circuit analysis and equipment sizing
- **Lead Time**: Utility coordination may require several months (utility must perform studies)
- **Assumption Risk**: If utility data unavailable, must assume conservative (high) fault current — may result in oversized (expensive) switchgear
- **Recommendation**: Initiate utility coordination early in design phase

**6. Hazardous Area Electrical Equipment**
- **Consideration**: Equipment in Class I Division 2 or Zone 2 areas requires special ratings (may affect motor starting calculations, available equipment ratings)
- **TBD**: Hazardous area classification study required to define classified area boundaries
- **Impact**: Explosion-proof or purged equipment may have different performance characteristics than standard equipment

**7. Grounding System Design**
- **Consideration**: Grounding grid design (IEEE Std 80) requires soil resistivity data (field measurements)
- **Impact**: High soil resistivity requires larger grounding grid (more conductor, closer spacing) to achieve target resistance
- **TBD**: Soil resistivity measurements (geotechnical investigation or separate electrical survey)
- **Typical Target**: Grid resistance < 5 ohms (lower is better for safety and equipment protection)

**8. Arc Flash Hazard Analysis**
- **Consideration**: CSA Z462 requires arc flash hazard analysis and equipment labeling
- **Impact**: High incident energy levels may require expensive mitigation (arc-resistant switchgear, remote operation, extensive PPE, restricted access)
- **Factors Affecting Incident Energy**: Available fault current (higher fault = higher energy), protective device clearing time (faster clearing = lower energy), working distance
- **Mitigation Strategies**: Optimize protective device settings (fast clearing), specify arc-resistant switchgear, use remote racking/operation, implement maintenance safety procedures
- **TBD**: Confirm arc flash study included in this deliverable or separate

## Trade-offs

**1. Equipment Sizing: Conservatism vs. Cost**
- **Trade-off**: Oversizing equipment (high spare capacity) vs. right-sizing (minimal spare capacity)
- **Conservative (20-25% spare)**: Accommodates future loads, load growth, design uncertainties; higher initial cost
- **Minimal Spare**: Lower initial cost; may require future upgrades if loads increase
- **Recommendation**: 20-25% spare capacity for main distribution (transformers, switchgear) to support Phase 2 expansion (OBJ-8); minimal spare for end-use branch circuits (easier to add circuits than replace transformers)

**2. Voltage Drop Limits: Code Minimum vs. IEEE Recommendation**
- **Trade-off**: Design to CEC maximum (5% total) vs. IEEE recommendation (3% feeder, 5% total)
- **CEC Maximum (5% total)**: Smaller cables, lower cost; acceptable voltage regulation for most loads
- **IEEE Recommendation (3% feeder)**: Larger cables, higher cost; better voltage regulation, improved motor performance, lower energy losses
- **Recommendation**: IEEE recommendation (3% feeder) for motor feeders and long runs; CEC maximum acceptable for lighting and receptacle circuits

**3. Protection Coordination: Speed vs. Selectivity**
- **Trade-off**: Fast fault clearing (minimizes damage, arc flash energy) vs. selective coordination (isolates only faulted circuit)
- **Fast Clearing**: Lower incident energy, reduced equipment damage; may sacrifice selectivity (larger portion of system affected by fault)
- **Selective Coordination**: Better reliability (minimizes outage extent); slower clearing may increase arc flash hazard
- **Solution**: Optimize settings to achieve both (to extent possible); use zone-selective interlocking or directional relays where needed
- **Recommendation**: Prioritize selectivity for main distribution; accept faster (less selective) clearing for low-voltage branch circuits to reduce arc flash hazard

**4. Calculation Software: Purchase vs. Manual Methods**
- **Trade-off**: Invest in software (ETAP, SKM ~$10k-50k) vs. manual calculations (Excel, hand calcs)
- **Software**: Faster, more accurate for complex systems, industry-standard output (TCC plots); high initial cost, learning curve
- **Manual**: Lower cost, good for simple systems; time-consuming for complex systems, prone to errors
- **Recommendation**: Use software for projects with complex coordination or arc flash requirements; manual methods adequate for small simple projects

**5. Grounding Grid: Minimal vs. Comprehensive**
- **Trade-off**: Minimal grid (meets code minimum) vs. comprehensive grid (exceeds code, robust design)
- **Minimal**: Lower cost; meets code but limited safety margin
- **Comprehensive**: Higher cost; better personnel safety, lower grid resistance, better equipment protection
- **Recommendation**: Comprehensive grid for facility with high fault currents and personnel exposure (main substations); minimal grid acceptable for remote equipment locations

## Examples

**1. Load Calculation Example (Simplified)**

**Pump Station Load Summary**:
- 10 × 100 HP transfer pumps @ 480V (motor FLA = 124A each, PF = 0.87)
- Connected Load = 10 × 100 HP × 0.746 kW/HP / 0.87 PF = 857 kW, 985 kVA
- Demand Factor = 0.75 (assumption: max 7-8 pumps operate simultaneously)
- Demand Load = 985 kVA × 0.75 = 739 kVA

**Transformer Sizing**:
- Demand Load = 739 kVA
- Spare Capacity (20%) = 739 × 0.20 = 148 kVA
- Total = 739 + 148 = 887 kVA
- **Selected Transformer**: 1000 kVA (next standard size)

**2. Short Circuit Calculation Example (Simplified)**

**Given**:
- Utility fault current at service point: 25 kA (from BC Hydro)
- Transformer: 1000 kVA, 25 kV/600V, 5.75% impedance
- Cable from transformer to MCC: 3/C 250 kcmil copper, 50m length

**Transformer Secondary Fault Current**:
- Base kVA = 1000 kVA
- Secondary Voltage = 600V
- I_base = 1000 kVA / (√3 × 0.6 kV) = 962A
- Z_transformer = 5.75% = 0.0575 pu
- I_fault (transformer secondary) = I_base / Z_transformer = 962A / 0.0575 = 16,700A = 16.7 kA

**MCC Bus Fault Current (with cable impedance)**:
- Cable impedance reduces fault current (assume cable Z = 0.01 pu for 50m run)
- Z_total = Z_transformer + Z_cable = 0.0575 + 0.01 = 0.0675 pu
- I_fault (MCC bus) = 962A / 0.0675 = 14,250A = 14.3 kA
- **MCC SCCR Requirement**: ≥ 14.3 kA × 1.25 = 17.9 kA → specify 18 kA or 22 kA SCCR MCC

**3. Voltage Drop Calculation Example (Simplified)**

**Given**:
- Circuit: 480V, 3-phase, 100A load (motor), 75m cable run
- Cable: 3/C #2 AWG copper, R = 0.197 Ω/km, X = 0.079 Ω/km (from tables)
- Power Factor: 0.87 lagging (cos θ = 0.87, sin θ = 0.49)

**Calculation**:
- L = 0.075 km (75m)
- VD = √3 × I × (R cos θ + X sin θ) × L
- VD = 1.732 × 100A × (0.197 × 0.87 + 0.079 × 0.49) × 0.075 km
- VD = 1.732 × 100 × (0.171 + 0.039) × 0.075 = 2.73V
- VD% = 2.73V / 480V × 100% = 0.57%
- **Result**: 0.57% voltage drop < 3% limit → cable size acceptable

**4. Protection Coordination Example (Conceptual)**

**Protective Device Sequence** (from load to source):
1. **Motor Starter Overload**: Pickup = 115% of motor FLA, Time Delay = inverse time (EEMAC Class 20)
2. **MCC Feeder Breaker (600A frame MCCB)**: Pickup = 500A, Long-Time Delay = 10 sec @ 600% (3000A), Instantaneous = 5000A
3. **Transformer Secondary Main Breaker (1600A LVPCB)**: Pickup = 1600A, LSIG settings TBD for coordination
4. **Transformer Primary Fuse (200E)**: Time-current curve per manufacturer
5. **MV Switchgear Feeder Relay (50/51)**: Pickup = 300A (transformer primary current × 1.25), Time Dial = 3, Instantaneous = 3000A primary (reflects to ~30 kA secondary)

**Coordination Check**: Plot all devices on log-log TCC; verify minimum 0.3 sec interval between curves at all current levels

**Reference Sources**:
- IEEE Std 141 (Red Book) — Comprehensive examples of industrial power system calculations
- IEEE Std 242 (Buff Book) — Protection coordination examples and TCC plots
- IEEE Std 80 — Grounding grid design examples
- ETAP and SKM PowerTools — Software manuals with tutorial examples
- **TBD**: Employer's Requirements or precedent project calculations

---
**Cross-Document Alignment Verified (Pass 3):** Principles 1-5 and Considerations 1-8 align with Specification.md functional and quality requirements (FR-1 through FR-6, QR-1 through QR-4). Trade-offs and examples support engineering decisions reflected in Datasheet.md and Procedure.md. No conflicts identified.
