# Specification — DEL-019-02: Weekly Meetings & Billing Coordination

**Document Type:** Specification (normative)
**Pass:** P3 (Semantic Lensing Enrichment)
**Generated:** 2026-02-26
**Agent:** 4_DOCUMENTS

---

## Scope

### What This Deliverable Covers

DEL-019-02 covers the establishment, execution, and documentation of:

1. **Weekly coordination meetings** between the Design-Builder (as Prime Contractor) and the County project manager, held for the full duration of the project. (Source: RFP §3.1, p.11; SOW-0086)
2. **Billing coordination** — all billing and payment claim submissions processed through the County project manager. (Source: RFP §3.1, p.11; SOW-0087)
3. All documentation arising from the above activities (agendas, minutes, billing records, correspondence). (Source: _CONTEXT.md — Success Criteria)

### What This Deliverable Excludes

- Subcontractor management (covered by DEL-019-03)
- Quality control management meetings (covered by DEL-019-04; QC status may appear as an agenda item in weekly meetings per ASSUMPTION below)
- Commissioning-specific meetings (covered by DEL-020-01; commissioning status may appear as agenda item per _DEPENDENCIES.md)
- Permitting and inspection coordination (covered by DEL-009-04; inspection scheduling may be a recurring agenda topic)
- Prime Contractor designation and OH&S program (covered by DEL-019-01, which is an upstream prerequisite)

---

## Requirements

### REQ-019-02-001: Weekly Meeting Frequency
**Statement:** The Design-Builder shall coordinate and hold weekly meetings with the County project manager.
**Source:** RFP §3.1, p.11; SOW-0086.
**Priority:** Mandatory.

### REQ-019-02-002: County Coordination Counterparty
**Statement:** All meeting coordination and billing shall be conducted through the County project manager. The identity of the County project manager shall be confirmed at the time of project award.
**Source:** RFP §3.1, p.11; SOW-0303 (TBD item).
**Priority:** Mandatory.

### REQ-019-02-003: Billing Coordination
**Statement:** The Design-Builder shall coordinate all billing through the County project manager.
**Source:** RFP §3.1, p.11; SOW-0087.
**Priority:** Mandatory.

### REQ-019-02-004: Invoice Submission Interval
**Statement:** A proper invoice must be submitted to the Owner at least every thirty-one (31) days.
**Source:** RFP §2.13.2 (Lien Holdback), p.11.
**Priority:** Mandatory.

### REQ-019-02-005: Payment Terms
**Statement:** Payment will be made within twenty-eight (28) days of the Owner receiving a proper invoice.
**Source:** RFP §2.13.2, p.11.
**Priority:** Informational (obligation on Owner; Design-Builder must submit compliant invoices to trigger this timeline).

### REQ-019-02-006: Lien Holdback
**Statement:** Ten percent (10%) of the value of Work performed shall be withheld from each payment in accordance with the Prompt Payment and Construction Lien Act (Alberta). The holdback shall be released upon project completion subject to the conditions in §2.13.2.1–2.13.2.3.
**Source:** RFP §2.13.2, p.11.
**Priority:** Mandatory.

### REQ-019-02-007: Holdback Release Documentation
**Statement:** Release of holdback and final payment is conditional upon submission of: (a) signed Construction Completion Certificate (CCC) issued by Owner; (b) letter from Design-Builder confirming all payment claims have been submitted; (c) WCB Letter of Clearance; (d) Statutory Declaration of no outstanding claims.
**Source:** RFP §2.13.2.1–2.13.2.3, p.11–12.
**Priority:** Mandatory.

### REQ-019-02-008: Meeting Documentation and Archival
**Statement:** Meeting minutes shall be recorded and archived for the project record.
**Source:** _CONTEXT.md (Success Criteria — "Documentation complete and archived"); MEMORY.md (Key Notes).
**Priority:** Mandatory (per project success criteria).

### REQ-019-02-009: Upstream Prerequisite — Prime Contractor Designation
**Statement:** The governance and authority structure established under DEL-019-01 (Prime Contractor Designation & OH&S Program) must be in place before weekly meeting governance can be formally established.
**Source:** _DEPENDENCIES.md (Upstream Dependencies).
**Priority:** Mandatory prerequisite.

### REQ-019-02-010: Stakeholder Participation Maintained
**Statement:** Stakeholder participation in weekly coordination meetings shall be maintained throughout the project duration.
**Source:** _CONTEXT.md (Success Criteria).
**Priority:** Mandatory (per project success criteria).

### REQ-019-02-011: Agenda Management
**Statement:** The Project Manager is responsible for agenda management for weekly meetings.
**Source:** _CONTEXT.md (Key Roles).
**Priority:** Mandatory.

### REQ-019-02-012: Escalation Process for Unresolved Items (TBD)
**Statement:** An escalation process shall be defined for unresolved action items and meeting non-attendance. The escalation path shall address: (a) action items unresolved after TBD consecutive meetings, and (b) required attendees absent without delegation for TBD consecutive meetings.
**Source:** ASSUMPTION — inferred from normative governance function of weekly meetings; prescriptive direction is undefined without an escalation path (Lensing: A-001). Procedure Step B-5 and Datasheet Attributes both flag escalation as TBD.
**Priority:** TBD — proposed as Mandatory once confirmed; proposed authority: Specification.
**Label: ASSUMPTION — escalation thresholds and actions require human ruling.**

### REQ-019-02-013: Meeting Minutes Distribution Timeline (TBD)
**Statement:** Meeting minutes shall be distributed to all attendees within TBD business days of the meeting.
**Source:** ASSUMPTION — inferred from mandatory practice lens; the minutes distribution timeline is a core operational requirement left undefined (Lensing: A-002). Procedure Step B-3 references "TBD days."
**Priority:** TBD — proposed as Mandatory once timeline is confirmed with County PM.
**Label: ASSUMPTION — timeline to be agreed with County PM at kickoff.**

### ASSUMPTION — REQ-019-02-A01: Meeting Agenda Distribution
It is assumed that meeting agendas shall be distributed to attendees in advance of each meeting (advance period: TBD — to be confirmed; see Lensing X-002 normalization note). This is not stated explicitly in the RFP but is consistent with standard construction project management practice and the Project Manager's described role in agenda management (_CONTEXT.md). **Label: ASSUMPTION.** [Lensing: X-002 — when advance period is agreed, update consistently across Specification, Procedure Step B-1, and Guidance Examples.]

### ASSUMPTION — REQ-019-02-A02: QC and Subcontractor Status as Agenda Items
It is assumed that quality control issues (DEL-019-04) and subcontractor management activities (DEL-019-03) will be presented as status items in the weekly meeting forum. **Label: ASSUMPTION — per _DEPENDENCIES.md (Internal Package Dependencies).**

### ASSUMPTION — REQ-019-02-A03: Commissioning Status Inclusion
It is assumed that as the project transitions to commissioning phases, the weekly meetings will incorporate commissioning status updates from DEL-020-01. **Label: ASSUMPTION — per _DEPENDENCIES.md (External Package Dependencies).**

---

## Standards

| Standard / Reference | Applicability | Accessibility |
|---|---|---|
| Alberta Prompt Payment and Construction Lien Act | Governs holdback amounts and release conditions. **Note [Lensing: A-004]:** The full text of this Act must be obtained for regulatory audit capability; the project team should confirm an access path (e.g., Alberta King's Printer, CanLII). **Note [Lensing: B-003]:** This Act defines "proper invoice" — the term used in REQ-019-02-004 and Procedure Step C-1. Until the definition is confirmed from the statute and any County-specific requirements, the invoice format remains TBD. See also Guidance Conflict Table. | Referenced in RFP §2.13.2; full text not in project sources (location TBD) — **action required: obtain for audit** |
| Alberta Occupational Health and Safety Act / Regulations | Governs Prime Contractor designation context relevant to meeting obligations | Referenced in RFP §2.15; full text not in project sources (location TBD) |
| CCDC 14–2013 Design-Build Stipulated Price Contract | Governs overall contract framework including payment administration. **Note [Lensing: D-001]:** The interaction between CCDC 14-2013 payment administration provisions and the RFP's meeting/billing coordination requirements is not yet documented. See Guidance for a directional note on this interaction. The contract text must be obtained to complete the governing regulatory framework. | Referenced in RFP §2.7; contract document not in project sources (location TBD) — **action required: obtain for regulatory completeness** |
| RFP §3.1 (Project Background) | Direct source for meeting and billing coordination requirements | Accessible — AB-2026-01424-WDMLRL RFP.pdf, p.11 |
| RFP §2.13 (Payment) | Direct source for invoice and payment requirements | Accessible — AB-2026-01424-WDMLRL RFP.pdf, p.11 |
| RFP §2.11 (Deficiency Holdback) | Governs Owner's deficiency holdback rights | Accessible — AB-2026-01424-WDMLRL RFP.pdf, p.7 |

---

## Verification

| Requirement | Verification Approach |
|---|---|
| REQ-019-02-001 (Weekly frequency) | Meeting schedule log / calendar showing weekly cadence; minutes dated at approximately weekly intervals. **Sufficiency note [Lensing: F-001]:** Verification should also confirm that meetings were actually *held* (not merely scheduled) — evidence: signed attendance record, minimum content in minutes (agenda coverage, decisions/action items recorded), and minimum duration/quorum criteria TBD. |
| REQ-019-02-002 (County counterparty) | County project manager identity confirmed and recorded at project award; meeting records show County PM as participant |
| REQ-019-02-003 (Billing coordination) | All invoice submissions and billing correspondence routed through County PM; correspondence records |
| REQ-019-02-004 (Invoice interval ≤ 31 days) | Invoice log showing submission dates at no more than 31-day intervals |
| REQ-019-02-005 (Payment within 28 days) | Payment receipt records tracked against invoice submission dates |
| REQ-019-02-006 (10% holdback withheld) | Payment summaries showing 10% holdback applied consistently |
| REQ-019-02-007 (Holdback release docs) | Checklist of CCC, payment claim letter, WCB clearance, statutory declaration — all obtained prior to final payment |
| REQ-019-02-008 (Minutes archival) | Archive of signed/approved meeting minutes for all meetings held |
| REQ-019-02-009 (DEL-019-01 prerequisite) | DEL-019-01 status confirmed as complete before first weekly meeting is formally scheduled |
| REQ-019-02-010 (Stakeholder participation) | Attendance records in meeting minutes; follow-up actions for absent parties. **Acceptance criteria note [Lensing: A-003]:** Add measurable threshold — e.g., minimum attendance percentage (TBD%) of required attendees per meeting, or mandatory follow-up protocol for absences (delegate required within TBD hours of scheduled meeting). Criteria TBD — requires human ruling. |
| REQ-019-02-011 (Agenda management) | Meeting agendas prepared and distributed by Project Manager; records of agenda distribution |
| REQ-019-02-012 (Escalation process) | Escalation process documented and communicated; escalation log maintained showing instances where escalation was triggered; resolution records [Lensing: A-001] |
| REQ-019-02-013 (Minutes distribution timeline) | Minutes distribution log showing distribution date vs. meeting date; compliance with agreed timeline [Lensing: A-002] |
| REQ-019-02-003/004 (Billing coordination timeliness) | **Internal process KPI [Lensing: X-003]:** Track time from work completion to invoice preparation (internal processing deadline TBD); verify that the internal billing coordination cycle supports consistent compliance with the 31-day maximum interval. Evidence: invoice preparation log with work-period-end date and invoice-submission date. |
| REQ-019-02-A01 (Agenda distribution — ASSUMPTION) | **[Lensing: D-002]:** If confirmed as a requirement, verify: agenda distributed to all confirmed attendees within agreed advance period (TBD); distribution records maintained. Currently ASSUMPTION — verification approach activated upon confirmation. |
| REQ-019-02-A02 (QC/subcontractor status — ASSUMPTION) | **[Lensing: D-002]:** If confirmed, verify: QC and subcontractor status appear as agenda items in meeting minutes for meetings where such status is relevant. Currently ASSUMPTION — verification approach activated upon confirmation. |
| REQ-019-02-A03 (Commissioning status — ASSUMPTION) | **[Lensing: D-002]:** If confirmed, verify: commissioning status updates appear in meeting minutes once project transitions to commissioning phase. Currently ASSUMPTION — verification approach activated upon confirmation. |

---

## Documentation

### Required Artifacts

The following artifacts shall be produced as outputs of DEL-019-02:

| Artifact | Description | Frequency |
|---|---|---|
| Meeting Agenda | Prepared by Project Manager in advance of each weekly meeting | Weekly |
| Meeting Minutes | Record of discussion, decisions, action items, and attendees for each meeting | Weekly |
| Meeting Schedule / Calendar | Master schedule of all weekly meeting dates and times for the project duration | Once (established at project start); updated as needed |
| Billing Correspondence Log | Record of all invoice submissions, billing coordination exchanges with County PM | Ongoing |
| Invoice Submissions | Proper invoices submitted to Owner at maximum 31-day intervals | At minimum monthly |
| Holdback Release Package | CCC, payment claim letter, WCB clearance letter, Statutory Declaration | Once (at project completion) |
| Stakeholder Contact List | Confirmed attendee list for weekly meetings including County PM contact details | Once (at project award); updated as needed |

### Document Control

- All meeting minutes and billing records shall be archived in the **Project Document Archive** (canonical term — see Guidance Vocabulary section) as part of the project record. (Source: _CONTEXT.md — Success Criteria) [Lensing: X-001 — term normalized across all four documents]
- Archival method: TBD (see MEMORY.md — Questions for Future Resolution)
