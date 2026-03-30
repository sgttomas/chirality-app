# Guidance — DEL-002-01 Preliminary Structural Design

---

## 1. Purpose

DEL-002-01 exists to obtain Camrose County's approval of the structural design concept before detailed engineering resources are committed to final design. The preliminary design is the Structural Engineer's first formal communication of the structural system intent to the Owner in a design-build context where the County "only has a concept in mind" (RFP §3.4). Approval at this stage protects both parties: the County confirms the structural approach aligns with its program requirements, and the Design-Builder locks in a design direction before incurring the full cost of detailed calculations and IFC drawings.

In the CCDC 14–2013 design-build delivery model, the Proponent holds design risk. The preliminary design stage is therefore the critical risk-check gate — structural system choices made and approved here propagate into all downstream structural deliverables (DEL-002-02 through DEL-002-12) and into the downstream construction packages (PKG-010, PKG-011).

### 1.1 Value Proposition (A-005)

The preliminary structural design stage creates value for both the Owner and the Design-Builder:

- **Risk reduction:** Structural system decisions confirmed at this stage prevent costly redesign during final engineering. Major structural changes after detailed design has begun can cascade through all disciplines.
- **Cost certainty:** By establishing the structural approach before final design, the Design-Builder can provide a more reliable cost estimate and the Owner can evaluate whether the structural approach fits within budget expectations. The variable-price foundation component (RFP §4.8.2) is explicitly identified and bounded at this stage.
- **Schedule protection:** County approval of the structural concept at the preliminary stage is a gate condition (SOW-0010b). Proceeding without this approval risks abortive work on final design if the County requires fundamental changes to the structural system.

**Source:** RFP §3.3.2 (County approval before final design), RFP §4.8.2 (variable-price), Decomposition §7 PKG-002 (downstream deliverable dependency). ASSUMPTION: value proposition framing inferred from standard design-build practice and the RFP structure; not explicitly stated in sources.

---

## 2. Principles

### 2.1 Design-Build Context

The RFP is explicit that the County has a conceptual program, not a complete brief (RFP §3.4). The Structural Engineer must therefore use engineering judgment to interpret the conceptual drawings (App B Shop) and the design requirements list (RFP §3.4) as a performance specification, not a prescriptive one. The preliminary design is the Structural Engineer's proposed interpretation for County confirmation.

**Source:** RFP §3.4 — "The County only has a concept in mind; therefore, it will be a design/build project."

### 2.2 Geotechnical Dependency

The foundation cannot be designed to a final standard until the geotechnical investigation (SOW-0001) is complete. The preliminary design must present the foundation concept transparently as a variable-price element, with the assumptions used for the preliminary cost estimate stated explicitly. The RFP acknowledges this: "pricing negotiated post-geotech report; estimate based on normal ground conditions" (Decomposition, SOW-0019 note; RFP §4.8.2).

**Rationale for proceeding without the geotechnical report (C-003):**

The preliminary design can proceed without the geotechnical report because:

1. **The RFP structure explicitly anticipates this sequence.** RFP §4.8.2 establishes the foundation as a variable-price element with pricing negotiated post-geotech report, indicating the County expects the design process to start before geotech results are available.
2. **The preliminary design addresses superstructure, not foundation details.** The primary purpose of DEL-002-01 is to establish the structural system concept for County approval. The superstructure design (wall system, roof framing, crane runway, mezzanine) can be developed independently of the foundation type.
3. **Foundation is presented as conditional.** The preliminary design will present the foundation approach based on the "normal ground conditions" assumption (Decomposition SOW-0019 note) and explicitly state that this is subject to revision upon receipt of geotechnical results.

**Limitations the Owner should understand:**

- The foundation section of the preliminary design presentation is provisional and will require revision once the geotechnical report is available.
- The preliminary cost estimate for foundation work is based on an assumption of normal ground conditions; actual costs could differ significantly if poor ground conditions are encountered.
- Certain superstructure design decisions (e.g., service pit depth, below-grade waterproofing) may need to be revisited based on groundwater conditions identified in the geotechnical report.

**Source:** RFP §4.8.2, SOW-0019, Decomposition §3.

### 2.3 Code Compliance Commitment

The preliminary design is the first formal opportunity for the Structural Engineer to commit to the governing code framework. Stating the intended code suite (NBC edition, ABC amendments, applicable CSA standards) at this stage sets the regulatory baseline for all subsequent structural design work and for permit applications (SOW-0005, SOW-0006, SOW-0007, SOW-0008, SOW-0009).

**Source:** RFP §3.3.2.

### 2.4 Downstream Deliverable Seeding

Every structural detail deliverable downstream (DEL-002-02 through DEL-002-09) derives from decisions made in this preliminary design. Choices made here regarding the structural grid, column spacing, crane runway type, mezzanine structural system, and service pit geometry directly determine the scope and complexity of subsequent drawing sets and the calculation package (DEL-002-10).

**Source:** Decomposition §7, PKG-002 deliverable table.

---

## 3. Considerations

### 3.1 Structural System for 35 ft Concrete Structure

A 35 ft (10.67 m) clear ceiling height is an unusually tall industrial building. This has significant implications for:

- Wall structural system (tilt-up concrete panels, precast concrete, cast-in-place concrete, or hybrid — TBD at preliminary stage; ASSUMPTION: structural system selection is within Structural Engineer's judgment)
- Column design (slender columns require careful buckling analysis)
- Lateral load resistance (wind and seismic design for a tall structure in an Alberta location)
- Roof structure spanning the 100 ft × 130 ft footprint

The preliminary design should address which wall/column system is proposed and the preliminary roof framing concept.

**Source:** RFP §3.4 (35 ft ceiling); App B (Shop) (130 ft × 100 ft conceptual footprint).

### 3.2 Overhead Crane Runway (Two 5-Tonne Cranes)

Two 5-tonne cranes on trolley impose significant vertical and horizontal loads on the runway structure. Key structural considerations include:

- Crane rail alignment and runway beam sizing (preliminary span/depth concept)
- Column or wall bracket design for runway support — must be compatible with the 35 ft ceiling height and the drive-through bay arrangement
- Crane fatigue category (CAN/CSA S16 — ASSUMPTION: likely applicable; location TBD)
- Clearance between crane hook height and ceiling/roof structure
- The conceptual floor plan (App B Shop) shows two crane tracks running the length of the main shop area, approximately 60 ft spacing (ASSUMPTION — scale-read from conceptual drawing)

**Source:** RFP §3.4, SOW-0067, App B (Shop).

### 3.3 Mezzanine Design Load

The mezzanine is described as capable of handling "heavy items such as several oil totes and oil pumping equipment" (RFP §3.4, SOW-0033). The Structural Engineer should propose a design live load appropriate for this use at the preliminary stage. Standard storage mezzanines often use 4.8 kPa (100 psf) or higher; the actual value should be based on realistic oil tote and equipment weights (ASSUMPTION — specific numerical load not stated in RFP; Structural Engineer to establish and propose for County review).

The mezzanine spans above three distinct spaces (parts room, utility room, wash bay), which may have different structural grid requirements.

**Source:** RFP §3.4, SOW-0032, SOW-0033, App B (Shop).

### 3.4 Service Pit / Trench

The service pit is a below-grade concrete structure that must:

- Accommodate mechanics working under large equipment (motor-scraper scale)
- Provide structural support for vehicles driving over it
- Include mechanical provisions (ventilation) and electrical provisions (lighting) coordinated with other disciplines
- The conceptual drawing (App B Shop) shows the Service Pit at approximately 24 ft wide × 100 ft long on the east side of the main shop (ASSUMPTION — scale-read from conceptual drawing)

The pit walls and slab must resist lateral earth pressure and any hydrostatic pressure depending on local groundwater conditions (TBD from geotech).

**Source:** RFP §3.4, SOW-0028, App B (Shop).

### 3.5 Steel Plate Embedments

Steel plates embedded in the concrete floor allow tracked and packer-type heavy equipment to operate without damaging the floor slab. The preliminary design should confirm:

- Plate thickness and grade (TBD at preliminary stage — ASSUMPTION: to be established by Structural Engineer)
- Embedment details (welded studs, rebar ties — TBD)
- Plate locations consistent with App B (Shop) conceptual drawing (multiple locations shown in the main shop and wash bay areas)

**Source:** RFP §3.4, SOW-0024, App B (Shop).

### 3.6 Wash Bay Structural Integration

The wash bay is a single enclosed bay (24 ft wide) with specific structural requirements:

- Wall and roof integration with the main building envelope at 35 ft ceiling
- Steel plate floor (per App B Shop notes and SOW-0027a)
- Drainage provisions through the slab (coordinated with plumbing: SOW-0027b)
- The exterior mud sump is outside the building envelope — structural implications for the sump itself may be limited (TBD)

**Source:** RFP §3.1, §3.4, SOW-0027a, SOW-0027b, App B (Shop).

### 3.7 Connection to Old North Shop

The New North Shop Addition is shown adjacent to the existing Old North Shop (105 ft × 40 ft) in the conceptual layout. The preliminary design should address:

- Whether the two structures will be structurally connected or separated by an expansion joint
- Any structural implications for the Old North Shop renovation items (mezzanine, washroom, locker/change room — SOW-0071, SOW-0072, SOW-0073)

This is a coordination item with the Architect (PKG-001).

**Source:** App B (Shop); SOW-0071–SOW-0073 (renovation scope).

---

## 4. Trade-offs

### 4.1 Concrete Wall System Selection

| Option | Advantage | Disadvantage |
|---|---|---|
| Tilt-up concrete panels | Fast erection, cost-effective for large footprint, integrates floor slab pour | Requires large crane for erection; not suitable if site access is constrained |
| Precast concrete | Factory quality control, can achieve complex shapes | Longer lead time; transportation constraints; expensive connections |
| Cast-in-place concrete | Maximum design flexibility; good for complex geometry | Formwork cost; slower construction; weather-dependent |

**Source:** ASSUMPTION — these are standard industry options for a concrete structure of this scale; no specific system is prescribed in the RFP. The Structural Engineer must select and present a preferred option at the preliminary stage.

### 4.2 Foundation Type

| Scenario | Likely Foundation Approach | Basis |
|---|---|---|
| Normal ground conditions | Conventional spread footings or strip footings | Decomposition SOW-0019 note; ASSUMPTION |
| Poor ground conditions (e.g., soft clay, fill) | Piles or deep foundations | TBD from geotech; variable-price scope |
| High groundwater | Modified design for service pit waterproofing and buoyancy | TBD from geotech |

**Source:** RFP §4.8.2, SOW-0019, SOW-0023. Geotechnical investigation (SOW-0001) is the upstream dependency.

### 4.3 Lateral Load Resistance System Selection (X-001)

For a 35 ft (10.67 m) concrete structure in Alberta, lateral load resistance (wind and seismic) is a primary design decision. Guidance §3.1 identifies this as a consideration but the trade-off analysis had not been developed. The following options are typical for a structure of this type:

| Option | Advantage | Disadvantage | Compatibility Notes |
|---|---|---|---|
| Concrete shear walls | High stiffness, integrates with tilt-up or precast panel systems, excellent for wind resistance | Limits future opening locations; may conflict with drive-through bay requirements (24 ft openings) | Compatible with tilt-up panel wall system (§4.1); may be the default choice if tilt-up is selected |
| Steel braced frames | Allows larger openings; lighter structural members; can be combined with concrete walls | Requires separate lateral system from wall system; connections must be designed for seismic; may conflict with crane runway clearances | More likely if a hybrid (concrete walls + steel roof) system is selected |
| Moment frames (steel or concrete) | Maximum architectural flexibility; no diagonal bracing members | Heavier, more expensive connections; larger column sizes; may require deep foundations | Typically used where shear walls/bracing cannot be accommodated; less common for this building type |

**Key considerations for this project:**

- The two drive-through repair bays (24 ft wide openings on opposite walls) reduce the available shear wall length on the east and west elevations.
- The 35 ft height-to-width ratio creates significant overturning demands under wind or seismic loads.
- Seismic design parameters are TBD (see Datasheet §3, F-001) but Alberta generally has low-to-moderate seismic hazard.
- The selected lateral system must be compatible with the crane runway support system (§4.4) and not interfere with crane operation.

**Source:** ASSUMPTION — standard structural engineering practice for lateral system selection; no specific lateral system is prescribed in the RFP or App B (Shop). Wind and seismic design requirements are governed by NBC (edition TBD, A-001) and are a fundamental design input for a 35 ft structure.

### 4.4 Crane Runway Structural System

| Option | Notes |
|---|---|
| Runway beams on corbels (wall-mounted) | Common in tilt-up concrete buildings; efficient but restricts wall penetrations |
| Freestanding runway columns | Independent of wall system; more flexible but additional floor area consumed |
| Combined column-runway bracket | Integral approach common in industrial pre-engineered buildings |

**Source:** ASSUMPTION — standard industrial crane runway design options; Structural Engineer to select and present at preliminary stage.

---

### 4.5 Schedule and Cost Implications of Preliminary Design Decisions (C-004)

Structural system decisions made at the preliminary design stage have significant downstream effects on project schedule and construction cost. The following considerations are relevant for the Owner's approval decision:

| Decision | Schedule Impact | Cost Impact |
|---|---|---|
| Wall system selection (tilt-up vs. precast vs. cast-in-place) | Tilt-up panels require favorable weather for erection (typically May–September in Alberta); precast requires factory lead time (ASSUMPTION: 8–12 weeks typical — location TBD); cast-in-place requires extensive formwork time | Tilt-up is generally most cost-effective for large footprint buildings; precast has higher unit cost but faster erection; cast-in-place is most expensive for this building type (ASSUMPTION) |
| Foundation type (dependent on geotech results) | Spread footings: standard construction timeline; deep foundations: additional mobilization and time | Spread footings: lower cost; piles: significant cost increase; this is the variable-price scope element (RFP §4.8.2) |
| Crane runway type | Runway on wall corbels minimizes secondary structure; freestanding columns require additional foundations | Wall-mounted runway is typically lower cost if wall system supports it; freestanding columns add cost |
| Lateral system | Shear walls require no additional structural members beyond the wall system; braced frames or moment frames add structural steel elements | Shear walls (if using tilt-up) have minimal incremental cost; braced frames and moment frames add cost |

> **Note (C-004):** These schedule and cost relationships are ASSUMPTION-level observations based on standard industry practice. Specific cost and schedule values should be developed by the Design-Builder's project management team. This information is provided to support the Owner's understanding of the implications of approving a particular structural approach at the preliminary stage.

**Source:** ASSUMPTION — standard construction industry practice for Alberta industrial buildings. RFP §4.8.2 (variable-price foundation). No specific cost or schedule data is available in accessible sources.

### 4.6 Success Criteria for the Preliminary Design (D-003)

Beyond the formal success criterion of County approval (REQ-001), the following indicators may be used to assess whether the preliminary design effectively serves its purpose:

| Criterion | Indicator | Assessment Basis |
|---|---|---|
| Design direction stability | No major structural system redesign required at final design stage (DEL-002-02 through DEL-002-12) | ASSUMPTION — a successful preliminary design should establish a stable baseline |
| TBD reduction | All TBDs identified in the preliminary design have either been resolved or have a clear resolution pathway by the time final design begins | Tracked via Conflict Table and open items list |
| Inter-discipline alignment | No unresolved structural coordination issues with other disciplines at time of County submission | Tracked via coordination log (Procedure Step 5) |
| Owner comprehension | County approval obtained without requiring major re-presentation or fundamental questions about the structural approach | ASSUMPTION — indicates that the presentation effectively communicated the structural concept |
| Downstream seeding quality | Final design deliverables (DEL-002-02 through DEL-002-12) can proceed without revisiting fundamental structural decisions from the preliminary design | ASSUMPTION — assessed retrospectively; Guidance §2.4 discusses downstream seeding |

> **Note (D-003):** These success criteria are ASSUMPTION-level proposals. They are not requirements from the RFP or accessible sources but are suggested as a framework for appraising the effectiveness of the preliminary design beyond the binary County approval gate.

**Source:** Decomposition §7 PKG-002 (downstream deliverables); RFP §3.3.2 (County approval); Guidance §2.4 (downstream seeding). ASSUMPTION: success criteria framework inferred from standard design-build practice.

---

## 5. Examples

No project-specific examples are available in accessible sources. Examples of similar industrial concrete buildings with overhead crane runways and service pits exist widely in Alberta industry practice, but no specific precedents are cited in the RFP or Appendix B.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CON-001 | App B (Shop) notes refer to "Overhead Mezzanine over Parts Room/Utility Room/Wash Bay" which is consistent with RFP §3.4 ("above utility and parts room"). However, the decomposition (SOW-0033) refers to "above parts room, utility room, and wash bay" while the App B legend note reads "Load Bearing Over Parts Room + Utility For Storage." It is unclear whether the wash bay portion of the mezzanine is also intended to be load-bearing for storage. | App B (Shop) legend note: "Load Bearing Over Parts Room + Utility For Storage" | RFP §3.4: "Mezzanine storage above utility and parts room capable of handling heavy items"; SOW-0032: "above parts room, utility room, and wash bay"; SOW-0033 same | Datasheet §2.1, Specification REQ-007, Guidance §3.3, Procedure §4 | PROPOSAL: Apply load-bearing requirement to all three mezzanine areas (parts room, utility room, wash bay) as a conservative default, pending human ruling. Note in design that the wash bay portion may be lower load if confirmed by County. | TBD |
| CON-002 | The RFP §3.4 states "Concrete structure 35' ceiling." App B (Shop) notes confirm "Concrete Structure (35' Ceiling)." The decomposition references this for the New North Shop (SOW-0012, SOW-0022). However, it is not explicit whether "concrete structure" refers only to the wall/column system, the floor slab, or the roof system as well. Different structural interpretations are possible. | RFP §3.4: "Concrete structure 35' ceiling" | No additional clarifying text in accessible sources | Datasheet §4, Specification REQ-002, Guidance §3.1 | PROPOSAL: Interpret as primary structural system in concrete (walls/columns and floor slab); roof structure material (concrete, steel, hybrid) to be proposed by Structural Engineer and presented at preliminary design stage for County confirmation. | TBD |

### CON-002 Rationale and Downstream Consequences (E-002)

The ambiguity in "concrete structure" matters for the preliminary design because each interpretation leads to fundamentally different structural systems, construction methods, and costs:

| Interpretation | Structural Implication | Construction Implication | Cost Implication |
|---|---|---|---|
| **Walls/columns only in concrete; steel roof** | Hybrid system: concrete tilt-up or precast walls with steel joist/beam/girder roof framing. Common in Alberta industrial buildings of this scale. | Allows independent erection of concrete walls and steel roof; roof steel can be designed to standard open-web steel joist spans | ASSUMPTION: typically lower roof cost; allows longer spans with lighter members |
| **Walls/columns and floor slab in concrete; steel roof** | Same as above, plus concrete floor slab (which is already expected given the steel plate embedments, REQ-006) | No additional construction impact beyond walls-only interpretation for roof | Similar to above |
| **Entire structure in concrete (walls, roof, floor)** | All-concrete system: precast double-tee or hollow core roof deck, or cast-in-place concrete roof. Significantly heavier structure. | Requires substantially heavier crane and formwork for roof; heavier foundation loads | ASSUMPTION: significantly more expensive for a 100 ft × 130 ft building; unusual for this building type in Alberta |

The proposed interpretation (PROPOSAL in CON-002) is that "concrete structure" refers to the primary vertical system (walls and columns) and the floor slab, with the roof material open for the Structural Engineer's recommendation. This interpretation is consistent with standard Alberta industrial building practice where tilt-up concrete walls with steel roof framing is the predominant system type. However, the County may have intended an all-concrete building, and this should be clarified at the preliminary design review.

**Source:** RFP §3.4, App B (Shop), SOW-0012, SOW-0022. ASSUMPTION: interpretation analysis based on standard structural engineering practice; no clarification available in accessible sources.
