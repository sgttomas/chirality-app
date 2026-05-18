# Procedure — DEL-05-03: Option — Access Control

## Purpose

This procedure describes:

1. **Production process** — the steps to produce the DEL-05-03 deliverable package (zoning concept, device schedule, pricing sheet) at the proposal stage.
2. **Implementation process** — the steps to implement the access control system during design and construction, if the Owner elects this option at award.

Both phases are addressed because this is an optional scope package with a lifecycle that spans from proposal (pricing/concept) through post-award implementation (if elected).

## Prerequisites

### For Proposal-Stage Production
- Access to the Functional Program (Appendix B of RFP) — specifically the Key Fob Access room designations
- Access to OSR S12.3 (Access Control requirement statement)
- Access to the architectural floor plan concept (from DEL-02-01_Architectural-Program-and-Space-Planning) — to enable zone mapping onto building layout
- **ASSUMPTION:** Coordination with the electrical/IT lead (DEL-02-06) for base building infrastructure integration assumptions
- Access to PKG-005 pricing framework and optional items structure (OSR S12; Decomposition)

### For Post-Award Implementation (if Owner-elected)
- Owner election of this option at contract award
- Issued-for-Construction (IFC) architectural drawings showing final door locations and room layouts
- Coordinated electrical design (DEL-02-06) confirming low-voltage infrastructure routing and panel locations
- Access control system supplier/sub-trade selection
- Integration plan with fire alarm system for electromagnetic lock release on fire-separation doors (**ASSUMPTION:** required per standard fire code practice)
- Integration plan with any other building security systems (if applicable)

## Steps

### Phase A: Proposal-Stage Deliverable Production

**Step A1 — Review Source Requirements**
- Read OSR S12.3 to confirm scope statement: main building only, multiple zones, shared-space and interdepartmental access control, ancillary buildings excluded.
- Review the Functional Program (Appendix B) Key Fob Access column to extract the minimum room list requiring access control hardware.
- Confirm that "Exterior Sand Shed" is excluded from this deliverable's scope (SOW-0400 OUT — pickled sand storage excluded from contract).

**Source:** OSR S12.3; Functional Program (Appendix B), page 46 of RFP; SOW-0400

**Step A2 — Develop Zoning Concept**
- Map the main building program onto conceptual access control zones, grouping rooms by operational function and access level:
  - Shared/open zones (no controlled access required)
  - Restricted utility zones (mechanical, electrical, IT, janitor rooms)
  - Fire Department operational zones (station office, SCBA/cascade, decontamination, gear storage)
  - Public Works operational zones (shop offices, warehousing, work/storage)
- Document the proposed zone structure in a zoning concept diagram or table, showing which rooms fall within each zone and the access hierarchy between zones.
- Verify that all Functional Program Key Fob Access rooms are covered within the zoning concept.

**Source:** OSR S12.3; Functional Program (Appendix B), page 46 of RFP; ASSUMPTION (zone categorization approach)

**Step A3 — Prepare Device Schedule**
- For each controlled opening identified in the zoning concept, prepare a device schedule row containing:
  - Location/room name
  - Door/opening ID (cross-referenced to architectural door schedule if available)
  - Access control zone assignment
  - Reader type (e.g., key fob reader — proximity RFID)
  - Lock hardware type — use normative terminology from Specification.md REQ-AC-004 Lock Hardware Terminology table: **electromagnetic lock** or **electric strike**
  - Fail-mode designation — use normative terminology: **fail-safe** or **fail-secure** (see Specification.md REQ-AC-004 Lock Hardware Terminology table for definitions)
  - Controller assignment
  - Any special requirements (e.g., dual-credential for sensitive areas)
- Confirm egress provisions: all controlled doors on egress paths must be fail-safe (unlock on power failure).
- Confirm fire-separation provisions: all electromagnetic locks on fire-separation doors must release on fire alarm activation.

**Source:** REQ-AC-004 (Specification.md); Functional Program (Appendix B); ASSUMPTION (device schedule content)

**Step A4 — Develop System Architecture Summary**
- Identify the proposed system controller/panel location(s) and management interface approach.
- Describe the power supply and backup approach (ASSUMPTION: battery backup for panels; duration TBD).
- Confirm maximum cable run / topology constraints for proposed equipment (see Datasheet.md Construction table).
- Note any network connectivity requirements for system management.
- Note event logging capability and audit trail storage approach (see Specification.md REQ-AC-009).
- Note cybersecurity provisions for network-connected components (see Specification.md REQ-AC-010).
- Identify integration touchpoints with the base building electrical/IT package (DEL-02-06).

**Source:** REQ-AC-006; REQ-AC-007; REQ-AC-009; REQ-AC-010 (Specification.md); ASSUMPTION

**Step A5 — Prepare Pricing Sheet**
- Compile a pricing sheet for the complete access control system as an optional priced item, including:
  - Materials: readers, lock hardware, controllers, panels, cabling, conduit, back boxes
  - Labour: installation, termination, programming, commissioning
  - Training: Owner staff orientation on system use and credential management
  - Any software licensing (if applicable) — note whether ongoing licence renewals are included or excluded
- Present the price as a separable lump sum (or itemized by zone if preferred), clearly distinct from base scope.
- Note any exclusions or assumptions embedded in the price (e.g., conduit rough-in assumed in base building electrical).
- State explicitly whether base-scope conduit rough-in for future access control is included (even if option is not elected) — see Guidance.md Consideration on non-election rough-in provisions.
- Where feasible, provide a lifecycle cost summary or note recurring cost categories (credential replacement, software licensing, maintenance) to support the Owner's election decision — see Guidance.md Consideration on lifecycle cost.

**Source:** REQ-AC-005 (Specification.md); OSR S12; _CONTEXT.md (Anticipated Artifacts)

**Step A6 — Assemble and Review Deliverable Package**
- Compile: zoning concept + device schedule + pricing sheet as the DEL-05-03 deliverable package.
- Perform internal review:
  - All Functional Program Key Fob Access rooms are included in the device schedule.
  - Sand shed / ancillary buildings are absent from the device schedule.
  - Pricing sheet is clearly separable and itemized consistently with the device schedule.
  - Zoning concept and device schedule are internally consistent (no rooms referenced in one but missing from the other).
  - Lock hardware terminology is consistent with Specification.md REQ-AC-004 Lock Hardware Terminology table.
- Confirm terminology consistency with Specification.md and Datasheet.md.

**Source:** Specification.md REQ-AC-001 through REQ-AC-010; SPEC (cross-document consistency)

---

### Phase B: Post-Award Implementation (if Owner-Elected)

**Step B1 — Confirm Election and Scope**
- At contract award, confirm with Owner that this option has been elected.
- Review the proposal-stage zoning concept and device schedule against the final IFC architectural program; update as required.
- Confirm integration scope with DEL-02-06 electrical/IT team.
- Confirm fire alarm integration scope with fire alarm system designer/installer.

**Step B2 — Detailed Design**
- Develop detailed access control system design drawings, including:
  - Final device location plan (overlaid on architectural drawings)
  - Riser/single-line diagram showing panel locations, cabling routes, and power supply
  - Door hardware details coordinated with architectural door schedule
  - Fire alarm interface wiring details for electromagnetic locks on fire-separation doors
- Confirm reader mounting heights comply with barrier-free access requirements (CSA B651 or Alberta Building Code accessibility provisions — specific height TBD; see Guidance.md Consideration on accessibility impact).
- Submit system submittals/shop drawings for Owner review per design milestone schedule (DEL-01-01).

**Source:** ASSUMPTION (consistent with RFP S7.1.8 design milestone requirements)

**Step B3 — Coordinate with Construction**
- Rough-in conduit and back boxes during framing/wall construction phase.
- Coordinate with electrical trades (base building) for panel power feeds and emergency power backup circuit confirmation.
- Coordinate door hardware installation with door frame installation schedule; confirm fail-safe/fail-secure lock types align with final architectural door schedule.
- Coordinate fire alarm integration: confirm wiring pathways for electromagnetic lock release circuits from fire alarm panel to access control doors on fire-separation paths (**ASSUMPTION:** standard practice for electromagnetic-lock-equipped fire-separation doors; per item A-004; fire alarm integration step required in Step B3).

**Source:** ASSUMPTION (standard construction sequencing; enhanced per lensing item A-004)

**Step B4 — Installation and Programming**
- Install access control panels, readers, lock hardware, and cabling.
- Program system: user groups, access levels, time schedules, zone assignments.
- Configure event logging and audit trail capability (per REQ-AC-009): set event log retention period per Owner confirmation (TBD-X001); test event logging during testing steps below.
- Implement cybersecurity provisions (per REQ-AC-010): change all default credentials/passwords, configure encrypted communications (where supported by equipment), confirm network segmentation with IT lead; submit cybersecurity checklist.
- Perform door-by-door functional testing per the Field Testing Protocol below (item D-001).

**Field Testing Protocol (D-001) — Required for REQ-AC-004, REQ-AC-007 Verification:**

For each controlled door, test and record pass/fail for each test item below:

| Test | Method | Acceptance Criterion |
|---|---|---|
| Credential read | Present valid fob at reader | Door unlocks within manufacturer-specified time (typically <1 second); event logged as "access granted" with timestamp |
| Credential deny | Present invalid/revoked fob | Door remains locked; event logged as "access denied" with timestamp and reason |
| Read range | Present valid fob at maximum specified distance | Reader responds reliably at manufacturer-rated read range |
| Fail-safe confirmation (egress doors) | Simulate power loss to lock hardware (disable panel power or disconnect lock power) | Door unlocks immediately on power loss; fails safely to prevent occupant trapping |
| Fail-secure confirmation (non-egress doors, if applicable) | Simulate power loss to lock hardware | Door remains locked on power loss (if lock type designated fail-secure per architectural requirements) |
| Fire alarm release (fire-separation doors with electromagnetic locks) | Activate fire alarm system in test mode (coordination with fire alarm sub-trade) | Electromagnetic lock releases within fire alarm release time requirement; door freely operable for egress |
| Forced-entry alarm (if applicable) | Attempt to open door without valid credential | Alarm event generated, logged with timestamp, and reported to management interface |
| Door-held-open alarm (if applicable) | Hold door open beyond programmed time threshold | Alarm event generated, logged with timestamp, and reported to management interface |

**Documentation:** All door-by-door test results shall be recorded on a test form with door location, test date, tester name, and pass/fail status. Results feed into integration test and commissioning report.

**Source:** REQ-AC-004, REQ-AC-007, REQ-AC-009 (Specification.md); item D-001 lensing requirement

**Step B4a — Integration Testing (D-002) — Required for REQ-AC-006 Verification:**

After individual door testing is complete, perform system-level integration testing to confirm all access control system components function correctly together:

- **Network connectivity:** Confirm management interface can communicate with all panels and readers; verify remote access capability (if applicable); test event log queries.
- **Emergency power switchover:** Simulate normal power loss; confirm panels switch to battery backup and all fail-safe doors unlock. Confirm system restores to normal operation when power is restored. Log battery backup performance event.
- **Fire alarm integration (if applicable):** Coordinate full-building fire alarm test with fire alarm system sub-trade; confirm all electromagnetic locks on fire-separation paths release on building fire alarm activation (not door-by-door, but system-level integration). Verify no egress path is blocked.
- **Event logging verification:** Confirm all integration test events are logged with correct timestamps; verify log retention and archival settings align with Owner TBD-X001 requirement.

**Documentation:** Document all integration test results in the commissioning report (Step B5 deliverable). Include network connectivity status, battery backup performance, fire alarm release confirmation, and event logging validation.

**Source:** REQ-AC-006, REQ-AC-009, REQ-AC-010 (Specification.md); item D-002 lensing requirement

**Step B5 — Commissioning and Training**
- Commission the access control system as part of the overall building commissioning process (DEL-01-07): confirm all requirements tested (REQ-AC-001 through REQ-AC-010) and document in commissioning report.
- Provide comprehensive training to Town of Penhold staff designated by Owner:
  - **System administrator training:** Master credential management (adding/revoking users), user group configuration, access level programming, event log review and interpretation, system monitoring, credential re-issuance procedures, firmware/software update procedures (per Guidance.md post-handover maintenance)
  - **General user training:** Credential use and care, reporting lost/stolen credentials, basic troubleshooting, emergency access procedure
- Perform credential management handover (X-002 — Essential Validated Deployment):
  - **Transfer master/administrator credentials** to the Owner-designated system administrator (typically IT staff or facilities manager)
  - **Document enrollment/revocation process** — create procedures for enrolling new user credentials and revoking departing staff credentials; include frequency of credential audits
  - **Competence confirmation** — validate that the designated system administrator can independently perform: add new user, revoke user credential, modify access level for existing user, query event log, export event logs
  - **Emergency access procedure** — provide master override/emergency access key or bypass procedure for lockout situations
  - **Handover sign-off** — document that Owner confirms receipt and acceptance of system administration capability
- Issue commissioning report confirming:
  - All 8 Functional Program key-fob rooms tested and access control operational (per REQ-AC-001, REQ-AC-003)
  - Field test protocol results from B4 (door-by-door testing)
  - Integration test results from B4a (system-level testing, emergency power, fire alarm release)
  - Event logging functional and retention period configured per Owner TBD-X001 requirement
  - Training completion and credential handover sign-off
  - All REQ-AC-001 through REQ-AC-010 verified and satisfied

**Source:** RFP S7.3.6 commissioning and training; DEL-01-07; REQ-AC-008; item X-002 lensing requirement

**Step B6 — Closeout Documentation**
- Submit as-built drawings showing final device locations, panel locations, reader mounting heights, cabling routes, and emergency power circuit details (verify barrier-free mounting height per CSA B651 or Alberta Building Code — item C-003).
- Submit comprehensive O&M manual for the access control system, including:
  - Manufacturer documentation for all equipment (readers, locks, panels, controllers, software)
  - Recommended preventive maintenance schedule (see Guidance.md Consideration X-004 on post-handover maintenance):
    - Annual credential audit procedure
    - Battery replacement schedule (typically 3-5 years; manufacturer-specific)
    - Firmware/software update procedures and frequency
    - Preventive inspection checklist for readers, locks, sensors, hardware
    - Event log archival and retention procedures
  - System architecture and networking documentation
  - Troubleshooting guide and emergency procedures
- Submit programming records documentation:
  - User groups defined and staffing levels
  - Access levels and zone assignments (cross-referenced to architectural room list)
  - Credential inventory and issuance log template
  - Time schedules and exception protocols
- Submit cybersecurity checklist confirming REQ-AC-010 provisions (see Specification.md):
  - Default credentials changed confirmation
  - Encrypted communications status (where supported)
  - Network segmentation confirmation with IT lead sign-off
  - Security update and patch management procedure
- Submit event logging documentation:
  - Event log retention period confirmed per Owner TBD-X001 requirement
  - Log query and export procedures
  - Event log archival location and frequency
- Transfer all warranties and software licenses to Owner:
  - Manufacturer warranty documentation for all major components (readers, locks, panels, software)
  - Warranty period statement; confirm minimum period per TBD-F004 (Owner decision)
  - Software license documentation (if system uses licensed management software)
  - License renewal requirements and costs (to inform Owner of lifecycle costs per Guidance.md A-005)

**Source:** RFP S7.5; DEL-01-07 closeout requirements; REQ-AC-009, REQ-AC-010; items A-005, X-004 lensing requirements

## Verification

| Step | Verification Check |
|---|---|
| A2 — Zoning Concept | All Functional Program Key Fob Access rooms appear in zoning concept; no ancillary buildings included; minimum zone groupings aligned with operational function |
| A3 — Device Schedule | Device count consistent with zoning concept; all egress doors designated fail-safe; all fire-separation doors with electromagnetic locks noted for fire alarm release; lock hardware terminology consistent with Specification.md REQ-AC-004 |
| A5 — Pricing Sheet | Price is separable from base; inclusions/exclusions are explicit; conduit rough-in allocation stated; lifecycle cost categories noted |
| A6 — Package Assembly | Internal consistency check complete; no cross-document discrepancies; lock hardware terminology consistent |
| B4 — Field Testing | Each controlled door tested per field testing protocol (credential read, deny, read range, fail-mode, fire alarm release as applicable); all results documented |
| B4a — Integration Testing | Network connectivity, emergency power switchover, fire alarm integration, and event logging verified at system level |
| B5 — Commissioning | Commissioning report issued (including B4 and B4a results); training records signed by attendees; credential management handover confirmed with system administrator |
| B6 — Closeout | As-builts, O&M manual (with maintenance schedule), programming records, cybersecurity checklist, and warranty documents submitted |

## Records

### Proposal Stage
| Record | Description |
|---|---|
| Zoning concept | Diagram or table defining access control zones and room assignments |
| Device schedule | Table of all controlled openings with hardware, fail-mode, and zone assignment (using normative terminology from Specification.md) |
| Pricing sheet | Separable optional price with inclusions/exclusions noted; lifecycle cost categories indicated |

### Post-Award (if elected)
| Record | Description |
|---|---|
| Shop drawing submittals | System equipment submittals reviewed and approved (including product certification documentation per REQ-AC-009, F-002) |
| As-built drawings | Final device locations, panel locations, cabling routes, reader mounting heights (barrier-free verification per C-003), emergency power circuit details |
| Field test records | Door-by-door test results per Field Testing Protocol (Step B4): credential read, deny, read range, fail-safe/fail-secure confirmation, fire alarm release, alarm events. Test form with location, date, tester, pass/fail status for each door. |
| Integration test records | System-level integration test results (Step B4a): network connectivity, emergency power switchover, fire alarm integration (if applicable), event logging verification. Document network status, battery performance, fire alarm release confirmation, event log validation. |
| Event logging documentation | Event log retention period configuration per Owner TBD-X001; query and export procedures; archival location and frequency (per REQ-AC-009) |
| Commissioning report | Consolidated test results for all controlled points (REQ-AC-001 through REQ-AC-010); field test protocol results (B4); integration test results (B4a); event logging functional confirmation; training completion sign-off; credential handover confirmation. |
| Training records | Signed attendance records for Owner staff training (administrator comprehensive training and general user training); administrator competency confirmation (per item X-002). |
| Credential handover record | Documentation of master/administrator credential transfer; procedures for enrollment/revocation; emergency access procedure; Owner system administrator sign-off confirming independent capability (add user, revoke user, modify access level, query event log). |
| O&M manual | Comprehensive operation and maintenance documentation: manufacturer documentation, preventive maintenance schedule (annual credential audit, battery replacement, firmware updates, preventive inspection, event log archival per Guidance.md X-004), system architecture/networking, troubleshooting guide, emergency procedures. |
| Programming records | User groups, access levels, time schedules, zone assignments, credential inventory template, exception protocols, staffing-to-access mappings. |
| Cybersecurity checklist | Confirmation of REQ-AC-010 provisions: default credentials changed, encryption configured (where supported), network segmentation confirmed with IT sign-off, security update/patch management procedure (per E-002). |
| Warranty documents | Manufacturer warranty documentation for all major components; warranty period statement (confirm minimum per TBD-F004); software license documentation; license renewal requirements and costs (to inform lifecycle cost awareness per A-005). |
