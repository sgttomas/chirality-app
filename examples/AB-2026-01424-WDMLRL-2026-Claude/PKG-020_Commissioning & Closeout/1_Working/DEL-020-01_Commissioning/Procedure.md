# Procedure — DEL-020-01: Building Systems Commissioning

**Document Type:** Procedure (operational)
**Deliverable ID:** DEL-020-01_Commissioning
**Package:** PKG-020 — Commissioning & Closeout
**Generated:** 2026-02-26 (Pass 1+2, P1_P2 run)
**Enriched:** 2026-02-26 (Pass 3, Semantic Lensing)

---

## Purpose

This procedure describes the steps to **produce and complete** the Building Systems Commissioning deliverable (DEL-020-01) for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. It covers the activities from commissioning planning through to final sign-off and handoff to the final inspection process (DEL-020-02).

The procedure is written from the perspective of the Commissioning Agent and Project Manager as responsible parties.

---

## Prerequisites

The following conditions must be satisfied before commissioning activities may begin. These are derived from declared upstream dependencies and contractual requirements.

| Prerequisite | Evidence Required | Source |
|---|---|---|
| Commissioning Agent assigned (meeting qualification requirements per REQ-020-01-014) | Assignment documentation / contract; qualification evidence | `_STATUS.md` Outstanding Items; `_CONTEXT.md` Key Roles; Specification REQ-020-01-014 |
| All construction substantially complete — PKG-019 sign-off obtained | Written sign-off from QC Manager (DEL-019-04) | `_DEPENDENCIES.md` |
| All trade installations complete: mechanical (PKG-013), plumbing (PKG-014), electrical (PKG-015), crane (PKG-016) | Trade completion reports / punch list close-out | Decomposition PKG-020 Exclusions |
| All applicable Safety Code inspections passed (PKG-009 scope) | Copies of completed inspection reports | RFP §3.3.2; SOW-0084, SOW-0085 |
| IFC design documents available for reference | IFC drawing set on site | ASSUMPTION: standard commissioning prerequisite |
| Commissioning Plan developed and approved (per REQ-020-01-003A) | Approved Commissioning Plan document | Specification REQ-020-01-003A; see Step 1 |
| County project manager identified and available | Contact confirmed at project award | RFP §3.1 |
| Commissioning schedule confirmed within overall project schedule | Schedule document | Guidance Considerations — Schedule Pressure |

---

## Steps

### Step 1 — Develop the Commissioning Plan

**Responsible Party:** Commissioning Agent

**Timing:** Before any system testing begins; ASSUMPTION: ideally during construction phase.

**Activities:**
1. Review IFC design documents for all systems to identify design parameters and acceptance criteria per system.
2. Identify all systems to be commissioned, grouping by discipline: mechanical, plumbing/water, electrical/low-voltage, crane, building envelope, safety/emergency systems. Include scope determination for fire protection systems (if any — see Specification Note [C-002]) and Old North Shop renovation-area systems (see Datasheet Note [B-002]).
3. Define measurable acceptance criteria for each system based on IFC design parameters and RFP §3.4 design requirements. Where IFC documents are not yet available, record acceptance criteria as TBD. Acceptance criteria must include pass/fail thresholds, not just evidence descriptions (see Note [A-005]).
4. Develop a system-by-system test sequence that respects installation dependencies (refer to Guidance — Considerations: System Interdependencies).
5. Assign commissioning responsibilities: who performs testing for each system (Commissioning Agent, trade subcontractors, equipment suppliers).
6. Identify any third-party testing requirements (e.g., crane load testing per Alberta Safety Code — specific requirements TBD). Consider whether independent third-party verification is warranted for safety-critical systems (see Guidance Note [F-001]).
7. Identify County PM involvement points: which milestone sign-offs require Owner attendance.
8. Develop commissioning schedule; confirm it fits within overall project schedule and December 31, 2026 deadline (SOW-0091; RFP §3.1).
9. Prepare test record templates for each system.
10. Define the Owner acceptance process for commissioning results (see Specification Note [F-003]).
11. Define the deficiency resolution process: maximum resolution timeframe, escalation path, and closure criteria (see Note [D-003]).
12. Define low-voltage systems commissioning scope boundary (wiring continuity only vs. end device functional testing) with Owner input (see Specification Note [X-001]).
13. Submit Commissioning Plan to County project manager for review.

**Output:** Approved Commissioning Plan document.

---

### Step 2 — Pre-Commissioning Verification

**Responsible Party:** Commissioning Agent; Trade Subcontractors

**Timing:** After construction completion, before functional testing.

**Activities:**
1. Walk all systems with trade subcontractors to confirm installation completeness.
2. Confirm all safety-critical items are in place before energizing systems (electrical isolation, pressure relief valves, crane clearances, etc.). ASSUMPTION: specific pre-commissioning checklist items will be identified in the Commissioning Plan.
3. Confirm electrical power is available and safe to energize per electrical contractor sign-off.
4. Confirm plumbing systems pressure-tested and passed inspection before filling with water.
5. Confirm crane structural supports, rails, and power circuits verified by installer.
6. Record any deficiencies found during pre-commissioning walk. Log all deficiencies in the deficiency log with severity classification, assigned party, and target resolution date per the deficiency resolution process defined in the Commissioning Plan (see Note [D-003]). Resolve deficiencies before proceeding to functional testing.
7. Notify County project manager that pre-commissioning verification is complete and functional testing is ready to begin.

**Output:** Completed pre-commissioning verification checklist; deficiency log (resolved).

---

### Step 3 — Electrical and Low-Voltage Systems Testing

**Responsible Party:** Commissioning Agent; Electrical Subcontractor

**Timing:** First in commissioning sequence — required to power downstream systems.

**Activities:**
1. Energize three-phase power distribution system; confirm service entrance, panels, and distribution correct.
2. Test all lighting circuits: confirm function in all areas (office, parts room, service pit, wash bay, shop bays, mezzanine, exterior). Record results.
3. Test all receptacle circuits by discipline (15A general; 50A/240V welding circuits per Decomposition D-009; ASSUMPTION: specific circuit ratings per IFC electrical drawings — location TBD).
4. Test overhead door power circuits: confirm operation of all overhead doors.
5. Test crane power circuits: confirm power available at each crane runway (functional test of crane in Step 4).
6. Test pump power circuits for plumbing systems.
7. Test low-voltage systems: security camera wiring continuity; radio antenna wiring continuity. ASSUMPTION: functional testing of security camera and radio equipment may require Owner-supplied equipment — confirm with County. Scope boundary (continuity only vs. functional testing) per Commissioning Plan determination (see Specification Note [X-001]).
8. Verify service pit lighting and ventilation circuits functional.
9. Record all test results against measurable acceptance criteria defined in the Commissioning Plan. Note any failures and initiate deficiency resolution per the defined process.

**Output:** Electrical systems test record (completed per system).

---

### Step 4 — Crane and Lifting Systems Testing

**Responsible Party:** Commissioning Agent; Crane Installer; (Third-party inspector if required by Alberta Safety Code — TBD)

**Timing:** After electrical systems commissioned (Step 3).

**Activities:**
1. Confirm crane structural installation and rail alignment complete.
2. Functional test Crane 1: bridge travel full span; trolley travel full beam; hoist raise and lower through full range; test limit switches (upper, lower, travel limits).
3. Functional test Crane 2: same as above.
4. Perform load testing per applicable Alberta Safety Code requirements (specific code section TBD — location TBD in accessible sources; see Specification Note [C-001]). ASSUMPTION: load test to rated capacity (5 tonnes) using calibrated test weights or load cells.
5. If Alberta Safety Code requires a Safety Codes Officer or certified inspector for crane acceptance, schedule and coordinate this inspection. Obtain inspection certificate.
6. Record all functional and load test results against measurable pass/fail criteria. Obtain inspector sign-off if required.
7. Confirm operator training will cover crane operation (see Step 10).

**Output:** Crane test record; load test results; Safety Codes Officer inspection certificate if required (TBD).

---

### Step 5 — Mechanical and HVAC Systems Testing

**Responsible Party:** Commissioning Agent; Mechanical Subcontractor

**Timing:** After electrical systems commissioned (Step 3); concurrent with or after plumbing (Step 6 may be concurrent).

**Activities:**
1. Start and test high recovery heating system: confirm ignition, heat output, thermostat/controls function. Record achieved output vs. design parameter (TBD per IFC mechanical drawings).
2. Test makeup air unit: confirm airflow, heating function, controls.
3. Test high volume air exchanger: confirm airflow rates. Record achieved rate vs. design parameter (TBD per IFC).
4. Test exhaust systems: confirm exhaust hose connections and fans function in repair bays.
5. Test welding station ventilation: confirm operation.
6. Test ceiling fans: confirm all units function.
7. Test service pit ventilation and lighting (coordinate with electrical test record from Step 3 for lighting; confirm mechanical ventilation if provided).
8. Record all test results against measurable acceptance criteria. Note any deficiencies.

**Output:** Mechanical/HVAC systems test record.

---

### Step 6 — Plumbing and Water Systems Testing

**Responsible Party:** Commissioning Agent; Plumbing Subcontractor

**Timing:** After electrical systems commissioned (pump power available — Step 3).

**Activities:**
1. Fill 50,000 L cistern: confirm capacity; inspect for leaks.
2. Test pump system: start pump; measure flow rate at fill connection. Target: 100 LPM (RFP §3.4). Record measured flow rate. Confirm 2.5 inch cistern filling connection functions correctly.
3. Test internal water distribution: confirm water pressure and flow at all fixtures (wash sink, emergency shower, washroom fixtures, bulk water fill — confirm all outlets functional).
4. Test bulk water fill: confirm high volume pump for external filling functions (flow rate TBD per IFC).
5. Confirm septic system connection and function (2,000 US Gallon holding tank per RFP §3.4); coordinate with any required Safety Code inspection.
6. Test wash bay drainage: confirm floor drain flow to mud sump.
7. Test mud sump: confirm sump function and cleanout access per design.
8. Test sump drains in repair bays: confirm drainage flow.
9. Test emergency shower: confirm activation and flow. Record performance parameters (flow rate, activation method). ASSUMPTION: emergency shower testing per applicable Alberta OH&S requirements — specific requirements TBD. (See also Datasheet Note [B-001] for system enumeration.)
10. Record all test results against measurable acceptance criteria. Note any deficiencies.

**Output:** Plumbing/water systems test record (including measured pump flow rate).

---

### Step 7 — Building Envelope Systems Testing

**Responsible Party:** Commissioning Agent; General Contractor / Subcontractors

**Timing:** After construction completion; may run concurrent with trade system testing.

**Activities:**
1. Test all overhead doors: confirm operation (manual and power), limit stops, safety reversal function.
2. Test all entrance doors: confirm operation, hardware function, sealing.
3. Test parts room roll-up door (6-foot wide, per RFP §3.4): confirm operation.
4. Inspect wash bay enclosure: confirm completeness and drainage integration (note: wash bay drainage tested under Step 6; enclosure integrity verified here — see Datasheet Note [E-001]).
5. Record all test results.

**Output:** Building envelope systems test record.

---

### Step 8 — Integrated Systems Verification

**Responsible Party:** Commissioning Agent

**Timing:** After all individual system tests complete (Steps 3–7).

**Activities:**
1. Verify cross-system interfaces: confirm HVAC and electrical systems operate together without interference.
2. Verify plumbing pump operation does not cause electrical circuit issues.
3. Confirm lighting levels in all areas adequate for intended use (ASSUMPTION: no specific lux levels defined in RFP — confirm with Owner; measurable criteria TBD per Commissioning Plan — see _SEMANTIC_LENSING.md D-002).
4. Walk facility with County project manager; demonstrate key system operations.
5. Confirm all deficiencies from individual system tests have been resolved per the deficiency resolution process. Update deficiency log to confirm closure.

**Output:** Integrated verification sign-off; resolved deficiency log.

---

### Step 9 — Performance Documentation, As-Built Verification, and Review

**Responsible Party:** Commissioning Agent; Project Manager

**Timing:** After integrated systems verification (Step 8).

**Activities:**
1. Compile all system test records into Performance Verification Report. Confirm each system's achieved performance against design parameters.
2. Identify any systems that did not meet acceptance criteria; document corrective actions taken and re-test results.
3. Compile O&M manuals received from subcontractors and equipment suppliers for all commissioned systems.
4. Compile all Safety Code inspection reports and certificates.
5. **Verify as-built drawings against installed conditions:** walk the facility with as-built drawings and confirm that all commissioned systems are accurately reflected in the as-built documentation. Record any discrepancies and coordinate corrections with the responsible trade before finalizing. (Source: Datasheet Anticipated Artifacts; _SEMANTIC_LENSING.md X-002.)
6. Compile verified as-built drawings into the commissioning documentation package.
7. Prepare draft Commissioning Completion Report: summary of all systems tested, results, deficiencies resolved, as-built verification status, and confirmation of facility readiness.
8. Submit draft to County project manager for review.

**Output:** Draft Commissioning Completion Report; compiled O&M manuals; compiled test records; verified as-built drawings.

---

### Step 10 — Operator Training

**Responsible Party:** Commissioning Agent; Trade Subcontractors / Equipment Suppliers (as applicable)

**Timing:** After systems verified functional (Steps 3–8); before facility occupancy.

**Activities:**
1. Identify County facility staff to be trained on each system.
2. Deliver training on each system: HVAC controls and maintenance; plumbing/cistern/pump operation; electrical panel and circuit management; crane operation and safety (ASSUMPTION: crane training requires qualified trainer); overhead door operation; emergency systems (emergency shower, fire protection if applicable — TBD).
3. Provide O&M manuals to trainees at time of training.
4. Record training attendance: names, roles, systems covered, date.
5. Verify training effectiveness through at least one competence verification method (e.g., demonstrated operation of key systems, observed task performance, or written/oral assessment). Record competence verification results. (Source: Specification Note [E-002]; _SEMANTIC_LENSING.md E-002.)
6. Obtain County representative sign-off confirming training received and competence demonstrated.

**Output:** Operator training records (attendance logs, competence verification results, sign-offs); O&M manuals delivered.

---

### Step 11 — Final Commissioning Sign-off and Handoff

**Responsible Party:** Project Manager; Commissioning Agent

**Timing:** After operator training complete (Step 10); before initiating DEL-020-02 (Final Inspection).

**Activities:**
1. Finalize Commissioning Completion Report incorporating all test records, performance results, as-built verification, and training records.
2. Confirm all commissioning documents compiled:
   - Commissioning Plan (approved)
   - System test records (all disciplines)
   - Performance Verification Report
   - Operator training records (including competence verification)
   - O&M manuals
   - Safety Code inspection reports and certificates
   - Verified as-built drawings
   - Commissioning schedule (actual vs. planned — see Note [X-003])
   - Commissioning Completion Report
3. Submit complete commissioning package to County project manager.
4. Obtain County project manager formal acceptance of commissioning package per the acceptance process defined in the Commissioning Plan (see Specification Note [F-003]).
5. Confirm facility readiness for final inspection (DEL-020-02 gate condition satisfied).
6. Notify Project Manager that DEL-020-01 is complete; initiate DEL-020-02.

**Output:** Finalized Commissioning Completion Report; complete commissioning documentation package delivered to Owner; DEL-020-02 gate confirmed open.

---

## Verification

| Verification Check | Evidence | Pass/Fail Basis | Timing |
|---|---|---|---|
| All systems tested: mechanical, plumbing, electrical, crane, building envelope | Test records for each system completed | All systems on the Commissioning Plan scope list have completed test records | After Steps 3–7 |
| Cistern pump achieves 100 LPM (RFP §3.4) | Measured flow rate recorded in plumbing test record (Step 6) | Measured flow rate >= 100 LPM | Step 6 |
| Cistern capacity confirmed at minimum 50,000 L (RFP §3.4) | Fill confirmation noted in plumbing test record (Step 6) | Confirmed fill to 50,000 L without overflow/leak | Step 6 |
| Septic tank (2,000 US Gallon) confirmed functional (RFP §3.4) | Plumbing test record (Step 6) | Tank holds volume; connections functional | Step 6 |
| Cranes (2 x 5-tonne) load tested (RFP §3.4) | Crane test record and load test results (Step 4) | Load test to rated capacity passed per Alberta Safety Code (specific criteria TBD) | Step 4 |
| All electrical circuits energized and functional | Electrical test record (Step 3) | All circuits on scope list tested; no unresolved failures | Step 3 |
| Deficiency log closed (all deficiencies resolved) | Resolved deficiency log per defined closure criteria | All deficiencies meet closure criteria defined in Commissioning Plan (see Note [D-003]) | Step 8 |
| Operator training delivered, documented, and competence verified | Training attendance records; competence verification results; O&M manuals delivered (Step 10) | Attendance complete; competence demonstrated per defined method | Step 10 |
| As-built drawings verified against installed conditions | As-built verification walkthrough record (Step 9) | Discrepancies identified and corrected | Step 9 |
| Safety Code inspections complete | Inspection reports on file | All applicable inspections passed; certificates on file | Prior to commissioning start (Prerequisite); ongoing through commissioning |
| Commissioning package complete and delivered to Owner | County PM formal acceptance (Step 11) | Package accepted per defined acceptance process | Step 11 |
| DEL-020-02 gate condition met | PM confirmation (Step 11) | Confirmation documented | Step 11 |
| December 31, 2026 deadline met (SOW-0091) | Commissioning schedule tracking (retained as record — see Note [X-003]) | Commissioning complete before deadline | Throughout |

**Note [A-005]:** The Verification table above has been enhanced to include a "Pass/Fail Basis" column that describes the measurable threshold or condition for each verification check. For checks where the pass/fail basis depends on IFC design parameters not yet available, the basis is stated as "per Commissioning Plan criteria" and remains TBD. This addresses the gap identified in _SEMANTIC_LENSING.md A-005. (Source: Procedure.md Verification; _SEMANTIC_LENSING.md A-005. ProposedAuthority: Commissioning Plan — once developed.)

---

## Records

The following records shall be retained as evidence of commissioning completion. These records feed into DEL-020-03 (Closeout Documentation).

| Record | Description | Custodian |
|---|---|---|
| Approved Commissioning Plan | Scope, protocols, acceptance criteria, schedule, responsibilities | Commissioning Agent / PM |
| Pre-commissioning verification checklist | Walk-through results before functional testing | Commissioning Agent |
| System test records (per discipline) | Completed test checklists: electrical, mechanical, plumbing, crane, envelope | Commissioning Agent |
| Deficiency log | All deficiencies identified, resolution actions, closure confirmation | Commissioning Agent |
| Performance Verification Report | Summary of achieved vs. design performance per system | Commissioning Agent / PM |
| Safety Code inspection reports and certificates | All applicable inspection reports (copies per SOW-0085) | Project Manager |
| Operator training records | Attendance logs, competence verification results, training materials, sign-offs | Commissioning Agent / PM |
| O&M Manuals | Operation and maintenance documentation; one set retained by Owner | Delivered to Owner (County) |
| Verified as-built drawings | As-built drawings confirmed against installed conditions during commissioning | Commissioning Agent / PM |
| Commissioning schedule (actual vs. planned) | Schedule tracking record showing commissioning timeline against project deadline | Commissioning Agent / PM |
| Commissioning Completion Report (final) | Formal record confirming commissioning outcomes; accepted by Owner | PM; copy to Owner |

**Note [X-003]:** The commissioning schedule has been added to the Records table. The Verification table cites "Project schedule tracking" as evidence for deadline compliance, but the commissioning schedule was not previously listed as a retained record. An auditor would require this record to verify deadline compliance. (Source: Procedure.md Verification final row; _SEMANTIC_LENSING.md X-003.)

**Note [A-004]:** Record retention and audit trail requirements should specify how commissioning records will be preserved, indexed, and made retrievable for future regulatory audit. The retention period, indexing scheme, and audit access mechanism are TBD — to be defined per Owner/County records policy and applicable regulatory requirements. ASSUMPTION: records should be retained for the duration of the guarantee period (2 years post-CCC per RFP §2.10) at minimum, and thereafter per applicable regulatory requirements. (Source: _SEMANTIC_LENSING.md A-004. ProposedAuthority: Owner/County records policy; CCDC 14-2013.)

**Note [D-003]:** The deficiency resolution process should define: (a) maximum resolution timeframe per deficiency severity, (b) escalation path if deficiencies cannot be resolved within the timeframe, and (c) criteria for determining when a deficiency is sufficiently resolved to proceed. These process parameters are TBD — to be established in the Commissioning Plan. Particular attention should be given to the December 31, 2026 deadline: if a deficiency cannot be resolved before the deadline, the escalation path and conditional acceptance provisions must be clearly defined. (Source: Procedure.md Steps 2, 8, 9; _SEMANTIC_LENSING.md D-003. ProposedAuthority: Commissioning Plan — once developed.)
