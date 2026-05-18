# Specification — DEL-002-07 Crane Support Structure Details

---

## Scope

### What this deliverable covers

DEL-002-07 covers the structural design and drawing documentation for the crane runway support structure serving two (2) 5-tonne overhead cranes on trolley within the New North Shop addition at the West Dried Meat Lake Regional Landfill (SW 14–44–21–W4, Camrose County, Alberta).

This drawing set shall document:
- Crane runway beam framing, sizing, and arrangement
- Runway beam support system (columns, corbels, brackets, or wall mounts as determined by the structural engineer)
- Connection details at runway beam-to-support interfaces
- End stop and bumper arrangement
- Anchor bolt or embedded plate details at support structure
- Design load table (crane wheel loads, runway beam reactions)
- Applicable code references and design notes

This deliverable is part of the broader SOW-0012 final structural design scope.

Source: _CONTEXT.md; WDMLRL_Decomposition_Claude.md §7 PKG-002; RFP §3.4

### What this deliverable excludes

- Crane equipment procurement and selection (covered under SOW-0067 / PKG-016)
- Crane electrical power distribution (covered under DEL-004 / SOW-0059)
- Foundation design (covered under DEL-002-02, DEL-002-11)
- General building structural framing (covered under DEL-002-03, DEL-002-04)
- Mezzanine structure (covered under DEL-002-05)
- Service pit structure (covered under DEL-002-06)

---

## Requirements

### REQ-007-01 — Crane Quantity and Capacity
The crane support structure shall be designed to carry two (2) overhead cranes, each with a rated lifting capacity of 5 tonnes.

**Source:** RFP §3.4 ("2 – 5-tonne overhead cranes on a trolley"); App B (Shop) note list ("(2) 5 Ton Cranes")
**Verification:** Drawing set load table; structural calculations (DEL-002-10)

---

### REQ-007-02 — Structural Design to Governing Codes
The crane support structure shall be designed in accordance with all applicable Alberta building codes and regulations and all Alberta Safety Codes.

**Source:** RFP §3.3.2 ("building design must adhere to all applicable Alberta building codes and regulations"); RFP §3.3.2 ("proposed building must adhere to all Alberta Safety Codes")
**Note:** Specific code editions (NBC, Alberta Building Code, CSA standards) are not named in the RFP. ASSUMPTION: National Building Code of Canada (NBC), Alberta Building Code, CSA S16, and CSA A23.3 are applicable; editions to be confirmed by the Structural Engineer of Record.
**Verification:** Engineer stamp; design notes on drawings; structural calculations (DEL-002-10)

---

### REQ-007-03 — IFC Drawings Signed and Stamped by P.Eng.
All Issued for Construction drawings forming this drawing set shall be signed and stamped by a professional engineer licensed to practice in the province of Alberta.

**Source:** RFP §3.3.2 ("All Issued for Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta")
**Verification:** Presence of P.Eng. stamp and signature on each issued drawing sheet

---

### REQ-007-04 — Compatibility with Concrete Building Structure
The crane support structure shall be designed as an integral component of, or structurally compatible with, the concrete building structure (35' ceiling height).

**Source:** RFP §3.4 ("Concrete structure 35' ceiling"); App B (Shop) note list ("Concrete Structure (35' Ceiling)")
**Note:** ASSUMPTION — runway beam supports will take the form of corbels on concrete columns or dedicated crane columns; final configuration to be determined by Structural Engineer based on crane supplier data and column layout.
**Verification:** Consistency check between DEL-002-07 and DEL-002-03 Framing Plans; DEL-002-04 Structural Sections

---

### REQ-007-05 — Design Load Basis from Crane Supplier Data
Crane wheel loads and bridge end-truck geometry used in the structural design shall be obtained from the selected crane supplier's equipment data sheet.

**Source:** ASSUMPTION (standard structural engineering practice for crane runway design); crane supplier not identified in RFP or App B
**Note:** This requirement cannot be verified until crane supplier selection is complete (PKG-016). The drawing set shall include a load table noting the governing crane wheel loads.
**Note [A-004]:** If design proceeds with assumed conservative loads prior to receipt of crane supplier data (see Procedure Step 1.4, Guidance Trade-offs), acceptance criteria for the assumed-loads fallback path must be defined: (a) what constitutes "sufficiently conservative" (e.g., percentage margin above expected loads), and (b) a mandatory re-verification gate requiring confirmation against actual crane supplier loads before IFC issuance. Proposed authority: Structural Engineer (PROPOSAL).
**Verification:** Load table present on drawings; loads traceable to crane supplier data sheet; structural calculations (DEL-002-10)

---

### REQ-007-06 — Runway Alignment and Deflection Limits
The crane runway beams and their supports shall be designed to maintain runway alignment within tolerances acceptable to the crane manufacturer and governing standards.

**Source:** ASSUMPTION — CMAA Spec 70 or equivalent likely applicable; specific tolerance values not stated in RFP or App B
**Note:** Deflection limits and alignment tolerances to be confirmed by Structural Engineer in accordance with applicable crane standard and crane manufacturer requirements.
**TBD [A-002]:** Specific deflection limit values (vertical and lateral) for crane runway beams must be obtained from the governing standard (CMAA Spec 70) and confirmed with the crane manufacturer. This is a necessary design input; numeric limits cannot be assumed. Proposed authority: Crane manufacturer + CMAA Spec 70 (PROPOSAL).
**Verification:** Deflection limits stated on drawings or in design notes; structural calculations (DEL-002-10)

---

### REQ-007-07 — End Stops
The runway shall be equipped with end stops at each end of each runway rail to prevent crane bridge from traveling beyond the end of the runway.

**Source:** ASSUMPTION (standard requirement for overhead crane runways; not explicitly stated in RFP or App B)
**Verification:** End stop details shown on drawings

---

### REQ-007-08 — Coordination with Electrical Power Supply
The crane support structure drawings shall identify conductor bar or festoon system entry/routing requirements for coordination with the electrical design (crane power per SOW-0059 / DEL-004).

**Source:** SOW-0059 ("Provide power for two 5-tonne overhead cranes"); ASSUMPTION that coordination note is required on structural drawings
**Verification:** Electrical coordination note or detail present on drawings

---

### REQ-007-10 — Hook Height and Ceiling Clearance Verification
The crane support structure design shall verify that the 35' ceiling height provides adequate clearance to accommodate the crane at full lift plus the structural depth of the runway beam system (beam, rail, and mounting hardware). The minimum required hook height shall be obtained from the crane supplier data sheet.

**Source [B-003]:** Guidance Principle 3 (runway elevation constrained by 35' ceiling and crane hook height); Procedure Step 2.5 (clearance check); RFP §3.4 (35' ceiling stated)
**Note:** This requirement closes a gap where Guidance and Procedure both reference the hook height/ceiling clearance check but no formal Specification requirement existed to anchor it.
**Verification:** Clearance calculation in structural calculations (DEL-002-10); hook height dimension stated on IFC drawings

---

### REQ-007-11 — Seismic Design Considerations
The crane support structure shall be designed for seismic forces in accordance with the National Building Code of Canada, accounting for the elevated mass of the crane bridge, trolley, and rated load. Seismic anchorage design for crane runway beam supports and connections shall be explicitly addressed.

**Source [F-001]:** NBC requires seismic design for building structures; Procedure Step 2.1 references seismic in load combinations; ASSUMPTION that crane support structure as a distinct elevated-mass subsystem requires explicit seismic design consideration
**Note:** The crane + bridge + rated load represents significant elevated mass. Seismic design of the crane support structure may govern anchorage and connection design beyond gravity and crane operational loads.
**Verification:** Seismic load combinations included in structural calculations (DEL-002-10); seismic design notes on IFC drawings

---

### REQ-007-12 — Design Capacity Margin Documentation
The structural design documentation shall state the maximum crane capacity that the as-built runway beam and support structure can support, documenting the design margin beyond the 5-tonne rated load.

**Source [E-002]:** ASSUMPTION — no explicit RFP or source requirement; included as prudent implementation practice to inform future Owner decisions regarding crane upgrades without requiring structural redesign investigation
**Note:** This requirement enables future facility planning. Knowing the actual structural capacity reserve of the runway system has no cost impact on the design documentation.
**Verification:** Maximum supportable crane capacity stated in structural calculations (DEL-002-10) or on IFC drawing design notes

---

### REQ-007-09 — Preliminary Design County Approval
The preliminary structural design (including conceptual crane support approach) shall be submitted to Camrose County for approval before proceeding to final IFC design.

**Source:** RFP §3.3.2 ("Deliver Preliminary Design for the County project team to approve"); SOW-0010b
**Note:** DEL-002-01 (Preliminary Structural Design) covers the preliminary design deliverable. This requirement governs the sequencing of DEL-002-07 production.
**Verification:** Evidence of County approval of preliminary design before IFC drawing set is finalized

---

## Standards

| Standard | Role | Accessibility |
|---|---|---|
| National Building Code of Canada (NBC) — current edition | Governing building code; structural loads (dead, live, snow, wind, seismic) | ASSUMPTION: applicable; location TBD |
| Alberta Building Code — current edition | Provincial amendment layer to NBC | ASSUMPTION: applicable; location TBD |
| CSA S16 — Design of Steel Structures | Runway beam design if steel beams are used; connections | ASSUMPTION: likely applicable; location TBD |
| CSA A23.3 — Design of Concrete Structures | Corbel/column design at crane support points | ASSUMPTION: likely applicable; location TBD |
| CMAA Specification No. 70 — Top-Running Bridge & Gantry Type Multiple Girder Cranes | Crane service class, wheel loads, runway alignment tolerances. **TBD [A-003]:** CMAA crane service class for the two 5-tonne cranes must be confirmed by crane supplier / PKG-016 to determine fatigue classification and design load factors. | ASSUMPTION: likely applicable; location TBD |
| CMAA Specification No. 74 — Top-Running & Under-Running Single Girder Cranes | If single-girder crane configuration is selected | ASSUMPTION: conditional; location TBD |
| Alberta Safety Codes Act and applicable Safety Code | Governs inspections and permits | RFP §3.3.2 (stated requirement) |

**Note:** No specific standard edition numbers are cited in the RFP or Appendix B. The Structural Engineer of Record is responsible for confirming applicable editions at time of design. **[A-001]** This is a material gap: different editions of NBC, CSA S16, and CSA A23.3 could yield materially different design requirements (e.g., seismic force levels, connection capacity provisions). The specific edition year for each governing standard must be confirmed and documented on the IFC drawings before final design proceeds. Proposed authority: Structural Engineer of Record (PROPOSAL).

---

## Verification

| Requirement | Verification Method | Responsible Party |
|---|---|---|
| REQ-007-01 — Crane quantity and capacity | Load table on drawing set; structural calculations | Structural Engineer |
| REQ-007-02 — Code compliance | P.Eng. design certification; Alberta Safety Code inspection | Structural Engineer; Authority Having Jurisdiction |
| REQ-007-03 — P.Eng. stamp | Visual inspection of issued drawings | Project Manager / Owner's Representative |
| REQ-007-04 — Concrete structure compatibility | Cross-check DEL-002-07 vs DEL-002-03 and DEL-002-04 | Structural Engineer; Design Coordinator |
| REQ-007-05 — Crane supplier load basis | Load table traceable to crane supplier data sheet | Structural Engineer |
| REQ-007-06 — Runway alignment and deflection | Deflection limits stated in design notes; calculations | Structural Engineer |
| REQ-007-07 — End stops | End stop details present on drawings | Structural Engineer |
| REQ-007-08 — Electrical coordination | Coordination note/detail on drawings | Structural Engineer; Electrical Engineer |
| REQ-007-09 — County preliminary approval | Approval record (meeting minutes or written confirmation) | Project Manager |
| REQ-007-10 — Hook height / ceiling clearance | Clearance calculation in DEL-002-10; hook height on IFC drawings | Structural Engineer |
| REQ-007-11 — Seismic design | Seismic load combinations in DEL-002-10; seismic notes on IFC drawings | Structural Engineer |
| REQ-007-12 — Design capacity margin | Maximum supportable capacity stated in DEL-002-10 or on drawings | Structural Engineer |
| REQ-007-06 — Field verification (construction phase) | Post-installation runway alignment survey and rail straightness measurement **[D-002]** | Structural Engineer / Crane installer |

**Note [D-001]:** The verification table assigns most checks to the "Structural Engineer" who is also the designer. For a safety-critical structural subsystem, the conformance acceptance authority should be clarified: whether the Structural Engineer of Record self-certifies, or whether an independent third-party structural review is required. Proposed authority for ruling: Project Manager / Owner's Representative (PROPOSAL). TBD.

**Note [E-003]:** Multiple verification rows reference "structural calculations (DEL-002-10)" as the verification method. It should be clarified whether DEL-002-10 is a single calculation package covering all of PKG-002 structural scope, or whether crane support structure calculations form a dedicated, independently reviewable section within that package. If crane support calculations are embedded in a larger package without clear section boundaries, independent review of the crane support design becomes harder. See Conflict Table in Guidance.md (CONF-007-03).

---

## Documentation

### Required Artifacts (Drawing Set — Anticipated)

The following drawing sheets are anticipated as the output of this deliverable. Final sheet list to be confirmed by Structural Engineer.

| Sheet (Anticipated) | Content | Source |
|---|---|---|
| Crane Runway Framing Plan | Plan view of runway beam layout, column/support locations, bay widths, runway lengths | ASSUMPTION (standard content) |
| Runway Beam Sections | Beam size, material, section properties; bearing details | ASSUMPTION |
| Support Structure Details | Column/corbel details or bracket details; anchor bolts or embedded plates | ASSUMPTION |
| Connection Details | Beam-to-support connections; splice details if required | ASSUMPTION |
| End Stop / Bumper Details | End stop configuration at runway terminations | ASSUMPTION |
| Design Notes and Load Table | Governing loads, code references, material specifications, deflection limits | ASSUMPTION |

### Related Deliverables

| Deliverable | Relationship |
|---|---|
| DEL-002-01 — Preliminary Structural Design | Upstream: crane support approach established in preliminary design |
| DEL-002-03 — Structural Framing Plans | Coordinate: column locations and building framing |
| DEL-002-04 — Structural Sections & Details | Coordinate: building section context |
| DEL-002-10 — Structural Calculation Package | Supporting: calculations must cover crane support structure |
| DEL-004 — Electrical Design | Coordinate: crane power (SOW-0059) |
| PKG-016 — Crane & Lifting Equipment | Upstream: crane supplier data sheet required for design loads |
