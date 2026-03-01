# Guidance — DEL-013-01: High-Recovery Heating System

---

## Purpose

DEL-013-01 exists to deliver the primary space-heating capability for the New North Shop addition at the West Dried Meat Lake Regional Landfill. The heating system is the thermal core of the HVAC network: it provides conditioned air to a large-volume industrial bay (approx. 13,000 sq ft, 35 ft ceiling) and enables the heat-recovery loop that integrates with the air exchanger and makeup air systems.

The system directly supports:
- **OBJ-001**: Deliver a code-compliant, fully functional maintenance shop addition — the heating system is an explicitly listed RFP requirement (R-01 §3.4) and must pass applicable inspections.
- **OBJ-004**: Install and commission all mechanical and HVAC systems to operational readiness — the heating system is the primary thermal plant within PKG-013.

Without a functional heating system, the facility cannot operate in Alberta winter conditions and cannot satisfy the County's operational program.

**Source:** R-01 §3.4; WDMLRL_Decomposition_Claude.md §5 OBJ-001, OBJ-004; `_CONTEXT.md` Description.

---

## Principles

### 1. Heat Recovery is the Defining Characteristic
The RFP explicitly specifies a "high recovery heating system" (R-01 §3.4), not a conventional heating unit. This designation means the system is intended to recover thermal energy — typically from exhaust air, return air, or combustion gases — and reuse it rather than exhausting it. Equipment selection must respect this design intent. A standard furnace or unit heater does not satisfy the RFP requirement.

**Energy Efficiency Value Proposition:** The high-recovery designation is specifically intended to reduce operating costs by recovering thermal energy that would otherwise be lost through exhaust streams. TBD — expected energy efficiency benefit (operating cost reduction percentage or energy savings estimate) to be quantified by Mechanical Engineer during design (estimated recovery efficiency from DEL-003-06/DEL-003-07). Without quantification, the value proposition rests on the qualitative principle that heat recovery reduces the net thermal input required to maintain space temperature. *(Lensing ref: F-004)*

**Source:** R-01 §3.4 (explicit).

### 2. This System is the Thermal Hub of PKG-013
The heating system is declared the "core of the HVAC network" in `_DEPENDENCIES.md`. All other PKG-013 subsystems (air exchanger, makeup air, exhaust systems, ceiling fans) either feed into or depend on the heating system's thermal capacity and controls. Scheduling, sequencing, and commissioning must treat DEL-013-01 as the lead system within PKG-013.

**Source:** `_DEPENDENCIES.md` Critical Path.

### 3. Design Before Procurement
This is a design-build project. The heating system shall not be procured until the Mechanical Engineer has issued the Mechanical Specification (DEL-003-07) and the relevant mechanical drawings (DEL-003-02, DEL-003-03). Premature equipment selection risks non-compliance with the engineered design or code requirements.

**Source:** R-01 §3.3.2 (IFC drawings required; P.Eng. stamped); OBJ-003 (complete design before construction begins); ASSUMPTION: standard design-build sequencing practice.

### 4. Utility Room is the Governing Spatial Constraint
All equipment must fit within the utility room (DEL-012-02) shown on the Appendix B (Shop) floor plan. The utility room shares the mezzanine level above it with the parts room and wash bay. Equipment footprint, service clearances, and ductwork routing must be coordinated with architectural and structural drawings before ordering or installing equipment.

**Source:** Appendix B (Shop) floor plan; `_DEPENDENCIES.md` Constraint Notes.

### 5. Code Compliance is Non-Negotiable
Alberta Safety Codes apply to all mechanical installations. The Authority Having Jurisdiction (AHJ) must inspect and approve the installation. All Safety Code permit fees are paid by Camrose County (they are excluded from the proponent's scope per R-01 §3.3.1), but the Proponent is responsible for obtaining and scheduling all inspections.

**Source:** R-01 §3.3.1 (County pays permit fees); R-01 §3.3.2 (Proponent obtains permits, coordinates inspections).

---

## Considerations

### Consideration A: Alberta Climate Loading
The shop is located near Ferintosh, Alberta (~30 km south of Camrose). Alberta's climate requires designing for significant winter heating loads. With a 35 ft ceiling height and high-volume air exchange occurring simultaneously, the heating system must overcome both the building envelope heat loss and the thermal deficit introduced by makeup air (DEL-013-03). The mechanical engineer's calculation package (DEL-003-06) will size the system accordingly. ASSUMPTION: The Mechanical Engineer will apply the Alberta design temperature for Camrose County when performing load calculations.

**Source:** R-01 §1.0 (project location); R-01 §3.4 (ceiling height, makeup air requirements); ASSUMPTION.

### Consideration B: Simultaneous Ventilation Load
The RFP requires both a high-volume air exchanger (DEL-013-02) and a forced-air makeup system (DEL-013-03). When operating simultaneously with the heating system, these introduce a significant amount of cold outdoor air that the heating system must condition. "High-recovery" functionality is specifically intended to mitigate this thermal penalty by recovering heat from exhaust streams before they leave the building. The interaction between heating capacity and ventilation volume is a critical design coordination point.

**Source:** R-01 §3.4; `_DEPENDENCIES.md`.

### Consideration C: Industrial Environment Durability
The shop houses heavy equipment (tracked vehicles, motor scrapers), a welding station, and exhaust-generating machinery. Equipment selected for the heating system must be rated for an industrial environment — this includes consideration of particulate loading, potential hydrocarbon exposure, and vibration. Equipment not designed for industrial service may fail prematurely or require costly maintenance.

**Source:** R-01 §3.1; Appendix B (Shop) floor plan (welding station, heavy equipment bays visible); ASSUMPTION: equipment selection to address industrial-grade requirement.

### Consideration D: Controls Integration Complexity
The `_DEPENDENCIES.md` specifies that controls must integrate with the building management system. PKG-013 contains six interdependent subsystems (DEL-013-01 through DEL-013-06). Coordinating controls across all six — while maintaining compatibility with the BMS — requires early engagement between the Mechanical Contractor, controls supplier, and electrical contractor (PKG-015). TBD: The BMS platform and controls protocol are not specified in the RFP; the design team must determine these (see CONF-003 and Specification REQ-008 BMS protocol note).

**Source:** `_DEPENDENCIES.md`; R-01 §3.3.2.

### Consideration E: Upstream Dependency on Utility Room
Installation cannot begin until DEL-012-02 (Utility Room) is substantially complete. If the utility room is delayed, the entire PKG-013 critical path is affected. The Project Manager (PKG-019) should track DEL-012-02 completion as a gating milestone for DEL-013-01 commencement.

**Source:** `_DEPENDENCIES.md` External Dependencies and Dependency Map.

### Consideration F: Manufacturer Installation Compliance Enforcement *(NEW — Lensing ref: D-001)*
REQ-003 and REQ-011 require compliance with manufacturer installation specifications. TBD: The responsible party for verifying manufacturer specification compliance during installation must be clarified. Options include:
- (a) Mechanical Engineer as independent reviewer during site visits
- (b) Third-party inspector engaged by the Owner
- (c) Mechanical Contractor's internal quality control (QC) program

This is distinct from the AHJ Safety Code inspection, which addresses code compliance but may not cover all manufacturer-specific requirements. The chosen approach should be documented in the Specification or this Guidance document once determined.

**Source:** Specification REQ-003, REQ-011; Procedure Phase 3 steps. Lensing ref: D-001.

### Consideration G: Owner Acceptance Criteria *(NEW — Lensing ref: D-003)*
The current documents address contractor obligations and code compliance, but do not describe the Owner's (Camrose County) specific expectations for heating system performance or satisfaction criteria at handover. TBD: Owner acceptance criteria beyond code compliance and commissioning pass should be confirmed with the Owner or Project Manager. These may include:
- Comfort criteria (temperature range, uniformity) for shop occupants
- Operating cost expectations
- Noise level limits in occupied spaces
- Ease of maintenance and operation by County staff

Without defined Owner acceptance criteria, the "conclusive merit verdict" for this deliverable rests solely on contractor and code compliance metrics.

**Source:** R-01 §2.14 (completion and acceptance); OBJ-001; OBJ-004. No explicit Owner-specific performance expectations found in accessible documents. Lensing ref: D-003.

### Consideration H: Guarantee Period Obligations (R-01 Section 2.10) *(NEW — Lensing ref: X-005)*
R-01 Section 2.10 establishes a Guarantee Period with a 10-day rectification obligation. For the heating system specifically, this means:
- After commissioning and Owner acceptance, the Mechanical Contractor remains obligated to rectify deficiencies identified during the guarantee period
- Deficiencies must be rectified within 10 days of notification
- This obligation applies to all components of DEL-013-01 including the heating unit, ductwork connections, controls integration, and heat recovery function
- The Mechanical Contractor should plan for reasonable post-commissioning support availability during the guarantee period

The guarantee period interacts with Procedure Step 5.4 (Deficiency Rectification) and the warranty terms required by Specification REQ-014. The Mechanical Contractor should ensure that manufacturer warranty terms are at least as protective as the R-01 guarantee period requirements.

**Source:** R-01 §2.10 Guarantee Period; Procedure Step 5.4. Lensing ref: X-005.

---

## Terminology Note *(NEW — Lensing ref: E-001, X-001)*

The following role terms are used across the four DEL-013-01 documents. To avoid ambiguity, the intended meaning of each is defined here:

| Term | Intended Meaning | Used In |
|---|---|---|
| **Mechanical Engineer** | The Professional Engineer (P.Eng.) of record responsible for the mechanical design, stamping IFC drawings, reviewing submittals, and accepting the commissioning report. This is the design authority. | Specification (REQ-003, Standards, Verification); Procedure (Phase 1, Phase 4–5); Datasheet (Attributes) |
| **Mechanical Contractor** | The trade contractor responsible for procuring, installing, and commissioning the heating system per the approved design. This is the execution authority. | Specification (Verification — primary responsible party); Procedure (all phases); Datasheet (Responsible Party) |
| **Design team** | Collective term for the Mechanical Engineer plus any supporting design disciplines (structural, electrical, architectural) involved in design coordination. Used when the activity involves multi-discipline coordination rather than single-discipline authority. | Guidance (Consideration D); Specification (REQ-006 Verification) |
| **Controls Contractor / BMS Integrator** | The party responsible for programming and integrating the building management system. May be the Mechanical Contractor, a sub-contractor, or a separate controls specialist depending on project structure. | Specification (REQ-008 Verification); Procedure (Step 3.5) |

> **Note:** Where Procedure previously used "Mechanical Engineer" for both design review and commissioning acceptance roles, both uses refer to the P.Eng. of record unless otherwise noted. The Mechanical Contractor's own engineer (if any) is not the "Mechanical Engineer" for the purposes of these documents.

---

## Trade-offs

### Trade-off 1: Equipment Selection — Proprietary vs. Specified-and-Tendered
High-recovery heating equipment (e.g., make-up air units with heat recovery, hydronic systems with heat exchangers, or radiant systems with recovery) varies significantly by manufacturer. A proprietary specification (sole-source) may allow tighter integration with other equipment but reduces competitive pricing. A performance specification approach preserves competition but requires the Mechanical Engineer to define minimum recovery efficiency and integration requirements precisely.

**Proposed approach (ASSUMPTION):** The Mechanical Engineer (DEL-003-07) should issue a performance-based specification with minimum thermal recovery efficiency, integration requirements, and environmental ratings, allowing the Mechanical Contractor to select a compliant product.

### Trade-off 2: Radiant Heat vs. Forced-Air Heat
High-bay industrial spaces (35 ft ceiling, large vehicle traffic) can be heated by either radiant heating systems (infrared or radiant tube) or high-efficiency forced-air units. Radiant heating is often more energy-efficient in high-bay spaces with heavy traffic and frequent door openings. However, integration with an air exchanger heat-recovery loop is more natural for forced-air configurations. The Mechanical Engineer's design (DEL-003-02/07) will determine the approach.

**TBD:** Equipment type confirmation pending mechanical design.

### Trade-off 3: Gas vs. Other Energy Source
Natural gas is the most common fuel source for industrial heating in Alberta and is referenced as a utility tie-in in R-01 §3.3.2. However, the RFP does not explicitly state the fuel source for the heating system. If natural gas is unavailable at the site, propane or electric alternatives may be required, each with different capacity, code, and cost implications. **Note:** If gas-fired, Alberta requires certified gas fitter installation and gas permits (see Specification REQ-012). *(Lensing ref: B-004, F-002)*

**ASSUMPTION:** Natural gas supply is available or will be made available via utility tie-in (R-01 §3.3.2 references gas tie-in). Confirm with the design team.

---

## Examples

TBD — No specific product examples or analogous installations are cited in the accessible source documents. The Mechanical Engineer (DEL-003-07) will identify suitable equipment references.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-001 | Fuel/energy source not specified. RFP references "coordinate natural gas... tie-ins" (§3.3.2) but does not explicitly assign natural gas to the heating system. This must be formally resolved before procurement; see Datasheet Fuel/Energy Source and Specification REQ-012 (conditional on fuel source). *(Elevated per B-004)* | R-01 §3.3.2 (natural gas tie-in referenced in site works scope) | No explicit fuel assignment for heating system in R-01 §3.4 | Specification REQ-003, REQ-012; Guidance Trade-off 3; Datasheet Attributes | PROPOSAL: Confirm natural gas as primary fuel source with Mechanical Engineer during design development (DEL-003-07) | TBD |
| CONF-002 | Heating system equipment type (radiant vs. forced-air vs. hydronic) is not defined in the RFP. "High recovery" is stated as a design requirement but the mechanism is unspecified. | R-01 §3.4 ("High recovery heating system" listed as a design requirement) | No equipment type detail in RFP §3.4 or Appendix B | Specification REQ-001, REQ-010; Guidance Trade-off 2 | PROPOSAL: Mechanical Engineer to determine equipment type in DEL-003-07 Mechanical Specification | TBD |
| CONF-003 | BMS platform and controls protocol are not defined in the RFP or decomposition. `_DEPENDENCIES.md` requires controls integration with BMS, but BMS is not specified. | `_DEPENDENCIES.md` ("Controls must integrate with building management system") | R-01 (no BMS specification found in accessible sections) | Specification REQ-008; Guidance Consideration D | PROPOSAL: Define BMS platform in mechanical/electrical design phase (PKG-003/PKG-004) before controls procurement | TBD |
| CONF-004 | Commissioning sign-off authority ambiguity. Specification Verification table (REQ-009) previously assigned commissioning sign-off to "Mechanical Contractor," while Procedure Step 5.1 submits the report to "Mechanical Engineer and Project Manager" for acceptance. *(NEW — Lensing ref: E-004)* | Specification Verification table REQ-009 (Mechanical Contractor signs commissioning report) | Procedure Step 5.1 (report submitted to Mechanical Engineer and Project Manager for acceptance) | Specification Verification REQ-009; Procedure Step 5.1 | PROPOSAL: Mechanical Contractor prepares and signs the commissioning report; Mechanical Engineer reviews and accepts it. Updated in Specification REQ-009 verification row. | TBD |

---

## Semantic Lensing Enrichment Log (Pass 3)

The following items from `_SEMANTIC_LENSING.md` were applied to this document:

| ItemID | Action Taken |
|---|---|
| B-004 | Elevated CONF-001 with note that fuel source ambiguity must be formally resolved before procurement; cross-referenced Datasheet and Specification REQ-012 |
| D-001 | Added Consideration F: Manufacturer Installation Compliance Enforcement — clarifying who verifies manufacturer spec compliance during installation |
| D-003 | Added Consideration G: Owner Acceptance Criteria — TBD for Owner-specific performance expectations beyond code compliance |
| E-001 | Added Terminology Note section standardizing use of "Mechanical Engineer," "Mechanical Contractor," "Design team," and "Controls Contractor" across all four documents |
| E-004 | Added CONF-004 to Conflict Table — commissioning sign-off authority ambiguity between Mechanical Contractor and Mechanical Engineer |
| F-004 | Added Energy Efficiency Value Proposition rationale to Principle 1, with TBD for quantified benefit |
| X-001 | Incorporated into Terminology Note — clarified that "Mechanical Engineer" refers to P.Eng. of record in all Procedure references |
| X-005 | Added Consideration H: Guarantee Period Obligations — explaining R-01 §2.10 implications for the heating system |
