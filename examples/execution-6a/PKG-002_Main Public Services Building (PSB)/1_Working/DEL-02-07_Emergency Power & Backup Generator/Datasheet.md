# Datasheet: DEL-02-07 Emergency Power & Backup Generator

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-02-07 |
| Name | Emergency Power & Backup Generator |
| Package | PKG-002 Main Public Services Building (PSB) |
| Discipline | Electrical / Mechanical |
| Type | Building design package (4-doc bundle) |
| Responsible Party | Design-Builder (Electrical/Mechanical) |
| Covers Scope Items | SOW-0222; SOW-0216 (backup mechanism aspects) |
| Supports Objectives | OBJ-002, OBJ-008 |
| Decomposition Reference | Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md, PKG-002 table |

---

## Attributes

### Generator Unit

| Attribute | Value | Source |
|---|---|---|
| Generator type | Diesel standby generator | SOW-0222 (Addendum 03 §1.15; Functional Program Appendix B) |
| Installation location | Outdoor area | Functional Program Appendix B, row 30.0 |
| Required runtime | 72 hours (per Functional Program notes) | SOW-0222 open issue note; Functional Program Appendix B (location TBD — exact row text partially obscured) |
| Runtime confirmation status | OPEN ISSUE — 72-hour runtime not yet confirmed by Owner | _CONTEXT.md Open Issues; _REFERENCES.md Notes |
| Sizing basis | To be determined based on essential loads list; spare capacity factor TBD (currently assumed 25% per ASSUMPTION; no normative source confirms this value) | ASSUMPTION (sizing to be completed by Design-Builder electrical engineer) [A-002] |
| Generator output (kW) | TBD (pending essential loads calculation) — **resolution depends on completion of essential loads list (Step A3) and sizing calculation (Step A4)** | — [B-001] |
| Fuel consumption rate (L/hr at design load) | TBD (pending generator model selection — required for fuel tank sizing per Step A5) | — [B-002] |
| Fuel tank capacity | TBD (to support confirmed runtime) | — |
| Generator voltage/frequency regulation performance | Voltage: ±TBD %; Frequency: ±TBD Hz under load — acceptance thresholds TBD per CSA C282 or manufacturer specifications | ASSUMPTION: performance parameters to be confirmed from CSA C282 and generator manufacturer specs [D-002] |
| Generator start time (cold/warm) | Cold-start: TBD seconds; Warm-start: TBD seconds from ATS signal to rated voltage/frequency. Acceptance threshold TBD per CSA C282. | ASSUMPTION: standard acceptance parameter for standby generators; confirm from CSA C282 [F-002] |

### Essential Loads (Minimum Required)

| Load | Area Served | Demand (kW) | Notes | Source |
|---|---|---|---|---|
| Kitchen | Main building kitchen/breakroom | TBD | Per minimum requirement; demand pending detailed electrical analysis | Addendum 03 §1.15; SOW-0222 |
| Meeting room / Incident Command Post (ICP) | Shared meeting room (doubles as ICP) | TBD | Per minimum requirement; demand pending detailed electrical analysis | Addendum 03 §1.15; SOW-0222 |
| Two bathrooms | To be identified on essential loads list | TBD | Per minimum requirement; demand pending detailed electrical analysis | Addendum 03 §1.15; SOW-0222 |
| Bay door secondary opening mechanism | Fire apparatus bays and PW bays (motorized overhead doors) | TBD | Count of doors TBD — coordinate with DEL-02-04 door schedule [X-001]; demand pending door operator selection [B-003] | Addendum 03 §1.15; SOW-0216; OSR §10.3.9 |
| Emergency/exit lighting | Building-wide per code (battery backup on exit lights) | TBD | Note: battery-backed exit lights are separate from generator (OSR §10.5); generator portion TBD | OSR §10.5 |
| Fire alarm panel | TBD — demand (kW) to be determined | TBD | Code-required life-safety load per ABC/NBCC; inclusion mandatory [B-003] | ASSUMPTION: code-required per ABC/NBCC |
| Communications systems | TBD — demand (kW) to be determined | TBD | Evaluate per code-required communications and OBJ-002 emergency operations capability [B-003] | ASSUMPTION: required for emergency operations per OBJ-002 |
| SCBA room | TBD — demand (kW) to be determined | TBD | Typical essential load for fire hall operations; evaluate per operational needs [B-003] | ASSUMPTION: typical for fire hall operations |
| PA system | TBD — demand (kW) to be determined | TBD | Typical essential load for emergency operations facility; evaluate per operational needs [B-003] | ASSUMPTION: typical for emergency operations |
| Additional essential loads (other) | TBD — to be determined during design | TBD | Design-Builder to evaluate and enumerate all additional loads required by code or operational necessity [B-003] | ASSUMPTION: per code and operational needs |

### Automatic Transfer Switch (ATS) / Distribution

| Attribute | Value | Source |
|---|---|---|
| ATS requirement | Required (auto-transfer from utility to generator on utility failure) | ASSUMPTION: standard practice for diesel standby generator installations |
| ATS location | TBD — to be coordinated with electrical distribution design | — |
| Essential loads panel/sub-panel | TBD — separate panel or sub-panel for essential loads | ASSUMPTION: standard practice |
| Distribution design | To be developed in DEL-02-06 coordination | ASSUMPTION |

### Bay Door Secondary Opening Mechanism

| Attribute | Value | Source |
|---|---|---|
| Doors requiring secondary opening mechanism | Motorized overhead doors in fire apparatus bays and PW bays — **exact door count TBD; coordinate with DEL-02-04 door schedule [X-001]** | SOW-0216; Addendum 03 §1.15; OSR §10.3.9 |
| Door size | 16 ft × 16 ft (motorized, with windows) | OSR §10.3.9; Addendum 03 §1.10 |
| Bay door secondary opening mechanism type | Generator backup power OR manual override (either acceptable) — Design-Builder to select method per Specification REQ-03 and document in proposal (Step A2) | Addendum 03 §1.15; Specification REQ-03 |
| Terminology — normalization | Note: terminology varies across documents ("Door Secondary Opening Mechanism", "Door Secondary Opening Power Integration", "Door Secondary Opening Method"). For consistency, use "Secondary Opening Mechanism" per Specification REQ-03 as canonical term [B-005]. | Datasheet enrichment [B-005] |
| Coordination required | DEL-02-04 (door specification and operator count); DEL-02-06 (electrical distribution and essential loads panel if generator-powered option selected) | ASSUMPTION: interface coordination per OSR §10.4 |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Facility type | Combined Fire Hall and Public Works facility (24/7 operational) | RFP §2.2; OSR §10.2 |
| Building design life | 50 years (main building) | RFP §2.2 |
| Operational context | Emergency operations capability required at all times | Addendum 03 §1.15; OBJ-002 |
| Climate | Penhold, Alberta (design for Alberta snow/wind/cold loads) | OSR §10.3.5 |
| Site altitude | TBD — required for generator derating calculation (Procedure Step B1); Penhold, Alberta altitude to be confirmed [B-004] | Datasheet enrichment [B-004] |
| Design ambient temperature (winter low) | TBD — required for cold-start reliability and generator derating; Penhold winter design temperature (expect -30C or colder per Guidance) to be confirmed [B-004] [F-003] | Guidance Cold-start reliability consideration; Datasheet enrichment [B-004] |
| Applicable codes | Alberta Building Code (ABC); National Building Code of Canada (NBCC); CSA standards | RFP §1 Definitions; OSR §10.3.2 |
| Post-disaster importance | AHJ intends to exempt post-disaster designation (not sole emergency facility in Penhold) | OSR §10.3.5 |
| Seismic anchorage requirement | TBD — to be confirmed with AHJ based on post-disaster importance category exemption status (OSR §10.3.5) [F-001] | OSR §10.3.5 (post-disaster exemption); Specification REQ-05 |
| Fuel type | Diesel | SOW-0222; Functional Program Appendix B (location TBD — exact wording partially obscured) |
| Generator lifecycle | 50-year building design life assumes generator replacement cycle of approximately 20-30 years; warranty and service life to be confirmed [F-004] | F-004 enrichment (lifecycle consideration) |

---

## Construction

### Anticipated Artifacts (from _CONTEXT.md)

| Artifact | Description |
|---|---|
| Essential loads list | Enumerated list of all loads to be served by generator, with demand values |
| Generator sizing basis | Calculation/narrative demonstrating generator kW selection |
| ATS/distribution design | Schematic or narrative describing automatic transfer switch and distribution arrangement |
| Runtime/fuel assumptions | Documented runtime target (72-hr per Functional Program, pending confirmation) and fuel tank sizing basis |
| Bay door secondary opening mechanism integration | Design narrative or schematic showing how overhead doors are powered during generator operation or provided with manual override |

### Key Interfaces

| Interface | Deliverable | Nature |
|---|---|---|
| Overhead door system | DEL-02-04 Envelope, Structure, Roof & Doors | Door operator compatibility with generator/backup power |
| Electrical distribution | DEL-02-06 Electrical Power, Lighting, IT/Telecom & PA | Essential loads panel integration; ATS placement |
| Mechanical | DEL-02-05 Mechanical, Plumbing, Ventilation & Exhaust | Generator exhaust routing; outdoor generator placement coordination |
| Site/civil | DEL-03-04 Site Utilities Distribution | Site electrical service; generator pad location |

---

## References

| Reference | Relevance | Accessibility |
|---|---|---|
| Addendum 03 §1.15 (July 31, 2024) | Generator requirement; essential loads; door secondary opening | Accessible — reviewed |
| SOW-0222 (Decomposition, PKG-002 table) | Generator diesel; runtime (72 hr); essential loads | Accessible — reviewed |
| SOW-0216 (Decomposition, PKG-002 table) | Overhead doors; secondary opening mechanism | Accessible — reviewed |
| OSR §10.3.9 (RFP Appendix A) | Door system — 16'×16', motorized, car-wash grade hardware | Accessible — reviewed (pp. 41–42) |
| OSR §10.4 (RFP Appendix A) | Electrical systems; coordination with door openers | Accessible — reviewed (p. 42) |
| Functional Program Appendix B (RFP p. 46) | Generator outdoor area; building essentials standby; 72-hr runtime note | Accessible — reviewed (row 30.0, text partially obscured) |
| Alberta Building Code (ABC) | Governing code for electrical and mechanical systems | Not directly accessible — location TBD |
| CSA C22.1 Canadian Electrical Code | Governing standard for electrical installation | Not directly accessible — location TBD |
| CSA C282 Emergency Electrical Power Supply | Standard for emergency generator systems | Not directly accessible — **ASSUMPTION: likely applicable [A-003].** Applicability not confirmed; Design-Builder electrical engineer to confirm with AHJ whether CSA C282 applies to this installation. |
| Alberta Fire Code | Governs diesel fuel storage on site | Not directly accessible — location TBD [D-001] |
| Environmental/Emission Standards | Potential diesel exhaust emission and environmental protection standards for outdoor diesel generators in Alberta | Not directly accessible — location TBD [E-001] |
