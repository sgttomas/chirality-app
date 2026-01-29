# Datasheet: DEL-05.01 Concrete Structures Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-05.01 |
| Name | Concrete Structures Design Drawing Set |
| Package | PKG-05 Concrete Structures |
| Discipline | Structural |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Drawing Number | To be issued per project document control / numbering system (**TBD**) |
| Sheet Size | Per project drawing standard (**TBD**) |
| Scale | Appropriate to features; match governing plan coordinate system (**TBD**) |
| CAD Standard | Project CAD standards / layering / symbology (**TBD**) |
| Revision | 00 (initial) — **ASSUMPTION** pending project revision scheme |
| Classification | Structural – Concrete Structures |
| Issue Format | PDF and native CAD files per project document control (**TBD**) |

## Conditions

**Context & constraints:**
- Deliverable defines the **design arrangement and details for concrete structures** per Employer's Requirements. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232.)
- Package scope includes **foundations, containment walls, equipment pads, thrust blocks, and ground liner system**. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226.)
- The decomposition covers the Contractor's scope only; Employer-responsible items are excluded except for interface connections. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49.)
- PKG-05 deliverables support **OBJ-3 Storage Capacity (45,000 MT)** and **OBJ-7 Environmental Protection** at a project level. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:782; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786.)
- Project location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:10.)
- Contract type: Design & Build. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:44.)

**Design basis items to be confirmed (TBD until sourced from ERs / design basis):**
- Design loads (dead/live/equipment/thermal/storage), settlement criteria, and serviceability limits.
- Seismic design parameters (seismic zone, site class, importance factors, R values).
- Environmental exposure classes (e.g., freeze-thaw, de-icing salts, sulfates, chlorides) and durability requirements.
- Concrete material properties (compressive strength, exposure class, cover requirements, air entrainment).
- Any hazardous area-related structural drawing requirements (only applicable if concrete elements interface with classified areas) — **TBD**.
- Bearing capacity and settlement tolerances from geotechnical investigation.

## Construction

**Intended drawing content (anticipated artifacts):**

1. **Foundation plans** (layout, dimensions, elevations, pile/footing details if applicable):
   - Tank foundation layouts (3 × 15,000 MT tanks)
   - Equipment pad foundation layouts (pumps, metering, railcar unloading equipment)
   - Building/control room foundation interfaces (**TBD** extent within PKG-05 scope)
   - Thrust block locations and sizing for underground piping
   - (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226.)

2. **Containment wall plans/sections** (waterstops/joints details where applicable):
   - Tank farm secondary containment walls (support OBJ-3 and OBJ-7)
   - Containment wall joint details (construction joints, control joints, expansion joints)
   - Waterstop details and penetration sealing
   - Ground liner system interface details (coordination with liner installation)
   - (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786.)

3. **Equipment pad details** (bearing, anchorage interfaces, grout pads):
   - Anchor bolt layouts and embedment details (interface with equipment vendor GAs — **TBD**)
   - Grout pocket/shim details
   - Equipment mounting elevation control
   - Vibration isolation requirements if applicable (**TBD**)
   - (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232.)

4. **Reinforcement drawings** (rebar schedules, bar marks, laps/couplers, clear cover notes):
   - Reinforcement plans for foundations, containment walls, and equipment pads
   - Bar bending schedules with bar marks
   - Lap splice and coupler specifications
   - Clear cover requirements by exposure zone
   - Reinforcement congestion details and pour sequence notes
   - (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232.)

**Typical details (ASSUMPTION — subject to project drafting standards):**
- Standard foundation details (footings, pile caps)
- Standard joint details (construction joints, control joints, expansion joints)
- Standard embedment details (anchor bolts, sleeves, blockouts)
- Standard reinforcement details (bar laps, couplers, corner reinforcement)

## References

- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232 — DEL-05.01 description and anticipated artifacts.
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226 — PKG-05 scope (foundation/containment/pads/thrust blocks/liner).
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49 — scope focus / contractor-only scope boundary.
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:782 and :786 — objective mappings (OBJ-3 Storage Capacity 45,000 MT, OBJ-7 Environmental Protection).
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:10 — project location.
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:44 — contract type (Design & Build).
- test/Volume_2_Part_2_Employers_Requirements.pdf — concrete requirements (section exists; clause locations TBD).
- execution/PKG-05_Concrete_Structures/0_References/_REFERENCE_INDEX.md — available baseline references for PKG-05.
- Specification.md — requirements for content, quality, and document control expectations for this drawing set.
- Guidance.md — rationale and considerations that guide what is emphasized in the drawings.
- Procedure.md — production and verification workflow used before issuing the drawing set.

## Cross-Document Points

- **Specification → Requirements:** Each drawing artifact listed in Construction must be explicitly required and verifiable in `Specification.md` (Scope/Requirements/Documentation sections).
- **Specification → Standards:** Design codes and concrete exposure classes referenced here must align with Standards section in `Specification.md`.
- **Procedure → Verification:** `Procedure.md` defines the checks that demonstrate the drawing set implements the `Specification.md` requirements (including QA/QC and IDC steps in Steps 6-7).
- **Guidance → Environmental/Containment Intent:** Environmental protection and containment intent (OBJ-7) must be expressed via clear detailing and notes consistent with Principles and Considerations in `Guidance.md`.
- **Guidance → Interface Coordination:** Interface requirements and hold points noted in Construction must be addressed in Considerations section of `Guidance.md` and Prerequisites in `Procedure.md`.
