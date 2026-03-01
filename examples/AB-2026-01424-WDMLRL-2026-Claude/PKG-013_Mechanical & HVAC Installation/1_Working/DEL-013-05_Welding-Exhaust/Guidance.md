# Guidance — DEL-013-05: Welding Station Exhaust System

---

## Purpose

The welding station exhaust system exists to protect workers from hazardous welding fumes and metal particulates generated during welding operations in the New North Shop. Welding fumes contain a complex mixture of metal oxides, flux compounds, and gases (including carbon monoxide and ozone depending on the welding process) that present acute and chronic health risks at sustained exposure levels.

The RFP explicitly requires "Ventilation at welding station" (R-01 §3.4) and the conceptual building notes on Appendix B (R-04) list "Welding Station Exhaust System" as a required building feature. This deliverable satisfies SOW-0039 ("Install welding station ventilation/exhaust system") and supports:
- **OBJ-001**: Deliver a code-compliant, fully functional maintenance shop that passes all applicable inspections.
- **OBJ-004**: Install and commission all mechanical systems to operational readiness.

Source-capture local exhaust ventilation (LEV) is the preferred and most effective approach for welding fumes because it captures contaminants before they disperse into the shop breathing zone, reducing the required airflow volume compared to dilution ventilation.

---

## Principles

### 1. Capture at Source Is Non-Negotiable
Alberta OHS Code requirements for welding fume control and the ACGIH Industrial Ventilation guidance (ASSUMPTION: applicable; location TBD) both establish that source-capture LEV is the primary engineering control. Dilution ventilation alone is generally insufficient for welding fumes. The design must prioritize capture efficiency at the hood.

**Health exposure basis:** The non-negotiable nature of source capture is grounded in occupational exposure limits for welding fumes. The Alberta OHS Code (ASSUMPTION: Schedule 1, Table 2, or equivalent) establishes time-weighted average (TWA) threshold limit values (TLVs) for welding fume constituents (e.g., iron oxide, manganese, hexavalent chromium depending on base metal and process). These TLVs are set at levels where sustained exposure without engineering controls poses documented health risks including metal fume fever, manganism, and respiratory disease. Source capture is the primary means of keeping worker exposure below these limits. TBD: Confirm specific TLV values and Schedule/Table references when the applicable Alberta OHS Code edition is confirmed. [C-003]

### 2. Hood Type Drives System Performance
The choice between a fixed-position enclosing hood, a backdraft/sidedraft hood, or an articulating-arm extraction unit (which can be repositioned close to the weld point) significantly affects capture efficiency and required CFM. The Appendix B floor plan (R-04) shows a single welding station in the northeast corner of the shop. The welding equipment specifications (to be provided by the County per R-01 §3.4) will inform which hood type is appropriate.

### 3. Flexible Ductwork for Workstation Adaptability
The _DEPENDENCIES.md notes that flexible ductwork is needed to allow workstation repositioning. This is important in a maintenance shop environment where work-piece size varies. The design should accommodate reasonable repositioning range while maintaining the capture distance within the hood's effective capture radius.

### 4. Filtration Selection Depends on Process
Welding fume filtration options range from simple HEPA filter banks to self-cleaning cartridge units. In a cold-climate Alberta maintenance shop, a recirculating filtered unit may be considered to recover conditioned air, but only if filtration efficiency is demonstrably sufficient to meet Alberta OHS Code exposure limits for all anticipated welding processes and base metals. ASSUMPTION: if recirculation is considered, the mechanical engineer must confirm filtration efficiency meets regulatory requirements for the specific welding processes used. See also Specification "Filtration Selection Criteria" section for procurement evaluation framework.

### 5. Exhaust Stack Location Requires Early Decision
The exhaust outlet location affects both the building envelope design (PKG-011) and environmental review. The outlet must be positioned to prevent re-entrainment into the building (particularly through the forced-air makeup inlets from DEL-013-03) and must meet minimum height above the roofline. This is identified in _DEPENDENCIES.md as an "Exhaust outlet location approval" external dependency. Early design coordination is recommended.

### 6. Makeup Air Balance Is a System-Level Concern
The welding exhaust system does not operate in isolation. Extracting air from the building creates negative pressure that must be compensated by makeup air (DEL-013-03). If the welding exhaust fan runs while the makeup air system is off or undersized, the building can go significantly negative, creating drafts at overhead doors, potential combustion appliance backdrafting, and worker comfort issues. The mechanical design must confirm airflow balance.

---

## Considerations

### Welding Station Count
The _STATUS.md notes that "welding station locations" require finalization. The Appendix B floor plan shows one welding station in the northeast corner. If additional welding stations are added during the design phase, the exhaust system capacity, ductwork layout, and makeup air requirements must be re-evaluated. ASSUMPTION: the current scope is based on one welding station unless the County confirms otherwise. See CT-002 in Conflict Table.

### Alberta Jurisdiction vs. OSHA Reference
The _CONTEXT.md references "OSHA-compliant installation." This project is in Alberta, Canada; the applicable occupational health and safety authority is the Alberta OHS Code (under the Occupational Health and Safety Act, Alberta), not US federal OSHA. ASSUMPTION: the _CONTEXT.md reference to OSHA is intended to mean "equivalent occupational health and safety compliance under Alberta OHS Code." The mechanical engineer must design to Alberta OHS Code requirements. See Conflict Table entry CT-001 below.

**Note on terminology normalization:** All four production documents (Datasheet, Specification, Guidance, Procedure) use "Alberta OHS Code" as the standard term for the applicable occupational health authority. The term "OSHA" has been removed from document body text except where quoting source documents directly. The _REFERENCES.md file (a metadata file not modified by this agent) retains the original "OSHA" language from seeding. [A-001]

### Alberta Regulatory Framework — Safety Codes Act and NBC Relationship
The Alberta Safety Codes Act is the provincial legislative framework under which building, fire, electrical, gas, plumbing, and other safety codes are adopted and enforced. The National Building Code of Canada (NBC) is adopted in Alberta through regulations under the Safety Codes Act, with Alberta-specific amendments. This means that compliance with "Alberta Safety Codes" and compliance with "NBC as adopted in Alberta" are not separate obligations — the Safety Codes Act is the mechanism by which NBC requirements become enforceable in Alberta. The Specification Standards table lists both to be explicit, but the design engineer should reference the Alberta-adopted edition of the NBC (and its Alberta amendments) as the authoritative code text. [C-001]

### Cold Climate Stack Considerations
In Alberta winters, a continuously exhausting stack can contribute to building heat loss. If the system runs continuously during shop hours, the makeup air system (DEL-013-03) will be conditioning cold outdoor air continuously. The mechanical engineer should consider:
- Blast gate or damper to close the exhaust when welding is not in progress
- Interlocking the exhaust fan with the welding station operation (see Specification REQ-007 note regarding interlock decision)
- Insulating the exhaust duct to prevent condensation of metal particulates in cold conditions

**Energy cost framing:** The energy impact of continuous welding exhaust in Alberta winter conditions is significant but difficult to quantify without design parameters. As a directional reference: exhausting conditioned air and replacing it with outdoor air at extreme Alberta winter temperatures (e.g., -30C to -40C) imposes a heating load on the makeup air system (DEL-013-03) proportional to the exhaust volume. TBD: The mechanical design engineer should quantify the approximate heat loss per unit of exhaust airflow (e.g., per 1,000 CFM) at design winter temperature as part of the energy evaluation at the design stage. This quantification will inform the interlock vs. continuous operation decision (see REQ-007). [F-003]

### Ductwork Material
Welding exhaust ductwork should be fabricated from materials resistant to the temperatures generated by welding fumes (which can be significantly hotter than ambient). Standard galvanized steel ductwork is commonly used. ASSUMPTION: ductwork material specification TBD per mechanical engineer's design.

### Fire and Spark Arrest
Metal particulates in welding exhaust can present a fire hazard, particularly where ductwork passes through or near combustible materials. ASSUMPTION: the mechanical engineer should evaluate the need for spark arrestors upstream of the filtration unit. Filtration unit location relative to the exterior wall should minimize duct length within the building. See Specification REQ-013 for the corresponding requirement.

### Coordination with DEL-013-04 (Heavy Equipment Exhaust)
DEL-013-04 is a separate exhaust system for heavy equipment repair bays. Both systems extract air from the same building volume. System interactions (aggregate exhaust volume, duct routing, fan noise, stack proximity) should be coordinated at the mechanical design stage. _DEPENDENCIES.md notes "Separate exhaust system coordination."

---

## Trade-offs

| Trade-off | Option A | Option B | Consideration |
|---|---|---|---|
| Exhaust vs. Recirculation | Exhaust to exterior (simpler, no re-exposure risk) | Filtered recirculation (retains conditioned air; saves heating cost) | Recirculation only acceptable if filtration efficiency is confirmed adequate for all welding processes. Alberta winters make recirculation attractive for energy cost. Engineering decision required. See CT-003. |
| Articulating arm hood vs. fixed hood | Articulating arm — higher capture efficiency, repositionable | Fixed backdraft hood — simpler, lower cost, less flexible | Depends on County's welding operations (work-piece size, frequency). Welding equipment specs (from County) will inform this. |
| Inline fan vs. roof-mounted fan | Inline fan in duct — quieter at work area, more accessible | Roof-mounted fan — farthest from work area, may freeze bearings in Alberta winter | Alberta climate suggests preference for indoor-accessible fan with external stack. ASSUMPTION. |
| Single-stage vs. multi-stage filtration | Single-stage cartridge — simpler, lower cost | Multi-stage (pre-filter + HEPA) — higher capture, longer main filter life | Multi-stage preferred if high welding volume or high-particulate processes anticipated. See Specification Filtration Selection Criteria. |
| Continuous vs. interlocked exhaust fan | Continuous operation — simpler controls, constant extraction | Interlocked with welding station — reduces energy loss when not welding | Cold-climate energy cost favors interlock; interlock adds complexity and requires welding equipment compatibility. See REQ-007 note and Cold Climate Stack Considerations above. [D-002] |

---

## Examples

No project-specific examples are available from the accessible source documents. General welding LEV configurations are described in ACGIH Industrial Ventilation Manual (ASSUMPTION: applicable; location TBD) and AWS fume control publications (ASSUMPTION: applicable; location TBD).

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CT-001 | Jurisdiction for occupational health compliance: _CONTEXT.md references "OSHA-compliant installation" but the project is in Alberta, Canada, where the Alberta OHS Code applies. All production documents have been normalized to use "Alberta OHS Code" terminology. [A-001] | _CONTEXT.md ("Code-compliant and OSHA-compliant installation") | R-01 §2.22 ("law of the Province of Alberta"); R-01 §3.3.2 ("Alberta Safety Codes") | Specification.md REQ-010; Procedure.md Prerequisites; Datasheet.md Attributes (Filtration efficiency, Regulatory environment) | PROPOSAL: Interpret "OSHA-compliant" in _CONTEXT.md as Alberta OHS Code compliance. Design and commission to Alberta OHS Code. | TBD |
| CT-002 | Number of welding stations: _STATUS.md indicates layout not finalized; Appendix B shows one welding station; _DEPENDENCIES.md notes "Multiple exhaust hoods may be needed." Directive authority for the station count is unresolved; station count directly impacts system capacity, ductwork layout, fan sizing, and makeup air requirements. [D-001] | R-04 (Appendix B — one welding station shown) | _DEPENDENCIES.md ("Multiple exhaust hoods may be needed") | Datasheet.md Attributes; Specification.md REQ-002, REQ-005, REQ-009 | PROPOSAL: County to confirm count. Design for one station with expansion capability. | TBD |
| CT-003 | Filtration recirculation vs. exhaust-only: no source document specifies whether the system exhausts to exterior only or may recirculate filtered air | _CONTEXT.md ("Exhaust outlet and stack installation" implies exterior exhaust) | _DEPENDENCIES.md (no explicit requirement either way) | Specification.md REQ-004, REQ-006; Guidance.md Trade-offs | PROPOSAL: Default to exterior exhaust system. Recirculation may be evaluated by the mechanical engineer if filtration efficiency can be confirmed for all welding processes. | TBD |
| CT-004 | Post-installation filter maintenance verification scope: Specification Verification for REQ-008 describes a one-time commissioning demonstration of filter access and replacement; Procedure Step 5.2 / O&M manual implies recurring maintenance. The boundary between one-time verification and ongoing maintenance obligation is unclear. [X-006] | Specification.md Verification (REQ-008: one-time demonstration) | Procedure.md Phase 5, Step 5.2 (O&M manual with "Filter replacement schedule and procedure" implies recurring) | Specification.md Verification (REQ-008); Specification.md Documentation; Procedure.md Phase 5 | PROPOSAL: One-time demonstration at commissioning confirms physical accessibility; O&M manual defines ongoing maintenance frequency and responsibility post-handover to County. | TBD |
