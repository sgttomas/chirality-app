# Guidance — DEL-004-01 Preliminary Electrical Design

---

## Purpose

DEL-004-01 exists to produce a preliminary electrical design presentation that the County project team can review and approve before the Electrical Engineer proceeds to final design. This gate is contractually established in RFP §3.3.2 and decomposed as SOW-0010d.

The preliminary design serves two functions:

1. **Owner alignment:** Confirms that the Proponent's electrical design intent matches the County's expectations (as expressed in RFP §3.4 and App B (Electrical)) before significant engineering investment in final drawings.
2. **Interdisciplinary coordination input:** The preliminary electrical layout informs the structural engineer (crane support locations, conduit sleeves through slabs), the mechanical engineer (exhaust fan power, makeup air unit power), and the architect (panel locations, ceiling penetrations) early enough to avoid costly late-stage changes.

The preliminary design is a scaffold — it does not need to be fully engineered at this stage, but it must be complete enough for an informed County review.

---

## Principles

### Source fidelity to App B (Electrical) conceptual drawing

The conceptual electrical drawing (App B — Electrical) establishes the Owner's intent for fixture counts, receptacle types, and key equipment circuits. The preliminary design should be consistent with this drawing and should deviate from it only with explicit justification (e.g., code requirements, coordination conflicts). Any deviations should be flagged for County awareness.

Source: App B (Electrical); RFP §2.1 ("appendices and any subsequent addenda are incorporated into, and form part of this RFP").

### Three-phase power is a firm design constraint

The RFP explicitly states "The proposed building shall run on three-phase power." This is not a recommendation. All circuit planning — crane feeds, welding receptacles, large equipment circuits — must be designed against a three-phase distribution system.

Source: RFP §3.4.

### Welding-grade receptacle density matters operationally

The RFP states "multiple electrical plugs throughout the shop area suitable for connecting high voltage welding equipment." The conceptual drawing (App B — Electrical) shows 50A/240V receptacles distributed throughout the main shop area. The distribution pattern matters: inadequate density forces long extension cord runs in a heavy equipment maintenance environment, which is both a safety and operational concern.

Source: RFP §3.4; App B (Electrical).

### The service pit lighting and ventilation requirement is safety-critical

RFP §3.4 requires the service pit to be "ventilated and lighted." In an industrial maintenance environment, lighting in the service pit is an occupational health and safety requirement, not simply a convenience. The electrical design must address this space explicitly. Fixture selection should account for the confined, potentially contaminated environment.

**ASSUMPTION (C-002):** The Alberta OHS Act/Regulation may impose additional requirements on the service pit as a confined or restricted space (lighting levels, ventilation rates, emergency provisions). The Electrical Engineer should confirm whether OHS confined-space provisions apply and whether they impose electrical design requirements beyond general code compliance. See also Specification Standards table.

Source: RFP §3.4; SOW-0028.

### Low-voltage systems require early conduit coordination

Security camera wiring and 2-way radio antenna wiring (App B — Electrical; SOW-0064, SOW-0065) require conduit infrastructure that must be roughed in during construction. If conduit routes are not coordinated at the preliminary design stage, they may be obstructed by structure, mechanical equipment, or other trades. The preliminary design should identify routing intent for low-voltage systems.

Source: App B (Electrical).

---

## Considerations

### Panel location and sizing

App B (Electrical) does not explicitly show a main distribution panel location. The panel location should be selected to:

- Minimize feeder runs to the major loads (cranes, large equipment circuits in the main shop).
- Be accessible for maintenance without obstructing the work bays.
- Be coordinated with the utility/mechanical room layout (per App B (Shop) and architectural design).
- ASSUMPTION: The utility room is a candidate panel location given its function in the building program; this should be confirmed with the Architect at preliminary design stage.

Panel sizing (service ampacity) is TBD pending load calculation (a final design deliverable — DEL-004-08), but the preliminary design should flag that the combined loads of two 5-tonne cranes, the 70A fire hose pump, 70A pressure washer, 40A compressor, welding receptacles, and general loads will require a substantial three-phase service. Preliminary planning should allow for a large service (TBD by Electrical Engineer).

### Crane power feed design considerations

Two 5-tonne overhead cranes on trolleys (SOW-0067; RFP §3.4) are major electrical loads. Crane power feeds in an industrial facility typically involve:

- Dedicated crane circuit(s) from the panel.
- Runway-mounted conductor bar or festoon cable systems.
- The structural engineer's crane support design (DEL-002-07) must be coordinated with the electrical feed routing.

Crane motor specifications are not provided in the RFP. The Electrical Engineer must obtain crane equipment specifications to size the crane circuits. This is a known design dependency.

Source: App B (Electrical); RFP §3.4.

### Separation of high-voltage and low-voltage systems

The combination of 50A welding receptacles, crane feeds, and low-voltage security/radio systems in one building creates an EMI and separation consideration. ASSUMPTION: The Canadian Electrical Code (likely applicable in Alberta, location TBD) imposes separation requirements between power and low-voltage conductors. The preliminary design should identify routing strategies that respect these separation requirements.

### Electrical service tie-in coordination

RFP §3.3.2 requires the Proponent to "coordinate and execute electrical service tie-in" (SOW-0081). The preliminary electrical design should identify:

- The anticipated service voltage and configuration from the utility.
- The proposed service entry point to the building.
- Whether a utility transformer is required on site (TBD — dependent on existing utility infrastructure at the landfill site).

The existing landfill site's electrical infrastructure is not described in the RFP. This is a design information gap that should be resolved during preliminary design (e.g., through site investigation and utility consultation).

**Existing site electrical infrastructure (B-004):** The following information should be obtained to support service tie-in design:
- What is the existing electrical service at the landfill site (voltage, capacity, provider)?
- Which utility provider serves the location?
- What is the process and timeline for obtaining service information and coordinating a new or upgraded service connection?
This information is not available in the RFP or App B (Electrical). The project team should initiate utility provider contact early in the preliminary design phase. See also Procedure Step 2.1.

### Coordination with mechanical for exhaust fans and ceiling fans

App B (Electrical) shows exhaust fans and ceiling fans requiring electrical power feeds. The mechanical engineer (PKG-003) will determine exhaust fan sizing and locations (exhaust hoses and fans per RFP §3.4; SOW-0038, SOW-0039). The electrical preliminary design should:

- Reserve circuit capacity for mechanical exhaust fans consistent with mechanical preliminary design (DEL-003-01).
- Coordinate ceiling fan power point locations with the structural and architectural reflected ceiling plan.

### Fire code implications for fire hose pump circuit (C-002)

The 70A fire hose pump circuit (SOW-0062; App B Electrical) may be subject to fire code provisions that impose specific wiring methods (e.g., fire-rated cable, dedicated raceway, circuit integrity requirements). **ASSUMPTION:** Fire code applicability to the fire hose pump wiring method has not been confirmed. The Electrical Engineer should verify whether Alberta fire code or National Fire Code of Canada provisions apply to this circuit and whether they impose requirements beyond standard CEC wiring methods. See also Specification Standards table.

### Lighting photometric sufficiency

The main shop high-bay lighting quantity and specification (5 × 4 = 20 fixtures at 150W / 22,000 lumens each) is prescribed by the Owner's conceptual drawing. However, the Electrical Engineer should confirm at preliminary design stage whether this quantity and arrangement achieves adequate illumination levels for a heavy equipment maintenance shop, considering the 35' ceiling height and the building's 130' × 100' footprint. If a photometric deficiency is identified, this should be reported to the County as part of the preliminary design submission.

Source: App B (Electrical); RFP §3.4.

### Preliminary-level adequacy definition (F-004)

The documents for DEL-004-01 repeatedly distinguish "preliminary" from "final" design but do not define the boundary between them. The following criteria are proposed as a working definition of "preliminary-level" adequacy for this electrical design presentation:

- **What is expected at preliminary level:** System approach and intent (three-phase distribution, panel location rationale, lighting approach), equipment circuit identification (loads listed with known or TBD ampacities), layout showing approximate locations of all fixtures, receptacles, and equipment connections, design narrative explaining approach and outstanding items.
- **What is deferred to final design:** Exact circuit routing, wire sizing calculations (DEL-004-08), panel schedule detail (DEL-004-06), conduit routing, P.Eng.-stamped IFC drawings (DEL-004-02 through DEL-004-09), photometric calculations, full code compliance verification.
- **How the County should evaluate the submission:** TBD — the County's evaluation criteria for the preliminary design have not been defined in the RFP. The Electrical Engineer should confirm with the County project team what level of detail they expect to see before approving advancement to final design. (See also R-016 acceptance criteria in Specification.)

**ASSUMPTION:** This boundary is inferred from the nature of a preliminary design presentation and the RFP's requirement structure. The actual boundary should be confirmed with the County.

### Owner alignment and County feedback mechanism (D-003, E-001)

The Guidance Purpose states that the preliminary design confirms "the Proponent's electrical design intent matches the County's expectations." The mechanism for this confirmation is not defined in the RFP. The following aspects should be clarified:

- **Communication approach:** Is the preliminary design submitted as a standalone document package, presented in a face-to-face meeting, or both? Is a cover letter or executive summary expected? (E-001)
- **Feedback mechanism:** What format does County feedback take (written comments, marked-up drawings, meeting minutes)? What is the expected review period?
- **Approval format:** Is County approval a formal written sign-off, verbal confirmation, or conditional approval with comments? What happens if the County requests changes — does the preliminary design iterate, or does the Electrical Engineer proceed to final design incorporating comments? (D-003)

**ASSUMPTION:** These questions are not answered in the RFP. The project team should establish the County communication and approval protocol before or concurrent with the preliminary design submission. See also Procedure Steps 7.2 and 7.3.

---

## Trade-offs

| Trade-off | Option A | Option B | Notes |
|---|---|---|---|
| Panel location | Utility room (central) | Near service entry at building perimeter | Utility room minimizes interdisciplinary conflicts; perimeter minimizes service feeder cost. TBD by Electrical Engineer. |
| Crane conductor system | Runway conductor bar | Festoon cable system | Conductor bar is lower maintenance for permanent installation; festoon is simpler to install. Choice depends on crane specification and trolley configuration. TBD. |
| Service entry metering | Single meter for whole building | Sub-metering for specific large loads | Single meter simplest; sub-metering allows Owner to track crane/wash bay energy use. ASSUMPTION: single-meter approach unless Owner specifies otherwise. |
| Service pit lighting fixture type | Standard industrial strip fixture | Vapour-proof fixture rated for confined space | Safety and code considerations favour vapour-proof fixtures for service pit environment. ASSUMPTION: vapour-proof or equivalent rating required; to be confirmed by Electrical Engineer with safety code review. |

---

## Examples

TBD — No comparable project examples are available in the accessible source material.

---

## Conflict Table (for human ruling)

No unresolvable conflicts have been identified between available source documents (RFP and App B — Electrical) at this stage. The following potential conflicts or ambiguities are noted for awareness:

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CF-004-001 | Welding receptacle ampacity: RFP §3.4 describes "high voltage welding equipment" without specifying ampacity. App B (Electrical) shows 50A/240V symbols in shop area. D-009 in Decomposition records assumption of 50A/240V. | RFP §3.4 | App B (Electrical); Decomposition D-009 | Specification R-006; Datasheet Receptacle table | PROPOSAL: Accept 50A/240V per App B (Electrical) and D-009 assumption unless County provides welding equipment specifications requiring a different ampacity. | TBD |
| CF-004-002 | Wash bay high-bay light specification: App B notes "2 Rows of 3 High Bay Lights" for wash bay, but does not state wattage or lumen output (unlike main shop which states 150W/22,000 lumens). | App B (Electrical) — Main Shop notes (explicit) | App B (Electrical) — Wash Bay (count only) | Specification R-003; Datasheet Lighting table | PROPOSAL: Electrical Engineer to select equivalent high-bay LED for wash bay consistent with 150W/22,000 lumen class used in main shop, unless Owner specifies otherwise. | TBD |
