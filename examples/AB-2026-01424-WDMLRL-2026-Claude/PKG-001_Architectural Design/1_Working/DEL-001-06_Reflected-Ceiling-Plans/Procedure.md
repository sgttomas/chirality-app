# Procedure — DEL-001-06 Reflected Ceiling Plans

---

## Purpose

This procedure describes the steps required to produce the Reflected Ceiling Plan (RCP) drawing set for DEL-001-06, from initiation through IFC (Issued For Construction) issue. The RCP drawings are part of the final architectural design (SOW-0011) and must be fully coordinated with structural, mechanical, and electrical discipline drawings.

*Source: OBJ-003; RFP §3.3.2*

---

## Prerequisites

### Required Inputs (upstream)

| Input | Source / Deliverable | Status |
|---|---|---|
| Approved Preliminary Architectural Design | DEL-001-01 (Preliminary Architectural Design) | Must be approved by County before IFC proceeds — OBJ-003 |
| Architectural Floor Plans (draft or IFC) | DEL-001-02 (Architectural Floor Plans) | RCP is produced in parallel and must match floor plan room layout exactly |
| Building Sections | DEL-001-04 (Building Sections) | Required to confirm ceiling heights in sections; 35' main shop height to be confirmed |
| Structural drawing set (ceiling/crane/mezzanine) | DEL-002 series (Structural Design package) | Required to confirm crane rail positions, mezzanine framing, and concrete ceiling configuration before RCP is finalized |
| Electrical lighting layout | DEL-004 series (Electrical Design package) | Required to confirm fixture counts, types, locations, and circuit layout before RCP finalized |
| Mechanical unit layout | DEL-003 series (Mechanical Design package) | Required to confirm forced air makeup unit locations, exhaust fan locations, and ventilation penetrations |
| Geotechnical report | Proponent-obtained | Required before final structural design; affects foundation but not directly RCP — noted for project schedule awareness |

### Required References

| Reference | Document |
|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf — §3.1, §3.4 Design Requirements |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf — Conceptual floor plan with ceiling notes |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf — Conceptual lighting and electrical layout |
| — | Applicable Alberta Safety Codes (building, electrical, fire) — location TBD |
| — | National Building Code of Canada (Alberta edition) — location TBD |

### Required Tools / Resources

- Architectural CAD/BIM software (platform and version TBD — must be confirmed by project team before RCP production begins; record confirmed platform in project log once decided. *(Enriched per C-003 — this is a critical execution precondition.)* — ASSUMPTION)
- Coordination set (all discipline drawing files accessible for overlay/comparison)
- Project drawing standards / title block template (TBD)

---

## Steps

### Phase A — Initiation and Base Plan Setup

**A-01. Obtain confirmed floor plan base.**
Source the confirmed architectural floor plan (DEL-001-02) as the base file for RCP production. The RCP must match the floor plan room layout, room names, and dimensions exactly. Do not proceed on a preliminary floor plan that has not been reviewed by the full design team. Confirm the floor plan file is the current approved version before using as RCP base; record the file version/date in the project log.

*Source: OBJ-003; standard RCP production practice*
*Note: Enriched per D-002 — original step did not specify version confirmation or version recording.*

**A-02. Identify all spaces requiring RCP coverage.**
Using RFP §3.1, §3.4, and App B (Shop), confirm the full list of spaces to be covered:
- New addition: Main Shop (two bays), Wash Bay, Service Pit/Pit, Parts Room, Utility Room, Office, Washroom, Overhead Mezzanine level
- Old North Shop renovation: Washroom below mezzanine, new Locker/Change Room, 2nd-level Mezzanine/Coffee Room

Record any spaces not covered and document the reason.

*Source: RFP §3.1, §3.4; App B (Shop)*

**A-03. Field-verify Old North Shop existing ceiling conditions.**
Before completing RCPs for renovation areas, conduct a field survey of the Old North Shop to record existing ceiling conditions. Minimum data to be captured during field verification:
- Existing ceiling heights (per room/area)
- Structural type and condition of existing ceiling
- Existing ceiling-mounted elements (lights, fans, ducts, etc.) and their approximate locations
- Condition photographs of ceiling areas to be renovated

Recording format: TBD per project standards (field report template or marked-up plan). Responsible party: architect or designated field survey team member.

*Source: App B (Shop) legend; RFP §3.1 ("Some renovations are to be completed in the existing maintenance shop")*
*Note: Enriched per A-004 — original step did not specify minimum data points, format, or responsible party.*

**A-04. Establish ceiling height matrix.**
Compile a ceiling height schedule for all spaces. Confirmed values:
- Main Shop: 35 feet (RFP §3.4)
- All other spaces: TBD from architectural/structural design

Record TBD values; do not assume. Resolve with structural engineer before IFC.

*Source: RFP §3.4*

### Phase B — Interdisciplinary Coordination

**B-01. Obtain structural ceiling inputs.**
Request from the structural engineer (DEL-002):
- Crane rail/beam layout: centerlines, structural depth, and bottom-of-rail elevation for both 5-tonne cranes
- Mezzanine framing layout and soffit elevation above main floor
- Concrete ceiling structure configuration (flat slab, beam-and-slab, etc.)
- Any structural penetrations or features at the ceiling plane

*Source: RFP §3.4; App B (Shop)*

**B-02. Obtain electrical ceiling inputs.**
Request from the electrical engineer (DEL-004):
- Final lighting layout confirming fixture type, quantity, and location for all spaces
- Exhaust fan ("E") locations at ceiling
- Overhead door operator mounting locations
- Security camera mounting locations
- Any changes from the conceptual App B (Electrical) layout

*Source: App B (Electrical); RFP §3.4*

**B-03. Obtain mechanical ceiling inputs.**
Request from the mechanical engineer (DEL-003):
- Forced air makeup unit locations and mounting dimensions
- All exhaust fan locations (welding station, repair bay hose drops, general ventilation)
- Any mechanical ductwork or equipment requiring ceiling penetrations or ceiling-level clearance

*Source: RFP §3.4 ("High recovery heating system," "High volume air exchanger," "Exhaust hoses and fans")*

**B-04. Resolve coordination conflicts.**
Overlay all ceiling-level inputs. Identify and resolve conflicts (e.g., crane rail vs. lighting fixture interference; mechanical unit vs. crane travel clearance). Document all resolved conflicts in the project coordination log. Flag unresolved conflicts for design team review. If unresolved conflicts cannot be resolved at the design team level, escalate per the escalation path described in Guidance C-07.

*Source: OBJ-003; RFP §3.3.2*

**B-05. Coordination gate — go/no-go for drawing production. *(added per F-003)***
Before proceeding to Phase C (RCP Drawing Production), obtain documented confirmation from all three disciplines (structural, mechanical, electrical) that their ceiling-level inputs are complete and coordination conflicts are resolved or formally deferred. Evidence: signed coordination log entry or email confirmation from each discipline lead. Do not proceed to Phase C without this gate.

*Source: OBJ-003; RFP §3.3.2 (coordination obligation); _SEMANTIC_LENSING F-003*
*ASSUMPTION: Formal gate is standard practice for coordination-intensive deliverables; format of confirmation TBD.*

### Phase C — RCP Drawing Production

**C-01. Set up drawing sheets.**
Create RCP drawing sheets using the project title block template. Establish sheet numbering per project drawing index. Recommended sheet breakdown (ASSUMPTION):
- Sheet RCP-01: Main Shop — full-height area (130' × 100' plan at 1:100)
- Sheet RCP-02: Ancillary rooms — Parts Room, Utility Room, Office, Washroom, Mezzanine level (at 1:50 or as required)
- Sheet RCP-03: Old North Shop renovation areas (at 1:50 or as required)

Adjust sheet breakdown as required by drawing size and legibility.

**C-02. Draw ceiling planes and heights.**
For each space, draw the reflected ceiling plane. Annotate ceiling height(s) with leader notes or spot elevations. Use distinct linework to differentiate:
- Structural ceiling (concrete) at 35'
- Mezzanine soffit (lower plane over Parts Room/Utility Room/Wash Bay) at TBD elevation
- Lower ancillary room ceilings (office, washroom, locker room) at TBD elevation

**C-03. Place ceiling-mounted elements.**
Insert and locate all ceiling-mounted elements in their confirmed positions:
- Light fixtures (high bay, 8' LED) per confirmed electrical layout
- Ceiling fans (6 units in main shop) per confirmed electrical layout
- Exhaust fans per confirmed mechanical/electrical layout
- Forced air makeup units per confirmed mechanical layout
- Crane rail centerlines (dashed or distinct symbol) with elevation annotation
- Exhaust hose drop points in repair bays
- Overhead door headers at all door openings
- Rough-in locations for security cameras (coordinate with electrical)

**C-04. Apply legend and symbols.**
Create or reference project drawing legend identifying all symbols used on the RCP. Symbols shall be consistent with electrical drawing legend where applicable (e.g., exhaust fan "E" symbol).

**C-05. Add cross-reference callouts.**
Add cross-reference callouts linking the RCP to:
- Electrical drawings (DEL-004) for each fixture type
- Structural drawings (DEL-002) for crane rail and mezzanine details
- Mechanical drawings (DEL-003) for mechanical unit and exhaust details
- Building Sections (DEL-001-04) for ceiling height confirmation

**C-06. Complete notes and general notes block.**
Add general notes to the RCP sheet including:
- "All ceiling heights to be confirmed with structural engineer"
- "Refer to electrical drawings for fixture wiring and circuit information"
- "Refer to mechanical drawings for equipment schedules"
- "Contractor to field verify existing ceiling conditions in renovation areas before commencement of work"
- "All construction to comply with applicable Alberta Safety Codes"

### Phase D — QA and Review

**D-01. Internal QA review.**
Architect to perform internal check:
- Confirm all spaces from the space list (A-02) have RCP coverage
- Confirm 35' annotation shown in main shop
- Confirm lighting fixture counts match App B (Electrical) minimums and confirmed electrical layout
- Confirm 6 ceiling fans shown in main shop
- Confirm exhaust fans shown at welding station and repair bay locations
- Confirm crane rail positions shown and annotated
- Confirm mezzanine soffit shown and annotated
- Confirm overhead door headers shown
- Confirm service pit/trench annotated with lighting and ventilation
- Confirm all symbols present in legend
- Confirm cross-references to discipline drawings are complete and correct

**D-02. Interdisciplinary coordination check.**
Distribute draft RCP to structural, mechanical, and electrical engineers for review and sign-off that the RCP is consistent with their respective discipline drawings. Resolve any noted conflicts before proceeding to IFC.

**D-03. Preliminary Design Review by County (if at preliminary stage).**
If RCPs are being issued as part of the preliminary design package (SOW-0010a), submit for County approval per OBJ-003. Incorporate County feedback before proceeding to IFC.

*Source: OBJ-003; RFP §3.3.2*

**D-04. Capture lessons learned. *(added per E-003)***
After completion of the RCP coordination and production process, record lessons learned including: coordination challenges encountered, conflict resolution outcomes, process improvements identified, and any recommendations for subsequent deliverable production within the project. Retain in project file.

*Source: Standard project practice; _SEMANTIC_LENSING E-003*
*ASSUMPTION: Lessons-learned capture is standard practice for coordination-intensive deliverables.*

---

## Verification

| Check | Method | Pass Condition |
|---|---|---|
| All spaces covered | Review sheet index against space list | Every space from the space list has RCP coverage |
| 35' ceiling annotated | Visual check of main shop RCP | "35'-0"" or "10,668" (mm) annotation present in main shop |
| Lighting consistent with electrical | Compare RCP fixture count/layout to DEL-004 | Zero discrepancies between RCP and electrical lighting plan |
| Ceiling fans shown | Count fan symbols on main shop RCP | 6 ceiling fans shown |
| Exhaust fans shown | Check welding station and repair bay areas | At minimum: welding station exhaust fan shown; repair bay exhaust drops shown |
| Crane rails shown (2 × 5-tonne) | Visual check of main shop RCP | Two crane rail centerlines shown with elevation annotations |
| Mezzanine soffit shown | Visual check of RCP at parts/utility/wash bay area | Mezzanine soffit boundary drawn and soffit height annotated (or TBD with note) |
| Overhead door headers shown | Check all overhead door locations | Headers shown at all overhead door openings |
| P.Eng. stamp present on IFC set | Check title block / stamp area of all sheets. P.Eng. stamp must be obtained at the IFC issue milestone; IFC distribution shall not proceed without stamp confirmation. *(Enriched per A-002 — original check did not specify timing or gating.)* | Stamp and signature of Alberta-licensed P.Eng. on each sheet; stamp obtained before IFC distribution |
| No conflicts with discipline drawings | Interdisciplinary review sign-off records | Written confirmation from structural, mechanical, electrical engineers |
| Code compliance | Design review against applicable Alberta Safety Codes | No identified non-compliances at IFC issue |

---

## Records

| Record | Description | Retained By | Retention Period |
|---|---|---|---|
| IFC RCP Drawing Set | Final issued-for-construction reflected ceiling plan sheets, stamped by P.Eng. | Project file / submitted to County | TBD per project-level record retention policy |
| Preliminary RCP submission | RCPs submitted as part of preliminary design package for County approval | Project file | TBD per project-level record retention policy |
| Coordination log | Record of interdisciplinary coordination issues and resolutions related to ceiling plane | Project file | TBD per project-level record retention policy |
| Field verification notes | Notes from Old North Shop existing ceiling condition survey (including ceiling heights, structural type, existing elements, condition photos per Step A-03) | Project file | TBD per project-level record retention policy |
| Discipline review sign-off | Written confirmation from structural, mechanical, electrical engineers that RCP is consistent with their drawings | Project file | TBD per project-level record retention policy |
| Redline / markup records | Any red-line markups from County or discipline reviews, and the architect's response. Redline tracking and formal response documentation should follow a structured process: track each markup, record the response action, and confirm resolution before IFC issue. *(Enriched per X-004)* | Project file | TBD per project-level record retention policy |
| Coordination gate confirmation | Signed coordination log entries or email confirmations from discipline leads confirming readiness to proceed from Phase B to Phase C *(added per F-003)* | Project file | TBD per project-level record retention policy |
| Lessons learned | Record of lessons learned from the RCP coordination and production process, to improve subsequent deliverable production within the project *(added per E-003)* | Project file | TBD per project-level record retention policy |

*Note (A-005): Record retention periods are TBD; reference project-level record retention policy once established. All records listed above should be retained for at least the duration specified by the governing retention policy.*
