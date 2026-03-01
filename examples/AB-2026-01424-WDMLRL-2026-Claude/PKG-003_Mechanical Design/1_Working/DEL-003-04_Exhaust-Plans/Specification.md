# Specification — DEL-003-04 Exhaust System Plans

---

## Scope

### What This Deliverable Covers

DEL-003-04 is the Exhaust System Plans drawing set for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition (New North Shop). It is one component of the overall final mechanical design required under SOW-0013 within PKG-003 — Mechanical Design.

This drawing set shall document the complete exhaust and ventilation systems for all identified exhaust sources within the building, including:

- Heavy equipment exhaust hose and fan systems in the two drive-through repair bays
- Welding station exhaust/ventilation system
- Service pit ventilation
- Wash bay exhaust/ventilation system
- General building exhaust fans
- Ceiling fan interaction assessment (air circulation patterns affecting exhaust capture)
- Coordination interfaces with the high-volume air exchanger (DEL-003-02/DEL-003-03) and forced-air makeup air system

**Source:** R-01 §3.4 (SOW-0038, SOW-0039); R-04 App B; Decomposition §7 DEL-003-04

> **Note (B-003):** Wash bay exhaust/ventilation system has been added to the scope list. The wash bay is an identified exhaust source (Datasheet Conditions; Guidance Principle 3) but was not previously listed in the scope statement. Scope inclusion is **ASSUMPTION** pending confirmation of DEL-003-04 vs. DEL-003-02 boundary. Source: R-01 §3.1, §3.4; _SEMANTIC_LENSING.md item B-003.

> **Note (C-002):** Ceiling fan interaction assessment has been added. See REQ-009 below. Source: _SEMANTIC_LENSING.md item C-002.

### What This Deliverable Excludes

| Excluded Item | Where Covered |
|---|---|
| HVAC heating system design | DEL-003-02 HVAC Plans |
| Ductwork distribution (non-exhaust) | DEL-003-03 Ductwork & Distribution Plans |
| Mechanical equipment schedule | DEL-003-05 Equipment Schedule |
| Mechanical calculations (load, fan sizing) | DEL-003-06 Calculation Package |
| Plumbing/drain systems | PKG-006 Plumbing Design |
| Electrical power supply to exhaust fans | PKG-004 Electrical Design (DEL-004 series) |
| Exhaust fan power circuits (panel circuits, power distribution) | DEL-004-03 (Power Distribution Plans), DEL-004-06 (Panel Schedules) |
| Structural penetrations and pit structure | PKG-002 Structural Design |
| Post-installation commissioning and functional testing | TBD -- may be covered by PKG-013 installation deliverables (see note C-003) |

> **Note (C-003):** Post-installation commissioning has been added to the exclusions table with a TBD scope assignment. Procedure covers design through IFC issue but does not address post-installation commissioning or functional performance verification. **PROPOSAL:** Confirm whether commissioning is covered by PKG-013 installation deliverables (DEL-013-04, DEL-013-05) or requires a separate scope assignment. Source: _SEMANTIC_LENSING.md item C-003.

---

## Requirements

### REQ-001 — Heavy Equipment Exhaust System (Repair Bays)

**Statement:** The Exhaust System Plans shall show exhaust hoses and fans for heavy equipment exhaust removal in the two drive-through repair bays.

**Source:** R-01 §3.4 ("Exhaust hoses and fans for heavy equipment in the repair bays."); SOW-0038

**Constraints:**
- Repair bays are 24' wide each (Source: R-01 §3.1, R-04 App B)
- Building ceiling height is 35 ft (Source: R-01 §3.4)
- Equipment class includes motor scraper and tracked heavy equipment (Source: R-01 §3.4, R-04 App B)
- Fan power supply must coordinate with electrical drawing (Source: R-05 App B-Elec, SOW-0066)

**Notes:** Number of exhaust drops, hose types, fan sizing, and duct routing are TBD pending mechanical calculations (DEL-003-06). **ASSUMPTION:** A minimum of one exhaust drop per repair bay is required; exact quantity determined by design.

> **Note (A-002):** The minimum exhaust drop quantity per repair bay is currently deferred to assumptions. This could change implementation decisions. **PROPOSAL:** Mechanical Engineer to confirm minimum exhaust drop quantity per DEL-003-06 calculations before finalizing this requirement. Source: Specification REQ-001 Notes; _SEMANTIC_LENSING.md item A-002.

---

### REQ-002 — Welding Station Exhaust System

**Statement:** The Exhaust System Plans shall show a dedicated exhaust/ventilation system at the welding station.

**Source:** R-01 §3.4 ("Ventilation at welding station."); R-04 App B (welding station shown at northeast corner of main shop area); SOW-0039

**Constraints:**
- Welding station is located as shown on conceptual drawing App B (northeast quadrant of main shop floor) (Source: R-04 App B)
- System must serve welding fume and heat extraction
- Coordination required with makeup air system (Source: R-04 App B, SOW-0037)

**Notes:** Specific welding station exhaust system type (local exhaust ventilation vs. dilution ventilation), airflow rates, and equipment are TBD pending calculations and applicable Alberta Safety Code requirements. **ASSUMPTION:** Local exhaust ventilation (LEV) at welding station is anticipated as the preferred approach for fume control; confirm against applicable Alberta OHS/code requirements.

---

### REQ-003 — Service Pit Ventilation

**Statement:** The service pit shall be ventilated. The Exhaust System Plans shall include the ventilation system for the below-grade service pit.

**Source:** R-01 §3.4 ("Ventilated and lighted service pit area for mechanics to perform servicing under equipment."); SOW-0028

**Constraints:**
- Service pit is a below-grade pit; exhaust/combustion gas accumulation is a safety concern (Source: R-01 §3.4)
- Lighting design for the pit is covered by PKG-004 Electrical Design
- Structural pit design is covered by PKG-002 Structural Design (DEL-002-06)

**Notes:** Airflow rates, fan sizing, and supply/exhaust arrangement for the service pit are TBD pending mechanical calculations and applicable confined-space/safety code requirements. **ASSUMPTION:** A mechanical supply-and-exhaust arrangement serving the service pit is required; confirm against Alberta Safety Codes and ASHRAE requirements (location TBD).

> **Terminology note (X-005):** This document adopts "service pit" as the primary term. The RFP source text (R-01 §3.4) uses both "service pit area" and "service trench." For consistency across all four production documents, "service pit" is used; "service trench" is treated as an alias. Source: R-01 §3.4; _SEMANTIC_LENSING.md item X-005.

---

### REQ-004 — General Exhaust Fans

**Statement:** The Exhaust System Plans shall include exhaust fan(s) as shown on the electrical drawing.

**Source:** R-05 App B-Elec ("Install exhaust fan(s) as shown on electrical drawing."); SOW-0066

**Constraints:**
- Exhaust fan locations and quantities to be coordinated with PKG-004 Electrical Design (R-05)
- Fan electrical circuits are outside this deliverable's scope

**Notes:** Specific exhaust fan locations, sizes, and types are TBD pending coordination with the electrical drawing (R-05). The electrical conceptual drawing was not accessible in sufficient detail during this drafting pass; coordination with DEL-004 is required. See Guidance CFT-002 for the coordination gap and proposed resolution.

> **Note (E-003):** Verification of REQ-004 is constrained by the R-05 data gap identified in Guidance CFT-002. Until R-05 App B-Elec is reviewed in sufficient detail, exhaust fan locations and quantities from the electrical drawing cannot be confirmed against the mechanical scope. **PROPOSAL:** Coordination meeting between Mechanical and Electrical Engineers to resolve. Source: Guidance CFT-002; _SEMANTIC_LENSING.md item E-003.

---

### REQ-005 — High-Volume Air Exchanger Interface

**Statement:** The Exhaust System Plans shall coordinate with the high-volume air exchanger to ensure the overall ventilation system is balanced (exhaust and makeup air).

**Source:** R-01 §3.4 ("High volume air exchanger."); SOW-0036; DEL-003-02 HVAC Plans; DEL-003-03 Ductwork & Distribution Plans

**Notes:** The air exchanger itself is documented in DEL-003-02. This deliverable must show how exhaust flows interface with the overall air balance. Specific balanced airflow values are TBD pending calculations (DEL-003-06).

---

### REQ-006 — IFC Drawing Standard

**Statement:** All drawings in this set shall be Issued for Construction (IFC) quality and signed/stamped by a Professional Engineer licensed to practice in the Province of Alberta.

**Source:** R-01 §3.3.2 ("All Issued For Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta."); SOW-0018

---

### REQ-007 — Preliminary Design Approval

**Statement:** A preliminary mechanical design (including exhaust system concept) shall be delivered to and approved by the County before IFC drawings are issued.

**Source:** R-01 §3.3.2 ("Deliver Preliminary Design for the County project team to approve."); SOW-0010c; DEL-003-01 Preliminary Mechanical Design

---

### REQ-008 — Code Compliance

**Statement:** The exhaust system design shall comply with all applicable Alberta Building Codes, Alberta Safety Codes, and regulations in effect at time of permitting.

**Source:** R-01 §3.3.2 ("The building design must adhere to all applicable building codes and regulations."), §3.4 ("The proposed building must adhere to all Alberta Safety Codes."); SOW-0008, SOW-0009

**Notes:** Specific code editions (National Building Code of Canada as adopted by Alberta, Alberta Fire Code, Alberta Safety Codes Act) are **ASSUMPTION: likely applicable** — precise editions and clause numbers are TBD pending permit application and code confirmation with the Authority Having Jurisdiction (AHJ).

> **Note (A-001):** No specific Alberta Building Code edition or Alberta Safety Codes Act edition is identified. All standards in the Standards table carry "ASSUMPTION: likely applicable" with "full text not accessible." **TBD:** Confirm applicable code editions and specific clause references for exhaust system requirements with the AHJ (Camrose County) at time of permitting. Source: Specification Standards table; _SEMANTIC_LENSING.md item A-001. **PROPOSAL:** AHJ (Camrose County) to confirm code editions.

> **Note (A-003):** Verification for REQ-008 currently relies entirely on downstream deliverables (safety code permits DEL-009-03; inspection reports DEL-009-04). There is no verification step within this deliverable's own review cycle. **PROPOSAL:** Include a design-phase code review step in Procedure (see Procedure Step 2.5 addition) to provide an internal pre-IFC code compliance check. Source: Specification Verification table REQ-008 row; _SEMANTIC_LENSING.md item A-003.

---

### REQ-009 — Ceiling Fan Interaction Assessment (NEW)

**Statement:** The exhaust system design shall account for the interaction between the 6 ceiling fans (SOW-0040) and exhaust capture systems, particularly source-capture systems (repair bay exhaust hoses, welding LEV). The design shall confirm that ceiling fan air circulation patterns do not degrade exhaust capture efficiency at the worker breathing zone.

**Source:** R-05 App B-Elec (SOW-0040 — 6 ceiling fans); Datasheet Conditions table (ceiling fans row); _SEMANTIC_LENSING.md item C-002

**Notes:** This is a new requirement added during Pass 3 enrichment. The 6 ceiling fans create air movement in the main shop area. Air circulation patterns may affect exhaust capture efficiency, particularly for the welding LEV system and repair bay hose-reel systems. The assessment may be qualitative (engineering judgment documented in calculations) or quantitative (CFD or other analysis) as determined by the Mechanical Engineer.

**ASSUMPTION:** A qualitative assessment documented in DEL-003-06 is anticipated as sufficient; confirm with Mechanical Engineer.

---

### REQ-010 — Noise and Vibration Considerations (NEW)

**Statement:** The exhaust system design shall consider noise and vibration impacts of exhaust fans and ductwork on occupants in the work area. Where applicable Alberta OHS Code occupational noise exposure requirements apply, the design shall document that exhaust equipment selections do not cause exceedances.

**Source:** _SEMANTIC_LENSING.md item E-004; Alberta OHS Code (location TBD)

**Notes:** This is a new requirement added during Pass 3 enrichment. Exhaust fans and ductwork generate noise and vibration. In a heavy-equipment industrial shop with 35 ft ceilings, background noise levels are typically high, but Alberta OHS Code may impose occupational noise exposure limits that interact with exhaust fan selection. **ASSUMPTION:** A noise/vibration assessment is warranted as a design consideration; the Mechanical Engineer shall assess whether it is a critical design factor for this facility type. Confirm against applicable Alberta OHS Code provisions (location TBD). **PROPOSAL:** Mechanical Engineer to assess whether noise/vibration is a design consideration for this facility type.

---

## Standards

| Standard / Code | Applicability | Access Status |
|---|---|---|
| Alberta Building Code (NBC as adopted by Alberta) | Building ventilation requirements, exhaust systems; edition TBD (A-001) | **ASSUMPTION: likely applicable** — full text not accessible; edition and clause references TBD pending AHJ confirmation |
| Alberta Safety Codes Act and Regulations | All safety code permits; mechanical/HVAC safety; edition TBD (A-001) | **ASSUMPTION: likely applicable** — full text not accessible; edition TBD pending AHJ confirmation |
| ASHRAE 62.1 (Ventilation for Acceptable Indoor Air Quality) | Ventilation rate calculations, exhaust system design | **ASSUMPTION: likely applicable** — full text not accessible; location TBD |
| ASHRAE 55 (Thermal Environmental Conditions) | May inform exhaust/comfort system balance | **ASSUMPTION: possibly applicable** — full text not accessible |
| Alberta Occupational Health and Safety Code | Welding fume exposure limits; confined space (service pit) ventilation; occupational noise exposure (E-004) | **ASSUMPTION: likely applicable** — full text not accessible; location TBD |
| SMACNA (Sheet Metal and Air Conditioning Contractors' National Association) standards | Duct construction and installation | **ASSUMPTION: industry standard practice** — full text not accessible |

> **Note (C-001):** The standards listed above are all marked "ASSUMPTION: likely applicable" with no explanation of which specific provisions apply to which exhaust subsystem. See Guidance for a new applicability rationale note explaining anticipated applicability by subsystem. Source: _SEMANTIC_LENSING.md item C-001. **PROPOSAL:** Mechanical Engineer to document detailed applicability rationale per subsystem.

---

## Verification

| Requirement | Verification Approach | Acceptance Criteria |
|---|---|---|
| REQ-001 — Heavy equipment exhaust shown on drawings | Drawing review: confirm exhaust drop locations and fan specifications shown for each repair bay; cross-reference with DEL-003-06 | Exhaust drop locations shown for each repair bay; fan airflow within TBD% of DEL-003-06 calculated values (F-002) |
| REQ-002 — Welding station exhaust shown on drawings | Drawing review: confirm dedicated exhaust system shown at welding station location per App B | Dedicated LEV or exhaust system shown at welding station; capture velocity per applicable standard (TBD) |
| REQ-003 — Service pit ventilation shown on drawings | Drawing review: confirm pit ventilation supply and exhaust arrangement shown | Supply and exhaust arrangement shown; airflow rate per applicable code (TBD); air changes per hour per DEL-003-06 |
| REQ-004 — General exhaust fans shown and coordinated | Cross-reference with electrical drawing (R-05/DEL-004); confirm fan locations match | Fan locations, types, and quantities match between mechanical and electrical drawings; see E-003/CFT-002 for current gap |
| REQ-005 — Air balance coordination | Review of mechanical calculation package (DEL-003-06); confirm exhaust/supply balance is documented | Total exhaust airflow documented; makeup air balance within TBD% of exhaust (F-002) |
| REQ-006 — IFC stamp | Verify P.Eng. stamp and Alberta licence on each drawing sheet; verify licence validity (X-001) | P.Eng. stamp and Alberta licence number on all sheets; licence confirmed as current (see Procedure Step 6.1) |
| REQ-007 — Preliminary approval | Confirm County sign-off on preliminary design (DEL-003-01) prior to IFC issuance | County approval record on file |
| REQ-008 — Code compliance | Design-phase code review (Procedure Step 2.5); safety code permits obtained (DEL-009-03); inspection reports confirm compliance (DEL-009-04) | Internal code review completed before IFC (A-003); permits and inspections passed |
| REQ-009 — Ceiling fan interaction | Engineering assessment documented in DEL-003-06 or design notes | Assessment confirms ceiling fan air patterns do not degrade exhaust capture below applicable standards (TBD) |
| REQ-010 — Noise and vibration | Noise assessment per applicable Alberta OHS Code; documented in DEL-003-06 or design notes | Assessment confirms exhaust equipment noise within applicable limits, or documents that limits are not exceeded given facility type |

> **Note (F-002):** Quantitative acceptance thresholds have been added as TBD placeholders in the Acceptance Criteria column. The prior version used only qualitative criteria ("drawing review," "cross-reference"). Specific tolerances (e.g., "airflow within +/-10% of calculated values") are TBD pending Mechanical Engineer definition per applicable standards. Source: _SEMANTIC_LENSING.md item F-002.

> **Note (X-004):** Post-installation airflow verification (e.g., air balance testing) is not included in this table because post-installation commissioning may be covered by PKG-013 (see C-003 scope note). If commissioning is confirmed as in scope of another deliverable, a reference to that verification should be added here. Source: _SEMANTIC_LENSING.md item X-004. **PROPOSAL:** Confirm with PKG-013.

---

## Documentation

### Required Artifacts (from _CONTEXT.md Anticipated Artifacts)

| Artifact | Description | Notes |
|---|---|---|
| Exhaust system layout plans | Plan-view drawings showing exhaust duct/hose routing, fan locations, and equipment connections for the full building footprint | Minimum deliverable |
| Vent stack and termination drawings | Drawings showing exterior termination points for exhaust systems, stack heights, and clearance details | Minimum deliverable |
| Exhaust system layouts and configurations | System-level diagrams showing exhaust source connections, fan arrangements, and interface with air exchanger | Minimum deliverable |

> **Note (X-002):** This table represents the minimum deliverable artifact list from _CONTEXT.md Anticipated Artifacts. The Procedure Step 5.1 contains a more detailed anticipated sheet list (6 sheets) that is illustrative -- the actual sheet list is determined by the Mechanical Engineer. The Procedure list expands upon but does not replace this minimum list. Source: _SEMANTIC_LENSING.md item X-002.

### SOW Traceability Matrix (NEW — F-001)

| SOW Item | Description | Mapped Requirement(s) | Coverage Status |
|---|---|---|---|
| SOW-0013 | Complete final mechanical design (exhaust system component) | All REQs (overall scope) | Covered (umbrella SOW) |
| SOW-0028 | Construct ventilated and lighted service pit | REQ-003 | Covered |
| SOW-0036 | Install high-volume air exchanger | REQ-005 | Covered (interface/coordination) |
| SOW-0038 | Install exhaust hoses and fans for heavy equipment in repair bays | REQ-001 | Covered |
| SOW-0039 | Install welding station ventilation/exhaust system | REQ-002 | Covered |
| SOW-0040 | Install 6 ceiling fans in main shop area | REQ-009 | Covered (interaction assessment) |
| SOW-0066 | Install exhaust fan(s) as shown on electrical drawing | REQ-004 | Covered (coordination with electrical) |

> **Note (F-001):** This traceability matrix has been added to confirm all SOW items assigned to DEL-003-04 are addressed by at least one requirement. The prior version did not include this mapping. SOW-0013 is the umbrella mechanical design SOW; SOW-0040 (ceiling fans) was previously untraced and is now linked to the new REQ-009. Source: Decomposition §7 PKG-003; Datasheet Identification; _SEMANTIC_LENSING.md item F-001.

### Supporting Documents (produced in parallel)

| Document | Deliverable ID |
|---|---|
| Mechanical Equipment Schedule (fans, exhaust units) | DEL-003-05 |
| Mechanical Calculation Package (fan sizing, airflow) | DEL-003-06 |
| Mechanical Specification (installation requirements) | DEL-003-07 |
| HVAC Plans (air exchanger, heating) | DEL-003-02 |
| Ductwork & Distribution Plans | DEL-003-03 |
