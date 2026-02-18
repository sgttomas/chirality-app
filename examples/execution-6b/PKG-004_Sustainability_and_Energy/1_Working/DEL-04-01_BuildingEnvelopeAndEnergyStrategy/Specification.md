# Specification: Building Envelope and Energy Strategy

## Scope

### What is Covered

This specification defines the content, requirements, and verification approach for DEL-04-01 -- the Building Envelope and Energy Strategy narrative, which is one of three discipline-level deliverables within PKG-004 (Sustainability & Energy).

- Building envelope thermal performance strategy (walls, roof, glazing)
- Air barrier system design location, continuity approach, and airtightness target
- Thermal bridging identification and mitigation approaches at key junctions
- Energy code compliance pathway (NECB or equivalent), including compliance method selection
- Overall building energy philosophy and quantified performance targets
- Integration with mechanical energy efficiency narrative (DEL-04-02): HVAC sizing, HRV, infiltration assumptions
- Integration with electrical energy efficiency narrative (DEL-04-03): lighting controls, solar-ready provisions
- Solar-ready roof provisions per Addendum 03 (orientation, structural loading allowance, rough-in strategy)
- Cold Storage zone envelope considerations (unheated, freeze-thaw dominant)

### What is Excluded

- Detailed mechanical energy equipment specifications and system selection (covered by DEL-04-02)
- Detailed electrical/lighting design specifications (covered by DEL-04-03)
- Architectural construction drawings or technical specifications
- Costed lifecycle analysis (unless used as supporting rationale for strategy choice)
- Durability and maintainability of envelope materials (covered by DEL-05-01 -- Architectural Durability)

### Applicable Context

- **Source Requirement:** SOW-0012 -- "Provide energy efficiency and sustainability approach narrative including solar-ready roof provisions, energy-efficient LED lighting, and building envelope strategy" (Decomposition v2.3, Scope Ledger)
- **RFP Section:** Section 7.1.2 Design Brief (narrative context); Section 7.1.4 sustainability subsection implicit
- **Objective:** OBJ-004 -- Deliver a strong Design Brief (contributes to 5-point Design Brief score, Decomposition §6)
- **Project Constraints:** 50-year main building design life; 20-year Cold Storage design life; cold Alberta climate; heating-dominated energy load
- **Coordination Points:**
  - DEL-04-02 (Mechanical Energy and Solar Readiness) -- envelope thermal load feeds HVAC sizing; airtightness target informs HRV assumptions
  - DEL-04-03 (Electrical Energy Efficiency) -- solar-ready electrical provisions; lighting internal heat gain assumptions
  - DEL-05-01 (Architectural Durability) -- material selection longevity and maintenance strategy

---

## Requirements

### R-ENV-001: Energy Philosophy Statement
**Requirement:** Articulate a clear, concise building energy philosophy statement that covers design intent, climate adaptation strategy, and the relationship between envelope performance and the 50-year design life of the main building.

**Source:** SOW-0012 ("overall building energy philosophy and performance targets"), Decomposition v2.3, Scope Ledger.

**Rationale:** Design Brief evaluators require a narrative explanation of design intent before technical detail. A coherent philosophy frames all subsequent strategy choices and demonstrates integrated thinking.

**Verification:**
- Philosophy statement is present and clearly articulated (2-4 sentences minimum)
- Statement addresses: (a) climate context, (b) envelope's role in energy performance, (c) 50-year design life intent
- Language is accessible to non-technical evaluators (Project Committee, permitting authority)

---

### R-ENV-002: Thermal Performance Targets
**Requirement:** Define building envelope thermal performance targets for walls, roof, and glazing expressed as R-values, U-values, or equivalent metrics; justify targets relative to energy code baseline or climate requirements.

**Source:** Deliverable description ("wall, roof, and glazing thermal performance targets"), _CONTEXT.md; SOW-0012, Decomposition v2.3.

**Rationale:** Explicit thermal performance targets are the primary quantitative output of the envelope strategy. They directly inform mechanical sizing (DEL-04-02) and form the basis for NECB compliance demonstration.

**Verification:**
- Targets stated explicitly with units (R-value in RSI or imperial, or U-value in W/m²K)
- Each assembly type addressed: above-grade walls, roof (and/or attic), glazing by orientation using the standard four-category classification: **south, east, west, north** (differentiated where thermal or solar gain performance differs by orientation) [Ref: Semantic Lensing C-002]
- Targets justified relative to NECB minimum or climate data reference
- If exceeding code minimum, increment and rationale stated

---

### R-ENV-003: Air Barrier Strategy
**Requirement:** Document the air barrier system design approach: location (inner or outer leaf), material type, continuity strategy, airtightness target (ACH50 or equivalent), and key transition details (penetrations, interfaces, Cold Storage isolation).

**Source:** Deliverable description ("air barrier continuity approach"), _CONTEXT.md; SOW-0012, Decomposition v2.3.

**Rationale:** Air barrier continuity is a primary driver of cold-climate building energy performance and moisture management. 50-year design life requires durable, accessible air barrier design.

**Verification:**
- Air barrier system location clearly specified (inner face, outer face, or hybrid)
- Material type referenced (membrane, sealed sheathing, or structural air barrier)
- Airtightness target stated (ACH50 or equivalent metric)
- Continuity approach documented at: wall-to-foundation, wall-to-roof, window/door frames, and mechanical penetrations
- Cold Storage zone isolation addressed (where conditioned/unconditioned zones meet)
- **Construction-phase airtightness verification:** Blower door test (per ASTM E779 or ASTM E1827) acceptance threshold stated; at minimum, the narrative must commit to a blower door test during construction and define the pass/fail criterion (e.g., "ACH50 < 3.5 as measured by blower door test per ASTM E779"). Design review alone is insufficient to confirm achieved airtightness. [Ref: Semantic Lensing C-001; SourcePath: Specification.md R-ENV-003 and Verification Approach table]

---

### R-ENV-003A: Vapor Management Strategy

**Requirement:** Document the vapor management strategy as a complement to the air barrier strategy (R-ENV-003): identify vapor drive direction by season, specify vapor retarder/barrier placement and permeability class, and address condensation risk at critical assembly locations including the Cold Storage boundary.

**Source:** Guidance.md P-001 (vapor-open outer layer), Guidance.md C-001 (vapor permeability management), Guidance.md C-002 (condensation risk). [Ref: Semantic Lensing X-001]

**Rationale:** In cold climates, moisture drive and condensation risk are critical to long-term envelope durability. The air barrier strategy (R-ENV-003) addresses air leakage but does not explicitly address vapor diffusion, which is a distinct moisture transport mechanism. The 50-year design life demands explicit vapor management to prevent concealed condensation and material degradation.

**Verification:**
- Vapor drive direction identified (outward in winter for cold climates)
- Vapor retarder/barrier location and permeability class stated (Class I, II, or III per applicable standard)
- Condensation risk assessment approach stated for key assemblies (walls, roof, Cold Storage boundary)
- Vapor-open outer layer strategy documented (if applicable, per Guidance P-001 recommendation)
- Coordination with air barrier location to avoid moisture trapping between two vapor-impermeable layers

---

### R-ENV-004: Thermal Bridging Mitigation
**Requirement:** Identify primary thermal bridge locations in the envelope and describe mitigation approaches for each; state an overarching thermal bridge performance objective.

**Source:** Deliverable description ("thermal bridging mitigation"), _CONTEXT.md; SOW-0012, Decomposition v2.3.

**Rationale:** Thermal bridging can account for 10-20% of additional heat loss in cold-climate buildings (ASSUMPTION: representative of typical cold-climate construction; exact value depends on assembly). Unmitigated thermal bridges undermine envelope R-value claims and may cause localized condensation or frost.

**Verification:**
- Key thermal bridge locations identified (minimum: wall-to-foundation, wall-to-roof, window/door frames, major mechanical penetrations)
- Mitigation strategy stated for each identified location
- Overarching thermal bridge performance objective stated (e.g., percentage additional heat loss limit or commitment to thermal modeling at Design Development phase)
- **Pass/fail acceptance criterion for thermal bridge performance:** The narrative must define a quantified threshold for acceptable thermal bridge impact (e.g., "thermal bridges shall not increase assembly heat loss by more than X% versus the clear-field R-value"). TBD -- the 10% figure cited in Guidance C-003 is labeled ASSUMPTION and requires confirmation by the Building Science Consultant before it can serve as a normative acceptance criterion. If unconfirmed, state the commitment to define this threshold during Design Development. [Ref: Semantic Lensing D-001; SourcePath: Specification.md R-ENV-004 Verification; Guidance.md C-003]

---

### R-ENV-005: Energy Code Compliance Pathway
**Requirement:** Identify the governing energy code (NECB or equivalent) and describe the selected compliance method (prescriptive path, performance path, or hybrid); document key assumptions and the timeline for formal compliance verification.

**Source:** Deliverable description ("energy code compliance pathway (NECB or equivalent)"), _CONTEXT.md; NECB listed in _REFERENCES.md; SOW-0012, Decomposition v2.3.

**Rationale:** Energy code compliance is a regulatory requirement and a mandatory element of the Design Brief. Clear compliance pathway avoids ambiguity during permitting and demonstrates design discipline.

**ASSUMPTION:** NECB is the applicable energy code for Alberta public buildings. OSR (Appendix A) may specify an alternative or additional standard; consult OSR and project AHJ to confirm. Source: _REFERENCES.md lists NECB; OSR reference location TBD.

**Verification:**
- Energy code identified with specific edition year (e.g., "NECB 2020" or "NECB 2017"); if edition year is not yet confirmed, state "NECB edition year TBD -- to be confirmed with AHJ during Design Development" rather than "current edition per AHJ" [Ref: Semantic Lensing A-001; SourcePath: Specification.md, R-ENV-005]
- Compliance method selected (prescriptive, performance, or hybrid) with rationale
- Key assumptions stated (e.g., climate zone, occupancy type, baseline reference building)
- Verification timeline stated (Design Development phase or later)

---

### R-ENV-006: Quantified Energy Performance Targets
**Requirement:** State at least one quantified energy performance target (e.g., percentage better than NECB baseline, estimated annual energy intensity in kWh/m²/year, or equivalent) for the main building.

**Source:** SOW-0012 ("energy efficiency and sustainability approach narrative"); Deliverable description ("overall building energy philosophy and performance targets"), _CONTEXT.md.

**Rationale:** Quantified targets signal analytical rigor and give evaluators a concrete benchmark. Even if formal energy modeling is not performed at Design Brief stage, a target range demonstrates commitment.

**Verification:**
- At least one quantified target stated with units or expressed as percentage relative to NECB baseline
- Scope of target clearly defined (main building; Cold Storage excluded from quantified target is acceptable given unheated classification)
- Basis for target stated (code minimum, parametric estimate, or comparable project reference); if estimated, label ASSUMPTION
- **Minimum ambition threshold:** The quantified target must demonstrate meaningful energy performance improvement consistent with the energy philosophy (P-003 "Energy Code as Floor, Not Ceiling"). TBD -- a minimum threshold (e.g., "at least 15% better than NECB baseline") should be defined to ensure the target reflects the stated energy ambition. A nominal target (e.g., 1% improvement) would technically satisfy the quantified target requirement but would not demonstrate the energy strategy described in Guidance P-003. [Ref: Semantic Lensing X-003; SourcePath: Specification.md R-ENV-006; Guidance.md P-003]

---

### R-ENV-007: Mechanical Integration
**Requirement:** Describe how the envelope strategy interfaces with mechanical energy efficiency (DEL-04-02): identify the key assumptions shared with mechanical design (airtightness, infiltration, heating/cooling load reduction) and any dependencies.

**Source:** _REFERENCES.md cross-reference to DEL-04-02; SOW-0012; Decomposition v2.3 DEC-008 (PKG-004 split by discipline, with coordination expected).

**Rationale:** Envelope and mechanical systems must be co-designed for whole-building energy performance. Misalignment between envelope load assumptions and HVAC sizing produces either over-sized equipment or unmet loads.

**Verification:**
- Key assumptions shared with mechanical identified (ACH50 target, wall/roof R-values, glazing SHGC by orientation, infiltration rate baseline)
- Dependency on DEL-04-02 coordination noted
- Any received feedback from mechanical integrated into envelope targets or noted as pending

---

### R-ENV-008: Electrical Integration and Solar-Ready Provisions
**Requirement:** Acknowledge the electrical energy efficiency strategy (DEL-04-03) and address solar-ready roof provisions per Addendum 03: roof orientation, structural loading allowance for future solar arrays, and rough-in strategy coordination.

**Source:** Addendum 03 s1.x (solar-capable roofing; orientation: flat, south, west, or southwest); _REFERENCES.md cross-reference to DEL-04-03; SOW-0012; Decomposition v2.3.

**Rationale:** Addendum 03 establishes a mandatory solar-readiness requirement. The building envelope (specifically the roof) is the primary deployment surface and must be designed for future solar installation.

**Verification:**
- Roof orientation stated and confirmed as aligned with Addendum 03 preference (flat, south, west, or southwest)
- Structural loading allowance for future solar array stated (design assumption, e.g., kg/m² distributed load)
- Mechanical rough-in strategy reference included (conduit, access, drain routing -- detailed by DEL-04-02)
- Electrical solar-ready provisions reference included (conduit, panel space, inverter location -- detailed by DEL-04-03)
- Coordination with DEL-04-02 and DEL-04-03 on solar-ready provisions documented

---

## Standards

| Standard | Reference | Applicability | Status |
|----------|-----------|----------------|--------|
| National Energy Code for Buildings (NECB), current edition | National Research Council Canada | Mandatory for energy code compliance pathway | **ASSUMPTION: likely applicable; confirm with AHJ** -- location TBD |
| CAN/ULC-S742 or CAN/CGSB-51.32 | Air barrier materials standard | Applicable for air barrier membrane specification | **location TBD** |
| ASTM E779 / ASTM E1827 | Building air tightness testing (blower door test) | Applicable for airtightness verification at Design Development | **location TBD** |
| RFP OSR (Appendix A) | Owner Statement of Requirements | Governs project-specific energy/sustainability requirements | **location TBD** -- accessible via RFP document |
| RFP Addendum 03 (Jul 31, 2024) | Solar-ready roofing requirements | Mandatory; governs solar orientation and rough-in | Available in `test/execution-6b/_Sources/` |
| Alberta Building Code (ABC) | Energy compliance (if applicable via provincial reference to NECB) | **Applicability to be confirmed with AHJ:** Alberta may adopt NECB by reference with provincial amendments, or impose additional provincial requirements. Determine whether ABC applies as a mandatory governing standard in addition to (or instead of) NECB, or only as a potential alternative pathway. This determination is required before energy code compliance pathway can be finalized. [Ref: Semantic Lensing A-002] | **location TBD** -- confirm with AHJ |

---

## Verification

### Verification Approach

| Requirement | Verification Method | Acceptance Criteria |
|-------------|---------------------|-------------------|
| R-ENV-001 (Philosophy) | Narrative coherence review | Philosophy present; addresses climate, envelope role, and 50-year life |
| R-ENV-002 (Thermal targets) | Narrative review + calculation check | Targets stated with units; justified vs. NECB or climate data |
| R-ENV-003 (Air barrier) | Design review + construction-phase blower door test commitment | Location, material, airtightness target, and continuity strategy documented; blower door test acceptance criterion stated (ACH50 threshold per ASTM E779/E1827) |
| R-ENV-003A (Vapor management) | Design review | Vapor drive, retarder placement, permeability class, and condensation risk approach documented |
| R-ENV-004 (Thermal bridging) | Narrative review + thermal modeling commitment | Key locations identified; mitigation strategies described; quantified performance acceptance criterion stated (% additional heat loss limit) or commitment to define threshold during Design Development |
| R-ENV-005 (Energy code) | Compliance pathway review | Code identified; method selected; assumptions and verification timeline documented |
| R-ENV-006 (Quantified targets) | Numerical check | At least one quantified energy target with units and basis |
| R-ENV-007 (Mechanical integration) | Cross-reference review with DEL-04-02 | Key assumptions identified; dependency on coordination documented |
| R-ENV-008 (Electrical/solar-ready) | Cross-reference review with DEL-04-03 + Addendum 03 check | Orientation aligned; structural loading stated; rough-in coordination documented |
| Cold Storage thermal boundary (R-ENV-003/R-ENV-008 supplemental) | Design review -- dedicated Cold Storage verification | Thermal boundary between conditioned main building and unconditioned Cold Storage meets NECB requirements for conditioned/unconditioned zone separation; freeze-thaw detailing addressed; vapor management at boundary documented [Ref: Semantic Lensing F-001; SourcePath: Specification.md R-ENV-003, R-ENV-008] |

### Verification Checklist

- [ ] Energy philosophy statement is present and clear (2-4 sentences minimum)
- [ ] Thermal performance targets stated for walls, roof, and glazing with units and rationale
- [ ] Air barrier location, material, airtightness target, continuity strategy, and blower door test commitment documented
- [ ] Vapor management strategy documented: vapor drive, retarder placement, permeability class, condensation risk
- [ ] Thermal bridge mitigation addressed for minimum: wall-to-foundation, wall-to-roof, window frames, major penetrations; pass/fail criterion stated or commitment to define in Design Development
- [ ] Energy code identified (NECB or equivalent); compliance method selected and documented
- [ ] At least one quantified energy performance target stated with units
- [ ] Key mechanical coordination assumptions shared (ACH50, load reduction, infiltration baseline)
- [ ] Solar-ready roof provisions aligned with Addendum 03; coordination with DEL-04-02 and DEL-04-03 documented
- [ ] Cold Storage zone envelope considerations addressed
- [ ] All cross-references checked: DEL-04-02, DEL-04-03, DEL-05-01 consistent with this deliverable
- [ ] ASSUMPTION labels applied to all inferred content

---

## Documentation

### Deliverable Artifact

**Format:** Narrative document section (Building Envelope and Energy Strategy) submitted as part of the Design Brief proposal package (PKG-004 contribution to the broader Design Brief evaluation).

**Anticipated Content Outline:**
1. Building Energy Philosophy
2. Climate Adaptation and Energy Performance Targets (with quantified target)
3. Thermal Performance Strategy -- Walls, Roof, Glazing (with R-values or U-values)
4. Air Barrier System Design (location, material, airtightness target, continuity)
5. Thermal Bridging Mitigation (key locations and strategies)
6. Energy Code Compliance Pathway (code identification, method, key assumptions, verification timeline)
7. Integration with Mechanical Systems (DEL-04-02 coordination)
8. Solar-Ready Provisions and Electrical Integration (DEL-04-03, Addendum 03 compliance)
9. Cold Storage Envelope Considerations
10. Forward: Design Development Phase Requirements

**Document-Level Readability Standard:**
All sections of the narrative (R-ENV-001 through R-ENV-008, including technical content) must use language accessible to non-technical evaluators (Project Committee, permitting authority). This standard currently appears only in R-ENV-001 verification ("Language is accessible to non-technical evaluators") but applies to the entire document, since the complete narrative targets the same non-specialist evaluation audience. Technical terms must be defined on first use; acronyms must be expanded. [Ref: Semantic Lensing E-002; SourcePath: Specification.md R-ENV-001 Verification bullet 3; Documentation section]

**Cross-Document Consistency Requirements:**
- Envelope thermal targets (R-values, U-values) must be consistent with the heating/cooling load assumptions in DEL-04-02
- Airtightness target (ACH50) must be consistent between this document and DEL-04-02 (mechanical ventilation sizing)
- Solar-ready roof orientation and structural loading must be consistent across DEL-04-01, DEL-04-02, and DEL-04-03
- Cold Storage zone treatment must be consistent with DEL-05-01 (Architectural Durability)
- "50-year design life" terminology must be used consistently (main building); "20-year design life" for Cold Storage

**Supporting Documents (to be produced in Design Development, not this deliverable):**
- NECB compliance checklist or energy model documentation
- Detailed wall, roof, and glazing section drawings with R-value calculations
- Blower door test protocol and acceptance criteria
- Thermal bridge modeling outputs (THERM or equivalent)
