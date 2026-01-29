# Specification: DEL-26.01 Coating Technical Specification

## Scope

This specification defines performance, materials, and workmanship requirements for protective coatings applied to structures and equipment within the Canola Oil Transload Facility at Fraser Surrey Terminal, Surrey, BC.

**Source:** Decomposition DEL-26.01 description

**Project context:**
- **Facility:** Canola oil transload (1,000,000 MT/a permitted throughput, 45,000 MT storage in 3 × 15,000 MT tanks)
- **Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- **Contract type:** Design & Build (D&B)
- **Source:** Decomposition Section 1; README.md

**Project objectives addressed:**
- **OBJ-3:** Storage Capacity (45,000 MT) — Tank internal coatings must maintain food-grade integrity without compromising storage capacity
- **OBJ-9:** Lifecycle Cost Optimization — Coating selection must balance initial cost with long-term durability and maintenance
- **Source:** Decomposition Section 6; Datasheet.md; Guidance.md (Purpose)

### Inclusions

This specification covers:

- **Tank internal coatings:** Food-grade lining systems for canola oil storage tanks (3 × 15,000 MT tanks per PKG-13)
- **Tank external coatings:** Atmospheric corrosion protection for storage tank exteriors
- **Structural steel coatings:** Protective coatings for structural steel framing, platforms, and supports (PKG-06)
- **Marine coatings:** Coatings for marine structures including berths, fenders, and loading equipment (PKG-08, PKG-09, PKG-11)
- **Field painting:** Touch-up and field application procedures

**Source:** Decomposition PKG-26 scope; Datasheet.md (Construction)

### Exclusions

- Shop-applied coatings by equipment manufacturers (governed by equipment specifications) unless coordination is required per this specification
- Coatings for vendor-supplied packaged equipment (unless specified otherwise)
- **TBD** — Other exclusions to be confirmed per ER and design development

## Requirements

### Functional Requirements

**FR-1: Product Compatibility (Tank Internal Coatings)**
- Tank internal coatings shall be compatible with canola oil (food-grade edible oil product)
- Coatings shall not impart taste, odor, or contamination to stored product
- Coatings shall resist canola oil and cleaning agents used for tank maintenance
- **Source:** Project description (canola oil transload facility); Datasheet.md §Tank Coatings (Internal); **ASSUMPTION** — food-grade requirement pending ER confirmation
- **Rationale:** See Guidance.md §Principles (Tank Internals)
- **Verification:** Procedure.md §Step 2.2; DEL-26.03 §Material Certificates; DEL-26.04 §Acceptance Testing Records
- **Traceability:** OBJ-3 (Storage Capacity) — Decomposition Section 6

**FR-2: Corrosion Protection**
- Coatings shall provide corrosion protection appropriate to the atmospheric corrosivity category of the installation environment
- Corrosivity category shall be determined per ISO 12944-2 based on site assessment or conservative assumption (C4 or C5 for coastal marine/industrial environment)
- **Source:** ISO 12944-2; Datasheet.md §Conditions (Environmental); **ASSUMPTION** — Marine/industrial environment classification pending site corrosivity assessment
- **Rationale:** See Guidance.md §Principles (Multi-Environment Design)
- **Verification:** Procedure.md §Step 1.2; DEL-27.01 §Site Corrosivity Assessment
- **Traceability:** OBJ-9 (Lifecycle Cost Optimization) — Decomposition Section 6

**FR-3: Service Life**
- Coating systems shall be designed to achieve the specified service life with defined maintenance intervals
- Service life requirement: **TBD** — to be confirmed per ER or design basis (DEL-27.01)
- Durability classification per ISO 12944-1: **TBD** — Low (L), Medium (M), High (H), or Very High (VH)
- **Source:** ISO 12944-1; Datasheet.md §Conditions (Design Requirements); Guidance.md §Trade-offs (Durability vs. Maintenance)
- **Rationale:** Service life and maintenance strategy trade-off per Guidance.md §Trade-offs
- **Verification:** Procedure.md §Step 1.2
- **Traceability:** OBJ-9 (Lifecycle Cost Optimization) — Decomposition Section 6

### Performance Requirements

**PR-1: Food Contact Compliance (Tank Internal Coatings)**
- Tank internal coatings shall comply with applicable food contact regulations:
  - **FDA 21 CFR 175.300** (Resinous and polymeric coatings) or equivalent — **location TBD**
  - **NSF/ANSI 61** (Drinking water system components – Health effects) or equivalent — **location TBD**
- Certificate of compliance shall be provided by coating manufacturer
- **Source:** **ASSUMPTION** based on food-grade product storage requirement; Datasheet.md §Tank Coatings (Internal)
- **Rationale:** Guidance.md §Principles (Food Contact Regulations)
- **Verification:** Procedure.md §Step 1.5; DEL-26.03 §Manufacturer Certificates
- **Traceability:** FR-1 (Product Compatibility)

**PR-2: Corrosion Protection Performance**
- Coating systems shall be selected to provide corrosion protection per ISO 12944-1 durability classification appropriate to the corrosivity category and required service life:
  - Immersion zones: **TBD** — Durability classification per marine exposure
  - Splash zones: **TBD** — Durability classification per marine exposure
  - Atmospheric zones: **TBD** — Likely High (H) or Very High (VH) durability for C4/C5 environment
- **Source:** ISO 12944-1 (durability classification); Datasheet.md §Conditions (Design Requirements)
- **Rationale:** Guidance.md §Principles (Multi-Environment Design)
- **Verification:** Procedure.md §Step 1.2; DEL-27.01 §Design Basis
- **Traceability:** FR-2 (Corrosion Protection); FR-3 (Service Life)

**PR-3: Adhesion**
- Coatings shall meet minimum adhesion requirements per ASTM D3359 (cross-hatch adhesion test) or equivalent
- Minimum rating: **TBD** — typically 4B or 5B per industry practice
- **Source:** ASTM D3359; **ASSUMPTION** — industry standard practice — **location TBD**
- **Rationale:** Adhesion is critical to coating performance and longevity per Guidance.md §Considerations
- **Verification:** Procedure.md §Step 2; DEL-26.04 §Adhesion Test Records
- **Traceability:** QR-1 (Inspection and Testing)

**PR-4: Dry Film Thickness (DFT)**
- Minimum DFT shall be specified per coating system and application:
  - **Tank internal coatings:** **TBD** — typical 10-16 mils per Guidance.md §Examples
  - **Tank external coatings:** **TBD** — typical 9-14 mils total per Guidance.md §Examples
  - **Structural steel coatings:** **TBD** — per coating system selected
  - **Marine coatings:** **TBD** — per NACE/SSPC marine coating guidance
- DFT shall be verified per SSPC-PA 2 (Measurement of Dry Coating Thickness with Magnetic Gages)
- **Source:** SSPC-PA 2; Datasheet.md §Construction (DFT values); Guidance.md §Examples
- **Rationale:** DFT directly affects corrosion protection and service life per Guidance.md §Principles
- **Verification:** Procedure.md §Step 2; DEL-26.04 §DFT Measurement Records
- **Traceability:** QR-1 (Inspection and Testing); FR-2 (Corrosion Protection)

**PR-5: Surface Preparation**
- Surface preparation shall meet minimum standards per SSPC specifications appropriate to the coating system and service environment:
  - **Tank internals:** **TBD** — likely SSPC-SP 10 (near-white blast cleaning) or SP-5 (white metal blast cleaning) for food-grade service
  - **Tank externals:** **TBD** — SSPC-SP 6 (commercial blast cleaning) or SP-10 per corrosivity category
  - **Structural steel:** **TBD** — per corrosivity category and coating system
  - **Marine structures:** **TBD** — likely SSPC-SP 10 for critical marine applications
- Surface cleanliness and profile shall be verified prior to coating application
- **Source:** SSPC surface preparation standards (SP series); Datasheet.md §Construction (Surface Preparation)
- **Rationale:** Guidance.md §Considerations (Surface Preparation Feasibility)
- **Verification:** Procedure.md §Step 2; DEL-26.02 §Surface Preparation Procedures; DEL-26.04 §Surface Preparation Records
- **Traceability:** QR-1 (Inspection and Testing); FR-2 (Corrosion Protection)

**PR-6: Application Conditions**
- Coating application shall be performed within environmental limits specified by manufacturer's product data sheet:
  - **Ambient temperature:** **TBD** — per manufacturer data
  - **Relative humidity:** **TBD** — typically ≤ 85% RH or per manufacturer
  - **Surface temperature:** Minimum 3°C above dew point — **ASSUMPTION** — **location TBD**
  - **Wind conditions:** **TBD** — per coating type (spray application limits)
- **Source:** **ASSUMPTION** — typical coating application requirements; Datasheet.md §Field Painting
- **Rationale:** Guidance.md §Considerations (Application Environment)
- **Verification:** Procedure.md §Step 2; DEL-26.02 §Application Procedures; DEL-26.04 §Application Records
- **Traceability:** QR-2 (Documentation)

### Interface Requirements

**IR-1: Tank Design Interface (PKG-13)**
- Tank internal coating specification shall be coordinated with tank design (PKG-13 Storage Tanks) to ensure compatibility with:
  - Tank geometry and internal access requirements for coating application
  - Nozzle, penetration, and manway details
  - Internal appurtenances (mixers, heating coils, baffles)
  - Surface preparation accessibility
- **Source:** Package cross-reference; Datasheet.md (Cross-references)
- **Rationale:** Tank design directly affects coating application feasibility and quality
- **Verification:** See Procedure.md (Step 1.4 — Coordinate with PKG-13); Step 3.2 (Interdisciplinary review)

**IR-2: Structural Steel Interface (PKG-06)**
- Structural steel coating specification shall be coordinated with structural design (PKG-06 Structural Steelwork) to ensure:
  - Shop vs. field coating responsibilities are clearly defined
  - Connection details accommodate coating thickness (bolt holes, fit-up)
  - Galvanizing compatibility addressed (if galvanizing is used)
  - Handling and transportation damage protection
- **Source:** Package cross-reference; Datasheet.md (Cross-references; Structural Steel Coatings — Shop vs. Field)
- **Rationale:** See Guidance.md (Considerations — Shop vs. Field Coating; Trade-offs — Shop Coatings vs. Field Coatings)
- **Verification:** See Procedure.md (Step 1.4 — Coordinate with PKG-06); Step 3.2 (Interdisciplinary review)

**IR-3: Marine Structure Interface (PKG-08, PKG-09, PKG-11)**
- Marine coating specification shall be coordinated with marine structure design (PKG-08 Marine Structures, PKG-09 Marine Outfitting, PKG-11 Marine Loading System) to address:
  - Immersion, splash, and atmospheric zone extents and requirements
  - Fender system coating compatibility and abrasion resistance
  - Loading arm coating requirements and mechanical/chemical resistance
  - Cathodic protection coordination (if applicable)
- **Source:** Package cross-reference; Datasheet.md (Cross-references; Marine Coatings — Exposure zones)
- **Rationale:** See Guidance.md (Engineering Rationale — Marine Immersion/Splash)
- **Verification:** See Procedure.md (Step 1.4 — Coordinate with PKG-08/09/11); Step 3.2 (Interdisciplinary review)

**IR-4: Procedure Coordination (DEL-26.02)**
- This specification shall be implemented per the coating procedures defined in DEL-26.02 (Coating Procedures)
- Surface preparation methods, application methods, and inspection methods shall be consistent between this specification and DEL-26.02
- **Source:** Deliverable cross-reference (internal to PKG-26); Datasheet.md (Cross-references)
- **Rationale:** Specification defines requirements; Procedures define implementation methods
- **Verification:** See Procedure.md (Step 6.2 — Notify downstream deliverable owners including DEL-26.02)

**IR-5: Commissioning Coordination (PKG-30)**
- Tank internal coating acceptance and food-grade cleanliness verification shall be coordinated with commissioning procedures (PKG-30)
- **Source:** Guidance.md (Considerations — Food-Grade Certification)
- **Rationale:** Food-grade coating acceptance requires validated cleaning and commissioning procedures
- **Verification:** See Procedure.md (Step 1.4 — Coordinate with related disciplines)

### Quality Requirements

**QR-1: Inspection and Testing**

Surface preparation inspection:
- Visual inspection per SSPC-VIS 1 (Visual Standard for Abrasive Blast Cleaned Steel) or equivalent
- Surface profile measurement per ASTM D4417 or SSPC-PA 17
- Inspection frequency: **TBD** — typically 100% visual, random profile measurements per DEL-26.02

DFT measurement:
- Measurement per SSPC-PA 2 (Measurement of Dry Coating Thickness with Magnetic Gages)
- Measurement frequency: **TBD** — per coating system and criticality (e.g., 100% for tank internals, spot measurements for structural steel)

Adhesion testing:
- Test method: ASTM D3359 (cross-hatch tape test) or equivalent
- Test frequency: **TBD** — per coating system and criticality

Holiday (pinhole) detection:
- Holiday detection required for immersion service coatings (tank internals, marine immersion zones)
- Test method: **TBD** — low-voltage wet sponge or high-voltage holiday detector per coating thickness
- Test frequency: **TBD** — typically 100% for immersion service

Visual inspection:
- Final visual inspection per SSPC-PA 2 or equivalent for surface defects (runs, sags, pinholes, contamination)

**Source:** SSPC and ASTM standards; Datasheet.md (Tank Coatings); **ASSUMPTION** — industry standard inspection practices
**Rationale:** See Guidance.md (Considerations — Inspection and Quality Control)
**Verification:** See Procedure.md (Step 2 — Specify inspection and testing requirements); DEL-26.02 (inspection procedures); DEL-26.04 (inspection and test records)

**QR-2: Documentation**

Required documentation (to be produced per this specification):
- Surface preparation records (environmental conditions, cleanliness verification) — DEL-26.04
- DFT measurement records (location, readings, acceptance/rejection) — DEL-26.04
- Adhesion test records — DEL-26.04
- Holiday detection records (for immersion service) — DEL-26.04
- Material certificates of compliance (manufacturer data sheets, FDA/NSF certificates for tank internals) — DEL-26.03
- Application records (environmental conditions during application, cure times, batch/lot numbers) — DEL-26.04

**Source:** Datasheet.md (Cross-references — DEL-26.03, DEL-26.04); **ASSUMPTION** — typical quality documentation
**Rationale:** Documentation provides traceability and evidence of compliance
**Verification:** See Procedure.md (Records section); DEL-26.04 (record templates and management)

**QR-3: Workmanship**

All coating work shall be performed by qualified coating applicators:
- Applicator qualifications: **TBD** — per project quality plan or industry certification (e.g., NACE/AMPP Coating Inspector Level 1/2, SSPC certification)
- Inspection qualifications: **TBD** — NACE/AMPP Coating Inspector Level 2 or equivalent recommended
- Training and competency verification: Per project quality procedures (PKG-33 HSE Management and project quality plan)

**Source:** **ASSUMPTION** — industry standard practice — **location TBD**
**Rationale:** Coating quality depends on qualified personnel
**Verification:** See Procedure.md (Prerequisites — Personnel requirements); project quality plan

## Standards

**Applicable codes and standards:**

### Primary Standards (Coatings)

**SSPC — The Society for Protective Coatings**
- **Surface preparation standards (SP series):**
  - SSPC-SP 5: White Metal Blast Cleaning
  - SSPC-SP 6: Commercial Blast Cleaning
  - SSPC-SP 10: Near-White Blast Cleaning
  - Others as applicable
- **Application standards (PA series):**
  - SSPC-PA 2: Measurement of Dry Coating Thickness with Magnetic Gages
  - SSPC-PA 17: Procedure for Determining Conformance to Dry Coating Thickness Requirements
  - Others as applicable
- **Visual standards:**
  - SSPC-VIS 1: Visual Standard for Abrasive Blast Cleaned Steel
- **Source:** Industry standard for protective coatings; Datasheet.md (References)

**NACE/AMPP — NACE International (now part of AMPP - Association for Materials Protection and Performance)**
- Corrosion control and coating standards
- Marine coating guidance
- Coating inspector certification programs
- **Source:** Industry standard for corrosion protection; Datasheet.md (References)

**ISO 12944 — Paints and varnishes — Corrosion protection of steel structures by protective paint systems**
- **Part 1:** General introduction (durability classification: Low, Medium, High, Very High)
- **Part 2:** Classification of environments (corrosivity categories C1 through CX, including marine environments)
- **Part 3:** Design considerations (drainage, accessibility, surface preparation compatibility)
- **Part 4:** Types of surface and surface preparation
- **Part 5:** Protective paint systems (generic types and expected performance)
- **Source:** International standard for protective coatings; Datasheet.md (References); Guidance.md (Applicable Standards Context — ISO 12944 Framework)

**CSA S6 Annex — Canadian Highway Bridge Design Code (coatings annex)**
- **ASSUMPTION:** May be applicable for structural steel coatings
- **location TBD** — verify applicability and obtain reference
- **Source:** Datasheet.md (References)

### Food Contact Standards

**FDA 21 CFR 175.300 — Resinous and polymeric coatings for food contact**
- Applicable for tank internal coatings contacting canola oil (food product)
- **location TBD** — obtain reference or confirm via ER
- **Source:** Datasheet.md (References); Guidance.md (Food Contact Regulations)

**NSF/ANSI 61 — Drinking water system components – Health effects**
- May be referenced as equivalent standard for food-grade coatings
- **location TBD** — verify applicability
- **Source:** Datasheet.md (References); Guidance.md (Food Contact Regulations)

### Testing Standards

**ASTM D3359 — Standard Test Methods for Rating Adhesion by Tape Test**
- Cross-hatch adhesion test for coating adhesion verification
- **Source:** PR-3 (Adhesion); QR-1 (Adhesion testing)

**ASTM D4417 — Standard Test Methods for Field Measurement of Surface Profile of Blast Cleaned Steel**
- Surface profile measurement for surface preparation verification
- **Source:** QR-1 (Surface preparation inspection)

**SSPC-VIS 1 — Visual Standard for Abrasive Blast Cleaned Steel**
- Visual reference for surface preparation acceptance
- **Source:** QR-1 (Surface preparation inspection)

**Additional ASTM standards:** **TBD** — per coating system type (e.g., ASTM D4541 pull-off adhesion, ASTM D5162 discontinuity/holiday detection)

### Environmental and Safety Standards

**VOC Regulations:**
- Provincial and federal air quality regulations for volatile organic compound (VOC) emissions
- **TBD** — Confirm applicable regulations and limits
- **Source:** Guidance.md (Regulatory Context); Datasheet.md (Environmental Conditions — VOC regulations)

**WorkSafeBC Regulations:**
- Worker health and safety requirements for coating application (ventilation, PPE, confined space entry)
- **Source:** Guidance.md (Regulatory Context); PKG-33 (HSE Management)

**CFIA (Canadian Food Inspection Agency) Requirements:**
- **TBD** — Confirm applicability for food-contact coatings
- **Source:** Guidance.md (Regulatory Context); **ASSUMPTION**

### Project-Specific Requirements

**Employer's Requirements (ER):**
- Project-specific coating requirements, performance criteria, and acceptance standards
- **TBD** — **location TBD** — to be reviewed and incorporated per Procedure.md (Step 1.1)

**Project Quality Management Plan:**
- Quality procedures and acceptance criteria for coating work
- **Source:** QR-1, QR-2, QR-3

**Project Document Control Procedures:**
- Document numbering, revision control, and distribution requirements
- **Source:** Procedure.md (Documentation section)

**Project Environmental Management Plan:**
- Environmental compliance for coating operations (VOC control, waste management)
- **Source:** Guidance.md (Regulatory Context)

## Verification

**Verification methods:**

### Document Review

**Technical review:**
- Coatings discipline lead review for technical accuracy and completeness
- Verify all coating types addressed (tank internal, tank external, structural steel, marine, field painting per Datasheet.md)
- Verify all requirements traceable to sources (ER, standards, design basis per Procedure.md Step 1)
- Verify coating system selections appropriate to environmental conditions

**Interdisciplinary review:**
- PKG-05 (Concrete Structures): Steel-to-concrete interface coatings
- PKG-06 (Structural Steelwork): Structural steel coating coordination, shop vs. field responsibilities
- PKG-08 (Marine Structures): Marine exposure zones, coating requirements
- PKG-09 (Marine Outfitting): Fender and equipment coatings
- PKG-11 (Marine Loading System): Loading arm coatings
- PKG-13 (Storage Tanks): Tank design coordination, internal coating accessibility
- **Source:** IR-1, IR-2, IR-3; Procedure.md (Step 3.2)

**QA/QC review:**
- Standards compliance verification (all cited standards correctly referenced per Standards section)
- Requirements traceability to ER — **TBD** pending ER review
- Document format compliance with project document control standards
- **Source:** Procedure.md (Step 3.3)

**Employer review:**
- Employer review and comment incorporation per D&B contract requirements
- **TBD** — Confirm Employer review and approval requirements
- **Source:** Procedure.md (Step 5)

### Compliance Verification

**Standards compliance matrix:**
- Verify all cited standards are properly referenced with current revision/date
- Verify no conflicts between standards (or conflicts identified and resolved)

**Requirements traceability:**
- All requirements traceable to ER, design basis, or standards
- No invented requirements without **ASSUMPTION** label and justification

**Interface verification:**
- All interface requirements (IR-1 through IR-5) coordinated and confirmed with related packages
- No unresolved interdisciplinary conflicts
- **Source:** Procedure.md (Step 4 — Comment resolution)

### Technical Validation

**Coating system selection validation:**
- Coating systems validated against:
  - **Environmental conditions:** Corrosivity category (C4/C5 or per site assessment)
  - **Service requirements:** Product compatibility (food-grade for tank internals), immersion/splash/atmospheric exposure
  - **Project objectives:**
    - **OBJ-3 (Storage Capacity):** Tank internal coatings do not compromise storage volume
    - **OBJ-9 (Lifecycle Cost Optimization):** Coating selection balances initial cost vs. lifecycle durability/maintenance
- **Source:** Decomposition Section 6 (Objectives); Datasheet.md (Project objectives); Guidance.md (Purpose, Trade-offs)

**Durability validation:**
- Durability classification (ISO 12944-1) appropriate to corrosivity and design life
- Maintenance strategy consistent with durability classification
- **Source:** FR-3 (Service Life); Guidance.md (Trade-offs — Durability vs. Maintenance Strategy)

**Food-grade validation:**
- Tank internal coating systems comply with FDA/NSF requirements
- Material certificates available from manufacturers
- **Source:** PR-1 (Food Contact Compliance); Guidance.md (Considerations — Food-Grade Certification)

### Acceptance Criteria

**The Coating Technical Specification deliverable is acceptable when:**

- ✓ All anticipated artifacts produced per Decomposition DEL-26.01:
  - Tank internal/external coating specification
  - Structural steel coating specification
- ✓ All requirements (FR, PR, IR, QR) defined and traceable to source documents (ER, standards, design basis)
- ✓ All applicable standards correctly referenced (SSPC, NACE, ISO 12944, FDA, NSF, ASTM)
- ✓ All interdisciplinary interfaces coordinated (PKG-05, PKG-06, PKG-08, PKG-09, PKG-11, PKG-13) and no unresolved conflicts
- ✓ All review comments addressed and closed (technical, interdisciplinary, QA/QC per Procedure.md Step 4)
- ✓ Employer review and approval obtained (if required per project) per Procedure.md Step 5
- ✓ Document format complies with project document control standards
- ✓ Document issued and distributed per project procedures (Procedure.md Step 6)
- ✓ Cross-document consistency verified (Datasheet, Specification, Guidance, Procedure align on terminology, entities, values)
- ✓ Project objectives (OBJ-3, OBJ-9) addressed by specification requirements
- ✓ **TBD** items documented and tracked for future resolution (or resolved prior to issue for construction)

**Source:** Procedure.md (Verification — Deliverable Acceptance Criteria)

## Documentation

**Required documentation outputs:**

This deliverable shall produce the following specification documents:

### 1. Tank Internal/External Coating Specification

**Content:**
- **Scope and applicability:** Storage tanks per PKG-13 (internal and external coatings)
- **Material requirements:**
  - Tank internals: Food-grade compliance (FDA/NSF), product compatibility
  - Tank externals: Atmospheric corrosion protection per corrosivity category
- **Surface preparation requirements:** SSPC standards per coating system
- **Application requirements:** Environmental limits, application methods, cure times
- **Inspection and testing requirements:** Surface prep inspection, DFT, adhesion, holiday detection (internals)
- **Acceptance criteria:** Per QR-1, QR-2, QR-3

**Source:** Decomposition DEL-26.01 anticipated artifacts; Datasheet.md (Tank Coatings Internal/External); Procedure.md (Step 2.2)

### 2. Structural Steel Coating Specification

**Content:**
- **Scope and applicability:** Structural steel per PKG-06 (all structural steel framing, platforms, supports)
- **Material requirements:** Atmospheric corrosion protection per corrosivity category
- **Surface preparation requirements:** SSPC standards per coating system
- **Shop vs. field coating delineation:** Responsibilities and interface requirements per IR-2
- **Application requirements:** Environmental limits, application methods (shop and field)
- **Inspection and testing requirements:** Surface prep inspection, DFT, adhesion
- **Acceptance criteria:** Per QR-1, QR-2, QR-3

**Source:** Decomposition DEL-26.01 anticipated artifacts; Datasheet.md (Structural Steel Coatings); Procedure.md (Step 2.3)

### Marine Coatings (Integration Note)

Marine coating requirements (PKG-08, PKG-09, PKG-11) may be:
- Integrated into the structural steel coating specification with marine environment sections, OR
- Issued as a separate marine coating specification section or document
- **TBD** — Determine integration approach per project document organization
- **Source:** Datasheet.md (Marine Coatings); Procedure.md (Step 2.4)

### Documentation Format

**Document numbering:** **TBD** — per project document control procedures
**Revision control:** Per project document management system
**Format standard:** **TBD** — project specification template (Procedure.md Step 2.1)
**Review and approval records:** Per project quality procedures

**Metadata requirements:**
- Deliverable ID: DEL-26.01
- Document number(s): **TBD**
- Revision history with dates and descriptions
- Originator, checker, approver signatures and dates
- Employer approval (if applicable)
- **Source:** Procedure.md (Metadata and Traceability)

### Document Relationships

**Implemented by:**
- **DEL-26.02** (Coating Procedures) — Surface preparation procedures, coating application procedures, inspection procedures

**Supported by:**
- **DEL-26.03** (Coating Data Sheet Package) — Manufacturer data sheets, FDA/NSF certificates, product compliance documentation

**Verified by:**
- **DEL-26.04** (Coating Installation & Test Records) — Surface preparation records, DFT records, adhesion test records, holiday detection records (demonstrating compliance with this specification)

**References (upstream):**
- **DEL-27.01** (Design Basis Documents) — Environmental conditions, corrosivity classification, design life
- **PKG-05, PKG-06, PKG-08, PKG-09, PKG-11, PKG-13** design deliverables — Interface coordination and design requirements
- **PKG-30** (Commissioning) — Tank internal coating acceptance procedures
- **PKG-32** (Regulatory & Permits) — Environmental permits and compliance requirements
- **PKG-33** (HSE Management) — Worker safety procedures for coating application

**Source:** Decomposition Section 5 (package and deliverable structure); Datasheet.md (Cross-references)

**Distribution:**
- Coating procedures author (DEL-26.02)
- Coating data sheet package author (DEL-26.03)
- QA/QC team (DEL-26.04 — inspection planning)
- Related discipline leads (PKG-05, PKG-06, PKG-08, PKG-09, PKG-11, PKG-13)
- Construction/fabrication teams (when issued for construction)
- Employer (per project requirements)
- **Source:** Procedure.md §Records (Access and Distribution)

---

## Cross-Document Verification Summary

| Specification Requirement | Datasheet § | Guidance § | Procedure § | DEL-26.0x |
|---------------------------|-------------|------------|-------------|-----------|
| FR-1 (Product Compatibility) | Tank Internal | Principles (Tank Internals) | Step 2.2 | DEL-26.03, DEL-26.04 |
| FR-2 (Corrosion Protection) | Conditions | Principles (Multi-Environment) | Step 1.2 | DEL-26.04 |
| FR-3 (Service Life) | Design Requirements | Trade-offs (Durability) | Step 1.2 | — |
| PR-1 (Food Contact) | Tank Internal | Principles (Food Contact) | Step 1.5 | DEL-26.03 |
| PR-2 (Corrosion Performance) | Design Requirements | Principles | Step 1.2 | DEL-26.04 |
| PR-3 (Adhesion) | — | Considerations | Step 2 | DEL-26.04 |
| PR-4 (DFT) | Construction | Examples | Step 2 | DEL-26.04 |
| PR-5 (Surface Preparation) | Construction | Considerations | Step 2 | DEL-26.02, DEL-26.04 |
| PR-6 (Application Conditions) | Field Painting | Considerations | Step 2 | DEL-26.02, DEL-26.04 |
| IR-1 (Tank Interface) | Cross-references | Coordination Points | Step 1.4, 3.2 | — |
| IR-2 (Structural Steel) | Cross-references | Coordination Points | Step 1.4, 3.2 | — |
| IR-3 (Marine Interface) | Cross-references | Coordination Points | Step 1.4, 3.2 | — |
| IR-4 (Procedure Coordination) | Cross-references | — | Step 6.2 | DEL-26.02 |
| IR-5 (Commissioning) | Cross-references | Considerations | Step 1.4 | — |
| QR-1 (Inspection/Testing) | — | Considerations | Step 2 | DEL-26.04 |
| QR-2 (Documentation) | Cross-references | — | Records | DEL-26.03, DEL-26.04 |
| QR-3 (Workmanship) | — | — | Prerequisites | — |

**Verification status:** Pass 3 complete — All requirements traceable to Datasheet, Guidance, Procedure, and downstream deliverables.
