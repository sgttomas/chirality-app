# Guidance
## DEL-009-04 | Code Compliance Register & Inspection Log

---

## Purpose

DEL-009-04 exists to provide centralized, real-time visibility into the project's regulatory compliance status. On a design-build project with multiple permit types, multiple regulatory authorities, and a hard completion deadline of December 31, 2026 (RFP §3.1), compliance failures discovered late are costly to rectify and may delay the Construction Completion Certificate (CCC). The register converts the compliance obligation — scattered across development, building, and Safety Code permit conditions — into a managed, trackable item set.

The RFP explicitly requires the Proponent to submit all inspection requests and to ensure the County project representative is present for all inspections, with copies of all completed reports provided to the County (RFP §3.3.2). DEL-009-04 is the mechanism that operationalizes these requirements across the project lifecycle.

The register also serves a risk management function (OBJ-007): proactive tracking of inspections and deficiencies allows corrective action before non-compliance becomes a contract or guarantee-period liability. Under RFP §2.10.6, guarantee-period deficiency rectification must occur within 10 days of the Owner's written instruction; a well-maintained register provides the audit trail necessary to demonstrate timely response.

---

## Principles

### 1. Consolidation Before Construction
All permit conditions from DEL-009-01 (Development Permit), DEL-009-02 (Building Permit), and DEL-009-03 (Safety Code Permits) should be loaded into the register before construction activities begin. This ensures the inspection schedule can be planned against actual permit conditions rather than assumed ones.

### 2. Source Fidelity
Each entry in the register should cite the specific permit condition or regulatory requirement it tracks. Paraphrasing conditions introduces ambiguity; conditions should be captured verbatim or with a precise reference to the permit document and clause.

### 3. County Coordination as a Workflow Step
The requirement for County project representative attendance at all inspections (RFP §3.3.2) means inspection coordination must be a formal workflow step — not an afterthought. Notify the County project representative in advance of each inspection; record the notification and the County representative's attendance in the register.

### 4. Proactive Deficiency Management
Deficiencies identified during inspections should be logged immediately and assigned a resolution owner and target date. Waiting for authority follow-up before logging a deficiency increases the risk of missed deadlines and non-compliance findings at subsequent inspections.

### 5. Living Document
The register is not a static deliverable. It is an operational tool active from permit issuance through project closeout. Entries are added, updated, and closed throughout the construction and commissioning phases.

---

## Considerations

### Timing and Sequencing
The register cannot be fully populated until the upstream permit deliverables (DEL-009-01, DEL-009-02, DEL-009-03) are complete. However, the register template and schema should be designed early so that conditions can be entered immediately upon permit issuance. Delayed template development risks a gap between permit issuance and systematic tracking.

### Multiple Regulatory Authorities
Safety Code permits in Alberta may involve multiple technical safety authorities (e.g., electrical, gas, pressure equipment). ASSUMPTION: each Safety Code discipline may have its own inspection regime and reporting requirements. The register schema should accommodate authority-specific tracking fields. Specific authorities are TBD pending permit issuance.

### County as Observer, Not Authority
The County project representative attends inspections but the inspection authority is the regulatory body (not the County). The register should distinguish between County notification/attendance records and official inspection authority sign-offs.

### Guarantee Period Scope
The guarantee period extends through the construction period plus two (2) years following the CCC (RFP §2.10.2). Deficiencies discovered during this period must be tracked using the same register framework. The register should not be archived at practical completion; it remains active through the guarantee period.

### Permit Fee Exclusion
Permit fees are paid by Camrose County, not the Proponent (RFP §3.3.1). The register tracks permit conditions and inspections, not fee payment status. Fee payment records are County-managed.

### Inspection Report Retention
All completed inspection reports are to be provided to the County (RFP §3.3.2). The register should log the date and method of delivery for each report. Physical or digital copies should be retained in the compliance evidence file.

### Alberta OH&S Prime Contractor Designation
As Prime Contractor (RFP §2.15), the Design-Builder holds site safety responsibility. While the OH&S compliance program is managed under DEL-019-01, the Code Compliance Register should cross-reference any safety-related inspections required by Safety Code permits to avoid duplicate tracking and to ensure consistent reporting to the County.

### Authority Chain for Compliance Determinations *(Enrichment: F-001)*
The Specification assigns verification responsibility to the "Project Manager" or "Project Manager / Compliance Officer" for each requirement, but the actual conformance authority for code compliance rests with the regulatory inspection bodies (e.g., Camrose County building inspector, Safety Codes authorities). The authority chain for a compliance determination flows as follows:

1. **Regulatory authority** issues the inspection determination (pass, conditional pass, or deficiency).
2. **Project Manager / Compliance Officer** receives the determination, records it in the register, and initiates corrective action if needed.
3. **County project representative** is informed via inspection report delivery (RFP §3.3.2) but does not hold compliance sign-off authority.

The register status for a compliance item should reflect the regulatory authority's determination, not the Project Manager's assessment. The Project Manager's role is operational stewardship of the register and coordination, not compliance adjudication. ASSUMPTION: this authority chain interpretation is consistent with Alberta Safety Codes and building inspection frameworks; confirm with regulatory authorities if questions arise.

### Compliance Status Reporting *(Enrichment: E-003)*
The register tracks compliance item-by-item, but project stakeholders require periodic summary reporting to support decision-making. The following reporting considerations apply:

- **Report audience:** Project Manager, Project Sponsor, County project representative (as contractually required), and any other stakeholders identified in the communication protocol.
- **Report content (ASSUMPTION):** Summary of register status by permit type, count of open/closed/deficient items, overdue inspection requests, deficiency resolution status, and KPI trends (per REQ-014).
- **Frequency:** TBD — ASSUMPTION: align with the periodic register audit frequency (REQ-011) so that audit and reporting occur together.
- **Format:** TBD — depends on register platform (see Trade-offs / System Platform below). The human should confirm the preferred reporting format and distribution list.

### Operationalizing the 10-Day Deficiency Rectification Obligation *(Enrichment: D-001)*
Specification REQ-007 and Procedure Step 4.2 reference the 10-day rectification requirement (RFP §2.10.6), but the practical implications for the register's timing fields require clarification:

- **During construction (pre-CCC):** Deficiency resolution timelines are driven by the inspection authority's requirements and the project schedule. The 10-day rectification clause in RFP §2.10.6 applies specifically to the guarantee period.
- **During the guarantee period (post-CCC):** The 10-day clock starts at the date of the Owner's written instruction to rectify the deficiency (RFP §2.10.6 — "within ten (10) Days of the Owner's written instruction"). The register should record both the Owner's instruction date and the 10-day deadline.
- **Register timing fields:** The register should include: (a) deficiency discovery date, (b) Owner written instruction date (guarantee period deficiencies), (c) 10-day deadline date (calculated), and (d) actual resolution date.

ASSUMPTION: For construction-phase deficiencies (pre-CCC), no specific contractual timeline is stated in the RFP; resolution timelines are managed operationally. The human should confirm whether the project intends to apply a standard resolution timeline for construction-phase deficiencies as well.

---

## Trade-offs

### Centralized Register vs. Per-Permit Tracking
A single centralized register provides unified visibility across all permit types but may be complex to manage when multiple permits have different inspection regimes. An alternative is per-permit tracking with a summary roll-up. The centralized approach is preferred given the RFP requirement to coordinate inspections through the County project representative; fragmented tracking would complicate the coordination obligation.

### Detail Level in Register Entries
Highly detailed register entries (verbatim conditions, full authority correspondence) provide maximum audit defensibility but require more administrative effort. Minimal entries (reference only) reduce effort but increase audit risk. ASSUMPTION: a balanced approach — verbatim condition text plus key tracking fields (status, inspection date, outcome, report reference) — is appropriate for a project of this scope. The human should confirm the preferred level of detail.

### System Platform (Spreadsheet vs. Project Management Tool)
The RFP and sources do not specify a platform for the register. ASSUMPTION: a spreadsheet-based register is appropriate for this project scale. If the project uses a construction management platform, integration with that platform would be preferable for real-time access. The human should confirm the intended platform.

TBD: Confirm register platform to determine whether real-time appraisal and reporting capabilities (compliance status dashboards, overdue-item alerts, automated KPI calculation) are feasible. The register's capacity for summary reporting (see Considerations / Compliance Status Reporting) and quality metrics (REQ-014) depends on the platform. A spreadsheet may require manual reporting; a PMIS may support automated dashboards. *(Enrichment: C-003 — platform confirmation needed for appraisal capacity.)*

---

## Examples

### Example Register Schema Fields (ASSUMPTION — for human review)
The following fields are representative of what a permit conditions compliance register entry would contain. This is an inferred structure based on the deliverable type and requirements; the actual schema should be confirmed by the Project Manager.

| Field | Example |
|-------|---------|
| Entry ID | CC-001 |
| Permit Type | Building Permit |
| Permit Reference | BP-XXXX (Camrose County) |
| Condition # | Condition 3 |
| Condition Text | [verbatim from permit] |
| Responsible Party | General Contractor |
| Required Inspection | Framing inspection prior to insulation |
| Inspection Requested (Date) | TBD |
| Authority | Camrose County Building Inspection |
| County Rep Notified (Date) | TBD |
| County Rep Attended (Y/N) | TBD |
| Inspection Date | TBD |
| Inspection Outcome | TBD (Pass / Deficiency) |
| Pass/Fail Criterion | [specific code section or inspection standard reference] |
| Deficiency Description | TBD |
| Corrective Action | TBD |
| Resolution Date | TBD |
| Report Delivered to County (Date) | TBD |
| Compliance Evidence Ref | TBD |
| Evidence Type | [signed certificate / authority letter / signed report / photo with sign-off] |
| Register Operator (entry by) | [name of person who recorded the entry] |
| Owner Instruction Date | [guarantee period deficiencies only] |
| 10-Day Deadline | [calculated, guarantee period deficiencies only] |
| Status | OPEN / RESOLVED / CLOSED |

---

## Conflict Table (for human ruling)

No unresolvable conflicts have been identified in the available sources at this stage. The following items represent open questions rather than source conflicts; they are recorded here for human resolution.

| Conflict ID | Issue | Source A | Source B | Impacted Sections | Proposal | Human Ruling |
|---|---|---|---|---|---|---|
| OQ-001 | Which specific Alberta Safety Codes apply to this project (electrical, gas, pressure equipment, elevating devices, etc.)? | RFP §3.3.2 (general reference only) | DEL-009-03 (not yet issued) | REQ-005; Inspection schedule matrix; Datasheet Applicable Regulatory Framework | Determine upon Safety Code permit issuance from DEL-009-03 | TBD |
| OQ-002 | What platform / system will host the Code Compliance Register (spreadsheet, construction management software, other)? | _CONTEXT.md (silent on platform) | Trade-offs section above | Register template; distribution; reporting capability; KPI automation (REQ-014) | ASSUMPTION: spreadsheet-based unless project uses a PMIS | TBD |
| OQ-003 | Who is the County project representative for inspections? | RFP §3.1 (identity confirmed at project award) | _STATUS.md (TBD) | REQ-002; inspection coordination workflow | Confirm with County at project award | TBD |
| OQ-004 | Are there OH&S-related inspections under Safety Code permits that overlap with DEL-019-01 Prime Contractor obligations? | RFP §2.15 (Prime Contractor); RFP §3.3.2 (Safety Codes) | DEL-019-01 (Prime Contractor package) | Inspection schedule; cross-reference with DEL-019-01 | Cross-reference Safety Code inspection items with OH&S program; avoid duplication | TBD |
| OQ-005 | What is the mandatory timeline for delivering inspection reports to County after inspection completion? *(Enrichment: A-002)* | RFP §3.3.2 (requires delivery but does not specify timeline) | Procedure Step 3.4 (TBD business days) | REQ-003; Procedure Step 3.4; REQ-014 KPI (inspection report delivery time) | Confirm with County project representative at project award | TBD |
| OQ-006 | What is the appropriate frequency for periodic register audit (REQ-011) and compliance status reporting? *(Enrichment: A-004, D-003, E-003)* | ASSUMPTION: monthly or at major milestones | No source specifies | REQ-011; REQ-014; Compliance Status Reporting | ASSUMPTION: monthly during active construction; confirm with Project Manager | TBD |
| OQ-007 | What records retention obligations apply beyond the guarantee period? *(Enrichment: B-002)* | Procedure Records (TBD — defers to "applicable Alberta records retention regulations") | No specific regulation identified in sources | Procedure Records section; compliance evidence file | Confirm with legal counsel; identify applicable Alberta regulations | TBD |
