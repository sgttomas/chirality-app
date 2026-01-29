# Guidance: DEL-09.02 Marine Outfitting Technical Specification

## Purpose

This guidance document supports the development of **Marine Outfitting Technical Specification** for **PKG-09 Marine Outfitting**.

**Decomposition definition (authoritative):** Defines performance, materials, and workmanship requirements for marine outfitting per Employer's Requirements. (**Source:** Decomposition, DEL-09.02 row)

This deliverable is classified as a **Specification** under the **Marine** discipline, to be produced by **D&B Contractor**.

**Downstream use:** This specification is the **controlling document** for all PKG-09 marine outfitting scope. It establishes requirements that:
- Govern procurement and vendor selection
- Define fabrication quality and workmanship expectations
- Establish installation acceptance criteria
- Are implemented via DEL-09.01 drawings
- Are substantiated via DEL-09.03 calculations and DEL-09.04 datasheets
- Are verified via DEL-09.05 installation and test records

## Principles

### Specification Intent

**Purpose and Function:**
- The marine outfitting technical specification is the **controlling document** for materials, workmanship, and testing expectations for all PKG-09 scope items: fenders, bollards, ladders, life-saving equipment, and existing Berth 10 upgrades/repairs.
- Requirements should be written so they can be **verified** via submittals, inspection, and tests.
- The specification governs three critical phases:
  - **Procurement:** Vendor selection basis; performance criteria for equipment selection
  - **Fabrication:** Quality expectations; material requirements; workmanship standards
  - **Installation:** Acceptance criteria; testing requirements; inspection hold/witness points

**Writing Requirements for Verifiability:**
- Each requirement should have clear acceptance criteria (what is acceptable/not acceptable).
- Performance requirements should be stated with measurable criteria (energy absorption in kJ, load capacity in kN, deflection in mm or %, etc.).
- Material requirements should cite specific standards/grades (e.g., "Steel shall be ASTM A572 Grade 50" not "Steel shall be high-strength grade").
- Test requirements should specify test method, acceptance criteria, and reporting requirements.
- Avoid vague language like "suitable," "appropriate," "adequate" without defining criteria.

**Cross-reference:** Requirements structure is defined in `Specification.md § 1–2`.

### Evidence Rules

**Source Fidelity:**
- If the Employer's Requirements do not specify a value or standard, do not invent one — mark **TBD** and identify the needed source (authority requirement, industry standard, or project decision).
- Cite sources for every non-trivial requirement: ER clause, code/standard designation and clause, calculation reference (DEL-09.03), or documented project decision.
- Requirements derived from engineering calculations should reference the calculation document (DEL-09.03) with specific section/page.

**Traceability:**
- Each requirement should be traceable to:
  - **Employer's Requirements (preferred):** Cite specific ER volume, section, clause
  - **Code/standard:** Cite designation and clause (e.g., "per BS 6349-4:2014 § 5.3")
  - **Design calculation:** Reference DEL-09.03 calculation section/page
  - **Project decision:** Reference meeting minutes, design basis document, or technical memo
- Where a requirement is inferred or assumed (not explicitly stated in sources), label it **ASSUMPTION** and cite the basis.

### Fenders (supports SPEC § 2.1)

**Design Philosophy:**
- Fenders are energy-absorbing systems that protect vessel hull and marine structure during berthing operations.
- Fender selection is a balance between:
  - **Energy absorption capacity:** Must exceed design berthing energy from DEL-08.06
  - **Reaction force:** Must be low enough for marine structure to support (coordinate with PKG-08)
  - **Deflection characteristics:** Must provide adequate clearance during compression
  - **Durability:** Must withstand marine environment and cyclic loading over design life
  - **Cost:** Balance performance with lifecycle cost

**Specification Requirements Derivation:**
- **Energy absorption capacity:** Derived from berthing energy calculations (DEL-08.06) — vessel characteristics, approach velocity, environmental conditions, berthing angle.
- **Reaction force limits:** Coordinated with PKG-08 structural capacity (DEL-08.03) — ensure structure can support fender loads with appropriate safety factors.
- **Deflection characteristics:** Substantiated via DEL-08.07 (fender system deflection data) and DEL-08.08 (supplier verification) — reaction force vs deflection curves, rated deflection percentage.
- **Material requirements:** Specify rubber compound grade (UV resistance, ozone resistance per ASTM D1149 or equivalent, temperature range), steel backing materials (grade, corrosion protection), fastener specifications.
- **Durability requirements:** Service life expectations (coordinate with ER design life requirements), cyclic loading resistance, environmental exposure (UV, ozone, temperature, saltwater).

**Key Considerations:**
- **Fender type selection:** Consider cylindrical fenders, cone fenders, cell fenders, arch fenders, foam-filled fenders based on:
  - Berthing energy and reaction force characteristics
  - Vessel hull geometry and contact area
  - Structural interface constraints (available attachment points, structural capacity)
  - Operational requirements (vessel maneuvering, multiple berth configurations)
  - **TBD:** Fender type pending berthing energy analysis and Employer's Requirements
- **Fender spacing and coverage:** Ensure fender spacing provides continuous protection along berthing face; avoid gaps that could allow hull/structure contact; consider vessel movement during cargo transfer.
- **Structural interface:** Fender reaction forces must be transferred to marine structure via properly designed mounting hardware and structural supports; coordinate with PKG-08 for structural capacity and connection details; specify attachment methods (welding, bolting), load transfer mechanisms, and interface corrosion protection.
- **Testing requirements:** Specify factory acceptance testing (FAT) to verify deflection characteristics; consider proof load testing if required by ER or project requirements; define test reporting requirements.

**ASSUMPTION:** Fender type and sizing will be coordinated with PKG-08 Marine Structures design and berthing energy analysis results prior to finalizing specification.

### Bollards (supports SPEC § 2.2)

**Design Philosophy:**
- Bollards provide mooring attachment points for vessel lines during cargo transfer operations.
- Bollard design is driven by:
  - **Mooring loads:** Line loads under design environmental conditions (wind, current, waves)
  - **Safety factors:** Code-required factors of safety (typically 2.0–2.5 for ultimate capacity)
  - **Operational requirements:** Mooring arrangement for design vessel; number of lines; line angles
  - **Durability:** Withstand marine environment and cyclic loading over design life

**Specification Requirements Derivation:**
- **Safe working load (SWL):** Derived from mooring analysis (DEL-08.09) — maximum mooring line loads for design vessel under all environmental conditions; expressed in kN or tonnes bollard pull.
- **Design load factors:** Per applicable codes (e.g., BS 6349, PIANC) — typically:
  - Ultimate load capacity = 2.0–2.5 × SWL (code-dependent)
  - Proof load (if testing required) = 1.5 × SWL (code/ER-dependent)
- **Material requirements:** Specify steel type and grade:
  - Cast steel (e.g., ASTM A27 Grade 65-35) for cast bollards — good for complex geometries, higher cost
  - Fabricated steel (e.g., ASTM A572 Grade 50) for fabricated bollards — more economical, suitable for simple geometries
  - Corrosion protection (coating system per `Specification.md § 1.4` or alternative protection)
- **Foundation requirements:** Specify base plate and anchor bolt requirements (coordinate with PKG-08 structural design); grout specifications (non-shrink grout, compressive strength).

**Key Considerations:**
- **Bollard type:** Consider:
  - Tee-head bollards (T-shaped head, traditional design)
  - Horn bollards (double horn, common for larger vessels)
  - Cruciform bollards (four-way, allows lines from multiple directions)
  - **TBD:** Bollard type pending mooring analysis and operational requirements
- **Bollard capacity:** Bollard SWL must accommodate maximum mooring line loads with appropriate safety factors; consider dynamic loading during vessel surge/sway; coordinate with mooring analysis (DEL-08.09).
- **Proof load testing:** Some codes/port authorities require proof load testing of bollards after installation to verify installed capacity:
  - Test load typically 1.5 × SWL
  - Requires test rig, hydraulic jacks, load cells, data recording
  - Adds time and cost to schedule
  - **TBD:** Proof load testing requirements per ER/code requirements; if required, specify test procedure, acceptance criteria, reporting requirements in specification
- **Foundation interface:** Bollard loads transferred to supporting structure via foundations/anchors; specify embedment details, anchor bolt sizes/grades, grouting requirements; coordinate with PKG-08 for structural capacity and foundation design.

**ASSUMPTION:** Bollard capacities will be defined by mooring analysis prior to finalizing specification.

### Marine Hardware (supports SPEC § 2.3)

**Scope Overview:**
- Marine hardware includes:
  - **Ladders:** Fixed vertical ladders with cages, inclined ship's ladders, access ladders for maintenance/emergency egress
  - **Life-saving equipment:** Life rings, rescue ladders, throw lines, retrieval hooks, emergency lighting, first aid stations
  - **Miscellaneous items:** Toe rails, edge protection, signage, equipment for existing Berth 10 upgrades/repairs

**Ladder Requirements Derivation:**
- **Type selection:** Based on application:
  - Fixed vertical ladder with safety cage: for access to elevated areas (berth deck, platform levels); required for heights exceeding code threshold (typically 2.4 m / 8 ft)
  - Inclined ship's ladder: for frequent access, lower heights; more ergonomic but requires more space
  - **TBD:** Ladder types and locations per operational requirements and DEL-09.01 drawings
- **Materials:** Stainless steel (316 grade for marine environment) or hot-dip galvanized steel; specify corrosion protection per `Specification.md § 1.4`.
- **Safety features:** Compliance with occupational safety codes (OSHA 1910.27, CSA Z259 series, or equivalent):
  - **Safety cages:** Required for vertical ladders exceeding threshold height (typically 2.4 m / 8 ft); specify cage diameter, clearances, landing platforms
  - **Rest platforms:** Required for extended climbing distances (typically every 9–12 m per codes); provide rest opportunities and emergency egress points
  - **Rung spacing, width, toe clearance:** Per code requirements (typically 300 mm rung spacing, 400 mm width minimum, 180 mm toe clearance)
  - **Fall protection:** Integration with fall arrest systems if required by codes or operational safety requirements
- **Structural requirements:** Specify live load capacity (per code, typically 1.0 kN / 100 kg per rung), deflection limits, attachment methods (coordinate with PKG-08 for attachment points and structural capacity).

**Life-Saving Equipment Requirements Derivation:**
- **Equipment list:** Per Employer's Requirements and applicable regulations:
  - Life rings (with or without self-igniting lights) — buoyancy per code
  - Rescue ladders — deployment method, strength requirements
  - Throw lines / rescue ropes — length, strength, floating/non-floating
  - Retrieval hooks — reach, strength
  - Emergency lighting (if applicable) — coverage, duration
  - First aid stations (if applicable) — contents per code
  - **TBD:** Specific equipment types, quantities, locations per ER
- **Regulatory compliance:** Equipment shall comply with:
  - Transport Canada or provincial port authority requirements (**TBD**)
  - SOLAS (Safety of Life at Sea) or equivalent for marine safety equipment (if applicable to port/terminal operations) (**TBD**)
  - Local marine safety regulations
- **Performance requirements:** Specify buoyancy (life rings), strength (ropes, ladders), visibility (color, lighting), durability (UV resistance, saltwater resistance).
- **Installation requirements:** Specify mounting locations (coverage per regulations, visibility, accessibility), mounting hardware (corrosion resistance, quick-release mechanisms), signage and marking.

**Existing Berth 10 Upgrades/Repairs:**
- Scope of upgrades/repairs based on condition assessment findings. (**TBD** — pending condition survey and ER requirements)
- Materials and workmanship for repair items shall match existing conditions where possible or coordinate with PKG-08 structural requirements.
- Interface requirements between existing and new elements (tie-in constraints, tolerances, corrosion protection).

## Considerations

### Factors to Consider During Development

| Factor | Consideration | Reference |
|--------|---------------|-----------|
| Scope boundaries | Confirm PKG-09 items vs. PKG-08 (structures) vs. PKG-11 (marine loading system); avoid scope gaps or overlaps | `Specification.md § 1.1` |
| Design inputs | Obtain berthing energy (DEL-08.06) and mooring analysis (DEL-08.09) results before finalizing performance requirements; missing inputs will result in TBD requirements | `Specification.md § 1.3, 2.1, 2.2` |
| Corrosion environment | Marine splash zone and immersion zone are severe corrosion environments; specify appropriate protection; coordinate with PKG-08 and PKG-26 for consistency | `Specification.md § 1.4` |
| Existing works | Berth 10 condition assessment findings required to define repair scope — **TBD** | `Specification.md § 2.3` |
| Testing requirements | Confirm proof load testing requirements from Employer's Requirements and authority requirements; testing adds cost and schedule impact | `Specification.md § 1.6, 2.2` |
| Code applicability | Identify which codes/standards apply (marine/port codes for fenders/bollards; safety codes for ladders; marine safety regulations for life-saving equipment) — may require interpretation and engineering judgment | `Specification.md § 1.2, Standards` |
| Verifiability | Write requirements in verifiable terms with measurable criteria; avoid vague language; specify test methods and acceptance criteria | `Specification.md § 2 (all subsections)` |

### Corrosion Protection (supports SPEC § 1.4)

**Environmental Exposure:**
- Marine outfitting operates in a severe corrosion environment:
  - **Immersed zone:** Continuous saltwater immersion (below low water level) — corrosion rate lower than splash zone but continuous exposure
  - **Splash zone:** Cyclic wetting between low water and high water plus splash — most severe corrosion environment due to oxygen availability and cyclic wetting
  - **Atmospheric zone:** Salt spray and UV exposure (above splash zone) — less severe than splash zone but still aggressive

**Specification Content:**
- **Exposure classification:** Define exposure classification for each equipment category (fenders, bollards, ladders) based on installation location relative to water levels.
- **Coating systems:** Specify coating type (epoxy, polyurethane, or other), number of coats (primer, intermediate, topcoat), total dry film thickness (DFT), surface preparation (SSPC-SP10 near-white blast or equivalent), application requirements (environmental conditions, curing).
- **Hot-dip galvanizing:** Specify for structural steel components where applicable (e.g., ladder cages, structural supports) — galvanizing standard (ASTM A123, ISO 1461), minimum coating thickness.
- **Stainless steel / corrosion-resistant alloys:** Specify for hardware/fasteners in marine environment (316 stainless steel or equivalent) — material grade, fastener specifications, passivation requirements.
- **Coordination:** Corrosion protection requirements shall be coordinated with:
  - PKG-08 Marine Structures for consistency at interfaces (same coating system, compatible cathodic protection if applicable)
  - PKG-26 Protective Coatings (if applicable) for system consistency across project

**Lifecycle Cost Considerations:**
- Higher initial investment in corrosion protection (e.g., duplex coating: galvanizing + organic coating) extends service life and reduces maintenance frequency.
- Balance initial cost vs. lifecycle cost (maintenance frequency, replacement intervals, operational disruptions for maintenance/replacement).
- Consider Employer's Requirements minimum and project financial criteria (e.g., 25-year design life, minimize maintenance).

### Interface Coordination (supports SPEC § 3)

**Critical Interfaces:**
- Marine outfitting interfaces primarily with:
  - **PKG-08 Marine Structures:** Load transfer (fender reaction forces, bollard loads, ladder live loads), fixing details (connection types, attachment points), structural capacity verification (PKG-08 to confirm structural adequacy for marine outfitting loads), corrosion protection coordination (consistent coating systems, compatible cathodic protection)
  - **PKG-11 Marine Loading System:** Operational clearances (safety zones around loading arms, line-of-sight for operators), access requirements (personnel access to loading arm platform, emergency egress)
  - **PKG-10 Railcar Unloading System (if applicable):** Access clearances, safety zones
  - **PKG-26 Protective Coatings (if applicable):** Coating system coordination for consistency across marine environment

**Specification Interface Requirements:**
- Interface loads and fixing requirements should be captured in both this specification (DEL-09.02) and interfacing package specifications to ensure consistency.
- Load assumptions (fender reaction forces, bollard capacities, ladder live loads) shall be coordinated with PKG-08 structural design and stated explicitly in specification.
- Interface corrosion protection (coating systems at connections, galvanic compatibility) shall be specified and coordinated with PKG-08/PKG-26.
- **TBD:** Interface register or coordination log to track interface requirements and coordination status.

**Coordination Mechanism:**
- Dependencies are managed externally (NOT_TRACKED). See `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`.
- Interface coordination confirmed via interdisciplinary check (IDC) per `Procedure.md § Step 6`.

## Trade-offs

### Competing Concerns to Evaluate

| Trade-off | Factors | Resolution Approach |
|-----------|---------|---------------------|
| Standard products vs. custom design | Standard products: availability, lead time, maintenance support, proven performance, lower cost; Custom design: optimized performance, tailored to specific conditions, higher cost, longer lead time | **Recommendation:** Prefer standard products where they meet requirements; specify custom design only where standard products do not meet performance criteria or interface constraints; balance performance optimization with procurement complexity and cost |
| Corrosion protection level vs. cost | Higher protection (e.g., duplex coating: galvanizing + organic coating, 316 stainless steel): extends service life, reduces maintenance frequency, higher initial cost; Lower protection (e.g., single coating system, galvanized steel): lower initial cost, shorter service life, higher maintenance frequency | **Recommendation:** Evaluate lifecycle cost considering initial capital cost, maintenance frequency/cost, replacement intervals, operational disruptions; follow Employer's Requirements minimum as baseline; consider upgrade to higher protection if lifecycle cost analysis justifies |
| Proof load testing vs. schedule/cost | Testing: provides assurance of installed capacity, identifies installation defects, adds time and cost (test rig, procedures, schedule impact); No testing: lower cost, faster schedule, relies on design calculations and quality control | **Recommendation:** Follow Employer's Requirements or code requirements; propose testing only where mandated or where risk justifies additional assurance; if testing not required by ER/codes, consider risk-based approach (e.g., test representative sample, test high-load bollards only) |
| Fender system type | Different fender types (cone, cell, foam-filled, arch, cylindrical): different energy absorption characteristics, reaction forces, costs, maintenance requirements, service life | **Recommendation:** Select based on berthing energy analysis (DEL-08.06), vessel compatibility, structural interface constraints (PKG-08 capacity), lifecycle cost; coordinate with PKG-08 to optimize fender/structure system |
| Ladder type (vertical vs. inclined) | Vertical ladder with cage: compact footprint, suitable for limited space, less ergonomic, requires cage for heights > 2.4 m; Inclined ship's ladder: more ergonomic, easier to climb, requires more space, higher cost | **Recommendation:** Select based on access frequency, available space, operational preferences; prioritize emergency egress requirements; consider ergonomics for frequent-access locations; coordinate with operational stakeholders if possible |

## Examples

### Reference Checklists

- Use `Datasheet.md` (Content Checklist) as the minimum content checklist for this deliverable.
- Use the decomposition's anticipated artifacts as the baseline:
  - Fender specification
  - Bollard specification
  - Marine hardware specification
- Expand as needed based on Employer's Requirements and project-specific requirements.

### Input Sources

| Input | Source Document | Purpose | Status |
|-------|-----------------|---------|--------|
| Berthing energy basis | DEL-08.06 Berthing Energy Calculation Report | Fender performance requirements (energy absorption, reaction force) | **TBD** |
| Mooring analysis | DEL-08.09 Mooring Analysis Report | Bollard capacity requirements (SWL, design loads) | **TBD** |
| Fender deflection data | DEL-08.07 Fender System Deflection Characteristics Data Package | Fender deflection characteristics for specification | **TBD** |
| Fender supplier verification | DEL-08.08 Fender Supplier Design Verification Letter/Report | Fender suitability confirmation | **TBD** |
| Marine structure capacity | DEL-08.03 Marine Structures Design Calculations | Structural capacity for fender/bollard loads | **TBD** |
| Employer's Requirements | Vol 2 Part 1–3 | All requirements (performance, materials, codes, quality, submittals) | **TBD** — clause extraction required |
| Applicable codes/standards | Regulatory Authority / Industry | Code requirements for fenders, bollards, ladders, life-saving equipment | **TBD** — code list to be confirmed |

### Typical Specification Sections

A typical marine outfitting specification may include the following sections (adapt as needed for project-specific requirements):

1. **Introduction and Scope:** Scope statement, inclusions/exclusions, related documents
2. **Reference Documents and Standards:** List of cited standards, codes, drawings, calculations
3. **Definitions and Abbreviations:** Technical terms used in specification
4. **Design Basis and Environmental Conditions:** Vessel characteristics, environmental loads, service life
5. **General Requirements:** Quality management, inspection, submittals, certifications
6. **Corrosion Protection Requirements:** Exposure classification, coating systems, galvanizing, stainless steel
7. **Installation Requirements:** Tolerances, interface requirements, environmental conditions for installation
8. **Fender Requirements:** Performance, materials, workmanship, testing, installation
9. **Bollard Requirements:** Performance, materials, workmanship, testing, installation
10. **Ladder and Access Equipment Requirements:** Types, materials, safety features, structural requirements, installation
11. **Life-Saving Equipment Requirements:** Equipment list, performance, materials, installation
12. **Miscellaneous Hardware Requirements:** Toe rails, signage, Berth 10 upgrades (as applicable)
13. **Inspection and Testing Requirements:** Hold/witness points, test procedures, acceptance criteria
14. **Documentation and Submittals:** Submittals list, review/approval process, as-built requirements

### Cross-Document Consistency

**Ensure consistency with other DEL-09.02 documents:**
- **Datasheet:** Content Checklist items match Specification requirements and Procedure steps.
- **Specification:** All requirements have corresponding rationale in this Guidance document and verification steps in Procedure.
- **Procedure:** All steps reference applicable Specification requirements and Guidance considerations.

**Ensure consistency with related PKG-09 deliverables:**
- **DEL-09.01:** Specification requirements are implementable via drawings
- **DEL-09.03:** Performance requirements are substantiable via calculations
- **DEL-09.04:** Equipment requirements are substantiable via vendor datasheets
- **DEL-09.05:** Installation and test requirements are verifiable via records

### Employer's Requirements

Employer's Requirements clauses and applicable authority requirements are **TBD** — to be extracted and cited during specification development (see `_REFERENCES.md`).

**Typical ER topics for marine outfitting (to be confirmed):**
- Fender system performance requirements (energy absorption, reaction force limits, deflection characteristics)
- Bollard capacity and spacing requirements (SWL, design factors, mooring arrangement)
- Ladder and access design standards (safety features, materials, codes)
- Life-saving equipment types and coverage (equipment list, regulatory compliance)
- Materials and corrosion protection requirements (coating systems, galvanizing, stainless steel)
- Quality assurance and testing requirements (inspection hold/witness points, certifications, proof load testing)
- Submittal requirements (datasheets, certificates, calculations, ITPs, as-builts)
- Design life and service life expectations
