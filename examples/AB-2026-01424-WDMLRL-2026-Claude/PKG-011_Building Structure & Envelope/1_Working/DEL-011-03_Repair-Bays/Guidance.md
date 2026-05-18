# Guidance — DEL-011-03 Drive-Through Repair Bays

**Document Type:** Guidance (Directional)
**Deliverable ID:** DEL-011-03
**Deliverable Name:** Drive-Through Repair Bays
**Package:** PKG-011 — Building Structure & Envelope
**Revision:** R1 — 2026-02-26 (Pass 3 enrichment)
**Status:** SEMANTIC_READY

---

## Purpose

DEL-011-03 exists to deliver the two drive-through repair bays that are the primary operational workspace of the New North Shop addition. The repair bays are where County maintenance staff will service heavy landfill equipment -- tracked machines, packers, motor scrapers, and similar large vehicles. These bays define the core functional intent of the new building.

The bays must be large enough, strong enough, and sufficiently serviced (drainage, exhaust, crane access, overhead door clearance) to support full-cycle heavy equipment maintenance. Getting these spaces right is the single most important outcome of PKG-011.

**Source:** RFP S3.1 (building program); RFP S3.4 (design requirements list); Decomposition OBJ-001.

---

## Principles

### 1. Size for the largest equipment, not the average -- and consider future growth

The RFP explicitly references motor scrapers as a sizing benchmark (RFP S3.3.2 -- driving surface; RFP S3.4 -- steel plates for tracked/packer equipment). A motor scraper is one of the largest pieces of construction equipment in landfill operations -- typically 10-14 metres long and 3.5-5 metres wide. Bay widths (nominally 24'), door heights, and door widths must be set in IFC drawings to ensure these machines can enter, be positioned, and exit without interference.

ASSUMPTION: Door height should allow clearance for raised attachments (blades, bowls) typical of motor scraper class machines. The human/design team should confirm the specific vehicle envelope at IFC design stage.

**Future equipment growth consideration (Lensing E-001):** This building is a long-life infrastructure asset expected to serve the County for decades. The current sizing is based on motor scraper class equipment. The design team should consider whether the 24' nominal bay width and door dimensions provide any margin for potential future equipment size increases. If the County's fleet planning anticipates larger equipment classes in future, that growth margin should be factored into IFC dimension decisions now, as bay width and door openings are effectively fixed once constructed. ASSUMPTION: current sizing is for present fleet; growth margin TBD pending County operations/fleet planning input.

### 2. Drive-through is an operational requirement, not a preference

The drive-through configuration (door at each end of each bay) means vehicles can pull straight through rather than reversing in or out. For large heavy equipment, reversing in a maintenance bay is a safety risk. The RFP states the building "shall have separate entrance/exit doors" (S3.1). The two repair bays shown on Appendix B are the primary embodiment of this requirement.

The drive-through configuration also reduces floor space consumed by maneuvering and keeps traffic flow through the shop predictable.

### 3. Repair bays are a structural dependency hub

The repair bays are not structurally independent -- they depend on:
- DEL-011-01 (Superstructure) for the concrete frame, columns, beams, and roof that enclose the bays
- DEL-011-02 (Steel Embedments) for the floor plates that protect the concrete slab from tracked equipment damage
- DEL-014-04 (Sump Drains) for floor drainage to capture fluids from equipment servicing
- DEL-013-04 (Exhaust System) for capture of diesel/exhaust fumes from running equipment inside
- DEL-015-04 (Equipment Power) for overhead door operators and general power
- DEL-016-01 (Overhead Cranes) for lifting equipment components during repair

Sequencing and coordination errors in any of these packages directly affect repair bay functionality. The General Contractor must manage these interfaces actively.

**Source:** _DEPENDENCIES.md; Decomposition PKG-011, PKG-013, PKG-014, PKG-015, PKG-016 entries.

### 4. The conceptual drawing is a program document, not a construction drawing

Appendix B (Shop) is a conceptual floor plan provided for bidding purposes. Dimensions on Appendix B (bay widths of 24', overall building 130' x 100', etc.) are programming intents, not IFC dimensions. The Structural Engineer and Architect must translate these into IFC drawings that account for column locations, wall thickness, door frame construction, and structural clearances.

ASSUMPTION: Final bay clear dimensions will be slightly smaller than 24' nominal once wall thickness and column allowances are applied. The design team should confirm that clear openings remain adequate for the intended equipment.

**Bay width dimension clarification needed (Lensing B-002):** The 24' dimension appears in multiple contexts across the document set. The IFC drawings must establish a single authoritative definition of the 24' dimension and explicitly distinguish nominal bay width from clear opening width. See Datasheet Normalization Note and Specification REQ-011-03-002 Note.

---

## Considerations

### Overhead Door Selection

Door type, size, and hardware are TBD in IFC drawings. The following considerations should inform selection:
- **Height:** Must accommodate the tallest equipment with attachments raised. ASSUMPTION: Minimum 14-16 feet clear height is likely needed for motor scraper class; confirm with equipment fleet dimensions. Location TBD in IFC documents.
- **Width:** Clear width should match or slightly exceed nominal 24' bay width. ASSUMPTION: 22'-24' clear width likely; confirm in IFC.
- **Type:** Industrial sectional or rolling steel overhead doors are standard for heavy-use industrial bays. High-cycle operators may be warranted given frequency of use. ASSUMPTION: operator type TBD.
- **Power:** Overhead door operators require electrical power circuits (SOW-0060, PKG-015). Coordinate door selection with PKG-015 electrical contractor for circuit sizing.
- **Insulation and R-value selection (Lensing A-005):** Given Alberta cold climate, insulated door panels are strongly advisable for energy performance. The design team should establish R-value selection criteria informed by Alberta climate zone data and energy modelling of the heated bay. Relevant factors include: expected heat loss through four large door openings at 35' ceiling height, cost-benefit of higher R-value panels versus heating system capacity (high-recovery heating, DEL-013-01), and any applicable Alberta energy code minimums for building envelope components. ASSUMPTION: insulated doors appropriate; specific R-value selection criteria TBD pending design team and energy modelling input.
- **Wind load:** Doors at the perimeter of the building are exposed to Alberta wind loads. Structural framing and door specifications must address this. TBD in IFC structural drawings.
- **Safety devices (Lensing A-002):** Motorised industrial overhead doors require obstruction sensors and auto-reverse mechanisms. This is now captured as a normative requirement (REQ-011-03-015) per safety code expectations for motorised industrial doors.
- **Weather seals (Lensing C-002):** Head, jamb, and floor seals are anticipated for a heated bay in Alberta climate. This is now captured as a normative requirement (REQ-011-03-016).
- **Lifecycle and maintenance access (Lensing C-003):** Overhead doors in heavy industrial use require periodic maintenance including torsion spring replacement, operator servicing, and track adjustment. At 35' ceiling height, spring and operator access may require specialized equipment (e.g., man lifts, scaffolding). The design team should consider: frequency of servicing for heavy-cycle industrial doors, ease of component replacement at height, access provisions for torsion spring maintenance at the top of a 14-16' door opening, and whether door type selection (sectional versus rolling) affects maintenance accessibility. This consideration should inform the door type trade-off decision. ASSUMPTION: lifecycle maintenance access is a relevant door selection factor; specific maintenance requirements TBD per manufacturer.

### Floor Drainage in Repair Bays

Sump drains are required in the repair bays (RFP S3.4; SOW-0045). The concrete floor design must include:
- Appropriate slope toward sump drain locations (ASSUMPTION: 1-2% slope typical for industrial shop floors; confirm with Structural/Civil Engineer). Measurable acceptance criteria for floor drainage slope (percentage, direction, and ponding test requirements) must be defined in IFC drawings (see REQ-011-03-007). (Lensing D-001)
- Sump pit sizing adequate for fluid volumes expected from large equipment service operations
- Coordination between DEL-011-03 structural rough-in and DEL-014-04 plumbing installation

The drain design should consider that the repair bays service equipment containing hydraulic fluid, diesel, coolant, and oil. Drain capacity and holding provisions should be sized accordingly. ASSUMPTION: An oil/water separator may be required by Alberta environmental regulations for repair bay floor drainage; this is TBD and should be confirmed with the design team and applicable regulatory authority (Alberta Environment and Protected Areas). If required, the separator must be designed before concrete is poured, as it affects sump drain design (DEL-014-04 interface) and potentially structural slab provisions (this deliverable). (Lensing C-001)

### Floor Slab Flatness (Lensing D-003)

Heavy tracked equipment operation on the repair bay floor requires adequate floor flatness and levelness. The structural engineer should assess whether a floor flatness classification (e.g., FF/FL numbers per ACI 117 or equivalent CSA standard) is appropriate for the repair bay areas, given that heavy tracked equipment operation on an excessively uneven floor could cause structural damage or operational issues. ASSUMPTION: floor flatness criterion may be applicable; specific standard and class TBD pending structural engineer assessment.

### Exhaust Provisions

The RFP requires exhaust hoses and fans for heavy equipment in the repair bays (S3.4; SOW-0038). These are typically drop-hose systems connected to ceiling-mounted fans or a central exhaust plenum. Structural provisions to consider:
- Overhead attachment points for hose reels or fixed hose drops (ASSUMPTION: ceiling-mounted; coordinate with DEL-013-04 mechanical scope)
- Penetrations through roof or walls for exhaust discharge
- Ensure exhaust provisions do not conflict with overhead crane runway beams (DEL-016-01 crane structural supports -- DEL-002-07)
- A coordination hold point between DEL-011-03 structural provisions and DEL-013-04 mechanical installation is required to confirm that provisions are correctly located before the mechanical contractor begins work. Without this hold point, structural provisions could be missed until mechanical rough-in begins. (Lensing X-002)

### Overhead Crane Interface

Two 5-tonne overhead cranes on trolley serve the main shop area (SOW-0067; Appendix B -- "5 TON CRANE" labels). The crane runway beams are integral to the building structure and are part of DEL-011-01 (Superstructure) / DEL-002-07 (Crane Support Details). The repair bay design must:
- Confirm that crane coverage extends into the repair bay area (Appendix B shows crane columns positioned between the two bays in the main shop area -- coverage over both bays is an open question flagged in the Conflict Table)
- Ensure that door height and bay height are consistent with the crane rail elevation and hook height requirements
- Avoid conflicts between overhead door operation and crane travel

ASSUMPTION: The cranes are intended to be usable within the repair bays for lifting engine components, axles, and similar heavy parts. The structural engineer must confirm crane coverage and clearances.

### Steel Plate Embedments in Bay Floor

Steel plates embedded in the concrete floor (DEL-011-02, SOW-0024) are located at "strategic locations" per Appendix B. These plates protect the concrete from damage by tracked and packer-type equipment. The repair bay floor will likely include steel plates at:
- Positions where tracked equipment (excavators, dozers) would park with tracks on the floor
- Entry/exit paths of heavy tracked machines

The exact plate layout is defined in DEL-002-08 (Embedment Plan, structural design scope). DEL-011-03 construction must confirm embedment locations are consistent with repair bay door positions and operational equipment parking positions.

### Fire Separation (Lensing F-002)

The design team should assess whether fire separation requirements apply between the repair bays and adjacent spaces (parts room, wash bay, storage areas). Repair bays involve potential exposure to flammable fluids (hydraulic oil, diesel fuel, coolant) during equipment servicing. Fire separation between an industrial repair bay and adjacent occupied/storage spaces is a standard building code consideration. The applicable Alberta Building Code / Fire Code requirements should be identified during IFC development. ASSUMPTION: fire separation requirements may apply; specific requirements TBD per design team and Alberta Building Code/Fire Code assessment.

### Construction Sequencing

ASSUMPTION: The following sequence applies (typical heavy industrial construction):
1. Foundation complete (DEL-010-01) -- prerequisite
2. Concrete superstructure erected (DEL-011-01) -- prerequisite
3. Steel plate embedments placed concurrent with or following floor pour (DEL-011-02) -- prerequisite or concurrent
4. Overhead door frames and structural rough openings constructed (this deliverable, DEL-011-03) -- depends on superstructure
5. Roofing and building envelope closure (DEL-011-01 / envelope scope)
6. MEP rough-in (PKG-013, PKG-014, PKG-015) -- follows structural enclosure; coordination hold points required at exhaust provisions (REQ-011-03-008) and sump drain provisions (REQ-011-03-007)
7. Overhead crane installation (DEL-016-01) -- typically after structural and electrical rough-in

Delays to the superstructure directly cascade to DEL-011-03 and all downstream MEP packages. The project schedule must reflect this dependency chain and protect the December 31, 2026 completion deadline.

**Door procurement lead time (Lensing D-002):** Industrial overhead doors typically have 8-16 week lead times (ASSUMPTION). The General Contractor must initiate procurement sufficiently in advance of the scheduled installation date to avoid schedule impact. Given the December 31, 2026 deadline, procurement should be anchored to a specific project schedule milestone. See Procedure Step 1.3.

---

## Trade-offs

| Trade-off | Options | Recommended Direction | Source/Basis |
|---|---|---|---|
| Door height vs. heating efficiency | Taller doors allow larger equipment but increase heat loss in cold climate; shorter doors reduce equipment access | Prioritise equipment clearance -- size doors for worst-case equipment with attachments raised; compensate with insulated doors (with R-value selected per energy modelling) and high-recovery heating | RFP S3.4 (equipment requirements and heating requirement both stated); Lensing A-005 |
| Sump drain sizing | Larger sumps provide more holding capacity but cost more and require more structural depth; oil/water separator may add complexity | Size for heavy equipment fluid volumes; confirm with plumbing engineer -- do not undersize; confirm oil/water separator requirement with Alberta Environment and Protected Areas (Lensing C-001) | RFP S3.4; SOW-0045 |
| Sectional vs. rolling overhead doors | Sectional doors are common, allow partial opening, generally easier maintenance access; rolling steel doors save headroom but may be harder to service at height | TBD in IFC -- both are acceptable industrial products; headroom is less of a constraint at 35' ceiling height; maintenance accessibility at height is a factor favoring sectional doors (Lensing C-003) | ASSUMPTION |
| Steel plate layout in bay floor | More plates = better protection but higher cost | Coordinate with Structural Engineer (DEL-002-08) -- plates should cover tracked equipment paths; minimum required by RFP at "strategic locations" | RFP S3.4; Appendix B |
| Current fleet sizing vs. future growth margin | Size strictly for current motor scraper class vs. add margin for potential future larger equipment | TBD -- County operations/fleet planning should advise; construction cost of wider bays/taller doors is incremental vs. cost of future retrofit; long-life asset favors growth margin where feasible (Lensing E-001) | ASSUMPTION |

---

## Examples

No construction examples are available from the accessible source documents. Design and construction team should reference comparable heavy equipment maintenance facilities in Alberta for bay sizing, door selection, and drainage system configuration.

ASSUMPTION: Alberta landfill operations and municipal maintenance shops are the most relevant analogue facility type.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|---|---|---|---|---|---|---|
| CT-001 | Crane coverage over repair bays: Appendix B labels show "5 TON CRANE" columns positioned in the main shop area between the bays. It is not fully clear from the conceptual drawing whether crane travel covers both repair bays fully or only one bay. Specification REQ-011-03-005 addresses equipment accommodation but does not include crane access as a repair bay requirement. | Appendix B (Shop) -- "5 TON CRANE" column positions between bays | Specification REQ-011-03-005 (silent on crane coverage over bays) | Specification REQ-011-03-005; Guidance Overhead Crane Interface consideration; DEL-016-01; DEL-002-07 | IFC structural/crane drawings (DEL-002-07) should confirm coverage -- PROPOSAL: crane coverage should extend over both repair bays (Lensing X-001) | TBD |
| CT-002 | Oil/water separator requirement for repair bay floor drainage: Guidance flags this as TBD but no requirement or exclusion is recorded in Specification. If required by Alberta environmental regulations, it would affect sump drain design (DEL-014-04 interface) and potentially structural slab provisions (this deliverable). Must be determined before concrete is poured. | Guidance Considerations > Floor Drainage (flags regulatory question) | Specification REQ-011-03-007 (silent on separator requirement) | Specification REQ-011-03-007; Procedure Step 2.3; DEL-014-04 interface | Alberta Environment and Protected Areas regulatory authority; design team -- PROPOSAL: confirm requirement early in design phase before slab pour (Lensing C-001) | TBD |
| CT-003 | Bay width dimension definition: 24' appears as nominal, structural, and clear dimension in different contexts across the document set. The authoritative definition (nominal vs. clear) must be established. | Appendix B (24' plan annotation) | Specification REQ-011-03-002 ("nominally 24 feet wide") | Datasheet Attributes; Specification REQ-011-03-002; Guidance Principles S4 | IFC drawings -- PROPOSAL: IFC must define nominal vs. clear bay width explicitly (Lensing B-002) | TBD |
