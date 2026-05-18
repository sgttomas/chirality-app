# DEL-018-04 | Datasheet — Cement & Gravel Pads

---

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-018-04 |
| **Title** | Cement & Gravel Pads |
| **Package** | PKG-018 — Sitework & Civil Construction |
| **Discipline** | Civil / Sitework Construction |
| **Type** | Construction |
| **Responsible Party** | General Contractor |
| **SOW Coverage** | SOW-0078 (Cement Pads), SOW-0079 (Gravel Pad) |
| **Objective Alignment** | OBJ-001 |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price |
| **Owner** | Camrose County |
| **Project** | 2026 Design Build — WDMLRL Maintenance Shop Addition |
| **Site Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Completion Deadline** | December 31, 2026 (Source: RFP §3.1) |

---

## Attributes

### Pad Types

Two distinct pad types are identified in the conceptual drawings (Appendix B) and scope of work:

| Pad Type | SOW Ref | Material Responsibility | Conceptual Drawing Location |
|----------|---------|------------------------|-----------------------------|
| Cement Pad(s) | SOW-0078 | Contractor supplies cement and prep; County/Landfill supplies gravel (see note below) | Shown between Overhead Pole Shed/Metal Racking zone and Gravel Pad area; also small notation adjacent to Wash Bay (east side) |
| Gravel Pad | SOW-0079 | County/Landfill supplies gravel; Contractor preps subgrade | Shown north of New North Shop (upper zone on Appendix B plan) |

> **Note — Material Supply:** Appendix B states: "Contractor to supply cement and prep – Landfill to supply gravel." This note applies to the overall site; the specific allocation by pad type is consistent with SOW-0078 (cement pads = contractor-supplied cement) and SOW-0079 (gravel pad = Landfill-supplied gravel, contractor-prepared subgrade). Source: Appendix B (Shop), note block.

### Cement Pad — Dimensional Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Pad locations | As shown on Appendix B conceptual drawing; IFC drawings to govern | App B |
| Approximate area — Cement Pad (south zone) | Visible on drawing as strip between Overhead Pole Shed/Metal Racking and Gravel Pad area; approximately 18' deep dimension annotated. **Note:** This is a single dimension from a conceptual drawing and does not constitute a design basis; the second dimension (width) is not stated on the conceptual drawing. Confirmed plan dimensions TBD pending IFC civil drawings. | App B |
| Additional cement pad notation | Small "CEMENT PAD" label on east side of drawing adjacent to Wash Bay Mud Sump | App B |
| Concrete strength / mix design | TBD (to be specified in IFC civil drawings; P.Eng.-stamped) | RFP §3.3.2 |
| Reinforcement | TBD (design-build; to be determined per loading and geotech) | RFP §3.4, §3.3.2 |
| Finish | TBD (slope for drainage required per grading design; RFP §3.4 and §3.3.2) | RFP §3.3.2, §3.4 |
| Steel plates in floor | Not applicable to exterior pads; steel plates in floor apply to building interior (New North Shop). ASSUMPTION: exterior cement pads do not include embedded steel plates unless IFC drawings indicate otherwise. | App B |

### Gravel Pad — Dimensional Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Pad location | North of New North Shop as shown on Appendix B; labeled "GRAVEL PAD" in upper zone | App B |
| Approximate depth (north–south) | Approximately 60' based on Appendix B annotation | App B |
| Approximate width (east–west) | Approximately 130' (full width of New North Shop) — ASSUMPTION based on plan proportions | App B |
| Gravel fill depth/thickness | TBD — minimum depth to be specified in IFC civil drawings per geotechnical report and civil engineer's specification. Essential for procurement volume calculation, placement lifts, and compaction verification. | TBD (IFC civil drawings) |
| Gravel supply | County/Landfill responsibility (SOW-0203, App B note) | App B, RFP §3.3.1 |
| Gravel specification | TBD (design-build; civil engineer to specify gradation, compaction) | RFP §3.3.2 |
| Subgrade preparation | Contractor responsibility; must follow DEL-018-02 (Site Grading) completion | _DEPENDENCIES.md |

---

## Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| **Prerequisite state** | Site grading (DEL-018-02) must be complete before pad placement | _DEPENDENCIES.md |
| **Upstream design dependency** | Pad layout and dimensions must be finalized in IFC civil drawings (PAD-LAYOUT-001); crane pad specs coordinated with DEL-016-01 | _DEPENDENCIES.md |
| **Concrete cure time** | TBD — ASSUMPTION: minimum 28-day cure before load application; actual requirement per engineer specification and Alberta Safety Codes | ASSUMPTION |
| **Drainage requirement** | Grading design must account for positive drainage; shall not alter drainage conditions of neighbouring properties | RFP §3.4 |
| **Load requirements** | Cement pads must support crane base loading (DEL-016-01) and heavy equipment. ASSUMPTION: pad design loads to be confirmed in IFC drawings per geotech and crane supplier data. | _DEPENDENCIES.md, App B |
| **Crane design loads (static)** | TBD — to be provided by crane supplier (DEL-016-01 data sheet); required input for P.Eng. pad structural design. Units: kN. | TBD (DEL-016-01 crane supplier) |
| **Crane design loads (dynamic)** | TBD — dynamic loads (hoist, trolley travel, impact) to be provided by crane supplier (DEL-016-01 data sheet); required input for P.Eng. pad structural design. Units: kN. | TBD (DEL-016-01 crane supplier) |
| **Critical path status** | On critical path — crane pad completion blocks DEL-016-01 (Overhead Cranes installation) | _DEPENDENCIES.md |
| **Climate / environment** | Alberta site; concrete placement subject to seasonal temperature requirements (ASSUMPTION: cold weather concreting provisions may apply depending on construction season) | ASSUMPTION |
| **Grading design compliance** | Final civil design must include drainage features per site grading plan; IFC drawings P.Eng.-stamped | RFP §3.3.2 |

---

## Construction

| Element | Description | Source |
|---------|-------------|--------|
| **Work scope (SOW-0078)** | Construct cement pads as shown on conceptual drawings | App B, Decomposition §SSOW-J |
| **Work scope (SOW-0079)** | Construct gravel pad as shown on conceptual drawings | App B, Decomposition §SSOW-J |
| **Subgrade preparation** | Strip topsoil (DEL-018-01) and grade site (DEL-018-02) must precede pad work | _DEPENDENCIES.md, _CONTEXT.md |
| **Formwork (cement pads)** | Contractor responsible for formwork design and installation (ASSUMPTION: standard edge-formed slab-on-grade or equivalent) | ASSUMPTION |
| **Concrete placement** | Contractor supplies cement; County/Landfill supplies gravel aggregate | App B |
| **Gravel delivery handoff** | Material supply handoff interface: County/Landfill delivers gravel to site; Contractor to accept on site. Acceptance record (delivery tickets, quantity, visual gradation check) TBD — see Procedure.md Records. | App B; RFP §3.3.1 |
| **Finishing (cement pads)** | TBD — must include slope for drainage (ASSUMPTION: broom finish or equivalent per civil engineer specification) | RFP §3.4; ASSUMPTION |
| **Compaction (gravel pad)** | TBD — ASSUMPTION: compacted granular material per civil engineer's specification; County/Landfill to supply gravel | App B; ASSUMPTION |
| **Crane pad coordination** | Cement pad design must be coordinated with DEL-016-01 crane specifications prior to construction | _DEPENDENCIES.md |
| **Warranty** | All materials and workmanship guaranteed for construction period plus 2-year warranty period post-CCC; defects rectified within 10 days of Owner's written instruction | RFP §2.10 |

---

## Anticipated Artifacts

| Artifact | Description |
|----------|-------------|
| IFC Civil Drawings (pad layout) | P.Eng.-stamped, issued for construction — governs pad dimensions, reinforcement, mix design |
| Concrete mix design record | Specifying strength (e.g., MPa), slump, admixtures — TBD |
| Compaction test reports | For subgrade and gravel pad — TBD |
| Concrete placement records | Including pour date, cure monitoring — TBD |
| Concrete placement weather log | Ambient temperature, humidity, wind speed at time of each pour — required for concrete quality assurance and cold weather compliance evidence |
| Inspection reports | County representative must be present; copies provided to County (RFP §3.3.2) |
| Construction Completion Certificate (CCC) contribution | Pad completion forms part of overall CCC submission |

---

## References

| Ref Code | Document | Relevance |
|----------|----------|-----------|
| R-01 / App B | AB-2026-01424-Appendix_B_(Shop).pdf | Conceptual floor plan showing CEMENT PAD and GRAVEL PAD locations and approximate dimensions |
| R-01 / §3.3.2 | AB-2026-01424-WDMLRL_RFP.pdf §3.3.2 | Scope of work: grading, drainage, inspection requirements, P.Eng. stamping |
| R-01 / §3.4 | AB-2026-01424-WDMLRL_RFP.pdf §3.4 | Design requirements: drainage, Alberta Safety Codes compliance |
| R-01 / §2.10 | AB-2026-01424-WDMLRL_RFP.pdf §2.10 | Guarantee/warranty period requirements |
| R-07 | AB-2026-01424-Appendix_C_-_Site_Maps.pdf | Site location and expansion area aerial; confirms construction location at SW 14–44–21–W4 |
| Decomposition | WDMLRL_Decomposition_Claude.md §SSOW-J, §7 PKG-018 | SOW-0078, SOW-0079 scope statements; DEL-018-04 package assignment |
