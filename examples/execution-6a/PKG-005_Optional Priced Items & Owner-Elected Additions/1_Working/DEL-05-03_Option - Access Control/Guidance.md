# Guidance — DEL-05-03: Option — Access Control

## Purpose

This deliverable exists to provide the Town of Penhold with a transparent, separately priced option for an access control system within the main Public Services Building (PSB). The PSB combines Fire Department and Public Works functions in a single facility, creating a shared-use environment where interdepartmental access management is operationally important — but not a base contract requirement.

By pricing this option separately, the Owner can make an informed decision about whether to include access control at the time of award or defer it to a future procurement. The deliverable must therefore provide enough design resolution at the proposal stage to support a credible Owner decision: a zoning concept, a device schedule, and a clearly separable price.

**Source:** OSR S12.3; OBJ-010; Decomposition DEL-05-03 entry

## Principles

### 1. Access control must serve the shared-use reality of the PSB
The PSB is a combined facility. Fire and Public Works staff share spaces such as the kitchen/breakroom, meeting/training room, and reception. Other areas — such as the electrical room, IT room, mechanical room, and departmental offices — require controlled access to prevent unauthorized entry and protect critical systems.

The zoning concept must reflect this dual reality: open and shared areas should remain accessible, while sensitive or restricted areas require controlled entry. The goal is operational efficiency, not security theatre.

**Source:** OSR S12.3 — "Designed to allow for shared space use and control of interdepartmental access."

### 2. The Functional Program provides the minimum zone list
The Functional Program (Appendix B) identifies specific rooms with "Key Fob Access" as a requirement. These represent the Owner's baseline expectation of which spaces should be access-controlled. The DB should treat this list as the minimum and may propose additional controlled points if operationally justified.

The DB should review the final architectural program and confirm the room list is complete before finalizing the device schedule.

**Source:** Functional Program (Appendix B), page 46 of RFP

### 3. Ancillary buildings are explicitly excluded
OSR S12.3 is unambiguous: ancillary buildings are not to be included in the access control system. The cold storage building is outside the access control scope. The DB should not price or design access control for any ancillary structure.

**Source:** OSR S12.3

### 4. Pricing must be separable
This is an optional priced item. The pricing sheet must present the access control system as a standalone, clearly separable addition to the base price. The Owner must be able to elect or decline this option without affecting the base contract.

**Source:** OSR S12; SOW-0502; OBJ-010

### 5. Emergency reliability is an operational consideration
The Fire Department operates 24/7. Any access control system must be designed to remain functional during power outages. At minimum, the DB should address battery backup for access control panels and confirm that all controlled egress doors fail-safe (unlock) on power failure, consistent with life safety code requirements.

This is an **ASSUMPTION** based on the 24/7 operations context. The exact power supply configuration is TBD and should be confirmed during detailed design if the option is elected.

**Source:** ASSUMPTION (inferred from OSR S10.2; life safety code requirements — location TBD)

## Considerations

### Zone Definition Approach
The DB should consider organizing zones around operational function rather than department alone:
- **Public/shared zones:** Reception, lobby, breakroom, shared washrooms, training/meeting room
- **Restricted/utility zones:** Electrical room, mechanical room, IT room, janitor room (access by trades and Town facilities staff)
- **Fire Department operational zones:** Station office, SCBA/cascade room, decontamination area, gear lockers
- **Public Works operational zones:** Shop offices, Bay Warehousing, Map Work Office, Map Work/Storage

This functional zoning approach aligns with the OSR intent of managing "interdepartmental access" and "shared space use."

**Source:** ASSUMPTION (inferred from OSR S12.3; Functional Program room types, page 46 of RFP)

### Credential Type
The Functional Program references "Key Fob Access" as the credential type for controlled rooms. Key fobs (RFID proximity cards/fobs) are a common, cost-effective, and operationally simple choice for a municipal facility with staff who are not IT specialists.

The DB may propose a single-credential-type system (fob only) for simplicity, or may propose multi-factor access for the most sensitive areas (e.g., IT room, electrical room) as an option within the option. The proposal should clearly describe what credential type(s) are included in the price.

**Source:** Functional Program (Appendix B), page 46 of RFP

### User Population and Visitor Credentials (TBD-B003)
**TBD:** No source document states the expected total number of credentialed users (Fire Department and Public Works staff headcount combined), nor whether the system needs to support visitor or temporary credential capability. These are essential inputs for system sizing and credential management complexity.

The DB should confirm the following with the Owner:
- Total expected number of unique credential holders
- Whether visitor/temporary credential issuance is required (e.g., for contractors, inspection officials, shared-use event visitors)
- Whether credential revocation/reissuance frequency has been estimated

**Source:** TBD — no source available; **ASSUMPTION:** user population sizing is relevant for system specification

### Integration with Building Electrical and IT (DEL-02-06)
Access control low-voltage cabling, conduit, and panel power supply should be coordinated with the base building electrical design. If the access control option is likely to be elected, the DB should rough-in conduit during base building construction to avoid costly future retrofitting.

The DB may wish to note in the pricing sheet whether conduit rough-in is included in the base scope or in the access control option price, to avoid ambiguity.

**Source:** ASSUMPTION (coordination requirement inferred from OSR S10.4; standard practice)

### Consequence of Non-Election: Rough-In Provisions (B-005)
**ASSUMPTION:** If the Owner does not elect this option at award, it is unclear whether conduit rough-in provisions should still be included in the base building scope to preserve future retrofit feasibility. The cost difference between including conduit rough-in at construction time versus retrofitting conduit into finished walls after occupancy is typically significant.

The DB should consider:
- Stating explicitly in the pricing sheet whether base-scope conduit rough-in is included for future access control (even if the option is not elected)
- If not included in base scope, noting the approximate cost premium for future retrofit versus election at award
- This is a consequential design decision that should be highlighted for the Owner in the pricing narrative

**Source:** ASSUMPTION (standard practice; no source document addresses non-election rough-in provisions)

### Relationship to Security/Camera System (DEL-05-04)
Access control (DEL-05-03) and the security/camera system (DEL-05-04) are two separate optional items in PKG-005. They may be complementary — for example, a camera at an access-controlled door provides both control and recording. However, they are priced separately and the Owner may elect one without the other.

The DB should design the access control system to be self-contained (not dependent on the camera system being selected), while noting any integration opportunities in the pricing narrative.

**Source:** Decomposition PKG-005; OSR S12.3 and S12.4

### Lifecycle Cost and Total Cost of Ownership (A-005)
**ASSUMPTION:** Guidance on the Owner's election decision should consider not only upfront capital cost but also ongoing operational costs, including:

- **Credential management:** Cost of replacement fobs, issuance for new staff, revocation for departing staff
- **Software licensing:** If the management interface requires ongoing software licence renewals
- **Maintenance:** Annual preventive maintenance for readers, locks, panels; battery replacement schedule for panel backup batteries
- **System updates:** Firmware and software updates to address security vulnerabilities and maintain functionality
- **Staff administration time:** Ongoing administrative effort for managing user groups, access levels, and event log review

The DB should provide the Owner with an estimate or framework for understanding these recurring costs as part of the pricing narrative, so the election decision is informed by total cost of ownership rather than capital cost alone.

**Source:** ASSUMPTION (standard practice for Owner-elected building system options; no source document addresses lifecycle cost framing)

### Accessibility Impact (C-003)
**ASSUMPTION:** The introduction of access control hardware (readers, electromagnetic locks, door position sensors) may affect barrier-free access for persons with disabilities. The DB should consider:

- **Reader mounting height:** Key fob readers should be mounted at a height accessible to persons using wheelchairs (CSA B651 or Alberta Building Code accessibility provisions — specific height TBD)
- **Automatic door operators:** If controlled doors currently have or require automatic door operators for barrier-free access, the access control system must integrate with these operators without degrading accessible function
- **Electromagnetic lock delay:** Where electromagnetic locks are used on doors with automatic operators, the unlock-to-open sequence must not create a barrier for persons with mobility impairments

This is a separate code requirement (accessibility) that intersects with the access control hardware scope. The DB should confirm that access control implementation does not introduce new accessibility barriers.

**Source:** ASSUMPTION (CSA B651 and Alberta Building Code accessibility provisions — location TBD; RFP S7.1.3 references accessibility compliance)

### Post-Handover Maintenance and Periodic Review (X-004)
**ASSUMPTION:** The four documents and Procedure address commissioning and closeout but not ongoing post-occupancy expectations. The Owner should plan for:

- **Annual credential audit:** Review active credentials against current staff roster; revoke departed staff credentials
- **Firmware and software updates:** Apply manufacturer security patches and feature updates on a regular schedule (frequency TBD per manufacturer recommendation)
- **Battery replacement schedule:** Panel backup batteries typically require replacement every 3-5 years (manufacturer-specific; DB to confirm during detailed design)
- **Preventive maintenance:** Annual inspection of readers, locks, door position sensors, and controller hardware
- **Event log review:** Periodic review of access event logs for security anomalies and unusual access patterns (frequency to be determined by Owner security policy; see REQ-AC-009)
- **System availability monitoring:** If REQ-AC-009 uptime requirement is adopted (TBD-X003), establish a regular system health check schedule to detect and address panel or reader failures before they impact access

The DB should include a recommended maintenance schedule in the O&M manual (see Procedure.md Step B6). The schedule should address all elements above and include battery replacement intervals, firmware update frequency, and event log archival/retention procedures.

**Source:** ASSUMPTION (standard practice for commercial access control system O&M; enhanced per REQ-AC-009 event logging and TBD-X003 uptime considerations)

## Trade-offs

### Tension: Granular zoning vs. cost and complexity
More zones provide finer control but increase cost (more readers, more hardware, more programming) and ongoing administrative burden (managing credential assignments for multiple zones). Fewer zones reduce cost but may not adequately separate interdepartmental access.

**Resolution:** The DB should propose a balanced zoning concept that covers all Functional Program key-fob rooms as a minimum, grouped into logical zones that reflect operational boundaries rather than over-engineering the system. The Owner can refine zone granularity during detailed design.

**Source:** ASSUMPTION (design judgment based on OSR S12.3 intent and Functional Program)

### Tension: Key fob simplicity vs. higher-security credentials
Key fobs are simple and familiar but offer limited audit trail capability and can be lost/shared. Higher-security options (smart card, PIN+card, biometric) offer stronger access control but at higher cost and with greater staff training requirements.

**Resolution:** For a municipal operations facility with non-specialist staff, key fob credentials are the appropriate base technology. The DB should price the system on key fobs and may note upgraded credential options as an addendum if desired.

**Source:** ASSUMPTION (informed by Functional Program key fob references and municipal operations context)

### Tension: Fail-safe vs. fail-secure door hardware
Fail-safe locks (unlock on power failure) are required for egress compliance but allow entry during outages. Fail-secure locks (lock on power failure) prevent unauthorized entry during outages but can trap occupants if egress provisions are not addressed. Most building codes require fail-safe on egress doors. See Specification.md REQ-AC-004 Lock Hardware Terminology table for normative definitions.

**Resolution:** All access-controlled doors on egress paths shall be fail-safe (unlock on power failure), per life safety code. Non-egress doors (e.g., server room, electrical room accessed from a secure corridor) may be fail-secure at DB's discretion with code confirmation.

**Source:** ASSUMPTION (standard practice and Alberta Building Code egress requirements — location TBD)

## Owner Election Decision Framework (D-003)

**ASSUMPTION:** The following factors are relevant to the Owner's go/no-go decision on electing this option at award. This framework is directional guidance to support a conclusive merit verdict, not a formal decision matrix.

| Factor | Consideration |
|---|---|
| **Cost of election at award vs. future retrofit** | Installing access control during construction is typically significantly less expensive than retrofitting after occupancy (conduit, cabling, and patching costs avoided). The DB should quantify this difference in the pricing narrative if feasible. Estimated retrofit cost premium should be noted to inform the election decision (see Consideration B-005 on rough-in provisions). |
| **Total cost of ownership (lifecycle cost)** | Upfront capital cost is only one dimension; the Owner should also evaluate ongoing operational costs including credential management, software licensing renewals, maintenance, and staff administration time (see Consideration A-005). The DB should provide a lifecycle cost summary or framework in the pricing narrative. |
| **Operational risk of no access control** | Without access control, all interior spaces in the shared-use PSB rely on mechanical keying alone, which offers no audit trail (limited event logging), limited access hierarchy flexibility, and higher re-keying cost when staff change. Electronic access control provides granular audit trail (REQ-AC-009), flexible access scheduling, and reduced mechanical re-keying dependency. |
| **Insurance implications** | TBD — the Owner should confirm whether building insurance premiums, coverage terms, or policy requirements are affected by the presence or absence of electronic access control in a municipal facility housing emergency services (Fire Department 24/7 operations). |
| **Staff security expectations** | Fire Department and Public Works staff may have expectations regarding controlled access to sensitive areas (IT room, SCBA/cascade room, evidence/records, station office). The Owner should gauge operational staff input on whether access control meets their operational needs. |
| **Accessibility compliance** | Access control hardware (readers, locks) must integrate with barrier-free access requirements for persons with disabilities (see Consideration C-003). The Owner should confirm that the proposed access control design does not introduce accessibility barriers. |
| **Integration opportunity with DEL-05-04** | If the Owner is also considering the security/camera option (DEL-05-04), electing both options together may provide integration efficiencies (e.g., cameras at access-controlled doors for recording). They are separately priced but functionally complementary. |
| **Future scalability and rough-in provisions** | A system installed at construction can be expanded more easily (additional doors, readers, zones) than a retrofit installation. See Datasheet.md system topology constraints and Consideration B-005 regarding conduit rough-in provisions in base scope (if option is not elected). |

**Source:** ASSUMPTION (decision framework enhanced per lensing items A-005, B-005, C-003, D-003; OSR S12 optional items framing and standard municipal procurement considerations)

## Examples

No project-specific examples are available in the accessible source documents.

**ASSUMPTION:** A typical access control implementation for a combined municipal operations facility of this type would include:
- 1 system controller/panel per access control zone cluster
- Fob reader at each controlled door (typically wall-mounted, interior and/or exterior)
- Electric strike or electromagnetic lock at each controlled opening (see Specification.md REQ-AC-004 Lock Hardware Terminology table)
- Management software accessible at a network workstation (station office or IT room)
- Battery backup for all panels (minimum 4-hour backup ASSUMPTION)
- Event logging capability with local or remote audit trail access (see REQ-AC-009)

These are illustrative only. The DB shall propose the specific configuration in the zoning concept and device schedule.

---

## Conflict Table & Open Items (for human ruling)

| Item ID | Item Type | Item | Source | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-AC-01 | Conflict | Functional Program lists "Exterior Sand Shed" as Key Fob Access, but the sand shed (pickled sand storage) is explicitly excluded from the contract scope (SOW-0400 OUT). | Functional Program (Appendix B), page 46 of RFP vs. Addendum 03 S1.2; SOW-0400 | REQ-AC-003; Device Schedule | Exclude sand shed from access control scope per SOW-0400 OUT. DB to confirm no other excluded facility appears on the key fob list. | TBD |
| CONF-AC-02 | Conflict | OSR S12.3 refers to "multiple zones" but does not specify a minimum number of zones. Functional Program implies a minimum set of rooms (8 key-fob rooms) but does not define a zone grouping structure. | OSR S12.3 | Functional Program (Appendix B), page 46 | REQ-AC-001; Zoning Concept | DB to propose zone structure (minimum 2 distinct zones recommended per Datasheet) in zoning concept; Owner to confirm at proposal review. | TBD |
| OPEN-AC-01 | TBD_Question | Total credentialed user count and visitor credential requirements unknown; essential for system sizing. | No source document states expected total users or visitor needs | REQ-AC-001, REQ-AC-003, Datasheet Attributes | DB to confirm with Owner before finalizing system proposal (item B-003). | TBD |
| OPEN-AC-02 | TBD_Question | Alberta-specific access control licensing or installer certification requirements (Alberta Security Services and Investigators Act) not confirmed. | TBD — no source accessed | REQ-AC-007 (Code Compliance), Datasheet Attributes | Owner / AHJ to confirm whether Alberta provincial licensing applies (item A-002). | TBD |
| OPEN-AC-03 | TBD_Question | System availability/uptime requirement (e.g., 99.9% availability) not specified despite 24/7 Fire Department operations context. | 24/7 operations noted in Datasheet & Guidance, but no uptime SLA stated | REQ-AC-006, Specification | Owner to decide whether TBD-X003 uptime requirement applies given 24/7 operations. | TBD |
| OPEN-AC-04 | TBD_Question | Event log retention period (REQ-AC-009) not specified; Owner to confirm required retention duration. | REQ-AC-009 (Event Logging) | Specification Documentation, Procedure Step B5 | Owner to confirm retention period (item TBD-X001); DB to implement in system configuration. | TBD |
| OPEN-AC-05 | TBD_Question | Minimum warranty period for access control system components not specified (manufacturer warranty vs. DB extended warranty). | Specification Documentation section lists warranty as TBD | Specification, Procedure Step B6 | Owner to confirm minimum warranty period requirement (item TBD-F004). | TBD |
| OPEN-AC-06 | RationaleGap | If access control option is not elected at award, it is unclear whether base building conduit rough-in should be included to enable future retrofit. Cost difference is significant. | Standard practice concern; no source document addresses non-election scenarios | Datasheet Construction, Guidance Consideration B-005 | DB to address in pricing narrative whether base-scope conduit rough-in is included for future access control retrofit (item B-005). | TBD |
