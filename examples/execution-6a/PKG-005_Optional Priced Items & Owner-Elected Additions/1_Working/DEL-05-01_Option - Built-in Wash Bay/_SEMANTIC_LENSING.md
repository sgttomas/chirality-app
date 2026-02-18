# Semantic Lensing Register: DEL-05-01 Option -- Built-in Wash Bay

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-005_Optional Priced Items & Owner-Elected Additions/1_Working/DEL-05-01_Option - Built-in Wash Bay/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-05-01_Optional-Wash-Bay (PKG-005, Multi-discipline, SOW-0500, OBJ-010)
- _STATUS.md -- Current State: SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md -- Matrices A, B, C, F, D, X, E parsed (7 matrices, 92 cells total)
- Datasheet.md -- Present; Identification, Attributes, Conditions, Construction, Anticipated Artifacts, References
- Specification.md -- Present; Scope, Requirements REQ-WB-01 through REQ-WB-11, Standards, Verification, Documentation
- Guidance.md -- Present; Purpose, Principles (5), Considerations (4 areas), Trade-offs (3), Conflict Table (3 entries)
- Procedure.md -- Present; Prerequisites, Steps (Phase A: 1-7, Phase B: 8-13), Verification, Records
- _REFERENCES.md -- Present; OSR Appendix A (section 12.1), Addendum 03 (section 1.9)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 3
  - Specification: 13
  - Guidance: 4
  - Procedure: 4
  - Multi: 4
- By matrix:
  - A: 5  B: 5  C: 3  F: 4  D: 3  X: 5  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 6
  - MissingSlot: 8
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Ventilation requirement lacks prescriptive basis |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Environmental compliance tagged ASSUMPTION with no code citation |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Standards table references are all "location TBD" |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure Step 9 addresses regulatory confirmation adequately |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear procedural direction through Steps 1-7 and 8-13 |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | No HVAC-specific step in Procedure Phase A |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure provides adequate assessment checkpoints |
| A:operative:reviewing | operative | reviewing | process audit | 1 | HAS_ITEMS | No internal QA review gate before proposal submission |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section provides clear value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance Pricing Transparency section addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs in Guidance adequately frame worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Step 7 internal consistency check covers quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | MissingSlot | Specification | Specification | Add a requirement (or TBD placeholder) for wash bay ventilation citing applicable code section | Ventilation is listed in Datasheet Construction table as "TBD (ASSUMPTION)" and discussed in Guidance Considerations but has no corresponding requirement in Specification. A prescriptive direction is missing. | Datasheet.md, Specification.md, Guidance.md | Datasheet#Construction (Ventilation row); Guidance#HVAC and Moisture Management; Specification#Requirements (absent) | -- | Specification.md | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Strengthen REQ-WB-11 by citing the specific Alberta regulation or removing the ASSUMPTION tag once confirmed | REQ-WB-11 (Environmental Compliance) is entirely tagged as ASSUMPTION and references "AEP requirements if applicable." This makes the mandatory practice ambiguous -- it is unclear whether this is an actual enforceable requirement or speculative. | Specification.md | Specification#REQ-WB-11 | -- | Specification.md | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add accessibility information for referenced standards (ABC, NPC, AEP regs, CSA/UL) or record as TBD pending sourcing | All five entries in the Standards table have "location TBD" for accessibility. Without accessible standard texts, compliance determination cannot be substantiated. | Specification.md | Specification#Standards | -- | Specification.md | TBD |
| A-004 | A:operative:applying | MissingSlot | Procedure | Procedure | Add a step in Phase A addressing HVAC/ventilation design input requirements for the wash bay concept | Guidance identifies HVAC and moisture management as a multi-discipline consideration, but Procedure Phase A has no explicit step for developing or documenting HVAC requirements as a design input. | Procedure.md, Guidance.md | Procedure#Phase A (missing); Guidance#HVAC and Moisture Management | -- | Procedure.md | TBD |
| A-005 | A:operative:reviewing | MissingSlot | Procedure | Procedure | Add a formal review/approval gate (e.g., discipline lead sign-off) before proposal submission in Phase A | Procedure Step 7 describes an internal consistency check but does not specify who reviews, who approves, or what constitutes a pass/fail for the review gate. | Procedure.md | Procedure#Step 7 | -- | Procedure.md | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Water supply sizing is essential but TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Wash equipment type/spec entirely TBD |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet provides comprehensive record of known facts and TBDs |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Vehicle dimension units inconsistent |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Wastewater disposal path unresolved |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context across documents provides adequate framing |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents collectively provide comprehensive account |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance provides adequate fundamental understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Procedure prerequisites identify required expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Combined documents provide thorough coverage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs provide essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Conflict table and trade-offs provide adequate judgment inputs |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic insight into the option |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: water supply flow rate and pressure requirements for wash bay (consult mechanical discipline lead and wash equipment vendor) | Water supply is listed as TBD in Datasheet Attributes. This is an essential fact needed for both pricing and concept development but cannot be determined without equipment selection. | Datasheet.md | Datasheet#Attributes (Water supply row) | -- | Design-Builder mechanical lead | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Datasheet | Datasheet | Record TBD: wash equipment type, capacity, and specification (consult wash equipment vendors or municipal fleet wash specialists) | Wash equipment is described as "type and specification: TBD" in Datasheet Attributes and "proposed by the Design-Builder" in Specification REQ-WB-04. No evidence base exists for equipment selection at this stage. | Datasheet.md, Specification.md | Datasheet#Attributes (Equipment specifics); Specification#REQ-WB-04 | -- | Design-Builder | TBD |
| B-003 | B:data:consistency | Normalization | Multi | Guidance | Normalize vehicle dimension notation format across documents (e.g., consistently use H x W x L with units) | Datasheet uses "9'9" wide" and "10'5" T" while Specification REQ-WB-05 uses "9'9" T x 9'9" W x 26'L". The "T" abbreviation is used inconsistently (sometimes meaning height, sometimes unclear). Guidance uses "30'L, 14'W". Standardize to a single convention. | Datasheet.md, Specification.md, Guidance.md | Datasheet#Attributes (vehicle dimensions); Specification#REQ-WB-05; Guidance#Sizing Considerations | -- | Guidance.md (vocabulary note) | TBD |
| B-004 | B:information:necessity | TBD_Question | Multi | Specification | Record TBD: confirm whether municipal sanitary sewer tie-in is available and permitted for wash bay effluent (consult Town of Penhold and AEP) | The effluent disposal path is identified as unresolved in Guidance and flagged as CONF-WB-03 in the Conflict Table. This is an essential signal that drives the entire containment concept design. | Guidance.md, Specification.md | Guidance#Drainage and Effluent Management; Guidance#Conflict Table CONF-WB-03; Specification#REQ-WB-08 | -- | Owner/DB to confirm with Town and AEP | TBD |
| B-005 | B:information:consistency | Normalization | Multi | Guidance | Standardize terminology: "wash bay" vs "vehicle wash bay" vs "built-in wash bay" -- adopt one canonical term and use consistently | Documents use varying terms: "Built-in Wash Bay" (title), "vehicle wash bay" (Guidance Purpose), "wash bay" (most usage), "permanent washing facilities" (quoting OSR). While contextually clear, the canonical deliverable term should be established for consistency. | Datasheet.md, Specification.md, Guidance.md, Procedure.md | entire document scanned (all four documents) | -- | Guidance.md | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Obligation | 1 | HAS_ITEMS | Code compliance requirement lacks specific code sections |
| C:normative:sufficiency | normative | sufficiency | Certified Authorization | 0 | NO_ITEMS | Authorization pathway adequately described |
| C:normative:completeness | normative | completeness | Comprehensive Regulatory Coverage | 1 | HAS_ITEMS | Missing fire code consideration |
| C:normative:consistency | normative | consistency | Harmonized Conformance | 0 | NO_ITEMS | Conformance approach is consistent |
| C:operative:necessity | operative | necessity | Essential Process Input | 0 | NO_ITEMS | Essential process inputs identified in Procedure prerequisites |
| C:operative:sufficiency | operative | sufficiency | Competent Execution | 0 | NO_ITEMS | Procedure steps provide adequate execution guidance |
| C:operative:completeness | operative | completeness | Exhaustive Operational Mastery | 0 | NO_ITEMS | Operational coverage is adequate for proposal stage |
| C:operative:consistency | operative | consistency | Standardized Practice | 0 | NO_ITEMS | Practice is standardized across procedure steps |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Worth Assessment | 0 | NO_ITEMS | Guidance Purpose establishes intrinsic worth |
| C:evaluative:sufficiency | evaluative | sufficiency | Qualified Merit Evaluation | 1 | HAS_ITEMS | No lifecycle cost evaluation framework |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Worth Appraisal | 0 | NO_ITEMS | Trade-offs provide comprehensive appraisal |
| C:evaluative:consistency | evaluative | consistency | Coherent Quality Standard | 0 | NO_ITEMS | Quality standards are coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-WB-10 by citing specific Alberta Building Code sections applicable to wash bay occupancy, plumbing, and ventilation (or record as TBD pending code review) | REQ-WB-10 requires "compliance with applicable Alberta Building Code" but does not cite specific ABC sections. This weakens the regulatory obligation because the scope of code applicability is undefined. | Specification.md | Specification#REQ-WB-10 | -- | Specification.md | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add consideration of fire code requirements for an enclosed wash bay (fire separation from adjacent bays, sprinkler requirements, hazardous area classification if wash chemicals stored) | No document addresses fire code or fire separation requirements for the wash bay. An enclosed bay with water, chemicals, and potential hydrocarbon-contaminated effluent may require fire code consideration under ABC. | Specification.md, Guidance.md | Specification#Standards (absent); Guidance#Considerations (absent) | -- | Specification.md | TBD |
| C-003 | C:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add guidance on lifecycle cost considerations for the wash bay option (e.g., operating cost of recirculating vs once-through, maintenance costs, consumables) to support Owner's election decision | Trade-off 3 (recirculating vs once-through) mentions "lifecycle cost" but provides no framework or even qualitative guidance for how the Owner or DB should evaluate lifecycle costs. The Owner's election decision would benefit from this context. | Guidance.md | Guidance#Trade-off 3 | -- | Guidance.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Compulsory Compliance Proof | 1 | HAS_ITEMS | No proof mechanism for code compliance at proposal stage |
| F:normative:sufficiency | normative | sufficiency | Warranted Compliance Evidence | 0 | NO_ITEMS | Verification table provides adequate evidence approach |
| F:normative:completeness | normative | completeness | Complete Governance Documentation | 0 | NO_ITEMS | Documentation section is complete |
| F:normative:consistency | normative | consistency | Disciplined Compliance Measure | 0 | NO_ITEMS | Compliance measures are disciplined and consistent |
| F:operative:necessity | operative | necessity | Baseline Workflow Imperative | 1 | HAS_ITEMS | Missing hot water requirement |
| F:operative:sufficiency | operative | sufficiency | Functional Method Competence | 0 | NO_ITEMS | Methods described are functionally competent |
| F:operative:completeness | operative | completeness | Exhaustive Method Documentation | 1 | HAS_ITEMS | Phase B steps lack detail for commissioning acceptance |
| F:operative:consistency | operative | consistency | Stable Process Indicator | 0 | NO_ITEMS | Process indicators are stable |
| F:evaluative:necessity | evaluative | necessity | Fundamental Value Evidence | 0 | NO_ITEMS | Value evidence established through separable pricing structure |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Worth Proof | 1 | HAS_ITEMS | Pricing sheet structure guidance lacks Owner comparison framework |
| F:evaluative:completeness | evaluative | completeness | Integral Evaluation Authority | 0 | NO_ITEMS | Evaluation authority adequately described |
| F:evaluative:consistency | evaluative | consistency | Harmonized Assessment Standard | 0 | NO_ITEMS | Assessment standard is harmonized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add verification approach for REQ-WB-10 and REQ-WB-11 that specifies what constitutes sufficient compliance proof at proposal stage vs post-award stage | Verification table entries for REQ-WB-10 and REQ-WB-11 say "Confirm DB's design basis statement references ABC" and "Confirm DB's containment concept addresses effluent management." These are weak verification methods -- they check for mention of compliance, not evidence of compliance. | Specification.md | Specification#Verification (REQ-WB-10 and REQ-WB-11 rows) | -- | Specification.md | TBD |
| F-002 | F:operative:necessity | MissingSlot | Specification | Specification | Add a requirement for hot water supply to the wash bay (or record as TBD pending equipment selection) | Datasheet Construction table lists "Hot/cold water supply" under Mechanical/plumbing. Guidance Examples section mentions "hot water supply" as typical. However, no Specification requirement explicitly requires hot water. For a permanent wash facility in a cold climate, hot water is a baseline workflow imperative. | Datasheet.md, Specification.md, Guidance.md | Datasheet#Construction (Mechanical/plumbing); Guidance#Examples; Specification#Requirements (absent) | -- | Specification.md | TBD |
| F-003 | F:operative:completeness | VerificationGap | Procedure | Procedure | Add commissioning acceptance criteria (pass/fail thresholds) for wash equipment performance test, drainage flow test, and containment integrity test in Step 13 | Procedure Step 13 lists commissioning activities (test wash equipment, test drainage, verify no water escape) but does not define acceptance criteria or pass/fail thresholds. Without these, commissioning results cannot be objectively evaluated. | Procedure.md | Procedure#Step 13 | -- | Procedure.md | TBD |
| F-004 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add guidance on how the Owner should evaluate the wash bay option price (e.g., comparison to external commercial wash service costs, or value of operational convenience) | Guidance Pricing Transparency section describes what the pricing sheet should contain but does not explain how the Owner should evaluate whether the price represents good value. This gap makes the defensible worth proof incomplete. | Guidance.md | Guidance#Pricing Transparency | -- | Guidance.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Authoritative Conformance Mandate | 0 | NO_ITEMS | Conformance mandate adequately established through requirements |
| D:normative:applying | normative | applying | Compulsory Regulatory Fulfillment | 0 | NO_ITEMS | Regulatory fulfillment pathway described |
| D:normative:judging | normative | judging | Conclusive Conformance Finding | 1 | HAS_ITEMS | No definitive conformance acceptance gate |
| D:normative:reviewing | normative | reviewing | Systematic Adherence Examination | 0 | NO_ITEMS | Step 7 and verification checks provide systematic examination |
| D:operative:guiding | operative | guiding | Established Methodical Guidance | 0 | NO_ITEMS | Procedure provides established methodical guidance |
| D:operative:applying | operative | applying | Validated Working Performance | 1 | HAS_ITEMS | No performance criteria for wash system capacity |
| D:operative:judging | operative | judging | Definitive Execution Evidence | 0 | NO_ITEMS | Verification table provides execution evidence checkpoints |
| D:operative:reviewing | operative | reviewing | Systematic Workflow Benchmark | 0 | NO_ITEMS | Procedure verification checks serve as workflow benchmarks |
| D:evaluative:guiding | evaluative | guiding | Principled Merit Direction | 0 | NO_ITEMS | Guidance principles provide merit direction |
| D:evaluative:applying | evaluative | applying | Validated Merit Realization | 1 | HAS_ITEMS | No mechanism to validate that the elected option delivers promised value |
| D:evaluative:judging | evaluative | judging | Conclusive Value Determination | 0 | NO_ITEMS | Trade-offs and conflict table provide value determination framework |
| D:evaluative:reviewing | evaluative | reviewing | Established Quality Examination | 0 | NO_ITEMS | Step 7 quality check is adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Specification | Add an explicit Owner acceptance/approval gate for the wash bay deliverable package before it is finalized in the proposal | Specification Verification table describes review methods but does not identify who performs the conformance review or what constitutes formal acceptance of the deliverable package. There is no conclusive conformance finding mechanism. | Specification.md | Specification#Verification | -- | Specification.md | TBD |
| D-002 | D:operative:applying | VerificationGap | Specification | Specification | Add performance criteria for wash system (e.g., minimum water pressure, flow rate, wash coverage area) or record as TBD pending equipment selection | REQ-WB-04 requires wash equipment be included but specifies no performance parameters. Without minimum performance criteria, validated working performance cannot be confirmed. | Specification.md | Specification#REQ-WB-04 | -- | Specification.md | TBD |
| D-003 | D:evaluative:applying | MissingSlot | Procedure | Procedure | Add a post-commissioning operational validation step (e.g., wash a representative fleet vehicle and confirm functionality, drainage, and containment under real conditions) | Procedure Step 13 tests equipment and containment but does not include a real-world operational validation with an actual fleet vehicle. This would provide validated merit realization evidence. | Procedure.md | Procedure#Step 13 | -- | Procedure.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Mandatory Governance Basis | 0 | NO_ITEMS | Governance basis established through OSR and SOW references |
| X:guiding:sufficiency | guiding | sufficiency | Warranted Directed Capability | 0 | NO_ITEMS | Directed capability adequately warranted |
| X:guiding:completeness | guiding | completeness | Comprehensive Mandate Leadership | 1 | HAS_ITEMS | Missing lighting requirement for wash bay |
| X:guiding:consistency | guiding | consistency | Harmonized Procedural Governance | 0 | NO_ITEMS | Procedural governance is harmonized |
| X:applying:necessity | applying | necessity | Mandatory Compliance Execution | 1 | HAS_ITEMS | Drainage compliance execution path unresolved |
| X:applying:sufficiency | applying | sufficiency | Confirmed Working Capability | 0 | NO_ITEMS | Working capability adequately confirmed through procedure |
| X:applying:completeness | applying | completeness | Exhaustive Performance Confirmation | 1 | HAS_ITEMS | No performance confirmation for containment system capacity |
| X:applying:consistency | applying | consistency | Consistent Compliance Discipline | 0 | NO_ITEMS | Compliance discipline is consistent |
| X:judging:necessity | judging | necessity | Mandatory Performance Verdict | 1 | HAS_ITEMS | No pass/fail criteria for concept layout review |
| X:judging:sufficiency | judging | sufficiency | Substantiated Compliance Finding | 0 | NO_ITEMS | Compliance findings are substantiated through verification table |
| X:judging:completeness | judging | completeness | Exhaustive Compliance Determination | 0 | NO_ITEMS | Compliance determination is adequately exhaustive |
| X:judging:consistency | judging | consistency | Stable Compliance Verdict | 0 | NO_ITEMS | Verdict framework is stable |
| X:reviewing:necessity | reviewing | necessity | Mandatory Compliance Scrutiny | 0 | NO_ITEMS | Scrutiny mechanisms present |
| X:reviewing:sufficiency | reviewing | sufficiency | Warranted Compliance Inspection | 1 | HAS_ITEMS | Inspection of base-scope vs option-scope boundary unclear |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Compliance Audit | 0 | NO_ITEMS | Audit coverage is adequate |
| X:reviewing:consistency | reviewing | consistency | Consistent Compliance Monitoring | 0 | NO_ITEMS | Monitoring is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Specification | Specification | Add a requirement for wash bay lighting (task lighting appropriate for wash operations, GFCI protection for wet location) or reference base building lighting standard | Datasheet Construction table mentions "lighting" under Electrical with "details TBD." Procedure Step 10 mentions "lighting" in detailed design drawings. However, no Specification requirement addresses wash bay lighting. For a permanent enclosed wash bay, task lighting is a necessary element for comprehensive mandate leadership. | Datasheet.md, Specification.md | Datasheet#Construction (Electrical row); Specification#Requirements (absent) | -- | Specification.md | TBD |
| X-002 | X:applying:necessity | Conflict | Multi | TBD | Clarify whether wash bay effluent can connect to the wastewater stub at the site corner (Addendum 03 section 1.6) or requires an independent disposal system | Datasheet references wastewater as TBD. Specification REQ-WB-08 requires the DB to propose an effluent management strategy. Guidance identifies this as unresolved (CONF-WB-03). Addendum 03 section 1.6 notes water and wastewater are stubbed at the site corner, but it is unclear whether this wastewater connection is available for wash bay effluent. | Datasheet.md, Specification.md, Guidance.md | Datasheet#Attributes (Wastewater/drainage); Specification#REQ-WB-08; Guidance#Conflict Table CONF-WB-03 | Datasheet#Attributes vs Guidance#CONF-WB-03 (unresolved disposal path) | Owner/Town of Penhold and AEP | TBD |
| X-003 | X:applying:completeness | VerificationGap | Specification | Specification | Add verification criteria for containment system capacity (e.g., containment volume relative to wash water volume, overflow prevention) | REQ-WB-03 requires containment but specifies no capacity or sizing criteria. Verification approach says "Review containment concept narrative" but does not define what adequate containment looks like quantitatively. | Specification.md | Specification#REQ-WB-03; Specification#Verification (REQ-WB-03 row) | -- | Specification.md | TBD |
| X-004 | X:judging:necessity | WeakStatement | Specification | Specification | Strengthen verification approach for REQ-WB-05 by specifying minimum clearance dimensions (e.g., minimum side clearance, minimum overhead clearance above tallest vehicle) | Verification for REQ-WB-05 says "Review concept layout against fleet vehicle dimensions; confirm clearances" but does not define what clearances are acceptable. Without pass/fail thresholds, the performance verdict is subjective. | Specification.md | Specification#Verification (REQ-WB-05 row) | -- | Specification.md | TBD |
| X-005 | X:reviewing:sufficiency | WeakStatement | Guidance | Guidance | Clarify the base-scope vs option-scope boundary definition with specific examples (e.g., is the overhead door base-scope or option-scope? is the sump base-scope?) | Guidance Principle 5 and Interaction with Base Building section discuss the base/option boundary conceptually but do not provide a definitive boundary list. Procedure Step 8 says "Confirm the exact scope boundary" but the boundary definition itself is ambiguous. | Guidance.md, Procedure.md | Guidance#Principle 5; Guidance#Interaction with Base Building; Procedure#Step 8 | -- | Guidance.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Enforced Regulatory Foundation | 1 | HAS_ITEMS | Regulatory foundation not fully enforced due to ASSUMPTION tags |
| E:normative:sufficiency | normative | sufficiency | Validated Governance Capability | 0 | NO_ITEMS | Governance capability adequately validated |
| E:normative:completeness | normative | completeness | Absolute Compliance Command | 0 | NO_ITEMS | Compliance command is comprehensive within known scope |
| E:normative:consistency | normative | consistency | Coherent Regulatory Discipline | 0 | NO_ITEMS | Regulatory discipline is coherent |
| E:operative:necessity | operative | necessity | Essential Procedural Authority | 0 | NO_ITEMS | Procedural authority established |
| E:operative:sufficiency | operative | sufficiency | Validated Operational Capacity | 0 | NO_ITEMS | Operational capacity validated through procedure |
| E:operative:completeness | operative | completeness | Total Operational Command | 1 | HAS_ITEMS | Missing floor finish specification |
| E:operative:consistency | operative | consistency | Stable Execution Discipline | 0 | NO_ITEMS | Execution discipline is stable |
| E:evaluative:necessity | evaluative | necessity | Foundational Merit Authority | 0 | NO_ITEMS | Merit authority established |
| E:evaluative:sufficiency | evaluative | sufficiency | Validated Merit Capacity | 0 | NO_ITEMS | Merit capacity adequately validated |
| E:evaluative:completeness | evaluative | completeness | Absolute Quality Command | 1 | HAS_ITEMS | No warranty/deficiency period specified for wash equipment |
| E:evaluative:consistency | evaluative | consistency | Coherent Merit Discipline | 0 | NO_ITEMS | Merit discipline is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:necessity | RationaleGap | Guidance | Guidance | Add rationale explaining why REQ-WB-10 and REQ-WB-11 are tagged as ASSUMPTION and what confirmation steps are needed to convert them to confirmed requirements | Multiple specification requirements (REQ-WB-10, REQ-WB-11) are tagged ASSUMPTION without Guidance explaining the rationale for the uncertainty or the path to resolution. The enforced regulatory foundation is weakened when the regulatory basis itself is uncertain. | Specification.md, Guidance.md | Specification#REQ-WB-10; Specification#REQ-WB-11; Guidance (absent rationale) | -- | Guidance.md | TBD |
| E-002 | E:operative:completeness | TBD_Question | Datasheet | Datasheet | Record TBD: wash bay floor finish specification (e.g., sealed concrete, epoxy coating, non-slip treatment) -- consult with architectural/structural discipline lead | Datasheet Construction table mentions "surface suitable for wet operations" for the floor/slab but does not specify a floor finish. Guidance Examples section mentions "epoxy or sealed surface" as typical. A floor finish specification is needed for total operational command. | Datasheet.md, Guidance.md | Datasheet#Construction (Floor/slab row); Guidance#Examples | -- | Design-Builder | TBD |
| E-003 | E:evaluative:completeness | MissingSlot | Specification | Specification | Add a requirement or TBD placeholder for warranty period and deficiency management for wash bay equipment and containment system | No document addresses warranty requirements for the wash bay option. Procedure Records section mentions commissioning records but not warranty documentation. For absolute quality command, warranty terms should be established. | Specification.md, Procedure.md | Specification#Requirements (absent); Procedure#Records (absent) | -- | Specification.md | TBD |
