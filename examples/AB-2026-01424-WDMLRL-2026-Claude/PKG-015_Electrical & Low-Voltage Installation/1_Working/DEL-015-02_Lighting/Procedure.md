# Procedure — DEL-015-02 Lighting Installation

**Deliverable ID:** DEL-015-02
**Title:** Lighting Installation
**Package:** PKG-015 — Electrical & Low-Voltage Installation
**Document Status:** SEMANTIC_READY (Pass 3 enrichment applied)
**Prepared By:** 4_DOCUMENTS Agent
**Date:** 2026-02-26

---

## Purpose

This procedure describes the steps to produce and complete the Lighting Installation deliverable for the New North Shop at the West Dried Meat Lake Regional Landfill. It covers activities from pre-installation design review through physical installation, energization, functional verification, and close-out documentation.

The procedure addresses the installation of all lighting fixtures and associated wiring in the five defined zones (Z-1 through Z-5), corresponding to SOW-0052 through SOW-0056.

*Sources: _CONTEXT.md; Specification REQ-L-01 through REQ-L-16; App B-Elec; Decomposition §7 DEL-015-02*

---

## Prerequisites

Before beginning any installation activities, all of the following prerequisites must be satisfied:

| # | Prerequisite | Source / Reference |
|---|---|---|
| P-1 | IFC electrical drawings for the lighting system are complete, stamped by a Professional Engineer licensed in Alberta, and approved for construction. IFC drawings must include: lighting layout for all five zones, circuit assignments, panel schedules, and switch locations. | RFP §3.3.2; Spec REQ-L-09 |
| P-2 | Electrical Safety Code Permit has been obtained from the authority having jurisdiction (AHJ) | RFP §3.3.2; Spec REQ-L-10 |
| P-3 | Building structure and ceiling are substantially complete in each zone prior to fixture installation in that zone | _DEPENDENCIES.md (external dependency) |
| P-4 | DEL-015-01 (Three-Phase Power Service) is installed and the main distribution panel is in place (not necessarily energized, but available for circuit termination) | _DEPENDENCIES.md (Upstream: DEL-015-01) |
| P-5 | Fixture data sheets for all LED fixture types have been reviewed and approved by the Electrical Engineer of Record (EOR), confirming compliance with REQ-L-02 (Main Shop 150 W / 22,000 lm), REQ-L-04 (Wash Bay wet/damp rating and performance per IFC), and REQ-L-08 (LED technology) | Spec REQ-L-02, REQ-L-04, REQ-L-08 |
| P-6 | Overhead crane shop drawings (PKG-016) have been reviewed for rail elevation and clearance envelope in the Main Shop to confirm lighting mounting positions do not conflict | Spec REQ-L-12; Guidance P-5 |
| P-7 | Fixture quantities and materials are on site and verified against the IFC drawing fixture schedule and approved submittal quantities. The BOM shall be cross-referenced to the IFC fixture schedule (not verified in isolation) to prevent circular reference. *(Enrichment: F-003; source: Procedure P-7 previously referenced BOM self-verification)* | ASSUMPTION: standard practice; Spec REQ-L-01, L-03, L-05, L-06, L-07 |
| P-8 | Appropriate elevated access equipment is available for Main Shop and Wash Bay fixture installation at 35-foot ceiling height. **Minimum requirement:** articulating boom lift or equivalent aerial work platform with working height rated to at least 40 feet (to provide safe working platform at 35-foot ceiling). Equipment type and specification shall be confirmed by the Electrical Contractor based on site access constraints and OSHA/provincial safety requirements. *(Enrichment: D-002; source: ASSUMPTION based on 35-foot ceiling height per RFP §3.4; equipment must exceed ceiling height for safe reach)* | Guidance C-6; ASSUMPTION |
| P-9 | **HOLD-POINT: Switching/controls design confirmed.** The switching and controls strategy (manual switches, occupancy sensors, or other — see Spec REQ-L-14 and Guidance C-3) has been decided by the Owner and implemented by the EOR in the IFC drawings before Phase 2 rough-in begins. Switch locations and control wiring must be shown on IFC drawings before conduit routing can be finalized. *(Enrichment: A-004; source: Spec REQ-L-14 TBD; Guidance C-3; Procedure Step 7 depends on switch locations)* | Spec REQ-L-14; Guidance C-3 |

---

## Steps

### Phase 1: Design Review and Pre-Installation Preparation

**Step 1 — Review IFC Drawings**
Review the IFC electrical drawings for the lighting system. Confirm that all five zones (Z-1 through Z-5) are covered, that fixture counts match the SOW requirements (REQ-L-01, REQ-L-03, REQ-L-05, REQ-L-06, REQ-L-07), and that circuit assignments, panel schedules, and switch locations are complete.

*Reference: Spec REQ-L-09; IFC Electrical Drawings*

**Step 2 — Confirm Fixture Submittals**
Submit fixture data sheets to the EOR and owner for review. Confirm the following for each fixture type:
- LED technology (all zones) — REQ-L-08
- 150 W minimum, 22,000 lm minimum for Main Shop high bays — REQ-L-02
- Wet or damp location rating for Wash Bay high bays — REQ-L-04
- 8-foot form factor for Office, Utility Room, and Parts/Tool Room — REQ-L-05, REQ-L-06, REQ-L-07
- Manufacturer product warranty documentation — REQ-L-13A *(Enrichment: D-003)*

Obtain written approval before ordering materials in final quantities.

*Reference: Spec REQ-L-02, REQ-L-04, REQ-L-08, REQ-L-13A*

**Step 3 — Coordinate Crane Clearances (Main Shop)**
Prior to marking out fixture mounting positions in the Main Shop, obtain the overhead crane rail elevation and maximum hook height from the crane supplier (PKG-016). Confirm minimum clearance between the bottom of any lighting fixture (at lowest pendant position) and the top of the crane hook at maximum elevation. Document the clearance confirmation.

*Reference: Spec REQ-L-12; Guidance P-5*

**Step 3a — Coordinate Ceiling Fan Mounting Positions (Main Shop)**
Prior to marking out high-bay fixture positions in the Main Shop (Step 4), coordinate with the ceiling fan scope owner (TBD — see Guidance CONF-L-03) to confirm:
- Intended mounting locations for the 6 ceiling fans noted in App B-Elec
- Any structural supports or mounting hardware that may conflict with high-bay fixture positions
- Minimum separation distances between ceiling fan blades and adjacent fixtures

If the ceiling fan scope owner has not been identified, record this as a hold-point and notify the project manager. Do not proceed with Main Shop fixture mark-out until fan locations are at least provisionally established or the coordination interface is formally waived.

*(Enrichment: C-004, E-001; sources: App B-Elec Electrical Notes "6 Ceiling Fans for Main Shop"; Guidance C-5, CONF-L-03)*

*Reference: Guidance C-5; Guidance CONF-L-03*

**Step 4 — Mark Out Fixture Positions**
Using the approved IFC drawings, mark out fixture mounting positions in each zone. Confirm row spacing and fixture-to-fixture spacing match the IFC layout.

For Z-1 (Main Shop): 5 rows of 4 fixtures — confirm row orientation relative to crane travel direction.
For Z-2 (Wash Bay): 2 rows of 3 fixtures.
For Z-3 through Z-5: positions per IFC drawings.

> **OWNER INSPECTION HOLD-POINT:** After fixture positions are marked out and before proceeding to Phase 2 rough-in, the Owner representative shall have the opportunity to inspect and approve the marked layout against the IFC drawings. *(Enrichment: X-004; source: Specification Verification table references Owner Inspector for layout conformance)*

*Reference: App B-Elec floor plan; IFC Electrical Drawings*

---

### Phase 2: Rough-In Wiring

**Step 5 — Install Conduit and Pull Boxes**
Install conduit runs, pull boxes, and junction boxes per the IFC electrical drawings. Use conduit type and supports as specified (TBD — per IFC design and CSA C22.1 requirements).

*Reference: Spec REQ-L-10; IFC Electrical Drawings*

**Step 6 — Pull Branch Circuit Wiring**
Pull branch circuit conductors from the distribution panel to each fixture location per the IFC drawings. Conductor sizing and insulation type shall comply with CSA C22.1 and the IFC design.

*Reference: Spec REQ-L-10; IFC Electrical Drawings*

**Step 7 — Install Switching Devices**
Install wall switches or other control devices at locations specified in the IFC drawings (confirmed per prerequisite P-9). Label each switch with the zone or circuit it controls.

*Reference: Spec REQ-L-14; IFC Electrical Drawings*

---

### Phase 3: Fixture Installation

**Step 8a — Install Main Shop High-Bay Fixtures (Z-1)**
Using elevated access equipment (minimum 40-foot working height per P-8), install 20 x 150 W LED high-bay fixtures in the Main Shop per the marked-out positions and IFC drawings. Mount fixtures using the specified hanging method (pendant, aircraft cable, or chain — per IFC). Ensure mounting hardware is rated for the fixture weight. Maintain clearance above the overhead crane envelope as confirmed in Step 3.

Arrange in 5 rows of 4 as per App B-Elec layout. Terminate wiring connections per manufacturer instructions and IFC drawings.

*Reference: SOW-0052; Spec REQ-L-01, REQ-L-02, REQ-L-12; App B-Elec*

**Step 8b — Install Wash Bay High-Bay Fixtures (Z-2)**
Using elevated access equipment, install 6 x LED high-bay fixtures (wet/damp-rated) in the Wash Bay per the IFC drawings, in 2 rows of 3. Confirm IP/NEMA rating is appropriate before installation.

*Reference: SOW-0053; Spec REQ-L-03, REQ-L-04*

**Step 8c — Install Office Fixture (Z-3)**
Install 1 x 8-foot LED linear fixture in the Office per the IFC drawings.

*Reference: SOW-0054; Spec REQ-L-05*

**Step 8d — Install Utility Room Fixtures (Z-4)**
Install 2 x 8-foot LED linear fixtures in the Utility Room per the IFC drawings.

*Reference: SOW-0055; Spec REQ-L-06*

**Step 8e — Install Parts / Tool Room Fixtures (Z-5)**
Install 6 x 8-foot LED linear fixtures in the Parts/Tool Room per the IFC drawings.

*Reference: SOW-0056; Spec REQ-L-07*

> **OWNER INSPECTION HOLD-POINT:** After all fixtures are installed (Steps 8a through 8e) and before proceeding to Phase 4 energization, the Owner representative shall have the opportunity to inspect installed fixtures for count, positioning, and workmanship. *(Enrichment: X-004)*

*Reference: Spec Verification table (Owner Inspector at completion)*

---

### Phase 4: Terminations and Energization

**Step 9 — Complete Electrical Terminations**
Complete all circuit terminations at the distribution panel. Apply circuit labels per the panel schedule on the IFC drawings. Verify all connections are torqued to specification and that no loose conductors exist.

*Reference: CSA C22.1; IFC Electrical Drawings*

**Step 10 — Pre-Energization Check**
Before energizing lighting circuits, confirm:
- DEL-015-01 (Three-Phase Power Service) is energized and panels are live — Spec REQ-L-11
- All lighting circuit wiring has been inspected by the electrician of record
- All fixture covers and enclosures are closed
- No personnel are in elevated positions near energized conductors

> **OWNER INSPECTION HOLD-POINT:** Before energization, the Owner representative shall confirm readiness and be present (or provide written waiver) for initial energization. *(Enrichment: X-004)*

*Reference: Spec REQ-L-11; ASSUMPTION re: safety protocol*

**Step 11 — Energize and Functional Test (Commissioning Acceptance)**
Energize each lighting circuit and operate all switches. Confirm:
- All fixtures illuminate on command
- No breaker trips on energization
- No visible arc flash, sparking, or unusual noise
- Switching controls operate as designed (correct fixtures controlled by correct switches)
- No fault conditions present on any circuit

Document results (pass/fail per circuit and zone). This functional test constitutes the **commissioning acceptance gate** referenced in Specification §Verification. All fixtures must be operational and all switches functional before proceeding to Safety Code inspection. *(Enrichment: X-002; source: Procedure Step 11 existing content; Specification Verification table now includes commissioning acceptance row)*

*Reference: Spec REQ-L-14; Spec Commissioning acceptance verification; ASSUMPTION re: functional test protocol*

---

### Phase 5: Inspection and Close-Out

**Step 12 — Safety Code Inspection**
Request electrical inspection from the authority having jurisdiction (AHJ). Ensure the County project representative is present and receives a copy of the completed inspection report, per RFP §3.3.2.

Address any deficiencies identified during inspection. Re-inspect if required by the AHJ.

*Reference: RFP §3.3.2; Spec REQ-L-10*

**Step 13 — As-Built Documentation**
Mark up IFC drawings to reflect any field deviations from the design (fixture positions, circuit routing changes, etc.). Provide redlined as-built drawings to the Electrical Engineer for incorporation into final record drawings. As-built drawings shall cover all five lighting zones (Z-1 through Z-5), circuit routing, and panel schedule updates. *(Enrichment: E-003; source: Specification §Documentation)*

*Reference: Spec Documentation section; ASSUMPTION: standard practice*

**Step 14 — Compile Close-Out Package**
Compile the following for submission to the Owner as part of the project close-out package:
- Completed inspection report(s) and permit close-out
- Fixture manufacturer data sheets
- Manufacturer product warranty certificates (per fixture type) *(Enrichment: D-003)*
- As-built / record drawings (all five zones, circuit routing, panel schedule)
- Contractor warranty letter (2 years from CCC date)
- Operating and maintenance instructions for fixture types (if provided by manufacturer)
- Commissioning test record (pass/fail log per Step 11) *(Enrichment: X-002)*
- EOR photometric analysis report (if required per REQ-L-16)

*Reference: RFP §2.14; Spec REQ-L-13, REQ-L-13A; Documentation section*

---

## Verification

| Check | What to Verify | Method | Reference |
|---|---|---|---|
| V-1: Fixture counts | 20 (Main Shop), 6 (Wash Bay), 1 (Office), 2 (Utility), 6 (Parts/Tool Room) installed | Physical count; compare to IFC drawing | REQ-L-01, L-03, L-05, L-06, L-07 |
| V-2: Fixture performance | Main Shop: 150 W / 22,000 lm per fixture per data sheet | Data sheet on file | REQ-L-02 |
| V-3: Wet-location rating | Wash Bay fixtures: IP65 or equivalent, wet/damp listed | Data sheet on file | REQ-L-04 |
| V-4: LED technology | All fixtures are LED type | Data sheet; visual inspection | REQ-L-08 |
| V-5: Layout conformance | Fixture positions match IFC drawings | Field walk against IFC; as-built drawing | REQ-L-09 |
| V-6: Code compliance | Safety Code inspection passed; permit closed | Inspection report | REQ-L-10 |
| V-7: Crane clearance | No fixture within crane hook / bridge clearance envelope | Measurement on site; record on file | REQ-L-12 |
| V-8: Functional operation | All fixtures illuminate; all switches control correct zones; no fault conditions | Energization test record (Step 11) | Spec general; Commissioning acceptance |
| V-9: Upstream power available | DEL-015-01 energized before lighting circuits commissioned | DEL-015-01 sign-off on file | REQ-L-11 |
| V-10: Contractor warranty | 2-year warranty letter included in close-out package | Close-out package check | REQ-L-13 |
| V-11: Manufacturer warranty | Manufacturer product warranty certificates on file for each fixture type | Close-out package check | REQ-L-13A *(Enrichment: D-003)* |
| V-12: Illuminance performance | EOR photometric analysis demonstrates minimum maintained illuminance per zone | Photometric analysis report on file | REQ-L-16 *(Enrichment: A-005, C-001, F-002)* |

---

## Records

The following records shall result from execution of this procedure and be retained in the project file:

| Record | Description | Produced At |
|---|---|---|
| Fixture submittal approvals | Written EOR/Owner approval of data sheets (including manufacturer warranty documentation) | Step 2 |
| Crane clearance confirmation | Written record of clearance measurement / confirmation | Step 3 |
| Ceiling fan coordination record | Documentation of coordination with ceiling fan scope owner, or hold-point notification to PM | Step 3a *(Enrichment: C-004)* |
| Safety Code Permit | Electrical permit from AHJ | Pre-installation (P-2) |
| Owner inspection — layout | Owner representative sign-off on marked fixture positions | Step 4 hold-point *(Enrichment: X-004)* |
| Owner inspection — installation | Owner representative sign-off on installed fixtures | Step 8e hold-point *(Enrichment: X-004)* |
| Owner inspection — pre-energization | Owner representative readiness confirmation or written waiver | Step 10 hold-point *(Enrichment: X-004)* |
| Safety Code Inspection Report | AHJ sign-off; copy to County project representative | Step 12 |
| Commissioning test record | Pass/fail log by circuit and zone documenting functional test results | Step 11 *(Enrichment: X-002)* |
| As-built drawings | Redlined IFC drawings reflecting as-installed conditions (all five zones, circuit routing, panel schedule) | Step 13 |
| Warranty documentation | Manufacturer product warranty certificates and contractor warranty letters | Step 14 |
| Close-out package | Full compilation submitted to Owner | Step 14 |
