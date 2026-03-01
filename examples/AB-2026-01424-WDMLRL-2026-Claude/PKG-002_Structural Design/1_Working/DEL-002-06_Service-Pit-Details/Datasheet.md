# Datasheet — DEL-002-06: Service Pit / Trench Structural Details

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-002-06 |
| **Deliverable Name** | Service Pit / Trench Structural Details |
| **Package** | PKG-002 Structural Design |
| **Discipline** | Structural Engineering |
| **Type** | Drawing Set |
| **Responsible Party** | Structural Engineer (P.Eng., licensed in Alberta) |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Project Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Covers SOW** | SOW-0028 (service pit/trench), SOW-0012 (final structural design). **Note:** _CONTEXT.md references only SOW-0012; SOW-0028 is included here because the Decomposition SOW traceability table maps SOW-0028 to PKG-011/DEL-011-06 (construction), while DEL-002-06 provides the design drawings that enable SOW-0028 construction. Normalization pending confirmation by Project Decomposition owner. (Lensing ref: E-001) |
| **Supports Objectives** | OBJ-001, OBJ-003 |
| **Decomposition Reference** | WDMLRL_Decomposition_Claude.md — PKG-002, DEL-002-06 |

---

## Attributes

### Functional Description

The service pit (also referred to as service trench) is a below-grade, in-floor structural element located within the New North Shop addition. It provides a working cavity allowing mechanics to access the underside of heavy equipment (e.g., motor scrapers, tracked equipment) at floor level without requiring a hoist. The pit must be ventilated and lighted per RFP §3.4.

**Source:** RFP §3.4 (SOW-0028); Appendix B (Shop) conceptual floor plan; Decomposition vocabulary map ("Service Pit / Trench: Below-grade pit/trench for under-equipment servicing").

### Conceptual Dimensions (from Appendix B drawing)

| Parameter | Value | Source | Confidence |
|---|---|---|---|
| Width (approximate) | 24 ft | App B floor plan (labeled dimension on Service Trench) | Conceptual — subject to structural design |
| Length (approximate) | 100 ft | App B floor plan (labeled dimension on Service Trench) | Conceptual — subject to structural design |
| Depth | TBD | Not stated in RFP or App B | **Critical missing essential fact.** Pit depth governs structural wall design, excavation scope, waterproofing extent, and cost. Sources required: Owner equipment clearance requirement + geotech frost depth (DEL-008-01). (Lensing ref: B-001) |
| Position within building | Right (east) side of New North Shop, central zone | App B floor plan | Conceptual |

> **Note:** The 24' x 100' dimensions are read from the conceptual floor plan (Appendix B). These are design targets, not confirmed structural dimensions. Final dimensions to be established by Structural Engineer based on equipment clearance requirements, structural analysis, and geotech findings. **Ambiguity:** It is unclear whether these represent interior clear dimensions or overall (exterior wall) dimensions -- see CON-001 in Guidance.md. Proposed treatment: interior clear dimensions until confirmed by Owner/Architect. (Lensing ref: B-003)

### Structural System Attributes

| Attribute | Value | Source |
|---|---|---|
| Structure type | Below-grade reinforced concrete pit/trench | ASSUMPTION — consistent with "concrete structure" specified for the building (RFP §3.4, App B notes) |
| Wall construction | TBD — reinforced concrete walls (ASSUMPTION: cast-in-place) | Structural design determination |
| Floor slab of pit | TBD — reinforced concrete slab-on-grade or suspended slab | Structural design determination |
| Top cover / access | TBD — removable steel grating or cover plates (ASSUMPTION based on operational function) | Not explicitly stated in sources |
| Surcharge loads | Must accommodate tracked and packer heavy equipment (e.g., motor scraper class) at floor level | RFP §3.4; App B notes ("Steel Plates in Floor as indicated") |
| Waterproofing/drainage | TBD | Not specified in accessible sources |
| Pit entry/exit | TBD — stairs or ladder access (ASSUMPTION) | Not explicitly stated in sources |

### Concrete Material Parameters (placeholder — to be confirmed by Structural Engineer)

> **Note:** These material parameters are required for the drawing set general notes (Procedure Step 6.2) and are essential operational parameters for the pit structural design. Values TBD until Structural Engineer confirms. (Lensing ref: F-002)

| Parameter | Value | Source |
|---|---|---|
| Concrete compressive strength (f'c) | TBD | Structural Engineer to specify |
| Reinforcement grade | TBD | Structural Engineer to specify (ASSUMPTION: CSA G30.18 400W or 400R) |
| Minimum cover to rebar (pit walls, below-grade) | TBD | Structural Engineer to specify per CSA A23.1 exposure class (ASSUMPTION: likely applicable) |
| Minimum cover to rebar (pit floor slab) | TBD | Structural Engineer to specify |

### Mechanical / Systems Attributes

| Attribute | Value | Source |
|---|---|---|
| Ventilation | Required — type and specification TBD | RFP §3.4 ("Ventilated…service pit") |
| Lighting | Required — type and specification TBD | RFP §3.4 ("…and lighted service pit area") |
| Sump/drainage within pit | TBD | Not stated in accessible sources; may be coordinated with PKG-006 (Plumbing Design) |

### Geotechnical / Site Conditions

| Attribute | Value | Source |
|---|---|---|
| Geotechnical report | TBD — required before structural design can be finalized | RFP §4.8.2; geotechnical investigation (DEL-008-01) is a prerequisite |
| Groundwater conditions | TBD | Dependent on geotech report |
| Frost depth | TBD — Alberta climate; design frost depth to be confirmed from geotech and NBC/ABC | ASSUMPTION: applicable |
| Subgrade bearing capacity | TBD | Dependent on geotech report |

### Geotechnical Design Parameters (placeholder — to be populated from DEL-008-01)

> **Note:** This table provides a structured placeholder for the specific geotechnical parameters that are essential inputs to the service pit structural design. Values shall be populated upon receipt of DEL-008-01 Geotechnical Investigation Report. (Lensing ref: B-002)

| Parameter | Value | Unit | Source |
|---|---|---|---|
| Allowable bearing capacity at pit founding elevation | TBD | kPa | DEL-008-01 |
| Design groundwater table (GWT) elevation | TBD | m (relative to pit floor) | DEL-008-01 |
| Design frost depth | TBD | m below grade | DEL-008-01 + NBC |
| Active earth pressure coefficient (Ka) | TBD | dimensionless | DEL-008-01 |
| Soil unit weight (backfill) | TBD | kN/m3 | DEL-008-01 |
| Soil classification (at pit depth) | TBD | — | DEL-008-01 |
| Special conditions (expansive soils, organics, deleterious materials) | TBD | — | DEL-008-01 |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Jurisdiction | Province of Alberta | RFP §2.22 |
| Governing building code | National Building Code of Canada 2019 (NBC 2019) as adopted in Alberta | ASSUMPTION: likely applicable (specific edition TBD — location TBD in sources) |
| Structural design standard | CSA A23.3 (Concrete Design); CSA S16 (Steel Design) | ASSUMPTION: likely applicable — standard practice for Alberta structural engineering |
| Occupancy/use classification | Industrial maintenance facility; heavy equipment servicing | RFP §3.1, §3.4 |
| Design life | Not stated — ASSUMPTION: consistent with 50-year building design life per NBC | ASSUMPTION |
| Guarantee period | 2 years post-CCC | RFP §2.10 |
| Completion deadline | December 31, 2026 | RFP §3.1 |
| IFC stamp requirement | Signed and stamped by a P.Eng. licensed to practice in Alberta | RFP §3.3.2 |

---

## Construction

| Field | Value | Source |
|---|---|---|
| Construction package | PKG-011 Building Structure & Envelope (DEL-011-06 Service Pit/Trench) | Decomposition §7 |
| Construction responsible party | General Contractor | Decomposition PKG-011 |
| Foundation dependency | Foundation design (DEL-002-11, DEL-010-01) must be completed or coordinated first | ASSUMPTION: logical sequencing |
| Geotech dependency | DEL-008-01 Geotechnical Investigation & Report | RFP §4.8.2 |
| Interface disciplines | Mechanical (ventilation — PKG-003/013), Electrical (lighting — PKG-004/015), Plumbing (drainage — PKG-006/014) | RFP §3.4 |
| Inspection records | DEL-009-04 — Inspection records shall record code compliance for this deliverable's built result (per Specification R-006 verification method) | Specification R-006; Lensing ref: E-002 |

---

## References

| Ref | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.4 Design Requirements: service pit specification (ventilated, lighted); §3.3.2: IFC stamp requirements |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan: service trench shown at approx. 24' × 100' in New North Shop |
| DECOMP | WDMLRL_Decomposition_Claude.md | DEL-002-06 entry; SOW-0028; PKG-002 scope; OBJ-001, OBJ-003 definitions |
| TBD | CSA A23.3 — Design of Concrete Structures | ASSUMPTION: governing structural standard (location TBD — not directly accessible) |
| TBD | CSA S16 — Design of Steel Structures | ASSUMPTION: governing standard for any steel cover elements (location TBD) |
| TBD | NBC 2019 (Alberta edition) | ASSUMPTION: governing building code (location TBD) |
| TBD | DEL-008-01 Geotechnical Investigation Report | Required input — not yet available |
