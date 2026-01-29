# Specification: DEL-27.02 HAZOP Study Reports

## Scope

This specification defines the requirements for **HAZOP Study Reports** within **PKG-27 Engineering Design**.

**Purpose:** Documents analysis and results for HAZOP study reports required for design verification and approvals (per _CONTEXT.md).

**Anticipated deliverable artifacts:**
- HAZOP Study Reports (comprehensive documentation of HAZ

OP study process, findings, and recommendations)

**Scope Boundaries:**

**Included:**
- Hazard and Operability (HAZOP) studies for all major process systems in Phase 1 canola oil transload facility
- Identification of hazards and operability issues using structured HAZOP methodology
- Hazardous area classification determination based on HAZOP findings
- Risk assessment (likelihood × consequence) for identified scenarios
- Recommendations for risk reduction measures (engineering controls, administrative controls, safeguards)
- Action item tracking and closure verification
- Hazardous area classification drawings or documentation

**Excluded:**
- Detailed engineering design of safeguards (covered in respective discipline package deliverables)
- Quantitative risk assessment (QRA) unless specifically required by Employer or regulations — **TBD**
- Layer of Protection Analysis (LOPA) unless specifically required — **TBD**
- Safety Instrumented System (SIS) detailed design (SIS requirements identified by HAZOP; SIS design in PKG-19)
- Emergency response planning and procedures (separate deliverables) — **TBD**
- Construction safety hazards (covered by construction HSE planning)

**Source:** _CONTEXT.md; Decomposition DEL-27.02 entry; **ASSUMPTION**: Standard HAZOP scope for process facility

## Requirements

### Functional Requirements

**FR-1: HAZOP Study Execution**
- HAZOP studies shall be conducted for all major process systems identified in Datasheet.md (Railcar Unloading, Storage Tanks, Transfer Piping, Marine Loading, Pumps, Valves, Electrical, Controls, Safety Systems)
- HAZOP shall use structured methodology per IEC 61882 or equivalent recognized standard
- HAZOP shall identify deviations from design intent, causes, consequences, existing safeguards, and recommendations
- **Source:** Datasheet.md; **ASSUMPTION**: IEC 61882 methodology; **TBD** — Employer-specific HAZOP requirements

**FR-2: Multi-Discipline Participation**
- HAZOP team shall include qualified personnel representing all relevant disciplines: process, mechanical, electrical, controls, safety, operations
- HAZOP facilitator shall be experienced and independent (not the primary designer)
- HAZOP team composition and qualifications shall be documented
- **TBD** — Specific qualifications and independence requirements from Employer or quality procedures
- **Source:** **ASSUMPTION**: Standard HAZOP team composition per IEC 61882 and industry practice

**FR-3: Design Basis Alignment**
- HAZOP shall be based on design basis established in DEL-27.01 (Design Basis Documents)
- HAZOP shall review P&IDs, PFDs, equipment datasheets, and operating philosophy
- Any deviations from design basis identified during HAZOP shall be documented and resolved (update design basis or justify deviation)
- **Source:** Datasheet.md; **ASSUMPTION**: Coordination with DEL-27.01

**FR-4: Hazardous Area Classification**
- HAZOP study shall identify all potential sources of hazardous atmosphere release
- Hazardous area classification shall be determined per Canadian Electrical Code (CEC) and/or API RP 505/IEC 60079 series
- Hazardous area classification shall inform electrical equipment selection and installation (PKG-17)
- Hazardous area classification drawings or documentation shall be produced
- **Source:** Datasheet.md; **ASSUMPTION**: Coordination with PKG-17 (Electrical Power Distribution)

**FR-5: Risk Ranking and Prioritization**
- All identified hazard scenarios shall be risk-ranked using likelihood × consequence matrix
- Risk ranking criteria shall be defined (e.g., 3×3 or 5×5 matrix) and documented
- High-risk scenarios shall be prioritized for risk reduction recommendations
- Residual risk after implementation of recommendations shall be assessed and documented
- **TBD** — Specific risk ranking criteria and acceptable risk levels from Employer or regulations
- **Source:** **ASSUMPTION**: Risk-based HAZOP approach per ISO 31000 and industry practice

**FR-6: Recommendation Development and Tracking**
- HAZOP shall generate recommendations for risk reduction for unacceptable or high-risk scenarios
- Recommendations shall be specific, actionable, and assigned to responsible parties with target completion dates
- Recommendations shall be tracked through design, construction, and commissioning phases
- Action item register shall be maintained and updated as recommendations are implemented and closed
- Follow-up HAZOP review shall verify closure of action items before facility startup
- **Source:** **ASSUMPTION**: Closed-loop HAZOP action item process per industry best practice

### Performance Requirements

**PR-1: Safety Performance (OBJ-1)**
- HAZOP shall support achievement of safe and reliable operation per OBJ-1
- HAZOP shall identify all credible hazard scenarios that could result in:
  - Personnel injury or fatality
  - Fire or explosion
  - Release of hazardous materials to environment
  - Major equipment damage or facility disruption
  - Loss of product containment
- **TBD** — Specific safety performance targets or risk tolerance criteria from Employer
- **Source:** Decomposition Section 2 (OBJ-1); **ASSUMPTION**: Comprehensive hazard identification for all consequence categories

**PR-2: Operability Assurance (OBJ-2, OBJ-4)**
- HAZOP shall identify operability issues that could prevent achievement of throughput capacity (OBJ-2) or operational flexibility (OBJ-4)
- Operability deviations shall be analyzed for impact on facility performance and availability
- Recommendations shall address both safety hazards and operability issues
- **Source:** Decomposition Section 2 (OBJ-2, OBJ-4)

**PR-3: Environmental Protection (OBJ-7)**
- HAZOP shall identify scenarios that could result in spills, releases, or environmental impacts
- Environmental consequences shall be assessed (soil contamination, water pollution, air emissions)
- Recommendations shall address environmental protection measures (containment, spill response, emissions control)
- **Source:** Decomposition Section 2 (OBJ-7)

**PR-4: Regulatory Compliance (OBJ-6)**
- HAZOP process and results shall support compliance with all applicable regulations, permits, and authority requirements (OBJ-6)
- HAZOP shall identify regulatory compliance gaps and recommend measures to achieve compliance
- **TBD** — Specific regulatory requirements for HAZOP from BC, federal, or municipal authorities
- **Source:** Decomposition Section 2 (OBJ-6); **ASSUMPTION**: HAZOP supports regulatory compliance demonstration

### Interface Requirements

**IR-1: Design Basis Interface (DEL-27.01)**
- HAZOP shall use Design Basis Documents (DEL-27.01) as foundation for process understanding and design intent
- HAZOP findings may trigger updates to design basis if fundamental assumptions or design philosophy need revision
- **TBD** — Coordination mechanism between HAZOP team and design basis authors
- **Source:** Datasheet.md; **ASSUMPTION**: Bidirectional interface between HAZOP and design basis

**IR-2: Detailed Engineering Interface (PKG-10 through PKG-26)**
- HAZOP recommendations shall be incorporated into detailed engineering deliverables for respective disciplines
- Engineering teams shall provide feedback to HAZOP team on feasibility and implementation of recommendations
- Design changes resulting from HAZOP recommendations shall be tracked and verified
- **Source:** **ASSUMPTION**: HAZOP recommendations flow down to all applicable discipline deliverables; see `_DEPENDENCIES.md` (NOT_TRACKED)

**IR-3: Control System and SIS Interface (PKG-19)**
- HAZOP shall identify Safety Instrumented Functions (SIFs) and Safety Integrity Level (SIL) requirements
- HAZOP findings inform control system design: interlocks, alarms, emergency shutdown (ESD) logic
- Control system design shall implement HAZOP-identified safeguards; SIS design per IEC 61508/61511 or equivalent
- **TBD** — SIL determination methodology and criteria
- **Source:** **ASSUMPTION**: HAZOP identifies SIS needs; PKG-19 deliverables implement SIS design

**IR-4: Electrical Hazardous Area Interface (PKG-17)**
- HAZOP-determined hazardous area classification informs electrical equipment selection (motor enclosures, wiring methods, etc.)
- Electrical design shall comply with hazardous area classification requirements per CEC Section 18
- **Source:** Datasheet.md; **ASSUMPTION**: Coordination with PKG-17

**IR-5: Fire Protection and Safety Systems Interface (PKG-23, PKG-24)**
- HAZOP fire and explosion scenarios inform fire protection system design
- HAZOP gas/vapor release scenarios inform gas detection system requirements (if applicable)
- Safety system design shall address HAZOP-identified scenarios
- **Source:** **ASSUMPTION**: Coordination with PKG-23, PKG-24

**IR-6: Operations and Maintenance Interface**
- HAZOP shall consider operations and maintenance activities (startup, shutdown, maintenance, abnormal conditions)
- HAZOP recommendations may include operational procedures, training requirements, or administrative controls
- Operating procedures and training shall reflect HAZOP findings
- **TBD** — Operations and maintenance deliverable references
- **Source:** **ASSUMPTION**: HAZOP considers full lifecycle operating modes

**IR-7: Independent Design Verification Interface (DEL-28.01)**
- HAZOP study process and results may be reviewed by independent design verifier (IDV) per DEL-28.01
- IDV may assess HAZOP adequacy, team qualifications, methodology rigor, recommendation appropriateness
- **TBD** — Specific IDV requirements for HAZOP review
- **Source:** **ASSUMPTION**: Coordination with DEL-28.01

### Quality Requirements

**QR-1: HAZOP Methodology Quality**
- HAZOP shall follow recognized methodology: IEC 61882, CCPS Guidelines, or equivalent
- HAZOP guidewords shall be systematically applied to all nodes: More, Less, No, Reverse, As Well As, Part Of, Other Than, etc.
- HAZOP worksheets shall be complete and traceable: node description, deviations, causes, consequences, safeguards, risk ranking, recommendations
- HAZOP facilitator and team qualifications shall meet industry standards — **TBD**
- **Source:** Datasheet.md; **ASSUMPTION**: IEC 61882 or equivalent methodology

**QR-2: Documentation Quality**
- HAZOP reports shall be comprehensive, clear, and suitable for use by engineering, operations, and regulatory audiences
- HAZOP worksheets shall be legible, complete, and properly cross-referenced
- All assumptions, limitations, and TBDs shall be clearly identified
- Report format and structure per Datasheet.md or project template — **TBD**
- **Source:** Datasheet.md; **ASSUMPTION**: Standard HAZOP documentation quality per ISO 9001 and industry practice

**QR-3: Review and Approval**
- HAZOP reports shall undergo technical review by HAZOP team leader and discipline leads
- HAZOP reports shall be approved by Project Engineering Manager and submitted to Employer for acceptance
- HAZOP action items shall be reviewed and approved before closure
- **TBD** — Specific approval workflow and sign-off requirements per project quality procedures
- **Source:** **ASSUMPTION**: Standard engineering review and approval per ISO 9001

**QR-4: Revision and Configuration Management**
- HAZOP studies shall be updated as design evolves through submission stages (30%, 60%, 90%, IFC per DEL-27.04)
- Preliminary HAZOP (30-60% stage) establishes initial hazard understanding; Detailed HAZOP (90% stage) provides comprehensive final analysis
- Pre-commissioning HAZOP review verifies action item closure and as-built alignment
- Revision history and change control per project document management procedures
- **Source:** Datasheet.md; **ASSUMPTION**: Multi-stage HAZOP approach aligned with design maturity

### Regulatory and Code Compliance

**RC-1: Canadian Regulatory Compliance**
- HAZOP process and results shall support compliance with all applicable BC, federal, and municipal regulations
- **TBD** — Specific regulations requiring HAZOP or equivalent hazard analysis (e.g., provincial occupational health and safety regulations, environmental regulations, port authority requirements)
- **Source:** Decomposition Section 2 (OBJ-6); **ASSUMPTION**: HAZOP supports regulatory compliance

**RC-2: Employer Requirements Compliance**
- HAZOP shall comply with Employer's Requirements for hazard analysis, safety studies, and design verification
- **TBD** — Specific Employer's Requirements for HAZOP methodology, documentation, review, and acceptance
- **Source:** Decomposition Section 3 (Reference Documents); **ASSUMPTION**: Employer's Requirements specify HAZOP requirements

**RC-3: Code and Standard Application**
- HAZOP methodology per IEC 61882 or equivalent recognized standard
- Hazardous area classification per CEC Part I Section 18, API RP 505, IEC 60079 series, or equivalent
- Risk management per ISO 31000 or equivalent
- **TBD** — Specific code editions and applicability
- **Source:** Datasheet.md; **ASSUMPTION**: Canadian and international standards apply

## Standards

**Applicable codes and standards:**

**HAZOP Methodology:**
- IEC 61882: Hazard and operability studies (HAZOP studies) — Application guide — **location TBD**
- CCPS (Center for Chemical Process Safety) Guidelines for Hazard Evaluation Procedures (3rd Edition, 2008 or later) — **location TBD**
- **TBD** — Project-specific HAZOP procedure or standard

**Hazardous Area Classification:**
- Canadian Electrical Code (CEC) Part I, Section 18: Hazardous locations — latest edition — **location TBD**
- API RP 505: Recommended Practice for Classification of Locations for Electrical Installations at Petroleum Facilities Classified as Class I, Zone 0, Zone 1, and Zone 2 — latest edition — **location TBD**
- IEC 60079 series: Explosive atmospheres — **location TBD**
- NFPA 497: Recommended Practice for the Classification of Flammable Liquids, Gases, or Vapors and of Hazardous (Classified) Locations for Electrical Installations in Chemical Process Areas — **location TBD**

**Safety and Risk Management:**
- ISO 31000: Risk management — Guidelines — latest edition — **location TBD**
- IEC 61508: Functional safety of electrical/electronic/programmable electronic safety-related systems — **location TBD** (if SIL determination required)
- IEC 61511: Functional safety — Safety instrumented systems for the process industry sector — **location TBD** (if SIS design required)

**Process Safety:**
- **TBD** — Applicable CSA or other Canadian process safety standards
- CCPS process safety guidelines — **location TBD**

**General:**
- ISO 9001: Quality Management Systems (documentation and quality requirements)
- Employer's Requirements (project-specific requirements) — **location TBD**

**Source:** Datasheet.md; **ASSUMPTION**: Standard codes and standards for HAZOP and hazardous area classification; **location TBD** for all standards

## Verification

**Verification methods for HAZOP Study Reports:**

**VM-1: Methodology Verification**
- Verify HAZOP methodology follows IEC 61882 or equivalent recognized standard
- Verify HAZOP guidewords systematically applied to all nodes
- Verify all major systems in scope are analyzed (per Datasheet.md system list)
- Verify HAZOP team composition includes all required disciplines and expertise

**Acceptance criteria:**
- HAZOP methodology documented and compliant with IEC 61882 or equivalent
- All guidewords applied to all nodes (completeness check)
- All systems in Datasheet.md covered by HAZOP nodes
- HAZOP team qualifications documented and adequate

**VM-2: Technical Content Verification**
- Verify P&IDs and design basis documents used in HAZOP are current and correct
- Verify identified deviations, causes, and consequences are technically sound
- Verify existing safeguards are correctly identified
- Verify risk rankings are consistent with defined risk matrix criteria
- Verify recommendations are specific, actionable, and technically feasible

**Acceptance criteria:**
- Reference documents are latest approved versions
- Technical content reviewed by discipline leads and found to be accurate
- Risk rankings are consistent and justified
- Recommendations are clear and implementable

**VM-3: Completeness Verification**
- Verify all nodes defined in HAZOP scope are analyzed
- Verify all guidewords applied (or justification provided if guideword not applicable)
- Verify all credible deviations are identified (no obvious gaps)
- Verify all high-risk scenarios have recommendations for risk reduction

**Acceptance criteria:**
- HAZOP coverage is complete per defined scope
- No significant hazard scenarios omitted
- All high-risk scenarios addressed with recommendations

**VM-4: Hazardous Area Classification Verification**
- Verify hazardous area classification methodology follows CEC, API RP 505, IEC 60079, or equivalent
- Verify all potential release sources identified
- Verify zone/division classifications are appropriate for identified release scenarios
- Verify hazardous area classification drawings are complete and consistent with HAZOP findings

**Acceptance criteria:**
- Hazardous area classification methodology documented and compliant with applicable standard
- All release sources from HAZOP analysis included in classification
- Hazardous area classification drawings complete and approved

**VM-5: Action Item Tracking Verification**
- Verify all recommendations are captured in action item register
- Verify action items have assigned responsibility and target dates
- Verify action item status is tracked and updated
- Verify completed action items have closure evidence

**Acceptance criteria:**
- All HAZOP recommendations are in action item register
- Action items are assigned and scheduled
- Action item register is current and maintained

**VM-6: Independent Design Verification (IDV)**
- HAZOP study process and results may undergo independent design verification per DEL-28.01
- IDV may include review of: HAZOP team qualifications, methodology rigor, P&ID accuracy, technical content, recommendation adequacy
- **TBD** — Specific IDV requirements for HAZOP review
- **Source:** **ASSUMPTION**: Coordination with DEL-28.01

**VM-7: Employer Review and Acceptance**
- HAZOP reports shall be submitted to Employer at appropriate design stages (per DEL-27.04)
- Employer review comments shall be addressed
- Employer acceptance obtained before proceeding to next design stage or construction

**Acceptance criteria:**
- Employer comments satisfactorily resolved
- Employer approval or acceptance issued

**Source for Verification section:** **ASSUMPTION**: Standard HAZOP verification approach per IEC 61882, ISO 9001, and industry best practice

## Documentation

**Required documentation outputs:**

Per _CONTEXT.md and Decomposition DEL-27.02:
- **HAZOP Study Reports** (comprehensive documentation per Datasheet.md report structure)

**Documentation structure and content:**

Per Datasheet.md, HAZOP Report typically includes:
1. Executive Summary
2. Introduction (project overview, methodology, objectives)
3. Study Organization (team, schedule, node definitions)
4. Design Basis Review (process description, P&IDs, operating philosophy, reference to DEL-27.01)
5. HAZOP Worksheets (node-by-node analysis with deviations, causes, consequences, safeguards, risk ranking, recommendations)
6. Hazardous Area Classification (methodology, source identification, zone classification, drawings)
7. Recommendations Summary (tabulated with priority, responsibility, target dates)
8. Action Item Tracking (register with status and closure)
9. Appendices (team qualifications, P&IDs, guideword definitions, risk matrix, references)

**Documentation requirements:**

- **Format:** **TBD** — PDF and native format per project document standards; may include Excel spreadsheets for HAZOP worksheets and action item register
- **Revision control:** Per project document numbering system — **TBD**
- **Submission stages:** **TBD** — Preliminary HAZOP at 30-60% design stage; Detailed HAZOP at 90% stage; Pre-commissioning HAZOP review before startup (align with DEL-27.04)
- **Document management:** Per project document control procedures
- **Distribution:** Engineering teams, operations, safety, Employer, IDV, regulatory authorities (as required) — **TBD**
- **Retention:** Long-term retention as critical safety document — **TBD** per regulatory and project requirements

**Supporting documentation:**

- P&IDs (marked-up with HAZOP node boundaries)
- Hazardous area classification drawings (may be standalone deliverable or appendix to HAZOP report)
- Action item register (living document maintained throughout project)
- HAZOP team attendance sheets and meeting minutes
- Follow-up HAZOP review reports (action item closure verification)

**Filing locations:**
- Working versions: `1_Working/` in deliverable folder (DEL-27.02_HAZOP_Study_Reports/)
- Review versions: `2_Checking/To/` for submissions; `2_Checking/From/` for received comments
- Issued versions: `3_Issued/` with revision and date in filename

**Source:** _CONTEXT.md; Datasheet.md; **ASSUMPTION**: Standard HAZOP documentation per IEC 61882 and project document lifecycle per AGENTS.md

---

**Cross-Document Verification (Pass 3):**
- All requirements linked to Guidance § for rationale and Procedure Step for implementation
- Datasheet.md: HAZOP scope systems (PKG-10 through PKG-24), hazardous area classification, report structure
- Guidance.md: Principles §1-11, Considerations, Trade-offs, Examples §1-4
- Procedure.md: Steps 1-6 for conducting HAZOP studies
- Terminology verified consistent with Datasheet.md, Guidance.md, Procedure.md
- Project parameters verified consistent: 1,000,000 MT/annum (OBJ-2), 45,000 MT storage (OBJ-3), 32 railcar stations
- Cross-references to DEL-27.01, DEL-27.04, DEL-28.01, PKG-10 through PKG-26 verified consistent across all documents
- HAZOP methodology (IEC 61882) and hazardous area standards (CEC, API RP 505, IEC 60079) verified consistent
