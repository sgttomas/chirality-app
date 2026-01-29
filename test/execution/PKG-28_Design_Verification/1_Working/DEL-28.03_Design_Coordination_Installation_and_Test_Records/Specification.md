# Specification: DEL-28.03 Design Coordination Installation & Test Records

## Scope

This specification defines the requirements for **Design Coordination Installation & Test Records** within **PKG-28 Design Verification**.

**Purpose:** Provides evidence of completion, inspection, and testing for design coordination, supporting design quality, constructability, and **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements."

**Source:** _CONTEXT.md (DEL-28.03 description); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6; Section 6, Objective-to-Deliverable Mapping)

**Anticipated deliverable artifacts:**
- Inter-discipline coordination records
- Clash detection reports
- RFI logs

**Scope Inclusions:**
- Documentation of inter-discipline design coordination activities
- Coordination meeting minutes and action item tracking
- 3D model-based clash detection reports (if BIM is used)
- Request for Information (RFI) logs
- Interface registers documenting interface agreements
- Coordination issue logs

**Scope Exclusions:**
- Design work itself (performed under PKG-01 through PKG-36)
- Independent Design Verification (covered under DEL-28.01)
- VFPA IP Review coordination (covered under DEL-28.02)
- Construction coordination (separate from design coordination)
- Testing and commissioning records (covered under PKG-29)

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-28 scope)

## Requirements

### Functional Requirements

| Req ID | Requirement | Guidance § | Procedure Step | Verification |
|--------|-------------|------------|----------------|--------------|
| FR-1 | All coordination meetings shall be documented with minutes including date, attendees, agenda, decisions, and action items. | C-3, E-1 | Step 2.3 | V-1 |
| FR-2 | Regular coordination meetings shall be held (min: **TBD** frequency). Intensive meetings before each design submission. | P-2 | Step 2.1 | V-1 |
| FR-3 | If BIM used, regular clash detection shall be performed per BEP. Minimum: prior to each design submission (30%, 60%, 90%, IFC). | P-4, C-4, T-3 | Step 3 | V-1 |
| FR-4 | Clashes shall be classified (Critical/Major/Minor) and resolved. All Critical/Major clashes resolved before design submission. | C-7, T-5 | Step 3.3, Step 4.1 | V-3 |
| FR-5 | Formal RFI system shall track design questions with RFI number, originator, addressee, description, response, dates, status. | C-5, E-3 | Step 4.2 | V-1 |
| FR-6 | Key inter-discipline interfaces shall be documented in interface registers with criteria, responsibilities, and status. | C-6, E-4 | Step 4.3 | V-1 |
| FR-7 | Coordination issues shall be tracked in issue logs with priority, responsibility, target date, resolution, and status. | P-6, C-7 | Step 4.4 | V-3 |

**TBD Items:**
- FR-2: Coordination meeting frequency
- FR-3: BIM coordination requirements per BEP; interim clash detection frequency
- FR-4: Specific clash classification criteria
- FR-5: RFI response timeframe
- FR-6: Interface documentation format

**Source:** Datasheet.md (coordination methods, record types)

### Performance Requirements

| Req ID | Requirement | Guidance § | Procedure Step | Verification |
|--------|-------------|------------|----------------|--------------|
| PR-1 | 100% of coordination meetings documented. 100% of clash runs documented. 100% of RFIs logged. | — | Step 6 | V-1 |
| PR-2 | All critical clashes and critical issues resolved before design submission. RFIs responded within **TBD** days. | C-7, T-5 | Step 4, Step 5 | V-3 |
| PR-3 | Coordination meeting minutes issued within **TBD** days. Clash reports issued within **TBD** days. | — | Step 2.3, Step 3.4 | V-1 |

**TBD Items:**
- PR-2: RFI response timeframe; % of major items resolved
- PR-3: Meeting minutes issuance timeframe; clash report issuance timeframe

**Source:** Guidance.md (P-6, C-7)

### Interface Requirements

| Req ID | Requirement | Guidance § | Procedure Step | Verification |
|--------|-------------|------------|----------------|--------------|
| IR-1 | Coordination records interface with all discipline packages (PKG-01 through PKG-36). Coordination issues resolved through design document revisions. | P-3 | Step 4 | V-3 |
| IR-2 | Coordination supports design submissions (DEL-27.04). Intensive coordination before submissions; status reported for submission readiness. | P-2, C-8 | Step 5 | V-3 |
| IR-3 | Coordination coordinates with IDV (DEL-28.01). IDV may identify coordination issues. Records demonstrate coordination to reviewers. | — | — | V-1 |
| IR-4 | Coordination coordinates with VFPA IP Review (DEL-28.02). VFPA requirements addressed consistently across disciplines. | — | — | V-3 |
| IR-5 | If BIM used, coordination shall comply with BIM Execution Plan (BEP). | C-4 | Step 1.1, Step 3 | V-1 |
| IR-6 | Coordination process shall comply with project Quality Management Plan (QMP). | — | Step 1.1 | V-4 |

**Source:** Datasheet.md (Cross-Deliverable Coordination); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4)

### Quality Requirements

| Req ID | Requirement | Guidance § | Procedure Step | Verification |
|--------|-------------|------------|----------------|--------------|
| QR-1 | All coordination work shall comply with ISO 9001 Quality Management System requirements. | P-1 | Step 1.1 | V-4 |
| QR-2 | Coordination records shall be accurate, complete, clearly documented. Meeting minutes reviewed/approved prior to distribution. | P-5 | Step 2.3, Step 7.2 | V-2, V-4 |
| QR-3 | All coordination records shall be controlled per project document control procedures. | C-9 | Step 6, Step 7 | V-5 |
| QR-4 | Coordination records shall be retained per project requirements (**TBD** — 7-10 years post-project). | C-9 | Step 7.3 | V-5 |

**Source:** Datasheet.md (applicable standards: ISO 9001)

## Standards

**Applicable codes and standards (Design discipline):**

| Standard | Applicability | Status |
|----------|---------------|--------|
| ISO 9001 | Quality Management — quality records | Applicable |
| ISO 19650 | BIM standards | **TBD**: If BIM used |
| Project BIM Standards | BIM coordination protocols | **TBD** |
| Employer's Requirements | Coordination requirements | **TBD**: Specific ER sections |
| EGBC Practice Standards | Professional practice | Applicable |

**Source:** Datasheet.md (applicable standards); Guidance.md (applicable standards context)

## Verification

**Verification methods for Record deliverables:**

| Verification ID | Method | Acceptance Criteria | Procedure Step |
|-----------------|--------|---------------------|----------------|
| V-1 | Records completeness check | All meetings documented; all clash runs documented; RFI log complete | Step 7.2 |
| V-2 | Data accuracy verification | Records accurate and consistent with source data | Step 7.2 |
| V-3 | Coordination issue closure | Critical clashes/issues resolved; major items resolved or action plans in place | Step 5 |
| V-4 | Record approval verification | Required approvals obtained | Step 7.2 |
| V-5 | Archival format compliance | Records properly filed and retrievable | Step 7.3 |

**Sign-off Requirements:**

| Role | Sign-off | Requirement Ref |
|------|----------|-----------------|
| Meeting Chair / Coordination Lead | Meeting minutes approval | FR-1, QR-2 |
| BIM Coordinator (if BIM) | Clash detection report approval | FR-3 |
| RFI Coordinator | RFI log compilation approval | FR-5 |
| D&B Contractor QA/QC Manager | Final record package approval | QR-1, QR-2 |

**Source:** Guidance.md (P-5: Documentation and Traceability); Procedure.md (Verification section)

## Documentation

**Required documentation outputs:**

| Document Type | Naming Convention | Frequency | Procedure Step |
|---------------|-------------------|-----------|----------------|
| Coordination Meeting Minutes | COORD-MTG-[###] | Per meeting | Step 2.3, Step 6.1 |
| Clash Detection Reports | CLASH-REPORT-[Date]-[Stage] | Per clash run | Step 3.4, Step 6.3 |
| RFI Log | RFI-LOG-[Date/Rev] | Ongoing; snapshots at milestones | Step 4.2, Step 6.2 |
| Interface Registers | INT-REG-[###] | As needed | Step 4.3, Step 6 |
| Coordination Issue Logs | COORD-ISSUES-[Date/Rev] | Ongoing; snapshots at milestones | Step 4.4, Step 6.4 |

**Source:** _CONTEXT.md (anticipated artifacts); Datasheet.md (Construction: Detailed Record Types)

**Documentation requirements:**

**D-1: Coordination Meeting Minutes** — See Datasheet.md Construction; Procedure.md Step 2.3
- Document naming: Sequential numbering (COORD-MTG-001, etc.)
- Format: PDF for issued; editable for drafts
- Distribution: Attendees, project management, discipline leads

**D-2: Clash Detection Reports** — See Datasheet.md Construction; Procedure.md Step 3.4
- Report naming: By date and stage (CLASH-REPORT-2026-01-15-60PCT)
- Format: PDF export from BIM software
- Distribution: Discipline leads, BIM coordinator, project management

**D-3: RFI Log** — See Datasheet.md Construction; Procedure.md Step 4.2
- Format: Spreadsheet or database maintained in real-time
- Export: PDF snapshots at design milestones
- Distribution: Project team access to live log; PDF exports with submissions

**D-4: Interface Registers** — See Datasheet.md Construction; Procedure.md Step 4.3
- Format: Spreadsheet or database
- Export: PDF for design milestones
- Distribution: Affected disciplines, project management

**D-5: Coordination Issue Logs** — See Datasheet.md Construction; Procedure.md Step 4.4
- Format: Spreadsheet or database maintained in real-time
- Export: PDF snapshots at milestones
- Distribution: Project team; summaries to management

**D-6: Document Control**
- Document numbering: **TBD** — Per project system
- Revision control: **TBD** — Version tracking for living documents; revision for issued documents

**D-7: Record Management**
- Working documents: `1_Working/DEL-28.03.../`
- Living documents: Working folder with milestone exports
- Final package: `3_Issued/` at project completion
- Retention: Per QR-4

**D-8: Submittal to Employer**
- **TBD**: Employer requirements for coordination records
- Typical: Status summaries with submissions; detailed records upon request

## Cross-Document Traceability Matrix

| Specification Requirement | Datasheet Section | Guidance Section | Procedure Step |
|---------------------------|-------------------|------------------|----------------|
| FR-1 (Meeting Documentation) | Construction (Meeting Minutes) | C-3, E-1 | Step 2.3 |
| FR-2 (Meeting Frequency) | Attributes (Coordination Frequency) | P-2, C-3 | Step 2.1 |
| FR-3 (Clash Detection) | Attributes (BIM/3D Coordination), Construction (Clash Reports) | P-4, C-4, T-3 | Step 3 |
| FR-4 (Clash Classification) | Construction (Clash Reports) | C-7, T-5 | Step 3.3, Step 4.1 |
| FR-5 (RFI System) | Construction (RFI Logs) | C-5, E-3 | Step 4.2 |
| FR-6 (Interface Documentation) | Construction (Interface Registers) | C-6, E-4 | Step 4.3 |
| FR-7 (Issue Tracking) | Construction (Issue Logs) | P-6, C-7 | Step 4.4 |
| PR-1 (Completeness) | — | — | Step 6 |
| PR-2 (Issue Resolution) | — | C-7, T-5 | Step 4, Step 5 |
| PR-3 (Timeliness) | — | — | Step 2.3, Step 3.4 |
| IR-1 (Discipline Packages) | Cross-Deliverable Coordination, Conditions | P-3 | Step 4 |
| IR-2 (Design Submissions) | Attributes (Coordination Phases), Cross-Deliverable Coordination | P-2, C-8 | Step 5 |
| IR-3 (IDV Coordination) | Cross-Deliverable Coordination | — | — |
| IR-4 (VFPA Coordination) | Cross-Deliverable Coordination | — | — |
| IR-5 (BIM Execution Plan) | Attributes (BIM/3D Coordination), References | C-4 | Step 1.1, Step 3 |
| IR-6 (QMS) | References | — | Step 1.1 |
| QR-1 (ISO 9001) | References | P-1 | Step 1.1 |
| QR-2 (Record Quality) | — | P-5, C-9 | Step 2.3, Step 7.2 |
| QR-3 (Document Control) | Attributes (Classification) | C-9 | Step 6, Step 7 |
| QR-4 (Retention) | Attributes (Retention Period) | C-9 | Step 7.3 |

**Source:** Cross-document consistency verification per AGENT_4_DOCUMENTS_REVISED_v3.md (Step 5)
