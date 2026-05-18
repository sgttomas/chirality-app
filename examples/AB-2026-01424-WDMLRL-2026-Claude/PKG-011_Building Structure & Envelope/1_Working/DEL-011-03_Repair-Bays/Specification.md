# Specification — DEL-011-03 Drive-Through Repair Bays

**Document Type:** Specification (Normative)
**Deliverable ID:** DEL-011-03
**Deliverable Name:** Drive-Through Repair Bays
**Package:** PKG-011 — Building Structure & Envelope
**Revision:** R1 — 2026-02-26 (Pass 3 enrichment)
**Status:** SEMANTIC_READY

---

## Scope

### What This Deliverable Covers

DEL-011-03 covers the construction of two drive-through repair bays within the New North Shop addition at the West Dried Meat Lake Regional Landfill site. Scope includes:

- Structural bay enclosure elements (walls, roof integration) as part of the concrete superstructure, consistent with DEL-011-01 (Superstructure)
- Overhead door frames, sills, and structural rough openings for bay entrance and exit doors (one pair per bay -- drive-through configuration)
- Overhead door units, tracks, hardware, safety devices, and weather seals
- Electrical power rough-in connections for overhead door operators (in coordination with PKG-015)
- Coordination interfaces with DEL-011-02 (Steel Plate Floor Embedments), PKG-013 (exhaust provisions), PKG-014 (sump drain rough-in), and PKG-015 (door operator power)

**Source:** RFP S3.1; SOW-0025; Appendix B (Shop); Decomposition PKG-011 deliverable table.

### What This Deliverable Excludes

| Excluded Item | Where It Is Handled |
|---|---|
| Concrete superstructure (columns, beams, roof) | DEL-011-01 Superstructure |
| Steel plate floor embedments | DEL-011-02 Steel Plate Floor Embedments |
| Sump drain installation in repair bays | DEL-014-04 Floor Drains & Sump Drains (PKG-014) |
| Exhaust hose and fan supply/installation | DEL-013-04 Heavy Equipment Exhaust System (PKG-013) |
| Three-phase power service and overhead door electrical circuits | DEL-015-04 Equipment Power Circuits (PKG-015) |
| Overhead crane installation | DEL-016-01 Two 5-Tonne Overhead Cranes (PKG-016) |
| Wash bay enclosure (separate enclosed bay) | DEL-011-05 Wash Bay Enclosure |
| Entrance/exit doors for the addition (personnel/vehicle entry separate from repair bay doors) | DEL-011-04 Entrance/Exit Doors |
| Parts storage room, utility room, office | PKG-012 Interior Construction & Fit-Out |

---

## Requirements

### REQ-011-03-001 — Quantity
**Shall:** Construct two (2) drive-through repair bays.
**Source:** RFP S3.1 ("two drive-through bays"); SOW-0025; Appendix B (Shop).

### REQ-011-03-002 — Bay Width
**Shall:** Each repair bay shall be nominally 24 feet wide.
**Source:** Appendix B (Shop) -- plan dimension annotation.
**Note:** The 24-foot dimension is taken from the conceptual floor plan (Appendix B). Whether this represents nominal structural bay width, centerline-to-centerline, or clear opening width is TBD pending IFC drawings. Final clear opening dimensions shall be confirmed in IFC architectural/structural drawings (DEL-001-02, DEL-002-03). IFC drawings should explicitly define nominal versus clear bay width to resolve this ambiguity (see Datasheet Normalization Note). (Lensing B-002)

### REQ-011-03-003 — Drive-Through Configuration
**Shall:** Each bay shall have a door at both the entrance and exit ends, providing a drive-through path for vehicles.
**Source:** RFP S3.1 ("separate entrance/exit doors"); SOW-0025 ("drive-through repair bays"); Appendix B (Shop).

### REQ-011-03-004 — Overhead Doors
**Shall:** Each bay entrance and exit shall be served by an overhead door.
**Source:** SOW-0025 ("overhead doors"); RFP S3.1.
**Note:** Door type (sectional, rolling steel, etc.), finished opening dimensions, and hardware specifications are TBD in IFC drawings. ASSUMPTION: industrial sectional overhead doors consistent with heavy equipment operation. Construction tolerances for door rough openings (plumb, square, dimensional tolerance) shall be per manufacturer's published installation requirements and IFC drawings; tolerances are TBD pending manufacturer selection and IFC issuance. (Lensing A-004)

### REQ-011-03-005 — Equipment Accommodation
**Shall:** Bay dimensions (width, height, door opening) shall accommodate large heavy construction equipment of at minimum motor scraper class.
**Source:** RFP S3.3.2 ("large construction equipment, such as a motor scraper"); RFP S3.4 (context of steel plates for tracked/packer equipment).
**Note:** Specific vehicle envelope dimensions (height, width, length, turning radius) to be confirmed by Structural Engineer in IFC drawings using County fleet data; motor scraper clearance envelope is TBD. ASSUMPTION: minimum door opening height of 14-16 feet likely needed for motor scraper class with raised attachments; confirm with actual equipment dimensions. (Lensing A-001, F-001)

### REQ-011-03-006 — Structural System
**Shall:** Repair bays shall be constructed as part of the concrete superstructure with a minimum clear interior ceiling height of 35 feet.
**Source:** RFP S3.4 ("Concrete structure 35' ceiling"); Appendix B (Shop).

### REQ-011-03-007 — Sump Drain Provisions
**Shall:** Structural rough-in (floor slope or sump pit framing as required) shall accommodate sump drains in each repair bay. Floor drainage slope shall be TBD by civil/structural engineer; acceptance criteria for slope (percentage, direction, and ponding test requirements) shall be defined in IFC drawings.
**Source:** RFP S3.4 ("Sump drains in the repair bays"); SOW-0045. Drain installation is DEL-014-04 scope; structural accommodation is this deliverable's responsibility.
**Note:** Measurable acceptance criteria for floor drainage slope are TBD pending civil/structural engineer specification. Verification must confirm slope direction and percentage to a defined standard rather than subjective assessment. (Lensing D-001)

### REQ-011-03-008 — Exhaust System Provisions
**Shall:** Structural and envelope provisions (penetrations, blocking, supports as required) shall accommodate exhaust hoses and fan installations for heavy equipment in the repair bays.
**Source:** RFP S3.4 ("Exhaust hoses and fans for heavy equipment"); SOW-0038. Equipment supply/installation is DEL-013-04 scope.
**Note:** A defined coordination hold point between DEL-011-03 structural provisions and DEL-013-04 mechanical installation is required to confirm provisions are correctly located before mechanical rough-in begins. (Lensing X-002)

### REQ-011-03-009 — Overhead Door Power Provisions
**Shall:** Structural rough-in shall allow for overhead door operator power supply coordination with PKG-015 (SOW-0060).
**Source:** SOW-0060; Decomposition PKG-015 scope.

### REQ-011-03-010 — IFC Drawings
**Shall:** All construction shall be executed in accordance with Issued for Construction (IFC) drawings signed and stamped by a Professional Engineer licensed in the Province of Alberta.
**Source:** RFP S3.3.2.

### REQ-011-03-011 — Code Compliance
**Shall:** All construction shall comply with applicable Alberta building codes, regulations, and Alberta Safety Codes.
**Source:** RFP S3.3.2; RFP S3.4.
**Note:** Specific Alberta Building Code edition and relevant clause numbers applicable to this scope are TBD pending permit documentation. The code edition governing this project must be identified from the development permit and/or building permit to enable compliance determination. (Lensing A-003)

### REQ-011-03-012 — Inspection Coordination
**Shall:** All required inspections shall be requested; the County project representative shall be present at all inspections and provided copies of all completed inspection reports.
**Source:** RFP S3.3.2.

### REQ-011-03-013 — Completion Deadline
**Shall:** All work forming part of this deliverable shall be complete on or before December 31, 2026.
**Source:** RFP S3.1 (bold project completion statement); SOW-0091.

### REQ-011-03-014 — Upstream Dependencies
**Shall:** Construction of repair bay structural elements shall not proceed until the concrete superstructure (DEL-011-01) and steel plate floor embedments (DEL-011-02) are sufficiently advanced to permit bay enclosure work.
**Source:** _DEPENDENCIES.md (declared upstream: DEL-011-01, DEL-011-02).

### REQ-011-03-015 — Overhead Door Safety Devices
**Shall:** Each motorised overhead door shall be equipped with safety devices including obstruction sensors and auto-reverse mechanism.
**Source:** ASSUMPTION: required for motorised industrial doors per Alberta Safety Codes and applicable door manufacturer standards; specific standard and clause TBD pending code edition identification. (Lensing A-002)
**Note:** Procedure Step 3.2 assumes safety devices are required but no corresponding normative requirement previously existed. This requirement is added as an ASSUMPTION pending confirmation of the applicable safety standard. The Procedure assumption is now normatively anchored here.

### REQ-011-03-016 — Weather Seals
**Shall:** Each overhead door installation shall include weather seals (head, jamb, and floor seals) appropriate for a heated industrial bay in Alberta cold climate conditions.
**Source:** ASSUMPTION: weather seals required for insulated/heated bay in Alberta climate; specification TBD in IFC drawings and door schedule. (Lensing C-002)
**Note:** Procedure Step 3.2 assumed weather seals as required but no corresponding normative requirement previously existed. This requirement is added as an ASSUMPTION pending design team confirmation of seal specifications.

### REQ-011-03-017 — Warranty Provisions
**Shall:** Overhead doors and operators shall be covered by manufacturer warranty documentation. Manufacturer warranty duration and scope shall be confirmed and shall not be less than the project guarantee period (construction period plus 2-year warranty period per RFP S2.10.2).
**Source:** RFP S2.10.2 (guarantee period definition); ASSUMPTION: manufacturer warranty should align with or exceed project guarantee period. (Lensing F-003)
**Note:** RFP S2.10.2 establishes a guarantee period encompassing the construction period and 2-year warranty following CCC date. Manufacturer-specific warranty terms are TBD pending door procurement. The General Contractor bears guarantee responsibility per RFP S2.10 regardless of manufacturer warranty duration.

---

## Standards

| Standard / Code | Applicability | Accessibility |
|---|---|---|
| Alberta Building Code (ABC) | Governing building code for the Province of Alberta -- specific edition and clause numbers TBD pending permit documentation (Lensing A-003) | ASSUMPTION: likely applicable; specific edition TBD -- location TBD |
| Alberta Safety Codes Act | Governing safety codes legislation; includes requirements for motorised door safety devices (Lensing A-002) | RFP S3.3.2, S3.4; location TBD |
| CCDC 14-2013 | Design-Build Stipulated Price Contract -- governs overall contractual obligations including guarantee period (S2.10) | RFP S2.7; location TBD |
| National Building Code of Canada (NBC) | Reference code basis for Alberta Building Code | ASSUMPTION: likely applicable as base code; location TBD |
| Alberta Fire Code | Potentially applicable for fire separation requirements between repair bays and adjacent spaces -- TBD (Lensing F-002) | ASSUMPTION: likely applicable; specific requirements TBD -- location TBD |
| CSA standards (steel, concrete) | Applicable to concrete and steel construction components | ASSUMPTION: likely applicable per engineering practice; specific standards TBD in IFC structural drawings |

**Note:** Specific code editions and clause-level requirements are TBD pending IFC drawings and permit documentation. No clause-level requirements are derived here from the above standards as the relevant texts are not directly accessible. Fire separation requirements between repair bays (potential flammable fluid exposure) and adjacent occupied/storage spaces (parts room, utility room) are a standard building code consideration that should be assessed by the design team during IFC development. (Lensing F-002)

---

## Verification

| Requirement | Verification Approach | Record |
|---|---|---|
| REQ-011-03-001 (Quantity) | Visual count and field measurement of completed bays | Construction completion record |
| REQ-011-03-002 (Bay Width) | Field measurement against IFC drawing dimensions; confirm whether measurement represents nominal or clear dimension per IFC definition (Lensing B-002) | As-built survey (DEL-008-04) |
| REQ-011-03-003 (Drive-Through) | Physical inspection -- confirm door at each end of each bay | Inspection report |
| REQ-011-03-004 (Overhead Doors) | Physical inspection -- confirm doors installed, operational, and matching IFC schedule; verify rough opening dimensions within manufacturer tolerances for plumb, square, and dimensional accuracy (Lensing A-004) | Functional testing report |
| REQ-011-03-005 (Equipment Accommodation) | Design review of IFC drawings for equipment clearance envelope using County fleet data (specific vehicle dimensions: height with raised attachments, width, length, turning radius); functional test with representative equipment if practicable (Lensing F-001) | IFC drawing review sign-off documenting clearance envelope dimensions verified; functional testing report |
| REQ-011-03-006 (Structural / 35' ceiling) | IFC structural drawing review; field measurement of ceiling height | Inspection report; as-built record |
| REQ-011-03-007 (Sump Drain Provisions) | Field inspection -- confirm floor drainage slope percentage and direction per IFC/civil drawings; measurable acceptance criteria (slope %, direction, ponding test if specified) TBD pending engineer specification (Lensing D-001) | Inspection report with slope measurements |
| REQ-011-03-008 (Exhaust Provisions) | Field inspection -- confirm structural provisions are in place; coordination hold point sign-off with PKG-013 mechanical contractor prior to MEP rough-in commencement (Lensing X-002) | Coordination record with hold point sign-off; inspection report |
| REQ-011-03-009 (Door Power Provisions) | Coordination sign-off with PKG-015 electrical contractor | Coordination record |
| REQ-011-03-010 (IFC Drawings) | Review and confirmation that P.Eng.-stamped IFC drawings are on site | Drawing register |
| REQ-011-03-011 (Code Compliance) | Inspection approvals from applicable Safety Code Officers; code edition confirmed from permit documentation (Lensing A-003) | Inspection reports (DEL-009-04); permit records identifying applicable code edition |
| REQ-011-03-012 (Inspection Coordination) | County representative sign-off on inspections; copies of reports filed | Inspection log (DEL-009-04) |
| REQ-011-03-013 (Completion Deadline) | Project schedule tracking; completion declaration | Project schedule; CCC documentation |
| REQ-011-03-014 (Upstream Dependencies) | Construction sequence confirmation prior to bay work commencement | Schedule / daily log |
| REQ-011-03-015 (Safety Devices) | Functional test of each door's obstruction sensor and auto-reverse mechanism during commissioning (Step 3.4) | Functional testing report |
| REQ-011-03-016 (Weather Seals) | Physical inspection confirming head, jamb, and floor seals installed and contacting surfaces correctly when door is closed | Inspection report |
| REQ-011-03-017 (Warranty Provisions) | Review of manufacturer warranty documentation; confirm warranty period meets or exceeds project guarantee period (RFP S2.10.2) | Warranty documentation on file |

---

## Documentation

The following artifacts are anticipated upon completion of this deliverable (per _CONTEXT.md):

| Artifact | Description |
|---|---|
| Repair bay structural installation documentation | Records confirming structural elements (bay walls, door frames, rough openings) installed per IFC drawings |
| Bay door and track installation records | Supplier/installer records confirming overhead doors, tracks, hardware, operators, safety devices, and weather seals installed per specifications |
| Functional testing reports | Records confirming each overhead door operates correctly through full open/close cycle including safety device verification |
| Inspection reports | Copies of all applicable Safety Code and building inspection reports for this scope |
| As-built markup | Red-line or digital as-built markups for bay dimensions and door rough openings (feeds DEL-008-04 as-built survey) |
| Warranty documentation | Manufacturer warranty certificates for overhead doors and operators with warranty period and scope confirmed (Lensing F-003) |
| Coordination hold point records | Sign-off records from PKG-013 (exhaust provisions) and PKG-014 (sump drain provisions) coordination gates (Lensing X-002) |
