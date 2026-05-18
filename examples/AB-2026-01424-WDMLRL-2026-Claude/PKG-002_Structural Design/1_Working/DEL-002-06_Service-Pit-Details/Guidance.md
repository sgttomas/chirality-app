# Guidance — DEL-002-06: Service Pit / Trench Structural Details

---

## Purpose

DEL-002-06 exists because the West Dried Meat Lake Regional Landfill Maintenance Shop Addition requires a below-grade service pit allowing mechanics to access the underside of heavy landfill equipment (tracked and packer machines, motor scrapers) at floor level without requiring a vehicle hoist. The RFP explicitly mandates this feature: "Ventilated and lighted service pit area for mechanics to perform servicing under equipment" (RFP §3.4, SOW-0028).

The structural drawing set produced under this deliverable translates the Owner's operational intent (expressed conceptually in Appendix B and RFP §3.4) into an engineered, code-compliant, constructable structural design. The drawings are the primary reference document for the General Contractor (PKG-011) constructing DEL-011-06.

This deliverable supports OBJ-001 (code-compliant, fully functional maintenance shop) and OBJ-003 (complete, P.Eng.-stamped IFC design documentation).

**Source:** RFP §3.4; Decomposition DEL-002-06, OBJ-001, OBJ-003.

---

## Principles

### P-1: Geotech-First Design Sequencing

The service pit is the most geotechnically sensitive structural element in the building after the foundation. A below-grade pit in Alberta is subject to groundwater pressure, frost heave, and soil lateral pressure that are site-specific and not predictable without a geotechnical investigation.

**Principle:** Do not finalize pit depth, wall thickness, or waterproofing system before the geotechnical report (DEL-008-01) is available. If preliminary drawings must be issued before geotech is complete, clearly annotate them as preliminary and list the assumed geotechnical parameters explicitly.

**Source:** RFP §4.8.2 (geotech investigation required; foundation pricing negotiated post-geotech); ASSUMPTION — standard structural practice.

---

### P-2: Heavy Equipment Load Is the Governing Live Load

The service pit cover system and the pit edges at floor level must be designed for heavy tracked and packer equipment loads, not standard floor live loads. A motor scraper is a very large, heavy machine (operating weight typically in the range of tens of tonnes — exact equipment specification TBD from County).

**Principle:** Obtain the equipment load specification (axle loads, track footprint, contact pressure) from Camrose County before finalizing the cover system structural design. Use the governing equipment load as the design live load for the pit cover and adjacent floor slab edge conditions. Do not default to standard industrial floor live loads without confirming they bound the actual equipment.

**Source:** RFP §3.4 ("Steel plating in concrete at strategic locations to accommodate track and packer type heavy equipment"); App B notes; SOW-0028. ASSUMPTION: equipment load specification must be confirmed with Owner.

---

### P-3: Pit Geometry Drives Multi-Discipline Coordination

The service pit is a large structural element (conceptually 24' × 100') that directly affects:
- Mechanical: ventilation duct routing and pit air supply/exhaust locations.
- Electrical: below-grade conduit routing, light fixture locations and mounting details.
- Plumbing: pit floor drainage, potential sump, connection to drain system.
- Architectural: floor plan coordination, access location relative to bays and equipment travel.

**Principle:** The Structural Engineer should confirm the pit plan geometry with the Architect and other discipline leads before committing to the structural layout. Penetrations and blockouts in the pit walls and floor slab must be coordinated and shown on the structural drawings (with cross-reference to the governing discipline drawing).

**Source:** Decomposition PKG-002 scope description; RFP §3.4; ASSUMPTION — multi-discipline coordination standard practice.

---

### P-4: Access and Egress Must Meet OH&S Requirements

Below-grade working areas in Alberta are governed by the Alberta OH&S Code. The pit access configuration (stairs vs. ladder, width, handrails, headroom) must satisfy applicable OH&S requirements and any NBC occupancy requirements for working spaces.

**Principle:** Coordinate the structural access detail with the Architect. Do not treat the access as a minor detail — it is a code compliance item and a safety requirement. If the pit qualifies as a confined space under Alberta OH&S, additional requirements may apply to its design (ventilation sizing, access dimensions).

**Source:** ASSUMPTION — Alberta OH&S Code applicable (location TBD); RFP §2.15 (Prime Contractor OH&S obligations); SOW-0083.

---

## Considerations

### C-1: Frost Depth and Below-Grade Wall Exposure

Alberta frost depths are significant (can exceed 1.5 m in central Alberta — ASSUMPTION; exact design frost depth from geotech). The pit walls are below grade and must be designed against frost action, particularly at the top of wall where the frost/thaw zone is active. The pit floor must be below frost depth, or insulation/heating provisions must be included.

**Source:** ASSUMPTION — Alberta climate; NBC frost depth provisions (location TBD).

---

### C-2: Groundwater and Waterproofing

If the geotech report identifies a high groundwater table or perched water conditions, the pit will require positive-side waterproofing. The structural concrete mix design must be appropriate for below-grade water contact (low w/c ratio, adequate cover to rebar). Drainage tile and/or a sump pump system may be required.

**Note:** This is a significant cost and schedule risk if not identified early. The geotech report (DEL-008-01) is the critical input.

**Cost/Schedule Risk Bounding Framework (Lensing ref: F-003):** The cost and schedule impact of geotech-dependent design decisions (pit depth, waterproofing system, wall thickness) is mentioned qualitatively but not quantified or bounded. A risk bounding exercise should be performed when geotech data is available, addressing:

| Risk Variable | Low-Impact Scenario | High-Impact Scenario | Cost/Schedule Delta |
|---|---|---|---|
| Groundwater table (below pit floor vs. above) | No positive-side waterproofing needed | Full positive-side waterproofing + sump system | TBD |
| Frost depth (shallow vs. deep) | Minimal additional depth | Pit floor must be deepened or insulated | TBD |
| Bearing capacity (adequate vs. poor) | Standard slab-on-grade | Engineered fill or deep foundation for pit floor | TBD |

> This framework should be populated by the Structural Engineer and/or Project Manager upon receipt of DEL-008-01. See also C-6 (timeline pressure). Source: ASSUMPTION -- engineering judgment on structural cost drivers.

**Source:** ASSUMPTION — standard below-grade design consideration.

---

### C-3: Concrete Shrinkage and Crack Control in a Long Trench

A 100 ft (approximately 30 m) long concrete trench is a significant continuous structure. Concrete shrinkage and thermal movement can cause cracking if construction joints are not properly designed and located. The structural drawings should specify construction joint locations, sealant types, and rebar continuity across joints.

**Source:** ASSUMPTION — standard structural engineering practice for long concrete elements; CSA A23.3 (location TBD).

---

### C-4: Steel Plates at Pit Edges

Appendix B (Shop) notes "Steel Plates in Floor as indicated." The relationship between the embedded floor steel plates (for heavy equipment) and the pit edge condition must be detailed. The pit edge may require a steel angle or embedded plate to protect the concrete edge from equipment impact and to support the cover/grating system.

**Source:** App B (Shop) floor plan notes; RFP §3.4 (steel plates in concrete).

---

### C-5: Ventilation System Structural Interface

The RFP mandates ventilation of the pit (SOW-0028). Ventilation in a below-grade pit typically requires supply air openings at one end and exhaust at the other, or continuous perforated duct along the pit length. The structural design must accommodate whatever duct routing the Mechanical Engineer specifies — this means wall penetrations or overhead connections must be coordinated before the concrete walls are formed.

**Source:** RFP §3.4; ASSUMPTION — standard ventilation interface requirement.

---

### C-6: Timeline Pressure

All Work must be completed by December 31, 2026 (RFP §3.1). The service pit is a below-grade concrete element that lies on the critical path for the building structure. It must be cast before the building floor slab is completed. Delays to geotech (DEL-008-01) or structural design approval will directly compress the construction schedule.

**Source:** RFP §3.1; OBJ-002.

---

## Trade-offs

### T-1: Pit Depth vs. Equipment Clearance vs. Structural Cost

A deeper pit provides better mechanic access and clearance under large equipment, but increases:
- Concrete volume (walls, floor slab).
- Lateral earth pressure on walls (increased reinforcement).
- Waterproofing requirements (greater groundwater head if GWT is relevant).
- Excavation depth (cost and schedule).

**Recommendation:** The County (Owner) should specify the minimum required working clearance under the equipment types to be serviced. The Structural Engineer will then determine the minimum pit depth consistent with that clearance and the undercarriage height of the equipment. A shallower pit that meets clearance requirements is structurally and economically preferable.

**Source:** ASSUMPTION — engineering judgment on structural cost drivers.

---

### T-2: Cast-in-Place vs. Precast Pit Walls

Cast-in-place reinforced concrete walls are the most common approach for an industrial pit of this size and loading in Alberta. Precast panels are an alternative that could reduce on-site forming time but introduce connection detailing complexity (particularly for a 100' long trench with heavy equipment loads).

**Recommendation:** ASSUMPTION — cast-in-place is the baseline approach. If schedule pressure is acute, the Structural Engineer should evaluate precast panels for the pit walls. Human ruling required if this trade-off becomes a design decision point.

**Source:** ASSUMPTION.

---

### T-3: Cover System — Removable Grating vs. Steel Plates vs. Hinged Covers

The pit cover system (what spans across the pit opening at floor level to allow equipment to drive over it when the pit is not in use) has several options:
- **Removable bar grating:** Provides light and air into pit when in place, but not rated for heavy tracked equipment loads without heavy framing.
- **Steel checker plate / floor plate covers:** Can be designed for heavy equipment loads; opaque; must be removed manually or mechanically.
- **Hinged or trench-cover system:** Proprietary systems may be available in appropriate load ratings.

**Recommendation:** The Structural Engineer must confirm the equipment load requirement with the County and select a cover system rated for those loads. This is a significant structural design decision. The conceptual drawings do not specify the cover type. Human ruling required if the Owner has a preference.

**Cost-Benefit Framing (Lensing ref: D-003):** The three cover system options above are described in terms of structural characteristics but not compared on cost, availability, or lead time. A comprehensive worth ruling for T-3 should include the following dimensions (all currently TBD):

| Option | Estimated Relative Cost | Lead Time | Local Availability | Maintenance Burden |
|---|---|---|---|---|
| Removable bar grating | TBD | TBD | TBD | TBD |
| Steel checker plate covers | TBD | TBD | TBD | TBD |
| Hinged/proprietary trench covers | TBD | TBD | TBD | TBD |

> The Structural Engineer and/or Cost Estimator should populate these dimensions when equipment load data is confirmed, to support an informed selection decision.

**Source:** ASSUMPTION — engineering judgment; cover system not specified in accessible sources.

---

## Examples

TBD — No specific service pit design examples were available in the accessible source documents. The Structural Engineer should reference comparable industrial below-grade pit designs from their own practice experience and applicable published standards.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CON-001 | Pit dimensions: App B labels "24'" width and "100'" length on the Service Pit, but it is unclear whether these are exterior wall dimensions, interior clear dimensions, or approximate. The Structural Engineer must confirm which dimension is the design target (interior clear or overall). | App B (Shop) floor plan — labeled 24' and 100' on Service Pit | RFP §3.4 — no dimension stated | Datasheet (Attributes), Specification (R-003), Procedure (Step 3) | PROPOSAL: treat App B dimensions as interior clear dimensions (i.e., usable pit width = 24', usable pit length = 100') until confirmed by Owner/Architect | TBD |
| CON-002 | Equipment load specification: RFP §3.4 specifies "tracked and packer type heavy equipment" including motor scraper class, but does not provide axle loads or contact pressures. The cover system and pit edge cannot be structurally designed without this data. No load data found in accessible sources. | RFP §3.4; App B | No load data in accessible sources | Specification (R-002), Guidance (T-1, T-3) | PROPOSAL: County to provide equipment load specification (governing axle load, track footprint, contact pressure) before structural drawings are finalized | TBD |
| CON-003 | Pit ventilation system type: RFP §3.4 mandates ventilation but does not specify the ventilation approach (forced air supply/exhaust, natural ventilation, connection to building HVAC). The structural penetration requirements depend on the mechanical design. No mechanical information accessible at this stage. | RFP §3.4 (ventilated pit required) | No mechanical design available in accessible sources | Specification (R-001), Guidance (C-5) | PROPOSAL: Mechanical Engineer (PKG-003) to provide penetration requirements before structural drawings are issued for construction | TBD |
