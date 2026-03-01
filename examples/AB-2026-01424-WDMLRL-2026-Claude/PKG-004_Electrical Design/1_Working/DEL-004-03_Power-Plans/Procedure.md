# Procedure — DEL-004-03 Power Distribution Plans

---

## Purpose

This procedure describes the steps to produce the Power Distribution Plans drawing set (DEL-004-03) for the New North Shop addition at the West Dried Meat Lake Regional Landfill Maintenance Shop, Ferintosh, Alberta. It covers the workflow from initial information gathering through IFC drawing issue, including required coordination gates and verification checkpoints.

The output of this procedure is an Issued for Construction (IFC) power distribution drawing set, P.Eng.-stamped by an Electrical Engineer licensed in the Province of Alberta, that can be used by PKG-015 (Electrical & Low-Voltage Installation) as the governing construction document.

---

## Prerequisites

### Information Prerequisites

| Item | Source / Deliverable | Status |
|---|---|---|
| County-approved Preliminary Electrical Design | DEL-004-01 Preliminary Electrical Design | Must be complete and County-approved before IFC release |
| Single-Line Diagram (at least draft) | DEL-004-02 Single-Line Diagram | Must be developed in parallel; final coordination required |
| RFP and Appendix B (Electrical) conceptual drawing | R-01 (RFP), R-05 (App B Electrical) | Available — accessed |
| Architectural floor plans (IFC or advanced draft) | DEL-001-02 Architectural Floor Plans | Required for spatial coordination; ASSUMPTION: available at time of electrical design |
| Structural framing plans | DEL-002-03 Structural Framing Plans | Required to coordinate conduit penetrations, crane support locations |
| Mechanical equipment schedule | DEL-003-05 Mechanical Equipment Schedule | Required to confirm motor ratings and electrical connections for HVAC/exhaust equipment |
| Crane supplier specifications | PKG-016 (Crane & Lifting Equipment procurement) | Required to confirm crane circuit ratings; ASSUMPTION: available before IFC |
| Utility service information | Local utility (ATCO Electric or equivalent) | Required to confirm service voltage, capacity, and metering requirements |
| County welding equipment specifications | County / Owner | Required to confirm welding receptacle ratings (RFP §3.4; currently ASSUMPTION 50A/240V per D-009) |
| Alberta Safety Code permit application requirements | Safety Codes Officer / authority having jurisdiction | Required to confirm inspection requirements and permit conditions |

### Personnel Prerequisites

| Requirement | Notes |
|---|---|
| Electrical Engineer of Record | P.Eng. licensed in the Province of Alberta; responsible for signing and stamping all IFC drawings |
| Electrical CAD/BIM technician | ASSUMPTION: required for drawing production |
| MEP coordination lead | ASSUMPTION: required for cross-discipline coordination |

---

## Steps

### Step 1 — Collect and Review Source Information

1.1 Obtain and review the following documents:
- RFP §3.4 Design Requirements (electrical scope)
- Appendix B (Electrical) conceptual drawing — extract all load types, quantities, circuit ratings, and layout positions
- Decomposition decisions D-001 (crane terminology), D-009 (welding receptacle rating assumption)

1.2 Confirm all outstanding TBDs and ASSUMPTIONS identified in the Specification and Guidance documents, specifically:
- Service voltage (CONF-003-02): initiate utility coordination to resolve
- 20A/120V vs. 20A/240V receptacle locations (CONF-003-01): review with Owner at preliminary design
- Ceiling fan locations (CONF-003-03): resolve with Owner at preliminary design
- Crane circuit rating: obtain from crane supplier (PKG-016)

1.3 Obtain the architectural floor plan (DEL-001-02) base drawing to use as the underlay for power distribution plan sheets.

**Output:** Annotated source document set with all identified loads, circuit ratings, and open items logged.

---

### Step 1A — Utility Service Information Gate (Enrichment: F-004)

Before proceeding to Step 2 (Load Calculation), confirm that utility service information has been received:

1A.1 Verify that the local utility (ATCO Electric or equivalent) has provided:
- Confirmed service voltage (120/208V or 347/600V three-phase)
- Available service capacity
- Metering requirements
- Service entrance requirements

1A.2 If utility service information has NOT been received:
- **Do not proceed to Step 2** until service voltage is confirmed, as it affects all downstream panel and conductor sizing
- Escalate through the Project Manager to obtain utility response
- Document the date of initial utility request and all follow-up actions

1A.3 If utility service information is partially received (e.g., voltage confirmed but capacity TBD), document what is known and proceed to Step 2 with noted assumptions.

**Output:** Confirmed utility service parameters, or documented escalation if not received.

(Source: Procedure Prerequisites table lists "Utility service information" but had no gate in the step sequence; Enrichment: F-004)

---

### Step 2 — Perform Load Calculation

2.1 Tabulate all electrical loads from Step 1, including:
- Crane loads (×2, ratings per crane specs)
- Motor loads: overhead doors, compressor (40A), fire hose pump (70A), pressure washer (70A), exhaust fans, mechanical equipment (makeup air, heating, air exchanger — per DEL-003-05)
- Welding receptacle loads (50A/240V × quantity per layout; ASSUMPTION per D-009)
- Receptacle loads by type: 15A/120V, 20A/120V, 20A/240V, 30A/240V, 50A/240V
- Lighting loads: 20 × 150W LED (main shop) + 6 × (wash bay, wattage TBD) + office + utility room + parts room
- Ceiling fans (×6)

2.2 Apply applicable demand factors per the Canadian Electrical Code (Part I, as adopted by Alberta) for: welding equipment, motors, general receptacles.

2.3 Size the main service, main disconnect, sub-feeders, and panelboards based on the calculated demand load.

2.4 Document the load calculation in DEL-004-08 (Electrical Calculation Package). The panel sizes shown on DEL-004-03 must be consistent with DEL-004-08.

**Output:** Confirmed service size, panelboard sizes, and feeder sizes. Input to drawing production.

---

### Step 2B — Drawing Production Readiness Checklist (Enrichment: D-002)

Before proceeding to Step 3 (Develop Drawing Set), confirm that all critical prerequisite information items have been received or formally waived. Complete the following checklist:

| Item | Required? | Status | Waiver Authority (if waived) |
|---|---|---|---|
| Utility service voltage confirmed (Step 1A) | Yes — mandatory | TBD | Cannot be waived; must be confirmed or assumed with documented risk |
| Crane supplier specifications received (PKG-016) | Yes — for crane circuit sizing | TBD | Electrical Engineer may proceed with conservative assumption and note "subject to confirmation" |
| County welding equipment specifications received | Yes — for welding receptacle confirmation | TBD | Electrical Engineer may proceed with ASSUMPTION (50A/240V per D-009) and note "subject to confirmation" |
| Architectural floor plans available (DEL-001-02) | Yes — for drawing underlay | TBD | Cannot be waived |
| Mechanical equipment schedule received (DEL-003-05) | Yes — for mechanical equipment power | TBD | Electrical Engineer may proceed with ASSUMPTION and note "subject to confirmation" |
| Load calculation complete (Step 2) | Yes — for panel and feeder sizing | TBD | Cannot be waived |

If any mandatory item is not received, the Electrical Engineer and Project Manager must agree on whether to:
(a) Proceed with documented assumptions and accept rework risk, or
(b) Delay drawing production until the item is received.

Document the readiness decision and any waivers in the project file.

(Source: Procedure Prerequisites section; Enrichment: D-002)

---

### Step 3 — Develop Drawing Set (Draft)

3.1 Set up drawing file(s) using the architectural floor plan as the base underlay.

3.2 Locate panelboard(s) on the floor plan. Consider:
- Proximity to service entry point
- Proximity to highest-demand loads (cranes, welding stations)
- Code-required clearances
- Structural wall and column locations

3.3 Draw power distribution elements on the plan:
- Service entry point and main disconnect location
- Panelboard locations with panel designation labels
- Feeder routing from service to main panel(s)
- Sub-feeder routing from main panel(s) to sub-panels (if applicable)
- Branch circuit homerun indicators to all load locations:
  - Crane runway feeds (×2)
  - Overhead door operators (all locations)
  - Compressor (40A)
  - Fire hose pump (70A)
  - Pressure washer (70A)
  - Welding receptacle circuits (50A/240V per layout)
  - All other receptacle circuits per App B layout (15A/120V, 20A/120V, 20A/240V, 30A/240V)
  - Exhaust fan circuits
  - All lighting circuits (coordinated with DEL-004-04)
  - Ceiling fan circuits (×6, main shop)
  - Mechanical equipment feeds (per DEL-003-05 coordination)

3.4 Annotate circuit designations consistently with DEL-004-06 Panel Schedules.

3.5 Prepare drawing legend and general notes sheet including:
- Legend of all symbols used
- Applicable code references
- General notes on conduit type, conductor sizing minimums, and grounding
- Cross-reference to related deliverables (DEL-004-02, DEL-004-05, DEL-004-06)

**Output:** Draft power distribution drawing set (not yet for issue).

---

### Step 4 — Internal Coordination Review

4.1 Cross-check power plans against Single-Line Diagram (DEL-004-02): confirm all loads shown on power plans are reflected on the single-line and vice versa.

4.2 Cross-check power plans against Receptacle Layout Plans (DEL-004-05): confirm receptacle locations and circuit assignments are consistent.

4.3 Cross-check power plans against Lighting Plans (DEL-004-04): confirm all luminaire circuits are shown on power plans.

4.4 Cross-check power plans against Panel Schedules (DEL-004-06): confirm all circuit designations and ratings are consistent.

4.5 Conduct MEP coordination review with mechanical engineer (PKG-003) to confirm:
- Mechanical equipment power requirements are correctly reflected on plans
- No conflicts with HVAC ductwork routing and electrical conduit routing

4.6 Conduct plumbing coordination review with plumbing engineer (PKG-006) to confirm (Enrichment: C-004):
- Plumbing equipment requiring electrical feeds (e.g., cistern pump, wash bay pump, water heater) are identified and power requirements are documented
- No conflicts between plumbing routing and electrical conduit routing
- Plumbing equipment electrical connections are reflected on the power distribution plans
(Source: Guidance Principle 4 and Specification scope note mention plumbing coordination with PKG-006/DEL-006; previously missing from Procedure Step 4)

4.7 Conduct structural coordination review with structural engineer (PKG-002) to confirm:
- Conduit penetrations through slabs/walls are structurally acceptable
- Crane runway electrical connections do not conflict with crane support structure

4.8 Log all conflicts and resolve; update drawings as needed.

**Output:** Internally coordinated drawing set with conflict log.

---

### Step 5 — Preliminary Design Submission and County Approval

> Note: This step applies to the preliminary design milestone (DEL-004-01), which must precede final IFC issue. The power distribution plans feed into the preliminary design package.

5.1 Incorporate power distribution plan content (at schematic/design development level) into the Preliminary Electrical Design (DEL-004-01) submission.

5.2 Submit to County for review and approval per RFP §3.3.2 and SOW-0010d.

5.3 Address County comments. If County-directed changes affect power distribution plan content, update accordingly.

5.4 Obtain written County approval confirmation before proceeding to IFC finalization.

**Output:** Documented County approval of preliminary electrical design.

---

### Step 6 — IFC Finalization and P.Eng. Stamp

6.1 Incorporate all comments from Steps 4 and 5 into the drawing set.

6.2 Perform final code compliance review against applicable Alberta Safety Code/CEC requirements.

6.3 Confirm all CONF items from the Guidance Conflict Table have been resolved or formally accepted:
- CONF-003-01: 20A receptacle voltage differentiation confirmed
- CONF-003-02: Service voltage confirmed with utility
- CONF-003-03: Ceiling fan locations confirmed

6.4 Electrical Engineer of Record performs final check and applies P.Eng. stamp and signature to all IFC drawing sheets.

6.5 Assign drawing revision status: IFC (Issued for Construction) with revision date.

**Output:** P.Eng.-stamped IFC power distribution drawing set.

---

### Step 7 — Issue for Construction

7.1 Issue drawing set to the construction team (PKG-015 Electrical & Low-Voltage Installation contractor).

7.2 Submit drawing set (or relevant sheets) to the authority having jurisdiction (Alberta Safety Codes Officer) as part of the electrical permit application (DEL-009-03).

7.3 Retain a copy of the issued set in the project document management system for record.

7.4 **Rough-In Inspection Hold Point (Enrichment: X-005):**
During construction, a mandatory rough-in inspection by the Safety Codes Officer (SCO) must occur before any electrical work is concealed (e.g., before drywall installation over wiring, before concrete pour over in-slab conduit). This is a mandatory milestone under Alberta Safety Codes.
- The Electrical Contractor shall request SCO rough-in inspection at the appropriate construction stage
- Electrical work shall NOT be concealed until the SCO rough-in inspection is passed or conditionally approved
- The power distribution plans should include a general note identifying this hold point for the contractor's awareness
- Source: ASSUMPTION — Alberta Safety Codes Act requires rough-in inspection before concealment of electrical work; specific regulation reference **TBD** (location TBD in Safety Codes Act)
- Responsible parties: Safety Codes Officer, Electrical Contractor, Project Manager

7.5 **Final Inspection:**
Upon completion of electrical installation, request SCO final inspection. Address any deficiencies per the inspection report guidance in Guidance (see "Inspection Report Content and Deficiency Tracking").

**Output:** Issued IFC drawing set in the hands of the installation contractor and Safety Codes authority; rough-in and final inspection hold points identified.

---

## Verification

| Check | Method | When |
|---|---|---|
| All identified loads from App B (Electrical) are shown on plans | Checklist comparison against App B load list | After Step 3 draft; before IFC issue |
| Circuit designations match Panel Schedules (DEL-004-06) | Cross-check drawing circuit labels against panel schedule | After Step 4 coordination |
| All drawings bear P.Eng. stamp and signature | Visual review of all IFC sheets | Step 6.4 |
| County approval of preliminary design documented | Written approval on file | Step 5.4 — before IFC issue |
| Safety Code permit application submitted | Permit application tracking | Step 7.2 |
| No open CONF items from Guidance Conflict Table | Review of Conflict Table status | Step 6.3 — before stamp |
| Feeder and panel sizes consistent with DEL-004-08 load calculation | Engineer cross-check: confirm that every feeder size and panel rating on DEL-004-03 matches DEL-004-08 load calculation output; pass/fail criterion: no discrepancy between plans and calculation. Electrical Engineer of Record to sign off before P.Eng. stamp (Enrichment: X-004) | After Step 2 and Step 6 |
| Crane supplier specifications received and incorporated | Confirm crane specs (from PKG-016) have been formally received; verify crane circuit sizing on power plans matches crane manufacturer requirements; document confirmation before IFC finalization (Enrichment: C-003) | Before Step 6 (IFC Finalization) |
| Mechanical equipment electrical ratings confirmed | Confirm mechanical equipment electrical ratings (from DEL-003-05) have been formally received and match what is shown on the power plans; cross-check against mechanical schedule (Enrichment: X-003) | After Step 4.5 (MEP coordination); before Step 6 |
| Utility service information confirmed | Confirm utility service voltage, capacity, and metering requirements have been received and are reflected on plans (see Step 1A gate) (Enrichment: F-004) | Before Step 2 (Load Calculation) |
| Rough-in inspection hold point identified | Confirm power distribution plans include a general note identifying the SCO rough-in inspection hold point (Enrichment: X-005) | Step 6 (before P.Eng. stamp) |
| Plumbing coordination complete | Confirm plumbing equipment electrical feeds are reflected on power plans per Step 4.6 coordination with PKG-006 (Enrichment: C-004) | After Step 4.6 |

---

## Records

| Record | Responsible Party | Retention |
|---|---|---|
| IFC Power Distribution Drawing Set (stamped) | Electrical Engineer / Design-Builder | Project duration + 2-year guarantee period; ASSUMPTION: per Alberta records retention requirements |
| County preliminary design approval letter/email | Project Manager | Project duration + 2-year guarantee period |
| MEP coordination meeting minutes / review log | MEP Coordination Lead | Project duration |
| Electrical permit application and issued permit | Project Manager / Electrical Contractor | Project duration + 2-year guarantee period |
| Inspection reports (rough-in, final) | Electrical Contractor / Project Manager | Project duration + 2-year guarantee period |
| Conflict resolution log (CONF items) | Electrical Engineer | Project duration |
| Drawing revision history | Electrical Engineer / CAD Technician | Project duration |
