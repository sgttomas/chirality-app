# Specification — DEL-002-09 Stair Details

---

## Scope

### In Scope

This deliverable covers the production of an Issued For Construction (IFC) structural drawing set providing complete structural details for the stair(s) accessing the overhead mezzanine within the New North Shop building at the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. The drawing set shall include all information required by the construction contractor (PKG-011) to build the stair structure, including member sizes, connection details, anchorage to the concrete structure, and any integral guardrail or handrail attachments that are structural in nature.

The stair serves the mezzanine storage level above the Parts Room, Utility Room, and Wash Bay as shown on Appendix B (Shop) conceptual drawing (R-04).

### Out of Scope

- Architectural finish selections for stair treads, nosings, or soffits (PKG-001 responsibility).
- Mechanical or electrical systems serving the mezzanine or stair (PKG-003, PKG-004 responsibility).
- Foundation design (DEL-002-11, variable-price scope).
- Structural calculations for the stair (covered by DEL-002-10 Structural Calculation Package).
- Mezzanine framing itself (covered by DEL-002-05 Mezzanine Framing Details).
- Construction execution (covered by PKG-011 DEL-011-07).

---

## Requirements

### REQ-001 — Stair Provision
The structural drawing set shall detail a stair providing access between the main shop floor level and the mezzanine level above the Parts Room, Utility Room, and Wash Bay.
- **Source:** R-04 (App B floor plan, "Stairs to Mezzanine" notation); Decomposition SOW-0034.
- **Status:** Confirmed requirement.

### REQ-002 — Mezzanine Load Compatibility
The stair structure shall be compatible with, and shall not compromise, a mezzanine rated for heavy storage loads, including oil totes and oil pumping equipment.
- **Source:** R-01 §3.4 ("Mezzanine storage above utility and parts room capable of handling heavy items such as several oil totes and oil pumping equipment"); Decomposition SOW-0033.
- **Status:** Confirmed requirement.

### REQ-003 — Concrete Structure Integration
The stair shall be designed to connect and anchor into the concrete superstructure of the New North Shop.
- **Source:** R-01 §3.4 ("Concrete structure 35' ceiling"); R-04 (App B note "Concrete Structure (35' Ceiling)").
- **Status:** Confirmed requirement.

### REQ-004 — Code Compliance
The stair design shall comply with all applicable Alberta Safety Codes and the Alberta Building Code, including requirements for minimum stair width, maximum riser height, minimum tread depth, handrail and guardrail heights, and structural live loads.
- **Source:** R-01 §3.3.2 ("The building design must adhere to all applicable building codes and regulations"); R-01 §3.4 ("The proposed building must adhere to all Alberta Safety Codes").
- **Status:** Confirmed requirement.
- **Note:** Specific clause references within the Alberta Building Code and Safety Codes are not available in the accessible source materials (location TBD). ASSUMPTION: The Alberta Building Code (current edition at time of permit application) governs.
- **[A-001] Enrichment:** TBD -- Identify the specific Alberta Building Code edition and clause numbers governing stair geometry, live loads, and guardrails. Without edition year and clause references, prescriptive direction for code compliance is incomplete. **Proposed authority:** Structural Engineer / Building Code authority.

### REQ-005 — P.Eng. Stamp
All IFC drawings in this set shall be signed and stamped by a Professional Engineer licensed to practice in the Province of Alberta.
- **Source:** R-01 §3.3.2 ("All Issued For Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta").
- **Status:** Confirmed requirement.

### REQ-006 — Handrail and Guardrail Structural Details
The drawing set shall include structural details for handrails and guardrails associated with the stair and at the mezzanine landing edge, sufficient for the construction contractor to fabricate and install code-compliant assemblies.
- **Source:** R-01 §3.3.2 (code compliance); R-01 §3.4 (Alberta Safety Codes).
- **Status:** ASSUMPTION — inferred from code compliance requirement and standard structural engineering practice for mezzanine stairs. Specific RFP clause not found.

### REQ-007 — Coordination with Mezzanine Framing
The stair structural details shall be coordinated with DEL-002-05 (Mezzanine Framing Details) to ensure compatible connection details, load transfer paths, and dimensional alignment.
- **Source:** Decomposition PKG-002 deliverable structure; standard structural engineering practice.
- **Status:** ASSUMPTION — no explicit cross-reference requirement stated in RFP; inferred from coordinated drawing set requirement (OBJ-003).

### REQ-008 — IFC Drawing Set Format
The drawing set shall be formatted and organized as Issued For Construction documents, suitable for building permit submission and contractor execution.
- **Source:** R-01 §3.3.2.
- **Status:** Confirmed requirement.

---

## Standards

> **[F-001] Enrichment note:** For each standard below, the edition year should be specified or confirmed as "current edition at time of permit application," and the design team should verify that the standard text is available to the team. Justified conformance requires knowing which edition is being designed to. This remains TBD pending confirmation by the Structural Engineer.

| Standard | Applicability | Edition | Availability |
|---|---|---|---|
| Alberta Building Code | Structural design of stairs, handrails, guardrails, loads | TBD -- confirm specific edition year (ASSUMPTION: current edition at time of permit application) | ASSUMPTION -- likely applicable; location TBD. Confirm standard text is available to design team. |
| Alberta Safety Codes Act and associated regulations | All aspects of building design in Alberta | TBD -- confirm current edition | Confirmed applicable -- R-01 section 3.4; location TBD |
| CCDC 14-2013 | Contract form governing the overall design-build | 2013 | R-01 section 2.7 |
| CSA S16 (Steel structures) | Steel stair framing if steel construction adopted | TBD -- confirm edition if steel selected | ASSUMPTION -- likely applicable if steel is selected; location TBD |
| CSA A23.3 (Concrete structures) | Concrete stair construction if concrete adopted | TBD -- confirm edition if concrete selected | ASSUMPTION -- likely applicable if concrete is selected; location TBD |
| National Building Code of Canada (NBC) | Alberta Building Code incorporates or references NBC; seismic provisions may apply (see [C-003]) | TBD -- confirm edition | ASSUMPTION -- location TBD |

---

## Verification

| Requirement | Verification Approach |
|---|---|
| REQ-001 — Stair provision | Drawing set review: confirm stair is shown at correct location connecting main floor to mezzanine |
| REQ-002 — Mezzanine load compatibility | Structural calculation review (DEL-002-10) and drawing set check for load path continuity. **[X-003] Enrichment:** Once live load design value is established, record it here as an explicit numeric acceptance criterion (e.g., "stair live load >= X kPa per ABC clause Y"). A binding determination requires a numeric threshold, not just a process check. |
| REQ-003 — Concrete structure integration | Drawing review: confirm anchorage details reference concrete substrate; check embedment/connection details |
| REQ-004 — Code compliance | P.Eng. review and building permit authority review; field inspection during construction (PKG-011). **[A-003] Enrichment:** Strengthen by specifying which ABC clauses will be checked and by what method (e.g., dimension check of riser height, tread depth, stair width, handrail height against specific ABC table references -- TBD until ABC edition is confirmed per [A-001]). Current verification approach is necessary but insufficient for compliance determination without clause-level specificity. |
| REQ-005 — P.Eng. stamp | Check drawings for valid Alberta P.Eng. stamp and signature prior to IFC release |
| REQ-006 — Handrail/guardrail details | Drawing set review: confirm handrail and guardrail details are present and call out code-required dimensions |
| REQ-007 — Coordination with mezzanine framing | Cross-check DEL-002-05 and DEL-002-09 drawing sets for compatible connection details and datums |
| REQ-008 — IFC format | Document control review: confirm IFC revision status and title block completeness |
| **[D-001] County preliminary design approval** | **Enrichment:** Verify that County approval of the preliminary stair design (Procedure Step 5) has been obtained and recorded before IFC issue. This is a precondition to conformance ruling for REQ-008. Source: R-01 section 3.3.2; Procedure Step 5. |
| **[C-001] Geotechnical prerequisite receipt** | **Enrichment:** Verify that the geotechnical investigation report (Procedure Prerequisites) has been received before stair base anchor design proceeds. This is an enforceable prerequisite -- design proceeding on unconfirmed bearing assumptions risks non-conformance. Source: R-01 section 3.3.2, section 4.8.2; Procedure Prerequisites table. |

---

## Documentation

### Anticipated Artifacts (from _CONTEXT.md)
- Drawing Set documents per RFP requirements

### Minimum Expected Drawing Set Contents (ASSUMPTION — inferred from deliverable type and structural engineering practice)

> **[E-001] Enrichment note:** The drawing set contents list below is ASSUMPTION-based. Confirm this list against the RFP requirements and/or applicable structural engineering standards of practice to establish verified implementation evidence. Proposed authority: Structural Engineer.
- Plan view of stair at mezzanine level (showing footprint, landing, and connection to mezzanine framing)
- Stair elevation and section views (showing riser/tread dimensions, overall stair height, structural member sizing)
- Connection details (base plate/anchor bolt details at concrete floor; top connection to mezzanine framing per DEL-002-05)
- Handrail and guardrail structural details (post spacing, attachment method, material specification)
- Material and finish schedule (steel members, concrete, surface treatment)
- General notes (applicable codes, design loads, fabrication and erection notes)
- P.Eng. stamp block, revision table, title block

### Related Deliverables
- DEL-002-05 — Mezzanine Framing Details (coordinate connection details)
- DEL-002-04 — Structural Sections & Details (overall building sections)
- DEL-002-10 — Structural Calculation Package (calculations supporting this drawing set)
- DEL-002-12 — Structural Specification (material and workmanship standards)
- DEL-011-07 — Mezzanine Structure & Stairs (construction deliverable consuming this drawing set)

---

## Semantic Lensing Enrichment Trace (Pass 3)

| ItemID | Type | Action Taken |
|---|---|---|
| A-001 | TBD_Question | Added enrichment note to REQ-004 requesting specific ABC edition and clause numbers |
| A-003 | WeakStatement | Strengthened REQ-004 verification approach with clause-level specificity guidance (TBD until ABC edition confirmed) |
| C-001 | VerificationGap | Added geotechnical prerequisite receipt verification row to Verification table |
| D-001 | VerificationGap | Added County preliminary design approval verification row to Verification table |
| E-001 | MissingSlot | Added enrichment note to Documentation section requesting RFP/standard confirmation of drawing set contents list |
| F-001 | WeakStatement | Restructured Standards table with Edition column; added enrichment note requesting edition year confirmation for all standards |
| X-003 | VerificationGap | Added enrichment to REQ-002 verification requiring explicit numeric live load acceptance criterion once established |
