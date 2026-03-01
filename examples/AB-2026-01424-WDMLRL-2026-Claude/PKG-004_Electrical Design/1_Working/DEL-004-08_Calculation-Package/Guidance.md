# Guidance — DEL-004-08 Electrical Calculation Package

---

## Purpose

DEL-004-08 exists to provide the engineering calculation evidence base that justifies the electrical design of the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. The calculation package is the professional record that demonstrates code compliance, adequate service sizing, and proper circuit design across all electrical systems in the new ~13,000 sq ft maintenance shop.

This deliverable directly supports:
- **OBJ-003**: Produce complete, P.Eng.-stamped IFC design documentation across all disciplines before construction begins. The electrical calculation package is a mandatory component of the IFC documentation set. (Source: Decomposition OBJ-003; RFP §3.3.2)
- **OBJ-005**: Install and commission all electrical and low-voltage systems to operational readiness. The calculation package establishes the sizing basis that the installation package (PKG-015) and commissioning (PKG-020) will rely upon. (Source: Decomposition OBJ-005)

Without this package, the Electrical Engineer cannot produce stamped IFC drawings, and construction cannot legally commence. The package is the professional liability anchor for all electrical design decisions.

---

## Principles

### Terminology: Canonical Building Name (Lensing B-005)
Project documentation uses several names for the building: "West Dried Meat Lake Regional Landfill Maintenance Shop Addition," "New North Shop," and "maintenance shop." For the purposes of this calculation package and all four DEL-004-08 documents, the canonical name is **"West Dried Meat Lake Regional Landfill Maintenance Shop Addition"** (per the RFP title and project name). The informal reference "New North Shop" may be used parenthetically for clarity where it appears in source documents, but should not be used as the primary name.

### Source-Fidelity First
Calculations shall be based on the requirements explicitly stated in RFP §3.4 and Appendix B (Electrical). Where the conceptual drawing provides specific values (fixture counts, circuit ratings, equipment ampacities), those values are the starting point. Where they are absent (e.g., crane ampacity, wash bay fixture wattage), the Electrical Engineer shall obtain or derive the missing data before finalizing calculations — not substitute assumptions into the final stamped package.

### Design-Build Context
The County has a concept, not a complete specification. The RFP states: "The County only has a concept in mind; therefore, it will be a design/build project." (RFP §3.4) This means the Electrical Engineer carries professional responsibility for translating the conceptual electrical layout (Appendix B) into a code-compliant, fully sized design. The calculation package is where that translation is formalized.

### Calculation Package as Living Document
In a design-build project, calculations are typically produced in parallel with drawings. The calculation package should be versioned and cross-referenced to the associated drawing set (DEL-004-02 through DEL-004-07). Revisions to drawings must trigger corresponding revision to calculations.

**Revision Linkage Mechanism (Lensing D-002):** The calculation package should include a cross-reference table (see Procedure Step 8.2) that maps each calculation section to the corresponding drawing number and revision. When a drawing revision changes a design parameter that affects a calculation (e.g., fixture count change, circuit rerouting, load addition), the Electrical Engineer shall:
1. Update the affected calculation section(s),
2. Update the cross-reference table with the new drawing revision,
3. Increment the calculation package revision, and
4. Re-verify affected downstream calculations (e.g., load schedule, service entrance sizing).

The trigger for re-calculation is any drawing change that modifies an input value used in the calculation package. The Electrical Engineer should assess this at each drawing revision cycle.

### Code Compliance is Non-Negotiable
All calculations shall be based on the Canadian Electrical Code (CEC), Part I, in the edition adopted by Alberta at the time of design, and all applicable Alberta Safety Codes. The Safety Code permit is obtained by the Proponent (RFP §3.3.2); the calculation package is the primary technical document supporting that permit application.

---

## Considerations

### Three-Phase Service Sizing
The RFP specifies three-phase power supply (RFP §3.4; SOW-0051). The maintenance shop is a heavy industrial facility with diverse electrical loads including two 5-tonne cranes, multiple 50 A / 240 V welding receptacles, 70 A pump circuits, and a large lighting system. The service entrance calculation is likely to result in a substantial panel size. The Electrical Engineer should consider future expansion capacity when sizing the service entrance, as maintenance shops often add equipment loads over time. **ASSUMPTION: a demand factor analysis will be appropriate given the diversity of load types; the Electrical Engineer shall determine the applicable demand factors per CEC.**

### Crane Power Feeds
Two 5-tonne overhead cranes represent the most demanding specialized loads in the building. Crane circuit sizing per CEC typically requires specific demand factor treatment distinct from general motor loads. The crane manufacturer's electrical data (not available in the RFP sources) is a prerequisite for finalizing these calculations. This data gap should be identified early and resolved before IFC.

### Welding Receptacle Density
The conceptual drawing (App B Electrical) shows a high density of 50 A / 240 V receptacles along the north wall (welding station area) and distributed through the main shop. Simultaneous use of multiple welding outlets at full load would create a significant demand. The Electrical Engineer should apply an appropriate demand factor for welding loads per CEC, or confirm with the County the expected simultaneous welding load. The County will supply welding equipment specifications (RFP §3.4), which should be obtained early in the design process.

### Service Pit Lighting
RFP §3.4 and SOW-0028 require the service pit to be "ventilated and lighted," but neither the RFP nor Appendix B (Electrical) specifies fixture type, illuminance level, or circuit arrangement for the pit. The Electrical Engineer must determine appropriate pit lighting (likely damp/wet location rated fixtures, potentially lower-voltage for safety in a below-grade confined space). This is a design decision that should be documented in the calculation package.

### Hazardous Area Classification — Service Pit (Lensing B-004)
The service pit is used for under-vehicle servicing of heavy maintenance equipment. Depending on the types of vehicles serviced and maintenance activities performed, there is a potential for accumulation of flammable vapors (fuel, solvents, hydraulic fluids) in the below-grade pit space. Under CEC rules, this may require hazardous area classification. The Electrical Engineer shall assess whether the service pit area meets the criteria for a hazardous location classification (CEC — specific section TBD once edition is confirmed). If classification applies, all electrical fixtures, receptacles, and wiring methods within the classified zone must be rated accordingly (e.g., explosion-proof fixtures). This assessment should be performed early in the design process as it affects both fixture selection (REQ-004-08-06) and circuit design for the pit zone. The classification assessment and its outcome shall be documented in the calculation package (REQ-004-08-24).

### Wash Bay Fixture Wattage
Appendix B (Electrical) specifies 150 W LED / 22,000 lm for main shop high bays but does not specify wattage for wash bay high bays (2 rows × 3 = 6 fixtures). The Electrical Engineer should confirm fixture selection. The wash bay is a wet/damp environment; IP-rated fixtures are required. **ASSUMPTION: same 150 W LED type is used unless the Electrical Engineer selects a wet-location rated alternative.**

### Low-Voltage Systems
Security camera wiring and 2-way radio antenna wire (SOW-0064, SOW-0065) are low-voltage systems. Their power supply requirements are typically modest, but the calculation package should document any powered equipment (e.g., POE switches, amplifiers) to confirm service entry into the main load schedule. Detailed design is captured in DEL-004-07 (Low-Voltage System Plans).

### Coordination with Mechanical
The ceiling fans (SOW-0040), exhaust fans (SOW-0066), and forced-air makeup air unit (SOW-0037) all have electrical power requirements that must be coordinated with PKG-003 (Mechanical Design). Fan motor ampacities should be confirmed with the Mechanical Engineer before finalizing the electrical load schedule.

### 40-Year Facility: Alberta Climate
The maintenance shop is in Alberta, subject to significant heating and lighting demands in winter. The electrical design should account for the operational context: a heavily used heavy equipment maintenance facility, likely operating year-round in sub-zero temperatures. This affects heat trace requirements (if any), lighting selection, and potentially the sizing of the forced-air makeup air electrical connection.

**Electrical System Lifecycle Considerations (Lensing D-004):** The 40-year facility horizon has specific implications for the electrical system design that should inform calculation decisions:
- **Conductor longevity:** Thermal cycling in Alberta (extreme cold to heated interior) affects conductor insulation over decades. ASSUMPTION: the Electrical Engineer should consider conductor insulation type selection for long-term thermal cycling performance.
- **Panel board spare capacity:** Over a 40-year lifespan, load additions are likely (new equipment, technology changes). The panel configuration (REQ-004-08-20) should account for spare breaker positions beyond the immediate growth margin.
- **Equipment accessibility for replacement:** Electrical panels, switchgear, and major circuit components will require replacement or upgrade within the 40-year period. The Electrical Engineer should consider accessibility in panel placement and main distribution design.
- **LED fixture lifespan:** While LED fixtures have long rated lives (typically 50,000-100,000 hours), the 40-year horizon may require one or more fixture replacement cycles. The circuit design should accommodate fixture replacement without rewiring.

---

## Trade-offs

| Trade-off | Options | Consideration | Source |
|---|---|---|---|
| Welding receptacle circuit grouping | Individual 50 A circuits vs. shared multi-outlet systems | Individual circuits provide flexibility; shared systems reduce panel space. CEC requirements and County welding load profile should drive the decision. | RFP §3.4; App B (Electrical); D-009 |
| Service entrance sizing margin | Size for current loads vs. size with growth allowance | Adding growth margin increases upfront cost but reduces future upgrade expense. Relevant for a 40-year public facility. **Decision framework (Lensing A-006):** The Electrical Engineer should consult with the Owner to determine the expected growth profile. For a public maintenance facility with a 40-year horizon, a recommended range of 20-25% spare capacity is typical practice (ASSUMPTION — Procedure Step 4.1). Factors to consider: (a) likelihood of additional equipment (welding, diagnostic equipment, EV charging), (b) Owner's capital vs. lifecycle cost preference, (c) whether the service entrance can be practically upgraded later without major disruption. The Electrical Engineer should document the growth margin decision with the Owner's input in the calculation package. | ASSUMPTION; Lensing A-006 |
| Wash bay lighting IP rating | IP65 vs. IP66/IP67 fixtures | Wash bay serves a motor-scraper-sized vehicle; high-pressure wash is likely. Higher IP rating costs more but reduces maintenance. **Decision criteria (Lensing F-003):** The Electrical Engineer should consider: (a) expected wash pressure — if high-pressure wash (>1000 psi) is used, IP66 minimum is recommended; (b) maintenance access — higher IP-rated fixtures typically have sealed housings that are harder to re-lamp but require less frequent maintenance; (c) cost threshold — obtain quotes for IP65 vs. IP66/IP67 in the selected fixture family to quantify the cost difference; (d) Owner maintenance capability — whether the County maintenance team can service higher-IP fixtures. The IP rating decision should be documented in the calculation package with the selected rationale. | App B (Electrical); ASSUMPTION; Lensing F-003 |
| Crane conductor routing | Busway/runway vs. conduit-and-wire | Busway is typically preferred for crane conductor systems; cost and coordination with structural (PKG-002) are factors. | ASSUMPTION |

---

## Examples

No worked examples are available from the accessible sources. The Electrical Engineer shall develop the calculation methodology in accordance with the CEC and accepted Alberta engineering practice.

- For illuminance calculation methodology: ASSUMPTION — IES (Illuminating Engineering Society) methodology or equivalent is commonly used in Alberta. Specific standards TBD by Electrical Engineer.
- For crane circuit sizing: CEC Section 40 (or equivalent current section) governs crane and hoist circuits — location TBD, CEC not accessible in provided sources.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-004-08-01 | Wash bay fixture wattage not specified in App B (Electrical); main shop fixtures are 150 W / 22,000 lm but no equivalent stated for wash bay | App B (Electrical) — main shop notes: "150 Watt LED 22,000 Lumens"; wash bay notes: "2 Rows of 3 High Bay Lights" (no wattage) | N/A — information absent, not conflicting | REQ-004-08-04; Datasheet — Lighting (Wash Bay); load schedule | PROPOSAL: Electrical Engineer to confirm wash bay fixture selection; use 150 W LED as planning assumption pending confirmation | TBD |
| CONF-004-08-02 | Welding receptacle ampacity assumed at 50 A / 240 V per Decomposition D-009, but County has not formally confirmed welding equipment specifications. **Lensing A-002 note:** The 50 A / 240 V rating is treated as a design value across Datasheet, Specification, and load schedule but is simultaneously flagged as an assumption awaiting County data. All documents should be updated upon receipt of County welding equipment specifications. | Decomposition D-009 (ASSUMPTION: 50 A / 240 V) | RFP §3.4 ("County to supply welding equipment specifications") | REQ-004-08-08; Datasheet — Receptacles; load schedule | PROPOSAL: County to provide welding equipment specifications before IFC; if not received, Electrical Engineer to document design assumption and risk in calculation package. Upon receipt, Electrical Engineer to update all documents (Datasheet, Specification, Procedure load schedule). | TBD |
| CONF-004-08-03 | Crane electrical data (ampacity, motor data) not available in RFP sources; circuit sizing cannot be finalized without manufacturer data | App B (Electrical) — "power for crane"; RFP §3.4 — "2-5 tonne overhead cranes" | No crane manufacturer data provided in accessible sources | REQ-004-08-09; load schedule; service entrance sizing; Datasheet — Crane Electrical Data table | PROPOSAL: Crane procurement (PKG-016) or early specification should be coordinated with Electrical Design; crane data must be obtained before IFC calculations are finalized | TBD |
| CONF-004-08-04 | Heating system and forced-air makeup air unit appear in Procedure Step 3.1 connected load schedule but had no corresponding Specification requirement (gap resolved by adding REQ-004-08-22). Electrical Engineer to confirm with Mechanical Engineer (PKG-003) that heating/MUA circuits are within the scope of this calculation package. (Lensing E-002, C-003) | Procedure.md — Step 3.1 (lists heating and MUA loads) | Specification.md — Requirements (formerly absent; now REQ-004-08-22 added) | REQ-004-08-22; Procedure Step 3.1; load schedule | PROPOSAL: Electrical Engineer to confirm heating/MUA scope with Mechanical Engineer and update REQ-004-08-22 accordingly | TBD |
| CONF-004-08-05 | Voltage drop limits: Procedure Step 7.1 states "typically 3% on feeders, 5% total" but qualifies this with "specific limits per current CEC edition, location TBD." Specification REQ-004-08-15 says "compliance with applicable code limits" without stating specific limits. The typical values may differ from the actual CEC edition requirements. (Lensing F-002) | Procedure.md — Step 7.1 ("typically 3% on feeders, 5% total") | Specification.md — REQ-004-08-15 ("compliance with applicable code limits") | REQ-004-08-15; Procedure Step 7.1; all voltage drop calculations | PROPOSAL: Once CEC edition is confirmed, update both documents with the actual code-specified voltage drop limits to ensure consistency | TBD |
