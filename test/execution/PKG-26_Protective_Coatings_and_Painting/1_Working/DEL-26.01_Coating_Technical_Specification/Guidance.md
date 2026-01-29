# Guidance: DEL-26.01 Coating Technical Specification

## Purpose

This guidance document supports the development and implementation of the **Coating Technical Specification** for **PKG-26 Protective Coatings & Painting**.

**Deliverable purpose:** Define performance, materials, and workmanship requirements for protective coatings applied to structures and equipment at the Canola Oil Transload Facility, ensuring corrosion protection, product compatibility, and lifecycle cost optimization.

**Source:** Decomposition DEL-26.01 description

**Deliverable classification:**
- **Type:** Specification
- **Discipline:** Coatings
- **Responsible:** D&B Contractor
- **Source:** `_CONTEXT.md`

**Project objectives supported:**
- **OBJ-3:** Storage Capacity (45,000 MT) — Tank internal coatings must maintain food-grade integrity without compromising storage volume
- **OBJ-9:** Lifecycle Cost Optimization — Coating selection must balance initial material/application costs with long-term durability, maintenance frequency, and service life
- **Source:** Decomposition Section 6 (Objective-to-Deliverable Mapping)

**Cross-document linkages:**
- **Datasheet.md:** Coating attributes and construction details — See §Attributes, §Construction
- **Specification.md:** Requirements derived from this guidance — See §FR-1 through §QR-3
- **Procedure.md:** Production steps implementing this guidance — See §Steps

## Principles

### Engineering Rationale

**Corrosion Protection Philosophy:**

Protective coatings serve as the primary barrier against atmospheric and immersion corrosion for steel structures and equipment. The coating specification must be performance-based, defining required outcomes (corrosion protection level, service life, product compatibility) rather than prescribing specific products, to allow for competitive procurement while ensuring fitness for purpose.

**Source:** **ASSUMPTION** — Standard coatings engineering practice

**Multi-Environment Design:**

The facility presents multiple corrosive environments requiring different coating approaches:

1. **Tank Internals (Product Contact):**
   - Primary concern: Food-grade compliance and product compatibility
   - Secondary concern: Resistance to canola oil and cleaning agents
   - Tertiary concern: Durability under thermal cycling (if applicable)
   - **Typical solution:** Epoxy phenolic or FDA-compliant epoxy linings
   - **Source:** **ASSUMPTION** — Industry practice for food-grade storage — **location TBD**
   - **Specification linkage:** FR-1 (Product Compatibility), PR-1 (Food Contact Compliance)
   - **Datasheet linkage:** §Tank Coatings (Internal)

2. **Atmospheric Exposure (Marine/Industrial):**
   - Primary concern: Atmospheric corrosion in coastal marine environment
   - Fraser River terminal location implies marine salt exposure + industrial pollutants
   - ISO 12944 corrosivity category likely C4 (High) or C5 (Very High)
   - **Typical solution:** Multi-coat systems (zinc-rich primer + epoxy intermediate + polyurethane topcoat)
   - **Source:** ISO 12944-2 (classification of environments); **ASSUMPTION** on site corrosivity
   - **Specification linkage:** FR-2 (Corrosion Protection), PR-2 (Corrosion Performance)
   - **Datasheet linkage:** §Conditions (Environmental), §Tank Coatings (External), §Structural Steel Coatings

3. **Marine Immersion/Splash:**
   - Primary concern: Accelerated corrosion in immersion and splash zones
   - Requires high-build, abrasion-resistant systems
   - **Typical solution:** Specialized marine coatings per NACE/SSPC standards
   - **Source:** **ASSUMPTION** — Marine coating practice
   - **Specification linkage:** FR-2 (Corrosion Protection), IR-3 (Marine Interface)
   - **Datasheet linkage:** §Marine Coatings

### Applicable Standards Context

**ISO 12944 Framework:**

ISO 12944 provides a systematic framework for corrosion protection:
- **Part 2:** Classifies atmospheric corrosivity (C1 through CX)
- **Part 3:** Guides design considerations (drainage, accessibility, etc.)
- **Part 4:** Defines surface preparation requirements per environment
- **Part 5:** Specifies protective paint system types and expected durability

The specification should reference ISO 12944 methodology for coating system selection based on corrosivity category and required durability.

**Source:** ISO 12944 series

**SSPC/NACE Standards:**

North American coating industry standards provide practical implementation guidance:
- **SSPC surface preparation standards (SP series):** Define surface cleanliness and profile requirements
- **SSPC application standards (PA series):** Define measurement and inspection methods
- **NACE standards:** Provide corrosion control best practices

**Source:** SSPC and NACE/AMPP standards organizations

**Food Contact Regulations:**

Tank internal coatings contacting canola oil (food product) must comply with:
- **FDA 21 CFR 175.300:** U.S. food contact coatings regulations
- **NSF/ANSI 61** or equivalent: Potable water/food contact standards
- Canadian Food Inspection Agency (CFIA) requirements — **TBD**

Manufacturer must provide compliance certificates for food-contact coatings.

**Source:** **ASSUMPTION** — Regulatory requirement for food-grade product storage — **location TBD**

## Considerations

### Design Development Factors

**1. Corrosivity Assessment**

A site-specific corrosivity assessment should be performed or referenced to confirm the atmospheric corrosivity category. This drives coating system selection per ISO 12944. In the absence of site-specific data, conservative assumptions (C4 or C5) are appropriate for coastal marine/industrial environments.

**ASSUMPTION:** Site corrosivity assessment to be performed or referenced during design development.

**2. Surface Preparation Feasibility**

Surface preparation requirements (blast cleaning standards) must be achievable in the project execution context:
- **Shop application:** Higher standards (SSPC-SP 10 or SP-5) are typically feasible
- **Field application:** Environmental controls may limit achievable standards
- **Confined spaces (tank internals):** Ventilation, access, and worker safety constraints apply

Surface preparation requirements should be realistic and verified with the coating procedures (DEL-26.02).

**3. Application Environment**

Coating application quality is highly sensitive to environmental conditions:
- Temperature and humidity windows per manufacturer's data sheets
- Dew point control (surface temperature > dew point + 3°C minimum)
- Seasonal application constraints in BC climate

The specification should define acceptable application conditions and reference the procedures (DEL-26.02) for environmental controls.

**4. Inspection and Quality Control**

Coating quality depends on rigorous inspection at each stage:
- Surface preparation verification before coating application
- DFT measurement during and after application
- Adhesion testing per specified frequency
- Holiday detection for immersion service coatings

The specification should define inspection requirements, frequency, and acceptance criteria, to be implemented per DEL-26.04 (Coating Installation & Test Records).

**5. Food-Grade Certification**

Tank internal coatings require:
- Material certification (FDA/NSF compliance certificates from manufacturer)
- Application certification (no contamination during application/cure)
- Cleaning and commissioning procedures to ensure food-grade cleanliness

Coordinate with commissioning procedures (PKG-30) for tank internal coating acceptance.

**6. Shop vs. Field Coating**

Responsibility for shop-applied vs. field-applied coatings must be clearly defined:
- **Shop coatings:** Applied by fabricator under controlled conditions (higher quality potential)
- **Field coatings:** Applied on-site (touch-up, welds, field joints, full field application)
- **Interface:** Field touch-up of shop-applied coatings requires compatible materials

Define shop/field split in coordination with fabrication and construction planning.

### Coordination Points

**PKG-05 (Concrete Structures):**
- Coatings for embedded steel or steel-to-concrete interfaces
- Tank foundation coating requirements

**PKG-06 (Structural Steelwork):**
- Structural steel shop coating vs. field coating responsibilities
- Connection detail coating accessibility
- Galvanizing compatibility (if applicable)

**PKG-08 (Marine Structures), PKG-09 (Marine Outfitting), PKG-11 (Marine Loading System):**
- Marine coating requirements (immersion, splash, atmospheric zones)
- Fender system coatings
- Loading arm coatings

**PKG-13 (Storage Tanks):**
- Tank internal lining specification
- Tank external coating specification
- Coordination with tank design and fabrication

**DEL-26.02 (Coating Procedures):**
- Implementation procedures for this specification
- Surface preparation methods
- Application methods and controls
- Inspection methods

**DEL-26.03 (Coating Data Sheet Package):**
- Material data sheets supporting coating system selection
- Manufacturer's product data

**DEL-26.04 (Coating Installation & Test Records):**
- Inspection and test records demonstrating compliance with this specification

**Source:** Package and deliverable relationships per Decomposition Section 5

### Regulatory Context

- **Environmental compliance:** VOC (volatile organic compound) limits per provincial/federal air quality regulations
- **Worker health & safety:** Ventilation requirements, PPE, confined space entry per WorkSafeBC and project HSE plan (PKG-33)
- **Food safety:** CFIA requirements for food-contact coatings (if applicable) — **TBD**

**ASSUMPTION:** Regulatory requirements to be confirmed during permitting and design development (PKG-32).

## Trade-offs

### 1. Performance vs. Cost

**Trade-off:** High-performance coating systems (e.g., multi-coat epoxy/polyurethane with extended durability) have higher material and application costs but longer service life and reduced maintenance.

**Considerations:**
- Initial capital cost vs. lifecycle maintenance cost
- Facility design life and expected operational duration
- Accessibility for future maintenance (coating renewal)
- Owner's maintenance philosophy and capabilities

**Guidance:** Perform lifecycle cost analysis for critical/difficult-to-maintain areas. OBJ-9 (Lifecycle Cost Optimization) emphasizes total cost of ownership, not just initial cost.

**Source:** Decomposition Section 6 (OBJ-9)

### 2. Shop Coatings vs. Field Coatings

**Trade-off:** Shop-applied coatings offer better quality control and environmental control but require handling/shipping protection and field touch-up. Field-applied coatings avoid damage during fabrication/shipping but have lower quality potential and weather dependency.

**Considerations:**
- Component size and transportability
- Field application environment and season
- Quality requirements (e.g., tank internals may require shop application for food-grade compliance)
- Construction schedule constraints

**Guidance:** Specify shop application for critical food-contact coatings (tank internals) and high-performance systems. Define field touch-up requirements and compatible materials.

### 3. Generic Specification vs. Proprietary Products

**Trade-off:** Generic performance-based specifications maximize competition but require rigorous product qualification and equivalency evaluation. Proprietary specifications simplify procurement but may increase cost and reduce competition.

**Considerations:**
- D&B contract delivery model (design-build implies some flexibility)
- Product availability and local supply chains
- Proven performance in similar applications
- Employer preferences (if any)

**Guidance:** Use performance-based specifications with reference to proven products as examples. Allow equivalent products subject to approval and demonstration of compliance with performance requirements.

**ASSUMPTION:** Performance-based approach preferred for D&B contracts unless ER specifies otherwise.

### 4. Durability Classification vs. Maintenance Strategy

**Trade-off:** Higher durability classifications (ISO 12944) require more robust (and expensive) coating systems but extend maintenance intervals. Lower durability classifications require more frequent maintenance.

**Considerations:**
- Facility access for maintenance (e.g., tank internals require outages)
- Maintenance cost and labor availability
- Operational continuity requirements
- Asset criticality

**Guidance:** For difficult-to-access areas (tank internals, confined spaces), specify higher durability. For accessible areas, balance durability with maintenance strategy.

### 5. Environmental Compliance vs. Performance

**Trade-off:** Low-VOC and water-based coatings have lower environmental impact but may have performance limitations compared to traditional solvent-based systems.

**Considerations:**
- Regulatory VOC limits
- Performance requirements (especially for immersion service)
- Application conditions (temperature, humidity constraints)

**Guidance:** Prioritize low-VOC systems where performance is adequate. For critical applications (tank internals, immersion), prioritize performance and manage VOC compliance through application controls.

## Examples

### Reference Precedents

**Similar Facilities:**

Canola oil and edible oil storage facilities with comparable requirements:
- **TBD** — Reference similar terminal or storage facilities with food-grade tank coatings
- **TBD** — Precedent specifications from owner's existing facilities (if any)

**Industry Standards:**

Tank internal lining examples per API/industry practice:
- **TBD** — **location TBD** — API coating standards or guidance documents

**Coating System Examples (Illustrative Only — Not Prescriptive):**

**Tank Internals (Food Contact):**
- Example: Epoxy phenolic lining system (e.g., Carboline Plasite 7122 or equivalent)
- Surface prep: SSPC-SP 10 (near-white blast cleaning)
- DFT: 10-16 mils (typical range)
- Note: Actual selection based on manufacturer data and ER requirements

**Tank Externals (Atmospheric):**
- Example: Three-coat epoxy system
  - Primer: Zinc-rich epoxy (3-5 mils DFT)
  - Intermediate: Epoxy (4-6 mils DFT)
  - Topcoat: Polyurethane (2-3 mils DFT)
- Surface prep: SSPC-SP 6 or SP 10 (commercial or near-white blast)
- Total DFT: 9-14 mils
- Expected durability: High (H) to Very High (VH) per ISO 12944

**Structural Steel (Atmospheric):**
- Example: Similar to tank externals, or galvanizing with compatible topcoat
- Surface prep: SSPC-SP 6 or SP 10
- Note: Coordinate with fabrication and structural design (PKG-06)

**Marine Structures (Splash/Immersion):**
- Example: High-build epoxy or coal tar epoxy system
- Surface prep: SSPC-SP 10 (near-white blast)
- DFT: **TBD** — per NACE/SSPC marine coating guidance
- Note: Coordinate with marine design (PKG-08, PKG-09, PKG-11)

**Source:** **ASSUMPTION** — Industry typical systems, not project-specific selections — **location TBD** for manufacturer data sheets

### Anticipated Artifacts (Final Specification Documents)

Per Decomposition DEL-26.01, this deliverable shall produce:

1. **Tank Internal/External Coating Specification**
   - Scope and applicability
   - Material requirements (food-grade compliance for internals)
   - Surface preparation requirements
   - Application requirements
   - Inspection and testing requirements
   - Acceptance criteria

2. **Structural Steel Coating Specification**
   - Scope and applicability (all structural steel per PKG-06)
   - Material requirements
   - Surface preparation requirements
   - Shop vs. field coating delineation
   - Application requirements
   - Inspection and testing requirements
   - Acceptance criteria

**Source:** Decomposition DEL-26.01 anticipated artifacts

These specifications shall be formatted per project document standards and reviewed/approved per project quality procedures (Procedure.md §Step 6).

---

## Conflict Table (for human ruling)

**Status:** No unresolved conflicts identified during Pass 3 enrichment.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | No conflicts detected | — | — | — | — | — |

**Note:** If conflicts are identified during future design development or review cycles, record them in this table for human resolution before proceeding. Conflicts may arise from:
- Inconsistencies between ER requirements and industry standards
- Interface coordination gaps between PKG-26 and other packages
- Competing performance vs. cost requirements per OBJ-9

---

## Cross-Document Verification Summary

| Guidance Section | Specification § | Datasheet § | Procedure § |
|------------------|-----------------|-------------|-------------|
| Purpose (Objectives) | Scope (Objectives) | Attributes, Project Objectives | — |
| Principles (Tank Internals) | FR-1, PR-1 | Tank Coatings (Internal) | Step 2.2 |
| Principles (Atmospheric) | FR-2, PR-2 | Conditions, Tank External, Structural | Step 1.2 |
| Principles (Marine) | FR-2, IR-3 | Marine Coatings | Step 2.4 |
| Principles (ISO 12944) | Standards | References | Step 1.3 |
| Principles (Food Contact) | PR-1, Standards | Tank Internal | Step 1.5 |
| Considerations (Corrosivity) | FR-2, PR-2 | Conditions | Step 1.2 |
| Considerations (Surface Prep) | PR-5 | Construction | Step 2 |
| Considerations (Application) | PR-6 | Field Painting | Step 2 |
| Considerations (Inspection) | QR-1 | — | Step 2 |
| Considerations (Food-Grade) | PR-1 | Tank Internal | Step 1.5 |
| Considerations (Shop vs. Field) | IR-2 | Structural Steel | Step 2.3 |
| Trade-offs (All) | FR-3, IR-2 | Design Requirements | Steps 2–4 |
| Examples (All) | PR-4 | Construction | Step 2 |

**Verification status:** Pass 3 complete — Cross-document section references verified and consistent.
