# Procedure — DEL-003-06 Mechanical Calculation Package

---

## Purpose

This procedure describes the steps required to **produce** the Mechanical Calculation Package (DEL-003-06) for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. It is addressed to the Mechanical Engineer responsible for PKG-003 — Mechanical Design.

Following this procedure will result in a complete, indexed, P.Eng.-stamped calculation package that:
- Provides the engineering basis of record for all mechanical systems in the addition
- Enables finalization of DEL-003-02 through DEL-003-05 and DEL-003-07
- Satisfies OBJ-003 (IFC design documentation) and OBJ-004 (mechanical system operational readiness)
- Meets the requirements of REQ-M-001 through REQ-M-013 as defined in Specification.md

---

## Prerequisites

The following items shall be confirmed or obtained before commencing the calculation package:

| # | Prerequisite | Status | Source |
|---|---|---|---|
| PR-01 | County approval of Preliminary Mechanical Design (DEL-003-01) | Required before final calculations | R-01 S3.3.2; SOW-0010c |
| PR-02 | Building envelope design inputs available from Architectural and Structural packages (wall/roof assemblies, U-values, window/door areas) | Required for heating load (REQ-M-001) | Decomposition PKG-001, PKG-002 |
| PR-03 | Conceptual floor plan (App B — R-04) reviewed and room dimensions/areas confirmed or updated | Required for zone sizing | R-04 App B |
| PR-04 | Overhead crane rail layout confirmed (crane envelope height clearance for overhead equipment) — **confirm crane envelope dimensions from structural/crane package (PKG-016) and determine minimum clearance per crane manufacturer requirements or Alberta OH&S** | Required to avoid conflicts with heating/exhaust equipment | SOW-0067; Decomposition PKG-016; [Enrichment X-001] |
| PR-05 | NBCC climate data for Ferintosh/Camrose County obtained (design heating temperatures, degree-days, etc.) | Required for heating load design conditions | ASSUMPTION: NBCC applicable |
| PR-06 | Applicable Alberta Building Code edition and relevant Alberta Safety Code bulletins on hand | Required for code compliance (REQ-M-010) | R-01 S3.3.2; SOW-0008, SOW-0009 |
| PR-07 | County welding equipment specifications received (formal request to County if not yet provided) | Required to finalize REQ-M-006; if not received, proceed with ASSUMPTION and flag | R-01 S3.4; SOW-0204 |
| PR-08 | Natural gas supply pressure and availability confirmed with utility (for gas-fired equipment sizing — ASSUMPTION: gas heating is selected) | Required for combustion equipment sizing | SOW-0080; ASSUMPTION |
| PR-09 | ACGIH Industrial Ventilation Manual (current edition), ASHRAE Fundamentals, and SMACNA standards accessible to the Mechanical Engineer | Required reference materials for calculation methodology | Specification.md Standards |

---

## Steps

### Step 1 — Document Setup and Index

1.1 Create the calculation package folder structure with the following sections:
- Section 1: Project Information and Design Basis
- Section 2: Heating Load Calculations
- Section 3: Ventilation Rate Calculations (including mezzanine zone and wash bay)
- Section 4: Makeup Air Unit Sizing
- Section 5: Heavy Equipment Exhaust Sizing
- Section 6: Welding Station Exhaust Sizing
- Section 7: Service Pit Ventilation
- Section 8: Ceiling Fan Selection
- Section 9: System Balance Summary
- Section 10: Code Compliance Reference Table
- Section 11: Assumptions Register

1.2 Complete Section 1 — Project Information and Design Basis:
- Project name, location, and description
- Deliverable ID: DEL-003-06
- Author, reviewer, P.Eng. stamp holder
- Revision status (PRELIMINARY until County approval; FINAL IFC-QUALITY after review and stamp)
- Reference list (all standards cited in Specification.md Standards)
- **Primary unit convention for airflow values (establish L/s or CFM as primary; see Guidance C-08) [Enrichment F-004]**

1.3 Complete Section 11 — Assumptions Register (populate this before calculations begin; update throughout):
- Record each design assumption with: assumption statement, basis, and consequence if assumption is wrong
- Flag all ASSUMPTIONs that are pending County input (PR-07: welding specs; PR-08: gas supply; PR-05: design temperature if not from NBCC)

**Verification:** Section 1 and Section 11 (stub) exist before proceeding to Step 2.

---

### Step 2 — Heating Load Calculation (REQ-M-001, REQ-M-002)

2.1 Obtain or establish the following inputs:
- Building floor area by zone (from App B and confirmed architectural drawings)
- Ceiling height: 35 ft main shop; other zones TBD from architectural drawings
- Wall, roof, slab, window, and door U-values (from Structural/Architectural — PR-02; ASSUMPTION if not yet available)
- Design outdoor heating temperature (from NBCC climate data — PR-05)
- Indoor design temperatures by zone (ASSUMPTION: shop/bays ~10C minimum; office per occupancy code; confirm with Owner)

2.2 Calculate zone-by-zone steady-state heat loss:
- Transmission losses through envelope elements (UA x dT method or equivalent)
- Infiltration losses (estimate air changes per hour through overhead doors, gaps — use ASHRAE crack method or equivalent)
- Slab-on-grade edge loss

2.3 Sum zone losses to determine total building peak heating load.

2.4 Apply a system safety factor (**value TBD — see Guidance Trade-off T-03 for considerations; document selected value and engineering basis in Section 2**).

> **[Enrichment F-002]:** Safety factor previously stated as "ASSUMPTION: 10-15% or per engineering judgment." The specific value and its basis shall be documented. See Guidance T-03. Source: Specification.md REQ-M-002; Procedure.md Step 2.

2.5 Select heating system type (see Trade-off T-01 in Guidance.md; document selected type in Section 1 of calculation package).

2.6 Confirm that selected heating equipment capacity >= calculated peak heating load.

2.7 Document results in Section 2. Update assumptions register.

**Verification:** Total calculated heating load and selected system capacity are consistent. Safety factor is justified and documented. Inputs are traceable to sources.

---

### Step 3 — Ventilation Rate Calculations (REQ-M-003, REQ-M-012)

3.1 Identify all zones and their occupancy category per Alberta Building Code and ASHRAE 62.1 (ASSUMPTION: applicable):
- Main shop / repair bays (vehicle exhaust environment, intermittent gaseous contaminants)
- Wash bay (humidity, cleaning chemicals — **see REQ-M-012 for dedicated moisture control calculation**)
- Service pit (below-grade, potential CO accumulation — safety-critical)
- Parts room, utility room, office (comfort ventilation)
- Mezzanine (storage — confirm if mechanical ventilation required by code; ASSUMPTION: likely required at minimum)

3.2 Determine minimum air change rates (ACH) for each zone from applicable code tables or industrial ventilation standards.

3.3 Calculate required ventilation airflow per zone = ACH x zone volume / 3600. **Use the primary unit convention established in Section 1 (see Guidance C-08) [Enrichment F-004].**

3.4 Identify which zones are served by the high-volume air exchanger vs. the heavy equipment exhaust systems vs. the welding exhaust system (coordinate with Step 5 and Step 6).

**3.5 Mezzanine zone determination: evaluate whether the mezzanine (above parts room, utility room, and wash bay) requires dedicated HVAC zoning or can be served by carryover ventilation from adjacent zones. Reference Guidance C-06 and applicable code provisions for storage areas containing oil totes and pump equipment. Document the code evaluation and conclusion in Section 3.**

> **[Enrichment A-004]:** Mezzanine zone procedure step added. Guidance C-06 identifies the mezzanine as a zone requiring code evaluation for ventilation, but no procedure step previously addressed this analysis. Source: Procedure.md Steps; Guidance.md C-06. PROPOSAL: Inserted as sub-step under Step 3 (Ventilation Rate Calculations).

**3.6 Wash bay ventilation and moisture control: calculate the required ventilation rate for the enclosed wash bay zone (REQ-M-012), addressing moisture removal during vehicle washing operations. Coordinate with wash bay drainage considerations from Guidance C-04. Determine whether dedicated exhaust is required or whether the high-volume air exchanger provides adequate moisture control for the wash bay zone.**

> **[Enrichment C-003]:** Wash bay ventilation step added. Procedure Steps 3-9 covered main shop, repair bays, service pit, welding, and ceiling fans, but there was no dedicated step for wash bay ventilation sizing. Source: Procedure.md Steps; Guidance.md C-04. PROPOSAL: Inserted as sub-step under Step 3.

3.7 Document results in Section 3.

**Verification:** Each zone has a documented minimum ventilation rate and the airflow calculation is traceable to a code or standard. Mezzanine zone determination is documented. Wash bay moisture control is addressed.

---

### Step 4 — Makeup Air Unit Sizing (REQ-M-004)

4.1 Sum all exhaust airflows from:
- Heavy equipment exhaust system (from Step 5)
- Welding station exhaust (from Step 6 — use ASSUMPTION if welding specs not yet received; flag)
- High-volume air exchanger exhaust component (from Step 3)
- Any other exhaust (service pit fans, wash bay exhaust, washroom exhaust — TBD)

4.2 Determine required MUA flow rate = total exhaust flow minus planned infiltration credit (ASSUMPTION: no infiltration credit in design — conservative).

4.3 Size MUA heating coil capacity:
- Coil inlet = design outdoor temperature (from PR-05)
- Coil outlet = supply air temperature (ASSUMPTION: minimum 15C or as required to avoid thermal comfort issues)
- Heating capacity = MUA flow x Cp x density x dT

4.4 Confirm gas supply capacity at PR-08 is sufficient for combined heating system and MUA (if gas-fired).

**4.5 If gas-fired equipment is selected: complete combustion air supply calculation (REQ-M-013) — confirm combustion air requirements for all gas-fired equipment and verify that the combustion air supply does not create negative pressure conditions conflicting with system balance (Step 9).**

> **[Enrichment X-002]:** Combustion air calculation step added, conditional on gas-fired equipment. Source: Specification.md REQ-M-013; Guidance.md C-05.

4.6 Confirm MUA can achieve balance with all exhaust systems operating simultaneously (worst-case).

4.7 Document results in Section 4. Note any ASSUMPTIONS on welding exhaust as preliminary values.

**Verification:** MUA capacity >= total exhaust; heating capacity confirmed. Combustion air addressed if gas-fired. All preliminary values flagged.

---

### Step 5 — Heavy Equipment Exhaust System Sizing (REQ-M-005)

5.1 Determine number of exhaust hose drops per repair bay (TBD — not specified in RFP; ASSUMPTION: minimum 1 per bay; confirm with Owner or set as design decision). **Note: this is an indispensable input — if each bay has 2 drops rather than 1, exhaust flow doubles, affecting MUA sizing (Step 4) and system balance (Step 9) [Enrichment F-003].**

5.2 Establish required capture velocity at tailpipe (ASSUMPTION: per ACGIH Industrial Ventilation Manual for vehicle exhaust — typically 100-200 fpm minimum in hose or per hose manufacturer recommendation; specific value TBD).

5.3 Determine duct/hose inside diameter from capture velocity and required flow rate.

5.4 Estimate system static pressure:
- Hose losses
- Duct friction losses (from fan to exhaust outlet)
- Fitting losses
- Roof penetration and termination losses

5.5 Select fans to operate at the calculated flow and static pressure (confirm AMCA-rated performance).

5.6 Confirm exhaust outlets are positioned to prevent re-entrainment of exhaust into building fresh air intakes.

5.7 Document results in Section 5.

**Verification:** Fan selection point lies within the fan curve operating range. Capture velocity meets minimum requirement.

---

### Step 6 — Welding Station Exhaust Sizing (REQ-M-006)

6.1 If County welding equipment specifications have been received (PR-07): use actual equipment heat input and fume generation rate.

6.2 If County welding equipment specifications have NOT been received: use ASSUMPTION based on typical heavy-equipment maintenance welding (ASSUMPTION: wire-feed MIG welder, approximately 250-400A capacity; hood capture velocity per ACGIH 100 fpm minimum at capture point; note this as PRELIMINARY and flag for revision).

6.3 Size exhaust hood: determine required capture velocity, hood face area, and resulting flow rate.

6.4 Estimate duct static pressure (similar method to Step 5).

6.5 Select exhaust fan.

6.6 Issue formal RFI to County requesting welding equipment specifications if not yet received.

6.7 Document results in Section 6 with clear PRELIMINARY flagging if welding specs are assumed.

**Verification:** Hood sizing methodology referenced to ACGIH or equivalent standard. ASSUMPTION clearly labeled if welding specs not received.

---

### Step 7 — Service Pit Ventilation (REQ-M-007)

7.1 Confirm pit dimensions from structural drawings (DEL-002-06 — Service Pit Details; ASSUMPTION if not yet available: approximate from App B drawing).

7.2 Determine applicable ventilation requirements for below-grade maintenance pit from Alberta OH&S Code (ASSUMPTION: applicable) and Alberta Building Code.

7.3 Calculate required ventilation flow rate to maintain safe CO concentration levels during equipment operation (ASSUMPTION: continuous mechanical ventilation while pit is occupied; CO generation rate from diesel equipment TBD).

7.4 Size exhaust fan(s) and supply connection for the pit.

7.5 Confirm the pit ventilation is connected to the overall system balance (Step 4).

7.6 Document results in Section 7.

**Verification:** Calculated ventilation rate meets or exceeds Alberta OH&S minimum for occupied below-grade maintenance spaces. ASSUMPTIONS on pit dimensions and CO generation are clearly labeled.

---

### Step 8 — Ceiling Fan Selection (REQ-M-008)

8.1 Confirm total main shop area to be served by ceiling fans (ASSUMPTION: main shop floor area approximately 7,000-8,000 sq ft based on 130 ft x ~55-65 ft for the main bay area, excluding rooms; exact area TBD from confirmed architectural drawings).

8.2 Determine required fan diameter for effective destratification at 35 ft ceiling height (ASSUMPTION: large-diameter HVLS — High Volume Low Speed — fans are appropriate; 20-24 ft diameter typical for this ceiling height and bay area).

8.3 Confirm 6 fans cover the main shop area with appropriate overlap. **Document the basis for the quantity of 6 fans (coverage area analysis, manufacturer recommendation, or Owner preference — see Datasheet Enrichment A-005).**

8.4 Confirm fan mounting clearance below crane travel path (crane envelope critical constraint — PR-04). **Use crane envelope dimensions from structural/crane package; confirm minimum clearance per crane manufacturer requirements or Alberta OH&S (see Guidance T-01, Enrichment X-001).**

8.5 Confirm power requirements for each fan (three-phase or single-phase, voltage TBD) and coordinate with electrical design (DEL-004-08).

8.6 Document selection rationale in Section 8.

**Verification:** 6 fans confirmed adequate for main shop area at 35 ft ceiling. Fan quantity basis documented. Crane clearance confirmed. Power requirements communicated to electrical design.

---

### Step 9 — System Balance Summary (REQ-M-009)

9.1 Compile a system balance table. **Note: the air exchanger line items below assume bidirectional operation (separate supply and exhaust). This assumption is conditional on the resolution of CON-M-002 (see Guidance Conflict Table). If the air exchanger is determined to be exhaust-only, remove the supply row and adjust accordingly.**

> **[Enrichment E-005]:** Procedure Step 9 previously listed both "Air Exchanger -- Supply" and "Air Exchanger -- Exhaust" as separate line items, which pre-decided the unresolved question in Guidance CON-M-002. The table is now explicitly conditional on that conflict's resolution. Source: Specification.md REQ-M-003; Specification.md REQ-M-004; Procedure.md Step 9; Guidance.md T-02; Guidance.md CON-M-002.

| System | Flow (use primary unit convention per Guidance C-08) | Supply or Exhaust |
|---|---|---|
| MUA Unit | TBD | Supply |
| Air Exchanger — Supply (conditional on CON-M-002 resolution) | TBD | Supply |
| Air Exchanger — Exhaust | TBD | Exhaust |
| Heavy Equipment Exhaust (Bay 1) | TBD | Exhaust |
| Heavy Equipment Exhaust (Bay 2) | TBD | Exhaust |
| Welding Station Exhaust | TBD | Exhaust |
| Service Pit Exhaust | TBD | Exhaust |
| Wash Bay Exhaust (if dedicated per REQ-M-012) | TBD | Exhaust |
| Other Exhaust (washroom, etc.) | TBD | Exhaust |
| Combustion Air Supply (if gas-fired per REQ-M-013) | TBD | Supply (or neutral if drawn from MUA supply) |
| **Net (Supply minus Exhaust)** | **TBD** | **Target: neutral to slight positive** |

9.2 Confirm net balance is within the **quantitative acceptance threshold established per REQ-M-009 (TBD — see Specification Enrichment A-003)**.

9.3 If significant imbalance exists: adjust MUA capacity or air exchanger capacity to correct.

9.4 Document results in Section 9.

**Verification:** System balance table complete; net balance documented and within acceptance threshold.

---

### Step 10 — Code Compliance Reference Table (REQ-M-010)

10.1 Complete Section 10 with a **code compliance cross-reference matrix** mapping each applicable code requirement to the calculation section demonstrating compliance:

| Requirement | Code/Standard | Clause (if known) | Compliance Demonstrated In |
|---|---|---|---|
| Minimum heating | Alberta Building Code | TBD | Section 2 |
| Minimum ventilation rates | Alberta Building Code / ASHRAE 62.1 | TBD | Section 3 |
| Service pit ventilation | Alberta OH&S Code | TBD | Section 7 |
| Welding fume control | Alberta OH&S Code / ACGIH | TBD | Section 6 |
| Wash bay ventilation | Alberta Building Code | TBD | Section 3 |
| Combustion air supply (if gas-fired) | Alberta Building Code | TBD | Section 4 |
| Energy efficiency (if ASHRAE 90.1 applies) | ASHRAE 90.1 | TBD | TBD |
| ... | ... | ... | ... |

> **[Enrichment X-003]:** Code compliance cross-reference matrix replaces simple code reference table. Source: Specification.md Verification (REQ-M-010 row). PROPOSAL: Require a code compliance cross-reference matrix as part of Section 10 of the calculation package.

10.2 Flag any clauses where TBD is noted as requiring Mechanical Engineer review of specific code text.

---

### Step 11 — Review, Stamp, and Issue

11.1 Internal review: a second Mechanical Engineer (or senior reviewer) reviews all sections using the following **structured review checklist**:

| Review Item | Check | Reviewer Initials | Date |
|---|---|---|---|
| Arithmetic accuracy | All calculations checked for arithmetic errors | | |
| Assumption justification | Each assumption has a documented basis and consequence | | |
| Input traceability | All inputs traced to sources (drawings, codes, specifications) | | |
| Missing inputs identified | All TBD items flagged with resolution path | | |
| Code compliance | Code compliance matrix (Section 10) is complete for all applicable clauses | | |
| System balance closure | Net supply/exhaust balance within acceptance threshold | | |
| Drawing set consistency | Calculated flows and equipment capacities match DEL-003-02 through DEL-003-05 | | |
| Unit consistency | Airflow units are consistent with primary convention (Guidance C-08) throughout | | |
| Safety-critical items | Service pit ventilation (Section 7) reviewed for OH&S compliance | | |
| Welding exhaust status | Either finalized (County specs) or clearly flagged PRELIMINARY | | |
| Combustion air (if gas-fired) | Combustion air calculation present and complete | | |
| Crane clearance | Overhead equipment positions confirmed clear of crane envelope | | |

> **[Enrichment X-004]:** Structured review checklist added to make the internal review reproducible and auditable. Source: Procedure.md Step 11. PROPOSAL: Added review checklist as sub-table in Step 11.

11.2 Address all review comments.

11.3 Update Assumptions Register (Section 11) to reflect final state of assumptions.

11.4 Obtain P.Eng. stamp from a professional engineer licensed in Alberta. **(Stamp scope per REQ-M-011 — see Specification Enrichment D-001 for clarification on PRELIMINARY vs. FINAL version stamping.)**

11.5 Issue the calculation package as part of the IFC document set (coordinate with DEL-003-02 through DEL-003-07 issuance).

**11.6 Drawing/schedule reconciliation verification: before IFC issuance, explicitly verify that all calculated values (flows, capacities, equipment selections) have been transmitted to and reconciled with DEL-003-02 (HVAC Plans), DEL-003-03 (Ductwork Plans), DEL-003-04 (Exhaust Plans), and DEL-003-05 (Equipment Schedule). Document the reconciliation check.**

> **[Enrichment D-002]:** Drawing reconciliation verification step added. Procedure Step 11.5 mentioned coordination but did not include a verification checkpoint for reconciling calculation values with drawing values. Source: Procedure.md Step 11; Procedure.md Verification. PROPOSAL: Added verification step for drawing/schedule reconciliation.

11.7 Transmit calculation package to County via project manager per project coordination protocol (weekly meeting / County project manager — SOW-0086, SOW-0087).

**Verification:** Calculation package is stamped, indexed, issued as FINAL IFC, included in the mechanical IFC submission, and reconciled with downstream deliverables.

---

## Verification

| Check | What to Confirm |
|---|---|
| All sections populated | Sections 1-11 all contain content; no blank sections (TBD content is labeled, not empty) |
| Assumptions register complete | All assumptions are listed with basis and consequence |
| Welding exhaust status clear | Either finalized (County specs received) or clearly flagged PRELIMINARY with RFI issued |
| System balance closed | Net supply/exhaust balance within quantitative acceptance threshold (per REQ-M-009) |
| Crane clearance confirmed | Ceiling fan mounting and overhead equipment heights do not conflict with crane travel envelope |
| Mezzanine zone addressed | Mezzanine HVAC determination documented in Section 3 |
| Wash bay ventilation addressed | Wash bay moisture control calculation documented in Section 3 (REQ-M-012) |
| Combustion air addressed | If gas-fired equipment selected, combustion air calculation present (REQ-M-013) |
| IFC stamp obtained | P.Eng. stamp from Alberta-licensed professional engineer applied |
| Drawing coordination | Calculated flows and equipment capacities match what is shown on DEL-003-02, DEL-003-03, DEL-003-04 |
| Drawing/schedule reconciliation | Explicit reconciliation verification completed before IFC issuance [Enrichment D-002] |
| Equipment schedule consistent | DEL-003-05 equipment capacities match calculation package selections |
| County inspection copy | Copy of calculation package provided to County project manager |
| Review checklist completed | Structured review checklist (Step 11.1) signed off by reviewer [Enrichment X-004] |
| Commissioning handoff | Calculation package outputs transmitted to PKG-020 for commissioning test procedures [Enrichment X-005] |

---

## Records

The following documents shall be produced and retained as evidence of this deliverable:

| Record | Description | Retained By |
|---|---|---|
| Calculation Package (PRELIMINARY) | Draft version submitted for internal review | Mechanical Engineer |
| Calculation Package (FINAL — IFC) | P.Eng.-stamped final version included in IFC submission | Project Records; County |
| Assumptions Register | Record of all design assumptions and their basis | Mechanical Engineer / Project Records |
| RFI to County (welding specs) | Formal request for welding equipment specifications (if not yet received) | Project Manager |
| Internal Review Comments and Responses | Evidence that review comments were addressed | Mechanical Engineer |
| Internal Review Checklist (signed) | Completed structured review checklist from Step 11.1 [Enrichment X-004] | Mechanical Engineer |
| Transmittal Record | Record of IFC calculation package transmittal to County | Project Manager |
| Coordination Notes | Notes on coordination with Electrical (DEL-004-08) for ceiling fan power, and with Structural (DEL-002-07) for crane clearance | Mechanical Engineer |
| Drawing/Schedule Reconciliation Record | Record confirming calculated values were reconciled with DEL-003-02 through DEL-003-05 before IFC issuance [Enrichment D-002] | Mechanical Engineer |
| Commissioning Handoff Record | Record confirming calculation package outputs (design flows, temperatures, pressures, equipment capacities) were transmitted to PKG-020 (Building Systems Commissioning) for use in commissioning test procedures [Enrichment X-005] | Mechanical Engineer / PKG-020 |
| Revision Log | **Revision tracking record showing revision number, date, author, and change description for each version of the calculation package (PRELIMINARY through FINAL)** [Enrichment E-004] | Mechanical Engineer / Project Records |

> **[Enrichment X-005]:** Commissioning handoff record added. The calculation package provides the basis values (design flows, temperatures, pressures) that commissioning must verify, but no record previously addressed this handoff. Source: Procedure.md Verification; Procedure.md Records; Datasheet.md Construction Package Context.

> **[Enrichment E-004]:** Revision tracking requirement added. No mechanism previously existed for tracking changes between PRELIMINARY and FINAL versions. Source: Procedure.md Records.
