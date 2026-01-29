# Guidance: DEL-21.01 Building Design Drawing Set

## Purpose

This guidance document supports the development of **Building Design Drawing Set** for **PKG-21 Building Structures & Envelope**.

**Deliverable Purpose:** Defines the design arrangement and details for building per ER requirements.

**Source:** Decomposition document line 513

**Deliverable Classification:**
- **Type:** Drawing
- **Discipline:** Buildings
- **Responsible:** D&B Contractor

**Source:** `_CONTEXT.md`

**Role in Project:**

This deliverable provides the primary design documentation for the MCC building and operator shelters, establishing:
- Building layouts and spatial organization
- Structural systems and framing
- Envelope systems (walls, roofing, cladding)
- Foundation interfaces
- Openings (doors, windows)

The drawings serve as the basis for:
- Building technical specifications (DEL-21.02)
- Structural design calculations (DEL-21.03)
- Shop/fabrication drawings (DEL-21.06)
- Building MEP design (PKG-22)
- Construction and installation (DEL-21.05)

**Project Objectives Supported:**

- **OBJ-1: Safe & Reliable Operation** — Buildings provide safe, weather-protected enclosures for electrical equipment (MCC building) and personnel (operator shelters)
- **OBJ-5: Terminal Continuity** — Building design and construction approach minimizes disturbance to existing terminal operations
- **OBJ-6: Regulatory Compliance** — Buildings comply with NBC 2020, provincial building code, and all applicable standards
- **OBJ-9: Lifecycle Cost Optimization** — Building design considers durability, maintainability, and operating costs (energy performance, corrosion resistance)

**Source:** Decomposition Section 2 (Project Objectives); objectives mapped based on building function and scope

## Principles

**Governing Engineering Principles:**

### P1: Code Compliance and Regulatory Framework

Canadian building design is governed by a comprehensive code framework:
- **NBC 2020** establishes minimum performance requirements for fire safety, structural adequacy, envelope performance, and accessibility
- Provincial building codes adopt and may modify NBC provisions — **TBD**: Confirm British Columbia Building Code (BCBC) specific amendments
- Local authorities having jurisdiction (AHJs) enforce building codes through permit and inspection processes

**Design Intent:** All building design drawings must demonstrate compliance with NBC 2020 and applicable provincial/local amendments. Code compliance is verified through design review and documented in design calculations (DEL-21.03).

**Source:** NBC 2020 (regulatory framework for building design in Canada)

### P2: Structural Safety and Load Resistance

Buildings must resist all applicable loads without exceeding structural capacity:
- **Dead loads:** Self-weight of structure and permanent building components
- **Live loads:** Occupancy loads, equipment loads, maintenance access loads
- **Snow loads:** NBC 2020 climatic data for Surrey, BC — **TBD**: Confirm ground snow load and roof snow load factors
- **Wind loads:** NBC 2020 wind pressure provisions or wind tunnel study for structures sensitive to wind effects
- **Seismic loads:** NBC 2020 seismic design provisions for Western Canada (seismic zone) — **TBD**: Site-specific seismic hazard parameters

**Design Intent:** Structural systems (framing, foundations, connections) are sized and detailed to resist factored load combinations per NBC 2020 Part 4 and CSA structural standards (A23.3 for concrete, S16 for steel).

**Source:** NBC 2020 Part 4; CSA A23.3; CSA S16

### P3: Envelope Performance and Environmental Separation

Building envelope must control:
- **Heat transfer:** Thermal resistance (R-value) per NBC 2020 Part 5 or ASHRAE 90.1 (if energy code applies)
- **Air leakage:** Air barrier system per NBC 2020 Part 5
- **Water penetration:** Rain screen or barrier wall systems with drainage provisions
- **Vapor diffusion:** Vapor control layer positioned to prevent condensation in envelope assemblies

**Climate Context:** Fraser Surrey Terminal is in coastal BC climate zone (mild, wet winters; moderate summers). Envelope design must address:
- High annual precipitation and driving rain exposure
- Marine/industrial corrosion exposure
- Freeze-thaw cycling (if exterior water trapped in assemblies)

**Design Intent:** Envelope systems are detailed to provide durable, low-maintenance performance in coastal industrial environment.

**Source:** NBC 2020 Part 5; ASHRAE 90.1; climate considerations based on Fraser Valley location

### P4: Fire Safety Strategy

Fire safety design follows NBC 2020 objectives-based approach:
- Limit fire spread and structural collapse
- Provide safe egress for building occupants
- Facilitate fire department access and firefighting

**Building Classification Factors (TBD):**
- Occupancy classification (industrial Group F typical for MCC buildings and operator shelters)
- Building height and area
- Construction type (combustible vs. non-combustible)
- Fire resistance ratings (if required)

**Design Intent:** Fire safety provisions (egress, fire separations, construction type) are determined through NBC 2020 Part 3 analysis and documented in drawings.

**Source:** NBC 2020 Part 3 (Fire Protection, Occupant Safety, and Accessibility)

### P5: Accessibility and Barrier-Free Design

Buildings with public or employee access must comply with NBC 2020 Part 3 Div B Section 3.8 (Barrier-Free Design):
- Accessible building entrances
- Accessible routes within buildings
- Door clearances and hardware (lever handles, appropriate opening force)
- **TBD**: Applicability to MCC building and operator shelters (depends on occupancy patterns and AHJ interpretation)

**Design Intent:** Accessibility provisions are integrated into building layout and door/hardware selections.

**Source:** NBC 2020 Part 3 Div B Section 3.8; CSA B651

### P6: Coordination and Interface Management

Building drawings interface with multiple disciplines:
- **Civil/site:** Building locations, finish grades, site drainage, access
- **Structural:** Foundation design, load transfer, geotechnical constraints
- **Mechanical/electrical/plumbing (MEP):** Space planning, equipment clearances, penetrations, roof-mounted equipment
- **Process/equipment:** MCC equipment layout, cable entry/exit, ventilation/cooling requirements
- **Hazardous area classification:** Ventilation, non-sparking requirements (if applicable)

**Design Intent:** Interdisciplinary coordination checks (IDC) are performed to resolve conflicts and ensure interface compatibility before drawings are issued.

**Source:** Multi-discipline project coordination requirements; dependencies coordinated externally per `_DEPENDENCIES.md`

### P7: Constructability and Practicality

Building design must be constructable with available materials, labor, and equipment:
- **Modular construction:** Pre-engineered or modular building systems can accelerate schedule and improve quality control (common for industrial MCC buildings)
- **Material availability:** Standard building materials and systems reduce cost and schedule risk
- **Construction access:** Site constraints and existing terminal operations affect construction sequencing and logistics (OBJ-5: Terminal Continuity)
- **Weather protection:** Construction schedule considers Fraser Valley wet season

**Design Intent:** Design approach balances performance requirements with constructability, cost, and schedule considerations. Construction sequencing and terminal continuity requirements influence building system selections.

**Source:** Design-build project delivery context; OBJ-5 (Terminal Continuity) from decomposition Section 2

## Considerations

**Factors to Consider During Drawing Development:**

### C1: MCC Building Specific Considerations

**Function:** Motor Control Center (MCC) building houses electrical distribution equipment serving the facility.

**Space Planning:**
- Equipment layout and clearances per electrical equipment manufacturer requirements — **TBD**
- Maintenance access aisles and equipment removal provisions
- Cable entry/exit points and cable routing
- Ventilation and cooling requirements for electrical equipment heat dissipation — **TBD**
- Lighting for equipment operation and maintenance
- **TBD**: Control room or operator workspace (if included in MCC building)

**Environmental Control:**
- Heating/cooling to maintain equipment operating temperature range — **TBD**
- Humidity control (if required for electrical equipment) — **TBD**
- Dust/contamination control (filtration, positive pressure, sealed envelope)

**Electrical Considerations:**
- **TBD**: Equipment grounding and bonding requirements
- **TBD**: Lightning protection (if required for building or equipment)
- **TBD**: Emergency lighting and exit signs

**Security and Access:**
- Controlled access to electrical equipment (keyed or electronic access control)
- Integration with facility security system (PKG-24) — **TBD**
- **TBD**: Windows (if any — may be omitted for security or temperature control)

**Source:** MCC building function; typical electrical building design considerations; PKG-24 (Security Systems)

### C2: Operator Shelter Specific Considerations

**Function:** Weather-protected shelters for personnel operating railcar connection/disconnection during unloading operations.

**Location and Number:**
- 32 railcar unloading stations per decomposition Section 1.1 — **TBD**: Number of shelters (one per station, one per multiple stations, or centralized shelter strategy?)
- Proximity to railcar unloading points for personnel efficiency and safety
- **TBD**: Shelter size (one-person vs. multi-person capacity)

**Environmental Protection:**
- Protection from rain, snow, wind during railcar connection operations
- **TBD**: Heating (portable heater, fixed heating, or passive shelter only?)
- **TBD**: Lighting (natural light via windows, or artificial lighting required?)
- **TBD**: Ventilation (natural or mechanical)

**Operational Considerations:**
- Visibility of railcar unloading operations from shelter
- Communication provisions (intercom, radio, phone) — **TBD**
- **TBD**: Tool/equipment storage within shelter
- Egress in emergency situations

**Structural Considerations:**
- Anchorage to track or adjacent structure
- Wind load resistance (exposed location)
- Impact resistance (proximity to rail operations)
- **TBD**: Portability/relocatability (permanent vs. temporary/moveable shelters?)

**Source:** Decomposition Section 1.1 (32 railcar unloading stations); operator shelter function inferred from railcar unloading operations

### C3: Site and Climate Considerations

**Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC

**Climate Characteristics (Fraser Valley Coastal BC):**
- Mild, wet winters (November–March high precipitation)
- Moderate summers
- Freeze-thaw cycling potential
- Wind exposure (coastal location)
- **TBD**: Design temperatures, wind speeds, snow loads (NBC 2020 climatic data for Surrey, BC)

**Site Constraints:**
- Active marine terminal — construction and building locations must minimize disturbance to existing operations (OBJ-5)
- **TBD**: Soil conditions and bearing capacity (geotechnical investigation input)
- **TBD**: Site grading and drainage patterns
- **TBD**: Existing underground utilities and above-ground obstructions
- **TBD**: Marine/coastal corrosion exposure (salt spray, humidity)

**Design Responses:**
- Corrosion-resistant materials and coatings (marine-grade or galvanized finishes)
- Envelope drainage and water management (sloped roof, gutters/downspouts, splash pads)
- Foundation design responsive to geotechnical conditions
- Construction logistics considering terminal operations continuity

**Source:** Decomposition Section 1.1 (project location); OBJ-5 (Terminal Continuity); Fraser Valley climate characteristics

### C4: Design-Build Contract Delivery Considerations

**Contract Type:** Design & Build (D&B Contractor responsible for design and construction)

**Implications for Drawing Development:**
- **Early contractor involvement:** Contractor design team can optimize for constructability, cost, and schedule
- **Single-point responsibility:** D&B Contractor owns coordination between design and construction
- **Value engineering opportunities:** Design approach can incorporate contractor means and methods expertise (e.g., modular building systems, prefabrication)
- **ER compliance:** Design must comply with Employer's Requirements (ER) performance criteria — **TBD**: Review ER Volume 2 Part 3 (Building Works) for specific requirements

**Design Approach:**
- Establish design criteria and performance requirements early (basis of design documentation)
- Engage building system suppliers/manufacturers for design-assist input (if modular or pre-engineered systems)
- Coordinate with construction planning for phasing, access, and terminal continuity
- Document design decisions and ER compliance in design calculations and specifications

**Source:** Decomposition Section 1 (contract type: Design & Build); D&B project delivery best practices

### C5: Lifecycle and Maintainability Considerations

**OBJ-9: Lifecycle Cost Optimization** — "The design minimizes future operating and maintenance costs"

**Design for Maintainability:**
- Durable, corrosion-resistant materials reduce maintenance frequency
- Accessible building envelope components (roof access, facade maintenance provisions)
- Replaceable building components (windows, doors, roofing membranes) with reasonable service life
- **TBD**: Maintenance access provisions (roof hatches, fixed ladders, anchor points for fall protection)

**Energy Efficiency (if conditioned space):**
- High-performance envelope (insulation, air sealing) reduces heating/cooling energy
- ASHRAE 90.1 compliance (if energy code applies) — **TBD**
- Daylighting and efficient lighting systems (if occupied spaces)

**Design Life:**
- **TBD**: Target design life (25 years, 50 years typical for industrial structures?)
- Material selections based on expected service life in marine/industrial environment

**Source:** Decomposition Section 2 (OBJ-9); lifecycle cost optimization principles

### C6: Regulatory and Permitting Considerations

**OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements"

**Building Permit Requirements:**
- **TBD**: Authority having jurisdiction (City of Surrey, BC?)
- **TBD**: Building permit submission requirements (drawings, calculations, specifications, design professional seal)
- **TBD**: Review and approval timeline
- **TBD**: Inspection hold points during construction

**Design Professional Seal:**
- **TBD**: Professional engineer (P.Eng.) seal required for structural design in BC
- **TBD**: Architect seal requirements (depends on building classification and AHJ)

**Other Permits/Approvals:**
- **TBD**: Development permit (if required)
- **TBD**: Fire department review and approval
- **TBD**: Occupancy permit requirements (post-construction)

**Source:** Decomposition Section 2 (OBJ-6); BC building regulatory framework

### C7: Future Expandability Considerations

**OBJ-8: Future Expandability** — "The design facilitates Phase 2 expansion with minimal disruption"

**Design Provisions for Future Expansion (if applicable to buildings):**
- **TBD**: MCC building sizing for future electrical capacity growth
- **TBD**: Structural provisions for future building additions (column grid extension, foundation design)
- **TBD**: Utility connections sized for future loads
- Site layout allowing future building additions without major reconstruction

**Source:** Decomposition Section 2 (OBJ-8)

## Trade-offs

**Competing Concerns to Evaluate During Design:**

### T1: Building System Selection — Custom vs. Pre-Engineered/Modular

**Option A: Custom-Designed Building (Conventional Stick-Built)**
- **Advantages:**
  - Design flexibility to meet exact spatial and functional requirements
  - Integration with site-specific constraints
  - Potentially optimized material usage
- **Disadvantages:**
  - Longer design and construction schedule
  - Higher on-site labor content and weather exposure during construction
  - Quality control dependent on field workmanship

**Option B: Pre-Engineered Metal Building (PEMB) or Modular Building**
- **Advantages:**
  - Faster design and procurement (manufacturer engineering support)
  - Faster construction (factory fabrication, bolt-together erection)
  - Quality control in factory environment
  - Reduced weather delays
  - Terminal continuity benefits (less on-site construction activity)
- **Disadvantages:**
  - Design constrained by manufacturer standard systems and modules
  - Potentially less architectural flexibility
  - Transportation and crane access requirements

**Design Decision Factors:**
- Schedule criticality (OBJ-5: Terminal Continuity favors faster construction)
- Site access and construction logistics
- Architectural/aesthetic requirements (if any)
- Cost and value engineering opportunities
- **TBD**: Employer preferences or ER requirements for building systems

**Source:** D&B contract delivery encourages constructability optimization; OBJ-5 (Terminal Continuity)

### T2: Envelope Thermal Performance — Code Minimum vs. Enhanced Performance

**Option A: NBC 2020 / ASHRAE 90.1 Minimum Compliance**
- **Advantages:**
  - Lower first cost (thinner insulation, standard envelope systems)
  - Code-compliant baseline
- **Disadvantages:**
  - Higher lifecycle operating costs (heating/cooling energy)
  - Potentially less occupant comfort

**Option B: Enhanced Envelope Performance (Higher R-values, Air Sealing)**
- **Advantages:**
  - Lower operating energy costs (OBJ-9: Lifecycle Cost Optimization)
  - Improved occupant comfort and equipment temperature stability
  - Potential utility rebates or incentives
- **Disadvantages:**
  - Higher first cost (thicker insulation, premium air barrier systems)

**Design Decision Factors:**
- Building conditioning requirements (MCC building may require cooling for equipment heat dissipation)
- Lifecycle cost analysis (energy cost projections vs. incremental envelope cost)
- Employer energy performance goals
- **TBD**: Applicability of ASHRAE 90.1 or energy code to project

**Source:** NBC 2020 Part 5; ASHRAE 90.1; OBJ-9 (Lifecycle Cost Optimization)

### T3: Foundation System Selection

**Option A: Shallow Foundations (Spread Footings)**
- **Advantages:**
  - Lower cost if soil bearing capacity adequate
  - Simpler design and construction
- **Disadvantages:**
  - Requires competent bearing soils at shallow depth
  - Settlement potential if soil conditions variable

**Option B: Deep Foundations (Piles)**
- **Advantages:**
  - Reliable load transfer to competent bearing strata
  - Reduced settlement risk
  - Can address poor surface soil conditions
- **Disadvantages:**
  - Higher cost
  - Specialized equipment and labor
  - Potential noise/vibration impacts to adjacent terminal operations

**Design Decision Factors:**
- Geotechnical investigation findings — **TBD**
- Building loads and settlement tolerance
- Site constraints and terminal operations continuity (OBJ-5)
- Cost and schedule implications

**Source:** Foundation design considerations; **TBD** pending geotechnical investigation

### T4: Operator Shelter Strategy — Quantity and Configuration

**Option A: Individual Shelters at Each Railcar Station (32 shelters)**
- **Advantages:**
  - Personnel always near work location (no walking between shelter and railcar)
  - Distributed protection across entire unloading area
- **Disadvantages:**
  - Higher capital cost (32 separate structures)
  - Higher maintenance burden (32 structures to maintain)

**Option B: Shared Shelters (Fewer, Larger Shelters Serving Multiple Stations)**
- **Advantages:**
  - Lower capital cost (fewer structures)
  - Easier to provide amenities (heating, lighting, communication)
  - Lower maintenance burden
- **Disadvantages:**
  - Personnel must walk between shelter and some railcar stations (weather exposure, efficiency)

**Option C: Centralized Shelter Building**
- **Advantages:**
  - Lowest capital cost
  - Best amenities (heated break room, washroom, tool storage)
  - Lowest maintenance burden
- **Disadvantages:**
  - Personnel must walk to/from all railcar stations (greatest weather exposure, lowest efficiency)

**Design Decision Factors:**
- Operational efficiency and personnel preference
- Weather exposure acceptance
- Capital vs. operating cost trade-off
- **TBD**: Employer operational preferences or ER requirements

**Source:** 32 railcar unloading stations per decomposition Section 1.1; operator shelter function

### T5: Construction Sequencing and Terminal Continuity

**Competing Concerns:**
- **Construction schedule:** Faster construction preferred (Design-Build delivery)
- **Terminal operations continuity:** OBJ-5 requires minimizing disturbance to existing terminal commercial activities
- **Cost:** Expedited construction and off-peak work may increase cost

**Trade-off Considerations:**
- Modular/prefabricated building systems reduce on-site construction duration (supports both schedule and terminal continuity)
- Construction phasing and site logistics planning to avoid conflicts with terminal operations
- Potential premium costs for off-peak or phased construction
- **TBD**: Employer constraints on construction hours, access routes, laydown areas

**Source:** Decomposition Section 2 (OBJ-5: Terminal Continuity); D&B contract schedule pressures

## Examples

**Reference Examples and Precedents:**

### E1: MCC Building Precedents

**Typical Industrial MCC Buildings:**
- Pre-engineered metal building (PEMB) with insulated metal panel (IMP) envelope
- Single-story, rectangular footprint (10m × 20m typical for medium-sized MCC installations)
- Equipment arranged in double-sided aisles for maintenance access
- Mechanical ventilation and cooling for equipment heat dissipation
- Controlled access (single personnel door with key/card reader; no windows or minimal windows)
- Overhead door (if required for equipment installation/removal)

**Source:** Typical industrial electrical building design practice

### E2: Operator Shelter Precedents

**Portable/Modular Shelter Units:**
- Factory-built shelter modules (2m × 2m to 3m × 4m typical)
- Insulated walls and roof
- Single door, window(s) for visibility
- Portable electric heater or no heating (depending on climate and occupancy duration)
- Anchored to concrete pad or structural frame

**Permanent Shelter Structures:**
- Stick-built or prefabricated shelter buildings
- Foundation (concrete pad or piles)
- Insulated envelope, heating, and lighting
- May include multiple shelters in a single structure (serving multiple railcar stations)

**Source:** Industrial site personnel shelter design practice

### E3: Coastal BC Building Envelope Precedents

**Durable Envelope Systems for Marine/Industrial Environment:**
- Insulated metal panels (IMP) with factory-applied finish (Kynar/PVDF coating for corrosion resistance)
- Standing-seam metal roofing with concealed fasteners (reduces water penetration and maintenance)
- Galvanized or stainless steel fasteners and trim
- Sealant joints designed for movement and long-term water-tightness
- Avoid exposed wood or untreated steel (corrosion/decay risk in coastal climate)

**Source:** Coastal BC building envelope best practices

### E4: NBC 2020 Code Compliance Examples

**Fire Safety:**
- Group F (Industrial) occupancy classification typical for MCC buildings and operator shelters
- Unsprinklered buildings: Area and height limits per NBC 2020 Table 3.2.2.50
- Travel distance to exit: 45m maximum per NBC 2020 (may be extended if building sprinklered)
- Exit door hardware: Panic hardware if occupant load ≥ certain threshold

**Accessibility:**
- If operator shelters are considered "normally occupied," accessible entrance and interior required per NBC 2020 Part 3 Div B Section 3.8
- Door clear width ≥ 810mm; lever-style handles; appropriate opening force

**Structural:**
- Seismic design: Site class per geotechnical investigation; spectral accelerations per NBC 2020 for Surrey, BC
- Snow load: Ground snow load per NBC 2020 climatic data Appendix C (Surrey, BC)
- Wind load: Reference wind pressure per NBC 2020 climatic data; exposure factor based on site terrain

**Source:** NBC 2020 code provisions (examples — **TBD**: Specific code analysis for project)

### E5: Drawing Set Organization Examples

**Typical Building Drawing Set Structure:**
- **Cover sheet:** Title sheet with project information, drawing index, abbreviations, symbols
- **Site plan (A-0.01):** Building location, site context, north arrow
- **Floor plans (A-1.01, A-1.02, etc.):** Plans for each floor level
- **Roof plan (A-1.99):** Roof layout, drainage, rooftop equipment
- **Elevations (A-2.01–A-2.04):** Exterior elevations (North, South, East, West)
- **Building sections (A-3.01, A-3.02, etc.):** Vertical sections through building
- **Wall sections (A-4.01, A-4.02, etc.):** Envelope assembly details
- **Details (A-5.01, A-5.02, etc.):** Connection details, door/window details, etc.
- **Schedules (A-6.01):** Door schedule, window schedule, wall type schedule

**Source:** Standard architectural/building drawing organization

### E6: Employer's Requirements Review

**Expected ER Content (Volume 2 Part 3: Building Works) — TBD:**
- Building functional requirements (space programs, clearances)
- Performance criteria (structural loads, envelope performance, fire ratings)
- Material and finish requirements (exterior appearance, interior finishes)
- Equipment requirements (HVAC, lighting, plumbing)
- Commissioning and acceptance criteria
- O&M documentation requirements

**Action:** Review ER Volume 2 Part 3 to extract project-specific building requirements and incorporate into design drawings.

**Source:** Decomposition Section 3 (Reference Documents); **TBD** pending ER access

---

**Note:** This guidance document is based on decomposition scope, applicable codes/standards, and typical building design practice. Specific design decisions require review of Employer's Requirements, geotechnical investigation, equipment specifications, and engineering analysis (DEL-21.03: Building Design Calculations).
