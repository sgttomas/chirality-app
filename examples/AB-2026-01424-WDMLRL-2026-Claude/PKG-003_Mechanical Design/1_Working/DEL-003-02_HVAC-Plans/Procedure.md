# Procedure — DEL-003-02 HVAC Layout Plans

---

## Purpose

This procedure describes the steps to produce the HVAC Layout Plans drawing set (DEL-003-02) for the WDMLRL Maintenance Shop Addition. It covers the workflow from design input collection through IFC drawing issuance. It is intended for use by the Mechanical Engineer and their team responsible for PKG-003 (Mechanical Design).

The procedure supports SOW-0013 (complete final mechanical design — HVAC, ventilation, exhaust systems) and contributes to OBJ-001 (code-compliant functional shop), OBJ-003 (complete IFC documentation), and OBJ-004 (mechanical systems commissioned to operational readiness).

---

## Prerequisites

### Upstream Design Inputs (Required Before IFC Layout Can Be Finalized)

| Input | Source | Status |
|---|---|---|
| Approved Preliminary Mechanical Design (DEL-003-01) | PKG-003 — Mechanical Design | Required: County approval must be received before IFC (R-01 §3.3.2; SOW-0010c) |
| Geotechnical Report (DEL-008-01) | PKG-008 — Geotech & Surveying | Required: confirms soil/site conditions affecting utility tie-ins |
| Architectural Floor Plans (DEL-001-02) | PKG-001 — Architectural Design | Required: base drawing for HVAC layout (room dimensions, door locations, structural grid) |
| Structural Framing Plans (DEL-002-03) | PKG-002 — Structural Design | Required: confirm crane clearances, equipment support locations, roof penetration feasibility |
| Electrical Plans (DEL-004-03, DEL-004-04) | PKG-004 — Electrical Design | Required: coordinate ceiling fan and equipment power locations |
| Mechanical Calculation Package (DEL-003-06) | PKG-003 — Mechanical Design | Required: equipment sizing governs unit selection and layout |
| Mechanical Equipment Schedule (DEL-003-05) | PKG-003 — Mechanical Design | Required: equipment tags and dimensions for layout |
| RFP and Appendix B | R-01, R-04 | Available — design basis documents |

### References Required

| Reference | Purpose |
|---|---|
| R-01 AB-2026-01424-WDMLRL RFP.pdf | Design requirements §3.4; scope §3.3.2 |
| R-04 AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan — equipment locations |
| National Building Code of Canada (Alberta Edition) | Code compliance — location TBD |
| Alberta Safety Codes (applicable Safety Codes) | Safety code compliance — location TBD |
| ASHRAE 62.1 | Ventilation rates — location TBD |
| ASHRAE 90.1 | Energy efficiency requirements — location TBD |
| CSA W117.2 | Welding fume ventilation requirements — location TBD |
| Firm's HVAC drawing standards / CAD standards | Drawing production — firm-specific. Note [A-004]: no firm-specific CAD/BIM standard has been identified in the deliverable set; this reference is external to the deliverable documents. Confirm applicable firm standard or note that it is outside this deliverable's scope. |

### Tools and Resources

| Tool/Resource | Purpose |
|---|---|
| CAD software (AutoCAD, Revit MEP, or equivalent) | Drawing production |
| HVAC load calculation software (e.g., Carrier HAP, Trane TRACE, or manual per ASHRAE) | Sizing support (feeds into DEL-003-06) |
| P.Eng. with Alberta APEGA registration | Signing authority for IFC |

---

## Steps

### Step 1 — Confirm County Approval of Preliminary Design

**Action:** Confirm that DEL-003-01 (Preliminary Mechanical Design) has received written County approval before proceeding to IFC layout production.

- If approval is pending: pause IFC production; proceed with preliminary-level layout development only.
- If approved: proceed to Step 2.

**Record:** Copy of County approval communication.

**Source:** R-01 §3.3.2 (SOW-0010c).

---

### Step 2 — Collect and Confirm Base Information

**Action:** Collect all upstream inputs listed in Prerequisites. Confirm the following are current and coordinated:

2a. Obtain current architectural floor plan (DEL-001-02) — confirm room names, dimensions, door locations, structural grid reference match Appendix B conceptual intent.

2b. Obtain structural framing plans (DEL-002-03) — identify crane rail locations and travel envelopes; confirm available overhead clearance for ductwork and equipment.

2c. Confirm equipment sizing from DEL-003-06 — obtain physical dimensions (width, depth, height, weight) of all HVAC units to be shown on layout.

2d. Confirm any County-issued RFP addenda (R-02 Addendum 1 and any subsequent addenda) have been reviewed for mechanical scope changes.

**Record:** Input drawing revision log; confirmation memo or email.

**Source:** R-01 §1.0, §3.3.2; Decomposition Step 1.

---

### Step 3 — Establish Drawing Sheet Set and Title Block

**Action:** Set up the drawing sheet set in the firm's CAD/BIM environment:

3a. Create a drawing index listing all HVAC layout plan sheets (minimum: main shop plan, wash bay/ancillary plan, service pit plan, notes/legend sheet).

3b. Apply standard title block including: project name (WDMLRL Maintenance Shop Addition), Owner (Camrose County), drawing title, drawing number, revision block, scale, and P.Eng. signature block.

3c. Reference the architectural floor plan as an underlay/base.

**Record:** Drawing index sheet (Sheet 0 or title sheet).

**Source:** ASSUMPTION per standard drawing production practice; R-01 §3.3.2 (IFC requirement).

---

### Step 4 — Place HVAC Equipment on Layout

**Action:** Place all HVAC equipment on the layout in coordination with the architectural and structural base. For each system:

**4a — Heating System (REQ-001):**
- Position high-recovery heating unit(s) in the main shop to achieve coverage of both repair bays and general shop area.
- Position units clear of crane travel envelopes (two 5-tonne cranes in main shop).
- Show heating provisions for wash bay, office, parts room, utility room, and mezzanine (if applicable).
- Assign equipment tags cross-referenced to DEL-003-05 (Equipment Schedule).

**4b — Air Exchanger (REQ-002):**
- Position high-volume air exchanger unit; show supply and exhaust connections (penetration points).
- Coordinate roof or wall penetration location with PKG-002 (Structural).

**4c — Makeup Air Unit / MUA (REQ-003):**
- Position MUA unit consistent with Appendix B conceptual location.
- Show supply discharge direction and indicate gas/electrical connection points.
- Coordinate roof/wall penetration with PKG-002.

**4d — Equipment Exhaust — Repair Bays (REQ-004):**
- Show exhaust hose drop/reel locations in each repair bay (minimum one per bay).
- Show exhaust fan locations (roof or wall) with connection to drop/reel.
- Coordinate penetrations with PKG-002.

**4e — Welding Station Exhaust (REQ-005):**
- Show welding exhaust capture device (arm/hood) at the welding station location (north-east area per App B).
- Show fan and exhaust discharge location.

**4f — Ceiling Fans (REQ-006):**
- Show exactly 6 ceiling fans distributed across main shop area.
- Note: Power by PKG-004 (Electrical Design); shown here for coordination and spatial reference.

**4g — Service Pit Ventilation (REQ-007):**
- Show supply and/or exhaust ventilation for below-grade service pit.
- Indicate connection to main exhaust or dedicated pit exhaust fan.

**4h — Wash Bay Ventilation (REQ-012):**
- Show ventilation supply and exhaust for enclosed wash bay.
- Confirm equipment rated for wash-down environment.

**Record:** Layout drawings in CAD/BIM with all equipment tagged.

**Source:** R-01 §3.4 (SOW-0035–SOW-0040, SOW-0028); R-04 App B.

---

### Step 5 — Coordinate with Other Disciplines

**Action:** Circulate the HVAC layout drawing set to the following disciplines for coordination review:

| Discipline | Coordination Item | Deliverable |
|---|---|---|
| Structural Engineer (PKG-002) | Roof/wall penetrations; equipment support loads; crane clearance | DEL-002-03 |
| Electrical Engineer (PKG-004) | Ceiling fan power locations; HVAC unit power connections | DEL-004-03, DEL-004-04 |
| Plumbing Engineer (PKG-006) | Gas connection points for heating/MUA; condensate drain routing | DEL-006-02 |
| Architect (PKG-001) | Confirm room functions and ceiling heights match assumptions | DEL-001-02 |

**Action:** Record all coordination comments received; revise layout to resolve conflicts before IFC issue.

**Record:** Coordination review comment log; revised drawing revision history. Note [D-003]: the coordination review comment log should use a defined format or template to ensure discipline sign-offs are recorded consistently. TBD: establish required fields for the comment log (e.g., discipline, reviewer name, date, comment, response, resolution status, sign-off). This is necessary for traceable coordination records per OBJ-003 (complete IFC documentation).

**Source:** ASSUMPTION per standard multi-discipline design coordination practice.

---

### Step 6 — Add Drawing Notes and Legend

**Action:** Complete drawing notes, general legend, and system abbreviations on all HVAC layout sheets:

6a. Add general notes covering applicable codes (Alberta Building Code, Safety Codes, ASHRAE references).

6b. Add legend showing all HVAC symbols used.

6c. Add system abbreviations table (e.g., MUA = Makeup Air Unit, AHU = Air Handling Unit, etc.).

6d. Cross-reference equipment tags to Mechanical Equipment Schedule (DEL-003-05).

**Record:** Notes and legend completed on all drawing sheets.

**Source:** ASSUMPTION per standard IFC drawing practice.

---

### Step 7 — Internal Review (QA Check)

**Action:** Conduct internal drawing quality check before P.Eng. review:

7a. Confirm all six required systems are shown (heating, air exchanger, MUA, equipment exhaust, welding exhaust, ceiling fans).

7b. Confirm service pit ventilation and wash bay ventilation are shown.

7c. Confirm ceiling fan count = 6 (REQ-006).

7d. Confirm equipment tags match DEL-003-05 (Equipment Schedule).

7e. Confirm no ductwork or equipment conflicts with crane clearances.

7f. Confirm all roof/wall penetrations are flagged for structural coordination.

7g. Cross-reference HVAC layout against DEL-003-03 (Ductwork & Distribution Plans) and DEL-003-04 (Exhaust System Plans) to confirm consistency between companion deliverables — verify that equipment locations, duct routing origins, and exhaust system connections shown on the HVAC layout are consistent with the detail shown in companion drawings. [X-005]

**Record:** Internal QA checklist sign-off.

**Source:** ASSUMPTION per QC obligation (R-01 §1.0; SOW-0089).

---

### Step 8 — P.Eng. Review and Stamp

**Action:** Submit drawing set to the signing Mechanical Engineer (P.Eng., Alberta APEGA registration) for review and IFC stamp:

8a. P.Eng. confirms drawings reflect approved design intent (consistent with DEL-003-01 approval).

8b. P.Eng. confirms code compliance representation is appropriate.

8c. P.Eng. signs and stamps all IFC sheets.

**Record:** IFC drawing set with P.Eng. stamp on each sheet.

**Source:** R-01 §3.3.2 (SOW-0018).

---

### Step 9 — Issue IFC Drawing Set

**Action:** Issue the IFC HVAC Layout Plans drawing set:

9a. Update revision block to IFC status.

9b. Provide copies to Owner (Camrose County) via the County project manager.

9c. Provide copies to all subcontractors requiring HVAC layout for construction (PKG-013 — Mechanical & HVAC Installation).

9d. File final IFC set in project document control system.

**Record:** Transmittal records; document control log entry.

**Source:** R-01 §3.3.2 (SOW-0018, SOW-0084, SOW-0085).

---

## Verification

| Check | Verification Action | Pass Criterion |
|---|---|---|
| County approval gate [D-002] | Confirm written County approval of DEL-003-01 (Preliminary Mechanical Design) has been received before proceeding to IFC-level work (Step 2) | County approval documentation on file; date recorded |
| All required systems shown | Count systems on layout against REQ-001 through REQ-007, REQ-012, and REQ-013 through REQ-016 where applicable | All required system types present (8 base + applicable new requirements) |
| Ceiling fan quantity | Count ceiling fans on layout | Exactly 6 fans in main shop area |
| P.Eng. stamp | Check each IFC sheet | Stamp and signature present on all sheets |
| Equipment tags | Cross-check tags against DEL-003-05 | All layout equipment tags match schedule |
| Crane clearance | Compare HVAC layout against structural crane envelope drawings | No conflicts identified |
| Coordination sign-offs | Review coordination comment log | All conflicts resolved or recorded as TBD with action assigned |
| Consistency with preliminary | Compare layout to approved DEL-003-01 | No unreported deviations from approved preliminary |
| Code reference notes | Check drawing notes for applicable code citations | Applicable codes cited on drawings |
| Companion deliverable consistency [X-005] | Cross-reference HVAC layout against DEL-003-03 and DEL-003-04 | Equipment locations and routing origins consistent across companion drawings |

---

## Records

| Record | Created At | Retained By | Retention Period | Format |
|---|---|---|---|---|
| County approval confirmation (DEL-003-01) | Step 1 | Mechanical Engineer / Project Manager | TBD — per project document retention policy [E-004] | TBD |
| Input drawing revision log | Step 2 | Mechanical Engineer | TBD [E-004] | TBD |
| Drawing index / title sheet | Step 3 | Mechanical Engineer / Document Control | TBD [E-004] | TBD |
| Coordination review comment log | Step 5 | Mechanical Engineer | TBD [E-004] | TBD — establish defined format per [D-003] |
| Internal QA checklist | Step 7 | Mechanical Engineer | TBD [E-004] | TBD |
| IFC drawing set with P.Eng. stamp | Step 8 | Mechanical Engineer / Document Control | TBD [E-004] | TBD |
| IFC transmittal records | Step 9 | Project Manager / Document Control | TBD [E-004] | TBD |
| Issued drawing set (County copy) | Step 9 | Owner (Camrose County) | TBD [E-004] | TBD |

**Note [E-004]:** Retention periods and format requirements for all QA records are TBD. The Project Manager / Owner should establish a document retention policy specifying minimum retention duration (e.g., project duration + warranty period, or per Alberta regulatory requirements) and required formats (e.g., PDF/A for long-term archival, native CAD for editable copies).
