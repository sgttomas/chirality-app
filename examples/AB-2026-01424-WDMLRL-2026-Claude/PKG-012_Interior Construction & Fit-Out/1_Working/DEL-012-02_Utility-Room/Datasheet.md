# Datasheet — DEL-012-02: Utility Room

**Document Type:** Datasheet (Descriptive)
**Deliverable ID:** DEL-012-02
**Package:** PKG-012 — Interior Construction & Fit-Out
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Revision:** R1 — 2026-02-26 (Pass 3 — Semantic Lensing Enrichment)

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-012-02 |
| Deliverable Title | Utility Room |
| Package | PKG-012 — Interior Construction & Fit-Out |
| Responsible Party | General Contractor |
| Activity Type | Construction |
| SOW Reference | SOW-0030 |
| Objective Linkage | OBJ-001 |
| Contract Form | CCDC 14-2013 Design-Build Stipulated Price Contract |
| Project Location | SW 14-44-21-W4, near Ferintosh, Alberta |
| Completion Deadline | December 31, 2026 (Source: RFP S3.1) |

---

## Attributes

### Spatial Attributes

| Attribute | Value | Source | Notes |
|---|---|---|---|
| Room footprint (length x width) | TBD -- Design team to confirm from IFC drawings. 16' bay width is ASSUMPTION only from column grid annotation. Resolution path: finalize at design stage per Step 1 coordination. | App B (Shop) | Utility room shown on conceptual floor plan adjacent to Parts Room; exact dimensions not dimensioned on concept drawing. (Enriched per B-001) |
| Room location | South side of New North Shop, between Parts Room (west) and Wash Bay (east) | App B (Shop) -- floor plan | |
| Building total useable area | ~13,000 sq ft | RFP S3.1 | Total new shop; utility room is one component |
| Building total plan dimensions | 130' x 100' (New North Shop footprint) | App B (Shop) -- floor plan dimensions | |
| Column bay widths | 16' bay width at utility room zone (south row) | App B (Shop) -- plan dimensions annotated | ASSUMPTION: the 16' bay annotation aligns with utility room zone |
| Building ceiling height | 35' (concrete structure) | RFP S3.4, App B (Shop) notes | Applies to overall building structure height |
| Utility room clear height (below mezzanine) | TBD -- Design team and Structural Engineer to confirm actual clear height from floor to underside of mezzanine deck. This measurement is critical for equipment clearance and ventilation design. Resolution path: confirm from structural/IFC drawings. | App B (Shop) -- mezzanine shown above utility room | Mezzanine forms the effective ceiling of the utility room; 35' building height does not represent the utility room clear height. (Enriched per B-003) |
| Mezzanine above | Yes -- load-bearing mezzanine overhead (capable of oil totes, pumping equipment) | RFP S3.4, App B (Shop) notes | Mezzanine spans over Parts Room, Utility Room, and Wash Bay |

### Lighting

| Attribute | Value | Source |
|---|---|---|
| Lighting fixture count | 2 x 8' LED fixtures | App B (Electrical) -- Electrical Notes |
| Lighting circuit type | 15 Amp 120V (per electrical drawing legend, utility room zone) | App B (Electrical) -- floor plan and legend |

### Electrical

| Attribute | Value | Source |
|---|---|---|
| Receptacle types present (utility room zone) | 15A/120V outlets per electrical drawing | App B (Electrical) -- floor plan |
| Building power supply | Three-phase | RFP S3.4 |
| Additional circuit provisions | TBD -- final electrical design to confirm dedicated circuits for mechanical equipment housed in utility room | App B (Electrical) |

### Plumbing

| Attribute | Value | Source |
|---|---|---|
| Floor drain | Present in utility room zone per plumbing plan | App B (Plumbing) -- floor plan |
| Water tap | Present in/adjacent to utility room zone | App B (Plumbing) -- floor plan annotation |
| 50,000 L Water Storage (cistern) | Located in utility room zone -- cistern shown on floor plan in utility room | App B (Shop), App B (Plumbing) -- "50,000 L Water Storage" label in utility room area |
| Stairs to mezzanine | Located in/adjacent to utility room | App B (Shop), App B (Plumbing) -- "Stairs to Mezzanine" label in utility room zone |

### Mechanical / HVAC Interface

| Attribute | Value | Source |
|---|---|---|
| Heating system host | ASSUMPTION: utility room is primary mechanical equipment host room for PKG-013 heating system | _DEPENDENCIES.md, App B (Shop) |
| Air exchanger host | ASSUMPTION: utility room hosts air exchanger and makeup air connections (PKG-013 DEL-013-02, DEL-013-03) | _DEPENDENCIES.md |
| Ventilation requirement | Adequate ventilation required for equipment environment -- TBD: mechanical engineer (PKG-013) to define specific ventilation rate or air changes per hour | _CONTEXT.md -- Key Requirements |
| Forced Air Makeup supply | Building-level system; distribution points in utility room TBD | App B (Shop) notes -- "Forced Air Makeup" |

### Access Door(s)

| Attribute | Value | Source | Notes |
|---|---|---|---|
| Door count | TBD -- minimum 1 access door required; confirm from IFC drawings | _CONTEXT.md -- Scope | (Enriched per B-002) |
| Door size | TBD -- must accommodate largest equipment item for initial installation and future replacement. Resolution path: confirm against PKG-013 equipment submittals at design stage. | Procedure Step 3.4; _CONTEXT.md -- Scope | (Enriched per B-002) |
| Door type | TBD -- confirm from IFC drawings (industrial access door anticipated) | _CONTEXT.md -- Scope | (Enriched per B-002) |
| Door fire rating | TBD -- confirm whether fire-rated door is required based on fire separation assessment (see Specification REQ-012-02-014 and Guidance C6). Resolution path: Design team + AHJ determination. | ASSUMPTION: may be required if utility room requires fire-rated separation | (Enriched per B-002, A-004) |
| Door swing direction | TBD -- confirm from IFC drawings; consider code egress requirements | _CONTEXT.md -- Scope | (Enriched per B-002) |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Environment type | Industrial / mechanical equipment room | _CONTEXT.md |
| Finish standard | Appropriate finishes for equipment environment -- TBD: design team to define measurable finish performance criteria (moisture resistance rating, abrasion class, cleanability) | _CONTEXT.md -- Key Requirements |
| Fire rating / fire separation | TBD -- Design team and AHJ to confirm whether the utility room, as a mechanical equipment host room, requires fire-rated wall separation from adjacent spaces under Alberta Building Code or National Fire Code. ASSUMPTION: likely required for a room housing mechanical/heating equipment. (Enriched per A-004) | RFP S3.3.2, S3.4; ASSUMPTION based on standard code practice for mechanical equipment rooms |
| Accessibility requirement | Accessible for maintenance and service of hosted mechanical equipment. TBD: confirm whether Alberta Building Code barrier-free access requirements apply to this mechanical equipment room in a public-authority-owned building. (Enriched per F-001) | _CONTEXT.md -- Key Requirements |
| Drainage requirement | Adequate drainage (floor drain confirmed) | _CONTEXT.md -- Key Requirements; App B (Plumbing) |
| Code compliance | Code-compliant construction per Alberta Safety Codes Act (RSA 2000), Alberta Building Code (current edition), National Fire Code (Alberta adoption -- ASSUMPTION: likely applicable), and all applicable local regulations | RFP S3.3.2, S3.4 (Enriched per F-003 -- harmonized with Specification Standards table) |
| Gas code applicability | TBD -- confirm fuel type for PKG-013 heating system. If gas-fired, Alberta Gas Safety Code applies and utility room construction must accommodate combustion air, flue penetrations, and gas line routing provisions. (Enriched per C-002) | ASSUMPTION: pending PKG-013 equipment selection |
| Warranty period | 2 years post-CCC (Construction Completion Certificate). TBD: confirm warranty coverage scope for specific PKG-012 utility room elements (equipment platforms, finishes, access doors, penetration sealing). (Enriched per F-005) | RFP S2.10.2 |
| Lien holdback | 10% withheld until project completion per Prompt Payment and Construction Lien Act | RFP S2.13.2 |

---

## Construction

| Element | Description | Source |
|---|---|---|
| Structural system | Concrete structure; utility room walls are non-structural interior partitions within the concrete building shell | RFP S3.4, App B (Shop) notes |
| Wall finishes | TBD -- design to specify; must be appropriate for mechanical equipment environment. Design team to define measurable performance criteria. | _CONTEXT.md |
| Wall fire rating | TBD -- confirm fire separation requirements per Alberta Building Code and National Fire Code. ASSUMPTION: fire-rated partitions may be required. (Enriched per A-004) | ASSUMPTION based on standard code practice |
| Floor finish | Concrete with floor drain; finish specification TBD | App B (Plumbing) |
| Ceiling treatment | TBD -- mezzanine deck forms overhead level; underside finish to be specified by design. Utility room clear height (floor to mezzanine underside) TBD. | App B (Shop) |
| Access door(s) | Access door(s) required for maintenance and service; door count, size, type, fire rating, and swing direction all TBD at design stage (see Access Door attributes table above). (Enriched per B-002) | _CONTEXT.md -- Scope |
| Access panels | Access panels as needed per IFC drawings | _CONTEXT.md -- Scope |
| Equipment platforms / mounting | Required for mechanical and HVAC equipment (PKG-013). Platform design driven by equipment submittals. | _CONTEXT.md -- Scope |
| Long-term serviceability provisions | TBD -- design should consider provisions for future equipment replacement: knock-out panels, rigging points, or equipment access paths wider than initial installation needs. (Enriched per E-001) | ASSUMPTION: standard practice for mechanical equipment rooms |
| Cistern integration | 50,000 L water storage cistern located in utility room zone. Structural pad responsibility: PROPOSAL -- PKG-012 provides structural pad; PKG-014 installs cistern equipment (see Conflict Table CON-012-02-02 in Guidance). | App B (Shop), RFP S3.4 |
| Mezzanine stair access | Stair to mezzanine located in/adjacent to utility room | App B (Shop), App B (Plumbing) |
| IFC Drawings required | All construction drawings must be P.Eng.-stamped; issued for construction before construction begins. P.Eng. stamp must be verified before construction commences. | RFP S3.3.2 |

---

## References

| Ref ID | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf -- S3.1, S3.4 | Project background, design requirements, scope of work |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan showing utility room location, dimensions, cistern, mezzanine |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf | Electrical layout -- 2x 8' LED fixtures in utility room, 15A outlets |
| R-06 | AB-2026-01424-Appendix B (Plumbing).pdf | Plumbing layout -- floor drain and water tap in utility room zone |
| -- | WDMLRL_Decomposition_Claude.md -- S7 PKG-012, S3 SOW-0030 | Deliverable and SOW definitions |
| -- | _CONTEXT.md | Deliverable identity, scope, key requirements |
| -- | _DEPENDENCIES.md | Upstream/downstream dependency constraints |
| -- | _SEMANTIC_LENSING.md | Pass 3 enrichment inputs (28 warranted items) |
