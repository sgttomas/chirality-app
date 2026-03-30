# Datasheet — DEL-002-04 Structural Sections & Details

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-002-04 |
| **Name** | Structural Sections & Details |
| **Package** | PKG-002 — Structural Design |
| **Discipline** | Structural Engineering |
| **Type** | Drawing Set |
| **Responsible Party** | Structural Engineer |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Completion Deadline** | December 31, 2026 |
| **Scope of Work Reference** | SOW-0012 (Complete final structural design — concrete structure, 35' ceiling) |
| **Supports Objectives** | OBJ-001 (code-compliant functional facility), OBJ-003 (complete P.Eng.-stamped IFC documentation) |
| **Decomposition Reference** | WDMLRL_Decomposition_Claude.md, §7 — PKG-002 Deliverables, row DEL-002-04 |

---

## Attributes

### Building Geometry (per Appendix B — Shop floor plan, R-04)

| Attribute | Value | Source |
|---|---|---|
| Addition footprint | 130 ft × 100 ft (approx. 13,000 sq ft usable) | R-04 (App B floor plan); R-01 §3.1 |
| Existing building (Old North Shop) | 105 ft × 40 ft | R-04 (App B floor plan) |
| Total site width (combined) | 235 ft | R-04 (App B floor plan) |
| Structural system | Concrete structure | R-01 §3.4, App B notes |
| Clear ceiling height | 35 ft | R-01 §3.4, App B notes |
| Drive-through repair bay width | 24 ft each (2 bays) | R-04 (App B floor plan) |
| Wash bay width | 24 ft (single enclosed bay, motor scraper-sized) | R-01 §3.1, §3.4; R-04 App B |
| Service pit / trench dimensions | 24 ft wide × 100 ft long; **depth TBD — not stated in RFP or App B; to be confirmed by County operations team and validated against geotechnical report** (see CON-002 in Guidance.md) | R-04 (App B floor plan — labeled "Service Pit"); lensing item B-001 |
| Parts storage room | ~400 sq ft | R-01 §3.4 |
| Mezzanine | Above parts room, utility room, and wash bay | R-01 §3.4, App B notes |
| Mezzanine load rating | Heavy items (oil totes, pumping equipment) — load capacity TBD by structural calculation | R-01 §3.4 |
| Stairs to mezzanine | Required | R-04 (App B — "Stairs to Mezzanine" annotated) |

### Vertical Reference Elevations (for section drawing datum)

| Attribute | Value | Source |
|---|---|---|
| Top-of-slab elevation (main floor) | TBD — to be established relative to project datum | ASSUMPTION: required for section drawings; no value in accessible sources (lensing item E-001) |
| Mezzanine floor elevation | TBD — to be established relative to project datum | ASSUMPTION: required for section drawings; no value in accessible sources (lensing item E-001) |
| Crane runway beam elevation | TBD — to be established relative to project datum | ASSUMPTION: required for section drawings; referenced implicitly in Procedure Step 6 (lensing item E-001) |
| Top-of-foundation elevation | TBD — dependent on DEL-002-02 Foundation Plan | ASSUMPTION: required for structural section interface per Guidance C-05 (lensing item E-001) |

### Structural Elements — Key Components

| Component | Description | Source |
|---|---|---|
| Concrete floor | Structural slab; steel plates embedded at strategic locations for tracked/packer heavy equipment | R-01 §3.4, App B |
| Steel plate embedments | At multiple locations per floor plan (labeled "Steel Plate" in App B). **Plate thickness, plan dimensions, and anchor type: TBD** — not quantified in RFP or App B. **Loading basis (equipment types and wheel/track loads): TBD** — plates serve tracked/packer heavy equipment but specific loading data absent from all sources (see CON-003 in Guidance.md; lensing items B-002, E-002) | R-04 (App B floor plan); R-01 §3.4 |
| 5-Tonne Overhead Crane supports | Two 5-Tonne Overhead Cranes on trolley; crane rail/runway beam structure required | R-01 §3.4, App B (labeled "Gantry" — see Vocabulary Map Note above) |
| Service pit (trench) | Below-grade, ventilated and lighted; structural walls and floor required | R-01 §3.4, App B |
| Wash bay enclosure | Enclosed structural bay; overhead door, walls, roof integration | R-01 §3.1, §3.4, App B |
| Mezzanine structure | Load-bearing framing above parts room, utility room, and wash bay | R-01 §3.4, App B |
| Stairs | Access to mezzanine | R-04 (App B) |
| Foundation | Priced separately (variable-price post-geotech); normal ground conditions assumed for estimation | R-01 §4.8.2 |

### 5-Tonne Overhead Crane (Vocabulary Map Note)

**Canonical term: "5-Tonne Overhead Crane."** Per decomposition Vocabulary Map (D-001), "Gantry" appearing on App B drawings is an alias for the same equipment. Two "Gantry" annotations visible in App B wash bay and main shop areas correspond to the two 5-Tonne Overhead Crane positions. All documents in this deliverable use the canonical term "5-Tonne Overhead Crane" except when quoting source text directly (lensing item B-004).

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Governing jurisdiction | Province of Alberta | R-01 §2.22 |
| Applicable codes | Alberta Building Code; Alberta Safety Codes (specific editions TBD — not stated in RFP) | R-01 §3.3.2, §3.4 |
| Stamp requirement | All IFC drawings signed/stamped by a P.Eng. licensed in Alberta | R-01 §3.3.2 |
| Foundation pricing | Variable-price; negotiated post-geotechnical investigation | R-01 §4.8.2 |
| Normal ground conditions | Pricing assumption for foundation estimate until geotech report available | R-01 §4.8.2 |
| Completion deadline | December 31, 2026 (hard contractual deadline) | R-01 §3.1 |
| County approval required | Preliminary structural design must receive County approval before proceeding to final design | R-01 §3.3.2 |

---

## Construction

### Relationship to Other DEL-002 Deliverables

| Related Deliverable | Relationship |
|---|---|
| DEL-002-01 Preliminary Structural Design | Precedes — sections and details are part of final IFC drawing set only |
| DEL-002-02 Foundation Plan | Parallel — foundation sections may be referenced here or remain separate |
| DEL-002-03 Structural Framing Plans | Parallel — sections are cut from framing plans; must coordinate on grid lines and member designations |
| DEL-002-05 Mezzanine Framing Details | Related — mezzanine framing details may appear in this set or as a dedicated drawing |
| DEL-002-06 Service Pit / Trench Structural Details | Related — service pit sections/details may appear in this set or separately |
| DEL-002-07 Crane Support Structure Details | Related — crane runway sections may appear here |
| DEL-002-08 Steel Plate Embedment Plan | Related — embedment sections and details may appear here |
| DEL-002-09 Stair Details | Related — stair sections and details may appear in this set |
| DEL-002-10 Structural Calculation Package | Downstream consumer — sections are the drawn expression of the structural analysis |
| DEL-002-12 Structural Specification | Coordinate — material specifications referenced in sections must match the Specification |

---

## References

| Ref # | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.4 structural design requirements; §3.3.2 IFC stamp and approval requirements; §4.8.2 foundation pricing |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan — building geometry, bay widths, steel plate locations, crane positions, Service Pit, mezzanine |
| Decomposition | WDMLRL_Decomposition_Claude.md | PKG-002 deliverable definitions; SOW-0012; OBJ-001, OBJ-003 |
| R-02 | AB-2026-01424-Addendum 1.pdf | Adds §4.11 Bid Security; no structural changes noted (location TBD — addendum not read in full) |

### Standards (Inferred — texts not available)

**Note:** No standard editions or clause-level references have been confirmed. The Structural Engineer and AHJ must confirm specific editions applicable at time of design (lensing items B-003, A-001).

| Standard | Applicability | Edition | Primary Clauses | Status |
|---|---|---|---|---|
| Alberta Building Code | Governing building code — Alberta jurisdiction | **Edition TBD** — confirm with AHJ (Camrose County / applicable Safety Codes authority) | **Clause-level references TBD** | ASSUMPTION: likely applicable |
| Alberta Safety Codes Act | Safety code compliance requirement | **Edition TBD** | **Clause-level references TBD** | ASSUMPTION: likely applicable |
| CSA A23.3 (Design of Concrete Structures) | Concrete structure design — walls, slabs, pit, mezzanine | **Edition TBD** | **Clause-level references TBD** — e.g., shear wall design, slab-on-grade, below-grade pit walls | ASSUMPTION: likely applicable for concrete structural system |
| CSA S16 (Design of Steel Structures) | Steel elements — crane rails, embedments, mezzanine steel | **Edition TBD** | **Clause-level references TBD** — e.g., crane runway fatigue, connection capacity | ASSUMPTION: likely applicable |
| AISC / CISC crane runway design provisions | Crane runway beam and bracket design for 5-Tonne Overhead Cranes | **Specific guide TBD** | **Clause-level references TBD** | ASSUMPTION: likely applicable |
| NBCC (National Building Code of Canada) | Referenced by Alberta Building Code for loads and structural provisions | **Edition TBD** | **Table 4.1.5.3 (storage occupancy) TBD** — relevant for mezzanine live load | ASSUMPTION: applicable via ABC adoption |
