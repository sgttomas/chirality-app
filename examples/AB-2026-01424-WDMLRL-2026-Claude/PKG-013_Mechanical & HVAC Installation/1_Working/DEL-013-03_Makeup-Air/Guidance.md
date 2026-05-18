# Guidance — DEL-013-03: Forced-Air Makeup System

---

## Purpose

The forced-air makeup air (MUA) system exists to maintain acceptable indoor air quality, worker safety, and thermal comfort in the New North Shop Addition by continuously replacing air that is exhausted by the heavy equipment exhaust system (DEL-013-04), the welding station exhaust system (DEL-013-05), and the primary air exchanger (DEL-013-02).

In a large industrial maintenance shop with 35' ceilings housing tracked and heavy equipment, the cumulative exhaust volumes from vehicle operation, welding, and general ventilation can create significant negative pressure without an active makeup air supply. This negative pressure can cause backdrafting of heating appliances, difficulty opening overhead doors, and degraded air quality. The MUA system prevents these conditions.

Source: _CONTEXT.md Description; _DEPENDENCIES.md Constraint Notes; Decomposition OBJ-004; RFP §3.4 (high recovery heating, high volume air exchanger, exhaust systems listed together as system group)

---

## Principles

### P1 — Volume Balance is the Primary Design Driver
The MUA system's capacity must be matched to the combined exhaust volumes of DEL-013-04 and DEL-013-05, with coordination against DEL-013-02. The mechanical engineer's calculation package (DEL-003-06) must establish these volumes before MUA equipment can be selected. Do not procure MUA equipment until airflow calculations are reviewed and approved.

Source: _DEPENDENCIES.md Constraint Notes; _CONTEXT.md Key Requirements

### P2 — Makeup Air Must Be Tempered
Introducing large volumes of unheated outside air into an occupied shop in an Alberta climate will rapidly make the space uninhabitable in winter and will overload the heating system. All makeup air shall be pre-conditioned (heated) before entry into the occupied zone. The MUA unit's heating coil or gas burner capacity must match the design supply volume at the design outdoor air temperature. The design outdoor air temperature for heating sizing should be sourced from ASHRAE climate data for the Camrose County region or from DEL-003-06 (currently TBD — see Datasheet Capacity & Performance).

Source: _DEPENDENCIES.md Constraint Notes ("Heating capacity must handle makeup air volume"); _DEPENDENCIES.md Internal Package Dependencies (DEL-013-01); RFP §3.4 ("High recovery heating system"); Enrichment B-002

### P3 — Controls Prevent Pressurization Problems
The system requires modulating damper control, not simple on/off operation. If the MUA supplies more air than the building can exhaust through the designed exhaust paths, building pressure will rise, creating difficulty with overhead door operation, potential structural loading on building envelope, and comfort problems. Controls must be coordinated across all ventilation systems. The maximum allowable pressure differential must be established by the mechanical engineer (see REQ-013-03-03 — currently TBD).

Source: _DEPENDENCIES.md Constraint Notes ("Controls must prevent excessive pressurization"); _DEPENDENCIES.md Critical Integration Points; Enrichment A-003

### P4 — Intake Location is Safety-Critical
The fresh air intake must be positioned to draw clean outdoor air, not recirculated exhaust from the vehicle exhaust fans, welding exhaust outlets, or the air exchanger exhaust. In industrial settings, intake-exhaust short-circuiting can introduce combustion products, particulates, or welding fumes into the fresh air supply. The minimum separation distance between intake and exhaust outlets must comply with ASHRAE 62.1 or equivalent standard (see REQ-013-03-04); visual confirmation alone is not sufficient for this safety-critical requirement.

Source: _DEPENDENCIES.md Critical Integration Points ("Fresh air intake coordinate with exchanger intake"); _DEPENDENCIES.md Constraint Notes ("Fresh air quality critical for safety and comfort"); Enrichment X-003

### P5 — Design Drawings Must Precede Installation
The MUA system installation depends on IFC (Issued for Construction) mechanical drawings from DEL-003-03 (Ductwork & Distribution Plans) and the mechanical specification (DEL-003-07). Do not begin ductwork fabrication or MUA unit procurement without approved drawings.

**Rationale for P.Eng. stamp requirement (REQ-013-03-10):** The requirement for P.Eng.-stamped IFC drawings is grounded in the Alberta Safety Codes Act and APEGA regulations, which mandate that engineered mechanical systems be designed under the supervision of a licensed Professional Engineer. In the design-build delivery model used for this project (CCDC 14-2013), the contractor's engineer of record produces the IFC drawings and assumes professional responsibility for the design. The P.Eng. stamp confirms that the design has been reviewed for code compliance, structural adequacy of supports, and system performance. (Enrichment: F-001)

Source: RFP §3.3.2 ("All Issued For Construction Drawings must be signed/stamped by a professional engineer"); _REFERENCES.md R-04; Decomposition DEL-003 series; Alberta Safety Codes Act / APEGA regulations (location TBD — Enrichment F-001)

---

## Considerations

### C1 — Sequence with Building Envelope
The fresh air intake penetration through the building exterior wall must be coordinated with the building envelope contractor and the structural engineer to ensure weathertight detailing and appropriate flashing. This penetration should be planned during building envelope construction, not cut in afterward.

Source: ASSUMPTION — consistent with standard construction sequencing for mechanical envelope penetrations

### C2 — Utility Room Readiness
The MUA unit is anticipated to be located in or adjacent to the Utility Room (DEL-012-02). The Utility Room must be substantially complete — with concrete floor, walls, roof, and electrical rough-in available — before the MUA unit can be set in place. Confirm the dependency schedule with the General Contractor early.

Source: _DEPENDENCIES.md External Dependencies ("DEL-012-02: Utility Room completion (equipment housing)")

### C3 — Coordination with Natural Gas Tie-In
If the MUA unit uses gas-fired heating (the most common approach in Alberta for units of this type — ASSUMPTION), the natural gas tie-in (SOW-0080) must be complete, or at minimum available to the utility room, before the MUA unit can be commissioned. This is a potential schedule constraint if gas service is delayed.

Source: SOW-0080; _DEPENDENCIES.md (ASSUMPTION re: gas-fired MUA)

### C4 — Ductwork Routing in a High-Bay Space
The main shop area has 35' ceilings and two 5-tonne overhead cranes (DEL-016-01) on crane rails. Supply ductwork must be routed to avoid interference with crane travel zones. Coordinate ductwork heights, hanger locations, and structural attachments with the structural engineer and crane supplier before ductwork is fabricated or hung.

Source: RFP §3.4 ("2 – 5-tonne overhead cranes"); App B (floor plan showing crane locations); _DEPENDENCIES.md Critical Integration Points

### C5 — Permit Lead Time
Alberta mechanical permits typically require submission of stamped IFC drawings before permit issuance. Ensure the AHJ permit application is submitted promptly once mechanical drawings are approved to avoid construction schedule delays.

Source: RFP §3.3.2 (permit obligations); ASSUMPTION re: typical AHJ permit timelines

### C6 — Test and Balance Scope
A test-and-balance (TAB) contractor should be engaged to verify airflow at all supply points and confirm the system meets design volumes. TAB should be performed after all ductwork is complete and before the Owner acceptance testing to allow any deficiencies to be corrected.

Source: ASSUMPTION — consistent with industry practice for HVAC commissioning; REQ-013-03-02 (Specification.md)

### C7 — Acoustic Impact of MUA Unit (Enrichment: E-001)
Large MUA units can generate significant noise, both from the fan motor and from airflow through ductwork. In a 35' high-bay shop with overhead cranes, MUA noise is a practical consideration for:
- **Worker safety:** Excessive background noise can impair communication near equipment, particularly during crane operations where audible signals are safety-critical.
- **Worker comfort:** Sustained noise contributes to fatigue.
- **Mitigation options:** Acoustic treatment, duct silencers, vibration isolation, or strategic unit placement (e.g., in the Utility Room rather than the open shop space) may reduce noise transmission to occupied areas.

The mechanical engineer should assess noise levels during equipment selection (DEL-003-05) and specify acoustic mitigation if warranted.

Source: ASSUMPTION: standard consideration for industrial MUA installations; occupational health standards (location TBD); Enrichment E-001

### C8 — Post-Commissioning Performance Monitoring (Enrichment: D-003, E-003)
The MUA system operates under significantly varying conditions across Alberta's seasons — from extreme winter cold (requiring full heating capacity) to shoulder-season conditions (where condensation, reduced heating demand, and variable exhaust loads change the operating profile). A single-point commissioning test may not capture all operating modes.

Consideration should be given to:
- A seasonal performance review after the first full heating season to validate design assumptions (supply volume adequacy, heating capacity, pressurization control).
- Establishing a simple performance monitoring protocol (e.g., periodic supply temperature and airflow spot-checks by facilities staff).
- **TBD:** Does the Owner (Camrose County) require a lessons-learned or performance feedback mechanism for major mechanical systems post-commissioning? If so, define the review scope and schedule.

Source: ASSUMPTION — given TBD design parameters and multiple assumptions, post-installation validation is prudent; Enrichments D-003, E-003

---

## Trade-offs

### T1 — Gas-Fired Direct Heating vs. Indirect (Heat Exchanger) Makeup Air Unit
Direct gas-fired MUA units are common in large industrial applications and provide high heating capacity at lower capital cost. Indirect units (using a separate heat source) offer flexibility and can integrate with the high-recovery heating system (DEL-013-01) for energy efficiency. The mechanical engineer's design selection (DEL-003-05) should be reviewed for its integration approach with DEL-013-01 to ensure no duplication or conflict.

Source: ASSUMPTION — decision deferred to mechanical engineer; _DEPENDENCIES.md Internal Package Dependencies

### T2 — Centralized vs. Distributed Supply
A single large MUA unit can supply all zones through a duct distribution network. Multiple smaller units serving discrete zones offer redundancy and zoning flexibility but increase capital and maintenance cost. Given the shop's layout (main shop, repair bays, wash bay, welding area as shown on App B), a centralized unit with zoned distribution is the most likely design approach, but this is TBD pending DEL-003-07 (Mechanical Specification).

Source: ASSUMPTION; _CONTEXT.md Scope; App B floor plan

### T3 — Energy Recovery on Makeup Air
An energy recovery ventilator (ERV) integrated with the MUA can recover heat from exhaust air to pre-condition the makeup air, reducing heating energy demand. However, this adds cost and complexity, and may duplicate the function of DEL-013-02 (High-Volume Air Exchanger). The mechanical engineer must confirm whether DEL-013-02 provides energy recovery on the exhaust stream and how the MUA interacts with it.

Source: ASSUMPTION — energy recovery consideration; _DEPENDENCIES.md Internal Package Dependencies (DEL-013-02 coordination)

---

## Examples

No directly accessible source examples are available. TBD — examples of similar industrial MUA installations in Alberta maintenance shops would be useful context for the mechanical designer.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CFT-013-03-01 | SOW-0037 references "App B" as the source for the forced-air makeup system requirement, but RFP §3.4 does not explicitly list it (§3.4 lists heating, air exchanger, exhaust, ventilation at welding — but not makeup air by name). This creates ambiguity about whether makeup air is a named §3.4 design requirement or an App B addition only. The Specification scope statement now acknowledges this ambiguity (Enrichment A-001). | Decomposition SOW-0037 (SourceRef: App B) | RFP §3.4 Design Requirements list (does not name makeup air explicitly; App B notes list "Forced Air Makeup") | Specification.md Scope; REQ-013-03-01 | App B is a governing source alongside §3.4 (both are RFP appendix documents); the omission from §3.4 is likely an oversight given App B explicitly calls it out. PROPOSAL: treat as IN scope per App B. | TBD |
