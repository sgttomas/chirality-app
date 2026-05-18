# Procedure — DEL-012-03: Office Space

**Document Type:** Procedure (operational)
**Deliverable ID:** DEL-012-03
**Package:** PKG-012 — Interior Construction & Fit-Out
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Revision:** R2 — 2026-02-26 (Pass 3 — Semantic Lensing Enrichment)
**Status:** SEMANTIC_READY

---

## Purpose

This procedure describes the steps to produce (construct and complete) the DEL-012-03 Office Space within the new north shop addition, from design coordination through construction completion and handover. It is intended to guide the General Contractor responsible for PKG-012 Interior Construction & Fit-Out.

**Source:** _CONTEXT.md; WDMLRL_Decomposition_Claude.md; RFP §2.14, §3.3.2

---

## Prerequisites

### Upstream Dependencies (must be satisfied before work can proceed)

| Prerequisite | Provider | Status |
|---|---|---|
| Facility structural shell complete in office area (walls, roof, concrete floor slab) | PKG-011 — General Contractor (Building Structure & Envelope) | TBD |
| IFC Architectural Drawings approved and P.Eng.-stamped (floor plans, finish schedule, reflected ceiling plans, door/window schedule) | PKG-001 — Architect | TBD |
| IFC Electrical Drawings approved and P.Eng.-stamped (office receptacles, lighting, low-voltage layout) | PKG-004 — Electrical Engineer / PKG-015 | TBD |
| IFC Mechanical Drawings approved and P.Eng.-stamped (HVAC zone for office) | PKG-003 — Mechanical Engineer / PKG-013 | TBD |
| Building permit obtained | General Contractor | TBD |
| Safety Code permits obtained (building, electrical, mechanical as applicable) | General Contractor | TBD |
| County Preliminary Design approval received | General Contractor / Architect | TBD |

**Source:** RFP §3.3.2; _DEPENDENCIES.md External Dependencies; WDMLRL_Decomposition_Claude.md OBJ-003

### Required Reference Documents

| Document | Reference ID |
|---|---|
| IFC Architectural Floor Plans | PKG-001 output |
| IFC Architectural Finish Schedule | PKG-001 output |
| IFC Reflected Ceiling Plans | PKG-001 output |
| IFC Door & Window Schedule | PKG-001 output |
| IFC Electrical Drawing (office area) | PKG-004 / PKG-015 output |
| IFC Mechanical / HVAC Drawing (office zone) | PKG-003 / PKG-013 output |
| AB-2026-01424-WDMLRL RFP.pdf | R-01 |
| AB-2026-01424-Appendix B (Shop).pdf (conceptual reference) | R-04 |
| AB-2026-01424-Appendix B (Electrical).pdf (conceptual reference) | R-05 |

---

## Steps

### Phase 1 — Design Coordination (Pre-Construction)

**Step 1.1 — Confirm Office Scope Boundaries**
Review IFC architectural, mechanical, and electrical drawings to confirm the office footprint, partition locations, ceiling height, and interface boundaries with PKG-013 (HVAC) and PKG-015 (Electrical). Resolve the scope boundary question for electrical rough-in (see Guidance.md Conflict Table CONF-001) with the project team and document in contractor scope documents.

**Step 1.2 — Review IFC Drawings for Office**
Confirm the following are defined in IFC documents before mobilizing for office fit-out:
- Partition locations and types
- Floor finish specification
- Ceiling finish / suspended ceiling specification and height
- Door type, size, and hardware (from door/window schedule)
- Electrical outlet types and locations (15A/120V; data points)
- Lighting fixture location and mounting height
- HVAC register/supply/return locations and penetration sizes
- Accessibility provisions (door widths, threshold details)

**Step 1.3 — Pre-Construction Coordination Meeting**
Conduct a coordination meeting with PKG-013 (HVAC) and PKG-015 (Electrical) subcontractors to align on sequencing, penetration locations, and scope boundaries within the office area. Document agreed sequencing.

**Source:** RFP §3.3.2; RFP §3.1 (coordinate through County project manager); ASSUMPTION (coordination meeting as standard practice)

---

### Phase 2 — Construction (Interior Fit-Out)

**Step 2.1 — Confirm Shell Readiness**
Verify that the structural shell in the office area is complete and suitable for interior work. **Measurable readiness criteria (TBD — coordinate with PKG-011 for shell readiness acceptance criteria):** [Lensing: F-003]
- Concrete floor slab poured and cured to specified strength (TBD — minimum compressive strength per structural engineer specification)
- Exterior walls and roof complete and weathertight (no standing water, no active leaks)
- Any structural elements above the office zone (mezzanine framing, if applicable) in place and structurally complete
- Floor slab level and within tolerance for finish application (TBD — flatness/levelness specification per IFC architectural drawings)

**Resolution trigger:** Coordinate with PKG-011 General Contractor for documented shell readiness acceptance criteria before commencing interior fit-out.

**Step 2.2 — Lay Out Partitions**
Mark partition locations on the floor slab in accordance with the IFC architectural floor plan. Confirm dimensions against the IFC drawings and verify alignment with adjacent spaces (Parts Room DEL-012-01, Utility Room DEL-012-02).

**Step 2.3 — Install Partition Framing**
Install interior partition framing (stud type, spacing, and blocking per IFC architectural drawings and applicable Alberta Building Code requirements). Provide blocking for door frames, signage, and any wall-mounted fixtures per IFC drawings.

**Step 2.4 — MEP Rough-In Coordination**
Coordinate with PKG-013 (HVAC) for duct penetrations, register blocking, and thermostat wiring chase locations within partitions and ceiling. Coordinate with PKG-015 (Electrical) for conduit rough-in, outlet boxes, lighting junction boxes, and data/communications conduit within the office (subject to scope boundary resolution per CONF-001). Do not close walls until MEP rough-in inspections are passed.

**Step 2.5 — Install Door Frames and Rough Openings**
Install door frames and confirm rough opening dimensions per the IFC door/window schedule. Ensure door widths comply with accessibility requirements.

**Step 2.5A — Install Partition Insulation (if required by IFC design) [Lensing: C-003]**
If the IFC architectural design specifies acoustic or thermal insulation within office partitions, install insulation in partition cavities after MEP rough-in coordination (Step 2.4) and before closing walls (Step 2.6). Insulation type and R-value per IFC architectural specification (TBD). **Note:** Step 3.1 references "insulation if applicable" in the inspection context; this step provides the corresponding construction action.

**Step 2.6 — Close Partition Walls**
Install wall finish substrate (drywall or equivalent per IFC finish schedule) on both faces of partitions after MEP rough-in inspections are complete and insulation is installed (if applicable per Step 2.5A). Apply tape, mud, and finish to the level specified in the IFC finish schedule.

**Step 2.7 — Install Ceiling System**
Install the ceiling finish system per the IFC reflected ceiling plans. Coordinate HVAC register, lighting fixture, and any sprinkler (ASSUMPTION: if required by Alberta Building Code for this occupancy — see Specification.md REQ-014) locations with the ceiling grid or finish.
**HOLD POINT [Lensing: A-004]:** Do not close the ceiling system until HVAC rough-in above the ceiling plane is inspected and approved (analogous to the wall closure hold point in Step 2.4). Confirm that all above-ceiling MEP work (HVAC ductwork, register connections, electrical junction boxes, sprinkler piping if applicable) is complete and inspected before installing ceiling tiles/panels or finishing the ceiling surface.

**Step 2.8 — Install Floor Finish**
Install the floor finish per the IFC finish schedule after wall and ceiling work is substantially complete and the area is protected from subsequent trade damage.

**Step 2.9 — Install Lighting Fixture**
Install 1× 8' LED fixture per the IFC electrical drawing and SOW-0054. (If scope boundary assigns this to PKG-015, ensure PKG-015 has completed installation before proceeding to final inspection — coordinate per Step 1.3 outcome.)

**Step 2.10 — Install Electrical Devices and Data Points**
Install 15A/120V receptacles and data/communications outlets per IFC electrical and low-voltage drawings. (Scope boundary with PKG-015 applies — confirm per Step 1.1 outcome.)

**Step 2.11 — Install Door Leaf and Hardware**
Install the door leaf and hardware per the IFC door/window schedule and architectural specification. Confirm accessibility compliance (lever hardware, door closer if required, threshold per accessibility standard).

**Step 2.12 — Install Safety and Accessibility Features**
Install any required exit signage, emergency lighting, fire extinguisher mounting (ASSUMPTION: per Alberta Building Code and Fire Code requirements — locations TBD in IFC drawings), and accessibility-related features per IFC drawings.

**Source:** _CONTEXT.md Scope; Specification.md REQ-001 through REQ-014; RFP §3.3.2; ASSUMPTION for specific construction sequence details where IFC drawings are not yet available

---

### Phase 3 — Inspection and Verification

**Step 3.1 — Request Interim Inspections**
Submit all required inspection requests to the applicable Safety Code authority at the appropriate construction stages (framing, rough-in, insulation if applicable, final). Ensure County project representative is notified and present at all inspections per RFP §3.3.2 and SOW-0084.

**Step 3.2 — Deficiency Correction**
Address any deficiencies identified during inspections promptly. Work required under guarantee shall be carried out within 10 days of Owner's written instruction per RFP §2.10.6.

**Step 3.3 — Final Self-Inspection**
Conduct a final self-inspection of the completed office space. Verify all requirements in Specification.md are met. Confirm the space is clean, tidy, and ready for Owner acceptance per RFP §2.14.1.

**Step 3.4 — Request Owner Inspection**
Submit written request to the Owner (Camrose County) for final inspection of the office space as part of the overall facility completion per RFP §2.14.2.

**Step 3.5 — Obtain CCC**
After successful final inspection and confirmation that all Contract document requirements are met, the Owner will issue the Construction Completion Certificate (CCC) per RFP §2.14.3. The 2-year warranty period begins at the CCC date.

**Source:** RFP §2.10.6, §2.14, §3.3.2; SOW-0084, SOW-0085, SOW-0090–SOW-0093

---

## Verification

| Step | Verification Check | Pass Criterion |
|---|---|---|
| 2.2–2.3 Partition layout and framing | Field measurement and inspection against IFC floor plan | Dimensions within tolerance of IFC drawings; framing plumb and level |
| 2.4 MEP rough-in | Safety Code inspection (framing/rough-in stage) | Inspection passed; no outstanding deficiencies |
| 2.5A Insulation (if applicable) | Visual inspection before wall closure [Lensing: C-003] | Insulation type and coverage per IFC specification; no gaps or compression |
| 2.6–2.7 Walls and ceiling | Visual inspection; Safety Code inspection if required; **ceiling hold point: above-ceiling MEP inspection passed before ceiling closure** [Lensing: A-004] | Finishes per IFC schedule; no defects; above-ceiling MEP complete and inspected |
| 2.8 Floor finish | Visual inspection | Finish per IFC schedule; no trip hazards; meets accessibility requirements |
| 2.9 Lighting | Operational test | 1× 8' LED fixture operational; confirmed against IFC electrical drawing |
| 2.10 Electrical receptacles | Circuit test | 15A/120V receptacles operational; count and location per IFC electrical drawing |
| 2.11 Door | Operational check; accessibility check | Door operates correctly; lever hardware; width per accessibility requirement |
| 3.1 Interim inspections | Inspection report | Safety Code inspection passed at each stage |
| 3.3 Final self-inspection | Checklist against Specification.md requirements | All REQ-001 through REQ-014 confirmed satisfied |
| 3.5 CCC | CCC document issued | CCC issued on or before December 31, 2026 |

---

## Records

The following records shall be created and retained as evidence that DEL-012-03 has been completed satisfactorily:

| Record | Description | Retained By |
|---|---|---|
| IFC Drawings (stamped) | Architectural, electrical, mechanical IFC drawings for office area | General Contractor; copy to Owner |
| Building Permit | Issued building permit for the new north shop addition | General Contractor; copy to Owner |
| Safety Code Inspection Reports | All interim and final inspection reports for the office area | General Contractor; copies to Owner per SOW-0085 |
| Deficiency List and Correction Log | Record of any deficiencies identified at inspection and how they were resolved | General Contractor |
| Photo Record | Construction progress photographs of office fit-out | General Contractor (ASSUMPTION: standard practice) |
| Construction Completion Certificate (CCC) | Issued by Camrose County upon successful final inspection | Owner; General Contractor |
| 2-Year Warranty Documentation | Written warranty from General Contractor covering materials and workmanship | General Contractor; copy to Owner |
| WCB Letter of Clearance | Workers' Compensation Board clearance | General Contractor; to Owner at final payment per RFP §2.13.2.3 |

**Source:** RFP §2.10.2, §2.13.2, §2.14, §3.3.2; SOW-0085, SOW-0093, SOW-0095
