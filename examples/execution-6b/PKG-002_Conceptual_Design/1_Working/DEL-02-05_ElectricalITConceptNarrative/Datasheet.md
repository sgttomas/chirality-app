# Datasheet — DEL-02-05: Electrical/IT Concept Narrative

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-02-05 |
| **Deliverable Name** | Electrical/IT Concept Narrative |
| **Package** | PKG-002 — Conceptual Design |
| **Type** | Design / Narrative |
| **Discipline** | Electrical Engineering / Information Technology |
| **Responsible Party** | Electrical Engineer |
| **Status** | INITIALIZED |
| **Last Updated** | 2026-02-17 |
| **Scope Coverage** | SOW-0009, SOW-0010 |
| **Objective Alignment** | OBJ-003 — Maximize Proposed Conceptual Design score (20 pts) |
| **RFP Reference** | RFP Section 7.1.1; Appendix A (OSR); Addendum 03 |

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| **Artifact Type** | Concept narrative (not detailed design drawings or calculations) | _CONTEXT.md; RFP 7.1.1 |
| **Primary Facility** | Main Public Services Building — combined Fire Hall and Public Works with shared spaces | RFP Section 7.1.1; Decomposition §8 PKG-002 |
| **Secondary Facility** | Cold Storage Building, 60' x 100', unheated | RFP Functional Program (Appendix B); Decomposition DEL-02-05 description |
| **Lighting Standard** | LED per IES (Illuminating Engineering Society) recommendations | _CONTEXT.md; Decomposition DEL-02-05 description |
| **Generator Scope Boundary** | Generator sizing, fuel type, and placement owned by DEL-02-04 (Mechanical); this deliverable covers electrical connection, transfer switching, essential panel, and load list | _CONTEXT.md; Decomposition DEL-02-04 and DEL-02-05 descriptions |
| **Generator Essential Loads (minimum)** | Kitchen; meeting room / ICP; 2 bathrooms; bay door secondary opening mechanism | Addendum 03 (generator requirement) |
| **Solar Roof Orientation (constraint)** | Flat, south, west, or southwest | Addendum 03 (solar-capable roofing requirement) |
| **Access Control** | Provisions to support Additional Option 3 (card reader / keypad access) | _CONTEXT.md; Decomposition vocabulary map; RFP Appendix H Schedule A |
| **Security / Cameras** | Provisions to support Additional Option 4 (CCTV / IP camera system) | _CONTEXT.md; Decomposition vocabulary map; RFP Appendix H Schedule A; Addendum 03 (no supplier preference) |
| **Solar Electrical Provisions** | Conduit, spare panel capacity, and inverter stub-out for future PV installation | Addendum 03; Decomposition DEL-04-03 description |
| **Fire Alarm** | Addressable system concept; coordination with Alberta Fire Code | _CONTEXT.md; Decomposition DEL-02-05 description |
| **Water Fill Stations** | Electrical supply provisions for two 2" fill stations (1 fire bay, 1 PW bay) | Addendum 03 (water fill station requirement) |
| **Utility Voltage Level** | TBD — assumed range: 120/208V 3-phase or 347/600V 3-phase, pending confirmation from utility provider and load calculation at detailed design | ASSUMPTION: standard Alberta municipal utility service options; Electrical Engineer to confirm (Semantic Lensing B-001) |
| **Cold Storage Estimated Electrical Load** | TBD — to be estimated by Electrical Engineer based on lighting (freeze-rated LED), minimal receptacles, and exterior lighting loads; no HVAC electrical loads (unheated building) | Decomposition DEL-02-05 description; C-006 in Guidance (Semantic Lensing B-002) |

---

## Conditions

| Condition | Detail | Source |
|---|---|---|
| **Design Life — Main Building** | 50 years | Decomposition §6 (OBJ-005); RFP evaluation criteria |
| **Design Life — Cold Storage** | 20 years (unheated) | Decomposition §6 (OBJ-005) |
| **Climate** | Central Alberta; cold climate, severe freeze-thaw; high snow load | RFP preamble; site: Waskasoo Avenue North, Penhold, AB |
| **Evaluation Weight** | 20 pts for Proposed Conceptual Design (PKG-002 shared across all five discipline deliverables); per-deliverable scoring distribution TBD — see Evaluation Scoring Distribution row below | Decomposition §15 Evaluation Crosswalk |
| **Addenda Governing Rule** | Addendum 03 governs over base RFP where conflict exists | Decomposition §2 |
| **Additional Options Pricing** | Access Control (Option 3) and Security/Cameras (Option 4) are priced separately in Appendix H Schedule A/B and are not in base cost | Decomposition vocabulary map; RFP Appendix H |
| **Pickled Sand Storage** | Excluded from this project per Addendum 03 | Decomposition §3 C-10 |
| **FF&E** | Additional item only; not in base cost | Addendum 03; Decomposition §3 C-11 |
| **Code Jurisdiction** | Alberta Building Code (NBCC basis); Alberta Fire Code; Canadian Electrical Code Part I (edition TBD — confirm current Alberta-adopted edition) | ASSUMPTION: applicable as Alberta provincial standards; CEC edition to be confirmed by Electrical Engineer or Alberta municipal building authority (Semantic Lensing A-002) |
| **Evaluation Scoring Distribution** | TBD — 20 pts for Proposed Conceptual Design (OBJ-003) shared across PKG-002; confirm whether scoring is holistic across the package or weighted per discipline deliverable | RFP Section 7.1.1 evaluation criteria; Decomposition §15 Evaluation Crosswalk (Semantic Lensing D-002) |

---

## Construction

This table summarizes the sections that the Electrical/IT Concept Narrative document will contain. Values are populated where established by sources; TBD where pending design authorship.

| Section | Content Summary | Source Basis | Status |
|---|---|---|---|
| **1. Electrical Service and Power Distribution** | Utility service entry approach; main switchboard location; branch circuit distribution strategy for Main Building and Cold Storage | RFP 7.1.1; SOW-0009 | TBD — to be authored by Electrical Engineer |
| **2. Lighting — LED per IES** | LED luminaire approach by space category (apparatus bays, offices, residential quarters, shared spaces, exterior/site, Cold Storage); IES footcandle targets; lighting controls strategy (occupancy, daylight, scheduling) | _CONTEXT.md; Decomposition DEL-02-05; SOW-0010 | TBD — IES standards to be cited |
| **3. Generator Connection and Transfer Switching** | ATS type; essential panel configuration; essential load list (minimum: kitchen, ICP meeting room, 2 bathrooms, bay door secondary opening); coordination with DEL-02-04 generator scope | Addendum 03; _CONTEXT.md | TBD — coordinated with Mechanical Engineer |
| **4. IT / Telecommunications** | Structured cabling concept (ASSUMPTION: Cat 6A copper horizontal; fiber backbone); Main Equipment Room (MER) sizing and location; network zone strategy; scalability provisions | _CONTEXT.md; SOW-0009 | TBD — to be authored by Electrical Engineer with IT input |
| **5. Access Control** | Card reader / keypad access concept for designated entry points — supports Additional Option 3 pricing; base design includes conduit and controller location provisions for future retrofit | _CONTEXT.md; Decomposition vocabulary map; Addendum 03 | TBD — Additional Option 3 |
| **6. Security / Cameras** | CCTV / IP camera coverage concept for apparatus bays, parking areas, perimeter, and interior areas — supports Additional Option 4 pricing; no Town supplier preference | _CONTEXT.md; Decomposition vocabulary map; Addendum 03 | TBD — Additional Option 4 |
| **7. Solar-Capable Roof Electrical Provisions** | Conduit, spare panel breaker space, and inverter stub-out for future PV; roof orientation: flat, south, west, or southwest | Addendum 03 | TBD — coordinated with Architect |
| **8. Fire Alarm System** | Addressable FACP; detector and pull station layout concept; HVAC interface; Alberta Fire Code / NBCC compliance pathway | _CONTEXT.md; Decomposition DEL-02-05 | TBD — to be authored by Electrical Engineer |
| **9. Water Fill Station Electrical Supply** | Dedicated 240V circuits to two 2" fill stations; 1 fire apparatus bay, 1 PW bay | Addendum 03 | TBD — coordinated with Mechanical Engineer |
| **10. PA / Paging System (if applicable)** | TBD — confirm whether a public address / paging system is required; if so, describe speaker zones, amplifier location, dispatch alerting integration, and circuit provisions | ASSUMPTION: PA/paging is typical for fire hall facilities; applicability TBD pending Owner confirmation (Semantic Lensing A-003, E-002) | TBD — pending Owner confirmation |

---

## References

| Reference | Description | Accessibility |
|---|---|---|
| RFP 2024_004, Section 7.1.1 | Proposed Conceptual Design requirements and evaluation criteria | Source document; full text not accessed in this session — location TBD |
| RFP Appendix A (OSR) | Owner Statement of Requirements; space list and specific requirements | Source document; full text not accessed — location TBD |
| RFP Appendix B (Functional Program) | Room program; equipment power requirements by space | Source document; full text not accessed — location TBD |
| Addendum 03 (Jul 31, 2024) | Solar-capable roof orientation; generator essential loads; security supplier note; fill stations; additional options | Referenced via Decomposition v2.3; full Addendum 03 text not accessed in this session |
| Decomposition v2.3 FINAL | DEL-02-05 description; SOW-0009, SOW-0010; vocabulary; objectives; evaluation crosswalk | Accessed and read in this session |
| DEL-02-01 (Architectural Concept Package) | Architectural layout, zone locations, building footprint — electrical concept follows architectural concept | Peer deliverable |
| DEL-02-02 (Civil/Site Concept) | Utility entry point(s), site electrical distribution approach — service entry coordination interface | Peer deliverable (Semantic Lensing E-001) |
| DEL-02-04 (Mechanical Concept Narrative) | Generator sizing, fuel type, placement — coordination interface for transfer switching | Peer deliverable |
| DEL-03-05 (Electrical/IT Design Brief) | Downstream Design Brief extending this concept | Downstream deliverable |
| DEL-04-03 (Electrical Energy Efficiency) | Solar-ready provisions and LED controls strategy — sustainability package | Related deliverable |
| DEL-05-04 (Electrical Maintainability) | Panel access, fixture lifecycle, IT infrastructure maintainability — durability package | Related deliverable |
| IES Lighting Handbook / IES Recommended Practices | LED lighting footcandle targets and quality recommendations | Referenced; specific standards location TBD |
| Canadian Electrical Code Part I | Electrical installations standard | ASSUMPTION: applicable; location TBD |
