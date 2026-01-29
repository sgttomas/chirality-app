# Procedure: DEL-27.01 Design Basis Documents

## Purpose

This procedure defines the process for producing and managing **Design Basis Documents** within **PKG-27 Engineering Design**.

**Scope:** Documents analysis and results for design basis documents required for design verification and approvals (per _CONTEXT.md).

**Deliverable type:** Report (Design Basis Memorandum, Design Criteria)

**Responsible party:** D&B Contractor

**Downstream use:** The Design Basis Documents establish the technical foundation for all subsequent engineering design work across all disciplines. These documents are critical inputs for detailed engineering (packages PKG-01 through PKG-26, PKG-29 through PKG-36) and design verification (DEL-28.01).

**Cross-Document Links:**
- Datasheet.md: Deliverable identification, attributes, project context, references
- Specification.md: Requirements (FR, PR, IR, QR, RC) that this procedure verifies
- Guidance.md: Principles and rationale underlying procedural steps

**Source:** _CONTEXT.md; Decomposition DEL-27.01

## Prerequisites

### Dependencies

**Dependency coordination:**
- Per `_DEPENDENCIES.md`: **NOT_TRACKED** — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Key upstream dependencies (coordination required):**

| Dependency | Description | Specification § |
|------------|-------------|-----------------|
| Employer's Requirements (all volumes) | Must be available and reviewed before design basis development | FR-1, FR-2, FR-3 |
| Project objectives and success criteria | Established in project initiation documentation | FR-2 |
| Permit conditions and regulatory requirements | Obtained by Employer, provided to Contractor | RC-1, IR-2 |
| Site investigation data | Geotechnical, environmental, survey data as available | FR-3, RC-2 |

- **TBD** — Specific upstream deliverables to be confirmed per project schedule

**Key parallel dependencies (coordination required during development):**

| Dependency | Description | Specification § | Guidance § |
|------------|-------------|-----------------|------------|
| DEL-27.02 (HAZOP Study Reports) | Safety requirements and hazardous area classification | PR-4 | Principles §8 |
| DEL-27.03 (Phase 2 Expansion Documentation) | Phase 2 interface requirements | FR-4, IR-4 | Principles §7 |
| DEL-27.04 (Design Submission Packages) | Submission stage requirements and schedule | QR-3 | Considerations |
| All discipline engineering leads | Multi-discipline input required | FR-1, IR-1 | Principles §3 |

- **TBD** — Additional coordination requirements per project organization

**Source:** _DEPENDENCIES.md; **ASSUMPTION**: Typical Design & Build project dependencies

### Reference Materials

**Required reference materials:**

| Reference | Description | Status | Specification § |
|-----------|-------------|--------|-----------------|
| Employer's Requirements Vol 2 Pt 1 | General Requirements | **location TBD** | FR-1, FR-2, FR-3 |
| Employer's Requirements Vol 2 Pt 2 | Civil & Process Mechanical Works | **location TBD** | FR-3, RC-1, RC-2 |
| Employer's Requirements Vol 2 Pt 3 | Building Works | **location TBD** | FR-3 |
| NBC/NBCC | National Building Code of Canada (latest edition) | **location TBD** | RC-3, Standards |
| CSA standards | Discipline-specific | **location TBD** | RC-3, Standards |
| Project Quality Management Plan | Quality procedures | **location TBD** | QR-1 |
| Project document control procedures | Document management | **location TBD** | QR-1, QR-3 |
| Site geotechnical investigation reports | Site conditions | **location TBD** | FR-3 |
| Site environmental assessment reports | Environmental conditions | **location TBD** | RC-2 |
| Permit conditions | Regulatory requirements | **location TBD** | RC-1, IR-2 |
| Existing Terminal as-built documentation | Interface information | **location TBD** | IR-3 |

**Additional references as available:**
- Industry best practices and precedents for canola oil handling facilities
- Lessons learned from similar Design & Build projects
- Vendor technical data for major equipment (as available during design basis development)

**Source:** _REFERENCES.md; Datasheet.md; **ASSUMPTION**: Standard reference document suite for Design & Build

### Personnel Requirements

**Personnel qualifications:**

| Role | Qualification | Responsibilities | Specification § |
|------|---------------|------------------|-----------------|
| Design Basis Lead | P.Eng. with multi-discipline facility design and D&B experience | Overall coordination, integration, technical coherence | All requirements |
| Discipline leads | Qualified engineers in respective disciplines | Develop discipline-specific criteria, review interfaces | FR-1, IR-1 |
| Technical reviewers | Senior engineers or engineering managers | Review for technical adequacy, completeness, consistency | Verification |
| Document preparer | Technical writer or engineer | Compile inputs, maintain document control | QR-1, Documentation |

- **TBD** — Specific personnel assignments and qualifications matrix per project organization

**Source:** **ASSUMPTION**: Typical Design & Build personnel requirements and roles

### Tools and Resources

**Software and tools:**
- Document preparation: Word processing software (Microsoft Word or equivalent)
- Calculation tools: Excel, MathCAD, or discipline-specific software as needed
- Drawing/sketching tools: AutoCAD or equivalent for conceptual layouts
- Document management: Project document management system — **TBD**

**Templates and forms:**
- Design Basis Memorandum template — **TBD** (see Specification § Documentation)
- Design Criteria template — **TBD** (see Specification § Documentation)
- Calculation sheet template — **TBD**
- Document transmittal forms — **TBD**

**Source:** **ASSUMPTION**: Standard engineering tools and resources

## Steps

### Step 1: Initiation and Planning

**1.1 Review Project Requirements**

| Action | Output | Verification | Specification § | Guidance § |
|--------|--------|--------------|-----------------|------------|
| Review Employer's Requirements (all volumes) | Requirements summary and checklist | Design Basis Lead review | FR-1, FR-2, FR-3 | Principles §2 |
| Review contract documents for D&B obligations | Key project parameters list | Design Basis Lead review | Scope | Principles §1 |
| Identify applicable regulations, permits, approvals | Applicable codes and standards list (preliminary) | Design Basis Lead review | RC-1, RC-3 | Principles §4 |
| Review project schedule for milestones | Milestone schedule for design basis | Project Manager concurrence | QR-3 | Considerations |

**Source:** **ASSUMPTION**: Standard project initiation process

**1.2 Establish Design Basis Team**

| Action | Output | Verification | Specification § | Guidance § |
|--------|--------|--------------|-----------------|------------|
| Identify and assign discipline leads | Team organization chart | Project Manager approval | FR-1, IR-1 | Principles §3 |
| Confirm personnel qualifications | Qualifications matrix | Project Manager approval | All | — |
| Define roles, responsibilities, communication | RACI matrix | Design Basis Lead approval | — | Considerations |
| Establish meeting schedule | Coordination plan | Team concurrence | — | Considerations |

**Source:** **ASSUMPTION**: Standard team mobilization process

**1.3 Develop Design Basis Work Plan**

| Action | Output | Verification | Specification § | Guidance § |
|--------|--------|--------------|-----------------|------------|
| Define document structure and content | Document outline | Design Basis Lead approval | Documentation | Examples §4 |
| Assign discipline responsibilities | Section responsibility matrix | Discipline leads concurrence | FR-1 | Principles §3 |
| Establish review and approval workflow | Review workflow diagram | Project Manager concurrence | QR-1 | Considerations |
| Identify key decision points | Decision log (initial) | Design Basis Lead approval | — | Trade-offs |

**Source:** **ASSUMPTION**: Standard planning process for complex deliverable

### Step 2: Information Gathering and Analysis

**2.1 Compile Reference Information**

| Action | Output | Verification | Specification § | Guidance § |
|--------|--------|--------------|-----------------|------------|
| Gather all reference materials from Prerequisites | Organized reference library | Design Basis Lead review | All | — |
| Extract key requirements from Employer's Requirements | Requirements traceability matrix | Design Basis Lead review | FR-1, FR-2, FR-3 | Principles §2 |
| Review site investigation data | Site conditions summary | Discipline leads review | FR-3, RC-2 | Considerations |
| Identify missing references | TBD list | Design Basis Lead approval | — | — |

**Source:** **ASSUMPTION**: Standard information management process

**2.2 Conduct Multi-Discipline Coordination Workshops**

| Workshop Topic | Purpose | Participants | Specification § | Guidance § |
|----------------|---------|--------------|-----------------|------------|
| Overall design philosophy and approach | Establish foundation for design | All discipline leads | FR-1 | Principles §1, §5 |
| Performance requirements (throughput, storage, flexibility, reliability) | Define performance criteria | Process, mechanical, electrical leads | PR-1 through PR-4 | Examples §1 |
| Environmental and operating conditions | Define design loads | Structural, civil, mechanical leads | FR-3, RC-2, RC-3 | Examples §3 |
| Code and standard selection | Select applicable codes | All discipline leads | RC-3 | Principles §4; Trade-offs §3, §4 |
| Safety requirements and HAZOP coordination | Define safety criteria | Safety, process leads | PR-4 | Principles §8 |
| Phase 2 expansion provisions | Define Phase 2 interfaces | All discipline leads | FR-4, IR-4 | Principles §7; Trade-offs §2 |
| Material selections and specifications | Define material criteria | All discipline leads | FR-3 | Considerations |
| Interface requirements | Define discipline interfaces | All discipline leads | IR-1 through IR-4 | Considerations |

**Outputs:**
- Workshop meeting minutes documenting discussions, decisions, action items
- Preliminary design criteria by discipline
- Interface requirements matrix
- Key assumptions and TBD list

**Verification:** All discipline leads review and approve workshop outputs

**Cross-References:** Coordination with DEL-27.02 (HAZOP), DEL-27.03 (Phase 2)

**Source:** **ASSUMPTION**: Multi-discipline coordination workshop approach

**2.3 Perform Design Criteria Calculations**

| Calculation Type | Purpose | Output | Specification § | Guidance § |
|------------------|---------|--------|-----------------|------------|
| Load calculations (seismic, wind, snow) | Establish design loads | Design load summary | RC-3 | Examples §3 |
| Equipment sizing bases | Establish capacity requirements | Equipment sizing criteria | PR-1, PR-2 | Examples §1 |
| Hydraulic calculations | Establish piping criteria | Piping design criteria | PR-1, PR-3 | Examples §2 |
| Electrical load estimates | Establish power requirements | Electrical design criteria | FR-1 | Considerations |

**Verification:** Discipline leads review and approve calculations; checker signs off per quality procedures (Specification § QR-1)

**Source:** **ASSUMPTION**: Calculations support design criteria development

### Step 3: Design Basis Document Preparation

**3.1 Prepare Design Basis Memorandum (Draft 1)**

Compile Design Basis Memorandum per template and document outline from Step 1.3.

**Document sections (typical structure):**

| Section | Content | Source | Specification § | Guidance § |
|---------|---------|--------|-----------------|------------|
| Executive Summary | Overview of design basis and key decisions | Steps 2.2, 2.3 | Scope | Purpose |
| Project Overview and Scope | Facility description, scope boundaries | Decomposition, _CONTEXT.md | Scope | Purpose |
| Design Philosophy and Technical Approach | Design principles and approach | Step 2.2 (philosophy workshop) | FR-1 | Principles §1-9 |
| Key Technical Decisions and Rationale | Documented decisions with rationale | Step 2.2 (all workshops) | FR-2 | Trade-offs |
| Code and Standard Selection | Selected codes and editions | Step 2.2 (code workshop) | RC-3, Standards | Principles §4 |
| Interface Requirements | Internal and external interfaces | Step 2.2 (interface workshop) | IR-1 through IR-4 | Considerations |
| Phase 2 Expansion Considerations | Phase 2 provisions and interfaces | Step 2.2 (Phase 2 workshop) | FR-4, IR-4 | Principles §7 |
| Assumptions and Exclusions | Documented assumptions and exclusions | All steps | Scope | Considerations |
| Glossary and Definitions | Terminology definitions | Project standards | — | — |

**Content development guidance:**
- Focus on "what" and "why" rather than detailed "how" (see Guidance § Principles §1)
- Document key decisions with clear rationale traceable to requirements or engineering judgment
- Identify all assumptions explicitly; flag TBDs for items requiring further information
- Address all Project Objectives (OBJ-1 through OBJ-10) per Specification § FR-2
- Maintain traceability to Employer's Requirements

**Output:** Design Basis Memorandum Draft 1 (for internal review)

**Verification:** Design Basis Lead reviews for completeness and coherence

**Source:** **ASSUMPTION**: Typical Design Basis Memorandum structure per Guidance.md Examples §4

**3.2 Prepare Design Criteria (Draft 1)**

Compile Design Criteria document per template and document outline from Step 1.3.

**Document sections (typical structure):**

| Section | Content | Source | Specification § | Guidance § |
|---------|---------|--------|-----------------|------------|
| Introduction and Scope | Criteria document scope | _CONTEXT.md, Step 1.3 | Scope | Purpose |
| Performance Requirements | Throughput, storage, flexibility, reliability | Step 2.2 (performance workshop) | PR-1 through PR-4 | Examples §1 |
| Design Loads and Environmental Conditions | Seismic, wind, snow, temperature, etc. | Step 2.2, 2.3 | RC-3 | Examples §3 |
| Material Specifications and Standards | Material criteria | Step 2.2 (material workshop) | FR-3 | Considerations |
| Structural Design Criteria | Structural system criteria | Step 2.2, 2.3 | FR-1, RC-3 | Considerations |
| Mechanical and Process Design Criteria | Piping, equipment criteria | Step 2.2, 2.3 | FR-3, PR-1, PR-2 | Examples §1, §2 |
| Electrical and Controls Design Criteria | Power, controls criteria | Step 2.2 | FR-1 | Considerations |
| Safety and Fire Protection Criteria | Safety system criteria | Step 2.2 (safety workshop) | PR-4, RC-1 | Principles §8 |
| Quality Assurance Requirements | Quality criteria | Project QMP | QR-1 through QR-3 | Considerations |
| Code and Standard References | Code list with editions | Step 2.2 (code workshop) | RC-3, Standards | Principles §4 |

**Content development guidance:**
- Provide specific, quantitative criteria where possible (see Guidance § Principles §5)
- Flag TBDs for criteria requiring detailed design development or additional data
- Ensure consistency across disciplines (use consistent load cases, environmental conditions)
- Reference applicable code sections and standard clauses where appropriate
- Include basis/rationale for criteria selections, especially where engineering judgment applied

**Output:** Design Criteria Draft 1 (for internal review)

**Verification:** All discipline leads review respective sections; Design Basis Lead reviews for overall consistency

**Source:** **ASSUMPTION**: Typical Design Criteria structure per Guidance.md Examples §1, §2, §3

**3.3 Internal Technical Review**

Distribute Draft 1 documents to internal reviewers per Specification § Verification (VM-1, VM-2).

**Review checklist (minimum items):**

| Check Item | Specification § | Guidance § |
|------------|-----------------|------------|
| All Project Objectives addressed | FR-2 | Principles §2 |
| All Employer's Requirements considered | FR-1, FR-3 | Principles §1 |
| All applicable codes and standards identified | RC-3, Standards | Principles §4 |
| All disciplines covered with adequate criteria | FR-1 | Principles §3 |
| All interfaces identified and addressed | IR-1 through IR-4 | Considerations |
| Phase 2 provisions included per OBJ-8 | FR-4, IR-4 | Principles §7 |
| Assumptions and TBDs clearly flagged | — | — |
| Calculations supporting criteria documented | — | — |

**Outputs:**
- Review comments from technical reviewers
- Comment resolution log

**Verification:** Design Basis Lead compiles and addresses review comments; reviewers concur with resolutions

**Source:** **ASSUMPTION**: Standard technical review process per quality procedures (Specification § QR-1)

### Step 4: Revision and Finalization

**4.1 Incorporate Review Comments**

| Action | Output | Verification | Specification § |
|--------|--------|--------------|-----------------|
| Address all technical review comments | Revised documents | Design Basis Lead confirmation | QR-1 |
| Update assumptions, TBDs, calculations | Updated supporting materials | Discipline leads concurrence | FR-3 |
| Resolve conflicting comments | Resolution decisions | Project Manager escalation if needed | — |

**Outputs:**
- Design Basis Memorandum Draft 2 (incorporating review comments)
- Design Criteria Draft 2 (incorporating review comments)
- Updated comment resolution log

**Source:** **ASSUMPTION**: Standard comment resolution process

**4.2 Perform Cross-Document Consistency Check**

| Check Item | Documents Verified | Specification § | Guidance § |
|------------|-------------------|-----------------|------------|
| Technical approach aligns | Memorandum ↔ Criteria | FR-1 | Principles §1 |
| Key decisions reflected | Memorandum ↔ Criteria | FR-2 | Trade-offs |
| Assumptions consistent | All documents | — | — |
| Code references consistent | All documents | RC-3, Standards | Principles §4 |
| Interface requirements consistent | All documents | IR-1 through IR-4 | Considerations |
| Phase 2 provisions consistent | All documents | FR-4, IR-4 | Principles §7 |
| Consistency with DEL-27.02, DEL-27.03 | All documents | PR-4, FR-4, IR-4 | Principles §7, §8 |
| Consistency across Datasheet, Specification, Guidance, Procedure | All four documents | — | — |

**Outputs:**
- Consistency check report with any issues identified
- Revised documents correcting inconsistencies

**Verification:** Design Basis Lead reviews consistency check; approves final consistency

**Source:** 4_DOCUMENTS agent instructions (cross-document consistency requirement)

**4.3 Prepare Final Submission Package**

| Action | Output | Specification § | Guidance § |
|--------|--------|-----------------|------------|
| Format documents per project standards | Formatted documents | QR-1 | — |
| Add cover page, revision history, signature block | Complete documents | QR-1 | — |
| Compile supporting appendices | Appendix package | Documentation | — |
| Perform quality check | QA checklist completed | QR-1 | — |
| Generate PDF versions | PDF distribution copies | QR-3 | Considerations |

**Submission package contents:**
- Design Basis Memorandum (final revision for this submission stage)
- Design Criteria (final revision for this submission stage)
- Supporting appendices as applicable
- Transmittal letter/form per project procedures

**Output:** Final Design Basis Documents submission package (30%, 60%, 90%, or IFC stage)

**Verification:** Document preparer performs QA check; Design Basis Lead reviews final package

**Source:** **ASSUMPTION**: Standard document packaging; submission stages per Datasheet.md (Specification § QR-3)

### Step 5: Approval and Issuance

**5.1 Internal Approval**

Route final submission package through internal approval workflow per Specification § QR-1.

**Required signatures:**

| Approver | Role | Specification § |
|----------|------|-----------------|
| Design Basis Lead | Author/originator | All |
| Discipline leads | Discipline-specific approval | FR-1, IR-1 |
| Project Engineering Manager | Technical approval | All |
| Project Quality Manager | Quality approval | QR-1 |
| **TBD** | Additional approvals per project matrix | — |

**Output:** Internally approved Design Basis Documents with signature page

**Verification:** All required signatures obtained; approval logged in document management system

**Source:** **ASSUMPTION**: Standard internal approval workflow per ISO 9001 (Specification § QR-1)

**5.2 Submission to Employer**

Submit approved Design Basis Documents to Employer per DEL-27.04 requirements.

| Action | Output | Specification § | Guidance § |
|--------|--------|-----------------|------------|
| Prepare transmittal documenting submission stage | Transmittal form | QR-3 | Considerations |
| Coordinate submission timing | Scheduled submission | QR-3 | Considerations |
| Submit to Employer | Submitted documents | QR-3 | — |
| Place copies in `2_Checking/To/` folder | Filed copies | — | — |

**Output:** Design Basis Documents submitted to Employer

**Verification:** Project Manager confirms submission completed; submission logged in tracking system

**Cross-Reference:** DEL-27.04 (Design Submission Packages)

**Source:** Specification.md (QR-3); Datasheet.md (submission stages)

**5.3 Employer Review and Comment Resolution**

| Action | Output | Specification § | Guidance § |
|--------|--------|-----------------|------------|
| Receive Employer review comments | Comment log | Verification (VM-4) | Considerations |
| Triage comments (editorial, technical, contractual) | Categorized comments | — | — |
| Develop comment responses | Response matrix | — | Considerations |
| Revise documents to address comments | Revised documents | — | Considerations |
| Submit response matrix and revised documents | Updated submission | — | — |
| Iterate as needed for disputed comments | Final acceptance | Verification (VM-4) | — |

**Comment resolution process:**
- Assign comments to discipline leads for response
- Conduct internal coordination meeting to review responses and revisions
- Obtain Design Basis Lead and Project Manager approval of responses
- Submit responses to Employer; iterate as needed to achieve concurrence

**Outputs:**
- Comment response matrix
- Revised Design Basis Documents incorporating accepted comments
- **TBD** — Additional iterations if needed

**Verification:** Employer concurs with comment responses; revised documents accepted (Specification § Verification VM-4)

**Source:** **ASSUMPTION**: Standard design submission and review process; Guidance.md Considerations (Comment Resolution)

**5.4 Issuance**

| Action | Output | Specification § | Guidance § |
|--------|--------|-----------------|------------|
| Issue final Design Basis Documents | Issued documents | Documentation | — |
| Update `_STATUS.md` to ISSUED | Updated status file | — | — |
| Place issued documents in `3_Issued/` folder | Filed issued copies | Documentation | — |
| Distribute to all stakeholders | Distribution confirmation | Documentation | — |

**Output:** Issued Design Basis Documents available for detailed engineering use

**Verification:** All stakeholders acknowledge receipt

**Cross-Reference:** DEL-28.01 (receives issued Design Basis for independent verification)

**Source:** **ASSUMPTION**: Deliverable issuance per AGENTS.md and README.md lifecycle model

### Step 6: Configuration Management

**6.1 Change Control**

After initial issuance, any changes to Design Basis Documents shall follow project change control procedures (Specification § QR-1).

**Change triggers:**

| Trigger | Source | Specification § | Guidance § |
|---------|--------|-----------------|------------|
| Employer direction or revised requirements | Employer | FR-1, FR-2 | — |
| Detailed engineering findings | Discipline teams | FR-3 | — |
| HAZOP or design verification findings | DEL-27.02, DEL-28.01 | PR-4, QR-2 | Principles §8 |
| Regulatory or permit changes | Authorities | RC-1 | — |
| Value engineering opportunities | Design team | — | Trade-offs §1 |

**Change control process:**
- Initiate change request documenting proposed change, rationale, and impacts
- Assess impacts on downstream detailed engineering work
- Obtain approval per project change authority matrix
- Revise Design Basis Documents and reissue
- Notify all affected parties; ensure downstream design updates

**Outputs:**
- Change requests and approvals
- Revised and reissued Design Basis Documents (new revision)

**Verification:** Change control log updated; all affected parties notified

**Source:** **ASSUMPTION**: Configuration management for foundational design documents

**6.2 Lessons Learned Capture**

| Action | Output | Timing | Guidance § |
|--------|--------|--------|------------|
| Capture lessons learned from Design Basis development | Lessons learned report | At milestones or completion | Considerations §1, §2, §3 |
| Document what worked well and improvements | Documented lessons | At milestones or completion | — |
| Share with project team and organization | Knowledge sharing | At milestones or completion | — |

**Lessons learned topics (examples):**
- Effectiveness of multi-discipline coordination approach (see Step 2.2)
- Adequacy of reference information available at design basis stage
- Usefulness of design basis documents for detailed engineering teams
- Employer review and comment resolution effectiveness (see Step 5.3)
- Timeliness and quality of stakeholder engagement

**Verification:** Project Manager reviews lessons learned; incorporates into organizational knowledge base

**Source:** **ASSUMPTION**: Continuous improvement per ISO 9001 and best practice; Guidance.md Considerations

## Verification

### Verification Activities

| Verification ID | Activity | Requirements Verified | Acceptance Criteria | Guidance § |
|-----------------|----------|----------------------|---------------------|------------|
| V-1 | Requirements Traceability Verification | FR-1, FR-2, FR-3 | All Employer's Requirements addressed or noted N/A with justification | Principles §2 |
| V-2 | Multi-Discipline Consistency Verification | FR-1, IR-1 | No contradictory criteria; all interfaces defined and agreed | Principles §3 |
| V-3 | Code and Standard Compliance Verification | RC-3, Standards | Codes complete; editions appropriate; criteria meet or exceed minimums | Principles §4 |
| V-4 | Independent Design Verification (IDV) | All requirements | IDV completed per DEL-28.01; all findings addressed | Considerations |
| V-5 | Employer Review and Approval | All requirements | Employer comments resolved; approval obtained | Considerations |

**V-1: Requirements Traceability Verification**
- Verify all Employer's Requirements are addressed in Design Basis Documents
- Verify traceability from requirements to design criteria
- Use requirements traceability matrix from Step 2.1
- **Specification §:** FR-1, FR-2, FR-3
- **Guidance §:** Principles §2 (Objective-Driven Design)

**V-2: Multi-Discipline Consistency Verification**
- Verify consistency of criteria across disciplines
- Verify interface requirements are mutually compatible
- Conduct multi-discipline consistency review workshop if needed
- **Specification §:** FR-1, IR-1
- **Guidance §:** Principles §3 (Multi-Discipline Integration)

**V-3: Code and Standard Compliance Verification**
- Verify all applicable codes and standards are identified
- Verify code edition selections are appropriate and approved
- Verify design criteria are consistent with selected codes/standards
- **Specification §:** RC-3, Standards
- **Guidance §:** Principles §4 (Code and Standard Basis)

**V-4: Independent Design Verification (IDV)**
- Design Basis Documents undergo independent design verification per DEL-28.01
- IDV performed by qualified personnel independent of design team
- IDV findings are resolved and design basis revised as needed
- **Specification §:** QR-2, Verification (VM-3)
- **Guidance §:** Considerations (IDV)
- **Cross-Reference:** DEL-28.01

**V-5: Employer Review and Approval**
- Design Basis Documents submitted at 30%, 60%, 90%, IFC per DEL-27.04
- Employer review comments are addressed
- Employer approval obtained for each stage
- **Specification §:** QR-3, Verification (VM-4)
- **Guidance §:** Considerations (Design Submission, Comment Resolution)

### Sign-Off Requirements

**Internal Sign-Offs:**

| Role | Sign-Off Type | Procedure Step | Specification § |
|------|---------------|----------------|-----------------|
| Design Basis Lead | Technical originator | Step 5.1 | All |
| All discipline leads | Discipline-specific approval | Step 5.1 | FR-1, IR-1 |
| Design Basis technical reviewer | Senior engineer review | Step 3.3 | Verification |
| Project Engineering Manager | Overall technical approval | Step 5.1 | All |
| Project Quality Manager | Quality compliance | Step 5.1 | QR-1 |

**External Sign-Offs:**

| Party | Sign-Off Type | Procedure Step | Specification § |
|-------|---------------|----------------|-----------------|
| Employer | Approval at each submission stage | Step 5.3 | QR-3, Verification |
| Independent design verifier | IDV sign-off per DEL-28.01 | V-4 | QR-2 |
| Authority having jurisdiction | **TBD** if required | **TBD** | RC-1 |

**Source:** **ASSUMPTION**: Sign-off protocol per ISO 9001 (Specification § QR-1)

## Records

### Documentation Outputs

**Primary deliverable artifacts (per _CONTEXT.md):**

| Artifact | Description | Procedure Step | Specification § |
|----------|-------------|----------------|-----------------|
| Design Basis Memorandum | Design philosophy, key decisions, technical approach | Step 3.1 | Documentation |
| Design Criteria | Performance requirements, design parameters, codes/standards | Step 3.2 | Documentation |

**Supporting documentation:**

| Document | Purpose | Procedure Step | Specification § |
|----------|---------|----------------|-----------------|
| Requirements traceability matrix | Link requirements to criteria | Step 2.1 | FR-1, FR-2 |
| Design basis calculations | Support design criteria | Step 2.3 | FR-3 |
| Workshop minutes and decisions | Document coordination | Step 2.2 | IR-1 |
| Interface requirements matrix | Document interfaces | Step 2.2 | IR-1 through IR-4 |
| Comment response matrices | Track review comments | Steps 3.3, 5.3 | Verification |
| Approval documentation | Record approvals | Step 5.1 | QR-1 |
| Change control records | Track changes | Step 6.1 | QR-1 |

**Source:** _CONTEXT.md; Datasheet.md

### Record Management

**Filing and storage:**

| Location | Contents | Procedure Step |
|----------|----------|----------------|
| `1_Working/` | Working versions, drafts | Steps 3, 4 |
| `2_Checking/To/` | Submissions to Employer | Step 5.2 |
| `2_Checking/From/` | Received comments | Step 5.3 |
| `3_Issued/` | Issued versions with revision and date | Step 5.4 |
| Project DMS | Electronic copies per project procedures | All steps |

**Retention requirements:**
- Design Basis Documents: Retain for project lifecycle plus applicable regulatory period
- **TBD** — Specific retention per project record retention schedule

**Version control:**
- Use project document numbering system — **TBD**
- Revision history documented in document header/footer and revision history page
- Previous revisions archived but accessible

**Source:** **ASSUMPTION**: Document lifecycle per AGENTS.md and README.md

### Traceability and Auditability

**Traceability provisions:**

| Traceability Link | From | To | Method |
|-------------------|------|-----|--------|
| Requirements to criteria | Employer's Requirements | Design Basis criteria | Requirements traceability matrix |
| Review comments to revisions | Review comments | Document revisions | Comment response matrix |
| Changes to approvals | Change requests | Revised documents | Change control records |

**Audit trail:**
- Document revision history captures who, when, why for each revision
- Approval signatures and dates demonstrate review and approval
- Submission records demonstrate Employer review and acceptance
- IDV reports (DEL-28.01) demonstrate independent verification

**Source:** **ASSUMPTION**: Traceability per ISO 9001 (Specification § QR-1)

### Access and Distribution

**Access control:**

| Document Type | Access Level | Distribution |
|---------------|--------------|--------------|
| Issued Design Basis Documents | All project engineering personnel | Per distribution list |
| Working drafts, internal reviews | Design basis team and reviewers only | Restricted |

**Distribution:**
- Issued Design Basis Documents distributed to all discipline leads, project management, Employer, IDV (DEL-28.01)
- **TBD** — Specific distribution matrix per project

**Source:** **ASSUMPTION**: Access control and distribution per project document management procedures

---

**Document Status:** This Procedure document is part of the DEL-27.01 deliverable working set. See `_STATUS.md` for current deliverable lifecycle state.

**Cross-Document Verification (Pass 3):**
- All Steps linked to Specification § requirements being verified
- All Steps linked to Guidance § principles and considerations for rationale
- All Verification activities linked to Specification § requirements
- Terminology verified consistent with Datasheet.md, Specification.md, Guidance.md
- Project parameters verified consistent: 1,000,000 MT/annum, 45,000 MT storage, 32 railcar stations
- Cross-references to DEL-27.02, DEL-27.03, DEL-27.04, DEL-28.01 verified consistent across all documents

**Source:** **ASSUMPTION**: Procedure document is living document aligned with deliverable lifecycle per AGENTS.md
