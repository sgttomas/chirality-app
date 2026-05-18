# Specification — DEL-02-05: Electrical/IT Concept Narrative

---

## Scope

### Inclusions

This deliverable is the Electrical Engineer's contribution to the PKG-002 Conceptual Design package. It covers the following topics in narrative form:

- Electrical service entry and main power distribution concept (Main Building and Cold Storage)
- Lighting approach using LED technology per IES recommendations, including controls strategy by space type
- Generator connection and automatic transfer switching, including essential load panel configuration and essential load list; coordinated with DEL-02-04 (Mechanical Concept) for generator sizing and fuel
- IT and telecommunications infrastructure concept: structured cabling, Main Equipment Room (MER) location and sizing, network zone strategy
- Access control provisions to support Additional Option 3 (card reader / keypad access at designated entry points)
- Security and camera system provisions to support Additional Option 4 (CCTV / IP camera coverage concept)
- Solar-capable roof electrical rough-in provisions: conduit, spare panel breaker space, inverter stub-out; roof orientation consistent with Addendum 03
- Fire alarm system concept: addressable FACP, detector and pull station coverage, HVAC interface, code compliance pathway
- Electrical supply provisions for two 2" water fill stations (1 fire apparatus bay, 1 PW bay) per Addendum 03

### Exclusions

- Detailed design drawings, load calculations, or equipment schedules (this is a concept narrative only)
- Generator sizing, fuel selection, and generator enclosure design (owned by DEL-02-04 — Mechanical Concept)
- Electrical energy efficiency narrative and solar PV performance analysis (owned by DEL-04-03 — Electrical Energy Efficiency)
- Electrical systems maintainability strategy (owned by DEL-05-04 — Electrical Maintainability)
- Electrical/IT Design Brief for RFP Section 7.1.2(5) (owned by DEL-03-05 — Electrical/IT Design Brief)
- Pickled Sand Storage building (removed from project per Addendum 03; Decomposition C-10)
- FF&E power provisions beyond rough-in stub-outs (FF&E is Additional Option 6, not in base cost per Addendum 03)
- Public address (PA) / paging system: TBD — confirm whether a PA or paging system is required for the facility. If required, include concept in narrative; if not required, confirm exclusion. (Semantic Lensing A-003, E-002; ASSUMPTION: PA may refer to "Public Address" system based on typical fire hall communication requirements; RFP and _CONTEXT.md do not provide definitive clarification)

---

## Requirements

| Req ID | Requirement Statement | Source | Verification Method |
|---|---|---|---|
| **R-EL-01** | The narrative shall describe the electrical service entry and main power distribution concept for both the Main Building and Cold Storage building. | RFP 7.1.1; SOW-0009 | Document review — confirm both buildings addressed; service entry and distribution described |
| **R-EL-02** | The narrative shall describe the LED lighting approach for all major space categories (apparatus bays, offices, residential quarters, shared/meeting spaces, exterior/site lighting, Cold Storage), with explicit reference to applicable IES Recommended Practice documents (e.g., IES RP-6 for parking areas, IES DG-4 for emergency egress — specific RP numbers to be confirmed by Electrical Engineer). | _CONTEXT.md; Decomposition DEL-02-05; SOW-0010; IES Recommended Practices — specific RP numbers TBD (Semantic Lensing F-001) | Document review — confirm specific IES RP documents cited by number; all space categories covered |
| **R-EL-03** | The narrative shall describe the lighting controls strategy by space type (occupancy sensors, daylight harvesting, manual switching, scheduling), with rationale for each selection. | Decomposition DEL-04-03 (alignment); SOW-0010 | Document review — confirm controls rationale present per space category |
| **R-EL-04** | The narrative shall describe the generator connection and automatic transfer switching concept, including essential panel configuration and ATS type, explicitly coordinated with DEL-02-04. | _CONTEXT.md; Addendum 03 (generator requirement); SOW-0010 | Cross-reference check with DEL-02-04; confirm ATS and essential panel concept described |
| **R-EL-05** | The essential load panel shall be confirmed to include, at minimum: kitchen, meeting room (ICP), 2 bathrooms, and bay door secondary opening mechanism. | Addendum 03 §1 (generator essential loads) | Checklist against Addendum 03 minimum load list — all four loads confirmed in narrative |
| **R-EL-06** | The narrative shall describe the IT and telecommunications infrastructure concept, including structured cabling approach, Main Equipment Room (MER) location and sizing concept, and network zone strategy. | _CONTEXT.md; SOW-0009 | Document review — IT section includes cabling, MER location and sizing, and network zone strategy |
| **R-EL-07** | The narrative shall describe access control provisions sufficient to support Additional Option 3 pricing, including concept for card reader / keypad access at designated entry points; base design must support future retrofit. | _CONTEXT.md; Decomposition vocabulary map; RFP Appendix H Schedule A | Confirm Option 3 provisions described; confirm base-design retrofit provisions noted |
| **R-EL-08** | The narrative shall describe security and camera system provisions sufficient to support Additional Option 4 pricing, including CCTV / IP camera coverage concept for apparatus bays, parking, exterior perimeter, and interior areas; no Town supplier preference shall be stated. | _CONTEXT.md; Decomposition vocabulary map; RFP Appendix H Schedule A; Addendum 03 | Confirm Option 4 provisions described; confirm no specific supplier named |
| **R-EL-09** | The narrative shall describe solar-capable roof electrical provisions: conduit pathway, spare panel breaker space, and inverter stub-out location. Roof orientation must be explicitly stated as consistent with Addendum 03 (flat, south, west, or southwest). | Addendum 03 (solar-capable roofing); SOW-0010; Decomposition DEL-04-03 | Document review — solar provisions stated; orientation matches Addendum 03 |
| **R-EL-10** | The narrative shall describe the fire alarm system concept, including addressable FACP approach, detector and pull station coverage, HVAC system interface, and code compliance pathway (Alberta Fire Code / NBCC). | _CONTEXT.md; SOW-0009 | Document review — FACP type, coverage, and code reference included |
| **R-EL-11** | The narrative shall address electrical supply provisions for two 2" water fill stations: one in the fire apparatus bay and one in the PW bay. | Addendum 03 (fill station requirement) | Checklist — both fill station locations and electrical supply concept confirmed in narrative |
| **R-EL-12** | All electrical-relevant program requirements from Addendum 03 shall be embedded and explicitly addressed in this narrative. | SOW-0010; Addendum 03 | Addendum 03 integration checklist review |
| **R-EL-13** | The narrative shall be spatially consistent with the architectural concept in DEL-02-01 regarding building layout, zone locations, and overall building configuration. | Decomposition DEL-02-01; SOW-0009 | Cross-reference review with DEL-02-01 — no contradictions in zone descriptions |
| **R-EL-14** | The narrative shall address emergency lighting with battery backup duration of minimum 90 minutes, consistent with Alberta Building Code requirements, including LED egress luminaires and exit signs on dedicated circuits. | Guidance P-006; Procedure Step 8; ASSUMPTION: Alberta Building Code minimum 90-minute battery backup (Semantic Lensing C-001) | Document review — confirm 90-minute battery backup duration stated; emergency lighting on dedicated circuits described |
| **R-EL-15** | The narrative shall address electrical supply provisions for bunker gear room ventilation fans, or explicitly state that ventilation fan motor supply is coordinated with DEL-02-04 (Mechanical) scope. | Addendum 03 (40 bunker gear lockers + room ventilation); Procedure Step 1 Addendum 03 checklist (Semantic Lensing C-002) | Document review — confirm bunker gear ventilation electrical supply addressed or coordination with DEL-02-04 explicitly stated |
| **R-EL-16** | The narrative shall address electrical supply for sump pump(s) if electrically operated, including circuit provisions and coordination with DEL-02-04 on sump design. | Addendum 03 (bay sumps — snow melting, minor washing); Procedure Step 1 checklist; Procedure Step 2 item 6 (Semantic Lensing X-003) | Document review — confirm sump pump electrical supply concept described or explicitly excluded with rationale |
| **R-EL-17** | The narrative shall either (a) include a concept for a public address (PA) / paging system if applicable to the facility, or (b) explicitly state that a PA system is excluded from scope with rationale. | ASSUMPTION: PA/paging is a common fire hall communication system; _CONTEXT.md and RFP do not explicitly address PA — TBD pending Owner confirmation (Semantic Lensing A-003, E-002) | Document review — confirm PA system concept present or explicit exclusion stated |

---

## Standards

| Standard | Applicability | Accessibility |
|---|---|---|
| **NBCC (National Building Code of Canada)** | Building code electrical provisions, fire alarm, life safety | Referenced in Decomposition vocabulary map; full text not accessed — location TBD |
| **Alberta Building Code** | Provincial building code overlay; occupancy and life safety requirements | ASSUMPTION: applicable as Alberta provincial standard; full text not accessed |
| **Alberta Fire Code** | Fire alarm system requirements; FACP and detection compliance | ASSUMPTION: applicable as Alberta provincial standard; full text not accessed |
| **Canadian Electrical Code (CEC) Part I** | Electrical installations standard governing all electrical work in Alberta; edition TBD — confirm current Alberta-adopted edition (e.g., CEC 2024 or as adopted by Alberta Safety Codes Act) | ASSUMPTION: applicable; edition and full text not accessed — location TBD (Semantic Lensing A-001, A-002) |
| **IES Lighting Handbook / IES Recommended Practices** | LED lighting footcandle targets and quality recommendations by space type; applicable RPs to be confirmed (e.g., IES RP-6 for parking areas, IES DG-4 for emergency egress — ASSUMPTION: standard references for this facility type) | Referenced in _CONTEXT.md and Decomposition DEL-02-05; specific RP document numbers TBD — Electrical Engineer to confirm (Semantic Lensing F-001) |
| **ULC S524 / ULC S527** | Fire alarm system installation (S524) and control equipment (S527) standards (Canada); edition TBD — confirm current editions applicable in Alberta | ASSUMPTION: applicable for Canadian fire alarm systems; edition and full text not accessed — location TBD (Semantic Lensing A-001) |
| **TIA-568 / ANSI/BICSI Standards** | Structured cabling standards for IT/telecom infrastructure; edition TBD — confirm current editions | ASSUMPTION: applicable for structured cabling design; edition and location TBD (Semantic Lensing A-001) |
| **CSA Standards** | Electrical equipment certification (Canadian market); specific CSA standard numbers TBD (e.g., CSA C22.1 for CEC, CSA C22.2 for equipment) | ASSUMPTION: applicable; specific standard numbers and editions TBD (Semantic Lensing A-001) |

> **Note:** If conflict exists between base RFP and Addendum 03, Addendum 03 governs. (Source: Decomposition §2)

---

## Verification

| Req ID | Verification Method | Acceptance Criteria |
|---|---|---|
| R-EL-01 | Document review | Narrative addresses both Main Building and Cold Storage; service entry and distribution concept described |
| R-EL-02 | Document review; IES citation check | All space categories listed with lighting level approach; IES standard referenced |
| R-EL-03 | Document review | Controls strategy (occupancy, daylight, manual, scheduling) described by space type with rationale |
| R-EL-04 | Document review; cross-reference with DEL-02-04 | ATS type and essential panel concept described; DEL-02-04 coordination explicitly noted |
| R-EL-05 | Addendum 03 checklist | All four Addendum 03 minimum essential loads confirmed present in narrative load list |
| R-EL-06 | Document review | IT section includes cabling approach, Main Equipment Room (MER) location concept, and network zone strategy |
| R-EL-07 | Document review; Option 3 pricing linkage check | Access control provisions described with sufficient detail to support separate Option 3 pricing; base retrofit provisions noted |
| R-EL-08 | Document review; Option 4 pricing linkage check; supplier check | Camera coverage concept described; sufficient detail for Option 4 pricing; no specific supplier named |
| R-EL-09 | Document review; orientation cross-check | Solar rough-in provisions stated (conduit, breaker space, inverter stub-out); orientation explicitly stated as flat/south/west/southwest |
| R-EL-10 | Document review | Addressable FACP concept described; ULC/Alberta Fire Code reference included; HVAC interface noted |
| R-EL-11 | Addendum 03 checklist | Both fill station locations (fire bay, PW bay) and electrical supply concept present in narrative |
| R-EL-12 | Addendum 03 integration checklist review — checklist must include, at minimum: generator essential loads, solar-capable roof provisions, fill station electrical supply, bunker gear room ventilation fan supply, bay sump electrical supply, 16 ft overhead door secondary opening mechanism, and security supplier neutrality; cross-reference with Procedure Step 1 Addendum 03 checklist for completeness | All electrical-relevant Addendum 03 items explicitly addressed; each checklist item traceable to a narrative section (Semantic Lensing X-002) |
| R-EL-13 | Cross-reference review with DEL-02-01 | No contradictions between electrical narrative zone descriptions and architectural concept layout |
| R-EL-14 | Document review; code reference check | Emergency lighting with minimum 90-minute battery backup duration stated; dedicated circuits for egress luminaires and exit signs described; Alberta Building Code cited |
| R-EL-15 | Document review; cross-reference with DEL-02-04 | Bunker gear room ventilation electrical supply addressed, or explicit coordination statement with DEL-02-04 present |
| R-EL-16 | Document review; cross-reference with DEL-02-04 | Sump pump electrical supply concept described, or explicit exclusion rationale stated |
| R-EL-17 | Document review; Owner confirmation | PA/paging system concept described, or explicit exclusion with rationale stated |

---

## Documentation

### Anticipated Artifacts

| Artifact | Description | Owner |
|---|---|---|
| Electrical/IT Concept Narrative | Primary deliverable — narrative document covering all content sections identified in this specification (nine base sections plus PA/paging if applicable) | Electrical Engineer |

> Supporting diagrams (e.g., single-line schematic concept, IT block diagram, fire alarm layout concept, solar provisions sketch) are desirable but secondary to the narrative. They are not listed as separate anticipated artifacts in _CONTEXT.md.

### Cross-Deliverable Relationships

| Deliverable ID | Relationship | Direction |
|---|---|---|
| DEL-02-01 — Architectural Concept Package | Electrical systems serve the architectural layout; coordination on zone locations and building footprint | Upstream context |
| DEL-02-02 — Civil/Site Concept | Utility entry point(s) and site electrical distribution approach — service entry coordination interface | Upstream context (Semantic Lensing E-001) |
| DEL-02-04 — Mechanical Concept Narrative | Generator sizing, fuel type, and placement — transfer switching coordination interface | Lateral coordination |
| DEL-03-05 — Electrical/IT Design Brief | Design Brief extends this concept narrative into rationale and philosophy per RFP Section 7.1.2(5) | Downstream |
| DEL-04-03 — Electrical Energy Efficiency | Solar-ready provisions and LED controls strategy — coordination on overlap topics | Lateral coordination |
| DEL-05-04 — Electrical Maintainability | Maintainability of panels, fixture types, and IT infrastructure — extends concept-phase decisions | Downstream |

### Documentation Requirements for Subsequent Design Phases

Per RFP Section 7.1.8, the concept established here shall be advanced in the following design submissions:
1. Building Design Development — drawings + outline specifications
2. 60% Detailed Design — coordinated construction drawings
3. Foundation IFC — foundation electrical provisions
4. 100% Building Detail Design — complete construction documents
5. 100% IFC (Issued For Construction) package

(Source: Decomposition DEL-06-02 description; RFP 7.1.8)
