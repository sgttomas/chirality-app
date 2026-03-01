# Semantic Lensing Register: DEL-008-03 Construction Survey

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-008_Geotechnical Investigation & Surveying/1_Working/DEL-008-03_Construction-Survey/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-008-03 Context (Deliverable Identity, Description, Scope)
- _STATUS.md -- DEL-008-03 Status (State: SEMANTIC_READY)
- _SEMANTIC.md -- DEL-008-03 Semantic Matrices (A, B, C, F, D, X, E parsed)
- Datasheet.md -- DEL-008-03 Construction Survey Datasheet (Identification, Attributes, Conditions, Construction)
- Specification.md -- DEL-008-03 Construction Survey Specification (Scope, Requirements REQ-008-03-01 through -10, Standards, Verification)
- Guidance.md -- DEL-008-03 Construction Survey Guidance (Purpose, Principles, Considerations, Trade-offs)
- Procedure.md -- DEL-008-03 Construction Survey Procedure (Prerequisites, Steps Phases A-D, Verification, Records)
- _REFERENCES.md -- DEL-008-03 References (Document References, Related Deliverables, Standards)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 3
  - Specification: 14
  - Guidance: 2
  - Procedure: 6
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 4
- By type:
  - Conflict: 0
  - VerificationGap: 8
  - MissingSlot: 5
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Accuracy tolerances TBD weakens prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | IFC requirement before staking is well-covered; accuracy tolerance gap affects mandatory practice |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Standards section relies on assumptions; compliance basis incomplete |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | County inspection requirements covered in Guidance and Procedure |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Phases A-D provide clear procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Survey methodology not specified beyond TBD |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Closure tolerances TBD in Procedure Step A2 |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Verification table in Procedure covers process audit checkpoints |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section adequately explains value proposition |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance trade-offs provide reasonable merit application context |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Documents adequately position the survey's worth relative to downstream construction |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification checklist in Procedure provides quality appraisal framework |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Define horizontal and vertical accuracy tolerances for construction survey, or reference the standard that governs them | The prescriptive direction lens reveals that the core normative guidance for this survey -- accuracy tolerances -- is explicitly TBD in both Specification (REQ-008-03-06) and Datasheet (Accuracy and Standards table). Without tolerances, the prescriptive direction is incomplete. | Specification.md; Datasheet.md | REQ-008-03-06 (Accuracy Tolerances: TBD); Conditions > Accuracy and Standards | -- | Licensed Surveyor / Alberta survey practice standards | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify whether "tolerances established in the survey plan" (REQ-008-03-06) creates a normative obligation or a delegated discretion for the Surveyor | REQ-008-03-06 states field verification checks against "tolerances established in the survey plan," but the survey plan itself is TBD. This creates a circular reference: the mandatory practice depends on a plan that has no specified minimum content for tolerances. | Specification.md | REQ-008-03-06 | -- | Surveyor / Design-Builder | TBD |
| A-003 | A:normative:judging | TBD_Question | Specification | Specification | Record TBD: Confirm specific Alberta survey standards and clause-level requirements applicable to construction survey compliance determination | The Standards section lists five standards/frameworks, all marked as "ASSUMPTION: likely applicable" or with clause-level requirements "TBD pending confirmation." Compliance determination cannot be performed without confirmed applicability. | Specification.md | Standards | -- | Licensed Surveyor / Alberta Land Surveyors Association | TBD |
| A-004 | A:operative:applying | WeakStatement | Procedure | Procedure | Clarify survey methodology selection criteria in Step A3 (total station, GNSS, or combination) -- add decision criteria or reference a methodology selection standard | Step A3 lists methodology options ("total station, GNSS, or combination") but provides no decision criteria or minimum requirements. Practical execution depends on methodology choice affecting accuracy achievable. | Procedure.md | Phase A > Step A3 | -- | Surveyor | TBD |
| A-005 | A:operative:judging | VerificationGap | Procedure | Procedure | Add specific closure tolerance thresholds or reference to standard for control verification check in Step A2 | Step A2 requires a "closure or redundant check" but notes "Specific closure tolerances are TBD." Performance assessment of the control verification cannot be made without a pass/fail criterion. | Procedure.md | Phase A > Step A2 | -- | Surveyor / Alberta survey practice | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Coordinate datum not explicitly stated |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet provides adequate evidence for site, upstream inputs, and building elements |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet artifact list is assumption-based |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Coordinate system / datum not specified |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Upstream dependency signals adequately documented |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context documents provide adequate framing |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Four documents together provide comprehensive account |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents are internally consistent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance principles demonstrate fundamental understanding of survey practice |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Trade-offs reflect competent expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Documents cover full survey lifecycle |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Geotech-foundation timing discernment could be stronger in Specification |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Guidance trade-offs show adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic view of survey context |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning across documents is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add essential datum: specify the geodetic datum and coordinate system (e.g., NAD83 CSRS, UTM Zone 12N) for all survey control | The essential fact for any construction survey is the coordinate reference system. Neither Datasheet nor Specification names the geodetic datum, projection, or vertical datum to be used. This is a fundamental data requirement for survey traceability. | Datasheet.md; Specification.md | Datasheet > Key Site Information; Specification > entire document scanned | -- | Licensed Surveyor / DEL-008-02 Preliminary Survey | TBD |
| B-002 | B:data:completeness | WeakStatement | Datasheet | Datasheet | Strengthen artifact list from ASSUMPTION to confirmed list, or mark as provisional pending Construction Manager input | The Datasheet Anticipated Artifacts section is explicitly marked as ASSUMPTION. The comprehensive record of expected deliverables from this survey is not confirmed by any authority. | Datasheet.md | Construction > Anticipated Artifacts | -- | Construction Manager / County | TBD |
| B-003 | B:data:consistency | Normalization | Multi | Datasheet | Standardize coordinate reference: add datum and coordinate system declaration to Datasheet Key Site Information; reference from Specification and Procedure | Datasheet provides a Plus Code and legal description but no geodetic datum. Procedure references "control point coordinates" without specifying the system. Consistent measurement requires a declared datum. | Datasheet.md; Procedure.md | Datasheet > Key Site Information; Procedure > Step A1 | -- | Surveyor / DEL-008-02 | TBD |
| B-004 | B:wisdom:necessity | RationaleGap | Specification | Guidance | Add rationale in Guidance for how the geotech-dependent foundation timing (RFP 4.8.2) should influence the survey plan phasing and re-staking provisions | Specification REQ-008-03-02 requires IFC drawings before staking, and Guidance Trade-off 3 discusses the problem, but the Specification itself does not address re-staking provisions or phased staking. The essential discernment about sequencing risk needs clearer normative-to-operational linkage. | Specification.md; Guidance.md | REQ-008-03-02; Trade-off 3 | -- | Design-Builder / Surveyor | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Imperative | 1 | HAS_ITEMS | Enforceability weakened by TBD tolerances |
| C:normative:sufficiency | normative | sufficiency | Prescribed Adequacy | 0 | NO_ITEMS | REQ-008-03-01 through -10 collectively establish prescribed adequacy |
| C:normative:completeness | normative | completeness | Exhaustive Mandate | 1 | HAS_ITEMS | Missing requirement for survey data retention period |
| C:normative:consistency | normative | consistency | Codified Uniformity | 0 | NO_ITEMS | Requirements are internally consistent; no codified conflicts |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | Prerequisites table in Procedure is comprehensive |
| C:operative:sufficiency | operative | sufficiency | Capable Execution | 0 | NO_ITEMS | Steps are detailed enough for capable execution |
| C:operative:completeness | operative | completeness | Thorough Operational Coverage | 0 | NO_ITEMS | Procedure covers mobilization through handoff |
| C:operative:consistency | operative | consistency | Dependable Method | 0 | NO_ITEMS | Procedure steps are methodologically consistent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Worth | 0 | NO_ITEMS | Guidance Purpose clearly establishes intrinsic worth |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit | 0 | NO_ITEMS | Value case is substantiated through source references |
| C:evaluative:completeness | evaluative | completeness | Holistic Valuation | 1 | HAS_ITEMS | Missing cost/schedule impact context |
| C:evaluative:consistency | evaluative | consistency | Calibrated Worth | 0 | NO_ITEMS | Worth assessment is calibrated and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add enforceable acceptance criteria for accuracy tolerances in REQ-008-03-06, or add a requirement that the survey plan must define tolerances before field work commences | The Enforceable Imperative lens highlights that REQ-008-03-06 contains no enforceable numeric threshold. The verification approach ("compare to tolerances in survey plan") cannot be enforced until the survey plan exists. A requirement that the plan must be approved before field work would close this gap. | Specification.md | REQ-008-03-06; Verification table | -- | Surveyor / Design-Builder | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add requirement for survey record retention period consistent with contract guarantee period and Alberta professional obligations | The Exhaustive Mandate lens reveals no requirement for how long survey records must be retained. REQ-008-03-08 requires documentation but does not address retention. The RFP guarantee period (RFP 2.10) may impose an implied retention need. | Specification.md; Procedure.md | REQ-008-03-08; Procedure > Records | -- | Contract / CCDC 14-2013 / Alberta Land Surveyors Act | TBD |
| C-003 | C:evaluative:completeness | MissingSlot | Guidance | Guidance | Add consideration of cost/schedule impact if survey errors propagate to rework, to complete the holistic valuation of this deliverable | The Holistic Valuation lens notes that Guidance discusses error consequences qualitatively (Principle 1, Considerations) but does not frame the cost/schedule risk. For a fixed-deadline project, quantifying rework risk supports decision-making about survey frequency and accuracy investment. | Guidance.md | Considerations; Trade-offs | -- | Construction Manager / Design-Builder | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandated Obligation | 1 | HAS_ITEMS | Core mandated obligations present but delegation chain incomplete |
| F:normative:sufficiency | normative | sufficiency | Qualified Conformance | 1 | HAS_ITEMS | Conformance qualification depends on unconfirmed standards |
| F:normative:completeness | normative | completeness | Exhaustive Governance | 0 | NO_ITEMS | Requirements cover governance scope adequately |
| F:normative:consistency | normative | consistency | Unified Codification | 0 | NO_ITEMS | Codification is internally unified |
| F:operative:necessity | operative | necessity | Critical Operating Condition | 0 | NO_ITEMS | Prerequisites adequately capture critical operating conditions |
| F:operative:sufficiency | operative | sufficiency | Validated Proficiency | 0 | NO_ITEMS | Procedure steps demonstrate validated proficiency approach |
| F:operative:completeness | operative | completeness | Total Process Command | 1 | HAS_ITEMS | Missing explicit hold/release gate for foundation staking |
| F:operative:consistency | operative | consistency | Integrated Reliability | 0 | NO_ITEMS | Process reliability is integrated across phases |
| F:evaluative:necessity | evaluative | necessity | Essential Value Basis | 0 | NO_ITEMS | Value basis established in Guidance |
| F:evaluative:sufficiency | evaluative | sufficiency | Grounded Assessment | 0 | NO_ITEMS | Assessment is grounded in source references |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Worth Authority | 0 | NO_ITEMS | Worth authority addressed through document set |
| F:evaluative:consistency | evaluative | consistency | Principled Valuation | 1 | HAS_ITEMS | Terminology inconsistency for "survey plan" |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add requirement that the Construction Survey Plan (referenced in Procedure Step A3) must be reviewed/approved before field survey work commences | REQ-008-03-06 delegates tolerance definition to "the survey plan," and Procedure Step A3 describes creating it, but no Specification requirement mandates its production or approval. The mandated obligation chain is broken: the plan is mentioned but not required. | Specification.md; Procedure.md | REQ-008-03-06; Step A3 | -- | Design-Builder / Construction Manager | TBD |
| F-002 | F:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen Standards section: confirm applicability of each listed standard or remove ASSUMPTION tags once confirmed by Surveyor | The Qualified Conformance lens shows that four of five entries in the Standards table are marked ASSUMPTION or have clause-level requirements TBD. Conformance cannot be qualified against unconfirmed standards. | Specification.md | Standards | -- | Licensed Surveyor / Alberta Land Surveyors Association | TBD |
| F-003 | F:operative:completeness | MissingSlot | Procedure | Procedure | Add explicit hold/release gate in Procedure Phase B for foundation staking: require written confirmation that foundation IFC drawings are final before proceeding from preliminary to final foundation staking | Guidance Trade-off 3 and Procedure Step B3 both discuss the risk of staking before final foundation design, but the procedure does not include an explicit hold point or gate requiring confirmation. Total Process Command requires this gate to be formalized. | Procedure.md; Guidance.md | Step B3; Trade-off 3 | -- | Structural Engineer / Design-Builder | TBD |
| F-004 | F:evaluative:consistency | Normalization | Multi | Guidance | Standardize terminology: "Construction Survey Plan" (Procedure Step A3, Specification Documentation) vs. "survey plan" (REQ-008-03-06, Step C6) -- use consistent capitalized term throughout | The Principled Valuation lens reveals inconsistent naming: "Construction Survey Plan" appears as a formal artifact in Procedure Step A3 and Specification Documentation table, while lowercase "survey plan" appears in REQ-008-03-06 and Step C6. This risks ambiguity about whether these refer to the same document. | Specification.md; Procedure.md | REQ-008-03-06; Step A3; Step C6; Documentation table | -- | -- | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Directed Resolve | 0 | NO_ITEMS | Requirements and Guidance are directionally aligned |
| D:normative:applying | normative | applying | Enforced Adherence | 1 | HAS_ITEMS | Adherence enforcement weakened by TBD items |
| D:normative:judging | normative | judging | Conclusive Ruling | 0 | NO_ITEMS | Verification table provides basis for conclusive rulings |
| D:normative:reviewing | normative | reviewing | Mandated Inspection | 1 | HAS_ITEMS | Inspection hold points not enumerated |
| D:operative:guiding | operative | guiding | Resolved Operational Aim | 0 | NO_ITEMS | Operational aims are resolved in Procedure |
| D:operative:applying | operative | applying | Confirmed Implementation | 0 | NO_ITEMS | Steps provide confirmed implementation path |
| D:operative:judging | operative | judging | Conclusive Proficiency | 0 | NO_ITEMS | Verification checks support proficiency assessment |
| D:operative:reviewing | operative | reviewing | Confirmed Systematic Review | 0 | NO_ITEMS | Progress surveys and verification provide systematic review |
| D:evaluative:guiding | evaluative | guiding | Resolved Merit Purpose | 0 | NO_ITEMS | Purpose is well-resolved in Guidance |
| D:evaluative:applying | evaluative | applying | Realized Appraisal | 0 | NO_ITEMS | Trade-off analysis provides realized appraisal context |
| D:evaluative:judging | evaluative | judging | Definitive Worth | 0 | NO_ITEMS | Worth is adequately demonstrated |
| D:evaluative:reviewing | evaluative | reviewing | Grounded Quality Audit | 1 | HAS_ITEMS | Quality audit criteria for survey deliverables undefined |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add verification approach for REQ-008-03-09 (Completion Deadline) that specifies how survey schedule compliance is tracked and reported, beyond "tracked against construction schedule" | The Enforced Adherence lens reveals that REQ-008-03-09 verification ("tracked against construction schedule; reported through County project manager coordination") is vague. There is no defined mechanism for tracking or reporting survey schedule adherence. | Specification.md | REQ-008-03-09; Verification table | -- | Construction Manager / County PM | TBD |
| D-002 | D:normative:reviewing | MissingSlot | Specification | Procedure | Add enumerated list of survey-related inspection hold points requiring County project representative presence (per RFP 3.3.2) | The Mandated Inspection lens reveals that while Guidance (County Inspection Requirements) and Procedure (Step C7) reference County inspection requirements, neither document enumerates which specific survey milestones constitute inspection hold points. RFP 3.3.2 requires County presence at "all inspections." | Specification.md; Procedure.md; Guidance.md | Guidance > County Inspection Requirements; Procedure > Step C7; Specification > REQ-008-03-10 | -- | County PM / Construction Manager | TBD |
| D-003 | D:evaluative:reviewing | RationaleGap | Guidance | Guidance | Add quality acceptance criteria or quality review framework for assessing the overall quality of the construction survey deliverable package | The Grounded Quality Audit lens reveals no defined criteria for what constitutes a quality survey deliverable package. The Procedure verification table checks for existence of records but not for quality attributes (accuracy achieved, completeness of coverage, discrepancy resolution). | Guidance.md; Procedure.md | Guidance > entire document scanned; Procedure > Verification | -- | Surveyor / Design-Builder | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Focused Certainty | 1 | HAS_ITEMS | Certainty unfocused due to TBD accuracy targets |
| X:guiding:sufficiency | guiding | sufficiency | Purposeful Competence | 0 | NO_ITEMS | Competence requirements addressed through Surveyor role |
| X:guiding:completeness | guiding | completeness | Total Oriented Authority | 0 | NO_ITEMS | Authority scope is complete for this deliverable |
| X:guiding:consistency | guiding | consistency | Harmonized Aim | 0 | NO_ITEMS | Aims are harmonized across documents |
| X:applying:necessity | applying | necessity | Confirmed Operational Need | 1 | HAS_ITEMS | OH&S operational needs not detailed |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Adequacy | 0 | NO_ITEMS | Adequacy demonstrated through detailed steps |
| X:applying:completeness | applying | completeness | Total Confirmed Coverage | 1 | HAS_ITEMS | Missing slab drainage slope verification |
| X:applying:consistency | applying | consistency | Confirmed Fidelity | 0 | NO_ITEMS | Fidelity between documents is confirmed |
| X:judging:necessity | judging | necessity | Decisive Evidence | 0 | NO_ITEMS | Evidence requirements addressed in verification |
| X:judging:sufficiency | judging | sufficiency | Conclusive Justification | 0 | NO_ITEMS | Justification for requirements is conclusive with source citations |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication | 1 | HAS_ITEMS | Discrepancy resolution process incomplete |
| X:judging:consistency | judging | consistency | Principled Verdict | 0 | NO_ITEMS | Verdict criteria consistent where defined |
| X:reviewing:necessity | reviewing | necessity | Obligatory Discovery | 0 | NO_ITEMS | Discovery obligations covered through verification checks |
| X:reviewing:sufficiency | reviewing | sufficiency | Competent Audit Evidence | 0 | NO_ITEMS | Audit evidence requirements addressed |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Trail | 1 | HAS_ITEMS | Record numbering/indexing scheme absent |
| X:reviewing:consistency | reviewing | consistency | Traceable Alignment | 0 | NO_ITEMS | Traceability approach is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | VerificationGap | Specification | Specification | Add requirement that accuracy targets must be defined in the Construction Survey Plan and approved before field verification can be assessed as pass/fail | Focused Certainty requires defined targets for verification to function. REQ-008-03-06 Accuracy Tolerances are TBD. Without them, verification checks (Steps C1-C5) have no quantitative pass/fail threshold. | Specification.md | REQ-008-03-06 | -- | Surveyor | TBD |
| X-002 | X:applying:necessity | TBD_Question | Procedure | Procedure | Record TBD: Add OH&S prerequisites or safety considerations for survey field operations on an active landfill site | The Confirmed Operational Need lens reveals that while the Standards section references Alberta OH&S and Prime Contractor obligations, the Procedure contains no safety prerequisites or considerations for working on an active landfill site (heavy equipment, variable terrain, potential hazards). | Procedure.md; Specification.md | Procedure > Prerequisites; Specification > Standards | -- | Prime Contractor / OH&S | TBD |
| X-003 | X:applying:completeness | VerificationGap | Procedure | Procedure | Add explicit slab drainage slope verification step between Step C3 (Slab-on-Grade Grade Control) and slab pour, confirming slope direction matches civil grading design | Step C3 mentions "Confirm that slab drainage slopes (if any) are reflected in grade control" but this is phrased as a parenthetical. Given REQ-008-03-04 (positive drainage), slab drainage slope verification should be an explicit verification check with a record. | Procedure.md | Phase C > Step C3 | -- | Surveyor / Civil Engineer | TBD |
| X-004 | X:judging:completeness | WeakStatement | Specification | Specification | Clarify discrepancy resolution authority and process in REQ-008-03-04 and REQ-008-03-06: specify who has authority to accept, reject, or remediate discrepancies | REQ-008-03-04 states discrepancies "shall be reported to the civil design engineer and construction manager" and Step C1 says "do not proceed until resolved," but there is no defined resolution authority or escalation path. Exhaustive Adjudication requires a clear decision chain. | Specification.md; Procedure.md | REQ-008-03-04; Step C1 | -- | Construction Manager / Design-Builder | TBD |
| X-005 | X:reviewing:completeness | RationaleGap | Procedure | Procedure | Add record numbering or indexing convention to the Records table to support exhaustive audit trail traceability | The Records table lists 13 record types but provides no numbering convention, indexing scheme, or file naming convention. An exhaustive audit trail requires records to be systematically identifiable and retrievable. | Procedure.md | Records | -- | Surveyor / Construction Manager | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Reference Point | 1 | HAS_ITEMS | Reference point authority incomplete without datum |
| E:guiding:information | guiding | information | Coherent Orientation Briefing | 0 | NO_ITEMS | Documents together provide coherent orientation |
| E:guiding:knowledge | guiding | knowledge | Integrated Expert Command | 0 | NO_ITEMS | Expert knowledge adequately integrated in Guidance |
| E:guiding:wisdom | guiding | wisdom | Principled Foresight | 0 | NO_ITEMS | Foresight demonstrated in Guidance trade-offs and principles |
| E:applying:data | applying | data | Confirmed Operational Baseline | 1 | HAS_ITEMS | Baseline confirmation dependent on unproduced upstream deliverables |
| E:applying:information | applying | information | Reliable Status Notification | 0 | NO_ITEMS | Status notification mechanisms addressed in Step C7 |
| E:applying:knowledge | applying | knowledge | Validated Applied Mastery | 0 | NO_ITEMS | Applied mastery demonstrated through detailed procedure |
| E:applying:wisdom | applying | wisdom | Demonstrated Prudent Governance | 0 | NO_ITEMS | Prudent governance shown in trade-off recommendations |
| E:judging:data | judging | data | Conclusive Evidential Record | 1 | HAS_ITEMS | Evidential record format undefined |
| E:judging:information | judging | information | Coherent Adjudicative Account | 0 | NO_ITEMS | Adjudicative accounts addressed through verification records |
| E:judging:knowledge | judging | knowledge | Authoritative Analytical Command | 0 | NO_ITEMS | Analytical command demonstrated in requirements and verification |
| E:judging:wisdom | judging | wisdom | Principled Adjudicative Wisdom | 0 | NO_ITEMS | Adjudicative wisdom addressed through conflict table in Guidance |
| E:reviewing:data | reviewing | data | Full Provenance Record | 1 | HAS_ITEMS | Provenance chain incomplete for control point transfer |
| E:reviewing:information | reviewing | information | Contextualized Audit Report | 0 | NO_ITEMS | Audit reporting addressed through documentation package |
| E:reviewing:knowledge | reviewing | knowledge | Traceable Audit Mastery | 0 | NO_ITEMS | Audit mastery demonstrated through systematic verification |
| E:reviewing:wisdom | reviewing | wisdom | Holistic Audit Stewardship | 0 | NO_ITEMS | Stewardship addressed through handoff to as-built survey |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Multi | Datasheet | Establish authoritative reference point declaration: add geodetic datum, coordinate projection, and vertical datum to Datasheet and cross-reference in Specification REQ-008-03-01 | The Authoritative Reference Point lens confirms that the most fundamental data element for a construction survey -- the coordinate reference framework -- is absent from all four documents. This is distinct from B-001/B-003 in that it affects the authoritative standing of all spatial data in the deliverable. | Datasheet.md; Specification.md | Datasheet > Key Site Information; Specification > REQ-008-03-01 | -- | Surveyor / DEL-008-02 | TBD |
| E-002 | E:applying:data | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm status and expected availability of upstream inputs (DEL-008-02, IFC drawings from PKG-001 through PKG-007, construction schedule from PKG-019) | The Confirmed Operational Baseline lens reveals that all four upstream inputs in the Datasheet are listed as dependencies with no availability dates or status. The operational baseline cannot be confirmed until these are available. | Datasheet.md | Attributes > Upstream Inputs Required | -- | Design-Builder / Construction Manager | TBD |
| E-003 | E:judging:data | VerificationGap | Specification | Specification | Add requirement specifying the format and minimum content of field verification records (not just that they must exist) | The Conclusive Evidential Record lens reveals that while REQ-008-03-08 requires documentation and the Verification table requires record review, no requirement specifies what a valid field verification record must contain (e.g., date, surveyor name, instrument used, drawing reference, measured values, design values, pass/fail determination). | Specification.md | REQ-008-03-08; Verification table | -- | Surveyor / Design-Builder | TBD |
| E-004 | E:reviewing:data | VerificationGap | Specification | Specification | Add requirement for documented chain-of-custody for control point data transfer from DEL-008-02 to DEL-008-03, and from DEL-008-03 to DEL-008-04 | The Full Provenance Record lens reveals that while REQ-008-03-01 requires use of DEL-008-02 control points and Procedure Step D3 addresses handoff to DEL-008-04, neither specifies a formal chain-of-custody or provenance documentation requirement for the control data transfer itself. | Specification.md; Procedure.md | REQ-008-03-01; Step A1; Step D3 | -- | Surveyor | TBD |
