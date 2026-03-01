# Datasheet — DEL-017-01 Kitchenette Renovation

**Document Type:** Datasheet (Descriptive)
**Deliverable ID:** DEL-017-01
**Revision:** R1 — 2026-02-26 (Pass 3 Semantic Lensing Enrichment)
**Status:** SEMANTIC_READY

---

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-017-01 |
| Title | Kitchenette Renovation |
| Package | PKG-017 — Existing Building Renovation (Old North Shop) |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Responsible Party | General Contractor |
| Deliverable Type | Construction |
| SOW Reference | SOW-0070 |
| Objective Reference | OBJ-001 |
| Decomposition Reference | WDMLRL_Decomposition_Claude.md — §7, PKG-017 |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price Contract |
| Completion Deadline | December 31, 2026 (Source: RFP §3.1) |

---

## Attributes

| Attribute | Value | Source | Notes |
|-----------|-------|--------|-------|
| Location | Old North Shop (existing building) | RFP §3.1, App B (Shop) | Building footprint approx. 105' x 40'. **Note:** The spatial identity of the "kitchenette" relative to the "2nd Level Mezzanine Coffee Room" and "Wash Station" shown in Appendix B (Shop) is ambiguous — see Guidance.md CF-001 for resolution path. (Lensing: B-001) |
| Kitchenette Area | 250 sq ft | RFP §3.4 / SOW-0070 | Explicit in RFP Design Requirements. **ASSUMPTION (measurement basis TBD):** It is not defined whether this figure represents net interior area, gross area, or a programmatic allocation. Different interpretations could yield materially different design outcomes. Clarification required from RFP / Owner / Architect. (Lensing: B-003) |
| Building | Old North Shop — existing maintenance shop building | RFP §3.1, App B | Distinct from the new 13,000 sq ft Addition |
| Work Category | Interior renovation | _CONTEXT.md | Removal of existing, installation of new |
| Scope Narrative | Full renovation of existing kitchenette space including removal of existing fixtures, updates to plumbing and electrical, installation of new cabinetry and appliances, and finishing work | _CONTEXT.md | |
| Fixture Scope | TBD | — | Specific fixture list subject to design phase and IFC drawings (PKG-001, PKG-006). Resolution expected upon design completion. (Lensing: B-002) |
| Plumbing Updates | TBD | — | Scope of plumbing modifications to be defined in design (PKG-006); existing service capacity requires verification (UTILITY-001). Resolution expected upon design completion. (Lensing: B-002) |
| Electrical Updates | TBD | — | Scope of electrical modifications to be defined in design (PKG-004); existing service capacity requires verification (UTILITY-001). Resolution expected upon design completion. (Lensing: B-002) |
| Cabinetry | TBD | — | Type, material, and configuration subject to design and Owner approval. **Procurement responsibility TBD:** It is unclear whether cabinetry is Contractor-furnished or Owner-furnished. The Specification Documentation table lists "Equipment/Appliance Schedule" produced by "Architect / Owner," implying Owner involvement in procurement, but Specification REQ-007 states "supplied and installed" without clarifying procurement responsibility. Clarification required from Owner / Contract terms. (Lensing: E-001) |
| Appliances | TBD | — | Appliance list and specifications subject to design and Owner approval. **Procurement responsibility TBD:** Same ambiguity as Cabinetry — see note above. Procurement responsibility affects construction sequencing, warranty, and cost allocation. (Lensing: E-001) |
| Finishes | TBD | — | Interior finish standard to be determined in design (PKG-001); must conform to finishes standard per RFP §3.3.2. Resolution expected upon design completion. (Lensing: B-002) |

---

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| Existing Conditions Survey | Survey and photos of existing kitchenette required before design and demolition begin | _DEPENDENCIES.md (EXISTING-001) |
| Design Approval | Kitchenette design plan must be approved before construction proceeds | _DEPENDENCIES.md (DESIGN-001) |
| Utility Capacity Verification | Existing plumbing and electrical service capacity must be confirmed before rough-in work | _DEPENDENCIES.md (UTILITY-001) |
| Building Envelope | ASSUMPTION: Kitchenette renovation can proceed after building envelope of Old North Shop is confirmed serviceable. Coordination required with DEL-017-02 and DEL-017-03 activities. | _DEPENDENCIES.md |
| Occupancy | ASSUMPTION: Old North Shop may remain partially operational during renovation; phasing to be confirmed with Owner at design stage. | — |
| Code Compliance | All work must comply with applicable Alberta Building Code and Alberta Safety Codes | RFP §3.3.2, §3.4 |
| Project Completion | All work, including this renovation, must be complete on or before December 31, 2026 | RFP §3.1 |

---

## Construction

| Element | Description | Source |
|---------|-------------|--------|
| Demolition | Removal of existing kitchenette fixtures, cabinetry, finishes, and associated rough-in as required | _CONTEXT.md |
| Plumbing Rough-In | Update/extend plumbing to serve new kitchenette layout | _CONTEXT.md; SOW-0070 (inferred from "renovation" scope) |
| Electrical Rough-In | Update/extend electrical circuits to serve new kitchenette layout | _CONTEXT.md; SOW-0070 (inferred from "renovation" scope) |
| Cabinetry Installation | Install new cabinetry per approved design | _CONTEXT.md |
| Appliance Installation | Install appliances per approved design | _CONTEXT.md |
| Finishing Work | Apply interior finishes (flooring, wall finish, ceiling finish) per approved design and finish schedule | _CONTEXT.md; DEL-001-08 (Finish Schedule, PKG-001) |
| IFC Drawings | All construction must follow IFC drawings signed/stamped by P.Eng. licensed in Alberta | RFP §3.3.2 |
| Inspection | All inspections to be submitted by Contractor; County representative to be present; copies of reports provided to County | RFP §3.3.2 |
| Warranty | All materials and workmanship guaranteed for construction period plus 2-year post-CCC guarantee period | RFP §2.10 |

---

## References

| Ref ID | Document | Relevance |
|--------|----------|-----------|
| R-01 | AB-2026-01424-WDMLRL_RFP.pdf | §3.4 — defines 250 sq ft kitchenette renovation requirement; §3.1 — project background and deadline; §3.3.2 — Contractor scope and code compliance |
| R-04 | AB-2026-01424-Appendix_B_(Shop).pdf | Conceptual floor plan of Old North Shop showing building layout and relationship of spaces |
| SOW-0070 | Structured Scope of Work item | "Renovate 250 sq ft kitchenette area in existing building" — the primary scope statement |
| OBJ-001 | Project Objective | Code-compliant, fully functional facility satisfying County operational program |
| WDMLRL_Decomposition_Claude.md | Project Decomposition | §7 PKG-017 deliverable table; §3 SSOW Section I; §5 Objectives |
| _CONTEXT.md | Deliverable context file | Scope narrative, package/objective alignment, authority references |
| _DEPENDENCIES.md | Deliverable dependencies file | Upstream dependencies: EXISTING-001, DESIGN-001, UTILITY-001 |
