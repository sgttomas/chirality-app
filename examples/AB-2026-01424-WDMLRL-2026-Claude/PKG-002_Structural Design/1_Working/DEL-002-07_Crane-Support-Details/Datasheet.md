# Datasheet — DEL-002-07 Crane Support Structure Details

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-002-07 |
| Deliverable Name | Crane Support Structure Details |
| Package | PKG-002 Structural Design |
| Discipline | Structural Engineering |
| Type | Drawing Set |
| Responsible Party | Structural Engineer (P.Eng., licensed in Alberta) |
| Covers SOW | SOW-0012 |
| Supports Objectives | OBJ-001, OBJ-003 |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Location | SW 14–44–21–W4, near Ferintosh, Alberta |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price Contract |
| Completion Deadline | December 31, 2026 |
| Source: _CONTEXT.md | — |
| Source: Decomposition | WDMLRL_Decomposition_Claude.md §7, PKG-002 table |

---

## Attributes

### Crane System

| Attribute | Value | Source |
|---|---|---|
| Crane type | Overhead crane on trolley | RFP §3.4; App B (Shop) note list |
| Crane quantity | 2 (two) | RFP §3.4; App B (Shop) drawing and note list |
| Crane rated capacity | 5 tonnes each | RFP §3.4; App B (Shop) note list ("(2) 5 Ton Cranes") |
| Crane designation on drawing | "5 TON CRANE" (two locations shown) | App B (Shop) floor plan |
| Crane span (bay width served) | TBD — not dimensioned on conceptual drawing; to be confirmed by structural engineer based on bay layout | App B (Shop) floor plan (spatial reference only) |
| Crane runway orientation | TBD — appears longitudinal along 100' building depth per App B layout; to be confirmed on IFC drawings | App B (Shop) floor plan (ASSUMPTION) |
| End stop requirements | TBD | Not stated in accessible sources |
| Bridge drive type | TBD | Not stated in accessible sources |
| Hoist type | TBD | Not stated in accessible sources |
| Crane supplier / model | TBD — not identified in RFP or Appendix B | — |
| Crane wheel gauge (distance between rail centerlines) | TBD — to be obtained from crane supplier data sheet; fundamental dimensional input for runway beam spacing | **[B-001]** Crane supplier data sheet (PROPOSAL) |

### Building Structure (Context for Crane Support)

| Attribute | Value | Source |
|---|---|---|
| Structure type | Concrete structure | RFP §3.4; App B (Shop) note list ("Concrete Structure (35' Ceiling)") |
| Building footprint | 130' × 100' (New North Shop addition) | App B (Shop) floor plan dimensions |
| Clear ceiling height | 35 feet (35') | RFP §3.4; App B (Shop) note list |
| Power supply to cranes | Three-phase power (to be provided per electrical design) | RFP §3.4 (three-phase power); SOW-0059 (power for two 5-tonne overhead cranes) |
| Minimum hook height | TBD — to be obtained from crane supplier; constrains runway beam elevation relative to 35' ceiling (see Guidance Principle 3, Procedure Step 2.5) | **[B-002]** Crane supplier / PKG-016 (PROPOSAL) |

### Crane Support Structure

| Attribute | Value | Source |
|---|---|---|
| Support structure type | TBD — runway beam/girder system with column corbels or dedicated crane columns; to be determined by structural engineer based on crane supplier data and geotechnical report | ASSUMPTION |
| Runway beam material | TBD | Not stated in accessible sources |
| Column/corbel arrangement | TBD — to be resolved during structural design; concrete columns implied by concrete structure type | ASSUMPTION |
| Runway beam span | TBD — dependent on column spacing (structural engineer to determine) | — |
| Design crane wheel loads | TBD — to be obtained from crane supplier data sheet and used for structural design | — |
| Runway beam end connections | TBD | — |
| Buffer/bumper requirements | TBD | — |
| Deflection limits | TBD — subject to governing code and crane classification | — |
| Fatigue classification | TBD — subject to CMAA service class of cranes and governing structural standard | ASSUMPTION: CMAA likely applicable |

### Gantry Note

| Attribute | Value | Source |
|---|---|---|
| "Gantry" reference on App B drawing | App B (Shop) floor plan labels "Gantry" near wash bay area | App B (Shop) floor plan |
| Decomposition resolution | Per D-001, gantry references on drawings are the same equipment as the two 5-tonne overhead cranes | WDMLRL_Decomposition_Claude.md §3, SOW-0067 Notes; Vocabulary Map |
| Interpretation | The two crane references on the App B floor plan (main shop bays) and the "Gantry" label (wash bay area) are treated as the same two overhead crane system per D-001 | ASSUMPTION (see Conflict Table in Guidance.md) |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Design codes — general | All applicable Alberta building codes and regulations; all Alberta Safety Codes | RFP §3.3.2 |
| IFC stamp requirement | Drawings must be signed/stamped by a P.Eng. licensed to practice in the province of Alberta | RFP §3.3.2 |
| Preliminary design approval | County approval required for preliminary structural design before proceeding to final | RFP §3.3.2; SOW-0010b |
| Geotechnical dependency | Foundation and column design dependent on geotechnical report; report to be provided to Owner | RFP §3.3.2; SOW-0001 |
| Coordination required | Crane support structure must be coordinated with crane supplier data sheet, electrical (power feeds per SOW-0059), and building structure (DEL-002-03 Framing Plans, DEL-002-04 Structural Sections) | ASSUMPTION (standard practice) |
| Guarantee period | Construction period plus 2 years post-CCC | RFP §2.10.2 |

---

## Construction

| Item | Value | Source |
|---|---|---|
| Deliverable form | Drawing Set (Issued for Construction) | _CONTEXT.md; Decomposition §7 PKG-002 |
| Drawing content (anticipated) | Crane runway beam framing plan; beam sections and connection details; column/corbel details; end stop/bumper details; anchor bolt plan; design notes and load table | ASSUMPTION (standard structural drawing set content for crane runway) |
| Stamp | P.Eng. licensed in Alberta | RFP §3.3.2 |
| Coordination drawings | Must be consistent with DEL-002-03 (Framing Plans), DEL-002-04 (Structural Sections & Details) | ASSUMPTION |
| Electrical interface | Crane power circuits per DEL-004 (Electrical Design); coordinate conductor entry points at crane runway | ASSUMPTION |
| Drawing numbering convention | TBD — drawing numbers to follow project document control standard; convention not yet defined or referenced in accessible sources (see Procedure Step 4.2) | **[X-002]** Project Manager (PROPOSAL) |

---

## References

| Ref | Document | Relevance | Accessible |
|---|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | Main RFP — §3.4 structural requirements, two 5-tonne cranes, 35' ceiling, concrete structure | Yes (reviewed) |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan — crane locations, building dimensions, structural notes | Yes (reviewed) |
| WDMLRL_Decomposition_Claude.md | Project Decomposition R1 2026-02-25 | DEL-002-07 entry, SOW-0012, SOW-0067, D-001 | Yes (reviewed) |
| NBC / Alberta Building Code | National Building Code of Canada; Alberta Building Code | Governing building code for structural design | ASSUMPTION: applicable; location TBD |
| CSA S16 | Design of Steel Structures | Crane runway beam design if steel runway beams used | ASSUMPTION: likely applicable; location TBD |
| CSA A23.3 | Design of Concrete Structures | Concrete column/corbel design for crane support | ASSUMPTION: likely applicable; location TBD |
| CMAA Spec 70/74 | Crane Manufacturers Association of America — Specifications for Top-Running & Underhung Overhead Cranes | Crane service class, wheel loads, runway alignment tolerances | ASSUMPTION: likely applicable; location TBD |
