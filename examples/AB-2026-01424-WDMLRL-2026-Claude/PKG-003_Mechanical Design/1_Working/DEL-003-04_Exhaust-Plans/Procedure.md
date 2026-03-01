# Procedure — DEL-003-04 Exhaust System Plans

---

## Purpose

This procedure describes the steps to produce the Exhaust System Plans drawing set (DEL-003-04) for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. It covers the workflow from design inputs through IFC drawing issue, including internal review, cross-discipline coordination, and County approval gating.

The procedure is oriented to the Mechanical Engineer responsible for this deliverable.

---

## Prerequisites

### Required Inputs

| Input | Source | Status |
|---|---|---|
| Conceptual floor plan (App B) — showing exhaust source locations | R-04 (App B) | Available |
| RFP §3.4 Design Requirements | R-01 | Available |
| Electrical conceptual drawing (App B-Elec) — exhaust fan locations | R-05 | Available (reference for coordination; detail review TBD per CFT-002) |
| Preliminary Mechanical Design (DEL-003-01) — County-approved | DEL-003-01 | Required before IFC; must be approved prior to Step 5 |
| Mechanical Calculation Package (DEL-003-06) — fan sizing, airflow | DEL-003-06 | Developed in parallel; required before final drawing completion |
| Structural drawings — penetration locations, pit structure, crane details | DEL-002-06 (Service Pit Details), DEL-002-07 (Structural Steel / Crane Details) | Required for pit ventilation detail and crane clearance coordination |
| Architectural drawings — ceiling routing, wall locations | DEL-001-02 (Floor Plans) | Required for duct routing coordination |
| Electrical design coordination — fan electrical characteristics | DEL-004 series | Required for equipment schedule coordination |
| Applicable Alberta Safety Codes and Building Code editions | Authority Having Jurisdiction (AHJ) | Required for code-compliant design |

### Required References

| Reference | Document |
|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf (§3.3.2, §3.4) |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf |
| DEL-003-07 | Mechanical Specification (governs installation requirements for exhaust components) |
| Alberta Building Code (current edition as adopted) | ASSUMPTION: likely applicable |
| Alberta Safety Codes Act and OHS Code | ASSUMPTION: likely applicable |
| ASHRAE 62.1 (Ventilation for Acceptable Indoor Air Quality) | ASSUMPTION: likely applicable |

---

## Steps

### Step 1 — Confirm Design Basis and Source Locations

1.1 Review the conceptual floor plan (R-04 App B) and identify all exhaust source locations:
- Two drive-through repair bays (24' wide each, approximate location: center of 130' building width per App B)
- Welding station (northeast quadrant of main shop floor per App B)
- Service pit (east side of main shop per App B)
- Wash bay (east end of building, enclosed, 24' wide per App B)
- General exhaust fan locations (coordinate with R-05 App B-Elec)

1.2 Confirm building geometry with architectural team (DEL-001-02):
- Ceiling height = 35 ft (Source: R-01 §3.4, R-04 App B)
- Building footprint = ~130' x 100' (Source: R-04 App B)
- Wall and partition locations affecting duct routing

1.3 Confirm power supply characteristics with electrical team (DEL-004): three-phase power available; determine voltage and amperage constraints for fan motor selection.

1.4 Obtain overhead crane data from structural team (DEL-002-07): crane type (5-tonne overhead on trolley), runway height, hook height, and travel envelope. These are constraints for exhaust duct and hose routing in the main shop area. (Source: SOW-0067; D-002)

**Output:** Confirmed source location list and design basis memo (internal).

> **Terminology note (X-005):** This Procedure uses "service pit" as the primary term. "Service trench" is treated as an alias. See Specification REQ-003 terminology note.

---

### Step 2 — Establish Design Criteria and Code Requirements

2.1 Identify the applicable edition of the Alberta Building Code (NBC as adopted by Alberta) and the Alberta Safety Codes Act regulations in effect at time of building permit application. Confirm with the Authority Having Jurisdiction (AHJ) for Camrose County.

2.2 Determine applicable ASHRAE 62.1 ventilation requirements for the space types (industrial shop, welding station, service pit). **ASSUMPTION:** ASHRAE 62.1 is applicable; confirm against AHJ requirements.

2.3 Determine applicable Alberta OHS Code requirements for:
- Diesel exhaust exposure in heavy equipment service bays
- Welding fume exposure limits and required ventilation measures
- Confined or enclosed space ventilation requirements for the service pit
- Occupational noise exposure limits relevant to exhaust fan selection (E-004)

2.4 Document design criteria in the Mechanical Calculation Package (DEL-003-06): design airflow rates, pressure classes, temperature ranges, winter design temperature for Ferintosh (E-001).

2.5 Conduct a design-phase code review: before proceeding to IFC (Step 5), review the exhaust system design against the confirmed applicable code editions and clause references identified in Steps 2.1-2.3. Document the review findings. This step provides an internal pre-IFC code compliance check that does not depend solely on downstream permits (DEL-009-03) and inspections (DEL-009-04). (Source: A-003)

**Output:** Design criteria table (documented in DEL-003-06; summary referenced in DEL-003-07 Specification). Code review record (internal, filed per Records table).

---

### Step 3 — System Design and Layout (Preliminary Design Phase)

3.1 Select exhaust system type for each source:
- Repair bays: exhaust hose-reel system with inline or remotely mounted exhaust fans connected to dedicated exhaust duct and exterior stack. (Source: R-01 §3.4 SOW-0038 — "exhaust hoses and fans"; ASSUMPTION: hose-reel source-capture approach)
- Welding station: local exhaust ventilation (LEV) system with capture hood, duct run, exhaust fan, and exterior termination. (Source: R-01 §3.4 SOW-0039; ASSUMPTION: LEV preferred — see Guidance)
- Service pit: mechanical supply-and-exhaust arrangement; supply from above-grade, exhaust from low point of pit. (Source: R-01 §3.4 SOW-0028; ASSUMPTION: continuous operation during occupied hours — see Guidance)
- Wash bay: exhaust/ventilation system for the enclosed wash bay to address steam, moisture, and potential vehicle exhaust during wash operations. System type TBD. (Source: R-01 §3.1, §3.4; R-04 App B; B-003, A-004)
- General exhaust fans: as shown on electrical conceptual drawing (R-05 App B-Elec); coordinate locations and flow rates. (Source: SOW-0066)

3.2 Size exhaust systems using load calculations (DEL-003-06):
- Repair bay: determine air volume per bay based on vehicle exhaust flow rates and dilution requirements
- Welding station: determine capture velocity and flow rate per ASHRAE or industry standard (location TBD)
- Service pit: determine air changes per hour per applicable code (location TBD); use pit dimensions from DEL-002-06 (B-001)
- Wash bay: determine exhaust requirements for enclosed wash bay (TBD)

3.3 Design duct routing:
- Minimize duct length and number of fittings
- Account for 35 ft ceiling height — hose drops from above for repair bays
- Route exhaust ducts to exterior with minimum code clearances at termination points
- Coordinate penetration locations with structural team (DEL-002)
- Clear overhead crane travel envelope (crane runway height and hook height from DEL-002-07; D-002)

3.4 Select exterior termination/stack locations:
- Avoid re-entrainment at building air intakes
- Provide weatherproof caps; account for cold-climate frost accumulation (use winter design temperature from E-001)
- **ASSUMPTION:** Roof termination preferred for all exhaust stacks (see Guidance)

3.5 Assess ceiling fan interaction with exhaust capture systems (REQ-009): confirm that the 6 ceiling fan locations (SOW-0040, R-05) do not conflict with exhaust capture zones at the welding station and repair bay hose drops. Document assessment in DEL-003-06 or design notes. (Source: C-002)

3.6 Coordinate forced-air makeup air balance (REQ-005): perform an explicit coordination step with the makeup air system design (SOW-0037, DEL-003-02) to confirm exhaust/makeup air balance. Document the total exhaust airflow and corresponding makeup air capacity. (Source: F-003)

3.7 Prepare preliminary exhaust system layout plans for inclusion in DEL-003-01 (Preliminary Mechanical Design) for County approval. **This step gates Step 4 — do not proceed to IFC until County approval of preliminary design is confirmed.**

**Output:** Preliminary exhaust system layout drawings; inclusion in DEL-003-01 submission.

> **Note (A-004):** Wash bay exhaust system design (Step 3.1, bullet 4) has been added. The wash bay was previously identified as an exhaust source in Step 1.1 but had no corresponding system design step. **PROPOSAL:** Mechanical Engineer to confirm if wash bay exhaust is in scope of DEL-003-04 or DEL-003-02. Source: _SEMANTIC_LENSING.md item A-004.

> **Note (F-003):** Makeup air balance coordination (Step 3.6) has been added as an explicit procedural step. The prior version included REQ-005 (air balance coordination) as a requirement but did not assign a specific procedural action for it. Source: _SEMANTIC_LENSING.md item F-003.

> **Note (D-001 — Gate Clarification):** Step 3.7 (previously Step 3.5) contains the preliminary design gate. Step 4 describes the County approval process for that preliminary design. The relationship is sequential: Step 3.7 produces the preliminary design and establishes the gate condition ("do not proceed to IFC until County approval"); Step 4 describes the submission and approval process that satisfies that gate. Step 4 output (County approval record) is the gate-opening artifact. Source: _SEMANTIC_LENSING.md item D-001.

---

### Step 4 — County Approval of Preliminary Design

4.1 Submit DEL-003-01 Preliminary Mechanical Design (including exhaust system concept) to County for approval per SOW-0010c and R-01 §3.3.2.

4.2 Address any County comments related to exhaust system concept.

4.3 Obtain County approval before proceeding to IFC drawing production. County approval record is the gate-opening artifact for Step 5.

**Output:** County approval record for preliminary design.

---

### Step 5 — Produce IFC Drawing Set

5.1 Develop the following drawing sheets (anticipated content — actual sheet list determined by Mechanical Engineer):

| Anticipated Sheet | Content |
|---|---|
| Exhaust System Overall Plan | Full building plan view showing all exhaust source locations, fan units, duct/hose routing, and exterior terminations |
| Repair Bay Exhaust Detail | Detailed plan and section of hose-reel system in each repair bay; fan unit location; duct to exterior |
| Welding Station Exhaust Detail | Detailed plan and section of LEV hood, duct run, fan, and stack termination |
| Service Pit Ventilation Detail | Section through pit showing supply and exhaust arrangement, fan location, grille locations |
| Wash Bay Exhaust Detail | Plan and/or section showing wash bay exhaust arrangement (if in scope per CFT-001) |
| Vent Stack and Termination Details | Exterior elevation/detail drawings showing stack heights, termination caps, clearances (corresponds to "Vent stack and termination drawings" artifact in Specification) |
| Exhaust Fan Schedule | Fan designation, location, airflow (CFM/L/s), static pressure (Pa/in wg), motor data, remarks |

> **Note (X-002):** This anticipated sheet list is illustrative. The Specification Documentation section lists 3 minimum required artifacts. This Procedure list expands upon but does not replace that minimum list. The actual sheet list is determined by the Mechanical Engineer. Source: _SEMANTIC_LENSING.md item X-002.

5.2 Ensure all drawing content is consistent with:
- Mechanical Calculation Package (DEL-003-06): fan sizes and airflow values match
- Mechanical Equipment Schedule (DEL-003-05): all fans and exhaust units listed
- Mechanical Specification (DEL-003-07): installation requirements for exhaust components
- HVAC Plans (DEL-003-02) and Ductwork Plans (DEL-003-03): no conflicting duct routing or boundary overlap (see Guidance CFT-001)
- Electrical Plans (DEL-004): fan locations match; electrical characteristics provided to electrical team

5.3 Complete internal QC review:
- Verify duct sizing and routing against calculations
- Verify exterior termination clearances against code requirements
- Verify coordination with structural penetration schedule (DEL-002)
- Verify design-phase code review findings (Step 2.5) have been addressed
- Document QC review findings using the project QC sign-off form (reference PKG-019 QC template if available; otherwise document per the QC sign-off format defined in the Records table below) (X-006)

**Output:** Complete exhaust system drawing set, IFC quality, internally reviewed.

---

### Step 6 — P.Eng. Stamp and Issue

6.1 Have all drawing sheets reviewed and stamped by a Professional Engineer licensed to practice in the Province of Alberta. Confirm that the reviewing P.Eng. holds a current Alberta practice licence before stamping (verify licence status with APEGA or equivalent registry). (Source: R-01 §3.3.2, SOW-0018; X-001)

6.2 Issue DEL-003-04 as IFC drawings to the project team (for use by PKG-013 mechanical contractor and for building permit/Safety Code permit applications — DEL-009-02, DEL-009-03).

6.3 Provide copies to County project manager as required by coordination protocol. (Source: R-01 §3.1, SOW-0086)

**Output:** Stamped IFC Exhaust System Plans drawing set, issued for construction and permitting.

> **Note (X-001):** Step 6.1 has been strengthened to include explicit P.Eng. licence validation. The prior version stated "Verify P.Eng. stamp and Alberta licence number on each drawing sheet" but did not specify who checks or how licence validity is confirmed. Source: _SEMANTIC_LENSING.md item X-001.

---

## Verification

After completing the drawing set, verify the following before issuance:

| Check | Verification Method | Pass Criterion |
|---|---|---|
| All exhaust sources covered | Review drawing set against source list from Step 1.1 (including wash bay per A-004) | All sources (repair bays, welding station, service pit, wash bay if in scope, general fans) shown |
| Fan sizes match calculations | Compare drawing fan schedule with DEL-003-06 | Airflow and static pressure values within TBD% tolerance of calculated values (F-002/A-005) |
| Makeup air balance confirmed | Review DEL-003-06 air balance calculation; confirm with DEL-003-02 team (F-003) | Total exhaust airflow documented; makeup air balance within TBD% of exhaust |
| Ceiling fan interaction assessed | Confirm assessment documented per Step 3.5 (C-002) | Assessment complete; no unresolved conflicts between ceiling fan positions and exhaust capture zones |
| Electrical coordination complete | Confirm with DEL-004 team that fan motor data is provided and received | No open coordination items; formal coordination record signed (X-003) |
| Structural penetrations coordinated | Confirm with DEL-002 team that penetration locations are accepted | No conflicts; structural drawing reflects penetration schedule; formal coordination record signed (X-003) |
| Architectural duct routing conflicts cleared | Cross-reference with DEL-001-02 | No interferences with structural elements, doors, overhead cranes; formal coordination record signed (X-003) |
| Overhead crane clearances maintained | Check duct/hose routing against crane runway heights (5-tonne cranes, DEL-002-07; D-002) | No interference with crane travel envelope |
| Exterior termination locations approved | Coordinate with architectural team (DEL-001) | No conflicts with building envelope or intake locations |
| Design-phase code review completed | Confirm Step 2.5 code review findings addressed (A-003) | All code review findings resolved or documented as accepted deviations |
| IFC stamp present and licence validated | Visual check of each drawing sheet; licence validation per Step 6.1 (X-001) | P.Eng. stamp and Alberta licence number on all sheets; licence confirmed as current |
| Consistency with DEL-003-05 Equipment Schedule | Cross-reference fan schedule on drawings with equipment schedule | All exhaust fans listed consistently in both documents |
| Consistency with DEL-003-07 Specification | Review specification for product requirements that affect drawing content | No conflicts between specification requirements and drawing details |
| SOW traceability confirmed | Review against Specification SOW Traceability Matrix (F-001) | All SOW items assigned to DEL-003-04 addressed by at least one drawing element |
| Noise/vibration assessment completed | Confirm assessment per REQ-010 documented (E-004) | Assessment documented; exhaust equipment within applicable noise limits or documented as acceptable |

> **Note (A-005):** Quantitative pass/fail criteria have been added as TBD placeholders where the prior version used only qualitative criteria. Specific tolerances are TBD pending Mechanical Engineer definition. Source: _SEMANTIC_LENSING.md item A-005.

> **Note (X-003):** Formal coordination records with each cross-discipline team (Electrical, Structural, Architectural) are now referenced as verification evidence. See Records table for coordination record format requirements. Source: _SEMANTIC_LENSING.md item X-003.

---

## Records

The following records shall result from execution of this procedure:

| Record | Location / Filing | Format / Content Requirements |
|---|---|---|
| Issued IFC Exhaust System Plans (stamped drawings) | DEL-003-04_Exhaust-Plans deliverable folder; copy to County | P.Eng.-stamped drawing set |
| Preliminary design drawings (County approval set) | DEL-003-01_Preliminary-Design deliverable folder | As submitted to County |
| County approval record for preliminary design | DEL-003-01 folder; project correspondence file | Written County approval (email, letter, or meeting minutes) |
| Design-phase code review record (A-003) | Project QC file; DEL-003-04 deliverable folder | Checklist of applicable code provisions reviewed, findings, and resolutions |
| Internal QC review sign-off (X-006) | Project QC file (PKG-019 QC management) | QC sign-off form including: reviewer name, date, checklist of items verified (per Step 5.3), findings summary, disposition of findings, reviewer signature. Reference PKG-019 QC template if available. |
| Coordination record — Electrical (DEL-004) (X-003) | Project coordination log | Record of coordination items exchanged, resolutions, and sign-off by both Mechanical and Electrical Engineers. Minimum content: items discussed, decisions made, date, signatories. |
| Coordination record — Structural (DEL-002) (X-003) | Project coordination log | Record of coordination items exchanged, resolutions, and sign-off by both Mechanical and Structural Engineers. Minimum content: items discussed, decisions made, date, signatories. |
| Coordination record — Architectural (DEL-001) (X-003) | Project coordination log | Record of coordination items exchanged, resolutions, and sign-off by both Mechanical and Architectural teams. Minimum content: items discussed, decisions made, date, signatories. |
| Calculation package (fan sizing, airflow balance) | DEL-003-06_Calculation-Package deliverable folder | Per DEL-003-06 requirements |
| Equipment schedule (all fans and exhaust units) | DEL-003-05_Equipment-Schedule deliverable folder | Per DEL-003-05 requirements |
| Building permit / Safety Code permit application (includes drawings) | DEL-009-02, DEL-009-03 deliverable folders | Per permit application requirements |

> **Note (X-003):** Coordination records have been expanded with minimum content requirements. The prior version listed "Coordination log" as a single entry without specifying content requirements or sign-off format. Each cross-discipline coordination is now tracked separately with defined minimum content. Source: _SEMANTIC_LENSING.md item X-003.

> **Note (X-006):** Internal QC review sign-off format has been defined. The prior version listed the record but did not specify content requirements. Source: _SEMANTIC_LENSING.md item X-006. **PROPOSAL:** Reference PKG-019 QC template if available.
