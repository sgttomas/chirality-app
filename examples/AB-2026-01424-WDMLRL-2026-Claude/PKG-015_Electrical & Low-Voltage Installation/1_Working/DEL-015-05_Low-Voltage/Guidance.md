# Guidance — DEL-015-05 Low-Voltage Systems

---

## Purpose

This deliverable exists to provide the West Dried Meat Lake Regional Landfill maintenance facility with the communication and surveillance infrastructure necessary for safe and effective operations. Specifically:

- **Security camera wiring** (SOW-0064) supports the Owner's facility security and monitoring objectives at an active landfill and maintenance site.
- **2-way radio antenna wiring** (SOW-0065) supports on-site and near-site radio communications for landfill operations staff.

These systems are called out explicitly in the conceptual electrical drawing (App B-Elec) and in Objective OBJ-005, which requires all electrical and low-voltage systems to be commissioned to operational readiness.

This deliverable also supports **OBJ-001** ("Deliver a code-compliant, fully functional maintenance shop addition and associated renovations that satisfy the County's operational program"). Low-voltage wiring for security cameras and 2-way radio communications is part of the "all spaces, systems, and equipment specified in the RFP and conceptual drawings" that OBJ-001 requires. Without these systems installed, the maintenance shop addition would not be fully functional for the County's operational program, as security monitoring and on-site radio communication are integral to facility operations at an active landfill. [Lensing: D-002]

**Source:** Decomposition §5 (OBJ-001, OBJ-005); App B-Elec (Electrical Notes); _CONTEXT.md

---

## Principles

1. **Wiring before walls close.** Low-voltage rough-in must be sequenced ahead of wall and ceiling closures. In a concrete structure with a 35' ceiling (RFP §3.4), penetration sleeves and conduit anchor points need to be coordinated with the structural and envelope trades (PKG-011) before pours. Missed rough-in in concrete construction is expensive to remedy.

2. **Design governs installation.** The IFC Low-Voltage System Plans (DEL-004-07) are the authoritative source for routing, cable types, quantities, and termination locations. Do not install low-voltage rough-in based solely on the conceptual drawing (App B-Elec); the conceptual drawing identifies that these systems are required but does not provide installation-level detail.

3. **Scope boundary clarity is essential.** The conceptual drawing uses the phrases "wiring for security cameras" and "antenna wire for 2-way radios." This language suggests the scope is limited to wiring/conduit rough-in, not the supply of camera or radio equipment. This boundary must be confirmed with the Owner and documented in DEL-004-07 or the contract schedule of values before procurement.
   - ASSUMPTION: Camera heads, mounting hardware, recording equipment, radio base stations, and antenna hardware are Owner-supplied or specified separately. This assumption must be confirmed.

4. **Communication line coordination.** RFP §3.3.2 requires the successful Proponent to "coordinate natural gas, electrical tie-ins, and communication lines." The antenna wiring for 2-way radios may involve an exterior building penetration or rooftop antenna mount, which requires coordination with the building envelope trade (PKG-011) and potentially with the County's radio system provider.
   - ASSUMPTION: The antenna is mounted on or near the building exterior; routing from antenna entry point to termination room (see Principle 7) to be confirmed in DEL-004-07.

5. **Alberta Safety Code requirements apply.** All low-voltage wiring in Alberta must comply with the Alberta Electrical Code (CEC Part I as adopted). Even where low-voltage systems are sometimes treated as "exempt" in other jurisdictions, Alberta's adoption of the CEC requires compliance and may require a permit and Safety Codes Officer inspection. Confirm with the project Electrical Engineer.

6. **Document precedence hierarchy.** REQ-015-05-03 establishes that IFC drawings govern where conflict exists between the Specification and IFC drawings. For broader document conflicts, the following hierarchy applies per CCDC 14-2013 order of precedence (ASSUMPTION: standard CCDC 14-2013 hierarchy -- confirm with contract administrator):
   - (1) Agreement between Owner and Contractor
   - (2) Definitions, General Conditions
   - (3) Supplementary Conditions
   - (4) Specifications (DEL-004-09, this Specification)
   - (5) Drawings (DEL-004-07 IFC drawings)
   - (6) Other contract documents listed in the Agreement

   Within the deliverable document set, the Specification is the normative (controlling) document. Guidance and Procedure are supportive and shall not override Specification requirements. Where Guidance or Procedure language conflicts with Specification, the Specification governs. [Lensing: X-001]

7. **Canonical terminology for termination location.** Throughout this deliverable's documents, the physical location where low-voltage cables terminate (camera home-runs, antenna cable endpoint) shall be referred to as the **"termination room"**. This term replaces the following synonyms used in earlier drafts: "head-end location," "IDF closet," "equipment room," "panel/termination location," "interior termination location," "distribution point," and "equipment location." The actual room designation (utility room, office, or dedicated space) is TBD per DEL-004-07. [Lensing: B-003]

---

## Considerations

### Sequencing

- Low-voltage rough-in (conduit and pull wire/cable) should be installed concurrently with or immediately following rough-in of power wiring in each zone, before insulation and drywalling/panel closures.
- In the wash bay, office, parts room, and utility room areas, confirm which spaces require security camera coverage before rough-in to avoid missed locations.
- The antenna cable run from exterior entry point to the termination room (see Principle 7) needs a clear path through the building structure. Identify this path during design coordination.

### Interface with DEL-004-07 (Low-Voltage Plans)

- DEL-015-05 cannot be fully planned until DEL-004-07 (Low-Voltage System Plans) is issued for construction. The IFC drawings will define:
  - Exact camera locations and coverage zones
  - Antenna cable entry point, routing path, and termination location
  - Cable type specifications (e.g., coaxial for antenna, Cat6/coax for cameras — TBD)
  - Conduit sizing and fill requirements
- Electrical Contractor should review the design drawings for constructability comments prior to IFC issue.

### Interface with DEL-015-04 (Equipment Power Circuits)

- Low-voltage systems may share conduit runs or pathway infrastructure with power wiring up to the point where separation is required by code. Coordinate with DEL-015-04 to avoid conflict and to share trench or conduit infrastructure where permitted.

### Security Camera System Design

- The number, type, and placement of security cameras are not specified in available sources (only "wiring for security cameras" noted on App B-Elec). Camera placement will be determined during detailed design (DEL-004-07).
- ASSUMPTION: Camera locations will be driven by security objectives at a working landfill facility (vehicle access areas, building entry points, equipment storage areas). The Electrical Engineer and Owner should confirm coverage intent before DEL-004-07 is issued.

### Low-Voltage-Specific Standards Rationale

No low-voltage-specific standards (TIA-568, BICSI, CSA T530) are currently referenced in this deliverable's documents. Rationale: the RFP and conceptual drawings cite only general Alberta Electrical Code compliance; the scope is limited to security camera wiring and radio antenna wiring (not data networking or structured cabling). If the Electrical Engineer determines in DEL-004-09 that structured cabling standards apply (e.g., if IP cameras require TIA-568 compliance for Category cable installation), the Specification Standards table shall be updated accordingly. [Lensing: C-002]

### Radio System Design

- The type of 2-way radio system is not specified in available sources (only "antenna wire for 2 way radios" noted on App B-Elec). Whether this is a VHF, UHF, or digital system, and whether it interfaces with an existing county radio network, is TBD.
- ASSUMPTION: The antenna wire installation is for a portable/handheld radio charger or base station inside the building, with an exterior antenna for improved signal range — typical for landfill/maintenance operations. Confirm with Owner.

---

## Trade-offs

| Decision | Option A | Option B | Recommended Direction | Source |
|---|---|---|---|---|
| Conduit vs. direct-buried cable for camera runs | EMT or rigid conduit (more code-compliant, easier future pulls) | Direct-stapled cable where permitted | Use conduit — preferred for industrial setting and for future flexibility | ASSUMPTION (industry practice); confirm in DEL-004-09 |
| Camera wiring cable type | Coaxial (RG-59/RG-6) for analog | Cat6/Cat6A for IP cameras | TBD — depends on camera system type selected by Owner or Electrical Engineer | DEL-004-07 (not yet issued) |
| Antenna cable type | RG-8/LMR-400 (low-loss for long runs) | RG-58/RG-6 (lower cost, higher loss) | TBD — depends on antenna location distance and radio system specs | DEL-004-07 (not yet issued) |
| Scope boundary (wiring only vs. equipment) | Contractor supplies and installs cameras/equipment | Contractor installs wiring/conduit only; Owner supplies equipment | Wiring/conduit only per SOW-0064/SOW-0065 language — ASSUMPTION; confirm with Owner | App B-Elec; SOW-0064/0065 |

> **Cost/schedule risk of unresolved scope boundary (CONF-015-05-01/02):** Delayed resolution of the scope boundary (wiring-only vs. equipment supply) may impact procurement lead times for cable and conduit materials, since cable type depends on whether IP cameras (Cat6/Cat6A) or analog cameras (coaxial) are selected. Additionally, delayed scope confirmation may affect sequencing with structural trades -- conduit sleeve sizes and quantities cannot be finalized until the scope and camera system type are confirmed. The primary risk to this deliverable's value delivery is the schedule impact of these unresolved decisions cascading into the construction window. ASSUMPTION: Design-Builder project controls should track this risk. [Lensing: F-004]

---

## Examples

No project-specific installation examples are available from the accessible sources. General reference:

- Typical industrial security camera rough-in: conduit stub-up at camera mounting height with pull string, junction box at mounting point, conduit home-run to termination room (see Principle 7 for canonical terminology [Lensing: B-003]).
- Typical radio antenna rough-in: coaxial cable from antenna mounting location (exterior roof/wall penetration) through watertight conduit fitting, down to termination room.

These are industry-standard practices — ASSUMPTION: apply pending DEL-004-07 issue.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-015-05-01 | Scope boundary unclear: "wiring for security cameras" (SOW-0064) may or may not include camera hardware supply and installation | SOW-0064 / App B-Elec: "wiring for security cameras" (wiring language) | _CONTEXT.md: "Data and security infrastructure" (broader language) | Specification.md §Excluded; Datasheet.md Attributes | PROPOSAL: Confirm scope is wiring/conduit rough-in only; camera equipment is Owner-furnished or specified separately. Resolve in contract schedule of values and DEL-004-07. | TBD |
| CONF-015-05-02 | Scope boundary unclear: "antenna wire for 2-way radios" (SOW-0065) may or may not include antenna hardware, mounts, or radio equipment | SOW-0065 / App B-Elec: "antenna wire" (wiring language) | _CONTEXT.md: "Control systems and communications" (broader language) | Specification.md §Excluded; Datasheet.md Attributes | PROPOSAL: Confirm scope is cable/conduit rough-in only; antenna hardware and radio equipment are Owner-furnished or specified separately. Resolve in contract schedule of values and DEL-004-07. | TBD |
| CONF-015-05-03 | Document precedence hierarchy incomplete: REQ-015-05-03 establishes IFC drawings > Specification, but no broader hierarchy covers RFP vs. Specification vs. Guidance vs. Procedure conflicts | Specification.md REQ-015-05-03 (IFC > Spec) | CCDC 14-2013 contract hierarchy (not quoted in deliverable docs) | Specification.md §Requirements; Guidance.md §Principles (Principle 6) | PROPOSAL: Guidance Principle 6 establishes interim hierarchy referencing CCDC 14-2013 order of precedence; confirm with contract administrator. [Lensing: X-001] | TBD |
| CONF-015-05-04 | Warranty scope: REQ-015-05-08 warrants "all materials and workmanship" for 2 years, but Procedure Step 6.2 previously allowed "specific exclusions (if any)" without defining permissible exclusion categories | Specification.md REQ-015-05-08 ("All materials and workmanship") | Procedure.md Step 6.2 (previously: "Include specific exclusions (if any)") | Specification.md §Requirements REQ-015-05-08; Procedure.md §Steps Phase 6; Specification.md §Documentation | PROPOSAL: Specification governs; any warranty exclusions require pre-approval by Owner in writing. Procedure language updated to align. [Lensing: E-002] | TBD |
