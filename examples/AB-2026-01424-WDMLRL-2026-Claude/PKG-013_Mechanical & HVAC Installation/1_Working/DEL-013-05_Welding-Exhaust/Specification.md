# Specification — DEL-013-05: Welding Station Exhaust System

---

## Scope

### Included

This specification governs the design, supply, installation, testing, and commissioning of the dedicated welding station exhaust (local exhaust ventilation) system in the New North Shop, as required by RFP §3.4 (R-01) and Appendix B (R-04).

The system includes:
- Welding station exhaust hood(s)
- Flexible exhaust ductwork connections
- Filtration system for welding fumes and metal particulates
- Exhaust fan(s)
- Exterior exhaust outlet and stack
- Controls and monitoring
- Performance testing and commissioning

### Excluded

- Welding equipment itself (County to supply; R-01 §3.4)
- Welding station electrical power outlets (scope of PKG-015 Electrical)
- General building HVAC (DEL-013-01 through DEL-013-04, DEL-013-06)
- Architectural penetrations design (structural/envelope coordination is PKG-011 scope; this deliverable specifies the mechanical system only)
- Mechanical design engineering (design is proponent responsibility per CCDC 14–2013 design-build; this specification establishes functional and compliance requirements)

### Design-Build Compliance Responsibility

Per CCDC 14–2013 design-build contract, the Mechanical Contractor's P.Eng. is responsible for the system design, including confirming code compliance within the design. The Authority Having Jurisdiction (AHJ) independently confirms compliance at inspection. The County may separately retain a code reviewer, but this is outside the scope of this specification. TBD: Confirm division of compliance responsibility via CCDC 14–2013 contract terms. [F-001]

---

## Requirements

### REQ-001 — Source Capture
**Requirement:** The exhaust system shall capture welding fumes and metal particulates at the point of generation at the welding station(s).
**Source:** R-01 §3.4 ("Ventilation at welding station"); _CONTEXT.md ("Safe capture of welding fumes at source")
**Priority:** Mandatory

### REQ-002 — Welding Station Hood Installation
**Requirement:** An exhaust hood shall be installed at each welding station. Hood type, placement, and airflow shall be sufficient to achieve effective capture of fumes before dispersion into the shop environment.
**Source:** _CONTEXT.md; R-04 (Appendix B — Welding Station shown on floor plan, "Welding Station Exhaust System" noted)
**Note:** Number of welding stations is TBD pending workstation layout finalization (_STATUS.md). See Guidance CT-002.

### REQ-003 — Flexible Ductwork Connections
**Requirement:** Flexible exhaust ductwork shall connect the hood(s) to the duct system. Flexible connections shall accommodate repositioning of the welding workstation within the designated welding area.
**Source:** _CONTEXT.md; _DEPENDENCIES.md

### REQ-004 — Filtration for Fumes and Particulates
**Requirement:** The system shall include a filtration unit capable of capturing welding fumes (gaseous and particulate) and metal particulates to the efficiency required by applicable Alberta OHS Code exposure limits and/or environmental discharge requirements.
**Source:** _CONTEXT.md ("Proper metal particulate filtration"); _DEPENDENCIES.md ("Filtration critical for particulate control")
**Note:** Filter type and efficiency rating are TBD pending mechanical design. Minimum efficiency shall meet regulatory requirements (see Standards section).

### REQ-005 — Exhaust Fan
**Requirement:** An exhaust fan of sufficient capacity shall be provided to maintain required capture velocity at the hood(s) under operating conditions.
**Source:** _CONTEXT.md; standard LEV design practice (ASSUMPTION)
**Note:** Fan size (CFM), static pressure, motor rating, and mounting location TBD per mechanical design.

### REQ-006 — Exterior Exhaust Outlet and Stack
**Requirement:** The system shall discharge exhaust to the building exterior via a stack or outlet that:
(a) prevents re-entry of exhaust into the building through doors, windows, or air intakes;
(b) meets minimum discharge height requirements per applicable codes and environmental regulations — TBD: specific code clause establishing minimum height to be identified by mechanical engineer at design stage (ASSUMPTION: NBC/Alberta Building Code mechanical exhaust provisions govern; location TBD) [E-003];
(c) is located and oriented to minimize nuisance to adjacent areas.
**Source:** _CONTEXT.md ("Proper outlet location and height"); _DEPENDENCIES.md ("Exhaust outlet location approval" as external dependency)
**Note:** Outlet location and stack height are TBD pending design and authority approval.

### REQ-007 — Controls and Monitoring
**Requirement:** The system shall include controls enabling operational on/off control of the exhaust fan. Monitoring sufficient to indicate system operational status shall be provided.
**Source:** _CONTEXT.md ("Controls and monitoring")
**Note:** Interlock with welding equipment operation is TBD per design. Given cold-climate energy implications (see Guidance Considerations "Cold Climate Stack Considerations"), the mechanical engineer should evaluate whether fan interlock with welding station operation should be mandatory to reduce unnecessary exhaust of conditioned air. ASSUMPTION: interlock is recommended but not yet confirmed as a requirement; decision to be resolved at design stage. [D-002]

### REQ-008 — Filtration Maintainability
**Requirement:** The filtration unit shall be designed to allow filter cleaning and/or element replacement without requiring system disassembly or special tools beyond what is readily available in a maintenance shop environment.
**Source:** _DEPENDENCIES.md ("System must be cleanable and filtration maintainable")

### REQ-009 — Makeup Air Coordination
**Requirement:** The exhaust airflow volume shall be coordinated with DEL-013-03 (Forced-Air Makeup System) to ensure adequate makeup air is provided to replace extracted air volume. The exhaust system shall not create a building negative pressure condition that impairs operation of other systems or creates hazards.
**Source:** _DEPENDENCIES.md ("Makeup air balances welding exhaust"; "Exhaust volume affects makeup air requirements")

### REQ-010 — Code and Regulatory Compliance
**Requirement:** The installed system shall comply with all applicable codes and regulations, including but not limited to:
- Alberta Safety Codes (building and mechanical)
- Alberta OHS Code (welding fume exposure limits, LEV requirements)
- Alberta Environmental Protection and Enhancement Act (EPEA) — discharge permit requirements for welding exhaust stack emissions to be reviewed (TBD: confirm whether EPEA review is required for welding exhaust discharge in this jurisdiction) [C-002]
- National Building Code of Canada (as adopted in Alberta via the Alberta Safety Codes Act) — location TBD
**Source:** R-01 §3.3.2 ("The building design must adhere to all applicable building codes and regulations"; "The proposed building must adhere to all Alberta Safety Codes"); _CONTEXT.md ("Code-compliant and OSHA-compliant installation; Environmental compliance")
**Note:** "OSHA-compliant" in _CONTEXT.md is interpreted as the applicable Alberta OHS Code requirements (ASSUMPTION: _CONTEXT.md reference to OSHA maps to Alberta OHS Code in the Alberta jurisdiction context; see Guidance CT-001).

### REQ-011 — Performance Testing and Commissioning
**Requirement:** The system shall be tested and commissioned prior to project completion. Commissioning shall demonstrate that capture velocity, airflow volume, and filtration performance meet design intent and regulatory requirements.
**Source:** _CONTEXT.md ("Performance testing and commissioning"); R-01 OBJ-004 ("commission all mechanical systems to operational readiness")

### REQ-012 — Warranty
**Requirement:** All materials and workmanship shall be warranted for a minimum of two (2) years from the Construction Completion Certificate date (per R-01 §2.14), consistent with the guarantee period specified in RFP §2.10.
**Source:** R-01 §2.10.2
**Note:** Warranty certificates from equipment manufacturers (fan, filtration unit, controls) shall be collected, verified for conformance with the two-year minimum, and handed over to the County as part of the closeout documentation package. [E-004]

### REQ-013 — Fire and Spark Hazard Mitigation
**Requirement:** The mechanical engineer shall evaluate and address the fire/spark hazard from welding particulates in exhaust ductwork and the filtration unit. Where the evaluation identifies a risk, appropriate mitigation measures (e.g., spark arrestor upstream of the filtration unit, noncombustible ductwork materials, filtration unit positioning to minimize duct length within the building) shall be incorporated into the design.
**Source:** Guidance.md Considerations ("Fire and Spark Arrest"); standard industrial LEV practice (ASSUMPTION: fire/spark evaluation is standard practice for welding exhaust systems)
**Priority:** Mandatory — evaluation required; specific mitigation measures TBD per design engineer's assessment [B-004]

---

## Standards

The following standards are identified as likely applicable. Specific editions and clauses are TBD pending formal design and regulatory review. **Note:** The mechanical design engineer should confirm applicable editions at design stage (Step 1.3) to enable compliance determination. [A-002]

| Standard | Authority | Applicability | Accessibility |
|---|---|---|---|
| Alberta Safety Codes Act and regulations | Province of Alberta | Governing building and mechanical code in Alberta; Alberta adopts the National Building Code via the Safety Codes Act (see Guidance for regulatory relationship explanation) | ASSUMPTION: applicable; specific code edition TBD |
| Alberta OHS Code — welding fume and LEV | Alberta Government | Occupational exposure limits, LEV requirements for welding | ASSUMPTION: applicable; specific Part TBD |
| National Building Code of Canada (NBC), adopted edition | NRC / Province of Alberta | Building and mechanical system requirements; adopted in Alberta via Safety Codes Act | ASSUMPTION: applicable; edition TBD |
| ASHRAE standards (ventilation / LEV) | ASHRAE | Ventilation design guidance for industrial exhaust | ASSUMPTION: likely referenced in design; location TBD |
| ACGIH Industrial Ventilation Manual | ACGIH | LEV design guidance and capture velocity tables | ASSUMPTION: likely referenced in design; location TBD |
| AWS (American Welding Society) fume control publications | AWS | Welding fume control guidance | ASSUMPTION: likely applicable; specific document TBD |
| Alberta Environmental Protection and Enhancement Act (EPEA) / regulations | Province of Alberta | Environmental discharge from exhaust stack; TBD whether discharge permit is required for welding exhaust | ASSUMPTION: applicable; specific regulation TBD |

---

## Verification

| Requirement | Verification Approach |
|---|---|
| REQ-001 (Source Capture) | Commissioning airflow measurement at hood; source capture verification using a defined test method — TBD: mechanical engineer to specify whether smoke test, tracer gas test, or anemometer traverse will be used, and define quantitative pass/fail criteria including minimum capture velocity value (ASSUMPTION: method and acceptance threshold TBD per mechanical engineer's commissioning plan, informed by ACGIH tables for welding) [A-003, X-004, X-005] |
| REQ-002 (Hood Installation) | Visual inspection against IFC drawings; measurement of hood position relative to welding station |
| REQ-003 (Flexible Ductwork) | Visual inspection; demonstration of workstation repositioning range |
| REQ-004 (Filtration) | Filter specification review against regulatory requirements; commissioning efficiency test (method TBD) |
| REQ-005 (Exhaust Fan) | Airflow (CFM) measurement at commissioning; comparison to design specification. TBD: acceptable CFM tolerance to be defined by mechanical engineer. |
| REQ-006 (Exhaust Outlet) | Visual inspection of outlet location; measurement of stack height against minimum code requirement (TBD: specific code clause to be identified at design stage) [E-003]; review against code requirements |
| REQ-007 (Controls) | Functional test of on/off control and status indication; interlock test (if installed) |
| REQ-008 (Maintainability) | Demonstration of filter access and replacement procedure. Note: this is a one-time commissioning demonstration confirming physical accessibility; ongoing maintenance frequency and responsibility post-handover are defined in the O&M manual (see Documentation and Procedure Step 5.2). [X-006] |
| REQ-009 (Makeup Air Coordination) | Building pressure measurement or airflow balance confirmation at commissioning (coordinate with DEL-013-03) |
| REQ-010 (Code Compliance) | Authority Having Jurisdiction (AHJ) inspection and sign-off; Safety Code permit close-out |
| REQ-011 (Commissioning) | Commissioning report documenting airflow, capture velocity, and filtration performance results; quantitative pass/fail thresholds to be established at IFC design stage [A-003] |
| REQ-012 (Warranty) | Contract documents; CCC date (per R-01 §2.14) establishes warranty start; warranty certificates collected from equipment manufacturers |
| REQ-013 (Fire/Spark) | Design engineer's documented fire/spark hazard evaluation; inspection of installed mitigation measures |

---

## Filtration Selection Criteria

The following evaluation criteria should be applied when selecting the filtration unit at procurement (Procedure Step 2.2). This section supports a structured merit evaluation rather than selection solely on regulatory minimum efficiency. [D-003]

| Criterion | Consideration | Source |
|---|---|---|
| Regulatory efficiency | Must meet Alberta OHS Code exposure limits for all anticipated welding processes and base metals | Specification REQ-004 |
| Lifecycle cost | Total cost of ownership including filter replacement frequency and energy consumption | ASSUMPTION: standard procurement consideration |
| Filter replacement frequency | Frequency and ease of filter element replacement; availability of replacement elements | Specification REQ-008; _DEPENDENCIES.md |
| Noise level | Fan and filtration unit noise at operating conditions; impact on shop working environment | TBD |
| Recirculation capability | Whether unit can recirculate filtered air to retain conditioned air in cold climate (only if filtration efficiency is confirmed adequate) | Guidance CT-003; Guidance Trade-offs |
| Multi-stage vs. single-stage | Pre-filter + main filter configuration for longer main filter life at higher welding volumes | Guidance Trade-offs |
| Physical size and access | Unit footprint, ceiling clearance, and maintenance access envelope | ASSUMPTION: standard procurement consideration |

---

## Documentation

The following artifacts are anticipated upon completion of this deliverable:

| Artifact | Description |
|---|---|
| IFC Mechanical Drawing | Issued-for-Construction drawing of welding exhaust system (P.Eng.-stamped, Alberta-licensed engineer) |
| Equipment specifications / cut sheets | Fan, filtration unit, hood, and controls product data |
| Installation record | As-built drawing reflecting installed ductwork routing and component locations |
| Photographic record of concealed work | Photographs documenting concealed installations (ductwork routing through walls/ceiling, penetration flashing) taken before closure. ASSUMPTION: standard practice for mechanical installations where ductwork may be concealed. [X-003] |
| Commissioning report | Airflow measurements, capture velocity results, filtration performance, system sign-off |
| Safety Code inspection reports | Copies of all inspection reports from Authority Having Jurisdiction |
| O&M manual | Operation and maintenance manual for exhaust fan, filtration unit, and controls; includes filter replacement schedule and procedure defining ongoing maintenance (see REQ-008 verification note) |
| Alberta OHS Code compliance documentation | Documentation confirming Alberta OHS Code compliance for welding fume control |
| Environmental compliance record | Exhaust outlet/stack location and height approval documentation; EPEA review documentation if required [C-002] |
| Warranty certificates | Equipment manufacturer warranty certificates (fan, filtration unit, controls) collected, verified for two-year minimum conformance, and included in closeout package [E-004] |

### P.Eng. Stamp Scope

The following documents require P.Eng. stamp by an Alberta-licensed engineer. TBD: Confirm whether the scope extends beyond IFC drawings to include commissioning report and/or system design calculations. [F-002]

| Document | P.Eng. Stamp Required | Status |
|---|---|---|
| IFC Mechanical Drawing | Yes | Confirmed (R-01 §3.3.2; Procedure Step 1.3) |
| Commissioning report | TBD | ASSUMPTION: may require P.Eng. certification depending on AHJ requirements |
| System design calculations | TBD | ASSUMPTION: typically part of design package; confirm with Mechanical Contractor |
| Filtration performance certification | TBD | ASSUMPTION: may be manufacturer-certified rather than P.Eng.-certified |
