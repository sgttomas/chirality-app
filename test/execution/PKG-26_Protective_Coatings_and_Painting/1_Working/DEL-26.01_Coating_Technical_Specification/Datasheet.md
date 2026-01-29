# Datasheet: DEL-26.01 Coating Technical Specification

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-26.01 |
| Name | Coating Technical Specification |
| Package | PKG-26 Protective Coatings & Painting |
| Discipline | Coatings |
| Type | Specification |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md`

## Attributes

| Attribute | Value | Source | Specification § | Procedure § |
|-----------|-------|--------|-----------------|-------------|
| Document Number | **TBD** | Project document control system | — | Step 6.1 |
| Specification Type | Technical (Performance, Materials, Workmanship) | Decomposition DEL-26.01 description | Scope | Step 2.1 |
| Specification Approach | Performance-based with reference products | Guidance.md §Trade-offs (Generic vs. Proprietary) | — | Step 2.5 |
| Revision | 0 (Initial Draft) | **ASSUMPTION** — Initial working draft | — | Step 6.3 |
| Applicable Standards | SSPC, NACE/AMPP, CSA S6 Annex, ISO 12944, FDA 21 CFR 175.300, NSF/ANSI 61 | Specification.md §Standards | Standards | Step 1.3 |
| Classification | D&B Contractor Specification | Decomposition DEL-26.01 | — | — |
| Coverage Scope | Tank coatings (internal/external), structural steel coatings, marine coatings, field painting | Decomposition PKG-26 scope | Scope (Inclusions) | Step 2.2–2.4 |

## Conditions

**Operating / Environmental Context:**

This specification governs protective coatings for a canola oil transload facility located at Fraser Surrey Terminal, Surrey, BC.

**Project Context:**
- **Project location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC — **Source:** Decomposition Section 1
- **Facility type:** Canola oil transload (1,000,000 MT/a permitted throughput, 45,000 MT storage) — **Source:** Decomposition Section 1
- **Storage configuration:** 3 × 15,000 MT storage tanks — **Source:** Decomposition Section 1; README.md project snapshot
- **Contract type:** Design & Build (D&B) — **Source:** README.md project snapshot

**Environmental Conditions:**
- **Operating temperature range:** **TBD** — Requires ER or design basis confirmation (DEL-27.01)
- **Environmental classification:** Coastal marine environment — **ASSUMPTION** based on Fraser River terminal location
- **Atmospheric corrosivity:** **TBD** — Marine/industrial environment, likely C4 (High) or C5 (Very High) per ISO 12944-2 — **ASSUMPTION** pending site corrosivity assessment
- **Seismic requirements:** **TBD** — BC seismic zone requirements per NBCC (National Building Code of Canada)
- **Hazardous area classification:** **TBD** — To be confirmed per facility hazardous area classification study
- **VOC regulations:** Subject to provincial/federal air quality regulations — **Source:** Guidance.md (Regulatory Context)

**Design Requirements:**
- **Design life:** **TBD** — Coating system design life to be specified in ER or design basis
- **Durability classification:** **TBD** — Per ISO 12944-1 (Low, Medium, High, Very High) — to be selected based on corrosivity and design life
- **Maintenance strategy:** **TBD** — Coordinate with owner's maintenance philosophy — **Source:** Guidance.md (Trade-offs — Durability vs. Maintenance)

## Construction

**Materials / Configuration:**

This deliverable defines materials and workmanship for protective coatings applied to:

### Tank Coatings (Internal)
- **Application:** Storage tank interiors (3 × 15,000 MT canola oil tanks) — **Source:** Decomposition Section 1, PKG-13
- **Product contact:** Canola oil (food-grade edible oil product) — **Source:** Project description
- **Functional requirement:** Product compatibility (FR-1) and food contact compliance (PR-1) — **Source:** Specification.md §FR-1, §PR-1
- **Food-grade compliance:** FDA 21 CFR 175.300, NSF/ANSI 61 (or equivalent) — **Source:** Specification.md §Standards (Food Contact Standards)
- **System type:** **TBD** — Likely epoxy phenolic or FDA-compliant epoxy lining — **ASSUMPTION** — **Source:** Guidance.md §Examples (Tank Internals)
- **DFT (Dry Film Thickness):** **TBD** — Typical range 10-16 mils per industry practice — **Source:** Specification.md §PR-4; Guidance.md §Examples
- **Surface preparation:** **TBD** — Likely SSPC-SP 10 (near-white blast) or SP-5 (white metal blast) — **Source:** Specification.md §PR-5
- **Performance requirement:** No taste/odor imparted to product; resistance to canola oil and cleaning agents — **Source:** Specification.md §FR-1
- **Project objective:** OBJ-3 (Storage Capacity 45,000 MT) — coating must not compromise storage volume — **Source:** Decomposition Section 6; Guidance.md §Purpose
- **Verification:** DEL-26.02 §Surface Preparation; DEL-26.04 §Holiday Detection Records — **Source:** Specification.md §QR-1; Procedure.md §Step 2.2

### Tank Coatings (External)
- **Application:** Storage tank exteriors and appurtenances
- **Exposure:** Atmospheric weathering, coastal marine/industrial environment
- **Functional requirement:** Corrosion protection (FR-2) per environmental classification — **Source:** Specification.md §FR-2
- **System type:** **TBD** — Multi-coat epoxy or epoxy/polyurethane system (zinc-rich primer + epoxy intermediate + polyurethane topcoat) — **Source:** Guidance.md §Examples (Tank Externals)
- **DFT (Dry Film Thickness):** **TBD** — Typical total 9-14 mils per industry practice — **Source:** Specification.md §PR-4; Guidance.md §Examples
- **Surface preparation:** **TBD** — SSPC-SP 6 (commercial blast) or SP-10 (near-white blast) per corrosivity category — **Source:** Specification.md §PR-5
- **Durability:** High (H) to Very High (VH) per ISO 12944-1 — **TBD** — **Source:** Specification.md §FR-3; Guidance.md §Examples
- **Project objective:** OBJ-9 (Lifecycle Cost Optimization) — balance initial cost vs. long-term durability — **Source:** Decomposition Section 6; Guidance.md §Purpose
- **Verification:** DEL-26.02 §Application Procedures; DEL-26.04 §DFT Measurement Records — **Source:** Specification.md §QR-1; Procedure.md §Step 2.2

### Structural Steel Coatings
- **Application:** Structural steel framing, platforms, supports (PKG-06)
- **Exposure:** Atmospheric weathering, marine/industrial environment
- **Functional requirement:** Corrosion protection (FR-2) and interface coordination (IR-2) — **Source:** Specification.md §FR-2, §IR-2
- **System type:** **TBD** — Similar to tank external (zinc-rich epoxy primer + epoxy intermediate + polyurethane topcoat) or galvanizing with compatible topcoat — **Source:** Guidance.md §Examples (Structural Steel)
- **DFT (Dry Film Thickness):** **TBD** — Per coating system selected — **Source:** Specification.md §PR-4
- **Surface preparation:** **TBD** — SSPC-SP 6 or SP-10 per corrosivity category — **Source:** Specification.md §PR-5
- **Shop vs. Field:** **TBD** — Responsibility split to be defined in coordination with PKG-06 — **Source:** Specification.md §IR-2; Guidance.md §Trade-offs (Shop vs. Field)
- **Corrosivity category:** **TBD** — Likely C4 or C5 per ISO 12944-2 — **ASSUMPTION** — **Source:** Guidance.md §Principles (Multi-Environment Design)
- **Verification:** DEL-26.02 §Shop/Field Procedures; DEL-26.04 §Inspection Records — **Source:** Procedure.md §Step 2.3

### Marine Coatings
- **Application:** Marine structures (berth, fenders, loading arms, marine equipment)
- **Coordination:** PKG-08 (Marine Structures), PKG-09 (Marine Outfitting), PKG-11 (Marine Loading System)
- **Exposure zones:**
  - Immersion zone: Continuous water immersion
  - Splash zone: Intermittent wetting, accelerated corrosion
  - Atmospheric zone: Above splash zone, atmospheric exposure
- **Functional requirement:** Corrosion protection (FR-2) and interface coordination (IR-3) — **Source:** Specification.md §FR-2, §IR-3
- **System type:** **TBD** — High-build epoxy or specialized marine coating per NACE/SSPC marine guidance — **Source:** Guidance.md §Examples (Marine Structures)
- **DFT (Dry Film Thickness):** **TBD** — Per NACE/SSPC marine coating guidance — **Source:** Specification.md §PR-4
- **Surface preparation:** **TBD** — Likely SSPC-SP 10 (near-white blast) for critical marine applications — **Source:** Specification.md §PR-5
- **Verification:** DEL-26.02 §Marine Application Procedures; DEL-26.04 §Marine Inspection Records — **Source:** Procedure.md §Step 2.4

### Field Painting
- **Application:** Touch-up, field welds, field joints, field-installed components
- **Functional requirement:** Compatibility with shop-applied coatings — **Source:** Specification.md §Scope (Inclusions)
- **System type:** **TBD** — Compatible with base coating system — **ASSUMPTION**
- **Requirements:** Material compatibility, surface preparation for field conditions, application within environmental limits (PR-6) — **Source:** Specification.md §PR-6
- **Verification:** DEL-26.02 §Field Application Procedures; DEL-26.04 §Field Inspection Records — **Source:** Procedure.md §Step 2.3

## References

**Source documents:**
- **Decomposition:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
  - Section 1: Project description
  - Section 5: PKG-26 Protective Coatings & Painting
  - Section 6: Objectives (OBJ-3 Storage Capacity, OBJ-9 Lifecycle Cost Optimization)
- **Context:** `_CONTEXT.md` — Deliverable identity and description
- **References:** `_REFERENCES.md` — Reference materials location
- **Cross-documents:** `Specification.md`, `Guidance.md`, `Procedure.md` (this deliverable)

**Applicable standards:**
- **SSPC** (The Society for Protective Coatings) — Surface preparation (SP series) and application (PA series) standards
- **NACE/AMPP** (NACE International, now part of AMPP) — Corrosion control standards
- **ISO 12944** — Paints and varnishes — Corrosion protection of steel structures by protective paint systems
  - Part 1: General introduction (durability classification)
  - Part 2: Classification of environments (corrosivity categories C1-CX)
  - Part 3: Design considerations
  - Part 4: Types of surface and surface preparation
  - Part 5: Protective paint systems
- **CSA S6 Annex** — Canadian Highway Bridge Design Code (coatings annex) — **ASSUMPTION** — **location TBD**
- **FDA 21 CFR 175.300** — Resinous and polymeric coatings for food contact — **location TBD**
- **NSF/ANSI 61** — Drinking water system components – Health effects — **location TBD**
- **ASTM D3359** — Standard Test Methods for Rating Adhesion by Tape Test
- **SSPC-PA 2** — Measurement of Dry Coating Thickness with Magnetic Gages

**Cross-references (internal to PKG-26):**
- **DEL-26.02** (Coating Procedures) — Implementation procedures for this specification
- **DEL-26.03** (Coating Data Sheet Package) — Material data sheets supporting coating selection
- **DEL-26.04** (Coating Installation & Test Records) — Inspection and test records demonstrating compliance

**Cross-references (interdisciplinary coordination):**
- **PKG-05** (Concrete Structures) — Tank foundation and structure coatings coordination
- **PKG-06** (Structural Steelwork) — Structural steel coating coordination, shop vs. field responsibilities
- **PKG-08** (Marine Structures) — Marine structure coating coordination, exposure zones
- **PKG-09** (Marine Outfitting) — Fender and equipment coating coordination
- **PKG-11** (Marine Loading System) — Loading arm coating coordination
- **PKG-13** (Storage Tanks) — Tank coating specification integration, tank design coordination
- **PKG-27** (Engineering Design) — DEL-27.01 Design Basis Documents (corrosivity classification, environmental conditions)
- **PKG-30** (Commissioning) — Tank internal coating acceptance and food-grade cleanliness verification
- **PKG-32** (Regulatory & Permits) — Environmental permits (VOC compliance)
- **PKG-33** (HSE Management) — Worker safety for coating application (ventilation, confined space entry)

**Dependency tracking:** NOT_TRACKED — Dependencies coordinated externally by humans (see `_DEPENDENCIES.md`)

**Project objectives:**
- **OBJ-3:** Storage Capacity (45,000 MT) — Tank internal coatings must maintain food-grade integrity and not compromise storage capacity
- **OBJ-9:** Lifecycle Cost Optimization — Coating selection must balance initial cost with long-term durability and maintenance requirements

**Source:** Decomposition Section 6

---

## Cross-Document Verification Summary

| Datasheet Section | Specification § | Guidance § | Procedure § |
|-------------------|-----------------|------------|-------------|
| Attributes (Standards) | Standards | Principles (Standards Context) | Step 1.3 |
| Conditions (Environmental) | FR-2, PR-2 | Considerations (Corrosivity) | Step 1.2 |
| Tank Internal Coatings | FR-1, PR-1, PR-4, PR-5 | Principles (Tank Internals) | Step 2.2 |
| Tank External Coatings | FR-2, FR-3, PR-2, PR-4, PR-5 | Examples (Tank Externals) | Step 2.2 |
| Structural Steel Coatings | FR-2, IR-2, PR-4, PR-5 | Trade-offs (Shop vs. Field) | Step 2.3 |
| Marine Coatings | FR-2, IR-3, PR-4, PR-5 | Examples (Marine Structures) | Step 2.4 |
| Field Painting | PR-6 | Considerations (Application) | Step 2.3 |

**Verification status:** Pass 3 complete — Cross-document section references added and verified.
