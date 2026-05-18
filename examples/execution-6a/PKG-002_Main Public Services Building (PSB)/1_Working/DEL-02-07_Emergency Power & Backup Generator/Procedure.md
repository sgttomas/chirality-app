# Procedure: DEL-02-07 Emergency Power & Backup Generator

## Purpose

This procedure describes:
1. **Production process** — the steps required to develop and deliver the DEL-02-07 design basis artifacts during the proposal and early design phases.
2. **Operational context** — key steps for how the emergency power system will be operated, tested, and maintained post-occupancy (for O&M planning reference).

---

## Prerequisites

### Required Prior Inputs
| Input | Source | Status |
|---|---|---|
| Confirmed essential loads scope (minimum: kitchen, ICP room, 2 bathrooms) | Addendum 03 §1.15; SOW-0222 | Confirmed in source |
| Owner confirmation of 72-hour runtime requirement | SOW-0222 open issue; Functional Program Appendix B | OPEN ISSUE — not yet confirmed |
| Overhead door specification (size, operator type, number of doors) | DEL-02-04; OSR §10.3.9 | Size confirmed (16'×16'); operator/secondary method TBD |
| General electrical distribution concept | DEL-02-06 | TBD — must be developed concurrently |
| Site layout for generator pad location | DEL-03-01, DEL-03-04 | TBD |

### Required Reference Documents
| Document | Purpose |
|---|---|
| Addendum 03 (2024-07-31) — §1.15 | Generator and door secondary opening requirements |
| RFP OSR §10.3.9 | Door system requirements |
| RFP OSR §10.4 | Electrical system coordination requirements |
| Functional Program Appendix B | Generator area and runtime note |
| CSA C282 (Emergency Electrical Power Supply) | Generator system design standard — ASSUMPTION: applicable; text not yet accessed |
| CSA C22.1 (Canadian Electrical Code) | Electrical installation requirements |
| Alberta Building Code — applicable divisions | Code compliance for electrical and mechanical systems |
| Alberta Fire Code | Diesel fuel storage compliance |

### Required Personnel / Roles
| Role | Responsibility |
|---|---|
| Responsible Electrical Engineer (P.Eng., Alberta) | Essential loads calculation; generator sizing basis; ATS design; stamps/seals |
| Responsible Mechanical Engineer (P.Eng., Alberta) | Generator exhaust design; fuel storage mechanical design; coordination |
| Design-Builder Project Manager | Owner coordination; runtime confirmation; cross-deliverable coordination |

---

## Steps

### Phase A: Proposal Development (Pre-Award)

**Step A1 — Confirm 72-Hour Runtime with Owner**
- Status: OPEN ISSUE
- Action: Prior to finalizing proposal, submit a written question to Owner confirming whether 72-hour runtime is a firm requirement or whether a refuelling plan is an acceptable alternative.
- Record response as a design basis assumption in the essential loads and runtime artifact.
- Source: SOW-0222 open issue; _CONTEXT.md Open Issues.

**Step A2 — Select Bay Door Secondary Opening Mechanism Method**
- Review Addendum 03 §1.15: generator-powered door operators OR manual override.
- Coordinate with DEL-02-04 lead (door specification) to determine whether the preferred door operator has a manual override option or whether inclusion in the essential loads panel is required.
- Document the selected method and rationale in the bay door secondary opening mechanism integration artifact.
- Source: Addendum 03 §1.15; SOW-0216.

**Step A3 — Develop Initial Essential Loads List**
- Enumerate all loads to be served by the generator, starting from the Owner-required minimum (kitchen, ICP room, 2 bathrooms).
- Add code-required life-safety loads (fire alarm, emergency lighting, communications if code-required).
- Add bay door operators if generator-powered option selected (Step A2).
- Add any other operationally required loads justified by OBJ-002.
- For each load: record description, area served, connected load (kW), demand factor, and design load (kW).
- Source: Addendum 03 §1.15; OSR §10.4; ASSUMPTION (code compliance).

**Step A3a — Independent Review of Essential Loads List [X-004]**
- Before proceeding to generator sizing (Step A4), the essential loads list shall be reviewed by a second qualified party (e.g., peer electrical engineer, fire department operations representative, or Design-Builder QA reviewer).
- The review shall confirm: (a) all code-required loads are included, (b) all Owner-specified loads are included, (c) loads necessary for emergency operations (OBJ-002) have been evaluated, (d) demand values are reasonable.
- Record the review outcome (reviewer name, date, findings) before proceeding to Step A4.
- **ASSUMPTION:** This review step is not required by any accessed source but is recommended to reduce risk, as the essential loads list is the foundation of the entire deliverable.

**Step A4 — Calculate Generator Sizing Basis**
- Sum design loads from essential loads list (confirmed per Step A3a review).
- Apply appropriate demand factors per CSA C282 or NFPA 110 (ASSUMPTION: applicable standards).
- Apply spare capacity factor — **[A-002] Spare capacity factor status:** Currently assumed at 25%. This is an **ASSUMPTION only**; no accessible normative source confirms it. The responsible engineer shall confirm the appropriate spare capacity factor from CSA C282 or applicable standard before finalizing. Confirm this value and document the source in the generator sizing basis artifact.
- Select generator kW rating from standard manufacturer ratings that meets or exceeds the calculated demand.
- Document as the generator sizing basis artifact.
- Source: ASSUMPTION (standard engineering practice); CSA C282 (location TBD); NFPA 110 (applicability TBD).

**Step A5 — Determine Runtime and Fuel Tank Volume**
- Using confirmed runtime (72 hours pending Owner confirmation), calculate fuel consumption:
  - Fuel consumption (L/hr) at design load from manufacturer data sheet (TBD — pending generator selection).
  - Total volume = consumption rate × runtime + reserve margin (ASSUMPTION: 10% reserve).
- Check whether calculated tank volume triggers Alberta Fire Code secondary containment or environmental requirements.
- Document as the runtime/fuel assumptions artifact.
- Source: SOW-0222; Functional Program Appendix B (location TBD); ASSUMPTION for reserve margin.

**Step A6 — Develop ATS and Distribution Concept**
- Define ATS location (ASSUMPTION: adjacent to main electrical room or outdoor generator enclosure). **[X-002]:** ATS location shall be confirmed as physically coordinated with the electrical room layout in DEL-02-06; coordination shall go beyond a meeting record to include a documented site plan or one-line diagram showing spatial resolution.
- Define essential loads panel location and rating.
- Confirm whether the ATS serves a dedicated essential loads panel or a portion of an existing panel.
- Coordinate with DEL-02-06 electrical distribution concept to ensure one-line diagram consistency and ATS spatial placement.
- Document as the ATS/distribution design artifact (schematic or narrative).
- Source: OSR §10.4; ASSUMPTION (standard ATS practice); Specification REQ-09.

**Step A7 — Confirm Generator Outdoor Location**
- Coordinate with DEL-03-01 (site layout) and DEL-02-04 (building envelope) to identify generator pad location.
- Verify location meets:
  - Exhaust dispersion requirements (away from air intakes and apparatus bay doors)
  - Refuelling tanker access
  - Maintenance clearances
  - Freeze protection feasibility (enclosure or building-adjacency)
- Source: Functional Program Appendix B row 30.0 (location TBD); ASSUMPTION (standard siting practice).

**Step A8 — Compile and Submit Proposal Artifacts**
- Compile all five anticipated artifacts:
  1. Essential loads list
  2. Generator sizing basis
  3. ATS/distribution design
  4. Runtime/fuel assumptions
  5. Bay door secondary opening mechanism integration
- Submit as part of the DEL-02-07 proposal Design Brief narrative per RFP §4.

---

### Phase B: Detailed Design (Post-Award, for reference)

**Step B1 — Obtain Generator Manufacturer Data and Final Sizing**
- Issue a request for manufacturer information or sole-source confirmation once generator brand/model is selected.
- Finalize sizing based on actual derating curves for altitude and temperature at Penhold, Alberta. Site altitude and design ambient temperature data required (see Datasheet, Conditions — currently TBD [B-004]).
- **ASSUMPTION:** Altitude derating may apply depending on generator type; confirm with manufacturer.
- **Cold-start verification [F-003]:** Confirm with manufacturer that the selected generator can reliably start under worst-case Penhold winter conditions. Obtain the design ambient temperature for Penhold (currently TBD — expect -30C or colder) from site climate data (Datasheet Conditions [B-004]). Verify block heater and battery heater ratings are adequate for the design temperature. Document generator cold-start capability in the detailed design basis. Derating curves for altitude (Penhold altitude TBD [B-004]) and temperature shall be applied in final sizing calculations.

**Step B2 — Develop Permit-Ready Electrical Design Documents**
- Responsible electrical engineer develops stamped and sealed drawings:
  - One-line diagram showing ATS, essential panel, generator
  - Wiring diagrams for door operator circuits (if generator-powered)
  - Generator pad and enclosure detail
  - Fuel tank and secondary containment detail

**Step B3 — Develop Fuel System Design**
- Confirm tank type (sub-base, remote, belly tank).
- Design secondary containment per Alberta Fire Code.
- Coordinate fuel fill-point location for tanker access.

**Step B4 — Coordinate with Permitting**
- Obtain applicable permits for generator installation, fuel storage, and electrical work per DEL-01-04 permitting plan.

---

### Phase C: Construction and Commissioning (for reference)

**Step C1 — Inspection of Generator Installation**
- Verify generator, ATS, essential panel, and fuel system installed per approved drawings.
- Inspect clearances, exhaust routing, and fuel storage containment.

**Step C2 — Generator Load Bank Test**
- Conduct load bank test at 100% rated load for a minimum period per CSA C282 or NFPA 110 (duration TBD — standard text not accessed; **[A-004]** currently assumed at 2 hours at full load per standard practice, but this is an **ASSUMPTION only**). The responsible engineer shall confirm the minimum load bank test duration from CSA C282 or NFPA 110 before commissioning and document the source/reference in the commissioning test plan.
- Record results in commissioning record, including: load applied (kW), duration, voltage and frequency readings under load (compare to acceptance thresholds from Specification REQ-01 [D-002]), coolant temperature, oil pressure, and any anomalies observed.

**Step C3 — ATS Transfer Test**
- Simulate utility failure and confirm:
  - ATS transfers to generator within specified time — **[C-003, F-002] acceptance criterion: TBD seconds maximum** (ASSUMPTION: per CSA C282 requirements; standard text not accessed; responsible engineer to confirm acceptance threshold before commissioning)
  - Generator reaches rated voltage and frequency within TBD seconds from ATS signal [F-002] (acceptance threshold TBD per CSA C282 or manufacturer specs)
  - All essential loads energize correctly and simultaneously
  - Bay door operators function (if on essential loads panel) [REQ-03]
  - ATS retransfers to utility on restoration
- Record results in commissioning record, including measured transfer time, generator start time to rated output, voltage/frequency readings, and comparison to acceptance thresholds (once confirmed).

**Step C4 — Bay Door Secondary Opening Mechanism Functional Test**
- Simulate generator-only condition.
  - If generator-powered: confirm all bay doors open and close normally.
  - If manual override: confirm manual override procedure functions per manufacturer instructions; train staff.
- Record results in commissioning record.

**Step C5 — Owner Training**
- Provide training to designated Town of Penhold staff on:
  - Generator start/stop (manual and automatic)
  - ATS operation
  - Fuel level monitoring and refuelling procedure
  - Monthly and annual test procedures
  - Bay door manual override (if applicable)
- Source: RFP §7.3.6 Commissioning, Training, and Closeout Procedures.

---

### Phase D: Operational Use (Post-Occupancy, for O&M reference)

**Step D1 — Monthly Generator Exercise**
- Exercise generator under load for minimum duration per manufacturer and CSA C282 recommendations (ASSUMPTION: 30 minutes minimum monthly at load).
- Check fluid levels, battery condition, fuel level.
- Record test date and results in generator log.

**Step D2 — Annual Full-Load Test**
- Conduct annual load bank or building load test at or near rated capacity.
- Record results. Address any deficiencies.

**Step D3 — Fuel Level Monitoring and Refuelling**
- Monitor fuel level against confirmed runtime requirement (72 hours pending Owner confirmation).
- Establish refuelling trigger level (ASSUMPTION: refuel when tank drops below 50% capacity to maintain readiness).
- Maintain refuelling contract or standing arrangement with fuel supplier.
- If refuelling plan is approved as an alternative to full tank autonomy (Trade-off 3), ensure fuel supplier agreement documents guaranteed emergency response time and refuelling protocol during outage.

**Step D3a — Emergency Refuelling During Extended Outage [E-002]**
- During an extended utility power outage where the generator is running, fuel resupply logistics must be addressed. The following shall be established:
  - (a) Contact information for the fuel supplier with confirmed emergency response capability.
  - (b) Maximum acceptable fuel delivery response time, coordinated with the remaining fuel at the refuelling trigger level and the generator consumption rate.
  - (c) Contingency plan if road access is impaired (e.g., severe weather, flooding) during the outage.
  - (d) Safe refuelling procedure while the generator is running (or brief shutdown protocol if hot-refuelling is not permitted).
- **ASSUMPTION:** This step is not required by any accessed source but is operationally necessary for a 72-hour runtime facility. The Owner operations plan and fuel supplier agreement should address this scenario. See also Guidance, Trade-off 3 (Refuelling plan acceptability criteria).

**Step D4 — Preventive Maintenance**
- Follow manufacturer's preventive maintenance schedule (oil changes, filter replacements, coolant checks, load tests).
- Maintain maintenance log.

---

## Verification

| Step | Verification Check |
|---|---|
| A1 — Runtime confirmation | Written Owner response on file confirming runtime requirement |
| A2 — Bay door secondary opening mechanism method selection | Design decision recorded in artifacts with justification |
| A3 — Essential loads list | List includes all Owner-required loads; code-required loads present; demand values calculated |
| A3a — Essential loads list independent review | Review record on file with reviewer name, date, and confirmation of completeness [X-004] |
| A4 — Generator sizing basis | Calculation reviewed and signed by responsible electrical engineer |
| A5 — Fuel tank volume | Volume calculation present; Alberta Fire Code compliance noted |
| A6 — ATS/distribution concept | Coordination confirmed with DEL-02-06 electrical lead |
| A7 — Generator location | Site coordination record or plan confirms location; clearances noted |
| A8 — Proposal submission | All five anticipated artifacts present in proposal package |
| C2 — Load bank test | Commissioning report present; test results meet CSA C282 criteria; voltage and frequency regulation recorded [D-002] |
| C3 — ATS transfer test | Transfer test record present; all essential loads confirmed; transfer time measured against TBD acceptance criterion [C-003, F-002]; generator start time to rated output measured |
| C4 — Bay door secondary opening mechanism functional test | Door operation confirmed; training record present |

---

## Records

| Record | Owner | Retention |
|---|---|---|
| Essential loads list (stamped) | Design-Builder; submitted to Owner at closeout | Project file; O&M manual |
| Generator sizing basis (stamped) | Design-Builder; submitted to Owner at closeout | Project file; O&M manual |
| ATS/distribution design (stamped drawings) | Design-Builder; submitted to Owner at closeout | As-builts package |
| Runtime/fuel assumptions document | Design-Builder; submitted to Owner at closeout | Project file |
| Bay door secondary opening mechanism integration document | Design-Builder; submitted to Owner at closeout | Project file; O&M manual |
| Essential loads list independent review record | Design-Builder QA | Project file [X-004] |
| Owner runtime confirmation correspondence | Design-Builder PM | Project file |
| Commissioning reports (load bank, ATS, door tests) | Design-Builder (Cx lead) | Closeout package |
| Owner training completion records | Design-Builder | Closeout package |
| Ongoing generator maintenance log | Town of Penhold Operations | Facility O&M records |
