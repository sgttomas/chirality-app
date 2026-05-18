# Datasheet — DEL-002-11 Foundation Design Package (Variable-Price)

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-002-11 |
| Name | Foundation Design Package (Variable-Price) |
| Package | PKG-002 — Structural Design |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Location | SW 14–44–21–W4, near Ferintosh, Alberta |
| Discipline | Structural Engineering |
| Type | Design Package |
| Responsible Party | Structural Engineer |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price Contract |
| Covers SOW | SOW-0019 |
| Supports Objectives | OBJ-003, OBJ-006 |
| Decomposition Reference | WDMLRL_Decomposition_Claude.md — §7, PKG-002 row for DEL-002-11 |

> **Note (re: D-001 / CFT-001):** The mapping above reflects the decomposition's explicit assignment (OBJ-003, OBJ-006). Whether DEL-002-11 should also formally support OBJ-001 ("Deliver a code-compliant, fully functional maintenance shop addition") remains unresolved — see Guidance.md, Conflict Table, CFT-001. The foundation is intrinsic to a code-compliant building, but the decomposition may have intentionally excluded OBJ-001 from this variable-price design package. Human ruling required. (Source: Decomposition §5, OBJ-001; Decomposition §7, PKG-002 row for DEL-002-11)

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| Deliverable type | Design Package | _CONTEXT.md |
| Pricing mechanism | Variable-price (cost estimate for proposal based on normal ground conditions; final pricing negotiated post-geotech) | RFP §4.8.2 |
| Proposal estimate basis | Normal ground conditions, without deleterious subgrade material | RFP §4.8.2 |
| Final pricing trigger | Completion and delivery of full geotechnical investigation report to Owner | RFP §4.8.2 |
| Stamping requirement | All IFC drawings signed/stamped by a P.Eng. licensed in Alberta | RFP §3.3.2 |
| Structure type | Concrete structure | RFP §3.4, Appendix B (Shop) |
| Ceiling height (superstructure) | 35 feet | RFP §3.4, Appendix B (Shop) |
| Building footprint (Addition) | 130 ft x 100 ft (~13,000 sq ft useable area) | Appendix B (Shop), RFP §3.1 |
| Geotechnical input required | Full geotechnical investigation report (SOW-0001, PKG-008 / DEL-008-01) | RFP §3.3.2, §4.8.2 |
| Foundation type | TBD — dependent on geotechnical investigation results; ASSUMPTION: spread footings on assumed normal conditions (see Guidance.md, Trade-offs, "Foundation type on assumed conditions") | ASSUMPTION |
| Allowable bearing capacity | TBD — dependent on geotechnical report; ASSUMPTION: 100–150 kPa for central Alberta glacial till or similar normal ground conditions (interim design value for proposal phase) | RFP §4.8.2; ASSUMPTION — see Procedure.md Step 1.1 item 3 |
| Frost depth (design value) | TBD — to be confirmed from geotech report and NBC climatic appendix for Ferintosh, AB; ASSUMPTION: conservatively assume 2.0 m below grade for design purposes (typical range for central Alberta is 1.5–2.0 m; use upper bound as conservative design value) | ASSUMPTION |
| Groundwater condition | TBD — dependent on geotechnical report; ASSUMPTION: groundwater assumed absent under normal conditions per RFP §4.8.2 ("without deleterious subgrade material") — revise upon receipt of DEL-008-01 | RFP §4.8.2; ASSUMPTION |
| Subgrade conditions assumed for estimate | Normal, without deleterious material | RFP §4.8.2 |
| Seismic zone | TBD — to be confirmed from NBC seismic hazard maps for SW 14–44–21–W4, Ferintosh AB. Structural Engineer to confirm from NBC climatic appendix. | location TBD |
| Ground snow load | TBD — to be confirmed from NBC climatic data tables for Ferintosh, Alberta. Structural Engineer to confirm from NBC climatic appendix. | location TBD |
| Wind load | TBD — to be confirmed from NBC climatic data tables for Ferintosh, Alberta. Structural Engineer to confirm from NBC climatic appendix. | location TBD |
| Unit convention | Imperial for architectural/building dimensions (ft, sq ft); metric for geotechnical parameters (m, kPa) per Canadian engineering practice. Mixed convention is standard but is stated here explicitly for clarity. | ASSUMPTION — see E-002 |

> **Enrichment notes:**
> - **B-001 (frost depth):** Narrowed from "approximately 1.5–2.0 m" to "conservatively assume 2.0 m" as a single design value. The engineer must commit to a specific value for calculation purposes; 2.0 m is the conservative upper bound of the typical range. (Source: Procedure.md Step 1.1; central Alberta climatic norms)
> - **B-002 (bearing capacity):** Added interim assumed bearing capacity of 100–150 kPa from Procedure.md Step 1.1 item 3 to the Datasheet as the authoritative parameter register. (Source: Procedure.md Step 1.1)
> - **B-003 (groundwater):** Added groundwater condition row. Procedure.md Step 1.1 item 3 references "no deleterious groundwater"; RFP §4.8.2 references "without deleterious subgrade material." (Source: RFP §4.8.2; Procedure.md Step 1.1)
> - **A-001 (climatic/seismic TBDs):** Clarified that the Structural Engineer must confirm from NBC climatic appendix for the project location. Values remain TBD pending engineer confirmation. (Source: Datasheet.md — existing TBDs; _SEMANTIC_LENSING.md A-001)
> - **E-002 (unit convention):** Added explicit statement of mixed unit convention. (Source: Datasheet.md Attributes — imperial dimensions; Procedure.md Step 1.1 — metric geotech parameters)

---

## Conditions

| Condition | Description | Source |
|---|---|---|
| Pre-condition — Geotech | Full geotechnical investigation and report (DEL-008-01) must be available before final foundation pricing can be negotiated; design may proceed to IFC on assumed normal conditions for proposal phase | RFP §4.8.2 |
| Pre-condition — Preliminary design approval | Preliminary Structural Design (DEL-002-01) must receive County project team approval before IFC foundation documents are finalized | RFP §3.3.2 |
| Constraint — Variable-price contract structure | Foundation design and construction costs are separated from the stipulated price; scope and price are re-confirmed with successful Proponent after geotech report is available | RFP §4.8.2 |
| Constraint — Alberta codes | Design must adhere to all applicable Alberta building codes, regulations, and Alberta Safety Codes | RFP §3.3.2, §3.4 |
| Constraint — IFC stamping | Issued-for-Construction drawings must be signed/stamped by P.Eng. licensed in Alberta | RFP §3.3.2 |
| Interface — Foundation Plan (DEL-002-02) | Foundation design produced here feeds the Foundation Plan drawing deliverable; coordinate with DEL-002-02 and DEL-002-10 | Decomposition §7 PKG-002 |
| Interface — Foundation Construction (DEL-010-01) | This design package is the direct technical basis for PKG-010 Foundation Construction | Decomposition §6, §7 |

---

## Construction

| Element | Description | Source |
|---|---|---|
| Building type | New maintenance shop addition (Addition) to existing West Dried Meat Lake Regional Landfill facility | RFP §1.0 |
| Structure | Concrete structure with 35-foot ceiling height | RFP §3.4, Appendix B (Shop) |
| Floor loads — general | Must accommodate heavy tracked and packer equipment; steel plate embedments in concrete floor at strategic locations (see Appendix B for locations) | RFP §3.4, Appendix B (Shop) |
| Floor loads — mezzanine | Load-bearing mezzanine capable of heavy items (oil totes, pumping equipment) above parts room, utility room, and wash bay | RFP §3.4, Appendix B (Shop) |
| Crane loads | Two 5-tonne overhead cranes on trolley; crane support structure details in DEL-002-07 | RFP §3.4, Appendix B (Shop) |
| Service pit / trench | Below-grade Service Pit for under-equipment servicing; structural details in DEL-002-06 | RFP §3.4, Appendix B (Shop) |
| Wash bay | Single enclosed bay (24 ft wide) for large equipment (motor scraper class); integrated with floor slab and mud sump connection | RFP §3.1, §3.4, Appendix B (Shop) |
| Foundation system | TBD — pending geotechnical investigation; ASSUMPTION: spread footings or continuous strip footings consistent with normal ground conditions for this region |  |
| Steel plate embedments | Steel plate embedments in concrete floor at locations shown on Appendix B (Shop) drawing | RFP §3.4, Appendix B (Shop) |
| Cistern interface | 50,000 L water storage cistern to be located within or adjacent to the building; foundation design must account for cistern loads | RFP §3.4, Appendix B (Shop) |

> **Enrichment note (E-001 — terminology normalization):** The term "steel plate embedments" is adopted as the consistent term across all four documents, replacing variant phrasings ("steel plates embedded in concrete floor," "steel plate embedment locations," "steel plate embedments at strategic floor locations"). (Source: RFP §3.4, Appendix B (Shop); _SEMANTIC_LENSING.md E-001)

---

## References

| Ref ID | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | Main RFP — §3.3.2 (scope of services), §3.4 (design requirements), §4.8.2 (foundation variable-price) |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan and structural notes; building footprint, ceiling height, crane, steel plate embedments |
| DECOMP | WDMLRL_Decomposition_Claude.md | Project decomposition — §3 SSOW (SOW-0019, SOW-0023), §5 Objectives (OBJ-003, OBJ-006), §7 PKG-002 deliverables |
| NBC | National Building Code of Canada (current edition) | Structural loads, seismic, snow, wind — applicable edition per Alberta adoption. **Note (E-003):** To be sourced by Structural Engineer from reference library; "location TBD" means the document has not been obtained for this deliverable file — the engineer of record must possess the governing edition. | location TBD |
| ABC | Alberta Building Code (current edition) | Provincial amendments to NBC; Alberta-specific requirements. **Note (E-003):** To be sourced by Structural Engineer from reference library. | location TBD |
| CSA A23.3 | Design of Concrete Structures | Concrete design standard — ASSUMPTION: applicable. **Note (E-003):** To be sourced by Structural Engineer from reference library. | location TBD |
| CSA S16 | Design of Steel Structures | Steel embedment design — ASSUMPTION: applicable. **Note (E-003):** To be sourced by Structural Engineer from reference library. | location TBD |

> **Enrichment note (E-003):** Clarified the meaning of "location TBD" for standard code references. These are industry-standard codes that the engineer of record is expected to possess; "location TBD" indicates the document has not been obtained or filed within the project deliverable folder, not that the document does not exist. (Source: Datasheet.md References table; _SEMANTIC_LENSING.md E-003)
