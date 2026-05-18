# Datasheet — DEL-013-05: Welding Station Exhaust System

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-013-05 |
| Deliverable Name | Welding Station Exhaust System |
| Package | PKG-013 — Mechanical & HVAC Installation |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Location | SW 14–44–21–W4, near Ferintosh, Alberta |
| Responsible Party | Mechanical Contractor |
| Activity Type | Installation |
| SOW Reference | SOW-0039 |
| Objective Linkage | OBJ-001, OBJ-004 |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price |
| Completion Deadline | December 31, 2026 |
| Document Created | 2026-02-25 |

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| System type | Dedicated welding station local exhaust ventilation (LEV) | R-01 §3.4; R-04 |
| Primary function | Capture and remove welding fumes and metal particulates at source | _CONTEXT.md |
| Welding station location | Upper-right (northeast) corner of New North Shop main floor area | R-04 (Appendix B — Shop floor plan) |
| Number of welding stations | 1 shown on conceptual floor plan; final count TBD pending workstation layout finalization. See Guidance CT-002 for conflict between R-04 (1 station) and _DEPENDENCIES.md ("Multiple exhaust hoods may be needed"). | R-04; _STATUS.md; _DEPENDENCIES.md |
| Building ceiling height | 35 feet (concrete structure). ASSUMPTION: dimension sourced from R-04 (Appendix B floor plan); R-01 §3.4 provides HVAC scope context but is not the dimensional authority. See note [E-002]. | R-04 (primary dimensional source); R-01 §3.4 (HVAC scope context) |
| Building footprint (New North Shop) | Approximately 130 ft wide x 100 ft deep (main shop area). Note: "Approximately" qualifier reflects conceptual floor plan precision; confirm against dimensioned Appendix B drawing at design stage. | R-04 |
| Welding process types | TBD — County to supply welding equipment specifications (MIG, TIG, stick, flux-core, etc.) and base metals; required to determine fume character and filtration requirements. ASSUMPTION: County has not yet provided equipment specifications. | R-01 §3.4; Procedure Step 1.1 |
| Hood type | TBD — source-capture hood or articulating-arm hood (ASSUMPTION: source-capture hood typical for welding LEV; confirm with design engineer) | location TBD |
| Ductwork type | Flexible exhaust ductwork connections to welding station(s) | _CONTEXT.md |
| Filtration type | Filtration system for welding fumes and metal particulates | _CONTEXT.md |
| Fan configuration | Exhaust fan(s) — quantity, size, and static pressure rating TBD | TBD |
| Exhaust outlet/stack | Exterior exhaust outlet and stack — location and height TBD pending design | _CONTEXT.md; _DEPENDENCIES.md |
| Controls | Controls and monitoring — type TBD | _CONTEXT.md |
| Airflow capacity (CFM) | TBD — to be determined by mechanical design engineer based on welding process, hood type, and capture velocity requirements | TBD |
| Capture velocity | TBD — minimum per applicable standards. This is the single most critical design parameter for a welding LEV system; drives hood selection, fan sizing, and ductwork design. ASSUMPTION: ACGIH Industrial Ventilation Manual tables for welding to be applied by mechanical design engineer; specific numeric value TBD at design stage (Step 1.3). | TBD; ACGIH guidance (location TBD) |
| Static pressure | TBD | TBD |
| Filtration efficiency | TBD — must meet Alberta OHS Code requirements for welding fume (see Guidance CT-001 re: jurisdiction clarification) | _CONTEXT.md; Guidance CT-001 |
| Electrical supply | TBD — 3-phase power available in building per R-01 §3.4 | R-01 §3.4 |
| Welding equipment specs | County to supply welding equipment specifications (noted in RFP) | R-01 §3.4 |
| Rigid ductwork material | TBD — material specification to be determined by mechanical design engineer (ASSUMPTION: galvanized steel typical for welding LEV; see Guidance Considerations "Ductwork Material") | TBD; Guidance.md |
| Spark arrestor requirement | TBD — mechanical engineer to evaluate need for spark arrestor upstream of filtration unit (see Guidance Considerations "Fire and Spark Arrest") | TBD; Guidance.md |
| Recirculation vs. exhaust-only | TBD — default is exhaust-to-exterior; recirculation may be evaluated if filtration efficiency can be confirmed (see Guidance CT-003 and Trade-offs) | Guidance CT-003 |
| Noise/vibration limits | TBD — no numeric noise or vibration limits identified in source documents; to be established at design stage | TBD |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Operating environment | Indoor industrial maintenance shop; cold climate (Alberta) | R-01 §3.1; R-07 |
| Contaminants handled | Welding fumes (hot gases, metal oxides, flux particulates) and metal particulates generated during welding operations | _CONTEXT.md |
| Ambient temperature range | Cold-climate Alberta conditions; interior heated by DEL-013-01 (high-recovery heating system) | _DEPENDENCIES.md; R-01 |
| Exhaust volume impact | Exhaust volume must be balanced by makeup air from DEL-013-03 (Forced-Air Makeup System) | _DEPENDENCIES.md |
| Heat recovery interface | Potential heat recovery interface with DEL-013-01 (ASSUMPTION: welding exhaust heat recovery integration is an open design question) | _DEPENDENCIES.md |
| Flexible connection requirement | Flexible ductwork connections required to accommodate welding workstation repositioning | _DEPENDENCIES.md |
| Filtration maintenance | Filtration system must be cleanable and filter elements must be replaceable | _DEPENDENCIES.md |
| Regulatory environment | Alberta Safety Codes (provincial building and mechanical), Alberta OHS Code (occupational health and safety), Alberta Environmental Protection and Enhancement Act (EPEA) for potential discharge requirements. Note: all regulatory references in these documents use "Alberta OHS Code" as the applicable occupational health authority per Guidance CT-001. | R-01 §3.3.2; _CONTEXT.md; Guidance CT-001 |

---

## Construction

| Element | Description | Source |
|---|---|---|
| Welding exhaust hood(s) | Local exhaust hood(s) positioned at or near the welding station to capture fumes at source | _CONTEXT.md; R-04 |
| Flexible ductwork | Flexible exhaust ductwork connecting hood(s) to rigid duct system or directly to fan; allows workstation repositioning | _CONTEXT.md; _DEPENDENCIES.md |
| Rigid ductwork (if applicable) | TBD — rigid duct run from flexible duct transition to exhaust fan and outlet; routing TBD per final mechanical design; material specification TBD (see Attributes) | TBD |
| Filtration unit | Welding fume and metal particulate filtration unit — type (cartridge, HEPA, etc.) TBD per design | _CONTEXT.md |
| Exhaust fan | Inline or external exhaust fan — size, motor, and mounting TBD | _CONTEXT.md |
| Exhaust outlet / stack | Exterior exhaust outlet and stack penetrating building envelope; location TBD; minimum height above roofline TBD per code and environmental requirements | _CONTEXT.md; _DEPENDENCIES.md |
| Controls and monitoring | On/off control and operational monitoring — interlock with welding station operation TBD | _CONTEXT.md |
| Support structure | Ductwork hangers, brackets, and supports — TBD per mechanical drawing | TBD |
| Spark arrestor (if required) | TBD — evaluation required for spark arrestor upstream of filtration unit per fire/spark hazard assessment (see Guidance Considerations) | TBD; Guidance.md |

---

## References

| Ref ID | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.4 — "Ventilation at welding station" design requirement; §3.3.2 — general project scope; welding equipment plug note |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan showing welding station location (northeast corner, New North Shop); building dimensions (primary dimensional source); "Welding Station Exhaust System" listed in building notes |
| Decomposition | WDMLRL_Decomposition_Claude.md | SOW-0039, PKG-013, DEL-013-05 entry; OBJ-001 and OBJ-004 |
| _CONTEXT.md | DEL-013-05 _CONTEXT.md | Deliverable identity, scope, key requirements |
| _DEPENDENCIES.md | DEL-013-05 _DEPENDENCIES.md | Integration points with DEL-013-01, -02, -03; constraint notes |
| Standards (location TBD) | ACGIH Industrial Ventilation Manual | ASSUMPTION: likely referenced in design for capture velocity tables; specific edition TBD |
| Standards (location TBD) | Alberta OHS Code — welding fume exposure limits and LEV requirements | ASSUMPTION: likely applicable; specific Part and section TBD |
| Standards (location TBD) | AWS (American Welding Society) fume control guidelines | ASSUMPTION: likely applicable; specific document TBD |
| Standards (location TBD) | Alberta Environmental Protection and Enhancement Act (EPEA) — discharge requirements | ASSUMPTION: applicable for exhaust stack emissions; specific regulation TBD |
