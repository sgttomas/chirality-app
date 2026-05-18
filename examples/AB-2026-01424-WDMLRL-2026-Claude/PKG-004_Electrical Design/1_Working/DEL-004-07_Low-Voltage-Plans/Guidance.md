# Guidance: DEL-004-07 Low-Voltage System Plans

---

## Purpose

DEL-004-07 documents the low-voltage system design for the New North Shop Addition at the West Dried Meat Lake Regional Landfill. The drawing set gives the installation contractor (DEL-015-05) the routed, coordinated, IFC-stamped plans needed to install security camera system wiring and 2-way radio antenna wiring within the facility.

> **Note on scope boundary:** The Specification scope statement references "applicable renovation areas of the Old North Shop," but the Datasheet records Old North Shop low-voltage scope as TBD, and this Guidance and the Procedure address only the New North Shop Addition explicitly. See Conflict Table CON-007-02 below for resolution pathway.

Within the broader project objectives, this deliverable contributes to:

- **OBJ-001** — Code-compliant, fully functional maintenance shop that passes all applicable inspections (security and communications systems are part of the operational program).
- **OBJ-003** — Complete, P.Eng.-stamped IFC documentation across all disciplines before construction begins.
- **OBJ-005** — All electrical and low-voltage systems installed and commissioned to operational readiness (specifically SOW-0064 and SOW-0065).

Source: Decomposition §5 (Objectives), §7 (PKG-004 deliverables table); RFP §1.0.

---

## Vocabulary Note

> **Terminology normalization:** The following terms are used interchangeably across the four documents to refer to the same scope element. For consistency in future revisions, the preferred term is listed first:
> - **Security camera system wiring** (preferred) — also appears as "security camera wiring," "camera wiring," "security camera system" in various documents. All refer to the wiring scope under SOW-0064.
> - **2-way radio antenna wiring** (preferred) — also appears as "antenna wire," "radio antenna wire," "antenna wire for 2 way radios." All refer to the wiring scope under SOW-0065.
>
> Source: Normalization identified via lensing item B-005; see Datasheet §Attributes, Specification §Scope, Procedure §Steps.

---

## Principles

### Low-Voltage Scope is Narrow but Confirmed
The available source material explicitly identifies only two low-voltage systems: security camera wiring (SOW-0064) and 2-way radio antenna wire (SOW-0065). Both appear in the Appendix B Electrical Notes. The design-build nature of the contract (RFP §3.4) means the Electrical Engineer has latitude to determine the detailed routing, device counts, and cable specifications, provided the resulting design meets Alberta Safety Codes and fulfills the County's operational intent.

Source: RFP §3.4; App B-Elec; Decomp §3 (SOW-0064, SOW-0065).

### Design-Build Latitude Within a Defined Functional Intent
The RFP states: "The County only has a concept in mind; therefore, it will be a design/build project." (RFP §3.4). For low-voltage systems, this means the Electrical Engineer determines cable types, conduit fill, number of camera positions, and antenna routing based on professional judgment, code requirements, and the County's operational needs. Device counts and exact positions should be validated during the preliminary design review with the County.

Source: RFP §3.4; SOW-0010d.

### IFC Coordination Priority
The low-voltage plans must be fully coordinated with architectural, structural, and other electrical drawings before being issued for construction. Routing conduit through structural elements or into congested electrical zones without coordination is a common source of field conflicts. Because the building is a concrete structure with a 35' ceiling (App B-Elec; RFP §3.4), conduit routing and penetration sleeves must be resolved at the IFC stage.

Source: RFP §3.3.2; SOW-0018; App B-Elec.

### Security Camera System Context
The facility is a landfill maintenance shop with high-value equipment (two 5-tonne cranes, compressors, pressure washers, welding stations — App B-Elec). A security camera system supports asset protection and site monitoring. The exact camera technology (IP vs. analog), cable type (Cat 6, coax), and recording/NVR infrastructure are TBD and should be determined in consultation with the County during preliminary design.

Source: App B-Elec; ASSUMPTION — operational context inferred from facility type described in RFP §3.1 and App B-Elec.

### 2-Way Radio Antenna Context
The facility operates in a rural landfill environment approximately 30 km south of Camrose (RFP §1.0). 2-way radio communication is standard for heavy equipment operations. Antenna wire routing should account for the building's concrete construction (35' ceiling) which may attenuate radio signals inside the building, suggesting through-wall or roof-mounted antenna points. Specific antenna system design is TBD.

**Radio system type:** TBD — the radio system type (VHF/UHF, digital/analog) and whether in-building signal distribution is required have not been recorded in any source document. These parameters are essential to determining antenna placement, cable type, and whether a propagation study is warranted. Confirm with County operations staff.

**Antenna placement strategy rationale:** The decision between a single exterior antenna with interior distribution versus multiple antenna points with in-building distribution depends on: (a) the radio system frequency band (VHF vs. UHF have different propagation characteristics through concrete), (b) the degree of RF attenuation by the concrete structure, and (c) operational coverage requirements inside the building. A radio frequency propagation study may be warranted for this concrete structure if in-building coverage is required. The Electrical Engineer should assess whether the project scope and budget justify a propagation study or whether conservative antenna placement (e.g., exterior antenna with interior repeater) is sufficient. ASSUMPTION — rationale is inferred from general RF engineering principles applied to the concrete construction type stated in RFP §3.4.

Source: AB-2026-01424-Appendix_B__Electrical_.pdf; RFP §1.0, §3.4; ASSUMPTION — attenuation concern is inferred from concrete construction type stated in RFP §3.4.

---

## Considerations

### Scope Uncertainty: Additional Low-Voltage Systems
The available sources enumerate only security cameras and radio antenna wire. However, the County's operations may require additional low-voltage systems such as:
- Data/network cabling (for office functions)
- Fire alarm (code-required — ASSUMPTION)
- Access control (secure parts room, App B-Elec shows 6' roll-up door to parts area)
- Intercom or PA

The Electrical Engineer should raise these questions at the preliminary design stage. If additional systems are required by code or the County, they should be incorporated into this drawing set or clearly excluded with justification.

Source: ASSUMPTION — derived from facility program described in RFP §3.1, §3.4 and App B-Elec; specific additional systems not stated in available sources.

### Permit Pathway
Low-voltage installations in Alberta are regulated under the Safety Codes Act. The applicable permit category (electrical safety code permit) must be obtained before construction. The unresolved question is whether low-voltage systems (security cameras, radio antenna) require a **separate** Safety Code permit or are covered under the **general electrical Safety Code permit** (DEL-009-03). This distinction affects permit application timing, inspection scheduling, and cost.

**Resolution required:** The Electrical Engineer or Project Manager shall confirm with the AHJ whether a separate low-voltage/communications permit is required. The permit category determination shall be documented and verified prior to permit application (see Specification REQ-007-04a verification entry).

**Inspection sequence rationale:** Procedure Step 8 references "low-voltage rough-in and final inspection." The basis for this two-stage inspection sequence (rough-in before concealment, final after termination) is standard Alberta Safety Code practice for electrical installations. Whether low-voltage inspections are conducted separately from general electrical inspections or combined depends on the permit category determination above. The Electrical Engineer should confirm the applicable inspection sequence with the AHJ.

Source: RFP §3.3.2; SOW-0007, SOW-0009; ASSUMPTION — AHJ permit category and inspection sequence not specified in available sources; inspection rationale is ASSUMPTION based on standard Alberta Safety Code practice.

### Building Voltage and Low-Voltage Power Supply
The Datasheet records the building power supply as "ASSUMPTION: 120/208V or 347/600V" — the voltage class has not been confirmed. For low-voltage system equipment (e.g., PoE switches for IP cameras, NVR/DVR units), the applicable power supply is typically 120V single-phase from a branch circuit, regardless of the building's primary service voltage. The Electrical Engineer should confirm the building voltage class and ensure that branch circuits serving low-voltage equipment are appropriately sized and located. This voltage assumption should be normalized across all documents once confirmed.

Source: Datasheet §Conditions; RFP §3.4; ASSUMPTION — low-voltage equipment power supply inference is standard engineering practice.

### Coordination with Mechanical Systems
Ceiling fans (SOW-0040; 6 fans in main shop, App B-Elec) and exhaust fans (SOW-0066; App B-Elec) occupy ceiling space. Low-voltage conduit routing in the main shop ceiling must account for these mechanical elements.

Source: App B-Elec; SOW-0040, SOW-0066.

### Coordination with Crane Infrastructure
Two 5-tonne overhead cranes (SOW-0059, SOW-0067) operate on runway beams in the main shop. Low-voltage conduit and camera mounting locations must not conflict with crane travel envelopes.

Source: App B-Elec; SOW-0059, SOW-0067; ASSUMPTION — clearance coordination is inferred from crane-to-ceiling relationships standard in industrial crane installations.

---

## Trade-offs

| Trade-off | Option A | Option B | Proposed Direction | Source |
|---|---|---|---|---|
| Camera system technology | IP cameras (Cat 6 cabling, PoE) | Analog cameras (coaxial cabling) | ASSUMPTION: IP is current industry standard for new installations; confirm with County at preliminary design. **Evaluation criteria:** (1) Initial cost — IP typically higher camera cost but lower cabling cost (Cat 6 vs. coax + separate power); (2) Maintenance — IP systems offer remote diagnostics; analog requires local access; (3) Network bandwidth — IP requires network infrastructure (switches, NVR); analog requires dedicated coax runs; (4) Future-proofing — IP supports higher resolution and software upgrades; analog is legacy technology with declining manufacturer support; (5) PoE power budget — IP/PoE requires PoE switch sizing and UPS consideration. ASSUMPTION — evaluation criteria are general industry considerations, not project-specific analysis. | ASSUMPTION |
| Conduit vs. cable tray | Individual conduit runs | Cable tray in high-density zones | ASSUMPTION: cable tray may be more cost-effective in the main shop ceiling for multiple low-voltage runs; confirm at design stage | ASSUMPTION |
| Antenna point count | Single exterior antenna with interior distribution | Multiple antenna points with in-building distribution | TBD — depends on radio system type and concrete shielding assessment; confirm with County | TBD |
| Scope boundary: data/IT | Include in this drawing set | Separate IT infrastructure outside this contract | TBD — not stated in available sources; to be confirmed with County at preliminary design | TBD |

---

## Examples

TBD — No example low-voltage plans from comparable facilities are available in the accessible source material. The Electrical Engineer should draw on their experience with similar Alberta industrial/heavy-equipment facilities for layout conventions.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CON-007-01 | The RFP §3.4 lists design requirements for the building but does not enumerate specific low-voltage systems. App B-Elec lists only "Wiring for Security Cameras" and "Antenna Wire for 2 Way Radios." It is unclear whether additional low-voltage systems (fire alarm, data, access control) are expected within this deliverable's scope or are a County-supplied/separate scope. | RFP §3.4 (design requirements list) | AB-2026-01424-Appendix_B__Electrical_.pdf (Electrical Notes) | Specification REQ-007-08, REQ-007-09; Procedure Step 2 (scope confirmation) | PROPOSAL: Raise explicitly at preliminary design review (DEL-004-01) and confirm County intent before IFC issue. | TBD |
| CON-007-02 | Specification scope says "New North Shop Addition (and applicable renovation areas of the Old North Shop)" but Guidance and Procedure address only the New North Shop Addition explicitly. Datasheet records Old North Shop low-voltage scope as TBD. The scope boundary for Old North Shop renovation areas is inconsistent across documents. | Specification §Scope ("applicable renovation areas of the Old North Shop") | Datasheet §Facility Context ("Low-voltage scope for renovated areas TBD"); Guidance §Purpose and Procedure §Purpose (New North Shop Addition only) | Specification §Scope; Datasheet §Facility Context; Guidance §Purpose; Procedure §Purpose | PROPOSAL: County ruling at preliminary design to confirm whether Old North Shop renovation areas are in or out of DEL-004-07 scope. | TBD |
