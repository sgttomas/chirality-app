# Semantic Lensing Register: DEL-01-04 Permitting, Inspections & AHJ Coordination

**Generated:** 2026-02-17
**Deliverable Folder:** test/execution-6a/PKG-001_General Requirements & Delivery Controls/1_Working/DEL-01-04_Permitting, Inspections & AHJ Coordination/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — test/execution-6a/PKG-001_General Requirements & Delivery Controls/1_Working/DEL-01-04_Permitting, Inspections & AHJ Coordination/_CONTEXT.md
- _STATUS.md — test/execution-6a/PKG-001_General Requirements & Delivery Controls/1_Working/DEL-01-04_Permitting, Inspections & AHJ Coordination/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — test/execution-6a/PKG-001_General Requirements & Delivery Controls/1_Working/DEL-01-04_Permitting, Inspections & AHJ Coordination/_SEMANTIC.md
- Datasheet.md — test/execution-6a/PKG-001_General Requirements & Delivery Controls/1_Working/DEL-01-04_Permitting, Inspections & AHJ Coordination/Datasheet.md
- Specification.md — test/execution-6a/PKG-001_General Requirements & Delivery Controls/1_Working/DEL-01-04_Permitting, Inspections & AHJ Coordination/Specification.md
- Guidance.md — test/execution-6a/PKG-001_General Requirements & Delivery Controls/1_Working/DEL-01-04_Permitting, Inspections & AHJ Coordination/Guidance.md
- Procedure.md — test/execution-6a/PKG-001_General Requirements & Delivery Controls/1_Working/DEL-01-04_Permitting, Inspections & AHJ Coordination/Procedure.md
- _REFERENCES.md — test/execution-6a/PKG-001_General Requirements & Delivery Controls/1_Working/DEL-01-04_Permitting, Inspections & AHJ Coordination/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 19
- By document:
  - Datasheet: 3
  - Specification: 8
  - Guidance: 3
  - Procedure: 2
  - Multi: 3
- By matrix:
  - A: 4  B: 3  C: 2  F: 3  D: 2  X: 3  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Governing code clause-level prescriptions are TBD |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Permit fee estimation practice unclear |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | AHJ approval criteria not enumerated |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Audit process adequately covered across docs |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure doc provides adequate stepwise direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps are present in Procedure Phase B |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No performance metrics for permit processing times |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Verification tables cover review adequately |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles section covers value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Not salient for this regulatory deliverable |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Not salient for this regulatory deliverable |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Covered by inspection regime and verification tables |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Datasheet | Datasheet | Record TBD: Alberta Building Code clause-level requirements applicable to permitting and inspections need to be identified once the code text is accessible | The governing code is cited as the Alberta Building Code but clause-level requirements are explicitly marked TBD across Datasheet and Specification. Prescriptive direction cannot be fully established without these clauses. | Datasheet.md; Specification.md | Datasheet#Attributes (Governing code); Specification#Standards | -- | Alberta Building Code text | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify whether permit fee estimates must be itemized in the base price or may be carried as a lump sum allowance within the DB's proposal | RFP assigns all permit costs to DB, but no mechanism describes how the DB accounts for or reports permit fee expenditures. The mandatory practice of paying permit fees lacks a reporting structure. | Specification.md | REQ-01-04-01; REQ-01-04-02 | -- | RFP §7.2 | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for REQ-01-04-04 (Code Conformity) beyond "review permit approvals issued by AHJs" -- specify what constitutes sufficient evidence of conformity when AHJ has not inspected all work | REQ-01-04-04 requires all work to meet all building codes, but the verification approach relies solely on AHJ permit approvals. Some work may not be subject to AHJ inspection; conformity evidence for those items is unaddressed. | Specification.md | REQ-01-04-04; Verification table row for REQ-01-04-04 | -- | Specification.md | TBD |
| A-004 | A:operative:judging | MissingSlot | Specification | Specification | Add performance targets for permit processing (e.g., target turnaround times, maximum acceptable re-inspection count before escalation) | No performance assessment metrics exist for the permitting process itself. The verification table checks that permits are submitted and obtained but does not measure timeliness or process quality. | Specification.md | Verification section | -- | Specification.md | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | AHJ contact details missing from Datasheet |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Evidence requirements covered in Procedure verification |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Permit fee schedule data absent |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement approach consistent across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key information signals present |
| B:information:sufficiency | information | sufficiency | adequate context | 1 | HAS_ITEMS | RFP §7.5 not fully read -- occupancy permit context incomplete |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Account of permitting scope is comprehensive |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging is coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Understanding of permitting regime is established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements implicitly covered |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage adequate for current phase |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance Principles provide discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs section provides judgment framing |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Covered by Guidance Considerations and Trade-offs |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent across Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add AHJ contact information (or a reference pointer to it) as essential factual data: Town of Penhold permitting office, Alberta Safety Codes Officer, AEP (if applicable) | Procedure Step A1 and Guidance Considerations both reference AHJ contacts as needed, but the Datasheet does not record them as factual data. Essential facts for permit submission are incomplete. | Datasheet.md; Procedure.md | Datasheet#Conditions; Procedure#Prerequisites (AHJ Contact List) | -- | Datasheet.md | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add anticipated permit fee schedule or fee range data (or TBD placeholder) for each permit type to the Datasheet Attributes | The Datasheet records that the DB pays for all permits but does not include any factual data about anticipated permit fee amounts. For a comprehensive record, fee data (even as TBD placeholders) should be captured. | Datasheet.md | Datasheet#Attributes (Permit fee responsibility) | -- | Town of Penhold fee schedule | TBD |
| B-003 | B:information:sufficiency | WeakStatement | Specification | Specification | Clarify REQ-01-04-10 source: confirm RFP §7.5 content and update SourceRef from "location TBD" to a precise section reference once the RFP section is read | REQ-01-04-10 (Occupancy Permit) cites RFP §7.5 with "location TBD (section not read in this session)." This leaves the requirement's authority weakly grounded. Adequate context requires the actual source to be verified. | Specification.md | REQ-01-04-10 | -- | RFP §7.5 | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | regulatory imperative | 1 | HAS_ITEMS | Environmental approval imperative weakly stated |
| C:normative:sufficiency | normative | sufficiency | substantiated conformance | 0 | NO_ITEMS | Conformance substantiation approach present |
| C:normative:completeness | normative | completeness | comprehensive mandate coverage | 0 | NO_ITEMS | Mandate coverage is comprehensive across docs |
| C:normative:consistency | normative | consistency | harmonized regulatory alignment | 0 | NO_ITEMS | Regulatory alignment consistent across docs |
| C:operative:necessity | operative | necessity | core operational competence | 0 | NO_ITEMS | Operational competence requirements present |
| C:operative:sufficiency | operative | sufficiency | capable operational practice | 0 | NO_ITEMS | Operational practice adequately described |
| C:operative:completeness | operative | completeness | integrated process coverage | 1 | HAS_ITEMS | No linkage to DEL-01-03 H&S inspection overlap |
| C:operative:consistency | operative | consistency | disciplined operational method | 0 | NO_ITEMS | Methods are disciplined and consistent |
| C:evaluative:necessity | evaluative | necessity | foundational value criterion | 0 | NO_ITEMS | Value criteria present in Guidance Principles |
| C:evaluative:sufficiency | evaluative | sufficiency | substantiated merit appraisal | 0 | NO_ITEMS | Not salient -- regulatory deliverable |
| C:evaluative:completeness | evaluative | completeness | exhaustive quality assessment | 0 | NO_ITEMS | Quality assessment covered by verification |
| C:evaluative:consistency | evaluative | consistency | principled value consistency | 0 | NO_ITEMS | Value consistency maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Guidance | Guidance | Strengthen the environmental approvals entry under Permit Type Coverage: clarify whether AEP environmental approvals are a regulatory imperative or merely a contingency, and specify the trigger conditions | Guidance lists "Environmental approvals (AEP if required for flood/water constraints)" with conditional language. As a regulatory imperative, the trigger condition for when AEP approval is required should be stated more definitively, or a TBD question should be formally recorded. | Guidance.md | Considerations > Permit Type Coverage | -- | AEP / Decomposition Vocabulary Map | TBD |
| C-002 | C:operative:completeness | RationaleGap | Guidance | Guidance | Add rationale explaining the boundary between DEL-01-04 inspection activities and DEL-01-03 (H&S Plan) inspection activities to avoid duplication or gaps in integrated process coverage | Procedure references DEL-01-01 and DEL-01-02 as prerequisites, and Specification scopes out H&S (DEL-01-03). However, there is no rationale explaining how construction-phase safety inspections (H&S domain) interact with AHJ compliance inspections. The integrated process coverage lens reveals this boundary is not articulated. | Guidance.md; Specification.md | Guidance#Considerations; Specification#Out of Scope | -- | Guidance.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | binding compliance threshold | 1 | HAS_ITEMS | No explicit pass/fail threshold for permit matrix completeness |
| F:normative:sufficiency | normative | sufficiency | justified regulatory proficiency | 0 | NO_ITEMS | Proficiency requirements implicitly covered |
| F:normative:completeness | normative | completeness | total regulatory documentation | 1 | HAS_ITEMS | Permit application document retention not specified |
| F:normative:consistency | normative | consistency | coherent mandate uniformity | 0 | NO_ITEMS | Mandates are uniform across docs |
| F:operative:necessity | operative | necessity | essential procedural capability | 0 | NO_ITEMS | Procedural capabilities are established |
| F:operative:sufficiency | operative | sufficiency | demonstrated operational proficiency | 0 | NO_ITEMS | Proficiency demonstrated through verification |
| F:operative:completeness | operative | completeness | exhaustive process documentation | 1 | HAS_ITEMS | Discipline inspection report format not specified |
| F:operative:consistency | operative | consistency | calibrated methodological rigor | 0 | NO_ITEMS | Methodology is consistently rigorous |
| F:evaluative:necessity | evaluative | necessity | fundamental evaluative benchmark | 0 | NO_ITEMS | Benchmarks present in verification tables |
| F:evaluative:sufficiency | evaluative | sufficiency | contextualized evaluative standard | 0 | NO_ITEMS | Standards are contextualized |
| F:evaluative:completeness | evaluative | completeness | complete evaluative archive | 0 | NO_ITEMS | Archive requirements in Procedure Records |
| F:evaluative:consistency | evaluative | consistency | calibrated evaluative coherence | 0 | NO_ITEMS | Evaluation coherence maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add a binding compliance threshold for permit matrix completeness: define what constitutes an acceptable permit matrix (e.g., all known permit types populated, no blank status fields, updated within N days of status change) | REQ-01-04-05 requires a permit matrix, and the verification says "Review permit matrix for completeness," but there is no explicit threshold defining what "complete" means. Without a binding threshold, the verification is subjective. | Specification.md | REQ-01-04-05; Verification table row for REQ-01-04-05 | -- | Specification.md | TBD |
| F-002 | F:normative:completeness | MissingSlot | Procedure | Procedure | Add a step or record requirement for retaining copies of all submitted permit applications and AHJ correspondence as part of total regulatory documentation | Procedure Records table lists "Permit applications -- Filed copies of all permit applications" but does not specify a filing standard or confirm that all AHJ correspondence (conditions, queries, amendment requests) is retained. Total regulatory documentation requires these ancillary records. | Procedure.md | Records table | -- | Procedure.md | TBD |
| F-003 | F:operative:completeness | MissingSlot | Specification | Specification | Add a requirement specifying the minimum content/format for consultant discipline inspection reports (e.g., date, inspector, scope inspected, findings, recommendations, sign-off) | REQ-01-04-07 requires written inspection reports but does not define what constitutes a compliant report. The exhaustive process documentation lens reveals this format gap. | Specification.md | REQ-01-04-07 | -- | Specification.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | authoritative regulatory closure | 1 | HAS_ITEMS | No explicit closure criteria for permit lifecycle |
| D:normative:applying | normative | applying | enforced compliance action | 0 | NO_ITEMS | Compliance actions are enforced through steps |
| D:normative:judging | normative | judging | definitive conformance closure | 0 | NO_ITEMS | Conformance closure addressed via SP certification |
| D:normative:reviewing | normative | reviewing | systematic compliance settlement | 0 | NO_ITEMS | Settlement process adequate |
| D:operative:guiding | operative | guiding | settled process guidance | 0 | NO_ITEMS | Process guidance is settled in Procedure |
| D:operative:applying | operative | applying | demonstrated workflow closure | 0 | NO_ITEMS | Workflow closure demonstrated through verification |
| D:operative:judging | operative | judging | evidenced performance judgment | 1 | HAS_ITEMS | No evidence standard for re-inspection root cause analysis |
| D:operative:reviewing | operative | reviewing | calibrated process examination | 0 | NO_ITEMS | Process examination covered by verification checks |
| D:evaluative:guiding | evaluative | guiding | settled worth framework | 0 | NO_ITEMS | Worth framework established in Guidance Principles |
| D:evaluative:applying | evaluative | applying | enacted value judgment | 0 | NO_ITEMS | Value judgments enacted through trade-off decisions |
| D:evaluative:judging | evaluative | judging | definitive value closure | 0 | NO_ITEMS | Not salient for regulatory deliverable |
| D:evaluative:reviewing | evaluative | reviewing | calibrated quality examination | 0 | NO_ITEMS | Quality examination covered |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | VerificationGap | Specification | Specification | Add explicit closure criteria defining when the permit lifecycle is complete (e.g., all permits in "Approved" status, no outstanding conditions, occupancy permit obtained) | The objective of authoritative regulatory closure requires defined endpoints. While REQ-01-04-10 addresses the occupancy permit, there is no aggregate closure criterion stating all permits must reach a terminal approved state before the deliverable is considered complete. | Specification.md | REQ-01-04-05; REQ-01-04-10 | -- | Specification.md | TBD |
| D-002 | D:operative:judging | RationaleGap | Guidance | Guidance | Add rationale for how re-inspection root causes should be analyzed and what constitutes systemic quality failure warranting escalation | Guidance mentions tracking re-inspection frequency and root causes but does not explain what threshold of repeated failures constitutes a systemic issue or what escalation path applies. The evidenced performance judgment lens reveals this rationale gap. | Guidance.md | Considerations > Re-Inspection Management | -- | Guidance.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | foundational mandate direction | 0 | NO_ITEMS | Mandate direction established |
| X:guiding:sufficiency | guiding | sufficiency | justified operational steering | 0 | NO_ITEMS | Steering justified through Guidance Principles |
| X:guiding:completeness | guiding | completeness | holistic closure direction | 0 | NO_ITEMS | Closure direction present |
| X:guiding:consistency | guiding | consistency | unified methodological alignment | 1 | HAS_ITEMS | Terminology inconsistency across docs |
| X:applying:necessity | applying | necessity | mandatory capability deployment | 0 | NO_ITEMS | Capability deployment requirements present |
| X:applying:sufficiency | applying | sufficiency | justified execution proof | 1 | HAS_ITEMS | No requirement for proof of AHJ pre-application engagement |
| X:applying:completeness | applying | completeness | complete mandate execution | 0 | NO_ITEMS | Mandate execution steps complete in Procedure |
| X:applying:consistency | applying | consistency | dependable regulatory execution | 0 | NO_ITEMS | Execution approach is dependable |
| X:judging:necessity | judging | necessity | conclusive compliance ruling | 0 | NO_ITEMS | Compliance ruling via AHJ approvals |
| X:judging:sufficiency | judging | sufficiency | justified performance finding | 0 | NO_ITEMS | Performance findings justified |
| X:judging:completeness | judging | completeness | complete compliance adjudication | 0 | NO_ITEMS | Adjudication covered |
| X:judging:consistency | judging | consistency | uniform adjudication standard | 0 | NO_ITEMS | Adjudication standard consistent |
| X:reviewing:necessity | reviewing | necessity | foundational compliance scrutiny | 0 | NO_ITEMS | Scrutiny mechanisms present |
| X:reviewing:sufficiency | reviewing | sufficiency | justified procedural audit | 1 | HAS_ITEMS | Procedure verification lacks audit frequency |
| X:reviewing:completeness | reviewing | completeness | total regulatory closure audit | 0 | NO_ITEMS | Closure audit covered via SP package |
| X:reviewing:consistency | reviewing | consistency | reliable regulatory audit standard | 0 | NO_ITEMS | Audit standard reliable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:consistency | Normalization | Multi | Multi | Normalize terminology: "AHJ" vs "Authority Having Jurisdiction" vs "regulatory bodies" vs "AHJ Contact List" -- establish a vocabulary note in Guidance and use consistently across all four documents | The term "AHJ" is used inconsistently: Datasheet uses "Authority Having Jurisdiction (AHJ)" in Conditions but "AHJ" without expansion elsewhere; Procedure Prerequisites say "AHJ Contact List" as if it were a defined artifact; Guidance mixes "AHJ" and "regulatory bodies." Unified methodological alignment requires consistent terminology. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet#Conditions; Procedure#Prerequisites; Guidance#Considerations | -- | Guidance.md (vocabulary note) | TBD |
| X-002 | X:applying:sufficiency | VerificationGap | Procedure | Procedure | Add a verification check confirming that pre-application AHJ engagement (referenced in Guidance) has occurred before permit submission, or clarify that it is optional | Guidance recommends pre-application meetings with AHJ as advisable, but Procedure has no step or verification check for this activity. If justified execution proof is required, the engagement should either be a tracked step or explicitly documented as optional. | Procedure.md; Guidance.md | Guidance#Early AHJ Engagement; Procedure#Steps Phase B | -- | Procedure.md | TBD |
| X-003 | X:reviewing:sufficiency | VerificationGap | Procedure | Procedure | Specify the frequency and responsible party for auditing the permit matrix and inspection/testing plan beyond "Monthly (aligned with progress draws)" -- clarify who performs the review and what constitutes a passing audit | Procedure Verification table says "Permit matrix is complete and current" checked "Monthly," but does not specify who performs the review (DB PM? Owner? Third party?) or what the audit criteria are. A justified procedural audit requires these details. | Procedure.md | Verification table | -- | Procedure.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | binding conformance authority | 0 | NO_ITEMS | Conformance authority established via AHJ |
| E:normative:sufficiency | normative | sufficiency | validated compliance evidence | 1 | HAS_ITEMS | No requirement for independent compliance validation |
| E:normative:completeness | normative | completeness | total conformance resolution | 0 | NO_ITEMS | Conformance resolution path complete |
| E:normative:consistency | normative | consistency | harmonized compliance benchmark | 0 | NO_ITEMS | Compliance benchmarks harmonized |
| E:operative:necessity | operative | necessity | core procedural verification | 0 | NO_ITEMS | Procedural verification present |
| E:operative:sufficiency | operative | sufficiency | substantiated operational adequacy | 0 | NO_ITEMS | Operational adequacy substantiated |
| E:operative:completeness | operative | completeness | integrated operational finality | 0 | NO_ITEMS | Operational finality addressed via SP |
| E:operative:consistency | operative | consistency | stable procedural reliability | 0 | NO_ITEMS | Procedural reliability stable |
| E:evaluative:necessity | evaluative | necessity | definitive worth imperative | 0 | NO_ITEMS | Worth imperative established in Guidance |
| E:evaluative:sufficiency | evaluative | sufficiency | substantiated quality evidence | 1 | HAS_ITEMS | No quality evidence standard for permit documents |
| E:evaluative:completeness | evaluative | completeness | integrated quality finality | 0 | NO_ITEMS | Quality finality via SP certification |
| E:evaluative:consistency | evaluative | consistency | consistent quality benchmark | 0 | NO_ITEMS | Quality benchmark consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | TBD_Question | Multi | TBD | Record TBD: Does the Owner require any independent third-party compliance validation beyond AHJ approvals (e.g., independent code review, peer review of permit submissions)? | The validated compliance evidence lens asks whether AHJ approval alone is sufficient evidence of compliance, or whether additional validation is expected. The RFP does not address this. The question should be raised with the Owner. | Specification.md; Guidance.md | Specification#REQ-01-04-04; Guidance#Principle 2 | -- | Owner / RFP supplementary conditions | TBD |
| E-002 | E:evaluative:sufficiency | Normalization | Multi | Guidance | Normalize the quality standard for permit-related documents: establish whether NMS format (referenced in Specification Standards table) applies to permit applications, inspection reports, and re-inspection responses, or only to construction documents | Specification Standards table lists NMS as "Recommended format for construction documents and documentation" with an ASSUMPTION note. It is unclear whether permit-related documents (applications, inspection reports, re-inspection responses) fall under NMS formatting. Substantiated quality evidence requires clarity on what quality standard governs these documents. | Specification.md; Guidance.md | Specification#Standards (NMS row); Guidance#entire document scanned | -- | Guidance.md | TBD |
