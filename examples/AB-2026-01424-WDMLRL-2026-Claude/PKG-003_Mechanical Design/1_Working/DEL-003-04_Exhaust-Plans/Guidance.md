# Guidance — DEL-003-04 Exhaust System Plans

---

## Purpose

DEL-003-04 exists to document the engineered exhaust and localized ventilation systems for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition (New North Shop). The exhaust system plans are the primary design instrument used by the mechanical contractor (PKG-013) to install the heavy equipment exhaust, welding station ventilation, service pit ventilation, and building exhaust fans that are required to make the facility safe and functional for heavy equipment maintenance operations.

This deliverable contributes directly to:

- **OBJ-001** — Code-compliant, fully functional maintenance shop (all occupant-safety and operational ventilation systems must be present and pass inspection)
- **OBJ-003** — Complete, P.Eng.-stamped IFC design documentation across all disciplines before construction begins
- **OBJ-004** — Install and commission all mechanical systems to operational readiness

The facility serves a regional landfill operation. The equipment being maintained is heavy class: motor scrapers, tracked equipment, packer vehicles. The exhaust volumes and hazard levels from diesel engine exhaust, welding fumes, and below-grade service pit environments are materially different from a light-vehicle shop. The design must reflect this operating context.

**Source:** R-01 §3.1, §3.4; Decomposition §5 OBJ-001, OBJ-003, OBJ-004; Decomposition §7 DEL-003-04

---

## Principles

### 1. Source Capture Over Dilution

For heavy equipment exhaust and welding fumes, source-capture exhaust (extracting contaminated air at or near the point of generation) is generally preferable to dilution ventilation alone. A 35-ft ceiling space with large diesel equipment generates significant exhaust plumes; dilution alone may not meet occupational exposure limits at the worker breathing zone.

**ASSUMPTION:** Source-capture exhaust hose systems connected to a dedicated exhaust duct and fan are the anticipated approach for repair bay equipment exhaust. This is consistent with SOW-0038 ("exhaust hoses and fans") as opposed to a general exhaust fan approach alone.

**Source:** R-01 §3.4 (SOW-0038); general mechanical engineering principle — cite applicable ASHRAE 62.1 or Alberta OHS Code for specific requirements (location TBD).

> **Standards applicability note (C-001):** ASHRAE 62.1 is anticipated to apply to the ventilation rate procedure for the overall shop space (Section 6, Ventilation Rate Procedure for industrial occupancies). The Alberta OHS Code is anticipated to apply to occupational exposure limits for diesel exhaust particulates and CO at the worker breathing zone. Specific clause numbers are TBD pending access to current editions. Source: _SEMANTIC_LENSING.md item C-001. **PROPOSAL:** Mechanical Engineer to document specific clause applicability during Step 2 (Establish Design Criteria).

### 2. Makeup Air Balance

Any exhaust system creates a negative pressure in the building unless it is compensated by a makeup air source. This building includes both a forced-air makeup air system (SOW-0037) and a high-volume air exchanger (SOW-0036). The exhaust system design must be coordinated with these systems to achieve an overall balanced or slightly negative pressure appropriate for the space type.

**Source:** R-04 App B (lists Forced Air Makeup as a building feature); R-01 §3.4 (SOW-0036, SOW-0037)

### 3. Zone Isolation for the Wash Bay and Welding Station

The wash bay is an enclosed single-bay space. The welding station is in the main shop. These zones have distinct contamination types (wash water vapour/steam vs. metal fumes/arc radiation/UV). The exhaust system should be designed to handle each zone independently to avoid cross-contamination.

**ASSUMPTION:** Separate exhaust circuits or at minimum separate exhaust fans are anticipated for the wash bay and the welding station zone.

**Source:** R-01 §3.1, §3.4; R-04 App B (wash bay shown as enclosed; welding station at northeast corner of main shop)

### 4. Service Pit as a Confined Space Analogue

The service pit is a below-grade pit. Even if it does not meet the regulatory definition of a confined space, it is subject to accumulation of heavier-than-air exhaust gases (CO, NOx from diesel equipment operating above). The ventilation system for this pit should be designed to prevent dangerous gas accumulation during normal servicing operations.

**ASSUMPTION:** The service pit ventilation should be designed for continuous mechanical ventilation during occupied use, not merely emergency ventilation. Confirm against Alberta OHS Code requirements for service pit environments (location TBD).

**Source:** R-01 §3.4 (SOW-0028 — "ventilated and lighted service pit area")

> **Standards applicability note (C-001):** The Alberta OHS Code is anticipated to apply to confined/restricted space provisions (Part 5) for the service pit, even if the pit does not meet the strict definition of "confined space." Ventilation requirements for below-grade work areas where heavier-than-air gases may accumulate are specifically relevant. ASHRAE 62.1 may also govern air changes per hour for this space type. Specific clause numbers are TBD. Source: _SEMANTIC_LENSING.md item C-001.

### 5. Cold Climate Considerations

The facility is located near Ferintosh, Alberta, with significant winter design temperatures. Exhaust system terminations must be located and detailed to prevent backdraft in cold weather, frost accumulation at stack terminations, and cold air infiltration through exhaust dampers when fans are not operating.

**Source:** R-01 §1.0 (Alberta location); general cold-climate mechanical engineering practice — specific design temperatures TBD from applicable ASHRAE Fundamentals or Alberta Building Code climate data (location TBD)

> **Note (E-001):** The winter design temperature for Ferintosh, Alberta has been added as TBD in Datasheet Key Design Parameters. This value is essential for determining exhaust termination design details (e.g., frost protection, backdraft damper sizing, stack height relative to snow accumulation). Source: Datasheet Key Design Parameters; _SEMANTIC_LENSING.md item E-001.

### 6. Coordination with the Electrical Drawing

The RFP electrical conceptual drawing (R-05 App B-Elec) explicitly shows exhaust fan placement (SOW-0066). The Exhaust System Plans must coordinate fan locations with the electrical drawing so that power supply and circuit sizing (DEL-004) align with the mechanical fan specifications (DEL-003-05).

**Source:** R-05 App B-Elec; SOW-0066; Decomposition §7 DEL-004-04, DEL-004-06

### 7. Ceiling Fan Interaction with Exhaust Systems (NEW)

The 6 ceiling fans (SOW-0040) in the main shop area create air circulation patterns that interact with the exhaust capture systems operating in the same space. Ceiling fan downdraft can disrupt the capture envelope of source-capture exhaust systems (hose-reel drops, welding LEV hoods) if fan placement and speeds are not coordinated with exhaust system layout. The design should assess whether ceiling fan positions and operating modes conflict with exhaust capture zones, particularly at the welding station and repair bay hose drops.

**ASSUMPTION:** Ceiling fan interaction assessment is a design consideration that can be addressed qualitatively during system layout (Step 3). If the assessment identifies significant interactions, further analysis or operational restrictions (e.g., ceiling fans off during welding) may be needed.

**Source:** R-05 App B-Elec (SOW-0040); Datasheet Conditions (ceiling fans row); _SEMANTIC_LENSING.md item C-002

---

## Considerations

### Drawing Set Organization

**ASSUMPTION:** Given the range of exhaust systems, the drawing set is likely to include:
1. Overall exhaust system plan (full building footprint)
2. Repair bay exhaust detail plan (showing hose drops, fan unit, duct routing to exterior)
3. Welding station exhaust detail (showing LEV hood, duct, fan, stack termination)
4. Service pit ventilation detail (showing supply and exhaust arrangement)
5. Wash bay exhaust/ventilation detail (showing exhaust arrangement for the enclosed wash bay)
6. Exhaust termination and stack details (exterior elevations/details)
7. Exhaust fan schedule (coordinated with DEL-003-05 Equipment Schedule)

The exact sheet breakdown is determined by the Mechanical Engineer and may vary. The list above is directional only.

> **Note (B-003):** Wash bay exhaust/ventilation detail (item 5) has been added. Source: _SEMANTIC_LENSING.md item B-003.

### Relationship to Other PKG-003 Deliverables

The Exhaust System Plans (DEL-003-04) are tightly coupled with:

- **DEL-003-03 Ductwork & Distribution Plans**: Exhaust ductwork may be shown in whole or in part in DEL-003-03; the boundary between these two deliverables should be clearly defined to avoid duplication. **ASSUMPTION:** DEL-003-03 covers supply/return ductwork; DEL-003-04 covers exhaust-specific ductwork and hose systems.
- **DEL-003-05 Equipment Schedule**: All exhaust fans, exhaust units, and hose reel assemblies must appear in the equipment schedule with manufacturer, model, airflow, static pressure, and electrical characteristics.
- **DEL-003-06 Calculation Package**: Fan sizing, duct pressure drop calculations, and airflow balance calculations underpin the drawings; the drawings must be consistent with the calculations.
- **DEL-003-07 Mechanical Specification**: Specifies the quality and installation requirements for exhaust components shown on these drawings.

### Relationship to PKG-013 (Mechanical Installation)

DEL-013-04 (Heavy Equipment Exhaust System Installation) and DEL-013-05 (Welding Station Exhaust System Installation) are the downstream construction deliverables that depend on DEL-003-04. The Exhaust System Plans are the primary design document for those installations.

> **Note (C-003):** Post-installation commissioning and functional performance verification (e.g., air balance testing, airflow measurement at exhaust points) may be covered by PKG-013 installation deliverables (DEL-013-04, DEL-013-05) rather than by this design deliverable. **PROPOSAL:** Confirm the scope boundary for commissioning with the project team. Source: _SEMANTIC_LENSING.md item C-003.

**Source:** Decomposition §7 PKG-013

### Coordination with PKG-004 (Electrical)

Exhaust fans require electrical power. The electrical conceptual drawing (R-05) shows exhaust fan placement. Coordination must occur between the Mechanical Engineer (this deliverable) and the Electrical Engineer (DEL-004 series) to align:
- Fan motor voltage, phase, and amperage (affects circuit sizing)
- Fan locations (affects conduit routing)
- Control requirements (e.g., interlocks with makeup air unit, occupancy sensors)

**Source:** R-05 App B-Elec; SOW-0066; Decomposition PKG-004

### Coordination with PKG-002 (Structural)

Exhaust duct and pipe penetrations through the concrete structure (walls, floor for pit ventilation) require structural coordination. Hose reel mounting points in repair bays may require embedded anchors. Confirm with DEL-002 series.

**Source:** R-01 §3.4; R-04 App B; Decomposition PKG-002

### Standards Applicability Rationale (NEW — C-001)

The following table provides a preliminary mapping of anticipated standard applicability to each exhaust subsystem. This rationale is directional and must be confirmed by the Mechanical Engineer during design criteria establishment (Procedure Step 2).

| Standard / Code | Anticipated Applicable Subsystem(s) | Anticipated Provisions | Rationale for Applicability |
|---|---|---|---|
| ASHRAE 62.1 | Overall shop ventilation rate; repair bay ventilation; service pit air changes | Ventilation Rate Procedure (Section 6); exhaust system requirements for industrial occupancies | Industrial maintenance shop is an occupancy type addressed by ASHRAE 62.1; ventilation rate calculations drive fan sizing |
| Alberta OHS Code | Welding station LEV; service pit ventilation; noise/vibration (E-004) | Occupational exposure limits for welding fumes, diesel exhaust; confined/restricted space provisions (Part 5); occupational noise exposure limits | Workers are exposed to hazardous airborne contaminants; OHS Code governs workplace air quality and noise limits |
| Alberta Building Code (NBC as adopted) | All exhaust systems; building ventilation | Mechanical ventilation requirements; exhaust system design standards | Building code governs overall mechanical system compliance for permit approval |
| Alberta Safety Codes Act | All mechanical installations | Safety code permit requirements for mechanical systems | All mechanical installations require safety code permits under provincial legislation |
| SMACNA | Ductwork construction (exhaust ducts, stacks) | Duct construction standards; sealing and testing requirements | Industry standard for duct fabrication and installation quality |

> **Note (C-001):** This table has been added per _SEMANTIC_LENSING.md item C-001 to address the rationale gap for standards applicability. All entries are **ASSUMPTION** level -- specific clause numbers and editions are TBD pending code access and AHJ confirmation. Source: _SEMANTIC_LENSING.md item C-001.

### Guarantee Period Implications for Exhaust System Design (NEW — F-004)

The project guarantee period is "Construction period + 2 years post-CCC" (Source: R-01 §2.10; Datasheet Key Design Parameters). This has implications for exhaust system design choices:

- **Corrosion resistance:** Exhaust systems serving the wash bay are exposed to moisture, steam, and potentially chemical cleaning agents. Material selection (e.g., stainless steel or coated ductwork) should account for a minimum 2-year post-commissioning service life without significant corrosion. This is especially relevant for the wash bay exhaust (if in scope).
- **Flexible hose durability:** Exhaust hose-reel systems in repair bays undergo repeated connect/disconnect cycles with heavy equipment. Hose material and reel mechanism should be rated for the anticipated duty cycle over the guarantee period.
- **Maintainability and accessibility:** Exhaust fans, dampers, and filters must be accessible for maintenance. Fan bearings, belts, and motors should be serviceable without requiring scaffold or crane access where practicable.
- **Service pit ventilation components:** Below-grade components are exposed to moisture and potential contaminant accumulation; material selection should account for this environment.

**ASSUMPTION:** The guarantee period does not impose requirements beyond standard commercial/industrial HVAC practice, but the Mechanical Engineer should confirm that specified equipment is warranted for the guarantee period. The Mechanical Specification (DEL-003-07) should address material and equipment warranty requirements.

> **Note (F-004):** This section has been added per _SEMANTIC_LENSING.md item F-004 to address the rationale gap between the recorded guarantee period and exhaust system design choices. Source: R-01 §2.10; Datasheet Key Design Parameters; _SEMANTIC_LENSING.md item F-004. **PROPOSAL:** Mechanical Engineer to address in Guidance Considerations or DEL-003-07 Specification.

### Energy Efficiency of Exhaust Systems (NEW — E-002)

The building is located in a cold Alberta climate with significant heating costs. Exhausting heated indoor air in winter represents an energy penalty that should be considered during design:

- **Heat recovery from exhaust air:** The high-volume air exchanger (SOW-0036) implies that heat recovery is valued for the building's overall air handling system. The Mechanical Engineer should assess whether any exhaust streams (particularly the high-volume repair bay exhaust) warrant heat recovery, or whether the air exchanger's capacity is sufficient to offset exhaust heat losses.
- **Variable frequency drives (VFDs) on exhaust fans:** Where exhaust demand varies (e.g., repair bay exhaust needed only when vehicles are present), VFD-equipped fans or multi-speed operation can reduce energy consumption during low-demand periods.
- **Demand-controlled ventilation (non-pit zones):** For zones where exhaust is not required continuously (e.g., general shop exhaust when no vehicles are operating), demand-controlled ventilation via occupancy sensors or CO sensors can reduce unnecessary air exchange during unoccupied periods.

**ASSUMPTION:** Energy efficiency is a design consideration but not a primary driver for life-safety exhaust systems (service pit, welding LEV). For general exhaust and repair bay systems, energy-efficient options should be evaluated. Source: R-01 §3.4 (SOW-0036 implies heat recovery is valued); general cold-climate mechanical engineering practice; _SEMANTIC_LENSING.md item E-002. **PROPOSAL:** Mechanical Engineer to address in design trade-offs.

---

## Trade-offs

| Trade-off | Option A | Option B | Recommendation | Source |
|---|---|---|---|---|
| Repair bay exhaust: hose-reel drops vs. overhead capture | Flexible exhaust hose reels connected to vehicle tailpipe (source capture; best occupational hygiene) | Overhead general exhaust fans at high level (dilution; simpler but less effective at breathing zone) | **ASSUMPTION:** Hose-reel source capture preferred given heavy diesel equipment and high ceilings; RFP explicitly states "exhaust hoses" (SOW-0038). | R-01 §3.4 SOW-0038 |
| Welding exhaust: local exhaust ventilation (LEV) vs. dilution | LEV with capture hood at welding station (high capture efficiency, lower airflow) | Dilution ventilation via roof exhaust fans (simple, but high airflow needed) | **ASSUMPTION:** LEV preferred at welding station for fume control efficacy; may be supplemented by dilution | R-01 §3.4; Alberta OHS Code (location TBD) |
| Exhaust termination: roof vs. wall | Roof termination (preferred — avoids re-entrainment at grade, clear of vehicle traffic) | Wall termination (simpler ductwork, potential re-entrainment and frost issues) | **ASSUMPTION:** Roof termination preferred for exhaust stacks; coordinate with architectural/structural for roof penetrations | Cold climate engineering practice |
| Service pit ventilation: continuous vs. demand-controlled | Continuous mechanical ventilation during occupied hours (safer for gas accumulation) | Demand-controlled (CO/gas sensor activated; lower energy) | TBD — depends on Alberta OHS Code requirements for this pit type and sensor cost. **Decision pathway (B-004):** (1) Research applicable Alberta OHS Code provisions for below-grade service areas in industrial vehicle maintenance shops; (2) Determine if the pit meets the regulatory definition of "restricted space" or "confined space" under Alberta OHS Code Part 5; (3) If continuous ventilation is required by code, this trade-off is resolved; if not, evaluate CO/gas sensor demand-controlled ventilation with fail-safe to continuous. **PROPOSAL:** Mechanical Engineer + safety consultant to resolve. | R-01 §3.4 SOW-0028; Alberta OHS Code (location TBD); B-004 |
| Exhaust fan energy management: constant speed vs. VFD | Constant-speed fans (simpler controls, constant airflow) | VFD-equipped or multi-speed fans (energy savings during low-demand periods; higher capital cost) | **ASSUMPTION:** VFD or multi-speed operation is worth evaluating for repair bay exhaust fans where demand varies with vehicle presence; not applicable to continuous-duty systems (service pit, welding LEV during use). See E-002. | E-002; cold-climate energy practice |

> **Note (B-004):** The service pit ventilation trade-off row has been strengthened with a decision pathway to address the previously undefined resolution path. The prior version stated only "TBD -- depends on Alberta OHS Code requirements." Source: Guidance Trade-offs table; _SEMANTIC_LENSING.md item B-004.

---

## Examples

> No project-specific examples are available from the accessible sources. The conceptual floor plan (R-04 App B) shows the spatial location of the welding station, repair bays, and service pit, which inform system configuration. Specific product or system examples are TBD pending the Mechanical Engineer's design development.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CFT-001 | Boundary between DEL-003-03 (Ductwork & Distribution Plans) and DEL-003-04 (Exhaust Plans) is not defined in the decomposition. Exhaust ductwork could be shown in either deliverable, creating potential duplication or gap. This conflict also affects whether wash bay exhaust (B-003) is in scope of DEL-003-04 or split with DEL-003-02. | Decomposition §7 DEL-003-03 (Ductwork & Distribution Plans) | Decomposition §7 DEL-003-04 (Exhaust Plans) | Specification REQ-001, REQ-002, REQ-003; Specification Scope (wash bay); Guidance — Drawing Set Organization; Procedure Step 3 | PROPOSAL: DEL-003-03 covers supply/return/distribution ductwork; DEL-003-04 covers all exhaust-specific ductwork, hose systems, and exhaust fan units. Wash bay exhaust is in DEL-003-04 scope. Confirm with Mechanical Engineer. | TBD |
| CFT-002 | R-05 App B-Elec (electrical drawing showing exhaust fan locations) was referenced but not accessible in sufficient detail during this drafting pass. Exhaust fan locations and quantities cannot be confirmed against the electrical conceptual drawing. This data gap also affects verification of REQ-004 (E-003). | R-01 §3.4 / R-04 App B (mechanical scope) | R-05 App B-Elec (electrical drawing — not fully reviewed) | Specification REQ-004; Datasheet — Exhaust Fans (general); Specification Verification REQ-004 row | PROPOSAL: Coordination meeting between Mechanical Engineer and Electrical Engineer during design development to resolve fan locations and quantities; Electrical Engineer / DEL-004 team to provide R-05 detail. | TBD |
| CFT-003 | DEL-003-03 vs DEL-003-04 ductwork scope boundary as it affects this deliverable's completeness appraisal. Guidance CFT-001 proposes DEL-003-04 covers "all exhaust-specific ductwork" but this assumption has no confirmed authority. | Guidance CFT-001 (DEL-003-04 exhaust ductwork scope proposal) | Decomposition §7 DEL-003-03 (no explicit boundary defined) | Specification Scope; Guidance Drawing Set Organization; Procedure Step 3 | PROPOSAL: Per CFT-001 proposal — DEL-003-04 covers exhaust-specific ductwork. This conflict is a sub-issue of CFT-001. | TBD |

> **Note (D-003):** CFT-003 has been added to explicitly surface the ductwork scope boundary conflict for human ruling. The prior CFT-001 addressed the boundary but did not explicitly note that this assumption lacks confirmed authority. Source: _SEMANTIC_LENSING.md item D-003.
