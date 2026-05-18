# Specification — DEL-004-03 Power Distribution Plans

---

## Scope

### What This Deliverable Covers

DEL-004-03 Power Distribution Plans is the IFC (Issued for Construction) drawing set that graphically documents the power distribution system for the New North Shop addition at the West Dried Meat Lake Regional Landfill Maintenance Shop site, near Ferintosh, Alberta.

This deliverable covers:
- Floor-plan-level layout of all power distribution elements: service entry point, panelboard locations, branch circuit routing, and load connection points for all identified power loads
- Power feeds to: two 5-tonne overhead cranes, overhead doors, 40A compressor circuit, 70A fire hose pump circuit, 70A pressure washer circuit, welding-grade receptacles (50A/240V, ASSUMPTION per D-009), and all other receptacles per Appendix B (Electrical) layout
- Power feeds to all lighting loads (main shop high bay, wash bay high bay, office, utility room, parts/tool room) — coordinated with DEL-004-04 Lighting Plans
- Power feeds to exhaust fans and mechanical equipment requiring electrical connection
- Coordination with DEL-004-02 (Single-Line Diagram) for service-level context and DEL-004-06 (Panel Schedules) for circuit assignment tabulation
- Three-phase service supply to the building

This deliverable does not cover:
- Low-voltage systems (security cameras, antenna/radio wiring) — those are addressed in DEL-004-07 Low-Voltage System Plans
- Mechanical equipment selection or sizing — those are PKG-003 scope
- Plumbing system electrical connections not explicitly identified in Appendix B (Electrical) — coordinate with DEL-006
- Single-line diagram (DEL-004-02)
- Panel schedule tabulation (DEL-004-06)
- Receptacle layout detail beyond circuit identification (DEL-004-05 Receptacle Layout Plans)
- Electrical service tie-in coordination (PKG-018 Sitework) — though power distribution plans must show the service entry point

---

## Requirements

### REQ-003-01 — Three-Phase Power Supply
The building shall be designed to operate on three-phase power.
- Source: RFP §3.4 ("The Proposed building shall run on three-phase power.")
- Verification: Confirmed on Single-Line Diagram (DEL-004-02) and on power plans showing service entry.

### REQ-003-02 — Crane Power Circuits
The drawing set shall show power supply circuits for two (2) 5-tonne overhead cranes on trolley.
- Source: RFP §3.4 ("2 – 5-tonne overhead cranes on a trolley"); App B (Electrical) ("Will need power for crane")
- Circuit rating: TBD by engineer (ASSUMPTION: three-phase circuit; capacity to be confirmed per crane manufacturer requirements)
- Verification: Circuits shown on power plans; cross-referenced on panel schedule (DEL-004-06).

### REQ-003-03 — Overhead Door Power Circuits
The drawing set shall show power supply circuits for all overhead doors. The number of door operator circuits shall match the architectural door schedule (DEL-001-07).
- Source: App B (Electrical) ("Will need power for... Overhead Doors")
- Number of doors: **TBD** — specific count to be confirmed from the architectural door schedule (DEL-001-07, produced by Architect); ASSUMPTION: per conceptual floor plan, multiple 24' overhead doors in main shop and wash bay (Enrichment: F-001; Source: Architect / DEL-001-07)
- Circuit ratings: TBD by architect/engineer coordination
- Acceptance criteria: The number of door operator circuits shown on the power distribution plans shall equal the number of powered overhead doors identified in the architectural door schedule (DEL-001-07). Any discrepancy shall be resolved with the Architect before IFC issue (Enrichment: F-002)
- Verification: Circuits shown on power plans for each door operator location; count verified against architectural door schedule (DEL-001-07).

### REQ-003-04 — Compressor Circuit
The drawing set shall show a dedicated 40A circuit for the air compressor.
- Source: App B (Electrical) ("40 Amp Compressor")
- Verification: 40A circuit shown on power plans and panel schedule.

### REQ-003-05 — Fire Hose Pump Circuit
The drawing set shall show a dedicated 70A circuit for the fire hose pump.
- Source: App B (Electrical) ("70 Amp Fire Hose Pump")
- Verification: 70A circuit shown on power plans and panel schedule.

### REQ-003-06 — Pressure Washer Circuit
The drawing set shall show a dedicated 70A circuit for the pressure washer.
- Source: App B (Electrical) ("70 Amp Pressure Washer")
- Verification: 70A circuit shown on power plans and panel schedule.

### REQ-003-07 — Welding-Grade Receptacles
The drawing set shall show multiple high-voltage welding-grade electrical receptacles throughout the shop area.
- Source: RFP §3.4 ("Multiple electrical plugs throughout the shop area suitable for connecting high voltage welding equipment")
- Assumed rating: 50A/240V per Decomposition Decision D-009 — **ASSUMPTION**
- Note: County to supply welding equipment specifications; final receptacle type to be confirmed against County's welding equipment requirements (RFP §3.4, SOW-0204). **TBD:** Confirm welding receptacle rating (50A/240V assumed per D-009) against County welding equipment specifications before IFC (Enrichment: A-002; Source: RFP §3.4, SOW-0204)
- Verification: Receptacle locations and circuit feeds shown on power plans; coordinated with DEL-004-05.

### REQ-003-08 — Mixed-Grade Receptacle Circuits
The drawing set shall show power circuits for receptacles of the following ratings per the Appendix B (Electrical) layout:
- 15A/120V receptacles
- 20A/120V receptacles
- 20A/240V receptacles
- 30A/240V receptacles
- 50A/240V receptacles
- Source: App B (Electrical) (legend and layout markings throughout floor plan)
- Verification: Circuit feeds for each receptacle type shown on power plans; coordinated with DEL-004-05.

### REQ-003-09 — Exhaust Fan Power Circuits
The drawing set shall show power circuits for exhaust fan(s) as shown on the electrical drawing.
- Source: App B (Electrical) (exhaust fan symbol shown in drawing legend and on floor plan)
- Quantity and locations: Per Appendix B conceptual drawing layout
- Verification: Exhaust fan circuit(s) shown on power plans.

### REQ-003-10 — Lighting Power Circuits
The drawing set shall show branch circuit feeds to all luminaire locations, consistent with DEL-004-04 Lighting Plans:
- Main shop: 20 high bay LED fixtures (150W, 22,000 lumens each; 5 rows × 4)
- Wash bay: 6 high bay fixtures (2 rows × 3)
- Office: 1 × 8' LED fixture
- Utility room: 2 × 8' LED fixtures
- Parts/tool room: 6 × 8' LED fixtures
- Source: App B (Electrical) (electrical notes and luminaire symbols on floor plan)
- Verification: Lighting branch circuits shown on power plans; consistent with DEL-004-04.

### REQ-003-11 — Ceiling Fan Power Circuits
The drawing set shall show power circuits for 6 ceiling fans in the main shop area.
- Source: App B (Electrical) ("6 Ceiling Fans for Main Shop")
- Verification: Ceiling fan circuits shown on power plans.

### REQ-003-12 — Mechanical Equipment Power
The drawing set shall show power feeds to mechanical equipment requiring electrical connection, including (at minimum):
- Forced-air makeup air unit (ASSUMPTION: electrically powered; coordinate with PKG-003/DEL-003)
- High-recovery heating system (ASSUMPTION: electrically connected; coordinate with PKG-003/DEL-003)
- High-volume air exchanger (ASSUMPTION: electrically connected; coordinate with PKG-003/DEL-003)
- Source: RFP §3.4; App B (Shop); ASSUMPTION for electrical connection of mechanical equipment
- Verification: Mechanical equipment power feeds shown on power plans; confirmed through MEP coordination.

### REQ-003-13 — IFC Drawing Standard
All drawings shall be Issued for Construction (IFC) quality and signed/stamped by a Professional Engineer licensed in the Province of Alberta.
- Source: RFP §3.3.2 ("All Issued For Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta"); Decomposition SOW-0018
- Verification: Drawings bear P.Eng. stamp and signature prior to release for construction.

### REQ-003-14 — Preliminary Design Approval
A preliminary electrical design (DEL-004-01) must receive County approval before IFC drawings are issued.
- Source: RFP §3.3.2; Decomposition SOW-0010d
- Acceptance criteria: **TBD** — Define what constitutes "County approval" (e.g., signed approval letter, email confirmation from authorized County representative, stamped drawing return). The form of evidence shall be agreed upon with the County before the preliminary design submission (Enrichment: X-001; Source: Specification REQ-003-14, Verification table)
- Verification: County approval documented in the agreed form before IFC set is released.

### REQ-003-15 — Code Compliance
The electrical design shall adhere to all applicable Alberta Safety Codes and building codes and regulations.
- Source: RFP §3.3.2 ("The proposed building must adhere to all Alberta Safety Codes"); RFP §3.3.2 ("The building design must adhere to all applicable building codes and regulations")
- Applicable codes: ASSUMPTION — Alberta Electrical Code (CEC Part I as adopted by Alberta Safety Codes); Alberta Building Code; **specific code edition TBD** — Electrical Engineer to confirm with the authority having jurisdiction (AHJ) which edition of CEC Part I is currently adopted by Alberta for this project (Enrichment: A-001, source: Specification REQ-003-15 / Standards table)
- Code section applicability notes (ASSUMPTION — Electrical Engineer to confirm; location TBD in source text):
  - CEC Section 40 (or Alberta-adopted equivalent): crane and hoist wiring provisions — applies to REQ-003-02 (Enrichment: A-003)
  - CEC Section 26 (or Alberta-adopted equivalent): receptacle installation and rating provisions — applies to REQ-003-07, REQ-003-08 (Enrichment: A-003)
  - CEC GFCI/AFCI provisions: applicability to wet/damp locations (wash bay, washroom) and office areas — see REQ-003-16 below (Enrichment: A-003)
- Verification: Code compliance confirmed through Alberta Safety Code permit process (DEL-009-03); inspection reports submitted per SOW-0084/SOW-0085.

### REQ-003-16 — GFCI/AFCI Protection (NEW — Enrichment C-001)
The electrical design shall assess and apply Ground Fault Circuit Interrupter (GFCI) protection for receptacles in wet or damp locations (wash bay, washroom) and Arc Fault Circuit Interrupter (AFCI) protection in office/sleeping areas, as required by the applicable edition of CEC Part I as adopted by Alberta.
- Source: ASSUMPTION — Alberta Safety Code adoption of CEC Part I requires GFCI/AFCI provisions; specific code sections **TBD** (see Guidance: Code Compliance -- GFCI and AFCI consideration) (Enrichment: C-001)
- Verification: GFCI/AFCI protection provisions confirmed on power plans and/or noted in electrical specifications; verified during Safety Code inspection (Enrichment: C-001)

### REQ-003-17 — Grounding and Bonding System (NEW — Enrichment F-003)
The power distribution plans shall show the grounding and bonding system for the electrical installation, including (at minimum): grounding electrode conductor, equipment bonding conductors, and ground bus connections, per applicable CEC requirements.
- Source: ASSUMPTION — CEC Part I requires a grounding/bonding system for all electrical installations; specific code sections **TBD**; no explicit grounding requirement was found in RFP sources, but it is a code-mandated element (Enrichment: F-003)
- Verification: Grounding and bonding system elements shown on power distribution plans; verified during Safety Code inspection (Enrichment: F-003)

### REQ-003-18 — Fire Alarm and Emergency Power Scope Determination (NEW — Enrichment F-005)
**TBD:** Determine whether fire alarm system power provisions and/or emergency/standby power provisions are within the scope of this deliverable (DEL-004-03) or are addressed elsewhere in the project decomposition.
- Source: RFP references safety codes compliance; building is industrial occupancy; no explicit mention of fire alarm power or emergency lighting/power was found in any document for this deliverable (Enrichment: F-005)
- Resolution authority: Electrical Engineer / AHJ / project decomposition review
- Verification: TBD pending scope determination

---

## Standards

| Standard | Applicability | Accessibility / Status |
|---|---|---|
| Canadian Electrical Code (CEC), Part I — as adopted by Alberta | Governs electrical installation design in Alberta. Key sections (ASSUMPTION — Electrical Engineer to confirm with AHJ): Section 26 (receptacles), Section 40 (cranes/hoists), GFCI/AFCI provisions (Enrichment: A-001, A-003) | ASSUMPTION: likely applicable; **specific edition TBD** — Electrical Engineer to confirm with AHJ which edition is currently adopted (Enrichment: A-001) |
| Alberta Safety Codes Act | Governing safety code authority for Alberta | Referenced in RFP §3.3.2; full text not in sources |
| Alberta Building Code | Building design compliance | Referenced in RFP §3.3.2 ("all applicable building codes"); full text not in sources |
| CCDC 14-2013 Design-Build Stipulated Price Contract | Contract framework | RFP §2.7; document not in sources |
| CSA C22.1 (Canadian Electrical Code) and related product standards | **TBD** — Confirm whether CSA C22.1 is the specific standard adopted by Alberta, or whether Alberta adopts a different designation. If CSA C22.1 is confirmed, remove the ASSUMPTION qualifier; if not confirmed, retain as TBD (Enrichment: C-002) | ASSUMPTION: standard engineering practice; not cited in RFP sources — **TBD** pending confirmation by Electrical Engineer / AHJ (Enrichment: C-002) |

---

## Verification

| Requirement | Verification Approach |
|---|---|
| REQ-003-01 Three-phase supply | Confirm three-phase service on Single-Line Diagram (DEL-004-02) and power plans |
| REQ-003-02 Crane circuits | Crane circuits shown on drawings; circuit capacity confirmed against crane specs at detail design |
| REQ-003-03 Overhead door circuits | Door operator circuits shown; count verified against architectural door schedule (DEL-001-07); acceptance: circuit count equals door count per DEL-001-07 (Enrichment: F-002) |
| REQ-003-04 Compressor 40A | 40A circuit visible on plans and panel schedule |
| REQ-003-05 Fire hose pump 70A | 70A circuit visible on plans and panel schedule |
| REQ-003-06 Pressure washer 70A | 70A circuit visible on plans and panel schedule |
| REQ-003-07 Welding receptacles | 50A/240V circuits shown; County welding specs reviewed before IFC |
| REQ-003-08 Mixed receptacles | All receptacle circuit types present per App B layout |
| REQ-003-09 Exhaust fans | Fan circuits shown at locations per App B |
| REQ-003-10 Lighting circuits | Lighting branch circuits cross-referenced with DEL-004-04 |
| REQ-003-11 Ceiling fans | 6 ceiling fan circuits shown in main shop |
| REQ-003-12 Mechanical equipment | MEP coordination complete; mechanical equipment power shown |
| REQ-003-13 IFC + P.Eng. stamp | P.Eng. stamp present on IFC drawing set |
| REQ-003-14 Preliminary approval | County approval documented in agreed form (TBD — see REQ-003-14 acceptance criteria; Enrichment: X-001) before IFC release |
| REQ-003-15 Code compliance | Safety Code permit issued; inspection reports on file |
| REQ-003-16 GFCI/AFCI protection | GFCI/AFCI provisions shown on plans and/or noted in specifications; verified during Safety Code inspection (Enrichment: C-001) |
| REQ-003-17 Grounding and bonding | Grounding electrode, bonding conductors, and ground bus shown on plans; verified during Safety Code inspection (Enrichment: F-003) |
| REQ-003-18 Fire alarm / emergency power scope | TBD — verification pending scope determination (Enrichment: F-005) |

---

## Documentation

### Required Artifacts (Anticipated)

| Artifact | Description |
|---|---|
| Power Distribution Drawing Set (IFC) | Floor-plan-based drawings showing all power distribution elements; P.Eng.-stamped |
| Panel Schedule Cross-Reference | Branch circuit assignments cross-referenced to DEL-004-06 Panel Schedules |
| MEP Coordination Record | Documentation of coordination with PKG-003 (Mechanical) and PKG-006 (Plumbing) for shared equipment power. Minimum content shall include: meeting/review dates, attendees, decisions made, action items with responsible parties and due dates, and confirmation of equipment electrical ratings used in design (Enrichment: X-002; Source: Specification Documentation section) |

### Drawing Revision Convention (Enrichment: E-003)

**TBD:** Define the drawing revision numbering convention and revision history tracking method for the IFC set. ASSUMPTION: standard convention is Rev 0 = IFC; subsequent revisions numbered sequentially (Rev 1, Rev 2, etc.) with revision date and description. Electrical Engineer / project standards to confirm. (Source: Procedure Records table lists "Drawing revision history" as a required record but no convention is specified.)

### Related Deliverables

| Deliverable ID | Relationship |
|---|---|
| DEL-004-01 Preliminary Electrical Design | Predecessor — must be County-approved before IFC |
| DEL-004-02 Single-Line Diagram | Top-level system overview; power plans must be consistent |
| DEL-004-04 Lighting Plans | Lighting load coordination |
| DEL-004-05 Receptacle Layout Plans | Receptacle location coordination |
| DEL-004-06 Panel Schedules | Circuit assignment tabulation |
| DEL-004-09 Electrical Specification | Governs materials and workmanship for installation |
| DEL-009-03 Safety Code Permits | Electrical permit required before construction |
| PKG-015 Electrical & Low-Voltage Installation | Construction package that executes against these drawings |
