# Guidance: DEL-02-07 Emergency Power & Backup Generator

## Purpose

This deliverable exists to demonstrate that the Penhold Public Services Building (PSB) will maintain essential operational capability during a utility power interruption. The combined Fire Hall and Public Works facility serves as an emergency operations base (including the Incident Command Post in the meeting room). The Owner explicitly required a backup generator to ensure the kitchen, ICP meeting room, and bathrooms remain functional, and that fire apparatus bay doors can still be opened when the building is on generator power.

The deliverable therefore provides the design basis — not just a spec-sheet — that ties generator capacity to identified operational needs, confirms fuel autonomy, and resolves the critical interface between door operators and emergency power.

Sources: Addendum 03 §1.15; SOW-0222; OBJ-002 (Fire Department operational functionality); OBJ-008 (controlled Design-Build delivery).

---

## Principles

### P1: Operations-First Load Selection
The essential loads list must be grounded in what the facility actually needs to remain operational during an emergency, not just what is code-minimum. The Owner's explicit loads (kitchen, ICP room, two bathrooms) represent a functional floor, not a ceiling. The Design-Builder should evaluate whether additional loads — such as communications, fire alarm, SCBA room, PA system, and emergency lighting — are required by code or necessary for the Fire Hall's emergency operations role, and include them in the essential loads list.

Source: Addendum 03 §1.15; OBJ-002; OSR §10.3.4 (practical, easy-to-maintain systems).

### P2: Generator Sizing Discipline
Generator sizing should be based on the actual essential loads list, with appropriate demand factors applied. Oversizing adds unnecessary capital cost; undersizing risks operational failure at the worst possible time. The sizing basis document should show the calculation clearly enough that a reviewing engineer can verify it without additional information.

Source: ASSUMPTION — standard electrical engineering practice for standby power sizing.

### P3: Fuel Autonomy as a Planning Constraint
The 72-hour runtime target (from Functional Program Appendix B, location TBD) establishes the fuel tank sizing constraint. Until the Owner confirms this runtime, 72 hours should be used as the design basis. The Design-Builder should proactively raise this for Owner confirmation early in the proposal process, as it has a direct impact on tank size, footprint, and cost.

Source: SOW-0222 open issue; _CONTEXT.md Open Issues; _REFERENCES.md Notes.

### P4: Bay Door Secondary Opening Mechanism — Resolve the Method Early
Addendum 03 §1.15 allows two approaches: generator-powered door operators OR manual override. This is a design decision with implications for both the electrical distribution design (if powered) and the door specification (if manual). The Design-Builder should select one approach and document it in the proposal. Leaving this ambiguous into detailed design creates risk for both coordination and cost.

Source: Addendum 03 §1.15; SOW-0216.

### P5: Integration with DEL-02-06 Electrical Distribution
The emergency power system is not a standalone design. The ATS, essential loads panel, and any generator-powered door circuits must be coherently integrated with the general electrical distribution described in DEL-02-06. These two deliverables should be developed concurrently by the same electrical lead to avoid interface gaps.

Source: OSR §10.4; ASSUMPTION (standard electrical coordination practice).

---

## Considerations

### Generator Location and Service Access
The Functional Program indicates the generator occupies an outdoor area (Appendix B row 30.0, location TBD). The outdoor placement must consider:
- Exhaust dispersion away from air intakes, occupied areas, and apparatus bay doors
- Refuelling access (tanker truck access to fill diesel tank)
- Maintenance clearances per manufacturer and code
- Freeze protection for the generator set in Alberta winter conditions (block heater, battery heater, enclosure — ASSUMPTION: standard practice for Alberta climate).

**Cold-start reliability [F-003]:** Penhold, Alberta experiences winter temperatures of -30C or colder. The Design-Builder shall confirm with the generator manufacturer that the selected unit can reliably cold-start under worst-case design ambient temperature conditions, and that block heater and battery heater provisions are adequate. The design ambient temperature for Penhold (currently TBD in Datasheet Conditions) shall be established and documented. Generator derating curves for altitude and temperature shall be obtained and applied during detailed design (Procedure Step B1).

**Noise and vibration impact on facility operations [C-004]:** An outdoor diesel generator near an occupied facility creates potential noise and vibration concerns. The Design-Builder should:
- Evaluate generator noise levels (from manufacturer specification) against applicable municipal noise bylaws for Penhold (location TBD [C-004])
- Consider the impact on personnel in adjacent areas (apparatus bays, outdoor spaces)
- Propose noise abatement measures if needed (enclosure features, siting setbacks, vibration isolation)
- Document the noise assessment in the proposal or design basis

**ASSUMPTION:** Municipal noise bylaws may apply; manufacturer noise data required for assessment.

- Security and vandal resistance

**ASSUMPTION:** The generator will require a weatherproof enclosure or housing suitable for Penhold, Alberta climate conditions.

### 72-Hour Runtime — Open Issue
The Functional Program notes a 72-hour runtime; this has been flagged as an open issue requiring Owner confirmation. 72 hours is a demanding fuel autonomy requirement that will significantly affect tank volume and potentially require a sub-base or remote fuel tank. The Design-Builder should note this assumption in the proposal and explicitly invite Owner confirmation.

Source: SOW-0222 open issue; _CONTEXT.md Open Issues.

### Post-Disaster Importance Category
OSR §10.3.5 notes that the AHJ intends to exempt the PSB from post-disaster importance category, as it will not be the sole emergency management structure in Penhold. This affects the applicable seismic and structural provisions for the building generally, but the Design-Builder should confirm whether this exemption also affects generator system requirements under the ABC (some generator requirements are triggered by post-disaster classification).

Source: OSR §10.3.5.

### Coordination with Emergency Lighting
OSR §10.5 requires emergency exit lights with internal battery backup above personal doors. These battery-backup exit lights are separate from the generator system and must be provided regardless of whether the generator is running. The essential loads list should not conflate generator-backed lighting with battery-backed exit lighting.

Source: OSR §10.5.

### Diesel Fuel Storage Regulatory Compliance
Diesel fuel storage above certain thresholds triggers Alberta Fire Code and potentially environmental protection requirements. If a 72-hour runtime requires a large tank, the Design-Builder should confirm applicable thresholds and include the necessary secondary containment, venting, and labelling in the design.

Source: ASSUMPTION — standard regulatory practice; Alberta Fire Code location TBD.

---

## Trade-offs

### Trade-off 1: Generator-Powered Bay Door Secondary Opening Mechanism vs. Manual Override
**Tension:** Powering door operators from the essential loads panel is seamless operationally (doors work exactly as normal during a power outage) but adds load to the generator and complexity to the distribution design. Manual override is simpler and lower-cost but requires firefighters or staff to operate doors manually under emergency conditions — potentially in full gear and under time pressure.

**Design-Builder's decision:** Both options are acceptable per Addendum 03 §1.15. The proposal should state which option is selected and briefly justify it. For a Fire Hall, the generator-powered approach may be preferred to eliminate manual door operation risk during emergency response.

**ASSUMPTION:** Generator-powered door operators will be the preferred approach, but the Design-Builder retains the right to propose manual override with appropriate justification.

Source: Addendum 03 §1.15.

### Trade-off 2: Essential Loads List Scope (Minimum vs. Full Emergency Operations)
**Tension:** The Owner specified a minimum essential loads list (kitchen, ICP room, two bathrooms). A broader essential loads list (adding fire alarm, HVAC for ICP room, communications, SCBA room) increases generator kW rating and capital cost but better supports the building's emergency operations purpose.

**Resolution:** Code-required life-safety loads (fire alarm, emergency lighting, communication systems if code-required) must be included regardless of cost. Beyond code minimums, the Design-Builder should include loads necessary for Fire Department emergency operations and document the rationale. An independent review step (Procedure Step A3a) shall confirm completeness of the essential loads list before generator sizing proceeds.

**Adequacy evaluation criteria [A-005]:** The essential loads list scope shall be evaluated against:
- (a) **Code compliance:** All code-required minimum loads per ABC/NBCC life-safety provisions are included
- (b) **Operational mission:** Can the Fire Department sustain emergency operations (OBJ-002) using only the listed loads? Are critical communications, fire alarm, and SCBA room operations supported?
- (c) **Owner risk tolerance:** Is the Owner aware of and accepting of the essential loads scope? What functionality will be unavailable during outage?

The Specification (REQ-02 adequacy criteria) shall be verified against these criteria once the complete essential loads list is developed and peer-reviewed.

**ASSUMPTION:** No explicit acceptance criteria for essential loads scope adequacy exist in accessible sources; the above is proposed as a framework for human ruling.

Source: Addendum 03 §1.15; OBJ-002; ASSUMPTION (code compliance principle); Procedure Step A3a (independent review).

### Trade-off 3: Tank Size vs. Refuelling Plan
**Tension:** A larger fuel tank (to achieve 72-hour autonomy without refuelling) has higher capital cost, larger footprint, and potentially higher regulatory burden. A smaller tank with a documented refuelling agreement (e.g., supplier on call) may be an acceptable alternative if the Owner concurs.

**Resolution:** Until the Owner confirms the 72-hour runtime requirement and whether a refuelling plan is acceptable as an alternative, use 72 hours as the design basis. Raise the question in the proposal (Procedure Step A1).

**Refuelling plan acceptability criteria [D-003]:** If the Owner considers a refuelling plan as an alternative to full 72-hour tank autonomy, the following criteria should be used to evaluate acceptability:
- (a) **Fuel supplier agreement:** Documented agreement with fuel supplier specifying guaranteed emergency response time and refuelling protocol
- (b) **Response time compatibility:** Response time must be compatible with remaining fuel at the refuelling trigger level. Example: if tank holds 48 hours and trigger is set at 50% capacity, the supplier must be able to deliver within 24 hours
- (c) **Access impedance scenarios:** Consideration of scenarios where road access may be impaired during emergency (severe weather, flooding, debris); contingency plan if primary supplier cannot access site
- (d) **Operational acceptance:** Fire Department operations input on acceptable risk level; does the Fire Department agree that a refuelling-dependent plan is acceptable?
- (e) **Hot-refuelling capability:** Confirmation that safe refuelling procedure exists while generator is running, or documented shutdown protocol

**ASSUMPTION:** No explicit criteria for refuelling plan acceptability exist in accessible sources; the above is proposed for Owner/fire department ruling.

**Emergency refuelling logistics [E-002]:** During an extended utility power outage where the generator is running, fuel resupply logistics must be established (Procedure Step D3a). The Owner's operational plan shall address: contact information for fuel supplier with emergency capability, maximum acceptable delivery response time, contingency if road access is impaired, and safe refuelling procedure.

Source: SOW-0222 open issue; ASSUMPTION; Procedure Step D3a.

---

## Examples

No worked examples are available from accessible sources. The following describes the expected form of artifacts:

- **Essential loads list example format:** Table with columns: Load Description | Area/Circuit | Connected Load (kW) | Demand Factor | Design Load (kW). Totals row yields the generator sizing input. Should include all minimum loads (kitchen, ICP room, bathrooms), code-required loads (fire alarm, emergency lighting, communications), and any operationally required loads with documented rationale.

- **Generator sizing basis example:** Reference to CSA C282 or NFPA 110 sizing methodology. Apply demand factors per standard (to be confirmed from CSA C282 text). Apply spare capacity factor to design load total. **[A-002] Spare capacity factor status:** Currently assumed at 25% per Procedure Step A4. **This is an ASSUMPTION only.** No accessible normative source confirms this value. The responsible electrical engineer shall confirm the appropriate spare capacity factor (commonly 25% but may vary) from CSA C282 or applicable standard before finalizing generator sizing. This directly affects generator kW selection and must be documented in the generator sizing basis.

- **ATS design example:** Reference to single-line electrical diagram showing utility feed, ATS (with location confirmed coordinated with electrical room), main panel, and essential loads sub-panel. Diagram shall show all essential loads on the generator-fed side and show transfer logic/sequencing.

- **Noise assessment example (if applicable) [C-004]:** Generator noise rating from manufacturer (dB at rated output and at standard distance, e.g., 1 meter). Comparison to Penhold municipal noise bylaws (threshold distance and time-of-day limits TBD). Proposed noise abatement (enclosure insulation, setback distance, operating restrictions) if needed to meet bylaws.

---

## Additional Considerations (from Semantic Lensing Enrichment)

### Generator Lifecycle Cost and Warranty [F-004]
No document currently addresses generator warranty period, expected service life, or lifecycle cost considerations. For a facility with a 50-year building design life (RFP section 2.2), the generator replacement cycle and warranty terms should be evaluated. **ASSUMPTION:** Diesel standby generators typically have a service life of 20-30 years with proper maintenance, implying at least one replacement cycle during the building's design life. The Design-Builder should address: (a) minimum warranty period for the generator unit, (b) expected service life and replacement horizon, (c) lifecycle cost implications for generator and fuel system maintenance. **Source:** RFP section 2.2 (50-year design life); ASSUMPTION for generator service life range.

### Single-Generator vs. Redundant-Generator Philosophy [E-003]
The current design basis assumes a single diesel standby generator. No document discusses whether redundancy (e.g., N+1 configuration or parallel generators) should be evaluated for an emergency operations facility. **ASSUMPTION:** A single generator is the appropriate design basis for this facility given: (a) the AHJ intends to exempt the PSB from post-disaster importance category (OSR section 10.3.5), meaning the facility is not the sole emergency management structure in Penhold; (b) no accessible source requires generator redundancy for this facility type. However, the Owner should be informed of this assumption and given the opportunity to confirm that single-unit reliability (supplemented by routine testing and maintenance per Procedure Phase D) is acceptable. **Source:** OSR section 10.3.5; OBJ-002; ASSUMPTION.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-01 | 72-hour generator runtime: noted in Functional Program but not confirmed by Owner in Addendum 03 or other accessible sources | SOW-0222 open issue note; _CONTEXT.md Open Issues | Functional Program Appendix B row 30.0 (location TBD — text partially obscured) | REQ-04; Trade-off 3; generator sizing and fuel tank volume | Functional Program Appendix B pending Owner confirmation | TBD |
| CONF-02 | Door secondary opening method not specified: Addendum 03 §1.15 permits either generator-powered or manual override, but the choice has implications for essential loads list, generator sizing, and door specification | Addendum 03 §1.15 (either/or) | SOW-0216 (secondary mechanism required, method unspecified) | REQ-03; Trade-off 1; essential loads list; door schedule in DEL-02-04 | Design-Builder to select and document in proposal; Owner to confirm acceptability | TBD |
| CONF-03 | Single-generator vs. redundant-generator philosophy: current design assumes single diesel standby generator; no discussion of whether N+1 or parallel redundancy should be evaluated for an emergency operations facility | OSR §10.3.5 (post-disaster exemption implies single unit acceptable) | OBJ-002 (emergency operations capability); ASSUMPTION (no accessible source requires redundancy) | Guidance purpose statement; Specification REQ-01; Datasheet Generator Unit attributes | Owner risk tolerance / Post-disaster importance category exemption (OSR §10.3.5) | TBD |
