# Guidance: DEL-27.02 HAZOP Study Reports

## Purpose

This guidance document supports the development of **HAZOP Study Reports** for **PKG-27 Engineering Design**.

**Context:** Documents analysis and results for HAZOP study reports required for design verification and approvals (per _CONTEXT.md).

**Role in Project:** HAZOP (Hazard and Operability) studies are systematic, structured examinations of the canola oil transload facility design to identify and evaluate hazards and operability problems. HAZOP is a critical risk management tool that:
- Identifies potential safety hazards (personnel injury, fire, explosion, environmental release)
- Identifies operability issues that could impact throughput, reliability, or flexibility
- Informs design of safeguards (engineering controls, SIS, interlocks, alarms)
- Determines hazardous area electrical classification
- Supports regulatory compliance and Employer approval
- Provides foundation for safe operations, procedures, and training

**Deliverable Classification:**
- Type: Report
- Discipline: Design
- Responsible: D&B Contractor
- Submission stages: **TBD** — Preliminary at 30-60% design; Detailed at 90% design; Pre-commissioning review before startup

**Source:** _CONTEXT.md; Decomposition DEL-27.02; Datasheet.md; Specification.md

## Principles

### HAZOP Methodology Principles

**Principle 1: Structured Systematic Approach**
- HAZOP uses a structured, systematic methodology (IEC 61882) to ensure comprehensive hazard identification
- Process is broken into manageable "nodes" (sections of process with similar conditions)
- Guidewords (More, Less, No, Reverse, As Well As, Part Of, Other Than, etc.) are systematically applied to process parameters (Flow, Pressure, Temperature, Level, Composition, etc.) to identify deviations from design intent
- Structure ensures consistency, completeness, and traceability
- **Source:** Specification.md; **ASSUMPTION**: IEC 61882 methodology provides rigor and completeness

**Principle 2: Multi-Discipline Team-Based**
- HAZOP is a team activity, not an individual analysis
- Team brings diverse expertise: process design, mechanical, electrical, controls, safety, operations, maintenance
- Facilitated by experienced HAZOP leader who guides process and ensures methodology rigor
- Team discussions surface scenarios and insights that individuals might miss
- Team consensus on risk rankings and recommendations ensures buy-in
- **Source:** Specification.md (FR-2); **ASSUMPTION**: Team approach is fundamental to HAZOP effectiveness

**Principle 3: Design Intent as Baseline**
- HAZOP examines deviations from "design intent" — how the process is intended to operate under normal conditions
- Design intent is documented in P&IDs, PFDs, design basis (DEL-27.01), equipment datasheets, operating philosophy
- Deviations are explored: what happens if flow is "more than" design, "less than" design, "no" flow, "reverse" flow, etc.
- Understanding design intent is prerequisite for effective HAZOP
- **Source:** Specification.md (FR-3); Datasheet.md

**Principle 4: Identify Causes and Consequences**
- For each credible deviation, HAZOP identifies:
  - **Causes:** What could cause this deviation? (equipment failure, operator error, instrument malfunction, external event, etc.)
  - **Consequences:** What happens if this deviation occurs? (safety impact, environmental release, equipment damage, production loss, etc.)
  - **Existing safeguards:** What design features or procedures already exist to prevent or mitigate? (alarms, interlocks, relief valves, containment, etc.)
- Cause-consequence-safeguard linkage is core to HAZOP value
- **Source:** Specification.md (FR-1); **ASSUMPTION**: Cause-consequence analysis per IEC 61882

**Principle 5: Risk-Based Prioritization**
- Not all identified scenarios are equally significant
- Risk ranking (likelihood × consequence) prioritizes scenarios for action
- High-risk scenarios require recommendations for risk reduction to tolerable levels
- Low-risk scenarios may be accepted as-is or monitored
- Risk ranking criteria (matrix, definitions) must be defined and consistently applied
- **Source:** Specification.md (FR-5, PR-1); **ASSUMPTION**: Risk-based approach per ISO 31000

**Principle 6: Actionable Recommendations**
- HAZOP generates recommendations to reduce unacceptable risks
- Recommendations should be specific, actionable, and assigned (not vague suggestions)
- Recommendations may be: design changes, additional safeguards (SIS, interlocks, alarms), procedural controls, training, further analysis
- Recommendations are tracked as action items through design, construction, commissioning
- Follow-up HAZOP review verifies action item closure before facility startup
- **Source:** Specification.md (FR-6); **ASSUMPTION**: Closed-loop action item process

### Safety and Reliability Principles

**Principle 7: Inherent Safety Hierarchy**
- HAZOP recommendations should follow inherent safety hierarchy (per DEL-27.01 design philosophy):
  1. **Eliminate:** Remove the hazard entirely (change process, eliminate hazardous material)
  2. **Minimize:** Reduce hazard magnitude (reduce inventory, lower pressure/temperature)
  3. **Substitute:** Replace with less hazardous option (safer chemical, lower energy)
  4. **Moderate:** Control hazard conditions (containment, inert blanketing, temperature control)
  5. **Simplify:** Reduce complexity to reduce failure modes (simpler design, fewer failure points)
- Engineering controls preferred over administrative controls (procedures, training)
- Administrative controls are "last resort" when engineering solutions not feasible
- **Source:** Decomposition Section 2 (OBJ-1); **ASSUMPTION**: Inherent safety principles per CCPS guidelines and DEL-27.01

**Principle 8: Layers of Protection**
- Effective risk management uses multiple independent layers of protection
- Typical layers (from preventive to mitigative):
  1. Process design (inherent safety features)
  2. Basic process control system (BPCS — normal regulatory control)
  3. Alarms and operator intervention
  4. Safety Instrumented System (SIS) — automatic safety shutdown
  5. Physical protection (relief valves, rupture discs, containment)
  6. Emergency response (fire protection, spill response, evacuation)
- No single layer is 100% reliable; multiple layers provide defense-in-depth
- HAZOP identifies required layers for each scenario
- **Source:** **ASSUMPTION**: Layers of protection analysis (LOPA) principles; coordination with PKG-19 (SIS design)

**Principle 9: Facility Lifecycle Considerations**
- HAZOP considers all lifecycle phases: design, construction, commissioning, normal operation, maintenance, abnormal operation, emergency, decommissioning
- Operating modes to analyze: startup, steady-state operation, shutdown, mode transitions (tank storage to direct transfer), maintenance activities, upset conditions
- Human factors: operator errors, maintenance errors, communication failures
- External events: loss of utilities (power, instrument air, nitrogen), environmental events (seismic, flooding, extreme temperature)
- **Source:** Specification.md (FR-6 interface requirements); **ASSUMPTION**: Lifecycle HAZOP scope per industry best practice

### Hazardous Area Classification Principles

**Principle 10: Source-Based Classification**
- Hazardous area classification identifies locations where flammable/combustible atmosphere may be present
- Based on identification of "sources of release" — points where canola oil vapor or mist could escape
- Zone classification (Zone 0, 1, 2 per IEC or Division 1, 2 per NEC/CEC) based on:
  - Release frequency (continuous, likely during normal operation, unlikely/abnormal conditions only)
  - Release rate and duration
  - Ventilation (natural or mechanical)
  - Vapor density (lighter or heavier than air)
- Extent of classified area depends on release characteristics and dispersion modeling
- **Source:** Specification.md (FR-4); Datasheet.md; **ASSUMPTION**: CEC and API RP 505 methodology

**Principle 11: Conservative Classification for Safety**
- When uncertainty exists about release potential or ventilation effectiveness, classify conservatively (wider area, higher zone)
- Better to over-classify and install appropriate electrical equipment than under-classify and risk ignition
- Balance: excessive classification increases cost (all equipment in zone requires expensive rated enclosures); insufficient classification risks safety
- Engineering judgment and experience are essential
- **Source:** **ASSUMPTION**: Standard hazardous area classification practice balancing safety and cost

## Considerations

### Project-Specific HAZOP Considerations

**Canola Oil Product Characteristics:**
- **Combustible liquid:** Flash point ~300°C (572°F) — high flash point, not easily ignited at ambient temperature
- **Non-flammable at ambient:** Canola oil vapor pressure very low at normal temperatures; hazardous atmosphere unlikely at ambient conditions
- **Heated operations:** If canola oil is heated (for viscosity control, winterization, etc.), vapor generation and flammability risk increase; heated areas require more extensive hazardous area classification
- **Mist formation:** Canola oil mist (aerosol) can form during high-velocity leaks, spray scenarios, or agitation; mist can be combustible even below flash point
- **Food-grade product:** Contamination prevention considerations (material compatibility, cleaning, cross-contamination with non-food materials)
- **TBD** — Specific operating temperature range and heating requirements from design basis (DEL-27.01)
- **Source:** Decomposition Section 1.1; **ASSUMPTION**: CSD canola oil properties typical for vegetable oils; **TBD** — operating conditions

**Rail-to-Ship Transfer Facility Characteristics:**
- **Batch operations:** Railcar unloading is batch process (32 railcars at a time); marine loading is batch/semi-continuous (vessel size-dependent)
- **Mode flexibility:** Facility supports tank storage and direct rail-to-ship transfer; HAZOP must consider both modes and mode transitions
- **Large throughput:** 1,000,000 MT/year drives high flow rates, large piping, large pumps — failure consequences can be significant (large spills)
- **Large storage:** 3 × 15,000 MT tanks — large inventory means large potential release if containment fails
- **Marine interface:** Marine loading arms on waterfront; additional hazards from vessel operations, weather (high winds, waves), tidal variations, disconnection scenarios
- **TBD** — Operating philosophy for mode selection, transition procedures, simultaneous operations
- **Source:** Decomposition Section 1.1, Section 2 (OBJ-2, OBJ-3, OBJ-4); **ASSUMPTION**: Rail-to-ship transfer facility operational characteristics

**Fraser Surrey Terminal Location:**
- **Marine/waterfront environment:** Corrosive atmosphere (saltwater, humidity); may influence equipment reliability and failure rates
- **Existing terminal operations:** Facility must coexist with ongoing terminal commercial activities; HAZOP scenarios involving interaction with existing operations (shared utilities, shared access, emergency response coordination)
- **Seismic zone:** BC moderate-to-high seismic risk; seismic event scenarios in HAZOP (loss of containment, piping failures, tank damage, utility disruption)
- **Fraser River proximity:** Flooding risk considerations; environmental sensitivity (spill to river has major environmental consequence)
- **TBD** — Existing terminal interfaces, shared systems, emergency response coordination
- **Source:** Decomposition Section 1.1, Section 2 (OBJ-5, OBJ-7); **ASSUMPTION**: Site-specific hazards typical for Fraser River waterfront location

### HAZOP Timing and Staging

**Preliminary HAZOP (30-60% Design Stage):**
- **Purpose:** Identify major hazards early to inform design direction
- **Design maturity:** P&IDs may be preliminary; equipment sizes approximate; details TBD
- **Scope:** Focus on major systems, high-level process description, known major hazards
- **Value:** Early identification allows design changes when cost and schedule impact are minimal
- **Limitations:** Detailed scenarios may not be analyzable until design matures
- **Output:** High-level hazard identification, major recommendations to guide design
- **Source:** Specification.md (QR-4); **ASSUMPTION**: Preliminary HAZOP aligned with early design submission (30-60% per DEL-27.04)

**Detailed HAZOP (90% Design Stage):**
- **Purpose:** Comprehensive hazard analysis of mature design
- **Design maturity:** P&IDs near-final; equipment specified; control logic defined; instrumentation detailed
- **Scope:** All systems, all nodes, all guidewords, full cause-consequence-safeguard analysis
- **Value:** Final design hazard review; generates detailed recommendations for safeguards (SIS, interlocks, alarms, procedures)
- **Output:** Comprehensive HAZOP report, action item register, hazardous area classification
- **Source:** Specification.md (QR-4); **ASSUMPTION**: Detailed HAZOP aligned with late design submission (90% per DEL-27.04)

**Pre-Commissioning HAZOP Review:**
- **Purpose:** Verify HAZOP action items closed and as-built conditions match HAZOP assumptions
- **Design maturity:** As-built P&IDs; construction complete or substantially complete
- **Scope:** Review of action item register, walk-down verification, as-built changes review
- **Value:** Confirms facility is safe to commission and operate per HAZOP intent
- **Output:** Action item closure report, identification of any new issues from as-built changes
- **Source:** Specification.md (QR-4, VM-5); **ASSUMPTION**: Pre-commissioning HAZOP review before facility startup

**Post-Startup HAZOP Review (Optional):**
- **Purpose:** Capture lessons learned from commissioning and early operations
- **Timing:** After 3-6 months of operation
- **Scope:** Review of operating experience, near-misses, incidents, operability issues discovered during startup
- **Value:** Identifies hazards or operability issues not apparent during design HAZOP
- **Output:** Supplemental HAZOP recommendations based on operational experience
- **TBD** — Whether post-startup HAZOP review is in scope for DEL-27.02 or separate deliverable
- **Source:** **ASSUMPTION**: Post-startup HAZOP review is best practice but may be out of scope for design phase deliverable

### Multi-Discipline Coordination

**Design Basis Coordination (DEL-27.01):**
- HAZOP uses design basis as foundation; any gaps or ambiguities in design basis become apparent during HAZOP
- HAZOP findings may trigger design basis updates: revised assumptions, new constraints, additional safeguard requirements
- Bidirectional coordination: design basis informs HAZOP; HAZOP refines design basis
- **TBD** — Coordination mechanism and approval workflow for design basis changes triggered by HAZOP
- **Source:** Specification.md (IR-1); Datasheet.md

**Process and Mechanical Engineering Coordination (PKG-10 through PKG-16):**
- HAZOP recommendations flow to discipline deliverables: piping changes, equipment modifications, relief valve sizing, containment design, etc.
- Engineering teams provide feedback to HAZOP team on feasibility, cost, schedule impact of recommendations
- Iterative process: HAZOP identifies issue → engineering proposes solution → HAZOP reviews solution adequacy
- **TBD** — Recommendation tracking and closure workflow
- **Source:** Specification.md (IR-2)

**Control System and SIS Coordination (PKG-19):**
- HAZOP identifies Safety Instrumented Functions (SIFs): automatic actions required to prevent or mitigate hazardous scenarios
- SIF specification: what is being protected, what initiates action, what final element responds, required reliability (SIL)
- Control system design implements HAZOP-identified safeguards: interlocks, alarms, ESD logic
- SIL (Safety Integrity Level) determination may require additional analysis (LOPA) if high reliability required
- **TBD** — SIL determination methodology; LOPA scope
- **Source:** Specification.md (IR-3); **ASSUMPTION**: Coordination between HAZOP and SIS design per IEC 61508/61511

**Electrical Hazardous Area Coordination (PKG-17):**
- HAZOP-determined hazardous area classification drives electrical equipment selection
- Classified areas require explosion-proof, purged, or intrinsically safe equipment per CEC
- Iterative process: HAZOP identifies release sources → hazardous area classification determined → electrical design selects appropriate equipment → HAZOP reviews adequacy
- **Source:** Specification.md (IR-4); Datasheet.md

**Fire Protection Coordination (PKG-23, PKG-24):**
- HAZOP fire and explosion scenarios inform fire protection system design: fire detection, suppression, emergency response
- HAZOP identifies fire scenarios: ignition sources, combustible materials, fire propagation paths, consequences
- Fire protection design addresses HAZOP scenarios: automatic suppression, fire barriers, emergency shutdown, escape routes
- **Source:** Specification.md (IR-5)

**Operations and Training Coordination:**
- HAZOP identifies scenarios that require procedural controls (startup/shutdown procedures, emergency response, abnormal operation)
- Operating procedures developed based on HAZOP findings
- Training requirements identified: operator training on hazards, emergency response, abnormal situation management
- **TBD** — Operating procedures and training deliverables
- **Source:** Specification.md (IR-6)

### Regulatory and Compliance Considerations

**Canadian Regulatory Context:**
- **BC Occupational Health and Safety:** WorkSafeBC requirements for process safety, hazard assessment, risk management
- **Federal regulations:** Transport Canada (rail safety), Canadian Coast Guard (marine operations), Environment Canada (environmental protection)
- **Municipal:** City of Surrey regulations, permits, approvals
- **Port authority:** Vancouver Fraser Port Authority (VFPA) requirements for terminal operations, environmental protection, safety
- **TBD** — Specific regulations requiring HAZOP or equivalent hazard analysis; regulatory approval process for HAZOP
- **Source:** Decomposition Section 2 (OBJ-6); Specification.md (RC-1); **ASSUMPTION**: Multiple regulatory jurisdictions for BC marine terminal

**Employer Approval Requirements:**
- Employer (DP World Fraser Surrey Inc.) likely has corporate process safety standards and HAZOP requirements
- HAZOP reports submitted to Employer for review and acceptance at appropriate design stages
- Employer comments addressed; Employer acceptance required before proceeding
- **TBD** — Employer's HAZOP standards, review process, approval authority
- **Source:** Specification.md (RC-2, VM-7)

**Independent Design Verification (IDV) Considerations:**
- IDV (DEL-28.01) may include review of HAZOP study for adequacy, rigor, completeness
- IDV reviewer assesses: team qualifications, methodology compliance, technical content, recommendation appropriateness
- IDV findings may require HAZOP revisions or additional analysis
- **TBD** — Specific IDV scope and criteria for HAZOP
- **Source:** Specification.md (IR-7, VM-6)

## Trade-offs

### HAZOP Timing vs. Design Maturity

**Trade-off 1: Early HAZOP vs. Late HAZOP**
- **Early HAZOP (30-60% design):**
  - Advantages: Identifies major hazards when design changes are easier and cheaper; informs design direction
  - Disadvantages: Incomplete design means many scenarios cannot be fully analyzed; many TBDs; may need substantial rework as design matures
- **Late HAZOP (90% design or later):**
  - Advantages: Design mature enough for comprehensive analysis; fewer TBDs; more accurate consequences and safeguards
  - Disadvantages: Late identification of major hazards may require costly design rework; schedule pressure to avoid delaying project
- **Recommendation:** Multi-stage approach: Preliminary HAZOP at 30-60% to identify major issues early; Detailed HAZOP at 90% for comprehensive analysis; Pre-commissioning review to verify closure
- **Source:** Specification.md (QR-4); Datasheet.md; **ASSUMPTION**: Multi-stage HAZOP balances early identification with analysis rigor

### HAZOP Scope and Depth

**Trade-off 2: Comprehensive Scope vs. Focused Scope**
- **Comprehensive HAZOP:** Analyze all systems, all nodes, all guidewords exhaustively
  - Advantages: Thorough hazard identification; no major hazards missed
  - Disadvantages: Time-consuming, expensive; may generate too many low-value recommendations; "analysis paralysis"
- **Focused HAZOP:** Analyze high-hazard systems or critical nodes in detail; skim lower-hazard areas
  - Advantages: Efficient use of time and resources; focuses on high-impact scenarios
  - Disadvantages: Risk of missing hazards in "low-priority" areas; difficult to define focus boundary objectively
- **Recommendation:** Comprehensive scope for all major process systems (per Datasheet.md system list); focus team time on high-hazard nodes; experienced HAZOP leader can guide efficient analysis without sacrificing rigor
- **Source:** Datasheet.md (HAZOP scope); **ASSUMPTION**: Risk-based scoping balances thoroughness and efficiency

**Trade-off 3: HAZOP Detail Level**
- **Detailed node breakdown:** Many small nodes, each analyzed in detail
  - Advantages: Thorough, systematic, less chance of missing scenarios
  - Disadvantages: Time-consuming; may spend too much time on minor issues
- **High-level nodes:** Fewer, larger nodes
  - Advantages: Faster, focuses on big picture
  - Disadvantages: May miss detailed scenarios within large nodes
- **Recommendation:** Node size appropriate to system complexity: complex high-hazard systems (railcar unloading, marine loading) broken into detailed nodes; simpler systems (utilities, drainage) analyzed at higher level
- **Source:** **ASSUMPTION**: Node definition matched to system complexity per IEC 61882

### Risk Ranking and Acceptance

**Trade-off 4: Conservative Risk Ranking vs. Realistic Risk Ranking**
- **Conservative ranking:** Assume worst-case likelihood and consequence; rank many scenarios as high-risk
  - Advantages: Err on side of safety; comprehensive safeguards
  - Disadvantages: Over-design; many recommendations may not be cost-effective; "crying wolf" dilutes focus on truly high risks
- **Realistic ranking:** Use best estimate of likelihood and consequence based on experience and data
  - Advantages: Cost-effective risk management; focuses resources on genuine high risks
  - Disadvantages: Risk of under-estimating; relies on accuracy of data and judgment
- **Recommendation:** Use realistic risk ranking with clear criteria and definitions; document assumptions and uncertainties; for novel or uncertain scenarios, apply conservatism transparently
- **Source:** Specification.md (FR-5, PR-1); **ASSUMPTION**: Balanced risk ranking per ISO 31000

**Trade-off 5: Risk Tolerance and ALARP**
- **Zero-risk target:** Attempt to eliminate all risks, no matter how low
  - Advantages: Maximum safety
  - Disadvantages: Impossible and infinitely costly; diminishing returns
- **Risk-based acceptance:** Accept residual risks that are low and As Low As Reasonably Practicable (ALARP)
  - Advantages: Pragmatic, cost-effective, focuses on high risks
  - Disadvantages: Requires judgment on what is "tolerable" and "reasonably practicable"
- **Recommendation:** Define risk tolerance criteria explicitly (risk matrix with acceptance zones); high risks require reduction to medium or low; medium risks evaluated for ALARP; low risks generally accepted with monitoring
- **TBD** — Project-specific risk tolerance criteria from Employer or regulations
- **Source:** **ASSUMPTION**: ALARP principle per ISO 31000 and UK HSE guidance (widely adopted)

### Safeguard Selection

**Trade-off 6: Engineering Controls vs. Administrative Controls**
- **Engineering controls:** Hardware safeguards (SIS, interlocks, relief valves, containment, barriers)
  - Advantages: Reliable, always present, do not depend on human action
  - Disadvantages: Higher capital cost, add complexity, require maintenance
- **Administrative controls:** Procedures, training, permits, supervision, warnings
  - Advantages: Lower capital cost, flexible, can address broad range of scenarios
  - Disadvantages: Less reliable, depend on human compliance, can degrade over time
- **Recommendation:** Prefer engineering controls for high-consequence scenarios; administrative controls acceptable for low-risk scenarios or as supplementary layer; follow inherent safety hierarchy (Principle 7)
- **Source:** **ASSUMPTION**: Hierarchy of controls per CCPS and occupational safety best practice

**Trade-off 7: Passive vs. Active Safeguards**
- **Passive safeguards:** No moving parts, no actuation required (containment dikes, relief valves, fire walls, flame arrestors)
  - Advantages: High reliability, low maintenance, always ready
  - Disadvantages: Limited capability, cannot adapt to changing conditions
- **Active safeguards:** Require actuation (SIS, ESD valves, fire suppression systems)
  - Advantages: Can respond to complex scenarios, can be reset and reused
  - Disadvantages: Lower reliability (depend on detection, logic, actuation), require testing and maintenance
- **Recommendation:** Use passive safeguards where feasible (first line of defense); active safeguards for scenarios requiring dynamic response; combine layers (passive containment + active shutdown + administrative emergency response)
- **Source:** **ASSUMPTION**: Passive/active safeguard considerations per LOPA and process safety principles

### Hazardous Area Classification

**Trade-off 8: Extensive Classification vs. Minimal Classification**
- **Extensive classification:** Classify large areas as hazardous zones
  - Advantages: Conservative, reduces ignition risk
  - Disadvantages: High cost for rated electrical equipment (explosion-proof motors, lighting, instrumentation); operational constraints (hot work permits, ignition source control)
- **Minimal classification:** Classify only areas with clear, credible release potential
  - Advantages: Lower cost, fewer operational constraints
  - Disadvantages: Risk of under-classification if release scenarios are missed or under-estimated
- **Recommendation:** Classification based on rigorous analysis of release sources per CEC and API RP 505; use engineering controls to minimize release potential (sealed systems, ventilation) rather than compensating with extensive classification; document assumptions and uncertainties
- **Source:** Specification.md (FR-4); Datasheet.md; **ASSUMPTION**: Hazardous area classification optimization balancing safety and cost per API RP 505

## Examples

### HAZOP Node and Guideword Application Example

**Example 1: Railcar Unloading Pump Discharge — "No Flow" Deviation**

**Node:** Railcar Unloading Pump P-101 Discharge to Storage Tank T-101

**Design Intent:** Pump P-101 transfers canola oil from railcar to tank T-101 at 100 m³/hr when unloading

**Guideword:** No
**Parameter:** Flow
**Deviation:** No flow of canola oil from pump P-101 to tank T-101 when pump is running

**Causes:**
- Discharge valve closed (human error during startup)
- Discharge piping blocked (solidified product if cold, foreign object, closed isolation valve)
- Pump failure (mechanical failure, motor failure, loss of power)
- Suction strainer plugged (no flow to pump)
- Pump vapor-locked (air in suction line)

**Consequences:**
- **Safety:** Pump "dead-heading" → pressure rise → piping overpressure → potential rupture and spill
- **Equipment:** Pump overheating and damage; pressure relief valve lifts (if provided)
- **Operational:** Unloading operation stops; railcar cannot be unloaded; throughput impact

**Existing Safeguards:**
- Pressure relief valve PSV-101 on pump discharge (protects against overpressure, dumps to containment)
- High-pressure alarm PAH-101 on pump discharge (alerts operator)
- Pump motor current monitoring (high current may indicate dead-heading)

**Risk Ranking:** Medium (Likelihood: Possible; Consequence: Moderate — equipment damage, operational impact, spill to containment)

**Recommendations:**
1. Add pressure high-high interlock (PAHH-101) to automatically shut down pump P-101 on overpressure (reduces risk to Low) — **Action Item 001, assigned to Controls Lead, SIL determination TBD**
2. Include operating procedure for verifying discharge valve open before pump start — **Action Item 002, assigned to Operations, target: before commissioning**
3. Review adequacy of pressure relief valve PSV-101 sizing for pump dead-head scenario — **Action Item 003, assigned to Mechanical Lead, target: 90% design**

**Source:** **ASSUMPTION**: Typical HAZOP node analysis structure per IEC 61882; example scenario typical for pumped liquid transfer

**Example 2: Storage Tank T-101 — "High Level" Deviation**

**Node:** Storage Tank T-101

**Design Intent:** Tank T-101 stores canola oil at normal operating level 50-80% (7,500-12,000 MT); maximum capacity 15,000 MT

**Guideword:** More
**Parameter:** Level
**Deviation:** High level in tank T-101 exceeding normal maximum (> 80%)

**Causes:**
- Continued filling after tank nearly full (operator error, level instrument failure, control system failure)
- Inadvertent simultaneous filling from multiple sources (railcar unloading + tank-to-tank transfer)
- Level transmitter LT-101 failed low (indicates falsely low level, keeps filling)

**Consequences:**
- **Safety:** Tank overfill → product overflow from tank roof → large spill to secondary containment or environment (if containment breached) → environmental release to Fraser River (high environmental consequence)
- **Safety:** Personnel exposure if working near tank during overflow
- **Equipment:** Product contamination if overflow mixes with rainwater; tank structural overstress if overfilled significantly

**Existing Safeguards:**
- Level transmitter LT-101 with high-level alarm LAH-101 (alerts operator when 85% full)
- Secondary containment dike around tank (contains overflow, prevents environmental release)
- Manual observation (operator site visits)

**Risk Ranking:** High (Likelihood: Possible; Consequence: Major — large spill, potential environmental release to Fraser River)

**Recommendations:**
1. Add high-high level interlock (LAHH-101 at 90% full) to automatically close inlet valves and stop filling pumps (prevents overfill) — **Action Item 010, assigned to Controls Lead, SIL-2 recommended for environmental protection**
2. Add independent overfill protection: mechanical float switch or radar level transmitter as redundant high-high level detection — **Action Item 011, assigned to Instrumentation Lead**
3. Confirm secondary containment dike capacity is adequate for full tank overfill plus design storm rainfall (as per OBJ-7 environmental protection) — **Action Item 012, assigned to Civil Lead, target: 60% design**
4. Include overfill prevention procedures in operating manual and operator training — **Action Item 013, assigned to Operations**

**Source:** **ASSUMPTION**: Typical HAZOP tank overfill scenario; environmental consequence for Fraser River location per Decomposition Section 2 (OBJ-7)

### Hazardous Area Classification Example

**Example 3: Marine Loading Arm Area Classification**

**Source of Release:** Marine loading arm connection flange and swivel joints

**Product:** CSD canola oil (combustible liquid, flash point ~300°C)

**Release Scenario:**
- Normal operation: Occasional minor seepage or leakage at flanges/swivels (maintenance, connection/disconnection)
- Abnormal operation: Flange gasket failure, swivel seal failure, mechanical damage during vessel movement

**Release Characteristics:**
- Release rate: **TBD** — Order of magnitude: minor (< 1 kg/s) for normal seepage; moderate (1-10 kg/s) for gasket failure
- Release duration: Seconds to minutes (until detected and isolated)
- Ventilation: Open-air marine environment, good natural ventilation
- Vapor generation: At ambient temperature (~10-25°C), canola oil vapor pressure very low; minimal vapor generation; however, high-velocity jet or mist formation possible
- **TBD** — Operating temperature: if loading arm or product is heated, vapor generation increases significantly

**Zone Classification (Preliminary):**
- **Zone 1:** Within 1 meter radius of loading arm flanges, swivel joints, and coupling connection point (area where releases are likely during normal operations such as connection/disconnection)
  - Electrical equipment in Zone 1: Explosion-proof or purged enclosures per CEC
- **Zone 2:** Within 3 meter radius beyond Zone 1 boundary (area where releases are possible but unlikely, only under abnormal conditions)
  - Electrical equipment in Zone 2: Suitable for Zone 2 classification per CEC
- **Non-classified:** Beyond 3 meter radius, where adequate ventilation and low release potential result in negligible risk of combustible atmosphere
  - Electrical equipment: Standard industrial equipment

**Notes:**
- Classification assumes ambient temperature operations (~10-25°C); if product is heated above 100°C, classification extent may increase significantly — **TBD**
- Classification assumes good natural ventilation (open-air environment); if enclosures or buildings are added around loading arm, classification may change
- Hazardous area classification drawings to show Zone 1 and Zone 2 boundaries in plan and elevation views

**Source:** **ASSUMPTION**: Preliminary hazardous area classification per API RP 505 and CEC for combustible liquid loading; **TBD** — Detailed classification calculations and drawings; operating temperature confirmation

### HAZOP Recommendations and Action Items

**Example 4: HAZOP Action Item Register (Sample Entries)**

| ID | Recommendation | System | Priority | Assigned To | Target Date | Status | Closure Evidence |
|----|----------------|--------|----------|-------------|-------------|--------|------------------|
| 001 | Add PAHH-101 interlock to shut down pump P-101 on high discharge pressure (SIL TBD) | Railcar Unloading | High | Controls Lead (PKG-19) | 90% Design | Open | TBD |
| 002 | Operating procedure: verify discharge valve open before pump start | Railcar Unloading | Medium | Operations | Pre-commissioning | Open | TBD |
| 003 | Review PSV-101 relief valve sizing for pump dead-head scenario | Railcar Unloading | Medium | Mechanical Lead (PKG-14) | 90% Design | Open | TBD |
| 010 | Add LAHH-101 overfill protection interlock (SIL-2) to close inlet valves and stop pumps | Storage Tanks | High | Controls Lead (PKG-19) | 90% Design | Open | TBD |
| 011 | Add independent overfill detection (mechanical float switch or radar LT) | Storage Tanks | High | Instrumentation Lead (PKG-19) | 90% Design | Open | TBD |
| 012 | Confirm secondary containment dike capacity for tank overfill + storm rainfall | Storage Tanks | High | Civil Lead (PKG-03) | 60% Design | Open | TBD |
| 013 | Include overfill prevention in operating procedures and training | Storage Tanks | Medium | Operations | Pre-commissioning | Open | TBD |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Action Item Tracking Notes:**
- Priority: High (safety or environmental consequence), Medium (equipment or operational impact), Low (minor improvement)
- Status: Open (not started), In Progress (work underway), Closed (completed and verified)
- Closure evidence: Design change documented in P&IDs and specs, procedures issued and approved, training completed, etc.
- Follow-up HAZOP review before commissioning verifies all High and Medium priority items closed

**Source:** **ASSUMPTION**: Typical HAZOP action item register structure; examples consistent with scenarios above

### Lessons Learned and Best Practices

**Best Practice 1: Engage Operations Early**
- Include operations/maintenance personnel in HAZOP team (even if facility not yet built)
- Operations input on operating procedures, abnormal conditions, maintenance scenarios is invaluable
- Builds operations ownership of safety design; eases transition to operations phase
- **Source:** **ASSUMPTION**: Best practice for Design & Build HAZOP

**Best Practice 2: Manage HAZOP Schedule and Logistics**
- HAZOP sessions are intensive; limit to 3-4 hours per day to maintain team effectiveness
- Schedule sufficient sessions to cover all nodes without rushing (better to add sessions than rush and miss hazards)
- Book meeting rooms and team members well in advance; HAZOP is critical path for design
- **Source:** **ASSUMPTION**: HAZOP facilitation best practice per IEC 61882

**Best Practice 3: Integrate HAZOP with Design Process**
- Treat HAZOP as part of design, not separate external review
- HAZOP recommendations integrated into design deliverables (P&IDs, specs, datasheets, procedures)
- Design team owns closure of action items; HAZOP team reviews closure adequacy
- **Source:** **ASSUMPTION**: Integrated HAZOP approach for Design & Build projects

**Best Practice 4: Document Assumptions and Decisions**
- HAZOP quality depends on quality of design information (P&IDs, design basis, operating philosophy)
- Document key assumptions in HAZOP report; flag TBDs that may affect conclusions
- Document rationale for accepting residual risks (ALARP justification)
- Clear documentation supports Employer and regulatory approval
- **Source:** Specification.md (QR-2); **ASSUMPTION**: Documentation best practice per ISO 9001

**Source for Examples section:** **ASSUMPTION**: Typical HAZOP node analysis, hazardous area classification, and action item register examples for canola oil transload facility; illustrative of methodology and structure
