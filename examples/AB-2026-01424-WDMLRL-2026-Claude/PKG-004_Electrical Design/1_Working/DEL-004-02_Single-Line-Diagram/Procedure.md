# Procedure — DEL-004-02 Single-Line Diagram

**Document Type:** Procedure (operational)
**Deliverable ID:** DEL-004-02
**Deliverable Name:** Single-Line Diagram
**Package:** PKG-004 Electrical Design
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Responsible Party:** Electrical Engineer
**Last Updated:** 2026-02-26

---

## Purpose

This procedure describes the steps to produce the Single-Line Diagram (SLD) for the New North Shop electrical system (DEL-004-02), from initial load inventory through to IFC issue with P.Eng. stamp. The procedure supports fulfillment of SOW-0014 (complete final electrical design) and SOW-0018 (P.Eng.-stamped IFC drawings), and advances OBJ-003 (complete IFC documentation) and OBJ-005 (electrical systems commissioned to operational readiness).

---

## Prerequisites

### Design Inputs Required Before Starting

| Input | Source Deliverable / Reference | Status |
|---|---|---|
| County approval of Preliminary Electrical Design | DEL-004-01 (Preliminary Electrical Design) — SOW-0010d | Required before IFC issue; TBD at time of SLD draft |
| Conceptual electrical layout (load locations, circuit types, legend) | App B (Electrical) — Appendix B (Electrical) conceptual drawing | Available — primary source |
| Building floor plan dimensions and room configuration | App B (Shop) / DEL-001-02 (Architectural Floor Plans) | Conceptual dimensions available (130' × 100' building); IFC floor plans TBD |
| Mechanical equipment electrical requirements (MUA unit, heating, exhaust) | DEL-003-05 (Mechanical Equipment Schedule) | TBD — coordinate with Mechanical Engineer |
| Crane electrical specifications (motor ratings, locked-rotor current, duty class) | DEL-016-01 (Two 5-Tonne Overhead Cranes) | TBD — coordinate with crane supplier |
| Overhead door motor ratings and quantity | DEL-001-07 (Door & Window Schedule) | TBD — coordinate with Architect |
| Utility service available voltage and service capacity | Local utility / service authority | TBD — Electrical Engineer to confirm |
| Alberta Safety Codes — applicable edition of CEC | Safety Codes authority | TBD — Electrical Engineer to confirm adopted edition |

### References Required

| Reference | Location |
|---|---|
| AB-2026-01424-WDMLRL RFP.pdf (§3.4, §3.3.2) | _Sources/ |
| AB-2026-01424-Appendix B (Electrical).pdf | _Sources/ |
| WDMLRL_Decomposition_Claude.md (PKG-004 scope, SOW-0014) | _Decomposition/ |
| Canadian Electrical Code (CEC) CSA C22.1 — applicable edition | Electrical Engineer's library / Safety Codes authority |

---

## Steps

### Step 1 — Compile Load Inventory from All Sources

1.1 Extract all loads from App B (Electrical) conceptual drawing and record by circuit type:
- Lighting loads (L symbol): 20 fixtures main shop; 6 fixtures wash bay; 1 office; 2 utility room; 6 parts/tool room
- Exhaust fans (E symbol): quantity and location from conceptual drawing
- 15A/120V receptacles: count and locations from conceptual drawing
- 20A/120V receptacles: count and locations from conceptual drawing
- 20A/240V receptacles: count and locations from conceptual drawing
- 30A/240V receptacles: count and locations from conceptual drawing
- 50A/240V receptacles: count and locations from conceptual drawing (welding station zone — see D-009)
- Dedicated circuits: compressor (40A), fire hose pump (70A), pressure washer (70A)
- Crane power feeds: ×2 (rating TBD per crane specification)
- Overhead door motor(s): quantity and rating TBD per architectural schedule
- Ceiling fans: 6 units, rating TBD

1.2 Request and record mechanical equipment electrical data from Mechanical Engineer (DEL-003-05):
- Forced-air makeup air unit
- High-recovery heating system
- Exhaust fans (if electrically distinct from items in 1.1 above)

1.3 Note all TBD items and flag for resolution before IFC issue (Conflicts CONF-SLD-001, CONF-SLD-002, CONF-SLD-003 in Guidance.md).

**Output:** Complete load inventory spreadsheet or register, with circuit type, rating, quantity, and source reference for each item.

**Verification gate (before proceeding to Step 4):** The Electrical Engineer shall review the load inventory for completeness before drafting the SLD. The review shall confirm: (a) all load groups from App B (Electrical) conceptual drawing are accounted for, (b) all mechanical equipment electrical loads from DEL-003-05 are included (or flagged as TBD with expected resolution source), (c) all dedicated equipment circuits from SOW-0059 through SOW-0066 are listed, and (d) any TBD items have an identified resolution path and responsible party. The reviewed load inventory shall be signed/initialed by the Electrical Engineer before Step 4 commences. *(Added per X-002: adequate implementation evidence requires verifying inputs, not just outputs.)*

---

### Step 2 — Confirm System Voltage with Local Utility

2.1 Contact the local utility / service authority serving SW 14–44–21–W4 (near Ferintosh, Alberta) to determine:
- Available system voltage (typically 120/208V three-phase wye or 347/600V three-phase wye in Alberta rural industrial settings — ASSUMPTION; confirm)
- Maximum available service ampacity at the site
- Utility metering and protection requirements for service entrance

2.2 Document confirmed system voltage and utility requirements.

2.3 If 347/600V three-phase is available and selected: identify step-down transformer requirements for 120V and 240V loads on the load inventory.

**Output:** Confirmed system voltage; utility requirements documented. Resolves CONF-SLD-001.

---

### Step 3 — Perform Demand / Load Calculation (coordinate with DEL-004-08)

3.1 Using the load inventory (Step 1) and confirmed system voltage (Step 2), perform a demand calculation per applicable CEC requirements to determine:
- Total connected load
- Calculated demand (applying applicable demand factors per CEC)
- Required main service ampacity
- Required main distribution panel (MDP) bus rating

3.2 Identify sub-panel locations and feeder sizes based on load grouping and building dimensions (130' × 100' building — voltage drop over long runs must be considered).

3.3 The load calculation is the primary content of DEL-004-08 (Electrical Calculation Package). The SLD shall reflect the results of this calculation — Step 3 and SLD drafting (Step 4) are iterative.

**Output:** Main service size; MDP bus rating; sub-panel locations and feeder sizes. Feeds directly into SLD content.

---

### Step 4 — Draft Single-Line Diagram

4.1 **Select and document drawing platform/format:** The Electrical Engineer shall select the drawing platform (e.g., AutoCAD, Revit, MicroStation, or equivalent) and output format (DWG, PDF, or both) for the SLD, and record this decision in the project document register. If the project has an established CAD/BIM standard or the Owner has format preferences, those shall govern. If no project standard exists, the Electrical Engineer shall select the platform and document the choice before proceeding. *(Enriched per A-004: practical execution requires explicit platform/format specification or decision step.)* Open the SLD drawing file in the selected platform.

4.2 Lay out the SLD hierarchy from left to right (or top to bottom) per standard convention:
- Utility service entrance block (system voltage, phase, metering, main disconnect)
- Main Distribution Panel (MDP) block (bus rating, main breaker ampacity)
- Feeder runs to sub-panels (labelled, with conductor size and conduit type — TBD from calculation)
- Sub-panel blocks with bus ratings
- Branch circuit summary annotations (lighting, receptacle groups, dedicated equipment)

4.3 Add dedicated circuit blocks for:
- Crane #1 (5-tonne) — TBD rating; label as "CRANE 1 — TBD PENDING CRANE SPEC" until resolved
- Crane #2 (5-tonne) — TBD rating; label as "CRANE 2 — TBD PENDING CRANE SPEC"
- Overhead door(s) — TBD rating; label as "OVERHEAD DOORS — TBD PENDING ARCHITECTURAL SCHEDULE"
- Compressor — 40A dedicated circuit (App B — Electrical)
- Fire Hose Pump — 70A dedicated circuit (App B — Electrical)
- Pressure Washer — 70A dedicated circuit (App B — Electrical)
- Exhaust fan(s) — TBD; label as "EXHAUST FAN(S) — TBD PENDING MECHANICAL COORD."
- Ceiling fans (6) — TBD; label as "CEILING FANS — TBD PENDING EQUIP. SELECTION"

4.4 Add mechanical equipment power provisions block (TBD ratings from DEL-003-05; include TBD placeholder).

4.5 Add low-voltage system power notation if applicable (security cameras, radio antenna — TBD; note "SEE DEL-004-07 FOR LOW-VOLTAGE DESIGN").

4.6 **Establish drawing numbering and revision control convention:** Before applying the title block, the Electrical Engineer shall confirm or establish the project drawing numbering convention and revision control scheme. This includes: (a) drawing number format (e.g., project number + discipline prefix + sequential number), (b) revision letter/number convention (e.g., P1 for preliminary, Rev A/B/C for issued revisions), and (c) revision tracking method (revision cloud, delta marks, or revision table). If a project-level numbering convention exists (from the Project Manager or other discipline leads), adopt it. If none exists, establish one and document it in the project document register. *(Added per C-003: thorough execution coverage requires numbering convention established before drafting.)*

4.7 Apply title block, revision number, date, project name, deliverable ID (DEL-004-02), and drawing number per the established numbering convention (Step 4.6).

**Output:** Draft SLD drawing — preliminary issue (not yet stamped).

---

### Step 5 — Internal Electrical Engineer Review

5.1 Review draft SLD against the load inventory (Step 1) — confirm all loads accounted for.

5.2 Verify SLD is consistent with load calculation results (Step 3).

5.3 Confirm all TBD items are clearly labeled and none are accidentally left blank.

5.4 Check that three-phase service annotation is present (REQ-SLD-009).

**Output:** Internally reviewed draft SLD; punch list of TBD items requiring resolution before IFC.

---

### Step 6 — Interdisciplinary Coordination Review

6.1 Issue draft SLD to the following for review and comment:
- Mechanical Engineer — confirm mechanical equipment electrical provisions are included (DEL-003-05 coordination)
- Structural Engineer — confirm crane circuit sizing assumptions are noted as TBD pending crane specification (DEL-002-07 coordination)
- Architect — confirm overhead door quantities and any other architectural electrical feeds (DEL-001-07 coordination)
- Crane supplier (when selected) — request electrical specification to resolve CONF-SLD-002

6.2 Incorporate responses; revise SLD to reflect confirmed data or maintain TBD where data is outstanding.

6.3 Document coordination record (date issued, responses received, items resolved/outstanding).

**Output:** Coordinated SLD with interdisciplinary review record.

---

### Step 7 — Preliminary Issue for County Approval

7.1 Issue the coordinated SLD (preliminary, unsealed) as part of the Preliminary Electrical Design package (DEL-004-01) submission to Camrose County for approval.

7.2 Await County approval per SOW-0010d. Do not issue SLD as IFC until County approval is received.

7.3 If County provides comments: revise SLD to address comments; re-submit if required.

**Output:** County-approved preliminary SLD.

---

### Step 8 — Resolve Outstanding TBD Items and Finalize

8.1 Confirm all outstanding TBD items (crane rating, door motor rating, system voltage, mechanical equipment ratings, ceiling fan rating, exhaust fan rating) are resolved from equipment specifications and coordination responses.

8.2 Incorporate confirmed values into the SLD. Remove all TBD placeholders that have been resolved. Retain TBD labels only for items that genuinely cannot be resolved at IFC stage (document reason).

8.3 Update load calculation (DEL-004-08) if any confirmed values differ from assumptions used in Step 3.

8.4 Perform final check of SLD against DEL-004-03 (Power Distribution Plans), DEL-004-05 (Receptacle Layout Plans), and DEL-004-06 (Panel Schedules) for consistency (REQ-SLD-010).

**Output:** Finalized SLD drawing — ready for P.Eng. stamp.

---

### Step 9 — P.Eng. Stamp and IFC Issue

9.1 Responsible Electrical Engineer (P.Eng. licensed in Alberta) reviews the final SLD.

9.2 Upon satisfaction that the SLD meets CEC requirements, project scope, and professional engineering standards: apply P.Eng. stamp and signature to the drawing.

9.3 Issue the stamped SLD as part of the IFC drawing package (SOW-0018).

9.4 File a copy of the stamped SLD in the project document control system and provide a copy to Camrose County (SOW-0018, SOW-0093).

**Output:** IFC-issued, P.Eng.-stamped Single-Line Diagram (DEL-004-02 final).

---

### Step 10 — Deliverable Handoff to Downstream Users

10.1 Formally transmit the IFC-stamped SLD to the following downstream users, with transmittal record:
- Electrical contractor (PKG-015 Electrical & Low-Voltage Installation) — primary construction user
- General contractor / construction manager (PKG-013 Mechanical & HVAC Installation, PKG-018 Sitework & Civil Construction) — for utility tie-in coordination and mechanical electrical provisions awareness
- Project Manager — for project document control and permit file

10.2 Confirm receipt from each recipient and record the transmittal date, recipient name, and drawing revision number in the coordination record.

10.3 If the SLD is revised after initial IFC issue, re-transmit the updated version to all recipients with a revision notice identifying changes.

**Source:** ASSUMPTION: standard construction document control practice. SOW-0018 (IFC drawings), SOW-0093 (CCC documentation). *(Added per D-001: confirmed active delivery lens identified missing handoff step after IFC issue.)*

**Output:** Transmittal records for IFC SLD distribution to all downstream users.

---

## Verification

| Check | Verification Method | Timing |
|---|---|---|
| All loads from App B (Electrical) accounted for | Load inventory audit against SLD | After Step 4 (internal review — Step 5) |
| Three-phase service annotation present | Drawing review | Step 5 |
| All dedicated circuits individually labeled | Item-by-item check against REQ-SLD-005 table | Step 5 |
| TBD items clearly labeled (not blank) | Drawing review | Step 5 and Step 8 |
| Coordinated with mechanical, structural, architectural | Coordination record on file | Step 6 |
| County approval obtained before IFC | County approval letter / email on file | Step 7 before Step 9 |
| P.Eng. stamp and signature present on IFC issue | Visual confirmation | Step 9 |
| SLD consistent with DEL-004-06 (Panel Schedules) | Cross-reference check | Step 8 |
| SLD consistent with DEL-004-08 (Calculation Package) | Cross-reference check | Step 8 |
| Load inventory completeness verified before drafting | Signed/initialed load inventory review | After Step 1, before Step 4 *(per X-002)* |
| Drawing platform/format documented | Platform selection recorded in project document register | Step 4.1 *(per A-004)* |
| Drawing numbering convention established | Numbering convention documented before title block application | Step 4.6 *(per C-003)* |
| Voltage drop calculations performed for feeder runs | Calculation record on file; SLD feeder sizes reflect results | Step 3 *(per F-002)* |
| IFC SLD transmitted to downstream users | Transmittal records with recipient confirmation on file | Step 10 *(per D-001)* |
| Safety Codes inspection readiness confirmed | SLD package (stamped drawing, revision register, coordination record) assembled and available for inspection | After Step 9 *(per X-004)* |

---

## Records

The following records shall be created and retained as evidence of this procedure:

| Record | Description | Responsible |
|---|---|---|
| Load Inventory Register | Complete load list with source references, circuit types, ratings | Electrical Engineer |
| Utility Correspondence | Written confirmation of system voltage and service capacity from local utility | Electrical Engineer |
| Coordination Record | Log of interdisciplinary review issues, dates, and resolutions | Electrical Engineer / Project Manager |
| County Approval Record | Written County approval of preliminary SLD (DEL-004-01 acceptance) | Project Manager |
| Drawing Revision Register | Drawing revision history from draft through IFC | Electrical Engineer |
| IFC Drawing — Stamped SLD | Final P.Eng.-stamped drawing, copy to County and project document control | Electrical Engineer |
| IFC Transmittal Records | Transmittal documentation for IFC SLD distribution to downstream users (PKG-015, PKG-013, PKG-018, Project Manager) with receipt confirmations | Electrical Engineer / Project Manager |

**Note:** All records shall be available for Safety Codes inspection (SOW-0084, SOW-0085) and shall be included in CCC documentation submitted to Camrose County (SOW-0093).
