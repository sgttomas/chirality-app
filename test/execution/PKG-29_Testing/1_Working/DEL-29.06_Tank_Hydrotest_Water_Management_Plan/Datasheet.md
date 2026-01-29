# Datasheet: DEL-29.06 Tank Hydrotest Water Management Plan

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-29.06 |
| Name | Tank Hydrotest Water Management Plan |
| Package | PKG-29 Testing |
| Discipline | T&C |
| Type | Plan |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

**Source:** _CONTEXT.md, Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md line 651

## Attributes

| Attribute | Value |
|-----------|-------|
| Plan Type | Environmental Management Plan (Hydrotest Water) |
| Applicable Tanks | 3 × 15,000 MT storage tanks (TK-101, TK-102, TK-103) **ASSUMPTION** |
| Water Volume | ~45,000 m³ total (3 tanks) **ASSUMPTION based on 15,000 MT capacity** |
| Test Duration | 24-48 hours hold per tank (typical per API 650) **ASSUMPTION** |
| Environmental Focus | Water sourcing, treatment, quality, discharge/disposal compliance |

**Source:** _CONTEXT.md; Decomposition Section 1 (3 × 15,000 MT tanks); API 650 **ASSUMPTION**

**ASSUMPTION:** Storage tank hydrotest water management is environmentally significant due to large volumes and potential contaminants.

## Conditions

**Operating / Environmental Context:**

Defines the planned approach and controls for tank hydrotest water management plan to meet ER requirements. **Source:** Decomposition line 651

**Environmental Context:**

**Marine Terminal Location:**
- Fraser Surrey Terminal, Surrey, BC
- Adjacent to Fraser River
- Stormwater discharge likely subject to municipal and provincial permits
- Marine environment protection requirements

**Source:** Decomposition Section 1 (Project Context)

**Hydrotest Water Management Challenges:**

1. **Large Volume:** 3 tanks × ~15,000 m³ each = ~45,000 m³ water **ASSUMPTION**
2. **Water Sourcing:** Municipal water supply or river intake (permit requirements)
3. **Contamination:** Tank coatings may leach chemicals; rust/mill scale from steel surfaces
4. **Treatment:** May require filtration, chemical treatment, settling before discharge
5. **Discharge Compliance:** Must meet receiving water quality standards (Fraser River or municipal sewer)
6. **Timing:** Seasonal considerations (fish spawning periods, water temperature) **ASSUMPTION**

**Project Objectives Supported:**
- OBJ-7: Environmental Protection (water management prevents environmental impact)
- OBJ-6: Regulatory Compliance (permits and discharge standards)

**Source:** Decomposition Section 2, Section 6; general hydrotest water management concerns **ASSUMPTION**

## Construction

**Plan Components:**

### 1. Hydrotest Fill/Hold/Drain Plan

**Fill Plan:**
- Water source: Municipal potable water or permitted river intake **TBD**
- Fill rate: **TBD** m³/hr (limited by supply capacity)
- Fill duration per tank: **TBD** days
- Fill sequence: TK-101 → TK-102 → TK-103 (staggered to manage water demand) **ASSUMPTION**

**Hold Plan:**
- Hold duration: 24 hours minimum per API 650 **ASSUMPTION**
- Monitoring: Visual inspection for leaks, pressure/level monitoring
- Weather protection: Cover tank openings during hold period

**Drain Plan:**
- Drain rate: **TBD** m³/hr (controlled to allow treatment)
- Drain duration per tank: **TBD** days
- Drain destination: Treatment system → discharge or haul-away

**Source:** API 650 Section 7 (hydrotest requirements); typical hydrotest planning **ASSUMPTION**

### 2. Treatment Approach

**Potential Treatment Methods:**
- **Settling:** Allow suspended solids to settle before discharge
- **Filtration:** Remove particulates (rust, mill scale, coating particles)
- **pH Adjustment:** Neutralize if acidic or alkaline from coating leachate
- **Chemical Treatment:** Coagulants/flocculants to enhance settling
- **Oil/Grease Removal:** Skim any floating hydrocarbons

**Treatment System:**
- Temporary treatment system (tanks, filters, pumps) or mobile treatment unit
- Location: **TBD** — adjacent to tank farm
- Capacity: Match or exceed drain rate

**TBD:** Specific treatment requirements based on water quality testing (see DEL-29.07)

**Source:** General industrial wastewater treatment practices **ASSUMPTION**

### 3. Sampling/Testing Plan

**Sampling Strategy:**
- **Pre-fill:** Test source water quality (baseline)
- **Post-fill:** Sample from tanks after fill complete (check for contamination)
- **Pre-discharge:** Sample from each tank before draining (determine treatment needs)
- **Post-treatment:** Sample treated water before discharge (verify compliance)

**Test Parameters (typical):**
- pH, Temperature, Conductivity
- Total Suspended Solids (TSS)
- Oil & Grease
- Heavy Metals (if coating contains metals)
- Chemical Oxygen Demand (COD) or Biological Oxygen Demand (BOD)
- **TBD:** Specific parameters per discharge permit requirements

**Acceptance Criteria:**
- Discharge water must meet permit limits for receiving water (Fraser River or municipal sewer)
- **TBD:** Specific discharge limits per environmental permits **location TBD**

**Source:** Typical industrial discharge monitoring **ASSUMPTION**

### 4. Discharge/Hauling Plan

**Discharge Options:**

**Option A: Direct Discharge to Fraser River (with treatment)**
- Requires provincial discharge permit (BC Ministry of Environment)
- Must meet river water quality standards
- Discharge point: **TBD**
- Discharge rate: **TBD** (may be limited by permit)

**Option B: Discharge to Municipal Sewer (with treatment)**
- Requires municipal sewer discharge permit
- Must meet municipal wastewater acceptance criteria
- Discharge point: **TBD**
- May incur sewer use fees

**Option C: Haul-Away for Offsite Disposal**
- If water quality cannot meet discharge standards
- Licensed liquid waste hauler
- Disposal at approved wastewater treatment facility
- Volume: ~45,000 m³ → ~450 tanker truck loads (100 m³ per truck) **ASSUMPTION**
- Cost and logistics significant for haul-away option

**Selection:** **TBD** — Based on permit availability, water quality, and cost

**Source:** Typical disposal options for industrial wastewater **ASSUMPTION**

## References

**Decomposition & Context:**
- Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 5, PKG-29, line 651)
- _CONTEXT.md
- _REFERENCES.md

**Applicable Standards and Regulations:**
- API 650: Welded Tanks for Oil Storage (hydrotest requirements)
- BC Environmental Management Act (discharge permits)
- Metro Vancouver Sewer Use Bylaw (if municipal discharge) **ASSUMPTION**
- Fisheries Act (protection of fish habitat, Fraser River)
- Municipal stormwater bylaws
- Employer's Requirements: **location TBD**

**Cross-References:**

**Upstream (Input):**
- DEL-13.01-13.06: Storage Tanks (tank design, coatings, hydrotest requirements)
- Environmental permits **TBD**

**Downstream (Output):**
- DEL-29.01: Test Procedures (hydrotest procedures reference water management plan)
- DEL-29.07: Water Treatment & Discharge Testing Results (implements testing from this plan)
- DEL-29.08: Water Disposal Records (implements disposal from this plan)

See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)

---

## Cross-Document Linkage

| Document | Key Sections | Relationship |
|----------|--------------|--------------|
| Specification.md | §Requirements (FR-1 to FR-4, PR-1 to PR-2, IR-1 to IR-2, QR-1 to QR-2) | Defines requirements for water management components |
| Guidance.md | §Principles, §Considerations, §Trade-offs, §Examples | Provides rationale and examples for plan development |
| Procedure.md | §Steps 1-8 | Defines process for developing and approving the plan |

**Cross-Deliverable Consistency Notes:**
- Plan supports hydrotest procedures in DEL-29.01
- Testing results documented in DEL-29.07 (Water Treatment & Discharge Testing Results)
- Disposal records documented in DEL-29.08 (Water Disposal Records)
- Tank specifications from PKG-13 (3 × 15,000 MT tanks) drive water volume calculations
- Environmental objectives OBJ-7 (Environmental Protection) and OBJ-6 (Regulatory Compliance) are primary drivers
- Water volume (~45,000 m³) and Fraser River location are key constraints
