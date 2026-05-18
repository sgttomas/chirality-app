# Guidance: Building Envelope and Energy Strategy

## Purpose

DEL-04-01 exists to produce a Building Envelope and Energy Strategy narrative that serves three purposes simultaneously:

1. **Score the Design Brief** (OBJ-004, 5 pts): Demonstrates a credible, integrated energy strategy to evaluators. The narrative must be coherent, technically grounded, and show that the team understands cold-climate building performance. (Source: Decomposition v2.3, §6 Objectives table; Evaluation Criteria Crosswalk §15.)

2. **Coordinate the PKG-004 trio**: This deliverable (building science perspective) must be developed in parallel with DEL-04-02 (mechanical energy and solar readiness) and DEL-04-03 (electrical energy efficiency). Together they form a whole-building energy narrative. The architect/building science lead holds the coordinating role. (Source: Decomposition v2.3, §8 PKG-004 description; DEC-008.)

3. **Establish the envelope basis for downstream work**: Thermal targets, airtightness assumptions, and solar-ready provisions developed here will directly inform HVAC sizing (DEL-04-02), lighting load assumptions (DEL-04-03), and material durability strategy (DEL-05-01 Architectural Durability). (Source: Decomposition v2.3, DEL-04-01 description; _REFERENCES.md cross-references.)

**This is a proposal-stage narrative, not a design document.** The goal is to make commitments that are specific enough to score well, while being honest about what will be determined in Design Development. Use TBD rather than inventing values, and label all inferred content as ASSUMPTION.

### OBJ-004 Scoring Rubric Mapping

OBJ-004 ("Deliver a strong Design Brief") carries 5 evaluation points across PKG-003 and PKG-004. The following mapping connects this deliverable's content areas to the dimensions most likely to earn points from the Project Committee evaluation. [Ref: Semantic Lensing F-002; SourcePath: Decomposition v2.3 §6 Objectives table; Specification Applicable Context]

| Scoring Dimension (ASSUMPTION) | Relevant DEL-04-01 Content | Guidance for Maximizing Score |
|---|---|---|
| Technical credibility | Thermal performance targets (R-ENV-002); air barrier strategy (R-ENV-003); thermal bridging mitigation (R-ENV-004) | Provide specific, quantified values with NECB comparison; demonstrate understanding of cold-climate building physics |
| Integrated thinking | Mechanical integration (R-ENV-007); electrical integration (R-ENV-008); coordination with DEL-04-02 and DEL-04-03 | Show how envelope, mechanical, and electrical strategies are co-designed; reference shared assumptions explicitly |
| Climate adaptation | Energy philosophy (R-ENV-001); climate-first design considerations (P-001) | Frame all strategies relative to Penhold's cold climate; address freeze-thaw and heating dominance directly |
| Code compliance and ambition | Energy code compliance pathway (R-ENV-005); quantified energy targets (R-ENV-006) | Demonstrate NECB compliance as a floor; quantify performance above code minimum |
| Completeness | Solar-ready provisions (R-ENV-008); Cold Storage considerations; vapor management (R-ENV-003A) | Address all scope areas including Addendum 03 compliance, Cold Storage boundary, and vapor management |

**ASSUMPTION:** The specific scoring dimensions and their relative weights are inferred from general Design Brief evaluation practice and the Decomposition's evaluation crosswalk. The actual rubric used by the Project Committee is not directly accessible. The Proposal Manager should confirm scoring emphasis before final narrative assembly.

---

## Principles

### P-001: Climate-First Envelope Design

**Statement:** The primary driver of envelope performance in Penhold's cold Alberta climate is minimizing heating energy loss. Everything else (glazing area, solar gain, infiltration control) is secondary to getting the thermal envelope and air barrier right.

**Application:**
- Prioritize opaque wall and roof thermal resistance (high R-values) over other energy strategies
- Exploit south and southwest glazing for passive solar gain where room functions allow it; limit north, east, and west glazing where possible [Ref: Semantic Lensing C-002 -- standardized four-category orientation classification: south, east, west, north]
- Design air barrier for durability and continuity first; achieve tight performance targets second
- Account for freeze-thaw cycling at all envelope interfaces (wall-to-foundation, window perimeters, Cold Storage zone boundaries)

**Design Considerations:**
- Penhold, Alberta is approximately Climate Zone 6 (ASSUMPTION: based on Canadian climate zone mapping; confirm against NECB tables with building science consultant). Heating Degree Days are substantial.
- Winter solar radiation is limited but real; south-facing glass with high Solar Heat Gain Coefficient (SHGC) provides useful heat gain on clear days
- Cold Storage (60'x100', unheated) requires its own thermal analysis: the boundary between conditioned and unconditioned zones must be carefully detailed for condensation and frost prevention
- Air barrier placement determines whether moisture accumulates within the assembly; inner air barrier with a vapor-open outer layer is generally preferred in cold climates

---

### P-002: Integrated Whole-Building Energy Strategy

**Statement:** Envelope, mechanical, and electrical energy performance are interdependent. A tight, well-insulated envelope reduces heating loads, which allows right-sized mechanical equipment. Efficient lighting reduces cooling loads and electricity demand. All three must be coordinated.

**Application:**
- Share envelope airtightness target (ACH50) with mechanical engineer early so HVAC ventilation systems (including HRV) are sized correctly
- Share glazing Solar Heat Gain Coefficient (SHGC) assumptions with mechanical engineer so solar heat gain is accounted for in peak load calculations
- Share roof solar-ready provisions with both mechanical (thermal collector rough-in) and electrical (PV conduit and panel space)
- Receive mechanical and electrical feedback before finalizing envelope targets

**Integration Checkpoints:**

| Assumption | Shared with | Purpose |
|------------|-------------|---------|
| Envelope airtightness target (ACH50) | DEL-04-02 (Mechanical) | Infiltration baseline for HVAC sizing |
| Wall and roof R-values | DEL-04-02 (Mechanical) | Heating/cooling load calculation |
| Glazing SHGC by orientation | DEL-04-02 (Mechanical) | Solar heat gain for peak load |
| LED lighting efficacy (internal heat gain) | Receive from DEL-04-03 (Electrical) | Cooling load adjustment |
| Solar-ready roof area, structural loading | DEL-04-02 and DEL-04-03 | Coordinate mechanical/electrical rough-in |

---

### P-003: Energy Code as Floor, Not Ceiling

**Statement:** NECB compliance is a minimum regulatory requirement. For a 50-year public building, targeting performance meaningfully above the code minimum is typically worth the incremental first cost.

**Application:**
- Identify NECB prescriptive minimums for climate zone and then set project targets above them
- Quantify the incremental cost and the lifecycle energy savings (even rough estimates help the Project Committee)
- Frame the surplus above code as a "margin of safety" for air tightness variability and thermal bridging that is hard to predict at design brief stage

**Design Considerations:**
- NECB prescriptive path is simpler and appropriate at Design Brief stage; performance path modeling provides flexibility but requires energy modeling expertise and time
- For cold climates, incremental insulation cost above NECB minimum is typically small relative to lifetime heating savings -- ASSUMPTION based on general cold-climate building economics; actual payback depends on energy prices and assembly cost
- If performance path is selected, identify the tool (HOT2000, EnerGuide, or equivalent) early and allocate design team time for modeling in Design Development phase

---

### P-004: Durability of Envelope for 50-Year Design Life

**Statement:** Envelope system selection must be evaluated for long-term serviceability, not just initial thermal performance. Materials that degrade, absorb moisture, or require frequent replacement undermine the 50-year design life.

**Application:**
- Select air barrier materials rated for or expected to achieve 50-year service life, or plan replacement at a defined interval with clear access strategy
- Rigid insulation materials (XPS, EPS, mineral wool) have generally high long-term thermal stability; assess moisture sensitivity for the specific assembly
- Design envelope details for inspection accessibility: future maintenance of sealants, gaskets, and membrane edges is only practical if they are accessible
- Coordinate with DEL-05-01 (Architectural Durability) to ensure material selection and maintenance strategy are consistent

**Design Considerations:**
- Membrane air barriers (polyethylene, housewrap) may require replacement at 20-30 years depending on UV/freeze-thaw exposure; if used, document replacement plan in DEL-05-01
- Structural air barriers (sealed sheathing, concrete, masonry) generally achieve 50-year life with normal maintenance
- Sealants and gaskets at window perimeters typically require replacement at 15-25 years; design for access

---

### P-005: Solar-Ready by Design, Not Retrofit

**Statement:** Addendum 03 requires solar-capable roofing. The envelope must be designed from the start to accommodate future solar thermal or PV systems, not retrofitted later. (Source: Addendum 03, solar-capable roofing requirement; Decomposition v2.3, SOW-0010.)

**Application:**
- Confirm roof orientation during conceptual design (south, southwest, west, or flat preferred per Addendum 03)
- Size roof structural capacity for future solar array distributed load (ASSUMPTION: TBD -- see CONF-ENV-04 in Conflict Table; previously stated as 50-100 kg/m² but inconsistent with EX-002 (1.5 kPa / ~150 kg/m²) and Procedure Step 6 (1.0-1.5 kPa); Structural Engineer to confirm a single design value) [Ref: Semantic Lensing B-003]
- Provide mechanical rough-in (conduit access, connection points, drain routing) for future solar thermal loop in coordination with DEL-04-02
- Provide electrical rough-in (oversized conduit from roof to electrical room, spare breaker capacity, inverter location) in coordination with DEL-04-03
- Protect roof membrane under future racking attachment points (pre-flash or pre-pad at anticipated array locations)

---

## Considerations

### C-001: Thermal Performance Target Selection

**Envelope Cost vs. Mechanical System Cost Trade-off:**

The envelope and mechanical system are a coupled system. A higher-performance envelope costs more to build but allows smaller, lower-cost mechanical equipment and reduces annual energy consumption.

| Envelope Performance Level | Envelope Cost Premium | Mechanical Size Impact | Annual Energy Impact |
|---------------------------|----------------------|----------------------|---------------------|
| NECB minimum (prescriptive) | Baseline | Baseline | Baseline |
| NECB + 20-30% (recommended) | +5-15% envelope cost | -5-15% mechanical sizing | -10-20% energy |
| NECB + 40%+ (high performance) | +20-30% envelope cost | -15-25% mechanical sizing | -20-30% energy |

Source: ASSUMPTION based on general cold-climate building trade-off literature; actual values depend on specific assembly cost, equipment cost, and energy rates. Use lifecycle cost analysis in Design Development to validate.

**Wall System Options for Cold Climate:**
- **Cavity insulation only** (mineral wool or fiberglass): Achieves NECB minimum; lower R-value per inch; thermal bridging through studs reduces effective R-value; standard construction
- **Continuous insulation (exterior rigid foam)**: Better thermal bridge control; higher R-value potential; vapor permeability management required; adds cost and wall thickness
- **Hybrid (cavity + continuous exterior)**: Best thermal performance; higher cost; recommended for public buildings targeting 50-year life and NECB margin

**Roof System Options:**
- **Above-deck rigid foam insulation**: High R-value; protects membrane from thermal cycling; adds depth; compatible with solar-ready provisions
- **Below-deck sprayed foam or batt**: Easier installation; may complicate future solar roof access; HVAC penetrations can increase

---

### C-002: Air Barrier Strategy Selection

Three viable approaches for the Penhold PSB:

**Option A: Outer Membrane Air Barrier (Breather Membrane on Sheathing)**
- Advantages: Protects insulation; vapor-open; easier to inspect during construction
- Disadvantages: UV and freeze-thaw exposure; 20-30 year service life typical; difficult to repair after cladding installed
- **Best for:** Simpler assemblies; moderate durability requirement

**Option B: Inner Structural Air Barrier (Sealed Sheathing or Drywall)**
- Advantages: Protected from UV and weather; longer service life; easier quality control during framing phase
- Disadvantages: Requires meticulous penetration sealing; thermal bridging through studs remains; condensation risk if vapor drive not managed
- **Best for:** Commercial and public buildings; 50-year design life priority

**Option C: Hybrid (Sealed Sheathing + Interior Sealant Layer)**
- Advantages: Redundancy; robustness against construction defects; best moisture management
- Disadvantages: Higher cost; more labor-intensive; risk of moisture trapping if not designed correctly
- **Best for:** High-performance buildings; cold climates with high moisture risk

**Recommendation for Penhold PSB:** Option B or C given 50-year design life and public building context -- ASSUMPTION. Final selection should be confirmed by Building Science Consultant based on specific assembly design.

---

### C-003: Thermal Bridging at Key Locations

| Bridge Location | Severity | Recommended Mitigation |
|-----------------|----------|----------------------|
| Wall-to-foundation (sill plate / rim joist) | High | Continuous insulation below grade and at rim joist; thermal break at slab-on-grade edge |
| Wall-to-roof (eave/soffit junction) | High | Exterior insulation continuous past roof line; minimize structural framing exposure |
| Window and door frames | Medium-High | Thermally broken aluminum frames (three-chamber); insulated reveal at jamb and sill |
| Mechanical chases / roof penetrations | Medium | Route through conditioned space where possible; insulate chase exterior if exposed; pre-insulate penetration sleeves |
| Cold Storage zone boundary | High | Cold Storage is unheated; the boundary wall/roof between conditioned and unconditioned zones requires continuous insulation and vapor management per ASSUMPTION that freeze-thaw is primary durability driver |
| Structural columns through envelope | Medium | Thermally broken connection; continuous insulation on exterior of column where possible |

**Performance Objective:** Target thermal bridge impact to less than 10% additional heat loss vs. ideal uniform assembly -- ASSUMPTION based on general cold-climate design practice. Verify by thermal modeling (THERM or equivalent) at Design Development phase.

---

### C-004: Cold Storage Zone Envelope

The Cold Storage building (60'x100', unheated) has fundamentally different envelope requirements from the main building:
- **No heating system:** Freeze-thaw is the primary durability and energy driver (not thermal efficiency)
- **Envelope thermal objective:** Prevent rapid temperature swings that cause condensation; manage frost at boundaries
- **Air sealing objective:** Prevent moisture infiltration that causes ice accumulation on interior surfaces
- **Boundary wall/roof (if attached):** The thermal boundary between conditioned main building and unheated Cold Storage must be continuous and properly detailed

ASSUMPTION: Cold Storage envelope does not need to meet NECB heating energy requirements (unheated building); however, the thermal boundary between it and the conditioned main building must meet NECB requirements. Confirm with NECB and AHJ.

---

### C-005: Solar-Ready Implementation Options

Addendum 03 allows flexibility in solar-ready approach. Three implementation strategies:

| Strategy | Structural Provision | Mechanical Rough-in | Electrical Rough-in | Cost Premium |
|----------|---------------------|--------------------|--------------------|-------------|
| Minimal (conduit only) | None | Conduit access at roof | Conduit + spare panel capacity | Low (~1-2%) |
| Standard (full rough-in) | Zone-specific reinforcement | Conduit + connection points + drain | Conduit + panel space + inverter location | Medium (~3-5%) |
| Full preparation (structural + rough-in) | Full PV array load structural capacity | Full solar thermal loop rough-in | Full inverter/combiner box space + electrical service sizing | Higher (~5-8%) |

**Recommendation:** Standard approach is typical for municipal projects with solar-ready intent but no confirmed future solar budget. Provides meaningful preparation without over-investing in unconfirmed future systems -- ASSUMPTION.

---

## Trade-offs

### T-001: Thermal Performance vs. First Cost

- **Issue:** Higher insulation and thermally broken frames increase envelope first cost but reduce energy operating cost over 50 years.
- **Context:** For a 50-year public building, lifecycle cost is a better decision metric than first cost. Incremental insulation above NECB minimum typically pays back in 8-15 years in cold climates -- ASSUMPTION based on general literature.
- **Proposed Resolution:** Target NECB + 20-30% envelope performance. Use lifecycle cost analysis in Design Development to validate. Present to Project Committee as value-engineered position.

### T-002: Airtightness Ambition vs. Durability and Maintenance

- **Issue:** Very tight air barrier (ACH50 < 2.0) requires premium materials and exceptional installation quality; may require mid-life replacement of specific components. Moderate tightness (ACH50 < 5.0) is more forgiving and compatible with standard construction practices.
- **Context:** 50-year design life requires either: (a) durable air barrier materials that last 50 years without replacement, or (b) a maintenance and replacement plan for materials with shorter service lives.
- **Proposed Resolution:** Target ACH50 < 3.5 as a balance of performance and durability. Select structural air barrier (inner face) as primary system for longevity. Document sealant replacement schedule in DEL-05-01. Confirm with Building Science Consultant.

### T-003: Envelope Performance vs. Mechanical System Efficiency

- **Issue:** A higher-performance envelope reduces heating/cooling loads but increases first cost. Alternatively, a standard envelope with high-efficiency mechanical equipment achieves similar annual energy outcomes at potentially different capital cost split.
- **Context:** For cold-dominated Alberta climate, envelope efficiency typically provides higher ROI than mechanical efficiency per dollar invested -- ASSUMPTION based on general building physics in heating-dominated climates; confirm with lifecycle cost analysis.
- **Proposed Resolution:** Envelope-first strategy (optimize envelope to reduce loads; right-size equipment to loads). This aligns with the integrated approach of the PKG-004 trio.

### T-004: Glazing Area vs. Solar Gain and Occupant Comfort

- **Issue:** Larger south-facing glazing area increases winter solar heat gain (useful) but may increase summer cooling load (undesirable) and increase envelope heat loss in winter nights.
- **Context:** Public Services Building occupant comfort in apparatus bays and offices has different glazing requirements. Apparatus bays may have minimal glazing; office/residential spaces benefit from daylighting.
- **Proposed Resolution:** Orientation-specific glazing strategy: south-facing, high-SHGC (0.50+) double low-E glass for office/residential; minimal glazing on north, east, west faces; operable shading for west-facing glazing. SHGC and U-value targets differentiated by orientation using the standard four-category classification: **south, east, west, north**.

### T-004A: Window-to-Wall Ratio (WWR) by Orientation and Functional Zone

**Context:** T-004 addresses glazing thermal properties (SHGC, U-value) and orientation strategy, but does not address the *area* of glazing as a design parameter. Window-to-wall ratio (WWR) significantly affects both energy performance and daylighting quality, and must be considered alongside glazing thermal properties. [Ref: Semantic Lensing X-002; SourcePath: Guidance.md T-004]

**Guidance by Functional Zone (ASSUMPTION: based on general cold-climate building design practice):**

| Functional Zone | Recommended WWR Range | Rationale |
|---|---|---|
| Offices, administrative spaces | 25-40% (south); 15-25% (east/west); 10-20% (north) | Balance daylighting for occupant comfort with envelope thermal performance; south orientation captures passive solar gain |
| Apparatus bays (fire hall) | 5-15% (any orientation) | Minimal glazing needed; large overhead doors dominate wall area; prioritize thermal envelope integrity |
| Public Works shop / workshop | 10-20% (south/east preferred) | Moderate daylighting for work tasks; avoid excessive heat loss; overhead doors reduce available wall area |
| Shared / common areas | 20-35% (south preferred) | Daylighting for public-facing spaces; balance with energy performance |
| Cold Storage (unheated) | 0-5% | Minimal glazing; freeze-thaw and moisture management are primary concerns |

**Design Considerations:**
- Higher WWR on south faces is acceptable when paired with high-SHGC glazing (net winter energy benefit from passive solar gain may offset increased heat loss)
- WWR above 40% on any face significantly increases heating load in cold climates and may require compensating measures (triple glazing, external shading)
- NECB prescriptive path may impose maximum fenestration-to-wall ratios by orientation; confirm against NECB tables for the applicable climate zone (TBD)
- Coordinate WWR assumptions with DEL-04-02 (mechanical) for heating/cooling load implications and DEL-04-03 (electrical) for daylighting vs. artificial lighting trade-off

**ASSUMPTION:** WWR ranges are based on general cold-climate building design practice for similar building types. Actual WWR to be determined by the Architect during Design Development, informed by the energy philosophy and occupancy requirements.

---

## Examples

### EX-001: Cold Climate Wall Assembly (Worked Example)

**Scenario:** Main building above-grade wall targeting NECB + 20-30% in Alberta climate.

**Assembly (inside to outside):**
1. Interior finish (drywall or equivalent)
2. Interior air barrier sealant and gasket at all penetrations (structural air barrier layer)
3. Steel or wood stud framing with 90 mm mineral wool batt cavity insulation
4. Exterior structural sheathing (OSB or plywood, sealed at all edges and fastener penetrations)
5. 100-150 mm continuous rigid mineral wool exterior insulation (vapor-open; thermal bridge mitigation)
6. Ventilated rainscreen gap (minimum 10 mm)
7. Exterior cladding (metal panel, fiber cement, or brick)

**Thermal Performance:**
- Effective wall R-value: approximately R-40 to R-50 (combined cavity + continuous insulation, less thermal bridging credit)
- Meets and exceeds NECB prescriptive minimum for Climate Zone 6 -- ASSUMPTION pending NECB table confirmation
- Exterior continuous insulation eliminates approximately 50-60% of stud thermal bridging vs. cavity-only assembly -- ASSUMPTION based on general building science practice

**Coordination Note:** Electrical conduit and mechanical small pipes routed in cavity (interior to exterior continuous insulation) to avoid penetrating thermal bridge zone.

---

### EX-002: Solar-Ready Roof Assembly (Worked Example)

**Scenario:** Main building flat roof oriented south-southwest with standard solar-ready provisions.

**Assembly:**
1. Structural roof deck (metal deck on steel framing or engineered wood)
2. Above-deck rigid insulation (150-200 mm polyisocyanurate or mineral wool)
3. Roof membrane (TPO, modified bitumen, or equivalent; solar-durable specification preferred)
4. Mechanical rough-in conduit (25 mm minimum, from mechanical room to roof via pre-flashed penetration at south roof zone) for future solar thermal loop
5. Electrical rough-in conduit (38 mm minimum, from electrical room to roof) for future solar PV wiring
6. Structural reinforcement zones: TBD kPa superimposed dead load capacity at designated PV array locations -- ASSUMPTION; previously stated as 1.5 kPa (~150 kg/m²) but inconsistent with P-005 (50-100 kg/m²) and Procedure Step 6 (1.0-1.5 kPa); see CONF-ENV-04 in Conflict Table; Structural Engineer to confirm a single design value [Ref: Semantic Lensing B-003]

**Solar-Ready Features (Addendum 03 compliance):**
- Roof orientation: south-southwest (aligned with Addendum 03 preference)
- Structural capacity for future array: explicitly designed into structural brief
- Mechanical conduit: installed and capped at roof level; connection points in mechanical room
- Electrical conduit: installed and capped at roof level; panel space reserved; inverter location designated in electrical room

---

### EX-003: Thermal Bridge Detail -- Wall to Foundation (Worked Example)

**Scenario:** Above-grade main wall meeting slab-on-grade foundation at apparatus bay.

**Detail approach:**
- Below-grade insulation: 50-75 mm rigid XPS wrapping exterior face of foundation wall from grade to frost depth
- Slab edge insulation: 50 mm XPS under slab perimeter (minimum 600 mm wide from edge) to minimize heat loss at slab/grade interface
- Above-grade exterior insulation (from wall assembly) lapped to meet below-grade insulation with no gap at grade line
- Sealant / air barrier membrane from interior structural sheathing wrapped down and under slab edge, lapped with dampproofing at foundation

**Thermal bridge reduction:** Eliminates high-conductivity concrete path from interior slab to exterior; reduces junction heat loss by estimated 40-70% vs. uninsulated foundation edge -- ASSUMPTION based on general building science principles.

---

## Conflict Table (for human ruling)

| ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|----|----------|----------|----------|------------------|------------------|--------------|
| CONF-ENV-01 | Which energy code governs: NECB (national) or an Alberta provincial code, or both | _REFERENCES.md lists NECB; _CONTEXT.md references NECB or equivalent | OSR (Appendix A) may specify provincial override or AHJ-specific standard; OSR content not directly accessible | Specification R-ENV-005 (Energy Code Compliance Pathway); Standards table | Assume NECB until OSR reviewed; confirm with project AHJ and Building Science Consultant | TBD |
| CONF-ENV-02 | Solar-ready provisions: which deliverable takes primary responsibility for defining structural loading requirement | Addendum 03 requires solar-capable roofing; DEL-04-01 addresses roof envelope and structural loading allowance | DEL-04-02 (Mechanical) also addresses structural rough-in for solar thermal; structural loading could conflict if each deliverable makes independent assumptions | Specification R-ENV-008; P-005; T-004 | DEL-04-01 states envelope/structural envelope assumption; DEL-04-02 states mechanical rough-in; both must use same structural loading number. Coordinating architect resolves by agreeing one number early | TBD |
| CONF-ENV-03 | Airtightness target (ACH50): Specification proposes < 3.5 as a reasonable target; NECB prescriptive path may only require < 5.0 | Guidance C-002 and T-002 propose ACH50 < 3.5 | NECB prescriptive requirements for airtightness (location TBD; ASSUMPTION based on common NECB airtightness clause); DEL-04-02 may size HRV differently depending on infiltration rate | Specification R-ENV-003; Guidance C-002, T-002 | ACH50 < 3.5 is reasonable for 50-year public building. Confirm with mechanical engineer that HRV sizing is consistent with this target | TBD |
| CONF-ENV-04 | Solar array structural loading values inconsistent across documents: P-005 states "50-100 kg/m2" (ASSUMPTION); EX-002 states "1.5 kPa (approximately 150 kg/m2)"; Procedure Step 6 states "1.0 to 1.5 kPa" -- these three values are not the same range | Guidance P-005 (50-100 kg/m2); Guidance EX-002 (1.5 kPa / 150 kg/m2) | Procedure Step 6 (1.0-1.5 kPa) | Specification R-ENV-008; Guidance P-005, EX-002; Procedure Step 6 | Structural Engineer to confirm a single design loading value; all documents to be updated to use the confirmed value | TBD |

### Conflict Resolution Process [Ref: Semantic Lensing X-004]

The conflicts listed above (CONF-ENV-01 through CONF-ENV-04) all require human ruling before the Design Brief can be finalized. To prevent unresolved ambiguity from entering the Design Brief, the following resolution process applies:

| Step | Action | Responsible Party | Timeline |
|---|---|---|---|
| 1. Identification | Conflicts identified and recorded in this table during document drafting | Architect / Building Science Consultant | During Design Brief drafting (Weeks 1-3) |
| 2. Assignment | Proposed Authority column identifies the party best positioned to resolve each conflict | Architect / Design Lead | By end of Week 2 |
| 3. Investigation | Assigned party investigates and prepares a recommended resolution with supporting rationale | Per Proposed Authority column | Within 5 business days of assignment |
| 4. Decision | Architect/Design Lead reviews recommendation and records the Human Ruling in this table | Architect / Design Lead | Before final narrative assembly (Step 8 of Procedure) |
| 5. Implementation | Affected sections (per Impacted Sections column) are updated to reflect the ruling | Document author | Within 2 business days of ruling |
| 6. Verification | Updated sections reviewed for cross-document consistency | Per Procedure V-002 checklist | Before submission |

**Escalation:** If a conflict cannot be resolved by the Proposed Authority within the stated timeline, the Architect/Design Lead escalates to the Project Manager for a binding decision. Unresolved conflicts must not remain at TBD in the final submitted narrative.

---

## Notes and Forward References

- **Design Development:** Thermal performance targets stated in this narrative are commitments, not final specifications. Detailed calculations (NECB compliance tables, wall section R-value calculations, window U-value specifications) are Design Development deliverables.
- **Energy Modeling:** If performance path NECB compliance is selected, a qualified energy engineer must be engaged for Design Development phase modeling. Flag this resource requirement early.
- **Material Selection:** Specific product selections (insulation type and brand, air barrier membrane product, window frame system) are deferred to Design Development. This narrative defines performance criteria only.
- **Cold Storage Thermal Boundary:** The conditioned-to-unconditioned boundary (main building to Cold Storage) requires careful detail design. Flag for DEL-05-01 (Architectural Durability) and structural coordination.
- **Addendum 03 Compliance:** All three PKG-004 deliverables (DEL-04-01, DEL-04-02, DEL-04-03) must be reviewed together to confirm complete Addendum 03 solar-ready compliance. No single deliverable can satisfy the requirement alone.
