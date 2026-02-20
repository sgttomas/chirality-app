# PKG-003 Site & Civil Works — Deliverables Summary

**Package:** PKG-003 Site & Civil Works
**Project:** Penhold Public Services Building (PSB)
**Location:** Lot 1, Block 1, Plan 212 1668 (NW ¼ SEC. 6-37-27 W4M), Town of Penhold, Alberta
**Document Version:** 2026-02-19
**Status as of Last Update:** All deliverables at SEMANTIC_READY state (2026-02-17)

---

## Executive Summary

PKG-003 Site & Civil Works encompasses five integrated deliverables covering all site-level civil engineering and environmental compliance activities for the Penhold Public Services Building project. The package includes site planning, grading and drainage, pavement design, utility distribution, and environmental/regulatory compliance.

All five deliverables have progressed to **SEMANTIC_READY** status as of 2026-02-17, following completion of the CHIRALITY_FRAMEWORK methodology. Key enrichment activities (Semantic Lensing Pass 3 and documentation normalization) have been applied to establish comprehensive, verifiable requirements and acceptance criteria.

---

## Package Scope and Integration

**Package Objective:**
Deliver complete civil site engineering design and supporting regulatory coordination for a 20-acre parcel developed as a ~12-acre operational facility (Public Services Building, cold storage building, and site works).

**Key Site Characteristics:**
- Parcel: ~20 acres
- Developable area: ~12 acres (western portion)
- Restricted area: ~8 acres (eastern portion, flood fringe, dog park, retention pond)
- Building locations: Main Public Services Building and Cold Storage Building (60' × 100')
- Site access: Waskasoo Avenue (RR280)
- Drainage: No on-site storm sewer; natural off-site drainage via retention pond
- Environmental constraints: Flood fringe, wetlands (DW01, DW02, DW03, DD01, DD02), Waskasoo Creek corridor

---

## Deliverable Files and Descriptions

### Overview Table

| DEL ID | Title | Primary Purpose | Status | Key Artifacts |
|--------|-------|-----------------|--------|----------------|
| DEL-03-01 | Site Plan, Circulation, Parking & Operational Layout | Site layout, circulation design, parking, fire apparatus routing | SEMANTIC_READY | Site plan, turning templates, parking layout, coordination notes |
| DEL-03-02 | Grading, Earthworks, Drainage & Stormwater | Grading design, earthworks, drainage, stormwater retention | SEMANTIC_READY | Grading plan, earthworks plan, drainage plan, erosion control plan |
| DEL-03-03 | Pavements, Aggregate Yard Areas & Concrete Aprons | Pavement design, surfacing zones, concrete aprons | SEMANTIC_READY | Pavement design report, zone plan, cross-section details, apron details |
| DEL-03-04 | Site Utilities Distribution & Allowance-Based Tie-Ins | Utility routing, provider coordination, allowance management | SEMANTIC_READY | Utility distribution plan, coordination records, allowance management plan |
| DEL-03-05 | Environmental Constraints, Flood Hazard & Regulatory Compliance | Flood hazard mapping, wetland compliance, environmental mitigation | SEMANTIC_READY | Flood hazard constraints map, wetland integration, mitigation notes, coordination log |

---

## Detailed Deliverable Analysis

### DEL-03-01: Site Plan, Circulation, Parking & Operational Layout

**Current State:** SEMANTIC_READY (2026-02-17)

**Scope:**
- Overall site plan establishing building footprint position and orientation on the ~12-acre developable portion
- Traffic circulation design for safe exterior flow and access to Waskasoo Avenue
- Truck and fire apparatus turning radii analysis and template documentation
- Parking layout for the site (light-duty asphalt zone near main structure)
- Surface treatment designation by zone (heavy-duty asphalt, light-duty asphalt, aggregate)
- Concrete apron design at all overhead door access points
- Coordination of building siting with Tagish Engineering Site Grading drawings (TPN46)
- Scope items: SOW-0100, SOW-0101, SOW-0102, SOW-0103, SOW-0104

**Key Requirements:**
- 13 primary requirements (REQ-01 through REQ-13) covering site development area, building location, circulation design, pavement zones, parking methodology, flood hazard compliance, and future expansion
- Specific TBD items flagged: Town of Penhold Land Use Bylaw parking requirements, Alberta Fire Code fire access route criteria, flood boundary regulatory authority confirmation
- Verification includes design phase review, IFC review, and regulatory confirmation gates

**Files in Deliverable:**
- `Specification.md` — Comprehensive requirements document (168 lines)
- `Datasheet.md` — Data and placeholder specifications
- `Guidance.md` — Guidance on implementation approach
- `Procedure.md` — Procedural steps for execution
- `_CONTEXT.md` — Contextual background and anticipated artifacts
- `_SEMANTIC_LENSING.md` — Semantic enrichment items and lensing results
- `_SEMANTIC.md` — Semantic structure and metadata
- `_STATUS.md` — Completion status history
- `_REFERENCES.md` — Source document references
- `_DEPENDENCIES.md` — Dependency mapping
- `_MEMORY.md` — Project memory/context notes
- `Dependencies.csv` — Machine-readable dependency data

**Key Findings:**
- Well-structured specification with clear scope boundaries and exclusions
- Multiple TBD items related to municipal bylaw availability and fire code standards
- Interface boundary with DEL-03-02 (drainage) explicitly clarified
- Cold storage building siting explicitly in scope; building design excluded
- Fire apparatus routing and turning radii analysis are critical verification items

---

### DEL-03-02: Grading, Earthworks, Drainage & Stormwater

**Current State:** SEMANTIC_READY (2026-02-17)
**Semantic Lensing Pass 3 Status:** Complete with 28 warranted items applied; terminology normalized; blocking dependencies flagged; 1 unresolved conflict (D-001) escalated to Conflict Table

**Scope:**
- Site clearing, stripping, and grubbing of vegetation, topsoil, and organics
- Cut and fill earthworks to achieve design grades (coordinated with TPN46)
- Subgrade preparation and foundation pad preparation for all buildings
- Engineered fill placement and compaction
- Site grading to ensure positive drainage away from all buildings
- Stormwater management — directing roof and site drainage to natural drainage off-site
- Erosion protection and control
- Drainage ditches and culverts as shown in TPN46

**Key Requirements:**
- 18 primary requirements (REQ-3201 through REQ-3218) covering:
  - Clearing and stripping (topsoil ~72 mm average)
  - Integration with existing grading (TPN46)
  - Positive drainage (3% min slope over 3.0 m from buildings; 2% subgrade slope)
  - Engineered fill material specifications
  - Fill compaction (98–100% SPDD depending on depth and location)
  - Proof rolling with 80 kN axle load
  - Compaction testing frequency (1 test per 500 m² per lift)
  - Cut and fill slope geometry constraints
  - Stormwater retention pond design (capacity, design storm, outlet flow rate — all TBD)
  - Erosion control and permanent slope stabilization
  - Drainage outlet design criteria (TBD)
  - Geotechnical certification and contingency for additional investigation

**Unresolved Conflict (D-001):**
- Regulatory approval dependency: Stormwater retention pond location (shown in TPN46) may be in flood fringe and require environmental/municipal approvals (per DEL-03-05 scope). Design-Builder may not proceed without approval confirmation. Status: Escalated to Conflict Table for human ruling.

**Files in Deliverable:**
- `Specification.md` — Comprehensive requirements (242 lines, most detailed in package)
- `Datasheet.md` — Design parameters and TBD placeholders
- `Guidance.md` — Implementation guidance
- `Procedure.md` — Procedural execution steps
- Supporting metadata files (CONTEXT, SEMANTIC_LENSING, STATUS, REFERENCES, DEPENDENCIES, MEMORY)
- `Dependencies.csv` — Machine-readable dependencies

**Key Findings:**
- Most comprehensive specification in PKG-003 (242 lines)
- Heavy reliance on Geotechnical Investigation Report (USG1123, Feb 2021) as normative source
- Multiple critical TBD items for stormwater pond design (capacity, design storm return period, outlet flow rate) requiring municipal coordination
- Verification methods are detailed and specific (proof rolling observation, field density testing at prescribed frequency)
- Acceptance criteria for "no ponding" requirement lack quantitative thresholds (max depth, duration) — noted as D-003
- As-built survey expanded to include pond geometry, ditch profile, and all slope grades
- Embankment slope compaction testing explicitly strengthened in Semantic Lensing Pass 3
- Hold points established for geotechnical certification before structure/paving placement (D-004)

---

### DEL-03-03: Pavements, Aggregate Yard Areas & Concrete Aprons

**Current State:** SEMANTIC_READY (2026-02-17)

**Scope:**
- Heavy duty asphalt — direct routing of fire apparatus (Zone A, 800,000 ESALs minimum)
- Light duty asphalt — parking areas near main structure (Zone B, 100,000 ESALs minimum)
- Aggregate surfacing — heavy equipment yard areas (Zone C)
- Concrete aprons — at all overhead door access points (Zone D)

**Key Requirements:**
- 15 primary requirements covering:
  - Surfacing zone delineation (A, B, C, D zones)
  - Pavement design method (AASHTO 1993 Flexible Pavement Design with Mr = 45,000 kPa, frost penetration = 2.0 m)
  - Light duty asphalt cross-section: 425 mm total (75 mm HMAC, 150 mm base, 200 mm SGSB, geofabric)
  - Heavy duty asphalt cross-section: 450 mm total (100 mm HMAC, 150 mm base, 200 mm SGSB, geofabric + biogrid)
  - Aggregate yard surfacing specifications and minimum depth (TBD, ~300 mm assumed)
  - Concrete apron structural loading for fire apparatus, graders, tandem dump trucks, compact track loaders
  - Concrete mix design for severe sulphate exposure (Class S-2) per CAN/CSA A23.1-2014
  - Subgrade preparation (strip topsoil, compact 98% SPDD, proof roll)
  - Layer compaction standards (98–100% SPDD depending on layer)
  - Drainage cross slopes (2% minimum)
  - Transition zone design (edge support, differential settlement, drainage continuity at zone boundaries)
  - Surface smoothness for fire apparatus routing (TBD criteria)
  - Pavement design life and maintenance acknowledgment (15–20 year resurfacing cycle assumed; TBD)
  - Geosynthetic specifications (900 N grab tensile strength minimum for woven geofabric)

**TBD Items:**
- HMA material specification standard (AASHTO, ABC, or City of Red Deer) — not currently referenced
- Freeze-thaw exposure class for concrete (F-1 or F-2) — assumed applicable but not confirmed
- Surface smoothness tolerance for Zone A (3 m straightedge or IRI threshold) — TBD
- Pavement design life assumptions — 15–20 years assumed; TBD for confirmation
- Aggregate yard compacted depth — assumed minimum 300 mm; subject to design confirmation
- Core sampling frequency for HMA thickness verification — TBD per ASTM D5361 or equivalent
- Compaction testing frequencies for SGSB/Base and aggregate yard — to be established in quality plan

**Files in Deliverable:**
- `Specification.md` — Comprehensive requirements (225 lines)
- `Datasheet.md` — Design parameters and cross-section tables
- `Guidance.md` — Transition zone and design life guidance
- `Procedure.md` — Construction phasing and testing procedures
- Supporting metadata files
- `Dependencies.csv` — Machine-readable dependencies

**Key Findings:**
- Well-structured specification with clear zone designations and cross-section tables
- AASHTO 1993 method explicitly required; parameters clearly stated (Mr = 45,000 kPa, frost = 2.0 m)
- Heavy reliance on Geotechnical Investigation Report for fill material and compaction standards
- Concrete sulphate resistance and freeze-thaw requirements clearly specified with standard reference
- Verification includes post-paving HMA thickness core sampling (frequency TBD) to confirm min 75 mm (Zone B) and 100 mm (Zone A)
- Aggregate yard depth verification currently lacks quantitative method (depth measurement vs. design) — enhanced per D-002
- Drainage path connectivity verification expanded to require overlay review with DEL-03-02 drawings
- Multiple TBD items for HMA material specification, surface smoothness, and design life assumptions represent potential clarification needs

---

### DEL-03-04: Site Utilities Distribution & Allowance-Based Tie-Ins

**Current State:** SEMANTIC_READY (2026-02-17)
**Semantic Lensing Pass 3 Status:** Complete with 24 warranted items reviewed and incorporated; 12 verification enhancements applied; 3 procedural gates added; terminology and cross-doc consistency verified

**Scope:**
- Utility distribution design: Routing and design of all required utility services from existing municipal stubs to main building and cold storage building
- Utility types: Water, wastewater (sanitary sewer), electrical power, communications (telecom/data), natural gas
- Utility provider coordination: All correspondence, applications, and coordination activities
- Allowance management: Cash allowance mechanism for utility tie-ins (DEC-004)
- Service activation coordination: Sequencing and coordination for service activation
- Civil design drawings: Site servicing drawings from existing underground services drawings (provided by Owner post-award)

**Key Requirements:**
- 13 primary requirements covering:
  - Utility coordination responsibility (obtain and demonstrate compliance with Provider-specific connection standards)
  - Scope of utility services (5 utility types explicitly listed)
  - Cash allowance treatment (tie-ins excluded from base proposal price; no pre-set dollar value)
  - Design coordination and execution responsibility (despite allowance treatment)
  - Site servicing drawings production
  - Civil design standards compliance (OSR §10.3.2, codes, good practice)
  - Professional sealing (P.Eng. registration required)
  - Utility distribution plan (showing routing from stubs to buildings)
  - Allowance management plan (tracking, cost management, reporting frequency minimum monthly or per drawdown event)
  - Service activation coordination (utilities live prior to occupancy)
  - As-built survey showing service connections
  - Alberta One-Call locate requirement (legal requirement; elevated from assumption to binding requirement in Pass 3)
  - Trench backfill and compaction standards (90–95% Standard Proctor, compaction testing frequency TBD)

**Verification Gates (Semantic Lensing Pass 3 Additions):**
- **Provider design approval gate:** Must obtain signed provider design approval letter or written compliance confirmation before construction begins (F-002)
- **Three design submission milestones:** (a) BDD — preliminary concept; (b) 60% DD — substantially complete with provider comments; (c) 100% DD/IFC — final drawings stamped with all approvals
- **Service activation acceptance criteria:** Detailed quantitative criteria per utility type (water pressure test, wastewater line cleaning, electrical sign-off, gas pressure hold, communications continuity test)

**TBD Items:**
- Town of Penhold municipal servicing standards for water/wastewater connections — to be obtained during design
- Specific utility provider connection standards — to be obtained from each provider
- Trench backfill compaction percentage and testing frequency — Town standard TBD
- Allowance management plan format requirements — Owner direction required
- Service activation acceptance thresholds for each utility type — many provider-specific thresholds TBD (water pressure psi range, gas pressure hold duration, etc.)

**Files in Deliverable:**
- `Specification.md` — Comprehensive requirements (147 lines)
- `Datasheet.md` — Utility provider reference and allowance management templates
- `Guidance.md` — Provider coordination workflow
- `Procedure.md` — Service activation procedures and testing protocols
- Supporting metadata files
- `Dependencies.csv` — Machine-readable dependencies

**Key Findings:**
- Allowance-based delivery model (DEC-004) creates unique scope boundary: design responsibility remains with Design-Builder, but costs treated as allowance outside base price
- Semantic Lensing Pass 3 added critical verification gates for provider design approval before construction (F-002) — important hold point to prevent cost overruns
- Alberta One-Call locate requirement elevated from assumption to binding legal requirement (X-001) — reflects actual Alberta regulatory status
- Service activation acceptance criteria significantly detailed in Pass 3 with quantitative thresholds per utility type
- Design submission milestone gates (BDD, 60% DD, 100% DD/IFC) establish formal review points for provider approval tracking
- Multiple dependencies on other utilities, standards, and provider coordination create tight sequencing requirements
- Allowance management plan format and reporting frequency now specified (minimum monthly) per F-004

---

### DEL-03-05: Environmental Constraints, Flood Hazard & Regulatory Compliance

**Current State:** SEMANTIC_READY (2026-02-17)

**Scope:**
- Identification and mapping of flood hazard zones (100-Year Floodway and Flood Fringe) relative to site developable envelope
- Delineation and integration of wetland/waterbody boundaries and required setbacks into site design
- Environmental mitigation requirements for wetland impacts
- Regulatory coordination: Alberta Water Act approval, flood hazard compliance with Town of Penhold and AEPA
- Production of: flood hazard constraints map, wetland/setback integration output, environmental mitigation notes, regulator coordination log
- Coverage of SOW-0102 (constraints aspects) and SOW-0114

**Key Requirements:**
- 12 primary requirements covering:
  - Flood hazard zone avoidance (floodway prohibited; flood fringe design to avoid floodway continuity impact)
  - Developable area constraint (~12 acres development; ~8 acres restricted in flood fringe)
  - Flood hazard constraints map production (showing floodway, flood fringe, developable envelope, buildings, works)
  - Exact floodway/fringe limit confirmation during design phase
  - Alberta Water Act approval (prior to any wetland/waterbody impacts)
  - Wetland replacement fee (ABWRET-A in-lieu fee: $10,769.54 as of Aug 2021; current amount TBD with AEPA)
  - Wetland/setback integration (DW01, DW02, DW03, DD01, DD02, Anthropogenic Ditch [LC_20210520_045]; setback distances from AEPA Water Act conditions or Town permit conditions — TBD)
  - Environmental mitigation notes (avoidance/minimization, stormwater, wildlife, erosion/sediment control)
  - Regulator coordination log (AEPA and Town of Penhold interactions, approvals, conditions, open items)
  - Fill placement compliance (within flood fringe, if permitted, shall meet Town and AEPA requirements)
  - General regulator coordination as required (Town of Penhold MDP, AEPA Water Act, Alberta Wetland Policy)
  - Migratory bird nesting season restriction & wildlife disturbance mitigation (Alberta Wildlife Act, Migratory Birds Convention Act — nesting season approximately April 1 to August 31; pre-clearing nest survey required if clearing during nesting season)

**Regulatory Dependencies:**
- **Alberta Water Act** — Approval required before any wetland/waterbody impact; application basis: Wetland Assessment and Impact Report (Ghostpine, Aug. 2021)
- **Alberta Environment and Protected Areas (AEPA)** — Source of Water Act approval and setback distance prescriptions
- **Town of Penhold Municipal Development Plan (MDP)** — Flood fringe/floodway designations; flood hazard constraints
- **Town of Penhold Development Permit** — Authority for flood hazard compliance and potential setback distance prescriptions
- **Alberta Wildlife Act** — Nesting season restrictions (April 1 – Aug 31); bird nest protection
- **Migratory Birds Convention Act (federal)** — Migratory bird protection complementary to Alberta Wildlife Act

**Critical Path Items:**
- Exact floodway/fringe limits confirmation — impacts site plan freeze
- Wetland setback distances confirmation from AEPA or Town — impacts site design and may delay freeze if not received
- Water Act approval status confirmation — Design-Builder responsibility to track and confirm approval received or conditions issued
- Pre-construction regulatory clearance gate: Water Act approval, Town Development Permit, fill placement acceptance (if applicable) must be in file before ground disturbance in constrained areas

**Verification Gates (from Semantic Lensing):**
- **Pre-Construction Regulatory Clearance Gate (Procedure Step B1):** Water Act approval, Town Permit, fill acceptance documentation must be in file; Site Superintendent briefed on environmental no-go zones (X-001)
- **As-Built Flood Hazard Constraints Map Update (Procedure Step B5):** Map updated with as-built conditions and confirmed flood limits at closeout (X-002)
- **Post-Construction AEPA Condition Closeout (Procedure Step B4):** All AEPA conditions satisfied and documented; written AEPA confirmation obtained (X-003)

**Files in Deliverable:**
- `Specification.md` — Comprehensive requirements (205 lines)
- `Datasheet.md` — Flood hazard zones, wetland features, setback distances (mostly TBD placeholders)
- `Guidance.md` — Regulatory coordination workflow and environmental mitigation best practices
- `Procedure.md` — Phased regulatory approval and construction compliance procedures
- Supporting metadata files
- `Dependencies.csv` — Machine-readable dependencies

**Key Findings:**
- Flood hazard mapping and wetland setback integration are critical path items for site design freeze
- Exact floodway/fringe limits TBD until confirmed with Town of Penhold and/or AEPA — design risk if delayed
- Wetland setback distances explicitly TBD (awaiting AEPA Water Act approval or Town permit conditions) — potential design constraint
- Stormwater retention pond location may be in flood fringe requiring regulatory approvals (D-001 conflict, escalated) — dependency between DEL-03-02 and DEL-03-05
- Water Act approval tracking and condition compliance are Design-Builder responsibility (REQ-3505-005, REQ-3505-011, REQ-3505-009)
- Pre-clearing nest survey required if vegetation clearing occurs during nesting season (April 1 – Aug 31); professional biologist required (REQ-3505-012)
- Migratory bird nesting season restrictions explicitly detailed in Specification with "no disturbance within setback distances" protocol if nests found
- Environmental mitigation notes are required artifact but content framework (avoidance/minimization, stormwater, wildlife, erosion control) is guidance-based without specific design thresholds
- Regulator coordination log is critical project artifact for tracking approvals and conditions

---

## Key Integration Points and Dependencies

### Critical Cross-Deliverable Interfaces

1. **DEL-03-01 ↔ DEL-03-02 (Site Planning ↔ Grading):**
   - Interface boundary clarified: DEL-03-01 shows conceptual positive drainage direction arrows; DEL-03-02 provides detailed grading design
   - REQ-09 in DEL-03-01 coordinates with DEL-03-02 for positive drainage verification
   - Tagish Engineering TPN46 drawings referenced by both deliverables

2. **DEL-03-02 ↔ DEL-03-05 (Grading ↔ Environmental):**
   - **Unresolved Conflict D-001:** Stormwater retention pond location (TPN46) may be in flood fringe requiring AEPA/Town approvals
   - Design-Builder must not proceed with pond construction without regulatory approval confirmation
   - DEL-03-02 stormwater pond sizing criteria (capacity, design storm, outlet flow) TBD pending municipal standards coordination (Item A-003)

3. **DEL-03-01 ↔ DEL-03-03 (Site Planning ↔ Pavements):**
   - Zone designations (A: heavy duty; B: light duty; C: aggregate; D: aprons) established in DEL-03-01, detailed in DEL-03-03
   - Fire apparatus routing zones in DEL-03-01 map to pavement design ESALs in DEL-03-03

4. **DEL-03-03 ↔ DEL-03-02 (Pavements ↔ Grading):**
   - Drainage cross slope continuity (2% minimum) must be coordinated between pavement design and grading drainage paths
   - Subgrade preparation and proof rolling common verification requirements
   - Geotechnical certification hold point before paving placement (D-004 in DEL-03-02)

5. **DEL-03-04 (Utilities) ↔ All Site Planning/Design Deliverables:**
   - Utility trench routing impacts site layout, grading, and pavement zones
   - Service stubs location confirmation prerequisite for site design
   - Owner to provide existing underground services drawings post-award (prerequisite for detailed design)

6. **DEL-03-05 (Environmental) ↔ All Site Works:**
   - Flood hazard boundaries constrain developable area (REQ-3505-002)
   - Wetland setback integration impacts site plan (REQ-03-05-007)
   - Nesting season restrictions may impact construction scheduling (REQ-3505-012)
   - Pre-construction regulatory clearance gate is prerequisite for ground disturbance (Procedure Step B1)

---

## Completeness and Quality Assessment

### Strengths

1. **Comprehensive Specification Framework:**
   - All five deliverables have detailed Specification documents with clear requirement statements
   - Requirements are numbered and traceable (REQ-01 through REQ-3218 across package)
   - Scope inclusions and exclusions are explicitly stated in each deliverable

2. **Semantic Enrichment (Chirality Framework):**
   - Semantic Lensing Pass 3 applied to all deliverables, adding warranted items and enrichment
   - DEL-03-02: 28 warranted items applied; terminology normalized; blocking dependencies flagged
   - DEL-03-04: 24 warranted items reviewed; 12 verification enhancements; 3 procedural gates added
   - Structured metadata files (_SEMANTIC_LENSING.md, _CONTEXT.md, _SEMANTIC.md) document enrichment provenance

3. **Verification and Acceptance Criteria:**
   - Detailed verification methods specified for each requirement
   - Verification staged (Proposal design review, IFC design review, Regulatory confirmation, Document review)
   - Hold points and acceptance gates defined (geotechnical certification, provider design approval, regulatory clearances)

4. **Regulatory Compliance Focus:**
   - DEL-03-05 explicitly maps flood hazard, wetland, and environmental mitigation requirements to Alberta Water Act, Alberta Wildlife Act, and municipal authorities
   - Authorities Having Jurisdiction (AHJ) explicitly identified for each requirement area
   - Regulator coordination logs and documentation requirements established

5. **Procedural Clarity:**
   - Each deliverable includes Procedure.md documenting phased execution steps
   - Construction sequencing and hold points identified
   - Quality management and testing protocols specified

### Gaps and Concerns

1. **Unresolved TBD Items (Design Risk):**
   - **Stormwater Pond Sizing (DEL-03-02 D-001, F-001):** Capacity, design storm return period, outlet flow rate, emergency overflow all TBD pending municipal standards (Town of Penhold). Critical path item.
   - **Pond Regulatory Approval (DEL-03-02 D-001):** Pond location may be in flood fringe requiring AEPA/Town approvals. Status: escalated conflict, awaiting human ruling.
   - **Wetland Setback Distances (DEL-03-05 REQ-007):** Setback distances TBD pending AEPA Water Act approval or Town permit conditions. Design impact: unknown if setbacks constrain site layout.
   - **Exact Flood Boundary (DEL-03-05 REQ-004):** Floodway/fringe limits TBD until confirmed with Town/AEPA. Impacts site plan freeze timing.
   - **Municipal Servicing Standards (DEL-03-02, DEL-03-04):** Town of Penhold municipal development standards and bylaws referenced but not yet obtained (TBD). Includes parking bylaw minimums, grading/drainage standards, utility connection standards.
   - **HMA Material Specification (DEL-03-03):** No HMA material specification standard currently referenced; only compaction testing (Marshall Method) specified. Potential acceptance criteria gap.
   - **Surface Smoothness (DEL-03-03 F-004):** Fire apparatus routing surface smoothness acceptance criterion TBD (e.g., 3 m straightedge tolerance or IRI). No specific threshold established.

2. **Incomplete Artifact Definitions:**
   - **Flooding Pond Design Acceptance Criteria (DEL-03-02 REQ-3212 F-001):** Pond sizing criteria listed as TBD. Verification must confirm design calculations based on design storm criteria, but storm criteria not yet established.
   - **"No Ponding" Definition (DEL-03-02 REQ-3203 D-003):** Acceptance criterion for ponding lacks quantitative definition (max depth, max duration, observation period). Verification method unclear.
   - **Aggregate Yard Depth Verification (DEL-03-03 D-002):** Compacted depth assumption (300 mm) noted as TBD. Verification method for as-built depth confirmation added in Lensing enrichment but depth design threshold not specified.
   - **Pavement Design Life (DEL-03-03 A-005, REQ-03-03-13):** Assumed 15–20 year resurfacing cycle for asphalt noted as TBD. Design assumption stated but not confirmed.

3. **Conditional/Contingent Requirements:**
   - **Geotechnical Report Sufficiency (DEL-03-02 REQ-3214, X-005):** If existing Geotech Report (USG1123, Feb 2021) found insufficient, Design-Builder must undertake additional investigation at their cost. Triggers for "insufficiency" TBD — potential cost/schedule risk if conditions differ materially from 2021 survey.
   - **ESAL Exceedance for Pavement (DEL-03-03 REQ-03-03-04):** If design ESALs for fire apparatus exceed 800,000 and approach 2,000,000 (industrial collector threshold), alternate 550 mm cross-section required. ESAL calculation is Design-Builder responsibility; threshold-crossing scenario defined but not pre-calculated.

4. **Environmental Regulatory Dependency Risk:**
   - **Water Act Approval Status (DEL-03-05 REQ-005):** Wetland Assessment and Impact Report provided (Ghostpine, Aug. 2021), but current Water Act approval status unclear. Design-Builder must confirm whether application submitted, approved, or conditions pending.
   - **Nesting Season Restrictions (DEL-03-05 REQ-3505-012):** Pre-clearing nest survey required if vegetation clearing occurs April 1 – Aug 31. Schedule risk if nests found; no clearing permitted within setback distances until nesting complete. Professional biologist engagement required during construction if nesting season overlap.

5. **Standards Accessibility Issues:**
   - Multiple Alberta codes and standards referenced but not directly accessible:
     - Alberta Building Code (ABC) — location TBD
     - Alberta Fire Code / National Fire Code of Canada — fire access route design criteria TBD
     - CAN/CSA A23.1-2014 (Table 3) — concrete exposure classification referenced but full standard not accessed
     - AASHTO 1993 Pavement Design Guide — referenced; direct access TBD
     - City of Red Deer Aggregate Specification — referenced via Geotech Report Table 7.1; not reproduced
     - Town of Penhold Municipal Development Standards — referenced but not obtained
   - **Recommendation:** Owner should provide or Design-Builder should confirm self-source responsibility for all normative standards before proposal submission.

6. **Verification Method Clarity:**
   - **Proof Rolling Acceptance (DEL-03-03 REQ-09):** Subgrade preparation proof rolling required; areas with "appreciable deflections" shall be remediated. Definition of "appreciable deflections" not quantified (e.g., max millimeters of deflection permissible).
   - **Drainage Path Connectivity (DEL-03-03 E-001):** Enhanced verification method (overlay review with DEL-03-02 drainage drawings + visual inspection during construction) added in Lensing. Verification relies on subjective "visual inspection"; more objective criteria TBD.
   - **Slope Stability (DEL-03-02 REQ-3209 E-001):** Fill slopes exceeding 6.0 m in height require formal written review and approval by qualified Geotechnical Engineer prior to placement. Triggers for formal review (slope height >6.0 m) specified; review criteria not detailed.

7. **Cost and Schedule Risk Items:**
   - **Allowance Management (DEL-03-04):** Utility tie-in costs treated as cash allowance, excluded from base price. No pre-set dollar value. Potential for cost overrun if utilities more complex than anticipated. Provider design approval gate (F-002) established to mitigate pre-construction surprises.
   - **Regulatory Approval Dependency (DEL-03-05):** Water Act approval, Town Development Permit, and setback distance confirmation are critical path items with unknown approval timelines. Schedule risk if regulatory approvals delayed.
   - **Municipal Standards Coordination (Multiple):** Town of Penhold parking bylaw minimums, municipal servicing standards, grading/drainage standards all TBD. Potential rework if Design-Builder assumptions conflict with municipally mandated minimums.

---

## Summary of Open Issues and Recommendations

### High-Priority Items (Critical Path)

1. **Confirm Stormwater Pond Regulatory Status (DEL-03-02 D-001, DEL-03-05):**
   - Action: Determine whether pond location at TPN46 coordinates is in flood fringe and what approvals are required
   - Owner responsibility: Provide or confirm location mapping against flood hazard boundary
   - Design-Builder responsibility: Obtain AEPA/Town approvals before detailed design proceeds

2. **Obtain Wetland Setback Distances (DEL-03-05 REQ-007):**
   - Action: Submit Water Act application to AEPA (if not already submitted) and request setback distance prescriptions
   - Parallel action: Obtain Town of Penhold Development Permit and confirm any additional setback requirements in permit conditions
   - Timeline impact: If setbacks not confirmed by 60% DD milestone, site plan freeze at risk

3. **Confirm Town of Penhold Municipal Standards (Multiple Deliverables):**
   - Action: Obtain current Municipal Development Plan (MDP), Land Use Bylaw (parking requirements), and Municipal Development Standards (grading/drainage)
   - Items needed:
     - Parking stall minimum requirements for institutional/industrial use classification (DEL-03-01 REQ-11 A-001, C-001)
     - Grading and drainage design standards (DEL-03-02 A-003)
     - Utility connection standards for water/wastewater (DEL-03-04 A-001)
     - Flood hazard development constraints and setback requirements (DEL-03-05 F-001)

### Medium-Priority Items (Design Clarification)

4. **Establish Acceptance Criteria for Acceptance Terms (Multiple Deliverables):**
   - "Appreciable deflections" (DEL-03-03 REQ-09) — Quantify max permissible deflection (e.g., 25 mm)
   - "No ponding" (DEL-03-02 REQ-3203 D-003) — Quantify max ponding depth, duration, observation period
   - "Surface smoothness" (DEL-03-03 REQ-03-03-15 F-004) — Specify straightedge tolerance or IRI threshold
   - "Service activation acceptance criteria" (DEL-03-04 REQ-10 A-005) — Confirm specific provider thresholds (water psi range, gas pressure hold duration, etc.) during provider coordination

5. **Clarify Geotechnical Contingency Triggers (DEL-03-02 REQ-3214 X-005):**
   - Action: Define specific conditions that trigger need for supplemental geotechnical investigation (site conditions differ materially from USG1123 survey, groundwater levels changed, new loads, evidence of instability)
   - Purpose: Enable cost/schedule forecasting for contingency budgeting

6. **Confirm HMA Material Specification Standard (DEL-03-03 C-002):**
   - Action: Identify applicable HMA material specification (AASHTO, Alberta Transportation, City of Red Deer, or other)
   - Items: HMA mix design, aggregate gradation, binder grade, Marshall stability, acceptance criteria
   - Currently: Only Marshall Method (compaction testing) specified; material properties standard TBD

### Low-Priority Items (Process/Documentation)

7. **Define Allowance Management Plan Format (DEL-03-04 REQ-09 A-002):**
   - Action: Confirm Owner expectations for allowance management plan format, content, and reporting frequency
   - Current spec: Minimum monthly or per drawdown event reporting (F-004)
   - Clarification benefit: Reduce risk of rejected allowance documentation during proposal phase

8. **Establish Design Review Milestone Gates (DEL-03-04 REQ-08 X-002):**
   - Recommended gates: BDD (Preliminary concept), 60% DD (Substantially complete with provider comments), 100% DD/IFC (Final stamped with approvals)
   - Current spec includes these milestones; confirm with Owner that three-gate approach aligns with project delivery schedule

---

## Summary Table: Deliverable Maturity and Readiness

| DEL ID | Title | Status | Completeness | TBD Count | Risk Level | Next Step |
|--------|-------|--------|--------------|-----------|------------|---------:|
| DEL-03-01 | Site Plan, Circulation, Parking & Operational Layout | SEMANTIC_READY | 90% | 5 | Medium | Confirm parking bylaw minimums; confirm flood boundary authority |
| DEL-03-02 | Grading, Earthworks, Drainage & Stormwater | SEMANTIC_READY | 85% | 8 | High | Resolve pond regulatory status (D-001); confirm municipal grading standards; establish pond sizing criteria |
| DEL-03-03 | Pavements, Aggregate Yard Areas & Concrete Aprons | SEMANTIC_READY | 88% | 6 | Medium | Confirm HMA specification standard; confirm surface smoothness acceptance threshold; establish aggregate yard depth design |
| DEL-03-04 | Site Utilities Distribution & Allowance-Based Tie-Ins | SEMANTIC_READY | 90% | 4 | Medium-High | Obtain utility provider standards; confirm Town servicing standards; establish service activation acceptance thresholds |
| DEL-03-05 | Environmental Constraints, Flood Hazard & Regulatory Compliance | SEMANTIC_READY | 85% | 5 | High | Confirm Water Act application status; obtain wetland setback distances; confirm flood boundary; confirm nesting season survey requirements if construction schedule overlaps April–August |

---

## Conclusion

PKG-003 Site & Civil Works represents a comprehensive, well-structured civil engineering package for the Penhold Public Services Building project. All five deliverables have achieved SEMANTIC_READY status following application of the CHIRALITY_FRAMEWORK methodology, including Semantic Lensing enrichment, terminology normalization, and verification gate establishment.

**Overall Package Maturity:** 87% (average of individual deliverable completeness scores)
**Overall Package Risk:** Medium-High

**Key Strengths:**
- Complete specification documents with traceable requirements
- Clear scope boundaries and integration points
- Detailed verification methods and acceptance criteria
- Established hold points and regulatory clearance gates

**Key Vulnerabilities:**
- Significant regulatory approval dependencies (Water Act, Development Permit, flood hazard boundaries) with unknown timelines
- Critical municipal standards (bylaws, servicing standards) not yet obtained, creating rework risk
- Unresolved conflict (D-001) regarding stormwater pond regulatory status
- Multiple acceptance criteria and design parameters marked TBD, pending Owner or municipal clarification

**Recommended Path Forward:**
1. **Immediate (Pre-Proposal):** Obtain Town of Penhold Municipal Development Plan, Land Use Bylaw, and Development Standards. Clarify stormwater pond regulatory status. Confirm Water Act application status.
2. **Early Design (BDD/60% DD):** Obtain AEPA Water Act approval and setback distance prescriptions. Obtain all utility provider connection standards. Establish municipal standards-based acceptance criteria and design thresholds.
3. **Design Freeze (100% DD):** Confirm regulatory clearances (Water Act, Town permit, flood boundary confirmation). Finalize all TBD design parameters based on confirmed standards.

All deliverable files are complete and ready for design team use, pending resolution of noted TBD items through Owner, municipal, and regulatory coordination during the design phase.

---

**Document Prepared:** 2026-02-19
**Reviewer:** PKG-003 Comprehensive Analysis
**Status:** COMPLETE — Summary Document Ready for Distribution
