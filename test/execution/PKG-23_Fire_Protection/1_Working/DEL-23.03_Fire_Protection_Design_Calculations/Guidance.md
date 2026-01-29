# Guidance: DEL-23.03 Fire Protection Design Calculations

## Purpose

This guidance document supports the development of **Fire Protection Design Calculations** for **PKG-23 Fire Protection** within the Canola Oil Transload Facility — Phase 1 Design & Build project.

**Deliverable Purpose:**

Provides the engineering basis and sizing/verification calculations for fire protection systems, enabling:
- Determination of fire protection system performance requirements (flow rates, pressures, capacities)
- Sizing of fire protection equipment (piping, pumps, foam systems, fire alarm batteries)
- Verification of code compliance (NFPA 30, NFPA 24, NFPA 20, etc.)
- Technical basis for drawings (DEL-23.01) and specifications (DEL-23.02)
- Support for permitting and AHJ approval
- Documentation of engineering rationale for design decisions
- Source: Decomposition DEL-23.03 description and **ASSUMPTION** regarding calculation purpose

**Project Context:**
- **Project:** Canola Oil Transload Facility — Phase 1, Fraser Surrey Terminal, Surrey, BC
- **Deliverable Classification:** Calculation deliverable under Specialty discipline
- **Responsible Party:** D&B Contractor
- **Source:** Decomposition Section 1.1 and DEL-23.03 context

**Objective Alignment:**

This deliverable supports **OBJ-1: Safe & Reliable Operation** — calculations ensure fire protection systems are properly sized to meet safety and performance requirements.
- Source: Decomposition Section 2 (Project Objectives) and Section 6 (Objective-to-Deliverable Mapping)

## Principles

**Fire Protection Calculation Principles:**

**P-1: Code-Based Methodology**
- Fire protection calculations must follow methodologies prescribed by applicable NFPA codes (NFPA 30, NFPA 24, NFPA 20, NFPA 11, NFPA 16, NFPA 72)
- Where codes prescribe specific calculation methods, those methods shall be used (e.g., NFPA 30 fire water demand, NFPA 24 hydraulic analysis)
- Where codes do not prescribe methods, use recognized engineering methods and document basis
- Source: **ASSUMPTION**: Code-based design requirement for fire protection
- Application: Fire water demand per NFPA 30 methodology; hydraulic calculation per NFPA 24 methods

**P-2: Conservative Design Approach**
- Fire protection calculations should use conservative assumptions and safety factors
- Uncertainties addressed through conservatism (e.g., higher pipe roughness, lower available pressure, larger demand scenarios)
- Conservative design provides margin for unknowns and future conditions
- Source: **ASSUMPTION**: Fire protection engineering practice
- Application: Use conservative pipe roughness (C-factor), add safety margin to demands, design for worst-case scenarios

**P-3: Worst-Case Scenario Design**
- Fire protection systems designed for worst-case credible fire scenario per NFPA 30
- Typical worst case: largest single tank fire requiring foam suppression + cooling of adjacent tanks + hydrant streams for exposure protection + simultaneous operations (if applicable)
- Source: **ASSUMPTION**: NFPA 30 worst-case design approach
- Application: Fire water demand calculation considers largest tank plus exposures simultaneously

**P-4: Traceability and Documentation**
- All calculation inputs traceable to sources (drawings, codes, data sheets, site data)
- Assumptions clearly identified and justified
- Calculation steps documented for reproducibility and checking
- Source: **ASSUMPTION**: Engineering calculation standard
- Application: Cite sources for all input data, label assumptions, show calculation steps

**P-5: Independent Verification**
- Calculations independently checked by qualified engineer not the originator
- Critical or complex calculations verified using alternative methods or hand calculations
- Source: **ASSUMPTION**: Engineering quality control
- Application: Independent checker reviews all calculations; complex hydraulic calculations spot-checked with hand calculations

**P-6: Consistency with Design Documents**
- Calculation results must be consistent with drawings, specifications, and data sheets
- Iterative coordination as design develops (calculations inform drawings; drawings provide layout for calculations)
- Source: **ASSUMPTION**: Document set coordination
- Application: Pipe sizes in calculations match drawings; performance requirements in calculations match specifications

**P-7: Professional Engineering Responsibility**
- Fire protection calculations performed under responsible charge of Professional Engineer (P.Eng.)
- Engineer certifies calculations correct and code-compliant
- Source: **ASSUMPTION**: Professional engineering requirement for BC
- Application: P.Eng. signs and seals calculation packages (if required)

## Considerations

**Calculation Development Considerations:**

**C-1: Fire Water Demand Calculation Approach**
- NFPA 30 provides methodology for combustible liquid facility fire water demand
- Demand components typically include: (1) largest tank foam system, (2) cooling water for adjacent tanks, (3) hydrant streams for exposure protection, (4) marine/rail loading protection (if simultaneous)
- Duration typically 2–4 hours for combustible liquids depending on tank size and foam effectiveness
- Source: **ASSUMPTION**: NFPA 30 fire water demand methodology
- Impact: Fire water demand calculation structure and methodology

**C-2: Tank Foam System Sizing**
- NFPA 11 and NFPA 16 provide foam application rates for fixed foam systems on combustible liquid storage tanks
- Foam concentrate type affects application rate (AFFF, fluoroprotein, alcohol-resistant)
- Discharge duration typically 55 minutes for hydrocarbon foams, longer for alcohol-resistant foams
- Source: **ASSUMPTION**: NFPA 11/16 requirements
- Impact: Tank foam system calculations (foam concentrate storage, proportioning, discharge devices)

**C-3: Hydraulic Analysis Methodology**
- NFPA 24 requires hydraulic analysis to verify fire water system can deliver required flow and pressure
- Hazen-Williams equation commonly used for water systems (C-factor depends on pipe material and age)
- Analyze most hydraulically remote demand point (typically most distant hydrant or highest elevation point)
- Loop systems provide reliability; analyze loop with one section out of service
- Source: **ASSUMPTION**: NFPA 24 and hydraulic analysis practice
- Impact: Hydraulic calculation methodology and assumptions

**C-4: Fire Pump Sizing (if required)**
- NFPA 20 requires fire pump sized at 150% of demand at rated pressure
- Fire pump curve must meet or exceed system demand curve
- Electric or diesel driver selection based on power availability and reliability requirements
- Source: **ASSUMPTION**: NFPA 20 fire pump sizing requirements
- Impact: Fire pump calculation and selection

**C-5: Pipe Roughness and Friction Factors**
- Pipe roughness (Hazen-Williams C-factor) significantly affects friction loss calculations
- New ductile iron: C=140; new steel: C=120; aged pipes have lower C-factors
- Use conservative C-factors to account for aging and fouling over design life
- Source: **ASSUMPTION**: Hydraulic calculation practice
- Impact: Hydraulic calculation accuracy and conservatism

**C-6: Available Fire Water Supply**
- Fire water supply source (municipal supply, Employer's system, dedicated fire pump from source) must be characterized (available flow and pressure)
- Municipal supply: coordinate with utility for flow/pressure data (static, residual at demand)
- Fire pump from source: pump curve and suction source characteristics
- Source: **ASSUMPTION**: Fire water supply data requirement
- Impact: Hydraulic calculation starting point; fire pump sizing (if required)

**C-7: Simultaneous Demands**
- Determine if multiple fire demands can occur simultaneously (e.g., tank fire + marine loading fire)
- NFPA 30 generally requires worst single event, but simultaneous operations may be credible in large facilities
- Balance conservatism with practicality and risk assessment
- Source: **ASSUMPTION**: Fire demand scenario analysis
- Impact: Total fire water demand may increase if simultaneous demands credible

**C-8: Foam Concentrate Type Selection**
- Canola oil (Class IIIA combustible liquid) requires alcohol-resistant foam (AR-AFFF) or fluoroprotein foam
- Foam type affects application rate, storage volume, and proportioning method
- Foam concentrate freeze protection required for BC climate (heating/insulation of storage tank)
- Source: **ASSUMPTION**: Foam selection for combustible liquid
- Impact: Foam system calculations (application rate, storage volume, freeze protection)

**C-9: Fire Alarm Battery Capacity**
- NFPA 72 requires fire alarm battery capacity sized for 24-hour standby + 5-minute alarm (or longer per code/project requirements)
- Battery load includes control panel, detection devices, notification devices during alarm
- Source: **ASSUMPTION**: NFPA 72 battery capacity requirements
- Impact: Fire alarm battery sizing calculation

**C-10: Calculation Software Selection**
- Hydraulic analysis software (AFT Fathom, PIPE-FLO, AutoSPRINK) provides efficient hydraulic network analysis
- Software must be validated (compare to hand calculations, benchmark problems)
- Software version documented; calculations reproducible
- Source: **ASSUMPTION**: Calculation software practice
- Impact: Calculation efficiency, accuracy, documentation

**C-11: Design Changes and Calculation Updates**
- Design changes during development (tank sizes, pipe routing, equipment changes) require calculation updates
- Calculation revision control important to avoid using superseded calculations
- Source: **ASSUMPTION**: Design change management
- Impact: Calculation revision procedures, version control

**C-12: AHJ Requirements and Local Practices**
- Local fire marshal or authority may have specific calculation requirements or review practices
- Coordinate early with AHJ to understand submittal requirements and review criteria
- Source: **ASSUMPTION**: AHJ coordination
- Impact: Calculation format, documentation, submittal process

## Trade-offs

**T-1: Fire Water Demand Conservatism**
- **Option A:** Conservative demand (larger foam systems, more cooling water, more hydrants, longer duration) — higher capital cost (larger pumps, pipes, foam storage), greater safety margin
- **Option B:** Optimized demand (code-minimum or risk-based reduction) — lower capital cost, less safety margin, requires detailed risk assessment and justification
- **Trade-off:** Capital cost vs. safety margin vs. insurance/liability considerations
- **Decision Factors:** Risk tolerance, insurance requirements, Employer requirements, project budget
- **Status:** **TBD** — to be determined based on risk assessment, Employer requirements, and budget
- Source: **ASSUMPTION**: Fire protection design trade-off

**T-2: Hydraulic Analysis Detail Level**
- **Option A:** Detailed hydraulic network model (all pipes, valves, elevation changes modeled) — more accurate, identifies bottlenecks, longer to develop
- **Option B:** Simplified hydraulic analysis (critical path analysis, simplified network) — faster, less accurate, may miss local pressure issues
- **Trade-off:** Analysis accuracy and detail vs. engineering effort
- **Recommendation:** Detailed network model for final design; simplified analysis acceptable for conceptual design
- Source: **ASSUMPTION**: Hydraulic analysis approach trade-off

**T-3: Fire Pump Selection**
- **Option A:** Electric motor-driven fire pump — lower maintenance, requires reliable electrical power, no emissions
- **Option B:** Diesel engine-driven fire pump — independent of electrical power, higher maintenance, emissions, fuel storage
- **Option C:** Electric primary + diesel backup — highest reliability, highest capital and maintenance cost
- **Trade-off:** Reliability vs. capital cost vs. operating cost vs. maintenance
- **Decision Factors:** Electrical power reliability, Employer/insurance requirements, project budget
- **Status:** **TBD** — to be determined based on power reliability and requirements
- Source: **ASSUMPTION**: Fire pump driver selection trade-off

**T-4: Calculation Verification Method**
- **Option A:** Full independent recalculation by checker — most thorough, highest checking effort
- **Option B:** Spot-check calculation by checker (verify methodology, check key inputs/outputs, verify assumptions) — efficient, relies on checker judgment
- **Option C:** Software validation + spot-check — validates software accuracy, then spot-checks application
- **Trade-off:** Verification thoroughness vs. checking effort
- **Recommendation:** Software validation (one-time) + spot-check for routine calculations; full independent recalculation for critical/complex calculations
- Source: **ASSUMPTION**: Calculation checking trade-off

**T-5: Foam System Redundancy**
- **Option A:** Single foam proportioning system (code-minimum) — lower cost, single point of failure
- **Option B:** Redundant foam proportioning systems — higher cost, higher reliability, meets OBJ-1 (Reliable Operation)
- **Trade-off:** Capital cost vs. system reliability
- **Decision Factors:** Reliability requirements (OBJ-1), insurance requirements, risk tolerance
- **Status:** **TBD** — to be determined based on reliability analysis and requirements
- Source: **ASSUMPTION**: System reliability trade-off

## Examples

**E-1: Employer's Requirements**
- Refer to Employer's Requirements Volume 2 Parts 1–3 for project-specific fire protection design criteria, fire water demand basis, and calculation requirements
- Location: `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf`
- **Note:** Per INIT.md instruction, do not attempt to read ER files at this stage; reference them as inputs for future working sessions
- Source: Decomposition Section 3 (Reference Documents)

**E-2: NFPA 30 Fire Water Demand Example**
- NFPA 30 Chapter 16 provides fire protection requirements for storage tanks
- NFPA 30 Table 16.4.5.3 provides foam application rates for various combustible liquid classes
- NFPA 30 Section 16.6 provides exposure protection (cooling water) requirements
- Source: **ASSUMPTION**: NFPA 30 calculation methodology (location TBD — requires access to NFPA 30)

**E-3: NFPA 24 Hydraulic Calculation Example**
- NFPA 24 Annex C provides example hydraulic calculations for fire water systems
- Shows Hazen-Williams friction loss calculation, elevation head, velocity head, pressure drop through fittings/valves
- Source: **ASSUMPTION**: NFPA 24 includes calculation examples (location TBD)

**E-4: Hydraulic Analysis Software Output**
- Hydraulic analysis software produces system model, pressure/flow results, system curve, pump curve overlay
- Software output included as appendix to hydraulic calculation package
- Source: **ASSUMPTION**: Standard hydraulic software output

**E-5: Foam System Vendor Calculation Tools**
- Foam equipment manufacturers provide calculation tools and design guides for foam systems
- Vendor calculations may supplement engineer's calculations but do not replace professional engineer responsibility
- Source: **ASSUMPTION**: Vendor design support

**E-6: Fire Pump Manufacturer Pump Curves**
- Fire pump manufacturers provide pump performance curves (flow vs. head)
- Engineer selects pump from manufacturer curves to meet demand
- Pump curve included in fire pump sizing calculation
- Source: **ASSUMPTION**: Fire pump selection process

**E-7: Anticipated Calculation Artifacts**
- Fire water demand calculations — determines total fire water demand for facility
- Hydraulic calculations — verifies fire water system can deliver demand
- Source: Decomposition DEL-23.03 anticipated artifacts

**E-8: Related Calculation Examples (from other disciplines)**
- Structural calculations for fire pump/foam tank supports (PKG-06)
- Electrical load calculations for fire pump power (PKG-17)
- Source: **ASSUMPTION**: Interdisciplinary calculation coordination

## Conflict Table (for human ruling)

No conflicts identified at this stage of document development.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| *(none at INITIALIZED state)* | | | | | | |

**Note:** Conflicts that arise during calculation development (e.g., between code requirements, Employer's Requirements, and design constraints) will be documented here for human ruling.
