# Semantic Lensing Register: DEL-002-03 Structural Framing Plans

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-002_Structural Design/1_Working/DEL-002-03_Framing-Plans/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-002-03_Framing-Plans/_CONTEXT.md (## Description)
- _STATUS.md — DEL-002-03_Framing-Plans/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-002-03_Framing-Plans/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-002-03_Framing-Plans/Datasheet.md (## Identification, ## Attributes, ## Construction, ## References)
- Specification.md — DEL-002-03_Framing-Plans/Specification.md (## Scope, ## Requirements, ## Standards, ## Verification, ## Documentation)
- Guidance.md — DEL-002-03_Framing-Plans/Guidance.md (## Purpose, ## Principles, ## Considerations, ## Trade-offs, ## Conflict Table)
- Procedure.md — DEL-002-03_Framing-Plans/Procedure.md (## Purpose, ## Prerequisites, ## Steps, ## Verification, ## Records)
- _REFERENCES.md — DEL-002-03_Framing-Plans/_REFERENCES.md (## Applicable References)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 24
- By document:
  - Datasheet: 6
  - Specification: 8
  - Guidance: 3
  - Procedure: 3
  - Multi: 4
- By matrix:
  - A: 5  B: 4  C: 3  F: 3  D: 3  X: 3  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | NBC/ABC edition not pinned |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | P.Eng. stamp requirement clear; unit convention unresolved |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification gap on code edition |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Audit trail adequately addressed by Procedure V-07, V-08 |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Crane data procurement step lacks acceptance criteria |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps 1-6 in Procedure are sufficiently detailed |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Mezzanine design load TBD affects assessment |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Internal QA review step (5.1-5.3) present |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles adequately cover value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance addresses merit |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Cost/performance trade-offs documented |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Internal QA checklist noted in Procedure Records |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which edition of NBC/ABC governs design; pin to a specific edition year or state "edition adopted in Alberta at time of building permit application" | REQ-FP-14 references "current edition" but does not pin a specific code edition; this ambiguity could affect compliance determination if the code edition changes mid-project | Specification.md | ## Standards | — | Structural Engineer of Record | TBD |
| A-002 | A:normative:applying | TBD_Question | Multi | Specification | Record TBD: Confirm unit convention (metric vs. imperial) for the drawing set; REQ-FP-11 notes this is unconfirmed | REQ-FP-11 states units must be consistent but defers the decision; the drawing set cannot be produced without this decision | Specification.md | ## Requirements — REQ-FP-11 | — | Project team (Architect + Structural Engineer) | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification approach for REQ-FP-06 (mezzanine design live load stated on drawings) as a distinct check; currently grouped under REQ-FP-01 through REQ-FP-11 bulk check | REQ-FP-06 is a specific normative requirement (mezzanine live load shall be stated) but its verification is lumped with 10 other drawing content requirements in a single verification row | Specification.md | ## Verification — REQ-FP-01 through REQ-FP-11 | — | Specification.md author | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add acceptance criteria for crane data completeness (Step 1.3); specify minimum data items the Structural Engineer must receive before proceeding | Procedure Step 1.3 lists crane data items to collect but does not define what constitutes sufficient data to proceed to Step 2 | Procedure.md | ## Steps — Step 1.3 | — | Structural Engineer of Record | TBD |
| A-005 | A:operative:judging | TBD_Question | Datasheet | Datasheet | Record TBD: Mezzanine design live load value — required for performance assessment of mezzanine framing; Datasheet currently shows "TBD (structural calculation required)" | The mezzanine design load is a critical operative parameter that cannot be assessed until a numeric value is established; Guidance suggests minimum 4.8 kPa but this is an ASSUMPTION | Datasheet.md | ## Attributes — Structural Framing Elements — Mezzanine design load | — | Structural Engineer + County confirmation | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Snow/wind/seismic TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Service Pit dimension sourcing |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Crane manufacturer data absent |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Dimension unit ambiguity |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (OBJ-001, OBJ-003 linkage) present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequately provided in Guidance |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Document set provides comprehensive account |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging is coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Structural engineering fundamentals not within scope to evaluate |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | P.Eng. credential requirement addresses this |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Detailed structural knowledge outside document scope |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Technical understanding consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs provide adequate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off recommendations present |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view addressed via cross-deliverable references |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across Guidance and Specification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Snow load, wind load, and seismic zone values for site SW 14-44-21-W4 — these are essential facts required before structural design can proceed | Three essential design data values (snow, wind, seismic) are listed as TBD in the Datasheet; these are non-negotiable inputs for framing design | Datasheet.md | ## Attributes — Design Conditions | — | NBC climatic data tables + geotechnical report (DEL-008-01) | TBD |
| B-002 | B:data:sufficiency | Conflict | Multi | Guidance | Resolve Service Pit dimensions: R-04 shows "24'" and "100'" annotations near the SERVICE TRENCH label; Guidance notes 100 ft may refer to building depth not trench length | Service Pit width (24 ft) and length are used in Datasheet and Specification but CONF-FP-02 in Guidance flags that the 100 ft dimension may be building depth, not trench length; this data insufficiency propagates into framing design | Datasheet.md; Guidance.md | Datasheet ## Attributes — Service Pit; Guidance ## Conflict Table — CONF-FP-02 | Datasheet.md#Attributes (24 ft x 100 ft); Guidance.md#Conflict-Table (100 ft may be building depth) | County / Architect confirmation from R-04 | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add crane manufacturer data fields (wheel loads, wheel base, crane bridge span, crane weight) as TBD entries in Datasheet Attributes | Procedure Step 1.3 and Guidance Principle 2 identify crane manufacturer data as critical input, but the Datasheet does not enumerate the specific crane data fields needed; this gap makes the data record incomplete | Datasheet.md; Procedure.md | Datasheet ## Attributes — Structural Framing Elements; Procedure ## Steps — Step 1.3 | — | Crane supplier (SOW-0067) | TBD |
| B-004 | B:data:consistency | Normalization | Multi | Guidance | Standardize dimension units across documents; Datasheet uses imperial (ft), Specification REQ-FP-11 notes unit convention is TBD; establish a single unit convention and apply consistently | Dimensions appear in feet throughout Datasheet and Guidance, but Guidance Principle 3 uses metric (kPa); REQ-FP-11 acknowledges unit convention is unconfirmed; this inconsistency risks drift | Datasheet.md; Specification.md; Guidance.md | Datasheet ## Attributes; Specification ## Requirements — REQ-FP-11; Guidance ## Principles — Principle 3 | — | Project team decision | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Regulatory Command | 1 | HAS_ITEMS | ABC/Safety Codes cross-reference gap |
| C:normative:sufficiency | normative | sufficiency | Substantiated Prescriptive Proof | 0 | NO_ITEMS | Proof chain (REQ -> calc -> stamp) is adequately documented |
| C:normative:completeness | normative | completeness | Comprehensive Regulatory Coverage | 1 | HAS_ITEMS | Missing occupancy classification reference |
| C:normative:consistency | normative | consistency | Harmonized Conformance Standard | 0 | NO_ITEMS | Standards table is internally consistent |
| C:operative:necessity | operative | necessity | Indispensable Functional Gate | 1 | HAS_ITEMS | County approval gate lacks record format |
| C:operative:sufficiency | operative | sufficiency | Capable Validated Workflow | 0 | NO_ITEMS | Workflow steps are sufficiently detailed |
| C:operative:completeness | operative | completeness | Exhaustive Operational Coverage | 0 | NO_ITEMS | All operational steps from input through issuance covered |
| C:operative:consistency | operative | consistency | Dependable Uniform Method | 0 | NO_ITEMS | Method steps are consistent with verification checks |
| C:evaluative:necessity | evaluative | necessity | Inherent Requisite Value | 0 | NO_ITEMS | Value proposition clear in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Credible Warranted Appraisal | 0 | NO_ITEMS | Trade-offs table provides credible appraisal |
| C:evaluative:completeness | evaluative | completeness | Holistic Worth Assessment | 0 | NO_ITEMS | Worth assessment adequately covered |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add Alberta Safety Codes Act reference with specific applicability clause for industrial occupancies; REQ-FP-15 references "Alberta Safety Codes" without clause specificity | REQ-FP-15 mandates adherence to Alberta Safety Codes but provides no specific clause or section reference, making the enforceable regulatory command incomplete for verification | Specification.md | ## Requirements — REQ-FP-15 | — | Alberta Safety Codes Act + Structural Engineer | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add occupancy classification (Group F, Division 3 or similar per NBC) for the building; this classification affects load factors and fire resistance requirements that influence framing | The building occupancy classification is not stated in any production document; NBC structural requirements depend on occupancy classification, making regulatory coverage incomplete without it | Specification.md; Datasheet.md | Specification ## Standards; Datasheet ## Attributes — Design Conditions (entire section scanned) | — | Structural Engineer / Building Code consultant | TBD |
| C-003 | C:operative:necessity | RationaleGap | Procedure | Guidance | Add guidance on what form County preliminary approval must take (written letter, email, meeting minutes) and how it is recorded | Procedure Step 3.3 and Verification V-08 require County approval before IFC but neither document specifies the acceptable form of approval evidence; this makes the functional gate ambiguous | Procedure.md; Specification.md | Procedure ## Steps — Step 3.3; Specification ## Verification — REQ-FP-13 | — | County / project administration | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Compulsory Compliance Foundation | 1 | HAS_ITEMS | Foundation type TBD impact |
| F:normative:sufficiency | normative | sufficiency | Justified Regulatory Adherence | 0 | NO_ITEMS | Adherence pathway (calc + stamp + permit) documented |
| F:normative:completeness | normative | completeness | Total Mandate Fulfillment | 1 | HAS_ITEMS | REQ-FP-20 values all TBD |
| F:normative:consistency | normative | consistency | Coherent Regulatory Alignment | 0 | NO_ITEMS | Requirements consistently reference R-01 and R-04 |
| F:operative:necessity | operative | necessity | Vital Process Competence | 0 | NO_ITEMS | Prerequisites adequately defined |
| F:operative:sufficiency | operative | sufficiency | Proficient Operational Practice | 0 | NO_ITEMS | Steps detailed enough for proficient practitioner |
| F:operative:completeness | operative | completeness | Comprehensive Task Mastery | 0 | NO_ITEMS | Task coverage complete |
| F:operative:consistency | operative | consistency | Consistent Operational Discipline | 0 | NO_ITEMS | Steps and verification are aligned |
| F:evaluative:necessity | evaluative | necessity | Fundamental Merit Basis | 0 | NO_ITEMS | Merit basis established in Guidance |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Value Judgment | 1 | HAS_ITEMS | Hybrid system rationale weak |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Quality Account | 0 | NO_ITEMS | Quality checks in Procedure V-01 through V-11 |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Coherence | 0 | NO_ITEMS | Quality criteria consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Datasheet | Datasheet | Clarify foundation type dependency: state that framing plan column loads feed into DEL-002-02 and that foundation type (TBD) does not block framing plan production but does affect column base details | Datasheet lists foundation type as TBD pending geotech; the relationship between foundation type and framing plan is not explicit, creating ambiguity about whether DEL-002-03 can proceed before DEL-008-01 completes | Datasheet.md | ## Attributes — Design Conditions — Foundation type | — | Structural Engineer | TBD |
| F-002 | F:normative:completeness | VerificationGap | Specification | Specification | Add verification approach for REQ-FP-20 that specifies how NBC climatic data values will be confirmed (e.g., cross-check against NBC Appendix C for the specific location coordinates) | REQ-FP-20 verification says "Confirm design loads stated on drawings are consistent with NBC climatic data" but does not specify how consistency is checked when the values themselves are TBD | Specification.md | ## Verification — REQ-FP-20 | — | Structural Engineer of Record | TBD |
| F-003 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Expand rationale for when a hybrid concrete-steel system is preferable; add decision criteria (cost, schedule, fire rating, crane load path) that would make the case defensible for County approval | Guidance Trade-offs table mentions hybrid system possibility but the rationale is thin ("may be more cost-effective and faster"); a defensible value judgment requires clearer decision criteria since departure from RFP "concrete structure" language needs County buy-in | Guidance.md | ## Trade-offs — Concrete vs. steel framing | — | Structural Engineer | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Authoritative Mandate | 0 | NO_ITEMS | R-01 mandate clearly established |
| D:normative:applying | normative | applying | Resolved Compulsory Implementation | 1 | HAS_ITEMS | CSA standard applicability unresolved |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance determination pathway clear |
| D:normative:reviewing | normative | reviewing | Systematic Conformance Examination | 0 | NO_ITEMS | Verification table provides systematic examination |
| D:operative:guiding | operative | guiding | Established Workflow Governance | 0 | NO_ITEMS | Procedure establishes clear workflow |
| D:operative:applying | operative | applying | Resolved Skilled Execution | 0 | NO_ITEMS | Execution steps adequately detailed |
| D:operative:judging | operative | judging | Resolved Effectiveness Judgment | 1 | HAS_ITEMS | Cross-discipline coordination check lacks criteria |
| D:operative:reviewing | operative | reviewing | Confirmed Procedural Examination | 0 | NO_ITEMS | Internal QA review addresses this |
| D:evaluative:guiding | evaluative | guiding | Established Worth Priority | 0 | NO_ITEMS | OBJ-001 and OBJ-003 priorities clear |
| D:evaluative:applying | evaluative | applying | Resolved Quality Enactment | 0 | NO_ITEMS | Quality enactment through P.Eng. stamp |
| D:evaluative:judging | evaluative | judging | Definitive Merit Appraisal | 1 | HAS_ITEMS | No explicit quality metrics beyond checklist |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Worth Soundness | 0 | NO_ITEMS | Worth soundness confirmed by permit issuance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Specification | Specification | Resolve conditional applicability of CSA S16 and CSA A23.3: state which standard governs primary framing and which governs secondary elements, or state "to be confirmed upon structural system selection" | Standards table lists CSA S16 and CSA A23.3 both as "ASSUMPTION: applicable if..." — for resolved compulsory implementation, the governing design standard must be identified, not conditional | Specification.md | ## Standards | — | Structural Engineer of Record | TBD |
| D-002 | D:operative:judging | VerificationGap | Procedure | Procedure | Add pass/fail criteria for the cross-discipline coordination check (Step 5.2); specify what constitutes an acceptable outcome vs. a blocking conflict | Procedure Step 5.2 says "Perform a cross-discipline coordination check" and "Record any conflicts" but does not define criteria for judging effectiveness or when the check is complete | Procedure.md | ## Steps — Step 5.2 | — | Structural Engineer of Record | TBD |
| D-003 | D:evaluative:judging | MissingSlot | Specification | Specification | Add drawing quality metrics beyond the binary checklist (e.g., minimum annotation density, coordination completeness percentage, or reference to a drawing quality standard) | The Verification table in Specification is a binary pass/fail checklist; there is no merit appraisal framework that distinguishes a minimally acceptable drawing set from a high-quality one | Specification.md | ## Verification | — | Project quality management | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Cardinal Leadership Foundation | 0 | NO_ITEMS | Leadership basis (P.Eng. + County mandate) clear |
| X:guiding:sufficiency | guiding | sufficiency | Justified Governance Method | 0 | NO_ITEMS | Governance method (preliminary approval gate) justified |
| X:guiding:completeness | guiding | completeness | Comprehensive Governance Scope | 0 | NO_ITEMS | Governance scope covers design through IFC |
| X:guiding:consistency | guiding | consistency | Coherent Leadership Alignment | 0 | NO_ITEMS | Leadership alignment consistent across docs |
| X:applying:necessity | applying | necessity | Core Implementation Activation | 1 | HAS_ITEMS | Geotech report dependency unclear |
| X:applying:sufficiency | applying | sufficiency | Proficient Duty Demonstration | 0 | NO_ITEMS | Duty demonstration via P.Eng. stamp |
| X:applying:completeness | applying | completeness | Total Implementation Account | 1 | HAS_ITEMS | Drawing sheet count TBD |
| X:applying:consistency | applying | consistency | Unified Execution Measure | 0 | NO_ITEMS | Execution measures aligned |
| X:judging:necessity | judging | necessity | Foundational Verdict Basis | 0 | NO_ITEMS | Verdict basis (code compliance + calc package) present |
| X:judging:sufficiency | judging | sufficiency | Substantiated Assessment Finding | 0 | NO_ITEMS | Assessment linked to verification table |
| X:judging:completeness | judging | completeness | Exhaustive Verdict Record | 0 | NO_ITEMS | V-01 through V-11 provide exhaustive record |
| X:judging:consistency | judging | consistency | Stable Assessment Coherence | 0 | NO_ITEMS | Assessment criteria consistent |
| X:reviewing:necessity | reviewing | necessity | Foundational Verification Basis | 0 | NO_ITEMS | Verification basis established |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Verification Method | 1 | HAS_ITEMS | Verification methods mostly "drawing review" |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Record | 0 | NO_ITEMS | Records table in Procedure covers audit trail |
| X:reviewing:consistency | reviewing | consistency | Consistent Audit Alignment | 0 | NO_ITEMS | Audit alignment consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | RationaleGap | Procedure | Guidance | Add rationale for the sequencing dependency between DEL-008-01 (geotech) and DEL-002-03; clarify whether framing plan production can begin before geotech report is available or must wait | Procedure Prerequisites list geotech report as "Required before finalizing foundation/structural loads" but the framing plans (superstructure) may not require geotech for initial production; the dependency is stated but not explained | Procedure.md | ## Prerequisites — Information Inputs Required | — | Structural Engineer | TBD |
| X-002 | X:applying:completeness | VerificationGap | Specification | Specification | Add verification that the anticipated drawing sheet list (S-xx01 through S-xx04 plus General Notes) is accounted for in the IFC package; currently Documentation section lists sheets as "TBD at detailed design stage" with no completion check | The Documentation section lists anticipated sheets but the Verification section has no check confirming all anticipated sheets are produced; total implementation account cannot be verified | Specification.md | ## Documentation — Anticipated Artifacts; ## Verification | — | Structural Engineer of Record | TBD |
| X-003 | X:reviewing:sufficiency | Normalization | Specification | Specification | Differentiate verification methods: replace generic "Drawing review" with specific methods (e.g., "overlay comparison" for V-09, "NBC table lookup" for V-10, "stamp inspection" for V-07) | Eight of eleven verification rows use "Drawing review" as the method; for justified verification, the method should be specific enough that a reviewer knows what action to perform | Specification.md | ## Verification | — | Specification.md author | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Governance Record | 0 | NO_ITEMS | Governance records adequately specified |
| E:guiding:information | guiding | information | Coherent Governance Signal | 0 | NO_ITEMS | Governance signals clear |
| E:guiding:knowledge | guiding | knowledge | Integrated Leadership Mastery | 0 | NO_ITEMS | Leadership knowledge addressed by P.Eng. requirement |
| E:guiding:wisdom | guiding | wisdom | Principled Governance Foresight | 0 | NO_ITEMS | Foresight addressed in Guidance Principles |
| E:applying:data | applying | data | Evidenced Performance Record | 1 | HAS_ITEMS | Drawing transmittal record format undefined |
| E:applying:information | applying | information | Contextual Execution Account | 0 | NO_ITEMS | Execution context adequately described |
| E:applying:knowledge | applying | knowledge | Comprehensive Execution Mastery | 0 | NO_ITEMS | Execution knowledge addressed by credential requirements |
| E:applying:wisdom | applying | wisdom | Principled Execution Foresight | 0 | NO_ITEMS | Execution foresight addressed in Guidance considerations |
| E:judging:data | judging | data | Substantiated Verdict Record | 1 | HAS_ITEMS | Building dimension conflict unresolved |
| E:judging:information | judging | information | Coherent Verdict Account | 0 | NO_ITEMS | Verdict account coherent |
| E:judging:knowledge | judging | knowledge | Comprehensive Judgment Mastery | 0 | NO_ITEMS | Judgment mastery addressed by P.Eng. expertise |
| E:judging:wisdom | judging | wisdom | Principled Judgment Foresight | 0 | NO_ITEMS | Judgment foresight in Guidance trade-offs |
| E:reviewing:data | reviewing | data | Validated Inspection Record | 1 | HAS_ITEMS | Internal QA record format undefined |
| E:reviewing:information | reviewing | information | Coherent Verification Account | 0 | NO_ITEMS | Verification account coherent |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Verification Mastery | 0 | NO_ITEMS | Verification mastery addressed by engineer review |
| E:reviewing:wisdom | reviewing | wisdom | Principled Verification Foresight | 0 | NO_ITEMS | Verification foresight adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | Normalization | Procedure | Procedure | Define the format and required content of the drawing transmittal record (Record row "Drawing transmittal record"); specify minimum fields (date, recipient, drawing list, revision) | Procedure Records table lists "Drawing transmittal record" as a required record but does not define its format or required content fields; this makes the evidenced performance record non-standardized | Procedure.md | ## Records — Drawing transmittal record | — | Project administration | TBD |
| E-002 | E:judging:data | Conflict | Datasheet | Guidance | Resolve CONF-FP-01: Confirm whether 130 ft x 100 ft is the New North Shop addition only or includes the Old North Shop; this affects column grid geometry and all downstream framing | CONF-FP-01 in Guidance flags that the 130 ft dimension interpretation is ambiguous between R-01 and R-04; this conflict directly affects the foundational data for verdict on framing plan correctness | Datasheet.md; Guidance.md | Datasheet ## Attributes — Building Geometry; Guidance ## Conflict Table — CONF-FP-01 | Datasheet.md#Attributes (130 ft x 100 ft from R-04); Guidance.md#Conflict-Table (ambiguity with Old North Shop) | County / Architect confirmation | TBD |
| E-003 | E:reviewing:data | VerificationGap | Procedure | Procedure | Define the format and minimum content of the internal QA review record (currently noted as "ASSUMPTION: may be a QA checklist or internal review memo"); without a defined format, inspection record validation is not possible | Procedure Records lists "Internal QA review record" but qualifies it as an ASSUMPTION and does not specify whether it is a checklist, memo, or other format; a validated inspection record requires a defined format | Procedure.md | ## Records — Internal QA review record | — | Structural Engineer of Record / project QA | TBD |

---

*Semantic Lensing Register generated by CHIRALITY_LENS agent. Date: 2026-02-26.*
*No production documents were edited. All warranted items are enrichment-ready inputs for a subsequent enrichment pass.*
*All matrix cells from A, B, C, F, D, X, E have been processed as lenses (84 total cells; 24 warranted items recorded).*
