# Datasheet — DEL-011-06 Service Pit/Trench

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-011-06 |
| **Deliverable Name** | Service Pit/Trench |
| **Package** | PKG-011 — Building Structure & Envelope |
| **SOW Reference** | SOW-0028 |
| **Responsible Party** | General Contractor |
| **Deliverable Type** | Construction |
| **Discipline** | General Contractor (structural construction sub-scope) |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Completion Deadline** | December 31, 2026 |
| **Decomposition Revision** | R1 — 2026-02-25 |

**Sources:** _CONTEXT.md; WDMLRL_Decomposition_Claude.md §7 PKG-011 deliverable table and §8 Scope Ledger SOW-0028; RFP R-01 §3.4; Appendix B (Shop) R-04.

---

## Terminology Note

> This deliverable uses the term **"service pit"** as the primary designation. The term **"service trench"** appears in some sources (e.g., Appendix B floor plan labeling) and is treated as a synonym throughout this document set. If these terms refer to distinct geometries, the project team should clarify and establish the canonical term. *(Per Lensing Item B-003 — Normalization)*

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| **Feature Type** | Below-grade pit/trench in concrete floor | Decomposition Vocabulary Map; App B (Shop) R-04 |
| **Primary Function** | Under-equipment servicing by mechanics (standing below equipment) | RFP §3.4 |
| **Ventilation Requirement** | Ventilation required (type/capacity TBD); measurable performance criteria (air changes per hour or contaminant limits) TBD pending mechanical design (PKG-003) and Alberta OHS Code Parts 5/25 determination — see Specification REQ-011-06-02 | RFP §3.4; SOW-0028; *(enriched per Lensing Item F-003)* |
| **Lighting Requirement** | Artificial lighting within pit required; measurable illumination level (minimum lux) TBD pending electrical design (PKG-004) and applicable illumination standard (e.g., IESNA) — see Specification REQ-011-06-03 | RFP §3.4; SOW-0028; *(enriched per Lensing Item D-002)* |
| **Plan Location** | Right side of New North Shop main bay area, adjacent to 24'-wide repair bay column | App B (Shop) R-04 (conceptual — exact coordinates TBD per IFC drawings) |
| **Plan Dimensions** | TBD — conceptual drawing does not provide explicit pit dimensions; to be confirmed on IFC structural drawings (DEL-002-06). Structural engineer requires confirmed Owner equipment fleet dimensions before finalizing. | App B (Shop) R-04 — dimensions not labeled for pit itself; *(enriched per Lensing Items B-001, A-005)* |
| **Pit Depth** | TBD — to be determined by structural engineer per DEL-002-06 based on confirmed heavy equipment fleet undercarriage clearance data from Owner (Camrose County). ASSUMPTION: sufficient to allow upright working posture beneath heavy equipment. | ASSUMPTION; *(enriched per Lensing Item A-005 — Owner fleet data required)* |
| **Structural Form** | Concrete-lined pit/trench integrated into building slab | ASSUMPTION based on building type (concrete structure per App B); confirmed by DEL-002-06 scope |
| **Access** | TBD — entry/egress method (steps, stairs, ladder, or ramp) to be defined in structural and architectural IFC drawings. Selection affects pit end-wall structural detailing — decision required before DEL-002-06 can be finalized. Responsible: structural engineer and architect. | *(enriched per Lensing Item A-004 — decision path and responsible party noted)* |
| **Cover/Edge Protection** | Safety railings and edge protection required; pit cover/grating system type (removable steel grating vs. solid plate) TBD — clarification required on whether a cover system is mandatory or conditional. See Specification REQ-011-06-06 and REQ-011-06-11. | _CONTEXT.md Anticipated Artifacts; *(enriched per Lensing Item E-001)* |
| **Floor Material** | TBD — likely concrete or steel grating; to be confirmed per IFC drawings | |
| **Wall/Lining Material** | TBD — concrete structural lining assumed; finish to be confirmed per IFC drawings | ASSUMPTION |
| **Drainage** | TBD — pit floor drainage required (ASSUMPTION based on below-grade industrial maintenance environment). Drain location, pipe size, and connection point TBD pending plumbing design (PKG-006). Scope boundary (whether pit floor drainage is within this deliverable or PKG-006/PKG-014) requires clarification — see Guidance Conflict Table C-011-06-03 and C-011-06-04. | *(enriched per Lensing Items B-002, E-002)* |
| **Waterproofing/Damp-Proofing** | TBD — waterproofing or damp-proofing at pit base and wall/slab interface to be specified per IFC structural drawings. See Specification REQ-011-06-12. | *(added per Lensing Item C-002 — below-grade concrete structure requires waterproofing consideration)* |
| **Equipment Access** | Sized for heavy landfill maintenance equipment (motor scrapers, tracked/packer equipment). Confirmed fleet dimensions (undercarriage clearance, wheel/track gauge, overall length) required from Owner (Camrose County) — not yet received. | ASSUMPTION based on RFP §3.1, §3.4 general equipment context; *(enriched per Lensing Item A-005)* |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| **Jurisdiction** | Province of Alberta | RFP §2.22 |
| **Governing Code** | Alberta Safety Codes (Alberta Building Code) — specific edition TBD (see Specification Standards table) | RFP §3.3.2; *(enriched per Lensing Item A-001)* |
| **Ambient Environment** | Interior, heated building (forced air makeup air system in New North Shop) | App B (Shop) R-04; RFP §3.4 |
| **Occupancy Type** | Industrial maintenance shop | RFP §3.1 |
| **Temperature** | Heated interior — sub-zero ambient possible during construction (Alberta climate). Cold-weather concrete protection per CSA A23.1/ACI 306 may apply — see Guidance and Procedure Step 5.4. | ASSUMPTION; *(enriched per Lensing Item D-001)* |
| **Structural Loading** | Must support heavy equipment floor loads (tracked/packer equipment) adjacent to pit opening | RFP §3.4 (steel plates in floor for heavy equipment); ASSUMPTION that pit surround must accommodate similar loads |
| **OHS Requirements** | Confined space and fall protection provisions required per Alberta OHS Code. Confined space classification under Alberta OHS Code Part 5 requires confirmation — if classified as confined space, mandatory entry programs, atmospheric monitoring, and rescue provisions apply. If not classified, ASSUMPTION language should be removed. See Specification REQ-011-06-05. | ASSUMPTION; *(enriched per Lensing Item A-003 — classification determination pending)* |
| **Upstream Dependency** | Foundation (PKG-010) must be complete before pit excavation begins | _DEPENDENCIES.md |
| **Upstream Dependency** | Superstructure frame (DEL-011-01) may affect pit access during construction | _DEPENDENCIES.md |

---

## Construction

| Element | Description | Source |
|---|---|---|
| **Excavation** | Below-grade excavation within building footprint for pit/trench void. Dimensional tolerances TBD per IFC drawings (see Specification REQ-011-06-09). | _CONTEXT.md (SOW-0028 description); *(enriched per Lensing Item X-001)* |
| **Structural Construction** | Concrete structural walls, floor slab, and integration with building slab system. Concrete mix design (mix, slump, air content, cure duration) TBD per IFC drawings and DEL-002-06 — see Specification REQ-011-06-04. | ASSUMPTION based on building construction type (concrete, 35' ceiling) per App B; structural details per DEL-002-06; *(enriched per Lensing Item A-002)* |
| **Waterproofing** | Waterproofing or damp-proofing at pit base and wall/slab interface — method and materials TBD per IFC drawings. See Specification REQ-011-06-12. | *(added per Lensing Item C-002)* |
| **Lining and Finishing** | Pit lining and finishing installation (material and finish TBD per IFC drawings). Acceptance criteria (surface flatness tolerance, coating thickness, adhesion test) TBD — see Specification REQ-011-06-10. | _CONTEXT.md Anticipated Artifacts; *(enriched per Lensing Item C-003)* |
| **Safety Railings** | Edge protection and safety railing installation at pit perimeter. Minimum top rail height TBD (ASSUMPTION: 1,070 mm per Alberta OHS Code Part 9); mid-rail and toe board requirements TBD — see Specification REQ-011-06-06. | _CONTEXT.md Anticipated Artifacts; *(enriched per Lensing Item F-001)* |
| **Cover/Grating System** | Pit cover or grating system — type and specification TBD. Whether cover system is required (mandatory) or conditional ("if specified") requires clarification — see Specification REQ-011-06-11 and Guidance Conflict Table. | *(enriched per Lensing Item E-001)* |
| **Ventilation Rough-In** | Ventilation system provisions to be coordinated with PKG-003 (Mechanical Design) and PKG-013 (Mechanical & HVAC Installation) | ASSUMPTION: mechanical coordination required |
| **Lighting Rough-In** | Lighting provisions to be coordinated with PKG-004 (Electrical Design) and PKG-015 (Electrical & Low-Voltage Installation) | ASSUMPTION: electrical coordination required |
| **Contractor Responsible** | General Contractor | _CONTEXT.md |

---

## References

| Ref ID | Document | Section / Note |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.4 Design Requirements — "Ventilated and lighted service pit area for mechanics to perform servicing under equipment" |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | New North Shop conceptual floor plan — service trench shown in main bay, right side |
| DECOMP | WDMLRL_Decomposition_Claude.md | §3 SOW-0028; §7 PKG-011 DEL-011-06; §2 Vocabulary Map ("Service Pit") |
| _CONTEXT | _CONTEXT.md | Deliverable identification, description, anticipated artifacts |
| _DEPS | _DEPENDENCIES.md | Upstream/downstream dependencies |
| DEL-002-06 | Service Pit / Trench Structural Details (PKG-002) | Structural drawing set — IFC drawings not yet produced; location TBD |
| _SEM_LENS | _SEMANTIC_LENSING.md | Pass 3 enrichment source — 21 warranted items applied 2026-02-26 |
