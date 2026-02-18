# Semantic Lensing Register: DEL-03-01 Architectural Design Brief

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-003_Design_Brief/1_Working/DEL-03-01_ArchitecturalDesignBrief
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `PKG-003_Design_Brief/1_Working/DEL-03-01_ArchitecturalDesignBrief/_CONTEXT.md`
- _STATUS.md — `PKG-003_Design_Brief/1_Working/DEL-03-01_ArchitecturalDesignBrief/_STATUS.md` (SEMANTIC_READY)
- _SEMANTIC.md — `PKG-003_Design_Brief/1_Working/DEL-03-01_ArchitecturalDesignBrief/_SEMANTIC.md`
- Datasheet.md — `PKG-003_Design_Brief/1_Working/DEL-03-01_ArchitecturalDesignBrief/Datasheet.md`
- Specification.md — `PKG-003_Design_Brief/1_Working/DEL-03-01_ArchitecturalDesignBrief/Specification.md`
- Guidance.md — `PKG-003_Design_Brief/1_Working/DEL-03-01_ArchitecturalDesignBrief/Guidance.md`
- Procedure.md — `PKG-003_Design_Brief/1_Working/DEL-03-01_ArchitecturalDesignBrief/Procedure.md`
- _REFERENCES.md — `PKG-003_Design_Brief/1_Working/DEL-03-01_ArchitecturalDesignBrief/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 3
  - Specification: 7
  - Guidance: 3
  - Procedure: 2
  - Multi: 3
- By matrix:
  - A: 3  B: 3  C: 2  F: 3  D: 2  X: 3  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 4
  - MissingSlot: 5
  - WeakStatement: 4
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 1
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | OSR clause specificity gap |
| A:normative:applying | normative | applying | mandatory practice | 0 | NO_ITEMS | Addendum 03 integration well-covered across all docs |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | NFPA/CSA applicability unresolved |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification section covers audit approach |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Step 1 provides adequate direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Procedure lacks coordination-meeting protocol |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Review checklist in Procedure Step 2 adequate |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Verification and Records sections present |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P-002 and P-006 provide strong value framing |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance examples EX-001/EX-002 show merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | OBJ-004 scoring connection established in Guidance |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Procedure Step 2 reviewer checklist covers quality |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Strengthen ARCH-F03 and ARCH-C01 by adding specific OSR (Appendix A) clause references instead of repeated "location TBD" placeholders; if OSR text is not accessible, formalize this as a named TBD item with resolution trigger | Multiple requirements reference OSR Appendix A as prescriptive authority but all cite "location TBD" for specific clauses, weakening the prescriptive direction and making compliance determination unverifiable until resolved | Specification.md | Requirements > ARCH-F03, ARCH-C01; Standards | -- | RFP Appendix A (OSR) | TBD |
| A-002 | A:normative:judging | TBD_Question | Specification | Specification | Resolve NFPA and CSA applicability: confirm which NFPA standards (e.g., NFPA 1500, NFPA 1710) and CSA standards apply to fire apparatus bay design and materials; update Standards table from "ASSUMPTION: likely applicable" to confirmed or excluded | Standards table lists NFPA and CSA as "ASSUMPTION: likely applicable" with "location TBD" -- compliance determination cannot proceed without confirming applicability; this is a regulatory gap requiring human or consultant input | Specification.md | Standards | -- | AHJ / Fire code consultant | TBD |
| A-003 | A:operative:applying | MissingSlot | Procedure | Procedure | Add a coordination checkpoint (e.g., pre-draft coordination meeting or brief exchange) between DEL-03-01 author and sibling discipline brief authors (DEL-03-02 through DEL-03-06) before Step 1 drafting begins, to confirm scope boundaries and avoid duplication or gaps | Prerequisites list coordination commitments as checkboxes but provide no procedural mechanism (meeting, email exchange, shared tracker) for how these confirmations actually occur during practical execution | Procedure.md | Prerequisites > Coordination Commitments | -- | Design-Build PM | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Building classification gap |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet references section adequate |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Cold Storage design parameters sparse |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Sizing ranges consistently cited from Addendum 03 |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (7 topics, Addendum 03 items) well-established |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance C-001 covers info gaps adequately |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Seven-topic structure provides comprehensive framing |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology drift potential |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Operational literacy addressed in Guidance P-002 |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Procedure assigns qualified reviewer |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Seven-topic coverage thorough |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Cross-reference strategy consistent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs section provides discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Guidance T-001 through T-003 adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Downstream use and scoring context provided |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles P-001 through P-006 consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Specification | Specification | Add ABC building classification determination (Group classification) as a named data requirement in ARCH-F07 or Standards section; currently the brief is told to "state building classification" but no essential fact establishes what the classification is or should be | Building code compliance approach (ARCH-F07) requires stating building classification per ABC/NBCC, but no document provides or requires capturing the specific Group classification as an essential fact; Procedure Section 7 drafting guidance notes this as an ASSUMPTION requiring AHJ confirmation | Specification.md; Procedure.md | Requirements > ARCH-F07; Procedure Step 1 > Section 7 | -- | ABC / AHJ | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add Cold Storage Building (60x100) architectural parameters to Conditions or Construction table: envelope type, door configuration, floor type, foundation approach, intended use categories; currently only dimensions and "unheated" status are recorded | Cold Storage Building is within architectural scope (site plan rationale, placement) but Datasheet records only footprint dimensions and "unheated" status; no comprehensive record of its architectural design parameters exists in Datasheet despite it being a required facility | Datasheet.md | Conditions; Construction | -- | DEL-04-01 (Cold Storage Design Basis) | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Standardize terminology for the meeting/training room: documents alternate between "meeting room," "ICP meeting room," and "training room" without establishing whether these are the same space or distinct spaces; add clarifying note in Guidance or Datasheet vocabulary | Coherent messaging requires consistent terminology; "meeting room" appears in Datasheet backup generator context, "ICP meeting room" in Procedure, and "training room" in Procedure finishes table -- evaluators may be confused about whether the facility has one multi-use room or separate rooms | Datasheet.md; Procedure.md; Guidance.md | Datasheet > Conditions (backup generator); Procedure > Step 1 Section 4 finishes table; Guidance > P-002 | -- | Decomposition Vocabulary Map | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Binding Regulatory Imperative | 1 | HAS_ITEMS | ABC clause specificity gap |
| C:normative:sufficiency | normative | sufficiency | Mandated Evidentiary Threshold | 0 | NO_ITEMS | Verification approach per requirement is present |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Coverage | 1 | HAS_ITEMS | Addendum 03 checklist artifact TBD |
| C:normative:consistency | normative | consistency | Uniform Regulatory Alignment | 0 | NO_ITEMS | Standards table consistent across docs |
| C:operative:necessity | operative | necessity | Essential Operational Readiness | 0 | NO_ITEMS | Prerequisites checklist covers readiness |
| C:operative:sufficiency | operative | sufficiency | Adequate Execution Competence | 0 | NO_ITEMS | Qualified reviewer assigned |
| C:operative:completeness | operative | completeness | Comprehensive Operational Scope | 0 | NO_ITEMS | Five-step procedure with verification |
| C:operative:consistency | operative | consistency | Systematic Process Integrity | 0 | NO_ITEMS | Checklist approach systematic |
| C:evaluative:necessity | evaluative | necessity | Fundamental Value Criterion | 0 | NO_ITEMS | OBJ-004 scoring connection clear |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit Appraisal | 0 | NO_ITEMS | Examples substantiate merit expectations |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Worth Accounting | 0 | NO_ITEMS | All seven topics contribute to worth |
| C:evaluative:consistency | evaluative | consistency | Coherent Value Integrity | 0 | NO_ITEMS | Value messaging consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Replace "location TBD" for ABC/NBCC clause references in Standards table with at minimum the applicable Part numbers (e.g., ABC Part 3 for occupancy classification, Part 9 for small buildings if applicable); current phrasing undermines binding regulatory imperative | The Standards table lists ABC and NBCC as "Governing" but both entries state "location TBD for specific clause references" -- the binding regulatory imperative cannot be fully formulated without identifying which code parts/divisions apply to this building type | Specification.md | Standards | -- | ABC / Building code consultant | TBD |
| C-002 | C:normative:completeness | VerificationGap | Specification | Specification | Define content and format for the "Addendum 03 Compliance Checklist" artifact listed in Documentation section (currently "TBD"); this is the primary exhaustive compliance verification tool and its absence means coverage cannot be confirmed | Exhaustive compliance coverage requires a complete verification mechanism; the Addendum 03 Compliance Checklist is listed as a required artifact in Documentation but its status is TBD -- without it, the 18-item integration claimed in ARCH-C02 cannot be systematically verified | Specification.md | Documentation > Required Artifacts | -- | Design-Build PM | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Absolute Regulatory Obligation | 1 | HAS_ITEMS | Egress requirement specificity |
| F:normative:sufficiency | normative | sufficiency | Sufficient Compliance Substantiation | 0 | NO_ITEMS | Verification approach per requirement present |
| F:normative:completeness | normative | completeness | Total Regulatory Completeness | 0 | NO_ITEMS | Seven topics cover RFP scope |
| F:normative:consistency | normative | consistency | Principled Compliance Uniformity | 0 | NO_ITEMS | Requirements uniformly structured |
| F:operative:necessity | operative | necessity | Critical Operational Foundation | 1 | HAS_ITEMS | Ventilation performance criteria missing |
| F:operative:sufficiency | operative | sufficiency | Sufficient Operational Capability | 0 | NO_ITEMS | Procedure time estimates provide sufficiency guidance |
| F:operative:completeness | operative | completeness | Exhaustive Operational Coverage | 0 | NO_ITEMS | Five-step procedure covers full lifecycle |
| F:operative:consistency | operative | consistency | Disciplined Operational Coherence | 0 | NO_ITEMS | Consistent cross-reference pattern |
| F:evaluative:necessity | evaluative | necessity | Essential Worth Foundation | 0 | NO_ITEMS | OBJ-004 and OBJ-005 connections established |
| F:evaluative:sufficiency | evaluative | sufficiency | Adequate Worth Substantiation | 1 | HAS_ITEMS | Evaluation scoring guidance thin |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Value Accounting | 0 | NO_ITEMS | All value dimensions accounted for |
| F:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value messaging consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Strengthen ARCH-F07 egress requirement: specify that on-call sleeping areas require a fire-rated egress path independent of apparatus bay egress per ABC; current language says "egress and exiting" generically without specifying the fire-rated separation requirement for sleeping quarters that Procedure Section 7 and Guidance P-003 both elaborate | ARCH-F07 lists "egress and exiting" as a generic code compliance topic but does not explicitly require fire-rated independent egress for on-call sleeping areas, which is a critical life-safety obligation; Procedure and Guidance both recognize this more specifically, creating a gap in the normative requirement statement | Specification.md | Requirements > ARCH-F07 | -- | ABC / NBCC | TBD |
| F-002 | F:operative:necessity | MissingSlot | Specification | Specification | Add a requirement (or clarify in ARCH-F04/ARCH-F07) that the brief must state architectural ventilation performance intent for apparatus bays (e.g., air changes per hour target, contaminant capture approach) before cross-referencing DEL-03-04 for system design; currently the brief is told to note "ventilation compliance" without any architectural performance statement | Apparatus bay ventilation is a critical operational foundation for 24/7 fire hall operations; the brief is required to address ventilation compliance (ARCH-F07) and note exhaust ventilation (ARCH-C02) but no requirement asks the architect to state the architectural ventilation performance intent that DEL-03-04 must then deliver | Specification.md | Requirements > ARCH-F07, ARCH-C02 | -- | DEL-03-04 (Mechanical Design Brief) | TBD |
| F-003 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add guidance on how the brief should connect architectural decisions to OBJ-004 evaluation criteria; current Guidance establishes that OBJ-004 exists (5 pts) and that the brief contributes, but does not explain what evaluator behaviors or scoring rubric elements the brief should target | The worth substantiation for this deliverable depends on evaluator scoring under OBJ-004, but Guidance does not explain what evaluators specifically look for beyond general "design feasibility and operational fit"; this makes it harder for the author to calibrate depth and emphasis for scoring impact | Guidance.md | Purpose > Evaluation Scoring Support | -- | RFP evaluation criteria | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Regulatory Directive | 0 | NO_ITEMS | Seven-topic structure provides clear directive |
| D:normative:applying | normative | applying | Enforceable Compliance Protocol | 1 | HAS_ITEMS | Space schedule verification incomplete |
| D:normative:judging | normative | judging | Conclusive Compliance Ruling | 0 | NO_ITEMS | Verification section addresses ruling approach |
| D:normative:reviewing | normative | reviewing | Definitive Compliance Verification | 0 | NO_ITEMS | Step 5 verification checklist comprehensive |
| D:operative:guiding | operative | guiding | Established Operational Directive | 0 | NO_ITEMS | Procedure Step 1 drafting guidance thorough |
| D:operative:applying | operative | applying | Resolved Execution Delivery | 0 | NO_ITEMS | Five-step workflow resolves execution |
| D:operative:judging | operative | judging | Definitive Performance Judgment | 0 | NO_ITEMS | Reviewer checklist covers performance |
| D:operative:reviewing | operative | reviewing | Conclusive Process Verification | 0 | NO_ITEMS | Step 5 verification and records adequate |
| D:evaluative:guiding | evaluative | guiding | Established Value Direction | 0 | NO_ITEMS | Guidance principles establish direction |
| D:evaluative:applying | evaluative | applying | Substantiated Merit Deployment | 0 | NO_ITEMS | Examples demonstrate deployment |
| D:evaluative:judging | evaluative | judging | Conclusive Worth Determination | 1 | HAS_ITEMS | Approval criteria lack scoring dimension |
| D:evaluative:reviewing | evaluative | reviewing | Definitive Quality Assurance | 0 | NO_ITEMS | Final approval step provides QA |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add verification approach for ARCH-F06 that specifies what constitutes a compliant space schedule when DEL-02-01 areas are TBD; define interim acceptance criteria (e.g., "TBD areas flagged with resolution deadline") so compliance protocol can be enforced even before DEL-02-01 is finalized | Space Schedule with Addendum 03 Ranges is listed as required artifact (Documentation section, status TBD) and ARCH-F06 verification says "cross-check area schedule in DEL-02-01 against Addendum 03 sizing ranges" -- but if DEL-02-01 is not finalized, no enforceable compliance protocol exists for interim verification | Specification.md | Verification > ARCH-F06; Documentation > Space Schedule | -- | Design-Build PM | TBD |
| D-002 | D:evaluative:judging | RationaleGap | Procedure | Procedure | Add a scoring-relevance checkpoint to Step 4 (Final Approval) or Step 5 (Verification): reviewer should confirm that brief content is calibrated to maximize OBJ-004 scoring, not just meet minimum compliance; currently approval criteria are compliance-focused with no evaluative scoring dimension | Final approval (Step 4) and verification (Step 5) check compliance and completeness but do not ask whether the brief is persuasive and scoring-optimized for OBJ-004; this omits the evaluative judgment dimension of conclusive worth determination | Procedure.md | Steps > Step 4: Final Approval; Step 5: Verification | -- | Proposal Manager | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Authority | 0 | NO_ITEMS | RFP 7.1.2(1) provides directive authority |
| X:guiding:sufficiency | guiding | sufficiency | Adequate Directive Substantiation | 1 | HAS_ITEMS | OSR directive substantiation weak |
| X:guiding:completeness | guiding | completeness | Integral Directive Completeness | 0 | NO_ITEMS | Seven-topic directive complete |
| X:guiding:consistency | guiding | consistency | Coherent Directive Discipline | 0 | NO_ITEMS | Directive consistently structured |
| X:applying:necessity | applying | necessity | Critical Implementation Readiness | 1 | HAS_ITEMS | DEL-02-01 dependency timing |
| X:applying:sufficiency | applying | sufficiency | Sufficient Implementation Proof | 0 | NO_ITEMS | Verification approaches provide proof paths |
| X:applying:completeness | applying | completeness | Comprehensive Implementation Scope | 0 | NO_ITEMS | Implementation scope comprehensive |
| X:applying:consistency | applying | consistency | Disciplined Implementation Integrity | 0 | NO_ITEMS | Cross-reference discipline consistent |
| X:judging:necessity | judging | necessity | Essential Adjudicative Authority | 0 | NO_ITEMS | ABC/NBCC provide adjudicative authority |
| X:judging:sufficiency | judging | sufficiency | Adequate Adjudicative Basis | 0 | NO_ITEMS | Requirements traceable to sources |
| X:judging:completeness | judging | completeness | Comprehensive Adjudicative Scope | 0 | NO_ITEMS | All seven topics adjudicable |
| X:judging:consistency | judging | consistency | Principled Adjudicative Coherence | 0 | NO_ITEMS | Consistent verification pattern |
| X:reviewing:necessity | reviewing | necessity | Foundational Audit Imperative | 0 | NO_ITEMS | Records section provides audit trail |
| X:reviewing:sufficiency | reviewing | sufficiency | Adequate Audit Substantiation | 1 | HAS_ITEMS | Version control mechanism unspecified |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Scope | 0 | NO_ITEMS | Step 5 covers comprehensive scope |
| X:reviewing:consistency | reviewing | consistency | Coherent Audit Integrity | 0 | NO_ITEMS | Audit artifacts consistently defined |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | WeakStatement | Multi | Guidance | Strengthen OSR-related guidance: P-005 acknowledges OSR may not be directly accessible but the substantiation strategy ("provide ASSUMPTION-level interpretation") is weak for a prescriptive directive; add guidance on escalation path when OSR clauses cannot be accessed (e.g., request from Owner, or document as formal proposal risk) | Adequate directive substantiation requires either the source text or a clear escalation path; current approach of marking "location TBD" and providing assumptions does not resolve the substantiation gap and may persist through final proposal | Guidance.md; Specification.md | Guidance > P-005; Specification > Standards > OSR | -- | Proposal Manager | TBD |
| X-002 | X:applying:necessity | VerificationGap | Procedure | Procedure | Add a prerequisite gate or decision point in Procedure: if DEL-02-01 is not available in at least draft form, document what portions of DEL-03-01 can proceed and what must be held; current prerequisite checkbox treats DEL-02-01 as binary (available/not) without degraded-mode guidance | Critical implementation readiness depends on DEL-02-01 (upstream concept package); the prerequisite says it must be "available in draft or final form" but provides no verification mechanism or fallback if it is delayed, potentially blocking or degrading DEL-03-01 without explicit procedure | Procedure.md | Prerequisites > Design Documents and References | -- | Design-Build PM | TBD |
| X-003 | X:reviewing:sufficiency | MissingSlot | Procedure | Procedure | Add version control mechanism for the brief: specify how draft versions are tracked (filename convention, version log, or version control system); current Records section lists "Version control or project management system" for Approval Sign-Off Log but does not specify the versioning approach for the brief itself | Adequate audit substantiation requires traceable version history; the Records section references version control in passing but does not establish a specific mechanism for tracking brief iterations through Steps 1-4, reducing audit trail reliability | Procedure.md | Records > Artifacts Produced | -- | Design-Build PM | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Sovereign Compliance Authority | 0 | NO_ITEMS | RFP + ABC establish sovereign authority |
| E:normative:sufficiency | normative | sufficiency | Sufficient Regulatory Justification | 0 | NO_ITEMS | Requirements justify regulatory approach |
| E:normative:completeness | normative | completeness | Exhaustive Regulatory Jurisdiction | 1 | HAS_ITEMS | Flood hazard regulatory gap |
| E:normative:consistency | normative | consistency | Principled Regulatory Integrity | 0 | NO_ITEMS | Regulatory references consistent |
| E:operative:necessity | operative | necessity | Foundational Operational Authority | 0 | NO_ITEMS | Procedure establishes operational authority |
| E:operative:sufficiency | operative | sufficiency | Sufficient Operational Justification | 0 | NO_ITEMS | Procedure time estimates and steps adequate |
| E:operative:completeness | operative | completeness | Exhaustive Operational Jurisdiction | 0 | NO_ITEMS | Procedure scope comprehensive |
| E:operative:consistency | operative | consistency | Principled Operational Discipline | 0 | NO_ITEMS | Consistent process discipline |
| E:evaluative:necessity | evaluative | necessity | Sovereign Value Authority | 0 | NO_ITEMS | OBJ-004 establishes value authority |
| E:evaluative:sufficiency | evaluative | sufficiency | Sufficient Value Justification | 0 | NO_ITEMS | Guidance provides value justification |
| E:evaluative:completeness | evaluative | completeness | Exhaustive Value Jurisdiction | 1 | HAS_ITEMS | Energy/sustainability interface gap |
| E:evaluative:consistency | evaluative | consistency | Principled Value Integrity | 0 | NO_ITEMS | Value messaging consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | VerificationGap | Datasheet | Datasheet | Add flood hazard regulatory authority (e.g., Alberta Environment and Protected Areas, municipal development permit conditions) to References or Conditions table; Datasheet mentions "flood fringe" and "8 acres non-buildable" but does not identify the regulatory authority governing flood hazard compliance for the buildable portion | Exhaustive regulatory jurisdiction requires identifying all applicable regulatory bodies; the site has significant flood hazard constraints (8 of 20 acres) but no document identifies the regulatory authority or development permit conditions that govern building on the remaining 12 acres adjacent to a flood fringe | Datasheet.md | Construction > Site Context; References | -- | Municipal planning / Alberta Environment | TBD |
| E-002 | E:evaluative:completeness | Normalization | Multi | Guidance | Clarify interface between DEL-03-01 architectural brief and PKG-004 (Sustainability and Energy) deliverables: the brief addresses solar-capable roof orientation but does not cross-reference DEL-04-01 (Building Envelope and Energy Strategy) which also addresses envelope decisions; add cross-reference note to avoid evaluator confusion about which deliverable owns envelope energy strategy vs. architectural envelope design intent | Exhaustive value jurisdiction requires clear ownership boundaries for all value-bearing topics; the brief's exterior elevation section (ARCH-F03) discusses material palette and solar orientation, which overlaps with PKG-004 energy strategy scope; no cross-reference exists to DEL-04-01 despite both discussing building envelope decisions | Specification.md; Guidance.md | Specification > Requirements > ARCH-F03; Guidance > C-002 scope boundary table | -- | Lead Architect / Proposal Manager | TBD |
