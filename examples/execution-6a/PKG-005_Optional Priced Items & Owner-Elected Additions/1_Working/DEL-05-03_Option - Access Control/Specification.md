# Specification — DEL-05-03: Option — Access Control

## Scope

### In Scope
This specification governs the optional priced access control package for the Town of Penhold Public Services Building (PSB) main building. It covers:

- A zoning concept defining access control zones within the main building
- A device schedule identifying hardware at each controlled point
- A separable pricing sheet for Owner election
- All associated low-voltage systems, door hardware integration, and system infrastructure required to implement the proposed zoning concept

**Source:** OSR S12.3; SOW-0502; Decomposition DEL-05-03 entry

### Excluded from Scope
- Ancillary buildings (cold storage building) — explicitly excluded from access control (OSR S12.3)
- Pickled sand storage — excluded from contract scope entirely (Addendum 03 S1.2; SOW-0400 OUT)
- Security camera system — separate optional item (DEL-05-04; SOW-0503)
- Intercom or video doorbell systems — TBD (no requirement stated in OSR)
- Monitoring service costs — TBD (OSR S12.4 notes monitoring costs for camera system separately; no equivalent stated for access control; treat as TBD)

## Requirements

### Requirement Confidence Classification

Requirements are classified as follows to distinguish confirmed from unconfirmed obligations:

| Classification | Meaning |
|---|---|
| **Confirmed** | Derived directly from accessible source documents with explicit statements |
| **ASSUMPTION** | Inferred from standard practice, related source text, or domain conventions; requires confirmation by Owner or AHJ before treating as a binding obligation |

> **Note:** Requirements tagged **ASSUMPTION** should not be treated as optional during implementation. They represent the DB's best-practice obligations pending formal confirmation. The distinction is about source traceability, not requirement priority.

### REQ-AC-001 — Zoning Concept [Confirmed]
The Design-Builder shall provide a zoning concept document identifying all controlled access zones within the main PSB building.

- Zones shall reflect shared-space use and interdepartmental access control between Fire Department and Public Works functions.
- The zoning concept shall identify which spaces require controlled entry, which are shared/open, and the access hierarchy between zones.
- The zoning concept shall, at minimum, account for all 8 Functional Program key-fob-access rooms and organize them into logically distinct zone groupings aligned with operational function.

**Source:** OSR S12.3 — "Designed to allow for shared space use and control of interdepartmental access."

### REQ-AC-002 — Zone Coverage — Main Building Only [Confirmed]
The access control system shall cover the main PSB building only. Ancillary buildings shall not be included in the access control system.

**Source:** OSR S12.3 — "Ancillary buildings not to be included in access control."

### REQ-AC-003 — Key Fob Access (Minimum Credential Type) [Confirmed]
The access control system shall, at minimum, support key fob credentials for controlled spaces. The Functional Program identifies the following spaces as requiring Key Fob Access:

- Mechanical/sprinkler room
- Electrical room
- Janitor room
- IT room
- Station office
- Map Work Office
- Bay Warehousing
- Map Work/Storage

Note: "Exterior Sand Shed" is listed in the Functional Program as Key Fob Access but is outside this contract's scope (SOW-0400 OUT). The DB shall confirm the room list against the final architectural program and flag any discrepancies.

**Source:** Functional Program (Appendix B), page 46 of RFP — Key Fob Access column; SOW-0400 OUT

**ASSUMPTION:** The Functional Program list represents the minimum set of rooms requiring access control. The DB may propose additional controlled points within the zoning concept.

### REQ-AC-004 — Device Schedule [Confirmed]
The Design-Builder shall provide a device schedule as part of this deliverable, identifying:

- Door/opening locations with controlled access hardware
- Hardware type at each location (e.g., card/fob reader, electromagnetic lock, electric strike, door position sensor)
- Controller assignments per zone
- Credential type(s) per location
- Fail-mode designation per door (fail-safe or fail-secure) — see Lock Hardware Terminology table below

**Lock Hardware Terminology (normative for all DEL-05-03 documents):**

| Term | Definition | Typical Application |
|---|---|---|
| **Electromagnetic lock** | Magnetically held lock requiring continuous power to remain locked | Doors requiring immediate release (egress, fire-separation) |
| **Electric strike** | Electrically released strike plate allowing latch retraction | Interior doors with mechanical lockset |
| **Fail-safe** | Lock unlocks (releases) on power failure | Required on all egress-path doors per building code |
| **Fail-secure** | Lock remains locked on power failure | Permitted on non-egress doors only (e.g., server room from secure corridor), with code confirmation |

> **Note on terminology (B-004):** This terminology table is normative across all four DEL-05-03 documents. Guidance.md and Procedure.md reference this table for consistent lock hardware terminology.

**Source:** _CONTEXT.md (Anticipated Artifacts: "Device schedule"); Functional Program (Appendix B)

### REQ-AC-005 — Separable Pricing Sheet [Confirmed]
The Design-Builder shall provide a pricing sheet presenting the access control option as a separable, clearly identified optional price, distinct from the base scope.

- Pricing may be presented as a lump sum for the complete system, or itemized by zone or by system component.
- The pricing sheet shall include all materials, installation labour, commissioning, and any required training.

**Source:** OSR S12 (optional items framework); _CONTEXT.md (Anticipated Artifacts: "Pricing sheet"); SOW-0502

### REQ-AC-006 — Integration with Base Building Systems [ASSUMPTION]
The access control system shall be coordinated with the base building electrical and IT systems (DEL-02-06) for:
- Low-voltage power supply to access control panels and door hardware
- Conduit and cable routing integrated with base building electrical rough-in
- Network/data connectivity for system management interface (if applicable)

Emergency power backup for access control panels is recommended given 24/7 Fire Department operations, but the specific power supply requirements are TBD and shall be confirmed during detailed design.

**Note (C-001):** This requirement is tagged ASSUMPTION because it is inferred from standard practice rather than stated explicitly in the OSR. However, integration with base building systems is functionally essential for system operation. The DB should treat this as a de facto requirement pending Owner confirmation.

**Source:** ASSUMPTION (inferred from 24/7 operations requirement; OSR S10.2; OSR S10.4)

### REQ-AC-007 — Code Compliance [ASSUMPTION]
The access control system and associated door hardware shall comply with applicable codes and standards, including but not limited to:

- Alberta Building Code / National Building Code of Canada (egress requirements — controlled doors must not impede emergency egress)
- Alberta Fire Code — access-controlled doors on fire-separation paths shall release electromagnetic locks on fire alarm activation and shall not impede fire department access (**ASSUMPTION:** standard fire code requirement for electromagnetic-lock-equipped fire-separation doors; specific Alberta Fire Code clause TBD)
- CSA and applicable electrical standards for low-voltage systems
- **ASSUMPTION:** UL 294 or equivalent standard for access control equipment
- **ASSUMPTION:** CSA B651 (Accessible Design for the Built Environment) — reader mounting height and barrier-free access at controlled doors; see Guidance.md Consideration on accessibility impact

**Acceptance criteria for code compliance verification:**
- All access-controlled egress doors demonstrated to fail-safe (unlock) on power loss
- Electromagnetic locks on fire-separation paths demonstrated to release on fire alarm activation
- AHJ inspection completed with no outstanding deficiencies related to access control hardware
- Reader mounting heights confirmed compliant with barrier-free access requirements (specific height TBD per CSA B651 or Alberta Building Code accessibility provisions)

**Source:** RFP S7.1.3 (accessibility/code compliance); ASSUMPTION for specific access control standards (location TBD)

### REQ-AC-008 — Commissioning and Training [ASSUMPTION]
The access control system, if Owner-elected, shall be commissioned as part of the building commissioning process (DEL-01-07), and training on system operation shall be provided to Town of Penhold staff.

**Source:** ASSUMPTION (consistent with OSR S7.3.6 commissioning requirements for building systems)

### REQ-AC-009 — Event Logging and Audit Trail [ASSUMPTION]
The access control system shall provide event logging and audit trail capability, recording at minimum:

- Access granted events (credential, door, timestamp)
- Access denied events (credential, door, timestamp, reason)
- Forced-entry / door-held-open alarm events (door, timestamp)
- System administrative events (programming changes, credential issuance/revocation)

Logs shall be retained for a minimum duration TBD (Owner to confirm retention period). The system management interface shall provide the ability to query and export event logs.

**Note (X-001):** Event logging is a standard capability of commercial access control systems and is operationally important for a shared municipal facility where multiple departments share controlled spaces. No source document explicitly requires audit trail capability, but it is standard practice for systems of this type.

**Source:** ASSUMPTION (standard practice for commercial access control systems)

### REQ-AC-010 — Cybersecurity Provisions [ASSUMPTION]
Network-connected access control panels and management interfaces shall incorporate basic cybersecurity provisions, including:

- Encrypted communications between readers, panels, and management interface (where supported by proposed equipment)
- Change of all manufacturer default credentials/passwords prior to commissioning
- Placement of access control system on a dedicated or segregated network segment (coordination with base building IT per REQ-AC-006)

**Note (E-002):** REQ-AC-006 identifies network/data connectivity for the system management interface. Network-connected access control systems introduce cybersecurity risk that should be acknowledged and mitigated through basic provisions. Specific cybersecurity standards (e.g., NIST, CSA) are TBD and depend on Owner IT security policy.

**Source:** ASSUMPTION (standard practice for network-connected building systems; specific standard TBD)

### REQ-AC-009 — Event Logging and Audit Trail [ASSUMPTION]
The access control system shall provide event logging and audit trail capability, recording at minimum:

- Access granted events (credential, door, timestamp)
- Access denied events (credential, door, timestamp, reason)
- Forced-entry / door-held-open alarm events (door, timestamp)
- System administrative events (programming changes, credential issuance/revocation)

Logs shall be retained for a minimum duration TBD (Owner to confirm retention period). The system management interface shall provide the ability to query and export event logs.

**Note (X-001):** Event logging is a standard capability of commercial access control systems and is operationally important for a shared municipal facility where multiple departments share controlled spaces. No source document explicitly requires audit trail capability, but it is standard practice for systems of this type.

**Source:** ASSUMPTION (standard practice for commercial access control systems)

### REQ-AC-010 — Cybersecurity Provisions [ASSUMPTION]
Network-connected access control panels and management interfaces shall incorporate basic cybersecurity provisions, including:

- Encrypted communications between readers, panels, and management interface (where supported by proposed equipment)
- Change of all manufacturer default credentials/passwords prior to commissioning
- Placement of access control system on a dedicated or segregated network segment (coordination with base building IT per REQ-AC-006)

**Note (E-002):** REQ-AC-006 identifies network/data connectivity for the system management interface. Network-connected access control systems introduce cybersecurity risk that should be acknowledged and mitigated through basic provisions. Specific cybersecurity standards (e.g., NIST, CSA) are TBD and depend on Owner IT security policy.

**Source:** ASSUMPTION (standard practice for network-connected building systems; specific standard TBD)

### TBD Items (for Owner/AHJ Ruling)

| TBD ID | Question | Relevant Requirements | Proposed Authority |
|---|---|---|---|
| TBD-F003 | Should the specification require the DB to demonstrate access control system design competence (e.g., prior project experience, qualified sub-trade, or manufacturer certification)? Access control is a specialty sub-trade typically requiring manufacturer-certified installers. | All requirements (DB qualification) | Owner |
| TBD-X003 | Should the specification include a system availability/uptime requirement (e.g., 99.9% availability) given 24/7 Fire Department operations? | REQ-AC-006 (24/7 operations context); REQ-AC-009 (event logging retention); REQ-AC-010 (cybersecurity) | Owner |
| TBD-A002 | Do Alberta-specific access control licensing or installer certification requirements apply (e.g., Alberta Security Services and Investigators Act)? | REQ-AC-007 (Code Compliance) | Owner / AHJ |
| TBD-F004 | What is the minimum acceptable warranty period for access control system components (manufacturer warranty vs. DB-provided extended warranty)? | REQ-AC-008, REQ-AC-009 (post-handover support) | Owner |
| TBD-X001 | What is the required event log retention period? | REQ-AC-009 (Event Logging) | Owner |

## Standards

| Standard | Applicability | Accessibility | Confidence |
|---|---|---|---|
| Alberta Building Code / National Building Code of Canada | Egress requirements for controlled doors; door hardware code compliance | **ASSUMPTION:** likely applicable; location TBD | **ASSUMPTION** |
| Alberta Fire Code | Fire-separation door release requirements for electromagnetic locks; fire alarm integration | **ASSUMPTION:** likely applicable; location TBD | **ASSUMPTION** |
| CSA C22.1 (Canadian Electrical Code) | Low-voltage wiring and power supply for access control | **ASSUMPTION:** likely applicable; location TBD | **ASSUMPTION** |
| UL 294 — Access Control System Units | Equipment certification standard | **ASSUMPTION:** likely applicable; location TBD | **ASSUMPTION** |
| ANSI/BHMA A156.25 | Electrified locks and strikes | **ASSUMPTION:** likely applicable; location TBD | **ASSUMPTION** |
| CSA B651 — Accessible Design for the Built Environment | Reader mounting height and barrier-free access at controlled doors | **ASSUMPTION:** likely applicable; location TBD | **ASSUMPTION** |
| RFP 2024_004 — Design-Build requirements | General contract and proposal compliance | Accessible | Confirmed |
| OSR (Appendix A) S12.3 | Owner's access control requirement statement | Accessible (page 44 of RFP PDF) | Confirmed |

> **Note (A-001):** All access-control-specific standards (UL 294, ANSI/BHMA A156.25, CSA C22.1, CSA B651, Alberta Fire Code) are tagged as ASSUMPTION because the relevant standard text has not been directly accessed. The DB should confirm applicability of each standard during detailed design and update this table accordingly. See also the Requirement Confidence Classification table at the top of the Requirements section.

## Verification

| Requirement | Verification Approach | Acceptance Criteria |
|---|---|---|
| REQ-AC-001 — Zoning Concept | Review: Zoning concept document submitted with proposal; reviewed by Owner for adequacy and alignment with interdepartmental access intent (item F-001: define minimum acceptance criteria) | Zoning concept accounts for all 8 Functional Program key-fob rooms; zones organized into logically distinct groupings (minimum 2 distinct zone types recommended); access hierarchy documented; DB proposal meets proposed acceptance criteria |
| REQ-AC-002 — Main Building Only | Review: Confirm zoning concept and device schedule contain no ancillary building elements | No ancillary building locations appear in zoning concept or device schedule |
| REQ-AC-003 — Key Fob Access | Review + Inspection: Device schedule to confirm fob readers at all required locations; field inspection at commissioning | All 8 listed rooms have fob reader entries in device schedule; field inspection confirms operational readers at each location |
| REQ-AC-004 — Device Schedule | Review: Device schedule submitted with proposal; completeness check against zoning concept | Every controlled opening has: location, hardware type, fail-mode, controller assignment, credential type |
| REQ-AC-005 — Pricing Sheet | Review: Pricing sheet reviewed for separability and completeness of inclusions | Price clearly separable from base; all materials, labour, commissioning, training itemized or covered |
| REQ-AC-006 — Integration | Review: Coordination confirmed with electrical/IT package (DEL-02-06) prior to IFC; field inspection at rough-in and commissioning | Coordination letter/memo from DEL-02-06 lead confirming integration scope; field verification of power feeds and network connectivity |
| REQ-AC-007 — Code Compliance | Review + AHJ Inspection: Confirm door hardware and egress provisions comply with Alberta Building Code and Alberta Fire Code (item A-003: define specific acceptance criteria; item C-002: add fire code provisions) | All egress doors fail-safe demonstrated per acceptance criteria; electromagnetic locks on fire-separation paths release on fire alarm per Alberta Fire Code fire door release requirements; AHJ inspection completed with no outstanding access-control-related deficiencies; reader mounting heights confirmed barrier-free compliant per CSA B651 or Alberta Building Code accessibility provisions (specific height TBD) |
| REQ-AC-008 — Commissioning and Training | Commissioning report and training record submitted at closeout (if Owner elects this option) | Commissioning report issued documenting all controlled points tested; training attendance records signed |
| REQ-AC-009 — Event Logging | Review + Functional Test: Confirm system logs access events during commissioning testing (item X-001: audit trail required) | Event log query demonstrates recording of granted, denied, and alarm events with timestamps; event retention period confirmed with Owner |
| REQ-AC-010 — Cybersecurity | Review: Confirm default credentials changed; confirm network segmentation with IT lead (item E-002: acknowledge cybersecurity risk) | DB submits cybersecurity checklist confirming provisions (encrypted communications, default credential changes, network segmentation); IT lead confirms network segmentation on dedicated/segregated segment |
| Product Certification (F-002) | Review: Confirm proposed access control equipment holds applicable product certifications (UL 294, CSA, ANSI/BHMA A156.25 as applicable) (item F-002: add verification approach) | Equipment submittal includes current certification documentation for all major components (UL 294, ANSI/BHMA A156.25, CSA C22.1 as applicable); certifications verified as current prior to procurement |
| Warranty (F-004) | Review: Confirm warranty documentation specifies minimum warranty period for access control system components (item F-004: add warranty requirement) | Warranty period stated in submittal; minimum warranty period TBD — Owner to confirm whether minimum duration applies beyond manufacturer standard warranty |

## Documentation

### Proposal-Stage Deliverables (Anticipated Artifacts)
Per _CONTEXT.md, the following artifacts are anticipated with this deliverable:

1. **Zoning concept** — diagram or narrative identifying access control zones within the main building
2. **Device schedule** — table of controlled openings, hardware types, controller assignments, credential types, and fail-mode designations
3. **Pricing sheet** — separable optional price for the complete access control system

### Post-Award Deliverables (if Owner elects this option)
**ASSUMPTION:** If the access control option is selected by Owner, the following additional documentation is required consistent with general project closeout requirements:

- Detailed shop drawings / system submittals for access control equipment (including product certification documentation per F-002 and REQ-AC-009)
- As-built drawings showing final device locations and wiring
- System programming records (user groups, access levels, schedules)
- Event logging and audit trail configuration documentation (REQ-AC-009: retention period, query procedures, export capability)
- Cybersecurity checklist confirming REQ-AC-010 provisions (encrypted communications, default credential changes, network segmentation)
- O&M manual for access control system (including event logging procedures, cybersecurity maintenance, and post-handover maintenance schedule per Guidance.md Consideration X-004)
- Training records for Town of Penhold staff (administrator training and general user training per Procedure Step B5)
- Warranty documentation specifying warranty period for all access control system components (minimum warranty period TBD — Owner to confirm per TBD-F004)

**Source:** ASSUMPTION (consistent with OSR S7.3.6; DEL-01-07 commissioning/closeout requirements; REQ-AC-009, REQ-AC-010)
