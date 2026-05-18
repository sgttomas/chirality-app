# Guidance — DEL-003-02 HVAC Layout Plans

---

## Purpose

DEL-003-02 (HVAC Layout Plans) exists to graphically document the spatial arrangement of all heating, ventilation, and air exchange systems in the WDMLRL Maintenance Shop Addition, so that:

1. The mechanical design intent is communicated to the construction team for installation.
2. The Owner (Camrose County) can review system layouts for compliance with their operational program.
3. Coordination between mechanical, structural, electrical, and plumbing disciplines can be verified on a common drawing base.
4. Regulatory inspectors can confirm code-compliance at the IFC stage.

The HVAC layout is the primary instrument through which the Mechanical Engineer discharges SOW-0013 (complete final mechanical design). It is a contractual deliverable under CCDC 14-2013 and must be IFC-quality with a P.Eng. stamp before construction begins.

**Layout quality evaluation [A-005]:** Beyond system completeness, a high-quality HVAC layout should be evaluated against: (a) constructability — can the installing contractor interpret and build from the drawings without ambiguity; (b) maintainability — are equipment access clearances and service routes shown and adequate; (c) clarity of drawing communication — are scales appropriate, labels legible, and cross-references consistent with the Equipment Schedule (DEL-003-05). These quality dimensions serve the Owner's operational needs and the constructor's installation needs. TBD: Mechanical Engineer to confirm quality evaluation criteria appropriate for this project.

**Source:** R-01 §3.3.2 (IFC requirement); Decomposition OBJ-001, OBJ-003, OBJ-004.

---

## Principles

### P-1: Industrial-Grade Systems for Heavy-Equipment Environment

The building is a maintenance shop for heavy landfill equipment (motor scrapers, tracked equipment, packers). The HVAC systems must be selected and laid out for industrial, not commercial, service:

- High contaminant loads (diesel exhaust, hydraulic fluid vapors, welding fumes, vehicle off-gassing).
- High air-change rates required to maintain safe working conditions.
- Equipment must be robust, accessible for maintenance, and compatible with the industrial structural environment (35 ft concrete ceiling, heavy overhead crane loads).

**Source:** R-01 §3.1, §3.4.

### P-2: The High-Recovery Heating System Is the Thermal Anchor

The RFP explicitly specifies a "high recovery heating system" (R-01 §3.4). This language is consistent with heat-recovery unit heaters or indirect-fired radiant/convective systems with heat recovery — common in Alberta industrial shop applications. The layout must:

- Position heating units to achieve complete shop coverage including near overhead doors where cold air infiltration is highest.
- Anticipate the 35 ft ceiling height: stratification management (via ceiling fans — SOW-0040) is a companion design consideration.

**Source:** R-01 §3.4 (SOW-0035); R-04 App B (SOW-0040).

### P-3: Makeup Air Is Non-Negotiable for Exhaust-Heavy Operations

The forced-air makeup air (MUA) unit (SOW-0037) is required because exhaust fans (equipment exhaust, welding exhaust) will continuously remove large air volumes. Without a tempered MUA system:

- The building will depressurize, causing cold infiltration through door gaps and compromising heating efficiency.
- Backdrafting of combustion appliances may occur.
- Overhead door operation will be impaired by negative pressure.

The MUA unit must be sized to replace at minimum the exhaust volume of all simultaneously operating exhaust systems. ASSUMPTION: MUA sizing to be confirmed in DEL-003-06 (Mechanical Calculation Package).

**Source:** R-04 App B (SOW-0037); ASSUMPTION based on standard HVAC engineering principles.

### P-4: Source Capture Is the Preferred Strategy for Welding and Equipment Exhaust

For both the welding station exhaust (SOW-0039) and the equipment exhaust hose system (SOW-0038), source capture (exhaust at or near the point of generation) is strongly preferred over dilution ventilation:

- Source capture is more effective at lower airflow rates, reducing heating load on the MUA system.
- It is required by applicable safety codes for welding fumes (ASSUMPTION: Alberta Safety Codes align with CSA W117.2 welding safety — location TBD).
- For equipment exhaust, flexible hose drops attached to vehicle tailpipes are the standard approach for repair bay environments.

**Source:** R-01 §3.4 (SOW-0038, SOW-0039); ASSUMPTION per industry standard practice.

### P-5: The Service Pit Requires Special Attention

The below-grade service pit/trench (SOW-0028) is a confined-space-adjacent environment where heavier-than-air combustion gases (diesel exhaust, propane, CO) can accumulate. The HVAC layout must address:

- Forced supply and/or exhaust ventilation within the pit volume (not relying solely on general shop ventilation).
- Provision may need to meet Alberta confined space ventilation requirements (ASSUMPTION: applicable code — location TBD).

**Source:** R-01 §3.4 (SOW-0028); ASSUMPTION per safety code requirements.

### P-6: Ceiling Fans Serve Air Destratification, Not Cooling

The 6 ceiling fans in the main shop (SOW-0040) serve a destratification function in a building with a 35 ft ceiling. In Alberta winters, heated air rises and pools near the ceiling while workers at floor level are cold. The fans:

- Recirculate warm ceiling air back down to the working level.
- Reduce the heating demand by achieving more uniform temperature distribution.
- Should be positioned to provide coverage across the main shop floor area without creating excessive draughts.

Note: Ceiling fans are electrically powered (PKG-004 scope); their locations are shown on HVAC layout for coordination.

**Source:** R-04 App B-Elec (SOW-0040); ASSUMPTION per destratification engineering rationale.

---

## Considerations

### C-1: Coordination with Structural for Mechanical Penetrations and Hangers

The concrete structure (35 ft ceiling) requires all ductwork hangers, equipment supports, and roof/wall penetrations to be coordinated with PKG-002 (Structural Design) before IFC. The Mechanical Engineer should:

- Flag all roof penetration locations on the HVAC layout for structural review.
- Confirm that equipment weight does not conflict with crane clearance envelopes (two 5-tonne overhead cranes operating in the main shop — R-04 App B).
- Ensure ductwork routing does not obstruct crane travel paths.

**Source:** R-01 §3.4 (SOW-0067); R-04 App B.

### C-2: Overhead Door Infiltration Loads

The main shop has two 24 ft wide drive-through repair bay doors plus the wash bay door (24 ft wide). Frequent opening of these doors during Alberta winters creates significant infiltration loads. The heating and MUA systems must be sized accordingly. The HVAC layout should show any air curtains or vestibule heating provisions at major door locations (if included in design — TBD by Mechanical Engineer).

**Source:** R-01 §3.1, §3.4; R-04 App B.

### C-3: Wash Bay Humidity and Wash-Down Compatibility

The wash bay (SOW-0027a) is used for washing large equipment. The HVAC equipment in or serving the wash bay must be:

- Rated for humid/wash-down environments.
- Protected from direct water contact during washing operations.
- Capable of exhausting the elevated humidity generated during wash operations.

**Source:** R-01 §3.1, §3.4; R-04 App B.

### C-4: Ancillary Space Conditioning

The office, parts room, and utility room require heating and ventilation appropriate for occupied/habitable spaces, which differs from the industrial shop standard. The HVAC layout must show dedicated conditioning for these spaces. Specific ventilation rates for these spaces are governed by the Alberta Building Code (ASSUMPTION: applicable — location TBD).

**Source:** R-01 §3.1; R-04 App B.

### C-5: Mezzanine Ventilation

The mezzanine (above parts room, utility room, and wash bay — R-01 §3.4) is intended for storage (oil totes, pumping equipment). The HVAC layout should address whether the mezzanine space requires dedicated ventilation (for stored petroleum products — ASSUMPTION: may require ventilation per safety codes). This is TBD pending Mechanical Engineer assessment.

**Source:** R-01 §3.4; R-04 App B; ASSUMPTION.

### C-6: Natural Gas Tie-In Coordination

The heating system (high-recovery) and MUA unit are likely gas-fired (ASSUMPTION — most common in Alberta industrial shop applications). The gas supply connection is coordinated via the utility tie-in (SOW-0080). The HVAC layout should indicate gas connection points so PKG-018 (Sitework) and PKG-006 (Plumbing/gas distribution — ASSUMPTION) can coordinate.

**Source:** R-01 §3.3.2 (SOW-0080); ASSUMPTION.

### C-7: Energy Efficiency Implications of HVAC Layout Decisions [C-003]

ASHRAE 90.1 (Energy Standard for Buildings) is listed as an applicable standard (ASSUMPTION: applicable -- location TBD) in the Specification Standards table. HVAC layout decisions have direct implications for energy efficiency:

- Equipment placement relative to overhead doors affects infiltration heating losses.
- Ductwork routing length and complexity (shown in layout, detailed in DEL-003-03) affects fan energy and distribution losses.
- MUA unit placement and intake orientation affects preheat energy demand in Alberta winter conditions.
- Ceiling fan placement relative to heating units affects destratification effectiveness and heating system run-time.

TBD: Mechanical Engineer to confirm whether ASHRAE 90.1 compliance analysis is required for this project and, if so, how layout decisions should be evaluated against energy efficiency criteria. This is relevant to OBJ-001 (code-compliant functional shop) if energy code compliance is mandatory.

**Source:** Specification.md Standards table (ASHRAE 90.1 row); ASSUMPTION per engineering judgment.

### C-8: RFP Addenda Tracking and Integration [X-001]

Procedure Step 2d references checking RFP addenda (R-02 Addendum 1 and any subsequent addenda) for mechanical scope changes. However, there is no documented process for how addenda-driven scope changes should be evaluated and incorporated into the HVAC layout design. Considerations:

- Addenda may introduce new HVAC requirements, modify equipment specifications, or change building layout assumptions.
- Each addendum should be reviewed against the existing Specification requirements (REQ-001 through REQ-016) to identify impacts.
- Where an addendum changes a design basis assumption (e.g., building dimensions, system type), the impact should be traced through all four documents (Datasheet, Specification, Guidance, Procedure).

TBD: Project Manager / Mechanical Engineer to establish a process for tracking addenda impacts on the HVAC layout deliverable.

**Source:** Procedure.md Step 2d; R-02 (Addendum 1 -- adds section 4.11 Bid Security, no mechanical scope change identified); ASSUMPTION per standard design change management practice.

---

## Trade-offs

### T-1: Radiant Heat vs. Unit Heaters vs. Forced-Air for Main Shop

| Option | Advantages | Disadvantages |
|---|---|---|
| Overhead radiant (infrared) tube heaters | Heats objects/floor directly; less affected by door openings; low stratification concern | High upfront cost; potential interference with overhead cranes; uniform coverage harder to achieve in very large bays |
| Unit heaters (gas-fired, high-recovery) | Lower cost; proven in Alberta shops; easier to relocate | Hot air rises — requires ceiling fans for destratification; comfort affected by door openings |
| Forced-air central heating | Even distribution possible; compatible with MUA | High ductwork costs; difficult in 35 ft industrial space; crane interference |

The RFP specifies "high recovery heating system" — this language most closely aligns with high-efficiency gas-fired unit heaters or indirect-fired systems with heat recovery. Final selection is a Mechanical Engineer design decision, to be documented in DEL-003-07 (Mechanical Specification). ASSUMPTION: unit heaters or in-space high-recovery units are the likely choice.

**Source:** R-01 §3.4 (SOW-0035); ASSUMPTION per engineering judgment.

### T-2: Exhaust Fan Location (Roof vs. Wall)

Equipment exhaust fans in repair bays can be located at the roof or on the exterior wall. Considerations:

- Roof-mounted fans: cleaner interior aesthetics; crane clearance must be verified; roof penetration requires structural coordination.
- Wall-mounted fans: easier access for maintenance; potential interference with overhead door operation areas.

Final location is a Mechanical Engineer design decision. ASSUMPTION: roof-mounted is common for large industrial shops.

**Source:** R-01 §3.4 (SOW-0038); ASSUMPTION.

### T-3: Welding Exhaust — Fixed Hood vs. Flexible Arm

| Option | Advantages | Disadvantages |
|---|---|---|
| Fixed hood capture | Simple; robust | Only effective if welding always occurs in same position; can miss fumes |
| Flexible extraction arm | Captures at source regardless of position; very effective | Higher cost; requires wall/column mounting; reach limited |

ASSUMPTION: A flexible extraction arm system is the preferred approach for a permanent welding station. Final selection is Mechanical Engineer's determination.

**Source:** R-01 §3.4 (SOW-0039); R-04 App B; ASSUMPTION.

---

## Examples

No accessible examples or project-specific precedent drawings are available from the provided sources.

TBD — Mechanical Engineer to supply applicable design precedent or references as part of DEL-003-06 (Mechanical Calculation Package) or DEL-003-07 (Mechanical Specification).

---

## Conflict Table (for human ruling)

The following items are flagged as conflicts or design decisions requiring human determination:

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-001 | Heating system type not specified beyond "high recovery" — technology selection (radiant, unit heater, forced-air) is open | R-01 §3.4 (SOW-0035) — "high recovery heating system" | R-04 App B — "Forced Air Makeup" listed but separate from heating | REQ-001; Datasheet Attributes; Specification.md REQ-001 | Mechanical Engineer to select; document in DEL-003-07 | TBD |
| CONF-002 | Ceiling fan scope listed in App B-Elec (electrical drawing) — unclear whether shown on HVAC plan or electrical plan as primary location drawing. Confirm which deliverable is the primary drawing record for ceiling fans. [E-002] | R-04 App B-Elec (SOW-0040) — ceiling fans under electrical | Decomposition SOW-0040 assigned to Mechanical scope | REQ-006; Datasheet Attributes; coordination with DEL-004-04 (Lighting Plans) | Mechanical Engineer + Electrical Engineer / Project Manager to confirm primary record ownership | TBD |
| CONF-003 | Gas supply pipe design for HVAC units — whether gas piping within the building is Mechanical or Plumbing discipline scope. Compulsory practice cannot be settled until this scope boundary is declared. [D-001] | Not explicitly stated in RFP | Standard practice varies by jurisdiction | Datasheet Conditions; Specification.md Scope Exclusions; Guidance C-6 | Mechanical Engineer + Plumbing Engineer / Project Manager to declare PKG-003 / PKG-006 boundary | TBD |
| CONF-004 | Terminology inconsistency for heating system: "High-recovery heating system" (Datasheet), "high-recovery heating system" (Specification REQ-001), "high recovery heating system" (Guidance P-2), and "heat-recovery unit heaters" (Guidance P-2 interpretation). Adopt one canonical term and define it. [B-004] | Datasheet: HVAC Systems table — "High-recovery heating system" | Guidance P-2 — introduces "heat-recovery unit heaters" as interpretation | Datasheet HVAC Systems; Specification REQ-001; Guidance P-2; all cross-references | Mechanical Engineer to establish canonical term | TBD |
