# Procedure — DEL-004-06 Panel Schedules

---

## Purpose

This procedure describes the steps to produce and issue the Panel Schedules for DEL-004-06 as part of the PKG-004 Electrical Design IFC drawing set for the West Dried Meat Lake Regional Landfill New North Shop Addition.

The procedure covers: gathering design inputs, establishing the panel schedule structure, populating circuit data, coordinating with other PKG-004 deliverables and other disciplines, obtaining County approval at the preliminary stage, and issuing the final stamped document(s) for construction.

---

## Prerequisites

### Design Inputs Required

| Input | Source | Status |
|---|---|---|
| RFP §3.4 design requirements (three-phase, load list) | R-01: AB-2026-01424-WDMLRL RFP.pdf | Available |
| App B (Electrical) conceptual layout and load notes | R-05: AB-2026-01424-Appendix B (Electrical).pdf | Available |
| Utility service information (voltage, available fault current, service entrance location) | Utility provider (ATCO Electric or applicable utility) | TBD — Electrical Engineer to obtain |
| Crane electrical specifications | Crane supplier (2 × 5-tonne overhead cranes) | TBD — per RFP §3.4 |
| Welding equipment specifications | County (RFP §3.4: "County to supply welding equipment specifications") | TBD — County to supply |
| Exhaust fan specifications | PKG-003 Mechanical Design (DEL-003-05 Mechanical Equipment Schedule) | TBD — from Mechanical Engineer |
| Overhead door operator specifications | Architectural/Structural (PKG-001, PKG-011) | TBD |
| Compressor, fire hose pump, pressure washer specs (to confirm 40A, 70A, 70A) | Procurement / Owner | TBD — confirm against App B notes |
| DEL-004-02 Single-Line Diagram | PKG-004 internal | Required before finalizing panel hierarchy |
| DEL-004-03 Power Distribution Plans | PKG-004 internal | Required for panel locations and feeder routing |
| DEL-004-04 Lighting Plans | PKG-004 internal | Required for lighting circuit counts |
| DEL-004-05 Receptacle Layout Plans | PKG-004 internal | Required for receptacle circuit counts |
| DEL-004-08 Electrical Calculation Package | PKG-004 internal | Required for verified load values and breaker sizing |

### References Required

- Canadian Electrical Code, Part I (CSA C22.1) — current edition adopted in Alberta (location TBD — ASSUMPTION: applicable)
- Alberta Safety Codes Act and applicable Alberta Electrical Permit requirements (location TBD)
- CCDC 14–2013 (contract context — not a technical standard for panel schedule production)

### Personnel

- Electrical Engineer (P.Eng., licensed in Alberta) — design authority and stamp holder
- ASSUMPTION: Electrical design drafting staff (CAD/BIM technician) — TBD per Proponent's team structure

---

## Steps

### Phase 1 — Preliminary Panel Schedule (for County Approval)

**Step 1.1 — Compile the Load List**
Using Appendix B (Electrical) and RFP §3.4, compile a complete list of all electrical loads for the New North Shop Addition. For each load, record:
- Load description
- Estimated amperage and voltage (from App B or equipment specs when available)
- Phase type (1Ø or 3Ø)
- Space (area of building served)

Loads to include at minimum: all lighting circuits (including ceiling fans -- 6 units), all receptacle types, crane circuits (2 units), overhead doors, compressor (40A), fire hose pump (70A), pressure washer (70A), exhaust fans, service pit lighting and ventilation (per Guidance C5 and Specification REQ-004-06-05B), and provisions for low-voltage system power supplies.
Source: App B (Electrical) notes and legend; RFP §3.4.

**Step 1.2 — Confirm Utility Service Parameters**
Contact the applicable electrical utility (ASSUMPTION: ATCO Electric or distribution utility serving Camrose County — to be confirmed) to obtain:
- Available service voltage and phases
- Available fault current at the service entrance
- Service entrance location and capacity limitations

Record confirmed service voltage in panel schedule header(s). Until confirmed, hold as TBD.
Source: ASSUMPTION — standard pre-design requirement; not stated in RFP.

**Step 1.3 — Establish Panel Hierarchy**
In coordination with the Single-Line Diagram (DEL-004-02), determine:
- Number and designation of panels (main distribution panel, sub-panels if required)
- Panel locations (coordinate with Power Distribution Plans DEL-004-03)
- Feeder routing (from Power Distribution Plans)

ASSUMPTION: Panel hierarchy to be established by the Electrical Engineer based on load calculations and building layout.

**Step 1.4 — Produce Preliminary Panel Schedule Draft**
For each panel, create a tabular schedule including:
- Panel designation and location
- Supply source
- Main breaker/disconnect rating (estimated)
- Bus rating (estimated)
- Voltage, phase, wire configuration
- Circuit table with preliminary circuit assignments (load description, estimated amps, breaker size, poles)
- Phase load totals (estimated)
- Spare positions (minimum to be determined by Electrical Engineer)

Use TBD for values not yet confirmed. Label estimates clearly.

**Step 1.5 — Internal Cross-Check (Preliminary)**
Cross-check the preliminary panel schedule against:
- Lighting Plans (DEL-004-04) — verify all lighting circuits are present
- Receptacle Layout Plans (DEL-004-05) — verify all receptacle circuits are present
- Power Distribution Plans (DEL-004-03) — verify panel locations and feeder sizes are consistent
- Single-Line Diagram (DEL-004-02) — verify panel hierarchy is consistent

Resolve discrepancies before County submission.

**Step 1.6 — Submit Preliminary Design for County Approval**
Include the preliminary panel schedule (with other preliminary PKG-004 deliverables) in the Preliminary Design submission to the County project team for approval.
Source: RFP §3.3.2 ("Deliver Preliminary Design for the County project team to approve.").

**Step 1.7 — Incorporate County Feedback**
Record County comments. Revise panel schedule as directed. Document all changes.

---

### Transition Gate — Preliminary to IFC Readiness

Before proceeding to Phase 2, the Electrical Engineer shall confirm the following readiness criteria are met. This decision gate defines the transition from preliminary design to final IFC development:

| Criterion | Confirmation Required |
|---|---|
| County preliminary approval | Written or documented approval received per REQ-004-06-13 (format TBD) |
| Outstanding County comments | All comments from Step 1.7 resolved or dispositioned |
| Critical equipment specs status | Status of crane, welding, and exhaust fan specifications assessed; proceed/hold decision documented |
| Utility service parameters | Service voltage confirmed or proceed-with-TBD decision documented |

**If all criteria are met:** Proceed to Phase 2.
**If critical criteria are not met:** Document the gap and obtain Electrical Engineer's authorization to proceed at risk, or hold until resolved.

ASSUMPTION: This transition gate is inferred from standard engineering practice. Specific gate criteria are not stated in the RFP. The Electrical Engineer and project manager should define the specific gate criteria for this project. (Lensing item D-002.)

---

### Phase 2 — Final Panel Schedule (IFC)

**Step 2.1 — Obtain Outstanding Equipment Specifications**
Obtain and review:
- Crane electrical specifications (2 × 5-tonne) — verify circuit sizing required
- County-supplied welding equipment specifications — confirm receptacle ratings
- Exhaust fan schedules from Mechanical Engineer — confirm circuit sizing
- All other equipment specs flagged as TBD in Step 1.1

Update load list accordingly.

**Step 2.2 — Complete Electrical Calculation Package (DEL-004-08)**
Ensure Electrical Calculation Package is complete and that calculated demand loads, service sizing, and feeder sizing are finalized. Panel schedule breaker ratings and bus ratings must be consistent with the calculation package.
Source: ASSUMPTION — standard engineering practice.

**Step 2.3 — Finalize Panel Schedule Data**
For each panel, finalize:
- Main breaker/disconnect rating
- Bus rating
- All circuit assignments: circuit number, load description, poles, breaker size (amps), conductor size and type, connected load (amps or VA), demand factor, demand load
- Phase assignments for single-phase loads (verify load balance)
- Spare circuit positions (labeled "SPARE")
- Panel totals: connected load per phase, demand load per phase, power factor (if applicable)

Apply CEC Part I sizing rules throughout (ASSUMPTION: CEC Part I governs; location TBD).

**Step 2.3A — Three-Phase Load Balancing**
Distribute single-phase loads across the three phases to minimize imbalance per Guidance P2. For each panel:
1. List all single-phase loads with their phase assignment and amperage.
2. Calculate the total connected load per phase (Phase A, Phase B, Phase C).
3. Adjust phase assignments to minimize the difference between the highest and lowest loaded phases.
4. Document the phase balance summary showing load per phase and the resulting imbalance percentage.
5. Verify the imbalance is within the acceptable limit (TBD -- see Guidance Conflict Table CF-004-06-02 for the open question on the specific threshold).

The load balancing documentation shall be retained as part of the Internal Cross-Check Record (see Records).
ASSUMPTION: Load balancing procedure is inferred from standard three-phase distribution design practice. Specific procedure not stated in RFP or accessible sources. (Lensing item A-004.)

**Step 2.4 — Final Internal Cross-Check**
Repeat cross-check of Step 1.5 against all finalized IFC drawings:
- All loads on drawings have a corresponding circuit in the schedule
- Circuit numbers on drawings match circuit numbers in schedule
- Breaker ratings and conductor sizes are consistent with Calculation Package (DEL-004-08)
- Panel designations match Single-Line Diagram (DEL-004-02)
- No orphaned circuits (circuits in schedule not shown on drawings)

**Step 2.5 — Cross-Discipline Coordination Check**
Verify with other discipline leads. For each coordination item, document: (a) what data was exchanged, (b) confirmation of agreement or disagreement, and (c) the form of confirmation (email, meeting minutes, markup, etc.):

| Discipline | Coordination Item | Data to Exchange | Confirmation Record |
|---|---|---|---|
| Mechanical Engineer (PKG-003) | Exhaust fan circuits | Fan HP/kW, voltage, quantity from mechanical equipment schedule | Written confirmation that circuit sizing matches mechanical specs |
| Structural Engineer (PKG-002) | Electrical routing clearances | Panel locations, conduit routing near structural elements | Written confirmation of no conflicts |
| Plumbing Engineer (PKG-006) | Fire hose pump and pressure washer circuits | Equipment HP/kW, voltage, starting current from equipment specs | Written confirmation that circuit ratings match equipment requirements |

**If disagreements arise:** Document the disagreement, notify the project manager, and hold the affected circuit entries as TBD until resolved.

ASSUMPTION: Cross-discipline coordination is a standard design-build obligation; specific coordination protocol to be established by the Proponent's project manager. The table above defines a minimum coordination scope; additional items may be needed. (Lensing item C-003.)

**Step 2.6 — P.Eng. Review and Stamp**
The Electrical Engineer (P.Eng., Alberta) reviews all panel schedule sheets for technical correctness and code compliance. Upon satisfaction:
- Apply professional engineer stamp and signature to each panel schedule sheet
- Confirm date of issue

Source: RFP §3.3.2 ("All Issued For Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta.").

**Step 2.6A — Version Control and Revision Tracking**
Before issuing the IFC panel schedule, confirm that all revisions between the preliminary design (Step 1.4) and the final IFC version are tracked. The version control procedure shall include:
1. Revision numbering (e.g., Rev 0 = Preliminary, Rev 1 = IFC)
2. A revision log noting what changed between each version and why
3. Confirmation that superseded preliminary versions are clearly marked as such
4. Distribution of revision notices to all parties who received prior versions

**The specific version control and reissue protocol is TBD -- to be defined by the Proponent's project manager.** See Guidance C7.
ASSUMPTION: Version control procedure inferred from standard design-build practice; not stated in RFP. (Lensing item A-005.)

**Step 2.7 — Issue for Construction**
Issue the signed and stamped Panel Schedules as part of the IFC drawing set for PKG-004. Distribute to:
- Owner (Camrose County) / County project representative
- Electrical contractor (PKG-015)
- General contractor / Prime Contractor
- Project file

**Document the distribution with a transmittal record** that includes: date of issue, revision number, list of recipients, method of delivery, and confirmation of receipt. The transmittal record shall be retained in the project file. (Lensing item E-003.)

---

## Verification

| Check | Method | Pass Condition |
|---|---|---|
| All App B loads present | Compare panel schedule circuit list to App B load notes and legend | Every named load in App B has a circuit entry in the schedule |
| Three-phase service confirmed | Check panel schedule header | Header shows three-phase supply |
| Named equipment loads correct | Verify 40A compressor, 70A fire hose pump, 70A pressure washer circuit entries | Three entries present with correct amp ratings (or revised per equipment specs) |
| Crane circuits present | Count crane circuit entries | Minimum 2 crane circuits present |
| Load balance acceptable | Check phase totals per Step 2.3A load balancing documentation | Phase imbalance within acceptable limit -- **specific numeric threshold TBD** (per CEC Part I or Electrical Engineer's defined criterion; see Guidance Conflict Table CF-004-06-02) (lensing item X-004) |
| Ceiling fan circuits present | Confirm 6 ceiling fan circuit entries | Six ceiling fans accounted for with load data (per Specification REQ-004-06-05A) |
| Service pit circuits present | Confirm service pit lighting and ventilation circuit entries | Circuits present per Specification REQ-004-06-05B |
| Circuit number cross-reference | Compare circuit numbers on drawings vs. schedule | All numbers match |
| Calculation Package consistency | Compare panel ratings to DEL-004-08 calculated loads | Panel and breaker ratings match calculated demand loads |
| P.Eng. stamp present | Visual check of issued sheets | Stamp, signature, and date present on all sheets |
| County preliminary approval on file | Project document check | Approval documented prior to IFC issue |
| Alberta Safety Code compliance | P.Eng. review; subsequent inspection | No non-compliances noted |

---

## Records

The following records shall be produced and retained as evidence that this procedure was followed:

| Record | Description | Retained By |
|---|---|---|
| Preliminary Panel Schedule (draft) | Panel schedule as submitted with Preliminary Design | Project file |
| County Preliminary Approval | Written or email confirmation from County project team | Project file |
| Equipment Specification Log | Log of equipment specs received and incorporated. **Minimum required fields (TBD -- template to be defined by Electrical Engineer):** equipment name, spec received date, source/supplier, key electrical parameters (HP/kW, voltage, current, duty cycle), panel schedule circuits affected, and date incorporated into panel schedule. (Lensing item E-004.) | Electrical Engineer |
| Electrical Calculation Package (DEL-004-08) | Supporting load calculations for panel sizing | Electrical Engineer / Project file |
| Internal Cross-Check Record | Notes from Steps 1.5, 2.3A (load balancing), and 2.4. **Format TBD -- Electrical Engineer to define a cross-check record template.** At minimum, the record should include: (a) date of cross-check, (b) drawings/documents compared, (c) discrepancies found and resolution, (d) load balance summary per Step 2.3A, and (e) sign-off by the Electrical Engineer. (Lensing item X-005.) | Electrical Engineer |
| IFC Panel Schedule Sheets (stamped) | Final issued panel schedule sheets, P.Eng. stamped | Project file; distributed to parties above |
| IFC Transmittal Record | Distribution transmittal for Step 2.7 IFC issue, including: date, revision number, recipients, delivery method, receipt confirmation. (Lensing item E-003.) | Project file |
| Revision Log | Log of all revisions from preliminary to IFC per Step 2.6A, including revision number, date, description of changes, and reason. (Lensing item A-005.) | Project file |
| Alberta Safety Code Inspection Report | Inspection confirmation (obtained during construction by PKG-015) | Prime Contractor / Project file |

ASSUMPTION: Record retention requirements beyond the above may apply under the CCDC 14–2013 contract and/or Alberta Safety Codes Act. The Proponent's project manager should confirm retention obligations.
