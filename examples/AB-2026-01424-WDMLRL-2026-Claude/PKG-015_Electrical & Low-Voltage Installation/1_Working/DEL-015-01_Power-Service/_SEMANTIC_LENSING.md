# Semantic Lensing Register: DEL-015-01 Three-Phase Power Service

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-015_Electrical & Low-Voltage Installation/1_Working/DEL-015-01_Power-Service
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-015-01_Power-Service/_CONTEXT.md (Deliverable Overview, Scope of Work, Technical Context)
- _STATUS.md — DEL-015-01_Power-Service/_STATUS.md (Current Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-015-01_Power-Service/_SEMANTIC.md (Matrices A, B, C, F, D, X, E fully parsed)
- Datasheet.md — DEL-015-01_Power-Service/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-015-01_Power-Service/Specification.md (Scope, Requirements REQ-015-01-001 through -012, Standards, Verification, Documentation)
- Guidance.md — DEL-015-01_Power-Service/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-015-01_Power-Service/Procedure.md (Prerequisites, Steps Phases 1-4, Verification, Records)
- _REFERENCES.md — DEL-015-01_Power-Service/_REFERENCES.md (Primary References, SOW Documentation, Objective References, Related Deliverables)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 7
  - Specification: 10
  - Guidance: 4
  - Procedure: 4
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 6  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Service voltage prescriptive gap |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Code edition not identified |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Inspection pass criteria weak |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Audit trail adequately covered across Procedure and Specification |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Utility lead-time procedure gap |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps cover practical execution adequately |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables in Specification and Procedure cover performance assessment |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section in Procedure provides audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Spare capacity rationale incomplete |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Guidance conflict table covers value rulings |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification approach covers quality checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Which authority (RFP, utility, or design engineer) ultimately prescribes the service voltage? Add explicit authority chain for voltage selection in REQ-015-01-002. | REQ-015-01-002 defers to IFC drawings but does not state the prescriptive hierarchy (utility constraints vs. Owner preference vs. engineer judgment). Under the "prescriptive direction" lens this is an unresolved authority gap. | Specification.md | REQ-015-01-002 -- Service Voltage | | PKG-004 design engineer per Guidance CON-015-01-001 | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify which edition of CSA C22.1 and Alberta Building Code applies. Current text says "ASSUMPTION: applicable" without confirming edition. | Under "mandatory practice," the specific edition of the governing code must be identified to determine which mandatory practices apply. The Standards table lists codes without edition references. | Specification.md | Standards table | | PKG-004 design package or Alberta Safety Codes authority | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add measurable pass/fail criteria for ground resistance testing in Verification table (REQ-015-01-008 row). Currently states "ground continuity and resistance testing TBD per code." | Under "compliance determination," the verification approach for grounding lacks a quantitative acceptance threshold. Inspection sign-off alone is noted but the technical test criterion is TBD. | Specification.md | Verification table, REQ-015-01-008 row | | CSA C22.1 (applicable section on grounding) | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add a step or note in Phase 1 for documenting utility lead-time estimate and incorporating it into project schedule with milestone dates. | Under "procedural direction," Step 1.1 directs the contractor to confirm utility availability and lead time, but there is no explicit step to record the lead-time estimate and feed it back into the project schedule as a constraint. | Procedure.md | Phase 1 -- Design Coordination, Step 1.1 | | Proponent project manager | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale for why spare capacity is recommended and what "20-25% spare" is based on (industry practice, Owner direction, or assumption). | Under "value orientation," the Trade-offs table recommends 20-25% spare capacity but provides no justification basis. The recommendation is flagged as ASSUMPTION without explaining the value proposition or risk of not including it. | Guidance.md | Trade-offs table, row "Service capacity margin" | | Owner (Camrose County) and design engineer | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Service ampacity not established |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Load schedule approximate |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing downstream deliverable load data |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement references are consistently sourced to App B-Elec |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Utility provider identity unknown |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for each attribute is adequately sourced |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents provide comprehensive narrative of scope |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging is coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Documents demonstrate adequate understanding of electrical service fundamentals |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements covered by P.Eng. stamp requirement |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage sufficient for current design stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherently presented across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance conflict table demonstrates discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs table shows adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers holistic view adequately |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent with "design precedes installation" principle |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Service ampacity/size is an essential fact that must be established by PKG-004 electrical design. Add target date for when this value will be available. | Service ampacity is listed as TBD in the Attributes table. Under "essential fact," this is the single most critical sizing parameter for the deliverable and remains unresolved. | Datasheet.md | Attributes table, row "Service ampacity / size" | | PKG-004 electrical design engineer | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Datasheet | Datasheet | Clarify that load table circuit counts are "approximate from conceptual drawing" and add note that IFC load schedule will supersede. Ensure Specification REQ-015-01-003 references the same caveat. | Under "adequate evidence," the Known Downstream Load Summary states counts are approximate but does not explicitly flag that ampacity decisions cannot rely on these counts. The evidence is suggestive but not sufficient for design. | Datasheet.md | Known Downstream Load Summary | | IFC electrical drawings (PKG-004) | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add rows for DEL-015-05 (if applicable) and any other downstream loads not yet enumerated (e.g., HVAC loads, future expansion loads) to the Known Downstream Load Summary. | Under "comprehensive record," the load summary lists loads visible on App B-Elec but does not account for all downstream deliverables. DEL-015-05 loads and any HVAC or mechanical loads that may draw from the MDP are not listed. | Datasheet.md | Known Downstream Load Summary | | App B-Elec and PKG-004 IFC drawings | TBD |
| B-004 | B:information:necessity | TBD_Question | Multi | Datasheet | Record TBD: Identify the specific utility provider serving SW 14-44-21-W4. This is an essential signal for all utility coordination activities. | Under "essential signal," the utility provider is listed as TBD in the Datasheet Attributes. This information is prerequisite to Steps 1.1 and 1.2 in the Procedure and is referenced as an unresolved dependency in Guidance. | Datasheet.md; Procedure.md | Datasheet: Attributes "Utility provider"; Procedure: Step 1.1 | | Proponent to investigate during design phase | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Threshold Basis | 1 | HAS_ITEMS | Minimum code compliance threshold not quantified |
| C:normative:sufficiency | normative | sufficiency | Enforced Competence Proof | 0 | NO_ITEMS | P.Eng. stamp requirement adequately addresses competence proof |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Scope | 1 | HAS_ITEMS | Scope of code compliance not exhaustively enumerated |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Rigor | 0 | NO_ITEMS | Regulatory references are consistent across documents |
| C:operative:necessity | operative | necessity | Critical Operational Readiness | 0 | NO_ITEMS | Procedure prerequisites adequately establish readiness conditions |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Practical Capability | 0 | NO_ITEMS | Procedure steps demonstrate practical capability path |
| C:operative:completeness | operative | completeness | Whole-Process Delivery Coverage | 0 | NO_ITEMS | Four-phase procedure covers the whole delivery process |
| C:operative:consistency | operative | consistency | Uniform Execution Discipline | 0 | NO_ITEMS | Procedure is internally consistent in its execution steps |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Foundation | 0 | NO_ITEMS | Guidance Purpose section establishes merit foundation |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Worth Assessment | 0 | NO_ITEMS | Trade-offs table provides defensible assessment framework |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Portrait | 1 | HAS_ITEMS | No lifecycle cost or total-cost-of-ownership consideration |
| C:evaluative:consistency | evaluative | consistency | Principled Worth Integrity | 0 | NO_ITEMS | Value reasoning is consistent across Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Clarify whether "Alberta Safety Codes" in REQ-015-01-004 refers to the Safety Codes Act (RSA 2000, c. S-1) and its Electrical Code Regulation, or to specific technical standards. Add regulation citation. | Under "Compulsory Threshold Basis," the compulsory threshold for compliance is stated generically as "Alberta Safety Codes" without identifying the specific regulation or statutory instrument. This ambiguity could affect which compliance thresholds are binding. | Specification.md | REQ-015-01-004 -- Code Compliance | | Alberta Municipal Affairs (Safety Codes authority) | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add requirement or note addressing environmental/site conditions that may affect code compliance (e.g., ambient temperature derating, altitude derating, corrosive environment considerations for a landfill-adjacent site). | Under "Exhaustive Compliance Scope," the requirements address standard code compliance but do not consider site-specific code provisions. The project is at a landfill site, which may invoke specific code clauses for hazardous or corrosive environments. | Specification.md | Requirements section (after REQ-015-01-004) | | PKG-004 design engineer; Alberta Safety Codes officer | TBD |
| C-003 | C:evaluative:completeness | MissingSlot | Guidance | Guidance | Add a Considerations subsection addressing lifecycle cost implications of voltage selection and spare capacity decisions (e.g., higher-voltage system may reduce conductor costs but increase transformer costs). | Under "Holistic Value Portrait," the Guidance trade-offs table lists options but does not discuss lifecycle cost or total cost of ownership for the alternatives. A maintenance shop facility has a long operational life; voltage selection and spare capacity have long-term cost implications. | Guidance.md | Trade-offs table / Considerations section | | Owner (Camrose County) and design engineer | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Governance Ground | 1 | HAS_ITEMS | Permit governance gap |
| F:normative:sufficiency | normative | sufficiency | Certified Proficiency Standard | 0 | NO_ITEMS | P.Eng. certification requirement is clear |
| F:normative:completeness | normative | completeness | Total Jurisdictional Coverage | 1 | HAS_ITEMS | Municipal permits not addressed |
| F:normative:consistency | normative | consistency | Codified Enforcement Framework | 0 | NO_ITEMS | Enforcement references are consistent |
| F:operative:necessity | operative | necessity | Validated Workflow Prerequisite | 1 | HAS_ITEMS | Prerequisite validation gap |
| F:operative:sufficiency | operative | sufficiency | Verified Workmanship Fitness | 0 | NO_ITEMS | Workmanship verification covered by inspections |
| F:operative:completeness | operative | completeness | Complete Lifecycle Accounting | 0 | NO_ITEMS | Procedure Records section covers lifecycle documentation |
| F:operative:consistency | operative | consistency | Disciplined Throughput Stability | 0 | NO_ITEMS | Procedure is sequentially consistent |
| F:evaluative:necessity | evaluative | necessity | Warranted Merit Priority | 0 | NO_ITEMS | Guidance Purpose establishes merit priority |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Value Judgment | 1 | HAS_ITEMS | Trade-off recommendations unsubstantiated |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Merit Reckoning | 0 | NO_ITEMS | Adequately covered at current design stage |
| F:evaluative:consistency | evaluative | consistency | Integrated Ethical Alignment | 0 | NO_ITEMS | No ethical misalignment detected |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Specification | Add requirement addressing building permit / development permit obligations for electrical service installation, or confirm these are covered under PKG-011 or a project-level permit. | Under "Obligatory Governance Ground," the Specification requires an Electrical Safety Code permit (REQ-015-01-006) but does not address whether a separate building or development permit is needed for the service entrance / trench work. | Specification.md | Requirements section (after REQ-015-01-006) | | Camrose County planning department; Proponent | TBD |
| F-002 | F:normative:completeness | Normalization | Multi | Guidance | Normalize references to SOW-0081 scope: _CONTEXT.md says "Grounding and safety systems" as a scope item but does not mention SOW-0081; Datasheet Identification says "SOW-0081 (utility tie-in coordination)"; Specification says "coordinate and execute the electrical service tie-in." Confirm consistent scope description. | Under "Total Jurisdictional Coverage," SOW-0081 is described differently across documents. _CONTEXT.md does not mention it at all; Datasheet and Specification use different wording. Consistent terminology prevents jurisdictional gaps. | _CONTEXT.md; Datasheet.md; Specification.md | _CONTEXT.md: Scope of Work; Datasheet.md: Identification "Covers SOW"; Specification.md: REQ-015-01-007 | _CONTEXT.md#Scope of Work vs. Datasheet.md#Identification vs. Specification.md#REQ-015-01-007 | Decomposition document (SOW-0081 definition) | TBD |
| F-003 | F:operative:necessity | VerificationGap | Procedure | Procedure | Add a prerequisite validation checkpoint: before proceeding from Phase 1 to Phase 2, confirm all PRE-1 through PRE-7 are satisfied and document the confirmation. | Under "Validated Workflow Prerequisite," the Procedure lists seven prerequisites but does not include an explicit gate-check step confirming all prerequisites are met before proceeding to Phase 2 (installation). The prerequisites could be skipped without formal validation. | Procedure.md | Prerequisites section / transition from Phase 1 to Phase 2 | | Proponent project manager | TBD |
| F-004 | F:evaluative:sufficiency | WeakStatement | Guidance | Guidance | Strengthen Trade-offs "Recommended approach" column with explicit criteria or conditions under which each option would be selected, rather than deferring all decisions to PKG-004. | Under "Substantiated Value Judgment," the Trade-offs table lists three trade-offs but each "Recommended approach" defers entirely to PKG-004 or states ASSUMPTION. No substantive judgment criteria are provided for the reader to evaluate the recommendation. | Guidance.md | Trade-offs table | | Design engineer (PKG-004) and Owner | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Directive Authority | 1 | HAS_ITEMS | Directive authority for voltage unclear |
| D:normative:applying | normative | applying | Compulsory Qualification Enactment | 0 | NO_ITEMS | P.Eng. requirement enacts qualification compulsion |
| D:normative:judging | normative | judging | Binding Conformance Closure | 1 | HAS_ITEMS | No formal conformance closure mechanism |
| D:normative:reviewing | normative | reviewing | Settled Compliance Architecture | 0 | NO_ITEMS | Inspection and records architecture is settled |
| D:operative:guiding | operative | guiding | Grounded Process Navigation | 0 | NO_ITEMS | Procedure provides grounded process navigation |
| D:operative:applying | operative | applying | Confirmed Task Deployment | 0 | NO_ITEMS | Steps are deployable and specific |
| D:operative:judging | operative | judging | Closed Delivery Verdict | 0 | NO_ITEMS | Commissioning record in Step 4.3 closes delivery |
| D:operative:reviewing | operative | reviewing | Confirmed Process Rhythm | 0 | NO_ITEMS | Four-phase structure provides clear rhythm |
| D:evaluative:guiding | evaluative | guiding | Settled Value Compass | 0 | NO_ITEMS | Guidance Purpose section sets value compass |
| D:evaluative:applying | evaluative | applying | Settled Merit Delivery | 0 | NO_ITEMS | Trade-offs and conflict table address merit delivery |
| D:evaluative:judging | evaluative | judging | Definitive Value Finding | 1 | HAS_ITEMS | No mechanism to record Owner value decisions |
| D:evaluative:reviewing | evaluative | reviewing | Settled Excellence Assessment | 0 | NO_ITEMS | Quality appraisal covered by inspection framework |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | Conflict | Specification | Guidance | Resolve: Specification REQ-015-01-002 says voltage "shall be as specified in the IFC electrical design drawings" while Guidance CON-015-01-001 proposes the design engineer determines it "in consultation with utility and Owner." These are compatible but the directive authority is not identical -- one makes IFC drawings the authority, the other makes a consultation process the authority. | Under "Established Directive Authority," the directive authority for voltage selection is split between two documents with different emphasis. This could cause confusion about whether the IFC drawing alone is authoritative or whether the consultation process is. | Specification.md; Guidance.md | Specification.md#REQ-015-01-002; Guidance.md#Conflict Table CON-015-01-001 | Specification.md#REQ-015-01-002 vs. Guidance.md#Conflict Table CON-015-01-001 | Human ruling needed: clarify whether IFC drawing is sole authority or whether Owner consultation is a prerequisite | TBD |
| D-002 | D:normative:judging | MissingSlot | Specification | Specification | Add a requirement or verification row defining the formal conformance closure mechanism (e.g., a commissioning sign-off checklist or certificate of conformance that confirms all REQ items are satisfied before CCC). | Under "Binding Conformance Closure," the Specification lists 12 requirements and a verification table, but there is no single conformance closure artifact that formally attests all requirements are met. The CCC is mentioned in Documentation but is Owner-issued, not a contractor conformance record. | Specification.md | Verification section / Documentation section | | Proponent and County project representative | TBD |
| D-003 | D:evaluative:judging | MissingSlot | Guidance | Guidance | Add a section or note in Guidance describing how Owner value decisions (e.g., spare capacity preference, voltage preference) will be recorded and fed back into the design process. | Under "Definitive Value Finding," the Guidance identifies several decisions requiring Owner input (welding specs, spare capacity, voltage) but provides no mechanism for recording the Owner's value-based decisions once made. Conflict table has HumanRuling=TBD but no process for resolving them. | Guidance.md | Conflict Table | | Owner (Camrose County) | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Priority Mandate | 0 | NO_ITEMS | Priority mandates are established |
| X:guiding:sufficiency | guiding | sufficiency | Justified Steering Competence | 0 | NO_ITEMS | Steering competence addressed by P.Eng. and Guidance principles |
| X:guiding:completeness | guiding | completeness | Exhaustive Governance Scope | 1 | HAS_ITEMS | As-built drawing requirement ambiguous |
| X:guiding:consistency | guiding | consistency | Stable Directional Harmony | 0 | NO_ITEMS | Directional consistency maintained across documents |
| X:applying:necessity | applying | necessity | Confirmed Qualification Basis | 1 | HAS_ITEMS | Contractor qualification not specified |
| X:applying:sufficiency | applying | sufficiency | Competent Certification Fit | 0 | NO_ITEMS | Certification requirements adequately addressed |
| X:applying:completeness | applying | completeness | Comprehensive Task Proficiency | 0 | NO_ITEMS | Task coverage is comprehensive |
| X:applying:consistency | applying | consistency | Coherent Delivery Assurance | 0 | NO_ITEMS | Delivery assurance is coherent |
| X:judging:necessity | judging | necessity | Decisive Conformance Marker | 1 | HAS_ITEMS | Phase rotation verification incomplete |
| X:judging:sufficiency | judging | sufficiency | Qualified Verdict Evidence | 1 | HAS_ITEMS | Verdict evidence for grounding incomplete |
| X:judging:completeness | judging | completeness | Exhaustive Verdict Record | 0 | NO_ITEMS | Verdict records adequately enumerated |
| X:judging:consistency | judging | consistency | Unambiguous Conformance Finding | 0 | NO_ITEMS | Conformance findings are unambiguous |
| X:reviewing:necessity | reviewing | necessity | Fundamental Audit Basis | 1 | HAS_ITEMS | Audit basis for utility coordination incomplete |
| X:reviewing:sufficiency | reviewing | sufficiency | Competent Structural Review | 0 | NO_ITEMS | Structural review adequately addressed through inspection |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Quality Accounting | 1 | HAS_ITEMS | Quality accounting for metering incomplete |
| X:reviewing:consistency | reviewing | consistency | Harmonized Architecture Check | 0 | NO_ITEMS | Architecture checks are harmonized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | WeakStatement | Procedure | Specification | Clarify whether as-built drawings are contractually required. Step 4.4 says "TBD whether formal as-built drawings are required under contract -- confirm with project manager." This should be resolved and stated as a requirement or explicitly excluded. | Under "Exhaustive Governance Scope," the as-built drawing obligation is stated as TBD in the Procedure, which means the governance scope for documentation is incomplete. As-built drawings are a standard deliverable for electrical service; their status should be definitive. | Procedure.md | Phase 4, Step 4.4 | | CCDC 14-2013 contract terms; project manager | TBD |
| X-002 | X:applying:necessity | MissingSlot | Specification | Specification | Add a requirement or prerequisite stating the minimum qualifications for the electrical contractor performing this work (e.g., Alberta master electrician license, Safety Codes-certified). | Under "Confirmed Qualification Basis," the Specification requires P.Eng.-stamped IFC drawings but does not state the qualification requirements for the installing contractor. Alberta requires licensed electrical contractors for permit work; this should be explicitly stated. | Specification.md | Requirements section (general) | | Alberta Safety Codes Act; Electrical Code Regulation | TBD |
| X-003 | X:judging:necessity | VerificationGap | Procedure | Procedure | Add explicit verification step for phase rotation direction at MDP after utility energization (Step 3.4 mentions "correct voltage and phase rotation" but does not specify the verification method or instrument). | Under "Decisive Conformance Marker," phase rotation is mentioned as a check in Step 3.4 but without specifying the method (phase rotation meter) or the expected result (e.g., ABC rotation per IFC design). This is a decisive conformance marker that needs a defined verification method. | Procedure.md | Phase 3, Step 3.4 | | CSA C22.1 and IFC drawings | TBD |
| X-004 | X:judging:sufficiency | VerificationGap | Specification | Specification | Add quantitative acceptance criteria for grounding system verification: specify ground resistance limit (e.g., per CSA C22.1 Section 10) and test method (e.g., fall-of-potential or clamp-on ground resistance tester). | Under "Qualified Verdict Evidence," the Specification verification table for REQ-015-01-008 says "ground continuity and resistance testing TBD per code." This does not provide qualified verdict evidence because the acceptance criterion is not stated. Related to A-003 but focused on the evidence standard. | Specification.md | Verification table, REQ-015-01-008 row | | CSA C22.1 Section 10 | TBD |
| X-005 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Add a verification step or record requirement for utility coordination milestones (application date, confirmation date, scheduled energization date) to establish an auditable trail for SOW-0081 completion. | Under "Fundamental Audit Basis," the Procedure Steps 1.1 and 1.2 direct utility coordination but do not require specific date-stamped records of each coordination milestone. The Records section lists "Utility service application and confirmation" but does not require interim milestone documentation. | Procedure.md | Phase 1, Steps 1.1-1.2; Records section | | Proponent project manager | TBD |
| X-006 | X:reviewing:completeness | Normalization | Datasheet | Datasheet | Normalize metering terminology: Datasheet Attributes says "Metering: TBD -- utility company metering requirements to be confirmed at tie-in coordination." Specification REQ-015-01-002 mentions metering as part of service entrance. Procedure Step 2.2 says "Meter base per utility specifications." Align terminology and confirm metering is in scope of this deliverable or is a utility-provided item. | Under "Exhaustive Quality Accounting," metering is referenced in three documents with slightly different framing (TBD in Datasheet, implicit in Specification, explicit installation step in Procedure). The quality accounting for metering is incomplete because scope ownership is ambiguous. | Datasheet.md; Specification.md; Procedure.md | Datasheet.md#Attributes "Metering"; Specification.md#In Scope item 2; Procedure.md#Step 2.2 | Datasheet.md#Attributes vs. Procedure.md#Step 2.2 | Utility company (metering is typically utility-owned in Alberta) | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Evidenced Governance Baseline | 1 | HAS_ITEMS | Governance baseline reference gap |
| E:guiding:information | guiding | information | Anchored Governance Signal | 0 | NO_ITEMS | Governance signals adequately anchored in RFP and decomposition |
| E:guiding:knowledge | guiding | knowledge | Masterful Governance Navigation | 0 | NO_ITEMS | Governance navigation demonstrated in Guidance principles |
| E:guiding:wisdom | guiding | wisdom | Panoramic Leadership Foresight | 0 | NO_ITEMS | Foresight demonstrated in Guidance conflict table and trade-offs |
| E:applying:data | applying | data | Demonstrated Capability Record | 1 | HAS_ITEMS | No capability record template |
| E:applying:information | applying | information | Contextualized Task Briefing | 0 | NO_ITEMS | Procedure provides contextualized task briefing |
| E:applying:knowledge | applying | knowledge | Proficient Craft Authority | 0 | NO_ITEMS | Craft authority established through P.Eng. requirement |
| E:applying:wisdom | applying | wisdom | Measured Craft Foresight | 0 | NO_ITEMS | Guidance considerations demonstrate craft foresight |
| E:judging:data | judging | data | Grounded Conformance Evidence | 0 | NO_ITEMS | Evidence requirements covered in verification tables |
| E:judging:information | judging | information | Definitive Adjudication Account | 0 | NO_ITEMS | Adjudication pathways established in conflict table |
| E:judging:knowledge | judging | knowledge | Expert Adjudication Mastery | 0 | NO_ITEMS | Expert adjudication deferred to P.Eng. and Safety Codes officer |
| E:judging:wisdom | judging | wisdom | Principled Verdict Insight | 0 | NO_ITEMS | Principled reasoning present in Guidance |
| E:reviewing:data | reviewing | data | Grounded Inspection Ledger | 1 | HAS_ITEMS | Inspection record cross-reference gap |
| E:reviewing:information | reviewing | information | Comprehensive Audit Briefing | 0 | NO_ITEMS | Records section provides audit briefing |
| E:reviewing:knowledge | reviewing | knowledge | Proficient Inspection Authority | 0 | NO_ITEMS | Inspection authority established (Safety Codes officer) |
| E:reviewing:wisdom | reviewing | wisdom | Panoramic Inspection Wisdom | 0 | NO_ITEMS | Inspection wisdom adequately represented |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Datasheet | Datasheet | Normalize the References table: Datasheet References lists R-01 and R-05 but _REFERENCES.md uses the same IDs with different descriptions. Align descriptions and confirm both files reference the same source documents. | Under "Evidenced Governance Baseline," the evidential baseline depends on consistent reference identification. Datasheet says "R-01: AB-2026-01424-WDMLRL RFP.pdf" while _REFERENCES.md says "R-01: Main RFP SS3.4 (Electrical System Requirements)." The scope descriptions differ. | Datasheet.md; _REFERENCES.md | Datasheet.md#References table; _REFERENCES.md#Primary References | Datasheet.md#References vs. _REFERENCES.md#Primary References | Project document control | TBD |
| E-002 | E:applying:data | RationaleGap | Specification | Guidance | Add rationale in Guidance explaining why REQ-015-01-010 (Welding Circuits) is scoped under DEL-015-01 (Power Service) rather than DEL-015-03 (Receptacle Installation) or DEL-015-04 (Equipment Power Circuits). The boundary between service-level and branch-level scope is not explained. | Under "Demonstrated Capability Record," the welding circuit requirement sits in the power service deliverable but welding circuits are branch-level work. The scoping rationale is not documented, which could cause confusion about which deliverable owns the welding circuit installation. | Specification.md | REQ-015-01-010 -- Welding Circuits | | Decomposition document (PKG-015 deliverable boundaries) | TBD |
| E-003 | E:reviewing:data | Conflict | Procedure | Specification | Resolve: Procedure Verification table includes "Downstream circuits energizable" as a verification check, but Specification Out of Scope explicitly excludes "Branch circuit wiring and fixtures downstream of MDP." Clarify whether verifying downstream circuit energizability is in scope of this deliverable or is a downstream deliverable responsibility. | Under "Grounded Inspection Ledger," the inspection/verification scope in the Procedure extends to downstream circuit energizability, while the Specification explicitly places downstream circuits out of scope. This creates an ambiguity about the verification boundary. | Procedure.md; Specification.md | Procedure.md#Verification table "Downstream circuits energizable"; Specification.md#Out of Scope | Procedure.md#Verification table vs. Specification.md#Out of Scope | Human ruling needed: define verification boundary at MDP output terminals vs. downstream load points | TBD |
