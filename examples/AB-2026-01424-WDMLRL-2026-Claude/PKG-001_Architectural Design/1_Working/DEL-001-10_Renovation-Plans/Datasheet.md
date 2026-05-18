# Datasheet — DEL-001-10 Old North Shop Renovation Plans

**Document Type:** Datasheet (descriptive)
**Deliverable ID:** DEL-001-10
**Last Updated:** 2026-02-26
**Status:** SEMANTIC_READY

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-001-10 |
| Deliverable Name | Old North Shop Renovation Plans |
| Package | PKG-001 — Architectural Design |
| Deliverable Type | Drawing Set |
| Responsible Party | Architect |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price Contract |
| Project Location | SW 14–44–21–W4, near Ferintosh, Alberta |
| Completion Deadline | December 31, 2026 |
| Decomposition Reference | `_Decomposition/WDMLRL_Decomposition_Claude.md` — DEL-001-10 row, §7 PKG-001 table |

---

## Attributes

### Terminology Note (Lensing item X-003)

The following canonical terms are established for the washroom and locker room areas to ensure consistent terminology across all four documents:
- **"Washroom"** — refers to the existing washroom below the mezzanine being renovated (SOW-0072) and expanded with a urinal (SOW-0074)
- **"Locker room"** — refers to the new locker/change room with laundry services (SOW-0073)
- **"Washroom/locker room"** — refers to the combined cluster of SOW-0072, SOW-0073, and SOW-0074 when discussed as a co-located functional zone

Previous drafts used varying terms including "washroom/change room," "locker/change room," "washroom facilities," and "change room." These have been retained where they appear in source-quoted text but the canonical terms above should govern new content and construction document references. (Source: Lensing item X-003; all four production documents.)

### Scope Summary

DEL-001-10 is the architectural drawing set documenting the renovation of the existing Old North Shop building at the West Dried Meat Lake Regional Landfill. It covers five scope-of-work items:

| SOW ID | Description | Source |
|---|---|---|
| SOW-0070 | Renovate 250 sq ft kitchenette area in existing building | RFP §3.4; Decomposition §3-I |
| SOW-0071 | Renovate Old North Shop mezzanine (2nd-level coffee room) | App B (Shop); Decomposition §3-I |
| SOW-0072 | Renovate existing washroom below mezzanine in Old North Shop | App B (Shop); Decomposition §3-I |
| SOW-0073 | Construct new locker/change room with laundry services | RFP §3.4; Decomposition §3-I |
| SOW-0074 | Expand washroom facilities to include urinal | RFP §3.4; Decomposition §3-I |

### Objectives Supported

| Objective ID | Statement (abbreviated) | Association Basis |
|---|---|---|
| OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition and associated renovations | Decomposition §5, OBJ-001 row; SOW-0070–SOW-0074 listed |
| OBJ-003 | Produce complete, P.Eng.-stamped IFC design documentation across all disciplines | Decomposition §5, OBJ-003 row; PKG-001 deliverables listed |

**ASSUMPTION (package-grouping heuristic):** OBJ-001 and OBJ-003 are associated with DEL-001-10 because the decomposition's Objective-to-Deliverable mapping lists this deliverable in the PKG-001 table under these objectives. The mapping is by package group, not by individual deliverable ID; treat as directionally relevant context.

### Downstream Construction Deliverables (drawing consumers)

The renovation drawings produced by DEL-001-10 are consumed by construction packages in PKG-017:

| Construction Deliverable | Description | SOW |
|---|---|---|
| DEL-017-01_Kitchenette-Reno | Kitchenette Renovation | SOW-0070 |
| DEL-017-02_Mezzanine-Reno | Old North Shop Mezzanine Renovation | SOW-0071 |
| DEL-017-03_Washroom-Reno | Washroom Renovation & Expansion | SOW-0072, SOW-0074 |
| DEL-017-04_Locker-Room | New Locker/Change Room | SOW-0073 |

Source: Decomposition §7 PKG-017 table. Note: Formal downstream dependency tracking is NOT_RUN_YET per `_DEPENDENCIES.md`.

---

## Conditions

### Project Conditions

| Condition | Value | Source |
|---|---|---|
| Existing building being renovated | Old North Shop | App B (Shop) |
| Old North Shop footprint (approximate) | 105 ft wide × 40 ft deep (approx 4,200 sq ft) | App B (Shop) — plan dimensions; see note |
| Existing mezzanine | 2nd-level coffee room, located within Old North Shop at west end of building | App B (Shop) |
| Existing washroom | Located below mezzanine in Old North Shop | App B (Shop) |
| Kitchenette area | 250 sq ft | RFP §3.4 |
| Relationship to New North Shop | Old North Shop adjoins the New North Shop; total combined plan length shown as 235 ft | App B (Shop) |
| Completion deadline | All work on or before December 31, 2026 | RFP §3.1 |
| Governing jurisdiction | Province of Alberta | RFP §2.22 |
| Contract form | CCDC 14–2013 Design-Build Stipulated Price | RFP §2.7 |

**Note on Old North Shop dimensions:** Appendix B shows the Old North Shop as occupying approximately 105 ft of the 235 ft overall building width, with a 40 ft depth shared with the New North Shop plan depth. The 40 ft depth dimension shown on App B applies to the combined building section. The Old North Shop-specific internal depth is TBD pending confirmed as-built drawings.

**CAUTION (Lensing item B-003):** The dimensions cited above (approximately 105 ft wide x 40 ft deep, approx 4,200 sq ft) are derived from Appendix B (Shop), which is a conceptual drawing for the New North Shop that shows the Old North Shop as contextual background only. These dimensions should not be relied upon for renovation design. See Guidance Conflict Table CONF-001. The confirmed Old North Shop internal depth dimension shall be recorded here once the field survey (Procedure Step 1) is complete. (Source: App B (Shop); Guidance.md CONF-001.)

**Action required (Lensing item B-001):** Once the Architect of Record completes the field survey of the Old North Shop (Procedure Step 1), the confirmed internal depth dimension and total verified footprint shall be entered in this Conditions table to replace the approximate values. No mechanism currently ensures this update occurs; the Architect of Record should flag this table for update upon survey completion. (Source: Datasheet.md Conditions; Procedure.md Step 1.)

### Regulatory Conditions

| Condition | Source |
|---|---|
| Building must adhere to all applicable Alberta Safety Codes | RFP §3.3.2 |
| All IFC Drawings must be signed/stamped by a P.Eng. licensed in Alberta | RFP §3.3.2 |
| Development permit and building permit required from the County | RFP §3.3.2 |
| Governing law is Province of Alberta | RFP §2.22 |
| Specific code edition (e.g., Alberta Building Code 2019) | ASSUMPTION: likely applicable — exact edition not cited in RFP; location TBD |

---

## Construction

### Existing Conditions Baseline (Lensing item E-002)

This subsection is a placeholder to be populated after the Architect of Record completes the existing conditions field survey (Procedure Step 1). The as-found conditions documented here will serve as the assessment baseline for the renovation design, enabling judgment of whether the renovation intent (documented in the program elements below) is achieved.

| Baseline Item | Value | Survey Date | Recorded By |
|---|---|---|---|
| Old North Shop verified internal dimensions (L x W x H) | TBD | TBD | TBD |
| Mezzanine dimensions and structural framing type | TBD | TBD | TBD |
| Existing washroom dimensions and configuration | TBD | TBD | TBD |
| Existing kitchenette area dimensions | TBD | TBD | TBD |
| Existing mechanical/plumbing rough-in locations | TBD | TBD | TBD |
| Existing electrical panel and branch circuits | TBD | TBD | TBD |
| Existing door/window inventory | TBD | TBD | TBD |
| Photographic record filed | TBD | TBD | TBD |

(Source: Lensing item E-002 — documented assessment evidence requires a baseline. Currently the Datasheet describes the anticipated program but has no section for as-found conditions.)

### Coordination Dependency Tracking (Lensing item E-003)

| Dependency | Deliverable | Status | Last Checked |
|---|---|---|---|
| Demolition Plans (required upstream for renovation design basis) | DEL-001-09 | TBD — not yet tracked | TBD |

**Note (Lensing item E-003):** DEL-001-09 (Demolition Plans) is a required upstream input whose production status must be tracked to validate the renovation design basis. The status shown above should be updated when DEL-001-09 production status is confirmed. (Source: Procedure.md Information Prerequisites — DEL-001-09 row; Datasheet.md References table.)

---

### Renovation Areas and Program Elements

The following renovation areas and program elements are identified from source documents:

#### Kitchenette (SOW-0070)
- Renovation of existing 250 sq ft kitchenette area within the Old North Shop
- Source: RFP §3.4 ("Renovate 250 square foot kitchenette area located in the existing building")
- Specific fitout details: TBD (RFP references concept only; design-build responsibility)

#### Mezzanine — 2nd Level Coffee Room (SOW-0071)
- Renovation of the existing 2nd-level mezzanine/coffee room within the Old North Shop
- Appendix B note: "Old North Shop Mezzanine to be renovated"
- Mezzanine location: West section of Old North Shop, above existing lower level
- Load requirements for mezzanine: TBD (structural to confirm; coordinate with PKG-002)
- Source: App B (Shop)

#### Washroom (SOW-0072, SOW-0074)
- Renovation of existing washroom located below the mezzanine in the Old North Shop
- Expansion to include urinal
- Expansion to include locker/change room with laundry services
- Source: App B (Shop); RFP §3.4 ("Expand washroom facilities to include urinal and locker change room, including laundry services")

#### Locker/Change Room (SOW-0073)
- Construction of new locker/change room
- Includes laundry services
- Source: RFP §3.4; App B (Shop) — "new locker room" noted

### Drawing Set Composition (Anticipated Artifacts)

Per `_CONTEXT.md` anticipated artifacts, the drawing set is expected to include:

- Renovation plan drawings for Old North Shop (kitchenette, mezzanine, washroom, locker room)
- ASSUMPTION: The drawing set will include, at minimum: existing conditions plan (or reference to DEL-001-09 Demolition Plans), renovation floor plan(s), interior elevations of key renovation areas, door/window schedule references, and finish notes.
- Relationship to DEL-001-09: DEL-001-09 (Old North Shop Demolition Plans) covers SOW-0070, SOW-0071, SOW-0072 and is the predecessor demolition document. DEL-001-10 renovation plans build on the post-demolition conditions.

---

## References

| Ref ID | Document | Relevance to DEL-001-10 | Accessibility |
|---|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | Main RFP — §3.1 project background, §3.3 scope of work, §3.4 design requirements including kitchenette (250 sq ft), washroom expansion, locker room | Accessible |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan showing Old North Shop layout, mezzanine/coffee room, washroom location, dimensions | Accessible |
| DECOMP | WDMLRL_Decomposition_Claude.md | SOW-0070–SOW-0074 definitions, PKG-001 deliverable table, OBJ-001/OBJ-003 statements | Accessible |
| R-02 | AB-2026-01424-Addendum 1.pdf | Addendum No. 1 (Feb 19, 2026) — adds §4.11 Bid Security; renovation scope unchanged | Not reviewed (not listed in _REFERENCES.md as relevant to this deliverable) |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf | Electrical conceptual layout — coordination reference for renovated spaces | Not reviewed for this deliverable |
| R-06 | AB-2026-01424-Appendix B (Plumbing).pdf | Plumbing layout — coordination reference for washroom/kitchenette renovations | Not reviewed for this deliverable |
