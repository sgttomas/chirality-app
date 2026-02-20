# PKG-004 Cold Storage Building Deliverables Summary

**Package Name:** PKG-004 Cold Storage Building (Unheated, 60'x100')
**Project:** Town of Penhold Public Services Building (PSB) — RFP 2024_004
**Owner:** Town of Penhold
**Contract Form:** CCDC 14-2013 (Design-Build)
**Review Date:** 2026-02-19

---

## Executive Summary

Package PKG-004 contains four (4) integrated design deliverables for an unheated cold storage building (60' × 100' clear-span footprint) serving as ancillary storage for seasonal equipment and materials for the Town of Penhold's Public Services Building project. All four deliverables have achieved **SEMANTIC_READY** status as of 2026-02-17, following completion of the CHIRALITY_FRAMEWORK semantic enrichment process.

The deliverables are comprehensive specification packages structured using a standardized 4-document bundle format (Specification, Datasheet, Guidance, and Procedure), supplemented with semantic and contextual documentation. All deliverables are actively being developed for design-build submission.

---

## Deliverable Inventory

### 1. DEL-04-01: Cold Storage — Design Basis & Configuration

**Location:** `/1_Working/DEL-04-01_Cold Storage - Design Basis & Configuration/`

**Scope:**
- Building footprint (60' × 100') and clear-span interior configuration
- Structural framing system basis and design life (20 years)
- Building height and operational clearance for fleet equipment
- Openings configuration (two opposite sides, one overhead door + one person door per side)
- Aesthetic coordination with main building
- General site placement and drainage considerations
- Weather-tight envelope and condensation prevention requirements

**Key Documents:**
| Document | Purpose | Status |
|----------|---------|--------|
| Specification.md | Normative requirements (15 REQs: 04-01-001 through 04-01-015) | Complete |
| Datasheet.md | Building attributes, conditions, and construction details | Complete |
| Guidance.md | Design rationale and guidance for requirement implementation | Ready |
| Procedure.md | Design process steps and verification approach | Ready |
| _CONTEXT.md | Scope summary and artifact list | Complete |
| _SEMANTIC.md | Semantic analysis and knowledge representation | Complete |
| _SEMANTIC_LENSING.md | Gap analysis and implementation flags | Complete |
| _DEPENDENCIES.md | Cross-package dependencies documented | Complete |
| _MEMORY.md | Design decisions and assumptions tracking | Ready |
| _REFERENCES.md | Source document cross-references | Complete |
| Dependencies.csv | Machine-readable dependency matrix | Complete |

**Responsible:** Design-Builder (Architect/Structural)

**Scope Coverage:** SOW-0300, SOW-0301

**Objective Support:** OBJ-004 (Cold Storage Building Implementation)

**Key Requirements Highlights:**
- REQ-04-01-001: 60' × 100' clear-span interior
- REQ-04-01-002: Unheated building (no mechanical heating)
- REQ-04-01-003: Minimum eave height for fleet operations (TBD with equipment envelope analysis)
- REQ-04-01-004: 20-year design life
- REQ-04-01-005: Clear-span framing system (DB-proposed)
- REQ-04-01-006: Structural loads per ABC/NBC for Penhold, Alberta
- REQ-04-01-011: Condensation/icing prevention via ventilation (detail in DEL-04-04)
- REQ-04-01-014: Site placement within 12-acre developable area
- REQ-04-01-015: ABC compliance and permits (fire separation TBD)

**Known TBDs / Lensing Flags:**
- [A-001] Alberta Building Code edition TBD
- [A-002] Non-combustible material classification verification required
- [A-003] Climatic design data (ground snow load, wind pressure, seismic) TBD
- [B-001] ABC importance category classification TBD
- [B-002] Geotechnical confirmation at cold storage footprint location TBD
- [C-001] Equipment envelope analysis and minimum eave height TBD
- [E-001] Accessibility exemption confirmation TBD
- [F-001] Joint watertightness verification method TBD
- [F-002] Fire separation/spatial separation requirements TBD
- [X-001] Ventilation performance criteria and post-construction verification approach TBD

---

### 2. DEL-04-02: Cold Storage — Doors, Openings & Hardware

**Location:** `/1_Working/DEL-04-02_Cold Storage - Doors, Openings & Hardware/`

**Scope:**
- Door schedule and hardware specification (18 REQs)
- Overhead doors: two (2) units, 16' × 16', motorized openers with remote control
- Person doors: two (2) units, keyed deadbolt hardware
- Window profile alignment with main building
- Concrete aprons at all door access points
- Emergency exit lighting and weatherproof switches
- Vehicle clearance verification for Public Works equipment

**Key Documents:**
| Document | Purpose | Status |
|----------|---------|--------|
| Specification.md | Normative requirements (18 REQs: 4202-01 through 4202-18) | Complete |
| Datasheet.md | Door schedule attributes and hardware basis | Complete |
| Guidance.md | Door selection and coordination guidance | Ready |
| Procedure.md | Verification procedure for door/hardware compliance | Ready |
| _CONTEXT.md | Door schedule context and anticipated artifacts | Complete |
| _SEMANTIC.md | Semantic analysis of door requirements | Complete |
| _SEMANTIC_LENSING.md | Gap analysis and implementation flags | Complete |
| _DEPENDENCIES.md | Cross-deliverable dependencies (PKG-002, DEL-04-03, DEL-04-04) | Complete |
| _MEMORY.md | Design decisions and key coordination items | Ready |
| _REFERENCES.md | Standards and cross-references | Complete |
| Dependencies.csv | Machine-readable dependency matrix | Complete |

**Responsible:** Design-Builder (Architect) with MEP coordination for electrical

**Scope Coverage:** SOW-0302

**Objective Support:** OBJ-004 (Campus Aesthetic Coherence)

**Key Requirements Highlights:**
- REQ-4202-01/02: Two overhead doors, 16' × 16' each
- REQ-4202-03: Window profile identical to main building (PKG-002 cross-reference required)
- REQ-4202-04: Motorized openers with remote control capability
- REQ-4202-06/07/08: Two person doors with keyed deadbolt (same key as pickled-sand building)
- REQ-4202-09: ABC building code egress compliance
- REQ-4202-10/13: Concrete aprons and vehicle clearance for equipment
- REQ-4202-11/12: Emergency exit lighting and weatherproof switches
- REQ-4202-14: Electrical coordination with DEL-04-04

**Known TBDs / Lensing Flags:**
- [A-001] ABC edition and person door minimum dimensions TBD
- [A-003] IES emergency lighting requirements and foot-candle verification TBD
- [C-001/C-002] Fire separation and wind-load rating TBD per ABC
- [C-003] Weatherstripping/sealing specifications TBD
- [E-001] Standards accessibility status and confirmation TBD
- [F-001] Standards accessibility and verification details TBD
- [F-002] Window profile alignment artifact documentation (cross-reference with PKG-002) TBD
- [F-003] Equipment clearance confirmation artifact (graders, tandem dump trucks, loaders, bobcats) TBD
- [X-003] Physical key test verification procedure TBD
- [X-004] Concrete apron cure time specification TBD

**Cross-Package Dependencies:**
- **PKG-002 (Main Building):** Door window profile specification for overhead doors; keying coordination
- **DEL-04-03 (Floor & Foundation):** Concrete apron interface and bearing capacity
- **DEL-04-04 (Electrical & Ventilation):** Overhead door opener electrical supply; emergency lighting and switches
- **Pickled-Sand Storage Building:** Key coordination requirement (currently out of scope but referenced)

---

### 3. DEL-04-03: Cold Storage — Floor & Foundation (DB Proposed)

**Location:** `/1_Working/DEL-04-03_Cold Storage - Floor & Foundation (DB Proposed)/`

**Scope:**
- Design-Builder proposed floor system selection for cold storage operations
- Foundation system proposal (most cost-effective, code-compliant)
- Geotechnical compliance (Union Street Geotechnical Ltd. Report USG1123, Feb 2021)
- Concrete design for severe sulphate exposure (Class S-2)
- Subgrade preparation and proof-rolling requirements
- Concrete aprons at door access points
- Slab/edge details and bearing capacity assumptions

**Key Documents:**
| Document | Purpose | Status |
|----------|---------|--------|
| Specification.md | Normative requirements (12 REQs: REQ-01 through REQ-08, with sub-requirements) | Complete |
| Datasheet.md | Floor/foundation attributes and geotechnical context | Complete |
| Guidance.md | Foundation selection and floor system decision guidance | Ready |
| Procedure.md | Construction procedure and verification steps | Ready |
| _CONTEXT.md | Geotechnical scope and artifact expectations | Complete |
| _SEMANTIC.md | Semantic analysis of foundation/floor requirements | Complete |
| _SEMANTIC_LENSING.md | Gap analysis and implementation flags | Complete |
| _DEPENDENCIES.md | Geotechnical report dependencies and PKG-003 coordination | Complete |
| _MEMORY.md | Foundation design decisions and assumptions | Ready |
| _REFERENCES.md | Geotechnical and code references | Complete |
| Dependencies.csv | Machine-readable dependency matrix | Complete |

**Responsible:** Design-Builder (Structural/Civil Engineer) with Geotechnical Consultant

**Scope Coverage:** SOW-0303, SOW-0304

**Objective Support:** OBJ-004

**Key Requirements Highlights:**
- REQ-01: Foundation system proposal (most cost-effective, code-compliant)
- REQ-01A: Seismic design loads (Seismic Site Class C per geotechnical report)
- REQ-02: Frost design (2.0 m frost penetration depth for Penhold region)
  - Driven piles: minimum 5.3 m embedment
  - Screw piles: upper helical plate below 2.0 m frost depth
  - Shallow footings: minimum 2.0 m founding depth
- REQ-03: Bearing stratum on native sand or till (avoid high-plasticity clay)
- REQ-04: Single foundation system type (no mixing)
- REQ-05: Single floor solution proposal (two OSR options cited: asphalt millings + concrete strips, or full concrete)
- REQ-06: Concrete aprons at all door access points
- REQ-07: Concrete mix design (severe sulphate exposure Class S-2)
  - Sulphate-resistant cement (Type HS or Type 10 + fly ash)
  - Minimum 32 MPa 56-day strength
  - Maximum w/c ratio 0.45
  - Air entrainment required

**Known TBDs / Lensing Flags:**
- [A-003] Floor live load criteria TBD
- [B-001] Geotechnical site confirmation and additional investigation TBD
- [B-002] Borehole coverage adequacy for cold storage footprint TBD
- [C-002] Scope boundary clarification: building-perimeter drainage (first 3.0 m) vs. site-level drainage (PKG-003)
- [D-001] Concrete curing specification and duration TBD
- [E-001] Air entrainment percentage (per CAN/CSA A23.1 Table 4) TBD
- [E-002] Vapour barrier thickness, lap width, and sealing method TBD
- [F-001] Minimum concrete slab thickness TBD by structural engineer
- [F-002] Proof-roll acceptance criteria and soft-spot remediation TBD

**Cross-Package Dependencies:**
- **Geotechnical Report (Union Street Geotechnical Ltd., File USG1123, Feb 2021):** Frost depth, seismic site class, bearing stratum, pile/footing recommendations
- **PKG-003 (Site & Civil Works):** Grading and site-level drainage coordination; scope boundary at building perimeter
- **DEL-04-01 (Design Basis):** Building footprint and height confirmation for structural analysis
- **DEL-04-02 (Doors & Hardware):** Concrete apron locations and vehicle loading basis

---

### 4. DEL-04-04: Cold Storage — Electrical & Ventilation

**Location:** `/1_Working/DEL-04-04_Cold Storage - Electrical & Ventilation/`

**Scope:**
- Electrical power distribution and receptacle layout (interior and exterior)
- Overhead door opener electrical supply (two motorized doors)
- Interior and emergency exit lighting (IES-compliant LED)
- Ventilation/air circulation system to prevent condensation and icing
- Weatherproof electrical devices at person door locations
- Grounding system (CEC compliance)
- Electrical code compliance (Canadian Electrical Code)

**Key Documents:**
| Document | Purpose | Status |
|----------|---------|--------|
| Specification.md | Normative requirements (13+ REQs: R-01 through R-13, enriched) | Complete |
| Datasheet.md | Electrical/ventilation attributes, climate conditions, and operational context | Complete |
| Guidance.md | MEP design guidance for lighting and ventilation | Ready |
| Procedure.md | Construction and verification procedures | Ready |
| _CONTEXT.md | MEP scope summary and anticipated deliverables | Complete |
| _SEMANTIC.md | Semantic analysis of electrical/ventilation requirements | Complete |
| _SEMANTIC_LENSING.md | Gap analysis and implementation flags (extensive enrichment) | Complete |
| _DEPENDENCIES.md | DEL-04-01, DEL-04-02, equipment operational requirements | Complete |
| _MEMORY.md | Design decisions and engineering considerations | Ready |
| _REFERENCES.md | Code standards and cross-references | Complete |
| Dependencies.csv | Machine-readable dependency matrix | Complete |

**Responsible:** Design-Builder (MEP Engineer)

**Scope Coverage:** SOW-0300 (MEP aspects)

**Objective Support:** OBJ-004

**Key Requirements Highlights:**
- R-01: Electrical system for current needs and future flexibility
- R-02/03: Interior and exterior electrical receptacles (quantity TBD)
- R-04: Dedicated circuits for two motorized overhead door openers with remote control
- R-05: Grounding system per CEC (ground resistance limit TBD)
- R-06: IES-compliant interior lighting with LED fixtures
- R-07: Lighting fixture height adjusted to avoid equipment interference
- R-08: Emergency exit lighting above person doors with battery backup
- R-09: Weatherproof switches at person door locations
- R-10: Condensation/icing prevention via ventilation or air circulation
- R-11: Ventilation method and sizing (DB-proposed, with stamped calculations)
- R-12: Durable, non-combustible, watertight materials
- R-13: CEC and ABC compliance

**Known TBDs / Lensing Flags:**
- [A-003] Lighting foot-candle target for storage occupancy category per IES TBD
- [A-004] Electrical service size (amps) from load calculation TBD
- [B-001] Ceiling/eave/ridge height from DEL-04-01 required for fixture height and ventilation sizing
- [B-002] Exterior building-mounted lighting requirement TBD (explicitly to be confirmed)
- [B-003] Climate data (design temperatures, HDD, CDD, humidity, wind speed, precipitation) TBD
- [B-005] Exterior lighting scope confirmation (interior/exterior distinction unclear in OSR)
- [C-2/C-003] Interior receptacle quantity and spacing guidance TBD
- [C-004] Cold-temperature rating requirements for emergency exit lights TBD
- [C-5] Maximum stored equipment height for fixture height planning TBD
- [D-001] Emergency exit light placement per Alberta Fire Code TBD
- [D-003] Cold-temperature rated LED specifications TBD
- [E-002] Block heater receptacles requirement confirmation TBD (operational need in Alberta)
- [E-003] Maintenance access planning and equipment height confirmation TBD
- [F-001] Stamped engineering calculations for ventilation design TBD
- [X-001] Condensation risk analysis methodology and performance verification TBD
- [X-004] CEC ground resistance acceptance value (ohms) TBD

**Cross-Package Dependencies:**
- **DEL-04-01 (Design Basis):** Building height (eave/ridge/ceiling) for fixture height and ventilation sizing
- **DEL-04-02 (Doors & Hardware):** Overhead door opener electrical load; emergency lighting locations; weatherproof switch placement
- **Environmental Data:** Climate normals for Penhold, AB (Environment Canada); Seismic hazard data for ventilation passive approach assessment
- **Standards:** Canadian Electrical Code (edition TBD); IES Illuminating Engineering Society recommendations; Alberta Fire Code

**Enrichment Status:** This deliverable received the most extensive semantic lensing enrichment, with 20+ implementation flags (A-001 through X-004) capturing design gaps, TBD items, and verification needs.

---

## Directory Structure and File Organization

All deliverables are organized in the `1_Working` subdirectory with a consistent structure:

```
PKG-004_Cold Storage Building (Unheated, 60'x100')/
└── 1_Working/
    ├── DEL-04-01_Cold Storage - Design Basis & Configuration/
    │   ├── Specification.md          (normative requirements)
    │   ├── Datasheet.md              (descriptive attributes)
    │   ├── Guidance.md               (design rationale)
    │   ├── Procedure.md              (process and verification)
    │   ├── _CONTEXT.md               (scope and artifacts)
    │   ├── _SEMANTIC.md              (knowledge representation)
    │   ├── _SEMANTIC_LENSING.md     (gap analysis)
    │   ├── _DEPENDENCIES.md          (cross-package links)
    │   ├── _MEMORY.md                (design decisions)
    │   ├── _REFERENCES.md            (source citations)
    │   ├── _STATUS.md                (current state: SEMANTIC_READY)
    │   └── Dependencies.csv          (machine-readable matrix)
    │
    ├── DEL-04-02_Cold Storage - Doors, Openings & Hardware/
    │   └── [same 12-file structure as DEL-04-01]
    │
    ├── DEL-04-03_Cold Storage - Floor & Foundation (DB Proposed)/
    │   └── [same 12-file structure as DEL-04-01]
    │
    └── DEL-04-04_Cold Storage - Electrical & Ventilation/
        └── [same 12-file structure as DEL-04-01]
```

**Total File Count:** 48 files across 4 deliverables (12 files per deliverable)

---

## Completeness Assessment

### Strengths

1. **Comprehensive Specification Coverage**
   - All four deliverables have detailed, normative requirements (totaling 60+ requirements across the package)
   - Requirements are well-sourced with explicit citations to the OSR (Owner's Statement of Requirements), RFP, and design decisions
   - Clear traceability from requirements to scope items (SOW-0300 through SOW-0304)

2. **Structured Documentation Framework**
   - Consistent 4-document bundle format enables knowledge aggregation and semantic analysis
   - Specification, Datasheet, Guidance, and Procedure documents provide both normative and descriptive information
   - Semantic enrichment files (_SEMANTIC, _SEMANTIC_LENSING, _DEPENDENCIES, _MEMORY) support knowledge representation and impact analysis

3. **Semantic Readiness**
   - All deliverables have achieved SEMANTIC_READY status following CHIRALITY_FRAMEWORK enrichment
   - Lensing analysis has identified 40+ implementation gaps and TBD items, promoting visibility and accountability
   - Cross-package dependencies are explicitly documented and linked

4. **Design-Build Alignment**
   - Appropriate use of "DB Proposed" language in DEL-04-03 (floor/foundation) to allow Design-Builder flexibility while maintaining performance requirements
   - Clear delineation between mandatory requirements and Design-Builder proposed solutions
   - Owner coordination points and assumptions clearly marked

5. **Integration with Broader Project**
   - Scope boundaries clearly established (with notes on out-of-scope items, e.g., pickled-sand storage removed)
   - Cross-package dependencies documented (references to PKG-002, PKG-003, PKG-005)
   - Aesthetic coordination with main building (PKG-002) specified

### Gaps and Concerns

1. **Design Development Status**
   - **Status:** Proposal-phase specifications; not yet issued for construction (IFC)
   - All deliverables are in active development and contain numerous TBDs
   - No issued-for-construction (IFC) design drawings are present in the deliverable package
   - Anticipated artifacts (general arrangement drawings, elevations, door schedules, etc.) are referenced but not yet delivered

2. **Standards and Code References**
   - **Alberta Building Code (ABC) Edition TBD:** Multiple requirements depend on confirmation of the applicable ABC edition (affects structural loads, importance categories, accessibility, fire separation, etc.)
   - **Canadian Electrical Code (CEC) Edition TBD:** Electrical grounding and compliance basis not finalized
   - **Canadian Standards (CSA) Population TBD:** DEL-04-01 Spec Table identifies three CSA standard slots (A23.3, O86, S136 candidates) but actual selections TBD
   - **IES Illuminating Engineering Society Standards:** Specific lighting foot-candle values and emergency lighting requirements reference IES standards not directly accessed; DB must confirm

3. **Geotechnical and Site-Specific Information**
   - **Geotechnical Confirmation TBD:** Existing borehole data (BH101-BH116) provided in the Feb 2021 geotechnical report may not cover the cold storage footprint location; additional investigation may be required (cost borne by DB)
   - **Climate Design Data TBD:** Ground snow load, wind pressure, and seismic hazard values for Penhold, AB must be extracted from ABC Appendix C during design development
   - **Scope Boundary (DEL-04-03 [C-002]):** Building-perimeter drainage (first 3.0 m from building) is DEL-04-03 responsibility; site-level drainage is PKG-003 responsibility; coordination required but not yet formalized

4. **Design Verification and Test Procedures**
   - **Equipment Clearance Artifact TBD (DEL-04-02 [F-003]):** Door opening height (16'×16') must be verified against actual Public Works equipment inventory; no equipment list is currently referenced or attached
   - **Window Profile Alignment Documentation TBD (DEL-04-02 [F-002]):** Cross-reference with PKG-002 main building overhead door specification required; comparison artifact (drawing overlay, manufacturer model confirmation, side-by-side spec sheet) not yet prepared
   - **Condensation Risk Analysis TBD (DEL-04-04 [X-001]):** Ventilation design methodology and post-construction verification approach (winter monitoring protocol, temperature/humidity logging) not yet detailed
   - **Concrete Apron Cure Time TBD (DEL-04-02 [X-004]):** Minimum cure time and early loading restrictions not specified; delegated to structural/civil designer specification
   - **Proof-Roll Acceptance Criteria TBD (DEL-04-03 [F-002]):** Geotechnical engineer must establish quantitative rut depth/deflection limits for proof-rolling acceptance

5. **Operational and Maintenance Gaps**
   - **Equipment Storage Height TBD (DEL-04-04 [C-5], DEL-04-04 [E-003]):** Maximum height of equipment to be stored in cold storage (tractors, graders, loaders, bobcats) not yet confirmed; impacts lighting fixture height, maintenance access, and ventilation opening placement
   - **Minimum Eave Height TBD (DEL-04-01 [C-001]):** Building height must support "safe maneuverability for loading and unloading" but no numeric minimum eave height is specified; DB must conduct equipment envelope analysis during design development
   - **Block Heater Receptacles TBD (DEL-04-04 [E-002]):** Common in Alberta cold-climate operations but not explicitly required; Owner confirmation needed on whether block heater receptacles are operationally necessary

6. **Electrical and Code Compliance Gaps**
   - **Electrical Service Size TBD (DEL-04-04 [A-004]):** Total electrical load (lighting, receptacles, two door openers, ventilation fans if active, block heaters if required) not yet calculated; service size must be determined by DB MEP engineer
   - **Exterior Lighting Scope TBD (DEL-04-04 [B-002], [B-005]):** OSR §10.5 addresses lighting generally but does not clearly differentiate interior vs. exterior building-mounted lighting for the cold storage building; this ambiguity must be resolved with the Owner
   - **CEC Ground Resistance Value TBD (DEL-04-04 [X-004]):** Canadian Electrical Code specifies ground resistance limits, but the specific acceptance value (in ohms) is not stated in the deliverables

7. **Key Coordination and Interface Points**
   - **PKG-002 (Main Building) Interface:** Window profile alignment for overhead doors, keying coordination for person doors — requires active coordination during design development; no formal interface document or IFC schedule is present
   - **PKG-003 (Site & Civil Works) Interface:** Building drainage, site grading, foundation perimeter preparation — scope boundary at 3.0 m from building; coordination approach not yet formalized
   - **Pickled-Sand Storage Building (out of scope but referenced):** Key coordination for person door locks specified in DEL-04-02; this building was removed from procurement per Addendum 03 but is still referenced in requirements — clarification needed

8. **Document Artifacts Not Yet Delivered**
   - General arrangement drawings (floor plan showing 60'×100' footprint)
   - Elevations and sections (showing building height, openings, door locations)
   - Clear-span framing concept narrative or sketch
   - Door schedule (tabular format with door marks, sizes, hardware sets, openers)
   - Hardware specifications and basis-of-design
   - Ventilation design calculations (stamped by MEP engineer)
   - Condensation risk analysis
   - Equipment clearance verification matrix
   - Structural/civil calculations (foundation selection, concrete design, subgrade preparation)
   - Electrical one-line diagram and load calculation
   - Lighting design and fixture schedule

---

## Quality Assessment

### Positive Indicators

1. **Requirements Discipline:** Requirements are written using clear imperative language ("shall"), with explicit sources and status designations (Mandatory, Informational, TBD)
2. **Traceability:** Each requirement is linked to source documents (OSR sections, SOW items, design decisions)
3. **Assumption Documentation:** Design assumptions and TBDs are explicitly flagged with [lensing item] codes for tracking
4. **Semantic Enrichment:** The addition of _SEMANTIC, _LENSING, and _DEPENDENCIES files shows a commitment to knowledge representation and impact analysis
5. **Design-Builder Flexibility:** Appropriate use of "DB Proposed" and "DB shall determine" language balances Owner control with Design-Builder cost optimization

### Concerns

1. **TBD Density:** High number of TBDs (40+ across package) indicates incomplete definition of design baseline; typical for proposal phase but should be resolved before IFC
2. **Assumption Dependencies:** Multiple requirements depend on unconfirmed assumptions (e.g., ABC edition, geotechnical site conditions, climate data)
3. **Document Maturity:** Specification and datasheet documents are mature; Guidance and Procedure documents marked "Ready" but not fully reviewed
4. **Artifact Absence:** Deliverables are specification/requirements documents; design drawings and calculations are not yet present (expected for proposal phase but should be present before IFC)
5. **Cross-Package Coordination:** References to PKG-002, PKG-003, and pickled-sand building indicate dependencies that may create coordination risks if not actively managed

---

## Known Issues and Action Items

### Critical Path Items (must be resolved before IFC)

1. **ABC Edition Confirmation** (affects DEL-04-01, 02, 03, 04)
   - Action: Owner to confirm applicable ABC edition; DB to extract climatic design data (Ss, q, Sa) and implement structural/code requirements
   - Impact: Structural loads, importance category, accessibility, emergency lighting, wind-load rating

2. **Geotechnical Site Confirmation** (DEL-04-03)
   - Action: DB to confirm that existing borehole coverage (BH101-BH116) is adequate for proposed cold storage footprint; if not, DB to commission additional investigation and bear cost
   - Impact: Foundation system selection, bearing stratum confirmation, frost design depth

3. **Equipment Clearance and Height Verification** (affects DEL-04-01, 04)
   - Action: Operations/Owner to provide actual equipment list (tractors, graders, loaders, bobcats, pickup trucks with attachments) with maximum heights; DB to design building height and lighting/ventilation accordingly
   - Impact: Minimum eave height, lighting fixture placement, ventilation opening sizing

4. **PKG-002 Interface Finalization** (DEL-04-02)
   - Action: DB to obtain main building overhead door specification (manufacturer, model, window panel configuration) and confirm compatibility; prepare cross-reference artifact
   - Impact: Door schedule, aesthetic coordination, window profile alignment

### Design Development Items (TBD Resolution)

5. **Concrete Design and Slab Thickness** (DEL-04-03)
   - Action: Structural engineer to finalize concrete mix design (severe sulphate exposure S-2 per geotechnical report), establish minimum slab thickness based on loads and bearing conditions
   - Required Inputs: Floor live loads (TBD), bearing soil properties, equipment loading from operations

6. **Ventilation Design and Condensation Analysis** (DEL-04-04)
   - Action: MEP engineer to propose ventilation method (active fans, passive openings, or hybrid), conduct condensation risk analysis for Penhold climate, provide stamped calculations
   - Required Inputs: Climate data (temperature, humidity, design conditions), building height/configuration from DEL-04-01, equipment storage duration and operational profile

7. **Electrical Load Calculation and Service Sizing** (DEL-04-04)
   - Action: MEP engineer to calculate connected electrical load (lighting, receptacles, two door openers, ventilation fans, block heaters if required) and specify service size (amps)
   - Required Inputs: Lighting fixture schedule, receptacle quantity and duty cycles, door opener specifications, ventilation method

8. **Lighting Design and Foot-Candle Target** (DEL-04-04)
   - Action: Lighting designer to select LED fixtures with cold-temperature ratings, determine IES foot-candle target for storage occupancy category, prepare fixture schedule
   - Required Inputs: IES recommendations for storage facility occupancy (foot-candle value TBD), maximum equipment height for fixture placement clearance

### Post-Design Items (After IFC Issuance)

9. **Window Profile Alignment Verification** (DEL-04-02)
   - Action: Before construction, physical key test to confirm that person door deadbolt keys function identically across cold storage and pickled-sand buildings (if pickled-sand building scope is restored)
   - Impact: Operational ease of access

10. **Proof-Roll and Subgrade Acceptance** (DEL-04-03)
    - Action: Geotechnical engineer of record to establish and monitor proof-roll acceptance criteria (rut depth, deflection limits); remediate soft/pumping areas
    - Impact: Foundation/slab performance

11. **Condensation and Icing Winter Monitoring** (DEL-04-04)
    - Action: During first winter season, monitor interior conditions (temperature, humidity, visual inspection for condensation/icing) to verify ventilation system adequacy
    - Impact: Operational performance validation

---

## Cross-Package Dependencies Summary

| Dependency | Source | Target | Type | Status |
|------------|--------|--------|------|--------|
| Main building overhead door specification | PKG-002 | DEL-04-02 | Window profile alignment | TBD |
| Main building key/keying coordination | PKG-002 | DEL-04-02 | Person door deadbolt keying | TBD |
| Site grading and drainage | PKG-003 | DEL-04-03 | Foundation perimeter drainage coordination | TBD |
| Building height and roof configuration | DEL-04-01 | DEL-04-04 | Lighting fixture height, ventilation opening placement | TBD |
| Door opener specifications | DEL-04-02 | DEL-04-04 | Electrical circuit and load requirements | TBD |
| Concrete apron locations and loads | DEL-04-02, 04 | DEL-04-03 | Slab thickness and bearing design | TBD |
| Geotechnical Report (USG1123, Feb 2021) | External | DEL-04-03 | Foundation system and concrete design basis | TBD Confirmation |
| Pickled-sand storage building (out of scope) | OSR / Addendum 03 | DEL-04-02 | Person door key coordination (if scope restored) | Clarification Needed |

---

## Recommendations

### For Design Team

1. **Immediately Resolve ABC Edition:** Confirm the applicable Alberta Building Code edition with the Owner and Authority Having Jurisdiction (AHJ) at project start; extract climatic design data and implement all edition-specific requirements

2. **Conduct Early Coordination Meetings:**
   - With PKG-002 design team: finalize overhead door specification alignment and keying coordination
   - With PKG-003 site team: establish formal scope boundary at building perimeter (3.0 m) and drainage coordination interface
   - With Owner/Operations: obtain equipment list with maximum heights, confirm block heater receptor need, clarify exterior lighting requirement

3. **Commission Supplemental Geotechnical Investigation (if needed):** If existing borehole coverage is inadequate for the proposed cold storage footprint, initiate additional site investigation immediately to avoid schedule delays

4. **Develop Equipment Envelope Analysis:** Prepare a detailed analysis of the largest equipment expected to be stored (height, width, access needs) to establish minimum eave height and lighting/ventilation fixture placement clearances

5. **Prepare Cross-Reference Artifacts Early:** For door schedule (DEL-04-02), obtain PKG-002 specifications and prepare side-by-side window profile comparison and manufacturer model alignment documentation before design finalization

6. **Specify Cold-Temperature Equipment:** Confirm that all electrical fixtures (LED lights, emergency exit lights, receptacles) and ventilation components have cold-temperature ratings suitable for unheated Alberta storage

### For Owner/Project Manager

1. **Clarify Scope Boundaries:**
   - Confirm whether the pickled-sand storage building (removed per Addendum 03) may be restored in scope; if not, remove DEL-04-02 references to pickled-sand building keying coordination
   - Clarify exterior lighting requirement for the cold storage building (scope item [B-005] in DEL-04-04)

2. **Provide Design Inputs:**
   - Equipment list with maximum heights and storage duration (seasonal vs. year-round)
   - Operational needs (e.g., block heater receptacles, access requirements)
   - Confirmation of building height suitability for fleet maneuvering

3. **Establish Coordination Protocol:**
   - Formal interface agreement with PKG-002 team on door specifications and keying
   - Drainage coordination agreement with PKG-003 team (3.0 m building-perimeter scope boundary)
   - AHJ pre-submission meeting to confirm ABC edition, code requirements, and permit path

4. **Schedule Verification Reviews:**
   - Design development phase: review DEL-04-01 building height and general arrangement, confirm against equipment clearance analysis
   - 50% IFC phase: review door schedule (DEL-04-02) with window profile alignment artifact; confirm ventilation calculations (DEL-04-04)
   - 100% IFC phase: confirm all TBDs resolved, all drawings and calculations complete, all cross-package coordination finalized

### For Quality Assurance

1. **Traceability Verification:** Confirm that all artifacts listed in _CONTEXT.md for each deliverable are eventually produced and traced to requirements
2. **TBD Closure:** Monitor lensing flags and TBD items; ensure each is assigned ownership and closure target date
3. **Standards Accessibility:** Before IFC issuance, confirm that all referenced standards (ABC edition, CEC, CSA standards, IES recommendations) are accessible to the design team
4. **Peer Review:** Conduct independent specification review of each deliverable to identify gaps, inconsistencies, or ambiguities before final issue

---

## Conclusion

Package PKG-004 represents a comprehensive, well-structured set of proposal-phase specifications for the cold storage building component of the Penhold Public Services Building project. The deliverables demonstrate strong requirements discipline, semantic enrichment, and integration with the broader project scope.

**Current Status:** All four deliverables have achieved **SEMANTIC_READY** status with 40+ identified TBDs and gaps captured in lensing analysis. The package is suitable for design-build proposal development and requires active management of cross-package dependencies and owner coordination to advance to IFC phase.

**Key Strengths:**
- Comprehensive, well-sourced requirements (60+ across package)
- Clear scope boundaries and out-of-scope designations
- Explicit handling of Design-Builder proposed solutions and owner coordination points
- Semantic enrichment files supporting knowledge representation and impact analysis

**Key Concerns:**
- High TBD density indicates incomplete design baseline; typical for proposal phase but should be resolved before IFC
- Multiple dependencies on unconfirmed external inputs (ABC edition, climate data, geotechnical confirmation, equipment clearance)
- Design drawings, calculations, and detail artifacts not yet present in deliverable package
- Cross-package coordination interfaces require active management

**Next Steps:**
1. Resolve ABC edition and climatic design data (critical path)
2. Confirm geotechnical site conditions (if not fully covered by existing investigation)
3. Obtain equipment clearance and operational requirements from Owner
4. Finalize PKG-002 and PKG-003 coordination interfaces
5. Develop detailed design and prepare artifact deliverables for IFC phase

---

**Document Prepared:** 2026-02-19
**Review Period:** PKG-004 Deliverables Summary (DEL-04-01 through DEL-04-04, Status: SEMANTIC_READY)
**Prepared By:** Deliverables Analysis (Execution-6a Review)
