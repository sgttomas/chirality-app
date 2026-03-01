# Procedure — DEL-015-05 Low-Voltage Systems

---

## Purpose

This procedure describes the steps to produce (install) the low-voltage systems deliverable for the New North Shop addition at the West Dried Meat Lake Regional Landfill. It covers the installation of security camera wiring (SOW-0064) and 2-way radio antenna wiring (SOW-0065), from pre-construction coordination through to commissioning verification and closeout records.

**Source:** Decomposition §7 PKG-015; App B-Elec; RFP §3.3.2; _DEPENDENCIES.md

---

## Prerequisites

### Document Prerequisites (must be in place before installation begins)

| # | Prerequisite | Source | Status |
|---|---|---|---|
| P-01 | IFC Low-Voltage System Plans (DEL-004-07) issued and P.Eng.-stamped | RFP §3.3.2; REQ-015-05-05 | Not yet issued |
| P-02 | Electrical Specification (DEL-004-09) issued | REQ-015-05-03 | Not yet issued |
| P-03 | Electrical Safety Code permit obtained from Alberta authority having jurisdiction (AHJ) | REQ-015-05-04; RFP §3.3.2 | TBD |
| P-04 | Contract scope boundary confirmed: wiring/conduit only vs. equipment supply (CONF-015-05-01, CONF-015-05-02) | Guidance.md Conflict Table | TBD |

### Upstream Work Prerequisites

| # | Predecessor Deliverable | Dependency Type | Notes |
|---|---|---|---|
| U-01 | DEL-015-04 Equipment Power Circuits — rough-in coordination | Coordination | Shared conduit pathways and penetrations should be coordinated before installation |
| U-02 | PKG-011 Building Structure & Envelope — concrete pours and framing | Hard predecessor | Low-voltage conduit sleeves must be embedded or roughed-in before pours and wall closures; cannot retrofit through concrete without core drilling |
| U-03 | Control system design specifications (external) | Information | If security or radio system specs are provided by Owner, these inform cable type selection |

**Source:** _DEPENDENCIES.md; RFP §3.4 (concrete structure); Guidance.md §Considerations

### Personnel Prerequisites

| # | Requirement | Source |
|---|---|---|
| R-01 | Electrical Contractor with qualified electricians licensed in Alberta | RFP §2.15; ASSUMPTION: Alberta Electrical Code requires licensed electricians |
| R-02 | Design-Builder Prime Contractor OH&S compliance | RFP §2.15 |

---

## Steps

> Note: Steps below assume IFC drawings (DEL-004-07) and Electrical Specification (DEL-004-09) are issued. Steps referencing TBD items are contingent on those documents.

> **HOLD POINT (HP-01):** Do not proceed past Phase 1 until DEL-004-07 IFC drawings are issued, reviewed for constructability, and accepted. This is an explicit procedural gate -- not merely a prerequisite note. If DEL-004-07 is not issued, no Phase 2 work shall commence. Design-Builder schedule coordination is required to track this gate. [Lensing: A-004]

### Phase 1 — Pre-Construction Coordination

**Step 1.1 — Review IFC Low-Voltage Plans**
Review DEL-004-07 (IFC Low-Voltage System Plans) for:
- Security camera rough-in locations, mounting heights, and conduit routes
- Antenna cable entry point, routing path, and termination location
- Cable types and sizes specified
- Conduit types, sizes, and fill requirements

Raise any constructability concerns with the Electrical Engineer before ordering materials.

**Step 1.2 — Coordinate with Structural/Envelope Trade**
Identify all conduit penetrations through concrete slabs, walls, or roof assembly required for security camera conduit runs and antenna cable entry. Communicate sleeve sizes and locations to PKG-011 contractor before concrete pours or wall closures occur.

*Source: Guidance.md §Principles (Principle 1); RFP §3.3.2*

**Step 1.3 — Coordinate with Equipment Power Circuits Trade**
Review DEL-015-04 routing plan for shared conduit pathways, panel locations, and any shared penetrations. Confirm separation requirements per Alberta Electrical Code for low-voltage wiring alongside power wiring.

**Step 1.4 — Obtain Safety Code Permit**
Obtain electrical permit from the Alberta Safety Codes authority having jurisdiction (AHJ) for low-voltage work. REQ-015-05-04 mandates Alberta Safety Code compliance, which typically requires a permit for electrical installation work. If the AHJ determines that a permit is not required for this specific low-voltage scope, obtain and retain written confirmation from the AHJ documenting that determination. Do not proceed with installation without either an issued permit or documented AHJ exemption. Confirm inspection hold points with AHJ. [Lensing: C-001]

**Step 1.5 — Procure Materials**
Based on DEL-004-07 and DEL-004-09, procure:
- Conduit (type TBD per DEL-004-09)
- Pull string or low-voltage cable as specified (cable type TBD per DEL-004-07)
- Junction boxes, conduit fittings, cable supports, and penetration sleeves
- Antenna cable entry weatherhead or watertight conduit fitting (if exterior penetration required)

**Step 1.6 — Material Staging and Storage**
Arrange for appropriate material staging and storage on site:
- Store cable reels indoors or under weather protection to prevent moisture damage
- Secure fittings, junction boxes, and conduit accessories in a locked storage area or container
- Coordinate staging location with Design-Builder site logistics to avoid interference with active construction areas
- Protect materials from damage during the construction period (concrete structure with 35' ceiling -- active construction site with overhead work)
[Lensing: F-003]

---

### Phase 2 — Rough-In Installation

**Step 2.1 — Install Conduit Sleeves (Pre-Pour)**
Prior to any concrete pours or permanent wall closures, install all conduit sleeves at penetration locations identified in DEL-004-07. Confirm sleeve sizes and locations with structural trade. Document installed sleeve locations on working drawings.

**Step 2.2 — Install Security Camera Conduit Rough-In**
Install conduit from camera mounting locations to termination room per DEL-004-07 (see Guidance Principle 7 for canonical terminology [Lensing: B-003]):
- Install junction boxes at camera mounting points at heights per drawings
- Run conduit from junction boxes to termination room per routing shown
- Install pull string in each conduit run
- Cap open conduit ends to prevent debris entry during construction

**Step 2.3 — Install Antenna Conduit Rough-In**
Install antenna cable conduit/pathway from exterior building penetration point to termination room per DEL-004-07 (see Guidance Principle 7 for canonical terminology [Lensing: B-003]):
- Install watertight conduit fitting or weatherhead at exterior penetration
- Run conduit from exterior entry to termination room
- Seal all exterior penetrations to maintain building envelope integrity (coordinate with PKG-011)
- Install pull string in conduit run

**Step 2.4 — Install Low-Voltage Cable (if specified pre-pull)**
If DEL-004-07 specifies pre-pulling cable during rough-in phase (rather than at trim-out):
- Pull cable through installed conduit
- Leave sufficient slack at all termination points per drawing requirements
- Label cables at both ends per DEL-004-07 labeling schedule (if specified; see Step 4.3 for labeling scheme reference [Lensing: C-003])
- Protect cable ends from damage

*Note: Whether cable is installed at rough-in or trim-out depends on DEL-004-07 specifications — TBD.*

---

### Phase 3 — Rough-In Inspection

**Step 3.1 — Contractor Self-Inspection**
Prior to requesting Safety Codes Officer inspection, the Electrical Contractor shall verify:
- All conduit routes match DEL-004-07
- All junction boxes are installed at correct locations and heights
- All penetrations are sleeved and sealed (where applicable)
- Pull strings are installed in all conduit runs
- No open conduit ends exposed to construction debris

**Step 3.2 — Request Rough-In Inspection**
Submit inspection request to the AHJ Safety Codes Officer. Notify County project representative. Coordinate timing to ensure County representative can be present (RFP §3.3.2).

**Step 3.3 — Remedy Deficiencies**
If the Safety Codes Officer or County representative identifies deficiencies, remedy all items before proceeding to the next phase. Document all remedial actions.

---

### Phase 4 — Trim-Out and Cable Installation (if not pre-pulled)

**Step 4.1 — Pull Cable**
After walls/ceilings are closed and painted (or as coordinated with general schedule), pull specified cable through conduit runs per DEL-004-07.

**Step 4.2 — Install Terminations**
Install cable terminations at camera junction boxes and at termination room per DEL-004-07 (see Guidance Principle 7 [Lensing: B-003]). Cable termination type depends on camera system selected — TBD.

**Step 4.3 — Label Cables**
Label all cables at both ends per DEL-004-07 labeling schedule. Labeling scheme TBD -- Electrical Engineer to define in DEL-004-07 or DEL-004-09. If no labeling schedule is provided in IFC documents, apply labeling per TIA-606-C (or equivalent industry standard) as a default, subject to Electrical Engineer approval. [Lensing: C-003]

---

### Phase 5 — Commissioning Verification

**Step 5.1 — Continuity and Connectivity Check**
Verify continuity of all installed cable runs. Confirm no shorts or opens.

**Step 5.2 — Camera System Operational Check**
ASSUMPTION: If camera heads are supplied and installed (by Contractor or Owner), verify each camera provides signal to head-end recording equipment. If wiring-only scope, verify cable continuity and present pulls to Owner/integrator for equipment hook-up. Document results.

**Step 5.3 — Radio Antenna Check**
ASSUMPTION: If radio antenna is supplied and installed, verify antenna cable connection and radio communication from building location. If wiring-only scope, verify antenna cable continuity and present to Owner/radio system integrator. Document results.

*Source: REQ-015-05-01, REQ-015-05-02; OBJ-005 (commission to operational readiness)*

> **Commissioning scope clarification (TBD):** The definition of "operational readiness" (OBJ-005) for this deliverable depends on the resolved scope boundary (CONF-015-05-01/02). If scope is limited to rough-in wiring, operational readiness means verified cable continuity at all termination points, ready for equipment hook-up by Owner or integrator. If scope includes active components, operational readiness means demonstrated camera/radio function. Owner to confirm commissioning scope once CONF-015-05-01/02 are resolved. [Lensing: X-003]

**Step 5.4 — Final Inspection**
Submit request for final Safety Codes Officer inspection. Notify County project representative. Accompany inspector; provide access to all installed work.

**Step 5.5 — Remedy Final Deficiencies**
Remedy any deficiencies identified at final inspection before requesting Construction Completion Certificate.

---

### Phase 6 — Closeout

**Step 6.1 — Produce As-Built Drawings**
Mark up IFC drawings to show any field deviations from designed routing or locations. Submit as-built drawings to Design-Builder for inclusion in project closeout package.

**Step 6.2 — Submit Warranty Documentation**
Provide written warranty letter covering all materials and workmanship for the 2-year guarantee period post-CCC per REQ-015-05-08. Warranty shall cover all materials and workmanship; any exclusions require pre-approval by the Owner in writing. Permitted exclusion categories TBD -- Specification governs warranty scope. [Lensing: E-002]

**Step 6.3 — Assemble and Submit Inspection Records**
Compile copies of all Safety Code inspection reports, deficiency lists, and sign-offs. Submit to Design-Builder and Owner.

**Step 6.4 — Support Construction Completion Certificate (CCC)**
Provide Design-Builder with confirmation that all low-voltage systems work (SOW-0064, SOW-0065) is complete, inspected, and ready for Owner acceptance, to support issuance of the CCC.

---

## Verification

| Step | Verification Check | Verified By | Record |
|---|---|---|---|
| After Step 2.1–2.4 | Rough-in conduit and cable routes match DEL-004-07 | Electrical Contractor self-check | Marked-up drawing |
| After Step 3.2 | Safety Codes Officer rough-in inspection passed | Safety Codes Officer; County representative | Inspection report |
| After Step 5.1 | Cable continuity verified | Electrical Contractor | Test record |
| After Step 5.2 | Camera signal or cable continuity confirmed | Electrical Contractor; Owner/integrator | Commissioning record |
| After Step 5.3 | Antenna cable continuity or radio link confirmed | Electrical Contractor; Owner/integrator | Commissioning record |
| After Step 5.4 | Final Safety Codes Officer inspection passed | Safety Codes Officer; County representative | Final inspection report |
| After Step 6.1 | As-built drawings submitted | Electrical Contractor; Design-Builder | As-built drawing set |
| Prior to CCC | All SOW-0064 and SOW-0065 work complete and documented | Electrical Contractor; Design-Builder | CCC support package |

---

## Records

The following records shall be produced and retained as evidence of work completion:

| Record | Description | Retained By |
|---|---|---|
| Pre-construction coordination meeting record | Formal meeting record documenting coordination between Electrical Contractor, Design-Builder, and structural/envelope trade for REQ-015-05-09. Record shall include: date, attendees (required: Electrical Contractor foreman, Design-Builder project manager, structural trade foreman), items discussed (sleeve locations, conduit pathway coordination, separation distances), decisions made, and sign-off by attendees. [Lensing: F-002] | Electrical Contractor; Design-Builder |
| Material delivery receipts | Evidence of specified cable and conduit materials received | Electrical Contractor |
| Rough-in inspection report | Safety Codes Officer sign-off on rough-in. Inspection reports shall use AHJ-provided forms where available and shall include at minimum: date, inspector name, areas/systems inspected, deficiencies identified (if any), and sign-off. Retention format (paper or digital) per Design-Builder QA protocol. [Lensing: D-001] | Electrical Contractor; Design-Builder; County |
| Cable test records | Continuity test results for all camera and antenna cable runs | Electrical Contractor |
| Commissioning records | Camera and radio system operational verification | Electrical Contractor; Owner |
| Final inspection report | Safety Codes Officer final sign-off. Format per D-001 requirements (see rough-in inspection report format above). [Lensing: D-001] | Electrical Contractor; Design-Builder; County |
| As-built drawings | Marked-up DEL-004-07 showing actual installed routes | Design-Builder; Owner |
| Warranty letter | 2-year guarantee covering materials and workmanship | Owner |
| Lien holdback release documents | WCB clearance letter; statutory declaration (per RFP §2.13.2) | Owner; Design-Builder |
