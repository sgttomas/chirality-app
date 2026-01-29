# Specification: DEL-09.02 Marine Outfitting Technical Specification

## Scope

This specification defines the requirements for producing **Marine Outfitting Technical Specification** within **PKG-09 Marine Outfitting**.

**Decomposition definition (authoritative):** Defines performance, materials, and workmanship requirements for marine outfitting per Employer's Requirements. (**Source:** Decomposition, DEL-09.02 row)

**Package scope (PKG-09):** Fenders, bollards, ladders, life-saving equipment, existing Berth 10 upgrades and repairs. (**Source:** Decomposition, PKG-09)

**Anticipated deliverable artifacts:**
- Fender specification
- Bollard specification
- Marine hardware specification

**Purpose:** This specification is the **controlling document** for materials, workmanship, and testing requirements for all PKG-09 scope items. It governs procurement (vendor selection basis), fabrication (quality expectations), and installation (acceptance criteria).

## Requirements

### 1) Specification Structure Requirements

The technical specification shall include the following sections (as applicable). Cross-reference to `Datasheet.md` Content Checklist and `Guidance.md` principles.

#### 1.1 Scope and Definitions

**Requirements:**
- Scope statement shall explicitly define inclusions and exclusions consistent with PKG-09 package scope (fenders, bollards, ladders, life-saving equipment, existing Berth 10 upgrades/repairs).
- Definitions and abbreviations section shall define technical terms used in the specification.
- Referenced documents section shall list all cited standards, codes, drawings, calculations, and other deliverables (including DEL-09.01, DEL-09.03, DEL-09.04, DEL-09.05, applicable PKG-08 deliverables).
- **TBD:** Specific scope boundaries with PKG-08 Marine Structures (e.g., where does structural design end and outfitting begin?) and PKG-11 Marine Loading System.

**Rationale:** See `Guidance.md § Principles (Specification Intent)`.
**Verification:** See `Procedure.md § Steps 1, 5` (scope confirmation, self-check for completeness).

#### 1.2 Applicable Codes and Standards

**Requirements:**
- List of applicable codes and standards from Employer's Requirements shall be included. (**TBD** — ER clauses to be extracted)
- Marine industry standards shall be cited where applicable, which may include:
  - PIANC (World Association for Waterborne Transport Infrastructure) guidelines for marine fender systems
  - BS 6349 (British Standard for Maritime Works) or equivalent for bollards and mooring equipment
  - OSHA / CSA (Canadian Standards Association) occupational safety codes for ladders and access (e.g., CSA Z259 series)
  - Transport Canada or provincial port authority requirements for life-saving equipment
  - NFPA (National Fire Protection Association) or equivalent for marine safety equipment (if applicable)
- **TBD:** Specific codes and standards to be confirmed from Employer's Requirements and applicable authority requirements.
- **ASSUMPTION:** Where ER does not specify, industry-standard marine/port codes apply (to be confirmed during design development).

**Rationale:** See `Guidance.md § Principles (Evidence Rules)`.
**Verification:** See `Procedure.md § Step 2` (extract requirements from sources).

#### 1.3 Design Basis

**Requirements:**
- Design vessel characteristics shall be stated, including:
  - Vessel type, length overall (LOA), beam, displacement (**TBD** — from ER and berthing energy analysis DEL-08.06)
  - Design approach velocity, berthing angle (**TBD** — from DEL-08.06)
  - Mooring arrangement (number of lines, line types, pretension) (**TBD** — from mooring analysis DEL-08.09)
- Environmental conditions shall be stated, including:
  - Wind speed (sustained, gust) (**TBD**)
  - Current velocity (**TBD**)
  - Wave height (significant wave height, design wave) (**TBD**)
  - Tidal range (high water, low water, mean tide levels) (**TBD**)
  - Temperature range (ambient air, water) (**TBD**)
- Service life and design life requirements shall be stated. (**TBD** — from ER; **ASSUMPTION:** Typical marine structures 25-50 year design life)

**Rationale:** See `Guidance.md § Considerations (Design Inputs)`.
**Verification:** See `Procedure.md § Step 2` (gather design inputs).

#### 1.4 Corrosion Protection Requirements

**Requirements:**
- Environmental exposure classification shall be defined for each equipment category:
  - **Immersed zone:** Equipment below low water level (continuous immersion)
  - **Splash zone:** Equipment between low water and high water plus splash (cyclic wetting, most severe corrosion environment)
  - **Atmospheric zone:** Equipment above splash zone (salt spray, UV exposure)
- Coating system requirements shall be specified for steel components, including:
  - Coating type (e.g., epoxy, polyurethane) (**TBD**)
  - Number of coats (primer, intermediate, topcoat) (**TBD**)
  - Total dry film thickness (DFT) (**TBD**)
  - Surface preparation (e.g., SSPC-SP10 near-white blast cleaning) (**TBD**)
  - Application requirements (environmental conditions, curing) (**TBD**)
- Hot-dip galvanizing requirements shall be specified for structural steel components where applicable, including:
  - Galvanizing standard (e.g., ASTM A123, ISO 1461) (**TBD**)
  - Minimum coating thickness (**TBD**)
- Stainless steel or corrosion-resistant alloy requirements shall be specified for hardware/fasteners, including:
  - Material grade (e.g., 316 stainless steel for marine environment) (**TBD**)
  - Fastener specifications (material, coating, passivation) (**TBD**)
- **Coordination:** Corrosion protection requirements shall be coordinated with PKG-08 Marine Structures and PKG-26 Protective Coatings (if applicable) for system consistency.

**Rationale:** See `Guidance.md § Considerations (Corrosion Protection)`.
**Verification:** See `Procedure.md § Steps 3, 6` (draft specification, IDC with PKG-08/PKG-26).

#### 1.5 Installation Requirements

**Requirements:**
- General installation requirements for marine outfitting items shall be specified, including:
  - Setting-out and alignment tolerances (**TBD** — coordinate with PKG-08 structural tolerances)
  - Fixing methods (welding, bolting, grouting, adhesive bonding) and requirements
  - Environmental conditions for installation (temperature, weather restrictions)
  - Access and staging requirements
- Interface requirements with marine structure (PKG-08) shall be specified:
  - Connection types and details (coordinate with DEL-08.01 drawings and DEL-08.03 calculations)
  - Load transfer requirements (fender reaction forces, bollard loads, ladder live loads)
  - Structural capacity verification (PKG-08 to confirm structural adequacy)
- **TBD:** Specific installation tolerances and interface requirements to be confirmed during design development.

**Rationale:** See `Guidance.md § Considerations (Interface Coordination)`.
**Verification:** See `Procedure.md § Steps 3, 6` (draft specification, IDC with PKG-08). Installation compliance verification per DEL-09.05.

#### 1.6 Quality / Inspection Requirements

**Requirements:**
- Inspection and testing requirements shall be specified for each equipment category (fenders, bollards, ladders, life-saving equipment).
- Hold points and witness points shall be defined for critical inspection activities:
  - **Hold point:** Work shall not proceed without inspector approval (e.g., welding procedure qualification, proof load testing)
  - **Witness point:** Inspector shall be notified but work may proceed if inspector not available (e.g., coating application)
  - **TBD:** Specific hold/witness points to be defined per project quality plan and Employer's Requirements.
- Certification requirements shall be specified:
  - Material test reports (MTRs) / mill certificates for steel components
  - Welding procedure specifications (WPS) and welder qualifications
  - Coating inspection reports and DFT measurements
  - Proof load test certificates (bollards, if required)
  - Product certifications (life-saving equipment, ladder safety features)
  - **TBD:** Specific certification requirements per ER and project quality plan.
- Non-conformance and corrective action procedures shall be specified or referenced (per project quality procedures).

**Rationale:** See `Guidance.md § Principles (Specification Intent)`.
**Verification:** See `Procedure.md § Step 4` (define quality/testing requirements).

#### 1.7 Submittal Requirements

**Requirements:**
- The following submittals shall be required (cross-reference to related PKG-09 deliverables):
  - **Data sheets (DEL-09.04):** Vendor datasheets for fenders, bollards, ladders, life-saving equipment demonstrating compliance with specification requirements
  - **Certificates and test reports:** Material certificates, weld qualifications, coating inspection reports, proof load test reports (per § 1.6 above)
  - **Calculations (DEL-09.03):** Design calculations verifying performance requirements (fender energy absorption, bollard capacity, ladder structural adequacy)
  - **Inspection and test plans (ITPs):** Detailed inspection/test procedures for critical activities (cross-reference DEL-09.05)
  - **Installation procedures:** Method statements for installation of fenders, bollards, ladders (if required by ER or project quality plan)
  - **As-built documentation:** Revisions to drawings (DEL-09.01) reflecting as-installed conditions
- Submittal review and approval process shall be specified or referenced (per project document control procedures). (**TBD**)
- Submittal schedule and lead times shall be coordinated with construction schedule. (**TBD**)

**Rationale:** See `Guidance.md § Principles (Specification Intent)`.
**Verification:** See `Procedure.md § Step 4` (define submittal requirements).

### 2) Content Coverage Requirements

The specification shall contain explicit requirements for each equipment category. Requirements shall be written in verifiable terms (performance criteria, acceptance criteria, test methods clearly stated).

#### 2.1 Fenders

**Performance Requirements:**
- Berthing energy absorption capacity shall be specified (in kJ or equivalent), derived from berthing energy calculations (DEL-08.06). (**TBD** — pending DEL-08.06 results)
- Reaction force limits shall be specified (maximum reaction force at rated deflection in kN), ensuring marine structure can support fender loads (coordinate with PKG-08 structural capacity). (**TBD** — pending DEL-08.06 results and PKG-08 coordination)
- Deflection characteristics shall be specified (reaction force vs deflection curve per DEL-08.07), confirming vessel hull clearance during compression. (**TBD** — pending DEL-08.07 data)
- Rated deflection (% of fender dimension) shall be specified. (**TBD**)

**Material Requirements:**
- Rubber compound shall be specified:
  - Rubber type (natural rubber, synthetic rubber, or blend) (**TBD**)
  - Rubber grade/hardness (Shore A hardness) (**TBD**)
  - UV resistance, ozone resistance (per ASTM D1149 or equivalent) (**TBD**)
  - Temperature range (operating temperature limits) (**TBD**)
- Steel backing/hardware materials shall be specified:
  - Steel grade (e.g., ASTM A36, A572) (**TBD**)
  - Corrosion protection (coating system per § 1.4 or galvanizing) (**TBD**)
- Fasteners and attachment hardware shall be specified (material, grade, corrosion protection). (**TBD**)

**Workmanship Requirements:**
- Manufacturing quality standards shall be specified (e.g., ISO 9001 or equivalent). (**TBD**)
- Dimensional tolerances for fender components shall be specified. (**TBD**)
- Bonding requirements for rubber-to-steel interfaces shall be specified (if applicable). (**TBD**)

**Testing Requirements:**
- Factory acceptance testing (FAT) shall be specified:
  - Compression testing to verify deflection characteristics (per DEL-08.07 or fender manufacturer's standard)
  - Visual inspection and dimensional verification
  - Material property testing (rubber hardness, tensile strength) (**TBD** — per applicable standard)
- Proof load testing (if required) shall be specified. (**TBD** — per ER or project requirements)
- Test reporting requirements shall be specified (format, content, certification).

**Installation Requirements:**
- Mounting and anchorage details shall be specified (coordinate with DEL-09.01 drawings).
- Alignment tolerances shall be specified. (**TBD**)
- Inspection requirements during installation shall be specified (witness points, hold points per § 1.6).

**Rationale:** See `Guidance.md § Principles (Fenders)`.
**Verification:** See `Procedure.md § Step 3` (draft fender requirements). Performance substantiated by DEL-09.03 calculations and DEL-09.04 datasheets.

#### 2.2 Bollards

**Performance Requirements:**
- Safe working load (SWL) shall be specified (in kN or tonnes bollard pull), derived from mooring analysis (DEL-08.09). (**TBD** — pending DEL-08.09 results)
- Design load factors shall be specified per applicable codes:
  - Ultimate load capacity (factored load) (**TBD** — per code requirements, typically 2.0–2.5 × SWL)
  - Proof load (if testing required) (**TBD** — per ER/code requirements, typically 1.5 × SWL)
- Bollard capacity shall accommodate maximum mooring line loads for design vessel under all environmental conditions (coordinate with DEL-08.09). (**TBD** — pending mooring analysis)

**Material Requirements:**
- Steel type and grade shall be specified:
  - Cast steel (e.g., ASTM A27 Grade 65-35 or equivalent) for cast bollards (**TBD**)
  - Fabricated steel (e.g., ASTM A572 Grade 50 or equivalent) for fabricated bollards (**TBD**)
  - Corrosion protection (coating system per § 1.4) (**TBD**)
- Base plate and anchor bolt materials shall be specified (grade, corrosion protection). (**TBD**)
- Grout material for base plate installation shall be specified (non-shrink grout, compressive strength). (**TBD**)

**Workmanship Requirements:**
- Manufacturing quality standards shall be specified (e.g., AWS D1.1 for welding). (**TBD**)
- Welding requirements shall be specified (procedures, qualifications, inspection). (**TBD**)
- Surface finishing requirements shall be specified (grinding, coating preparation). (**TBD**)
- Dimensional tolerances shall be specified. (**TBD**)

**Testing Requirements:**
- Proof load testing shall be specified if required by Employer's Requirements or port authority codes:
  - Test load (typically 1.5 × SWL) (**TBD**)
  - Test procedure (loading method, hold time, acceptance criteria)
  - Test reporting requirements
  - **TBD:** Proof load testing requirements to be confirmed from ER/codes.
- Non-destructive testing (NDT) shall be specified if required (visual inspection, magnetic particle testing for welds, ultrasonic testing). (**TBD**)
- Material testing shall be specified (mill test reports, mechanical property verification). (**TBD**)

**Installation Requirements:**
- Foundation and grouting details shall be specified (coordinate with DEL-09.01 drawings and PKG-08 structural design):
  - Base plate embedment or anchor bolt installation
  - Grout placement and curing requirements
  - Alignment and leveling tolerances
- Inspection requirements during installation shall be specified (witness points, hold points per § 1.6).

**Rationale:** See `Guidance.md § Principles (Bollards)`.
**Verification:** See `Procedure.md § Step 3` (draft bollard requirements). Performance substantiated by DEL-09.03 calculations and DEL-09.04 datasheets.

#### 2.3 Marine Hardware (Ladders, Life-Saving Equipment, Miscellaneous)

**Ladder Requirements:**
- Ladder type shall be specified based on application:
  - Fixed vertical ladder with safety cage (for heights exceeding threshold, typically 2.4 m / 8 ft)
  - Inclined ship's ladder (for frequent access, lower heights)
  - **TBD:** Ladder types and locations per operational requirements and DEL-09.01 drawings
- Materials shall be specified:
  - Stainless steel (e.g., 316 stainless for marine environment) or hot-dip galvanized steel (**TBD**)
  - Corrosion protection requirements (per § 1.4)
- Safety features shall comply with applicable occupational safety codes:
  - Safety cages for vertical ladders exceeding threshold height (cage diameter, clearances per code) (**TBD** — per applicable code, e.g., CSA Z259, OSHA 1910.27)
  - Rest platforms for extended climbing distances (platform spacing per code, typically 9–12 m) (**TBD**)
  - Rung spacing, width, toe clearance per code requirements (**TBD**)
  - Fall protection provisions (if required) (**TBD**)
- Structural requirements shall be specified:
  - Live load capacity (per code requirements, typically 1.0 kN / 100 kg per rung)
  - Deflection limits
  - Attachment methods and capacities (coordinate with PKG-08)
- Fixing details shall be specified (coordinate with DEL-09.01 drawings).

**Life-Saving Equipment Requirements:**
- Equipment list shall be specified per Employer's Requirements, which may include:
  - Life rings (with or without self-igniting lights)
  - Rescue ladders
  - Throw lines / rescue ropes
  - Retrieval hooks
  - Emergency lighting (if applicable)
  - First aid stations (if applicable)
  - **TBD:** Specific equipment types, quantities, and locations per ER
- Performance requirements shall be specified per applicable regulations:
  - Transport Canada or provincial port authority requirements (**TBD**)
  - SOLAS (Safety of Life at Sea) or equivalent for marine safety equipment (if applicable) (**TBD**)
- Material and construction requirements shall be specified:
  - Life ring material (buoyancy, UV resistance, color)
  - Rope material (strength, UV resistance, floating/non-floating)
  - Mounting hardware (corrosion resistance, quick-release mechanisms)
- Installation requirements shall be specified:
  - Mounting locations (coverage, visibility, accessibility per regulations)
  - Mounting details (coordinate with DEL-09.01 drawings)
  - Signage and marking requirements

**Miscellaneous Hardware Requirements (Existing Berth 10 Upgrades/Repairs):**
- Scope of upgrades/repairs shall be specified based on condition assessment findings. (**TBD** — pending condition survey and ER requirements)
- Materials and workmanship requirements for repair items shall be specified (coordinate with existing conditions and PKG-08 structural requirements).
- Interface requirements between existing and new elements shall be specified.

**Rationale:** See `Guidance.md § Principles (Marine Hardware)`.
**Verification:** See `Procedure.md § Step 3` (draft marine hardware requirements). Compliance substantiated by DEL-09.04 datasheets and DEL-09.05 installation records.

### 3) Interface / Coordination Requirements

**Interface coordination is critical for this specification.** Requirements affecting other packages/disciplines shall be clearly stated and coordinated.

#### 3.1 PKG-08 Marine Structures Interfaces

- Fender reaction forces and load transfer requirements shall be specified and coordinated with PKG-08 structural capacity (DEL-08.03 calculations).
- Bollard loads and foundation requirements shall be specified and coordinated with PKG-08 structural design.
- Ladder attachment loads and structural support requirements shall be specified and coordinated with PKG-08.
- Corrosion protection requirements shall be coordinated with PKG-08 materials specifications for consistency at interfaces.
- **TBD:** Specific interface requirements to be defined during design development and confirmed via interdisciplinary check (IDC) per `Procedure.md § Step 6`.

#### 3.2 Other Interfaces

- **PKG-11 Marine Loading System:** Operational clearances and safety zones around loading arms; access requirements.
- **PKG-10 Railcar Unloading System:** Access clearances and safety zones (if applicable).
- **PKG-26 Protective Coatings (if applicable):** Coating system coordination for consistency across marine environment.
- **Coordination mechanism:** Dependencies are managed externally (NOT_TRACKED). See `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`. Interface coordination to be confirmed via IDC per `Procedure.md § Step 6`.

**Verification:** See `Procedure.md § Step 6 (IDC)` for interface verification process.

### 4) Quality / Traceability Requirements

**Traceability is essential for specification requirements:**
- Each non-trivial requirement shall be traceable to:
  - **Employer's Requirements clause (preferred):** Cite specific ER volume, section, clause
  - **Cited standard or code:** Cite specific standard/code designation and clause (e.g., "per BS 6349-4:2014 § 5.3")
  - **Design calculation:** Reference DEL-09.03 calculation section/page
  - **Documented project decision:** Reference meeting minutes, design basis document, or technical memo
- Where information is missing, mark **TBD** and record the needed source/input with action owner.
- Where a requirement is inferred or assumed (not explicitly stated in sources), label it **ASSUMPTION** and cite the basis for the assumption.

**Verification:** See `Procedure.md § Step 5` (self-check for traceability).

## Standards

**Applicable standards and codes (to be confirmed from Employer's Requirements and regulatory approvals):**

- Employer's Requirements (Vol 2 Part 1–3) — applicable clauses **TBD** (see `_REFERENCES.md`).
- **ASSUMPTION:** Marine industry standards and port authority requirements, which may include:
  - **PIANC (World Association for Waterborne Transport Infrastructure):** Guidelines for marine fender systems (e.g., PIANC WG33 "Guidelines for the Design of Fenders Systems: 2002" or later)
  - **BS 6349 (British Standard for Maritime Works):** Port design codes for bollards and mooring equipment (e.g., BS 6349-4:2014 "Code of practice for design of fendering and mooring systems")
  - **ASTM (American Society for Testing and Materials):** Material standards (e.g., ASTM A36, A572 for steel; ASTM D1149 for rubber ozone resistance)
  - **AWS (American Welding Society):** Welding standards (e.g., AWS D1.1 "Structural Welding Code—Steel")
  - **OSHA / CSA (Occupational Safety and Health Administration / Canadian Standards Association):** Occupational safety codes for ladders and access (e.g., OSHA 1910.27, CSA Z259 series for fall protection)
  - **Transport Canada or provincial port authority:** Requirements for life-saving equipment and marine safety
  - **NFPA (National Fire Protection Association):** Marine safety equipment standards (if applicable)

**Code compliance verification:** Per `Procedure.md § Step 7` (independent check for code compliance).

## Verification

**Verification methods for Specification deliverables (per `Procedure.md`):**

| Method | Applicability | Criteria | Procedure § |
|--------|---------------|----------|-------------|
| Self-check | All sections | Completeness, consistency, traceability | Proc § Step 5 |
| Interdisciplinary check (IDC) | Interface requirements | Coordination with PKG-08, PKG-11, PKG-26; no conflicts | Proc § Step 6 |
| Independent check | All sections | Technical accuracy, ER compliance, verifiability of requirements, code compliance | Proc § Step 7 |
| Document control compliance | All | Per project document control procedures | Proc § Step 8 |

**Acceptance criteria (per `Datasheet.md § Acceptance`):**
- Specification covers all decomposition-listed artifacts for DEL-09.02 (fender specification, bollard specification, marine hardware specification).
- All Content Checklist items in `Datasheet.md` are addressed (either resolved or TBD with action owners).
- Requirements are written in verifiable terms with clear performance criteria, acceptance criteria, and test methods.
- All requirements are traceable to sources (ER, codes/standards, calculations, project decisions) or marked TBD/ASSUMPTION with justification.
- Cross-document consistency verified with `Guidance.md` (design intent) and `Procedure.md` (verification steps).
- Interface requirements coordinated with PKG-08 and other packages via IDC with sign-off.

## Documentation

**Required documentation outputs (per decomposition and `Datasheet.md`):**
- Fender specification
- Bollard specification
- Marine hardware specification
- (May be combined into a single technical specification document or separate documents, depending on project document control preferences)

**Documentation requirements:**
- All documents shall comply with project document control procedures.
- Revision control per project numbering system — **TBD**.
- Format: **TBD** — **ASSUMPTION:** Per project document management requirements (PDF for review/approval; editable format for internal development).
- Records management per `Procedure.md § Records`.
