# Datasheet — DEL-05-03: Option — Access Control

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-05-03_Optional-Access-Control |
| **Name** | Option — Access Control |
| **Package** | PKG-005 Optional Priced Items & Owner-Elected Additions |
| **Discipline** | Security / IT |
| **Type** | Optional scope package (4-doc bundle) |
| **Responsible Party** | Design-Builder |
| **Scope Coverage** | SOW-0502 |
| **Objective Support** | OBJ-010 |
| **Status** | Optional priced item — not included in base price unless Owner elects |

## Attributes

| Attribute | Value | Source | Confidence |
|---|---|---|---|
| **Building scope** | Main building (PSB) only | OSR S12.3 | Confirmed |
| **Ancillary buildings included?** | No — explicitly excluded | OSR S12.3 | Confirmed |
| **Number of zones** | Multiple (exact count DB-proposed; minimum zone count shall be derived from Functional Program room groupings, currently identifying minimum 8 key-fob-access rooms that DB must organize into logically distinct zone groupings — see Procedure Step A2) | OSR S12.3; Functional Program (Appendix B), page 46 of RFP | Confirmed (minimum room list); **ASSUMPTION** (zone grouping approach from B-001) |
| **Zone purpose** | Shared space use and interdepartmental access control | OSR S12.3 | Confirmed |
| **Estimated number of controlled doors** | TBD (minimum 8 doors corresponding to the 8 Functional Program key-fob rooms; actual count depends on DB zoning concept and architectural door schedule) | Functional Program (Appendix B), page 46 of RFP; _CONTEXT.md | **ASSUMPTION** (minimum count derived from room list) |
| **Estimated number of credential holders** | TBD — depends on Fire Department and Public Works staff headcount; DB to confirm with Owner before finalizing system sizing (item B-003: total credentialed user count and visitor credential requirements) | TBD — no source available; ASSUMPTION per B-003 | TBD |
| **Access control technology** | TBD (key fob access referenced in Functional Program; system type to be proposed by DB) | Functional Program (Appendix B), page 46 of RFP | Confirmed (key fob minimum) |
| **Device schedule** | TBD — to be produced by DB as part of this deliverable | _CONTEXT.md (Anticipated Artifacts) | Confirmed |
| **Pricing sheet** | TBD — separable pricing required | _CONTEXT.md (Anticipated Artifacts); OSR S12 | Confirmed |
| **Integration with base building IT** | TBD — coordination with DEL-02-06 electrical/IT package; **ASSUMPTION:** likely required | ASSUMPTION | **ASSUMPTION** |
| **Integration with security/camera system** | TBD — DEL-05-04 is a separate optional item; interface boundaries TBD | Decomposition (PKG-005) | Confirmed (separate item) |
| **Provincial licensing requirements** | TBD — confirm whether Alberta-specific access control licensing or installer certification requirements apply (e.g., Alberta Security Services and Investigators Act); see Specification.md TBD-F003 for related DB qualification question | TBD — no source accessed; **ASSUMPTION:** likely applicable for security system installation in Alberta | TBD |

## Conditions

| Condition | Description | Source | Confidence |
|---|---|---|---|
| **Operational context** | Combined Fire Department and Public Works facility with shared spaces; interdepartmental access control is the primary driver | OSR S12.3; OSR S10.2 | Confirmed |
| **Shared space requirement** | Access control must accommodate shared-space use (e.g., kitchen/breakroom, meeting room, training room) while securing departmental or restricted areas | OSR S12.3 | Confirmed |
| **Key fob access rooms** | Functional Program identifies the following rooms as "Key Fob Access": Mechanical/sprinkler room, Electrical room, Janitor room, IT room, Station office, Map Work Office, Bay Warehousing, Map Work/Storage (note: Exterior Sand Shed listed in Functional Program but excluded from contract scope per Addendum 03) | Functional Program (Appendix B), page 46 of RFP | Confirmed |
| **Excluded facilities** | Ancillary buildings (cold storage building) are explicitly excluded from the access control system | OSR S12.3 | Confirmed |
| **Optional item pricing** | Pricing must be separable from base scope and clearly identifiable as an Owner-elected addition | OSR S12; Decomposition PKG-005 | Confirmed |
| **24/7 operations** | Fire Department operates 24/7; access control system must function reliably without interruption | **ASSUMPTION** (inferred from 24/7 emergency operations requirement; OSR S10.2) | **ASSUMPTION** |

## Construction

| Element | Description | Source | Confidence |
|---|---|---|---|
| **Zoning concept** | DB to propose a zoning concept identifying control zones within the main building, reflecting interdepartmental and shared-space boundaries | OSR S12.3; _CONTEXT.md | Confirmed |
| **Device schedule** | DB to produce a device schedule listing reader locations, door hardware (e.g., electromagnetic lock, electric strike), controllers, and credential types (e.g., key fobs) per zone | _CONTEXT.md; Functional Program (Appendix B) | Confirmed |
| **Credential type** | Key fob referenced in Functional Program; DB may propose alternate or supplemental credentials (e.g., PIN pad, card reader) | Functional Program (Appendix B), page 46 of RFP | Confirmed (minimum) |
| **System controller/head-end** | TBD — DB to propose panel/controller location and management interface | TBD | TBD |
| **Maximum cable run / topology constraint** | TBD — DB to confirm during detailed design (Step B2) maximum reader-to-panel cable run distance and system topology constraints based on proposed equipment (item B-002; affects device schedule feasibility) | TBD — equipment-dependent | TBD |
| **Power supply** | TBD — **ASSUMPTION:** access control panels to be on emergency power circuit to maintain function during power interruptions given 24/7 Fire operations | ASSUMPTION | **ASSUMPTION** |
| **Conduit and cabling** | TBD — **ASSUMPTION:** low-voltage conduit/cabling coordinated with base building electrical (DEL-02-06) | ASSUMPTION | **ASSUMPTION** |
| **Door hardware integration** | TBD — coordination with architectural door schedule required | ASSUMPTION | **ASSUMPTION** |
| **Fire alarm integration** | TBD — **ASSUMPTION:** electromagnetic locks on fire-separation doors must release on fire alarm activation; coordination with fire alarm system required | **ASSUMPTION** (standard practice for electromagnetic-lock-equipped doors on fire-separation paths) | **ASSUMPTION** |
| **Monitoring / management interface** | TBD — DB to advise on local vs. remote management capability | TBD | TBD |
| **Pricing sheet** | Lump sum or itemized-by-zone pricing sheet to be included as a separable optional price | _CONTEXT.md; OSR S12 | Confirmed |

## References

| Reference | Relevance | Accessibility |
|---|---|---|
| OSR (Appendix A) S12.3 — Access Control | Primary requirement statement for this optional item | Accessible (RFP PDF, page 44) |
| OSR (Appendix A) S12 — Additional Optional Items | Establishes optional pricing framework for all optional items in PKG-005 | Accessible (RFP PDF, page 44) |
| Functional Program (Appendix B) — page 46 of RFP | Identifies rooms with Key Fob Access designation and informs zone concept | Accessible (RFP PDF, page 46) |
| RFP 2024_004 — General (Design-Build requirements) | Contract framework, delivery model, AB code compliance | Accessible |
| Decomposition DEL-05-03 entry | Deliverable definition, scope coverage, objective support | Accessible |
| Alberta Building Code / National Building Code of Canada | **ASSUMPTION:** likely applicable to door hardware and egress requirements | Not directly accessed; location TBD |
| Alberta Fire Code | **ASSUMPTION:** likely applicable for access-controlled doors on fire-separation paths | Not directly accessed; location TBD |
| UL 294 (Access Control System Units) | **ASSUMPTION:** likely applicable standard for access control equipment | Not directly accessed; location TBD |
| ANSI/BHMA A156.25 (Electrified Locks and Strikes) | **ASSUMPTION:** likely applicable for electrified lock hardware | Not directly accessed; location TBD |
| CSA C22.1 (Canadian Electrical Code) | **ASSUMPTION:** likely applicable for low-voltage wiring | Not directly accessed; location TBD |
| CSA B651 (Accessible Design for the Built Environment) | **ASSUMPTION:** may be applicable for reader mounting height and barrier-free access at controlled doors | Not directly accessed; location TBD |
| Alberta Security Services and Investigators Act | TBD — may impose installer certification requirements for security system installation | Not directly accessed; location TBD |
