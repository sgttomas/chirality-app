# Specification: DEL-03-02 Detailed Design and Construction Docs Plan

## Scope

### Included in This Deliverable
This plan document describes the process, responsibilities, and controls for producing detailed design and construction documents for the Penhold Public Services Building Design-Build project. The plan covers:

- **Discipline deliverables:** Definition of what each design discipline (architecture, structural, mechanical, electrical, civil, landscape) will produce at each phase
- **QA/QC checks:** Quality assurance and quality control procedures to ensure completeness, code compliance, and coordination
- **Review cycles:** Internal coordination reviews, Owner review milestones, and approval processes
- **Document control:** Numbering, revision tracking, distribution, and archival protocols
- **Coordination processes:** Interdisciplinary coordination methods, clash detection, and interface management
- **Issuance procedures:** Protocols for issuing documents for Owner review, permit submission, and construction

*Source: _CONTEXT.md (acceptance criteria), decomposition Section 8 (DEL-03-02 description)*

### Excluded from This Deliverable
- **Design methodology narrative:** Covered in DEL-03-01 (companion deliverable in PKG-05)
- **Detailed project schedule:** Covered in DEL-08-01 (timing and milestones for document production)
- **Construction methodology:** Covered in PKG-06 deliverables (how construction will be executed)
- **Actual design documents:** This is the *plan* for producing documents, not the documents themselves

*Source: Decomposition Section 7 (PKG boundaries) and Section 8 (deliverable scope differentiation)*

### Scope Boundaries (ASSUMPTION: based on typical Design-Build practice)
- **Start point:** Owner acceptance of conceptual design (post-proposal award)
- **End point:** Issuance of final coordinated construction documents (IFC set)
- **Lifecycle coverage:** Design Development (DD) through Construction Documents (CD) and IFC issuance

## Requirements

### RQ-01: Document Completeness
**Requirement:** The plan shall describe how completeness of construction documents will be ensured across all disciplines.

**Details (ASSUMPTION):**
- Each discipline shall produce a complete set of drawings, specifications, and calculations as required for permit and construction
- Cover sheet with drawing index listing all sheets by discipline
- General notes, legends, symbols, and abbreviations sheets
- Cross-referencing between drawings and specifications
- Verification checklists for each discipline lead to confirm scope coverage

**Verification:** Review of plan document to confirm completeness procedures are defined; sample checklist templates provided (if applicable)

*Source: _CONTEXT.md (acceptance criteria: "Describes completeness..."), RFP Section 7.1.8 — location TBD*

---

### RQ-02: Interdisciplinary Coordination
**Requirement:** The plan shall describe the coordination process to prevent conflicts and ensure integration across disciplines.

**Details (ASSUMPTION):**
- Regular coordination meetings (frequency TBD; typical: weekly during active design phases)
- BIM coordination for structural and MEP systems (clash detection runs at DD and CD milestones)
- 2D overlay reviews for site/civil and architectural integration
- Interface matrix defining discipline boundaries and handoff points
- Coordination issue log and resolution tracking

**Verification:** Review of plan document to confirm coordination procedures and tools are specified

*Source: _CONTEXT.md (acceptance criteria: "coordination"), RFP Section 7.1.8 — location TBD*

---

### RQ-03: Quality Assurance and Quality Control (QA/QC)
**Requirement:** The plan shall define QA/QC checks at each phase to ensure quality, code compliance, and Owner requirements are met.

**Details (ASSUMPTION):**
- **Internal QA:** Discipline lead self-check before submittal to Design Manager
- **Design Manager review:** Consolidated review for completeness and cross-discipline consistency
- **Code compliance review:** Third-party or internal code specialist review at DD and CD phases (minimum)
- **Constructability review:** Construction Manager input on buildability, sequencing, cost alignment
- **Owner review cycles:** Formal submittal and comment incorporation at phase gates (SD approval, DD approval, CD approval)

**Verification:** Review of plan document to confirm QA/QC checkpoints and responsible parties are identified

*Source: _CONTEXT.md (acceptance criteria: "QA checks"), decomposition SOW-027 (quality management plan reference), RFP Section 7.1.8 — location TBD*

---

### RQ-04: Document Control and Revision Tracking
**Requirement:** The plan shall establish document control procedures including numbering, revision tracking, distribution, and archival.

**Details (ASSUMPTION):**
- Drawing numbering system by discipline (e.g., A-001 for architectural, S-001 for structural, etc.)
- Revision tracking with revision clouds, delta markers, and revision history table on each sheet
- **Electronic document management system (DMS):** Mandatory for Design-Build execution (not optional "if required")
- Distribution protocols: who receives which documents, in what format, at what milestones
- Archival and retention per Owner requirements and regulatory standards (TBD; typical: 10 years post-substantial completion)

> **[SL:C-001]** Electronic document management system (DMS) is a mandatory component of document control for Design-Build projects, not an optional "if required" provision. Modern construction practice expects DMS for version control, access management, and audit trail. *(SourcePath: Specification.md § RQ-04 Verification table; Datasheet.md § Document Control Attributes)*

**Verification:** Review of plan document to confirm document control protocols are defined, including mandatory DMS specification

*Source: _CONTEXT.md (acceptance criteria: "control of issued drawings/specs"), RFP Section 7.1.8 — location TBD; retention period ASSUMPTION*

---

### RQ-05: Owner Review and Approval Process
**Requirement:** The plan shall describe the process for Owner review, comment incorporation, and formal approvals at key milestones.

**Details (TBD: specific Owner review requirements):**
- Submittal format and delivery method (digital, hard copy, or both)
- Review period duration (typical: 2-3 weeks per milestone — ASSUMPTION)
- Comment format and tracking (comment log, response matrix)
- Approval signoff requirements (written acceptance from Owner's representative)
- Resubmittal protocols if major revisions are required

> **[SL:A-001]** The plan must state a specific proposed review period (e.g., 2-3 weeks for DD/CD submittals) subject to Owner negotiation during contract finalization. This normative guiding directive ensures the schedule is realistic and Owner expectations are managed. *(SourcePath: Specification.md § RQ-05; Guidance.md § Considerations / Owner Review Period Duration)*

**Verification:** Review of plan document to confirm Owner interface procedures are described, including specific proposed review period durations

*Source: RFP Section 7.1.8 requirements — location TBD; ASSUMPTION on typical review periods*

---

### RQ-06: Discipline Scope Definition
**Requirement:** The plan shall define the scope of deliverables for each design discipline at each phase.

**Details (ASSUMPTION: typical scope by discipline):**
- **Architectural:** Plans, elevations, sections, details, finish schedules, door/window schedules, room data sheets
- **Structural:** Foundation plans, framing plans, structural details, calculations, geotechnical integration
- **Mechanical:** HVAC layout, plumbing layout, fire protection, equipment schedules, exhaust systems (fire apparatus per Addendum 03)
- **Electrical:** Power distribution, lighting layout, fire alarm, communications, generator integration (ICP support per decomposition), panel schedules
- **Civil:** Site grading, utilities, drainage, paving, service tie-ins (allowance approach per Addendum 03)
- **Landscape:** Planting plans, irrigation — **TBD: Scope requires confirmation before finalizing**

> **[SL:F-004]** Landscape discipline scope must be resolved before plan finalization. Current documents are inconsistent: Datasheet and Specification flag landscape as conditional ("if applicable"/"TBD"), while some Procedure steps assume landscape is included. Decision required: if in scope, remove all conditional language and specify deliverables; if out of scope, remove landscape from all discipline lists and procedure steps. *(SourcePath: Datasheet.md, Specification.md, Guidance.md vs. Procedure.md § Part B)*

**Verification:** Review of plan document to confirm discipline scopes are listed

*Source: Decomposition Section 4 (Addendum 03 impacts: exhaust systems, generator, service tie-ins), project description (Fire Hall + Public Works); specific discipline deliverable lists from RFP Section 7.1.8 or Appendix I — location TBD*

---

### RQ-07: Code Compliance and Permitting Alignment
**Requirement:** The plan shall address how construction documents will meet Alberta Building Code and local permitting requirements.

**Details (ASSUMPTION):**
- Code analysis at DD phase to confirm compliance approach
- Stamped/sealed drawings by registered professionals per Alberta regulatory requirements
- Permit application package preparation (drawings + specifications + supporting documentation)
- Coordination with authority having jurisdiction (AHJ) for permit review and approval
- Incorporation of permit review comments into IFC set

> **[SL:A-003]** The plan must clarify whether third-party code review at CD phase is mandatory (best practice for Fire Hall life safety criticality) or optional (team choice). If third-party review is proposed, identify reviewer by name/firm with credentials. If internal review is proposed, confirm in-house code expertise with responsible person identification. *(SourcePath: Specification.md § RQ-07 and § Verification table)*

> **[SL:F-001]** Code compliance proficiency must be confirmed, not merely stated. The plan should identify the code reviewer (third-party or internal) by name/firm with credentials, demonstrating confirmed regulatory proficiency rather than just a strategy description. *(SourcePath: Specification.md § RQ-07)*

**Verification:** Review of plan document to confirm code compliance and permitting strategy is addressed; code reviewer credentials identified (third-party or internal with qualifications stated)

*Source: ASSUMPTION (Alberta jurisdiction; typical municipal facility permitting); RFP contract terms or Appendix A (OSR) — location TBD*

---

### RQ-08: Addenda Integration
**Requirement:** The plan shall ensure that Addendum 03 clarifications are integrated into the detailed design documentation.

**Details (from decomposition Section 4):**
- **Overhead doors:** 16 ft height requirement integrated into architectural and structural design
- **Bay sumps:** Included in mechanical/plumbing design
- **Fire apparatus exhaust systems:** Mechanical design scope confirmed
- **Generator:** Electrical design scope (ICP support); fuel system coordination
- **Fill stations:** Civil/mechanical coordination for fuel infrastructure (if in scope)
- **Solar-ready provisions:** Roof structural design, conduit/panel space allowances, orientation considerations
- **Sample room sizes:** Architectural design to incorporate Addendum 03 room sizing guidance where program lacks specific dimensions

> **[SL:A-002]** Integration verification must include an explicit addenda checklist artifact cross-mapping each Addendum 03 item to: (1) responsible discipline, (2) specific scope element, and (3) QA/QC checkpoint where compliance will be verified. The term "integrated" means traceable and verifiable, not merely acknowledged. *(SourcePath: Specification.md § RQ-08; Procedure.md § Step A-08)*

**Verification:** Review of plan document to confirm addenda requirements are explicitly called out in discipline scopes; addenda integration checklist artifact provided

*Source: Decomposition Section 4 (Addendum 03 impacts summary)*

---

### RQ-09: Drawing and Specification Coordination
**Requirement:** The plan shall describe how drawings and written specifications will be coordinated to avoid conflicts.

**Details (ASSUMPTION):**
- CSI MasterFormat specification structure aligned with drawing organization
- Specification sections cross-referenced to drawing details
- Materials and systems specified in specifications match those shown on drawings
- Joint review of drawings and specifications during QA/QC cycles

**Verification:** Review of plan document to confirm drawing/spec coordination process is described

*Source: Industry standard practice (ASSUMPTION); RFP Section 7.1.8 — location TBD*

---

### RQ-10: Issuance and Distribution Protocols
**Requirement:** The plan shall define protocols for issuing documents at each phase and distributing them to stakeholders.

**Details (TBD: specific issuance requirements):**
- **Phase milestones:** SD review, DD review, CD review, permit submission, IFC issuance
- **Issue designations:** "Issued for Owner Review," "Issued for Permit," "Issued for Construction," "Issued for Record (as-builts)"
- **Distribution list:** Owner, Design-Build team, subtrades (per Appendix I), AHJ (for permit)
- **Format:** Digital (PDF), native files (CAD/BIM as required), hard copy sets (quantity TBD)

**Verification:** Review of plan document to confirm issuance and distribution procedures are defined

*Source: Standard practice (ASSUMPTION); Owner distribution requirements from RFP or contract terms — location TBD*

## Standards

### Governing Codes and Standards (ASSUMPTION: applicable to Alberta municipal facility)
- **Alberta Building Code (ABC):** Primary building code authority
- **National Fire Code of Canada (NFC):** Fire protection and life safety requirements (applicable to Fire Hall component)
- **CSA Standards (Canadian Standards Association):**
  - CSA B651 — Accessible design for the built environment (accessibility requirements)
  - CSA C22.1 — Canadian Electrical Code (electrical systems)
  - CSA B52 — Mechanical refrigeration code (HVAC systems)
  - CSA B149.1 — Natural gas and propane installation code (if applicable to generator/heating)
- **CSI MasterFormat:** Specification organization standard
- **AEC document management standards:** ISO 19650 (BIM and information management) or equivalent (if applicable — TBD)

> **[SL:C-002]** Standards section expanded for integral regulatory coverage. Fire Hall + Public Works facilities require compliance with CSA standards (electrical, mechanical, accessibility) in addition to building and fire codes. Specific standards from RFP Appendix A (OSR) should be cited when available. *(SourcePath: Specification.md § Standards)*

*Source: ASSUMPTION based on project location (Alberta) and facility type (Fire Hall + Public Works); specific code references from RFP Appendix A — location TBD*

### Design-Build Best Practices (ASSUMPTION)
- **Design-Build Institute of America (DBIA) guidelines:** Document control and quality management best practices for Design-Build delivery

*Source: ASSUMPTION (industry standard for Design-Build projects); not explicitly required by RFP — assumption for credibility*

## Verification

### How Requirements Will Be Verified

> **[SL:C-004]** Verification methods standardized for repeatable process discipline. All requirements use consistent verification structure: (1) plan document review, (2) specific evidence artifact, (3) checklist criteria. *(SourcePath: Specification.md § Verification table)*

> **[SL:D-001]** Role transition clarification: During proposal phase, Proposal Manager verifies plan credibility for submission. Post-award, responsibility transitions to Design Manager for execution. Verification table reflects proposal phase roles; Procedure Part B defines post-award execution roles. *(SourcePath: Specification.md § Verification table vs. Procedure.md § Part B)*

| Requirement | Verification Method | Evidence Artifact | Responsible Party (Proposal Phase) | Timing |
|-------------|---------------------|-------------------|-----------------------------------|--------|
| RQ-01: Completeness | Plan document review | Completeness checklist template provided | Proposal Manager | Proposal phase |
| RQ-02: Coordination | Plan document review | Coordination process description with meeting frequency and tools specified | Proposal Manager | Proposal phase |
| RQ-03: QA/QC | Plan document review | QA/QC checkpoint table with layers, phases, and responsible parties | Proposal Manager | Proposal phase |
| RQ-04: Document Control | Plan document review | Numbering system, revision protocol, DMS specification documented | Proposal Manager | Proposal phase |
| RQ-05: Owner Review | Plan document review | Owner review process with specific review periods stated | Proposal Manager | Proposal phase |
| RQ-06: Discipline Scope | Plan document review | Discipline deliverable matrix by phase | Proposal Manager | Proposal phase |
| RQ-07: Code Compliance | Plan document review | Code compliance strategy with reviewer credentials identified | Proposal Manager | Proposal phase |
| RQ-08: Addenda Integration | Plan document review | Addenda integration checklist cross-mapping all Addendum 03 items | Proposal Manager | Proposal phase |
| RQ-09: Drawing/Spec Coordination | Plan document review | Drawing/specification coordination workflow documented | Proposal Manager | Proposal phase |
| RQ-10: Issuance Protocols | Plan document review | Issuance procedure with designations and distribution list | Proposal Manager | Proposal phase |

*Note: Post-award execution verification responsibilities transfer to Design Manager per Procedure Part B.*

*Source: Decomposition Section 8 (DEL-03-02 acceptance criteria), standard proposal evaluation practice (ASSUMPTION)*

### Acceptance Criteria (from _CONTEXT.md)
The plan document is acceptable when it:
- **Describes completeness:** Procedures for ensuring all required documents are produced
- **Describes coordination:** Methods for interdisciplinary integration and conflict resolution
- **Describes control:** Document numbering, revision tracking, distribution, and archival protocols

## Documentation

### Required Documentation for This Deliverable
- **Plan narrative document:** Written description of all processes, procedures, and responsibilities (the primary artifact of DEL-03-02)
- **Sample templates (optional but recommended):** Drawing index template, revision tracking template, QA/QC checklist templates, comment log template

*Source: _CONTEXT.md (anticipated artifacts), ASSUMPTION on templates as value-add for proposal credibility*

### Related Documentation (produced by other deliverables)
- **DEL-03-01 (Design Methodology Narrative):** Provides context for the overall design approach
- **DEL-08-01 (Detailed Project Schedule):** Provides timeline for document production milestones
- **DEL-09-01 (Risk Register):** Identifies risks affecting design documentation (e.g., permit delays, coordination challenges)
- **DEL-07-03 (Appendix I Subtrades List):** Identifies which disciplines/consultants are responsible for which scopes

*Source: Decomposition Section 8 (deliverable relationships)*

---

**Document Status:** DRAFT (Semantic Lensing Pass 3 complete — enrichment items incorporated)

**Semantic Lensing Items Incorporated:** A-001 (Owner review period directive), A-002 (addenda integration checklist), A-003 (third-party code review clarification), C-001 (mandatory DMS), C-002 (expanded standards), C-004 (verification consistency), D-001 (role transition clarity), F-001 (code proficiency confirmation), F-004 (landscape scope conflict)

**TBD Items for resolution:**
- Specific RFP Section 7.1.8 detailed requirements (document control, QA/QC, Owner review process)
- Owner review period durations (proposed 2-3 weeks subject to negotiation)
- Document retention period requirements
- Issuance format preferences (digital vs. hard copy, file formats)
- **Landscape discipline scope inclusion/exclusion (CONFLICT: requires decision)**
- BIM coordination software platform and protocols
- **Third-party code review: mandatory or optional (requires decision with credentials identification)**

**Assumptions flagged:**
- Design disciplines list and scope breakdown (landscape TBD)
- QA/QC checkpoint structure (internal, Design Manager, code review, constructability, Owner)
- Coordination tools (BIM, 2D overlays)
- Document control protocols (numbering, revision tracking, mandatory DMS)
- Typical review periods (2-3 weeks per milestone — must be stated in plan)
- Applicable codes and standards (ABC, NFC, CSA standards, CSI MasterFormat)
- DBIA best practices for Design-Build
