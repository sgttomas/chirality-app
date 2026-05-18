# Specification — DEL-015-01 Three-Phase Power Service

---

## Scope

### In Scope

This deliverable covers the supply and installation of the primary three-phase electrical service for the new West Dried Meat Lake Regional Landfill Maintenance Shop Addition, including:

1. Coordination with the utility company to establish the building service connection (SOW-0081).
2. Installation of the service entrance conductors, metering provisions (meter base per utility specifications; meter is utility-owned and utility-installed — see Datasheet Attributes [X-006]), and main disconnecting means.
3. Installation and energization of the main distribution panel (MDP) within the building.
4. Establishment of the building grounding and bonding system.
5. All labour, materials, equipment, and inspections required to bring the three-phase service to operational readiness at the MDP, such that all downstream PKG-015 deliverables can be energized.

### Out of Scope

- Electrical design and IFC drawing production (PKG-004 — Electrical Design package).
- Branch circuit wiring and fixtures downstream of MDP (DEL-015-02 through DEL-015-05).
- Crane procurement and installation (PKG-016), though crane power circuits are downstream of this service.
- Utility company infrastructure external to the building property line.
- Building structure and electrical room construction (PKG-011).
- Supply of aggregate, brushing/clearing, bulk cut and fill (Owner-supplied — RFP §3.3.1).
- **[E-003] Verification of downstream circuit operation beyond the MDP output terminals.** Verification that downstream circuits are energizable is the responsibility of the respective downstream deliverables (DEL-015-02 through DEL-015-05). This deliverable's verification boundary ends at the MDP output terminals. See Guidance Conflict Table CON-015-01-005.

---

## Requirements

### REQ-015-01-001 — Three-Phase Service
The building electrical service shall be three-phase AC.
*Source: RFP §3.4 ("The Proposed building shall run on three-phase power."); Decomposition SOW-0051.*

### REQ-015-01-002 — Service Voltage
Service voltage shall be as specified in the IFC electrical design drawings, stamped by a P.Eng. licensed in Alberta. **[A-001] The prescriptive hierarchy for voltage selection (utility constraints vs. Owner preference vs. engineer judgment) is TBD. See Guidance Conflict Table CON-015-01-001.**
*Source: RFP §3.3.2; PKG-004. Specific voltage level TBD pending design.*

### REQ-015-01-003 — Service Capacity
The service ampacity shall be sufficient to supply all connected loads shown on the IFC electrical drawings without exceeding rated capacity, including:
- High bay lighting (multiple circuits)
- General purpose receptacles (15A/120V, 20A/120V)
- 240V receptacles (20A, 30A, 50A)
- Air compressor (40A, as noted on App B-Elec)
- Fire hose pump (70A, as noted on App B-Elec)
- Pressure washer (70A, as noted on App B-Elec)
- Two (2) 5-tonne overhead crane power circuits (ampacity TBD in design)
- Overhead door operators
- Exhaust fans and ceiling fans

**[B-002] Note: The load values listed above are approximate, derived from the App B-Elec conceptual drawing. They are not sufficient for final sizing decisions. The IFC load schedule (PKG-004) will supersede these values. See Datasheet Known Downstream Load Summary for the same caveat.**

*Source: App B-Elec conceptual drawing (load schedule); RFP §3.4 (cranes, welding, doors). Final ampacity determined by PKG-004 electrical design.*

### REQ-015-01-004 — Code Compliance
All work shall comply with:
- Alberta Safety Codes — **[C-001] specifically the Safety Codes Act (RSA 2000, c. S-1) and its regulations, including the Electrical Code Regulation. The specific statutory instrument and edition that establishes compulsory compliance thresholds for this work is TBD — to be confirmed with Alberta Municipal Affairs (Safety Codes authority).** (as required by RFP §3.3.2)
- Canadian Electrical Code, CSA C22.1 — **[A-002] edition TBD; the specific edition adopted by Alberta at the time of permit application governs. ASSUMPTION: applicable as Alberta's adopted electrical safety code; edition confirmation required from Alberta Safety Codes authority or PKG-004 design package.**
- All applicable Alberta Building Code requirements
- **[C-002] Site-specific code provisions: The project is located at a landfill site (SW 14-44-21-W4). The PKG-004 design engineer shall evaluate whether site-specific code clauses apply, including but not limited to: ambient temperature derating, altitude derating for equipment ratings, and corrosive environment considerations. ASSUMPTION: site-specific provisions may apply; applicability TBD.**
*Source: RFP §3.3.2 ("adhere to all Alberta Safety Codes").*

### REQ-015-01-005 — IFC Drawings
All Issued for Construction (IFC) electrical drawings shall be signed and stamped by a professional engineer licensed to practice in the Province of Alberta.
*Source: RFP §3.3.2.*

### REQ-015-01-006 — Permits and Safety Code Inspections
The Proponent shall obtain all applicable electrical Safety Code permits. All inspection requests shall be submitted and the County project representative shall be provided copies of all completed inspection reports. The County representative must be present for all inspections.
*Source: RFP §3.3.2.*

### REQ-015-01-006A — Building / Development Permit [F-001]
**TBD — Confirm whether a separate building permit or development permit is required for the electrical service entrance installation and/or service trench excavation, or whether these are covered under a project-level building permit (potentially PKG-011) or the Electrical Safety Code permit alone. Camrose County planning department to confirm.**
*Source: ASSUMPTION — standard practice for construction work involving ground disturbance and service entrance installation may require a development permit in addition to the Safety Code permit; location TBD in municipal bylaws.*

### REQ-015-01-007 — Utility Tie-In Coordination
The Proponent shall coordinate and execute the electrical service tie-in with the applicable utility company. **[F-002] Note: SOW-0081 in the Decomposition is assigned to DEL-018-06 (Utility Tie-Ins). This deliverable addresses the electrical portion of the utility tie-in coordination under its SOW-0051 scope. See Guidance Conflict Table CON-015-01-004 for the scope boundary clarification.**
*Source: Decomposition SOW-0081; RFP §3.3.2 ("Coordinate natural gas, electrical tie-ins, and communication lines.").*

### REQ-015-01-008 — Grounding and Bonding
The service shall include a complete grounding and bonding system per applicable code requirements. **[A-003, X-004] Quantitative acceptance criteria: ground resistance shall not exceed the limits specified in CSA C22.1 (applicable section on grounding — section reference TBD). Testing shall be conducted using a fall-of-potential method or clamp-on ground resistance tester per CSA C22.1 requirements. Specific resistance threshold value: TBD per applicable code edition.**
*Source: ASSUMPTION (standard requirement under CSA C22.1 and Alberta Safety Code); RFP §3.3.2 (general code compliance requirement).*

### REQ-015-01-009 — Main Distribution Panel (MDP)
A main distribution panel shall be installed to distribute power to all branch circuits serving the building. The MDP shall be sized and equipped per the IFC electrical design.
*Source: _CONTEXT.md ("Main distribution panel setup"); App B-Elec (branch circuit distribution shown from central point).*

### REQ-015-01-010 — Welding Circuits
Multiple high-voltage electrical outlets suitable for welding equipment shall be provided throughout the shop area. County to supply welding equipment specifications to the electrical design team (PKG-004). **[E-002] Note: The scoping of welding circuits under DEL-015-01 (Power Service) rather than DEL-015-03 (Receptacle Installation) or DEL-015-04 (Equipment Power Circuits) is based on the RFP's placement of welding provisions alongside the three-phase power requirement in §3.4. See Guidance for the scoping rationale.**
*Source: RFP §3.4 ("Multiple electrical plugs throughout the shop area suitable for connecting high voltage welding equipment"); App B-Elec (50A 240V circuits at welding station).*

### REQ-015-01-011 — Completion Deadline
All electrical service installation work shall be complete, commissioned, and inspection-ready on or before December 31, 2026.
*Source: RFP §3.1 ("All Work...must be completed on or before December 31, 2026.").*

### REQ-015-01-012 — Guarantee Period
Materials and workmanship are guaranteed for two (2) years following the Construction Completion Certificate (CCC) date. Defects shall be rectified within ten (10) days of Owner's written instruction.
*Source: RFP §2.10.*

### REQ-015-01-013 — Electrical Contractor Qualifications [X-002]
**The electrical contractor performing this work shall hold a valid Alberta master electrician license and be certified under the Safety Codes Act to perform electrical work in the Province of Alberta. ASSUMPTION: Alberta requires licensed electrical contractors for Safety Code permit work; specific license class and registration requirements TBD per Alberta Safety Codes Act and Electrical Code Regulation.**
*Source: ASSUMPTION — standard Alberta regulatory requirement for electrical installation work; location TBD in Safety Codes Act and Electrical Code Regulation.*

### REQ-015-01-014 — Conformance Closure [D-002]
**Upon completion of all installation, inspection, and commissioning activities, the electrical contractor shall prepare a Conformance Closure Checklist attesting that all requirements (REQ-015-01-001 through REQ-015-01-013) have been satisfied. This checklist shall be submitted to the Proponent project manager and the County project representative prior to the issuance of the Construction Completion Certificate (CCC). Format: TBD.**
*Source: ASSUMPTION — standard practice for design-build projects; the CCC (RFP §2.14) is Owner-issued and requires contractor evidence of conformance.*

---

## Standards

| Standard | Description | Accessibility |
|---|---|---|
| Alberta Safety Codes | Governing safety code for construction in Alberta — **[C-001] specifically the Safety Codes Act (RSA 2000, c. S-1) and associated regulations** | Cited in RFP §3.3.2; specific regulation and edition TBD |
| CSA C22.1 — Canadian Electrical Code | Electrical installation standard adopted in Alberta — **[A-002] edition TBD; confirm with Alberta Safety Codes authority which edition is in force at time of permit** | ASSUMPTION: applicable; edition reference TBD |
| Alberta Building Code | Building code applicable to the province | Cited in RFP §3.3.2; edition TBD |
| CCDC 14–2013 | Design-Build Stipulated Price Contract form | RFP §2.7 |
| Alberta Prompt Payment and Construction Lien Act | Governs payment holdback | RFP §2.13.2 |

*Note: Specific code editions and clause references to be confirmed in the IFC electrical design package (PKG-004).*

---

## Verification

| Requirement | Verification Approach |
|---|---|
| REQ-015-01-001 (Three-phase) | Confirm service configuration with utility tie-in documentation and MDP nameplate |
| REQ-015-01-002 (Service voltage) | Verify against IFC drawings and utility connection documentation |
| REQ-015-01-003 (Service capacity) | Verify MDP rating against IFC load schedule; confirm no overloading at energization |
| REQ-015-01-004 (Code compliance) | Electrical Safety Code inspection — pass/approval from Alberta Safety Codes authority |
| REQ-015-01-005 (IFC drawings P.Eng. stamp) | Review IFC drawing set for Alberta P.Eng. stamp and signature |
| REQ-015-01-006 (Permits and inspections) | Confirm Safety Code permit obtained; confirm inspection reports provided to County |
| REQ-015-01-006A (Building / development permit) | **[F-001] Confirm with Camrose County planning department whether additional permit is required; if yes, confirm obtained** |
| REQ-015-01-007 (Utility tie-in) | Confirm utility connection agreement / service confirmation documentation |
| REQ-015-01-008 (Grounding) | **[A-003, X-004] Ground resistance testing using fall-of-potential method or clamp-on ground resistance tester per CSA C22.1. Pass condition: ground resistance within code-required limits (specific threshold TBD per applicable code edition). Inspection sign-off from Safety Codes officer.** |
| REQ-015-01-009 (MDP installed) | Physical inspection; MDP energized and functional; **[E-003] verification boundary is MDP output terminals — downstream circuit energizability is verified by respective downstream deliverables** |
| REQ-015-01-010 (Welding circuits) | Verify 50A 240V circuits at welding station per IFC drawings and App B-Elec layout |
| REQ-015-01-011 (Deadline) | Project schedule milestone; completion date confirmed by CCC or substantial completion |
| REQ-015-01-012 (Guarantee) | Contract documentation; deficiency log during 2-year guarantee period |
| REQ-015-01-013 (Contractor qualifications) | **[X-002] Verify contractor holds valid Alberta master electrician license and Safety Codes Act registration prior to commencement of work** |
| REQ-015-01-014 (Conformance closure) | **[D-002] Conformance Closure Checklist submitted, reviewed, and accepted by Proponent and County representative prior to CCC** |

---

## Documentation

The following artifacts are anticipated for this deliverable:

| Artifact | Description |
|---|---|
| IFC Electrical Drawings (electrical service sheets) | P.Eng.-stamped drawings showing service entrance, MDP, grounding — produced under PKG-004 |
| Electrical Safety Code Permit | Permit obtained from Alberta Safety Codes authority prior to installation |
| Utility Service Agreement / Connection Confirmation | Utility company documentation confirming service connection (SOW-0081) |
| Inspection Reports | Copies of all completed electrical inspection reports provided to County |
| As-Built / Record Drawings | **[X-001] TBD — to be confirmed: as-built drawings are standard practice for electrical service installations. Confirm contractual obligation under CCDC 14-2013 contract terms. Project manager to resolve. See Procedure Step 4.4.** |
| Commissioning Record | Confirmation that service is energized and MDP operational |
| Construction Completion Certificate (CCC) | Issued by Owner upon satisfactory final inspection (RFP §2.14) |
| **Conformance Closure Checklist [D-002]** | **Contractor attestation that all REQ items are satisfied — submitted prior to CCC** |

---

## Enrichment Provenance (Pass 3)

*The following warranted items from `_SEMANTIC_LENSING.md` were incorporated into this document during Pass 3 enrichment:*

| ItemID | Type | Section Modified | Action Taken |
|---|---|---|---|
| A-001 | TBD_Question | REQ-015-01-002 | Added authority chain gap notation; cross-reference to Conflict Table CON-015-01-001 |
| A-002 | WeakStatement | REQ-015-01-004, Standards table | Clarified edition TBD for CSA C22.1; added instruction to confirm edition with Safety Codes authority |
| A-003 | VerificationGap | REQ-015-01-008, Verification table | Added quantitative ground resistance testing method and acceptance criteria (TBD per code) |
| C-001 | WeakStatement | REQ-015-01-004, Standards table | Added specific statutory reference (Safety Codes Act RSA 2000 c. S-1); marked edition TBD |
| C-002 | MissingSlot | REQ-015-01-004 | Added site-specific code provisions for landfill-adjacent conditions |
| D-002 | MissingSlot | New REQ-015-01-014, Verification, Documentation | Added Conformance Closure Checklist requirement and verification row |
| E-002 | RationaleGap | REQ-015-01-010 | Added scoping rationale note; cross-reference to Guidance |
| E-003 | Conflict | Out of Scope, Verification (REQ-015-01-009) | Clarified verification boundary at MDP output terminals; added Conflict Table CON-015-01-005 reference |
| F-001 | MissingSlot | New REQ-015-01-006A, Verification | Added building/development permit requirement as TBD |
| F-002 | Normalization | REQ-015-01-007 | Normalized SOW-0081 scope description; added scope boundary note |
| X-001 | WeakStatement | Documentation (As-Built) | Strengthened as-built drawing requirement with contractual confirmation instruction |
| X-002 | MissingSlot | New REQ-015-01-013, Verification | Added electrical contractor qualifications requirement |
| X-004 | VerificationGap | REQ-015-01-008, Verification table | Added quantitative acceptance criteria and test method for grounding (merged with A-003) |
| X-006 | Normalization | In Scope item 2 | Normalized metering terminology; clarified utility-owned vs. contractor-installed scope |
