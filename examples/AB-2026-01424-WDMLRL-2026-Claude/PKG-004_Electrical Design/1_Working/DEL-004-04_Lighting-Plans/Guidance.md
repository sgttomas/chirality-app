# Guidance — DEL-004-04 Lighting Plans

---

## Purpose

DEL-004-04 Lighting Plans exists to provide the construction team (and the Owner) with engineered, IFC-quality documentation of the lighting system for the New North Shop addition at the West Dried Meat Lake Regional Landfill Maintenance Shop. The lighting plan set translates the conceptual layout shown in Appendix B (Electrical) of the RFP into a stamped engineering drawing set from which the electrical contractor (PKG-015) can install the system.

The drawing set is a key component of OBJ-003 (produce complete, P.Eng.-stamped IFC documentation across all disciplines) and OBJ-005 (install and commission all electrical and low-voltage systems to operational readiness). It is also a prerequisite for obtaining electrical Safety Code permits (DEL-009-03) and for the electrical contractor's pricing and installation work.

Source: Decomposition §5 (OBJ-001, OBJ-003, OBJ-005); RFP §3.3.2; App B-Elec.

---

## Principles

### P-1: Derive Layout from Conceptual Drawing, Not From Scratch

Appendix B (Electrical) provides a specific layout for all lighting zones — fixture counts, row/column arrangement, and zone assignments are defined. The Electrical Engineer's job is to engineer and document that layout (verify compliance, specify products, confirm circuits), not to redesign it without cause. Deviations from the conceptual layout require Owner coordination.

Source: App B-Elec (Electrical Notes and Layout); RFP §3.3.2.

### P-2: LED Technology Is Specified for All Zones

The high bay fixtures in the main shop are explicitly specified as LED (150W, 22,000 lumens). The 8-foot fixtures in the office, utility room, and parts/tool room are described as "8' LED." The Electrical Engineer should treat LED as the specified technology for all interior zones and select compliant products accordingly.

Source: App B-Elec (Electrical Notes).

### P-3: High Bay Photometric Performance Drives Layout Validity

At 35-foot ceiling height and 150W/22,000-lumen output per fixture, the Electrical Engineer should verify that the 5×4 main shop layout achieves adequate illuminance for a heavy equipment maintenance environment. If photometric calculations are required for code compliance or Safety Code permit, this should be coordinated with DEL-004-08 (Electrical Calculation Package).

ASSUMPTION: Illuminance targets for Alberta industrial occupancies are governed by applicable codes/standards; specific lux/footcandle targets are TBD pending code research by the Electrical Engineer.

### P-4: Service Pit Lighting Detail Is Unresolved at Conceptual Stage

The RFP (§3.4) requires the service pit to be "ventilated and lighted," and the App B-Elec layout shows an "L" symbol at the Service Pit area. However, the conceptual drawing does not specify fixture type, count, wattage, or mounting method for the service pit. The Electrical Engineer must resolve this detail and document it in the drawing set.

ASSUMPTION: Given the below-grade, industrial-maintenance environment of a service pit, fixtures suitable for wet/damp locations and robust against physical impact (ASSUMPTION: appropriate enclosure rating per CEC) will be required. Specific product selection TBD.

**Wet/Damp Location Fixture Knowledge Note [B-004]:** For both the wash bay (wet environment from equipment washing) and service pit (below-grade, potentially damp or wet), applicable CEC or Alberta code provisions govern the minimum enclosure rating (e.g., IP rating, "suitable for wet locations" or "suitable for damp locations" per CEC definitions). The Electrical Engineer should research and document the specific code basis for enclosure rating requirements in these zones. Current references to wet/damp location requirements in this deliverable are ASSUMPTIONS not yet supported by specific code citations. This knowledge gap should be resolved during code research (see Procedure Step 1.3).

### P-5: Wash Bay Lighting Specification Is Partially Defined

The RFP specifies "2 Rows of 3 High Bay Lights" for the wash bay (6 fixtures), but does not state wattage or lumen output for wash bay fixtures in the source text. The Electrical Engineer should determine appropriate wash bay fixture specifications. Given the wash bay is a wet environment (equipment washing), fixture IP/wet-location rating is a design consideration.

ASSUMPTION: Wash bay fixtures require wet-location or wash-down rating; specific specifications TBD.

### P-6: Coordination with Mechanical Is Required

The main shop has 6 ceiling fans (SOW-0040; DEL-013-06) and exhaust fans (SOW-0066; DEL-015-04 for power; App B-Elec shows "E" symbol). Ceiling fan and exhaust fan locations relative to high bay fixture rows must be coordinated to avoid conflicts and to confirm switch/circuit groupings. This coordination occurs between PKG-004 (Electrical Design) and PKG-003 (Mechanical Design).

Source: App B-Elec (layout symbols); SOW-0040; SOW-0066.

### Terminology Note [E-002]

**Canonical fixture terminology** for cross-document consistency:

| Fixture Category | Canonical Term | Variants Found (normalize to canonical) |
|---|---|---|
| Main shop / wash bay ceiling fixtures | **High Bay LED** | "high bay", "High Bay LED fixture" |
| Office / utility / parts-tool room linear fixtures | **8-foot LED strip** | "8' LED", "8-foot LED fixture", "8-foot LED strip fixture" |

All production documents (Datasheet, Specification, Guidance, Procedure) should use the canonical terms above. Where source documents (App B-Elec, RFP) use variant terminology, the canonical term should be used in the production documents and the source variant noted where relevant. This normalization reduces confusion in fixture schedule preparation and procurement.

---

## Considerations

### C-1: Fixture Mounting at 35-Foot Ceiling Height

Mounting high bay fixtures at 35 feet introduces practical considerations for the drawing: pendant length, mounting method (chain, rigid stem, cable), and whether fixtures are shown on a reflected ceiling plan or on the plan-view electrical drawing. ASSUMPTION: For an industrial shop at this ceiling height, chain or rigid-stem pendant mount is typical; coordination with the structural drawings (DEL-002) for mounting points may be required if fixtures are attached to the structure above.

### C-2: Circuit Grouping and Switching

The lighting plan should show circuit designations for each zone's fixtures. For a maintenance shop, zone-based switching (main shop bays separately switched, wash bay independently switched, office and utility/parts room on separate circuits) is a reasonable approach. ASSUMPTION: Specific switching layout TBD pending Owner input through the preliminary design approval process (DEL-004-01).

**Switching Scheme Design Rationale [X-002]:** The switching scheme should be designed considering:
- **Zone-based control:** Each functional zone (main shop, wash bay, office, utility, parts/tool room) should be independently switchable to allow selective lighting during different operational modes (e.g., after-hours access to office only, wash bay operation independent of main shop).
- **Energy management:** For a 13,000 sq ft shop with 20 high bay fixtures at 150W each (3,000W total for main shop alone), the ability to light partial zones reduces energy consumption during low-occupancy periods. Consider whether row-by-row switching within the main shop is warranted.
- **Owner input required:** The Owner's operational preferences for switching (e.g., single-switch full-shop lighting vs. zone control) should be confirmed during the preliminary design approval process (DEL-004-01). ASSUMPTION: zone-based switching is the baseline approach pending Owner direction.

### C-3: Emergency Lighting and Exit Lighting

The RFP and conceptual drawing do not explicitly specify emergency lighting or exit lighting. However, for a building of this occupancy and size in Alberta, emergency and exit lighting requirements may be imposed by the Alberta Building Code or applicable Safety Codes.

ASSUMPTION: Emergency and exit lighting requirements should be assessed by the Electrical Engineer during design. If required, they would appear on the Lighting Plans. This is flagged as a potential addition to scope not explicitly stated in the conceptual source.

### C-4: Scope Boundary with PKG-015

The Lighting Plans drawing set is a design deliverable (PKG-004). The actual installation of the lighting system is DEL-015-02 (Lighting Installation, PKG-015). The Lighting Plans must be complete and IFC-stamped before the electrical contractor can commence lighting installation work.

Source: Decomposition §7 PKG-015; RFP §3.3.2.

### C-5: Relationship to Preliminary Design Approval

The conceptual layout in App B-Elec represents the Owner's program intent. The preliminary electrical design (DEL-004-01) must be approved by the County before final Lighting Plans (this deliverable) are issued for construction. Changes to lighting layout that arise during preliminary design approval must be tracked and documented.

Source: RFP §3.3.2; SOW-0010d.

---

## Trade-offs

### T-1: Conceptual Fixture Count vs. Photometric Verification

The Owner has specified fixture counts (5×4 main shop, 2×3 wash bay). If photometric analysis at preliminary design stage shows that the layout does not meet code-minimum illuminance, the Electrical Engineer faces a trade-off between adhering to the Owner-specified layout and meeting code. This should be raised with the Owner during the preliminary design review (DEL-004-01), not silently resolved.

### T-2: Fixture Selection Value Trade-offs [F-004]

When specifying fixture products (particularly for high bay fixtures at 35-foot ceiling height), the Electrical Engineer faces value trade-offs that affect both capital cost and long-term operational cost:

- **Energy efficiency:** Higher-efficacy LED fixtures (lumens per watt) reduce operational energy cost but may carry higher initial cost. For 20+ high bay fixtures operating in a maintenance environment with expected long daily run hours, energy cost is a significant lifecycle factor.
- **Maintenance access at 35-foot ceiling:** Fixture replacement and maintenance at 35 feet requires specialized access equipment (man-lift, scaffolding). Fixtures with longer rated lifetimes (e.g., 100,000+ hour L70 rating) reduce maintenance frequency and associated costs. This is a significant practical consideration for an industrial facility.
- **Lifecycle cost vs. capital cost:** The Owner's value priorities regarding capital cost sensitivity vs. lifecycle cost optimization should be confirmed during preliminary design review. ASSUMPTION: lifecycle cost is a relevant consideration but the Owner's weighting of capital vs. operating cost has not been stated in source documents.
- **Enclosure rating (wash bay and service pit):** Wet/damp-rated fixtures carry a cost premium. The minimum enclosure rating is driven by code (TBD -- see Principles P-4 and P-5), but higher ratings may be warranted depending on the actual wash bay operating conditions.

Source: ASSUMPTION -- trade-off framework inferred from deliverable type and building characteristics. No source document states Owner value priorities for fixture selection.

### T-3: Level of Detail on Lighting Plans

For a Design-Build project at IFC stage, the Lighting Plans may combine lighting layout with circuit identification on a single drawing, or may produce separate drawings (layout plan + fixture schedule + circuit plan). The appropriate level of detail should be confirmed during preliminary design and documented in the drawing set organization.

ASSUMPTION: At minimum, IFC-quality plans include: fixture symbols with quantity, circuit designation, fixture schedule, and switching notes. Additional detail (mounting heights, photometric overlay) may be added at engineer's discretion.

---

## Examples

Examples of lighting layout organization similar to what this deliverable should produce are not available in accessible source documents.

The conceptual layout in Appendix B (Electrical) serves as the closest available reference: it shows "L" symbols placed on a floor plan in rows/columns per zone, with the Electrical Notes list providing fixture counts and specifications. The final Lighting Plans drawing set should use standard electrical drawing conventions (e.g., CSA/IEEE symbols, or as required by the Safety Code authority) rather than the simplified conceptual notation.

Source: App B-Elec (reference only — conceptual, not IFC quality).

---

## Conflict Table (for human ruling)

### Conflict Resolution Prioritization [D-003]

The following conflicts require human resolution. Proposed prioritization and resolution milestones:

| Priority | Conflict ID | Resolution Milestone | Rationale |
|---|---|---|---|
| 1 (highest) | CONF-LT-003 | Before preliminary design submission (DEL-004-01) | Emergency/exit lighting applicability determines whether additional fixtures must be designed and shown on plans; late discovery could require redesign. Code research should be completed early. |
| 2 | CONF-LT-001 | At or before preliminary design review | Wash bay fixture specifications affect fixture schedule, photometric calculations, and procurement. Resolution before County approval avoids rework. |
| 3 | CONF-LT-002 | At or before preliminary design review | Service pit fixture selection requires environmental assessment (wet/damp, impact) and product research. Can proceed in parallel with CONF-LT-001. |

ASSUMPTION: Prioritization is based on the risk of downstream rework if each conflict is resolved late. The Project Manager / Owner should confirm or adjust the proposed resolution milestones.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-LT-001 | Wash bay fixture specifications (wattage/lumens) not stated. Main shop high bays are 150W/22,000lm; wash bay only states "2 Rows of 3 High Bay Lights" with no wattage or lumen specification. | App B-Elec Electrical Notes (main shop: 150W LED 22,000 lm; wash bay: silent on wattage) | RFP §3.4 (silent on wash bay lighting detail) | REQ-LT-002; Datasheet Attributes; Fixture Schedule | PROPOSAL: Electrical Engineer to specify wash bay fixtures based on photometric need for the wash bay environment; confirm with Owner at preliminary design review | TBD |
| CONF-LT-002 | Service pit lighting fixture type and count not specified in any accessible source beyond a generic "lighted" requirement and an "L" symbol on the conceptual drawing. | RFP §3.4 ("Ventilated and lighted service pit area") | App B-Elec (shows "L" near Service Pit — no count or type specified) | REQ-LT-006; Datasheet Attributes | PROPOSAL: Electrical Engineer to specify service pit lighting; wet/damp-location fixtures assumed; confirm count and type at preliminary design review | TBD |
| CONF-LT-003 | Emergency and exit lighting not mentioned in RFP or conceptual drawings but may be required by Alberta Building Code for this occupancy type. | App B-Elec (no emergency lighting shown) | Alberta Building Code (location TBD — not in accessible sources) | REQ-LT-008; Specification Standards | PROPOSAL: Electrical Engineer to determine applicability during code review; add to Lighting Plans if required | TBD |
