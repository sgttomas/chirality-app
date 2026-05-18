# Procedure: DEL-004-07 Low-Voltage System Plans

---

## Purpose

This procedure describes the steps to produce the Low-Voltage System Plans drawing set (DEL-004-07) for the New North Shop Addition at the West Dried Meat Lake Regional Landfill. The output is an IFC Drawing Set, signed and stamped by a P.Eng. licensed in Alberta, showing security camera wiring and 2-way radio antenna wire routing, ready for use by the installation contractor (DEL-015-05).

---

## Prerequisites

### Upstream Dependencies
The following must be sufficiently advanced or complete before final IFC drawings can be produced:

| Prerequisite | Status Trigger | Deliverable |
|---|---|---|
| Preliminary Electrical Design (including preliminary low-voltage scope) reviewed and approved by County | County written approval received | DEL-004-01 |
| Architectural Floor Plans available for coordination | IFC or coordinated draft available | DEL-001-02 |
| Structural drawings available (concrete structure, crane beams, penetration locations) | Coordinated draft available | DEL-002-03, DEL-002-07 |
| Power Distribution Plans coordinated | Coordinated draft available | DEL-004-03 |
| Geotechnical report available (for foundation context affecting underground conduit, if applicable) | Report issued | DEL-008-01 |
| Safety Code permit pathway confirmed with AHJ | Pre-application consultation complete | DEL-009-03 |

### Required References
| Reference | Purpose |
|---|---|
| AB-2026-01424-WDMLRL_RFP.pdf (§3.3.2, §3.4) | Scope of work and design requirements |
| AB-2026-01424-Appendix_B__Electrical_.pdf | Conceptual electrical layout and notes (primary source for low-voltage items) |
| Applicable Alberta Safety Codes (Canadian Electrical Code Part I, as adopted) | Code compliance — location TBD; obtain current adopted edition |
| CCDC 14–2013 | Contract framework |
| Decomposition: WDMLRL_Decomposition_Claude.md (SOW-0064, SOW-0065, OBJ-005) | Scope confirmation |

### Qualified Personnel
- Electrical Engineer (P.Eng. licensed in Alberta) — responsible for design, drawings, and IFC stamp
- CAD/drafting technician (as applicable)

---

## Steps

### Step 1 — Confirm Low-Voltage Scope with County at Preliminary Design

**Action:** During preparation of DEL-004-01 (Preliminary Electrical Design), present the proposed low-voltage scope to the County for review and approval. Confirm:
- Camera system: quantity of cameras, technology (IP vs. analog), recording infrastructure
- Radio antenna: number of antenna points, antenna system type, interior coverage approach
- Any additional low-voltage systems (fire alarm, data/network, access control, intercom) required by code or County program
- Scope boundary for Old North Shop renovation areas: confirm whether low-voltage systems are required in renovated areas or excluded from DEL-004-07

**Output:** Written County approval of preliminary electrical design confirming low-voltage scope (per SOW-0010d). The approval record shall explicitly document which low-voltage systems were confirmed and which were excluded, with exclusion rationale where applicable (see Specification REQ-007-05 and REQ-007-08 verification requirements).

**Source:** RFP §3.3.2; SOW-0010d; Guidance CON-007-01.

---

### Step 2 — Obtain Applicable Code Requirements and Permit Information

**Action:**
1. Identify the current edition of the Canadian Electrical Code Part I (CSA C22.1) as adopted in Alberta for low-voltage installations.
2. Confirm with the Authority Having Jurisdiction (AHJ) whether a separate low-voltage/communications permit is required or whether coverage falls under the general electrical Safety Code permit.
3. Identify any Alberta Safety Code requirements specific to industrial facilities for security/communications cabling (e.g., installation methods, firestopping, equipment room requirements).

**Output:** Code reference list and permit pathway confirmed.

**Source:** RFP §3.3.2; SOW-0007, SOW-0009; REQ-007-04.

---

### Step 3 — Gather Coordination Information

**Action:**
1. Obtain coordinated architectural floor plans (DEL-001-02) showing wall/partition layout, room boundaries, door and window locations.
2. Obtain structural drawings showing crane beam locations, concrete column locations, and any reserved penetration sleeve locations.
3. Obtain power distribution plan (DEL-004-03) to identify occupied conduit zones and panel room locations.
4. Identify ceiling height constraints: main shop has 35' ceiling (RFP §3.4; App B-Elec); confirm clearances under crane travel envelope (5-tonne cranes on trolley, App B-Elec).
5. Identify ceiling fan locations (6 fans, main shop) and exhaust fan locations to avoid routing conflicts.

**Output:** Marked-up base plan with constraints, crane envelope, and occupied zones noted.

**Source:** App B-Elec; RFP §3.4; SOW-0040, SOW-0059, SOW-0066, SOW-0067; REQ-007-06.

---

### Step 4 — Design Low-Voltage System Layout

**Action:**
1. Determine camera coverage zones for each area of the facility (main shop, wash bay, parts room, office, utility room, exterior approaches — TBD per confirmed scope).
2. Select camera locations that achieve coverage requirements without conflicting with crane travel, ceiling fans, or high bay light fixtures (5 rows of 4 in main shop; 2 rows of 3 in wash bay — App B-Elec).
3. Design conduit/cable pathway from each camera location to the head-end equipment location (TBD — NVR/DVR room location not specified in available sources).
4. Design 2-way radio antenna wiring pathway from antenna termination point(s) to radio equipment location(s). Account for potential RF attenuation through concrete structure (RFP §3.4 — concrete structure with 35' ceiling).
5. Confirm conduit sizing, fill calculations, and cable type per applicable CEC requirements.
6. If additional low-voltage systems are confirmed in Step 1, incorporate into the layout.

**Output:** Preliminary low-voltage plan showing camera and antenna routing, equipment locations.

**Source:** App B-Elec; SOW-0064, SOW-0065; REQ-007-01, REQ-007-02, REQ-007-06.

---

### Step 5 — Prepare Drawing Set

**Action:**
1. Produce plan view drawing(s) at appropriate scale showing:
   - Security camera wiring routes, conduit sizes, termination points
   - 2-way radio antenna wire routes, conduit sizes, antenna and equipment locations
   - Any additional confirmed low-voltage systems
   - Low-voltage legend and general notes
   - Code reference notes
2. Coordinate with other PKG-004 drawings to confirm no conflicts with power distribution, lighting, or receptacle layouts.
3. Coordinate with architectural and structural drawing sets to confirm penetration locations and wall mounting details.
4. Incorporate firestopping and penetration details as required by code:
   - a. Identify all locations where low-voltage conduit/cable penetrates fire-rated walls, floors, or ceilings.
   - b. Specify firestopping materials and methods per applicable Alberta Building Code and CEC requirements.
   - c. Document firestopping locations on the drawing set (detail or schedule).
   - d. Verify firestopping design compliance with applicable code requirements before IFC issue.

**Output:** Complete draft drawing set for internal review, including firestopping details.

**Source:** REQ-007-01 through REQ-007-06; App B-Elec.

---

### Step 6 — Internal Review and Coordination

**Action:**
1. Conduct internal electrical engineer review of all drawings for completeness, code compliance, and consistency with the balance of the PKG-004 drawing set.
2. Conduct multi-discipline coordination review with architectural and structural design team to confirm no routing conflicts.
3. Resolve any conflicts identified. If conflicts cannot be resolved with available information, flag for County consultation.
4. Update drawings to reflect resolution of review comments.

**Output:** Reviewed and coordinated drawing set; conflict log resolved or documented.

**Source:** RFP §3.3.2; SOW-0018; REQ-007-06.

---

### Step 7 — Issue for Construction (IFC)

**Action:**
1. Obtain P.Eng. stamp and signature on all sheets of the low-voltage system plans.
2. Issue the drawing set as IFC at the same time as, or coordinated with, the balance of the PKG-004 IFC drawing set.
3. Confirm County has received the IFC set and that the County project manager has been notified.

**Output:** IFC-stamped Low-Voltage System Plans drawing set.

**Source:** RFP §3.3.2; SOW-0018; REQ-007-03.

---

### Step 8 — Support Construction and Inspections

**Action:**
1. Submit all applicable inspection requests to the AHJ (Safety Code inspection for low-voltage rough-in and final). Ensure County representative is notified and present at inspections. Note: whether low-voltage inspections are separate from or combined with general electrical inspections depends on the permit category determination (see Guidance §Permit Pathway).
2. Provide copies of all completed inspection reports to the County.
3. Issue drawing revisions as required to address field conditions or inspection findings. Maintain IFC revision control per project-level revision control procedure (TBD — reference or establish a revision control standard including: revision numbering convention, RFI tracking method, revision issue log, and distribution protocol). Each revision shall be logged in the drawing revision log.

**Output:** Completed inspection reports; revised IFC drawings as needed (RFI/revision log maintained per revision control procedure).

**Source:** RFP §3.3.2; SOW-0084, SOW-0085; REQ-007-07.

---

## Verification

| Check | Method | Timing |
|---|---|---|
| All required low-voltage systems shown on drawings | Drawing completeness review against confirmed scope (Step 1 output) | Prior to IFC issue |
| Camera wiring routes fully depicted | Plan view review — all cameras connected to head-end | Prior to IFC issue |
| Antenna wire routing fully depicted | Plan view review — all antenna points connected to radio equipment | Prior to IFC issue |
| No routing conflicts with structural, mechanical, or electrical systems | Coordination review sign-off (formal sign-off record documenting clearance) | Prior to IFC issue |
| Firestopping locations identified and detailed | Review of firestopping schedule/details against fire-rated assembly locations | Prior to IFC issue |
| Conduit fill calculations comply with CEC | Review of conduit fill calculations for all low-voltage conduit runs | Prior to IFC issue |
| P.Eng. stamp on all IFC sheets | Visual confirmation on each sheet | At IFC issue |
| Safety Code compliance | AHJ inspection passed | During/after construction |
| County inspection attendance and reports | Inspection report copies on file | During construction |

---

## Records

The following records shall result from execution of this procedure:

| Record | Owner | Retention |
|---|---|---|
| County written approval of preliminary electrical design (low-voltage scope confirmed) | Project Manager | Project file |
| AHJ permit(s) for low-voltage/electrical installation | Project Manager | Project file |
| IFC drawing set (stamped) — DEL-004-07 | Electrical Engineer / Project Manager | Project file + County handoff |
| Coordination review log/comments | Electrical Engineer | Project file |
| Inspection requests submitted to AHJ | Project Manager | Project file |
| Completed inspection reports (copies to County) | Project Manager | Project file + County |
| Drawing revision log (RFI register) | Electrical Engineer / Project Manager | Project file |
